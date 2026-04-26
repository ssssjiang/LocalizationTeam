# AI Talk 前 4 阶段扩到 1h 改稿设计

- **日期**：2026-04-19
- **状态**：approved（brainstorming 走完，进入实现）
- **关联**：`projects/personal-ai-talk-2026-04-24/`
- **前置 spec**：`2026-04-18-ai-talk-topic-b-prep-design.md`

---

## 1. 背景与目标

周五（2026-04-24）晚上是「与 AI 共进」分享群第一次分享。原稿 `05-full-script.md` 是 40 min + 15 min 讨论的版本，结构是「4 老阶段 + 3 新方向 + 收尾」。

**新决定**：第一次只讲「4 老阶段」，3 新方向（推理大模型 / 具身 VLA / World Models 突破）整体留作下次。

**目标**：把 4 老阶段从 ~31 min 扩到 60 min，同时保证：

- 信息准确，所有新加事实点都有一手来源
- 「我有判断」的人设贯穿全场（②为主③为辅）
- 听众层次按半技术听众设计（懂编程 / 用过 LLM API，但没读过论文）

## 2. 决策摘要

| 决策 | 选项 | 说明 |
|---|---|---|
| 总盘 | **B 方案** | 3 + 8 + 22 + 15 + 8 + 4 = 60 min |
| 扩展手法 | **②为主③为辅** | 技术原理多讲一层（直觉为主，无公式）+ 判断 / 视角 |
| 听众深度 | **B 半技术** | 可用关键概念名带口语解释，不假设论文背景 |
| 核查强度 | **④ 严核 + 区分新旧** | 原稿沿用 09 已核结论；新加内容全部 web 一手核查 |
| 执行顺序 | **先核后改** | 每批 web 核完 → 写入 09 §F → 再改 05 对应段 |
| 影响范围 | **只动 README** | 06 / 07 本轮不动，留给下次扩第二讲时统一处理 |
| 核查批次 | **4 批** | 按主题聚合 web 搜索 |
| 流程 | **自动推进** | 不等用户 review，每批完成简短汇报 |

## 3. 每段扩展计划

### 3.1 开场（保持 3 min，改一句话）

- **改写**：把「主体 31 min（4 老阶段）」改成「今天 60 min 分享，4 个老阶段我讲完整；下次再讲 3 个新方向（推理大模型 / 具身 VLA / World Models 突破）」——一开始就把「分两次讲」摊明。
- **新事实点**：0。

### 3.2 第一阶段（6 → 8 min，+2 min）

定位：**奠基段，故事感够、判断到位即可，不深挖原理**。

- **保留**：CNN 取消手工特征 / RNN 串行问题 / ResNet 残差直觉 / 「AI 第一次端到端学特征」判断。
- **新加**：
  1. AlexNet 那晚的故事（Hinton + Krizhevsky + Sutskever，2 张 GTX 580，ImageNet 当晚 top-5 15.3% 把第二名 26.2% 拉开 11 个百分点 → 第二天起 CV 圈一夜变天）
  2. 「为什么 ImageNet 数据集本身才是更深的引擎」一句小判断（数据 > 模型，呼应 scaling law 的伏笔）
- **不加**：BatchNorm / Dropout / 优化器细节。
- **新事实点**（~5）：
  - AlexNet 三作者（Hinton / Krizhevsky / Sutskever）
  - 训练硬件（2 张 GTX 580）
  - ImageNet 数据规模
  - top-5 错误率 26.2 → 15.3
  - ResNet 错误率 3.57

### 3.3 第二阶段（10 → 22 min，+12 min，最大块）

定位：**全场最重要的一段，「工业化堆规模」这个判断的论证段**。

#### 子结构

- **2.1 Transformer 的直觉**（4 min）：self-attention 直觉（Q/K/V 用「问题 / 索引 / 内容」类比，不上公式）+ multi-head 直觉（多个角度同时看）+ positional encoding 为什么要补回去。
- **2.2 Scaling Law**（4 min）：Kaplan 2020 那张图怎么读 + Chinchilla（DeepMind 2022）的「compute optimal」修正——Kaplan 论文低估了数据的重要性、Chinchilla 用同等算力 70B + 1.4T tokens 打败 280B Gopher。讲完给一句判断。
- **2.3 涌现 + ChatGPT**（3 min）：保留原稿 + 一段「涌现争议」——2023 年 Stanford 那篇 *Are Emergent Abilities a Mirage?*。判断：争议没定论，但「涌现」一词要谨慎用。
- **2.4 RLHF 的直觉**（2 min，新段）：SFT → Reward Model → PPO 三阶段直觉，不上损失函数。判断：RLHF 是「产品化对齐」的关键，比模型本身更影响用户体验。
- **2.5 架构分化（Mamba + hybrid）**（2 min）：原稿保留 + 一句直觉（SSM 怎么做到 O(n)——把「看所有历史」压缩成固定大小的隐状态滚动更新）。
- **2.6 推理 scaling 是新维度**（1 min，承上启下，**不展开 o1**）：「2024 年起 AI 增长换了第二条腿——推理时多算一会就能更强，下次再讲」。
- **2.7 frontier 三大厂时间线 + 国内副线**（5 min）：保留原稿 + **每家差异化打法展开一层**（Qwen 全家族 + 国产芯片、GLM 小尺寸高性能、Kimi agent 路线、DeepSeek 小模型 + 后训练）。判断：「模型本身不再是壁垒，护城河在数据飞轮 / 后训练 / agent 编排 / 部署生态」。
- **2.8 二阶段总结**（1 min）：保留原稿「工业化时代起点」+ 一句**SLAM 视角**：「Transformer 范式后来怎么影响了 SLAM——VGGT 用 transformer 端到端做 SfM 是这个范式跨界的代表，下次讲」。

#### 新事实点（~25）

- Q/K/V / multi-head / positional encoding 的标准描述
- Kaplan 2020 论文标题与核心结论
- Chinchilla 70B / 1.4T tokens / 击败 Gopher 280B
- Stanford 涌现争议论文（Schaeffer et al., 2023, *Are Emergent Abilities a Mirage?*）
- InstructGPT / RLHF 三阶段（SFT / RM / PPO）的标准表述
- Mamba SSM 状态压缩机制描述
- Mamba-3（2026.03）数字
- Qwen3 / Qwen3-Max / Qwen3.5 Omni 数字（已在 09 中核过的复用，新加部分核）
- GLM-4.6 数字 + 国产芯片适配的具体表述
- Kimi K2.5 agent swarm 数字
- DeepSeek V3.x 现状
- 三大厂时间线：GPT-5 / 5.4 / Gemini 3.1 Pro / Claude Opus 4.7（已在 09 中核过的复用）

### 3.4 第三阶段（8 → 15 min，+7 min）

#### 子结构

- **3.1 GAN/VAE/Autoregressive 为什么不行**（2 min）：GAN 模式崩塌直觉、VAE 模糊直觉、Autoregressive 太慢直觉，引出「diffusion 用迭代化解了这些」。
- **3.2 Diffusion 的直觉**（3 min）：原稿保留 + score matching（不上公式，只讲「模型学的是噪声方向，不是图像本身」）+ classifier-free guidance（「两个模型加权混合，调 strength 控制提示词的影响」）。
- **3.3 Latent Diffusion + SD**（2 min，新段）：Stable Diffusion 凭什么能跑在消费级 GPU 上——把 diffusion 搬到 VAE latent space，分辨率从 512×512 降到 64×64，**这一招把成本砍了两个数量级**。Rombach et al. CVPR 2022。判断：架构创新有时不在「更牛的模型」，而在「工程上让它跑起来」。
- **3.4 CLIP 的直觉**（3 min）：原稿基础上展开对比学习——一个 batch 里所有 (图,文) 对，对的接近、错的远离，softmax 在 batch 内做 cross-entropy。WIT 4 亿对数据从哪来（互联网爬 + 弱监督 alt-text）。判断：CLIP 的真正贡献是「用自然语言当监督信号」——把 NLP 的 scale 经验搬到 CV 的钥匙。
- **3.5 VLM 范式**（3 min）：保留原稿 + 一层结构展开——「VLM = vision encoder（CLIP-ViT）+ projector（MLP）+ LLM」三件套。LLaVA 用 GPT-4 自动生成 instruction-tuning 数据是关键 trick。判断：这个三件套架构后面会被 VLA 直接搬过去（vision encoder + projector + LLM + action head）——为下次留伏笔。
- **3.6 三阶段总结**（2 min）：保留原稿「打通」判断 + 加一句**SLAM 视角**：「Diffusion 的去噪迭代、和 SLAM 的 bundle adjustment 迭代优化在精神上很像——都是从坏猜测出发逐步收敛」。

#### 新事实点（~15）

- GAN 模式崩塌的标准描述、Goodfellow 2014
- score matching 起源（Hyvärinen 2005, Song & Ermon 2019）
- Stable Diffusion latent 维度（64×64）+ Rombach et al. CVPR 2022 的标题与归属
- classifier-free guidance（Ho & Salimans 2022）
- CLIP WIT 4 亿对数据 + 训练目标的标准描述
- LLaVA GPT-4 数据生成 trick（Liu et al. 2023）
- VLM 三件套（vision encoder + projector + LLM）的标准提法

### 3.5 第四阶段（7 → 8 min，+1 min teaser）

定位：**承上启下的 teaser 段，明确说「为下次留种子」**。

- **保留**：原稿全部内容（World Models 2018 + GEN-1 2023 + LeCun JEPA + 判断）。
- **新加**：
  - 开头一句过渡：「接下来这一段比较短，因为它正好是下次分享的入口——我今天只讲它的『起源』，让你们听完知道为什么 2024 之后 World Models 突然从概念变产品」。
  - 结尾一句承诺：「这条线后面发生了什么，下次讲」。
- **判断**保留 LeCun JEPA 那段，但**收紧**：原稿略偏长，压到 30 秒。
- **新事实点**（~3）：World Models 论文 V+M+C 名称、GEN-1 Runway 时间、LeCun JEPA 提出年份。

### 3.6 收尾（5 → 4 min，精简版）

- 1 min：4 阶段整体判断（「AI 演进 = 端到端 → scale → 创造 → 走向世界」）
- 1 min：今天讲到的国内贡献（保留 Qwen / GLM / Kimi / DeepSeek 那段）
- 1 min：**预告下次**——下次讲 3 个新方向，把今天埋的「推理 scaling / VLA / World Model 产品化」伏笔接上
- 1 min：抛 1–2 个讨论问题（保留 Q1 scaling 尽头 + Q2 开源 vs 闭源；Q3 留到下次）
- **新事实点**：0。

## 4. 改稿动作清单（针对 05-full-script.md）

- **4.1 移除**：延伸 1 / 延伸 2 / 延伸 3 整段 + 收尾里 Q3。
- **4.2 改写**：开场「主体 31 min」→ 60 min 拆分声明 + 头部「总结构」声明同步改。
- **4.3 新加**：每段细分子段（按 §3 子结构）。
- **4.4 调整**：每段时长标注全部更新；表头「演讲式，约 40 min + 15 min 讨论」改为「演讲式，约 60 min + 讨论」。
- **4.5 节奏标注**：每个子段保留至少 1 个 `[节奏]` 标注，主要在判断句前。

## 5. 事实核查计划

### 5.1 核查批次（4 批，按主题聚合 web 搜索）

| 批次 | 主题 | 涵盖事实点 | 估计点数 |
|---|---|---|---|
| **Batch-1** | 第一阶段历史 | AlexNet 当晚故事、ImageNet 错误率年度演进、ResNet 数字、RNN/LSTM 时间线 | ~7 |
| **Batch-2** | Transformer / Scaling Law / RLHF | Chinchilla 论文细节、Kaplan 数据低估、Stanford 涌现争议论文、RLHF 三阶段、InstructGPT | ~12 |
| **Batch-3** | Mamba + 国内 LLM 差异化打法 | Mamba SSM 状态压缩机制、Qwen3 全家族尺寸列表、GLM 国产芯片适配、Kimi agent、DeepSeek V3.x | ~13 |
| **Batch-4** | Diffusion + VLM 技术细节 | GAN 模式崩塌、score matching、SD latent 维度、Rombach et al.、classifier-free guidance、CLIP WIT、LLaVA trick | ~16 |

### 5.2 每个新点的核查记录格式（写入 09 §F）

每点至少包含：
- **表述**：稿件里的原句或核心断言
- **一手来源**：URL（优先官方博客 / arxiv 论文 / 官方 release notes）
- **核查日期**：YYYY-MM-DD
- **核查结论**：保留 / 修正（含修正后表述）/ 移除（含原因）

### 5.3 09 文件改造

- 在 09 末尾新建 **§F「60 min 版第二轮核查（2026-04-19）」**，分 §F.1 ~ §F.4 对应 4 个批次。
- 维持原有 §A–§E 不动。
- 在 §F 顶部维护一个「修正应用状态总览」子表，标记每点已应用 / 待应用 / 未应用。

## 6. 文件影响范围

- **主修改**：`projects/personal-ai-talk-2026-04-24/05-full-script.md`
- **增量更新**：`projects/personal-ai-talk-2026-04-24/09-fact-check-log.md`（新建 §F）
- **README**：`projects/personal-ai-talk-2026-04-24/README.md`，更新一行（「60 min 版」+「新方向留下次」）
- **不动**：`06-reading-list.md` / `07-qa-bank.md`（下次扩第二讲时再处理）

## 7. 执行顺序

```
spec 写完 → commit
  ↓
Batch-1 web 核 → 写入 09 §F.1 → 改 05 第一阶段
  ↓
Batch-2 web 核 → 写入 09 §F.2 → 改 05 第二阶段（Transformer / Scaling / RLHF / 涌现）
  ↓
Batch-3 web 核 → 写入 09 §F.3 → 改 05 第二阶段（Mamba + 国内 + 三大厂时间线）
  ↓
Batch-4 web 核 → 写入 09 §F.4 → 改 05 第三阶段
  ↓
改 05 第四阶段（teaser，~3 个新点用 Batch-1/2 余量或就地核）
  ↓
改开场 + 收尾
  ↓
更新 README
  ↓
读全稿一遍，自检密度 / 节奏 / 时长配重
  ↓
commit + push
```

每批完成简短汇报，**不等用户 review，自动推进**。

## 8. 验收标准

- 05 整体读下来无明显冗余、节奏标注完整
- 4 阶段总时长 ≈ 60 min（按口语 ~150 字/min 估算字数）
- 所有新事实点在 09 §F 有对应核查记录与一手 URL
- 延伸段 1/2/3 全部移除，无残留引用
- README 反映「分两次讲」的新结构
- 工作树干净后 commit 并 push 到 origin/main

## 9. 风险与应对

| 风险 | 应对 |
|---|---|
| 22 min 二阶段子段过碎，听众跟不上 | 每个子段开头用 1 句话明示「这段我要讲什么」；每段结尾给 1 句小判断收 |
| 60 min 字数估错（口语 150 字/min ≈ 9000 字，但口语停顿 / 互动会消耗时间） | 每段写完后做字数估算，整体留 5 min buffer（55–60 min 范围都算达成） |
| Batch-3 国内 LLM 数字时效性强（2026.04 频繁更新） | 优先用官方博客 / 官方 release notes；不可考的数字用区间表述（「约 X 万亿参数」） |
| 涌现争议论文表述被听众反推 | 引用时明确说「Schaeffer et al. 2023」+ 给「争议没定论」的判断态度 |
| SLAM 视角穿插过密变成「主线被打断」 | 总共只 2 处（2.8 / 3.6），且都在阶段总结位置，不在主体段 |

---

**spec 写完，进入 Batch-1。**
