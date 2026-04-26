# 必读材料清单（11 节点）

> **使用方式**：
>
> - 周一至周四每晚 3h，按"必读 → 选读"顺序读
> - 全部为英文原文 / 官方博客 / 顶会论文 / 权威讲座，**不含知乎/CSDN**
> - 每个节点标了"最低投入时间"和"完整投入时间"
> - 优先级：⭐⭐⭐ 必读 > ⭐⭐ 强烈建议 > ⭐ 时间允许时读
> - **目标不是读完所有材料**——是配合稿件吃透每个节点的核心逻辑

## 时间预算建议


| 节点                 | 最低投入   | 完整投入    | 备注              |
| ------------------ | ------ | ------- | --------------- |
| 1 RNN/CNN          | 30 min | 90 min  | 概念熟悉即可          |
| 2 ResNet           | 30 min | 60 min  | 单点突破            |
| 3 **Transformer**  | 90 min | 180 min | **重点**，必须吃透     |
| 4 LLM              | 60 min | 120 min | scaling law 是关键 |
| 5 Diffusion        | 60 min | 120 min | 思想 > 数学         |
| 6 VLM              | 45 min | 90 min  | CLIP 是核心        |
| 7 World Models 起源  | 30 min | 60 min  | 老论文，看个故事        |
| 8 GEN-1            | 20 min | 30 min  | 节点窄             |
| 9 推理大模型            | 60 min | 120 min | DeepSeek R1 是必读 |
| 10 **VLA**         | 90 min | 180 min | **全场命门**，必须吃透   |
| 11 World Models 突破 | 45 min | 90 min  | 与节点 7 呼应        |


**最低总投入**：~~9.5 h
**完整总投入**：~~19 h

**4 个晚上 12h 的推荐分配**：

- 周一晚（3h）：节点 3 Transformer + 节点 4 LLM
- 周二晚（3h）：节点 10 VLA（一晚专攻命门）
- 周三晚（3h）：节点 5 Diffusion + 节点 6 VLM + 节点 9 推理大模型
- 周四晚（3h）：节点 1/2/7/8/11（轻量节点扫一遍）+ 全文串讲一次

---

# 节点 1：RNN / CNN

### ⭐⭐⭐ 必读（30 min）

1. **Stanford CS231n — Convolutional Neural Networks**
  [https://cs231n.github.io/convolutional-networks/](https://cs231n.github.io/convolutional-networks/)
  - 读"Architecture Overview" + "Layer Patterns" 两节即可
  - 投入：20 min
  - 学到：CNN 为什么能学图像特征 / 卷积 + pooling 的物理意义
2. **Christopher Olah — Understanding LSTMs**
  [https://colah.github.io/posts/2015-08-Understanding-LSTMs/](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
  - RNN/LSTM 最经典的可视化解释，业内公认入门首选
  - 投入：10 min
  - 学到：RNN 为什么有梯度消失、LSTM 如何解决

### ⭐⭐ 强烈建议（额外 30 min）

1. **Yann LeCun et al. — Gradient-Based Learning Applied to Document Recognition** (1998, LeNet)
  [http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf](http://yann.lecun.com/exdb/publis/pdf/lecun-01a.pdf)
  - 只读 Section I + II（约 5 页），看 CNN 起源
  - 投入：20 min
2. **Krizhevsky et al. — ImageNet Classification with Deep CNNs** (2012, AlexNet)
  [https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
  - 只读 Abstract + Introduction + Results
  - 投入：10 min
  - 学到：AlexNet 凭什么引爆深度学习

### ⭐ 时间允许（额外 30 min）

1. **3Blue1Brown — Neural Networks (YouTube 系列)**
  [https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
  - 第 1-4 集，可视化讲解
  - 投入：30 min

---

# 节点 2：ResNet

### ⭐⭐⭐ 必读（30 min）

1. **He et al. — Deep Residual Learning for Image Recognition** (CVPR 2016 Best Paper)
  [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)
  - 必读 Abstract + Section 1 (Introduction) + Section 3 (Deep Residual Learning) + Section 4.1 前半
  - 投入：30 min
  - 学到：① 退化现象（degradation）的本质 ② 残差连接为什么 work ③ identity mapping 的优雅

### ⭐⭐ 强烈建议（额外 30 min）

1. **He et al. — Identity Mappings in Deep Residual Networks** (ECCV 2016)
  [https://arxiv.org/abs/1603.05027](https://arxiv.org/abs/1603.05027)
  - ResNet v2，进一步分析"为什么残差连接工作"——比 v1 更深刻
  - 只读 Section 1 + Section 3
  - 投入：30 min
  - 学到：identity mapping 在前向 / 反向传播中的优雅性

### ⭐ 时间允许

1. **Kaiming He — ResNet 最初提交版的演讲**
  [https://www.youtube.com/results?search_query=Kaiming+He+ResNet+talk](https://www.youtube.com/results?search_query=Kaiming+He+ResNet+talk)
  - 何恺明本人讲 ResNet 设计动机
  - 投入：20 min

---

# 节点 3：Transformer ⭐ 全场重点

### ⭐⭐⭐ 必读（90 min）

1. **Jay Alammar — The Illustrated Transformer**
  [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
  - **业内公认 Transformer 最佳入门可视化讲解**，英文原文
  - 投入：45 min
  - 学到：self-attention 的物理意义、Q/K/V 的几何解释、multi-head 为什么需要、positional encoding
2. **Vaswani et al. — Attention Is All You Need** (NeurIPS 2017)
  [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
  - 必读 Abstract + Section 1 + Section 3 (Model Architecture, **整段都读**) + Section 7 (Conclusion)
  - 投入：30 min
  - 学到：Transformer 的完整结构定义、为什么 abandon recurrence and convolution
3. **Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out**
  [https://www.youtube.com/watch?v=kCc8FmEb1nY](https://www.youtube.com/watch?v=kCc8FmEb1nY)
  - **Karpathy 亲自从 0 实现 Transformer，2 小时**——看前 30 min 即可（讲清 self-attention）
  - 投入：30 min（看 0:00-0:35 部分）
  - 学到：从"为什么需要 attention"到"代码层面在做什么"

### ⭐⭐ 强烈建议（额外 90 min）

1. **Lilian Weng — Attention? Attention!**
  [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
  - OpenAI 研究员的综述，把 attention 的演进讲清楚（从 2014 Bahdanau 到 Transformer）
  - 投入：30 min
2. **Mu Li (李沐) — Attention Is All You Need 论文逐段精读** (B 站，英文论文中文讲解)
  [https://www.bilibili.com/video/BV1pu411o7BE/](https://www.bilibili.com/video/BV1pu411o7BE/)
  - 1.5h 视频，李沐逐段读论文，比自己读高效
  - 投入：60 min（1.5x 速度）
  - 注：B 站不属于"中文社区博客"，是论文讲解视频，质量高

### ⭐ 时间允许

1. **Stanford CS25 — Transformers United** (course)
  [https://web.stanford.edu/class/cs25/](https://web.stanford.edu/class/cs25/)
  - 第一讲 Introduction to Transformers
  - 投入：60 min
2. **Anthropic — A Mathematical Framework for Transformer Circuits**
  [https://transformer-circuits.pub/2021/framework/index.html](https://transformer-circuits.pub/2021/framework/index.html)
  - 深度理解 attention 在做什么的最新视角，难度高
  - 投入：60 min

### ⭐⭐ 2026 新增（必看 — 挑战 Transformer 的 Mamba 路线）

1. **Mamba-3: Improved Sequence Modeling using State Space Principles** (arXiv 2603.15569, 2026.03)
  [https://arxiv.org/abs/2603.15569v1](https://arxiv.org/abs/2603.15569v1)
  - 必读 Abstract + Section 1
  - 投入：30 min
  - 学到：① SSM vs Transformer 的本质权衡 O(n) vs O(n²) ② Mamba-3 的 3 个新机制（指数-梯形离散化 / 复数值状态跟踪 / MIMO formulation）
2. **Goomba Lab — Mamba-3 Part 1 博客**
  [https://goombalab.github.io/blog/2026/mamba3-part1/](https://goombalab.github.io/blog/2026/mamba3-part1/)
  - Mamba 团队官方博客解读
  - 投入：20 min
  - 学到：为什么 Mamba-3 强调 inference-first 而不是 training efficiency

---

# 节点 4：LLM

### ⭐⭐⭐ 必读（60 min）

1. **Kaplan et al. — Scaling Laws for Neural Language Models** (OpenAI 2020)
  [https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361)
  - 必读 Abstract + Section 1 + Section 3.1 + Section 6
  - 投入：30 min
  - 学到：scaling law 的精确陈述、N (params) / D (data) / C (compute) 的幂律关系
2. **Wei et al. — Emergent Abilities of Large Language Models** (2022)
  [https://arxiv.org/abs/2206.07682](https://arxiv.org/abs/2206.07682)
  - 必读 Abstract + Section 1 + Section 2 + Figure 2/3
  - 投入：30 min
  - 学到："涌现"的精确定义和典型例子（这是面对追问最容易被打的概念）

### ⭐⭐ 强烈建议（额外 60 min）

1. **Hoffmann et al. — Training Compute-Optimal LLMs** (Chinchilla, DeepMind 2022)
  [https://arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556)
  - 必读 Abstract + Section 1 + Section 3
  - 投入：20 min
  - 学到：Chinchilla 修正了 Kaplan 的结论——data 比之前以为的更重要
2. **Brown et al. — Language Models are Few-Shot Learners** (GPT-3, 2020)
  [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
  - 只读 Abstract + Section 1 + Section 3.1
  - 投入：20 min
  - 学到：in-context learning 的发现
3. **Ouyang et al. — Training language models to follow instructions with human feedback** (InstructGPT/RLHF, 2022)
  [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
  - 只读 Abstract + Section 1 + Figure 2
  - 投入：20 min
  - 学到：RLHF 的 3 步 pipeline（不需要细节）

### ⭐ 时间允许

1. **Lilian Weng — Prompt Engineering**
  [https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
  - LLM 怎么用的综述
  - 投入：30 min
2. **Jared Kaplan — Scaling Laws talk** (YouTube)
  [https://www.youtube.com/watch?v=h1d5LtOe1xw](https://www.youtube.com/watch?v=h1d5LtOe1xw)
  - 论文一作讲解
  - 投入：45 min

### ⭐⭐ 2026 一线模型必读

1. **Anthropic — Introducing Claude Opus 4.7** (2026.04.16，3 天前刚发布)
  [https://www.anthropic.com/news/claude-opus-4-7](https://www.anthropic.com/news/claude-opus-4-7)
  - 最新一线模型的能力 + 设计哲学（verification 机制、软件工程能力）
  - 投入：15 min
2. **Google — Gemini 3.1 Pro 官方博客** (2026.02.19)
  [https://deepmind.google/blog/gemini-3-1-pro-a-smarter-model-for-your-most-complex-tasks/](https://deepmind.google/blog/gemini-3-1-pro-a-smarter-model-for-your-most-complex-tasks/)
  - **ARC-AGI-2 拿到 77.1%**（不是网上常误传的 GPQA 94.3%）
  - **1M 输入 / 64K 输出上下文**（不是 2M）
  - 投入：15 min
3. **OpenAI — Introducing GPT-5** (2025.08.07)
  [https://openai.com/index/introducing-gpt-5/](https://openai.com/index/introducing-gpt-5/)
  - GPT-5 本体的发布博客——首次内置 thinking + 通用模型
  - 投入：10 min
4. **OpenAI — Introducing GPT-5.4** (2026.03)
  [https://openai.com/index/introducing-gpt-5-4/](https://openai.com/index/introducing-gpt-5-4/)
  - 1M 上下文 + 原生 computer-use（OSWorld 75%）
  - 投入：10 min

### ⭐⭐⭐ 国内 LLM 必读（2025-2026）

1. **Alibaba Qwen3-Max 官方介绍** (2025.10)
  [https://www.alibabacloud.com/blog/602621](https://www.alibabacloud.com/blog/602621)
  - 1T 参数 / 36T tokens / SWE-Bench 69.6% / Tau2-Bench 74.8%
  - 投入：15 min
2. **Alibaba Qwen3.5 Omni** (2026.03)
  [https://www.marktechpost.com/2026/03/30/alibaba-qwen-team-releases-qwen3-5-omni-a-native-multimodal-model-for-text-audio-video-and-realtime-interaction/](https://www.marktechpost.com/2026/03/30/alibaba-qwen-team-releases-qwen3-5-omni-a-native-multimodal-model-for-text-audio-video-and-realtime-interaction/)
  - 原生多模态（文本+音频+视频+实时）+ 256K 上下文 + Hybrid-Attention MoE
  - 投入：10 min
3. **Zhipu AI GLM-4.6** (2025.09.30)
  [https://baike.baidu.com/en/item/GLM-4.6/1428092](https://baike.baidu.com/en/item/GLM-4.6/1428092)
  - 355B MoE / 32B 激活 / 200K 上下文 / LMArena 第 4
  - 投入：10 min
4. **Moonshot Kimi K2.5 官方** (2026.01.27) ⭐⭐⭐
  - GitHub: [https://github.com/MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5)
  - 详细解读: [https://llm-stats.com/blog/research/kimi-k2-5-launch](https://llm-stats.com/blog/research/kimi-k2-5-launch)
  - 1T MoE / 32B 激活 / 256K 上下文 / **100 sub-agent 并行 / 1500 tools 同时**
  - 投入：20 min
  - **重点**：agent swarm 范式是 2026 年的大趋势，必须吃透
5. **Moonshot Kimi K2** (2025.07，K2.5 的前身)
  [https://www.marktechpost.com/2025/07/11/moonshot-ai-releases-kimi-k2-a-trillion-parameter-moe-model-focused-on-long-context-code-reasoning-and-agentic-behavior/](https://www.marktechpost.com/2025/07/11/moonshot-ai-releases-kimi-k2-a-trillion-parameter-moe-model-focused-on-long-context-code-reasoning-and-agentic-behavior/)
  - 1T MoE / 32B 激活 / Apache 2.0 / MuonClip optimizer
  - 投入：15 min

---

# 节点 5：Diffusion

### ⭐⭐⭐ 必读（60 min）

1. **Lilian Weng — What are Diffusion Models?**
  [https://lilianweng.github.io/posts/2021-07-11-diffusion-models/](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
  - **业内公认 Diffusion 最佳综述**，英文原文，OpenAI 研究员写
  - 投入：45 min
  - 学到：DDPM 的完整推导、forward / reverse process、和 score-based 的关系
2. **Ho et al. — Denoising Diffusion Probabilistic Models** (DDPM, NeurIPS 2020)
  [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
  - 只读 Abstract + Section 1 + Section 2 + Algorithm 1/2
  - 投入：15 min
  - 学到：训练目标的精确形式（不要陷推导）

### ⭐⭐ 强烈建议（额外 60 min）

1. **Rombach et al. — High-Resolution Image Synthesis with Latent Diffusion Models** (Stable Diffusion, CVPR 2022)
  [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
  - 必读 Abstract + Section 1 + Section 3 + Figure 3
  - 投入：30 min
  - 学到：为什么 latent space 比 pixel space 更高效
2. **Ramesh et al. — Hierarchical Text-Conditional Image Generation with CLIP Latents** (DALL-E 2, 2022)
  [https://arxiv.org/abs/2204.06125](https://arxiv.org/abs/2204.06125)
  - 只读 Abstract + Section 1
  - 投入：15 min
  - 学到：text-to-image 的 prior + decoder 架构
3. **Yang Song — Generative Modeling by Estimating Gradients of the Data Distribution**
  [https://yang-song.net/blog/2021/score/](https://yang-song.net/blog/2021/score/)
  - score-based 视角讲 diffusion，更深刻
  - 投入：30 min

### ⭐ 时间允许

1. **CVPR 2023 Tutorial — Denoising Diffusion-based Generative Modeling**
  [https://cvpr2023-tutorial-diffusion-models.github.io/](https://cvpr2023-tutorial-diffusion-models.github.io/)
  - 顶会教程，全面深入
  - 投入：90 min

---

# 节点 6：VLM

### ⭐⭐⭐ 必读（45 min）

1. **Radford et al. — Learning Transferable Visual Models From Natural Language Supervision** (CLIP, 2021)
  [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
  - 必读 Abstract + Section 1 + Section 2.3 (Method) + Section 3.1
  - 投入：30 min
  - 学到：contrastive learning + 4 亿图文对的训练范式
2. **OpenAI Blog — CLIP: Connecting Text and Images**
  [https://openai.com/research/clip](https://openai.com/research/clip)
  - 官方博客，配图清晰
  - 投入：15 min

### ⭐⭐ 强烈建议（额外 45 min）

1. **OpenAI — GPT-4V(ision) System Card** (2023)
  [https://cdn.openai.com/papers/GPTV_System_Card.pdf](https://cdn.openai.com/papers/GPTV_System_Card.pdf)
  - GPT-4V 的官方文档，看能力 demo + safety 部分
  - 投入：20 min
2. **Liu et al. — Visual Instruction Tuning** (LLaVA, NeurIPS 2023)
  [https://arxiv.org/abs/2304.08485](https://arxiv.org/abs/2304.08485)
  - 必读 Abstract + Section 1 + Section 3
  - 投入：25 min
  - 学到：开源 VLM 的训练范式（GPT-4V 闭源，LLaVA 是社区主流）

### ⭐ 时间允许

1. **Bai et al. — Qwen-VL: A Versatile Vision-Language Model** (Alibaba 2023)
  [https://arxiv.org/abs/2308.12966](https://arxiv.org/abs/2308.12966)
  - 国内代表
  - 投入：20 min
2. **Yin et al. — A Survey on Multimodal Large Language Models**
  [https://arxiv.org/abs/2306.13549](https://arxiv.org/abs/2306.13549)
  - 综述，全面但长
  - 投入：60 min（选读）

---

# 节点 7：World Models 起源

### ⭐⭐⭐ 必读（30 min）

1. **Ha & Schmidhuber — World Models** (NeurIPS 2018)
  [https://arxiv.org/abs/1803.10122](https://arxiv.org/abs/1803.10122)
  - 必读 Abstract + Section 1 + Figure 1/2 + Section 4
  - **强烈推荐看交互式版本**：[https://worldmodels.github.io/](https://worldmodels.github.io/)
  - 投入：30 min
  - 学到：VAE + RNN + Controller 的三件套 / "在梦里训练"的核心思想

### ⭐⭐ 强烈建议（额外 30 min）

1. **Hafner et al. — Dream to Control: Learning Behaviors by Latent Imagination** (Dreamer v1, ICLR 2020)
  [https://arxiv.org/abs/1912.01603](https://arxiv.org/abs/1912.01603)
  - 只读 Abstract + Section 1 + Figure 1
  - 投入：20 min
  - 学到：Dreamer 系列开山，从玩具任务走向真实控制
2. **LeCun — A Path Towards Autonomous Machine Intelligence** (JEPA 路线, 2022)
  [https://openreview.net/pdf?id=BZ5a1r-kVsf](https://openreview.net/pdf?id=BZ5a1r-kVsf)
  - LeCun 的 AGI 路线图，强调 world model 是 AGI 核心
  - 只读 Section 1 + Section 2
  - 投入：30 min

### ⭐ 时间允许

1. **David Ha — World Models (interactive blog)**
  [https://worldmodels.github.io/](https://worldmodels.github.io/)
  - 已在必读里
  - 投入：30 min（细看交互 demo）

---

# 节点 8：GEN-1

### ⭐⭐⭐ 必读（20 min）

1. **Esser et al. — Structure and Content-Guided Video Synthesis with Diffusion Models** (Runway GEN-1, 2023)
  [https://arxiv.org/abs/2302.03011](https://arxiv.org/abs/2302.03011)
  - 必读 Abstract + Section 1 + Figure 2
  - 投入：15 min
2. **Runway Research — Gen-1 / Gen-2 / Gen-3 Pages**
  [https://research.runwayml.com/gen2](https://research.runwayml.com/gen2)
  - 官方介绍，看产品形态和能力 demo
  - 投入：5 min

### ⭐ 时间允许

1. **OpenAI — Sora Technical Report** (2024)
  [https://openai.com/research/video-generation-models-as-world-simulators](https://openai.com/research/video-generation-models-as-world-simulators)
  - Sora 的官方技术报告（不是论文，是 blog post）
  - 投入：20 min
  - 学到：video generation 走向 world simulator 的争论

---

# 节点 9：推理大模型 ⭐ 重点

### ⭐⭐⭐ 必读（60 min）

1. **OpenAI — Learning to Reason with LLMs** (o1 官方介绍, 2024.09)
  [https://openai.com/index/learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)
  - o1 的官方 blog，看 test-time compute scaling 的 figure（最重要的图）
  - 投入：15 min
2. **DeepSeek-AI — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning** (2025.01)
  [https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)
  - **必读全文**，R1 的完整训练 pipeline
  - 重点读 Abstract + Section 1 + Section 2 + Section 4
  - 投入：45 min
  - 学到：① RL-only 训练 reasoning 是可行的 ② cold-start data 的作用 ③ self-evolution 现象

### ⭐⭐ 强烈建议（额外 60 min）

1. **Snell et al. — Scaling LLM Test-Time Compute Optimally Can Be More Effective Than Scaling Model Parameters** (DeepMind 2024)
  [https://arxiv.org/abs/2408.03314](https://arxiv.org/abs/2408.03314)
  - 必读 Abstract + Section 1 + Figure 1/2
  - 投入：30 min
  - 学到：test-time compute scaling law 的精确陈述
2. **OpenAI — Introducing OpenAI o3 and o3-mini** (2024.12)
  [https://openai.com/12-days/](https://openai.com/12-days/)
  - o3 的官方介绍 + ARC-AGI 突破的演示
  - 投入：15 min
3. **Anthropic — Claude's Extended Thinking** (2025)
  [https://www.anthropic.com/news/visible-extended-thinking](https://www.anthropic.com/news/visible-extended-thinking)
  - Claude 加入推理能力的官方说明
  - 投入：15 min

### ⭐ 时间允许

1. **Sasha Rush — Speculations on Test-Time Scaling**
  [https://srush.github.io/awesome-o1/](https://srush.github.io/awesome-o1/)
  - Cornell 教授整理的 o1 / R1 相关资源
  - 投入：30 min

### ⭐⭐⭐ 2026 新增（必读 — 开源追平闭源的关键证据）

1. **DeepSeek-R2 解读** (decodethefuture, 2026.04)
  [https://decodethefuture.org/en/deepseek-r2-explained/](https://decodethefuture.org/en/deepseek-r2-explained/)
  - **R2 实际是 32B dense（不是传言中的 670B MoE）**
  - 92.7% AIME 2025 / 128K 上下文 / MIT license
  - **可在单张 24GB 消费 GPU 上运行**
  - 投入：15 min
2. **Reasoning Models Roundup 2026** (CrazyRouter)
  [https://crazyrouter.com/en/blog/openai-o3-vs-deepseek-r2-vs-kimi-k2-reasoning-models](https://crazyrouter.com/en/blog/openai-o3-vs-deepseek-r2-vs-kimi-k2-reasoning-models)
  - o3 vs R2 vs Kimi K2 横向对比
  - 投入：15 min
3. **OpenAI o3 系列时间线**
  - o3-preview announced 2024.12.20
  - o3-mini released 2025.01.31
  - o3 full release 2025.04.16
  - o3-pro released 2025.06.10
  - 参考：[https://openai.com/research/introducing-o3-and-o4-mini](https://openai.com/research/introducing-o3-and-o4-mini)
  - 投入：10 min

---

# 节点 10：VLA ⭐⭐ 全场命门

### ⭐⭐⭐ 必读（90 min）

1. **Brohan et al. — RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control** (Google DeepMind, 2023)
  [https://arxiv.org/abs/2307.15818](https://arxiv.org/abs/2307.15818)
  - **VLA 范式的开山之作，必读**
  - 重点读 Abstract + Section 1 + Section 3 + Figure 1/3
  - 投入：30 min
  - 学到：怎么把 VLM 的文本输出 token 化成机器人动作
2. **Physical Intelligence — π₀: Our First Generalist Policy** (官方博客, 2024.10)
  [https://www.physicalintelligence.company/blog/pi0](https://www.physicalintelligence.company/blog/pi0)
  - **π₀ 官方介绍**，必读
  - 投入：15 min
3. **Black et al. — π₀: A Vision-Language-Action Flow Model for General Robot Control** (论文)
  [https://arxiv.org/abs/2410.24164](https://arxiv.org/abs/2410.24164)
  - 必读 Abstract + Section 1 + Section 3 + Section 4.1
  - 投入：30 min
  - 学到：① diffusion-based action expert ② cross-embodiment 训练
4. **Figure AI — Helix: A Vision-Language-Action Model for Generalist Humanoid Control** (官方博客, 2025.02)
  [https://www.figure.ai/news/helix](https://www.figure.ai/news/helix)
  - **Helix 官方介绍**，必读 System 1 / System 2 双系统设计
  - 投入：15 min

### ⭐⭐ 强烈建议（额外 90 min）

1. **Kim et al. — OpenVLA: An Open-Source Vision-Language-Action Model** (2024)
  [https://arxiv.org/abs/2406.09246](https://arxiv.org/abs/2406.09246)
  - 开源 VLA 的代表，看训练 pipeline
  - 必读 Abstract + Section 1 + Section 3
  - 投入：30 min
2. **Physical Intelligence — π₀.₅: A VLA with Open-World Generalization** (2025.04)
  [https://www.physicalintelligence.company/blog/pi05](https://www.physicalintelligence.company/blog/pi05)
  - π₀ 的进化版
  - 投入：15 min
3. **NVIDIA — GR00T N1: An Open Foundation Model for Generalist Humanoid Robots** (2025)
  [https://research.nvidia.com/labs/gear/gr00t-n1/](https://research.nvidia.com/labs/gear/gr00t-n1/)
  - GR00T 官方介绍 + paper
  - 投入：30 min
  - 学到：vision encoder + LLM planner + diffusion action head 的现代 VLA 标准架构
4. **DeepMind — Gemini Robotics: Bringing AI into the Physical World** (2025.03)
  [https://deepmind.google/technologies/gemini-robotics/](https://deepmind.google/technologies/gemini-robotics/)
  - Google 入场具身的官方说明
  - 投入：15 min

### ⭐ 时间允许

1. **Chi et al. — Diffusion Policy: Visuomotor Policy Learning via Action Diffusion** (RSS 2023)
  [https://arxiv.org/abs/2303.04137](https://arxiv.org/abs/2303.04137)
  - VLA 用的 diffusion action 的源头
  - 投入：30 min
2. **Awesome VLA repo (GitHub)**
  [https://github.com/Jiaaqiliu/Awesome-VLA-Robotics](https://github.com/Jiaaqiliu/Awesome-VLA-Robotics)
  - 持续更新的 VLA 论文 / 模型清单
  - 投入：浏览 15 min

### ⭐⭐⭐ 2026 新增（必读 — 这部分是命门中的命门）

1. **Figure AI — Introducing Helix 02: Full-Body Autonomy** (2026.01.27，3 个月前)
  [https://www.figure.ai/news/helix-02](https://www.figure.ai/news/helix-02)
  - **必读**，Helix 02 官方介绍——三级架构（System 0 / 1 / 2），10M 参数神经网络替代 109,504 行 C++
  - 投入：20 min
  - 学到：洗碗机 4 分钟连续自主任务怎么做到的
2. **Figure AI — Helix 02 Living Room Tidy** (2026.03.09)
  [https://www.figure.ai/news/helix-02-living-room-tidy](https://www.figure.ai/news/helix-02-living-room-tidy)
  - 客厅整理 demo，Elon Musk 公开质疑真实性的那个
  - 投入：10 min
3. **Figure AI — Introducing Figure 03** (2025.10)
  [https://www.figure.ai/news/introducing-figure-03](https://www.figure.ai/news/introducing-figure-03)
  - 第三代人形机器人硬件，掌内嵌摄像头 + 触觉传感器（3 克级别力感知）
  - 投入：15 min
4. **NVIDIA — GR00T N1.5** (2025.06.11)
  [https://research.nvidia.com/labs/gear/gr00t-n1_5/](https://research.nvidia.com/labs/gear/gr00t-n1_5/)
  - **GR00T N1.5 官方页面**，重点看 FLARE 目标（从人类视频学习）
  - 投入：20 min
5. **NVIDIA Isaac-GR00T GitHub (含 N1.6 release notes, 2026.04.15)**
  [https://github.com/NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)
  - **GR00T N1.6 是 4 天前刚发布的**，重点看：
    - 内部 VLM 升级到 NVIDIA Cosmos-Reason-2B
    - Diffusion Transformer 翻倍（32 vs 16 层）
    - 训练时解冻 VLM 顶部 4 层
  - 投入：20 min
  - 学到：**VLA + World Model 融合首次进入产品级**的具体技术细节

### ⭐⭐⭐ 国内具身必读（强烈建议，演讲直接用）

1. **银河通用 GraspVLA** (2025.01.09)
  - 官方解读: [https://www.aibase.com/news/14630](https://www.aibase.com/news/14630)
  - **全球首个端到端具身抓取基础大模型** + 七大泛化金标准 + 10 亿帧合成数据预训练
  - 配套 Galbot 在 NVIDIA CES 2025 托举 RTX 5090 的视频值得看一下
  - 投入：15 min
2. **智元（AgiBot）GO-1** (2025.03.10)
  - 官方 paper: [https://agibot-world.com/blog/agibot_go1.pdf](https://agibot-world.com/blog/agibot_go1.pdf)
  - 全球新闻稿: [https://www.globenewswire.com/news-release/2025/03/11/3040608/0/en/AgiBot-GO-1-The-Evolution-of-Generalist-Embodied-Foundation-Model-from-VLA-to-ViLLA.html](https://www.globenewswire.com/news-release/2025/03/11/3040608/0/en/AgiBot-GO-1-The-Evolution-of-Generalist-Embodied-Foundation-Model-from-VLA-to-ViLLA.html)
  - **ViLLA 架构**（VLA → Vision-Language-Latent-Action）+ AgiBot World 数据集（100 万条 / 217 任务）
  - 投入：20 min
3. **宇树 UnifoLM-VLA-0** (2026)
  - 解读: [https://robohorizon.cn/zh/news/2026/03/unitree-g1-practical-skills/](https://robohorizon.cn/zh/news/2026/03/unitree-g1-practical-skills/)
  - 基于 Qwen2.5-VL-7B 的 VLA / 12 类操作任务 / 全部开源
  - 投入：15 min
  - **重点**：这是 Qwen 被国内具身公司用作 backbone 的真实案例

---

# 节点 11：World Models 突破

### ⭐⭐⭐ 必读（45 min）

1. **DeepMind — Genie 3: A new frontier for world models** (2025.08.05)
  [https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)
  - **必读**，Genie 3 官方博客 + demo 视频
  - **20-24 fps / 720p / 几分钟一致性**（不要被夸大数字误导）
  - 投入：20 min
2. **NVIDIA — Cosmos World Foundation Model Platform for Physical AI** (2025.01, CES 发布)
  [https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai](https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai)
  - **必读**，Cosmos 官方论文 + tech report
  - 重点读 Abstract + Section 1 + Section 3
  - 投入：30 min
  - 学到：world foundation model 的概念 + 为机器人/自动驾驶训练设计的目标 + 三个模型族（Predict / Transfer / Reason）
3. **NVIDIA Cosmos 官方页面**
  [https://www.nvidia.com/en-us/ai/cosmos/](https://www.nvidia.com/en-us/ai/cosmos/)
  - 看产品形态 + 早期采用者列表（Figure AI / Uber / Waabi）
  - 投入：10 min
4. **NVIDIA Tech Blog — Cosmos Reason 2 + GR00T N1.6** (2026.04)
  [https://developer.nvidia.com/blog/building-generalist-humanoid-capabilities-with-nvidia-isaac-gr00t-n1-6-using-a-sim-to-real-workflow/](https://developer.nvidia.com/blog/building-generalist-humanoid-capabilities-with-nvidia-isaac-gr00t-n1-6-using-a-sim-to-real-workflow/)
  - 4 天前发布的 Cosmos Reason 2（2B / 8B / 256K context）+ GR00T N1.6 集成
  - 投入：15 min
  - 学到：world model + VLA 融合的产品级实现细节

### ⭐⭐⭐ 重建侧（你主业最相关，立人设的核心抓手）

1. **3D Gaussian Splatting** (Inria, SIGGRAPH 2023 best paper)
  - 项目主页: [https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)
  - GitHub: [https://github.com/graphdeco-inria/gaussian-splatting/](https://github.com/graphdeco-inria/gaussian-splatting/)
  - 必读 Abstract + Section 1 + Section 4 + Figure 1
  - 投入：30 min
  - **重点**：3DGS 已经是你工作的一部分，但讲给非 SLAM 听众时**核心是"100+ fps 实时 + 训练几分钟达到 Mip-NeRF360 画质"** 这个对比
2. **DUSt3R / MASt3R** (Naver Labs, CVPR 2024)
  - DUSt3R 主页: [https://dust3r.europe.naverlabs.com/](https://dust3r.europe.naverlabs.com/)
  - MASt3R 解读: [https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/](https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/)
  - 必读 DUSt3R Abstract + Section 1
  - 投入：30 min
  - 学到：**transformer 替代传统 SfM/SLAM** 的范式 + "image matching as a 3D task"
3. **VGGT — Visual Geometry Grounded Transformer** (Meta + Oxford VGG, **CVPR 2025 Best Paper**) ⭐⭐⭐
  - 项目主页: [https://vgg-t.github.io/](https://vgg-t.github.io/)
  - GitHub: [https://github.com/facebookresearch/vggt](https://github.com/facebookresearch/vggt)
  - 论文: [https://arxiv.org/pdf/2503.11651](https://arxiv.org/pdf/2503.11651)
  - 必读 Abstract + Section 1 + Figure 1
  - 投入：40 min
  - **重点**：feed-forward transformer / 1 秒内输出相机参数+深度+点云+3D track / **完全不需要 bundle adjustment 后处理**
  - **这是你"重建 vs 生成汇合"判断最强的事实支撑——必须吃透**

### ⭐⭐ 强烈建议（额外 45 min）

1. **DeepMind — Genie 2: A large-scale foundation world model** (2024.12)
  [https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)
  - Genie 系列演进
  - 投入：15 min
2. **Bruce et al. — Genie: Generative Interactive Environments** (Genie 1 论文, ICML 2024)
  [https://arxiv.org/abs/2402.15391](https://arxiv.org/abs/2402.15391)
  - 必读 Abstract + Section 1 + Figure 1
  - 投入：20 min
3. **Tian et al. — Visual Autoregressive Modeling: Scalable Image Generation via Next-Scale Prediction** (NeurIPS 2024 Best Paper)
  [https://arxiv.org/abs/2404.02905](https://arxiv.org/abs/2404.02905)
  - 视觉 generative scaling 的最新代表（理解 world model 为什么能 scale）
  - 投入：30 min

### ⭐ 时间允许

1. **Yann LeCun — JEPA: A Path Towards Autonomous Machine Intelligence** (2022, 已在节点 7)
  - 节点 7 已列，重读用
  - 投入：30 min
2. **OpenAI — Video generation models as world simulators** (Sora technical report, 2024)
  [https://openai.com/research/video-generation-models-as-world-simulators](https://openai.com/research/video-generation-models-as-world-simulators)
  - Sora 的"world simulator" 论述（争议焦点）
  - 投入：20 min

---

# 全场补充：综述 + 时间线类材料

> 这部分**不是节点专属**，而是帮你建立全局视角的材料。建议周一晚上花 30 min 扫一下，建立认知地图。

### ⭐⭐⭐ 必读

1. **State of AI Report 2025** (Nathan Benaich)
  [https://www.stateof.ai/](https://www.stateof.ai/)
  - 业内最权威的年度 AI 总结，每年 10 月发布
  - 重点看 Research / Industry 两个 section 的 summary
  - 投入：30 min
2. **Stanford AI Index Report 2025**
  [https://aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/)
  - 学术 + 产业 + 政策的综合报告
  - 看 Executive Summary 即可
  - 投入：15 min

### ⭐⭐ 强烈建议

1. **Andrej Karpathy — Deep Dive into LLMs like ChatGPT** (YouTube, 2025.02)
  [https://www.youtube.com/watch?v=7xTGNNLPyMI](https://www.youtube.com/watch?v=7xTGNNLPyMI)
  - Karpathy 3.5 小时讲透 LLM 演进，非常好的串讲
  - 投入：60-90 min（1.5x 速度看精华段）
2. **Sebastian Raschka — Understanding Reasoning LLMs**
  [https://magazine.sebastianraschka.com/p/understanding-reasoning-llms](https://magazine.sebastianraschka.com/p/understanding-reasoning-llms)
  - 推理大模型的英文综述（节点 9 的最佳辅助阅读）
  - 投入：30 min

---

# 阅读策略建议

### 怎么读论文（应对你的"主动质疑"诉求）

每篇论文按这个顺序：

1. **读 Abstract**（2 min）—— 知道说了什么
2. **读 Introduction**（5 min）—— 知道为什么重要
3. **看 Figure 1/2/3 + Caption**（5 min）—— 抓核心思想
4. **跳读 Method**（5-10 min）—— 知道怎么做的，**不要陷数学**
5. **看 Results 主表 + 主图**（5 min）—— 知道效果

**全文细读 = 仅在你打算挑战这篇论文的时候做**。其他时候按上面 5 步走，每篇 20-30 min。

### 怎么应对追问

针对每个节点，强迫自己回答 3 个问题（你周二开始读时同步在 `07-qa-bank.md` 上对答案）：

1. **"这个为什么 work？"** — 直觉解释（不要只说"因为它是 X 架构"）
2. **"它解决了什么问题？前人怎么做的？"** — 历史对比
3. **"它有什么 limitation？"** — 没有任何技术是完美的，知道边界 = 知道这个技术

这 3 个问题如果都能答 30 秒，节点就吃透了。

### 不懂时怎么办

- **第一选择**：再读一次必读材料的对应章节
- **第二选择**：看 ⭐⭐ 的辅助资料
- **第三选择**：搜 "[concept] explained" + 限定 site:openai.com / site:deepmind.google / site:anthropic.com / site:lilianweng.github.io / site:karpathy.ai
- **第四选择**：问我（在 chat 里贴具体困惑点）—— 我会帮你诊断到底是哪一层不通

