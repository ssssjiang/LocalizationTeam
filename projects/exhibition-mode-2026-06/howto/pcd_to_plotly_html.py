#!/usr/bin/env python3
"""
PCD → 单 HTML 文件（带 Plotly 3D 交互可视化）

输出的 HTML 是单文件，发给任何人双击浏览器打开就能看
（不需要 web server / 不需要安装任何东西）。

用途：
- 给销售/老板/客户发邮件附件 demo
- 嵌入 PPT（用 PPT "插入对象" → HTML）
- 投标方案附件

依赖：plotly, numpy

用法：
    pip install plotly numpy
    python3 pcd_to_plotly_html.py input.pcd output.html [max_points]

参数：
    max_points: 降采样后的点数上限，默认 50 万（避免浏览器卡）
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
            raise ValueError("only binary PCD")
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
    max_pts = int(sys.argv[3]) if len(sys.argv) > 3 else 500_000

    try:
        import plotly.graph_objects as go
    except ImportError:
        print("ERROR: plotly not installed. Run: pip install plotly")
        sys.exit(1)

    print(f"[1/4] Reading {inp}")
    raw = parse_pcd(inp)
    xyz = np.stack([raw["x"], raw["y"], raw["z"]], axis=1)
    n_total = len(xyz)
    print(f"      total points: {n_total:,}")

    rgb = None
    if "rgb" in raw.dtype.names and raw["rgb"].dtype in (np.float32, np.uint32):
        rgb_u32 = raw["rgb"].view(np.uint32)
        r = ((rgb_u32 >> 16) & 0xFF).astype(np.uint8)
        g = ((rgb_u32 >> 8) & 0xFF).astype(np.uint8)
        b = (rgb_u32 & 0xFF).astype(np.uint8)
        rgb = np.stack([r, g, b], axis=1)

    print(f"[2/4] Downsampling to {max_pts:,}")
    if n_total > max_pts:
        idx = np.random.choice(n_total, max_pts, replace=False)
        xyz = xyz[idx]
        if rgb is not None:
            rgb = rgb[idx]

    print(f"[3/4] Building Plotly figure")
    if rgb is not None:
        # Plotly 接受 'rgb(r,g,b)' 字符串数组
        colors = [f"rgb({r},{g},{b})" for r, g, b in rgb]
    else:
        # 没颜色按高度上色
        colors = xyz[:, 2]

    fig = go.Figure(data=[go.Scatter3d(
        x=xyz[:, 0], y=xyz[:, 1], z=xyz[:, 2],
        mode='markers',
        marker=dict(
            size=1.5,
            color=colors,
            opacity=0.9,
        ),
    )])

    fig.update_layout(
        scene=dict(
            aspectmode='data',  # 真实比例（不要被压成立方体）
            bgcolor='black',
            xaxis=dict(visible=False, showgrid=False, showbackground=False),
            yaxis=dict(visible=False, showgrid=False, showbackground=False),
            zaxis=dict(visible=False, showgrid=False, showbackground=False),
        ),
        paper_bgcolor='black',
        margin=dict(l=0, r=0, t=0, b=0),
        title=dict(text=f"Point Cloud: {Path(inp).name}  ({len(xyz):,} pts)",
                   font=dict(color='white', size=14)),
    )

    print(f"[4/4] Writing {out}")
    fig.write_html(out, include_plotlyjs='cdn', full_html=True)

    sz = Path(out).stat().st_size / 1024
    print(f"      done: {out}  ({sz:.0f} KB)")
    print(f"      → 双击打开浏览器即可，无需任何依赖")


if __name__ == "__main__":
    main()
