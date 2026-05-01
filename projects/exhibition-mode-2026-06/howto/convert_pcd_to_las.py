#!/usr/bin/env python3
"""
PCD → LAS 转换脚本（正确处理 RGB + 修正 bbox）

关键修正：
- 解包 PCD 的 packed RGB（PDAL 不会自动做）
- 添加 8 个虚拟"立方体角点"，强制 PotreeConverter 不要把扁平点云的 bbox 撑成立方体
  （否则 Potree 渲染时会因为虚假的稀疏 Z 范围而做错误的 LOD 裁剪，显示残缺）

依赖：numpy, laspy

用法：
    python3 convert_pcd_to_las.py input.pcd output.las
"""

import sys
from pathlib import Path

import numpy as np

try:
    import laspy
except ImportError:
    print("ERROR: laspy not installed. Run: pip install laspy")
    sys.exit(1)


PCD_TYPE = {
    ("F", 4): np.float32, ("F", 8): np.float64,
    ("U", 1): np.uint8,   ("U", 2): np.uint16, ("U", 4): np.uint32,
    ("I", 1): np.int8,    ("I", 2): np.int16,  ("I", 4): np.int32,
}


def parse_pcd(path: str):
    with open(path, "rb") as f:
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


def convert(pcd_path: str, las_path: str) -> None:
    print(f"[1/5] Reading PCD: {pcd_path}")
    raw = parse_pcd(pcd_path)
    n = len(raw)
    xyz = np.stack([raw["x"], raw["y"], raw["z"]], axis=1).astype(np.float64)
    print(f"      points: {n:,}")

    # 解 RGB
    has_color = False
    rgb = None
    if "rgb" in raw.dtype.names and raw["rgb"].dtype in (np.float32, np.uint32):
        rgb_u32 = raw["rgb"].view(np.uint32)
        r = ((rgb_u32 >> 16) & 0xFF).astype(np.uint8)
        g = ((rgb_u32 >> 8) & 0xFF).astype(np.uint8)
        b = (rgb_u32 & 0xFF).astype(np.uint8)
        rgb = np.stack([r, g, b], axis=1)
        has_color = True
        print(f"      RGB sample: R={r[0]} G={g[0]} B={b[0]}")

    # ----- 关键修正：添加立方体 anchor points -----
    # PotreeConverter 内部用 cubicAABB（强制立方体 bbox），扁平点云会被错误 LOD 裁剪
    # 解决：在 bbox 的 8 个角点位置插入"几乎透明"的占位点，强制 bbox 立方体化
    print(f"[2/5] Adding bbox anchor points to prevent Potree LOD bug")
    mn = xyz.min(axis=0)
    mx = xyz.max(axis=0)
    span = mx - mn
    cube_size = span.max()
    center = (mn + mx) / 2
    half = cube_size / 2
    cube_min = center - half
    cube_max = center + half

    anchor_xyz = np.array([
        [cube_min[0], cube_min[1], cube_min[2]],
        [cube_max[0], cube_min[1], cube_min[2]],
        [cube_min[0], cube_max[1], cube_min[2]],
        [cube_max[0], cube_max[1], cube_min[2]],
        [cube_min[0], cube_min[1], cube_max[2]],
        [cube_max[0], cube_min[1], cube_max[2]],
        [cube_min[0], cube_max[1], cube_max[2]],
        [cube_max[0], cube_max[1], cube_max[2]],
    ], dtype=np.float64)
    # 用黑色（不显眼）
    anchor_rgb = np.zeros((8, 3), dtype=np.uint8) if has_color else None

    xyz = np.vstack([xyz, anchor_xyz])
    if has_color:
        rgb = np.vstack([rgb, anchor_rgb])
    print(f"      cube bbox: min={cube_min}  max={cube_max}")
    print(f"      total points after anchors: {len(xyz):,}")

    # ----- 写 LAS -----
    print(f"[3/5] Building LAS structure (PointFormat 3, RGB uint16)")
    header = laspy.LasHeader(point_format=3, version="1.2")
    header.scales = np.array([0.001, 0.001, 0.001])
    header.offsets = xyz.min(axis=0)

    las = laspy.LasData(header)
    las.x = xyz[:, 0]
    las.y = xyz[:, 1]
    las.z = xyz[:, 2]

    if has_color:
        rgb16 = rgb.astype(np.uint16) * 257
        las.red = rgb16[:, 0]
        las.green = rgb16[:, 1]
        las.blue = rgb16[:, 2]

    print(f"[4/5] Writing LAS: {las_path}")
    las.write(las_path)

    out_size = Path(las_path).stat().st_size / 1024 / 1024
    print(f"[5/5] Done. {out_size:.1f} MB")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
