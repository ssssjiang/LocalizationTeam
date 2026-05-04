# 08-knowledge-doc.md 重写 Design


|               |                                                            |
| ------------- | ---------------------------------------------------------- |
| Created       | 2026-05-04                                                 |
| Project       | `projects/personal-ai-talk-2026-04-24`                     |
| Target file   | `projects/personal-ai-talk-2026-04-24/08-knowledge-doc.md` |
| Source script | `projects/personal-ai-talk-2026-04-24/05-full-script.md`   |
| Style guide   | `~/.cursor/rules/personal-doc-style.mdc`（Workflow Skill）   |
| Time cutoff   | 2026-05-04                                                 |
| Doc title     | AI 演进笔记 (2012-2026)                                          |


## 1 Goal

把 40 分钟 talk 的逐字稿（`05-full-script.md`）重写为一份 ~20-22K 字的 knowledge record（`08-knowledge-doc.md`），按 `personal-doc-style.mdc` 全程生效：

- 客观陈述（不出现"我认为/趋势是/建立...范式"）
- 来源可追溯（每条 fact / 数据 / 结论附 paper-style 引用）
- 金字塔结构（论据 → 推断 → 结论；不跳过中间桥）
- 简洁标题（≤ 12 字，名词或短词组）
- 自然中文（避免英文直译腔）

## 2 关键 Decision（Q1-Q7 + Approach + 反馈调整）


| ID       | 主题           | 决定                                                   |
| -------- | ------------ | ---------------------------------------------------- |
| Q1       | 总篇幅与覆盖优先级    | A. 全面覆盖 ~18-20K 字（调研 + grill 后实际约 21.6K，详 §3）       |
| Q2       | 章节骨架         | A. 保留 7 阶段骨架（4 老 + 3 延伸 + 开放问题；G5 砍收尾"整体回收"）       |
| Q3       | 同类多 model 粒度 | A. 同类打包为 1 `###` (1500-2500 字)，内部 `####` / 表格分 model |
| Q4       | 国内副线深度       | (cancelled，已被 Q1+Q3 决定)                              |
| Q5       | SLAM 视角对照    | B. 删去重建 vs 生成对照；重建侧不专门成节                             |
| Q6       | Time cutoff  | B. today 2026-05-04（覆盖 talk 后两周新 release）            |
| Q7       | Spec 位置      | A. `projects/personal-ai-talk-2026-04-24/specs/`     |
| Approach | 写作流程         | A. 分阶段增量（1 `##` / 轮 → 落 doc + commit + user review）  |


**反馈调整**

- 删去原"主线一句话版"节（AI 味）
- 删去原"延伸 3"内的"重建侧工作"节（突兀，不必与 script 一致）
- 开放问题从 3 条减为 2 条（VLA home 泛化 + World Models 与重建合流）
- 第三阶段（生成式）/ 第四阶段（World Models 起源）的时间线虽有重叠（Diffusion 2020 vs World Models 2018），按 talk 顺序保留

**Grill 决定（G1-G7，2026-05-04 由 grill-me skill 出，§3-§10 已对齐）**

| ID  | 主题                       | 决定                                                                                       |
| --- | ------------------------ | ---------------------------------------------------------------------------------------- |
| G1  | 跨节内容重复（R2 / Cosmos / Genie） | 主节展开 model 本体；横向节（三种打法 / +WM）只谈横向关系 + 一句话回引                                              |
| G2  | 字数预算与 Q3 对齐              | 国际 VLA 1300 → 1800 字；其余打包 ### 维持 1200-1300（Q3 下界外可接受，model 数 ≤ 4）                       |
| G3  | `##` 阶段引子句               | 每个 `##` 顶部 1 句：时间锚点 + sub-topic 列举，不下"建立 X 范式"判断                                         |
| G4  | 时间锚点粒度                   | 模型 release 优先 YYYY-MM-DD（查不到给 YYYY-MM）；论文 venue YYYY；同节同 model 第一次给完整日期，后续仅给 model 名     |
| G5  | 开篇 / 收尾总结                | 砍收尾"整体回收"；保留开篇"整体趋势"；末尾直接进"两个开放问题"                                                       |
| G6  | 全文标题 + ## 标题客观化          | 全文标题 "AI 演进笔记 (2012-2026)"；阶段 ## 加时间锚点替代判断词（"成熟" / "突破"）                                |
| G7  | 每轮交付与 review             | 我写完 + commit + 自动 self-check report + drift 提示；user OK 进下轮 / 不 OK 在该轮迭代；commit message 见 §5 |
| G8  | scope 重定向：删延伸 1 推理大模型      | 业务为扫地 / 割草机扩具身、user 做 SLAM；推理大模型与业务弱关联，整节删（净省 ~3200 字）；+推理融合节 inline 补 ~200 字 reasoning 极简介绍 |
| G9  | 重建侧工作回归                  | user 是定位建图算法工程师，重建侧是专业 background；§4.7 (原 §4.8) 加回 "重建侧工作 (3DGS/DUSt3R/VGGT)" ~1500 字客观介绍，不与生成做主观对照（避开 Q5 严禁的 SLAM 视角对照） |

## 3 总体骨架


| `##` 阶段                            | 长度预算       | `###` sub-topics                                                                                          |
| ---------------------------------- | ---------- | --------------------------------------------------------------------------------------------------------- |
| 整体趋势（开篇短段，不开 ##）                  | ~250       | 7 条 bullet 或一段，每条阶段时间锚点 + 代表 work + 1 句 scope statement（覆盖 AI 整体演进，doc 偏 SLAM / 具身视角，不展开 LLM 推理大模型，G8）   |
| 第一阶段：判别式 AI (2012-2015)            | ~2200      | CNN (700) / RNN (600) / ResNet (900)（3）                                                                   |
| 第二阶段：Transformer 范式 (2017-2026)    | ~4800      | Transformer (1000) / Scaling Law (800) / ChatGPT (600) / 2026 主线大模型 (1200) / 国内大模型 (1200)（5）              |
| 第三阶段：生成式 AI (2020-2024)            | ~2600      | Diffusion (1000) / CLIP (800) / GPT-4V (800)（3）                                                           |
| 第四阶段：World Models 起源 (2018-2023)   | ~1600      | World Models 2018 (800) / Runway GEN-1 (800)（2）                                                           |
| 延伸 1：具身 VLA (2023-2026)             | ~4600      | 国际 VLA (1800) / 国内 VLA (1200) / VLA+推理 (**900**, inline reasoning 200) / VLA+World Models (700)（4）        |
| 延伸 2：World Models 近期形态 (2024-2026) | ~3300      | Genie 3 (1000) / NVIDIA Cosmos (800) / **重建侧工作 (1500, 3DGS/DUSt3R/VGGT，G9)**（3）                            |
| 两个开放问题                             | ~700       | VLA 在 home 场景泛化 / World Models 与 metric 重建合流（2，各 ~350）                                                    |
| **Total**                          | **~20.1K** | **20 ###**                                                                                                |


## 4 各 ### Facts Outline

格式：`核心一句话 / 必含 facts / 候选 refs / 候选 image`。

### 4.1 整体趋势（~250）

- 8 阶段连续脉络一段话总结，仅事实陈述，不下"未来如何"判断
- 每阶段时间锚点 + 代表 work 名字

### 4.2 第一阶段：判别式 AI (2012-2015)

**CNN：视觉端到端特征学习** (~700)

- AlexNet 2012 替代手工特征（SIFT/HOG），ImageNet top-5 错误率 16.4% vs SIFT-FV 26.2%
- 关键设计：ReLU / dropout / conv+pool stack / GPU 训练
- 后续推进：VGG (2014) / GoogLeNet (2014)；LeNet (1998) 远端起点
- Refs: Krizhevsky 2012 (AlexNet); LeCun 1998 LeNet; Russakovsky 2015 ILSVRC; Simonyan 2014 VGG
- Image: AlexNet architecture (Krizhevsky 2012 Fig. 2)

**RNN：序列建模** (~600)

- vanilla RNN / LSTM / GRU 三档；hidden state 时序传递；长序列梯度衰减问题
- 应用：NMT (Sutskever 2014 seq2seq) / speech (DeepSpeech 2014)
- Transformer 出现后 NMT/LM 主线快速从 RNN 切到 attention
- Refs: Hochreiter & Schmidhuber 1997 LSTM; Cho 2014 GRU; Sutskever 2014 seq2seq; Hannun 2014 DeepSpeech

**ResNet 与残差连接** (~900)

- 复用 v3 demo（已在当前 `08-knowledge-doc.md` 内），8 条 refs 已齐
- **写作时合并** `### 历史背景` 与 `### 现象` 为单一项

### 4.3 第二阶段：Transformer 范式 (2017-2026)

**Transformer：注意力机制** (~1000)

- self-attention 替代 RNN 的循环结构；scaled dot-product + multi-head + position encoding
- encoder-decoder 在 NMT (WMT'14 EN-DE BLEU 28.4) 超过 RNN baseline
- 三派分化：encoder-only (BERT 2018) / decoder-only (GPT 2018) / encoder-decoder (T5 2019)
- Refs: Vaswani 2017; Devlin 2018 BERT; Radford 2018 GPT-1; Raffel 2019 T5
- Image: Transformer architecture (Vaswani 2017 Fig. 1)

**Scaling Law 与 GPT-3** (~800)

- Kaplan 2020 拟合：loss ~ N^-α · D^-β · C^-γ（N 参数 / D 数据 / C compute）
- GPT-3 175B (Brown 2020)，few-shot in-context learning
- Chinchilla (Hoffmann 2022) 修正：data 与 model 应同速 scale
- Emergent abilities (Wei 2022)
- Refs: Kaplan 2020; Brown 2020 GPT-3; Hoffmann 2022 Chinchilla; Wei 2022 emergent

**ChatGPT 与 RLHF** (~600)

- GPT-3.5 + RLHF (InstructGPT, Ouyang 2022) → ChatGPT 2022.11
- 三阶段：SFT → reward model → PPO；alignment 三 H (helpful/harmless/honest)
- 影响：LLM 第一次"被普通用户日常使用"
- Refs: Ouyang 2022 InstructGPT; Christiano 2017 RLHF; OpenAI 2022.11.30 ChatGPT release

**2026 主线大模型** (~1200, 打包)

- 4 个 model + 表格 + 段落分点 (`####` 或加粗)
  - **GPT-5.5** (OpenAI 2026-04-23)：smartest to date，agentic coding / computer use 强化，speed 同 5.4
  - **Gemini 3.1 Pro** (Google DeepMind 2026-02-19) + Deep Think (02-12) + Flash TTS (04-15) + Enterprise Agent Platform (04-22)
  - **Claude Opus 4.7** (Anthropic 2026-04-16)：1M context，$5/M input + $25/M output
  - **Mamba** (架构线，State Space Models)：Gu & Dao 2023; Mamba-2 2024 等
- 表格列：模型 / release / context / 关键能力 / 价格
- Refs: openai.com/index/introducing-gpt-5-5/; deepmind.google/models/model-cards/gemini-3-1-pro/; anthropic.com/news/claude-opus-4-7; Gu & Dao 2023 Mamba

**国内大模型** (~1200, 打包)

- 4 个 model + 表格 + 段落分点
  - **Qwen3.6-Max-Preview** (Alibaba 2026-04-20)：1T+ MoE 稀疏，API only，coding agent
  - **Kimi K2.6** (Moonshot 2026-04-21)：1T MoE / 32B active，open-weight Modified MIT
  - **GLM-4.6** (Zhipu)：基础大模型，企业级落地
  - **DeepSeek V4** (2026-04)：新 base model
- 表格列：模型 / release / 参数量 / context / 开源闭源 / 定位
- Refs: 各模型官方 release page；deeplearning.ai/the-batch/.../kimi-k2-6-...; lilting.ch/.../qwen36-max-preview-kimi-k26-release-compare

### 4.4 第三阶段：生成式 AI (2020-2024)

**Diffusion 模型与 DDPM** (~1000)

- forward noise / reverse denoise；DDPM (Ho 2020) 训练目标
- 加速：DDIM (Song 2021) 1000 → 50 步内
- Classifier guidance (Dhariwal 2021), classifier-free guidance (Ho 2022)
- Latent Diffusion / Stable Diffusion (Rombach 2022) 把 diffusion 放到 VAE latent space
- 应用线：DALL-E 2 (2022.04), Stable Diffusion (2022.08), Midjourney v3-v6, Imagen
- Refs: Ho 2020 DDPM; Song 2021 DDIM; Dhariwal 2021; Rombach 2022 LDM; Ramesh 2022 DALL-E 2
- Image: forward / reverse diffusion process (Ho 2020 Fig. 2)

**CLIP 与多模态对齐** (~800)

- contrastive img-text 对齐 (Radford 2021)；4M ~ 400M pairs 训练
- zero-shot ImageNet ~76.2% (ViT-L/14)；prompt-based 分类
- 应用：open-vocab detection (OWL-ViT), Stable Diffusion text encoder
- Refs: Radford 2021 CLIP; Jia 2021 ALIGN
- Image: CLIP contrastive training diagram

**GPT-4V 与多模态大模型** (~800)

- vision encoder + LLM；GPT-4V (2023-09), LLaVA (Liu 2023-04 / 1.5 2023-10)
- 国内同期：Qwen-VL (2023-08), InternVL (2023-12)
- 多模态 = 大模型 standard configuration（2024 起几乎所有主流 LLM 自带视觉）
- Refs: OpenAI 2023.09 GPT-4V system card; Liu 2023 LLaVA; Bai 2023 Qwen-VL; Chen 2023 InternVL

### 4.5 第四阶段：World Models 起源 (2018-2023)

**World Models 2018 (Ha & Schmidhuber)** (~800)

- 三模块 V (VAE 视觉 encoder) + M (RNN 动力学预测) + C (controller policy)
- 在 latent space 学世界动力学，agent 用 "dream" 训练 policy
- Tasks: CarRacing-v0 / VizDoom；reward 远超 baseline
- Schmidhuber 早期 (1990 RL with world model) 思想延续
- Refs: Ha & Schmidhuber 2018; Schmidhuber 1990 RL world model
- Image: V/M/C 三模块 architecture (Ha 2018)

**Runway GEN-1 与视频生成** (~800)

- GEN-1 (Runway 2023-02)：video diffusion 早期，depth + img → video stylization
- 后续路线：Stable Video Diffusion (2023-11), Sora (OpenAI 2024-02), Veo (Google 2024-05), Veo 3 (2024)
- 共性：视频 = 3D tensor，diffusion / autoregressive / hybrid 三种范式
- Refs: Esser 2023 GEN-1 (Runway research); Blattmann 2023 SVD; OpenAI 2024.02 Sora technical report

### 4.6 延伸 1：具身 VLA (2023-2026)

**国际 VLA 时间线** (~1800, 打包；G2 扩字数到此值，avg ~300 字/model）

- 4-5 个 model + 表格 + `####` 段落
  - **RT-2** (Google DeepMind 2023-07)：VLM (PaLI-X / PaLM-E) + action token；首个把 VLM 直接转 VLA 的工作
  - **Physical Intelligence π₀** (2024-10)：generalist policy，7 个 robot embodiment，~10k hours 训练
  - **π₀.5** (2025-04-22)：open-world generalization
  - **π₀.7** (2026-04-16)：steerable robot foundation，"step-change in generalization"
  - **Figure AI Helix 02** (2026-01)：full-body autonomy 统一 visuomotor net；Living room tidy demo (2026-03)
  - **NVIDIA GR00T N1** (2025-03) → **N1.7** (2026-04-17)：3B param "Action Cascade" = Cosmos-Reason2-2B (System 2) + 32-layer DiT (System 1)；20,854 hrs human egocentric video (EgoScale)；**首个 robot dexterity scaling law** (1k → 20k hrs 性能 doubling)
- 表格列：model / 公司 / release / robot / 训练数据 / 关键贡献
- Refs: 各 release page；huggingface.co/blog/nvidia/gr00t-n1-7; physicalintelligence.company/blog
- **写作时 verify**：是否有 Helix 03 公开 release；π₀.7 是否替代 π₀ 主线

**国内 VLA 进展** (~1200, 打包)

- 3 个 model + 表格 + `####` 段落
  - **GraspVLA** (银河通用 2025-01-09)：上半身抓取大模型；十亿帧合成数据预训练；七大泛化金标准（光照 / 背景 / 位置 / 高度 / 动作策略 / 动态干扰 / 物体类别）；规划融合 GraspVLA + TrackVLA + 人机交互 → GALBOT VLA
  - **AgiBot GO-1** (智元)：**写作时 verify** release date 与具体 spec
  - **UnifoLM-VLA-0** (宇树 2026-01-29)：基于 Qwen2.5-VL-7B，单一 policy 在 G1 完成 12 类操作（开闭抽屉 / 插拔 / 抓放）；开源
- 表格列：model / 公司 / release / robot / 训练数据 / 开源闭源
- Refs: baike.baidu.com/item/GraspVLA; tech.huanqiu.com/article/4QAL55JkZVE

**VLA + 推理融合** (~900；G8 含 inline reasoning 极简介绍 ~200)

- dual-system 模式：System 1 (反射动作 / 高频 VLA) + System 2 (慢思考 / 推理)
- inline reasoning 极简介绍（~200 字，G8）：reasoning model = 把 chain-of-thought 内置为 model 能力（RL on CoT），代表工作 OpenAI o1 (2024-09) / o3 (2025-04) / DeepSeek R1 (2025-01) / R2 (2026-04)；本 doc 不单独展开（scope 偏 SLAM / 具身）
- 实例：Figure Helix System 1+2; π₀.5 reasoning version；GR00T N1.7 Action Cascade (Cosmos-Reason2-2B 当 System 2)
- 关键挑战：System 1/2 协调延迟、long-horizon planning
- Refs: Helix 2026-01 release; physicalintelligence.company/blog/pi05; huggingface.co/blog/nvidia/gr00t-n1-7; OpenAI 2024.09 o1 system card; DeepSeek 2025.01 R1 paper (arXiv:2501.12948)

**VLA + World Models 融合** (~700)

- 按 G1，Cosmos / Genie 在此节仅简提一句话 + 回引 §4.7，重点放在融合机制
- 用 World Model dreaming 训练 VLA policy（Ha & Schmidhuber 2018 思路延续到当代 VLA training）
- 实例：DeepMind Genie 系列被用于 VLA training playground；GR00T 用 Cosmos 做 sim-to-real；Unitree UnifoLM dreamer
- Refs: Cosmos technical report; UnifoLM release（model 详情见 §4.7 / §4.6 国内 VLA）

### 4.7 延伸 2：World Models 近期形态 (2024-2026)

**Genie 3 与可交互世界生成** (~1000)

- DeepMind Genie 1 (2024-02) → Genie 2 (2024-12) → Genie 3 (2025-08)
- Genie 3：720p / 24fps real-time interactive，photorealistic，60s session 一致性
- 与 Sora-style 视频生成区别：可交互（user 操作影响 world state）
- 公开化：Project Genie (2026-01-29) Google AI Ultra US 18+ 用户
- 应用线：Waymo World Model (2026-02 自动驾驶仿真)
- Refs: deepmind.google/en/blog/genie-3-...; deepmind.google/blog/project-genie-...
- Image: Genie 3 demo screenshot

**NVIDIA Cosmos 与机器人仿真** (~800)

- Cosmos (2025-01) → Predict2.5 / Transfer2.5 / Reason2 (2025-2026)
  - **Predict2.5**：flow-based world prediction（text-to-world / image-to-world / video-to-world 统一）
  - **Transfer2.5**：multi-controlnet 可控生成（depth maps / segmentation 输入）
  - **Reason2**：VLM 增强 spatial-temporal 理解；GR00T N1.7 System 2 backbone
- 定位：physical AI 工具链，与 GR00T 配套
- Early adopters：1X / Agility Robotics / Figure AI / Uber
- Refs: developer.nvidia.com/cosmos; developer.nvidia.com/blog/advancing-physical-ai-with-nvidia-cosmos-...

**重建侧工作 (3DGS / DUSt3R / VGGT)** (~1500，G9 加回；纯客观介绍，不与生成做主观对照)

- 与生成路线对照的"重建路线"近期工作；本节仅客观介绍方法（输入 / 输出 / 关键 paper），不下"重建 vs 生成"判断（Q5 严禁）
- **3D Gaussian Splatting (3DGS)** (Kerbl et al. SIGGRAPH 2023, arXiv:2308.04079)：把 3D 场景表示为 explicit 3D Gaussians，可微分 splatting 渲染；速度 / 质量 在 NeRF-class 任务上同时领先
  - 后续：4DGS（含时间维度）、deformable GS（动态场景）、SuperSplat / GS-LRM（feed-forward 大模型化）
- **DUSt3R / MASt3R** (Wang et al. CVPR 2024, arXiv:2312.14132 / Leroy et al. ECCV 2024, arXiv:2406.09756)：image pair → 3D point map / matching；feed-forward Transformer，无需 SfM 初始化
  - 应用：sparse-view 重建、SLAM front-end、camera pose recovery
- **VGGT (Visual Geometry Grounded Transformer)** (Wang et al. CVPR 2025, arXiv:2503.11651)：1-N images → camera params + depth + point maps + tracking 一次性输出；large-scale Transformer scale
  - 影响：把传统 SfM / MVS pipeline 整合为单一 feed-forward model
- 共性：explicit geometric primitives + neural rendering / 大模型化 feed-forward；与 latent video（Genie 3 / Cosmos）形成两条不同的"3D 表示"路线（仅陈述方法差异，不下判断）
- Refs: Kerbl 2023 3DGS; Wang 2024 DUSt3R; Leroy 2024 MASt3R; Wang 2025 VGGT
- Image: 3DGS rendering vs NeRF 对比 / DUSt3R pair-prediction diagram

### 4.8 两个开放问题（~700, 各 ~350）

- **开放问题 1：VLA 在 home / 长尾场景的泛化**
  - 现状：工厂 / pick-place 任务 robust（GR00T N1.7 EgoScale 已显示 dexterity scaling law）
  - 缺口：home 场景在公开 benchmark 上的 success rate 仍未广泛报告；π₀.5 open-world generalization 是早期信号
  - 待观察：是否有标准 home benchmark；scaling law 在 home 任务上是否同样成立
- **开放问题 2：World Models 与 metric 重建是否合流**
  - Genie 3 / Cosmos 走 latent video 路线（隐式 / 像素级一致性）
  - 3DGS / DUSt3R / VGGT 走 explicit primitives 路线（显式几何 / metric scale）
  - 待观察：某 scale 下两条线产出是否会 converge；是否会出现统一表征

## 5 写作流程（方案 A 落地版）


| 轮次  | 内容                                                              | 备注                                                        | Commit + review |
| --- | --------------------------------------------------------------- | --------------------------------------------------------- | --------------- |
| 1   | 第一阶段（CNN / RNN / ResNet）                                        | ResNet 复用 v3 + 合并历史背景+现象；CNN / RNN 新写                                                    | ✓               |
| 2   | 第二阶段（Transformer 5 ###）                                         | 含 GPT-5.5 / Gemini 3.1 / Claude 4.7 / 国内 LLM 4 家（已 batch）                                | ✓               |
| 3   | 第三阶段（Diffusion / CLIP / GPT-4V）                                 |                                                                                          | ✓               |
| 4   | 第四阶段（World Models 2018 / GEN-1）                                 |                                                                                          | ✓               |
| 5   | 延伸 1（具身 VLA：国际 / 国内 / +推理 / +WM）                                | 国际 VLA 扩到 1800（G2）；+推理含 inline reasoning 极简介绍（G8）；+WM Cosmos / Genie 仅简提（G1）            | ✓               |
| 6   | 延伸 2（World Models 近期形态：Genie 3 / Cosmos / 重建侧工作）                | 重建侧工作回归（3DGS / DUSt3R / VGGT，~1500，G9）                                                   | ✓               |
| 7   | 整体趋势（开篇）+ 两个开放问题（收尾）                                            | 整体趋势 postpone 到此轮写有 navigation-correct 优势（G5）                                            | ✓               |
| 8   | Audit pass：grep 禁用词 / time anchor 一致性 / citation 完整性 / 风格扫描     |                                                                                          | ✓               |


**每轮 deliverable**（G7）：

1. 该 `##` 阶段所有 `###` 写完，落到 `08-knowledge-doc.md`（in-place 替换该阶段）
2. 自动跑 §8 self-check + audit grep，**报告 pass / 需 fix 项**
3. 附 drift 提示：本轮新出 facts / refs 数 / 字数实际 vs 预算 drift（< 20% 接受） / time anchor 一致性
4. commit message：`doc(knowledge-doc): rewrite stage N — <sub-topic 列举>`
5. user review：不 OK → 在该轮迭代；OK → 进下一轮

## 6 References 处理

按 `personal-doc-style.mdc` 已确定的"每个 `##` 末尾独立编号"：

- 每个阶段（`##`）末尾一个 `### References` 小节，列本阶段所有引用
- 编号 `[1]…[N]` 在该 `##` 内编号，跨 `##` 不复用
- 格式：`[N] Author et al., Title, Venue YYYY. arXiv:XXXX.XXXXX` 或 `[N] Org, Title, YYYY-MM-DD. URL`
- 全文预计 6-15 条 / 阶段，总 ~80-100 条

## 7 Image Suggestions

按 SKILL，文中以 `<!-- REVIEW: 此处建议补 ... 来源 [N]。 -->` 注释形式标记，**inline 放在相关段落之后**（与 ResNet demo v3 一致），由用户后续手动判断粘入。每节 0-2 个建议点。候选已在 §4 各 ### 末尾标 "Image: ..."。

## 8 Verification & Self-Check

每节写完后跑 `personal-doc-style.mdc` §7 Self-check List：

- 客观：没有 "我认为 / 趋势是 / 建立...范式" 等
- 来源：每条 fact / 数据 / 结论可追溯（引用编号）
- 简洁：没有 "不是...而是..."、"值得注意的是 / 这意味着 / 从整体来看" 等套话
- 标题：≤ 12 字，名词或短词组
- 中文感：没有 "建立 X 范式 / 实现 Y 突破" 等英文直译腔
- Pyramid：论据 → 推断 → 结论，不跳过中间桥
- Time anchor：每 "目前 / 最新" 都有 release date

全文 audit pass（轮 9）额外跑：

```bash
rg -n "(我认为|趋势是|建立.{0,4}范式|不是.{1,8}而是|值得注意|这意味着|从整体来看)" projects/personal-ai-talk-2026-04-24/08-knowledge-doc.md
```

## 9 待写作时 Verify 项（主体已 batch，剩余边缘项写作时 verify）

- **Helix 03 / Helix 04** 是否有公开 release（当前 search 只找到 Helix 02 + Living Room Tidy demo）
- **AgiBot GO-1（智元）** release date / 关键 spec / 训练数据规模
- 各篇关键论文的 arXiv 编号 / 发表 venue（写每节时实时 verify）
- Mamba 系列在 2026 主线大模型节中的份额（是否已有非纯 Mamba 的主流 model）
- DeepSeek V4 与 R2 的关系（V4 是 base model，R2 是 reasoning post-training？）

## 10 Acceptance Criteria

最终 `08-knowledge-doc.md` 满足：

- 总长 ~20.1K 字（落在 20-22K 区间，G8+G9 净减 ~1.5K）
- 20 个 `###`（按 §3 骨架表；G8 删延伸 1 推理大模型 -3 ###；G9 加回 重建侧工作 +1 ###）
- 全文标题 `# AI 演进笔记 (2012-2026)`
- 每个 `##` 阶段名加时间锚点（替代"成熟" / "突破"等判断词，G6）
- 每个 `##` 顶部 1 句引子句：时间锚点 + sub-topic 列举（G3）
- 每个 `##` 末尾有 `### References` 列引用（每 `##` 内独立 `[N]` 编号，跨 `##` 不复用）
- 每节通过 §8 Self-check
- 全文 audit pass（§8 grep 命令）零 hit
- Time anchor 一致（YYYY-MM-DD / venue YYYY，G4）；同节同 model 第一次给完整日期
- 跨节内容不重复：主节展开 model 本体，横向节回引（G1）
- 用户对每轮内容确认 OK

