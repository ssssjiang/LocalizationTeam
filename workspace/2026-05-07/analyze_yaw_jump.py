#!/usr/bin/env python3
"""
analyze_yaw_jump.py

Compare 2~N TUM trajectories focusing on yaw and xy-position "jumps".
No speed computation, no event detection — just overview + XY + |Δyaw| histogram.

Usage example:
    python analyze_yaw_jump.py \
        -t baseline.tum  -n "Original" \
        -t smooth.tum    -n "LowSpeedSmooth" \
        -t newscheme.tum -n "AngKeepLIO" \
        -o ./out_yaw_jump

Optional flags:
    --freq-hz 50          # resample rate for common grid (default: median of first)
    --dyaw-floor-deg 0.001  # lower clip for |Δyaw| log-axis
    --dpos-floor-m 1e-4   # lower clip for |Δpos| log-axis

Inputs are TUM files: each line `time x y z qx qy qz qw`.
Comments (`#`) and blank lines are skipped.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    t = traj[:, 0]
    in_range = (t_grid >= t[0]) & (t_grid <= t[-1])
    tg = t_grid[in_range]

    pos = interp1d(t, traj[:, 1:4], axis=0, kind="linear")(tg)

    rots = R.from_quat(traj[:, 4:8])  # scipy expects (x,y,z,w)
    slerp = Slerp(t, rots)
    quat = slerp(tg).as_quat()

    return np.column_stack([tg, pos, quat]), in_range


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
def per_step_quantities(xyz, yaw):
    dyaw = angle_diff_wrap(yaw)                                  # rad / step
    dpos = np.linalg.norm(np.diff(xyz[:, :2], axis=0), axis=1)   # m / step
    return dyaw, dpos


def summarize(name, t, dyaw, dpos):
    return {
        "name": name,
        "n_samples": len(t),
        "duration_s": float(t[-1] - t[0]),
        "|dyaw|_max [deg]": float(np.degrees(np.max(np.abs(dyaw)))),
        "|dyaw|_p99 [deg]": float(np.degrees(np.percentile(np.abs(dyaw), 99))),
        "|dyaw|_p95 [deg]": float(np.degrees(np.percentile(np.abs(dyaw), 95))),
        "|dyaw|_rms [deg]": float(np.degrees(np.sqrt(np.mean(dyaw ** 2)))),
        "|dpos|_max [m]": float(np.max(dpos)),
        "|dpos|_p99 [m]": float(np.percentile(dpos, 99)),
        "|dpos|_p95 [m]": float(np.percentile(dpos, 95)),
        "|dpos|_rms [m]": float(np.sqrt(np.mean(dpos ** 2))),
    }


# ------------------------------------------------------------ plotting --------
def plot_overview(out_dir: Path, names, datas, dyaw_floor_deg, dpos_floor_m):
    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

    for n, (t, _, yaw) in zip(names, datas):
        axes[0].plot(t, np.degrees(yaw), label=n, lw=1)
    axes[0].set_ylabel("yaw [deg]")
    axes[0].legend(loc="best")
    axes[0].grid(alpha=0.3)

    for n, (t, _, yaw) in zip(names, datas):
        d = np.degrees(np.abs(angle_diff_wrap(yaw)))
        axes[1].plot(t[1:], d, label=n, lw=0.8)
    axes[1].set_ylabel("|Δyaw| per step [deg]")
    axes[1].set_yscale("symlog", linthresh=dyaw_floor_deg)
    axes[1].grid(alpha=0.3)
    axes[1].legend(loc="best")

    for n, (t, xyz, _) in zip(names, datas):
        dpos = np.linalg.norm(np.diff(xyz[:, :2], axis=0), axis=1)
        axes[2].plot(t[1:], dpos, label=n, lw=0.8)
    axes[2].set_ylabel("|Δpos| per step [m]")
    axes[2].set_yscale("symlog", linthresh=dpos_floor_m)
    axes[2].set_xlabel("time [s]")
    axes[2].grid(alpha=0.3)
    axes[2].legend(loc="best")

    fig.tight_layout()
    fig.savefig(out_dir / "overview.png", dpi=150)
    plt.close(fig)


def plot_xy(out_dir: Path, names, datas):
    fig, ax = plt.subplots(figsize=(8, 8))
    for n, (t, xyz, _) in zip(names, datas):
        ax.plot(xyz[:, 0], xyz[:, 1], label=n, lw=1)
        ax.scatter([xyz[0, 0]], [xyz[0, 1]], marker="o", s=30)
    ax.set_aspect("equal")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("XY trajectories")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "xy.png", dpi=150)
    plt.close(fig)


def plot_dyaw_hist(out_dir: Path, names, datas):
    fig, ax = plt.subplots(figsize=(10, 5))
    bins = np.logspace(-3, 1, 80)  # 0.001~10 deg
    for n, (t, _, yaw) in zip(names, datas):
        d = np.degrees(np.abs(angle_diff_wrap(yaw)))
        d = d[d > 0]
        ax.hist(d, bins=bins, histtype="step", label=n, lw=1.2)
    ax.set_xscale("log")
    ax.set_xlabel("|Δyaw| per step [deg]")
    ax.set_ylabel("count")
    ax.set_title("|Δyaw| distribution (log scale)")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "dyaw_hist.png", dpi=150)
    plt.close(fig)


def plot_dpos_hist(out_dir: Path, names, datas):
    fig, ax = plt.subplots(figsize=(10, 5))
    bins = np.logspace(-5, 0, 80)  # 1e-5 ~ 1 m
    for n, (t, xyz, _) in zip(names, datas):
        d = np.linalg.norm(np.diff(xyz[:, :2], axis=0), axis=1)
        d = d[d > 0]
        ax.hist(d, bins=bins, histtype="step", label=n, lw=1.2)
    ax.set_xscale("log")
    ax.set_xlabel("|Δpos| per step [m]")
    ax.set_ylabel("count")
    ax.set_title("|Δpos| distribution (log scale)")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "dpos_hist.png", dpi=150)
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
    parser.add_argument("--freq-hz", type=float, default=None)
    parser.add_argument("--dyaw-floor-deg", type=float, default=0.001,
                        help="Lower clip for |Δyaw| log-axis")
    parser.add_argument("--dpos-floor-m", type=float, default=1e-4,
                        help="Lower clip for |Δpos| log-axis")
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

    datas = []  # list of (t, xyz, yaw_unwrapped)
    for tr in raw_trajs:
        a, _ = align_to_grid(tr, grid)
        t = a[:, 0]
        xyz = a[:, 1:4]
        quat = a[:, 4:8]
        yaw = yaw_unwrap(quat)
        datas.append((t, xyz, yaw))

    print("[*] computing global metrics...")
    summary_rows = []
    for n, (t, xyz, yaw) in zip(args.name, datas):
        dyaw, dpos = per_step_quantities(xyz, yaw)
        summary_rows.append(summarize(n, t, dyaw, dpos))
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(out_dir / "summary.csv", index=False)
    print(summary_df.to_string(index=False))

    print("\n[*] generating plots...")
    plot_overview(out_dir, args.name, datas,
                  args.dyaw_floor_deg, args.dpos_floor_m)
    plot_xy(out_dir, args.name, datas)
    plot_dyaw_hist(out_dir, args.name, datas)
    plot_dpos_hist(out_dir, args.name, datas)

    print(f"\n[OK] outputs in {out_dir}")
    print("     summary.csv, overview.png, xy.png, dyaw_hist.png, dpos_hist.png")


if __name__ == "__main__":
    main()
