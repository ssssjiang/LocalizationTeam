# AI 演进笔记 (2012-2026)

## 1. 整体趋势

2012-2026 间 AI 演进经历 5 个 foundation 阶段（判别式 → Transformer → 视觉与视频生成 → 多模态理解 → World Models 起源）与 2 个延伸方向（具身 VLA / World Models 近期形态）。主线时间锚点：

- **2012-2015 判别式 AI**：AlexNet (NeurIPS 2012) / VGG / GoogLeNet / ResNet (CVPR 2016) — CNN 端到端特征学习
- **2017 Transformer**：Vaswani et al. — self-attention 替代 RNN，LLM 工业化基础
- **2020-2022 LLM scaling**：GPT-3 (NeurIPS 2020) / Chinchilla (NeurIPS 2022) / ChatGPT (2022-11)
- **2020-2024 视觉与视频生成**：DDPM (NeurIPS 2020) → Stable Diffusion (2022-08) → Sora (2024-02)
- **2020-2024 多模态理解**：CLIP (ICML 2021) → GPT-4V (2023-09) → LLaVA (NeurIPS 2023)
- **2018 / 2023 World Models 起源**：Ha & Schmidhuber (NeurIPS 2018) V+M+C / Runway GEN-1 (2023-02)
- **2023-2026 具身 VLA**：RT-2 (2023-07) → π₀ (2024-10) → π₀.7 (2026-04-16) / Helix 02 (2026-01) / GR00T N1.7 (2026-04-17)
- **2024-2026 World Models 近期形态**：Genie 3 (2025-08) / Cosmos (2025-01 起)

本笔记 narrative arc 是「演进路径 + 应用扩展 + 解决什么问题」。覆盖 AI 整体演进的主线脉络（CNN/RNN → ResNet → Transformer → LLM → Diffusion → CLIP/VLM → World Models / VLA），不做 frontier 模型横扫（具体 model 列表见 `09-sweeper-embodied-roadmap.md` §1 行业技术现状地图）。LLM 推理大模型（OpenAI o1 / o3、DeepSeek R1 / R2、Qwen3-Max-Thinking、Kimi K2.5 等）极简介绍仅在 §7.2.1 VLA + 推理融合 节内 inline 200 字 background 出现。

## 2. 第一阶段：判别式 AI (2012-2015)

2012-2015 间，CNN / RNN / ResNet 在视觉端到端特征学习、序列建模、深网络优化退化三个方向出现关键工作；后续 Transformer / Diffusion / VLA 等架构沿用其中的核心组件（CNN backbone、ResNet 残差连接）。

### 2.1 CNN：视觉端到端特征学习

AlexNet (Krizhevsky et al., NeurIPS 2012)[1] 在 ImageNet ILSVRC-2012（1.2M 图像 / 1000 类）上把 top-5 错误率从 SIFT-FV (Fisher Vector) baseline 的 25.8% 降到 16.4%[1, 2]。同期 SIFT / HOG + classifier 的 hand-crafted pipeline 被替换为 end-to-end CNN：raw RGB pixel → 卷积层堆叠 → softmax 分类。

#### 关键设计

AlexNet 的关键构件[1]：

- 5 层卷积 + 3 层全连接，60M 参数
- ReLU 激活函数（替代 sigmoid / tanh）加速收敛
- Dropout (Hinton et al., 2012)[3] 减轻过拟合
- 双 GPU 数据并行（NVIDIA GTX 580，3GB VRAM × 2；当时单 GPU 内存放不下完整模型）
- Local Response Normalization（后续被 BatchNorm 替代）

#### 后续推进

后续工作沿同一范式深化：

- VGG (Simonyan & Zisserman, ICLR 2015)[4]：加深到 16-19 层，全部用 3×3 卷积；ImageNet top-5 错误率 7.32%
- GoogLeNet / Inception (Szegedy et al., CVPR 2015)[5]：Inception module 多尺度分支并联；top-5 6.67%，参数量较 VGG 小 ~12×
- LeNet (LeCun et al., Proc. IEEE 1998)[6]：首个卷积 + pooling + 全连接架构，应用于 MNIST 手写体识别；AlexNet 在大规模数据 + GPU 算力下扩展了 LeNet 思路

### 2.2 RNN：序列建模

RNN (Recurrent Neural Network) 通过 hidden state 在时序上的递归传递处理序列数据。1980-1990s 提出，实用化集中在 2014-2017 年（Sutskever 2014 seq2seq[7]、Bahdanau 2014 attention[8]）。

#### 主要 variant

- **vanilla RNN**：hidden state h_t = tanh(W_h h_{t-1} + W_x x_t)；长序列梯度衰减 / 爆炸严重
- **LSTM** (Hochreiter & Schmidhuber, Neural Computation 1997)[9]：引入 input / forget / output 三门控 + cell state，缓解长序列梯度衰减；2014-2017 年是 NMT / speech 主流 backbone
- **GRU** (Cho et al., EMNLP 2014)[10]：简化 LSTM 为 update / reset 两门，参数比 LSTM 少 ~25%，多数任务上性能相当

#### 应用

RNN 推动了两个领域的端到端化：

- **NMT** (Neural Machine Translation)：Sutskever et al. (NeurIPS 2014)[7] 用 encoder-decoder LSTM 在 WMT'14 EN-FR 上达到 BLEU 34.81（vs phrase-based SMT 33.30）
- **Speech recognition**：DeepSpeech (Hannun et al., 2014)[11] 用 RNN + CTC loss 替代传统 HMM-GMM pipeline，WER 在 Switchboard 上 16%（vs 商业 baseline 18.4%）

#### 已知局限

RNN 在 2017 年后被 Transformer 在 NMT / LM 主线快速取代，主要因：

- **串行依赖**：当前 step 依赖前一 step hidden state，无法 GPU 并行
- **长距离依赖衰减**：即使 LSTM 也只能稳定捕获 ~100-1000 step 内信息
- 这两条 Transformer (Vaswani et al., NeurIPS 2017)[12] 同时解决

### 2.3 ResNet 与残差连接

ResNet 引入残差连接 `y = F(x) + x`[13]，解决了深网络的优化退化（degradation）问题。该机制后续在 Transformer[12]、Diffusion U-Net、具身机器人模型的视觉 head 等主流架构的 block 中被沿用，成为不绑定具体任务范式的通用组件。

#### 历史背景与退化现象

ResNet (He et al., 2015-12)[13] 之前，Highway Networks (Srivastava et al., NeurIPS 2015)[14] 已提出"门控 + 恒等通路"的思路：每层输出为 `y = T(x) · F(x) + (1 − T(x)) · x`，T(x) 是受 LSTM 启发的 sigmoid 门控函数。Highway 网络可训练 100+ 层，但门控参数随深度增加难以稳定收敛。

CNN 深度从 20 层加到 56 层时，训练误差与测试误差同时升高[13]。这一现象不能用过拟合解释——若是过拟合，训练误差应继续下降。该现象被归因为优化层面的退化：随深度增加，SGD (stochastic gradient descent) 在更复杂的损失曲面上更难找到与浅层网络等价的解[13]。Li et al. (NeurIPS 2018) 通过损失曲面可视化进一步证实，残差连接显著平滑了深网络的损失曲面，使 SGD 更易收敛[15]。

ResNet 把 Highway 的 T(x) 固定为 1，简化为无门控的恒等加和 `y = F(x) + x`，参数更少、训练更稳定，并在 ImageNet 上得到验证。

#### 机制

每个 block 的输出由 `y = F(x)` 改为 `y = F(x) + x`[13]。F 学到 0 时 block 退化为恒等映射；更深的网络至少不会比更浅的等价网络更差，给优化器一条保底通路。

反向传播时，残差连接为梯度提供一条 unit-multiplier 通路：`∂L/∂x = ∂L/∂y · (1 + ∂F/∂x)`。即使 F 部分的梯度衰减为 0，外层梯度也能经 `1` 这条通路直接传至浅层，缓解深网络中常见的梯度衰减问题[13]。

ResNet 用了两种 block 设计[13]：

- **Basic block**（用于 ResNet-18 / 34）：两个 3×3 卷积 + 残差加和
- **Bottleneck block**（用于 ResNet-50 / 101 / 152）：1×1 → 3×3 → 1×1 三层卷积 + 残差加和。1×1 卷积先压缩通道再恢复，参数与计算量约为 basic block 的一半

He et al. 在 Pre-activation 工作（ECCV 2016）[16] 把 BN 与 ReLU 移到卷积之前（即 BN-ReLU-Conv 而非 Conv-BN-ReLU），让残差通路更接近纯恒等映射，可训练深度从 152 层扩展到 1001 层。

#### 直接效果

ResNet 在 ImageNet 上的 top-5 错误率随深度变化（来源：[13] Table 4，single-model single-crop）：


| 模型         | 错误率   | 参数量   |
| ---------- | ----- | ----- |
| ResNet-18  | 7.55% | 11.7M |
| ResNet-34  | 6.50% | 21.8M |
| ResNet-50  | 5.71% | 25.6M |
| ResNet-101 | 5.05% | 44.5M |
| ResNet-152 | 4.49% | 60.2M |


ResNet-152 ensemble 后达到 3.57%[13]。同期对照：GoogLeNet 6.67%、VGG 7.32%、AlexNet (2012) 16.4%。

ResNet 在一年内取代 VGG / GoogLeNet 成为下游 CV 任务的默认 backbone：COCO 目标检测 mAP 从 33.5（VGG-Faster R-CNN）提升到 37.4（ResNet-101-Faster R-CNN）[13]；ImageNet localization 错误率从 19.4% 降到 9.0%[13]。

#### 后续理论解释 (ensemble view + loss landscape)

Veit et al. (NeurIPS 2016)[17] 提出 ResNet 行为更接近"相对浅网络的 ensemble"：在已训练的 ResNet 中删除任意一个 block，输出几乎不变；这表明残差通路提供了多条并行路径，网络的实际有效深度远小于其名义深度。该机制层面的两类解释——He et al. 的 identity mapping 通路[13] 与 Veit et al. 的 ensemble 路径[17]——均有论文支撑且并不互斥，提示残差连接可能同时提供了"恒等映射的可达性"与"梯度路径的多样性"两类作用。

#### 跨架构延续

残差连接在多种主流架构中以不同形式出现：

- **Transformer**：每个 sub-layer 后采用 `LayerNorm(x + Sublayer(x))`，其中 `+` 即残差连接[12]
- **DenseNet** (Huang et al., CVPR 2017)[18]：把 sum 改为前序所有层的 concat，使每层都能直接看到所有前序特征
- **ResNeXt** (Xie et al., CVPR 2017)[19]：在残差通路内引入分组卷积，把"加深 / 加宽"扩展为"加 cardinality"
- **Diffusion U-Net**：encoder / decoder 之间用 skip connection 跨层 concat，结构上是残差思路的另一变种
- **具身机器人模型** 的视觉 / 动作 head 的基础 block 多含残差结构

CNN 的卷积、RNN 的循环是架构特异性的归纳偏置；残差连接不绑定具体任务范式，仅为深网络优化提供一条线性通路。这一架构无关属性使其在 CNN[13]、Transformer[12]、Diffusion U-Net、具身视觉 head 等不同范式中均有沿用，且常与各架构原有的归纳偏置（卷积、attention 等）正交叠加。

### References

- [1] Krizhevsky et al., ImageNet Classification with Deep Convolutional Neural Networks, NeurIPS 2012. papers.nips.cc/paper/4824
- [2] Russakovsky et al., ImageNet Large Scale Visual Recognition Challenge, IJCV 2015. arXiv:1409.0575
- [3] Hinton et al., Improving neural networks by preventing co-adaptation of feature detectors, arXiv 2012. arXiv:1207.0580
- [4] Simonyan & Zisserman, Very Deep Convolutional Networks for Large-Scale Image Recognition, ICLR 2015. arXiv:1409.1556
- [5] Szegedy et al., Going Deeper with Convolutions, CVPR 2015. arXiv:1409.4842
- [6] LeCun et al., Gradient-Based Learning Applied to Document Recognition, Proc. IEEE 1998.
- [7] Sutskever et al., Sequence to Sequence Learning with Neural Networks, NeurIPS 2014. arXiv:1409.3215
- [8] Bahdanau et al., Neural Machine Translation by Jointly Learning to Align and Translate, ICLR 2015. arXiv:1409.0473
- [9] Hochreiter & Schmidhuber, Long Short-Term Memory, Neural Computation 1997.
- [10] Cho et al., Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation, EMNLP 2014. arXiv:1406.1078
- [11] Hannun et al., Deep Speech: Scaling up end-to-end speech recognition, arXiv 2014. arXiv:1412.5567
- [12] Vaswani et al., Attention Is All You Need, NeurIPS 2017. arXiv:1706.03762
- [13] He et al., Deep Residual Learning for Image Recognition, CVPR 2016. arXiv:1512.03385
- [14] Srivastava et al., Training Very Deep Networks (Highway Networks), NeurIPS 2015. arXiv:1507.06228
- [15] Li et al., Visualizing the Loss Landscape of Neural Nets, NeurIPS 2018. arXiv:1712.09913
- [16] He et al., Identity Mappings in Deep Residual Networks (Pre-activation), ECCV 2016. arXiv:1603.05027
- [17] Veit et al., Residual Networks Behave Like Ensembles of Relatively Shallow Networks, NeurIPS 2016. arXiv:1605.06431
- [18] Huang et al., Densely Connected Convolutional Networks, CVPR 2017. arXiv:1608.06993
- [19] Xie et al., Aggregated Residual Transformations for Deep Neural Networks, CVPR 2017. arXiv:1611.05431

---

## 3. 第二阶段：Transformer 范式 (2017-2026)

Transformer (Vaswani et al., 2017) 用 self-attention 替代 RNN 循环，解决并行 + 长距离依赖两个硬伤；后续 9 年间经 Scaling Law / RLHF / 多模态 / 推理 scaling 几次范式扩展，演变为 LLM 工业化的统一基底。

### 3.1 Transformer：注意力机制

Transformer (Vaswani et al., NeurIPS 2017)[1] 完全用 self-attention + position-wise FFN 取代 RNN 循环结构与 CNN 卷积。在 WMT'14 EN-DE 翻译任务上 BLEU 28.4，超过当时 RNN encoder-decoder baseline 25.16[1]。

#### 关键设计

- **Scaled dot-product attention**：`Attention(Q, K, V) = softmax(QK^T / √d_k) V`[1]；√d_k 缩放避免 softmax 进入饱和区
- **Multi-head attention**：把 Q / K / V 线性投影到 h 个子空间各自做 attention 后 concat；让模型在不同 representation subspace 关注不同模式
- **Position encoding**：self-attention 本身排序无关；用 sinusoidal positional encoding 把绝对位置注入 embedding（后来 RoPE 等替代方案）
- **Encoder-decoder + residual + LayerNorm**：每个 sub-layer 后 `LayerNorm(x + Sublayer(x))`，残差连接来自 ResNet[2]

#### 解决了 RNN 的两个硬伤

- **并行性**：self-attention 矩阵运算所有 step 一次性算出，GPU 满负载；RNN 必须串行
- **长距离依赖**：任意两 token 直接 O(1) 交互，不经 hidden state 衰减；LSTM 只能稳定捕捉 ~100-1000 step 内信息

#### 三派分化与下游影响

Transformer 之后 LLM 主要分三派架构：

- **encoder-only** (BERT, Devlin et al., NAACL 2019)[3]：masked language modeling，适合 representation / NLU
- **decoder-only** (GPT, Radford et al., 2018)[4]：causal LM 自回归生成，后续成为 LLM 主线
- **encoder-decoder** (T5, Raffel et al., JMLR 2020)[5]：text-to-text 统一 framework

attention 机制本身在 Bahdanau et al. (ICLR 2015)[6] 就已用于 NMT；Transformer 的核心贡献是把 "更大 = 更强" 工程化为可预测、可并行 scale 的事实，后续 Scaling Law 在此基础上验证。

### 3.2 Scaling Law 与 GPT-3

Kaplan et al. (OpenAI 2020)[7] 实验拟合：LLM cross-entropy loss 与参数量 N、数据量 D、计算量 C 呈幂律：

`L(N) ∝ N^-0.076`、`L(D) ∝ D^-0.095`、`L(C) ∝ C^-0.05`[7]

含义：给定 compute budget 可预测最优 N / D 配比与最终 loss。这是 LLM 工程化的核心依据 — 模型设计从 "试新 architecture" 转向 "scale 现有架构 + 调数据 / 训练流程"。

#### GPT-3 (Brown et al., NeurIPS 2020)[8]

- 175B 参数，300B token 训练；in-context learning (few-shot) 显示无需 fine-tune 即可做翻译 / QA / 算术 / code
- 性能曲线随 scale 平滑提升，验证 Kaplan 2020 预测

#### Chinchilla 修正 (Hoffmann et al., DeepMind 2022)[9]

Kaplan 2020 的最优配比偏向 "参数大 / 数据少"；Hoffmann et al. 用 400+ 个新实验拟合发现 N 与 D 应同速 scale (compute-optimal: 1B 参数 ↔ 20B token)。Chinchilla 70B (1.4T token) 性能超过 Gopher 280B (300B token)，验证 GPT-3 严重 undertrained。

#### Emergent abilities 与争议

Wei et al. (TMLR 2022)[10] 列出 137 个 BIG-Bench 任务的 emergence 曲线：某些任务 (multi-step arithmetic / chain-of-thought) 在小模型几乎随机，到某个 scale 阈值后性能突然提升。

Schaeffer et al. (NeurIPS 2023)[11] 提出反例：多数 emergence 现象由 metric 选择 (discontinuous metrics like exact-match) 造成的伪迹；换连续 metric 后曲线平滑。Emergence 是否真实仍是开放问题。

### 3.3 ChatGPT 与 RLHF

ChatGPT (OpenAI 2022-11-30)[12] 的技术基底 = GPT-3.5 + InstructGPT-style RLHF (Ouyang et al., NeurIPS 2022)[13]。

#### RLHF 三阶段[13]

- **SFT (supervised fine-tuning)**：用人类示范回复做 supervised learning，让 base model 学会对话格式
- **Reward model**：让人类对多个候选回复排序，训一个 reward model 模拟人类偏好
- **PPO RL**：用 reward model 作 reward signal，PPO 优化 policy LM

设计目标 = 三 H (helpful / harmless / honest)。RLHF 思想源自 Christiano et al. (NIPS 2017)[14] 的 RL from human preferences。

#### 产品意义

ChatGPT 5 天 100 万用户、2 个月 1 亿用户。技术上 GPT-3.5 + RLHF 不是飞跃 (InstructGPT 2022-01 已上线)，但产品形态 (对话 UI + alignment to human preference) 是 LLM 第一次被普通用户日常使用的关键节点。后续 Anthropic Claude (Constitutional AI, Bai et al., 2022)[15]、DeepSeek R1 (RL-from-base, 2025-01) 均沿用 RL-from-feedback 思路。

ChatGPT 之后 (2024-2026)，LLM frontier 由 OpenAI / Google DeepMind / Anthropic 三家闭源主线 + Alibaba / Moonshot / Zhipu / DeepSeek 国内 4 家开源主线推进，主流 release 包括 GPT-5.5 / Gemini 3.1 Pro / Claude Opus 4.7 / Qwen3.6-Max / Kimi K2.6 / GLM-4.6 / DeepSeek V4 等；架构线另有 Mamba 系列 (SSM) 在长 context / inference cost 敏感场景作为 Transformer 替代。本笔记 narrative 聚焦"演进 → 解决什么问题 → 应用扩展"主线，不展开 frontier 横扫；具体 model 参数 / benchmark / 价格对比详见 `09-sweeper-embodied-roadmap.md` §1 行业技术现状地图。

### References

- [1] Vaswani et al., Attention Is All You Need, NeurIPS 2017. arXiv:1706.03762
- [2] He et al., Deep Residual Learning for Image Recognition, CVPR 2016. arXiv:1512.03385
- [3] Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding, NAACL 2019. arXiv:1810.04805
- [4] Radford et al., Improving Language Understanding by Generative Pre-Training (GPT-1), OpenAI 2018.
- [5] Raffel et al., Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5), JMLR 2020. arXiv:1910.10683
- [6] Bahdanau et al., Neural Machine Translation by Jointly Learning to Align and Translate, ICLR 2015. arXiv:1409.0473
- [7] Kaplan et al., Scaling Laws for Neural Language Models, arXiv 2020. arXiv:2001.08361
- [8] Brown et al., Language Models are Few-Shot Learners (GPT-3), NeurIPS 2020. arXiv:2005.14165
- [9] Hoffmann et al., Training Compute-Optimal Large Language Models (Chinchilla), NeurIPS 2022. arXiv:2203.15556
- [10] Wei et al., Emergent Abilities of Large Language Models, TMLR 2022. arXiv:2206.07682
- [11] Schaeffer et al., Are Emergent Abilities of Large Language Models a Mirage?, NeurIPS 2023. arXiv:2304.15004
- [12] OpenAI, Introducing ChatGPT, openai.com/blog 2022-11-30.
- [13] Ouyang et al., Training Language Models to Follow Instructions with Human Feedback (InstructGPT), NeurIPS 2022. arXiv:2203.02155
- [14] Christiano et al., Deep Reinforcement Learning from Human Preferences, NIPS 2017. arXiv:1706.03741
- [15] Bai et al., Constitutional AI: Harmlessness from AI Feedback, arXiv 2022. arXiv:2212.08073

---

## 4. 第三阶段：视觉与视频生成 (2020-2024)

2020-2024 间 Diffusion 主线把图像 / 视频生成做大：DDPM (NeurIPS 2020) 把生成 cast 为 iterative denoising → DDIM 加速 → Latent Diffusion / Stable Diffusion (CVPR 2022) 降 compute → DALL-E 2 / Imagen / Midjourney / Sora / Veo 应用线展开。本节按方法演进 + 应用扩展两条线展开。

### 4.1 方法演进 (Diffusion 主线)

Diffusion 模型把 "从噪声生成图像" 问题 cast 为 iterative denoising：给定图像 x_0，forward 过程逐步加 Gaussian 噪声直到 x_T ≈ N(0, I)；reverse 过程训练 model 预测每步去噪的 score（或直接预测噪声 ε）。训练 stable，scale 友好。方法演进沿四个里程碑展开：基础 (DDPM) → 加速 (DDIM) → 条件控制 (Guidance) → 降算力 (Latent Diffusion)。

#### DDPM (Ho et al., NeurIPS 2020)[1]

- Forward：`q(x_t | x_{t-1}) = N(x_t; √(1-β_t) x_{t-1}, β_t I)`，β_t 是 noise schedule
- Reverse：训 ε_θ(x_t, t) 预测加入的噪声；损失 `L = E[||ε - ε_θ(x_t, t)||²]`
- T 通常 1000 步，直接采样需 1000 次 forward pass

#### 加速：DDIM (Song et al., ICLR 2021)[2]

- DDIM 把 reverse 过程改为 deterministic non-Markovian path
- 1000 → 50 步内 sample，质量基本无损
- 后续 DPM-Solver / EDM 等进一步压到 10-20 步

#### Guidance：Classifier vs Classifier-free

- **Classifier guidance** (Dhariwal & Nichol, NeurIPS 2021)[3]：训一个 classifier `p(y|x_t)`，reverse 时用其梯度 `∇_x log p(y|x)` 引导生成
- **Classifier-free guidance** (Ho & Salimans, 2022)[4]：同时训 conditional / unconditional model，sampling 时混合 `ε = ε_uncond + w · (ε_cond - ε_uncond)`；不需要单独 classifier，是当前 text-to-image 主流

#### Latent Diffusion 与 Stable Diffusion (Rombach et al., CVPR 2022)[5]

LDM 把 diffusion 从 pixel space 移到 VAE encoder 输出的 latent space（典型 4× downsample），显著降低 compute。Stable Diffusion (2022-08，open-weight) 基于 LDM + LAION-5B 训练，是首个消费级 GPU (8GB VRAM) 可跑的 text-to-image 模型；开源后社区驱动迅速展开周边生态 (ControlNet 2023-02 / LoRA / ComfyUI 等)。

### 4.2 应用扩展 (2022-2024)

- **DALL-E 2** (Ramesh et al., OpenAI 2022-04)[6]：CLIP latent + diffusion prior + diffusion decoder
- **Imagen** (Saharia et al., Google NeurIPS 2022)[7]：T5 text encoder + cascaded pixel diffusion
- **Midjourney** v3 (2022-08) → v5 (2023-03) → v6 (2024-04)：闭源，偏艺术风格
- **Stable Diffusion 1.x → 2.x → SDXL (2023-07) → SD3 (2024-02)**：开源主线；FLUX (Black Forest Labs 2024-08) 接力
- **视频扩展**：Stable Video Diffusion (2023-11)[9] / Sora (OpenAI 2024-02 technical report)[8] / Veo 3 (Google 2024-12)

### References

- [1] Ho et al., Denoising Diffusion Probabilistic Models (DDPM), NeurIPS 2020. arXiv:2006.11239
- [2] Song et al., Denoising Diffusion Implicit Models (DDIM), ICLR 2021. arXiv:2010.02502
- [3] Dhariwal & Nichol, Diffusion Models Beat GANs on Image Synthesis (Classifier guidance), NeurIPS 2021. arXiv:2105.05233
- [4] Ho & Salimans, Classifier-Free Diffusion Guidance, arXiv 2022. arXiv:2207.12598
- [5] Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, CVPR 2022. arXiv:2112.10752
- [6] Ramesh et al., Hierarchical Text-Conditional Image Generation with CLIP Latents (DALL-E 2), arXiv 2022. arXiv:2204.06125
- [7] Saharia et al., Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding (Imagen), NeurIPS 2022. arXiv:2205.11487
- [8] OpenAI, Video generation models as world simulators (Sora technical report), 2024-02.
- [9] Blattmann et al., Stable Video Diffusion, arXiv 2023. arXiv:2311.15127

---

## 5. 第四阶段：多模态理解 (2020-2024)

2020-2024 间，CLIP (ICML 2021) 用 contrastive learning 把图像与文本对齐到统一 embedding space，解决跨模态表征问题；GPT-4V (2023-09) 起把 vision 装进 LLM，多模态从此成为 LLM standard configuration。本节按 representation 与 LLM 融合两条线展开，二者共同支撑后续 VLM / VLA 的视觉理解组件。

### 5.1 CLIP 与多模态对齐

CLIP (Contrastive Language-Image Pre-training, Radford et al., OpenAI ICML 2021)[1] 用 contrastive learning 把图像与文本对齐到同一 embedding space。

#### 训练框架[1]

- **数据**：400M（图像，文本描述）pair，从 web 收集（WIT-400M）
- **Encoder**：image encoder (ViT-B/16, ViT-L/14, ResNet) + text encoder (Transformer)
- **Loss**：InfoNCE，把 batch 内对齐的 (image, text) 对作 positive，其他作 negative
- 训出后两个 encoder 共享 latent space，同义图文相似度高

#### Zero-shot 分类[1]

- 给定类别名 list（如 ImageNet 1000 类），把每类做 prompt template `a photo of a {class}`，编码得到 1000 个文本 embedding
- 输入图像编码后，计算与所有文本 embedding 的相似度，取最高者为类别
- ViT-L/14 在 ImageNet zero-shot top-1 ~76.2%，接近 supervised ResNet-50 baseline

#### 平行工作：ALIGN

ALIGN (Jia et al., Google ICML 2021)[2] 同期独立工作，用 1.8B noisy 图文对（vs CLIP 400M cleaner pairs），验证 contrastive pre-training scale 路线 robust。

#### 下游影响

- **Text-to-image generation**：Stable Diffusion / DALL-E 2 / Imagen 的 text encoder 都是 CLIP（或衍生的 OpenCLIP / T5）
- **Open-vocabulary detection / segmentation**：OWL-ViT (Minderer et al., ECCV 2022)[3] / GroundingDINO / SAM-2 prompt
- **VLM backbone**：LLaVA / Qwen-VL / InternVL 的 vision tower 通常用 CLIP-ViT（或 SigLIP）抽取 visual feature

CLIP 是后续 VLM 与 VLA（V-base = VLM）的 visual backbone 主流来源；§7.1.1 国际 VLA 节中 RT-2 / π₀ 等 model 内的 vision encoder 多溯源到 CLIP / SigLIP 系列。

### 5.2 GPT-4V 与多模态 LLM

GPT-4V (OpenAI 2023-09 system card)[4] 是 GPT-4 的视觉扩展版本，把图像作为另一种 token 输入 decoder-only LLM。多模态从此从单独研究方向变为 LLM 的 standard configuration。

#### LLaVA 与开源 VLM 路线 (Liu et al., NeurIPS 2023)[5]

LLaVA (2023-04) 用 minimum-effort 方案验证 VLM 可行性：

- Vision encoder (CLIP ViT-L/14 frozen) + projection (单层 linear / 后续 MLP) + LLM (Vicuna)
- 训练 stage 1：align projection (CC3M subset 558K pairs)
- 训练 stage 2：instruction tuning (GPT-4 generated 158K visual instruction data)

开源后成为 VLM 基本范式；LLaVA-1.5 (2023-10) 替换 projection 为 MLP，benchmark 进一步提升。

2024 年起多模态成为 LLM standard configuration（Gemini / Claude 3 / GPT-4o / Qwen-VL / Qwen Omni / Kimi K2 / GLM-4.6 等），VLM 由此成为后续 VLA（V-base = VLM）与 World Models（Cosmos-Reason 系列）的 ready-made 视觉理解组件。具体模型横扫详见 `09-sweeper-embodied-roadmap.md` §1。

### References

- [1] Radford et al., Learning Transferable Visual Models From Natural Language Supervision (CLIP), ICML 2021. arXiv:2103.00020
- [2] Jia et al., Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision (ALIGN), ICML 2021. arXiv:2102.05918
- [3] Minderer et al., Simple Open-Vocabulary Object Detection with Vision Transformers (OWL-ViT), ECCV 2022. arXiv:2205.06230
- [4] OpenAI, GPT-4V(ision) System Card, openai.com 2023-09.
- [5] Liu et al., Visual Instruction Tuning (LLaVA), NeurIPS 2023. arXiv:2304.08485

---

## 6. 第五阶段：World Models 起源 (2018-2023)

2018 年 Ha & Schmidhuber 提出 V+M+C 架构是 world model 在深度学习时代的现代起点；2023 年 Runway GEN-1 把 diffusion 推向视频生成工程化。两条路线在 2024-2026 收敛为 latent video → 可交互 world model（详见 §8）；本节是后续延伸 1（具身 VLA）+ 延伸 2（World Models 近期形态）的两条根。

### 6.1 World Models 2018 (Ha & Schmidhuber)

Ha & Schmidhuber (NeurIPS 2018)[1] 提出 agent 在内部 world model 中 "dream" rollout，用 dream 训 policy，而非每步与真实环境交互。该工作沿用 Schmidhuber 早期 (1990, 1991) RL with world model 的思路[2]，在深度学习时代以 V+M+C 三模块实现。

#### V+M+C 三模块[1]

- **V (Vision)**：VAE encoder 把高维 observation 压缩到 latent z（32 维）
- **M (Memory)**：MDN-RNN（mixture density net + RNN）在 latent space 预测下一时刻 `z_{t+1} | z_t, a_t`
- **C (Controller)**：简单 linear policy `a = W [z_t; h_t]`，h_t 是 RNN hidden state；用 evolution strategy (CMA-ES) 训练，不需要 backprop 透 V / M

#### 关键实验[1]

- **CarRacing-v0** (OpenAI Gym)：agent 完全在 dream rollout 中训练 policy，直接 deploy 到真实 environment 取得 906 ± 21 分（vs 当时 best published 591），首次在 reward 上证明 dream-based policy training 可行
- **ViZDoom Take Cover**：类似 setup，agent 在 dream 中训练后真实 env 中 sample 上 1100 step（baseline ~280 step）

#### 6 年实践停滞 (2018-2024)

V+M+C 在玩具 task 上验证后，2018-2024 间未出现规模化 successful application：

- VAE 表示能力受限，无法 scale 到复杂场景 / 高分辨率
- MDN-RNN 长 horizon 推演 drift 严重
- 训练数据规模与 LLM / Diffusion 时代不匹配

实际突破等到 2024-2025 大模型时代（Cosmos / Genie 系列），详见 §8。

#### 路线分歧：JEPA vs LLM 主线

LeCun (Meta) 持续主张 AGI 核心是 self-supervised world model，提出 JEPA (Joint Embedding Predictive Architecture, 2022)[3] 路线：在 embedding space 做 predictive learning，不做 pixel-level reconstruction。后续 V-JEPA (Bardes et al., 2024)[4]、V-JEPA-2 (Meta 2025-06)[5] 用于 video understanding。

主流 LLM / VLA 阵营则相信预训练 + 推理 scaling + RL fine-tune 路线（GPT / Gemini / Claude / DeepSeek 全部此路线）。这是 AI 领域一条公开未解决的路线分歧。

### 6.2 Runway GEN-1 与视频生成

GEN-1 (Esser et al., Runway research 2023-02)[6] 把 diffusion 思路 extend 到视频生成的工程产品。技术上不是最强（后续 Sora / Veo 3 性能远超），但是 video diffusion 工程化的早期里程碑，提出了 "条件生成视频" 的若干 design choice。

#### GEN-1 (Runway 2023-02)[6]

- **输入**：source video + reference image / text prompt
- **输出**：stylized video（depth / mask / structure 保留 + appearance 替换）
- **架构**：latent diffusion 扩展到 video，depth + structure 作为 conditioning
- **应用**：商业视频后期 / 风格迁移；SaaS 形态，非技术用户可用

#### 后续主线 (2023-2024)

GEN-1 之后视频生成沿三种范式展开（Diffusion / Autoregressive / Hybrid），代表性 release：

- **Stable Video Diffusion** (Blattmann et al., 2023-11)[7]：Diffusion 范式，开源 video diffusion，1.5B-3.5B param，14-25 frames @ 576×1024
- **Sora** (OpenAI 2024-02 technical report)[8]：Diffusion 范式，spacetime patch + Diffusion Transformer (DiT, Peebles & Xie, ICCV 2023)[9]，60s 长视频；2024-12 公开 release 名 Sora Turbo
- **Veo / Veo 3** (Google DeepMind 2024-05 / 2024-12)[1]：Diffusion 范式，闭源，高质量 + 长片段 + 物理一致性；集成进 Vertex AI
- **VideoPoet** (Google 2023-12)：Autoregressive 范式，用 LLM 范式生成 video token；长 horizon 强但慢
- **Pika / Runway Gen-3** (2024)：Diffusion 范式，商业向偏短片 / 创意
- **Hybrid (latent autoregressive + diffusion refinement)**：探索阶段

Diffusion 范式当前是主流；3D tensor (frame × H × W) 生成任务上，三种范式各自的 trade-off 待 video model scale 进一步放大后再观察。

#### 与 World Models 收敛 (2024-2025)

视频生成主线在 2024-2025 与 World Models 路线收敛：

- 视频生成 model 是 implicit world model（隐式学环境动力学）
- DeepMind Genie 系列把 video generation 改造为 user-action-controllable，即 explicit world model（详见 §8）
- NVIDIA Cosmos Predict 直接以 "world model 工具链" 命名其 video diffusion model（详见 §8）

第四阶段（2018 V+M+C / 2023 GEN-1）是后续延伸 1（具身 VLA）与延伸 2（World Models 近期形态）的两条根：

- VLA training 用 World Model dream 替代部分真机数据（§7.2.2 VLA + World Models 融合 节）
- World Models 近期形态在 2024-2026 通过 latent video diffusion + interactive control 实现产品级（§8）

### References

- [1] Ha & Schmidhuber, World Models, NeurIPS 2018. arXiv:1803.10122 (worldmodels.github.io)
- [2] Schmidhuber, On Learning to Think: Algorithmic Information Theory for Novel Combinations of RL Controllers and Recurrent Neural World Models, arXiv 2015. arXiv:1511.09249（含 1990 / 1991 RL+world-model 早期工作回顾）
- [3] LeCun, A Path Towards Autonomous Machine Intelligence (JEPA position paper), Open Review 2022.
- [4] Bardes et al., V-JEPA: Latent Video Prediction for Visual Representation Learning, arXiv 2024. arXiv:2404.08471
- [5] Meta AI, V-JEPA-2 release, ai.meta.com 2025-06.
- [6] Esser et al., Structure and Content-Guided Video Synthesis with Diffusion Models (GEN-1), Runway research 2023-02. arXiv:2302.03011
- [7] Blattmann et al., Stable Video Diffusion, arXiv 2023. arXiv:2311.15127
- [8] OpenAI, Video generation models as world simulators (Sora technical report), 2024-02.
- [9] Peebles & Xie, Scalable Diffusion Models with Transformers (DiT), ICCV 2023. arXiv:2212.09748
- [1] Google DeepMind, Veo 3 release, deepmind.google 2024-12.

---

## 7. 延伸 1：具身 VLA (2023-2026)

VLA (Vision-Language-Action) 把视觉 + 语言 model 输出端从 token 改为 action，直接输出机器人执行序列。2023 年 Google DeepMind RT-2 是首个工业级 VLA；2024-2026 间 Physical Intelligence π 系列 / Figure Helix / NVIDIA GR00T 把 VLA 推到产品级 + 跨形态泛化；国内 GraspVLA / GO-1 / UnifoLM-VLA-0 跟进。

### 7.1 VLA 进展（按地理）

VLA 进展按地理分两支：国际线（Google → Physical Intelligence → Figure → NVIDIA 四条主线）与国内线（银河通用 / 智元 / 宇树 三家 2025-2026 跟进）。两支主线时间锚点错开 ~1.5 年，国内多数 model 直接复用国际 VLM backbone（CLIP / Qwen-VL）。

#### 7.1.1 国际 VLA 时间线

国际 VLA 主线：Google DeepMind RT-2 → Physical Intelligence π 系列 → Figure AI Helix → NVIDIA GR00T 四条线。截至 2026-05-04 主流 release：


| Model      | 公司                    | Release    | Robot                | 训练数据                           | 关键贡献                                                     |
| ---------- | --------------------- | ---------- | -------------------- | ------------------------------ | -------------------------------------------------------- |
| RT-2       | Google DeepMind       | 2023-07    | dual-arm RT robot    | web-scale + RT-1               | VLM 直接转 VLA 的首个工作                                        |
| π₀         | Physical Intelligence | 2024-10    | 7 个 embodiment       | ~10k hrs robot data            | generalist policy 跨形态                                    |
| π₀.5       | Physical Intelligence | 2025-04-22 | 同 π₀ + new           | + open-world data              | open-world generalization                                |
| π₀.7       | Physical Intelligence | 2026-04-16 | steerable foundation | scaled                         | step-change in generalization                            |
| Helix 02   | Figure AI             | 2026-01    | Figure 02 humanoid   | full-body data                 | unified visuomotor net + 4 分钟洗碗机连续自主                     |
| GR00T N1   | NVIDIA                | 2025-03    | humanoid (open)      | open data + sim                | 开源 humanoid foundation                                   |
| GR00T N1.7 | NVIDIA                | 2026-04-17 | humanoid             | EgoScale 20,854 hrs egocentric | Action Cascade dual-system + dexterity scaling law (首报告) |


**Google DeepMind RT-2 (2023-07)[1]**

RT-2 (Brohan et al., Google DeepMind 2023-07)[1] 是首个把 VLM (PaLI-X 5B/55B / PaLM-E 12B/562B) 直接 fine-tune 成 VLA 的工作。action 被 tokenize 为 LLM vocabulary 中的 token，output 端 LLM 直接生成 action token。

- **数据**：web-scale pretraining（从 PaLI-X / PaLM-E 继承）+ RT-1 收集的 13 个机器人 17 个月数据（~130k 任务 episode）
- **泛化**：零样本对未见过的 object / instruction，closed-loop success +60% on novel objects（vs RT-1 baseline）
- **影响**：把 "VLM → fine-tune → VLA" 模式确立为后续标准（LLaVA / Qwen-VL / SigLIP 等都被尝试当 V-base）

**Physical Intelligence π 系列 (2024-2026)**

Physical Intelligence (PI) 是 Sergey Levine 等创立的具身公司，主线 π₀ → π₀.5 → π₀.7：

- **π₀** (2024-10)[2]：generalist robot policy，1 个 model 跨 7 个 embodiment（Franka / UR5e / Mobile Aloha / Trossen 等），~10k hrs 真机数据训练。VLM (PaliGemma) + flow matching action head。PI 公开 demo 在洗衣 / 折叠 / 打包多场景
- **π₀.5** (2025-04-22)[3]：open-world generalization。用 action knowledge transfer（从 web video + lab data 联合训练）在未训练过的 home / kitchen 场景 0-shot 表现
- **π₀.7** (2026-04-16)[4]：steerable robot foundation，PI 公开报告中描述为 "step-change in generalization"；具体 architecture 与训练 scale 待 paper release（写作时 verify）

PI 路线：闭源 + 大规模真机数据 + flow-matching action head（区别于 RT-2 的 token-by-token autoregressive action）。

**Figure AI Helix (2026-01 / 2026-03)**

Figure AI 在 humanoid 方向，Helix 系列把 full-body 操作统一为单一 visuomotor net：

- **Helix** (2025-02)：上半身 + 双机协作，嵌入式低功耗 GPU
- **Helix 02** (2026-01)[5]：full-body 自主，三层 dual-system（System 0 + 1 + 2，详见 +推理融合 节）；单一神经网络（10M 参数）替代 109,504 行 C++ 工程代码；Living room tidy demo (2026-03) 显示连续 4 分钟以上长任务自主

Figure 路线：humanoid 形态 + 量产硬件（Figure 03 2025-10 demo 掌内 camera + 触觉传感器）+ 算法 / 硬件协同迭代。

**NVIDIA GR00T (2025-03 → 2026-04-17)**

NVIDIA GR00T 是 humanoid foundation model 开源线：

- **GR00T N1** (2025-03)[6]：首个开源 humanoid foundation model，dual-system（VLM 推理 + Diffusion Transformer 动作）
- **GR00T N1.5** (2025-06)：加入 FLARE（从人类视频学习）
- **GR00T N1.6** (2026-04-15)：VLM 升级到 NVIDIA Cosmos-Reason-2B
- **GR00T N1.7** (2026-04-17)[7]：3B 参数 "Action Cascade" = Cosmos-Reason2-2B (System 2) + 32-layer DiT (System 1)；EgoScale 20,854 hrs 人类 egocentric video 数据集；NVIDIA 公开报告中提出 "robot dexterity scaling law"（1k → 20k hrs 训练数据 dexterity 表现 doubling），是 VLA 领域第一次报告 scaling law 现象

NVIDIA 路线：open foundation + 与 Cosmos / Isaac Sim 工具链强绑定；与 Boston Dynamics / Agility / Figure 等多家 humanoid 厂商合作。

**写作时 verify（截至 2026-05-04）**

- 未见 Figure Helix 03 公开 release；留待后续追加
- π₀.7 (2026-04-16) 是 PI 当前主线，是否取代 π₀ 作为 default baseline 待后续 paper / release 明确

#### 7.1.2 国内 VLA 进展

国内 VLA 在 2025-2026 出现 3 家主线：银河通用 GraspVLA / 智元 GO-1 / 宇树 UnifoLM：


| Model         | 公司   | Release    | Robot       | 训练数据                    | 开源闭源       |
| ------------- | ---- | ---------- | ----------- | ----------------------- | ---------- |
| GraspVLA      | 银河通用 | 2025-01-09 | Galbot 上半身  | 10 亿帧合成 + 真机            | 闭源         |
| AgiBot GO-1   | 智元   | 2025-03-10 | 多形态         | AgiBot World 100 万 demo | 闭源 + 公开数据集 |
| UnifoLM-VLA-0 | 宇树   | 2026-01-29 | G1 humanoid | 真机 + 模拟                 | 开源         |


**银河通用 GraspVLA (2025-01-09)[8]**

GraspVLA 是与智源 / 北大 / 港大合作的具身抓取大模型：

- **数据**：10 亿帧合成 "视觉-语言-动作" 对预训练 + 真机 fine-tune
- **七大泛化金标准**（银河通用提出）：光照 / 背景 / 平面位置 / 空间高度 / 动作策略 / 动态干扰 / 物体类别
- **集成**：GraspVLA + TrackVLA + 人机交互模块 → GALBOT VLA agent；Galbot G1 上半身机器人在 NVIDIA CES 2025 demo 中托举 RTX 5090

**智元 AgiBot GO-1 (2025-03-10)[9]**

GO-1 是智元 (AgiBot) 的 ViLLA (Vision-Language-Latent-Action) 架构：

- **架构**：MoE + Latent Planner + Action Expert 三件套，在 latent space 做 planning 而不是直接 action token
- **训练数据**：AgiBot World 数据集，100 万条真实机器人 demonstration，217 个任务；国内首个公开大规模 VLA 数据集
- **性能**：平均成功率 46% → 78%（vs GO-1 之前 baseline）

**宇树 UnifoLM-VLA-0 (2026-01-29)[10]**

UnifoLM-VLA-0 是宇树为 G1 humanoid 设计的 VLA：

- **Backbone**：基于阿里 Qwen2.5-VL-7B（国内 VLA 直接复用 Qwen 系列 VLM 的代表案例）
- **任务**：单一 policy 在 G1 上完成 12 类操作（开闭抽屉 / 插拔 / 抓放 / 工具使用）
- **开源 + 硬件价格**：开源 + G1 售价约 $13.5K（vs Figure 02 等海外 humanoid 一个数量级低）

### 7.2 VLA 融合方向

VLA 与其他范式的融合主要沿两条方向展开：与 reasoning（推理大模型）融合形成 dual-system 架构，与 World Models 融合形成 dream-based training。前者解 long-horizon 任务规划，后者解真机数据稀缺。

#### 7.2.1 VLA + 推理融合

VLA + reasoning 融合的核心模式是 dual-system：System 1 高频反射动作 (VLA policy) + System 2 慢思考 (reasoning LLM) 协同，应对 long-horizon / 多步任务。

**Reasoning model 极简介绍（背景，~200 字）**

Reasoning model 把 chain-of-thought 推理内置为 model 能力，通过 RL on CoT 训练（而非外部 prompt-engineering）。代表工作：OpenAI o1 (2024-09)[11] / o3 (2025-04) / DeepSeek R1 (2025-01)[12] / DeepSeek R2 (2026-04，32B dense 单 24GB GPU 可跑)。性能特点：AIME / GPQA / Codeforces 等 multi-step 推理 benchmark 显著超过同期 GPT-4 / GPT-5 base。本 doc scope 偏 SLAM / 具身，不单独展开；此处仅作为 VLA + 推理融合的 background。

**Dual-system 三个实例**

- **Figure Helix System 1+2** (2026-01)[5]：三级架构 — System 0 实时平衡 (1 kHz) / System 1 视觉运动 (200 Hz, VLA policy) / System 2 高层推理 (LLM reasoning)；公开报告中明确借鉴 Kahneman 快 / 慢思考二系统；4 分钟连续洗碗机自主 demo (2026-01) 由该架构实现
- **π₀.5 reasoning version** (2025-04-22)[3]：π₀.5 在 base policy 之外集成 reasoning 模块；用 LLM 对当前 task 拆解为 sub-task 后由 base policy 执行
- **GR00T N1.7 Action Cascade** (NVIDIA 2026-04-17)[7]：System 2 = Cosmos-Reason2-2B（NVIDIA 自家 reasoning VLM，详见 §8.2 Cosmos），System 1 = 32-layer Diffusion Transformer；"Action Cascade" 命名强调 reasoning 输出的 plan 级联到 DiT action 生成

**关键挑战**

- **System 1/2 latency 协调**：System 2 LLM 推理 ~秒级延迟，System 1 控制 ~10 ms；协调机制（event-triggered / 周期性 / 异步并行）直接影响系统响应
- **Long-horizon planning**：System 2 输出的 plan 在 System 1 执行过程中可能偏离，何时重 plan 是开放问题
- **Plan ↔ action 接口形式**：language token / latent vector / sub-task list，当前各家 design choice 不同，没有 standard

#### 7.2.2 VLA + World Models 融合

VLA + World Models 融合的核心模式是 World Model dreaming：用 world model 生成大量 rollout 数据训练 VLA policy，替代 / 补充真机数据收集。思路延续 Ha & Schmidhuber 2018 dream-based policy training（详见 §6），但 world model 从 V+M+C 升级到 latent video diffusion 大模型。

**Cosmos / Genie / V-JEPA 在此节简提（详见 §8）**

- **NVIDIA Cosmos** (2025-01 起)：physical AI world model 工具链，包括 Predict (未来状态) / Transfer (sim-to-real) / Reason (VLM)
- **DeepMind Genie 系列** (2024-02 / 2024-12 / 2025-08)：可交互 latent world model，被多家 VLA 团队当 training playground 使用
- **V-JEPA-2** (Meta 2025-06)：JEPA 路线的 video predictive model

详细内容见 §8 World Models 近期形态；本节仅讨论与 VLA training 的融合机制。

**三个融合机制**

- **Sim-to-real via Cosmos Transfer**：NVIDIA Cosmos Transfer 把 sim renderer 输出经 diffusion 改造成接近真机分布的图像，用于 VLA training data augmentation；GR00T N1.7 (2026-04-17) 公开报告中使用此 pipeline
- **Dream-based RL training**：world model 生成 rollout，VLA policy 在 dream 中做 RL；银河通用 / 宇树 UnifoLM 等公开报告中提到 dreamer-like 训练方式
- **Reasoning + World Model 在同一 model 内**：NVIDIA GR00T N1.7 把 Cosmos-Reason2-2B 同时作 System 2 reasoning 与 world model state predictor，把 reasoning 与 dream 在同一 model 内统一

**当前局限与开放问题**

- **Sim-to-real gap 仍在**：world model dream 的物理一致性与真机 distribution 仍有 gap，完全 dream-only training 在长尾任务上未广泛验证
- **训练数据分布对齐**：world model 训练数据 vs VLA policy 训练数据 distribution 是否需要联合归一化，当前各家 design 不同
- **真机数据规模仍是瓶颈**：GR00T N1.7 dexterity scaling law 在 1k-20k hrs 真机数据上验证，是否能用 world model dream 进一步 scale 待验证（开放问题 1，§9）

### References

- [1] Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, arXiv 2023. arXiv:2307.15818
- [2] Black et al. (Physical Intelligence), π₀: A Vision-Language-Action Flow Model for General Robot Control, arXiv 2024. arXiv:2410.24164
- [3] Physical Intelligence, π₀.5 release, physicalintelligence.company/blog/pi05 2025-04-22.
- [4] Physical Intelligence, π₀.7 release, physicalintelligence.company/blog/pi07 2026-04-16.
- [5] Figure AI, Helix 02 release, figure.ai/news/helix 2026-01.
- [6] NVIDIA, GR00T N1 release, developer.nvidia.com 2025-03.
- [7] NVIDIA, GR00T N1.7: Action Cascade and EgoScale, huggingface.co/blog/nvidia/gr00t-n1-7 2026-04-17.
- [8] 银河通用, GraspVLA + 七大泛化金标准, 银河通用 blog 2025-01-09; baike.baidu.com/item/GraspVLA
- [9] AgiBot, GO-1 + AgiBot World 数据集 release, agibot.com 2025-03-10; tech.huanqiu.com/article/4QAL55JkZVE
- [10] Unitree, UnifoLM-VLA-0 release, unitree.com 2026-01-29.
- [11] OpenAI, o1 system card, openai.com/index/learning-to-reason-with-llms 2024-09-12.
- [12] DeepSeek, DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, arXiv 2025. arXiv:2501.12948

---

## 8. 延伸 2：World Models 近期形态 (2024-2026)

2024-2026 间 World Models 走出 V+M+C 玩具阶段，由 latent video diffusion 大模型 + interactive control 实现产品级 / 公众级 release。DeepMind Genie 系列与 NVIDIA Cosmos 工具链是当前两大主线。

### 8.1 可交互世界生成（Genie 3）

DeepMind Genie 系列把 video generation 改造为 user-action-controllable，即 explicit world model。

#### Genie 系列时间线

主线 Genie 1 → Genie 2 → Genie 3 → Project Genie：

- **Genie 1** (DeepMind, ICML 2024)[1]：第一代 foundation world model，256×256，11B 参数，从 200k+ 小时 unlabeled internet video 学；可生成 2D platform-style world，user 用 action token 控制 agent
- **Genie 2** (DeepMind 2024-12)[2]：升级到 3D 环境，支持 first-person / third-person 视角，~1 分钟 horizon 一致性
- **Genie 3** (DeepMind 2025-08-05)[3]：720p / 24 fps real-time interactive，photorealistic；60s session 一致性；用户从一张图或一段文字出发实时操控生成的 3D 环境；距 2018 Ha World Models 论文 7 年，是 World Models 公众级 demo 的标志性 release
- **Project Genie** (DeepMind 2026-01-29)[4]：Genie 3 商业化产品，集成 Google AI Ultra（US 18+ 用户）

#### 应用与对比

**应用线**：

- **Waymo World Model** (Waymo 2026-02)[5]：自动驾驶 closed-loop 仿真，在内部 world model 中 sample edge case 训练 / evaluate L4 policy
- **VLA training playground**（多家 humanoid VLA）：用 Genie 系列环境做 RL pretrain / sim2real 验证（详见 §7.2.2 VLA + World Models 融合）

**与 Sora-style 视频生成的区别**：视频生成 model 是 implicit world model，但 Sora / Veo 输出的是固定 video clip，user 不能在生成中途介入。Genie 系列三个核心区别：

- **Action-conditioned**：每帧生成依赖 user 当前 action token，系统在线 sample 而非 batch 生成
- **State maintenance**：跨 frame 维护 world state（物体位置 / 物理一致性 / 相机轨迹）
- **Interactive latency**：real-time (~24 fps) 生成 vs offline batch generation

### 8.2 机器人仿真训练（NVIDIA Cosmos）

NVIDIA Cosmos (2025-01 起) 是 physical AI 的 world model 工具链，与 NVIDIA Isaac Sim / GR00T humanoid foundation 配套形成 stack。

#### Cosmos 体系（3 子族 + 工具链定位）

**3 个子族 (2025-2026)[6, 7]**：

- **Cosmos Predict (Predict 2.5, 2026-04)**：flow-based world prediction；统一接口（text-to-world / image-to-world / video-to-world）；2.5 系列在长 horizon 物理一致性上较 1.x 显著 improve
- **Cosmos Transfer (Transfer 2.5, 2026-04)**：multi-controlnet 可控生成（depth map / segmentation / pose / sketch 等多种 input 条件）；用于 sim-to-real data augmentation（sim renderer 输出 → diffusion 改造为 real-distribution）
- **Cosmos Reason (Reason 2, 2026-04)**：VLM 增强 spatial-temporal 理解的 reasoning model；NVIDIA GR00T N1.6 / N1.7 直接用 Reason2-2B 作为 System 2 backbone（详见 §7.2.1 VLA + 推理融合）

**工具链定位**：Cosmos 不是单点 model，而是 NVIDIA "physical AI stack" 的 foundation 层：

- **Foundation**：Cosmos foundation models (Predict / Transfer / Reason)
- **Sim**：NVIDIA Isaac Sim / Isaac Lab（sim 引擎）
- **Embodiment**：GR00T N1.x humanoid foundation
- **Hardware**：Jetson Thor / DGX Spark（具身 inference 硬件）

#### 应用与对比

**公开 early adopter**[7]：NVIDIA 公开报告中 Cosmos 早期 adopter 包含 humanoid + 自动驾驶两个方向：

- **Humanoid**：1X / Agility Robotics / Figure AI / Boston Dynamics（Cosmos Transfer 用作 sim-to-real）
- **自动驾驶**：Uber / Waabi（Cosmos Predict 用作 closed-loop 仿真）

**与 Genie 路线的差异**：Cosmos 与 Genie 共享 latent video world model 核心思路，但 design choice 不同：

- **Target user**：Cosmos 偏 robot / 自动驾驶 industry developer；Genie 偏 consumer / game / general public
- **Open vs closed**：Cosmos 部分模型开源 (Cosmos-Reason2-2B 等)，Genie 闭源
- **Toolchain integration**：Cosmos 与 NVIDIA Isaac Sim 深度集成；Genie 暂无类似 sim 引擎绑定

### References

- [1] Bruce et al. (DeepMind), Genie: Generative Interactive Environments, ICML 2024. arXiv:2402.15391
- [2] DeepMind, Genie 2: A large-scale foundation world model, deepmind.google 2024-12.
- [3] DeepMind, Genie 3: A new frontier for world models, deepmind.google/en/blog/genie-3 2025-08-05.
- [4] DeepMind, Project Genie + Google AI Ultra release, deepmind.google 2026-01-29.
- [5] Waymo, Waymo World Model release, waymo.com 2026-02.
- [6] NVIDIA, Cosmos World Foundation Models, developer.nvidia.com/cosmos 2025-01 (CES).
- [7] NVIDIA, Advancing Physical AI with Cosmos 2.5 + Reason2, developer.nvidia.com/blog 2026-04.

---

## 9. 两个开放问题

两个与具身 / 重建相关的、当前未解决的问题。仅描述现状 / 缺口 / 待观察项，不下判断。

### 9.1 VLA 在 home / 长尾场景的泛化

**现状**：VLA 在工厂 / 结构化 pick-place / lab demo 任务上 robust。GR00T N1.7 (2026-04-17)[1] 在 EgoScale 20,854 hrs 数据上首次报告 robot dexterity scaling law（1k → 20k hrs 训练数据 → dexterity 表现 doubling），是 VLA scale 路线的 positive signal。

**缺口**：home / 长尾场景的公开 benchmark + success rate 仍未广泛报告：

- Physical Intelligence π₀.5 (2025-04-22)[2] 在 open-world generalization 上是早期信号
- π₀.7 (2026-04-16) "step-change in generalization" 描述待 paper 公开（写作时 verify）
- Figure Helix 02 (2026-01) 4 分钟洗碗机 demo 是单点案例，不是统计意义上的成功率

**待观察**：

- 是否有标准 home benchmark（类似 ImageNet / COCO 在 CV 时代的角色）
- scaling law 在 home / 长尾 task 上是否同样成立，还是会饱和
- World Model dream 替代真机数据是否能 scale 到 home 场景多样性（与开放问题 2 部分耦合）

### 9.2 World Models 与 metric 重建是否合流

**现状**：当前两条线在工具上都 reach Transformer feed-forward 大模型化，但 design choice 仍分化：

- **生成路线 (Genie 3 / Cosmos)**：latent video 表示，隐式 / pixel-level 一致性，无显式 metric 几何
- **重建路线 (3DGS / DUSt3R / VGGT)**：explicit geometry 表示（point / Gaussian / camera matrix），metric 精度（PSNR / pose error）

**两种合流的可能形态**：

- **Latent → metric**：world model 内部加显式 3D consistency loss（与 SfM / NeRF / 3DGS supervision 联合训练），让 latent 同时具 metric 几何
- **Metric → generative**：重建 model 加 video diffusion prior 做 sparse-view / extrapolation，让 reconstruction 在 unseen view 上具生成能力

**待观察**：

- 是否有 paper 在同一 benchmark（如 ScanNet / Tanks-and-Temples）同时报告 metric 精度（pose error / depth RMSE）与 generative 质量（PSNR / FID）
- VLA training 端是否需要 metric 几何（manipulation 时物体精确位置 / SLAM 闭环）
- 是否出现标准化 evaluation protocol 同时 cover 两类指标

### References

- [1] NVIDIA, GR00T N1.7: Action Cascade and EgoScale, huggingface.co/blog/nvidia/gr00t-n1-7 2026-04-17.
- [2] Physical Intelligence, π₀.5 release, physicalintelligence.company/blog/pi05 2025-04-22.

