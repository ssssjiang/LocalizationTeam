#!/usr/bin/env python3
"""
synth_u_turn.py

Synthesize a hairpin / U-turn trajectory (mimicking MMT-station scenario)
in TUM format, with three behavioral variants for the fusion module:

  A_original           - no low-speed reweighting; LIO-driven yaw can be
                         slightly noisy during low-speed turning.
  B_lowspeedsmooth     - low-speed downweights LIO entirely; yaw lags GT
                         during the U-turn, then jumps ~4° when speed
                         crosses 0.2 m/s upward (the bug we want to repro).
  C_angkeep_lio        - low-speed downweights ONLY position; yaw keeps
                         tracking LIO. No yaw jump at speed crossing,
                         small position drift during low-speed (accepted).

Geometry (close to image: hairpin/U with short straights):
  straight 1 (yaw=0)  -> decel -> 180° arc -> accel -> straight 2 (yaw=pi)
"""
import argparse
from pathlib import Path

import numpy as np
from scipy.spatial.transform import Rotation as R


def build_speed_profile(t):
    """Speed profile in m/s. Stays < 0.2 during the U-turn."""
    s = np.zeros_like(t)
    # 0~5s : straight at 0.6
    # 5~7s : decel 0.6 -> 0.1
    # 7~17s: U-turn at 0.1 (10s low speed)
    # 17~19s: accel 0.1 -> 0.6
    # 19~30s: straight at 0.6
    for i, ti in enumerate(t):
        if ti <= 5.0:
            s[i] = 0.6
        elif ti <= 7.0:
            s[i] = 0.6 - (ti - 5.0) / 2.0 * 0.5  # 0.6 -> 0.1
        elif ti <= 17.0:
            s[i] = 0.1
        elif ti <= 19.0:
            s[i] = 0.1 + (ti - 17.0) / 2.0 * 0.5  # 0.1 -> 0.6
        else:
            s[i] = 0.6
    return s


def build_yaw_profile(t):
    """Ground-truth yaw [rad]: 0 -> pi linearly during 7~17s."""
    yaw = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti <= 7.0:
            yaw[i] = 0.0
        elif ti <= 17.0:
            yaw[i] = (ti - 7.0) / 10.0 * np.pi
        else:
            yaw[i] = np.pi
    return yaw


def integrate_xy(speed, yaw, dt):
    """Integrate (vx, vy) along yaw direction."""
    vx = speed * np.cos(yaw)
    vy = speed * np.sin(yaw)
    x = np.cumsum(vx) * dt
    y = np.cumsum(vy) * dt
    return x, y


def write_tum(path: Path, t, x, y, yaw, z=None):
    if z is None:
        z = np.zeros_like(x)
    rots = R.from_euler("z", yaw.reshape(-1, 1))
    q = rots.as_quat()  # x y z w
    arr = np.column_stack([t, x, y, z, q])
    np.savetxt(str(path), arr, fmt="%.6f")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-o", "--out-dir", default="./synth_data",
                        help="Output directory for the three TUM files")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--jump-deg", type=float, default=4.0,
                        help="Magnitude of yaw jump at speed crossing in scheme B (deg)")
    parser.add_argument("--lowspeed-yaw-noise-deg", type=float, default=0.5,
                        help="Yaw 1-sigma noise during low-speed in scheme A (deg)")
    parser.add_argument("--lowspeed-pos-drift-m", type=float, default=0.05,
                        help="Lateral position drift accumulated during low-speed in scheme C (m)")
    args = parser.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)

    dt = 0.02
    t = np.arange(0.0, 30.0, dt)
    N = len(t)

    speed = build_speed_profile(t)
    yaw_gt = build_yaw_profile(t)
    x_gt, y_gt = integrate_xy(speed, yaw_gt, dt)

    low_mask = (t >= 7.0) & (t <= 17.0)
    cross_idx = int(17.0 / dt)  # speed crosses 0.2 around here in profile

    # ---- Scheme A: original — LIO yaw with small low-speed noise ----
    yaw_A = yaw_gt.copy()
    yaw_A[low_mask] += rng.normal(
        0.0, np.deg2rad(args.lowspeed_yaw_noise_deg), low_mask.sum()
    )
    x_A, y_A = x_gt.copy(), y_gt.copy()
    write_tum(out / "A_original.tum", t, x_A, y_A, yaw_A)

    # ---- Scheme B: low-speed-smooth — yaw lags then jumps ----
    yaw_B = yaw_gt.copy()
    # During low-speed: linearly accumulate a yaw lag from 0 -> jump_deg
    lag = np.zeros_like(t)
    if low_mask.sum() > 1:
        lag[low_mask] = np.linspace(
            0.0, np.deg2rad(args.jump_deg), low_mask.sum()
        )
    # The lag persists briefly after low-speed ends...
    persist_mask = (t > 17.0) & (t <= 17.0 + dt * 1.5)  # ~1 frame
    lag[persist_mask] = np.deg2rad(args.jump_deg)
    # ...and then snaps to zero (the "jump") at the next frame.
    yaw_B = yaw_gt - lag
    # Position drifts modestly in the lateral direction during low-speed
    side = 0.5 * args.lowspeed_pos_drift_m
    drift_y = np.zeros_like(t)
    if low_mask.sum() > 1:
        drift_y[low_mask] = np.linspace(0.0, side, low_mask.sum())
    drift_y[t > 17.0] = side  # carries over (no snap on position)
    x_B = x_gt.copy()
    y_B = y_gt + drift_y
    write_tum(out / "B_lowspeedsmooth.tum", t, x_B, y_B, yaw_B)

    # ---- Scheme C: angle-keep-LIO — yaw clean, position has slight drift ----
    yaw_C = yaw_gt.copy()  # clean
    drift_y_c = np.zeros_like(t)
    if low_mask.sum() > 1:
        drift_y_c[low_mask] = np.linspace(0.0, args.lowspeed_pos_drift_m,
                                          low_mask.sum())
    drift_y_c[t > 17.0] = args.lowspeed_pos_drift_m
    x_C = x_gt.copy()
    y_C = y_gt + drift_y_c
    write_tum(out / "C_angkeep_lio.tum", t, x_C, y_C, yaw_C)

    # ---- Summary ----
    print(f"Generated 3 TUM files at {out}/")
    print(f"  A_original.tum       N={N}  yaw 1sigma noise={args.lowspeed_yaw_noise_deg} deg in low-speed")
    print(f"  B_lowspeedsmooth.tum N={N}  yaw jump={args.jump_deg} deg at t~17.0s")
    print(f"  C_angkeep_lio.tum    N={N}  position drift={args.lowspeed_pos_drift_m} m in low-speed")
    print(f"\nSpeed profile: 0.6 -> decel(5-7s) -> 0.1 (low) -> accel(17-19s) -> 0.6")
    print(f"Low-speed window:  7.0 ~ 17.0 s  (10 s)")
    print(f"Speed crossing:    ~17.0 s")


if __name__ == "__main__":
    main()
