# AI 演进笔记 (2012-2026)

## 1. 整体趋势

2012-2026 间 AI 演进经历 5 个 foundation 阶段（判别式 → Transformer → 视觉与视频生成 → 多模态理解 → World Models 起源）与 2 个延伸方向（具身 VLA / World Models 近期形态）。时间线：

- **2012-2015 判别式 AI**：AlexNet (NeurIPS 2012) / VGG / GoogLeNet / ResNet (CVPR 2016) — CNN 端到端特征学习
- **2017 Transformer**：Vaswani et al. — self-attention 替代 RNN，LLM 工业化基础
- **2020-2022 LLM scaling**：GPT-3 (NeurIPS 2020) / Chinchilla (NeurIPS 2022) / ChatGPT (2022-11)
- **2020-2024 视觉与视频生成**：DDPM (NeurIPS 2020) → Stable Diffusion (2022-08) → Sora (2024-02)
- **2020-2024 多模态理解**：CLIP (ICML 2021) → GPT-4V (2023-09) → LLaVA (NeurIPS 2023)
- **2018 / 2023 World Models 起源**：Ha & Schmidhuber (NeurIPS 2018) V+M+C / Runway GEN-1 (2023-02)
- **2023-2026 具身 VLA**：RT-2 (2023-07) → π₀ (2024-10) → π₀.7 (2026-04-16) / Helix 02 (2026-01) / GR00T N1.7 (2026-04-17)
- **2024-2026 World Models 近期形态**：Genie 3 (2025-08) / Cosmos (2025-01 起)

本笔记按「演进路径 + 应用扩展 + 解决的问题」组织。覆盖 AI 整体演进的主线脉络（CNN/RNN → ResNet → Transformer → LLM → Diffusion → CLIP/VLM → World Models / VLA），不做 frontier 模型横扫；具体模型列表见 `09-sweeper-embodied-roadmap.md` §1 行业技术现状地图。LLM 推理模型（OpenAI o1 / o3、DeepSeek R1 / R2、Qwen3-Max-Thinking、Kimi K2.5 等）只在 §7.2.1 VLA + 推理融合 中作为背景简述。

## 2. 第一阶段：判别式 AI (2012-2015)

2012-2015 间，CNN / RNN / ResNet 分别推进了视觉端到端特征学习、序列建模和深网络训练。后续 Transformer / Diffusion / VLA 等架构继续沿用其中的组件，例如 CNN backbone 与 ResNet 残差连接。

### 2.1 CNN：视觉端到端特征学习

AlexNet (Krizhevsky et al., NeurIPS 2012)[1] 在 ImageNet ILSVRC-2012（1.2M 图像 / 1000 类）上把 top-5 错误率从 SIFT-FV (Fisher Vector) baseline 的 25.8% 降到 15.3%[1, 2]。在这一范式里，传统的 SIFT / HOG 特征工程 + 分类器流程被端到端 CNN 替代：原始 RGB 图像输入网络，经多层卷积提特征，最后由 softmax 输出类别。AlexNet 沿用 LeNet (LeCun et al., Proc. IEEE 1998)[6] 在 MNIST 上确立的卷积 + pooling + 全连接模板，并把它扩展到 ImageNet 规模数据和 GPU 训练。

#### 2.1.1 关键设计

AlexNet 关键构件[1]：

- **网络架构**：5 层卷积 + 3 层全连接，60M 参数；当时 NVIDIA GTX 580 单卡 3GB VRAM 装不下，采用双 GPU 数据并行
- **训练方法**：ReLU 激活函数替代 sigmoid / tanh，加速收敛；Dropout (Hinton et al., 2012)[3] 减轻过拟合；Local Response Normalization 后续被 BatchNorm 替代

#### 2.1.2 后续推进

后续工作继续沿「更深 / 更宽 / 更高效」方向改进 CNN：

- VGG (Simonyan & Zisserman, ICLR 2015)[4]：加深到 16-19 层，全部用 3×3 卷积；ImageNet top-5 错误率 7.32%
- GoogLeNet / Inception (Szegedy et al., CVPR 2015)[5]：Inception module 多尺度分支并联；top-5 6.67%，参数量较 VGG 小 ~12×

### 2.2 RNN：序列建模

RNN (Recurrent Neural Network) 用 hidden state 在时间步之间传递信息，因此可以处理文本、语音等序列数据。RNN 在 1980-1990s 已提出，实用化集中在 2014-2017 年，例如 Sutskever 2014 seq2seq[7] 与 Bahdanau 2014 attention[8]。

#### 2.2.1 主要 variant

- **vanilla RNN**：用 `h_t = tanh(W_h h_{t-1} + W_x x_t)` 更新 hidden state；长序列训练中容易出现梯度衰减或梯度爆炸
- **LSTM** (Hochreiter & Schmidhuber, Neural Computation 1997)[9]：引入 input / forget / output 三个门控和 cell state，缓解长序列梯度衰减；2014-2017 年是 NMT / speech 主流 backbone
- **GRU** (Cho et al., EMNLP 2014)[10]：简化 LSTM 为 update / reset 两门，参数比 LSTM 少 ~25%，多数任务上性能相当

#### 2.2.2 应用

RNN 在两个领域替代了部分传统多模块流程：

- **NMT** (Neural Machine Translation)：Sutskever et al. (NeurIPS 2014)[7] 用 encoder-decoder LSTM 在 WMT'14 EN-FR 上达到 BLEU 34.81（vs phrase-based SMT 33.30）
- **Speech recognition**：DeepSpeech (Hannun et al., 2014)[11] 用 RNN + CTC loss 替代传统 HMM-GMM pipeline，WER 在 Switchboard 上 16%（vs 商业 baseline 18.4%）

#### 2.2.3 已知局限

RNN 在 2017 年后被 Transformer 在 NMT / LM 主线快速取代，主要因：

- **串行依赖**：当前 step 依赖前一 step 的 hidden state，难以在 GPU 上并行计算
- **长距离依赖衰减**：即使使用 LSTM，也只能较稳定地捕获约 100-1000 step 内的信息

这两条由 Transformer (Vaswani et al., NeurIPS 2017)[12] 同时解决。

### 2.3 ResNet 与残差连接

ResNet 引入残差连接 `y = F(x) + x`[13]，解决了深网络的优化退化（degradation）问题。该机制后续在 Transformer[12]、Diffusion U-Net、具身机器人模型的视觉 head 等主流架构的 block 中被沿用，成为不绑定具体任务范式的通用组件。

本节按「问题 → 方法 → 影响」展开：先说明深网络为什么会出现优化退化，再说明残差 block 如何提供恒等通路，最后说明残差连接为什么能跨架构沿用。

#### 2.3.1 起因

ResNet (He et al., 2015-12)[13] 之前，Highway Networks (Srivastava et al., NeurIPS 2015)[14] 已提出"门控 + 恒等通路"的思路：每层输出为 `y = T(x) · F(x) + (1 − T(x)) · x`，T(x) 是受 LSTM 启发的 sigmoid 门控函数。Highway 网络可训练 100+ 层，但门控参数随深度增加难以稳定收敛。

CNN 深度从 20 层加到 56 层时，训练误差与测试误差同时升高[13]。这一现象不能用过拟合解释：若是过拟合，训练误差应继续下降，测试误差才会上升。普通深层 CNN 理论上可以让额外层学习恒等映射，从而复现浅层网络的解；但没有残差连接时，SGD (stochastic gradient descent) 很难把这些额外层优化成恒等映射，训练误差因此升高[13]。Li et al. (NeurIPS 2018) 通过损失曲面可视化进一步说明，残差连接能让深网络的损失曲面更平滑，使 SGD 更易收敛[15]。

ResNet 把 Highway 的 T(x) 固定为 1，简化为无门控的恒等加和 `y = F(x) + x`，参数更少、训练更稳定，并在 ImageNet 上得到验证。

#### 2.3.2 解决

**残差 block 与梯度路径**

每个 block 的输出由 `y = F(x)` 改为 `y = F(x) + x`[13]。如果 `F(x)` 学到 0，这个 block 就退化为恒等映射；更深网络可以通过这种方式复现浅层网络的解，给优化器一条保底通路。

对残差 block `y = F(x) + x`，反向传播时梯度不仅经过 `F(x)` 分支，也能沿 `+x` 的恒等分支直接回传：`∂L/∂x = ∂L/∂y · (1 + ∂F/∂x)`。即使 `F(x)` 分支的梯度很小，恒等分支中的 `1` 仍会把外层梯度传到浅层，缓解深网络中的梯度衰减[13]。

ResNet 用了两种 block 设计[13]：

- **Basic block**（用于 ResNet-18 / 34）：两个 3×3 卷积后与输入做残差加和
- **Bottleneck block**（用于 ResNet-50 / 101 / 152）：采用 1×1 → 3×3 → 1×1 三层卷积后再做残差加和。前后两个 1×1 卷积先压缩通道再恢复通道，使参数量和计算量低于直接堆叠 3×3 卷积

He et al. 在 Pre-activation 工作（ECCV 2016）[16] 把 BN 与 ReLU 移到卷积之前（即 BN-ReLU-Conv 而非 Conv-BN-ReLU），让残差通路更接近纯恒等映射，可训练深度从 152 层扩展到 1001 层。

**ImageNet 实验**

ResNet 在 ImageNet 上的 top-5 错误率随深度变化（来源：[13] Table 4，single-model single-crop）：


| 模型         | 错误率   | 参数量   |
| ---------- | ----- | ----- |
| ResNet-18  | 7.55% | 11.7M |
| ResNet-34  | 6.50% | 21.8M |
| ResNet-50  | 5.71% | 25.6M |
| ResNet-101 | 5.05% | 44.5M |
| ResNet-152 | 4.49% | 60.2M |


ResNet-152 ensemble 后达到 3.57%[13]。同期对照：GoogLeNet 6.67%、VGG 7.32%、AlexNet (2012) 15.3%[1]。ResNet 在一年内取代 VGG / GoogLeNet 成为下游 CV 任务的默认 backbone：COCO 目标检测 mAP 从 33.5（VGG-Faster R-CNN）提升到 37.4（ResNet-101-Faster R-CNN）[13]；ImageNet localization 错误率从 19.4% 降到 9.0%[13]。

#### 2.3.3 影响

**后续理论解释 (ensemble view + loss landscape)**

Veit et al. (NeurIPS 2016)[17] 提出 ResNet 行为更接近"相对浅网络的 ensemble"：在已训练的 ResNet 中删除任意一个 block，输出几乎不变；这表明残差通路提供了多条并行路径，网络的实际有效深度远小于其名义深度。该机制层面的两类解释——He et al. 的 identity mapping 通路[13] 与 Veit et al. 的 ensemble 路径[17]——均有论文支撑且并不互斥，提示残差连接可能同时提供了"恒等映射的可达性"与"梯度路径的多样性"两类作用。

**跨架构延续**

残差连接在三大领域的主流架构中均有沿用：

- **Transformer 系**（NLP / LLM 主线）：每个 attention 或 FFN 子层外都加残差连接和 LayerNorm，即先计算 `x + Sublayer(x)`，再做归一化[12]；后续 LLM / VLM / VLA 大量复用这一 block 模板
- **视觉与生成模型**：
  - **DenseNet** (Huang et al., CVPR 2017)[18]：把 sum 改为前序所有层的 concat，使每层都能直接看到所有前序特征
  - **ResNeXt** (Xie et al., CVPR 2017)[19]：在残差 block 内加入分组卷积，用多组并行卷积分支替代单一路径；`cardinality` 指这些并行分支的数量
  - **Diffusion U-Net**：encoder / decoder 之间用 skip connection 跨层 concat，结构上是残差思路的另一变种
- **具身机器人模型**：视觉 / 动作 head 的基础 block 多含残差结构

CNN 的卷积、RNN 的循环都带有特定任务假设；残差连接不同，它主要为深网络优化提供一条线性直通路径，不绑定某一类任务。这个特性使残差连接可以与卷积、attention 等不同结构叠加，并在 CNN[13]、Transformer[12]、Diffusion U-Net、具身视觉 head 等架构中沿用。

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

Transformer (Vaswani et al., 2017) 用 self-attention 替代 RNN 循环，同时解决并行训练和长距离依赖两个问题。后续 Scaling Law、RLHF、多模态和推理模型都建立在这一可扩展架构之上，Transformer 因此成为 LLM 工业化的基础结构。

### 3.1 Transformer：注意力机制

Transformer (Vaswani et al., NeurIPS 2017)[1] 用 self-attention 和 position-wise FFN 取代 RNN 循环结构与 CNN 卷积。self-attention 负责让不同 token 直接交互；position-wise FFN 对每个 token 的表示单独做非线性变换。在 WMT'14 EN-DE 翻译任务上，Transformer BLEU 达到 28.4，超过当时 RNN encoder-decoder baseline 的 25.16[1]。

#### 3.1.1 关键设计

- **Attention 机制**：Scaled dot-product `Attention(Q, K, V) = softmax(QK^T / √d_k) V`[1]，其中 Q 表示当前 token 要查找的信息，K 表示其他 token 可被匹配的信息，V 表示被关注后提供的内容；`√d_k` 缩放避免 softmax 进入饱和。Multi-head attention 用多套线性变换生成多组 Q / K / V，并行计算多次 attention；不同 head 可以关注不同 token 关系，最后把结果拼接输出
- **Position encoding**：self-attention 本身不包含词序信息；Transformer 需要额外加入 positional encoding，让每个 token 的表示同时包含「词义」和「位置」。原始 Transformer 使用 sin / cos 生成固定位置编码，后续 LLM 多使用 RoPE 等方案
- **架构组合**：原始 Transformer 采用 encoder-decoder 结构：encoder 编码源序列，decoder 根据 encoder 输出生成目标序列。每个 attention 或 FFN 子层外都加残差连接和 LayerNorm，即先计算 `x + Sublayer(x)`，再做归一化；其中残差连接沿用了 ResNet 的 `F(x) + x` 思路[2]

#### 3.1.2 解决两个硬伤

- **并行性**：self-attention 可用矩阵运算一次性计算所有 token 之间的关系，适合 GPU 并行；RNN 必须按时间步串行计算
- **长距离依赖**：任意两个 token 可直接交互，不必经过一串 hidden state 传递；LSTM 通常只能较稳定地捕获约 100-1000 step 内的信息

#### 3.1.3 三派与影响

Transformer 之后 LLM 主要分三派架构：

- **encoder-only** (BERT, Devlin et al., NAACL 2019)[3]：只保留 Transformer encoder，通过 masked language modeling 训练模型根据上下文补全被遮住的词；输出的是上下文语义表示，适合文本分类、实体识别、句子匹配等语言理解任务
- **decoder-only** (GPT, Radford et al., 2018)[4]：只保留 Transformer decoder，通过 causal language modeling 训练模型从左到右预测下一个 token；生成时每次输出一个 token，再把该 token 接回上下文继续生成。后续 LLM 多采用这一结构
- **encoder-decoder** (T5, Raffel et al., JMLR 2020)[5]：保留 encoder 和 decoder，把翻译、摘要、分类、问答等任务都改写成「文本输入 → 文本输出」格式，因此不同 NLP 任务可以用同一套模型结构和训练形式处理

Attention 机制本身在 Bahdanau et al. (ICLR 2015)[6] 中已用于 NMT (Neural Machine Translation, 神经机器翻译)：生成目标语言每个词时，模型会动态关注源语言句子中最相关的位置。Transformer 的变化不是首次使用 attention，而是去掉 RNN 循环结构，把 self-attention 作为序列建模主干；self-attention 可并行计算，任意两个 token 也可直接交互。后续 Scaling Law 在这一可并行架构上验证了参数量、数据量与计算量扩大后的可预测收益。

### 3.2 Scaling Law 与 GPT-3

Kaplan et al. (OpenAI 2020)[7] 实验拟合：LLM cross-entropy loss 与参数量 N、数据量 D、计算量 C 呈幂律：

`L(N) ∝ N^-0.076`、`L(D) ∝ D^-0.095`、`L(C) ∝ C^-0.05`[7]

含义：给定计算预算后，可以估算较优的参数量 N、数据量 D 配比以及最终 loss。这使模型设计从频繁尝试新架构，转向在既有 Transformer 架构上扩大模型、增加数据并调整训练流程。

#### 3.2.1 GPT-3 (2020)

GPT-3 (Brown et al., NeurIPS 2020)[8] 175B 参数，300B token 训练。

- in-context learning (few-shot)：不更新模型参数，只在 prompt 中给少量任务示例，模型就能按示例格式完成翻译、问答、算术和代码生成等任务
- 性能曲线随模型规模平滑提升，与 Kaplan 2020 的 scaling law 预测一致

#### 3.2.2 Chinchilla 修正 (2022)

Kaplan 2020 的最优配比让早期 LLM 更偏向增加参数量；Hoffmann et al. (DeepMind 2022)[9] 通过 400+ 个实验修正了这一结论：在固定算力下，参数量 N 和训练 token 数 D 应同步增加，约为 1B 参数对应 20B token。Chinchilla 只有 70B 参数，但用 1.4T token 训练，性能超过 280B 参数、300B token 的 Gopher；这说明 GPT-3 / Gopher 这类模型参数很大，但训练数据不足。

#### 3.2.3 Emergent abilities 与争议

Wei et al. (TMLR 2022)[10] 列出 137 个 BIG-Bench 任务的 emergence 曲线：部分任务（如 multi-step arithmetic / chain-of-thought）在小模型上接近随机，但模型规模超过某个阈值后表现明显上升，这类现象被称为 emergent abilities。

Schaeffer et al. (NeurIPS 2023)[11] 提出反例：很多「突然上升」来自 exact-match 这类离散指标，答案只要不完全正确就记 0 分，因此平滑进步会被显示成跳变。换成连续评价指标后，部分任务的性能曲线变得平滑。Emergence 是否真实仍是开放问题。

### 3.3 ChatGPT 与 RLHF

ChatGPT (OpenAI 2022-11-30)[12] 的技术基底 = GPT-3.5 + InstructGPT-style RLHF (Ouyang et al., NeurIPS 2022)[13]。

#### 3.3.1 RLHF 三阶段

- **SFT (supervised fine-tuning)**：用人类示范回复做监督微调，让 base model 学会对话格式
- **Reward model**：让人类对多个候选回复排序，训一个 reward model 模拟人类偏好
- **PPO RL**：用 reward model 作 reward signal，PPO 优化 policy LM

设计目标是三 H：helpful / harmless / honest。RLHF 思想源自 Christiano et al. (NIPS 2017)[14] 的 RL from human preferences。

#### 3.3.2 产品意义

ChatGPT 5 天达到 100 万用户、2 个月达到 1 亿用户。GPT-3.5 + RLHF 的技术组合在 InstructGPT 2022-01 已出现，但 ChatGPT 把对话 UI 与人类偏好对齐结合起来，使 LLM 进入普通用户的日常使用场景。后续 Anthropic Claude (Constitutional AI, Bai et al., 2022)[15]、DeepSeek R1 (RL-from-base, 2025-01) 均沿用 RL-from-feedback 思路。

ChatGPT 之后 (2024-2026)，LLM frontier 由 OpenAI / Google DeepMind / Anthropic 三家闭源主线，以及 Alibaba / Moonshot / Zhipu / DeepSeek 等国内开源或开放权重主线推进。主流 release 包括 GPT-5.5 / Gemini 3.1 Pro / Claude Opus 4.7 / Qwen3.6-Max / Kimi K2.6 / GLM-4.6 / DeepSeek V4 等；架构线另有 Mamba 系列 (SSM) 在长 context / inference cost 敏感场景作为 Transformer 替代。本笔记聚焦「演进 → 解决什么问题 → 应用扩展」主线，不展开 frontier 横扫；具体模型参数、benchmark 与价格对比见 `09-sweeper-embodied-roadmap.md` §1 行业技术现状地图。

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

2020-2024 间，Diffusion 成为图像 / 视频生成主线：DDPM (NeurIPS 2020) 定义逐步去噪框架，DDIM 加速采样，Latent Diffusion / Stable Diffusion (CVPR 2022) 降低计算量，DALL-E 2 / Imagen / Midjourney / Sora / Veo 把这条路线带入产品应用。本节按方法演进与应用扩展两条线展开。

### 4.1 方法演进 (Diffusion 主线)

Diffusion 模型把图像生成写成「逐步去噪」问题。训练时先把真实图像 `x_0` 一步步加高斯噪声，直到接近纯噪声 `x_T`；模型学习反向过程：给定带噪图像 `x_t` 和步数 `t`，预测其中的噪声并逐步去掉。DDPM 定义了这一框架；DDIM 减少去噪步数，Latent Diffusion 把去噪搬到压缩后的 latent space 以降低计算量；Guidance 则让生成结果受文本或类别等条件控制。

#### 4.1.1 基础：DDPM (2020)

DDPM (Ho et al., NeurIPS 2020)[1] 是现代 Diffusion 的起点：训练时逐步加噪，生成时从纯噪声逐步去噪。

- **Forward**：`q(x_t | x_{t-1}) = N(x_t; √(1-β_t) x_{t-1}, β_t I)`，表示从 `x_{t-1}` 到 `x_t` 时按 `β_t` 指定的强度加入高斯噪声；`β_t` 是 noise schedule，即每一步加多少噪声的时间表
- **Reverse**：模型 `ε_θ(x_t, t)` 输入带噪图像 `x_t` 和步数 `t`，预测这一步加入的噪声 `ε`；训练损失 `L = E[||ε - ε_θ(x_t, t)||²]` 让预测噪声接近真实噪声
- **采样步数**：原始 DDPM 通常设 `T=1000`，生成一张图需要从 `x_T` 逐步去噪到 `x_0`，因此约需 1000 次模型前向推理

#### 4.1.2 效率优化

效率优化沿两个方向展开：DDIM 减少采样步数，Latent Diffusion 降低每一步的计算量。

**加速 sampling：DDIM (2021)**

DDIM (Song et al., ICLR 2021)[2] 改写了 diffusion 的反向采样路径：生成时不必严格按 `x_T → x_{T-1} → ... → x_0` 逐步去噪，而是可以跳过大量中间时间步，并在确定性路径上生成图像。

- 原始 DDPM 约 1000 步的采样过程可压缩到约 50 步，图像质量损失较小
- 后续 DPM-Solver / EDM 等采样器进一步把步数压到 10-20 步

**降算力：Latent Diffusion (2022)**

Latent Diffusion (Rombach et al., CVPR 2022)[5] 不直接在像素空间去噪，而是先用 VAE encoder 把图像压缩到 latent space（典型 4× downsample），再在 latent space 做 diffusion，因此显著降低计算量。Stable Diffusion (2022-08，open-weight) 基于 LDM + LAION-5B 训练，是早期可在消费级 GPU（8GB VRAM）上运行的 text-to-image 模型；开源后带动 ControlNet (2023-02)、LoRA、ComfyUI 等社区生态。

#### 4.1.3 条件控制：Guidance

- **Classifier guidance** (Dhariwal & Nichol, NeurIPS 2021)[3]：额外训练一个分类器 `p(y|x_t)`，反向去噪时用分类器梯度 `∇_x log p(y|x)` 把生成结果推向目标类别
- **Classifier-free guidance** (Ho & Salimans, 2022)[4]：同一个模型同时学习有条件和无条件生成，采样时混合两种噪声预测 `ε = ε_uncond + w · (ε_cond - ε_uncond)`；它不需要单独分类器，是当前 text-to-image 主流做法

### 4.2 应用扩展 (2022-2024)

应用扩展沿图像和视频两条线展开：

- **图像生成**（按 release 时间序）：
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

2020-2024 年，多模态理解沿两条线发展：CLIP (ICML 2021) 用对比学习把图像和文本编码到同一个向量空间，使图文可以直接匹配；GPT-4V (2023-09) 则把图像输入接入 LLM，让语言模型可以基于图片回答问题。前者解决图文表征对齐，后者把视觉理解并入 LLM；这两条线共同构成后续 VLM 和 VLA 的视觉理解基础。

### 5.1 CLIP 与多模态对齐

CLIP (Contrastive Language-Image Pre-training, Radford et al., OpenAI ICML 2021)[1] 用 contrastive learning 训练图像 encoder 和文本 encoder，把图像与文本映射到同一个 embedding space。

#### 5.1.1 训练框架

- **数据**：400M 对图像和文本描述，从 web 收集（WIT-400M）
- **Encoder**：image encoder (ViT-B/16, ViT-L/14, ResNet) 把图像编码成向量，text encoder (Transformer) 把文本编码成向量
- **Loss**：InfoNCE 在一个 batch 内把原本配对的 (image, text) 作为正样本，把错配图文作为负样本；训练目标是提高正样本图文向量的相似度，同时降低错配图文向量的相似度

训练完成后，两个 encoder 输出到同一个 latent space；语义匹配的图像和文本向量相似度更高。同期 Google 的 ALIGN (Jia et al., ICML 2021)[2] 采用类似的图文对比学习框架，但训练数据扩大到 1.8B 对网页图文。相比 CLIP 的 400M 对相对清洗数据，ALIGN 的数据规模更大、噪声也更高；其结果说明图文对比预训练在大规模 noisy 数据上仍能学到有效的跨模态表示。

#### 5.1.2 Zero-shot 分类

- 给定类别名列表（如 ImageNet 1000 类），把每类写成 prompt template `a photo of a {class}`，编码得到 1000 个文本 embedding
- 输入图像编码后，计算图像 embedding 与所有文本 embedding 的相似度，取相似度最高的类别
- ViT-L/14 在 ImageNet zero-shot top-1 ~76.2%，接近 supervised ResNet-50 baseline

#### 5.1.3 下游影响

- **Text-to-image generation**：Stable Diffusion / DALL-E 2 / Imagen 的 text encoder 都是 CLIP（或衍生的 OpenCLIP / T5）
- **Open-vocabulary detection / segmentation**：OWL-ViT (Minderer et al., ECCV 2022)[3] / GroundingDINO / SAM-2 prompt
- **VLM backbone**：LLaVA / Qwen-VL / InternVL 的 vision tower 通常用 CLIP-ViT（或 SigLIP）抽取视觉特征

CLIP 是后续 VLM 与 VLA（V-base = VLM）中视觉 backbone 的常见来源；§7.1.1 国际 VLA 节中 RT-2 / π₀ 等模型的 vision encoder 多来自 CLIP / SigLIP 系列。

### 5.2 GPT-4V 与多模态 LLM

GPT-4V (OpenAI 2023-09 system card)[4] 是 GPT-4 的视觉扩展版本，支持把图像与文本一起输入 decoder-only LLM。此后，图像理解逐渐成为主流 LLM 的默认能力之一。

#### 5.2.1 LLaVA (2023)

LLaVA (Liu et al., NeurIPS 2023)[5] 在 2023-04 release，用较少结构改动验证了 VLM 的基本路线：保留已有 vision encoder 和 LLM，只训练中间连接层与视觉指令数据，让 LLM 能接收图像信息并回答视觉问题。

- **模型结构**：冻结 CLIP ViT-L/14 作为 vision encoder，用 projection layer 把图像特征映射到 LLM 可接收的 token 表示，再接入 Vicuna；早期 projection 是单层 linear，后续版本改为 MLP
- **Stage 1：图文对齐**：用 CC3M 子集中的 558K 图文对训练 projection layer，让图像特征能对齐到 LLM 的语言表示空间
- **Stage 2：视觉指令微调**：用 GPT-4 生成的 158K 条视觉指令数据做 instruction tuning，让模型学会按用户问题基于图像内容作答

LLaVA 开源后成为 VLM 的常见实现模板；LLaVA-1.5 (2023-10) 把 projection 从单层 linear 改为 MLP，benchmark 结果进一步提升。

2024 年起，多模态逐渐成为 LLM 标准能力（Gemini / Claude 3 / GPT-4o / Qwen-VL / Qwen Omni / Kimi K2 / GLM-4.6 等）。VLM 因此成为后续 VLA（V-base = VLM）与 World Models（Cosmos-Reason 系列）的视觉理解组件来源。具体模型列表见 `09-sweeper-embodied-roadmap.md` §1。

### References

- [1] Radford et al., Learning Transferable Visual Models From Natural Language Supervision (CLIP), ICML 2021. arXiv:2103.00020
- [2] Jia et al., Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision (ALIGN), ICML 2021. arXiv:2102.05918
- [3] Minderer et al., Simple Open-Vocabulary Object Detection with Vision Transformers (OWL-ViT), ECCV 2022. arXiv:2205.06230
- [4] OpenAI, GPT-4V(ision) System Card, openai.com 2023-09.
- [5] Liu et al., Visual Instruction Tuning (LLaVA), NeurIPS 2023. arXiv:2304.08485

---

## 6. 第五阶段：World Models 起源 (2018-2023)

2018 年 Ha & Schmidhuber 提出的 V+M+C 架构，是 deep learning 语境下 world model 的早期代表；2023 年 Runway GEN-1 把 diffusion 用到视频生成产品中。两条线在 2024-2026 年汇合到 latent video 与可交互 world model（详见 §8）：前者影响后续 VLA 训练，后者进入 World Models 近期形态。

### 6.1 World Models 2018 (Ha & Schmidhuber)

Ha & Schmidhuber (NeurIPS 2018)[1] 提出：agent 可以先学习一个内部 world model，再在这个模型中模拟环境轨迹（dream rollout）来训练 policy，而不是每一步都与真实环境交互。该工作沿用 Schmidhuber 早期 (1990, 1991) RL with world model 的思路[2]，并在深度学习时代用 V+M+C 三模块实现。

#### 6.1.1 方法与实验

**V+M+C 三模块**[1]：

- **V (Vision)**：VAE encoder 把高维 observation 压缩成 32 维 latent `z`
- **M (Memory)**：MDN-RNN（mixture density net + RNN）在 latent space 预测下一时刻状态 `z_{t+1} | z_t, a_t`
- **C (Controller)**：简单 linear policy `a = W [z_t; h_t]` 根据当前 latent `z_t` 和 RNN hidden state `h_t` 输出动作；该 policy 用 evolution strategy (CMA-ES) 训练，不需要反向传播穿过 V / M

**关键实验**[1]：

- **CarRacing-v0** (OpenAI Gym)：agent 完全在 dream rollout 中训练 policy，再直接部署到真实 environment，取得 906 ± 21 分（vs 当时 best published 591），说明 dream-based policy training 可以在该任务上得到有效 reward
- **ViZDoom Take Cover**：采用类似设置，agent 在 dream 中训练后，在真实 environment 中可存活约 1100 step（baseline ~280 step）

#### 6.1.2 实践停滞 (2018-2024)

V+M+C 在玩具任务上验证后，2018-2024 间没有扩展到复杂真实场景，主要限制包括：

- VAE 表示能力受限，难以处理复杂场景和高分辨率视频
- MDN-RNN 做长 horizon 推演时容易 drift，即预测状态逐步偏离真实环境
- 训练数据规模与 LLM / Diffusion 时代不匹配

2024-2025 年的 Cosmos / Genie 系列把 world model 扩展到更大规模的视频和交互场景，详见 §8。

#### 6.1.3 路线分歧：JEPA vs LLM 主线

LeCun (Meta) 持续主张 AGI 核心是 self-supervised world model，并提出 JEPA (Joint Embedding Predictive Architecture, 2022)[3] 路线：模型在 embedding space 预测未来表示，而不是重建像素级图像。后续 V-JEPA (Bardes et al., 2024)[4]、V-JEPA-2 (Meta 2025-06)[5] 被用于 video understanding。

主流 LLM / VLA 阵营则采用预训练 + 推理 scaling + RL fine-tune 路线（GPT / Gemini / Claude / DeepSeek 均在此方向上演进）。两条路线对「世界模型是否应显式建模环境」给出不同答案，公开材料中尚未出现统一路线。

### 6.2 Runway GEN-1 与视频生成

GEN-1 (Esser et al., ICCV 2023)[6] 把 diffusion 用到视频生成产品中；Runway research blog 公开时间为 2023-02。后续 Sora / Veo 3 的生成质量更高，但 GEN-1 较早把 video diffusion 做成可用产品，并明确了「用源视频 + 文本 / 图像条件生成新视频」这一任务形式。

#### 6.2.1 GEN-1 (2023-02)

- **I/O**：输入 source video 与 reference image / text prompt，输出 stylized video；生成时尽量保留 depth / mask / structure，并替换 appearance
- **架构**：把 latent diffusion 扩展到 video，把 depth 和 structure 作为 conditioning 信号
- **应用**：面向商业视频后期和风格迁移，以 SaaS 形态提供给非技术用户

#### 6.2.2 后续主线 (2023-2024)

GEN-1 之后，视频生成沿三类方法展开（Diffusion / Autoregressive / Hybrid）：

- **Diffusion 范式**（当前主流）：
  - **Stable Video Diffusion** (Blattmann et al., 2023-11)[7]：开源 video diffusion，1.5B-3.5B 参数，生成 14-25 frames @ 576×1024
  - **Sora** (OpenAI 2024-02 technical report)[8]：把视频切成 spacetime patch，并用 Diffusion Transformer (DiT, Peebles & Xie, ICCV 2023)[9] 生成最长 60s 的视频；2024-12 公开 release 名为 Sora Turbo
  - **Veo / Veo 3** (Google DeepMind 2024-05 / 2024-12)[1]：闭源，高质量 + 长片段 + 物理一致性；集成进 Vertex AI
  - **Pika / Runway Gen-3** (2024)：商业向偏短片 / 创意
- **Autoregressive 范式**：**VideoPoet** (Google 2023-12) 像 LLM 生成文本 token 一样生成 video token；长 horizon 表现较强，但推理速度较慢
- **Hybrid 范式**：latent autoregressive + diffusion refinement，探索阶段

视频是 `frame × H × W` 的 3D tensor；三类方法在质量、速度、长 horizon 一致性上的取舍，仍需要在更大规模 video model 上继续观察。

#### 6.2.3 与 World Models 收敛 (2024-2025)

视频生成主线在 2024-2025 与 World Models 路线收敛：

- 视频生成模型可视为 implicit world model：它通过视频数据隐式学习环境随时间变化的规律
- DeepMind Genie 系列把 video generation 改造成 user-action-controllable，让用户动作影响后续画面，因此更接近 explicit world model（详见 §8）
- NVIDIA Cosmos Predict 直接把 video diffusion model 放入 "world model 工具链"（详见 §8）

2018 V+M+C 与 2023 GEN-1 分别连接到后续两条延伸线：

- VLA training 使用 world model dream 补充部分真机数据（§7.2.2 VLA + World Models 融合）
- World Models 近期形态在 2024-2026 年通过 latent video diffusion + interactive control 进入产品级 demo（§8）

### References

- [1] Ha & Schmidhuber, World Models, NeurIPS 2018. arXiv:1803.10122 (worldmodels.github.io)
- [2] Schmidhuber, On Learning to Think: Algorithmic Information Theory for Novel Combinations of RL Controllers and Recurrent Neural World Models, arXiv 2015. arXiv:1511.09249（含 1990 / 1991 RL+world-model 早期工作回顾）
- [3] LeCun, A Path Towards Autonomous Machine Intelligence (JEPA position paper), Open Review 2022.
- [4] Bardes et al., V-JEPA: Latent Video Prediction for Visual Representation Learning, arXiv 2024. arXiv:2404.08471
- [5] Meta AI, V-JEPA-2 release, ai.meta.com 2025-06.
- [6] Esser et al., Structure and Content-Guided Video Synthesis with Diffusion Models, ICCV 2023. openaccess.thecvf.com/content/ICCV2023/html/Esser_Structure_and_Content-Guided_Video_Synthesis_with_Diffusion_Models_ICCV_2023_paper.html（preprint：arXiv:2302.03011）
- [7] Blattmann et al., Stable Video Diffusion, arXiv 2023. arXiv:2311.15127
- [8] OpenAI, Video generation models as world simulators (Sora technical report), 2024-02.
- [9] Peebles & Xie, Scalable Diffusion Models with Transformers (DiT), ICCV 2023. arXiv:2212.09748
- [1] Google DeepMind, Veo 3 release, deepmind.google 2024-12.

---

## 7. 延伸 1：具身 VLA (2023-2026)

VLA (Vision-Language-Action) 在视觉和语言输入之外，把模型输出从文本 token 扩展为机器人动作。2023 年 Google DeepMind RT-2 把 VLM fine-tune 成可输出动作的 VLA；2024-2026 年，Physical Intelligence π 系列、NVIDIA GR00T、Gemini Robotics、OpenVLA / Octo 等路线继续推进跨机器人形态泛化、开源 baseline 和产品化；国内 AgiBot World / GO-1、Galaxea G0、RynnBrain / RynnVLA、LingBot-VLA、UnifoLM-VLA-0、Xiaomi-Robotics-0 等路线跟进。

### 7.1 VLA 进展（按地理）

VLA 进展按地理分两支：国际线以 Google / DeepMind、Physical Intelligence、NVIDIA 等产业主线和 OpenVLA、Octo 等开源 baseline 为代表；国内线在 2025-2026 年形成以数据集、开源权重和真机部署为中心的多条路线。两支主线在时间线上错开约 1.5 年，国内多数 model 直接复用国际或国产 VLM backbone（CLIP / Qwen-VL）。

#### 7.1.1 国际 VLA 初步地图

国际 VLA 可分为三类：RT-2 / Gemini Robotics 代表 Google / DeepMind 的闭源研究主线，π 系列 / GR00T 代表产业化 humanoid 主线，OpenVLA / Octo 代表开源学术和 baseline 主线。下表保留已有论文、开源资产、持续发布或产业工具链支撑的代表项。


| Model | 机构 | Release | Robot / 场景 | 数据 / 训练特点 | 公开状态 | 关键贡献 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RT-2 | Google DeepMind | 2023-07 | dual-arm RT robot | web-scale + RT-1 | 官方模型 / 权重未开放；有第三方复现 | 将 VLM fine-tune 为 VLA | [1] |
| Octo | UC Berkeley / Stanford 等 | 2024-05 | 多机器人 manipulation | Open X-Embodiment，约 800k robot episodes | 代码 MIT；checkpoint 公开 | 开源 generalist robot policy baseline | [2] |
| OpenVLA | Stanford / Berkeley 等 | 2024-06 / 2025 | 多机器人 manipulation | Open X-Embodiment，970k robot demonstrations | 代码 / 权重 MIT | 7B 开源 VLA，面向可微调部署 | [3] |
| π 系列 | Physical Intelligence | 2024-2026 | 7 个 embodiment + open-world 场景 | π₀ 使用 ~10k hrs robot data；π₀.5 / π₀.7 继续扩展泛化 | π₀ / π₀.5 代码与 checkpoint 公开（Apache-2.0）；π₀.7 公开论文 / 报告，未见公开 checkpoint | generalist policy + flow-matching action head | [4, 5, 9] |
| GR00T N1 | NVIDIA | 2025-03 | humanoid | open data + sim | 代码 / 权重公开；N1 / N1.5 权重偏非商用许可 | humanoid foundation model | [6] |
| Gemini Robotics 1.5 / ER 1.5 | Google DeepMind | 2025 | ALOHA / Bi-arm Franka / Apollo humanoid 等 | multi-embodiment robot data + Motion Transfer | ER 1.5 API；Robotics 1.5 面向 select partners | VLA + embodied reasoning 双模型组合 | [7] |
| GR00T N1.7 | NVIDIA | 2026-04-17 | humanoid | EgoScale 20,854 hrs egocentric | EA；代码 / 权重公开，商业许可需按 NVIDIA release 条款核对 | Action Cascade dual-system + dexterity scaling law | [10] |


**Google DeepMind RT-2 (2023-07)[1]**

RT-2 (Brohan et al., Google DeepMind 2023-07)[1] 把 VLM (PaLI-X 5B/55B / PaLM-E 12B/562B) 直接 fine-tune 成 VLA。它把机器人动作离散化为 LLM vocabulary 中的 token，使 LLM 在输出端直接生成 action token。

- **数据**：继承 PaLI-X / PaLM-E 的 web-scale pretraining，再加入 RT-1 收集的 13 个机器人、17 个月数据（~130k 任务 episode）
- **泛化**：对未见过的 object / instruction 做零样本执行，novel objects 上的 closed-loop success 相比 RT-1 baseline 提升 +60%
- **影响**：把 "VLM → fine-tune → VLA" 模式确立为后续标准（LLaVA / Qwen-VL / SigLIP 等都被尝试当 V-base）

**Physical Intelligence π 系列 (2024-2026)**

Physical Intelligence (PI) 是 Sergey Levine 等创立的具身公司，主线 π₀ → π₀.5 → π₀.7：

- **π₀** (2024-10)[4]：generalist robot policy，1 个 model 跨 7 个 embodiment（Franka / UR5e / Mobile Aloha / Trossen 等），~10k hrs 真机数据训练。VLM (PaliGemma) + flow matching action head。PI 公开 demo 在洗衣 / 折叠 / 打包多场景
- **π₀.5** (2025-04-22)[5]：open-world generalization。用 action knowledge transfer（从 web video + lab data 联合训练）在未训练过的 home / kitchen 场景 0-shot 表现
- **π₀.7** (2026-04-16)[9]：steerable robot foundation，PI 公开报告中描述为泛化能力进一步提升；具体 architecture 与训练规模待 paper release（写作时 verify）

PI 路线使用大规模真机数据和 flow-matching action head；`openpi` 已公开 π₀、π₀-FAST、π₀.5 的代码与 base checkpoints。π₀.7 已公开论文 / 报告，但 `openpi` 当前模型列表未包含 π₀.7 checkpoint。这与 RT-2 逐 token 自回归生成动作的方式不同。

**NVIDIA GR00T (2025-03 → 2026-04-17)**

NVIDIA GR00T 是 humanoid foundation model 的开放路线：

- **GR00T N1** (2025-03)[6]：首个开源 humanoid foundation model，dual-system（VLM 推理 + Diffusion Transformer 动作）
- **GR00T N1.5** (2025-06)：加入 FLARE（从人类视频学习）
- **GR00T N1.6** (2026-04-15)：VLM 升级到 NVIDIA Cosmos-Reason-2B
- **GR00T N1.7** (2026-04-17)[9]：3B 参数 "Action Cascade" = Cosmos-Reason2-2B (System 2) + 32-layer DiT (System 1)；使用 EgoScale 20,854 hrs 人类 egocentric video 数据集；NVIDIA 公开报告中提出 "robot dexterity scaling law"，即训练数据从 1k hrs 增至 20k hrs 后 dexterity 表现约 doubling

NVIDIA 路线强调开放 foundation model，并与 Cosmos / Isaac Sim 工具链绑定；合作厂商包括 Boston Dynamics / Agility / Figure 等 humanoid 公司。

**开源学术与 Google 后续线**

OpenVLA 与 Octo 是国际开源路线中常用的 baseline。OpenVLA 是 7B VLA，基于 Open X-Embodiment 的 970k robot demonstrations 训练；Octo 是 open-source generalist robot policy，基于约 800k robot episodes 训练，提供 27M / 93M 两种规模[2, 3]。Google DeepMind 在 RT-2 之后公开 Gemini Robotics 1.5 / Gemini Robotics-ER 1.5：前者是 multi-embodiment VLA，后者是 embodied reasoning VLM，用于空间理解、任务规划和进度估计[7]。

> **写作时 verify（截至 2026-05-06）**：
>
> - π₀.7 (2026-04-16) 是 PI 当前主线，是否取代 π₀ 作为 default baseline 待后续 paper / release 明确

#### 7.1.2 国内 VLA 初步地图

国内 VLA / 具身 foundation model 在 2025-2026 年形成多条公开路线。主表采用三类筛选标准：公开资产较完整、数据规模清楚、真机部署或 benchmark 信息可复核。

| Model | 公司 / 团队 | Release | Robot / 场景 | 数据 / 训练特点 | 公开状态 | 来源 |
| --- | --- | --- | --- | --- | --- | --- |
| AgiBot GO-1 | 智元 | 2025-03-10 | 多形态机器人 | AgiBot World：1M+ trajectories，217 个任务 | 代码 / 数据 / GO-1 权重公开；权重 CC BY-NC-SA 4.0 | [11] |
| Galaxea G0 | 星海图 Galaxea | 2025-09 | 移动双臂操作 | Galaxea Open-World Dataset：500 小时、50 个场景、150+ 任务 | 数据 / 模型公开；G0-VLA CC BY-NC-SA 4.0，G0Plus 为非商用社区许可 | [12] |
| RynnBrain / RynnVLA | 阿里达摩院 | 2026-02 / 2025-11 | embodied foundation / LIBERO + LeRobot | RynnBrain 含 2B / 8B / 30B-A3B MoE；RynnVLA-002 统一 VLA 与 world model | 代码 / checkpoint Apache-2.0 | [13, 14] |
| LingBot-VLA | 蚂蚁 / Robbyant | 2026-01 | 9 种双臂机器人配置 | 约 20,000 小时真实机器人数据；评估覆盖 3 个平台、100 个任务 | 代码 / 4B 权重 / benchmark data 公开，Apache-2.0 | [15] |
| UnifoLM-VLA-0 | 宇树 | 2026-01-29 | G1 humanoid | 基于 Qwen2.5-VL-7B，面向 12 类操作任务 | 代码 BSD-3-Clause；权重 CC BY-NC-SA 4.0 | [16] |
| Xiaomi-Robotics-0 | 小米机器人 | 2026-02 | 双臂实时控制 | 4.7B VLA；约 200M robot timesteps + 80M vision-language samples | 代码 / checkpoint Apache-2.0 | [17] |

**智元 AgiBot GO-1 (2025-03-10)[11]**

GO-1 是智元 (AgiBot) 的 ViLLA (Vision-Language-Latent-Action) 架构。它不直接生成动作 token，而是在 latent space 中做中间规划，再由 action expert 输出动作：

- **架构**：MoE + Latent Planner + Action Expert 三件套，在 latent space 做 planning，而不是直接生成 action token
- **训练数据**：AgiBot World 数据集，1M+ trajectories，217 个任务；公开材料将其定位为大规模 robotic learning platform
- **性能**：平均成功率 46% → 78%（vs GO-1 之前 baseline）

**宇树 UnifoLM-VLA-0 (2026-01-29)[16]**

UnifoLM-VLA-0 是宇树为 G1 humanoid 设计的 VLA：

- **Backbone**：基于阿里 Qwen2.5-VL-7B（国内 VLA 直接复用 Qwen 系列 VLM 的代表案例）
- **任务**：单一 policy 在 G1 上完成 12 类操作（开闭抽屉 / 插拔 / 抓放 / 工具使用）
- **公开状态**：UnifoLM-VLA-Base 已在 Hugging Face 公开；任务侧聚焦 G1 humanoid 操作

### 7.2 VLA 融合方向

VLA 与其他范式的融合主要沿两条方向展开：与 reasoning model 融合形成 dual-system 架构，与 World Models 融合形成 dream-based training。前者处理 long-horizon 任务规划，后者补充真机数据不足。

#### 7.2.1 VLA + 推理融合

VLA + reasoning 融合的核心模式是 dual-system：System 1 是高频动作 policy，负责实时控制；System 2 是慢速 reasoning LLM，负责拆解任务和规划步骤。两者协同处理 long-horizon / 多步任务。

**Reasoning model 极简介绍（背景，~200 字）**

Reasoning model 把 chain-of-thought 推理训练成模型能力，而不是只依赖外部 prompt-engineering。代表工作包括 OpenAI o1 (2024-09)[18] / o3 (2025-04) / DeepSeek R1 (2025-01)[19] / DeepSeek R2 (2026-04，32B dense 单 24GB GPU 可跑)。这些模型在 AIME / GPQA / Codeforces 等 multi-step 推理 benchmark 上明显超过同期 GPT-4 / GPT-5 base。本笔记偏 SLAM / 具身，只在此处作为 VLA + 推理融合背景简述。

**Dual-system 三个实例**

- **Figure Helix System 1+2** (2026-01)[8]：三级架构包括 System 0 实时平衡 (1 kHz)、System 1 视觉运动 (200 Hz, VLA policy)、System 2 高层推理 (LLM reasoning)；公开报告中明确借鉴 Kahneman 快 / 慢思考二系统；2026-01 的 4 分钟连续洗碗机自主 demo 由该架构实现
- **π₀.5 reasoning version** (2025-04-22)[5]：π₀.5 在 base policy 之外集成 reasoning 模块；LLM 先把当前 task 拆成 sub-task，再交由 base policy 执行
- **GR00T N1.7 Action Cascade** (NVIDIA 2026-04-17)[10]：System 2 使用 Cosmos-Reason2-2B（NVIDIA 自家 reasoning VLM，详见 §8.2 Cosmos），System 1 使用 32-layer Diffusion Transformer；"Action Cascade" 指 reasoning 输出的 plan 会级联到 DiT action 生成

**关键挑战**

- **System 1/2 latency 协调**：System 2 LLM 推理 ~秒级延迟，System 1 控制 ~10 ms；协调机制（event-triggered / 周期性 / 异步并行）直接影响系统响应
- **Long-horizon planning**：System 2 输出的 plan 在 System 1 执行过程中可能偏离，何时重 plan 是开放问题
- **Plan ↔ action 接口形式**：language token / latent vector / sub-task list，当前各家 design choice 不同，尚无统一接口

#### 7.2.2 VLA + World Models 融合

VLA + World Models 融合的核心模式是 World Model dreaming：先用 world model 生成大量模拟 rollout，再用这些 rollout 训练 VLA policy，以补充真机数据。这个思路延续 Ha & Schmidhuber 2018 的 dream-based policy training（详见 §6），但 world model 从 V+M+C 升级为 latent video diffusion 大模型。

**Cosmos / Genie / V-JEPA 在此节简提（详见 §8）**

- **NVIDIA Cosmos** (2025-01 起)：physical AI world model 工具链，包括 Predict（预测未来状态）、Transfer（sim-to-real 数据转换）、Reason（VLM reasoning）
- **DeepMind Genie 系列** (2024-02 / 2024-12 / 2025-08)：可交互 latent world model，可作为 VLA 的 training playground
- **V-JEPA-2** (Meta 2025-06)：JEPA 路线的 video predictive model

详细内容见 §8 World Models 近期形态；本节仅讨论与 VLA training 的融合机制。

**三个融合机制**

- **Sim-to-real via Cosmos Transfer**：NVIDIA Cosmos Transfer 把 sim renderer 输出经 diffusion 改造成更接近真机分布的图像，用于 VLA training data augmentation；GR00T N1.7 (2026-04-17) 公开报告中使用了这一 pipeline[10]
- **Dream-based RL training**：world model 先生成 rollout，VLA policy 再在这些 dream 环境中做 RL；银河通用 / 宇树 UnifoLM 等公开报告中提到 dreamer-like 训练方式
- **Reasoning + World Model 在同一 model 内**：NVIDIA GR00T N1.7 把 Cosmos-Reason2-2B 同时用于 System 2 reasoning 与 world model state prediction，使推理和 dream 共享同一模型组件

**当前局限与开放问题**

- **Sim-to-real gap 仍在**：world model dream 的物理一致性与真机 distribution 仍有 gap，完全 dream-only training 在长尾任务上未广泛验证
- **训练数据分布对齐**：world model 训练数据 vs VLA policy 训练数据 distribution 是否需要联合归一化，当前各家 design 不同
- **真机数据规模仍是瓶颈**：GR00T N1.7 dexterity scaling law 在 1k-20k hrs 真机数据上验证；world model dream 能否进一步扩大训练数据规模仍待验证（开放问题 1，§9）

### References

- [1] Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, arXiv 2023. arXiv:2307.15818
- [2] Octo Model Team, Octo: An Open-Source Generalist Robot Policy, arXiv 2024. arXiv:2405.12213; GitHub: github.com/octo-models/octo; Project: octo-models.github.io
- [3] Kim et al., OpenVLA: An Open-Source Vision-Language-Action Model, CoRL 2024 / PMLR 2025. arXiv:2406.09246; GitHub: github.com/openvla/openvla; Hugging Face: huggingface.co/openvla/openvla-7b
- [4] Black et al. (Physical Intelligence), π₀: A Vision-Language-Action Flow Model for General Robot Control, arXiv 2024. arXiv:2410.24164; GitHub: github.com/Physical-Intelligence/openpi (Apache-2.0)
- [5] Physical Intelligence, π₀.5 release, physicalintelligence.company/blog/pi05 2025-04-22; GitHub: github.com/Physical-Intelligence/openpi (Apache-2.0)
- [6] NVIDIA, GR00T N1 release, developer.nvidia.com 2025-03; GitHub: github.com/NVIDIA/Isaac-GR00T; Hugging Face: huggingface.co/nvidia/GR00T-N1-2B
- [7] Google DeepMind, Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer, technical report 2025; deepmind.google/models/gemini-robotics
- [8] Figure AI, Helix 02 release, figure.ai/news/helix 2026-01.
- [9] Physical Intelligence, π₀.7 release, physicalintelligence.company/blog/pi07 2026-04-16.
- [10] NVIDIA, GR00T N1.7: Action Cascade and EgoScale, huggingface.co/blog/nvidia/gr00t-n1-7 2026-04-17; GitHub: github.com/NVIDIA/Isaac-GR00T; Hugging Face: huggingface.co/collections/nvidia/gr00t-n17
- [11] AgiBot, GO-1 + AgiBot World 数据集 release, agibot.com 2025-03-10; GitHub: github.com/OpenDriveLab/Agibot-World; Hugging Face: huggingface.co/agibot-world/GO-1
- [12] Galaxea, Galaxea Open-World Dataset and G0 Dual-System VLA Model, arXiv 2025. arXiv:2509.00576; GitHub: github.com/OpenGalaxea/GalaxeaVLA; Hugging Face: huggingface.co/OpenGalaxea/G0-VLA
- [13] Alibaba DAMO Academy, RynnBrain: Open Embodied Foundation Models, arXiv 2026. arXiv:2602.14979; GitHub: github.com/alibaba-damo-academy/RynnBrain
- [14] Alibaba DAMO Academy, RynnVLA-002: A Unified Vision-Language-Action and World Model, GitHub: github.com/alibaba-damo-academy/RynnVLA-002; Hugging Face: hf.co/Alibaba-DAMO-Academy/RynnVLA-002
- [15] Robbyant, A Pragmatic VLA Foundation Model (LingBot-VLA), arXiv 2026. arXiv:2601.18692; GitHub: github.com/Robbyant/lingbot-vla; Hugging Face: hf.co/robbyant/lingbot-vla-4b
- [16] Unitree, UnifoLM-VLA-0 release, unitree.com 2026-01-29; GitHub: github.com/unitreerobotics/unifolm-vla; Hugging Face: huggingface.co/unitreerobotics/UnifoLM-VLA-Base
- [17] Xiaomi Robotics, Xiaomi-Robotics-0: An Open-Sourced Vision-Language-Action Model with Real-Time Execution, arXiv 2026. arXiv:2602.12684; GitHub: github.com/XiaomiRobotics/Xiaomi-Robotics-0; Hugging Face: huggingface.co/XiaomiRobotics/Xiaomi-Robotics-0-Pretrain
- [18] OpenAI, o1 system card, openai.com/index/learning-to-reason-with-llms 2024-09-12.
- [19] DeepSeek, DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, arXiv 2025. arXiv:2501.12948

---

## 8. 延伸 2：World Models 近期形态 (2024-2026)

2024-2026 间，World Models 从 V+M+C 玩具任务走向大规模视频和交互场景。DeepMind Genie 系列把 world model 做成可交互环境；NVIDIA Cosmos 则把 world model 做成 physical AI 工具链。

### 8.1 可交互世界生成（Genie 3）

DeepMind Genie 系列把 video generation 改造成 user-action-controllable：用户动作会影响后续画面，因此它从固定视频生成转向显式可交互 world model。

#### 8.1.1 Genie 系列时间线

主线 Genie 1 → Genie 2 → Genie 3 → Project Genie：

- **Genie 1** (DeepMind, ICML 2024)[1]：第一代 foundation world model，256×256，11B 参数，从 200k+ 小时 unlabeled internet video 学习；可生成 2D platform-style world，用户用 action token 控制 agent
- **Genie 2** (DeepMind 2024-12)[2]：扩展到 3D 环境，支持 first-person / third-person 视角，保持约 1 分钟 horizon 一致性
- **Genie 3** (DeepMind 2025-08-05)[3]：720p / 24 fps real-time interactive，photorealistic；官方表述为在 720p 下可保持「几分钟」级一致性（retaining consistency for a few minutes）[3]；用户可以从一张图或一段文字出发，实时操控生成的 3D 环境
- **Project Genie** (DeepMind 2026-01-29)[4]：Genie 3 商业化产品，集成 Google AI Ultra（US 18+ 用户）

#### 8.1.2 应用与对比

**应用线**：

- **Waymo World Model** (Waymo 2026-02)[5]：用于自动驾驶 closed-loop 仿真，在内部 world model 中 sample edge case，用于训练和评估 L4 policy
- **VLA training playground**（多家 humanoid VLA）：用 Genie 系列环境做 RL pretrain / sim2real 验证（详见 §7.2.2 VLA + World Models 融合）

**与 Sora-style 视频生成的区别**：视频生成 model 可视为 implicit world model，但 Sora / Veo 输出的是固定 video clip，用户不能在生成过程中改变动作。Genie 系列的区别在于：

- **Action-conditioned**：每帧生成依赖用户当前 action token，系统在线 sample，而不是一次性 batch 生成完整视频
- **State maintenance**：跨 frame 维护 world state，例如物体位置、物理一致性和相机轨迹
- **Interactive latency**：目标是 real-time (~24 fps) 交互生成，而不是 offline batch generation

### 8.2 机器人仿真训练（NVIDIA Cosmos）

NVIDIA Cosmos (2025-01 起) 是 physical AI 的 world model 工具链，与 NVIDIA Isaac Sim / GR00T humanoid foundation 配套，形成仿真、数据生成、reasoning 与机器人 policy 的完整 stack。

#### 8.2.1 Cosmos 体系（3 子族 + 工具链定位）

**3 个子族 (2025-2026)[6, 7]**：

- **Cosmos Predict (Predict 2.5, 2026-04)**：flow-based world prediction，统一支持 text-to-world / image-to-world / video-to-world；2.5 系列相比 1.x 改善长 horizon 物理一致性
- **Cosmos Transfer (Transfer 2.5, 2026-04)**：multi-controlnet 可控生成，支持 depth map / segmentation / pose / sketch 等输入条件；用于 sim-to-real data augmentation，把 sim renderer 输出经 diffusion 改造成更接近真实分布的图像
- **Cosmos Reason (Reason 2, 2026-04)**：增强 spatial-temporal 理解的 VLM reasoning model；NVIDIA GR00T N1.6 / N1.7 直接用 Reason2-2B 作为 System 2 backbone（详见 §7.2.1 VLA + 推理融合）

**工具链定位**：Cosmos 不是单点 model，而是 NVIDIA "physical AI stack" 的 foundation 层：

- **Foundation**：Cosmos foundation models，包括 Predict / Transfer / Reason
- **Sim**：NVIDIA Isaac Sim / Isaac Lab，提供仿真引擎
- **Embodiment**：GR00T N1.x humanoid foundation，提供机器人 policy
- **Hardware**：Jetson Thor / DGX Spark，提供具身 inference 硬件

#### 8.2.2 应用与对比

**公开 early adopter**[7]：NVIDIA 公开报告中，Cosmos 早期 adopter 覆盖 humanoid 与自动驾驶两个方向：

- **Humanoid**：1X / Agility Robotics / Figure AI / Boston Dynamics，Cosmos Transfer 用于 sim-to-real
- **自动驾驶**：Uber / Waabi（Cosmos Predict 用作 closed-loop 仿真）

**与 Genie 路线的差异**：Cosmos 与 Genie 共享 latent video world model 核心思路，但 design choice 不同：

- **Target user**：Cosmos 面向机器人 / 自动驾驶行业开发者；Genie 面向 consumer / game / general public
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

这里保留两个与具身 / 重建相关的开放问题，只描述现状、缺口和待观察项，不下结论。

### 9.1 VLA 在 home / 长尾场景的泛化

**现状**：VLA 在工厂、结构化 pick-place 和 lab demo 任务上已有较多成功案例。GR00T N1.7 (2026-04-17)[1] 在 EgoScale 20,854 hrs 数据上报告 robot dexterity scaling law：训练数据从 1k hrs 增至 20k hrs 后，dexterity 表现约 doubling。该结果说明数据规模扩大与 dexterity 提升有关。

**缺口**：home / 长尾场景仍缺少广泛公开的 benchmark 和 success rate：

- Physical Intelligence π₀.5 (2025-04-22)[2] 在 open-world generalization 上是早期信号
- π₀.7 (2026-04-16) "step-change in generalization" 描述待 paper 公开（写作时 verify）
- Figure Helix 02 (2026-01) 4 分钟洗碗机 demo 是单点案例，不能替代统计意义上的成功率

**待观察**：

- 是否有标准 home benchmark（类似 ImageNet / COCO 在 CV 时代的角色）
- scaling law 在 home / 长尾 task 上是否同样成立，还是会饱和
- World Model dream 替代真机数据是否能 scale 到 home 场景多样性（与开放问题 2 部分耦合）

### 9.2 World Models 与 metric 重建是否合流

**现状**：当前两条线都在使用 Transformer / feed-forward 大模型，但表示方式仍分化：

- **生成路线 (Genie 3 / Cosmos)**：使用 latent video 表示，强调隐式的 pixel-level 一致性，不显式输出 metric 几何
- **重建路线 (3DGS / DUSt3R / VGGT)**：使用 explicit geometry 表示，例如 point / Gaussian / camera matrix，强调 metric 精度（PSNR / pose error）

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