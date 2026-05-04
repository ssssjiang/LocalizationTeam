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

## 第二阶段：Transformer 范式的崛起

### 业界公认的意义

- Transformer 的关键贡献不是 attention 本身，而是**第一次让 AI 模型变成可堆规模**
- LLM 时代发现了 AI 的"摩尔定律"——scaling law
- AI 由此从「设计聪明的模型」转向「准备数据 / 用好算力 / 训得更稳」的工程化时代

### Transformer 本体（2017, "Attention Is All You Need"）

#### 做了什么

- 完全抛弃 RNN 循环 + CNN 卷积，只用 self-attention + FFN

#### 解决了两个硬伤

- 所有位置可并行（GPU 满载）
- 任意两位置直接交互，无距离衰减

#### 真正的贡献

- attention 机制 2014 Bahdanau 就有了
- Transformer 的贡献是**让"更大 = 更强"变成可工程化、可预测的事实**

### Scaling Law（2020, OpenAI）

#### 核心发现

- 性能 vs 参数 / 数据 / 算力 = 干净的幂律
- 含义：给定算力可以预测模型性能

#### GPT-3（2020, 175B）

- 首次证明：通用模型靠 prompt 就能做翻译/写代码/问答/写诗
- GPT-2 还做不到的事，GPT-3 突然做到了

#### 涌现能力（仍未完全理解）

- 某些任务在小模型完全做不了，到一定规模突然就会
- 多步推理 / code / in-context learning
- 学界对涌现的成因和真实性仍有争议

### ChatGPT（2022.11）

- 技术上 = GPT-3.5 + RLHF
- 业界共识：真正贡献在产品形态（对话界面 + 对齐到人类偏好），不在底层技术
- 5 天 100 万用户、2 个月 1 亿用户，AI 第一次出圈

### 2026 年的拐点

#### 架构开始分化

- Mamba（2023+）状态空间模型，线性复杂度 O(n) + 常数显存
- Mamba-3（2026.03）：1.5B 上准确率超 Mamba-2 ~2pt，state size 减半
- 业界共识：Mamba 不取代 Transformer，而是补足；越来越多 hybrid 架构

#### Scaling 范式开始换腿

- 业界观察到从「模型规模 scaling」转向「推理 compute scaling」
- 详见延伸 1

#### Frontier 不再被三大厂垄断

- GPT-5.4（2026.03）：1M 上下文 + 原生电脑使用（OSWorld 75%）
- Gemini 3.1 Pro（2026.02.19）：1M 输入 / 64K 输出，ARC-AGI-2 拿到 77.1%
- Claude Opus 4.7（2026.04.16）：长程编码 verification 机制
- 共同特征：这一代的提升主要靠「思考机制变深」，而非「模型变大」

### 国内 LLM 副线（2025-2026 三种差异化打法）

#### Qwen 系列（阿里）

- 路线：scaling + 全家族开源
- Qwen3（2025.04 起）开源 0.6B 到 235B MoE + 混合推理
- Qwen3-Max（2025.10）1T 参数 / SWE-Bench 69.6% / Tau2-Bench 74.8%
- Qwen3.5 Omni（2026.03）原生多模态 + 256K

#### GLM 系列（智谱）

- 路线：小尺寸高性能 + 国产芯片适配
- GLM-4.6（2025.09）355B MoE / 32B 激活，200K 上下文
- LMArena 排第 4（国内并列第一），代码能力对标 Claude Sonnet 4

#### Kimi 系列（Moonshot）

- 路线：押 agent
- Kimi K2（2025.07）1T MoE 开源（Apache 2.0）
- Kimi K2.5（2026.01.27）self-directed agent swarm：100 sub-agents 并行 + 1500 工具调用同时执行；速度比单 agent 快 4.5×
- 公开报告中 agent benchmark 上超过 GPT-5.2 / Claude 4.5 Opus / Gemini 3 Pro

#### 业界对国内 LLM 的现状描述

- 三家选了三种不同的差异化路线
- 在多个维度（开源生态 / 部署成本 / agent 编排）已经站到 frontier
- 整体处于「在某些维度领先」而非单纯「追赶」的阶段

---

## 第三阶段：生成式 AI 的爆发

### 业界公认的意义

- 关键词：**打通**
- Diffusion 打通：AI 不只是判别器，也能是创造者
- VLM 打通：视觉和语言不再是两条独立研究线
- 合起来 → AI 开始具备类人的创造和理解能力，真正进入大众视野

### Diffusion：让生成式 AI 第一次"真正可用"

#### Diffusion 之前的困境

- GAN（2014）训练不稳定、模式崩塌
- VAE 生成模糊
- Autoregressive 太慢

#### 反直觉的核心思路

- 不学「怎么生成图像」，学「怎么去噪声」
- Forward：清晰图像逐步加噪 → 纯噪声
- Reverse：训练模型从纯噪声逐步还原回清晰图像
- 把「从无到有」拆成「每步去一点点噪声」，训练稳定可 scale

#### 生态爆发

- DDPM 论文（2020）→ 两年内 DALL-E 2（2022.04）+ Stable Diffusion（2022.08，**开源**）+ Midjourney
- Stable Diffusion 开源被业界视为关键节点：消费级 GPU 跑 image generation，开源社区一夜起飞

### VLM：CLIP 是起点

#### CLIP（2021, OpenAI）

- 4 亿对（图像，文本描述）做对比学习
- 把图像和文本对齐到同一个语义空间
- 含义：图与对应文本描述向量接近，跨类别向量距离远

#### 三大下游影响

- 零样本图像分类（不需要专门训练分类器）
- DALL-E 2 / Stable Diffusion 的 text encoder 都是 CLIP
- GPT-4V / Qwen-VL / LLaVA 本质上都是 CLIP 范式上叠加 LLM

#### GPT-4V（2023.09）

- AI 第一次能"看懂"用户发的图并回答问题

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