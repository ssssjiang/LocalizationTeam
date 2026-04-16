"""
Dual Wedge Prism Scanning Pattern Visualization
Demonstrates why Mid360-style LiDAR uses two prisms instead of one.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import matplotlib.animation as animation

# ── parameters ──────────────────────────────────────────────────────────────
DELTA = 1.0          # each prism deflection angle (normalized)
W1    = 1.0          # prism 1 angular velocity
W2    = 1.618        # prism 2 angular velocity  (golden ratio → near-irrational)
T_MAX = 4 * np.pi    # total time span shown
FPS   = 60


def beam_position(t, w1=W1, w2=W2, d=DELTA):
    """Combined beam direction from two counter-rotating prisms."""
    x = d * np.cos(w1 * t) + d * np.cos(w2 * t)
    y = d * np.sin(w1 * t) + d * np.sin(w2 * t)
    return x, y


def make_static_figure():
    fig = plt.figure(figsize=(16, 10), facecolor="#0f0f1a")
    fig.suptitle("双棱镜扫描原理 — Mid360 非重复扫描",
                 color="white", fontsize=16, fontweight="bold", y=0.97)

    gs = gridspec.GridSpec(2, 3, figure=fig,
                           hspace=0.45, wspace=0.35,
                           left=0.06, right=0.97, top=0.91, bottom=0.07)

    ax_style = dict(facecolor="#12122a", xlim=(-2.3, 2.3), ylim=(-2.3, 2.3))
    title_kw = dict(color="white", fontsize=11, pad=8)

    # ── Panel 1: single prism → circle ──────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0], **ax_style)
    t   = np.linspace(0, 2 * np.pi, 500)
    ax1.plot(np.cos(t), np.sin(t), color="#4fc3f7", lw=1.8)
    ax1.set_aspect("equal")
    ax1.set_title("① 单棱镜旋转\n→ 只画一个圆环", **title_kw)
    ax1.set_xlabel("中心区域永远是盲区", color="#aaaaaa", fontsize=9)
    _style_ax(ax1)

    # ── Panel 2: two prisms same speed → shifted circle ─────────────────────
    ax2 = fig.add_subplot(gs[0, 1], **ax_style)
    x2  = np.cos(t) + np.cos(t)       # same freq → just bigger circle
    y2  = np.sin(t) + np.sin(t)
    ax2.plot(x2 / 2, y2 / 2, color="#4fc3f7", lw=1.8)
    ax2.set_aspect("equal")
    ax2.set_title("② 双棱镜 同速旋转\n→ 仍然只是圆环", **title_kw)
    ax2.set_xlabel("速比 ω₁/ω₂ = 1，无法填充面积", color="#aaaaaa", fontsize=9)
    _style_ax(ax2)

    # ── Panel 3: two prisms different speed → epicycloid ────────────────────
    ax3 = fig.add_subplot(gs[0, 2], **ax_style)
    t3  = np.linspace(0, T_MAX, 3000)
    x3, y3 = beam_position(t3)
    ax3.plot(x3, y3, color="#4fc3f7", lw=0.6, alpha=0.7)
    ax3.set_aspect("equal")
    ax3.set_title(f"③ 双棱镜 不同速 (ω₂/ω₁={W2:.3f})\n→ 外摆线，开始填充面积", **title_kw)
    ax3.set_xlabel(f"时间 = {T_MAX/np.pi:.0f}π", color="#aaaaaa", fontsize=9)
    _style_ax(ax3)

    # ── Panel 4,5,6: coverage builds up over time ───────────────────────────
    for col, t_end_factor, label in [
        (0, 0.05, "单帧 ~33 ms"),
        (1, 0.3,  "~200 ms"),
        (2, 1.0,  "~1 秒 (积分)"),
    ]:
        ax = fig.add_subplot(gs[1, col], **ax_style)
        t_end = t_end_factor * T_MAX
        t_sub = np.linspace(0, t_end, max(100, int(t_end_factor * 8000)))
        xs, ys = beam_position(t_sub)

        # density heatmap using 2d histogram
        h, xedg, yedg = np.histogram2d(xs, ys, bins=80,
                                        range=[[-2.2, 2.2], [-2.2, 2.2]])
        h = np.log1p(h).T
        ax.imshow(h, extent=[-2.2, 2.2, -2.2, 2.2],
                  origin="lower", cmap="hot", alpha=0.85,
                  vmin=0, vmax=h.max())

        # overlay trajectory
        ax.plot(xs, ys, color="#80d8ff", lw=0.5, alpha=0.4)

        # coverage estimate (fraction of bins with hits)
        coverage = np.sum(h > 0) / h.size * 100
        ax.set_aspect("equal")
        ax.set_title(f"覆盖积分：{label}\n覆盖率 ≈ {coverage:.0f}%", **title_kw)
        _style_ax(ax)

    plt.savefig("tools/dual_prism_pattern.png", dpi=150,
                bbox_inches="tight", facecolor=fig.get_facecolor())
    print("Saved → tools/dual_prism_pattern.png")
    plt.close()


def _style_ax(ax):
    ax.tick_params(colors="#555566", labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor("#333355")
    ax.set_xticks([])
    ax.set_yticks([])
    # draw boundary circle representing max FOV
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(2.1 * np.cos(t), 2.1 * np.sin(t),
            color="#444466", lw=1, ls="--", alpha=0.5)
    ax.plot(0, 0, "+", color="#888899", ms=6, mew=1)


if __name__ == "__main__":
    make_static_figure()
