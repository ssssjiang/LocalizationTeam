# 完整逐字稿件（演讲式，约 50 min + 10 min 讨论）

> **使用方式**：
>
> - 这是一份"可念稿件"，但**强烈建议你按自己语言改写**——念稿和讲是两件事
> - 每段标了**预计时长**和**关键 hook**（这一段必须传递的核心信号）
> - 用 `[投影]` 标记建议在投影上展示什么
> - 用 `[节奏]` 标记重要的停顿、互动、抛问
> - 公式骨架（共 5 行）只用作机制讲解的"指针"，不展开推导
>
> **总结构（第一次分享：50 min 我讲 + 10 min 讨论）**：
>
> - 开场 4 min
> - 主体 43 min（4 老阶段：判别式 AI / Transformer 范式 / 生成式 AI / World Models 起源）
> - 收尾 3 min（含 3 个讨论问题，引出 10 min 讨论）
> - **3 个新方向（推理大模型 / 具身 VLA / World Models 突破）留到下次分享展开**

---

# 开场（4 min）

> **核心 hook**：建立基调——"我不是来讲技术细节的，我是来串一条线、给我自己的判断的"。一上来就要把"我有视角"这个信号打出来；同时把"今天讲什么、不讲什么"提前讲清楚，让听众有正确预期。

[投影：标题页 — "AI 技术演进探讨（上篇）"，副标题 "从 RNN/CNN 到 World Models 起源，一条线 + 我的几个判断"]

各位，晚上好。

我能给的：**一条主线，加我对每个节点的几个判断**。

我先把今晚的范围说清楚——曹姐原来的列表加上后面这几年的演进，整个故事我把它分成 **4 老阶段 + 3 个新方向**。**今晚我只讲前 4 阶段**——AI 从 RNN/CNN 一路走到 World Models 起源，**12 年的故事**。

3 个新方向——**推理大模型、具身 VLA、World Models 真正突破**——我留到下次分享。原因有两个：① 我自己对这 3 个方向的理解还在更新中，今晚讲不透；② 4 个阶段已经是 12 年的故事，**讲透比讲全重要**。

至于"我能给什么"——**一条主线，加我对每个节点的几个判断**。

[节奏：这里需要修正一个之前的承诺——既然要讲"机制档"，就不能再说"完全不讲细节"]

我之前说过"今晚不讲技术细节"——这个承诺今晚要做一个**小修正**。我**不推公式**——比如 Transformer 的 attention 怎么从变分下界推、Diffusion 怎么从 ELBO 推、RLHF 的 PPO 损失怎么写——这些今晚都不展开。**但**我会写出几个**关键公式骨架**——比如 attention、diffusion 的训练目标、scaling law——**只是把它写在板上，用来解释直觉**，不做推导。原因是：这些机制如果不写出公式骨架，"为什么这样设计"很难讲清楚。

我答应：**写出公式只用来解释直觉，不展开数学**。今晚一共会出现 5 行公式骨架，分散在二/三/四阶段。

[投影：主线总览图——8 老节点（今晚讲）+ 3 新方向（下次讲）横向时间轴]

曹姐原来给的列表是 8 个节点：RNN/CNN、ResNet、Transformer、LLM、Diffusion、VLM、World Models、GEN-1。我把它们按 4 个阶段重新组织：

- **第一阶段 — 判别式 AI 的成熟**（RNN/CNN + ResNet）
- **第二阶段 — Transformer 范式的崛起**（Transformer + LLM）
- **第三阶段 — 生成式 AI 的爆发**（Diffusion + VLM）
- **第四阶段 — 走向世界模型与具身**（World Models + GEN-1）

[节奏：在这里停 1 秒，然后语气加重]

---

# 第一阶段：判别式 AI 的成熟（7 min）

> **核心 hook**：奠基视角——AI 第一次能"端到端学特征"，这是后面所有事的前提。

> **小观点**：判别式 AI 这个时代解决的不是"AI 能做多强"，而是"AI 能不能脱离手工特征"。

![](images/Pasted%20image%2020260427014931.png)

我们从 2012 年的 AlexNet 说起。

在 AlexNet 之前，做图像识别的标准流程是什么？工程师手工设计特征——SIFT、HOG、LBP——然后接一个分类器（SVM 或者浅层神经网络）。**整个 pipeline 的核心创新点在"特征工程"**——一个研究员的专业能力，很大程度上就体现在他能不能为某个任务设计出好特征。

CNN 做了什么？它把"特征工程"这件事**取消**了。**输入图像，模型自己端到端从数据里学出 layer 1 学边缘、layer 2 学纹理、layer 3 学物体部件、layer 4 学整个物体**。这是 AlexNet 在 2012 年 ImageNet 上一举把 top-5 错误率从 26.2% 降到 15.3% 之后，整个学术界突然意识到的事——CNN 学到的特征比人类工程师手工设计的要好得多。

[节奏：这里进入 CNN 机制段——讲清"为什么 CNN 真的能学到层级特征"]

> **CNN 为什么能学到层级特征**——讲两件事：

**第一件，卷积核 = 局部连接 + 权重共享**。

如果你做全连接，一个 224×224×3 的图像接到下一层每个神经元，参数量是 W×H×C × 输出维度——爆炸。CNN 把每个"神经元"换成一个**小卷积核**（比如 3×3），**在整张图上滑动**——参数量从 W×H×C 降到 k×k×C。

直觉上为什么这样合理？**一个'检测竖直边缘'的滤波器，在图像左上角和右下角应该是同一个滤波器**——所以参数应该复用。这是 CNN 强加的"先验"——平移不变性。

**第二件，层级特征 = 感受野叠加**。

第 1 层每个神经元只看到 3×3 的局部像素——能学到的最多是边缘、点、颜色块。但第 5 层呢？经过几次池化和卷积叠加，**第 5 层的一个神经元的感受野能覆盖到 50×50 像素左右**——这时候它能"看到"物体部件（眼睛、轮子）。第 10 层覆盖半张图——"看"整只猫。

[投影：Zeiler & Fergus 2013 论文的特征可视化图]

Zeiler & Fergus 在 2013 年 ECCV 那篇《Visualizing and Understanding CNNs》把这件事**用图直接画了出来**——第 1 层学到的是各个方向的边缘，第 2 层学到了纹理，第 3 层学到了物体部件，第 4 层学到了完整物体。这张图当年震撼了整个领域——**层级特征不再是猜测，是被可视化证实的**。

> **例子**：AlexNet 之后两年（2014），ImageNet 第一名变成了 GoogLeNet 和 VGG，错误率降到 7%。又过了一年（2015），ResNet 出来，降到 3.57%——**首次低于人类水平**。这中间没有一个工作回到"手工特征"的路线。

[节奏：转到 RNN 故事]

RNN 是平行的故事。在 RNN/LSTM 之前，处理序列（比如机器翻译、语音识别）也是分阶段 pipeline——分词、词性标注、语法树、对齐……每一步都是独立的模型。LSTM 在 1997 年就被 Hochreiter 和 Schmidhuber 提出了，但**真正爆发是 2014 年——Sutskever 那篇 seq2seq + Bahdanau attention**——一个端到端的 RNN 直接学会从英文映射到法文，**BLEU 分数 34.8，超过了当时所有 pipeline 系统**。

[节奏：这里抛一个连接点]

但 RNN 有一个致命问题——**它必须按时间步串行计算**，GPU 的并行能力用不上；**长序列还会梯度消失**。

> **梯度消失到底是什么**——讲清楚一句话：

RNN 反向传播时，梯度沿时间反向走，每一步都乘上权重矩阵 W——**N 步之后，梯度就是 W 的 N 次幂**。如果 W 的奇异值小于 1，梯度指数衰减到 0；大于 1，梯度爆炸。**长序列 = 长连乘 = 不可控**。

LSTM 怎么缓解？它在 RNN 上面加了一个 **cell state 通道**，这个通道的更新是**加法**而不是连乘——`c_t = f_t · c_{t-1} + i_t · g_t`——梯度沿这条通道走，**不会指数衰减**。

[节奏：这里给一个意外的连接，听众会"啊"一下]

**有意思的是——LSTM 这个"加法路径不衰减梯度"的思路，3 年后会再次出现，叫 ResNet 的残差连接**。两件事**没有引用关系**，但**事后看，思路高度相似**——这是深度学习领域反复出现的一个机制：**给梯度一条加法的高速公路**。

这个梯度问题 LSTM 只是缓解，没有根本解决——**最后真正解决它的，是 2017 年的 Transformer**。我们等下会讲到。

> **我的判断（小结）**：第一阶段的真正意义，不在于 RNN/CNN 的架构本身——它们今天已经被 Transformer 在大部分任务上替代。它的意义在于**第一次证明了"端到端从数据里学特征"这条路是 work 的**。这个范式确立之后，AI 才有了规模化的可能。这之前的 AI 是"工程师设计 + 数据训练"，这之后的 AI 是"架构 + 数据 + 算力"——人退到了二线。

参考资料：

- **Stanford CS231n — Convolutional Neural Networks**
[https://cs231n.github.io/convolutional-networks/](https://cs231n.github.io/convolutional-networks/)
- **Christopher Olah — Understanding LSTMs**
[https://colah.github.io/posts/2015-08-Understanding-LSTMs/](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- **Zeiler & Fergus — Visualizing and Understanding CNNs** (ECCV 2014)
[https://arxiv.org/abs/1311.2901](https://arxiv.org/abs/1311.2901)
- **Hochreiter & Schmidhuber — Long Short-Term Memory** (1997)
[https://www.bioinf.jku.at/publications/older/2604.pdf](https://www.bioinf.jku.at/publications/older/2604.pdf)
- **Sutskever et al. — Sequence to Sequence Learning with Neural Networks** (NeurIPS 2014)
[https://arxiv.org/abs/1409.3215](https://arxiv.org/abs/1409.3215)
- **Bahdanau et al. — Neural Machine Translation by Jointly Learning to Align and Translate** (ICLR 2015)
[https://arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473)

---

# ResNet 这个节点单独说 1 分钟 —— 它有点特殊（包含在第一阶段 7 min 内）

![](images/Pasted%20image%2020260427071822.png)

ResNet 在 2015 年出来。它解决的问题在当时看起来很反直觉——**网络越深，效果应该越好对吧？但 2015 年之前，网络深到 30 层之后，效果反而开始变差**。这不是过拟合（训练误差也在升高），是**优化层面的退化（degradation）**。

何恺明的方案优雅得不像话：让某一层的输入可以"跳过"中间几层直接加到后面，**公式上是 `y = F(x) + x` 而不是 `y = F(x)`**。

[节奏：这里讲清楚为什么残差连接真的能帮助优化——一句话保留"恒等映射保底"的直觉，但要补一个更准确的"梯度反传"机制]

> **残差连接为什么真的 work**——直觉解释 + 梯度机制各讲一句：

**直觉解释**：最差情况下中间层只要学到 `F(x) ≈ 0`，输出就退化成 `y = x`——**优化器有了一个保底退路**，可以放心做深。这是流传最广的解释，但**不是最准确的**。

**梯度机制**（这个更深一层）：写出反传公式

```
∂L / ∂x = ∂L / ∂y · (1 + ∂F/∂x)
```

看到那个 **+1** 没？它的意义是——**深层 loss 信号可以通过那个 +1 直接传到浅层**，不会被中间层的 `∂F/∂x` 完全吞掉。**残差连接给反向传播开了一条加法的高速公路**。

这就是为什么 ResNet 之后 152 层、1000 层都能训得动——不是因为"恒等映射保底"这种事后解释，而是因为**梯度路径被拉直了**。

ResNet 之后，152 层成了 ImageNet 2015 冠军，top-5 错误率降到 **3.57%**——首次低于人类水平。

> **我的判断**：ResNet 表面上是给 CNN 用的，但**残差连接这个机制后来被 Transformer 也用了**——你打开任何一篇 Transformer 的论文，都能看到 "Add & Norm" 那个标签，那个 "Add" 就是残差。它已经成为深度学习的**底层基础设施**，跨架构通用。**Transformer 之所以能堆 96 层、175B 参数训得动，靠的就是这个机制**。这告诉我一件事——**真正重要的创新往往不是一个具体架构，而是一个可以跨架构复用的机制**。

参考资料：

- **He et al. — Deep Residual Learning for Image Recognition** (CVPR 2016 Best Paper)
[https://arxiv.org/abs/1512.03385](https://arxiv.org/abs/1512.03385)

---

# 第二阶段：Transformer 范式的崛起（14 min，重点段）

> **核心 hook**：这是全场最重要的转折点。Transformer 的真正意义不是 attention 本身，是它打开了"工业化堆规模"这条路。本段是机制档的技术峰值——会写出 3 行公式骨架（attention / scaling law / SSM）。

![](images/Pasted%20image%2020260427001425.png)

进入第二阶段。

2017 年，Google 的几个研究员发了一篇论文，标题简单粗暴——**"Attention Is All You Need"**。这篇论文做了一件几乎"反潮流"的事——**完全抛弃 RNN 的循环结构和 CNN 的卷积结构，只用 attention 和前馈网络**。

> **小观点 1**：Transformer 解决了 RNN 和 CNN 各自的硬伤。

我们前面说，RNN 的两个痛点：① 串行计算，没法并行；② 长距离依赖会衰减。CNN 的痛点：感受野有限，看远距离信息要堆很多层。

Transformer 用 self-attention 一举解决了这些——**每个位置的输出由"看其他所有位置 + 计算相关性权重 + 加权求和"得到**。这意味着两件事：① 所有位置可以**并行**计算（GPU 满载）；② 任何两个位置都是**直接交互**（没有距离衰减）。

[节奏：进入 self-attention 机制段——这是全场技术深度的最高峰，要慢、要稳]

> **self-attention 内部到底在做什么**——讲清三件事：

**第一件，Q / K / V 三个角色**：每个位置同时扮演三个身份。

- **Query（Q）**：我作为这个位置，提出一个问题——"我想找什么样的信息？"
- **Key（K）**：每个位置举出一个牌子——"我能提供什么信息？"
- **Value（V）**：每个位置真正要给出去的内容

[投影：Q/K/V 角色示意图]

**第二件，公式骨架**——写出来：

```
Attention(Q, K, V) = softmax( QKᵀ / √d_k ) · V
```

三步看：

1. `QKᵀ` —— 把 Q 和每个 K 做点积，**得到一个相似度矩阵**——每对位置一个分数
2. `√d_k` —— 这个根号 d 是干嘛的？因为维度大的时候点积方差会很大，softmax 会"饱和"成 one-hot——**梯度直接消失**。除以 √d_k 让分数保持在合理范围，softmax 输出"软选择"而不是"硬选择"。**这是论文里专门讲的一个工程细节**（§3.2.1）。
3. `softmax(...) · V` —— 把上一步的相似度归一化成权重，对所有位置的 V 做加权和

**所以本质是什么？是一个"软查表"**——Q 提问、K 提供索引、V 提供内容，softmax 决定每个 V 的权重。

**第三件，multi-head + 位置编码**——这两个一句话带过：

- **Multi-head**：不是只查一次表，是同时从 8 个不同的角度查 8 次再拼起来——每个 head 学不同的关系（语法关系、语义关系、共指关系……）。
- **Positional encoding**：self-attention 自己看不出顺序——交换两个位置结果不变。所以要把"第几个位置"编码成一个向量加进 input embedding 里。**位置信息是外挂的**。

[节奏：进入 Transformer 整体架构段——重点回扣 ResNet]

> **小观点 1.5**：Transformer 的整体架构——为什么 GPT 系把 encoder 拿掉了？

原始 Transformer 是 **encoder–decoder** 结构（机器翻译用），但 GPT 系做了一个简化——**只保留 decoder + causal mask，把 encoder 拿掉**。

什么是 **causal mask**？训练时每个位置只能看到自己和左边的位置——**不许偷看未来**。这样做有什么好处？**next-token prediction 自带监督信号**——下一个词就是 label，**任何文本都是天然的训练数据**。这一下就把训练数据从"标注的语料"扩大到了"全互联网"。

[节奏：这里给一个伏笔回收]

还有一件事必须讲——**回扣阶段一的 ResNet**。你打开任何一篇 Transformer 的代码，每个 attention 块和每个 FFN 块的最后都有一行 "**Add & Norm**"——那个 "Add" 就是 ResNet 的残差连接。**Transformer 之所以能堆 96 层、175B 参数训得动，就是靠的阶段一讲的那个机制**。这是一个跨阶段的伏笔回收——**ResNet 不是 CNN 的局部技巧，是整个深度学习的底层基础设施**。

[节奏：这里停 1 秒，强调下一段]

> **小观点 2**：但 Transformer 的真正意义，不是 attention 本身。

attention 在 Transformer 之前就有了——2014 年 Bahdanau 在 RNN 翻译里就用了 attention。Transformer 的真正贡献，是**第一次让 AI 模型变成了"可以无限堆规模"的东西**。

为什么这件事重要？因为 RNN 没法做大——串行 + 梯度问题让它在某个规模之后边际收益递减。CNN 做大也有边际递减。*Transformer 一出来，"更大 = 更强" 变成了可工程化、可预测的事实*。

这就引出了第二个里程碑——**LLM 时代**。

![](images/Pasted%20image%2020260426233653.png)

[投影：scaling law 论文里的核心图，loss vs compute 的幂律曲线]

> **小观点 3**：LLM 时代发现了 AI 的"摩尔定律"——scaling law。

2020 年，OpenAI 发了一篇论文叫 "Scaling Laws for Neural Language Models"（Kaplan et al.）。这篇论文做了一件听起来很简单但影响巨大的事——**他们系统地测量了：模型参数（N）、训练数据（D）、训练算力（C）这三者和性能（loss L）之间的关系**。

[节奏：写公式骨架]

发现的结论是——**loss 和这三者呈幂律关系**：

```
L(N, D, C) ≈ A · N^(-α) + B · N^(-β) + L_∞
```

意思是：每多一个数量级算力，loss 下降一个固定的小台阶——**这是可预测的**。给我更多算力，我能告诉你模型会变多强。

[节奏：进入 Chinchilla 修正——这一段补准确性]

但 2022 年 DeepMind 发了一篇 **Chinchilla** 论文——把 Kaplan 的结论修正了一下。Kaplan 当时认为"算力主要应该堆给模型规模"，Chinchilla 说"**不对——模型规模和数据应该同步 scale**"。具体地——**模型每翻一倍，数据也应该翻一倍**。Chinchilla 用 70B 参数 + 1.4T tokens 训出来，把 GPT-3（175B）和 Megatron-Turing（530B）都打败了。

**这个修正的工程影响很大**——你看 2024 年的 Llama-3 70B 用 **15T token** 训练，就是 Chinchilla 比例的延续。

> **例子**：OpenAI 在 2020 年发布 GPT-3，1750 亿参数。当时所有人都被震惊——一个**通用**模型，不需要为每个任务专门训练，靠 prompt 就能做翻译、写代码、做问答、写诗。GPT-2 还做不到这些，GPT-3 突然就做到了。

[节奏：这里停 1.5 秒，引出"涌现"概念，并补一个修正]

而且更让人困惑的是——**当模型规模到一定程度时，会突然出现"涌现能力"**。某些任务在小模型上完全做不了，到一定规模突然就会了。比如多步推理、代码生成、in-context learning。

> **关于"涌现"的一个修正**——这是 NeurIPS 2023 Outstanding Paper 提出的：

Stanford 的 Schaeffer 等人在 2023 年发了一篇《Are Emergent Abilities of LLMs a Mirage?》——他们的论点是：**很多所谓"涌现"可能是评估指标不连续造成的假象**。如果你用 0/1 准确率（要么全对要么 0 分），就会看到"突然涌现"的曲线；但如果你用连续指标（token-level log-prob），就会看到平滑、可预测的提升。

我的态度——**不站队，但要知道这个修正存在**。"涌现"在科普语境里被讲得有点神秘，但学界本身还在争论它是真现象还是评估幻觉。我倾向于"两者都有一部分"，但这是个 open question。

> **小观点 4**：然后是 ChatGPT，2022 年 11 月。

ChatGPT 在技术上其实没有多少新东西——它是 GPT-3.5 加上 RLHF（人类反馈强化学习）。但它在**产品形态**上做对了一件事——**对话界面 + 对齐到人类偏好**。结果是 5 天突破 100 万用户，2 个月突破 1 亿用户，AI 第一次真正出圈。

![](images/Pasted%20image%2020260426231612.png)
[投影：Transformer vs Mamba 对比图，O(n²) vs O(n)]

> **小观点 5**：但讲到 2026 年的 Transformer，我必须提一个变化——**它不再是唯一的选择**。

2023 年开始，**Mamba 这个基于状态空间模型（SSM）的新架构**慢慢起来。它的核心 selling point 是**线性复杂度 O(n) + 常数显存**——这恰好命中了 Transformer 最大的痛点：序列长了 attention 就吃不消（O(n²)）。

[节奏：写第二个公式骨架——SSM]

> **SSM 内部在做什么**——写一行公式：

```
h_t = A · h_{t-1} + B · x_t      （状态更新）
y_t = C · h_t                     （输出）
```

这就是经典控制论里的**状态空间模型**——每一步只更新一个固定大小的隐状态 h，**不需要回看历史**——所以是 O(n) 的。**RNN 是它的特殊情况**——Mamba 本质是把 60 年代控制论的工具搬到了深度学习。

**Mamba 的关键创新——selective SSM**：让 **B、C、Δ 三个参数随输入动态变化**（Δ 是把连续时间 SSM 离散化的步长）。A 矩阵保持固定（HiPPO 初始化）。这让模型能根据当前 token 的语义内容**决定保留还是丢弃信息**——类似 attention 的"软选择"，但**保留了 O(n) 复杂度**。

2026 年 3 月 **Mamba-3** 出来——在 1.5B 规模上，准确率超过 Mamba-2 接近 2 个百分点，state size 减半，**专门为推理优化**。

但有意思的是——**业界共识是 Mamba 不会取代 Transformer，而是补足**。

- **Attention** 是软查表——精确但 O(n²)
- **SSM** 是状态压缩——高效但有损

Transformer 强在推理、in-context learning、精确检索；Mamba 强在长序列、推理速度、显存效率。所以我们看到越来越多 **hybrid 架构**——某些层用 Transformer，某些层用 Mamba。

![](images/Pasted%20image%2020260426230517.png)
[投影：scaling law 论文里的核心图，loss vs compute 的幂律曲线]

> **小观点 6**：再讲到 2026 年的 LLM 一线模型——它们已经走到了一个新的拐点。

时间线先理清楚：**GPT-5 本体 2025.08.07 发布**（首次内置 thinking + 通用模型），之后是 GPT-5.1 / 5.3 / **5.4（2026.03）**；**Gemini 3.1 Pro（2026.02.19）**；**Claude Opus 4.7（3 天前，2026.04.16）**。

这些模型有一个共同特征——**它们不再主要靠"模型变大"来提升性能，而是靠"思考机制变深"**。

具体表现：

- **Gemini 3.1 Pro**：1M 输入 / 64K 输出上下文，**ARC-AGI-2 拿到 77.1%**（推理 benchmark 难度比 GPQA 高得多，是当前最硬的指标之一）
- **GPT-5.4**：1M 上下文 + 原生电脑使用能力（OSWorld 75%），更高效的 reasoning
- **Claude Opus 4.7**：复杂长程编码任务的 **verification 机制**——模型能自己检查输出再上报，软件工程能力大幅提升

[节奏：这里停 1 秒，进入国内副线——这一段是稿件的重要补充]

> **小观点 7**：但讲 LLM 不能只讲三大厂——国内的进展同样在 frontier 水平。

[投影：国内 LLM 时间线（2025–2026）：Qwen3 / GLM-4.6 / Kimi K2.5 / DeepSeek V3.x]

我特别想把国内的几条线列出来，因为今天群里我们做的就是中国的产品：

- **Qwen 系列（阿里）**：**Qwen3（2025.04 起）**全家族开源（0.6B 到 235B MoE）+ 混合推理模式；**Qwen3-Max（2025.10）**1 万亿参数 / SWE-Bench 69.6% / Tau2-Bench 74.8%，超过 Claude Opus 4 和 DeepSeek V3.1；**Qwen3.5 Omni（2026.03）**原生多模态（文本+音频+视频+实时交互），256K 上下文
- **GLM 系列（智谱）**：**GLM-4.6（2025.09）**——355B MoE / 32B 激活，200K 上下文，**LMArena 排第 4**（国内并列第一），代码能力对标 Claude Sonnet 4
- **Kimi 系列（Moonshot）**：**Kimi K2（2025.07）**1T MoE 开源（Apache 2.0），**Kimi K2.5（2026.01.27）升级版——1T MoE / 32B 激活 / 256K 上下文，最大亮点是"self-directed agent swarm"——可以调度 100 个 sub-agent 并行 + 1500 个工具调用同时执行，速度比单 agent 快 4.5 倍。在 agent benchmark 上超过 GPT-5.2 / Claude 4.5 Opus / Gemini 3 Pro**

> **我的判断**：国内 LLM 的策略已经从"追赶"变成"在某些维度领先"——Qwen 走 scaling + 全家族开源路线，GLM 走"小尺寸高性能 + 国产芯片适配"，Kimi 直接押 agent 路线。**三家选了三种不同的差异化打法**——这比单纯"做一个对标 GPT 的模型"格局高。

> **我的判断（小结）**：第二阶段最颠覆性的，不是 AI 学会了写代码或者聊天——**是它告诉我们：通用能力可以靠堆规模获得，而不必靠精巧的算法设计**。这把 AI 从"科学"变成了"工程"。从"怎么设计聪明的模型"变成"怎么准备更多数据、怎么用好更大算力、怎么训得更稳"。这是 AI 进入**工业化时代**的起点。

但 2026 年这个故事正在出现新变化——**架构开始"分化"**（Transformer + Mamba 各占生态位），**scaling 范式开始"换腿"**（从模型规模 scaling 转向推理 compute scaling），**而且 frontier 不再被三大厂垄断**——中国的 Qwen / GLM / Kimi / DeepSeek 已经在多个维度站到一线。AI 工业化已经到了"全球分布、精细化分工"的阶段。

参考资料：

- **Jay Alammar — The Illustrated Transformer**
[https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/)
- **Vaswani et al. — Attention Is All You Need** (NeurIPS 2017)
[https://arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- **Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out**
[https://www.youtube.com/watch?v=kCc8FmEb1nY](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- **Kaplan et al. — Scaling Laws for Neural Language Models** (OpenAI 2020)
[https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361)
- **Hoffmann et al. — Training Compute-Optimal LLMs (Chinchilla)** (DeepMind 2022)
[https://arxiv.org/abs/2203.15556](https://arxiv.org/abs/2203.15556)
- **Wei et al. — Emergent Abilities of Large Language Models** (2022)
[https://arxiv.org/abs/2206.07682](https://arxiv.org/abs/2206.07682)
- **Schaeffer et al. — Are Emergent Abilities of LLMs a Mirage?** (NeurIPS 2023 Outstanding Paper)
[https://arxiv.org/abs/2304.15004](https://arxiv.org/abs/2304.15004)
- **Gu & Dao — Mamba: Linear-Time Sequence Modeling with Selective State Spaces** (2023)
[https://arxiv.org/abs/2312.00752](https://arxiv.org/abs/2312.00752)
- **Anthropic — Introducing Claude Opus 4.7**
[https://www.anthropic.com/news/claude-opus-4-7](https://www.anthropic.com/news/claude-opus-4-7)
- **Google — Gemini 3.1 Pro 官方博客** (2026.02.19)
[https://deepmind.google/blog/gemini-3-1-pro-a-smarter-model-for-your-most-complex-tasks/](https://deepmind.google/blog/gemini-3-1-pro-a-smarter-model-for-your-most-complex-tasks/)
- **OpenAI — Introducing GPT-5** (2025.08.07)
[https://openai.com/index/introducing-gpt-5/](https://openai.com/index/introducing-gpt-5/)
- **OpenAI — Introducing GPT-5.4** 
[https://openai.com/index/introducing-gpt-5-4/](https://openai.com/index/introducing-gpt-5-4/)
- **Alibaba Qwen3-Max 官方介绍** (2025.10)
[https://www.alibabacloud.com/blog/602621](https://www.alibabacloud.com/blog/602621)
- **Alibaba Qwen3.5 Omni** (2026.03)
  [https://www.marktechpost.com/2026/03/30/alibaba-qwen-team-releases-qwen3-5-omni-a-native-multimodal-model-for-text-audio-video-and-realtime-interaction/](https://www.marktechpost.com/2026/03/30/alibaba-qwen-team-releases-qwen3-5-omni-a-native-multimodal-model-for-text-audio-video-and-realtime-interaction/)
- **Zhipu AI GLM-4.6** (2025.09.30)
[https://baike.baidu.com/en/item/GLM-4.6/1428092](https://baike.baidu.com/en/item/GLM-4.6/1428092)
- **Moonshot Kimi K2.5 官方** (2026.01.27) 
- GitHub: [https://github.com/MoonshotAI/Kimi-K2.5](https://github.com/MoonshotAI/Kimi-K2.5)
- 详细解读: [https://llm-stats.com/blog/research/kimi-k2-5-launch](https://llm-stats.com/blog/research/kimi-k2-5-launch)
- **Moonshot Kimi K2** (2025.07，K2.5 的前身)
  [https://www.marktechpost.com/2025/07/11/moonshot-ai-releases-kimi-k2-a-trillion-parameter-moe-model-focused-on-long-context-code-reasoning-and-agentic-behavior/](https://www.marktechpost.com/2025/07/11/moonshot-ai-releases-kimi-k2-a-trillion-parameter-moe-model-focused-on-long-context-code-reasoning-and-agentic-behavior/)

---

# 第三阶段：生成式 AI 的爆发（12 min）

> **核心 hook**：AI 从"判别器"走向"创造者"。Diffusion 是真正可用的生成式 AI 起点，VLM 把视觉和语言打通。本段会讲清 Diffusion 为什么稳、CLIP 怎么训、两者怎么合体造 text-to-image。会写出 1 行公式骨架（DDPM L_simple）。

![](images/Pasted%20image%2020260426225331.png)
[投影：Stable Diffusion 生成的几张图 + DALL-E 2 / Midjourney 对比]

进入第三阶段。

> **小观点 1**：Diffusion 让生成式 AI 第一次"真正可用"。

在 Diffusion 之前，生成式 AI 一直处在"demo 很惊艳但实际没用"的阶段。

[节奏：把 GAN/VAE 失败的真正机制讲清楚，不是只列结论]

> **GAN 和 VAE 各自的失败到底在哪**——讲清两件事：

**GAN（2014）训练不稳定的根**：min-max 博弈——生成器 G 和判别器 D 互相对抗，**没有单一的 loss 在下降**。如果 D 训得太快，G 拿不到有用梯度；G 训得太快，D 又跟不上。**工程上极难判断收敛**——这是 GAN 在 2014–2020 年一直没真正可用的根本原因。

**VAE 生成模糊的根**：reconstruction loss 用 L2——而 L2 本质上对应**高斯分布假设（单峰）**。但图像的真实分布是**多峰的**——一只猫可以是橘色、黑色、白色，强行用 L2 就是在做平均，**平均出来的就是糊的**。

**Autoregressive（PixelRNN/PixelCNN）**则太慢——一个像素一个像素生成，1024×1024 图要生成 100 万次。

Diffusion 用一个**反直觉**的思路解决了这两边的痛点——

[节奏：这里语气慢一点，因为要讲反直觉的概念]

**它不直接学"怎么生成图像"——它学"怎么去噪声"**。

具体来说：

- **Forward process（不学，固定的）**：把清晰图像 x_0 逐步加噪声，最后变成纯随机噪声 x_T。重要的是——**任意一步 t 都可以从 x_0 一步采样到**：

  ```
  x_t = √ᾱ_t · x_0 + √(1 - ᾱ_t) · ε     ε ~ N(0, I)
  ```

  其中 ᾱ_t 是从 0 到 t 的 α 累积积。**这意味着训练时不需要真的跑 1000 步**，可以并行采样任意 t——这是 diffusion 训练能 scale 的关键。

- **Reverse process（要学）**：网络输入 (x_t, t)，输出**对加进去的噪声 ε 的估计** ε_θ(x_t, t)。

[节奏：这里写出第二个公式骨架——DDPM 的训练目标]

> **DDPM 的训练目标极简**——一行公式：

```
L_simple = E[ ‖ ε - ε_θ(x_t, t) ‖² ]
```

**就是个 L2 回归**——预测加进去的噪声是什么。

**讲三件事**：

1. **极简的训练目标**——L2 回归，没有对抗博弈，没有 ELBO 推导（虽然论文里有）。**实际工程上，你只需要这一行**。
2. **为什么预测 ε 不预测 x_0**？DDPM 论文里两种参数化都试过——**预测噪声 ε 训练更稳、loss 更平滑**。这是工程发现，不是数学必然。
3. **为什么稳**？每一步只学一个**小的噪声差**，没有 GAN 的 min-max 博弈，也没有 VAE 的单峰分布假设——**两边的痛点同时被绕开**。

> **采样加速**：DDPM 训练时是 1000 步，推理时也要 1000 步——慢。**DDIM (Song et al. 2021)** 把采样过程从 SDE 重写成 ODE，可以**跳步采样**——20–50 步达到 1000 步同等质量。这是 Stable Diffusion 能在消费级 GPU 上 5 秒出图的工程基础。

> **Latent Diffusion——SD 工业落地的真正机制核心**：

Stable Diffusion 不是直接在 512×512 像素空间扩散——**它先用 VAE 把 512×512 RGB 压到 64×64 latent，在 latent 空间扩散，最后再 VAE decode 回 512×512**。

为什么？**计算量降一个数量级**——512×512×3 ≈ 79 万维 vs 64×64×4 ≈ 1.6 万维。这是 Rombach 2022 那篇 CVPR 论文的核心贡献，也是 Stable Diffusion 能开源跑起来的真正原因。

> **例子**：DDPM 论文（2020）出来之后两年内，DALL-E 2（2022.04）+ Stable Diffusion（2022.08，**开源**）+ Midjourney 全面爆发。Stable Diffusion 开源这件事尤其关键——它让普通人在家用一张消费级 GPU 就能跑 image generation，整个开源社区一夜之间起飞。

> **小观点 2**：VLM 让 AI 第一次有了"看到 + 理解 + 描述"的闭环。
![](images/Pasted%20image%2020260426220616.png)

VLM 的起点是 CLIP，2021 年 OpenAI 发的。CLIP 做了一件极简的事——**用 4 亿对（图像，文本描述）做对比学习，把图像和文本对齐到同一个语义空间**。

[节奏：进入 CLIP 对比学习机制段]

> **CLIP 对比学习内部在做什么**——讲清三件事：

**第一件，训练设置**：

- 一个 batch 里 N 对（图，文）—— 比如 N = 32K
- 把每张图过 image encoder（ViT 或 ResNet）→ 图像向量；每段文本过 text encoder（Transformer）→ 文本向量
- 把所有图像向量和所有文本向量**两两算余弦相似度**——得到一个 N×N 的相似度矩阵

**第二件，InfoNCE loss 的直觉**（不写公式）：

- 这个 N×N 矩阵的**对角线**是真正的 (图_i, 文_i) 配对
- 训练目标：**让对角线相似度最大，让其他 N²−N 个错配对相似度最小**
- 本质是个 **N 选 1 分类**——给定一张图，从 N 段文本里挑出真正配对的那一段

**第三件，为什么 4 亿对数据是关键**？对比学习的负样本质量决定一切——你能从 4 亿对里挑出多难的负样本，模型就能学到多细的语义区分。**数据规模本身就是模型质量**。

什么意思？训练完之后，"一张猫的图片" 的向量和 "a photo of a cat" 这串文字的向量，**在 embedding 空间里非常接近**。一张狗的图和 "a photo of a dog" 也接近。但猫的图和狗的描述，向量距离就远。

这件事的影响有多大？

- **零样本图像分类**：把 ImageNet 的 1000 个类名变成 "a photo of a {class}" 的句子，全部编码后和图像比相似度——**不用任何 ImageNet 训练数据**，CLIP 就能在原始 ImageNet validation 上达到**和监督训练的 ResNet-50 持平**的准确率。这件事在 2021 年是震撼的——一个**完全没在 ImageNet 上训过的模型**，直接和 ImageNet 上训出来的标杆持平。
- **DALL-E 2 / Stable Diffusion 的 text encoder 都是 CLIP**——你输入的 prompt 怎么变成图像？通过 CLIP 把文字编码成向量，再 condition diffusion 模型去生成对应的图。
- **GPT-4V、Qwen-VL、LLaVA 这些"看图说话"模型**——本质上都是在 CLIP 范式上叠加 LLM。

[节奏：进入 Diffusion + CLIP 合体段——这是阶段三的高潮]

> **小观点 3**：Diffusion 和 CLIP 合体——text-to-image 是怎么做的。

DALL-E 2、Stable Diffusion 这些产品，从用户输入 prompt 到出图，内部流程拆开来是这样的：

1. 用户输入文字 prompt（比如 "an astronaut riding a horse"）
2. **CLIP text encoder** 把 prompt 编码成向量——VLM 在这里发挥作用
3. 这个向量作为 **condition** 注入到 diffusion U-Net 的每一层——**通过 cross-attention 实现**（U-Net 看图像 latent 是 query，看 CLIP embedding 是 key/value）
4. Diffusion 反向去噪，每一步都参考这个 condition——**生成一张和文字描述匹配的图**

> **关键洞见**：**Diffusion 提供生成能力，CLIP 提供语义理解，两者通过 cross-attention 耦合**——这是第一次**两个独立技术线合体造出了"听懂人话画图"的产品**。这个 pattern 后来被复用到 ControlNet（加深度图条件）、视频生成（加时间一致性）、3D 生成等等。

> **Classifier-free guidance 一句话**——Stable Diffusion 用户都见过的那个 "CFG scale 7.5" 参数，机制由来：训练时**随机 drop 掉 condition**（比如 10% 概率不给文本），让模型同时学会"有条件"和"无条件"两种生成。推理时通过 `ε_cond - ε_uncond` 的差值放大条件强度——**CFG scale 越高，越严格按文本生成；越低，越自由**。

[节奏：这里抛个连接]

> **小观点 4**：到 GPT-4V（2023.09）发布的时候，AI 第一次能"看懂"用户发的图并回答问题。

> **我的判断（小结）**：第三阶段的关键词是**"打通"**。Diffusion 打通了"AI 不只是判别器，也能是创造者"——而且是**第一次稳定可训练的生成式范式**；VLM 打通了"视觉和语言不再是两条独立的研究线"。这两个打通合起来，意味着——**AI 开始有了"类人的"创造和理解能力**。也正是从这里开始，AI 真正进入了大众视野。

参考资料：

- **Lilian Weng — What are Diffusion Models?**
[https://lilianweng.github.io/posts/2021-07-11-diffusion-models/](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
  - **业内公认 Diffusion 最佳综述**，英文原文，OpenAI 研究员写
- **Ho et al. — Denoising Diffusion Probabilistic Models** (DDPM, NeurIPS 2020)
[https://arxiv.org/abs/2006.11239](https://arxiv.org/abs/2006.11239)
- **Song et al. — Denoising Diffusion Implicit Models (DDIM)** (ICLR 2021)
[https://arxiv.org/abs/2010.02502](https://arxiv.org/abs/2010.02502)
- **Rombach et al. — High-Resolution Image Synthesis with Latent Diffusion Models** (CVPR 2022, Stable Diffusion 论文)
[https://arxiv.org/abs/2112.10752](https://arxiv.org/abs/2112.10752)
- **Ho & Salimans — Classifier-Free Diffusion Guidance** (2022)
[https://arxiv.org/abs/2207.12598](https://arxiv.org/abs/2207.12598)
- **Radford et al. — Learning Transferable Visual Models From Natural Language Supervision** (CLIP, 2021)
[https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- **OpenAI Blog — CLIP: Connecting Text and Images**
  [https://openai.com/research/clip](https://openai.com/research/clip)

---

# 第四阶段：走向世界模型与具身——起源篇（10 min）

> **核心 hook**：World Models 这个概念 2018 年就有了，但停在玩具任务上。GEN-1 代表 diffusion 走向视频生成。这两个方向都在为下一个时代铺路。本段会写出 1 行函数签名（V+M+C 的 controller）；JEPA 之争一段是为下次分享留的钩子。

![](images/Pasted%20image%2020260426205929.png)
[投影：David Ha 2018 年 World Models 论文里的 CarRacing 截图]

进入第四阶段。

> **小观点 1**：World Models 是一个 2018 年就提出、但停留了 6 年的概念。

2018 年，David Ha 和 Jürgen Schmidhuber 发了一篇论文，标题就叫 **"World Models"**。核心思想是——**让 AI 在内部建立一个"世界的模拟器"，agent 可以在这个模拟器里想象、规划、推演**，而不是只在真实世界试错。

[节奏：进入 V+M+C 机制段——三件事讲清]

> **V + M + C 三件事讲清架构怎么 work**：

**V (Vision，VAE)**：把每一帧 64×64 RGB 图像（≈12K 维像素）通过卷积 VAE **压到 32 维 latent z**。这一步把"高维像素世界"变成"低维状态向量"——**为后面所有事铺路**。

**M (Memory，MDN-RNN)**：输入当前 latent z_t 和动作 a_t，输出 **下一帧 latent 的概率分布** P(z_{t+1} | z_t, a_t, h_t)。**关键是输出分布而不是单值**——因为现实世界本身有不确定性（混合密度网络 MDN 就是输出多个高斯分布的混合）。这是 LeCun 后来反复强调的一个点——**预测未来必须输出分布，不能输出单点**。

**C (Controller)**：输入是 (z_t, h_t)，输出动作 a_t。函数签名写出来：

```
C : (z_t, h_t) → a_t
```

这是个**很小的线性策略**（参数只有几百个）。训练用 **CMA-ES 演化算法**——不是反向传播，因为 C 太小了，演化算法反而比 SGD 更高效。

> **"在梦里训练"的真实含义**：

1. 先用真实环境收集 rollout 数据 → 训 V 和 M
2. **抛开真实环境**，让 M 自己生成 latent 序列（就像在做梦）→ 在 M 模拟出来的"梦境"里训 C
3. 训完的 C 放回真实环境——**zero-shot 跑通 CarRacing-v0**，分数从 632 提升到 906

**这是 2018 年最反直觉的结果**——一个 agent 在自己想象出来的世界里训练，居然能在真实环境里 work。

[节奏：转到"为什么没 scale 6 年"——这是为下次分享留的钩子]

> **为什么 World Models 这个想法停留了 6 年**？

**规模太小**：V 是个小 VAE，M 是个 LSTM，整个模型加起来 < 10M 参数。32 维 latent 表达力太有限——CarRacing 这种几何简单的任务能用，换个稍微复杂一点的环境（连 Atari 游戏都不太行）画质就跟不上。

**它需要等三件事**：① 大模型基础设施（Transformer + 大算力）；② 大规模视频数据；③ 高质量的 latent 表达（VQ-VAE / 扩散 latent）。

这三件事在 **2024–2025 年才全部齐备**。所以 world models 的真正爆发——Genie 3（2025.08）、NVIDIA Cosmos（2025.01）、GR00T N1.6（2026.04）——**都集中在最近 12 个月**。

**今天我不展开这些**——它们是下次分享的核心。但你记住这条线：**2018 年 V+M+C 是种子，2025–2026 是发芽**。

[节奏：进入 JEPA 之争——为下次留钩子]

> **小观点 1.5**：但讲 World Models 起源就绕不开 LeCun 这条线——这是 AI 领域一条重要的路线分歧。

**LLM 自回归路线的本质**——模型学的是 `P(x_t | x_<t)`：给定历史 token，预测下一个 token。GPT 系所有模型都是这个范式。

**LeCun 反对这条路**，理由是两点：

1. **像素/token 空间预测会强迫模型预测所有细节**——包括无意义的细节（背景纹理、毛发方向）。**这浪费容量**——模型把大量能力花在"画出每一根毛"上，而不是花在"理解世界动力学"上。
2. **现实世界的下一刻本质上不可完美预测**（多峰分布）——下一秒车可能左转也可能右转。强制单点预测会导致"预测的平均"——**模糊或回避**，而不是真正的世界理解。

**LeCun 提的 JEPA 路线是怎么解的**？把 x 和 y（"现在"和"未来"）都过一个 encoder，得到 `s_x`、`s_y`。学的是 `Pred(s_x) ≈ s_y`——**在表示空间里预测，不是像素级预测**。配合 VICReg / I-JEPA / V-JEPA 这套非对比学习——避免 collapse（所有 s 都变成同一个向量）。

**直觉对比**：**LLM 是预测下一个词，JEPA 是预测下一个"抽象状态"**——前者细节准、后者懂动力学。

> **现状（坦诚的钩子）**：

JEPA 路线 LeCun 2022 年提出，I-JEPA 2023 出来，V-JEPA 2024 出来——**至今没有 GPT 量级的爆点产品**，但概念吸引力很强。

我对这场争论的态度——**不站队**。两件事我能确定：

1. JEPA 这条路 2025–2026 在落地——**Genie 3 / NVIDIA Cosmos / GR00T N1.6 其实都是这条思路的某种变体**（在抽象状态上预测，而不是直接预测像素）
2. LLM 自回归路线**也没撞墙**——推理大模型（o1 / R1）让它继续涨

**这两条路最后会汇合还是替代——是 AI 领域当前最大的 open question**。下次分享我会展开讲这个汇合在 2025–2026 已经发生到了什么程度。

> **小观点 2**：GEN-1 代表了 diffusion 范式从图像走向视频。

![](images/Pasted%20image%2020260426214738.png)
[投影：GEN-1 / GEN-2 视频 demo 截图]

GEN-1 是 Runway 2023 年 2 月发布的模型，论文发在 ICCV 2023——**第一个把 diffusion 思路系统地用到视频生成的工业级产品**。

[节奏：进入 GEN-1 时间一致性机制段]

> **视频生成 vs 图像生成的核心难点 = 时间一致性**：

**同一个物体在第 t 帧和第 t+1 帧应该是同一个物体**——颜色、形状、纹理不能漂。这件事在 GEN-1 之前没有好解法。

**GEN-1 的解法（Esser et al. ICCV 2023）**——三件事：

1. **Structure / Content 解耦**：从输入视频提取**深度图（用 MiDaS）**作为 structure（保证几何一致性），文本/参考图通过 **CLIP embedding** 作为 content（控制风格、外观）。这样几何和外观分离开。

2. **Temporal layer 插入**：在原本的 image diffusion U-Net 里，**每个 spatial attention 之后插入一个 temporal attention 层**——让每一帧能"看到"相邻帧。**直觉：把 2D U-Net "拉伸" 成 3D**——空间维度由原本的 image diffusion 处理，时间维度由新加的 temporal attention 处理。

3. **微调而不是从头训**：基于已经训好的 image diffusion 模型，只训 temporal 层 + structure encoder——**这是 GEN-1 能在合理算力下跑出来的工程关键**。

> **为什么是工程突破而不是机制突破**？每一块都是已有技术（diffusion + attention + 深度图条件 + CLIP embedding）——**新意在组合方式**。"工程化 = 把已有零件以正确方式组合起来跑通 SaaS 产品"——这是 GEN-1 的真正价值。

而且 Runway 把它做成了 SaaS 产品，让非技术用户也能用——这是 AI 商业化的早期代表案例。

> **现状对照**：今天（2026.04）的 Sora（2024.02）/ Veo（2024.05）/ Veo 3（2026）都是这条路线的工业化版本——**核心机制（Structure-Content 分解 + temporal attention + 微调）没本质变化，只是规模和数据量大了几个数量级**。GEN-1 当时的方法论今天还在用。

> **我的判断（小结）**：第四阶段的两个节点很有意思——一个（World Models）是"概念领先实践很多年"的代表，一个（GEN-1）是"工程落地推动技术普及"的代表。它们都不是当时的"最强技术"，但**它们指出了下一个阶段会爆发的方向**。

**今天我讲到这里**。下一次分享我会展开 3 件事——**推理大模型怎么让 AI 学会"慢思考"、VLA 怎么让 AI 走出屏幕、World Models 怎么从今天讲的 V+M+C 一路走到 Genie 3 和 GR00T**。**这就是把今晚埋下的种子全部展开**。

[节奏：在这里停 2 秒，自然过渡到收尾]

参考资料：

- **Ha & Schmidhuber — World Models** (NeurIPS 2018)
[https://arxiv.org/abs/1803.10122](https://arxiv.org/abs/1803.10122)
- **World Models 交互式博客**（强烈推荐）
[https://worldmodels.github.io/](https://worldmodels.github.io/)
- **LeCun — A Path Towards Autonomous Machine Intelligence** (JEPA 路线提出文, 2022)
[https://openreview.net/pdf?id=BZ5a1r-kVsf](https://openreview.net/pdf?id=BZ5a1r-kVsf)
- **Assran et al. — I-JEPA** (CVPR 2023)
[https://arxiv.org/abs/2301.08243](https://arxiv.org/abs/2301.08243)
- **Bardes et al. — V-JEPA** (Meta 2024.02)
[https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)
- **Bardes / Ponce / LeCun — VICReg** (ICLR 2022)
[https://arxiv.org/abs/2105.04906](https://arxiv.org/abs/2105.04906)
- **Esser et al. — Structure and Content-Guided Video Synthesis with Diffusion Models** (Runway GEN-1, ICCV 2023)
[https://openaccess.thecvf.com/content/ICCV2023/papers/Esser_Structure_and_Content-Guided_Video_Synthesis_with_Diffusion_Models_ICCV_2023_paper.pdf](https://openaccess.thecvf.com/content/ICCV2023/papers/Esser_Structure_and_Content-Guided_Video_Synthesis_with_Diffusion_Models_ICCV_2023_paper.pdf)
- **Runway Research — Gen-1 / Gen-2 / Gen-3 Pages**
[https://research.runwayml.com/gen2](https://research.runwayml.com/gen2)

---

<!--
  以下"延伸段"完整保留，本场（50 min 主线）不讲，留待下次分享展开。
  保留目的：① 现场被追问时可临时拉某一段（参见"情况 3"应对）
            ② 下次分享直接复用
            ③ 收尾段提到这 3 个名词时可快速翻到这里查事实
-->

# [⏭️ 下次分享内容 · 本场不讲] 延伸段：2023 之后的关键进展（9 min）

> ⚠️ **本段不在本场（2026.04.24）的 50 min 主线中**——4 个老阶段已经是 12 年的故事，3 个新方向（推理大模型 / 具身 VLA / World Models 突破）留到下次分享。**本段全部内容仍然准确并已通过事实核查**，可以放心使用。

> **过渡话术**

[投影：时间轴，2023.02 GEN-1 之后留白，然后用箭头指向 2024-2026]

刚才讲的 8 个节点——曹姐原来给的列表——里面**最新的就是 2023 年 2 月的 GEN-1**，到今天 3 年多。AI 这 3 年发生的事不少。所以我特别选了**3 个 2024–2026 的方向补进来**，它们分别是：**推理大模型、具身 VLA、World Models 的真正突破**。

我没选另外两个大家可能也想到的方向——**多模态原生大模型**（GPT-4o/Gemini 2.0）和**视频生成的飞跃**（Sora/Veo 3/可灵 2）。**不是它们不重要**，是因为我今天选这 3 个的判断标准是——**它们之间有一条暗线，最后会汇成一件事**。这条暗线最后会揭。

---

## 延伸 1：推理大模型（2.5 min）



[投影：OpenAI o1 论文里的 test-time compute scaling 曲线]

> **小观点**：推理大模型发现了 LLM 的**第二条 scaling law**。

**时间线**：OpenAI **o1-preview（2024.09.12）**首次提出"内置推理"范式 → **o3-preview（2024.12.20）**在 ARC-AGI-1 上拿到 87.5% 震惊业界 → **o3 正式发布（2025.04.16）+ o3-pro（2025.06.10）**进入产品级 → 2025-2026 整个 OpenAI 路线都围绕 reasoning。它和之前所有 LLM 最大的不同——**它在回答问题之前，会先在内部生成一长串推理过程（chain-of-thought），然后再给答案**。

这件事的颠覆性在哪里？

我们前面讲第二阶段的时候说，scaling law 告诉我们——**模型大就强**。这是**预训练 scaling**：用更多算力、更多数据训练更大的模型。

o1 发现了一件新事——**推理 scaling**：让模型在回答前**想得更久**，性能继续涨。OpenAI 论文里那张图非常震撼——**给模型 1 秒、10 秒、100 秒思考时间，AIME 数学竞赛通过率持续上升**。GPT-4o 在 AIME 上 13%，o1 直接到 83%。

> **例子**：2025 年 1 月，DeepSeek 开源了 R1 模型——性能对标 o1，**成本显著低于 OpenAI**，而且公开了完整的训练 pipeline。这件事对开源社区是一次震动——一个之前 OpenAI 完全闭源垄断的方向，几个月内就被开源追平。

而到了 2026 年，**国内的开源推理模型已经做到三种不同的极端**：

- **DeepSeek R2（2026.04，这周）**——和 2025 年盛传的"670B MoE"完全不一样，实际是 **32B dense transformer**，**单张 24GB 消费级 GPU（如 RTX 4090）就能跑**，AIME 2025 拿到 92.7%，128K 上下文，MIT license。**走的是"小而精 + 后训练优化"路线**。
- **Kimi K2.5（2026.01.27）**——1T MoE / 32B 激活 / 256K 上下文，但真正的差异化是**"self-directed agent swarm"**：可以**自动调度 100 个 sub-agent 并行 + 1500 个工具调用同时执行**，速度比单 agent 快 4.5 倍。在 agent benchmark 上**超过 GPT-5.2 / Claude 4.5 Opus / Gemini 3 Pro**。**走的是"agent 化 + 并行编排"路线**。
- **Qwen3-Max-Thinking（2025.10）**——1 万亿参数 / 36T tokens 训练，**配合 tool use + 推理 compute scaling 在 AIME 25 / HMMT 上拿到 100%**。**走的是"超大模型 + 推理 scaling"路线**。

[节奏：这里停 1 秒，对比一下三家的判断]

**当前最强的单模型 SOTA 仍是 OpenAI o3 系列**（o3-pro 2025.06，MATH-500 98.1% / SWE-bench 61.5%），但**开源已经在 2026 年把"推理能力 + 可部署性"的组合做到了 frontier 水平**——而且**这件事主要是中国团队在推进**。

> **我的判断**：推理大模型最颠覆的不是它能解奥数——是它**为 AI 能力增长打开了第二条腿**。预训练 scaling 让 AI 在 2020-2024 年涨了一波；推理 scaling 让 AI 在 2024 年起又能继续涨。**这是 LLM 演进的根本性新维度**。
>
> 而且 2026 年还有一个让我感受很深的事——**Kimi K2.5 的 agent swarm 路线、DeepSeek R2 的小模型 + 后训练路线、Qwen3-Max 的 1T 参数 + 推理 scaling 路线**——三家中国团队选了三种完全不同的差异化打法。**护城河已经从"模型本身"转移到了：数据飞轮 / 后训练工艺 / agent 编排 / 部署生态 / 应用场景**。模型规模本身不再是壁垒。

参考资料：

- 1. **OpenAI — Learning to Reason with LLMs** (o1 官方介绍, 2024.09)
  [https://openai.com/index/learning-to-reason-with-llms/](https://openai.com/index/learning-to-reason-with-llms/)
- **DeepSeek-AI — DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning** (2025.01)
  [https://arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948)
- **DeepSeek-R2 解读** (decodethefuture, 2026.04)
[https://decodethefuture.org/en/deepseek-r2-explained/](https://decodethefuture.org/en/deepseek-r2-explained/)

1. **Reasoning Models Roundup 2026** (CrazyRouter)
  [https://crazyrouter.com/en/blog/openai-o3-vs-deepseek-r2-vs-kimi-k2-reasoning-models](https://crazyrouter.com/en/blog/openai-o3-vs-deepseek-r2-vs-kimi-k2-reasoning-models)

---

## 延伸 2：具身 VLA（4 min，重点段）


[投影：Figure 02 / Pi-0 / GR00T 几个机器人的演示截图拼图]

> **小观点 1**：VLA 让 AI 第一次走出了屏幕。

VLA = Vision + Language + Action。在我们前面讲的 VLM（看图 + 理解语言）基础上，加上**动作输出**——**模型直接生成机器人控制指令**。

为什么这件事重要？因为在 VLA 之前，**所有 AI 都活在数字世界里**——文本、图像、视频，输出的都是 token 或像素。VLA 让 AI 第一次**直接输出动作**，和物理世界形成闭环。

> **例子（按时间线）**：
>
> - **2023.07** Google DeepMind RT-2 —— VLA 开山之作
> - **2024.10** Physical Intelligence π₀ —— 首个真正"通用基础模型"级 VLA，跨多种机器人形态
> - **2025.02** Figure AI Helix —— 第一个全上半身控制 VLA + 双机协作 + 嵌入式低功耗 GPU 部署
> - **2025.03** NVIDIA GR00T N1 —— 首个开源人形机器人 foundation model（双系统架构：VLM 推理 + Diffusion Transformer 动作）
> - **2025.06** GR00T N1.5 —— 加入 FLARE 目标（Future Latent Representation Alignment），可以从人类视频学习
> - **2025.10** **Figure 03 硬件** —— 第三代人形机器人，掌内嵌摄像头 + 触觉传感器（3 克级别力感知），为大规模量产设计
> - **2026.01** **Figure Helix 02** —— **3 个月前刚发布**。三级层级架构（System 0 / 1 / 2），单一神经网络（10M 参数）替代了 109,504 行 C++ 代码控制全身。**洗碗机连续 4 分钟自主操作**——目前最长最复杂的人形机器人自主任务
> - **2026.03** Helix 02 客厅整理 demo —— Elon Musk 公开质疑真实性
> - **2026.04.15** **GR00T N1.6**（**4 天前刚发布**）—— 内部 VLM 升级到 NVIDIA Cosmos-Reason-2B，Diffusion Transformer 翻倍（32 vs 16 层），训练时解冻 VLM 顶部 4 层

[节奏：这里停 1 秒，进入国内副线——这一段同样重要]

> **国内进展也必须单独讲**——这恰好是中国 AI 工作里被国际同行追平甚至局部领先的一个领域：

- **银河通用 GraspVLA**（2025.01.09）——**全球首个端到端具身抓取基础大模型**，与智源、北大、港大合作。**预训练完全用合成数据**（10 亿帧"视觉-语言-动作"对），实现零样本测试能力。提出了 VLA 基础模型需满足的"七大泛化金标准"（光照 / 背景 / 平面位置 / 空间高度 / 动作策略 / 动态干扰 / 物体类别）。配套机器人 **Galbot** 在 NVIDIA CES 2025 发布会上托举 RTX 5090 出场。
- **智元（AgiBot）GO-1**（2025.03.10）——提出 **ViLLA 架构**（Vision-Language-Latent-Action），用**MoE + Latent Planner + Action Expert** 三件套，在 100 万条真实机器人 demonstration 上训练。基于 **AgiBot World 数据集**（100 万条轨迹 / 217 个任务），平均成功率从 46% 提升到 78%。**国内首个把 VLA 推到产品级 + 公开大规模数据集的工作**。
- **宇树（Unitree）UnifoLM-VLA-0**（2026 开源）——给 G1 人形机器人装"具身 AI 大脑"，能开药瓶、装网球拍、整理工具。**基于阿里 Qwen2.5-VL-7B**——你看，**这是 Qwen 直接被国内具身公司用作 backbone 的真实案例**。整个项目 GitHub 开源。

[节奏：抛一句判断]

**国内具身这条线和国外的差异**：硅谷（Figure / Physical Intelligence）走"重金投入 + 全栈自研"；NVIDIA 走"开源 foundation model + 生态绑定"；**国内主要走"硬件价格优势 + 开源 + 数据规模"路线**——宇树 G1 售价 $13.5K（一个数量级低于 Figure 02），加上免费的 UnifoLM-VLA-0，整个研究门槛被打到了消费级。**这个组合可能是中国在具身领域走到全球前列的关键**。

[节奏：这里停 1 秒，然后讲 SLAM 视角——这是你的人设抓手，要慢、要稳]

> **小观点 2**：VLA 这个方向我特别有感受，因为它和我做的 SLAM/3DGS 直接接壤。



VLA 模型负责"听人话 + 看场景 + 出动作"。但有一个它自己解决不了的问题——**机器人怎么知道自己在哪里、世界长什么样？怎么判断这条路能不能走？怎么在一个新环境里建图？**

这恰恰是 SLAM、3D 重建、3DGS 这些方向在解决的问题。

[节奏：这里再停 1 秒，给观点强调]

**VLA 不是要替代 SLAM——是 SLAM 上面再叠一层智能决策**。一个完整的具身智能 agent，至少需要三层：**底层是 SLAM/重建（环境理解 + 自定位）→ 中层是 VLA（动作生成）→ 上层是任务规划（推理大模型）**。这三层都在快速迭代，未来会越来越紧密耦合。

> **小观点 3**：但有人可能会觉得，VLA 这个词已经讲了一两年，是不是过气了？

我的看法正好相反——**VLA 真正的爆发其实刚开始**。

[投影：3 节点闭环图——推理 + VLA + World Models 三圈相交]

为什么？因为**VLA 正在和我前面讲的另外两个新方向融合**：

- **VLA + 推理大模型**：让机器人能做长程任务规划。**Figure Helix 02 的三级架构**（System 0 实时平衡 1kHz / System 1 视觉运动 200Hz / System 2 高层推理）就是最典型的例子——明确借鉴了 Kahneman "快思考 + 慢思考"。**洗碗机 4 分钟连续自主任务**就是这个架构跑出来的。
- **VLA + World Models**：用想象出来的世界训练 agent。**最新最强的信号**——4 天前发布的 **NVIDIA GR00T N1.6**，把内部 VLM 直接换成了 **Cosmos-Reason-2B**——也就是说 NVIDIA 把自家 world model（Cosmos 系列）直接集成进 VLA 模型了。**这是 VLA + World Model 融合首次进入产品级**。

[节奏：这里给整段最高权重的一句话，慢、稳、有力]

> **我的判断**：**这三条线在 2026 年开始合并成一件事——下一代具身智能基础模型**。VLA 不是孤立的方向，它是这个闭环的"中间执行器"。Figure Helix 02 是"VLA + 推理"融合的代表，**4 天前刚出的 GR00T N1.6 把 Cosmos world model 直接吃进 VLA**——这件事不再是研究话题，而是产品路线图。**所以 VLA 没过时，反而是整个具身领域的"交汇点"**。

参考资料：

- **Brohan et al. — RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control** (Google DeepMind, 2023)
[https://arxiv.org/abs/2307.15818](https://arxiv.org/abs/2307.15818)
  - **VLA 范式的开山之作**
- **Physical Intelligence — π₀: Our First Generalist Policy** (官方博客, 2024.10)
[https://www.physicalintelligence.company/blog/pi0](https://www.physicalintelligence.company/blog/pi0)
  - **π₀ 官方介绍**，
- **Black et al. — π₀: A Vision-Language-Action Flow Model for General Robot Control** (论文)
  [https://arxiv.org/abs/2410.24164](https://arxiv.org/abs/2410.24164)
- **Figure AI — Helix: A Vision-Language-Action Model for Generalist Humanoid Control** (官方博客, 2025.02)
[https://www.figure.ai/news/helix](https://www.figure.ai/news/helix)
  - **Helix 官方介绍**
- **Figure AI — Introducing Helix 02: Full-Body Autonomy** (2026.01.27，3 个月前)
[https://www.figure.ai/news/helix-02](https://www.figure.ai/news/helix-02)
  - Helix 02 官方介绍——三级架构（System 0 / 1 / 2），10M 参数神经网络替代 109,504 行 C++
- **Figure AI — Helix 02 Living Room Tidy** (2026.03.09)
[https://www.figure.ai/news/helix-02-living-room-tidy](https://www.figure.ai/news/helix-02-living-room-tidy)
  - 客厅整理 demo，Elon Musk 公开质疑真实性的那个
- **Figure AI — Introducing Figure 03** (2025.10)
[https://www.figure.ai/news/introducing-figure-03](https://www.figure.ai/news/introducing-figure-03)
  - 第三代人形机器人硬件，掌内嵌摄像头 + 触觉传感器（3 克级别力感知）
- **NVIDIA — GR00T N1.5** (2025.06.11)
[https://research.nvidia.com/labs/gear/gr00t-n1_5/](https://research.nvidia.com/labs/gear/gr00t-n1_5/)
  - **GR00T N1.5 官方页面**，重点看 FLARE 目标（从人类视频学习）
- **NVIDIA Isaac-GR00T GitHub (含 N1.6 release notes, 2026.04.15)**
[https://github.com/NVIDIA/Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T)
- **银河通用 GraspVLA** (2025.01.09)
  - 官方解读: [https://www.aibase.com/news/14630](https://www.aibase.com/news/14630)
  - **全球首个端到端具身抓取基础大模型** + 七大泛化标准 + 10 亿帧合成数据预训练
- **智元（AgiBot）GO-1** (2025.03.10)
  - 官方 paper: [https://agibot-world.com/blog/agibot_go1.pdf](https://agibot-world.com/blog/agibot_go1.pdf)
  - 全球新闻稿: [https://www.globenewswire.com/news-release/2025/03/11/3040608/0/en/AgiBot-GO-1-The-Evolution-of-Generalist-Embodied-Foundation-Model-from-VLA-to-ViLLA.html](https://www.globenewswire.com/news-release/2025/03/11/3040608/0/en/AgiBot-GO-1-The-Evolution-of-Generalist-Embodied-Foundation-Model-from-VLA-to-ViLLA.html)
  - **ViLLA 架构**（VLA → Vision-Language-Latent-Action）+ AgiBot World 数据集（100 万条 / 217 任务）
- **宇树 UnifoLM-VLA-0** (2026)
  - 解读: [https://robohorizon.cn/zh/news/2026/03/unitree-g1-practical-skills/](https://robohorizon.cn/zh/news/2026/03/unitree-g1-practical-skills/)
  - 基于 Qwen2.5-VL-7B 的 VLA / 12 类操作任务 / 全部开源

---

## 延伸 3：World Models 的真正突破（2.5 min）



[投影：Genie 3 demo gif + NVIDIA Cosmos 概念图]

> **小观点**：还记得我前面讲 2018 年 David Ha 那篇 World Models 论文吗？过了 7 年，**world model 终于走出了玩具任务，开始走向通用化和产品化**。

**第一个标志性事件 — Genie 3 发布（2025.08.05，DeepMind）**：

[投影：Genie 3 demo gif，720p 实时交互场景]

- **第一个面向公众的实时交互通用 world model**
- **20-24 fps，720p，可保持几分钟的一致性**
- 用户从一张图或一段文字出发，可以**实时操控**生成的 3D 环境探索
- 距 2018 Ha 那篇论文的"小玩具任务"**整整 7 年**——质变发生在 2024-2025 年大模型基础设施齐备之后

跟 2018 年 Ha 那个 V+M+C 架构比，**Genie 3 不是同一个量级**——它的训练数据规模、生成画质、可交互性都是 LLM 时代的产物。

**第二个标志性事件 — NVIDIA Cosmos 成为 Physical AI 的基础设施层**：

- 2025.01 CES 发布，**至今下载量超 200 万**
- 三个模型族：**Predict**（未来状态模拟）/ **Transfer**（仿真到现实迁移）/ **Reason**（物理推理）
- 早期采用者：**Figure AI、Uber、Waabi**——你看，**这恰好是 VLA + 自动驾驶厂商**

而且我前面讲过 —— **4 天前发布的 GR00T N1.6 + Cosmos Reason 2 一起**。GR00T N1.6 直接用 **Cosmos-Reason-2B 作为内部 VLM**——它就是 NVIDIA 自家最新的 world model。**这是 world model 真正进入产品级的标志**——不是研究 paper，是产品 release。

[节奏：这里抛出一个独特视角——我做 SLAM 的人怎么看这件事]

> **小观点**：但讲 World Models 不能只讲"生成"这一侧——还有"重建"这条对照线。

[投影：左边 Genie 3 / Cosmos 生成的虚拟世界；右边 3DGS / VGGT 重建的真实世界]

我做 SLAM 和 3D 重建，看 World Models 的角度有点不一样——**它不是 AI 第一次试图"理解世界"，它是 AI "理解世界"的另一条路线**。重建这条路线最近 3 年也在飞速演进：

- **3D Gaussian Splatting（3DGS，2023.07，Inria，SIGGRAPH 2023 best paper）**——彻底改变了 3D 重建。100+ fps 的 1080p 实时渲染、训练几分钟达到 Mip-NeRF360 的画质。**3DGS 把"重建已存在的世界"这件事的成本降了一个数量级**。
- **DUSt3R / MASt3R（Naver Labs，CVPR 2024）**——彻底改变了"传统 SLAM 依赖标定 + 多视几何"的范式。**给一组未标定图像，直接 transformer 输出 3D pointmap + 相机参数**，map-free relocalization 上中位平移误差从 1.17 降到 0.36，旋转误差砍 80%。
- **VGGT（Visual Geometry Grounded Transformer，Meta + Oxford，CVPR 2025 best paper）**——这是**重建侧最新的"震撼弹"**。一个 feed-forward transformer，输入一张到几百张图，**1 秒内**直接输出相机参数 + 深度图 + 点云 + 3D track。**完全不需要传统的 bundle adjustment / 后处理优化**——这意味着 SfM 这件事被一个 transformer 端到端替代了。

[节奏：这里抛出真正的判断——这是你的人设抓手]

> **我的判断（我做 SLAM 视角的核心判断）**：World Models 让我看到一件有意思的事——**"重建世界" 和 "生成世界" 这两条线正在汇合**。
>
> 仔细对比就能发现——**两条线在用越来越相似的工具**：都用 transformer 做主干、都向 foundation model 方向走、都开始用海量数据预训练。3DGS 和 Genie 3 在某种意义上做的是同一件事——**用神经网络表示 3D 世界**，区别只是数据来源（观察 vs 训练）和目标（精确重建 vs 可信生成）。
>
> **VGGT 是这条汇合线最强的信号**——一个 transformer 做 SfM 这件事在 2 年前是不可想象的。同样地，Genie 3 能从一张图生成可交互 3D 环境，2 年前也不可想象。**这两条线最终可能会变成一件事——AI 既能理解你给它看的世界，也能想象出没看见过的世界**。
>
> 这个方向 2023-2026 这 3 年的进展速度，让我相信**它会成为 2027-2028 AI 的核心战场之一**——和 LLM 、推理大模型并列，而不是替代关系。**我们这些做 SLAM/3D 视觉的人，恰好就站在这场汇合的中心**。

参考资料：

- **DeepMind — Genie 3: A new frontier for world models** (2025.08.05)
[https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)
- **NVIDIA — Cosmos World Foundation Model Platform for Physical AI** (2025.01, CES 发布)
[https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai](https://research.nvidia.com/publication/2025-01_cosmos-world-foundation-model-platform-physical-ai)
- **NVIDIA Cosmos 官方页面**
[https://www.nvidia.com/en-us/ai/cosmos/](https://www.nvidia.com/en-us/ai/cosmos/)
- **NVIDIA Tech Blog — Cosmos Reason 2 + GR00T N1.6** (2026.04)
[https://developer.nvidia.com/blog/building-generalist-humanoid-capabilities-with-nvidia-isaac-gr00t-n1-6-using-a-sim-to-real-workflow/](https://developer.nvidia.com/blog/building-generalist-humanoid-capabilities-with-nvidia-isaac-gr00t-n1-6-using-a-sim-to-real-workflow/)
- **3D Gaussian Splatting** (Inria, SIGGRAPH 2023 best paper)
  - 项目主页: [https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)
  - GitHub: [https://github.com/graphdeco-inria/gaussian-splatting/](https://github.com/graphdeco-inria/gaussian-splatting/)
- **DUSt3R / MASt3R** (Naver Labs, CVPR 2024)
  - DUSt3R 主页: [https://dust3r.europe.naverlabs.com/](https://dust3r.europe.naverlabs.com/)
  - MASt3R 解读: [https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/](https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/)
- **VGGT — Visual Geometry Grounded Transformer** (Meta + Oxford VGG, **CVPR 2025 Best Paper**)
  - 项目主页: [https://vgg-t.github.io/](https://vgg-t.github.io/)
  - GitHub: [https://github.com/facebookresearch/vggt](https://github.com/facebookresearch/vggt)
  - 论文: [https://arxiv.org/pdf/2503.11651](https://arxiv.org/pdf/2503.11651)

---

# 收尾（3 min）

> **核心 hook**：① 整体判断回收开场承诺 ② 加一句"风险缓冲过渡"承认还有内容没展开 ③ 抛 3 个讨论问题，自然过渡到 10 min 讨论
>
> **重要**：这一段提到的"推理大模型 / VLA / World Models 突破"和 Q3 提到的"VLA / JEPA"是**今晚没正式展开的内容**——所以前面要加一句风险缓冲过渡，让听众知道这是为下次分享留的钩子，避免被现场追问。

[投影：全场总览图——4 老阶段（今晚）+ 3 新方向（下次）+ 闭环图]

讲到这里，今天的主体结束了。我想用 1 分钟做一个整体判断，然后抛 3 个问题给大家讨论。

[节奏：这里先加风险缓冲过渡句，5 秒，让听众知道下面提到的几个名词是为下次分享留的钩子]

> **风险缓冲过渡（5 秒，必念）**：

下面我整体判断里会提到 3 个新方向——**推理大模型、VLA、World Models 突破**——还有等下 Q3 会提到的**几条具身路线**——**这些今晚没展开**，是我下次分享的核心。今晚先把这几个名词放在你脑子里，下次我专门讲。

> **我的整体判断**：

如果让我用一句话总结今天讲的——**AI 演进到现在，正在从"各管各的能力建设"走向"闭环融合"**。

前面讲的 4 个老阶段，每一个都是**单点能力的建立**：

- 第一阶段建立了"AI 能学特征"
- 第二阶段建立了"AI 能 scale"
- 第三阶段建立了"AI 能创造、能跨模态理解"
- 第四阶段为下一个时代埋下了种子

下一个阶段（**也就是下次分享的主线**），是这些能力**开始合并成 agent**：

- 推理大模型让 AI **会想**
- VLA 让 AI **会做**
- World Models 让 AI 能在脑内 **演**

而且 **2026 这一年这个合并已经从概念走到产品**——**4 天前**（2026.04）NVIDIA 发布 GR00T N1.6 + Cosmos Reason 2，把 world model 直接吃进 VLA；**3 个月前**（2026.01）Figure Helix 02 用三级架构完成了 4 分钟的洗碗机连续自主任务；**8 个月前**（2025.08）Genie 3 让 world model 第一次走向公众。这些时间点告诉我们——**AI 演进的速度比我们想象的快**。

[节奏：这里加一个收尾判断，关于国内的位置——全文保留，因为前面已经有风险缓冲过渡句"具身一线"是为下次留的钩子]

而且大家可以注意到——**今天我讲到的 release 里，很大比例是中国团队**：Qwen3.5、GLM-4.6、Kimi K2.5、DeepSeek R2 在 LLM 一线；银河通用 GraspVLA、智元 GO-1、宇树 UnifoLM-VLA-0 在具身一线。**这不是凑数据——是 2025-2026 年 AI 全球格局真实的变化**。"AI 在硅谷诞生但需要全球协作完成"——我们恰好生在了一个中国不只是参与、而是**核心贡献者**的时代。

下一个阶段，会是**这些 agent 真正走出实验室、进入物理世界**的阶段。这恰好对应曹姐这个群的名字——"与AI共进"。我们这些做技术的人，不只是看客，是参与者。

[节奏：在这里停 2 秒，自然过渡到讨论]

> **抛 3 个讨论问题给大家**：

[投影：3 个问题，编号清晰]

**Q1：scaling 的尽头**

我们讲了预训练 scaling。但 LLM 还有"推理 scaling"这第二条腿（下次分享会展开）。这两条腿都还能跑多远？什么时候会撞墙？撞墙后下一条 scaling 的腿可能是什么？

**Q2：开源 vs 闭源的格局**

DeepSeek R1 让我们看到——一个之前闭源垄断的方向（推理大模型），4 个月就被开源追平。这个"开源追赶速度"是会持续，还是 R1 是个例外？大模型的护城河到底在哪？

**Q3：具身智能的路径之争**

VLA 路线（端到端模型）vs 传统机器人控制（分层规划）vs 完全 world model 驱动（LeCun 的 JEPA 路线）——大家觉得哪条路会赢？还是会融合？我的猜测是融合，但具体怎么融合？

[节奏：以一个轻松的收尾结束自己的部分]

好，我能给的就这么多。接下来 10 分钟时间留给大家讨论，**有任何想展开的话题都欢迎抛**——包括今晚我没讲的那 3 个新方向，如果有人特别想听某一个，我可以现场展开半段。

谢谢大家！

---

# 附：现场可能遇到的几种情况 + 应对

## 情况 1：有人打断追问

**保持镇定**：

- 如果是确认性问题（"你刚说的 X 是不是 Y 意思？"）→ 直接答 → 继续讲
- 如果是细节追问（"attention 公式怎么推？"）→ "这个细节我今天不展开，有兴趣会后聊；接下来我们讲 ..."
- 如果是质疑（"我觉得你说的不对，因为 ..."）→ "好观点。我的依据是 ...（如果有把握）" / "我没考虑过这个角度，会后我想再了解一下你的视角"（如果没把握）

## 情况 2：时间超了（目标 50 min，超 5+ min 要砍）

**砍掉的优先级**（按"砍了不影响主线 + 不影响判断"排序）：

1. 先砍**阶段一 CNN 的 Zeiler-Fergus 可视化段**（约 1 min，砍了不影响 CNN 学层级特征的主线）
2. 再砍**阶段二的 Chinchilla 修正段 + 涌现争议（Schaeffer）那一段**（约 2 min，砍了主线还在，只是不再有"我有最新视角"信号）
3. 再砍**阶段三 classifier-free guidance 一句话**（30 秒）和 **DDIM 采样加速一句话**（30 秒）
4. 再砍**阶段四 JEPA 之争里 VICReg 的细节**（约 1.5 min，把 JEPA 直接简化成"LeCun 反对 LLM、提了一个在表示空间预测的路线，至今没爆点"）
5. 最后砍**开场的"我能给 / 不给"段**（约 1 min，但可能影响基调）

## 情况 3：时间不够 45 min 就讲完了

**补充内容**：

1. 在每个"我的判断"段后面加一句"大家有没有不同看法？"，制造短互动
2. 在第二阶段后追加"Transformer 之后，CV 领域的 ViT、蛋白质领域的 AlphaFold 也都用了 Transformer——一个架构吃下所有领域，这在 AI 史上前所未有"
3. 在阶段四 JEPA 之争段后追加："这场争论 2026 年的最新进展我留到下次分享展开，但有人现在想听吗？"——把延伸段的内容**临时拉一段**进来
4. 收尾的 3 个讨论问题展开成 5 个

## 情况 4：曹姐对哪个方向特别感兴趣，想多听

**让她带一段**："这块我了解的可能还不够深，曹姐你怎么看？" → 把麦给她，自己学习

---

# 现场口语化清单（念之前自己改写）

这份稿件偏书面。**强烈建议你周一-周四把它改写成自己的语言**。改写时注意：

- 删掉所有"我们前面说"——口语里太啰嗦，改成"刚才讲的"
- "颠覆性的"、"革命性的"等形容词能删就删，换具体事实
- 加一些"嗯"、"对"、"我觉得"这种语气词在判断句前面，听起来像在讲不像在念
- 长句拆短，讲的时候 1 句话不超过 25 个字
- 关键转折前加一个短停顿（在稿件上标 `[停 1 秒]`）

**你周四晚上的最后一晚，应该花 1.5h 做完整空讲 + 录音**。听一遍录音，把听起来"像念稿"的地方改掉。