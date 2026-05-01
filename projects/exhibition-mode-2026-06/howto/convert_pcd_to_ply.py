#!/usr/bin/env python3
"""
PCD → PLY (binary, RGB uint8) 转换脚本

为什么用 PLY 而不是 LAS：
- PLY 的 RGB 直接用 uint8 [0,255]，无歧义
- LAS 的 RGB 是 uint16 [0,65535]，PotreeConverter 在转换时可能误处理 sRGB/linear
- PLY 是 PotreeConverter 原生支持的格式

依赖：numpy（无需 laspy/open3d）

用法：
    python3 convert_pcd_to_ply.py input.pcd output.ply
"""

import sys
from pathlib import Path

import numpy as np

PCD_TYPE = {
    ("F", 4): np.float32, ("F", 8): np.float64,
    ("U", 1): np.uint8,   ("U", 2): np.uint16, ("U", 4): np.uint32,
    ("I", 1): np.int8,    ("I", 2): np.int16,  ("I", 4): np.int32,
}


def parse_pcd(path):
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


def write_ply_binary(path, xyz, rgb=None):
    """写小端二进制 PLY，RGB 为 uint8。"""
    n = len(xyz)
    with open(path, "wb") as f:
        # ASCII header
        header = "ply\n"
        header += "format binary_little_endian 1.0\n"
        header += f"element vertex {n}\n"
        header += "property float x\nproperty float y\nproperty float z\n"
        if rgb is not None:
            header += "property uchar red\nproperty uchar green\nproperty uchar blue\n"
        header += "end_header\n"
        f.write(header.encode("ascii"))

        # binary body
        if rgb is not None:
            dt = np.dtype([("x", "f4"), ("y", "f4"), ("z", "f4"),
                           ("r", "u1"), ("g", "u1"), ("b", "u1")])
            rec = np.empty(n, dtype=dt)
            rec["x"] = xyz[:, 0]
            rec["y"] = xyz[:, 1]
            rec["z"] = xyz[:, 2]
            rec["r"] = rgb[:, 0]
            rec["g"] = rgb[:, 1]
            rec["b"] = rgb[:, 2]
            f.write(rec.tobytes())
        else:
            dt = np.dtype([("x", "f4"), ("y", "f4"), ("z", "f4")])
            rec = np.empty(n, dtype=dt)
            rec["x"], rec["y"], rec["z"] = xyz[:, 0], xyz[:, 1], xyz[:, 2]
            f.write(rec.tobytes())


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    inp, out = sys.argv[1], sys.argv[2]

    print(f"[1/3] Reading {inp}")
    raw = parse_pcd(inp)
    n = len(raw)
    print(f"      points: {n:,}")

    xyz = np.stack([raw["x"], raw["y"], raw["z"]], axis=1).astype(np.float32)

    rgb = None
    if "rgb" in raw.dtype.names and raw["rgb"].dtype in (np.float32, np.uint32):
        rgb_u32 = raw["rgb"].view(np.uint32)
        r = ((rgb_u32 >> 16) & 0xFF).astype(np.uint8)
        g = ((rgb_u32 >> 8) & 0xFF).astype(np.uint8)
        b = (rgb_u32 & 0xFF).astype(np.uint8)
        rgb = np.stack([r, g, b], axis=1)
        print(f"      RGB sample: R={r[0]} G={g[0]} B={b[0]}  (means R={r.mean():.0f} G={g.mean():.0f} B={b.mean():.0f})")
    else:
        print("      WARN: no rgb field, output will be grayscale")

    print(f"[2/3] Writing {out}")
    write_ply_binary(out, xyz, rgb)

    sz = Path(out).stat().st_size / 1024 / 1024
    print(f"[3/3] Done. {sz:.1f} MB")


if __name__ == "__main__":
    main()
