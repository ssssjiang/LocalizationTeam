# AI 演进笔记 （2012-2026） 

## 1. 整体趋势

2012-2026 间 AI 演进经历 5 个 foundation 阶段（判别式 → Transformer → Diffusion 与视觉生成 → VLM 与多模态理解 → World Models 起源）与 2 个延伸方向（具身 VLA / World Models 近期形态）。时间线：

- **2012-2015 判别式 AI**：AlexNet （NeurIPS 2012） / VGG / GoogLeNet / ResNet （CVPR 2016） — CNN 端到端特征学习；
- **2017 Transformer**: Vaswani et al. — self-attention 替代 RNN，LLM 工业化基础；
- **2020-2022 LLM scaling**: GPT-3 (NeurIPS 2020) / Chinchilla (NeurIPS 2022) / ChatGPT (2022-11); 
- **2020-2024 Diffusion 与视觉生成**：DDPM （NeurIPS 2020） → Stable Diffusion （2022-08） → Sora （2024-02）；
- **2020-2024 VLM 与多模态理解**：CLIP （ICML 2021） → GPT-4V （2023-09） → LLaVA （NeurIPS 2023）；
- **2018 World Models 起源**：Ha & Schmidhuber （NeurIPS 2018） V+M+C；
- **2023-2026 具身 VLA**：RT-2 （2023-07） → π₀ （2024-10） → π₀。7 (2026-04-16) / Helix 02 (2026-01) / GR00T N1.7 (2026-04-17); 
- **2024-2026 World Models 近期形态**：Genie 3 （2025-08） / Cosmos （2025-01 起）；

## 2. 第一阶段：判别式 AI （2012-2015）

2012 年前后的判别任务仍以分类、检测、序列输出为目标；变化发生在中间表示。图像识别等任务从「人工特征 + classifier」转向端到端训练，特征由神经网络从数据中学习。CNN、RNN、ResNet 分别处理这条路线上的 3 个问题。

- **CNN**：raw RGB pixel 直接进入网络，替代 SIFT / HOG 等人工特征；
- **RNN / LSTM**：同一端到端训练方式扩展到翻译、语音等序列任务；
- **ResNet**：在网络继续加深时，通过残差连接缓解优化退化。

后续 Transformer、Diffusion、VLM、VLA 的任务形式已经超出判别任务，但仍复用这一阶段留下的视觉 backbone，以及残差连接、归一化、GPU 端到端训练等深网络工程组件。

### 2.1 CNN：视觉端到端特征学习

2012 年前后的图像识别系统通常分两段：人设计图像特征，模型基于这些特征做分类。AlexNet 把两段合入同一个网络：输入 raw RGB pixel，卷积层学习边缘、纹理、物体部件，softmax 输出类别。

AlexNet 在 ImageNet ILSVRC-2012 上 top-5 错误率为 15.3%，第二名为 26.2%[1]。该结果对应的系统分工变化是：特征由网络在监督信号下学习，而非主要依赖人工规则。

![image.png](images/SqYabeUpeoyALIxdZ15cG7L0njg.png)

AlexNet 之后，VGG 和 GoogLeNet 继续沿端到端 CNN 路线处理两个工程问题：

- **VGG**：全部用 3×3 卷积堆深网络，验证重复 block 也能形成强视觉表示[2]；
- **GoogLeNet / Inception**：在同一层里并联不同尺度的卷积分支，用更少参数处理多尺度视觉模式[3]。

![image.png](images/V8tlbVclFokr7LxIz08caPj9nze.png)

CNN 解决的是「一张图如何变成可分类的视觉特征」。当输入变成句子或语音时，问题多了一个时间轴：模型不能只看一张固定大小的图，还要按顺序读入一个变长序列。

### 2.2 RNN：序列建模

RNN 在第 `t` 个 token 处同时使用当前输入 `x_t` 和前一时刻的 hidden state `h_{t-1}`。hidden state 在时间步之间递归传递，使模型能够处理句子、音频片段和时间序列。

普通 RNN 的问题是长序列训练不稳定。LSTM 在 1997 年提出 cell state 和 input / forget / output 三个门控，用显式的记忆通路缓解梯度衰减[4]。到 2014 年，seq2seq 把 RNN / LSTM 组织成 encoder-decoder：encoder 读入源句子，decoder 生成目标句子[5]。

这条路线把端到端学习从图像扩展到翻译和语音。Deep Speech 在 2014 年使用深度 RNN 处理语音识别[7]；Bahdanau attention 让 decoder 在生成每个词时关注源句子中的相关位置，降低对单一 encoder 向量的依赖[6]。

RNN 的结构瓶颈来自时间步依赖：第 `t` 步依赖第 `t-1` 步，训练和推理难以并行；长距离信息需要逐步传递，路径变长后更难保留。2017 年 Transformer 用 self-attention 直接连接任意两个 token，替换了 RNN 的递归结构[8]。

### 2.3 ResNet 与残差连接

CNN 和 RNN 说明表示可以由网络学习。继续加深网络可以提升表示能力，但普通 CNN 从 20 层加到 56 层时，训练误差和测试误差同时升高[9]。

![image.png](images/ROKrbrqxRoYGfdxCq49cGo3nnMc.png)

该现象不能用过拟合解释。过拟合通常表现为训练误差下降、测试误差升高；这里训练误差也升高，问题来自优化退化。更深的普通网络理论上可以通过额外层学习恒等映射来复现浅层网络，实际 SGD 很难自动得到该解[9]。

ResNet 把每个 block 的目标从直接学习 `y = F(x)`，改成学习残差 `y = F(x) + x`[9]。

![image.png](images/Oe8Ibdq43oSYxExfdmHcfFT4nuU.png)

当 `F(x)` 接近 0 时，残差 block 退化为恒等映射。反向传播时，梯度可以沿 `+x` 的恒等分支传回浅层。残差连接给优化器提供了更直接的梯度路径，因此 152 层 ResNet 可以在 ImageNet 上训练，并在 ILSVRC 2015 分类任务上取得 3.57% top-5 错误率[9]。

残差连接后来进入多类深网络架构。Transformer 每个 attention / FFN 子层外都有 `x + Sublayer(x)`[8]；Diffusion U-Net 也使用跨层 skip connection。CNN 的卷积和 RNN 的循环绑定具体输入结构；残差连接的作用更通用，核心是给深层网络的信息和梯度提供更短路径。

CNN、RNN、ResNet 共同构成这一阶段的主线：模型先从图像和序列中学习表示，再通过残差连接支持更深网络训练。第二阶段的 Transformer 与这条主线有两层关系：用 self-attention 替换 RNN 的递归结构，改善序列建模的并行性和长距离依赖；沿用 ResNet 的残差连接，使更深的序列模型可以稳定训练。

### References

- [1] Krizhevsky et al., ImageNet Classification with Deep Convolutional Neural Networks (AlexNet), NeurIPS 2012.
- [2] Simonyan & Zisserman, Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG), ICLR 2015. arXiv:1409.1556
- [3] Szegedy et al., Going Deeper with Convolutions (GoogLeNet / Inception), CVPR 2015. arXiv:1409.4842
- [4] Hochreiter & Schmidhuber, Long Short-Term Memory, Neural Computation 1997.
- [5] Sutskever et al., Sequence to Sequence Learning with Neural Networks, NeurIPS 2014. arXiv:1409.3215
- [6] Bahdanau et al., Neural Machine Translation by Jointly Learning to Align and Translate, ICLR 2015. arXiv:1409.0473
- [7] Hannun et al., Deep Speech: Scaling up end-to-end speech recognition, arXiv 2014. arXiv:1412.5567
- [8] Vaswani et al., Attention Is All You Need, NeurIPS 2017. arXiv:1706.03762
- [9] He et al., Deep Residual Learning for Image Recognition, CVPR 2016. arXiv:1512.03385

---

## 3. 第二阶段：Transformer 范式 （2017-2026）

Transformer 的核心问题是序列建模：给定一段文本，模型需要为每个 token 建立与其它 token 的依赖关系。RNN 通过 hidden state 按顺序传递上下文；Transformer 用 self-attention 一次性计算 token 间相关性，使训练并行性和长距离依赖建模同时改善[1]。

后续 Scaling Law、GPT-3、ChatGPT 与 RLHF，分别沿着模型规模、少样本泛化和人类偏好对齐继续扩展这条路线。

### 3.1 [Transformer](https://jalammar.github.io/illustrated-transformer/)：注意力机制

Transformer (Vaswani et al.，NeurIPS 2017）[1] 用 self-attention + position-wise FFN 取代 RNN 循环结构与 CNN 卷积。Self-attention 将每个 token 映射为三组向量：

- Query：当前 token 用于匹配其它 token 的查询向量；
- Key：其它 token 用于被匹配的键向量；
- Value：匹配后参与加权汇总的值向量。

Scaled dot-product attention 用 Query 和 Key 的相似度计算权重，再对 Value 做加权汇总。Multi-head attention 并行计算多组 Q/K/V，使模型在不同表示子空间中建模 token 关系[1]。

在 WMT'14 EN-DE 翻译任务上 BLEU 28.4，超过当时 RNN encoder-decoder baseline 25.16[1]。

![image.png](images/Y8iebndifopGarxZDZEcfOG9nAb.png)

#### 3.1.1 关键设计

- **Attention 机制**：Scaled dot-product $\operatorname{Attention}(Q, K, V)=\operatorname{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$ [1]，$\sqrt{d_k}$ 缩放用于避免 dot product 过大后 softmax 过早饱和。
- **Position encoding**：Self-attention 不包含词序信息；Transformer 给每个 token 加入 positional encoding，让表示同时包含词义和位置。原始 Transformer 使用 sin/cos 固定位置编码，后续 LLM 多使用 RoPE 等位置编码方案。
- **架构组合**：原始 Transformer 采用 encoder-decoder 结构；每个 attention 或 FFN 子层外加残差连接和 LayerNorm，即 `LayerNorm(x + Sublayer(x))`，其中残差连接沿用了 ResNet 的 `F(x) + x` 思路[2]。

#### 3.1.2 工程后果

- **并行训练**：RNN 的状态递推存在时间步依赖；self-attention 将 token 两两关系表示为矩阵，训练时可并行计算。
- **长距离依赖**：RNN 中远距离信息需要经过多个 hidden state 传递；self-attention 中任意两个 token 可在同一层建立依赖。

#### 3.1.3 三派与影响

Transformer 后来形成三种常见用法，差异主要在输入读取和输出生成方式：

- **encoder-only** (BERT, Devlin et al.，NAACL 2019）[3]：整句一起读，用 masked language modeling 训练模型根据上下文补全被遮住的词。它输出的是上下文语义表示，主要用于文本分类、实体识别、句子匹配等语言理解任务[3]。
- **decoder-only** (GPT, Radford et al.，2018）[4]：只看当前位置左侧上下文，用 causal language modeling 训练模型预测下一个 token。生成时每次输出一个 token，再把该 token 接回上下文继续生成；这一自回归形式后来成为 LLM 的主流结构[4]。
- **encoder-decoder** (T5, Raffel et al.，JMLR 2020）[5]：encoder 先读输入文本，decoder 再生成输出文本。T5 把翻译、摘要、分类、问答等任务都改写成「文本输入 → 文本输出」格式，因此不同 NLP 任务可以用同一套模型结构和训练形式处理[5]。

Attention 机制本身在 Bahdanau et al.（ICLR 2015）[6] 中已用于 NMT（Neural Machine Translation，神经机器翻译）：生成目标语言每个词时，模型会动态关注源语言句子中最相关的位置。Transformer 的变化，是把 attention 从辅助模块变成整套网络的主干。

### 3.2 Scaling Law 与 GPT-3

Transformer 给出了可并行训练的结构，下一步问题转向规模扩展：参数、数据、算力增加后，模型 loss 如何变化。Kaplan et al.（OpenAI 2020）[7] 用实验拟合出 LLM cross-entropy loss 与参数量 N、数据量 D、计算量 C 的幂律关系：

![image.png](images/ZRrtbPYJko2s8zx24wZcGXKlnBe.png)

这条曲线把大模型训练转向可估算的工程扩展问题：给定 compute budget 后，可以估计参数量、训练 token 数和最终 loss 之间的关系。工程重点也从频繁更换新架构，转向 scale 现有架构、配数据和调训练流程。

#### 3.2.1 GPT-3 (2020)

GPT-3 (Brown et al.，NeurIPS 2020）[8] 175B 参数，300B token 训练，展示了 in-context learning：

- 不更新模型参数，只在 prompt 中给少量任务示例，模型就能按示例格式完成翻译、问答、算术和代码生成等任务；
- 多项任务的性能曲线随 scale 平滑提升，与 Kaplan 2020 的预测方向一致[7][8]。

#### 3.2.2 Chinchilla 修正 （2022）

- Kaplan 2020 的 scaling law 让早期 LLM 更偏向增加参数量；
- Hoffmann et al. 2022 通过 400+ 个实验修正了这一结论：在固定算力下，参数量和训练 token 数应同步增加，约为 1B 参数对应 20B token。
- Chinchilla 只有 70B 参数，但用 1.4T token 训练，性能超过 280B 参数、300B token 的 Gopher，说明 GPT-3 / Gopher 这类模型参数很大，但训练数据不足。

#### 3.2.3 Emergent abilities 与争议

- Wei et al.（TMLR 2022）[10] 认为，部分 BIG-Bench 任务在小模型上接近随机，但模型规模超过某个阈值后表现突然上升，这类现象被称为 emergent abilities。
- Schaeffer et al.（NeurIPS 2023）[11] 反驳说，很多“突然上升”来自 exact-match 这类离散指标：答案只要不完全正确就记 0 分，因此平滑进步会被显示成跳变。换成连续评价指标后，部分任务的性能曲线变得平滑。

### 3.3 ChatGPT 与 RLHF

GPT-3 说明大语言模型可以通过 prompt 适配任务；面向对话产品时，还需要约束输出：理解指令、按人类偏好组织答案，并降低有害回复概率。ChatGPT（OpenAI 2022-11-30）[12] 的技术基底是 GPT-3.5 加 InstructGPT-style RLHF（Ouyang et al.，NeurIPS 2022）[13]。

![image.png](images/Fi0fbsKkXo8ElpxMuCTcSqEenxA.png)

#### 3.3.1 RLHF 三阶段

- **SFT（supervised fine-tuning）**：用人类示范回复做 supervised learning，让 base model 学会对话格式；
- **Reward model**：让人类对多个候选回复排序，训练一个 reward model 近似人类偏好；
- **PPO RL**：用 reward model 作为 reward signal，再用 PPO 优化 policy LM。

InstructGPT 把目标概括为三 H：helpful、harmless、honest[13]。

RLHF 思想源自 Christiano et al.（NIPS 2017）[14] 的 RL from human preferences。

#### 3.3.2 产品意义

- ChatGPT 5 天 100 万用户、2 个月 1 亿用户。技术路线接续 InstructGPT；产品形态上，对话 UI 和 alignment to human preference 让 LLM 进入普通用户的日常使用场景。
- 后续 Anthropic Claude 的 Constitutional AI 继续围绕人类偏好与安全约束改进模型输出[15]。

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

## 4. 第三阶段：Diffusion 与视觉生成（2020-2024）

2020-2024 间，Diffusion 把生成问题改写为逐步去噪：训练阶段学习噪声预测器，推理阶段从随机噪声或加噪后的输入出发，反复调用同一个网络更新采样状态[1]。DDIM、Classifier-Free Guidance (CFG) 与 Latent Diffusion 分别改动采样路径、条件输入和计算空间，之后被 DALL-E 2、Imagen、Stable Diffusion、Stable Video Diffusion 与 Sora 等系统沿用[2][3][4][5][6][7][8][9]。

### 4.1 基本机制

Diffusion 的基本机制由三段构成：前置生成模型给出背景，DDPM 给出训练去噪器的接口，采样阶段反复调用同一个去噪器生成结果。

#### 4.1.1 生成模型前史

2020 年 DDPM 出现前，深度生成模型已沿 GAN、VAE、Normalizing Flow 三条路线发展。三类方法都从随机变量生成样本，但训练稳定性、可逆性约束和样本质量之间的取舍不同。

| 路线 | 生成方式 | 训练约束 | 来源 |
|---|---|---|---|
| GAN | 生成器与判别器做对抗训练 | 目标函数是 min-max optimization | [10] |
| VAE | 编码器学习 latent distribution，解码器从 latent 生成样本 | 用 evidence lower bound 替代直接 log-likelihood | [11] |
| Normalizing Flow | 学习可逆变换，把简单分布映射到数据分布 | 变换需可逆，并计算 Jacobian determinant | [12] |

DDPM 把从噪声到图像的映射拆成多步去噪；后续工程改动大多围绕采样步数、条件输入和计算空间展开。

#### 4.1.2 DDPM：训练去噪器

DDPM (Denoising Diffusion Probabilistic Models) 把真实图像 `x_0` 逐步加噪到 `x_T`，再训练网络预测每一步加进去的噪声[1]。模型在给定噪声强度 `t` 时，估计 `x_t` 中的噪声分量。

![image.png](images/RDu8bf1ZGodRjWxGKolckxGjnwg.png)

DDPM 的训练接口可以压缩成 5 行：

```python
t = randint(1, T)
eps = randn_like(x_0)
x_t = sqrt(alpha_bar[t]) * x_0 + sqrt(1 - alpha_bar[t]) * eps
eps_pred = model(x_t, t)
loss = mse(eps, eps_pred)
```

对应的简化损失为：

$$L = \mathbb{E}_{t, x_0, \epsilon}[||\epsilon - \epsilon_\theta(x_t, t)||^2]$$

其中 `ε` 是实际加入的高斯噪声，`ε_θ(x_t, t)` 是模型预测的噪声。这个目标把生成问题变成监督回归：输入带噪图和时间步，输出与图像同形状的噪声张量[1]。

#### 4.1.3 推理：反复使用去噪器

推理阶段没有真实图像 `x_0`。系统先采样 `x_T ~ N(0, I)`，再按 `T, T-1, ..., 1` 的顺序反复调用同一个去噪网络，把 `x_t` 更新为噪声更低的 `x_{t-1}`[1]。

| 阶段 | 输入 | 网络输出 | 是否需要真实图 |
|---|---|---|---|
| 训练 | `x_0`、随机时间步 `t`、随机噪声 `ε` | `ε_θ(x_t, t)` | 需要 |
| 推理 | `x_T ~ N(0, I)`、时间步序列、可选条件 `c` | `ε_θ(x_t, t, c)` | 不需要 |

无条件采样循环：

```python
x = randn(shape)
for t in reversed(range(1, T + 1)):
    eps_pred = model(x, t)
    x = sampler_step(x, t, eps_pred)
return x
```

文生图只是在每一步多传入文本条件。文本编码器先把 prompt 变成向量 `c`，去噪网络再根据 `x_t`、`t` 和 `c` 预测噪声；随机起点仍是 `x_T ~ N(0, I)`[3][4]。

```python
c = text_encoder(prompt)
x = randn(shape)
for t in reversed(range(1, T + 1)):
    eps_pred = model(x, t, c)
    x = sampler_step(x, t, eps_pred)
return x
```

推理阶段的工作流可以按采样起点和条件输入区分：

| 使用方式 | 采样起点 | 条件输入 | 输出关系 | 来源 |
|---|---|---|---|---|
| 无条件生成 | `x_T ~ N(0, I)` | 无 | 从训练分布中采样新图像 | [1] |
| 文生图 | `x_T ~ N(0, I)` | 文本 embedding | 文本条件影响每一步噪声预测 | [3][4][5][6] |
| img2img | 输入图加噪到中间时间步 | 文本或图像条件 | 保留部分输入图结构，再沿条件去噪 | [14] |
| inpainting | 已知区域固定，缺失区域从噪声开始 | mask 与可选文本条件 | 只更新 mask 指定区域 | [4] |
| ControlNet | `x_T` 或图像相关起点 | 边缘、姿态、深度等控制图 | 结构条件通过额外网络进入去噪过程 | [13] |

训练阶段的真实图只用于构造监督信号。推理阶段保留的是训练好的参数、随机起点、时间步序列和可选条件；不同产品形态改变的是采样起点、条件输入或 sampler。

### 4.2 扩展路线

DDPM 给出基本接口后，后续扩展主要发生在工程接口、去噪对象和产品交付三处。三者共同说明 diffusion 如何从图像论文方法进入图像 / 视频生成系统。

#### 4.2.1 工程改进

DDPM 给出训练和采样接口后，2021-2022 年的后续工作主要改动三个位置：采样路径走多少步、条件怎样进入每一步、去噪张量放在哪个空间里计算。

| 问题 | 解法 | 接口变化 | 来源 |
|---|---|---|---|
| 采样慢 | DDIM | 把反向过程改成 deterministic non-Markovian path，使采样可跳过部分中间时间步 | [2] |
| 条件控制 | CFG | 同一网络同时预测有条件与无条件噪声，采样时线性组合两次预测 | [3] |
| pixel space 计算贵 | Latent Diffusion | 先用 VAE 把图像压到 latent space，再在 latent 上去噪 | [4] |

CFG 的采样公式为：

$$\epsilon = \epsilon_{\mathrm{uncond}} + w \cdot (\epsilon_{\mathrm{cond}} - \epsilon_{\mathrm{uncond}})$$

`w` 控制条件强度；文本、类别或图像条件通过每一步噪声预测影响采样轨迹[3][4]。Latent Diffusion 则把每一步去噪从 pixel space 移到 VAE encoder 压缩后的 latent space，Stable Diffusion 基于这一设计训练 text-to-image 模型，并在 2022-08 公开发布模型权重[4][8]。

![image.png](images/W6jHbK4qJocDf0x9mUhcHc5Fnuc.png)

#### 4.2.2 图像到视频

2022-2024 间，Diffusion 的去噪对象从单张图像扩展到视频表示。图像系统在图像或图像 latent 上去噪，视频系统在带时间维度的 latent、frame sequence 或 spacetime patch 上去噪。

| 系统 | 时间 | 去噪对象 | 说明 | 来源 |
|---|---|---|---|---|
| DALL-E 2 / Imagen / Stable Diffusion | 2022 | 图像或图像 latent | 文本条件进入每一步去噪；Stable Diffusion 使用 LDM 公开 text-to-image 权重 | [4][5][6][8] |
| GEN-1 | 2023-02 | video latent | 输入 source video 与文本 / 图像条件，输出保留原视频结构约束的 stylized video | [15] |
| Stable Video Diffusion | 2023-11 | video latent | 基于 video diffusion 生成短视频片段 | [9] |
| Sora | 2024-02 | spacetime patch | 把视频表示为时空 patch，再在这些 token 上做去噪生成 | [7][16] |

视频生成比图像生成多出时间一致性约束：同一人物、物体位置、运动轨迹和场景状态需要跨帧保持一致。OpenAI Sora 技术报告以 "world simulators" 描述 video generation models[7]；§8 再展开可交互 world model。

#### 4.2.3 产品路线

2022-2024 间，diffusion 产品按公开方式可分为闭源图像 / 视频生成、开放权重图像生成、开放视频生成三类。三类系统使用相近的去噪接口，但交付形式不同。

| 路线 | 代表系统 | 公开形式 | 工具链特征 | 来源 |
|---|---|---|---|---|
| 闭源图像 / 视频生成 | DALL-E 2、Imagen、Sora、Veo | API、网页产品或技术报告 | 模型权重未公开，用户通过产品入口调用 | [5][6][7][17] |
| 开放权重图像生成 | Stable Diffusion | 权重与代码生态公开 | LoRA、ControlNet、ComfyUI 等工具围绕开源权重扩展 | [4][8][13] |
| 开放视频生成 | Stable Video Diffusion | 研究权重或代码生态公开 | 主要用于短片段生成与研究复现 | [9] |

产品路线没有改变 §4.1.3 的基本接口：生成结果仍由采样起点、条件输入、sampler 和训练好的去噪网络共同决定。

### References

- [1] Ho et al., Denoising Diffusion Probabilistic Models (DDPM), NeurIPS 2020. arXiv:2006.11239
- [2] Song et al., Denoising Diffusion Implicit Models (DDIM), ICLR 2021. arXiv:2010.02502
- [3] Ho & Salimans, Classifier-Free Diffusion Guidance, arXiv 2022. arXiv:2207.12598
- [4] Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, CVPR 2022. arXiv:2112.10752
- [5] Ramesh et al., Hierarchical Text-Conditional Image Generation with CLIP Latents (DALL-E 2), arXiv 2022. arXiv:2204.06125
- [6] Saharia et al., Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding (Imagen), NeurIPS 2022. arXiv:2205.11487
- [7] OpenAI, Video generation models as world simulators (Sora technical report), 2024-02.
- [8] Stability AI, Stable Diffusion Public Release, stability.ai 2022-08-22.
- [9] Blattmann et al., Stable Video Diffusion, arXiv 2023. arXiv:2311.15127
- [10] Goodfellow et al., Generative Adversarial Nets, NeurIPS 2014. arXiv:1406.2661
- [11] Kingma & Welling, Auto-Encoding Variational Bayes, ICLR 2014. arXiv:1312.6114
- [12] Rezende & Mohamed, Variational Inference with Normalizing Flows, ICML 2015. arXiv:1505.05770
- [13] Zhang & Agrawala, Adding Conditional Control to Text-to-Image Diffusion Models (ControlNet), ICCV 2023. arXiv:2302.05543
- [14] Meng et al., SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations, ICLR 2022. arXiv:2108.01073
- [15] Esser et al., Structure and Content-Guided Video Synthesis with Diffusion Models (GEN-1), ICCV 2023. arXiv:2302.03011
- [16] Peebles & Xie, Scalable Diffusion Models with Transformers (DiT), ICCV 2023. arXiv:2212.09748
- [17] Google DeepMind, Veo 3 release, deepmind.google 2024-12.

---

## 5. 第四阶段：VLM 与多模态理解 （2020-2024）

2020-2024 年，多模态理解从图文表征对齐走向 VLM。

1. CLIP （ICML 2021） 用对比学习把图像和文本编码到同一个向量空间，解决图文匹配与 open-vocabulary 视觉理解；
2. GPT-4V / LLaVA 把视觉特征接入 LLM，使语言模型可以基于图像回答问题；
3. VLA 则在 VLM 基础上把输出从文本扩展为机器人动作。

CLIP 提供视觉-文本对齐，VLM 提供视觉输入下的语言推理，VLA 把这种推理接到 embodied action。

![image.png](images/Rw0hbe7aUodELmx48h6cPZMNnuf.png)

### 5.1 CLIP：图文对齐（2021）

CLIP (Contrastive Language-Image Pre-training, Radford et al.， OpenAI ICML 2021）[1] 用 contrastive learning 训练图像 encoder 和文本 encoder，把图像与文本映射到同一个 embedding space。

![image.png](images/CInnbLRvuolFB8xWagWcrSDwnfd.png)

#### 5.1.1 训练框架

- **数据**：400M 对图像和文本描述，从 web 收集（WIT-400M）;
- **Encoder**：image encoder （ViT-B/16， ViT-L/14， ResNet） 把图像编码成向量，text encoder （Transformer） 把文本编码成向量，联合训练；
- **Loss**：InfoNCE 在一个 batch 内把原本配对的 （image， text） 作为正样本，把错配图文作为负样本；训练目标是提高正样本图文向量的相似度，同时降低错配图文向量的相似度；
  $\mathcal{L}_{\mathrm{CLIP}}=-\frac{1}{2 N} \sum_{i=1}^N\left[\log \frac{e^{\operatorname{sim}\left(v_i, t_i\right) / \tau}}{\sum_{j=1}^N e^{\sin \left(v_i, t_j\right) / \tau}}+\log \frac{e^{\operatorname{sim}\left(t_i, v_i\right) / \tau}}{\sum_{j=1}^N e^{\operatorname{sim}\left(t_i, v_j\right) / \tau}}\right]$

训练完成后，匹配的图文对具有较高的余弦相似度。

#### 5.1.2 下游影响

CLIP 展示了卓越的零样本迁移能力：在没有任何任务特定微调的情况下，它就能对图像进行分类、根据文本查询检索图像，并执行视觉推理。CLIP 的 vision encoder 成为后续 VLMs  的标准 backbone。§7.1.1 中 RT-2 / π₀ 等模型也多用 CLIP / SigLIP 系列先抽取视觉特征。

- **Text-to-image generation**：Stable Diffusion / DALL-E 2 / Imagen 的 text encoder 都是 CLIP（或衍生的 OpenCLIP / T5）；
- **Open-vocabulary detection / segmentation**: OWL-ViT (Minderer et al., ECCV 2022)[3] / GroundingDINO / SAM-2 prompt; 
- **VLM 的视觉模块：**
  - LLaVA / Qwen-VL / InternVL 等模型常用 CLIP-ViT（或 SigLIP）先把图像变成视觉特征；
  - 这些特征还需要通过 projection / adapter / cross-attention 对齐到 LLM 能处理的 token 表示；

### 5.2 VLM：把视觉接入 LLM （Generative VLMs (2022--2023)）

CLIP 之后，下一步是把视觉 encoder 接到生成式语言模型上。模型不再只判断图文是否匹配，而是基于图像生成开放式文本回答。

#### 5.2.1 LLaVA (2023)

LLaVA (Liu et al.， NeurIPS 2023）[5] ，用 CLIP 特征到 LLM token space 的线性 projection，加上 visual instruction tuning，验证了 VLM 的基本路线。相比需要复杂跨模态模块的方案，这条路线更轻：保留已有 vision encoder 和 LLM，**只训练中间连接层与视觉指令数据**，让 LLM 能接收图像信息并回答视觉问题。

![image.png](images/GKGTbGAAOovyipxWgo7cKVAZnbf.png)

- **模型结构**：冻结 CLIP ViT-L/14 作为 vision encoder，用 projection layer 把图像特征映射到 LLM 可接收的 token 表示，再接入 Vicuna；
> LaVA 使用一个约有 2000 万参数的 2 层 MLP 将 CLIP ViT-L（3.04 亿参数）连接到 Vicuna-13B（130 亿参数）。为什么这么小的桥接模块能够奏效？
> 
> 1. CLIP ViT-L 已经能产生与语言对齐的特征（通过在 4 亿对数据上的对比训练获得）；
> 2. Vicuna-13B 已经理解语言结构、推理和遵循指令；
> 3. MLP 桥只需要在它们的嵌入空间之间进行转换，而不必从零学习视觉或语言理解；
- **Stage 1：图文对齐**：用 558K 图文对训练 projection layer，让图像特征能对齐到 LLM 的语言表示空间；
- **Stage 2：视觉指令微调**：用 GPT-4 生成的 158K 条视觉指令数据做 instruction tuning，让模型学会按用户问题基于图像内容作答；

LLaVA 开源后成为 VLM 的常见实现模板；LLaVA-1.5 （2023-10） 把 projection 从单层 linear 改为 MLP，benchmark 结果进一步提升。

2024 年起，多模态能力从「冻结视觉编码器 + 桥接模块 + LLM」的模块化路线，进入更原生的多模态模型阶段：

- **GPT-4o**：OpenAI 将其描述为跨文本、视觉和音频端到端训练的单一模型；
- **Gemini**：Google 技术报告称 Gemini 是 natively multimodal，并在文本、图像、音频、视频上联合训练[7]；

> 关键区别：早期的视觉-语言模型是将视觉功能附加到语言模型上。原生多模态模型在预训练期间将所有模态视为同等重要，有可能学习到更深层的跨模态表征。

### 5.3 从 VLM 到 VLA

- VLM 的输出仍然是文本；VLA （Vision-Language-Action） 把输出空间从文本 token 扩展到机器人动作。
- RT-2 的做法是把机器人动作离散化为 token，让 VLM 通过 fine-tuning 直接输出 action token；π₀ / GR00T 等后续路线则常把 VLM 作为语义理解或 reasoning 模块，再接 continuous action head、diffusion transformer 或 flow-matching action head[6]。

这一步改变了模型接口：VLM 解决「看图后如何用语言回答」，VLA 解决「看图和指令后如何执行动作」。

### References

- [1] Radford et al., Learning Transferable Visual Models From Natural Language Supervision (CLIP), ICML 2021. arXiv:2103.00020
- [2] Jia et al., Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision (ALIGN), ICML 2021. arXiv:2102.05918
- [3] Minderer et al., Simple Open-Vocabulary Object Detection with Vision Transformers (OWL-ViT), ECCV 2022. arXiv:2205.06230
- [4] OpenAI, GPT-4V(ision) System Card, openai.com 2023-09.
- [5] Liu et al., Visual Instruction Tuning (LLaVA), NeurIPS 2023. arXiv:2304.08485
- [6] Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, arXiv 2023. arXiv:2307.15818
- [7] Gemini Team, Gemini: A Family of Highly Capable Multimodal Models, 2023. Technical Report.
- [8] Anthropic, The Claude 3 Model Family: Opus, Sonnet, Haiku, 2024. Model Card.
- [9] Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, arXiv 2023. arXiv:2307.15818

---

## 6. 第五阶段：World Models 起源（2018）

2018 年 Ha & Schmidhuber 的 V+M+C 架构是 deep learning 语境下 world model 的早期代表[1]。该工作把视觉压缩、latent dynamics 与 policy training 分成三个模块；video diffusion 的产品化路径见 §4.2.2。

### 6.1 V+M+C：dream-based 训练雏形

Ha & Schmidhuber 提出：agent 先学一个内部 world model，再在该模型中模拟环境轨迹（dream rollout）训练 policy，而非每步与真实环境交互[1]。三模块构成：

| 模块 | 功能 | 实现 |
|---|---|---|
| V (Vision) | 高维 observation 压缩到 latent | VAE encoder，32 维 latent z |
| M (Memory) | 在 latent 空间预测下一时刻状态 | MDN-RNN 预测 $z_{t+1} \mid z_t, a_t$ |
| C (Controller) | 根据 latent 输出动作 | 线性 policy，CMA-ES 训练 |

agent 在 dream rollout 中训练 policy 后 0-shot 部署到真实环境，CarRacing-v0 上取得 906 ± 21 分（同期 best published 591）[1]。

V+M+C 使用 VAE、MDN-RNN 与玩具环境轨迹数据[1]。§8 另列 2024-2026 年的 latent video diffusion、web-scale 视频数据和可交互 world model 路线。

### References

- [1] Ha & Schmidhuber, World Models, NeurIPS 2018. arXiv:1803.10122 (worldmodels.github.io)

---

## 7. 延伸 1：具身 VLA （2023-2026）

VLA （Vision-Language-Action） 在视觉和语言输入之外，把模型输出从文本 token 扩展为机器人动作。

- 2023 年 Google DeepMind RT-2 把 VLM fine-tune 成可输出动作的 VLA；
- 2024-2026 年，Physical Intelligence π 系列、NVIDIA GR00T、Gemini Robotics、OpenVLA / Octo 等路线继续推进跨机器人形态泛化、开源 baseline 和产品化；
- 国内 AgiBot World / GO-1、Galaxea G0、RynnBrain / RynnVLA、LingBot-VLA、UnifoLM-VLA-0、Xiaomi-Robotics-0 等路线跟进。
- 

### 7.1 VLA 进展

VLA 进展分两支：

1. 国际线以 Google / DeepMind、Physical Intelligence、NVIDIA 等产业主线和 OpenVLA、Octo 等开源 baseline 为代表；
2. 国内线在 2025-2026 年形成以数据集、开源权重和真机部署为中心的多条路线。

#### 7.1.1 国际 VLA 路线

国际 VLA 可分为三类：

1. RT-2 / Gemini Robotics 代表 Google / DeepMind 的闭源研究主线；
2. π 系列 / GR00T 代表产业化 humanoid 主线；
3. OpenVLA / Octo 代表开源学术和 baseline 主线。

| Model | 机构 | Release | Robot / 场景 | 数据 / 训练特点 | 公开状态 | 关键贡献 | 来源 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RT-2 | Google DeepMind | 2023-07 | dual-arm RT robot | web-scale + RT-1 | 官方模型 / 权重未开放；有第三方复现 | 将 VLM fine-tune 为 VLA | [1] |
| Octo | UC Berkeley / Stanford 等 | 2024-05 | 多机器人 manipulation | Open X-Embodiment，约 800k robot episodes | 代码 MIT；checkpoint 公开 | 开源 generalist robot policy baseline | [2] |
| OpenVLA | Stanford / Berkeley 等 | 2024-06 / 2025 | 多机器人 manipulation | Open X-Embodiment, 970k robot demonstrations | 代码 / 权重 MIT | 7B 开源 VLA，面向可微调部署 | [3] |
| π 系列 | Physical Intelligence | 2024-2026 | 7 个 embodiment + open-world 场景 | π₀ 使用 ～10k hrs robot data；π₀.5 / π₀.7 继续扩展泛化 | π₀ / π₀.5 代码与 checkpoint 公开（Apache-2.0）；π₀.7 公开论文 / 报告，未见公开 checkpoint | generalist policy + flow-matching action head | [4, 5, 9] |
| GR00T N1 | NVIDIA | 2025-03 | humanoid | open data + sim | 代码 / 权重公开；N1 / N1.5 权重偏非商用许可 | humanoid foundation model | [6] |
| Gemini Robotics 1.5 / ER 1.5 | Google DeepMind | 2025 | ALOHA / Bi-arm Franka / Apollo humanoid 等 | multi-embodiment robot data + Motion Transfer | ER 1.5 API; Robotics 1.5 面向 select partners | VLA + embodied reasoning 双模型组合 | [7] |
| GR00T N1.7 | NVIDIA | 2026-04-17 | humanoid | EgoScale 20,854 hrs egocentric | EA; 代码 / 权重公开，商业许可需按 NVIDIA release 条款核对 | Action Cascade dual-system + dexterity scaling law | [10] |

**Google DeepMind RT-2 (2023-07)[1]**

RT-2 (Brohan et al.， Google DeepMind 2023-07）[1] 把 VLM （PaLI-X 5B/55B / PaLM-E 12B/562B） 直接 fine-tune 成 VLA。

它把机器人动作离散化为 LLM vocabulary 中的 token，使 LLM 在输出端直接生成 action token。

- **数据**：继承 PaLI-X / PaLM-E 的 web-scale pretraining，再加入 RT-1 收集的 13 个机器人、17 个月数据（～130k 任务 episode）；
- **泛化**：对未见过的 object / instruction 做零样本执行，novel objects 上的 closed-loop success 相比 RT-1 baseline 提升 +60%；
- **影响**：把 "VLM → fine-tune → VLA" 模式确立为后续标准（LLaVA / Qwen-VL / SigLIP 等都被尝试当 V-base）；

**Physical Intelligence π 系列 （2024-2026）**

Physical Intelligence （PI） 是 Sergey Levine 等创立的具身公司，主线 π₀ → π₀。5 → π₀.7: 

- **π₀** （2024-10）[4]：generalist robot policy，1 个 model 跨 7 个 embodiment（Franka / UR5e / Mobile Aloha / Trossen 等），～10k hrs 真机数据训练；VLM (PaliGemma) + flow matching action head. PI 公开 demo 在洗衣 / 折叠 / 打包多场景；
- **π₀.5** (2025-04-22)[5]: open-world generalization. 用 action knowledge transfer（从 web video + lab data 联合训练）在未训练过的 home / kitchen 场景 0-shot 表现；
- **π₀.7** （2026-04-16）[8]：steerable robot foundation，PI 公开报告中描述为泛化能力进一步提升；具体 architecture 与训练规模待 paper release（写作时 verify）；

PI 路线使用闭源模型、大规模真机数据和 flow-matching action head；这与 RT-2 逐 token 自回归生成动作的方式不同。

**NVIDIA GR00T (2025-03 → 2026-04-17)**

NVIDIA GR00T 是 humanoid foundation model 的开放路线：

- **GR00T N1** （2025-03）[6]：首个开源 humanoid foundation model，dual-system（VLM 推理 + Diffusion Transformer 动作）；
- **GR00T N1.5** （2025-06）：加入 FLARE（从人类视频学习）；
- **GR00T N1.6** （2026-04-15）：VLM 升级到 NVIDIA Cosmos-Reason-2B；
- **GR00T N1.7** （2026-04-17）[9]：3B 参数 "Action Cascade" = Cosmos-Reason2-2B （System 2） + 32-layer DiT （System 1）；GR00T N1.7 使用 EgoScale 数据集训练，该数据集包含 20,854 小时人类第一视角操作视频。NVIDIA 公开报告中提出 robot dexterity scaling law：当 EgoScale 训练数据从 1k 小时增加到 20k 小时时，模型在灵巧操作任务上的表现约翻倍；这说明更大规模的人类操作视频可能有助于提升 humanoid 的操作能力。

NVIDIA 路线强调开放 foundation model，并与 Cosmos / Isaac Sim 工具链绑定；合作厂商包括 Boston Dynamics / Agility / Figure 等 humanoid 公司。

**开源学术与 Google 后续线**

OpenVLA 与 Octo 是国际开源路线中常用的 baseline。

- OpenVLA 是 7B VLA，基于 Open X-Embodiment 的 970k robot demonstrations 训练；Octo 是 open-source generalist robot policy，基于约 800k robot episodes 训练，提供 27M / 93M 两种规模[2， 3]。Google DeepMind 在 RT-2 之后公开 Gemini Robotics 1.5 / Gemini Robotics-ER 1.5：前者是 multi-embodiment VLA，后者是 embodied reasoning VLM，用于空间理解、任务规划和进度估计[7]。

- π₀.7 （2026-04-16） 是 PI 当前主线，是否取代 π₀ 作为 default baseline 待后续 paper / release 明确

#### 7.1.2 国内 VLA 路线

国内 VLA / 具身 foundation model 在 2025-2026 年形成多条公开路线。

| Model | 公司 / 团队 | Release | Robot / 场景 | 数据 / 训练特点 | 公开状态 | 来源 |
| --- | --- | --- | --- | --- | --- | --- |
| AgiBot GO-1 | 智元 | 2025-03-10 | 多形态机器人 | AgiBot World：1M+ trajectories，217 个任务 | 代码 / 数据 / GO-1 权重公开；权重 CC BY-NC-SA 4.0 | [11] |
| Galaxea G0 | 星海图 Galaxea | 2025-09 | 移动双臂操作 | Galaxea Open-World Dataset：500 小时、50 个场景、150+ 任务 | 数据 / 模型公开；G0-VLA CC BY-NC-SA 4.0，G0Plus 为非商用社区许可 | [12] |
| RynnBrain / RynnVLA | 阿里达摩院 | 2026-02 / 2025-11 | embodied foundation / LIBERO + LeRobot | RynnBrain 含 2B / 8B / 30B-A3B MoE；RynnVLA-002 统一 VLA 与 world model | 代码 / checkpoint Apache-2.0 | [13, 14] |
| LingBot-VLA | 蚂蚁 / Robbyant | 2026-01 | 9 种双臂机器人配置 | 约 20,000 小时真实机器人数据；评估覆盖 3 个平台、100 个任务 | 代码 / 4B 权重 / benchmark data 公开，Apache-2.0 | [15] |
| UnifoLM-VLA-0 | 宇树 | 2026-01-29 | G1 humanoid | 基于 Qwen2.5-VL-7B，面向 12 类操作任务 | 代码 BSD-3-Clause；权重 CC BY-NC-SA 4.0 | [16] |
| Xiaomi-Robotics-0 | 小米机器人 | 2026-02 | 双臂实时控制 | 4.7B VLA; 约 200M robot timesteps + 80M vision-language samples | 代码 / checkpoint Apache-2.0 | [17] |

**智元 AgiBot GO-1 （2025-03-10）[11]**

GO-1 是智元 （AgiBot） 的 ViLLA （Vision-Language-Latent-Action） 架构。它不直接生成动作 token，而是在 latent space 中做中间规划，再由 action expert 输出动作：

- **架构**：MoE + Latent Planner + Action Expert 三件套，在 latent space 做 planning，而不是直接生成 action token；
- **训练数据**：AgiBot World 数据集，1M+ trajectories，217 个任务；公开材料将其定位为大规模 robotic learning platform；
- **性能**：平均成功率 46% → 78%（vs GO-1 之前 baseline）；

**宇树 UnifoLM-VLA-0 （2026-01-29）[16]**

UnifoLM-VLA-0 是宇树为 G1 humanoid 设计的 VLA：

- **Backbone**：基于阿里 Qwen2.5-VL-7B（国内 VLA 直接复用 Qwen 系列 VLM 的代表案例）；
- **任务**：单一 policy 在 G1 上完成 12 类操作（开闭抽屉 / 插拔 / 抓放 / 工具使用）；
- **公开状态**：UnifoLM-VLA-Base 已在 Hugging Face 公开；任务侧聚焦 G1 humanoid 操作；

### 7.2 VLA 融合方向

VLA 与其他范式的融合主要沿两条方向展开：与 reasoning model 融合形成 dual-system 架构，与 World Models 融合形成 dream-based training。前者处理 long-horizon 任务规划，后者补充真机数据不足。

#### 7.2.1 VLA + 推理融合

VLA + reasoning 融合的核心模式是 dual-system：System 1 是高频动作 policy，负责实时控制；System 2 是慢速 reasoning LLM，负责拆解任务和规划步骤。两者协同处理 long-horizon / 多步任务。

**Reasoning model 介绍**

Reasoning model 把 chain-of-thought 推理训练成模型能力，而不是只依赖外部 prompt-engineering。

代表工作包括 OpenAI o1 （2024-09）[18] / o3 （2025-04） / DeepSeek R1 （2025-01）[19] / DeepSeek R2 （2026-04，32B dense 单 24GB GPU 可跑）。

这些模型在 AIME / GPQA / Codeforces 等 multi-step 推理 benchmark 上明显超过同期 GPT-4 / GPT-5 base。

**Dual-system 三个实例**

- **Figure Helix System 1+2** ( 2026-01) [8]: 
  - 三级架构包括 System 0 实时平衡 （1 kHz）、System 1 视觉运动 （200 Hz， VLA policy）、System 2 高层推理 （LLM reasoning）；
  - 公开报告中明确借鉴 Kahneman 快 / 慢思考二系统；
  - 2026-01 的 4 分钟连续洗碗机自主 demo 由该架构实现；
- **π₀.5 reasoning version** (2025-04-22)[5]: 
  - π₀.5 在 base policy 之外集成 reasoning 模块；
  - LLM 先把当前 task 拆成 sub-task，再交由 base policy 执行；
- **GR00T N1.7 Action Cascade** ( NVIDIA 2026-04-17) [10]: 
  - System 2 使用 Cosmos-Reason2-2B（NVIDIA 自家 reasoning VLM，详见 §8.2 Cosmos），System 1 使用 32-layer Diffusion Transformer；
  - "Action Cascade" 指 reasoning 输出的 plan 会级联到 DiT action 生成；

**关键挑战**

- **System 1/2 latency 协调**：
  - System 2 LLM 推理 ～秒级延迟，System 1 控制 ～10 ms；
  - 协调机制（event-triggered / 周期性 / 异步并行）直接影响系统响应
- **Long-horizon planning**：System 2 输出的 plan 在 System 1 执行过程中可能偏离，何时重 plan 是开放问题；
- **Plan ↔ action 接口形式**：language token / latent vector / sub-task list，当前各家 design choice 不同，尚无统一接口；

#### 7.2.2 VLA + World Models 融合

VLA 与 World Models 的耦合范式（5 种架构选择）以及 World Models 作为 simulator 替代真机做 RL / evaluation 的两种独立角色，统一在 §8 展开[20]。当前公开报告中可见的具体融合点包括：sim-to-real data augmentation（NVIDIA Cosmos Transfer 用于 GR00T N1.7 训练[10]）、VLA 内化 future prediction 作为辅助 loss（GR-1 / WorldVLA / UniVLA 等[20]）、dream-based RL 训练（综述 §4.1[20]）。

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
- [11] AgiBot， GO-1 + AgiBot World 数据集 release， agibot.com 2025-03-10； GitHub: github.com/OpenDriveLab/Agibot-World; Hugging Face: huggingface.co/agibot-world/GO-1
- [12] Galaxea, Galaxea Open-World Dataset and G0 Dual-System VLA Model, arXiv 2025. arXiv:2509.00576; GitHub: github.com/OpenGalaxea/GalaxeaVLA; Hugging Face: huggingface.co/OpenGalaxea/G0-VLA
- [13] Alibaba DAMO Academy, RynnBrain: Open Embodied Foundation Models, arXiv 2026. arXiv:2602.14979; GitHub: github.com/alibaba-damo-academy/RynnBrain
- [14] Alibaba DAMO Academy, RynnVLA-002: A Unified Vision-Language-Action and World Model, GitHub: github.com/alibaba-damo-academy/RynnVLA-002; Hugging Face: hf.co/Alibaba-DAMO-Academy/RynnVLA-002
- [15] Robbyant, A Pragmatic VLA Foundation Model (LingBot-VLA), arXiv 2026. arXiv:2601.18692; GitHub: github.com/Robbyant/lingbot-vla; Hugging Face: hf.co/robbyant/lingbot-vla-4b
- [16] Unitree, UnifoLM-VLA-0 release, unitree.com 2026-01-29; GitHub: github.com/unitreerobotics/unifolm-vla; Hugging Face: huggingface.co/unitreerobotics/UnifoLM-VLA-Base
- [17] Xiaomi Robotics, Xiaomi-Robotics-0: An Open-Sourced Vision-Language-Action Model with Real-Time Execution, arXiv 2026. arXiv:2602.12684; GitHub: github.com/XiaomiRobotics/Xiaomi-Robotics-0; Hugging Face: huggingface.co/XiaomiRobotics/Xiaomi-Robotics-0-Pretrain
- [18] OpenAI, o1 system card, openai.com/index/learning-to-reason-with-llms 2024-09-12.
- [19] DeepSeek, DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning, arXiv 2025. arXiv:2501.12948
- [20] NTU MARS et al., World Model for Robot Learning: A Comprehensive Survey, arXiv 2026. arXiv:2605.00080v1

---

## 8. 延伸 2：World Models 范式与近期形态 （2024-2026）

V+M+C （§6.1） 之后，World Models 在 2024-2026 沿两条线展开：与 VLA policy 的 5 种耦合范式（§8.2）、独立作为 simulator 的两种角色（§8.3）；2025-2026 进入 foundation 化阶段，代表为 DeepMind Genie 与 NVIDIA Cosmos[1]。

### 8.1 概念再定位

World Model 在本节指 action-conditioned 的视觉 / 状态预测器：给定当前观测 $o_t$ 与候选动作序列 $a_{t:t+H-1}$，输出未来观测序列 $o_{t+1:t+H}$[1]。

它与 §4 video generation 的差别在动作维度：换不同的 $a$ 输入，输出未来必须以物理一致的方式不同。纯文本 / 图像条件的 video diffusion 模型不满足这一性质，被综述定义为 **passive world model**[1]。

### 8.2 范式：World Model 与 policy 的耦合

综述按 backbone 共享程度归纳出 5 种范式，按"WM 与 policy 的耦合紧密度"递增排列[1]。下面展开 3 种主流：

#### 8.2.1 IDM-style：先想象再行动

WM 与 policy 是两个独立模型。WM 先按 $\hat{o}_{t+1:t+H} = W(o_t, l)$ 生成未来视频，policy 再按 $\pi(a \mid o_t, l, \hat{o}_{t+1:t+H})$ 从想象的未来反推动作；本质是把联合分布做 chain-rule 两步采样[1]。代表作 UniPi[2]。

#### 8.2.2 Single-backbone：联合生成

未来视频与未来动作拼成同一个目标向量 $x = [z_v; z_a]$，由一个共享 backbone（通常是 video diffusion transformer）联合去噪生成；动作被当作"额外的 latent frame"塞进视频生成序列[1]。代表作 Cosmos Policy[3]。

#### 8.2.3 Latent-space WM：表征空间预测

不预测像素或视频 latent，而是直接预测未来观测的 embedding，与 action 生成在同一个 MLLM backbone 内联合优化；推理时不解码任何视觉输出[1]。这条路线对应 LeCun 的 JEPA (Joint Embedding Predictive Architecture) 主张：未来的"语义表征"比"长什么样"更对 control 有用。代表作 VLA-JEPA[4]。

剩余 MoE/MoT 与 Unified VLA 范式是上述 3 种之间的中间形态：MoE/MoT 在 Single-backbone 基础上保留视频与动作的专家分工，Unified VLA 在 Latent-space WM 基础上把 future prediction 当作 VLA 的辅助 loss[1]。横向对比：

| 范式 | Backbone | 推理时是否生成未来 | 与 §3 - §5 的继承关系 | 代表作 |
|---|---|---|---|---|
| IDM-style | Video diffusion (§4) | 必须 | 沿用 §4 video diffusion 接口 | UniPi[2] |
| Single-backbone | Video diffusion (§4) | 可选 | 把 §3 attention + §4 DiT 用作联合生成 backbone | Cosmos Policy[3] |
| MoE/MoT | Video diffusion (§4) | 看选择 | 把 π0 双专家结构（§7.1.1）迁移到 video backbone | Motus[1] / GE-Act[1] |
| Unified VLA | MLLM (§5) | 通常不 | 直接复用 §5 VLM backbone，加 future prediction 辅助 loss | GR-1[1] / WorldVLA[1] |
| Latent-space WM | MLLM (§5) | 不生成 | 复用 §5 VLM 表征空间，对齐 JEPA 主张 | VLA-JEPA[4] |

<!-- REVIEW: 此处建议补 Survey arXiv:2605.00080v1 Fig. 3 (5 种范式的架构对比图)，截到 images/world-model_5paradigms_from-survey2605.png -->

### 8.3 角色：policy 一部分 vs 独立 simulator

WM 在系统中的角色分两类[1]：

- **作为 policy 的一部分**：通过 imagined future 给 action 生成提供条件或约束，对应 §8.2 的 5 种范式（§7.2.2 已涉及部分代表方法）；
- **作为 simulator**：替代真机环境，让 policy 在想象 rollout 中做 RL 训练（WMPO[5] / WoVR[6]），或对候选 policy / checkpoint 做离线评估（WorldEval[7]）。

WoVR 进一步指出 simulator 角色的核心瓶颈是 **action faithfulness**——若 WM 的预测对 action 不敏感，evaluation 信号本身失效；因此 simulator-用途的 WM 与 policy 之间常采用 co-evolution 训练（policy rollout 反过来 refine WM）[6]。

<!-- REVIEW: 此处建议补 Survey arXiv:2605.00080v1 Fig. 5 (WM as RL vs Evaluation 双角色图)，截到 images/world-model_2roles_from-survey2605.png -->

### 8.4 当前形态：foundation 化的代表

2025-2026 间，WM 从单点模型走向通用 foundation 平台，代表为 Genie 与 Cosmos[1]。

- **DeepMind Genie 系列**：Genie 1 (2024-02) 256×256 / 11B 参数，2D platform-style 可交互生成[8]；Genie 2 (2024-12) 扩展到 3D，约 1 分钟一致性[9]；Genie 3 (2025-08-05) 720p / 24 fps real-time，官方表述可在 720p 下保持「几分钟」级一致性[10]；Project Genie (2026-01-29) 商业化为 Google AI Ultra 产品[11]。
- **NVIDIA Cosmos**（2025-01 起）：physical AI 工具链。Predict 2.5 做未来状态预测、Transfer 2.5 做 sim-to-real 数据增强、Reason 2 提供 VLM reasoning（同时被 GR00T N1.6 / N1.7 用作 System 2 backbone，§7.2.1）；与 Isaac Sim / GR00T 形成完整 stack[12]。

综述对当前阶段的总结：领域瓶颈已从「生成更真实视频」转向「生成在 action 因果对齐、长 horizon 物理自洽、跨视角一致、交互稳定 4 个维度上都可信的未来」[1]。

### References

- [1] NTU MARS et al., World Model for Robot Learning: A Comprehensive Survey, arXiv 2026. arXiv:2605.00080v1
- [2] Du et al., Learning Universal Policies via Text-Guided Video Generation (UniPi), NeurIPS 2023. arXiv:2302.00111
- [3] Cosmos Policy (Kim et al., 2026)，见 [1] §3.3 / Table 1
- [4] VLA-JEPA (Sun et al., 2026)，见 [1] §3.6 / Table 1
- [5] WMPO (Zhu et al., 2026)，见 [1] §4.1
- [6] WoVR (Jiang et al., 2026)，见 [1] §4.1
- [7] WorldEval (Li et al., 2025e)，见 [1] §4.2
- [8] Bruce et al., Genie: Generative Interactive Environments, ICML 2024. arXiv:2402.15391
- [9] DeepMind, Genie 2: A large-scale foundation world model, deepmind.google 2024-12.
- [10] DeepMind, Genie 3: A new frontier for world models, deepmind.google/en/blog/genie-3 2025-08-05.
- [11] DeepMind, Project Genie + Google AI Ultra release, deepmind.google 2026-01-29.
- [12] NVIDIA, Advancing Physical AI with Cosmos 2.5 + Reason2, developer.nvidia.com/blog 2026-04.