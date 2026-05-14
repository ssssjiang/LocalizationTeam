# 📘 第 4 课：CLIP 核心思想与架构

> 学习目标：理解 CLIP 要解决什么问题、它的关键设计、以及著名的 N×N 矩阵图每一项在算什么。
>
> 前置：第 1-3 章对比学习预热。CLIP 在数学上就是 SimCLR 把"图-图对比"换成"图-文对比"。
>
> 预计阅读时间：30 分钟。

---

## 一、CLIP 要解决什么问题

### 回到第 1 章的痛点

第 1 章我们说过监督学习的"封闭词表困境"：

> ImageNet 1000 类已是人类标注的工程极限。模型只能识别这 1000 类，模型对"狗"超类的理解被人为切碎了。

到 2020 年，这个困境催生了一系列尝试：

| 方法 | 思路 | 结果 |
|---|---|---|
| 扩大标注数据集 | JFT-300M、Instagram Hashtag | 贵到只有 Google/Facebook 玩得起 |
| 自监督预训练 + 监督微调 | SimCLR、MoCo + ImageNet linear probe | 接近监督学习，但仍受限于下游标注 |
| 多任务学习 | 在多个数据集上联合训练 | 能力相加，但**仍然封闭** |

无论哪种思路，本质问题都没解决：**模型最终能识别什么类，由人类预先决定**。

### CLIP 的关键问题

OpenAI 在 2020 年问了一个更激进的问题：

> **能不能让模型识别"任何用自然语言描述的概念"——不需要预先定义类别？**

比如：
- 不是"识别 ImageNet 里的 1000 类"
- 而是"给我一张图，再给我任意一句话，告诉我它们多大程度上匹配"

如果能做到这件事，那么：

- **零样本分类**：把 1000 个类名变成 "a photo of a {class}"，逐一和图比相似度，最相似的就是预测类别。
- **检索**：给一句话，找最匹配的图。
- **新概念识别**：见到"赛博朋克咖啡馆"这种 ImageNet 里完全没有的概念，也能识别。

但要做到这件事，需要回答两个问题：

1. **监督信号从哪来？**——不能再靠"人类标的类别"
2. **怎么把图像和文本放进同一个语义空间？**

---

## 二、CLIP 的两个关键洞察

### 洞察 1：自然语言是天然的、规模无限的、零样本可泛化的监督信号

互联网上有海量的"图 + 描述"对：

- Flickr 上每张图都有 caption
- Wikipedia 文章里的图都有 alt-text
- Instagram 帖子有图 + 标题
- 新闻网站的图都有图说

> **自然语言不需要被设计成类别——它本身就是开放词表。**

OpenAI 从公开互联网爬了 **4 亿** (image, text) 对，构成 WIT（WebImageText）数据集。这个规模是 ImageNet 的 28 倍。

**为什么不用现成的 caption 数据集（如 MS-COCO 60 万对）？**

因为 60 万对太少了——CLIP 论文做了 ablation：

| 数据规模 | ImageNet zero-shot 精度 |
|---|---|
| 1500 万对 | 11% |
| 4 亿对 | **76.2%** |

→ **数据规模是 CLIP 工作的核心要素**。互联网爬取（虽然有噪声）是唯一可行的扩量途径。

### 洞察 2：用对比学习，而不是用文本生成

OpenAI 一开始做了一个**生成式**版本：让模型给图像生成 caption（类似 image captioning）。

这条路走不通——**4 亿对训练 12 天，效果不如对比学习的 1/12 时间**。

为什么？

> **生成 caption 是个超难任务**：模型不仅要懂图，还要选词、组语法、保持流畅。绝大部分算力浪费在"语言学层面"，而不是"图文对齐"上。
>
> **对比学习只问一个简单问题**：这张图和这段文本配不配？是个二分类（升级版的 N+1 类分类），算力全部花在对齐上。

→ **关键设计选择**：CLIP 选了对比学习，并把 SimCLR 的范式 1:1 搬过来。

这一步做完，所有铺垫到位——剩下的就是把 SimCLR 的架构改成"图-文对比"。

---

## 三、CLIP 的双塔架构

### 整体结构图

```
   一张图 x                        一段文本 t
       │                                │
       ▼                                ▼
 ┌──────────┐                    ┌──────────┐
 │ Image    │                    │  Text    │
 │ Encoder  │                    │ Encoder  │
 │ (ViT)    │                    │(Transf.) │
 └──────────┘                    └──────────┘
       │                                │
       ▼                                ▼
   h_image                          h_text
       │                                │
       │   Linear Projection (W_I)      │   Linear Projection (W_T)
       ▼                                ▼
   I ∈ ℝ^D                          T ∈ ℝ^D
       │                                │
       │  L2 normalize                  │  L2 normalize
       ▼                                ▼
       └────── 对比损失 InfoNCE ────────┘
```

### 关键细节

**Image Encoder**：CLIP 论文同时实验了两种：
- **ResNet 系列**：ResNet-50 / 101 / 50x4（经典 CNN）
- **Vision Transformer**：ViT-B/32, ViT-B/16, ViT-L/14（后者最强，是今天大家说"CLIP-ViT"的默认指代）

CLIP 之后所有人都用 ViT-L/14（特别是 LLaVA）。

**Text Encoder**：63M 参数的 Transformer：
- 12 层、8 头注意力、512 维
- 词表用 BPE，49152 tokens
- 输入末尾加 [EOS] token，**用 [EOS] 位置的输出向量作为整段文本的表征**

> 注意：CLIP 的 text encoder 比当时的 BERT 小很多。OpenAI 发现"模型规模上 image encoder 远比 text encoder 重要"——因为图像信息密度高，文本信息密度低。

**两个独立的投影矩阵 $W_I, W_T$**：把两个模态投影到**共享的** $D$ 维空间（CLIP 用 512 / 768 维）。

**L2 归一化**：保证后续相似度计算用的是余弦相似度。

### 为什么是"双塔"而不是"单塔"

"单塔"模型（如 ViLT、ALBEF 早期版本）会让图像 token 和文本 token 在同一个 Transformer 里做 cross-attention。这种设计：

- 优点：能学到细粒度的图文交互
- 缺点：**推理时必须把每对 (图, 文) 都过一遍 Transformer**

举例：在 100 万张图里检索一句话最匹配的图。
- 单塔：必须算 100 万次 cross-attention → 慢得不可用
- 双塔：图和文各算一次 encoder → 然后只是 100 万次内积 → 极快

> **双塔架构 = 推理时图和文可以分别独立编码、缓存、检索。这是 CLIP 能在工业界大规模部署的根本原因。**

代价是：双塔之间没有交互，模型对**细粒度图文对齐**（比如"猫的左爪在右下角"）天生不擅长。这是 CLIP 后续被 BLIP / LLaVA 改进的方向（第 6 章会讲）。

---

## 四、对称 InfoNCE 损失

### 一个 batch 的几何

设 batch size $N$。每个 batch 抽 $N$ 个图文对：$(\mathbf{x}_1, \mathbf{t}_1), (\mathbf{x}_2, \mathbf{t}_2), \ldots, (\mathbf{x}_N, \mathbf{t}_N)$。

经过编码后得到：
- $\mathbf{I}_1, \mathbf{I}_2, \ldots, \mathbf{I}_N \in \mathbb{R}^D$（$N$ 个图像嵌入）
- $\mathbf{T}_1, \mathbf{T}_2, \ldots, \mathbf{T}_N \in \mathbb{R}^D$（$N$ 个文本嵌入）

构造**相似度矩阵** $\mathbf{S} \in \mathbb{R}^{N \times N}$：

$$
S_{ij} = \mathbf{I}_i^\top \mathbf{T}_j / \tau
$$

注意：$\mathbf{I}_i, \mathbf{T}_j$ 已经 L2 归一化，所以 $\mathbf{I}_i^\top \mathbf{T}_j$ 等于余弦相似度，范围 [-1, 1]，再除以 $\tau$ 控制锐度。

### 著名的 N×N 矩阵图（CLIP 论文 Figure 1）

设 $N = 4$，$\mathbf{S}$ 长这样（⭐ 表示对角线，是正例对）：

```
                T_1   T_2   T_3   T_4
            ┌─────────────────────────┐
       I_1  │  ⭐    .     .     .    │  ← 第 1 行：I_1 vs 所有 T
            │                         │     正例是 (I_1, T_1)
       I_2  │  .     ⭐    .     .    │
            │                         │
       I_3  │  .     .     ⭐    .    │
            │                         │
       I_4  │  .     .     .     ⭐   │
            └─────────────────────────┘

        ↑ 第 1 列：所有 I vs T_1
          正例是 (I_1, T_1)
```

**对角线 $S_{ii}$ 是正例**（图 $i$ 配文 $i$）；**非对角线 $S_{ij}, i \neq j$ 是负例**。

### 对称损失：i2t + t2i

CLIP 的损失同时在**两个方向**做 InfoNCE：

**方向 1：image-to-text (i2t)**——以图为 query 找正确的文

对相似度矩阵的**每一行**做 softmax + 交叉熵，正确答案是对角线上的元素：

$$
\mathcal{L}_{\text{i2t}} = -\frac{1}{N} \sum_{i=1}^{N} \log \frac{\exp(S_{ii})}{\sum_{j=1}^{N} \exp(S_{ij})}
$$

物理含义：对每张图 $\mathbf{I}_i$，把"它和 $\mathbf{T}_i$ 的相似度"凸出来，把"它和其他文本的相似度"压下去。

**方向 2：text-to-image (t2i)**——以文为 query 找正确的图

对相似度矩阵的**每一列**做 softmax + 交叉熵：

$$
\mathcal{L}_{\text{t2i}} = -\frac{1}{N} \sum_{j=1}^{N} \log \frac{\exp(S_{jj})}{\sum_{i=1}^{N} \exp(S_{ij})}
$$

物理含义：对每段文本 $\mathbf{T}_j$，把"它和 $\mathbf{I}_j$ 的相似度"凸出来。

**对称损失**：

$$
\boxed{\ \mathcal{L}_{\text{CLIP}} = \frac{1}{2} \big( \mathcal{L}_{\text{i2t}} + \mathcal{L}_{\text{t2i}} \big)\ }
$$

### 为什么必须双向？

如果只做 i2t（每行 softmax），模型可能学到一种**退化解**：

- 把所有 $\mathbf{T}$ 学成一团，让 $\mathbf{T}_i$ 在和 $\mathbf{I}_i$ 比时，相似度只比其他 $\mathbf{T}$ 略高一点
- 此时每行 softmax 看起来对（对角线最大），但**列方向**完全乱（$\mathbf{T}_j$ 可能匹配 $\mathbf{I}_5$）

→ **加上 t2i 方向，就强迫整个矩阵在两个方向都对得上**——只有真正学到双射映射的模型才能两个 loss 都低。

这是 CLIP 比早期 image-text matching 模型（如 VSE++）效果好的关键设计。

---

## 五、CLIP 的 pseudo-code（论文 Figure 3）

CLIP 论文的 Figure 3 给了一段极简的 numpy 风格 pseudo-code，是理解 CLIP 训练管线的最佳载体：

```python
# image_encoder - ResNet 或 Vision Transformer
# text_encoder - CBOW 或 Text Transformer
# I[n, h, w, c] - 一个 minibatch 的对齐图像
# T[n, l] - 一个 minibatch 的对齐文本（n 个文本，每个长 l）
# W_i[d_i, d_e] - 图像投影矩阵
# W_t[d_t, d_e] - 文本投影矩阵
# t - 可学习的 temperature 参数

# 1. 提取每个模态的特征
I_f = image_encoder(I)    # [n, d_i]
T_f = text_encoder(T)     # [n, d_t]

# 2. 联合多模态嵌入空间 [n, d_e]
I_e = l2_normalize(np.dot(I_f, W_i), axis=1)
T_e = l2_normalize(np.dot(T_f, W_t), axis=1)

# 3. 缩放后的成对余弦相似度 [n, n]
logits = np.dot(I_e, T_e.T) * np.exp(t)

# 4. 对称的损失函数
labels = np.arange(n)
loss_i = cross_entropy_loss(logits, labels, axis=0)   # i2t
loss_t = cross_entropy_loss(logits, labels, axis=1)   # t2i
loss = (loss_i + loss_t) / 2
```

### 这段代码每一行在做什么

**第 1 步**：图像和文本各自通过 encoder，得到原始特征。
- `I_f`：图像特征，维度 $[n, d_i]$，比如 ViT-L/14 输出 $[n, 768]$。
- `T_f`：文本特征，维度 $[n, d_t]$。

**第 2 步**：投影到共享空间 + L2 归一化。
- `np.dot(I_f, W_i)`：线性投影，把图像特征映射到 $d_e$ 维（比如 512）。
- `l2_normalize`：让所有向量长度为 1。

**第 3 步**：算 N×N 相似度矩阵。
- `np.dot(I_e, T_e.T)`：内积矩阵，由于已归一化，等价于余弦相似度。
- `* np.exp(t)`：注意这里——CLIP 把 temperature 实现为 `exp(t)`，避免数值问题，**且 `t` 是可学习参数**。
  - $\exp(t) = 1/\tau$，所以这等价于第 2 章公式里除以 $\tau$。
  - `t` 初始化为 $\log(1/0.07) \approx 2.66$。

**第 4 步**：对称损失。
- `labels = np.arange(n)`：正确答案是对角线，第 $i$ 行的正确类别是第 $i$ 列。
- `axis=0` / `axis=1`：分别在两个方向算交叉熵。
- 最后两个 loss 取平均。

### 仔细看一下，整个 CLIP 训练循环就 4 行

去掉注释和初始化，CLIP 的核心训练逻辑只有 4-5 行 numpy。

> 🎯 **CLIP 的优雅之处**：思想极简，工程极重。
>
> 思想 = SimCLR 的图文版 = 4 行代码。
> 工程 = 4 亿对数据 + 32K batch + 几百张 V100 + 12 天。

---

## 六、与 SimCLR 的对照

把 SimCLR 和 CLIP 并排放：

| | SimCLR | CLIP |
|---|---|---|
| 输入对的来源 | 同一张图的两次随机增强 | 一张图 + 配套的文本描述 |
| 编码器 | 一个 ResNet（图-图共享） | 两个独立 encoder（图 + 文） |
| projection | 2 层 MLP | 1 层 linear |
| 损失方向 | 一个方向（图 vs 图） | **对称双向**（i2t + t2i） |
| Temperature | 固定 0.5 | **可学习参数** |
| Batch size | 4096 | **32768** |
| 训练数据 | ImageNet 1.28M 张 | **4 亿** 图文对 |
| 学到的能力 | 视觉表征（下游需 fine-tune） | **零样本图像分类**（无需 fine-tune） |

→ CLIP = SimCLR 范式 × 跨模态 × 8 倍规模。

---

## 七、本章一句话总结

> 🎓 **CLIP = 双塔编码器 + 对称 InfoNCE + 4 亿图文对。**
>
> 思想：让"图 i 配文 i"成为训练目标，4 亿次重复后，模型学会把图像和文本投到同一个语义空间。
>
> 这个简单的统一空间，催生了零样本分类、跨模态检索、CLIP-guided 生成等一整代应用——下一章详细讲。

---

## ✅ 课后检查

### Q1（必答 · 理解题）
为什么 CLIP 要做"对称损失"（i2t + t2i）？只做单向会出什么问题？

### Q2（必答 · 比较题）
"双塔" vs "单塔"模型的核心取舍是什么？为什么 CLIP 选了双塔？

### Q3（必答 · 计算题）
CLIP 论文用了 $N = 32768$ 的 batch size。每张图在每个 batch 里要和多少个负例文本对比？这个数字相对 SimCLR ($N=4096$) 大多少倍？

### Q4（选答 · 综合题）
CLIP 的 pseudo-code 第 3 行：`logits = np.dot(I_e, T_e.T) * np.exp(t)`，为什么 temperature 实现为 `exp(t)` 而不是直接除以 $\tau$？提示：考虑数值稳定性。

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
>
> Q3:
>
> Q4:

## 🤔 我的疑问（你来填）

> -
> -

---

## 📋 参考答案

<details>
<summary>点开看 Q1 参考</summary>

只做单向（如只做 i2t）的问题：

模型可以学到一种**退化解**——把所有文本表征 $\mathbf{T}$ 学成一团（彼此相似），同时让 $\mathbf{T}_i$ 在和 $\mathbf{I}_i$ 比时仅"略高于"其他 $\mathbf{T}$。

这种解下：
- **i2t 方向**：每一行 softmax 看起来对（对角线最大），loss 低。
- **t2i 方向**：完全乱套——$\mathbf{T}_j$ 作为 query 时，可能匹配到 $\mathbf{I}_5$（因为所有 $\mathbf{T}$ 都没有清晰判别力，列方向的对齐没保证）。

加上 t2i 损失后，模型必须保证：**任意 $\mathbf{T}_j$ 在和所有图像比较时，也要和 $\mathbf{I}_j$ 最匹配**。这强迫整个矩阵在两个方向都形成清晰的对角结构——也就是真正的双射对齐。

→ 对称损失保证了**真正的双向匹配能力**，这是 CLIP 能做检索（图找文、文找图都行）的基础。
</details>

<details>
<summary>点开看 Q2 参考</summary>

**核心取舍**：

| 维度 | 双塔 | 单塔（cross-attention） |
|---|---|---|
| 推理速度 | 极快（图和文分别编码 + 内积） | 极慢（每对必须过一遍模型） |
| 可缓存性 | 完美（编码结果可预计算） | 差（每次查询都重算） |
| 细粒度对齐 | 弱（无显式 cross-attention） | 强 |
| 对比学习兼容性 | 好（一个 batch 内 N×N 比较） | 差（cross-attention 模型很难做大 batch 对比） |

**CLIP 选双塔的原因**：

1. **对比学习需求**：CLIP 的核心训练范式是 InfoNCE，要求 batch 内 N×N 全对比。单塔模型的 N² 次 cross-attention 计算量爆炸，无法用大 batch。
2. **零样本检索是 killer app**：CLIP 的核心应用是"用文本描述检索图像 / 用 ImageNet 类名做零样本分类"，这两件事都要求**预计算并缓存图像表征**。双塔架构下，4 亿张图可以一次性编码，之后任意 query 都是毫秒级响应。
3. **OpenAI 当时算力受限**：双塔训练成本远低于单塔。

代价是对**细粒度对齐**的牺牲——CLIP 不擅长"猫的左爪在哪"这种空间细节。后来 BLIP-2 / LLaVA 走的就是"用 CLIP 双塔做特征提取 + 后续 cross-attention/LLM 做细粒度推理"的两段式路线。
</details>

<details>
<summary>点开看 Q3 参考</summary>

CLIP $N = 32768$：每张图要和 **32767** 个负例文本对比（除掉自己对应的正例）。

SimCLR $N = 4096$：每个样本要和 **8190** 个负例对比（$2N - 2$，因为每张图有 2 个视图）。

**比例**：$32767 / 8190 \approx 4$ 倍。

但要注意：CLIP 的 32K 是**图-文跨模态对比**，每个负例的"信息量"比 SimCLR 的图-图对比更大——因为图和文之间的对齐是更深的语义任务。

回顾第 2 章"负样本越多越好"的核心直觉：

$$
I(q; k^+) \geq \log N - \mathcal{L}_{\text{InfoNCE}}
$$

$N$ 越大，互信息下界越紧。CLIP 的 32K 把这个下界推到了当时所有图文对齐方法的最高水平。
</details>

<details>
<summary>点开看 Q4 参考</summary>

**用 `exp(t)` 而不是直接学 $\tau$ 的理由**：

1. **数值稳定**：$\tau$ 必须**严格为正**（否则 softmax 失去意义）。如果直接学 $\tau$，需要约束（如 ReLU、softplus），反传梯度会有问题。学一个无约束的 $t$，然后取 $\exp(t)$，自动保证为正。

2. **梯度尺度合适**：在对数尺度上学习温度，相当于学习 $1/\tau$ 的对数。比如 $\tau$ 从 0.1 变到 0.01（10 倍变化）对应 $t$ 从 2.3 变到 4.6（线性 +2.3）——梯度尺度温和、训练稳定。

3. **CLIP 的具体实现**（PyTorch）：

```python
self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))
# 训练时
logit_scale = self.logit_scale.exp().clamp(max=100)
logits = logit_scale * I_e @ T_e.T
```

`clamp(max=100)` 是为了防止 $\exp(t)$ 学到太大的值（对应 $\tau$ 过小，训练崩溃）。

→ 这种"学习对数温度"的设计是 CLIP 的小细节，但被后续所有 VLM 继承。
</details>

---

**下一课预告**：

➡️ [`05-CLIP训练数据与零样本应用.md`](./05-CLIP训练数据与零样本应用.md)

第 5 章我们解决三件事：

1. **WIT 数据集**：4 亿对从哪来、怎么爬、为什么不用现成的 caption 数据
2. **零样本分类的运行机制**：训完之后，怎么把 CLIP 用在 ImageNet 上做"零样本"？
3. **prompt engineering**：为什么 "a photo of a {class}" 比裸类名好那么多？prompt ensemble 是什么？
4. **CLIP 的能力边界**：哪些任务它做不好？为什么？

读完第 5 章，你对 CLIP 的理解就**完整闭环**了。
