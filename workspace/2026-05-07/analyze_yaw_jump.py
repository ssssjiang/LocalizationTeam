#!/usr/bin/env python3
"""
analyze_yaw_jump.py

Compare 2~N TUM trajectories (e.g., baseline / low-speed-smooth / angle-keep-LIO)
focusing on yaw and position "jumps" derived from the trajectory itself —
no speed-based gating, no event windowing.

|Δyaw| is computed over a configurable time window  (default 0.2 s):
    Δyaw(t) = yaw(t) - yaw(t - W)
A short window (~0.2 s, ~1 LIO frame) suppresses single-step noise while
preserving step-like jumps; longer windows (>1 s) are dominated by real
turning motion and lose contrast.

Usage:
    python analyze_yaw_jump.py \
        -t baseline.tum  -n "Original" \
        -t smooth.tum    -n "LowSpeedSmooth" \
        -t newscheme.tum -n "AngKeepLIO" \
        -o ./out_yaw_jump \
        [--dyaw-window-s 0.2]

Inputs are TUM files: each line `time x y z qx qy qz qw`.
Comments (`#`) and blank lines are skipped.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator
from scipy.spatial.transform import Rotation as R, Slerp
from scipy.interpolate import interp1d


# ---------------------------------------------------------------- IO ----------
def load_tum(path: Path) -> np.ndarray:
    arr = np.loadtxt(str(path), comments="#")
    if arr.ndim != 2 or arr.shape[1] != 8:
        raise ValueError(
            f"{path}: TUM expects 8 columns (t x y z qx qy qz qw), got shape {arr.shape}"
        )
    arr = arr[np.argsort(arr[:, 0])]
    keep = np.concatenate([[True], np.diff(arr[:, 0]) > 1e-9])
    arr = arr[keep]
    return arr


# ------------------------------------------------------ time alignment --------
def align_to_grid(traj: np.ndarray, t_grid: np.ndarray):
    """Interpolate `traj` onto `t_grid`. Returns resampled array (N,8)."""
    t = traj[:, 0]
    in_range = (t_grid >= t[0]) & (t_grid <= t[-1])
    tg = t_grid[in_range]

    pos = interp1d(t, traj[:, 1:4], axis=0, kind="linear")(tg)

    rots = R.from_quat(traj[:, 4:8])  # scipy expects (x,y,z,w)
    slerp = Slerp(t, rots)
    quat = slerp(tg).as_quat()

    return np.column_stack([tg, pos, quat])


def make_common_grid(trajs, freq_hz=None) -> np.ndarray:
    t_min = max(tr[0, 0] for tr in trajs)
    t_max = min(tr[-1, 0] for tr in trajs)
    if t_max <= t_min:
        raise ValueError("No time overlap between trajectories.")
    if freq_hz is None:
        dt = float(np.median(np.diff(trajs[0][:, 0])))
    else:
        dt = 1.0 / float(freq_hz)
    return np.arange(t_min, t_max + dt / 2.0, dt)


# ------------------------------------------------------------- math -----------
def yaw_unwrap(quat: np.ndarray) -> np.ndarray:
    """quat (N,4) xyzw -> unwrapped yaw (rad), using ZYX intrinsic Euler."""
    eul = R.from_quat(quat).as_euler("zyx", degrees=False)
    return np.unwrap(eul[:, 0])


def angle_diff_wrap(a: np.ndarray) -> np.ndarray:
    d = np.diff(a)
    return (d + np.pi) % (2 * np.pi) - np.pi


# ---------------------------------------------------------- metrics -----------
def dyaw_window(t: np.ndarray, yaw: np.ndarray, window_s: float) -> np.ndarray:
    """Windowed yaw difference: out[i] = yaw[i] - yaw[i-N], N = round(window_s/dt).
    First N entries are NaN. yaw is assumed already unwrapped (no wrap needed)."""
    if len(yaw) < 2:
        return np.full(len(yaw), np.nan)
    dt = float(np.median(np.diff(t)))
    N = max(1, int(round(window_s / dt)))
    out = np.full(len(yaw), np.nan)
    if N < len(yaw):
        out[N:] = yaw[N:] - yaw[:-N]
    return out


def per_step_quantities(t, xyz, yaw):
    """Single-step (adjacent-sample) quantities, used for fine-grained stats."""
    dt = np.diff(t)
    dt_safe = np.maximum(dt, 1e-9)
    dyaw_step = angle_diff_wrap(yaw)                            # rad / step
    dpos = np.linalg.norm(np.diff(xyz[:, :2], axis=0), axis=1)  # m / step
    yaw_rate = dyaw_step / dt_safe                              # rad/s
    yaw_acc = np.diff(yaw_rate) / np.maximum(dt[1:], 1e-9)      # rad/s^2
    pos_acc = np.diff(dpos / dt_safe) / np.maximum(dt[1:], 1e-9)
    return dpos, yaw_rate, yaw_acc, pos_acc


def summarize(name, t, dyaw_win, win_s, dpos, yaw_rate, yaw_acc, pos_acc):
    dy = dyaw_win[~np.isnan(dyaw_win)]
    return {
        "name": name,
        "n_samples": len(t),
        "duration_s": float(t[-1] - t[0]),
        f"|dyaw|@{win_s}s_max [deg]": float(np.degrees(np.max(np.abs(dy)))),
        f"|dyaw|@{win_s}s_p99 [deg]": float(np.degrees(np.percentile(np.abs(dy), 99))),
        f"|dyaw|@{win_s}s_rms [deg]": float(np.degrees(np.sqrt(np.mean(dy ** 2)))),
        "yaw_rate_max [deg/s]": float(np.degrees(np.max(np.abs(yaw_rate)))),
        "yaw_acc_max [deg/s2]": float(np.degrees(np.max(np.abs(yaw_acc)))),
        "|dpos|_max [m]": float(np.max(dpos)),
        "|dpos|_p99 [m]": float(np.percentile(dpos, 99)),
        "|dpos|_rms [m]": float(np.sqrt(np.mean(dpos ** 2))),
        "pos_acc_max [m/s2]": float(np.max(np.abs(pos_acc))),
    }


# ------------------------------------------------------------ plotting --------
def _grid_with_minor(ax, log_y=False):
    """Major solid + minor dashed grid; finer y ticks."""
    ax.minorticks_on()
    if log_y:
        ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
    else:
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.grid(which="major", linestyle="-", alpha=0.45)
    ax.grid(which="minor", linestyle="--", alpha=0.25)


def _annotate_peak(ax, t, y, name, color, log_y=False, dy_offset=8):
    """Mark argmax(|y|) and label with the peak value."""
    arr = np.asarray(y, dtype=float)
    valid = np.isfinite(arr)
    if not valid.any():
        return
    abs_arr = np.where(valid, np.abs(arr), -np.inf)
    idx = int(np.argmax(abs_arr))
    yv = float(arr[idx])
    tv = float(np.asarray(t)[idx])
    ax.scatter([tv], [yv], color=color, s=28, zorder=5,
               edgecolors="black", linewidths=0.6)
    ax.annotate(f"{name}: {yv:.3g}",
                xy=(tv, yv),
                xytext=(6, dy_offset),
                textcoords="offset points",
                fontsize=8, color=color, zorder=6,
                bbox=dict(boxstyle="round,pad=0.15",
                          fc="white", ec=color, alpha=0.85, lw=0.5))


def plot_overview(out_dir: Path, names, datas, win_s):
    fig, axes = plt.subplots(3, 1, figsize=(14, 11), sharex=True)

    # ----- yaw (no peak annotation: peaks are usually start/end angles, not informative) -----
    for n, (t, _, yaw) in zip(names, datas):
        axes[0].plot(t, np.degrees(yaw), label=n, lw=1)
    axes[0].set_ylabel("yaw [deg]")
    axes[0].legend(loc="best")
    _grid_with_minor(axes[0])

    offsets = (10, -14, 22)  # text-offset stagger when labels overlap

    # ----- |Δyaw|@Ws -----
    dy_max_global = 0.0
    for k, (n, (t, _, yaw)) in enumerate(zip(names, datas)):
        d = np.degrees(np.abs(dyaw_window(t, yaw, win_s)))
        line, = axes[1].plot(t, d, label=n, lw=0.9)
        finite = d[np.isfinite(d)]
        if finite.size:
            dy_max_global = max(dy_max_global, float(finite.max()))
        _annotate_peak(axes[1], t, d, n, line.get_color(), log_y=True,
                       dy_offset=offsets[k % len(offsets)])
    axes[1].set_ylabel(f"|Δyaw|@{win_s}s [deg]")
    axes[1].set_yscale("log")
    if dy_max_global > 0:
        axes[1].set_ylim(max(1e-3, dy_max_global * 1e-4), dy_max_global * 3.0)
    _grid_with_minor(axes[1], log_y=True)
    axes[1].legend(loc="best")

    # ----- |Δpos| per step -----
    dp_max_global = 0.0
    for k, (n, (t, xyz, _)) in enumerate(zip(names, datas)):
        dpos = np.linalg.norm(np.diff(xyz[:, :2], axis=0), axis=1)
        line, = axes[2].plot(t[1:], dpos, label=n, lw=0.8)
        if dpos.size:
            dp_max_global = max(dp_max_global, float(dpos.max()))
        _annotate_peak(axes[2], t[1:], dpos, n, line.get_color(), log_y=True,
                       dy_offset=offsets[k % len(offsets)])
    axes[2].set_ylabel("|Δpos| per step [m]")
    axes[2].set_yscale("log")
    if dp_max_global > 0:
        axes[2].set_ylim(max(1e-5, dp_max_global * 1e-3), dp_max_global * 3.0)
    axes[2].set_xlabel("time [s]")
    _grid_with_minor(axes[2], log_y=True)
    axes[2].legend(loc="best")

    fig.tight_layout()
    fig.savefig(out_dir / "overview.png", dpi=150)
    plt.close(fig)


def plot_xy(out_dir: Path, names, datas):
    fig, ax = plt.subplots(figsize=(8, 8))
    for n, (t, xyz, _) in zip(names, datas):
        line, = ax.plot(xyz[:, 0], xyz[:, 1], label=n, lw=1)
        ax.scatter([xyz[0, 0]], [xyz[0, 1]], marker="o", s=30,
                   color=line.get_color(), edgecolors="black", linewidths=0.5)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("XY trajectories")
    ax.legend()
    _grid_with_minor(ax)
    fig.tight_layout()
    fig.savefig(out_dir / "xy.png", dpi=150)
    plt.close(fig)


def plot_dyaw_hist(out_dir: Path, names, datas, win_s):
    fig, ax = plt.subplots(figsize=(10, 5))
    bins = np.logspace(-3, 2.5, 80)  # 0.001~316 deg
    peaks = []
    for n, (t, _, yaw) in zip(names, datas):
        d = np.degrees(np.abs(dyaw_window(t, yaw, win_s)))
        d = d[np.isfinite(d) & (d > 0)]
        line_artists = ax.hist(d, bins=bins, histtype="step", label=n, lw=1.3)
        color = line_artists[2][0].get_edgecolor()
        peaks.append((n, float(d.max()) if d.size else float("nan"), color))
    ax.set_xscale("log")
    ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.set_xlabel(f"|Δyaw|@{win_s}s [deg]")
    ax.set_ylabel("count")
    ax.set_title(f"|Δyaw|@{win_s}s distribution (log scale)")
    ax.grid(which="major", linestyle="-", alpha=0.45)
    ax.grid(which="minor", linestyle="--", alpha=0.25)

    y_top = ax.get_ylim()[1]
    for k, (n, peak, color) in enumerate(peaks):
        if not np.isfinite(peak):
            continue
        ax.axvline(peak, color=color, ls=":", lw=1.0, alpha=0.8)
        ax.annotate(f"{n} max: {peak:.3g}",
                    xy=(peak, y_top * (0.92 - 0.08 * k)),
                    xytext=(4, 0), textcoords="offset points",
                    fontsize=8, color=color,
                    bbox=dict(boxstyle="round,pad=0.15",
                              fc="white", ec=color, alpha=0.85, lw=0.5))
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "dyaw_hist.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------- main --------
def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-t", "--traj", action="append", required=True,
                        help="TUM file path. Use multiple times for multiple trajs.")
    parser.add_argument("-n", "--name", action="append", required=True,
                        help="Display name for each --traj (same order, same count).")
    parser.add_argument("-o", "--out-dir", default="./out_yaw_jump")
    parser.add_argument("--freq-hz", type=float, default=None,
                        help="Resample rate (default: median of first traj)")
    parser.add_argument("--dyaw-window-s", type=float, default=0.2,
                        help="Window for Δyaw = yaw(t) - yaw(t-W), seconds (default: 0.2)")
    args = parser.parse_args()

    if len(args.traj) != len(args.name):
        sys.exit("ERROR: --traj and --name count mismatch.")
    if len(args.traj) < 2:
        sys.exit("ERROR: need at least 2 trajectories to compare.")

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] loading {len(args.traj)} TUM files...")
    raw_trajs = []
    for p, n in zip(args.traj, args.name):
        tr = load_tum(Path(p))
        print(f"    {n:30s} {tr.shape[0]:6d} samples,  "
              f"{tr[0, 0]:.3f} ~ {tr[-1, 0]:.3f}s  ({Path(p).name})")
        raw_trajs.append(tr)

    grid = make_common_grid(raw_trajs, freq_hz=args.freq_hz)
    print(f"[*] common grid: {grid[0]:.3f} ~ {grid[-1]:.3f}s, "
          f"N={len(grid)}, dt={np.mean(np.diff(grid))*1000:.1f} ms")

    datas = []   # list of (t, xyz, yaw_unwrapped)
    for tr in raw_trajs:
        a = align_to_grid(tr, grid)
        t = a[:, 0]
        xyz = a[:, 1:4]
        yaw = yaw_unwrap(a[:, 4:8])
        datas.append((t, xyz, yaw))

    win_s = float(args.dyaw_window_s)
    print(f"[*] computing global metrics  (Δyaw window = {win_s}s) ...")
    summary_rows = []
    for n, (t, xyz, yaw) in zip(args.name, datas):
        dpos, yr, ya, pa = per_step_quantities(t, xyz, yaw)
        dyaw_win = dyaw_window(t, yaw, win_s)
        summary_rows.append(summarize(n, t, dyaw_win, win_s, dpos, yr, ya, pa))
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(out_dir / "summary.csv", index=False)
    print(summary_df.to_string(index=False))

    print("\n[*] generating plots...")
    plot_overview(out_dir, args.name, datas, win_s)
    plot_xy(out_dir, args.name, datas)
    plot_dyaw_hist(out_dir, args.name, datas, win_s)

    print(f"\n[OK] outputs in {out_dir}")
    print("     summary.csv, overview.png, xy.png, dyaw_hist.png")


if __name__ == "__main__":
    main()
