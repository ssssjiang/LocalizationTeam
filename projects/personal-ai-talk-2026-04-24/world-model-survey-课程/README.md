# World Model for Robot Learning · 综述精读课程

> 论文：**World Model for Robot Learning: A Comprehensive Survey** (arXiv: 2605.00080v1, NTU MARS et al., 2026)
> 教学方式：每节课讲一个核心概念，配课后小问，循序渐进。

## 课程目录

| # | 主题 | 对应论文章节 | 状态 |
|---|---|---|---|
| 01 | 到底什么是「世界模型 World Model」？ | Sec 1 + Sec 2.1.1 | ✅ 已完成 |
| 02 | 为什么纯 VLA 不够？为什么要把 WM 引进来？ | Sec 1 + Sec 3.1 | ✅ 已完成 |
| 03 | 概率统一视角：Policy / 被动 WM / 可控 WM / IDM 是同一回事 | Sec 3.1 公式 (4)–(8) | ✅ 已完成 |
| 04 | 范式 1：IDM-Style（先想象，再行动） | Sec 3.2 | ✅ 已完成 |
| 05 | 范式 2：Single-Backbone（一个 backbone 通吃） | Sec 3.3 | ✅ 已完成 |
| 06 | 范式 3：MoE / MoT（专家分工） | Sec 3.4 | ✅ 已完成 |
| 07 | 范式 4：Unified VLA（把 WM 内化进 VLA） | Sec 3.5 | ✅ 已完成 |
| 08 | 范式 5：Latent-Space WM（不画像素，只在表征空间预测） | Sec 3.6 | ✅ 已完成 |
| 09 | WM 作为 Simulator：替代真机 RL 与 Policy 评测 | Sec 4 | ✅ 已完成 |
| 10 | 视频世界模型的能力进化：想象 → 可控 → 结构 → 基础模型 | Sec 5 | ✅ 已完成 |
| 11 | 评测的"三层金字塔"：开环 / 闭环 / 物理诊断 | Sec 7 | ⏳ |
| 12 | 六大开放挑战，下一步研究在哪 | Sec 8 | ⏳ |

## 公式渲染说明
本目录下所有 `.md` 都使用标准 LaTeX 数学语法（`$...$` 行内、`$$...$$` 行间），
请用支持 KaTeX/MathJax 的 markdown 阅读器查看（VS Code、Typora、Obsidian、Cursor 内置预览均可）。

## 学习沉淀建议
建议在每节课的文件末尾自己补上：
- **我的回答**：把课后题答案写下来
- **我的疑问**：哪里没听懂、想去查的延伸资料
- **我的笔记**：自己重述一遍核心概念
