#!/usr/bin/env python3
"""
SLAM export (TUM pose + NV12 + RGB PCD) → COLMAP text for 3DGS training.

Dependencies: numpy, Pillow
"""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import sys
import warnings
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow required: pip install pillow", file=sys.stderr)
    sys.exit(1)

# -----------------------------------------------------------------------------
# Default calibration (Roborock long-sequence rig — rectified pinhole)
# -----------------------------------------------------------------------------

DEFAULT_INTRINSICS = {
    "model": "PINHOLE",
    "width": 640,
    "height": 544,
    "fx": 241.984,
    "fy": 241.984,
    "cx": 339.823,
    "cy": 275.645,
}

# Rotation lidar → camera (row-major), translation (meters)
_RCL_FLAT = (
    -0.999865,
    -0.0067944,
    0.0149309,
    -0.0157783,
    0.14933,
    -0.988662,
    0.00448773,
    -0.988764,
    -0.149417,
)
_PCL = (0.029879, -0.031769, -0.495527)


def default_T_cam_lidar() -> np.ndarray:
    R = np.array(_RCL_FLAT, dtype=np.float64).reshape(3, 3)
    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = R
    T[:3, 3] = _PCL
    return T


# -----------------------------------------------------------------------------
# PCD (binary)
# -----------------------------------------------------------------------------

PCD_TYPE = {
    ("F", 4): np.float32,
    ("F", 8): np.float64,
    ("U", 1): np.uint8,
    ("U", 2): np.uint16,
    ("U", 4): np.uint32,
    ("I", 1): np.int8,
    ("I", 2): np.int16,
    ("I", 4): np.int32,
}


def parse_pcd(path: Path) -> np.ndarray:
    with path.open("rb") as f:
        header = {}
        while True:
            line = f.readline().decode("ascii", errors="replace").strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition(" ")
            header[key] = value
            if key == "DATA":
                break
        fields = header["FIELDS"].split()
        sizes = [int(x) for x in header["SIZE"].split()]
        types = header["TYPE"].split()
        counts = [int(x) for x in header["COUNT"].split()]
        n = int(header["POINTS"])
        if header["DATA"].lower() != "binary":
            raise ValueError(f"only binary PCD supported, got {header['DATA']}")
        dt_fields = []
        for nm, t, s, c in zip(fields, types, sizes, counts):
            np_t = PCD_TYPE[(t, s)]
            dt_fields.append((nm, np_t) if c == 1 else (nm, np_t, c))
        raw = np.frombuffer(f.read(), dtype=np.dtype(dt_fields), count=n)
    return raw


# -----------------------------------------------------------------------------
# Poses & files
# -----------------------------------------------------------------------------


def load_poses(pose_path: Path) -> np.ndarray:
    """
    TUM: timestamp tx ty tz qx qy qz qw
    Returns float64 array shape (N, 8).
    """
    data = np.loadtxt(pose_path, dtype=np.float64)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    if data.shape[1] != 8:
        raise ValueError(f"expected 8 columns in TUM pose, got shape {data.shape}")
    return data


def list_cam_files(cam_dir: Path) -> List[Tuple[float, Path]]:
    """Map each frame file to timestamp in seconds (filename = milliseconds)."""
    out: List[Tuple[float, Path]] = []
    for p in sorted(cam_dir.iterdir()):
        if not p.is_file():
            continue
        stem = p.stem
        if not stem.isdigit():
            continue
        ms = int(stem)
        out.append((ms / 1000.0, p))
    out.sort(key=lambda x: x[0])
    return out


def align_timestamps(
    poses: np.ndarray,
    cam_files: Sequence[Tuple[float, Path]],
    tolerance_ms: float,
) -> List[Tuple[np.ndarray, float, Path]]:
    if not cam_files:
        return []
    cam_ts = np.array([t for t, _ in cam_files], dtype=np.float64)
    paths = [p for _, p in cam_files]
    tol_sec = tolerance_ms / 1000.0
    matched: List[Tuple[np.ndarray, float, Path]] = []
    for row in poses:
        t = float(row[0])
        idx = int(np.searchsorted(cam_ts, t))
        cand = []
        if idx > 0:
            cand.append(idx - 1)
        if idx < len(cam_ts):
            cand.append(idx)
        best = min(cand, key=lambda i: abs(cam_ts[i] - t))
        if abs(cam_ts[best] - t) <= tol_sec:
            matched.append((row, float(cam_ts[best]), paths[best]))
    return matched


# -----------------------------------------------------------------------------
# SE(3)
# -----------------------------------------------------------------------------


def quat_xyzw_to_R(qx: float, qy: float, qz: float, qw: float) -> np.ndarray:
    """Unit quaternion (x,y,z,w) → rotation matrix (active rotation)."""
    n = np.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
    if n == 0:
        raise ValueError("zero quaternion")
    qx, qy, qz, qw = qx / n, qy / n, qz / n, qw / n
    xx, yy, zz = qx * qx, qy * qy, qz * qz
    xy, xz, yz = qx * qy, qx * qz, qy * qz
    wx, wy, wz = qw * qx, qw * qy, qw * qz
    return np.array(
        [
            [1 - 2 * (yy + zz), 2 * (xy - wz), 2 * (xz + wy)],
            [2 * (xy + wz), 1 - 2 * (xx + zz), 2 * (yz - wx)],
            [2 * (xz - wy), 2 * (yz + wx), 1 - 2 * (xx + yy)],
        ],
        dtype=np.float64,
    )


def pose_row_to_T_world_lidar(row: np.ndarray) -> np.ndarray:
    """TUM row: ts tx ty tz qx qy qz qw → T_4x4, p_world = R @ p_lidar + t."""
    _, tx, ty, tz, qx, qy, qz, qw = row
    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = quat_xyzw_to_R(qx, qy, qz, qw)
    T[:3, 3] = (tx, ty, tz)
    return T


def se3_inv(T: np.ndarray) -> np.ndarray:
    R = T[:3, :3]
    t = T[:3, 3]
    Ti = np.eye(4, dtype=np.float64)
    Ti[:3, :3] = R.T
    Ti[:3, 3] = -R.T @ t
    return Ti


def rotation_matrix_to_quaternion_wxyz(R: np.ndarray) -> Tuple[float, float, float, float]:
    """Shepperd's method → (qw, qx, qy, qz)."""
    R = np.asarray(R, dtype=np.float64).reshape(3, 3)
    tr = float(np.trace(R))
    if tr > 0.0:
        S = np.sqrt(tr + 1.0) * 2.0
        qw = 0.25 * S
        qx = (R[2, 1] - R[1, 2]) / S
        qy = (R[0, 2] - R[2, 0]) / S
        qz = (R[1, 0] - R[0, 1]) / S
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2.0
        qw = (R[2, 1] - R[1, 2]) / S
        qx = 0.25 * S
        qy = (R[0, 1] + R[1, 0]) / S
        qz = (R[0, 2] + R[2, 0]) / S
    elif R[1, 1] > R[2, 2]:
        S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2.0
        qw = (R[0, 2] - R[2, 0]) / S
        qx = (R[0, 1] + R[1, 0]) / S
        qy = 0.25 * S
        qz = (R[1, 2] + R[2, 1]) / S
    else:
        S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2.0
        qw = (R[1, 0] - R[0, 1]) / S
        qx = (R[0, 2] + R[2, 0]) / S
        qy = (R[1, 2] + R[2, 1]) / S
        qz = 0.25 * S
    q = np.array([qw, qx, qy, qz], dtype=np.float64)
    q /= np.linalg.norm(q)
    return float(q[0]), float(q[1]), float(q[2]), float(q[3])


def world_to_cam_from_pose_row(row: np.ndarray, T_cam_lidar: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    COLMAP world→camera (p_cam = R @ p_world + t).
    T_w2c = T_cam_lidar @ inv(T_world_lidar).
    """
    T_w_l = pose_row_to_T_world_lidar(row)
    T_w2c = T_cam_lidar @ se3_inv(T_w_l)
    R = T_w2c[:3, :3]
    t = T_w2c[:3, 3]
    return R, t


# -----------------------------------------------------------------------------
# NV12 → RGB (BT.601 full swing, same as common embedded nv12 decoders)
# -----------------------------------------------------------------------------


def nv12_to_rgb(buf: bytes, width: int, height: int) -> np.ndarray:
    expected = int(width * height * 1.5)
    if len(buf) < expected:
        raise ValueError(f"NV12 buffer too small: {len(buf)} < {expected}")
    y_plane = np.frombuffer(buf, dtype=np.uint8, count=width * height).reshape(
        (height, width)
    )
    uv = np.frombuffer(
        buf, dtype=np.uint8, offset=width * height, count=(width * height) // 2
    ).reshape((height // 2, width // 2, 2))

    u = np.repeat(np.repeat(uv[:, :, 0], 2, axis=0), 2, axis=1)[:height, :width].astype(
        np.float32
    )
    v = np.repeat(np.repeat(uv[:, :, 1], 2, axis=0), 2, axis=1)[:height, :width].astype(
        np.float32
    )
    y = y_plane.astype(np.float32)

    # BT.601 limited range YUV → RGB (common for 8-bit video)
    y1 = (y - 16.0) * (255.0 / 219.0)
    u1 = (u - 128.0) * (255.0 / 224.0)
    v1 = (v - 128.0) * (255.0 / 224.0)

    r = y1 + 1.402 * v1
    g = y1 - 0.344136 * u1 - 0.714136 * v1
    b = y1 + 1.772 * u1

    rgb = np.stack([r, g, b], axis=-1)
    np.clip(rgb, 0, 255, out=rgb)
    return rgb.astype(np.uint8)


def _decode_job(task: Tuple[str, str, int, int]) -> Tuple[bool, str]:
    src, dst, width, height = task
    try:
        path_in = Path(src)
        buf = path_in.read_bytes()
        rgb = nv12_to_rgb(buf, width, height)
        Image.fromarray(rgb).save(dst)
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{src}: {exc}"


def decode_all_nv12(
    jobs: Sequence[Tuple[Path, Path]],
    width: int,
    height: int,
    njobs: int,
) -> int:
    tasks = [(str(a), str(b), width, height) for a, b in jobs]
    failed = 0
    if njobs <= 1:
        for t in tasks:
            ok, msg = _decode_job(t)
            if not ok:
                failed += 1
                warnings.warn(msg, stacklevel=2)
        return failed
    with mp.Pool(processes=njobs) as pool:
        for ok, msg in pool.imap_unordered(_decode_job, tasks, chunksize=8):
            if not ok:
                failed += 1
                warnings.warn(msg, stacklevel=2)
    return failed


# -----------------------------------------------------------------------------
# COLMAP text writers
# -----------------------------------------------------------------------------


def write_cameras_txt(path: Path, intr: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Camera list with one line of data per camera:",
        "#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]",
        f"# Generated by slam_to_colmap.py",
        (
            f"1 {intr['model']} {intr['width']} {intr['height']} "
            f"{intr['fx']} {intr['fy']} {intr['cx']} {intr['cy']}"
        ),
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_images_txt(
    path: Path,
    frames: Sequence[Tuple[np.ndarray, float, str]],
    T_cam_lidar: np.ndarray,
) -> None:
    """frames: (pose_row, t_cam, png_basename) preserving order."""
    lines = [
        "# Image list with two lines of data per image:",
        "#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME",
        "#   POINTS2D[] as (X, Y, POINT3D_ID)",
        "# Generated by slam_to_colmap.py",
    ]
    for image_id, (row, _, basename) in enumerate(frames, start=1):
        R, t = world_to_cam_from_pose_row(row, T_cam_lidar)
        qw, qx, qy, qz = rotation_matrix_to_quaternion_wxyz(R)
        tx, ty, tz = t
        lines.append(
            f"{image_id} {qw} {qx} {qy} {qz} {tx} {ty} {tz} 1 {basename}"
        )
        lines.append("")  # empty POINTS2D line
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pcd_to_points3d_txt(
    pcd_path: Path,
    out_path: Path,
    max_points: int,
    rng: np.random.Generator,
) -> None:
    raw = parse_pcd(pcd_path)
    n = len(raw)
    xyz = np.stack([raw["x"], raw["y"], raw["z"]], axis=1).astype(np.float64)

    if "rgb" not in raw.dtype.names:
        rgb = np.full((n, 3), 128, dtype=np.uint8)
    elif raw["rgb"].dtype in (np.float32, np.uint32):
        rgb_u32 = raw["rgb"].view(np.uint32)
        r = ((rgb_u32 >> 16) & 0xFF).astype(np.int32)
        g = ((rgb_u32 >> 8) & 0xFF).astype(np.int32)
        b = (rgb_u32 & 0xFF).astype(np.int32)
        rgb = np.stack([r, g, b], axis=1)
    else:
        raise ValueError(f"unsupported rgb dtype {raw['rgb'].dtype}")

    if n > max_points:
        choice = rng.choice(n, size=max_points, replace=False)
        xyz = xyz[choice]
        rgb = rgb[choice]

    lines = [
        "# 3D point list with one line of data per point:",
        "#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)",
        "# Generated by slam_to_colmap.py",
    ]
    for i in range(len(xyz)):
        x, y, z = xyz[i]
        r, g, b = int(rgb[i, 0]), int(rgb[i, 1]), int(rgb[i, 2])
        lines.append(f"{i + 1} {x} {y} {z} {r} {g} {b} 0.0")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True, help="dataset root")
    p.add_argument("--output", type=Path, required=True, help="COLMAP output root")
    p.add_argument("--downsample", type=int, default=20, help="keep every N-th frame")
    p.add_argument("--max-pcd-points", type=int, default=100_000)
    p.add_argument("--tolerance-ms", type=float, default=20.0)
    p.add_argument("--cam-subdir", type=str, default="camera/camera0")
    p.add_argument("--pose-file", type=str, default="pose.txt")
    p.add_argument("--pcd-file", type=str, default="0.01_downsample_rgb_0.01.pcd")
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=544)
    p.add_argument(
        "--jobs",
        type=int,
        default=max(1, (os.cpu_count() or 4) - 1),
        help="parallel NV12 decode workers",
    )
    p.add_argument("--seed", type=int, default=42, help="PCD subsample RNG seed")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    inp: Path = args.input.expanduser().resolve()
    out: Path = args.output.expanduser().resolve()

    pose_path = inp / args.pose_file
    cam_dir = inp / args.cam_subdir
    pcd_path = inp / args.pcd_file

    for label, p in [("pose", pose_path), ("camera dir", cam_dir), ("pcd", pcd_path)]:
        if not p.exists():
            print(f"ERROR: missing {label}: {p}", file=sys.stderr)
            sys.exit(1)

    poses = load_poses(pose_path)
    cam_files = list_cam_files(cam_dir)
    if not cam_files:
        print(f"ERROR: no numeric timestamp files under {cam_dir}", file=sys.stderr)
        sys.exit(1)

    matched = align_timestamps(poses, cam_files, args.tolerance_ms)
    print(
        f"matched {len(matched)} / {len(poses)} poses to {cam_dir} "
        f"(tolerance ±{args.tolerance_ms} ms)"
    )

    if args.downsample < 1:
        print("ERROR: --downsample must be >= 1", file=sys.stderr)
        sys.exit(1)
    sampled = matched[:: args.downsample]
    print(f"downsampled (every {args.downsample}) → {len(sampled)} frames")

    images_dir = out / "images"
    sparse_dir = out / "sparse" / "0"
    images_dir.mkdir(parents=True, exist_ok=True)
    sparse_dir.mkdir(parents=True, exist_ok=True)

    intr = {**DEFAULT_INTRINSICS, "width": args.width, "height": args.height}

    T_cam_lidar = default_T_cam_lidar()

    decode_jobs: List[Tuple[Path, Path]] = []
    meta: List[Tuple[np.ndarray, float, str]] = []

    for row, t_cam, src in sampled:
        png_name = f"{int(round(t_cam * 1000))}.png"
        dst = images_dir / png_name
        decode_jobs.append((src, dst))
        meta.append((row, t_cam, png_name))

    nj = min(args.jobs, max(1, len(decode_jobs)))
    print(f"decoding {len(decode_jobs)} NV12 frames with {nj} worker(s)...")
    failed = decode_all_nv12(decode_jobs, args.width, args.height, nj)
    if failed:
        print(f"WARN: {failed} decode(s) failed (see warnings); omitting from images.txt")

    frames_for_txt: List[Tuple[np.ndarray, float, str]] = []
    for (row, t_cam, png_name), (_, dst) in zip(meta, decode_jobs):
        if dst.is_file() and dst.stat().st_size > 0:
            frames_for_txt.append((row, t_cam, png_name))

    if not frames_for_txt:
        print("ERROR: no images decoded successfully", file=sys.stderr)
        sys.exit(1)

    write_cameras_txt(sparse_dir / "cameras.txt", intr)
    write_images_txt(sparse_dir / "images.txt", frames_for_txt, T_cam_lidar)

    rng = np.random.default_rng(args.seed)
    print(f"writing points3D.txt from {pcd_path} (max {args.max_pcd_points} points)...")
    pcd_to_points3d_txt(pcd_path, sparse_dir / "points3D.txt", args.max_pcd_points, rng)

    print("done.")
    print(f"  images:  {images_dir}")
    print(f"  sparse:  {sparse_dir}")


if __name__ == "__main__":
    # Support Windows; child processes need guard.
    mp.freeze_support()
    main()
