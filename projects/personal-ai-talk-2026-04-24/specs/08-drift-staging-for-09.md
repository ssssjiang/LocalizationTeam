# 08 → 09 Drift Staging

> 本文档收集 2026-05-04 grill 决定（Q1-Q7）从 `08-knowledge-doc.md` 移出的 drift 内容。
> 用途：作为未来 `09-sweeper-embodied-roadmap.md` §1「行业技术现状地图」的 raw material。
>
> 等 09 brainstorm 完成 form factor / 算力预算 / 时间节点 / 团队 gap 决定后，按 09 章节结构重新整理。

## 1. 移出原因

08 是「演进笔记 (reference)」，narrative arc：演进路径 + 应用扩展 + 解决什么问题；frontier 模型横扫 / reference table 不在该 narrative 上，应归入 09「行业现状地图」。

## 2. drift 块清单

| 来源 | 内容 | 字数 |
|---|---|---|
| 08 §3.4 + §3.5 | 2026 主线大模型（GPT-5.5 / Gemini 3.1 / Claude 4.7 / Mamba-3）+ 国内大模型（Qwen / Kimi / GLM / DeepSeek）| ~2400 |
| 08 §4.3 后半 | 多模态 LLM frontier（国内同期 VLM + 多模态作为 LLM standard）| ~400 |
| 08 §7.3 | 几何重建（3DGS / DUSt3R / VGGT）| ~1500 |

## 3. LLM frontier (来自 08 §3.4 §3.5)

### 3.4 2026 主线大模型

2024-2026 间 LLM frontier 由 OpenAI / Google DeepMind / Anthropic 三家闭源 + Mamba 类替代架构线推进。截至 2026-05-04 主流 release：


| 模型              | 公司              | Release    | Context      | 关键特点                                                                                          | 价格 (in/out per M) |
| --------------- | --------------- | ---------- | ------------ | --------------------------------------------------------------------------------------------- | ----------------- |
| GPT-5.5         | OpenAI          | 2026-04-23 | 1M           | smartest to date；agentic coding / computer use 强化，speed 同 5.4                                 | TBD               |
| Gemini 3.1 Pro  | Google DeepMind | 2026-02-19 | 1M / 64K out | ARC-AGI-2 77.1%；Deep Think (02-12) / Flash TTS (04-15) / Enterprise Agent Platform (04-22) 配套 | TBD               |
| Claude Opus 4.7 | Anthropic       | 2026-04-16 | 1M           | 长程编码 verification，长任务 self-check                                                              | $5 / $25          |
| Mamba-3         | Princeton + CMU | 2026-03    | 长序列          | State Space Model，O(n) 时间 + 常数显存                                                              | open              |


#### 主线方向

- **GPT-5.5** (OpenAI 2026-04-23)[18]：比 GPT-5.4 在 agentic coding / computer use (browser / OS automation) 显著强化；推理 cost / speed 同 5.4
- **Gemini 3.1 Pro** (Google DeepMind 2026-02-19)[19]：1M 输入 / 64K 输出；配套 Deep Think (2026-02-12 推理模式) + Flash TTS (2026-04-15) + Enterprise Agent Platform (2026-04-22)，Gemini 系列从单一 LLM 扩展为 agent 工具链
- **Claude Opus 4.7** (Anthropic 2026-04-16)[20]：长程编码 verification 机制 — 模型在长任务中段自检 + 修正；$5 / $25 per M token，定价显著高于 Gemini / DeepSeek 同档

#### 架构线：Mamba 与 SSM

Mamba (Gu & Dao, 2023)[16] 用 selective State Space Model (SSM) 替代 self-attention，推理时间复杂度 O(n) + 常数显存（vs Transformer O(n²) + O(n) KV cache）；在 1B-3B scale 与 Transformer 持平。Mamba-2 (Dao & Gu, ICML 2024)[17] 引入 SSD (state-space duality) 框架，把 SSM 与 attention 统一。Mamba-3 (2026-03) 在 1.5B 上准确率较 Mamba-2 +2pt，state size 减半。

主流 frontier 模型仍以 Transformer 为主干；Mamba / SSM 在长序列 / 长 context / inference cost 敏感场景作为补充，多在 hybrid 架构 (Jamba 等，Mamba + Transformer block 交替) 中出现。

### 3.5 国内大模型

国内 frontier LLM 在 2025-2026 出现 4 家主线：Alibaba Qwen / Moonshot Kimi / Zhipu GLM / DeepSeek。截至 2026-05-04 主流 release：


| 模型                  | 公司       | Release    | 参数量                   | Context | 开源闭源                       | 定位                   |
| ------------------- | -------- | ---------- | --------------------- | ------- | -------------------------- | -------------------- |
| Qwen3.6-Max-Preview | Alibaba  | 2026-04-20 | 1T+ MoE 稀疏            | 256K    | API only                   | coding agent         |
| Kimi K2.6           | Moonshot | 2026-04-21 | 1T MoE / 32B active   | 256K    | open-weight (Modified MIT) | long-context + agent |
| GLM-4.6             | Zhipu    | 2025-09    | 355B MoE / 32B active | 200K    | open-weight                | 企业级落地 + 代码           |
| DeepSeek V4         | DeepSeek | 2026-04    | TBD                   | TBD     | open-weight                | base + 推理 cost 优化    |


#### 主线特点

- **Alibaba Qwen 系列**[21]：全家族开源 + scaling 路线。Qwen3 (2025-04 起) 0.6B → 235B MoE 全开源；Qwen3-Max (2025-10) 1T 参数，SWE-Bench 69.6% / Tau2-Bench 74.8%；Qwen3.5 Omni (2026-03) 原生多模态 + 256K；Qwen3.6-Max-Preview (2026-04-20) 进一步扩到 1T+ MoE 稀疏，API-only，主打 coding agent
- **Moonshot Kimi 系列**[22]：agent 与 long-context 路线。Kimi K2 (2025-07) 1T MoE 开源 (Apache 2.0)；K2.5 (2026-01-27) self-directed agent swarm (100 sub-agents 并行 + 1500 tool 同时调用，速度比 single-agent ~4.5×)；K2.6 (2026-04-21) 1T MoE / 32B active，open-weight Modified MIT，agent benchmark 与 GPT-5 / Claude 同档
- **Zhipu GLM 系列**[23]：小尺寸高性能 + 国产芯片适配。GLM-4.6 (2025-09) 355B MoE / 32B active，200K context；LMArena 第 4 (国内并列第一)；代码能力对标 Claude Sonnet 4
- **DeepSeek 系列**[24]：cost / quality 极致优化路线。V3 (2024-12) → V3.5 → V4 (2026-04, base) → R1 (2025-01 推理) → R2 (2026-04 推理 32B dense，单 24GB GPU 可跑)；推理线相关详见 §4.6 +推理融合 节内 inline 简介

#### Frontier 现状

2025-2026 的 frontier release 中，国内 4 家在多个维度站到第一梯队：开源生态 (Qwen / Kimi / GLM 全开源)、agent benchmark (Kimi K2.6)、推理 cost (DeepSeek R2)、coding (Qwen3.6-Max / GLM-4.6)。同期闭源 frontier 仍由 OpenAI / Google / Anthropic 三家把持，绝对差距收窄到月级。

### References (LLM frontier)

- [16] Gu & Dao, Mamba: Linear-Time Sequence Modeling with Selective State Spaces, arXiv 2023. arXiv:2312.00752
- [17] Dao & Gu, Transformers are SSMs (Mamba-2), ICML 2024. arXiv:2405.21060
- [18] OpenAI, Introducing GPT-5.5, openai.com/index/introducing-gpt-5-5 2026-04-23.
- [19] Google DeepMind, Gemini 3.1 Pro Model Card, deepmind.google/models/model-cards/gemini-3-1-pro 2026-02-19.
- [20] Anthropic, Claude Opus 4.7, anthropic.com/news/claude-opus-4-7 2026-04-16.
- [21] Alibaba Qwen team, Qwen3.6-Max-Preview release, qwenlm.github.io 2026-04-20.
- [22] Moonshot AI, Kimi K2.6 release, deeplearning.ai/the-batch 2026-04-21.
- [23] Zhipu, GLM-4.6 release, zhipu.ai 2025-09.
- [24] DeepSeek, DeepSeek V4 release, deepseek.com 2026-04.

## 4. 多模态 LLM frontier (来自 08 §4.3 后半)

#### 国内同期 VLM

- **Qwen-VL** (Bai et al., Alibaba 2023-08)[15]：ViT + Qwen-7B，支持中英文 OCR / grounding / referring expression
- **InternVL** (Chen et al., Shanghai AI Lab CVPR 2024)[16]：6B vision encoder（放大 ViT scale）+ LLM，多模态 benchmark 上对标 GPT-4V

#### 多模态作为 LLM standard

2024 年起，主流 LLM release 默认含多模态：

- Gemini (Google 2023-12 起 native multimodal)
- Claude 3 (Anthropic 2024-03 native vision)
- GPT-4o (OpenAI 2024-05 omni：text + vision + audio)
- Qwen2-VL (2024-08) / Qwen2.5-VL (2025-01) / Qwen3.5 Omni (2026-03)
- Kimi K2 / GLM-4.6 等国内 frontier 均含视觉

VLM 的标准化为 VLA（V-base = VLM）与 World Models（Cosmos-Reason 系列）提供了 ready-made 视觉理解组件；§4.6（具身 VLA）/ §4.7（World Models 近期形态）中绝大多数 model 的 vision tower 直接复用或微调自这条 VLM 主线。

> 上文说"§4.6（具身 VLA）/ §4.7（World Models 近期形态）"是旧 numbering，整理进 09 时按 09 章节重新引用。

## 5. 几何重建 (来自 08 §7.3)

### 7.3 几何重建（3DGS / DUSt3R / VGGT）

与生成路线（Genie / Cosmos）在 latent video 上学世界动力学不同，重建侧工作直接从图像 / 视频数据恢复显式 3D 几何（point cloud / mesh / Gaussians）。2023-2025 间，重建侧 reach explicit primitives + neural rendering / 大模型化 feed-forward 两类突破。本节客观介绍方法（输入 / 输出 / 关键 paper），不下重建 vs 生成的判断。

#### 3D Gaussian Splatting (3DGS) — Kerbl et al., SIGGRAPH 2023[8]

3DGS 把 3D 场景表示为 explicit 3D Gaussians（位置 / 协方差 / 颜色 / opacity），可微分 splatting 渲染。

- **Pipeline**：SfM 初始化 sparse point cloud → 每点初始化为 3D Gaussian → 可微分渲染 + per-pixel L1 / SSIM loss → adaptive density control（split / clone / prune）
- **性能**：1080p 100+ fps real-time render；训练几分钟达到 Mip-NeRF360 PSNR
- **后续工作**：
  - **4DGS**（含时间维度，Wu et al. CVPR 2024）：动态场景
  - **Deformable GS**：变形场建模
  - **SuperSplat / GS-LRM** (Zhang et al. ECCV 2024)[9]：feed-forward 大模型化，从图像直接预测 Gaussians，去除 SfM 初始化 + per-scene optimization

#### DUSt3R / MASt3R — Wang et al., CVPR 2024[10] / Leroy et al., ECCV 2024[11]

DUSt3R 把 3D 重建从 "SfM + MVS + BA" 多阶段 pipeline 改为单 Transformer feed-forward。

- **DUSt3R 输入**：image pair（无标定相机）→ **输出**：两张图分别的 dense 3D point map（在 reference 相机系下），pixel-wise 对应
- **泛化**：任意场景 sparse-view 重建，web image / phone image / video frame 均可
- **MASt3R**：在 DUSt3R 上加 dense matching head，提升 keypoint matching 精度；map-free relocalization 中位平移误差 1.17m → 0.36m，旋转误差降 80%[11]
- **应用**：sparse-view 重建 / SLAM front-end / camera pose recovery；已被 SLAM 社区作 front-end 集成

#### VGGT (Visual Geometry Grounded Transformer) — Wang et al., CVPR 2025[12]

VGGT 把传统 SfM / MVS pipeline 整合为单一大型 feed-forward Transformer。

- **输入**：1-N 张图（任意视角，无标定）
- **一次性输出**：camera intrinsics & extrinsics + per-pixel depth + 3D point cloud + 3D point tracking
- **特点**：不需要 BA 后处理优化；1 秒级 inference（vs 传统 SfM 分钟级 - 小时级）；训练 scale 是 DUSt3R 的几倍
- **影响**：SfM / MVS 传统多阶段 pipeline 被 Transformer feed-forward 端到端整合的近期工作之一

#### 共性与差异

重建侧工作（3DGS / DUSt3R / VGGT）的共性：

- **Explicit geometric primitives**：输出显式 3D 表示（Gaussians / points / camera params），区别于 latent video model 的隐式 world state
- **Neural rendering / feed-forward 大模型化**：3DGS 的 differentiable rasterizer / DUSt3R / VGGT 的 Transformer feed-forward，与 LLM / VLM 时代 architecture 趋同
- **Web-scale data + foundation training**：VGGT / GS-LRM 等大模型化路线开始用 web image / video 大规模 pretrain，与 VLM / VLA 走相同 path

重建侧与生成侧（Genie / Cosmos）的差异（仅陈述方法层面，不下判断）：

- **数据来源**：重建从 observation（real image）出发，生成从 prior + condition 出发
- **几何表示**：重建保留显式几何（point / Gaussian / camera matrix），生成多用 latent feature
- **任务目标**：重建追求 metric 精度（PSNR / pose error），生成追求 photorealism + plausibility

两条线的关系是开放问题之一（详见 §4.8 开放问题 2）。

### References (几何重建)

- [8] Kerbl et al., 3D Gaussian Splatting for Real-Time Radiance Field Rendering, SIGGRAPH 2023. arXiv:2308.04079
- [9] Zhang et al., GS-LRM: Large Reconstruction Model for 3D Gaussian Splatting, ECCV 2024. arXiv:2404.19702
- [10] Wang et al., DUSt3R: Geometric 3D Vision Made Easy, CVPR 2024. arXiv:2312.14132
- [11] Leroy et al., Grounding Image Matching in 3D with MASt3R, ECCV 2024. arXiv:2406.09756
- [12] Wang et al., VGGT: Visual Geometry Grounded Transformer, CVPR 2025. arXiv:2503.11651

## 6. 整理进 09 的建议结构

待 form factor 决定后细化。初步结构：

- 09 §1.1 LLM frontier 当前形态（cover §3 staging 内容）
- 09 §1.2 多模态 LLM frontier（cover §4 staging 内容）
- 09 §1.3 几何重建大模型化（cover §5 staging 内容；与 SLAM / 具身 SoC 选型直接相关）
