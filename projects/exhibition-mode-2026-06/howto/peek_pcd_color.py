#!/usr/bin/env python3
"""
最朴素的 PCD 彩色预览：直接渲染一张俯视图 PNG。

用途：验证 PCD 原始颜色是否正常，不经任何转换链路。

用法：
    python3 peek_pcd_color.py input.pcd [output.png]

依赖：numpy, matplotlib（无需 open3d/pcl/pdal/blender）
"""

import sys
import numpy as np


def parse_pcd(path):
    with open(path, "rb") as f:
        while True:
            line = f.readline().decode("ascii", errors="replace").strip()
            if line.startswith("DATA"):
                break
        # 假设标准 XYZ + rgb(u4 或 f4，4字节) 排布
        dt = np.dtype([("x", "f4"), ("y", "f4"), ("z", "f4"), ("rgb", "u4")])
        raw = np.frombuffer(f.read(), dtype=dt)
    xyz = np.stack([raw["x"], raw["y"], raw["z"]], axis=1)
    rgb_u32 = raw["rgb"].view(np.uint32)
    r = ((rgb_u32 >> 16) & 0xFF).astype(np.uint8)
    g = ((rgb_u32 >> 8) & 0xFF).astype(np.uint8)
    b = (rgb_u32 & 0xFF).astype(np.uint8)
    rgb = np.stack([r, g, b], axis=1)
    return xyz, rgb


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    pcd_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/tmp/pcd_preview.png"

    print(f"[1/3] Parsing {pcd_path}")
    xyz, rgb = parse_pcd(pcd_path)
    print(f"      points: {len(xyz):,}")
    print(f"      RGB stats: R[{rgb[:,0].min()}-{rgb[:,0].max()},mean={rgb[:,0].mean():.0f}] "
          f"G[{rgb[:,1].min()}-{rgb[:,1].max()},mean={rgb[:,1].mean():.0f}] "
          f"B[{rgb[:,2].min()}-{rgb[:,2].max()},mean={rgb[:,2].mean():.0f}]")

    # 降采样到 50 万点（matplotlib 太多点会卡）
    n_target = 500_000
    if len(xyz) > n_target:
        idx = np.random.choice(len(xyz), n_target, replace=False)
        xyz, rgb = xyz[idx], rgb[idx]

    print(f"[2/3] Rendering top-down view ({len(xyz):,} points sampled)")
    import matplotlib
    matplotlib.use("Agg")  # 无 GUI 后端，直接出图
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(16, 12), dpi=120, facecolor="black")
    ax.set_facecolor("black")
    # 用 RGB / 255 作为颜色
    ax.scatter(xyz[:, 0], xyz[:, 1], c=rgb / 255.0, s=0.5, marker=".", linewidths=0)
    ax.set_aspect("equal")
    ax.set_title(f"PCD top-down view (color from raw RGB) - {len(xyz):,} pts",
                 color="white", fontsize=12)
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")
    plt.tight_layout()

    print(f"[3/3] Saving to {out_path}")
    plt.savefig(out_path, dpi=120, facecolor="black")
    print(f"      done. open with: xdg-open {out_path}")


if __name__ == "__main__":
    main()
