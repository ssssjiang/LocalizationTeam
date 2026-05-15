# AI 演进笔记学习清单（按 `08-knowledge-doc.md`）

> **使用方式**
>
> - 周一至周四每晚约 3h，按「必读 → 强烈建议 → 时间允许」顺序读。
> - 全部优先选英文原文 / 官方博客 / 顶会论文 / 学校课程 / 权威讲座；**不含知乎 / CSDN**。
> - 图解优先：Jay Alammar、Colah、Lilian Weng、Karpathy 这类材料优先于纯论文。
> - YouTube / 公开视频优先保留，方便边走边听；但必须来自课程、论文作者、权威研究者或官方渠道。
> - 论文只读关键部分：Abstract / Introduction / Figure 1-3 / Method 核心段 / 主结果表。
> - 每个节点标「最低投入」和「完整投入」；目标不是读完所有材料，而是配合 `08-knowledge-doc.md` 吃透每章核心逻辑。

## 时间预算建议


| 章节                  | 最低投入    | 完整投入    | 备注                              |
| ------------------- | ------- | ------- | ------------------------------- |
| 1 整体趋势              | 30 min  | 60 min  | 建时间线，不深挖                        |
| 2 判别式 AI            | 60 min  | 150 min | CNN / RNN / ResNet 基础           |
| 3 Transformer / LLM | 120 min | 240 min | 重点，必须吃透                         |
| 4 Diffusion         | 90 min  | 210 min | 思想 > 数学，按 VAE→GAN→Diffusion 谱系串 |
| 5 VLM 与多模态理解        | 60 min  | 150 min | CLIP + LLaVA 是核心                |
| 6 具身 VLA            | 150 min | 300 min | VLM → action，动作表示，连续控制          |
| 7 World Models 近期形态 | 60 min  | 195 min | Genie / Cosmos                  |
| 补充：开放问题             | 60 min  | 150 min | VLA 泛化 + 3D 重建                  |


**最低总投入**：约 10.5h
**完整投入**：约 24.25h

**4 晚 12h 推荐分配**：

- 周一晚：§3 Transformer / LLM
- 周二晚：§6 具身 VLA
- 周三晚：§4 Diffusion + §5 VLM 与多模态理解
- 周四晚：§2 / §7 / 开放问题快速补齐 + 全文串讲一次

---

# 章节 1：整体趋势

### ⭐⭐⭐ 必读（30 min）

1. **State of AI Report 2025**
  [https://www.stateof.ai/](https://www.stateof.ai/)
  - 只读 Research / Industry 两个 section 的 summary。
  - 投入：20 min
  - 学到：2025 前后 AI 产业和研究主线如何被外部报告归纳。
2. **Stanford AI Index Report 2025**
  [https://aiindex.stanford.edu/report/](https://aiindex.stanford.edu/report/)
  - 只看 Executive Summary。
  - 投入：10 min
  - 学到：模型、算力、产业采用、政策侧的宏观背景。

### ⭐⭐ 强烈建议（额外 30 min）

1. **Jürgen Schmidhuber — Annotated History of Modern AI and Deep Learning**
  [http://people.idsia.ch/~juergen/deep-learning-history.html](http://people.idsia.ch/~juergen/deep-learning-history.html)
  - 只扫目录和关键年份，不需要逐段读。
  - 投入：30 min
  - 学到：深度学习不是 2012 才开始，但 2012 后进入工程爆发期。

---

# 章节 2：判别式 AI（CNN / RNN / ResNet）

### ⭐⭐⭐ 必读（60 min）

1. **Stanford CS231n — Convolutional Neural Networks**
  [https://cs231n.github.io/convolutional-networks/](https://cs231n.github.io/convolutional-networks/)
  - 只读 "Architecture Overview" + "Layer Patterns"。
  - 投入：25 min
  - 学到：CNN 为什么能学图像特征，卷积 / pooling 的物理意义。
2. **Christopher Olah — Understanding LSTMs**
  [https://colah.github.io/posts/2015-08-Understanding-LSTMs/](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
  - 重点看 cell state、forget gate、input gate、output gate 的图。
  - 投入：20 min
  - 学到：RNN 为什么容易梯度衰减，LSTM 如何用门控和加法路径缓解。
3. **He et al. — Deep Residual Learning for Image Recognition**
  [https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)
  - 读 Abstract + Section 1 + Section 3 + Table 4。
  - 投入：15 min
  - 学到：degradation problem、`F(x)+x`、ResNet 为什么能训深。

### ⭐⭐ 强烈建议（额外 60 min）

1. **Zeiler & Fergus — Visualizing and Understanding CNNs**
  [https://arxiv.org/abs/1311.2901](https://arxiv.org/abs/1311.2901)
  - 只看 Figure 2 + §2 deconvnet 思路。
  - 投入：15 min
  - 学到：CNN 层级特征不是猜测，是被可视化证实的。
2. **He et al. — Identity Mappings in Deep Residual Networks**
  [https://arxiv.org/abs/1603.05027](https://arxiv.org/abs/1603.05027)
  - 只读 Section 1 + Section 3。
  - 投入：25 min
  - 学到：identity mapping 在前向 / 反向传播里的作用。
3. **3Blue1Brown — Neural Networks**
  [https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
  - 看第 1-4 集即可。
  - 投入：20 min
  - 学到：神经网络、梯度下降、反向传播的直觉。

---

# 章节 3：Transformer / LLM

### ⭐⭐⭐ 必读（120 min）

1. **Jay Alammar — The Illustrated Transformer**
  [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
  - 这是 Transformer 第一学习入口。
  - 投入：45 min
  - 学到：encoder-decoder、Q/K/V、multi-head attention、position encoding。
2. **Vaswani et al. — Attention Is All You Need**
  [https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
  - 读 Abstract + Section 1 + Section 3 + Figure 1。
  - 投入：30 min
  - 学到：Transformer 完整结构定义，以及为什么去掉 RNN / CNN。
3. **Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out**
  [https://www.youtube.com/watch?v=kCc8FmEb1nY](https://www.youtube.com/watch?v=kCc8FmEb1nY)
  - 看 0:00-0:35，重点是 self-attention。
  - 投入：45 min
  - 学到：从代码角度理解 attention 到底在算什么。

### ⭐⭐ 强烈建议（额外 90 min）

1. **Lilian Weng — Attention? Attention!**
  [https://lilianweng.github.io/posts/2018-06-24-attention/](https://lilianweng.github.io/posts/2018-06-24-attention/)
  - 重点看 Bahdanau attention → self-attention → Transformer 的演进。
  - 投入：30 min
  - 学到：attention 不是 Transformer 首创，Transformer 的变化是把 attention 作为主干。
2. **Scaling Laws and LLMs**
  [https://datafield.dev/aibook/part-04/chapter-22/index.html](https://datafield.dev/aibook/part-04/chapter-22/index.html)
  - 读 Kaplan / Chinchilla / emergence 三段。
  - 投入：30 min
  - 学到：参数、数据、计算量为什么能形成可预测关系。
3. **Ouyang et al. — Training language models to follow instructions with human feedback**
  [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
  - 只读 Abstract + Figure 2。
  - 投入：30 min
  - 学到：SFT / reward model / PPO 三步 RLHF pipeline。

### ⭐ 时间允许

1. **李沐 — Attention Is All You Need 论文逐段精读**
  [https://www.bilibili.com/video/BV1pu411o7BE/](https://www.bilibili.com/video/BV1pu411o7BE/)
  - 权威论文讲解视频，适合散步或通勤听。
  - 投入：60 min（1.5x 速度）

---

# 章节 4：Diffusion

> 学习目标：把 **VAE → GAN → Diffusion** 串成一条线，理解生成式模型的演进；不追数学推导，先建直觉。

### ⭐⭐⭐ 必读（90 min）

1. **MIT 6.S191 (2024) Lecture 4 — Deep Generative Modeling (Ava Amini)**
  [https://www.youtube.com/watch?v=Dmm4UG-6jxA](https://www.youtube.com/watch?v=Dmm4UG-6jxA)
  - 把 latent variable model → VAE（reparameterization trick）→ GAN（CycleGAN）→ Diffusion 串成一条主线讲。
  - 投入：38 min（1.5x 速度）
  - 学到：生成式模型为什么从 explicit density（VAE）→ implicit（GAN）→ score / denoising（Diffusion），各自解决了前一棒的什么问题。
2. **Lilian Weng — What are Diffusion Models?**
  [https://lilianweng.github.io/posts/2021-07-11-diffusion-models/](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
  - 先看图和 forward / reverse process，不要陷推导。
  - 投入：35 min
  - 学到：DDPM、score-based、denoising 的统一直觉。
3. **Ari Seff — What are Diffusion Models? (YouTube, 17 min)**
  [https://www.youtube.com/watch?v=fbLgFrlTnGU](https://www.youtube.com/watch?v=fbLgFrlTnGU)
  - Princeton 研究者，17 分钟把 Markov chain、variational lower bound、噪声预测、score matching 等价性串完。
  - 投入：17 min（1x 听一遍即可）
  - 学到：为什么训练目标是「预测噪声」而不是直接生成图像；DDPM 与 score-based 模型本质同构。

### ⭐⭐ 强烈建议（额外 95 min）

1. **Diffusion Explainer — Polo Club @ Georgia Tech**
  [https://poloclub.github.io/diffusion-explainer/](https://poloclub.github.io/diffusion-explainer/)
  - IEEE VIS 2024 论文支撑（[arXiv 2305.03509](https://arxiv.org/abs/2305.03509)）；浏览器交互式教学，可拖时间步、改 prompt、看 cross-attention。
  - 投入：25 min
  - 学到：Stable Diffusion 文生图整条管线（text encoder → latent → image refiner → denoising）每一步在算什么。
2. **Ho et al. — Denoising Diffusion Probabilistic Models**
  [https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
  - 看 Abstract + Algorithm 1/2，确认训练 / 采样的具体形式。
  - 投入：15 min
  - 学到：DDPM 经典论文是哪一篇、训练目标怎么写。
3. **Rombach et al. — Latent Diffusion Models**
  [https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
  - 看 Abstract + Section 3 + Figure 3。
  - 投入：30 min
  - 学到：Stable Diffusion 为什么能在消费级 GPU 上跑（在 latent 空间扩散，不是像素空间）。
4. **Hugging Face Diffusion Course — Unit 1**
  [https://huggingface.co/learn/diffusion-course/unit1/1](https://huggingface.co/learn/diffusion-course/unit1/1)
  - 只看 Introduction + sampling 概念。
  - 投入：25 min
  - 学到：scheduler / denoising / inference pipeline 的工程视角。

### ⭐ 时间允许

1. **Song et al. — DDIM**
  [https://arxiv.org/abs/2010.02502](https://arxiv.org/abs/2010.02502)
  - 只读 Abstract + Section 1。
  - 投入：15 min
  - 学到：为什么可以从 1000 步采样压到几十步。
2. **The Annotated Diffusion Model — Hugging Face 官方博客**
  [https://huggingface.co/blog/annotated-diffusion](https://huggingface.co/blog/annotated-diffusion)
  - *Annotated Transformer* 同款风格：PyTorch 代码 + 数学 + 文字解释逐段交错，可在 Colab 跑。
  - 投入：30 min
  - 学到：`q_sample` / `p_losses` / `sample` 三个核心函数的实现细节。

---

# 章节 5：VLM 与多模态理解

### ⭐⭐⭐ 必读（60 min）

1. **OpenAI Blog — CLIP: Connecting Text and Images**
  [https://openai.com/research/clip](https://openai.com/research/clip)
  - 先看官方博客和图，不先啃论文。
  - 投入：20 min
  - 学到：图文为什么可以放进同一个 embedding space。
2. **Radford et al. — CLIP**
  [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
  - 读 Abstract + Section 2.3 + zero-shot 分类部分。
  - 投入：25 min
  - 学到：InfoNCE、positive / negative pair、zero-shot。
3. **LLaVA GitHub**
  [https://github.com/haotian-liu/LLaVA](https://github.com/haotian-liu/LLaVA)
  - 看模型图、training data、release note。
  - 投入：15 min
  - 学到：vision encoder + projection + LLM 的最小 VLM 框架。

### ⭐⭐ 强烈建议（额外 60 min）

1. **Liu et al. — Visual Instruction Tuning**
  [https://arxiv.org/abs/2304.08485](https://arxiv.org/abs/2304.08485)
  - 读 Abstract + Section 1 + Section 3。
  - 投入：30 min
  - 学到：GPT-4 生成视觉指令数据、两阶段训练。
2. **Vision Language Models study plan**
  [https://pixelbank.dev/vlm-study-plan](https://pixelbank.dev/vlm-study-plan)
  - 只看目录和 CLIP / LLaVA 章节。
  - 投入：30 min
  - 学到：VLM 技术地图。

---

# 章节 6：具身 VLA

> 学习目标：先把 **VLM → VLA** 的接口变化讲清楚，再看动作表示怎么从 token 走向 action chunk / flow matching。读模型列表前，先回答一个问题：机器人动作为什么不能只当成普通文本 token？

### 资料权威性核对

| 资料 | 权威性判断 | 适合放在本章的位置 |
| --- | --- | --- |
| **Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications** | arXiv 综述，作者来自 University of Tokyo / Oxford / UT Austin，覆盖 VLA 定义、架构、训练、数据、平台和评估；适合作为全栈框架参考，不作为单个模型指标的唯一来源。 | 主骨架：定义 VLA、梳理发展阶段、列挑战 |
| **A Survey on Vision-Language-Action Models: An Action Tokenization Perspective** | arXiv 综述，作者来自 PKU / PKU-PsiBot Joint Lab；视角集中在 action token taxonomy，适合作为教程解释“动作怎么表示”。 | 教程核心：action token / trajectory / latent / raw action |
| **Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey** | arXiv 综述，作者来自 HIT Shenzhen，聚焦 large VLM-based VLA；适合解释 VLM backbone、single-system / dual-system / hierarchical 三类结构。 | 承接 §5：VLM 怎么接到 action expert |
| **A Pragmatic VLA Foundation Model (LingBot-VLA)** | arXiv 原始模型论文，配套公开 code、base model、benchmark data；适合作为国内公开工程路线案例，不是综述。 | 案例：Qwen2.5-VL + MoT + Flow Matching |

### ⭐⭐⭐ 必读（150 min）

1. **Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications**
  [https://arxiv.org/pdf/2510.07077](https://arxiv.org/pdf/2510.07077)
  - 读 Abstract + Definition I.1 + Figure 1/2 + Section III。
  - 投入：45 min
  - 学到：VLA 的严格定义：输入视觉观测和自然语言指令，输出机器人控制命令；以及 VLA 为什么需要同时处理数据、embodiment、算力和部署问题。
2. **A Survey on Vision-Language-Action Models: An Action Tokenization Perspective**
  [https://arxiv.org/abs/2507.01925](https://arxiv.org/abs/2507.01925)
  - 读 Abstract + Executive Summary + Figure 1 + action token taxonomy。
  - 投入：40 min
  - 学到：动作不只有 raw action，还可以是 language description、code、affordance、trajectory、goal state、latent representation、reasoning；这一篇用来支撑 §6 的教程主线。
3. **RT-2 project page**
  [https://robotics-transformer2.github.io/](https://robotics-transformer2.github.io/)
  - 先看项目页 demo 和图，再读论文。
  - 投入：25 min
  - 学到：VLM 如何把机器人动作离散化成 action token。
4. **openpi / π 系列**
  [https://github.com/Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi)
  - 看 README 的 model list、requirements、checkpoint table。
  - 投入：40 min
  - 学到：π₀ / π₀-FAST / π₀.5 如何用 VLM backbone + flow matching action head 表示连续动作。

### ⭐⭐ 强烈建议（额外 150 min）

1. **Large VLM-based Vision-Language-Action Models for Robotic Manipulation: A Survey**
  [https://arxiv.org/abs/2508.13073](https://arxiv.org/abs/2508.13073)
  - 读 Abstract + Figure 2/3 + Section 2.1 / 2.2 + monolithic / hierarchical taxonomy。
  - 投入：40 min
  - 学到：VLM-based VLA 如何分成 single-system、dual-system、hierarchical；这一篇适合用来承接 §5 的 VLM。
2. **Brohan et al. — RT-2**
  [https://arxiv.org/abs/2307.15818](https://arxiv.org/abs/2307.15818)
  - 读 Abstract + Section 1 + Figure 1/3。
  - 投入：30 min
  - 学到：VLM → VLA 的早期标准做法：把动作作为 token 接到语言模型输出端。
3. **Kim et al. — OpenVLA**
  [https://arxiv.org/abs/2406.09246](https://arxiv.org/abs/2406.09246)
  - 读 Abstract + Section 1 + Section 3。
  - 投入：25 min
  - 学到：Open X-Embodiment + 7B VLA，为什么 OpenVLA 适合作开源 baseline。
4. **A Pragmatic VLA Foundation Model (LingBot-VLA)**
  [https://arxiv.org/abs/2601.18692](https://arxiv.org/abs/2601.18692)
  - 读 Abstract + Section 4.1 + Figure 1 + 数据与评估概览。
  - 投入：30 min
  - 学到：LingBot-VLA 如何用 Qwen2.5-VL、Mixture-of-Transformers 和 Flow Matching 做连续动作建模；为什么它适合作为国内公开工程路线案例。
5. **NVIDIA Isaac-GR00T GitHub**
  [https://github.com/NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)
  - 看 N1.7 release / model card / license。
  - 投入：25 min
  - 学到：GR00T 如何把 VLM reasoning 和 diffusion action head 组合起来。

### ⭐ 时间允许

1. **Google DeepMind — Gemini Robotics**
  [https://deepmind.google/technologies/gemini-robotics/](https://deepmind.google/technologies/gemini-robotics/)
  - 看 Gemini Robotics / ER 的产品页。
  - 投入：20 min
  - 学到：VLA + embodied reasoning 双模型组合。
2. **OpenVLA project page**
  [https://openvla.github.io/](https://openvla.github.io/)
  - 看 architecture / dataset / results。
  - 投入：20 min
  - 学到：开源 VLA baseline 的训练和部署入口。

---

# 章节 7：World Models 近期形态

### ⭐⭐⭐ 必读（60 min）

1. **DeepMind — Genie 3**
  [https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models)
  - 看官方 demo 和能力边界。
  - 投入：20 min
  - 学到：interactive world model 和普通视频生成的差别。
2. **NVIDIA Cosmos docs**
  [https://docs.nvidia.com/cosmos/latest/introduction.html](https://docs.nvidia.com/cosmos/latest/introduction.html)
  - 看 Introduction + model family。
  - 投入：20 min
  - 学到：Predict / Transfer / Reason 分别做什么。
3. **Cosmos World Foundation Models paper**
  [https://arxiv.org/html/2501.03575](https://arxiv.org/html/2501.03575)
  - 读 Abstract + Section 1 + platform overview。
  - 投入：20 min
  - 学到：Cosmos 作为 physical AI stack 的定位。

### ⭐⭐ 强烈建议（额外 105 min）

1. **DeepMind — Genie 2**
  [https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)
  - 投入：20 min
  - 学到：Genie 1 → 2 → 3 的演进。
2. **OpenAI — Video generation models as world simulators**
  [https://openai.com/research/video-generation-models-as-world-simulators](https://openai.com/research/video-generation-models-as-world-simulators)
  - 投入：20 min
  - 学到：Sora 的 world simulator 论述和争议点。
3. **NVIDIA Cosmos official page**
  [https://www.nvidia.com/en-us/ai/cosmos/](https://www.nvidia.com/en-us/ai/cosmos/)
  - 投入：20 min
  - 学到：产品形态和 early adopter。
4. **Hou et al. — World Model for Robot Learning: A Comprehensive Survey**
  [https://arxiv.org/html/2605.00080v1](https://arxiv.org/html/2605.00080v1)
  - 读 Abstract + Figure 1/2 + Section 3/4/5 taxonomy + open challenges。
  - 投入：45 min
  - 学到：world model 如何在机器人学习里连接 VLA policy、learned simulator、video generation、planning / evaluation / data generation。

---

# 补充：开放问题

### ⭐⭐⭐ 必读（60 min）

1. **Vision-Language-Action Models for Robotics: A Review Towards Real-World Applications**
  [https://arxiv.org/pdf/2510.07077](https://arxiv.org/pdf/2510.07077)
  - 看 generalization / real-world deployment / data scaling 相关章节。
  - 投入：30 min
  - 学到：home / long-tail 泛化为什么难。
2. **DUSt3R GitHub**
  [https://github.com/naver/dust3r](https://github.com/naver/dust3r)
  - 看 README demo + method 图。
  - 投入：15 min
  - 学到：feed-forward 3D reconstruction 如何替代部分 SfM pipeline。
3. **VGGT project**
  [https://vgg-t.github.io/](https://vgg-t.github.io/)
  - 看 Figure 1 + demo。
  - 投入：15 min
  - 学到：Transformer 一次性预测 camera / depth / point map / track。

### ⭐⭐ 强烈建议（额外 90 min）

1. **3D Gaussian Splatting**
  [https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)
  - 看项目页图和 abstract。
  - 投入：30 min
  - 学到：explicit 3D 表示如何支撑实时渲染。
2. **DUSt3R paper**
  [https://arxiv.org/abs/2312.14132](https://arxiv.org/abs/2312.14132)
  - 读 Abstract + Figure 1。
  - 投入：30 min
  - 学到：image matching as 3D task。
3. **VGGT paper**
  [https://arxiv.org/pdf/2503.11651](https://arxiv.org/pdf/2503.11651)
  - 读 Abstract + Section 1 + Figure 1。
  - 投入：30 min
  - 学到：feed-forward geometry foundation model 的能力边界。

---

# 阅读策略

## 怎么读论文

每篇论文按这个顺序：

1. 读 Abstract：知道说了什么。
2. 读 Introduction：知道为什么重要。
3. 看 Figure 1/2/3 + caption：抓核心思想。
4. 跳读 Method：知道怎么做，**不要陷数学**。
5. 看 Results 主表：知道效果。

全文细读只用于你准备挑战这篇论文时。其他时候每篇控制在 20-30 min。

## 怎么应对追问

针对每个章节，强迫自己回答 3 个问题：

1. 这个为什么 work？
2. 它解决了什么问题？前人怎么做？
3. 它有什么 limitation？

这 3 个问题如果都能答 30 秒，就说明这个节点能讲给同事听。

## 不懂时怎么办

- 第一选择：再看图解 / 官方博客。
- 第二选择：看权威视频讲解。
- 第三选择：读论文 Abstract + Figure。
- 第四选择：把具体卡住的句子贴出来问我。

