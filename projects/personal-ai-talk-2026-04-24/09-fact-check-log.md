# 全节点事实核查日志

> **核查时间**：2026-04-19（演讲前 5 天）
> **最终状态更新**：2026-04-20（所有修正已应用到主线文件）
> **范围**：11 个节点 + 全场综合（不止 2026 信息，**所有时间点和事实**）
> **核查方式**：对每个关键事实做独立 web search 验证
> **本文件性质**：✅ **修正历史档案**（不再是待办清单）— 所有 A 节列出的修正都已应用到 05/06/07
>
> ⚠️ **诚实声明**：上一轮交付中**多处事实是错误的或基于 hallucination**（错误来源文件已删除），
> 这次核查是为了把所有错误集中识别并修正。**对之前给出错误信息表示道歉**。
>
> ---
>
> ## 修正应用状态总览
>
>
> | 修正项                                                                                                      | 主线文件状态              |
> | -------------------------------------------------------------------------------------------------------- | ------------------- |
> | A1 Genie 3 时间（2026.03 → 2025.08.05）和能力（500+ 分钟 → 几分钟）                                                    | ✅ 已应用到 05 / 06 / 07 |
> | A2 OpenAI "code red" 完全移除                                                                                | ✅ 已从所有主线文件移除        |
> | A3 DeepSeek R2 架构（670B MoE → 32B dense）                                                                  | ✅ 已应用到 05 / 06 / 07 |
> | A4 Gemini 3.1 Pro 数字（GPQA 94.3% / 2M → ARC-AGI-2 77.1% / 1M）                                             | ✅ 已应用到 05 / 06      |
> | A5 GPT-5 完整时间线（补充 GPT-5 本体 2025.08.07）                                                                   | ✅ 已应用到 05 / 06      |
> | A6 AlexNet 错误率（16% → 15.3%）                                                                              | ✅ 已应用到 05           |
> | A7 o3 真实发布时间（preview 2024.12 / 正式 2025.04.16 / pro 2025.06.10）                                           | ✅ 已应用到 05 / 06      |
> | A8 DeepSeek R1 论文修订时间（last revised 2026.01.04）                                                           | ✅ 已记录在 06           |
> | A9 Helix 02 细节（三级架构 / 61 actions / 10M 参数 / 109,504 行 C++）                                               | ✅ 已应用到 05 / 06 / 07 |
> | A10 GR00T N1.6 + Cosmos Reason 2 真实细节                                                                    | ✅ 已应用到 05 / 06 / 07 |
> | A11 Claude Opus 4.7 完整能力描述                                                                               | ✅ 已应用到 05 / 06      |
> | A12 国内 LLM + 国内具身 + 重建侧（Qwen / GLM / Kimi K2.5 / GraspVLA / GO-1 / UnifoLM-VLA-0 / 3DGS / DUSt3R / VGGT） | ✅ 已应用到 05 / 06 / 07 |
>
>
> **状态**：✅ **所有 12 项修正全部应用完毕**。本文件保留作为"事实档案"，供周五现场被追问时快速查阅权威事实。

---

## A. 🔴 必须修正的严重错误

### A1. Genie 3 发布时间和能力（节点 11）

**错误**：之前我写"Genie 3 于 2026.03 公开发布，720p / 24 fps / **500+ 分钟一致性**"

**实际**：

- **发布时间：2025.08.05**（错了 7 个月）
- **一致性：几分钟**（不是 500+ 分钟，**错了 100 倍**）
- 720p / 20-24 fps 是对的

**来源**：[DeepMind 官方博客](https://deepmind.google/en/blog/genie-3-a-new-frontier-for-world-models/)

**根因**：上一轮搜到的 [aibusinessweekly.net 文章](https://aibusinessweekly.net/p/deepmind-genie-3-nvidia-cosmos-world-models-race-2026) 内容**夸大或错误**，我没做交叉验证就直接采用。

---

### A2. OpenAI "code red" — 极可能是单源传言或 hallucination

**错误**：之前我写"OpenAI 内部宣布 code red 加速给 GPT-5 加空间理解"，并把这件事描述成"ChatGPT 之后业界第二次大洗牌"

**实际核查结果**：

- **专门搜 "OpenAI code red Genie 3" 没找到独立来源**
- 2026.04 时间点上 OpenAI 真正在做的事是 **"Spud" 项目**（GPT-5.5/6 内部代号），但和 Genie 3 / 空间理解的直接关联**没有官方或多源证据**
- 上一轮的来源（aibusinessweekly.net）是单一可疑来源

**结论**：**"code red" 这件事不能讲**——讲了等于在分享里散布未经核实的 rumor。**必须从所有文件移除**。

**根因**：单一来源 + 没做交叉验证 + 内容太"故事性"以至于没怀疑。

---

### A3. DeepSeek R2 架构（节点 9）

**错误**：之前我写"R2 是 670B MoE / 37B 激活 / 价格只有 o3 的 1/40"

**实际**：

- **R2 实际是 32B dense transformer**（不是 670B MoE）
- 670B MoE 是 **2025 年的 rumor**，最终没发布
- 上下文 128K（不是更大）
- 性能：92.7% AIME 2025
- License: MIT
- API 成本约比西方 frontier 模型便宜 70%（不是 1/40）
- **发布时间：2026.04**（这周——但具体日期搜索没说清，可能仍在 release 前后）

**来源**：[decodethefuture.org](https://decodethefuture.org/en/deepseek-r2-explained/)

**根因**：上一轮搜到的"670B MoE / 37B 激活 / 1/40 价格"是 2025 年传言数字，被我当成已确认事实写进去。

---

### A4. Gemini 3.1 Pro 数据（节点 4）

**错误**：之前我写"GPQA Diamond 94.3% / 2M token 上下文"

**实际**：

- **ARC-AGI-2 77.1%**（不是 GPQA Diamond）
- **1M token 输入上下文 / 64K 输出**（不是 2M）
- 2026.02.19 发布（时间是对的）

**来源**：[DeepMind 官方](https://deepmind.google/blog/gemini-3-1-pro-a-smarter-model-for-your-most-complex-tasks/) | [Model Card](https://deepmind.google/models/model-cards/gemini-3-1-pro/)

---

### A5. GPT-5 系列发布时间（节点 4）

**之前没提 GPT-5 本体**——直接跳到了 GPT-5.4。这给人一种"GPT-5.4 就是最新一代"的错觉，实际 GPT-5 已经发布快 9 个月了。

**实际时间线**：

- **GPT-5: 2025.08.07**（GPT-5 + GPT-5 Thinking 双系统架构）
- GPT-5.1 Thinking: 2025.11
- GPT-5.3-Codex: 2026.02.05
- GPT-5.3-Codex-Spark: 2026.02.12
- **GPT-5.4: 2026.03.05**（最新通用模型，1M 上下文，computer-use 75% OSWorld）

**来源**：[OpenAI introducing-gpt-5](https://openai.com/index/introducing-gpt-5/) | [OpenAI introducing-gpt-5-4](https://openai.com/index/introducing-gpt-5-4/)

---

### A6. AlexNet 准确率（节点 1）

**小错**：我写"top-5 错误率从 26% 降到 16%"

**实际**：**15.3%**（不是 16%）。第二名是 26.2%。

**来源**：[Wikipedia AlexNet](https://en.wikipedia.org/wiki/AlexNet) + 原论文 NeurIPS 2012

---

### A7. OpenAI o3 真实发布时间（节点 9）

**错误**：之前我写"OpenAI o3 (2024.12)"

**实际**：

- **o3-preview: 2024.12.20 announced**（只是预告，不是发布）
- **o3-mini: 2025.01.31 released**
- **o3 full release: 2025.04.16 released**
- **o3-pro: 2025.06.10 released**
- **o4-mini 也已经发布**（具体时间需要再查）

**来源**：[OpenAI](https://openai.com/research/introducing-o3-and-o4-mini) | [Wikipedia OpenAI o3](https://en.wikipedia.org/wiki/OpenAI_o3)

**ARC-AGI 表现的 nuance**：2024.12 的 o3-preview 在 ARC-AGI-1 上拿了 75.7%（高效配置）/ 87.5%（低效，172x 算力）。但 2025.04 实际发布的 o3 在 ARC-AGI-1 只有 41%（low）/ 53%（medium），**ARC-AGI-2 都低于 3%**。**preview 和正式版差别巨大**——这件事如果讲出来很硬核。

---

### A8. DeepSeek R1 论文细节（节点 9）

**核查到一个我之前没注意的细节**：R1 论文（arXiv 2501.12948）**最后修订时间是 2026.01.04**——所以"R1 是 2025.01"是对的，但论文本身一直在更新。

---

### A9. Helix 02 关键细节（节点 10）

**实际确认**：

- 2026.01.27 发布
- 4 分钟洗碗机任务
- **61 separate loco-manipulation actions**（之前没提的细节）
- 三层架构：System 0（1kHz 平衡）+ System 1（200Hz 视觉运动）+ System 2（高层推理）—— **System 0 是新的**，之前我只说"System 1+System 2"
- 10M 参数神经网络替代 109,504 行 C++

**来源**：[Figure AI 官网](https://www.figure.ai/news/helix-02) | [techloy.com](https://www.techloy.com/figure-ais-helix-02-completes-4-minute-autonomous-kitchen-task-setting-new-humanoid-robotics-benchmark/)

---

### A10. GR00T N1.6 关键细节（节点 10）

**实际确认 + 补充**：

- 发布时间：**2026 National Robotics Week (2026.04 上旬)** — 之前我写的 04.15 应该是对的
- 实际是 **GR00T N1.6 + Cosmos Reason 2 一起发布**——Cosmos Reason 2 是新的 VLM
- Cosmos Reason 2 规格：**2B / 8B 两个版本**，**256K 上下文**，**spatio-temporal reasoning**
- GR00T N1.6 用 Cosmos-Reason-2B 作为内部 VLM
- N1.5 → N1.6 改进：Diffusion Transformer 翻倍（16→32 层）+ FLARE → 集成 Cosmos Reason 2 的因果推理 + state-relative actions（不是 absolute joint angles）

**来源**：[NVIDIA Tech Blog](https://developer.nvidia.com/blog/building-generalist-humanoid-capabilities-with-nvidia-isaac-gr00t-n1-6-using-a-sim-to-real-workflow/) | [NVIDIA Research](https://research.nvidia.com/labs/gear/gr00t-n1_6/)

---

### A11. Claude Opus 4.7 关键细节（节点 4）

**实际确认 + 补充**：

- 发布时间：**2026.04.16**（3 天前）✅
- 关键能力：**复杂长程编码任务的 verification 机制 + 视觉处理上限 2576 像素 + cyber safeguards**
- 价格：$5/M input + $25/M output
- **重要 nuance**：Opus 4.7 是当前 generally available 模型里最强的，**但还有一个 Claude Mythos Preview** 在 limited release 中，比 4.7 更强

**来源**：[Anthropic 官方](https://www.anthropic.com/news/claude-opus-4-7) | [rollingout.com](https://rollingout.com/2026/04/16/anthropic-claude-opus-4-7-new-upgrades/)

---

## A12. 国内 LLM + 国内具身 + 重建侧（2026-04-19 第二轮新增核查）

### 国内 LLM


| 模型               | 时间         | 关键事实                                                                                                    | 来源                                                                                                                                                                               |
| ---------------- | ---------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Qwen3**        | 2025.04 起  | 全家族开源（0.6B–235B MoE）+ 混合推理模式 + 119 语言                                                                   | [alibabagroup.com](https://www.alibabagroup.com/document-1853940226976645120)                                                                                                    |
| **Qwen3-Max**    | 2025.10    | 1T 参数 / 36T tokens / SWE-Bench 69.6% / Tau2-Bench 74.8%                                                 | [alibabacloud.com](https://www.alibabacloud.com/blog/602621)                                                                                                                     |
| **Qwen3.5 Omni** | 2026.03    | 原生多模态（文本+音频+视频+实时）/ 256K 上下文                                                                            | [marktechpost](https://www.marktechpost.com/2026/03/30/alibaba-qwen-team-releases-qwen3-5-omni-a-native-multimodal-model-for-text-audio-video-and-realtime-interaction/)         |
| **GLM-4.6**      | 2025.09.30 | 355B MoE / 32B 激活 / 200K 上下文 / LMArena 第 4 / 国产芯片适配                                                     | [baike.baidu.com/en/item/GLM-4.6](https://baike.baidu.com/en/item/GLM-4.6/1428092)                                                                                               |
| **Kimi K2**      | 2025.07    | 1T MoE / 32B 激活 / 128K 上下文 / Apache 2.0 / MuonClip optimizer                                            | [marktechpost](https://www.marktechpost.com/2025/07/11/moonshot-ai-releases-kimi-k2-a-trillion-parameter-moe-model-focused-on-long-context-code-reasoning-and-agentic-behavior/) |
| **Kimi K2.5** ⭐  | 2026.01.27 | 1T MoE / 32B 激活 / 256K 上下文 / **100 sub-agent / 1500 tools 并行** / 超过 GPT-5.2 / Claude 4.5 / Gemini 3 Pro | [GitHub](https://github.com/MoonshotAI/Kimi-K2.5) + [llm-stats.com](https://llm-stats.com/blog/research/kimi-k2-5-launch)                                                        |


> **特别说明**：之前我说"Kimi 2.5 不存在，可能是用户记错"——**这是错的，Kimi K2.5 确实存在且是 2026.01.27 真实发布**。向用户道歉。

### 国内具身


| 工作                   | 时间         | 关键事实                                                                                            | 来源                                                                                                                                                                                                                                                    |
| -------------------- | ---------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **银河通用 GraspVLA**    | 2025.01.09 | 全球首个端到端具身抓取基础大模型 + 与智源/北大/港大合作 + 10 亿帧合成数据预训练 + 七大泛化金标准                                         | [aibase.com/news/14630](https://www.aibase.com/news/14630)                                                                                                                                                                                            |
| **智元 GO-1**          | 2025.03.10 | ViLLA 架构（Vision-Language-Latent-Action）+ AgiBot World 数据集（100 万条 / 217 任务）+ 成功率 46% → 78%       | [agibot-world.com paper](https://agibot-world.com/blog/agibot_go1.pdf) + [globenewswire](https://www.globenewswire.com/news-release/2025/03/11/3040608/0/en/AgiBot-GO-1-The-Evolution-of-Generalist-Embodied-Foundation-Model-from-VLA-to-ViLLA.html) |
| **宇树 UnifoLM-VLA-0** | 2026 开源    | G1 人形机器人 / 12 类操作任务 / 基于阿里 Qwen2.5-VL-7B / 全部开源                                                 | [robohorizon](https://robohorizon.cn/zh/news/2026/03/unitree-g1-practical-skills/)                                                                                                                                                                    |
| **宇树 G1 / H1**       | 2024-2026  | G1: 127cm / 35kg / $13.5K-16K（**比 Figure 02 低一个数量级**）；H1: 180cm / 47kg / 3.7m/s 跑步速度（2024 世界最快） | [unitree.com](https://unitree.com/g1/)                                                                                                                                                                                                                |


### 重建侧（VGGT / 3DGS / DUSt3R）


| 工作                        | 时间                       | 关键事实                                                                                                   | 来源                                                                                                 |
| ------------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| **3D Gaussian Splatting** | 2023.07                  | Inria GRAPHDECO 团队 / SIGGRAPH 2023 best paper / 100+ fps 1080p / 训练几分钟达到 Mip-NeRF360 画质                | [Inria 主页](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)                              |
| **DUSt3R**                | CVPR 2024                | Naver Labs Europe / 未标定图像直接出 3D pointmap / 标准 transformer encoder + decoder                            | [DUSt3R 主页](https://dust3r.europe.naverlabs.com/)                                                  |
| **MASt3R**                | 2024                     | DUSt3R 升级 / "image matching as 3D task" / 中位平移误差 1.17 → 0.36 / 旋转误差砍 80%                               | [Naver Labs blog](https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/) |
| **VGGT** ⭐                | **CVPR 2025 Best Paper** | Meta + Oxford VGG / feed-forward transformer / 1 秒内输出相机参数+深度+点云+3D track / **完全不需要 bundle adjustment** | [vgg-t.github.io](https://vgg-t.github.io/) + [CVPR 2025 paper](https://arxiv.org/pdf/2503.11651)  |


---

## B. 🟢 核查通过的事实（不需要修改）


| 事实                                                                                               | 状态  |
| ------------------------------------------------------------------------------------------------ | --- |
| ResNet ImageNet 3.57% / 152 层 / He et al. CVPR 2016 best paper                                   | ✅   |
| GPT-3 175B / 2020.05.29 / Tom Brown / "Language Models are Few-Shot Learners"                    | ✅   |
| Chinchilla 70B / 1.4T tokens / DeepMind 2022.03 / 比 Gopher 280B 更强                               | ✅   |
| CLIP 2021.01 / 4 亿对图文 / contrastive learning                                                     | ✅   |
| DDPM / Ho/Jain/Abbeel UC Berkeley / NeurIPS 2020 / arXiv 2006.11239                              | ✅   |
| Stable Diffusion 2022.08.22 公开发布 / Stability AI / OpenRAIL-M license                             | ✅   |
| DALL-E 2 2022.04 announced / 2022.07 public beta / 2022.09.28 no waitlist                        | ✅   |
| GPT-4V 2023.09.25 released                                                                       | ✅   |
| RT-2 2023.07.28 / Google DeepMind / 用 PaLI-X / PaLM-E 做 backbone                                 | ✅   |
| π₀ 2024.10.31 / Physical Intelligence / 7 robot configs / 68 tasks / flow matching action expert | ✅   |
| OpenAI o1 2024.09.12 (o1-preview) / AIME 74% (single) / 83% (consensus 64) / 93% (re-rank 1000)  | ✅   |
| DeepSeek R1 2025.01.22 arXiv 提交 / 性能对标 o1-1217                                                   | ✅   |
| Helix 02 2026.01.27 / 4 分钟洗碗机 / 61 actions / 10M 参数 / 三级架构                                       | ✅   |
| Mamba-3 2026.03.16 / arXiv 2603.15569 / 1.5B 规模 1.8 点提升 / state size 减半 / inference-first        | ✅   |
| Claude Opus 4.7 2026.04.16                                                                       | ✅   |


---

## C. 影响的主线文件 + 改动列表（已全部应用 ✅）

> **以下原本是"待办清单"，现已全部应用到主线文件。保留作为修正历史，便于追溯每一处修改的依据。**

### C1. `05-full-script.md` 已应用的修改


| 段                     | 改动                                                                                                                                                                                                                    |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 节点 1 第一段              | "16%" → "15.3%"                                                                                                                                                                                                       |
| 节点 4 小观点 6（2026 LLM）  | "GPQA Diamond 94.3%" → "ARC-AGI-2 77.1%"；"2M 上下文" → "1M 输入 / 64K 输出"；**追加一句 GPT-5 本体 2025.08.07 发布的事实，让时间线完整**                                                                                                        |
| 节点 9 推理大模型            | **大改**：① 提到 o3 时区分 "o3-preview (2024.12 预告) vs o3 full release (2025.04.16) vs o3-pro (2025.06)"；② DeepSeek R2 数字全部改：32B dense（不是 670B MoE）/ 92.7% AIME / 128K 上下文 / 比西方贵 70%（不是 1/40）；③ 删除"4 个月就被开源追平"这种夸张表述，换成更准确陈述 |
| 节点 11 World Models 突破 | **大改**：① **"Genie 3 在 2026.03 公开发布" → "2025.08.05 发布"**；② **"500+ 分钟一致性" → "几分钟一致性"**；③ **完全删除"OpenAI code red"这件事**；④ 重新写 Genie 3 这段的"震撼度"——它仍然是重大突破，但要基于真实事实                                                        |
| 收尾段                   | "1 个月前 Genie 3 公开发布让 OpenAI 内部宣布 code red" → 必须改写。Genie 3 不是 1 个月前。code red 不能提                                                                                                                                       |


### C2. `06-reading-list.md` 已应用的修改


| 条目                               | 改动                                    |
| -------------------------------- | ------------------------------------- |
| 节点 11 ⭐⭐⭐ 第 1 条 Genie 3          | "(2026.03，3 周前)" → "**(2025.08.05)**" |
| 节点 11 ⭐⭐⭐ 第 2 条 aibusinessweekly | **建议删除**——这是错误信息源                     |
| 节点 9 ⭐⭐⭐ 2026 新增                 | DeepSeek R2 描述全部更新——32B dense，不是 MoE  |


### C3. `07-qa-bank.md` 已应用的修改


| 条目                         | 改动                                                     |
| -------------------------- | ------------------------------------------------------ |
| 节点 9 Q5（DeepSeek R2 vs o3） | 全部数字更新：32B dense / 92.7% AIME / 比 o3 系列贵约 30%（不是 1/40） |
| 节点 11 Q5（OpenAI code red）  | **整段删除**——code red 不能讲                                 |
| 综合追问 Q-X5                  | 删除 "Genie 3 + OpenAI code red" 那条；其他保留                 |


### C4. 已删除的过期文件

以下早期产出文件已删除（含错误内容、被本核查日志或主线文件覆盖）：

- `01-cheatsheet.md` / `02-judgment-appendix.md` / `03-outline-template.md` / `04-go-nogo-checklist.md` / `08-2026-updates.md`

---

## D. 我的反思（这次为什么会出错）

按你"分析模式"和"根因优先"的偏好：

**根因 1**：上一轮搜索"快"——15 min 内搜 5 个节点 + 写 4500 字报告，没做交叉验证。某个 source 说什么我就信。

**根因 2**：**我对 hallucination 的警觉不够**——"OpenAI code red" 这种"故事性强"的内容，我应该更怀疑而不是更兴奋。**任何一个 claim 如果只有单一来源，就应该标注为"未经独立确认"**。

**根因 3**：**没区分 rumor 和事实**——DeepSeek R2 670B MoE 是 2025 年的预测/泄漏，我把它当成已发布产品的规格。这种错误在 AI 领域非常容易犯，因为 rumor → fact 的转换很快但版本号经常变。

**根因 4**：**时间感知偏差**——我把 Genie 3 写成 2026.03 是因为"能力描述听起来像最新"。但实际 Genie 3 是 2025.08，2025 年 8 月也确实是当时最新的。**"听起来很新"不等于"确实是最新发布"**。

**改进**：

1. **任何时间和数字，都做至少 2 个独立来源核查**
2. **rumor 必须显式标记**（"据传 / 未经官方确认 / 业界传言"）
3. **"故事性强"的内容反而要更怀疑**（"code red" 这种话如果是真的，应该有 NYT / Bloomberg / Information 等大媒体报道）

---

## E. 最终状态（2026-04-20 更新）

✅ **所有修正已应用完毕**——本文件从"待办清单"转为"事实档案"。

### 现在 5 份文件的最终状态

```
README.md             — 入口 + 4 晚学习节奏
05-full-script.md     — 完整逐字稿件（事实已全部修正）
06-reading-list.md    — 必读材料清单（事实已全部修正）
07-qa-bank.md         — 追问 Q&A 储备（事实已全部修正）
09-fact-check-log.md  — 本文件（事实档案 + 修正历史）
```

### 周五现场使用 09 的方式

被追问某个时间/数字时，**直接翻 09 的 A 节或 B 节**：

- A 节是"曾经犯过的错 + 正确版本"——记得最深，应对追问最快
- B 节是"经核查确认无误的事实清单"——任何时间/数字都可在这里找到 ground truth
- A12 节专门覆盖 2025-2026 国内 LLM / 国内具身 / 重建侧的所有事实

**事实信任优先级**：09（权威）> 05/06/07（已和 09 对齐）> 任何凭印象的回忆。

---

## F. 60 min 版第二轮核查（2026-04-19）

> **背景**：决定第一次分享只讲 4 老阶段，扩稿到 60 min（spec：`docs/superpowers/specs/2026-04-19-ai-talk-front-4-stages-1h-design.md`）。
> 新加内容（~48 个新事实点）按 ④「严核 + 区分新旧」全部 web 一手核查。
> 分 4 个 Batch，按主题聚合。

### F.1 Batch-1：第一阶段历史

| # | 表述 | 来源 | 结论 |
|---|---|---|---|
| F.1.1 | AlexNet 三作者：Alex Krizhevsky（一作）+ Ilya Sutskever + Geoffrey Hinton（指导教授），University of Toronto | NIPS 2012 paper / Wikipedia | ✅ 保留；注意一作是 Krizhevsky |
| F.1.2 | AlexNet 训练硬件：2 张 NVIDIA GTX 580（每张 3GB VRAM），需要把模型切成两半跨卡训练 | Wikipedia AlexNet / 原论文 | ✅ 保留 |
| F.1.3 | AlexNet 在 ILSVRC-2012 拿到 top-5 错误率 15.3%，第二名 26.2%，差距 ~10.8 个百分点 | NIPS 2012 paper / cacm.acm.org | ✅ 保留 |
| F.1.4 | AlexNet 60M 参数 / 65 万神经元 / 5 conv + 3 FC | 原论文 | ✅ 保留（备用，可能不讲到这层细节） |
| F.1.5 | ImageNet 数据集本身是 AlexNet 成功的关键引擎之一（Fei-Fei Li 团队 2009 提出，~1500 万张标注图像 / 22000 类） | ILSVRC challenge 综述（arxiv 1409.0575） | ✅ 保留判断「数据 > 模型」是合理的范式视角 |
| F.1.6 | ResNet 2015：He / Zhang / Ren / Sun（MSRA，Microsoft Research Asia），arxiv 2015.12 提交，ImageNet top-5 错误率 3.57%，152 层 | arxiv 1512.03385 | ✅ 保留 |
| F.1.7 | LSTM：Hochreiter & Schmidhuber, *Neural Computation* Vol.9 No.8, 1997.11 | Neural Computation 直接引用 | ✅ 保留 |
| F.1.8 | seq2seq：**Sutskever / Vinyals / Le**, NIPS 2014 oral, "Sequence to Sequence Learning with Neural Networks"。WMT-14 英→法 BLEU 34.8（vs SMT baseline 33.3，rerank 后 36.5） | NIPS 2014 paper | ⚠️ **修正**：原稿只写「Sutskever 那篇」，扩稿要写全三作者；BLEU 表述要精确：「BLEU 略超 SMT baseline，rerank 后达到 SOTA 水平」 |
| F.1.9 | Bahdanau attention：Bahdanau / Cho / Bengio, arxiv 2014.09，ICLR 2015 oral，"Neural Machine Translation by Jointly Learning to Align and Translate" | arxiv 1409.0473 / ICLR 2015 | ✅ 保留 |
| F.1.10 | ImageNet ILSVRC-2010 第一名是 NEC-UIUC（SIFT + LBP + SVM），top-5 错误率 28.2%（**不是 2012 那个 26.2%**） | ImageNet 官网 LSVRC 2010 results | ✅ 保留作为「2012 之前还在手工特征时代」的对照（原稿没写 2010，是讲 2012 的对比，无需改） |

**应用状态**：F.1.8 BLEU 表述需在改稿时按"略超 SMT baseline，rerank 后达到 SOTA"措辞落地；其余 F.1.x 保留为新加事实。

