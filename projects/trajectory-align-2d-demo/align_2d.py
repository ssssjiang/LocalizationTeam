#!/usr/bin/env python3
"""
2D trajectory alignment demo (3DoF: x, y, yaw; scale = 1).

- Reference: RTK (timestamps are the anchor; XY only, RTK z is noisy).
- Source:    VSLAM PGO trajectory, resampled onto RTK timestamps.
- Method:    closed-form 2D rigid alignment (Umeyama 2D, R + t).
- Segments:  align over the first L meters of arclength (e.g. 1, 2, 5, 7).
- Output:    overlay plot + per-segment metrics (RMSE / drift / theta).

Input TUM format: `t x y z qx qy qz qw` (whitespace-separated).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np


# ----------------------------- I/O -----------------------------------------

@dataclass
class Traj:
    t: np.ndarray       # (N,) seconds, monotonically increasing
    xy: np.ndarray      # (N, 2)
    yaw: np.ndarray     # (N,) radians


def load_tum(path: Path) -> Traj:
    data = np.loadtxt(path, comments="#")
    if data.ndim != 2 or data.shape[1] < 3:
        raise ValueError(f"{path}: expected TUM-like format, got shape {data.shape}")
    t = data[:, 0]
    xy = data[:, 1:3]
    if data.shape[1] >= 8:
        qx, qy, qz, qw = data[:, 4], data[:, 5], data[:, 6], data[:, 7]
        yaw = _quat_to_yaw(qx, qy, qz, qw)
    else:
        yaw = np.zeros_like(t)
    order = np.argsort(t)
    return Traj(t[order], xy[order], yaw[order])


def _quat_to_yaw(qx, qy, qz, qw):
    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    return np.arctan2(siny_cosp, cosy_cosp)


# ----------------------- Time-axis interpolation ---------------------------

def resample_to(src: Traj, t_query: np.ndarray) -> tuple[Traj, np.ndarray]:
    """Resample src at t_query (no extrapolation).

    Returns (resampled, mask). The caller MUST apply `mask` to the reference
    trajectory too, so the two arrays stay index-aligned.
    """
    in_range = (t_query >= src.t[0]) & (t_query <= src.t[-1])
    tq = t_query[in_range]
    x = np.interp(tq, src.t, src.xy[:, 0])
    y = np.interp(tq, src.t, src.xy[:, 1])
    # Unwrap before linear interp to avoid ±pi jumps; wrap result back.
    yaw_q = np.interp(tq, src.t, np.unwrap(src.yaw))
    yaw_q = (yaw_q + np.pi) % (2 * np.pi) - np.pi
    return Traj(tq, np.column_stack([x, y]), yaw_q), in_range


# --------------------- 3DoF closed-form alignment --------------------------

@dataclass
class SE2:
    theta: float
    t: np.ndarray       # (2,)

    @property
    def R(self) -> np.ndarray:
        c, s = np.cos(self.theta), np.sin(self.theta)
        return np.array([[c, -s], [s, c]])

    def apply(self, xy: np.ndarray) -> np.ndarray:
        return xy @ self.R.T + self.t


def align_2d(src_xy: np.ndarray, dst_xy: np.ndarray) -> SE2:
    """Closed-form 2D rigid alignment (scale fixed to 1).

    Solve  min_{R in SO(2), t in R^2}  sum_i || R src_i + t - dst_i ||^2.

    Derivation (2D specialization of Umeyama):
        Let a_i = src_i - mean(src), b_i = dst_i - mean(dst), and
        H = sum_i a_i b_i^T (2x2). With R = [[c,-s],[s,c]],
            tr(R H) = c * (H00 + H11) + s * (H01 - H10)
                    = c * sum(a . b) + s * sum(a x b).
        Maximizing on the unit circle yields
            theta = atan2( sum(a_x b_y - a_y b_x),
                           sum(a_x b_x + a_y b_y) ).
        Translation falls out of the centroid constraint.

    Observability:
        Theta is observable as long as not BOTH sums vanish. A pure straight
        segment is fine: both cross and dot grow with segment length and
        atan2 still picks the right quadrant. Degeneracy only happens when
        src collapses to a single point (zero baseline).
    """
    assert src_xy.shape == dst_xy.shape and src_xy.shape[1] == 2
    if src_xy.shape[0] < 2:
        raise ValueError("alignment needs >= 2 point pairs")

    mu_s = src_xy.mean(axis=0)
    mu_d = dst_xy.mean(axis=0)
    a = src_xy - mu_s
    b = dst_xy - mu_d

    cross = float(np.sum(a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]))
    dot = float(np.sum(a[:, 0] * b[:, 0] + a[:, 1] * b[:, 1]))
    if abs(cross) + abs(dot) < 1e-12:
        raise ValueError("degenerate alignment: source baseline is zero")

    theta = np.arctan2(cross, dot)
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    return SE2(theta=theta, t=mu_d - R @ mu_s)


# -------------------- Segment selection / metrics --------------------------

def cum_arclen(xy: np.ndarray) -> np.ndarray:
    seg = np.linalg.norm(np.diff(xy, axis=0), axis=1)
    return np.concatenate([[0.0], np.cumsum(seg)])


def first_meters_mask(xy: np.ndarray, length: float) -> np.ndarray:
    return cum_arclen(xy) <= length


# ----------------------------- Main demo -----------------------------------

def run(rtk_path: Path, slam_path: Path, segments: Sequence[float], out_path: Path):
    rtk = load_tum(rtk_path)
    slam = load_tum(slam_path)

    slam_rs, mask = resample_to(slam, rtk.t)
    rtk_ov = Traj(rtk.t[mask], rtk.xy[mask], rtk.yaw[mask])
    if rtk_ov.xy.shape[0] < 2:
        raise RuntimeError("no time overlap between RTK and VSLAM")

    n_seg = len(segments)
    fig, axes = plt.subplots(1, n_seg + 1, figsize=(5 * (n_seg + 1), 5))
    if n_seg + 1 == 1:
        axes = [axes]

    hdr = f"{'L[m]':>6} {'N':>6} {'RMSE_xy[m]':>12} {'drift[m]':>12} {'theta[deg]':>12}"
    print(hdr)
    print("-" * len(hdr))

    s_all = cum_arclen(rtk_ov.xy)

    for ax, L in zip(axes[:-1], segments):
        seg = first_meters_mask(rtk_ov.xy, L)
        if seg.sum() < 2:
            print(f"{L:>6.1f} {int(seg.sum()):>6}   (insufficient samples)")
            continue
        T = align_2d(slam_rs.xy[seg], rtk_ov.xy[seg])
        aligned = T.apply(slam_rs.xy)

        err_seg = np.linalg.norm(aligned[seg] - rtk_ov.xy[seg], axis=1)
        rmse = float(np.sqrt(np.mean(err_seg ** 2)))
        drift = float(np.linalg.norm(aligned[-1] - rtk_ov.xy[-1]))

        print(f"{L:>6.1f} {int(seg.sum()):>6} {rmse:>12.4f} {drift:>12.4f} "
              f"{np.degrees(T.theta):>12.3f}")

        ax.plot(rtk_ov.xy[:, 0], rtk_ov.xy[:, 1], "k-", lw=1.5, label="RTK")
        ax.plot(aligned[:, 0], aligned[:, 1], "r--", lw=1.2, label="VSLAM aligned")
        ax.plot(rtk_ov.xy[seg, 0], rtk_ov.xy[seg, 1], "g", lw=4, alpha=0.35,
                label=f"align span {L} m")
        ax.set_aspect("equal", "datalim")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, loc="best")
        ax.set_title(f"L = {L} m\nRMSE = {rmse:.3f} m,  drift = {drift:.3f} m")

    ax = axes[-1]
    for L in segments:
        seg = first_meters_mask(rtk_ov.xy, L)
        if seg.sum() < 2:
            continue
        T = align_2d(slam_rs.xy[seg], rtk_ov.xy[seg])
        aligned = T.apply(slam_rs.xy)
        err = np.linalg.norm(aligned - rtk_ov.xy, axis=1)
        ax.plot(s_all, err, label=f"L = {L} m")
    ax.set_xlabel("RTK arclength [m]")
    ax.set_ylabel("|aligned - RTK| [m]")
    ax.set_title("pointwise error vs distance from start")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    print(f"saved figure -> {out_path}")


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--rtk", required=True, type=Path, help="RTK trajectory (TUM)")
    p.add_argument("--slam", required=True, type=Path, help="VSLAM PGO trajectory (TUM)")
    p.add_argument("--segments", type=float, nargs="+",
                   default=[1.0, 2.0, 5.0, 7.0],
                   help="alignment lengths in meters (default: 1 2 5 7)")
    p.add_argument("--out", type=Path, default=Path("align_2d.png"))
    args = p.parse_args()
    run(args.rtk, args.slam, args.segments, args.out)


if __name__ == "__main__":
    main()
