# VGGSfM → VGGT → VGGT-Ω · 精读教学课程

> 教学方式：每节课讲一个核心概念，生活类比先行 → 术语/公式 → 对比例子 → 课后小问，循序渐进、深入浅出。
> 主线：同一拨人（Oxford VGG + Meta AI，一作 Jianyuan Wang）三年里把「3D 重建」从**传统优化流水线**一步步推到**纯前馈大模型**的演进逻辑。
> 来源原则：每节课开头标注**真实来源**（arXiv ID / 官方项目页 / CVPR 页 / 官方博客），论文内容引用尽量给到 section。不含知乎 / CSDN。

## 课程目录

| # | 主题 | 对应来源 | 状态 |
|---|---|---|---|
| 00 | 这条线到底在解决什么问题？——SfM 五步 + 为什么传统流水线「痛」 | SfM 背景 + VGGSfM/VGGT 引言 | ✅ |
| 01 | 背景棋盘：理解三棒站在谁肩上（point tracking / pointmap regression / DINOv2） | CoTracker, DUSt3R, DINOv2 | ✅ |
| 02 | 支线 A — VGGSfM：把 SfM 做成端到端可微（但 bundle adjustment 还在 loop 里） | VGGSfM, CVPR 2024 | ✅ |
| 03 | 支线 B — DUSt3R & MASt3R：pointmap 回归家族，VGGT 的直接前身 | DUSt3R CVPR'24 / MASt3R ECCV'24 | ✅ |
| 04 | VGGT 总览：一次前馈出全部 3D 属性，扔掉所有后优化 | VGGT, CVPR 2025 Best Paper | ✅ |
| 05 | VGGT 架构：alternating attention + 多预测头 + 那个反直觉的推理 trick | VGGT 论文 Method | ✅ |
| 06 | VGGT-Ω：register attention + 单 dense head，怎么把这套 scale 上去 | VGGT-Ω, CVPR 2026 Oral | ✅ |
| 07 | VGGT-Ω：数据引擎 + 动态场景 + 自监督协议 | VGGT-Ω 论文 | ⏳ |
| 08 | 整条线回收 + 对你 SLAM / 重定位 / 3DGS 工作的意义 | 综合 | ⏳ |
| 补充 01 | track 到底用什么数据结构表达？——CoTracker / VGGSfM / VGGT 三家对比 | CoTracker §3 / VGGSfM §3.1-3.2 / VGGT §3.1,3.3 | ✅ |

> 结构说明：通往 VGGT 有两条平行支线——**支线 A（VGGSfM，可微 SfM）** 和 **支线 B（DUSt3R/MASt3R，pointmap 回归）**。两条都被 VGGT 收编，其中支线 B 是更直接的前身，故单列一节。
> 「补充」系列为跨课横切专题，可在读完相关正课后随时插入；与 00–08 主线编号互不干扰。

## 真实来源总表（每节会再具体标 section）

| 简称 | 全称 / 会议 | arXiv | 项目页 / 官方 |
|---|---|---|---|
| VGGSfM | Visual Geometry Grounded Deep Structure From Motion, CVPR 2024 Highlight | [2312.04563](https://arxiv.org/abs/2312.04563) | [vggsfm.github.io](https://vggsfm.github.io/) · [github](https://github.com/facebookresearch/vggsfm) |
| VGGT | Visual Geometry Grounded Transformer, CVPR 2025 **Best Paper** | [2503.11651](https://arxiv.org/abs/2503.11651) | [vgg-t.github.io](https://vgg-t.github.io/) · [github](https://github.com/facebookresearch/vggt) · [作者讲解视频](https://www.youtube.com/watch?v=7ZYwJEpCUUA) |
| VGGT-Ω | VGGT-Ω, CVPR 2026 **Oral**（2026-05-14） | [2605.15195](https://arxiv.org/abs/2605.15195) | [vggt-omega.github.io](https://vggt-omega.github.io/) |
| DUSt3R | Geometric 3D Vision Made Easy, CVPR 2024 | [2312.14132](https://arxiv.org/abs/2312.14132) | [dust3r 项目页](https://dust3r.europe.naverlabs.com/) · [github](https://github.com/naver/dust3r) |
| MASt3R | Grounding Image Matching in 3D with MASt3R, ECCV 2024 | [2406.09756](https://arxiv.org/abs/2406.09756) | [NAVER LABS 博客](https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/) · [github](https://github.com/naver/mast3r) |
| CoTracker | It is Better to Track Together | [2307.07635](https://arxiv.org/abs/2307.07635) | [co-tracker.github.io](https://co-tracker.github.io/) |
| DINOv2 | Learning Robust Visual Features without Supervision | [2304.07193](https://arxiv.org/abs/2304.07193) | [Meta 官方博客](https://ai.meta.com/blog/dino-v2-computer-vision-self-supervised-learning/) |
| ViT Registers | Vision Transformers Need Registers, ICLR 2024 oral | [2309.16588](https://arxiv.org/abs/2309.16588) | [OpenReview](https://openreview.net/forum?id=2dnO3LLiJ1) |

## 公式渲染说明
本目录下所有 `.md` 使用标准 LaTeX 数学语法（`$...$` 行内、`$$...$$` 行间），用支持 KaTeX/MathJax 的阅读器查看（VS Code / Cursor 预览、Typora、Obsidian 均可）。

## 学习沉淀建议
每节课文件末尾留了三块给你自己填：
- **我的回答**：把课后题答案写下来
- **我的疑问**：哪里没懂、想查的延伸资料
- **我的笔记**：自己重述一遍核心概念

完成课后题后告诉我，我再根据你答的程度决定下一节怎么讲（哪里要细化、哪里可以快进）。
