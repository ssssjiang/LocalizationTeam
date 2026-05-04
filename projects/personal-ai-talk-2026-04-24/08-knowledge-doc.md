# AI 技术演进知识地图：从单点能力到闭环融合

## 整体趋势（业界主流叙事）

- AI 演进的近年走向：从「各管各的能力建设」走向「闭环融合」
- 4 老阶段建立单点能力；3 个新方向（推理 / VLA / World Models）在 2024-2026 年开始把这些能力合并成 agent
- 2026 年这件事已经从概念走到产品（GR00T N1.6 / Figure Helix 02 / Genie 3）
- 中国团队在 2025-2026 年的 frontier 模型 release 中占比明显上升

## 第一阶段：判别式 AI (2012-2015)

2012-2015 间，CNN / RNN / ResNet 在视觉端到端特征学习、序列建模、深网络优化退化三个方向出现关键工作；后续 Transformer / Diffusion / VLA 等架构沿用其中的核心组件（CNN backbone、ResNet 残差连接）。

### CNN：视觉端到端特征学习

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

<!-- REVIEW: 此处建议补 AlexNet architecture 图（Krizhevsky 2012 Fig. 2）。来源 [1]。 -->

### RNN：序列建模

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

### ResNet 与残差连接

ResNet 引入残差连接 `y = F(x) + x`[13]，解决了深网络的优化退化（degradation）问题。该机制后续在 Transformer[12]、Diffusion U-Net、具身机器人模型的视觉 head 等主流架构的 block 中被沿用，成为不绑定具体任务范式的通用组件。

#### 历史背景与退化现象

ResNet (He et al., 2015-12)[13] 之前，Highway Networks (Srivastava et al., NeurIPS 2015)[14] 已提出"门控 + 恒等通路"的思路：每层输出为 `y = T(x) · F(x) + (1 − T(x)) · x`，T(x) 是受 LSTM 启发的 sigmoid 门控函数。Highway 网络可训练 100+ 层，但门控参数随深度增加难以稳定收敛。

CNN 深度从 20 层加到 56 层时，训练误差与测试误差同时升高[13]。这一现象不能用过拟合解释——若是过拟合，训练误差应继续下降。该现象被归因为优化层面的退化：随深度增加，SGD (stochastic gradient descent) 在更复杂的损失曲面上更难找到与浅层网络等价的解[13]。Li et al. (NeurIPS 2018) 通过损失曲面可视化进一步证实，残差连接显著平滑了深网络的损失曲面，使 SGD 更易收敛[15]。

ResNet 把 Highway 的 T(x) 固定为 1，简化为无门控的恒等加和 `y = F(x) + x`，参数更少、训练更稳定，并在 ImageNet 上得到验证。

#### 机制

每个 block 的输出由 `y = F(x)` 改为 `y = F(x) + x`[13]。F 学到 0 时 block 退化为恒等映射；更深的网络至少不会比更浅的等价网络更差，给优化器一条保底通路。

反向传播时，残差连接为梯度提供一条 unit-multiplier 通路：`∂L/∂x = ∂L/∂y · (1 + ∂F/∂x)`。即使 F 部分的梯度衰减为 0，外层梯度也能经 `1` 这条通路直接传至浅层，缓解深网络中常见的梯度衰减问题[13]。

<!-- REVIEW: 此处建议补 He et al. 2015 论文 Fig. 2（残差块结构图）。来源 [13]。 -->

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

#### 工作机制的另一种解释

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

## 第二阶段：Transformer 范式 (2017-2026)

Transformer (Vaswani et al., 2017) 用 self-attention 替代 RNN 循环，解决并行 + 长距离依赖两个硬伤；后续 9 年间经 Scaling Law / RLHF / 多模态 / 推理 scaling 几次范式扩展，演变为 LLM 工业化的统一基底。

### Transformer：注意力机制

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

<!-- REVIEW: 此处建议补 Transformer architecture 图（Vaswani 2017 Fig. 1）。来源 [1]。 -->

### Scaling Law 与 GPT-3

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

### ChatGPT 与 RLHF

ChatGPT (OpenAI 2022-11-30)[12] 的技术基底 = GPT-3.5 + InstructGPT-style RLHF (Ouyang et al., NeurIPS 2022)[13]。

#### RLHF 三阶段[13]

- **SFT (supervised fine-tuning)**：用人类示范回复做 supervised learning，让 base model 学会对话格式
- **Reward model**：让人类对多个候选回复排序，训一个 reward model 模拟人类偏好
- **PPO RL**：用 reward model 作 reward signal，PPO 优化 policy LM

设计目标 = 三 H (helpful / harmless / honest)。RLHF 思想源自 Christiano et al. (NIPS 2017)[14] 的 RL from human preferences。

#### 产品意义

ChatGPT 5 天 100 万用户、2 个月 1 亿用户。技术上 GPT-3.5 + RLHF 不是飞跃 (InstructGPT 2022-01 已上线)，但产品形态 (对话 UI + alignment to human preference) 是 LLM 第一次被普通用户日常使用的关键节点。后续 Anthropic Claude (Constitutional AI, Bai et al., 2022)[15]、DeepSeek R1 (RL-from-base, 2025-01) 均沿用 RL-from-feedback 思路。

### 2026 主线大模型

2024-2026 间 LLM frontier 由 OpenAI / Google DeepMind / Anthropic 三家闭源 + Mamba 类替代架构线推进。截至 2026-05-04 主流 release：

| 模型             | 公司              | Release    | Context    | 关键特点                                                                     | 价格 (in/out per M) |
| -------------- | --------------- | ---------- | ---------- | ------------------------------------------------------------------------ | ----------------- |
| GPT-5.5        | OpenAI          | 2026-04-23 | 1M         | smartest to date；agentic coding / computer use 强化，speed 同 5.4            | TBD               |
| Gemini 3.1 Pro | Google DeepMind | 2026-02-19 | 1M / 64K out | ARC-AGI-2 77.1%；Deep Think (02-12) / Flash TTS (04-15) / Enterprise Agent Platform (04-22) 配套 | TBD               |
| Claude Opus 4.7 | Anthropic       | 2026-04-16 | 1M         | 长程编码 verification，长任务 self-check                                          | $5 / $25          |
| Mamba-3         | Princeton + CMU | 2026-03    | 长序列        | State Space Model，O(n) 时间 + 常数显存                                          | open              |

#### 主线方向

- **GPT-5.5** (OpenAI 2026-04-23)[18]：比 GPT-5.4 在 agentic coding / computer use (browser / OS automation) 显著强化；推理 cost / speed 同 5.4
- **Gemini 3.1 Pro** (Google DeepMind 2026-02-19)[19]：1M 输入 / 64K 输出；配套 Deep Think (2026-02-12 推理模式) + Flash TTS (2026-04-15) + Enterprise Agent Platform (2026-04-22)，Gemini 系列从单一 LLM 扩展为 agent 工具链
- **Claude Opus 4.7** (Anthropic 2026-04-16)[20]：长程编码 verification 机制 — 模型在长任务中段自检 + 修正；$5 / $25 per M token，定价显著高于 Gemini / DeepSeek 同档

#### 架构线：Mamba 与 SSM

Mamba (Gu & Dao, 2023)[16] 用 selective State Space Model (SSM) 替代 self-attention，推理时间复杂度 O(n) + 常数显存（vs Transformer O(n²) + O(n) KV cache）；在 1B-3B scale 与 Transformer 持平。Mamba-2 (Dao & Gu, ICML 2024)[17] 引入 SSD (state-space duality) 框架，把 SSM 与 attention 统一。Mamba-3 (2026-03) 在 1.5B 上准确率较 Mamba-2 +2pt，state size 减半。

主流 frontier 模型仍以 Transformer 为主干；Mamba / SSM 在长序列 / 长 context / inference cost 敏感场景作为补充，多在 hybrid 架构 (Jamba 等，Mamba + Transformer block 交替) 中出现。

### 国内大模型

国内 frontier LLM 在 2025-2026 出现 4 家主线：Alibaba Qwen / Moonshot Kimi / Zhipu GLM / DeepSeek。截至 2026-05-04 主流 release：

| 模型                    | 公司       | Release    | 参数量              | Context | 开源闭源                  | 定位                |
| --------------------- | -------- | ---------- | ---------------- | ------- | --------------------- | ----------------- |
| Qwen3.6-Max-Preview   | Alibaba  | 2026-04-20 | 1T+ MoE 稀疏        | 256K    | API only              | coding agent      |
| Kimi K2.6             | Moonshot | 2026-04-21 | 1T MoE / 32B active | 256K    | open-weight (Modified MIT) | long-context + agent |
| GLM-4.6               | Zhipu    | 2025-09    | 355B MoE / 32B active | 200K    | open-weight           | 企业级落地 + 代码        |
| DeepSeek V4           | DeepSeek | 2026-04    | TBD              | TBD     | open-weight           | base + 推理 cost 优化 |

#### 主线特点

- **Alibaba Qwen 系列**[21]：全家族开源 + scaling 路线。Qwen3 (2025-04 起) 0.6B → 235B MoE 全开源；Qwen3-Max (2025-10) 1T 参数，SWE-Bench 69.6% / Tau2-Bench 74.8%；Qwen3.5 Omni (2026-03) 原生多模态 + 256K；Qwen3.6-Max-Preview (2026-04-20) 进一步扩到 1T+ MoE 稀疏，API-only，主打 coding agent
- **Moonshot Kimi 系列**[22]：agent 与 long-context 路线。Kimi K2 (2025-07) 1T MoE 开源 (Apache 2.0)；K2.5 (2026-01-27) self-directed agent swarm (100 sub-agents 并行 + 1500 tool 同时调用，速度比 single-agent ~4.5×)；K2.6 (2026-04-21) 1T MoE / 32B active，open-weight Modified MIT，agent benchmark 与 GPT-5 / Claude 同档
- **Zhipu GLM 系列**[23]：小尺寸高性能 + 国产芯片适配。GLM-4.6 (2025-09) 355B MoE / 32B active，200K context；LMArena 第 4 (国内并列第一)；代码能力对标 Claude Sonnet 4
- **DeepSeek 系列**[24]：cost / quality 极致优化路线。V3 (2024-12) → V3.5 → V4 (2026-04, base) → R1 (2025-01 推理) → R2 (2026-04 推理 32B dense，单 24GB GPU 可跑)；推理线相关详见 §4.6 +推理融合 节内 inline 简介

#### Frontier 现状

2025-2026 的 frontier release 中，国内 4 家在多个维度站到第一梯队：开源生态 (Qwen / Kimi / GLM 全开源)、agent benchmark (Kimi K2.6)、推理 cost (DeepSeek R2)、coding (Qwen3.6-Max / GLM-4.6)。同期闭源 frontier 仍由 OpenAI / Google / Anthropic 三家把持，绝对差距收窄到月级。

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
- [16] Gu & Dao, Mamba: Linear-Time Sequence Modeling with Selective State Spaces, arXiv 2023. arXiv:2312.00752
- [17] Dao & Gu, Transformers are SSMs (Mamba-2), ICML 2024. arXiv:2405.21060
- [18] OpenAI, Introducing GPT-5.5, openai.com/index/introducing-gpt-5-5 2026-04-23.
- [19] Google DeepMind, Gemini 3.1 Pro Model Card, deepmind.google/models/model-cards/gemini-3-1-pro 2026-02-19.
- [20] Anthropic, Claude Opus 4.7, anthropic.com/news/claude-opus-4-7 2026-04-16.
- [21] Alibaba Qwen team, Qwen3.6-Max-Preview release, qwenlm.github.io 2026-04-20.
- [22] Moonshot AI, Kimi K2.6 release, deeplearning.ai/the-batch 2026-04-21.
- [23] Zhipu, GLM-4.6 release, zhipu.ai 2025-09.
- [24] DeepSeek, DeepSeek V4 release, deepseek.com 2026-04.

---

## 第三阶段：生成式 AI (2020-2024)

2020-2024 间，Diffusion 与 CLIP 分别在生成与跨模态对齐上 reach scale；与 GPT-4V 起多模态成为 LLM 的 standard configuration。这条线为 World Models（latent video）与 VLA（V-base = VLM）提供视觉基础。

### Diffusion 模型与 DDPM

Diffusion 模型把 "从噪声生成图像" 问题 cast 为 iterative denoising：给定图像 x_0，forward 过程逐步加 Gaussian 噪声直到 x_T ≈ N(0, I)；reverse 过程训练 model 预测每步去噪的 score（或直接预测噪声 ε）。训练 stable，scale 友好。

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

#### 应用线 (2022-2024)

- **DALL-E 2** (Ramesh et al., OpenAI 2022-04)[6]：CLIP latent + diffusion prior + diffusion decoder
- **Imagen** (Saharia et al., Google NeurIPS 2022)[7]：T5 text encoder + cascaded pixel diffusion
- **Midjourney** v3 (2022-08) → v5 (2023-03) → v6 (2024-04)：闭源，偏艺术风格
- **Stable Diffusion 1.x → 2.x → SDXL (2023-07) → SD3 (2024-02)**：开源主线；FLUX (Black Forest Labs 2024-08) 接力
- **视频扩展**：Stable Video Diffusion (2023-11)[9] / Sora (OpenAI 2024-02 technical report)[8] / Veo 3 (Google 2024-12)

<!-- REVIEW: 此处建议补 forward / reverse diffusion process 图（Ho 2020 Fig. 2）。来源 [1]。 -->

### CLIP 与多模态对齐

CLIP (Contrastive Language-Image Pre-training, Radford et al., OpenAI ICML 2021)[10] 用 contrastive learning 把图像与文本对齐到同一 embedding space。

#### 训练框架[10]

- **数据**：400M（图像，文本描述）pair，从 web 收集（WIT-400M）
- **Encoder**：image encoder (ViT-B/16, ViT-L/14, ResNet) + text encoder (Transformer)
- **Loss**：InfoNCE，把 batch 内对齐的 (image, text) 对作 positive，其他作 negative
- 训出后两个 encoder 共享 latent space，同义图文相似度高

#### Zero-shot 分类[10]

- 给定类别名 list（如 ImageNet 1000 类），把每类做 prompt template `a photo of a {class}`，编码得到 1000 个文本 embedding
- 输入图像编码后，计算与所有文本 embedding 的相似度，取最高者为类别
- ViT-L/14 在 ImageNet zero-shot top-1 ~76.2%，接近 supervised ResNet-50 baseline

#### 平行工作：ALIGN

ALIGN (Jia et al., Google ICML 2021)[11] 同期独立工作，用 1.8B noisy 图文对（vs CLIP 400M cleaner pairs），验证 contrastive pre-training scale 路线 robust。

#### 下游影响

- **Text-to-image generation**：Stable Diffusion / DALL-E 2 / Imagen 的 text encoder 都是 CLIP（或衍生的 OpenCLIP / T5）
- **Open-vocabulary detection / segmentation**：OWL-ViT (Minderer et al., ECCV 2022)[12] / GroundingDINO / SAM-2 prompt
- **VLM backbone**：LLaVA / Qwen-VL / InternVL 的 vision tower 通常用 CLIP-ViT（或 SigLIP）抽取 visual feature

CLIP 是后续 VLM 与 VLA（V-base = VLM）的 visual backbone 主流来源；§4.6 国际 VLA 节中 RT-2 / π₀ 等 model 内的 vision encoder 多溯源到 CLIP / SigLIP 系列。

<!-- REVIEW: 此处建议补 CLIP contrastive training 框图（Radford 2021 Fig. 1）。来源 [10]。 -->

### GPT-4V 与多模态大模型

GPT-4V (OpenAI 2023-09 system card)[13] 是 GPT-4 的视觉扩展版本，把图像作为另一种 token 输入 decoder-only LLM。多模态从此从单独研究方向变为 LLM 的 standard configuration。

#### LLaVA 与开源 VLM 路线 (Liu et al., NeurIPS 2023)[14]

LLaVA (2023-04) 用 minimum-effort 方案验证 VLM 可行性：

- Vision encoder (CLIP ViT-L/14 frozen) + projection (单层 linear / 后续 MLP) + LLM (Vicuna)
- 训练 stage 1：align projection (CC3M subset 558K pairs)
- 训练 stage 2：instruction tuning (GPT-4 generated 158K visual instruction data)

开源后成为 VLM 基本范式；LLaVA-1.5 (2023-10) 替换 projection 为 MLP，benchmark 进一步提升。

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
- [10] Radford et al., Learning Transferable Visual Models From Natural Language Supervision (CLIP), ICML 2021. arXiv:2103.00020
- [11] Jia et al., Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision (ALIGN), ICML 2021. arXiv:2102.05918
- [12] Minderer et al., Simple Open-Vocabulary Object Detection with Vision Transformers (OWL-ViT), ECCV 2022. arXiv:2205.06230
- [13] OpenAI, GPT-4V(ision) System Card, openai.com 2023-09.
- [14] Liu et al., Visual Instruction Tuning (LLaVA), NeurIPS 2023. arXiv:2304.08485
- [15] Bai et al., Qwen-VL, arXiv 2023. arXiv:2308.12966
- [16] Chen et al., InternVL, CVPR 2024. arXiv:2312.14238

---

## 第四阶段：走向世界模型与具身（起源篇）

### 业界公认的意义

- 这阶段两个节点都不是当时最强技术，但事后看都指出了下一阶段会爆发的方向
- World Models = 概念领先实践 6 年的代表
- GEN-1 = 工程落地推动技术普及的代表

### World Models（2018, Ha & Schmidhuber）

#### 核心思想

- 让 AI 在内部建立"世界的模拟器"
- agent 在脑内想象 / 规划 / 推演，而非只在真实世界试错

#### V + M + C 架构

- V：VAE 把环境观察压缩成 latent
- M：RNN 预测下一个 latent
- C：简单 controller 在 latent space 决策
- Demo：CarRacing 完全在"梦里"训练，真实环境也 work

#### 6 年停滞

- 2018-2024 基本停留在 Atari 游戏 / 玩具机器人
- 无法 scale，画质差，不通用

#### 学界路线分歧（仍未有定论）

- LeCun 长期主张 AGI 核心是 world model，提出 JEPA 路线
- 主流 LLM 阵营则相信预训练 + 推理 scaling 可以走得很远
- 这是 AI 领域一条公开的、未解决的路线分歧

### GEN-1（2023.02, Runway）

#### 它是什么

- 第一个把 diffusion 思路系统用到视频生成的工业级产品

#### 它证明了什么

- 技术上不是最先进（后来 Sora、Veo 都更强）
- 但证明 diffusion 范式可扩展到视频，能处理时间一致性

#### 商业化意义

- 做成 SaaS，让非技术用户也能用
- AI 商业化的早期代表案例

---

## 延伸 1：推理大模型——LLM 的第二条 scaling law

### 业界共识

- 这一代 LLM 的提升主要不是「模型更大」，而是「模型想得更久」
- 推理 scaling 被视为 LLM 能力增长的第二条腿（test-time compute scaling）
- 业界普遍观察到护城河从「模型本身」转移到「数据飞轮 / 后训练工艺 / agent 编排 / 部署生态 / 应用场景」

### 时间线（OpenAI 主线）

- 2024.09.12 o1-preview：首次提出"内置推理"范式
- 2024.12.20 o3-preview：ARC-AGI-1 上 87.5% 震惊业界
- 2025.04.16 o3 正式发布；2025.06.10 o3-pro（MATH-500 98.1% / SWE-bench 61.5%）

### 关键证据：推理 scaling 曲线

- 给模型 1s / 10s / 100s 思考时间，AIME 通过率持续上升
- GPT-4o AIME 13% → o1 AIME 83%

### DeepSeek R1（2025.01）

- 开源对标 o1，成本显著低于 OpenAI
- 公开了完整训练 pipeline
- 业界普遍认为：推理大模型这条之前闭源垄断的路线，几个月就被开源追平

### 国内开源推理模型 2026 三种打法

#### DeepSeek R2（2026.04，本周）

- 32B dense transformer
- 单张 24GB 消费级 GPU（如 RTX 4090）就能跑
- AIME 2025 92.7%，128K 上下文，MIT license
- 路线：**小而精 + 后训练优化**

#### Kimi K2.5（2026.01.27）

- 1T MoE / 32B 激活 / 256K 上下文
- self-directed agent swarm：100 sub-agents 并行 + 1500 工具调用
- agent benchmark 上超过 GPT-5.2 / Claude 4.5 Opus / Gemini 3 Pro
- 路线：**agent 化 + 并行编排**

#### Qwen3-Max-Thinking（2025.10）

- 1T 参数 / 36T tokens 训练
- 配合 tool use + 推理 scaling 在 AIME 25 / HMMT 上拿到 100%
- 路线：**超大模型 + 推理 scaling**

#### 当前 SOTA 的全局描述

- 单模型 SOTA 仍是 OpenAI o3 系列
- 开源在 2026 把"推理能力 + 可部署性"组合做到了 frontier 水平
- 这一波开源主要由中国团队推进

---

## 延伸 2：具身 VLA——AI 第一次走出屏幕

### 业界共识

- VLA = Vision + Language + Action，让 AI 第一次直接输出动作，与物理世界形成闭环
- 学术与产业普遍认为 VLA 不会取代传统机器人控制和 SLAM，而是在它们之上叠加智能决策
- 一个完整具身 agent 通常被描述为三层：底层 SLAM/重建 → 中层 VLA → 上层任务规划

### VLA 国际时间线

#### 2023-2024 奠基

- 2023.07 Google DeepMind RT-2：开山之作
- 2024.10 Physical Intelligence π₀：首个跨形态通用基础模型

#### 2025 工程化

- 2025.02 Figure AI Helix：全上半身 + 双机协作 + 嵌入式低功耗 GPU
- 2025.03 NVIDIA GR00T N1：开源人形机器人 foundation model（双系统：VLM 推理 + Diffusion Transformer 动作）
- 2025.06 GR00T N1.5：加入 FLARE，可从人类视频学习
- 2025.10 Figure 03 硬件：掌内嵌摄像头 + 触觉传感器（3 克级别力感知），为大规模量产设计

#### 2026 三圈融合的拐点

- 2026.01 Figure Helix 02：三级架构（System 0/1/2），单一神经网络（10M 参数）替代 109,504 行 C++；**洗碗机连续 4 分钟自主操作**（目前最长最复杂的人形机器人自主任务）
- 2026.04.15 GR00T N1.6（4 天前）：内部 VLM 升级到 NVIDIA Cosmos-Reason-2B，Diffusion Transformer 翻倍（32 vs 16 层）

### VLA 国内时间线

#### 银河通用 GraspVLA（2025.01.09）

- 与智源 / 北大 / 港大合作
- **全球首个端到端具身抓取基础大模型**
- 预训练完全用合成数据（10 亿帧"视觉-语言-动作"对）
- 提出 VLA 基础模型"七大泛化金标准"（光照 / 背景 / 平面位置 / 空间高度 / 动作策略 / 动态干扰 / 物体类别）
- 配套机器人 Galbot 在 NVIDIA CES 2025 发布会托举 RTX 5090 出场

#### 智元 GO-1（2025.03.10）

- ViLLA 架构（Vision-Language-Latent-Action）
- MoE + Latent Planner + Action Expert 三件套
- 100 万条真实机器人 demonstration 训练（AgiBot World 数据集，217 个任务）
- 平均成功率 46% → 78%
- 业界普遍视为国内首个产品级 VLA + 公开大规模数据集的工作

#### 宇树 UnifoLM-VLA-0（2026 开源）

- 给 G1 装"具身 AI 大脑"：开药瓶 / 装网球拍 / 整理工具
- 基于阿里 Qwen2.5-VL-7B（Qwen 被国内具身公司直接用作 backbone 的真实案例）
- G1 售价 $13.5K（一个数量级低于 Figure 02）

### 国内 vs 国外打法对比（业内普遍观察）

- 硅谷（Figure / Physical Intelligence）：重金投入 + 全栈自研
- NVIDIA：开源 foundation model + 生态绑定
- 国内主流：硬件价格优势 + 开源 + 数据规模

### 三圈融合的两个最新信号（业界关注度最高）

#### VLA + 推理大模型

- Figure Helix 02 三级架构
  - System 0：实时平衡 1kHz
  - System 1：视觉运动 200Hz
  - System 2：高层推理
- 公开报告中明确借鉴 Kahneman「快思考 / 慢思考」
- 洗碗机 4 分钟连续自主任务由这个架构跑出来

#### VLA + World Models

- GR00T N1.6（4 天前）把内部 VLM 直接换成 NVIDIA Cosmos-Reason-2B
- NVIDIA 把自家 world model（Cosmos 系列）直接集成进 VLA 模型
- 业界普遍认为这是 VLA + World Model 融合首次进入产品级

---

## 延伸 3：World Models 的真正突破

### 业界共识

- 7 年后（2018→2025），world model 走出玩具任务，走向通用化 + 产品化
- 它代表 AI 理解世界的另一条路线（与 LLM 范式并列，而非替代）
- 业界观察到「重建世界」与「生成世界」两条线在工具上趋同（详见后文）

### 标志性事件 1：Genie 3（2025.08.05, DeepMind）

- 第一个面向公众的实时交互通用 world model
- 20-24 fps，720p，可保持几分钟一致性
- 用户从一张图或一段文字出发，可实时操控生成的 3D 环境探索
- 距 2018 Ha 那篇论文整整 7 年；业界普遍认为质变发生在 2024-2025 大模型基础设施齐备之后
- 跟 V+M+C 架构相比不是同一量级（训练规模、画质、可交互性都是 LLM 时代的产物）

### 标志性事件 2：NVIDIA Cosmos 成为 Physical AI 基础设施

- 2025.01 CES 发布；至今下载量超 200 万
- 三个模型族：
  - **Predict**：未来状态模拟
  - **Transfer**：仿真到现实迁移
  - **Reason**：物理推理
- 早期采用者：Figure AI / Uber / Waabi（VLA + 自动驾驶厂商）
- 2026.04 GR00T N1.6 直接用 Cosmos-Reason-2B 作为内部 VLM
- 业界普遍视为 world model 真正进入产品级的标志

### 重建侧：另一条对照线（2023-2025 飞速演进）

#### 3DGS（2023.07, Inria, SIGGRAPH 2023 best paper）

- 100+ fps 的 1080p 实时渲染
- 训练几分钟达到 Mip-NeRF360 画质
- 业界视为「重建已存在的世界」成本降低一个数量级的代表性工作

#### DUSt3R / MASt3R（Naver Labs, CVPR 2024）

- 给一组未标定图像，直接 transformer 输出 3D pointmap + 相机参数
- 改变了「传统 SLAM 依赖标定 + 多视几何」的范式
- map-free relocalization：中位平移误差 1.17 → 0.36，旋转误差砍 80%

#### VGGT（Meta + Oxford, CVPR 2025 best paper）

- feed-forward transformer，输入 1~几百张图，1 秒内输出相机 + 深度 + 点云 + 3D track
- 完全不需要传统 BA / 后处理优化
- 业界普遍视为 SfM 这件事被 transformer 端到端替代的标志

### 「重建 vs 生成」工具层面趋同（学界已开始讨论的现象）

#### 两条线在用越来越相似的工具

- transformer 主干
- foundation model 方向
- 海量数据预训练

#### 形式上相似的目标

- 3DGS 与 Genie 3 都是用神经网络表示 3D 世界
- 区别在数据来源（观察 vs 训练）和目标（精确重建 vs 可信生成）

#### 仍是开放问题

- 两条路线最终是融合、并存还是分化，目前学界没有定论
- 但 2027-2028 这是 AI 视觉/几何方向被广泛关注的战场之一

---

## 整体回收

### 一句话总结（业界主流叙事）

- AI 演进近年正在从「各管各的能力建设」走向「闭环融合」

### 老阶段：单点能力建立

- 第一阶段：AI 能学特征
- 第二阶段：AI 能 scale
- 第三阶段：AI 能创造、能跨模态理解
- 第四阶段：埋下 world model + 视频生成的种子

### 新方向：能力开始合并成 agent

- 推理大模型 → 让 AI **会想**
- VLA → 让 AI **会做**
- World Models → 让 AI 在脑内**演**

### 2026 已从概念走到产品（公开 release）

- 2026.04 NVIDIA GR00T N1.6 + Cosmos Reason 2：world model 直接吃进 VLA
- 2026.01 Figure Helix 02：三级架构完成 4 分钟洗碗机连续自主任务
- 2025.08 Genie 3：world model 第一次走向公众

### 中国格局（基于公开 release 的观察）

#### LLM 一线

- Qwen3.5 / GLM-4.6 / Kimi K2.5 / DeepSeek R2

#### 具身一线

- 银河通用 GraspVLA / 智元 GO-1 / 宇树 UnifoLM-VLA-0

#### 客观描述

- 2025-2026 年的 frontier release 中，中国团队的占比明显上升
- 在多个维度（开源生态 / 部署成本 / agent 编排 / 硬件价格）已经站在第一梯队

---

## 三个仍在讨论的开放问题（讨论环节用）

### Q1：scaling 的尽头

- 预训练 scaling + 推理 scaling 这两条腿还能跑多远？
- 撞墙时间？
- 撞墙后下一条 scaling 的腿可能是什么？
- 学界目前没有共识

### Q2：开源 vs 闭源的格局

- DeepSeek R1 让一个之前闭源垄断的方向（推理大模型）几个月被开源追平
- 这种「开源追赶速度」是会持续，还是 R1 是个例外？
- 大模型的护城河到底在哪？
- 业界讨论激烈但无定论

### Q3：具身智能的路径之争

- VLA（端到端）vs 传统机器人（分层规划）vs 完全 world model 驱动（LeCun JEPA）
- 哪条会赢？还是会融合？
- 这是当前具身领域最公开、最未解决的路线之争