#!/usr/bin/env python3
"""
PCD → 3DGS .ply 转换（每个点变成一个固定大小的 Gaussian 椭球）

⚠️ 注意：这不是真正的 3DGS 训练，只是把彩色点云"包装"成 3DGS 格式
   - 没有 view-dependent 高光
   - 没有自适应椭球大小
   - 每个 Gaussian 是固定球形（rotation = 单位四元数）
   - 仅作为可视化形态变换，效果取决于点云密度

输出可用以下 viewer 打开：
   - SuperSplat:        https://playcanvas.com/supersplat/editor
   - antimatter15 .splat viewer (需先转 .splat)
   - PolyCam viewer
   - Spectacular AI viewer

依赖：numpy, plyfile

用法：
    pip install numpy plyfile
    python3 pcd_to_3dgs.py input.pcd output.ply [scale]

参数：
    scale: 每个 Gaussian 的尺寸，默认 0.02m。点云越密 scale 越小。
"""

import sys
from pathlib import Path

import numpy as np

PCD_TYPE = {
    ("F", 4): np.float32, ("F", 8): np.float64,
    ("U", 1): np.uint8, ("U", 2): np.uint16, ("U", 4): np.uint32,
    ("I", 1): np.int8, ("I", 2): np.int16, ("I", 4): np.int32,
}

# 3DGS 用的球谐 0 阶系数（DC 项）的归一化常数
SH_C0 = 0.28209479177387814


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
            raise ValueError("only binary PCD supported")
        dt = []
        for nm, t, s, c in zip(fields, types, sizes, counts):
            np_t = PCD_TYPE[(t, s)]
            dt.append((nm, np_t) if c == 1 else (nm, np_t, c))
        raw = np.frombuffer(f.read(), dtype=np.dtype(dt), count=n)
    return raw


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    inp, out = sys.argv[1], sys.argv[2]
    gauss_scale = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02

    try:
        from plyfile import PlyData, PlyElement
    except ImportError:
        print("ERROR: plyfile not installed. Run: pip install plyfile")
        sys.exit(1)

    print(f"[1/4] Reading PCD: {inp}")
    raw = parse_pcd(inp)
    n = len(raw)
    xyz = np.stack([raw["x"], raw["y"], raw["z"]], axis=1).astype(np.float32)
    print(f"      points: {n:,}")

    # 解 RGB（PCD packed uint32 / float32）
    if "rgb" in raw.dtype.names and raw["rgb"].dtype in (np.float32, np.uint32):
        rgb_u32 = raw["rgb"].view(np.uint32)
        r = ((rgb_u32 >> 16) & 0xFF) / 255.0
        g = ((rgb_u32 >> 8) & 0xFF) / 255.0
        b = (rgb_u32 & 0xFF) / 255.0
    else:
        print("      WARN: no rgb in PCD, defaulting to gray")
        r = g = b = np.full(n, 0.5)

    print(f"[2/4] Building Gaussian parameters")
    # SH DC 项（0 阶球谐）：(rgb - 0.5) / SH_C0
    f_dc_0 = ((r.astype(np.float32) - 0.5) / SH_C0).astype(np.float32)
    f_dc_1 = ((g.astype(np.float32) - 0.5) / SH_C0).astype(np.float32)
    f_dc_2 = ((b.astype(np.float32) - 0.5) / SH_C0).astype(np.float32)

    # opacity: 用 logit 反函数（3DGS 内部 sigmoid 后才是真正 opacity）
    # 我们想要 opacity ≈ 0.99 → logit(0.99) ≈ 4.6
    opacity = np.full(n, 4.6, dtype=np.float32)

    # scale: 3DGS 内部 exp 后才是真正 scale
    # 想要真实 scale = gauss_scale → log(gauss_scale)
    scale_log = np.log(gauss_scale).astype(np.float32)
    scale_0 = np.full(n, scale_log, dtype=np.float32)
    scale_1 = np.full(n, scale_log, dtype=np.float32)
    scale_2 = np.full(n, scale_log, dtype=np.float32)

    # rotation: 单位四元数 (w, x, y, z) = (1, 0, 0, 0)
    rot_0 = np.ones(n, dtype=np.float32)
    rot_1 = np.zeros(n, dtype=np.float32)
    rot_2 = np.zeros(n, dtype=np.float32)
    rot_3 = np.zeros(n, dtype=np.float32)

    # normals（3DGS 标准格式要求有但不用）
    nx = ny = nz = np.zeros(n, dtype=np.float32)

    print(f"[3/4] Assembling 3DGS .ply structure")
    dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('nx', 'f4'), ('ny', 'f4'), ('nz', 'f4'),
        ('f_dc_0', 'f4'), ('f_dc_1', 'f4'), ('f_dc_2', 'f4'),
        ('opacity', 'f4'),
        ('scale_0', 'f4'), ('scale_1', 'f4'), ('scale_2', 'f4'),
        ('rot_0', 'f4'), ('rot_1', 'f4'), ('rot_2', 'f4'), ('rot_3', 'f4'),
    ]
    verts = np.empty(n, dtype=dtype)
    verts['x'], verts['y'], verts['z'] = xyz[:, 0], xyz[:, 1], xyz[:, 2]
    verts['nx'], verts['ny'], verts['nz'] = nx, ny, nz
    verts['f_dc_0'], verts['f_dc_1'], verts['f_dc_2'] = f_dc_0, f_dc_1, f_dc_2
    verts['opacity'] = opacity
    verts['scale_0'], verts['scale_1'], verts['scale_2'] = scale_0, scale_1, scale_2
    verts['rot_0'], verts['rot_1'], verts['rot_2'], verts['rot_3'] = rot_0, rot_1, rot_2, rot_3

    print(f"[4/4] Writing {out}")
    el = PlyElement.describe(verts, 'vertex')
    PlyData([el]).write(out)

    sz = Path(out).stat().st_size / 1024 / 1024
    print(f"      done. {sz:.1f} MB")
    print()
    print(f"建议 viewer:")
    print(f"  - SuperSplat (online):  https://playcanvas.com/supersplat/editor")
    print(f"    直接拖入 .ply 即可")
    print(f"  - antimatter15 splat:   先转 .splat 后用 https://antimatter15.com/splat/")


if __name__ == "__main__":
    main()
