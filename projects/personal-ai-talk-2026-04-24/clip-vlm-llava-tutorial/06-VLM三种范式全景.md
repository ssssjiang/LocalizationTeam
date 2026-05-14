# 📘 第 6 课：VLM 三种范式全景

> 学习目标：俯瞰整个 VLM 领域，建立"双编码器 / 编解码器 / LLM-based"三种范式的分类学。
>
> 重点：理解 BLIP-2 的 **Q-Former** 设计——它是从 CLIP 走向 LLaVA 的关键一跳。
>
> 预计阅读时间：30 分钟。读完本章，再看任何新 VLM 论文，你能秒判断它的流派与定位。

---

## 一、CLIP 之后的瓶颈：能"看"不能"说"

第 5 章末尾我们提到：

> CLIP 只能"判别"，不能"生成"。
>
> - 给图 + 候选文本：能告诉你哪个最匹配 ✅
> - 给图：不能告诉你"图里有什么" ❌
> - 给图 + 问题：不能回答 ❌

为什么？因为 CLIP 的两个 encoder 学的是**对齐**，文本 encoder 是把"a photo of a cat"压成一个向量然后扔了——它没学过"如何从向量反向生成文字"。

要做生成，必须在架构里有一个**生成式解码器**（autoregressive decoder）。

CLIP 之后的 VLM 演进，本质是在回答一个问题：

> **如何把"对齐"和"生成"统一在一个模型里？**

历史给了三种答案。

---

## 二、范式分类：三大流派

```
                ┌──────────────────────────────────┐
                │      VLM 三大范式                │
                └──────────────────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
   ┌─────────┐           ┌─────────┐           ┌─────────┐
   │ 范式 1  │           │ 范式 2  │           │ 范式 3  │
   │ 双编码器│           │ 编解码器│           │LLM-based│
   └─────────┘           └─────────┘           └─────────┘
       │                      │                      │
   CLIP                   BLIP                   Flamingo
   ALIGN                  BLIP-2                 LLaVA
   SigLIP                 CoCa                   MiniGPT-4
                                                 InternVL
                                                 Qwen-VL
       │                      │                      │
   强：检索/分类         强：caption/VQA        强：对话/推理/指令跟随
   弱：不能生成          弱：对话能力一般       弱：图像理解依赖 LLM
```

我们一个一个看。

---

## 三、范式 1：双编码器派（Dual Encoder）

### 代表模型

- **CLIP** (OpenAI 2021) —— 第 4-5 章主角
- **ALIGN** (Google 2021) —— 18 亿带噪声图文对训练，证明"数据规模 > 数据质量"
- **SigLIP** (Google 2023) —— 把 InfoNCE 换成 sigmoid loss，能用更大 batch
- **EVA-CLIP** (BAAI 2023) —— 改进的 CLIP，开源界事实标准

### 架构与训练

完全是第 4 章讲的双塔 + 对称 InfoNCE。这里不重复。

### 适用场景

| 任务 | 是否擅长 | 原因 |
|---|---|---|
| 图文检索（图找文 / 文找图） | ✅ 极强 | 双塔架构推理可缓存，秒级返回 |
| 零样本图像分类 | ✅ 极强 | "类名 → 文本嵌入 → 内积" 即可 |
| 图像聚类 / 数据分析 | ✅ 极强 | 嵌入空间已对齐 |
| 给图配文（image captioning） | ❌ 不能 | 没有解码器 |
| 视觉问答（VQA） | ❌ 不能 | 没有生成能力 |
| 多模态对话 | ❌ 不能 | 没有 LLM |

### 关键改进：SigLIP 的 sigmoid 损失

SigLIP（Zhai et al., 2023）做了一个**看似微小但很重要**的改动：

把 InfoNCE 的 softmax 损失换成 sigmoid 损失。

原 CLIP InfoNCE：

$$
\mathcal{L} = -\log \frac{\exp(S_{ii}/\tau)}{\sum_{j} \exp(S_{ij}/\tau)}
$$

SigLIP sigmoid loss：

$$
\mathcal{L}_{\text{SigLIP}} = -\sum_{i,j} \log \sigma\big(z_{ij} \cdot S_{ij}\big)
$$

其中 $z_{ij} = +1$（如果 $i = j$，是正例）或 $-1$（负例）。

**好处**：

1. **不需要 softmax 的全局归一化** → 跨 GPU 通信开销大幅下降
2. **每对样本独立判别** → 可以用更大的 batch（SigLIP 用了 32K-1M）
3. **小 batch 也能训** → 部署友好

→ SigLIP 是当前性能最强的开源 CLIP 类模型，许多新 VLM（LLaVA-NeXT 部分版本、Idefics2）已经把视觉编码器从 CLIP 换成 SigLIP。

> **设计哲学**：在 CLIP 这个层面上，"用更好的损失"和"用更多数据"都能涨点，但前者性价比更高。

---

## 四、范式 2：编解码器派（Encoder-Decoder）

### 代表模型

- **BLIP** (Salesforce 2022) —— 引入 captioning + filtering 自举式数据生产
- **BLIP-2** (Salesforce 2023.01) —— 引入 **Q-Former**，从此可以接 LLM
- **CoCa** (Google 2022) —— Contrastive + Captioning 联合训练

### 核心设计：在 CLIP 之上加生成

**最朴素的做法**：

```
[Image]  ─→  Image Encoder  ─→  视觉特征
                                    │
                                    ▼
                              Text Decoder  ─→  生成 caption
                                    │
                                    ▲
                              [START]  →  "a"  →  "cat"  →  "sitting"  ...
```

然后训练目标加一项 **language modeling loss**：让 decoder 自回归地生成正确的 caption。

最终损失：

$$
\mathcal{L}_{\text{BLIP}} = \mathcal{L}_{\text{ITC}} + \mathcal{L}_{\text{ITM}} + \mathcal{L}_{\text{LM}}
$$

- **ITC** (Image-Text Contrastive)：CLIP 风格的对比损失
- **ITM** (Image-Text Matching)：二分类（这对图文配不配）
- **LM** (Language Modeling)：自回归生成 caption

→ BLIP 既能做检索（用 ITC 部分），又能做生成（用 LM 部分）。

### BLIP-2 的关键创新：Q-Former

BLIP 有个问题：**视觉编码器和文本解码器都需要从头训练，开销大**。

BLIP-2 提出一个聪明的设计：

> **冻结预训练好的视觉编码器（CLIP-ViT）和 LLM，只训练一个轻量的桥接器**。

这个桥接器叫 **Q-Former**（Querying Transformer）。

### Q-Former 在做什么

问题：CLIP-ViT 输出的图像特征是 **256 个 patch tokens**（对于 224×224 图）。如果直接把 256 个 token 喂给 LLM，序列长度过长，注意力计算爆炸。

更深的问题：256 个 token 里大部分是冗余信息（背景、纹理、噪声）。LLM 真正需要的是被压缩、被组织过的视觉信息。

**Q-Former 的解法**：

```
图像 patch tokens [N×D]      ← N=256，CLIP-ViT 输出
       │
       │
       ▼
┌──────────────────┐
│   Q-Former       │
│                  │
│  可学习 queries   │      ← K=32 个 learnable query token
│   [K×D]          │           （这是关键！）
│                  │
│  ┌────────────┐  │
│  │Self-Attn   │  │      ← queries 之间互相 attend
│  ├────────────┤  │
│  │Cross-Attn  │  │      ← queries 去 attend 图像 tokens
│  │            │  │           "提问"出关键信息
│  ├────────────┤  │
│  │FFN         │  │
│  └────────────┘  │
│                  │
└──────────────────┘
       │
       ▼
压缩后的视觉 tokens [K×D]    ← 只剩 32 个 token，喂给 LLM
```

**精髓**：Q-Former 内部维护 **32 个可学习的 query token**。这些 query 通过 cross-attention "提问" 图像特征——本质是"我作为视觉信息提取器，需要从图像里提哪些信息？"

经过训练，这 32 个 query 学会了从图像中提取**对下游任务有用**的信息，把 256 维原始 patch 序列压缩成 32 维语义序列。

### Q-Former 的两阶段训练

**阶段 1：表征学习**（视觉编码器冻结，但还没接 LLM）
- 用 CLIP 风格的 ITC + ITM + ITG (image-grounded text generation) 三个目标训练 Q-Former
- 目标：让 32 个 query token 学会"提取语义对齐的视觉信息"

**阶段 2：生成学习**（视觉编码器和 LLM 都冻结，只训 Q-Former）
- Q-Former 输出的 32 个 token + 文本 prompt → 喂给冻结的 LLM
- LLM 自回归生成 caption / answer
- 只通过 Q-Former 反传梯度

### 为什么 Q-Former 是关键创新

它解决了一个核心问题：

> **如何把任意视觉编码器（CLIP-ViT, EVA-ViT 等）连接到任意 LLM（OPT, FlanT5 等），且不破坏两者的预训练知识？**

答案：**冻结两端，训练中间的轻量桥接器**。

这个思路被后续模型大量继承：
- **InstructBLIP**：BLIP-2 + 指令调优数据
- **MiniGPT-4**：BLIP-2 的 Q-Former 简化版 + Vicuna
- **mPLUG-Owl**：类似 Q-Former 的设计

但是 LLaVA 走了一条**完全不同的路**——它说："连 Q-Former 都太复杂了。"

→ 我们第 7 章看 LLaVA 怎么用更简单的设计达到更好的效果。

### BLIP-2 的局限

虽然 Q-Former 是个聪明设计，但 BLIP-2 也有短板：

1. **对话能力一般**：训练数据主要是 caption 和 VQA，不是多轮对话
2. **指令跟随弱**：模型不太懂"请用诗歌的形式描述这张图"这种复杂指令
3. **Q-Former 训练复杂**：两阶段训练 + 三个损失，调参痛苦
4. **能力受限于 LLM 选择**：BLIP-2 用 OPT-2.7B / 6.7B，能力远不如后来的 Vicuna / LLaMA

→ 这些短板正是 LLaVA 出现的契机。

---

## 五、范式 3：LLM-based 派

### 代表模型

- **Flamingo** (DeepMind 2022) —— 先驱，引入 cross-attention 注入视觉
- **LLaVA** (UW 2023.04) —— 极简架构 + GPT-4 造数据，本教程主线
- **MiniGPT-4** (KAUST 2023.04) —— 与 LLaVA 同期，类似思路
- **InternVL** (Shanghai AI Lab 2023+) —— 开源 SOTA
- **Qwen-VL / Qwen2-VL** (Alibaba) —— 中文圈最强开源
- **GPT-4V** (OpenAI 2023.09) —— 闭源标杆，技术细节不公开

### 核心设计：把视觉特征注入 LLM

LLM-based 范式的本质：

> **现成的 LLM 已经具备了强大的语言理解、推理、对话能力。我们只需要让它"看见"图像。**

具体做法是把视觉特征转化成 LLM 能理解的"伪 word embedding"，插入到文本 token 序列里。

### 三种注入方式

**方式 A：Cross-Attention**（Flamingo）

```
LLM Decoder Layer:
  ┌─────────────────────────┐
  │  Self-Attention         │      ← 文本 token 之间注意
  ├─────────────────────────┤
  │  Cross-Attention        │      ← 文本去 attend 视觉特征 ← 新增
  │  (image features)       │
  ├─────────────────────────┤
  │  FFN                    │
  └─────────────────────────┘
```

每隔几层 LLM transformer block 插入一个 cross-attention 层（Flamingo 用 Perceiver Resampler 先压缩视觉特征）。

- 优点：能保留 LLM 几乎所有原有能力，新加的 cross-attn 层独立训练
- 缺点：架构改动较大，训练复杂

**方式 B：Q-Former + Prompt Prefix**（BLIP-2 / InstructBLIP）

```
[Q-Former 输出 32 token] + [文本 prompt token]  →  LLM 输入序列
```

把 Q-Former 的输出当作"视觉前缀"，和文本 prompt 拼起来喂给 LLM。

- 优点：无需改 LLM 架构，即插即用
- 缺点：Q-Former 训练复杂

**方式 C：Linear Projection（LLaVA）**——极简

```
图像 → CLIP-ViT → patch features → Linear(W) → 视觉 token  →  LLM
                                       ↑
                          整个连接只有一个矩阵 W
```

直接用一个**线性投影**把 CLIP-ViT 的 patch features 映射到 LLM 的 word embedding 空间，然后当成普通 token 喂给 LLM。

- 优点：**简单到不可思议**——投影矩阵 W 是模型唯一可训练的桥接组件
- 第 7 章详细讲

→ LLaVA 证明了：**最简单的方式 + 高质量数据 = SOTA**。

---

## 六、三种范式横向对比

| 维度 | 双编码器（CLIP） | 编解码器（BLIP-2） | LLM-based（LLaVA） |
|---|---|---|---|
| 主要任务 | 检索、分类 | captioning、VQA | 对话、推理、指令跟随 |
| 视觉编码器 | ViT（从头训） | CLIP-ViT（冻结） | CLIP-ViT（冻结） |
| 文本部分 | Text Transformer | OPT/FlanT5 | LLaMA/Vicuna |
| 桥接方式 | 共享投影空间 | Q-Former（32 token） | Linear/MLP（256 token） |
| 训练数据 | 4 亿图文对 | 1.2 亿图文对 | 558K 对齐 + 158K 指令 |
| 能否生成文本 | ❌ | ✅ | ✅✅✅（更自然） |
| 能否多轮对话 | ❌ | △（有限） | ✅ |
| 能否跟随指令 | △（prompt 工程） | ✅（部分） | ✅✅✅ |
| 训练成本 | 极高（数百 GPU·年） | 中等 | **低**（8 张 A100 一天） |
| 推理成本 | 极低 | 中 | 中（受 LLM 影响） |
| 主要短板 | 无生成 | 对话弱 | 幻觉、视觉细粒度弱 |

### 选择指南

如果你要做……

- **大规模图像检索系统** → 用 **CLIP / SigLIP**（推理速度王者）
- **图像 caption / 简单 VQA** → 用 **BLIP-2**（专精此道）
- **多模态对话助手 / 复杂指令跟随** → 用 **LLaVA / Qwen-VL**（当前 SOTA 路线）
- **不在乎模型大小，要顶级效果** → 用 **GPT-4V / Claude 3.5 Sonnet / Gemini Vision**（闭源）

---

## 七、为什么 LLaVA 是当前的"事实标准"

观察 2024-2025 的开源 VLM 生态：

```
LLaVA (2023.04)
    │
    ├─→ LLaVA-1.5 (2023.10)
    │       │
    │       └─→ LLaVA-NeXT (2024.01)
    │               │
    │               └─→ LLaVA-OneVision (2024.08)
    │
    ├─→ MiniGPT-4 / MiniGPT-v2
    │
    ├─→ InternVL（沿袭 LLaVA 思路）
    │
    ├─→ Qwen-VL（受 LLaVA 启发）
    │
    └─→ ShareGPT4V（基于 LLaVA 改进数据）
```

**几乎所有开源多模态对话模型都受 LLaVA 启发**——架构上基本是 "视觉编码器 + 投影器 + LLM" 三件套，差异只在：
- 视觉编码器选什么（CLIP-ViT-L、SigLIP、EVA-CLIP）
- 投影器是 Linear / MLP / Q-Former
- LLM 选什么（Vicuna、LLaMA-2、Qwen、Mistral）
- 训练数据怎么准备

为什么 LLaVA 的范式赢了？三个原因：

1. **极简**：架构清晰、易复现、易扩展
2. **训练成本低**：558K + 158K 数据，8 张 A100 一天能跑完
3. **数据生产范式革新**：用 GPT-4 造高质量多模态指令数据（第 7 章详讲）

→ **LLaVA 真正改变的是"如何低成本造一个好的 VLM"的方法论。**

---

## 八、本章一句话总结

> 🎓 **VLM 三大范式：CLIP 派擅长"对齐"，BLIP 派加上"生成"，LLaVA 派把视觉接到 LLM 让模型学会"对话"。**
>
> 演进的核心驱动力是：**让模型从"看图判别"走向"看图说话"再走向"看图聊天"**。
>
> LLaVA 是当前事实标准，它的三个核心设计（极简架构、CLIP 冻结编码器、GPT-4 造数据）我们下一章详细拆。

---

## ✅ 课后检查

### Q1（必答 · 分类题）
下面 5 个模型，分别属于哪种范式？为什么？

- (a) DALL·E 2 的 CLIP 部分
- (b) BLIP-2
- (c) GPT-4V（OpenAI）
- (d) SigLIP
- (e) Qwen-VL

### Q2（必答 · 设计题）
Q-Former 用 32 个可学习 query token 把图像 patch（256 个）压缩成 32 个 token。如果改成 8 个或 128 个 token 会怎样？分别讨论。

### Q3（必答 · 对比题）
"BLIP-2 用 Q-Former 做桥接" vs "LLaVA 用 Linear projection 做桥接"，两种设计的取舍是什么？为什么 LLaVA 路线最终胜出？

### Q4（选答 · 综合题）
回顾全章，给一个判断题：如果你要做一个"在 1 亿张图的库里检索图像"的产品，应该选 LLaVA 还是 CLIP？为什么？反过来，如果要做"客户上传图片后回答关于图片的复杂问题"的客服 bot，应该选哪个？

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

- **(a) DALL·E 2 的 CLIP 部分** → **范式 1：双编码器**。CLIP 本身就是双塔；DALL·E 2 用 CLIP 做"文本嵌入 → 图像嵌入"的桥接，但 CLIP 部分依然是双编码器架构。
- **(b) BLIP-2** → **范式 2：编解码器**（带 Q-Former）。视觉编码器 + Q-Former + 文本解码器（LLM）。
- **(c) GPT-4V** → **范式 3：LLM-based**。OpenAI 没公开技术细节，但从行为推断是把视觉特征接到 GPT-4 主体。
- **(d) SigLIP** → **范式 1：双编码器**。CLIP 的改进版，把 InfoNCE 换成 sigmoid loss，但架构仍是双塔。
- **(e) Qwen-VL** → **范式 3：LLM-based**。基于 Qwen LLM + ViT 视觉编码器 + 类 Q-Former 桥接。

→ **快速判断诀窍**：看模型核心组件——
- 只有两个 encoder 在共享空间对比 → 范式 1
- 有 encoder + decoder + 显式桥接器（Q-Former 等） → 范式 2
- 主体是个大 LLM，视觉只是"插入" → 范式 3
</details>

<details>
<summary>点开看 Q2 参考</summary>

**Q-Former query 数量的取舍**：

| query 数 | 信息容量 | 计算开销 | 训练难度 |
|---|---|---|---|
| 8 | 极少 | 最低 | 困难（信息太挤压） |
| 32（默认） | 适中 | 适中 | 适中 |
| 128 | 充足 | 较高 | 较易 |
| 256（=patch 数） | 最大 | 最高 | 退化为不压缩 |

**8 个 token**：
- 优点：LLM 输入序列短，推理快
- 缺点：信息严重丢失，复杂场景描述不全（"图里有 5 个人，分别在做什么"这种问题答不出）
- 实际效果：在 caption 任务上还行，VQA 显著下降

**128 个 token**：
- 优点：信息保留更多，细粒度问题（"图右下角的招牌写什么"）回答更好
- 缺点：LLM 输入序列长 4 倍，训练和推理成本都涨
- 实际效果：复杂任务略涨，但性价比不如 32

**为什么 32 是 sweet spot**：

- 32 个 token × 4096 维（典型 LLM 隐藏维度） = 13 万维信息容量
- 一张图的"语义信息量"大致就在这个量级——再多就是冗余的视觉细节，对下游 LLM 没用
- 训练时梯度通路足够宽，但又不会让 Q-Former 过拟合到"复制"原图特征

**LLaVA 的反例**：

LLaVA 不用 Q-Former，直接用 256 个 patch token 接 LLM。这看起来"效率低"，但效果反而更好——因为：

1. 全部 patch 信息保留，细粒度任务更强
2. 没有 Q-Former 压缩带来的信息瓶颈
3. LLM 自己有 attention 机制，能从 256 个 token 里挑相关的

代价是 LLM 输入序列长。但**LLaVA 用得起**——因为它的 LLM (Vicuna-7B) 本来就支持长序列。
</details>

<details>
<summary>点开看 Q3 参考</summary>

**两种设计的取舍**：

| 维度 | Q-Former (BLIP-2) | Linear Projection (LLaVA) |
|---|---|---|
| 架构复杂度 | 高（Transformer） | 极低（一个矩阵 W） |
| 可训练参数 | ~100M | ~5M（Linear）/ ~20M（MLP） |
| 训练阶段数 | 2 阶段（表征 + 生成） | 2 阶段（对齐 + 指令） |
| 训练损失数 | 3 个（ITC + ITM + ITG） | 1 个（next token prediction） |
| 信息压缩 | 256 → 32 token | 256 → 256 token（不压缩） |
| 输入 LLM 序列长 | 短 | 长 |
| 训练数据要求 | 需大量 caption 数据 | 需高质量指令数据 |
| 可扩展性 | 调参复杂 | 简单（换 LLM 即可） |

**为什么 LLaVA 胜出**：

1. **简单即可靠**——更少的设计选择 = 更少的失败模式
2. **保留更多视觉信息**——256 token 比 32 token 信息量大 8 倍
3. **训练效率高**——一个 next token prediction 损失，调参简单
4. **数据为王**——LLaVA 的核心创新不在架构，而在 GPT-4 造数据；架构越简单，数据的作用越突出
5. **生态效应**——LLaVA 极简架构让所有人能复现、改进、扩展，形成开源滚雪球

→ **设计哲学**：在数据足够好的前提下，**架构越简单越好**。这与 GPT 系列"transformer + next token prediction" 的极简主义一脉相承。

实际上现在很多新模型（如 Cambrian、LLaVA-NeXT）回过头来发现：**Q-Former 在数据充分的场景下并没有真正优于 Linear projection**——压缩信息这件事，原本就该让下游 LLM 自己用 attention 决定，而不是预先压死。
</details>

<details>
<summary>点开看 Q4 参考</summary>

**场景 1：1 亿张图的检索系统** → **CLIP / SigLIP**

理由：

1. **推理速度**：CLIP 双塔架构可以**预计算并缓存**所有 1 亿张图的嵌入。查询时只需要算 1 次文本嵌入 + 1 亿次内积——毫秒级。LLaVA 必须把每张图都过一遍 LLM——不可用。

2. **可扩展性**：CLIP 嵌入可以存在向量数据库（FAISS、Milvus），用近似最近邻（ANN）算法搜索。LLaVA 没这个能力。

3. **不需要生成**：检索任务只需要"匹配度"，不需要文本输出。CLIP 完美胜任，LLaVA 是杀鸡用牛刀。

实际工业部署：Pinterest、TikTok、Google 图像搜索的核心都是 CLIP 类双编码器。

**场景 2：客服 bot 回答图片问题** → **LLaVA / Qwen-VL / GPT-4V**

理由：

1. **对话能力**：客户问"这张产品图里的红色按钮是干什么用的"，需要 LLM 的推理 + 自然语言生成。CLIP 完全做不到。

2. **指令跟随**：客户的问题千奇百怪（"帮我用专业术语描述"、"以表格形式列出"）——只有 LLM 能处理这种灵活指令。

3. **多轮对话**：客户可能继续追问"那蓝色按钮呢"——需要上下文理解，CLIP 没有。

4. **吞吐量要求低**：客服 bot 一次只处理一张图，LLaVA 推理速度（几秒）完全够用。

**结论**：

- CLIP 和 LLaVA 不是替代关系，而是**互补**的——前者是"快+广"，后者是"慢+深"。
- 实际系统经常组合使用：先用 CLIP 检索 / 过滤，再用 LLaVA 深度理解。
- 选模型的第一个问题永远是 **"这个任务需要生成文本吗？"** 是 → LLaVA 系；否 → CLIP 系。
</details>

---

**下一课预告**：

➡️ [`07-LLaVA架构与GPT-4造数据.md`](./07-LLaVA架构与GPT-4造数据.md)

LLaVA 的两个杀手级设计：

1. **极简架构**：CLIP-ViT (frozen) + Linear/MLP Projector + Vicuna LLM
2. **GPT-4 造数据**：用纯文本 GPT-4（没有视觉能力！）+ caption + bbox 文本，造出 158K 高质量多模态指令数据

第 7 章会让你理解 LLaVA 论文最大的贡献——**它告诉了世界"如何低成本造一个好的多模态对话模型"**。
