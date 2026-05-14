# 📘 第 6 课：范式 3 —— MoE / MoT（专家分工）

> 对应论文章节：**Sec 3.4 + 公式 (15) + Fig. 3(c) + Table 1 第三组**（第 12–13 页）
> 学习目标：理解为什么"双专家 + 深度交互"是 IDM-Style 和 Single-Backbone 的折中点；看懂 π0 哲学如何迁移到 video backbone 上。

---

## 0. 30 秒温习前两课

| 范式 | 核心思路 | 致命缺点 |
|---|---|---|
| 第 4 课 IDM-Style | 两个独立模型，先想象再行动 | 两阶段接口僵化，无法联合训练 |
| 第 5 课 Single-Backbone | 一个 backbone 通吃 | 视频和动作完全共享参数，**无法差异化优化** |

> 🎯 **今天的范式想要"鱼和熊掌兼得"**：
> 既要 Single-Backbone 的联合训练，又要 IDM-Style 的模态特化。

---

## 一、先把 MoE 和 MoT 这两个词讲清楚

如果你不熟这两个术语，先记住下面这两个一句话定义。

### MoE（Mixture of Experts，混合专家）
原本是大模型领域的概念：

> **同一个模型里有多个"专家"子网络，对每个输入选择性地激活其中一部分。**

经典例子：Mixtral、DeepSeek-MoE。一个 token 进来，路由器只激活几个专家，其它专家不算，**省算力**。

### MoT（Mixture of Transformers，混合 Transformer）
是 MoE 的一种特殊形态：

> **整个 transformer 被分成几个"专家流"（expert streams），每个流处理特定模态，但所有流之间通过 attention 互相交流。**

更适合多模态场景。论文里提到的 Motus、LingBot-VA、BagelVLA 都是这种结构。

> 💡 **简单类比**：
> - **MoE** 像超市里 10 个收银员，每个顾客只去其中 2–3 个收银台
> - **MoT** 像乐团：钢琴家、小提琴家、鼓手各自演奏专业部分，但通过指挥（shared attention）保持同步

---

## 二、一句话定义这个范式

> 🎯 **MoE/MoT 范式 = 保留视频专家和动作专家的独立参数，但让它们通过共享 attention 在每一层深度交互。**

论文第 12 页 Fig. 3(c) 长这样（我用文字画出来）：

```
                ┌─────────────────────────────┐
                │    LAYER L                   │
   视频流 hv ──▶│  ┌────────┐    ┌────────┐    │──▶ hv (下一层)
                │  │  Video │◀──▶│ Action │    │
   动作流 ha ──▶│  │ Expert │    │ Expert │    │──▶ ha (下一层)
                │  └────────┘    └────────┘    │
                │       ▲           ▲          │
                │       └─SHARED ATTN─┘        │
                │                              │
                │  observation o_t, language l │
                └─────────────────────────────┘
```

注意三件事：
1. **两个专家有各自的参数**（video expert 和 action expert）
2. **每一层都通过 shared/joint attention 交流**（不是只在最后融合）
3. **整个系统端到端训练**（不是先训 WM 再训 IDM）

---

## 三、和前两节的对比（这是这节课的核心）

我把三种范式放在一起，让你瞬间看清"专家分工"在哪儿：

| | IDM-Style（第 4 课） | Single-Backbone（第 5 课） | MoE/MoT（今天） |
|---|---|---|---|
| 模型/专家数 | 2 个独立模型 | 1 个共享 backbone | 2 个专家 + 共享 attention |
| 参数共享 | ❌ 完全独立 | ✅ 完全共享 | 🟡 部分共享（attention 共享，FFN 独立） |
| 联合训练 | ❌ 不行 | ✅ 可以 | ✅ 可以 |
| 模态差异化 | ✅ 完全独立优化 | ❌ 强行共享 | ✅ 各专家可独立优化 |
| 信息流 | 单向：WM → IDM | 双向 + 完全融合 | 双向 + 保留模态边界 |

> 🔑 **MoT 的设计哲学**：
> "完全独立"和"完全共享"都太极端了——
> **让 attention 共享（信息可以流动），让 FFN 独立（计算可以特化）**，是一个更聪明的折中。

---

## 四、数学形式（论文公式 (15)）

把这种"双专家 + 层级交互"写成数学：

$$
\bigl[h_v^{\ell+1},\; h_a^{\ell+1}\bigr] \;=\; F_{\ell}^{\text{mix}}\bigl(h_v^{\ell},\; h_a^{\ell};\; o_t,\; l\bigr)
$$

各符号含义：
- $\ell$：层的下标（第几层 transformer）
- $h_v^\ell$：视频专家在第 $\ell$ 层的隐藏状态
- $h_a^\ell$：动作专家在第 $\ell$ 层的隐藏状态
- $F_\ell^{\text{mix}}$：**层级交互算子**——可以是 joint attention、cross attention 或 shared attention

> 💡 **这个公式想表达的关键**：
> 视频和动作的隐藏状态在**每一层**都被一个 fusion 算子耦合一次，而不是只在输入或输出做一次拼接。
> 这种"逐层互相浸润"的方式，比 Single-Backbone 的"一锅炖"更结构化，比 IDM-Style 的"接力交付"更紧密。

---

## 五、为什么这么做有道理？

论文 Sec 3.4 给出的核心动机有两条：

### 动机 ①：视频和动作的"频率不同、精度不同、目标不同"

| | 视频生成 | 动作生成 |
|---|---|---|
| 时序频率 | 通常 5–30 FPS | 控制频率 50–500 Hz |
| 表征维度 | 高（像素或 latent） | 低（几个数值） |
| 优化目标 | 视觉重建（L2、感知 loss） | 动作精度（regression / discrete） |
| 训练数据 | 大量未标注视频 | 少量精确标注的机器人数据 |

强行用 Single-Backbone 处理这两者，就像让一个全能选手既练长跑又练短跑——容易**两边都不极致**。
MoE/MoT 让两个专家各自做自己擅长的事，**而 attention 负责保证它们在做同一件事**。

### 动机 ②：站在 π0 的肩膀上

如果你看过 π0 的论文，你会发现它的架构本来就是这种"双专家"思想：
- 一个大的 VLM 专家处理 vision-language
- 一个轻量的 action expert 处理控制

> 🎯 **MoE/MoT 范式的本质 = 把 π0 的"VLM 专家 + Action 专家"换成"Video 专家 + Action 专家"。**
>
> 唯一的差别是 backbone 从静态语义编码器换成了"擅长时序预测"的视频生成模型。

---

## 六、4 种"专家耦合模式"，按耦合深度排序

论文 Sec 3.4 把这一类方法分成几种风格，我整理成 4 种典型的耦合模式：

### 模式 A：浅耦合 — 视频是主，动作是辅

**代表**：**GE-Act**（Liao et al., 2026）

**结构**：
- 主干：一个 pretrained video diffusion 模型（基本不动）
- 副线：一条**轻量的 flow-matching action pathway**
- 耦合方式：通过 **deep cross-attention** 把视频 latent 注入动作分支

**核心设计**：
- 视频分支在线**不渲染像素**——它只跑 latent，提供"未来的预测结构"
- 动作分支接收这些 latent，translate 成可执行控制
- 推理时**视频分支不必生成完整视频**，只用其中间表征

> 💡 **比喻**：视频专家是"军师"（只在心里想未来），动作专家是"将军"（执行决策）。

### 模式 B：深耦合 — 真正的 MoT

**代表**：**Motus**（Bi et al., 2025）、**LingBot-VA**、**BagelVLA**、**DiT4DiT**

**结构**：
- 多个 expert 流（视频 expert、动作 expert，有时还有"理解 expert"）
- 每一层都有 **shared attention** 让所有 expert 互相看见
- 端到端联合训练

**Motus 的特色**：明确把架构 formulate 成 Mixture-of-Transformers，专家分别负责 understanding / video generation / action。

**LingBot-VA 的特色**：把 video token 和 action token **interleave 成一个共享自回归序列**，再用 dual-stream MoT 处理。

**BagelVLA 的特色**：把 linguistic planning / visual forecasting / action generation **三件事放进一个执行循环**，并通过 **Residual Flow Guidance** 做单步去噪（不需要全视频 rollout，速度快）。

### 模式 C：训练-推理解耦

**代表**：**Fast-WAM**（Yuan et al., 2026）

**结构**：训练时用 shared-attention MoT 让视频和动作专家联合学习，**但推理时跳过视频专家**。

**核心发现**：很多场景下，**联合训练带来的性能提升主要来自训练阶段的视频监督**，而不是推理时的视频生成。所以推理时把视频砍掉，性能损失很小、速度提升很大。

> 💡 这和上节课 GigaWorld-Policy 的"视觉分支可选"是同一种思想。

### 模式 D：Latent 空间专家化

**代表**：**LDA-1B**（Lyu et al., 2026）、**FRAPPE**（Zhao et al., 2026）

**结构**：
- 不在像素空间预测视频，而是在 **DINO latent 空间**或**视觉基础模型 latent 空间**做"视觉预测"
- 视频 expert 和 action expert 通过共享 self-attention 耦合

**为什么巧妙**：把"未来视觉"压缩到一个语义浓缩的 latent 空间里，**信噪比更高、训练更稳定**，避开了像素空间的冗余。

---

## 七、用第 3 课的"切片视角"回看

第 3 课的联合分布：

$$
p\bigl(o_{t+1:t+k},\; a_{t+1:t+k} \;\big|\; o_t,\; l\bigr)
$$

### 三种范式怎么"切"这个分布

| 范式 | 怎么处理这个联合分布 |
|---|---|
| IDM-Style | **链式分解 + 两个独立模型** |
| Single-Backbone | **直接联合建模 + 一个完全共享的网络** |
| MoE/MoT | **直接联合建模 + 一个"分专家但共享 attention"的网络** |

> 🎯 **用一句话总结三种范式的演进**：
>
> 从"完全独立"（IDM-Style）→ 经过"完全融合"（Single-Backbone）→ 找到"专业分工 + 共享语境"（MoE/MoT）的中间最优点。

这个演进路径，和大模型从 dense → MoE 的演进**几乎一样**——都是为了在"模型容量"和"差异化能力"之间找平衡。

---

## 八、MoE/MoT 的优缺点

### ✅ 优点

1. **吸收两边精华**：联合训练（继承 Single-Backbone）+ 模态特化（继承 IDM-Style）
2. **直接复用 π0 的工程经验**：很多 π0 / π0.5 的训练 trick 可以无缝迁移
3. **推理灵活**：通过砍掉某个专家，可以在"完整生成"和"快速决策"之间切换
4. **Scaling 友好**：MoE/MoT 在大模型里已被证明是高效的 scaling 路径

### ❌ 缺点

1. **架构复杂**：要小心设计 fusion 算子（joint vs cross vs shared attention），实现门槛高
2. **训练不稳定**：多专家联合训练容易出现"模态主导"问题——视频专家梯度大，动作专家梯度被淹没
3. **路由设计难**：如果想做真正的 MoE 风格（动态选择专家），路由器训练是个老大难
4. **算力依然不便宜**：虽然推理可以砍专家，但训练时所有专家都要算梯度

---

## 九、Table 1 第三组的横向对比（论文第 8 页）

| 方法 | 推理时的未来生成 | 耦合方式 |
|---|---|---|
| **GE-Act** | Latent visual guidance | Expert fusion |
| **Motus** | Expert rollout | MoT fusion |
| **LingBot-VA** | Visual predictive context | MoT fusion |
| **BagelVLA** | Single-step visual foresight | MoT fusion |
| **Fast-WAM** | Train-time video, **test-time skipped** | MoT fusion |
| **LDA-1B** | Latent dynamics only | Expert fusion |
| **FRAPPE** | Latent representation alignment | Parallel experts |
| **DiT4DiT** | Latent video guidance | Expert fusion |

> 📌 **共同点**：都是 VGM backbone + 专家化设计
> **差异点**：fusion 机制（cross-attention vs shared-attention vs interleaved sequence）

---

## 十、把三种范式放在一张"演进图"里

```
完全独立                                           完全融合
    │                                                │
    │  IDM-Style       MoE/MoT          Single-Backbone │
    │ ───────────  ──────────────     ──────────────── │
    │  (第 4 课)     (第 6 课)          (第 5 课)        │
    │                                                │
    │  2 个模型     2 个专家+共享attn   1 个 backbone   │
    │  各练各的     双人合奏           一人独奏         │
    │                                                │
    │  无联合训练   联合训练           联合训练         │
    │  模态独立     模态独立           模态强耦合       │
    │                                                │
    └─────────────────  ↓  ────────────────────────┘
            "如何处理同一个联合分布的不同选择"
```

> 🔑 **一个隐藏洞察**：
> MoE/MoT 不是为了击败 Single-Backbone，而是 **承认"完全共享参数"是一个过强的假设**。
> 现实中视频和动作的"信号特性"差距太大，让它们在 attention 层共享语境、在 FFN 层各练各的，往往是更稳定的工程选择。

---

## 十一、一句话总结今天

> 🎓 **MoE/MoT = 双专家 + 共享 attention 的中间路线：
> 既保留 IDM-Style 的模态特化，又拿到 Single-Backbone 的联合训练。
> 它的本质是把 π0 的"双专家"哲学迁移到 video pretrained backbone 上，
> 让视频专家提供"未来的预测结构"，让动作专家专注"精确控制"。**

---

## 十二、给你一个"何时选哪种范式"的速查表

如果你要做项目，这个表能给你一个**起点级**的设计建议：

| 你的处境 | 推荐范式 | 为什么 |
|---|---|---|
| 数据少、想快速验证想法 | **IDM-Style** | 模块化、易调试、能用预训练 video model |
| 数据多、算力多、追求极致性能 | **Single-Backbone** | 端到端联合训练，性能上限最高 |
| 数据中等、想兼顾性能和工程稳定性 | **MoE/MoT** | 折中，最容易复用 π0 / π0.5 的训练 trick |
| 推理速度优先，能容忍训练成本 | **MoE/MoT 模式 C**（Fast-WAM 风格） | 训练用视频教，推理砍掉视频 |

---

## ✅ 课后检查（这次建议至少答 Q1，让我看你能否清晰区分三种范式）

### Q1（必答 · 三方对比题）
请你**用一段话**把第 4、5、6 课的三种范式的本质差异讲清楚。
（提示：用"参数共享程度"和"是否能联合训练"这两个维度，最容易讲清）

### Q2（必答 · 应用题）
下面是几个真实场景，给每个场景挑一种最合适的范式，并说明理由：

- **(a)** 你拿到一个全新机器人形体，只有 200 条演示数据，但有 100 万段互联网未标注视频
- **(b)** 你有一个工业生产线机器人，需要 200Hz 的精确控制，但视觉只用来"观察"（不精确）
- **(c)** 你想做一个研究 demo，希望能"看到"机器人脑子里想什么（强可解释）

### Q3（选答 · 思辨题）
论文 Sec 3.4 提到一个有趣的发现（Fast-WAM）：**很多 MoE/MoT 方法的性能提升主要来自训练阶段的视频监督，而非推理时的视频生成。**
如果这个发现普遍成立，那是不是意味着——
**未来的趋势是"训练时用 WM 当 regularizer，推理时彻底丢掉 WM"？**
说说你的看法。

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
> - (a)
> - (b)
> - (c)
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -

---

**下一课预告**：
**第 7 课 — 范式 4：Unified VLA（把 WM 内化进 VLA）**

下节课你会看到一个"反方向"的设计哲学：
**不是"在 VLA 旁边加一个 WM"，而是"让 VLA 内部本身具有 WM 的能力"。**
代表作：GR-1、UP-VLA、WorldVLA、DreamVLA、UniVLA、CoWVLA、F1。
看完后你会理解：**为什么"未来图像预测"可以作为 VLA 训练时的"免费监督信号"。**
