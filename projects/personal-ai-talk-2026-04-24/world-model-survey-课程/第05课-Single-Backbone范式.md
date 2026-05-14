# 📘 第 5 课：范式 2 —— Single-Backbone（一个 backbone 通吃）

> 对应论文章节：**Sec 3.3 + 公式 (13)–(14) + Fig. 3(b) + Table 1 第二组**（第 10–12 页）
> 学习目标：理解为什么"把 action 当作 video 的额外一帧"是一个聪明的工程哲学；看清它和 IDM-Style 的本质差异。

---

## 0. 30 秒温习上节课

第 4 课的 IDM-Style 范式：

```
[WM] 想象未来视频 ──▶ [IDM] 反推动作
   两个独立模型，独立训练，接力运行
```

**痛点**：
- ① WM 不准 → IDM 救不回来
- ③ 两个模型接口固定 → IDM 没法"教" WM 生成对决策更有用的画面

> 🎯 **今天的范式直接把"两个独立模型"砍掉，换成"一个 backbone 通吃所有事情"。**

---

## 一、一句话定义这个范式

> 🎯 **Single-Backbone = 用一个共享的 transformer，同时建模"未来画面"和"未来动作"，
> 让两者在同一个生成过程里被联合优化。**

论文第 12 页的 Fig. 3(b) 长这样：

```
       ┌──────────────────────────────────────┐
观察 ──▶│                                      │
       │       SHARED BACKBONE                │
动作 ──▶│       (一个 transformer)              │──▶ 未来画面 + 未来动作
       │                                      │     (同一个生成过程吐出来)
指令 ──▶│                                      │
       └──────────────────────────────────────┘
```

注意和上节课**最关键的差别**：

| | IDM-Style（第 4 课） | Single-Backbone（今天） |
|---|---|---|
| 模型数 | 2 个 | 1 个 |
| 训练 | 两个独立目标 | 一个统一目标 |
| 推理 | 必须按顺序：先 WM 后 IDM | 一次前向同时吐画面和动作 |
| 信息流 | WM → IDM **单向** | 画面 ↔ 动作 **联合建模** |

> 🔑 **这种设计想表达的核心信念**：
> "未来画面"和"未来动作"应该是**同一个生成过程**的两个产物，而不是流水线上的两道工序。

---

## 二、最聪明的工程哲学：把 action 当成 video 的"额外一帧"

这是这种范式最值得记的设计巧思。

### 传统思路（IDM-Style）
- 视频是视频，动作是动作。视频在像素空间，动作在数值空间，两个完全不同的模态。
- 所以你需要一个 VGM 处理视频 + 一个 IDM 处理动作。

### Single-Backbone 思路
- 等等——预训练好的视频扩散模型（比如 CogVideoX）超级强，**何不让它顺手把动作也"画"出来**？
- 把动作 $a$ encode 成几个 token，**塞进视频 token 序列里**，让 backbone 把它们当成"特殊的视频帧"一起生成。

### 数学形式（论文公式 (13)–(14)）

把"未来画面"和"未来动作"拼成一个统一的目标向量：

$$
x = [z_v;\; z_a]
$$

- $z_v$：未来画面的 latent 表示
- $z_a$：未来动作的 latent 表示
- 拼接（concatenate）操作的意思就是"把它们当成同一个序列处理"

然后给一个共享 backbone $f_\theta$ 去做去噪：

$$
\hat{y} \;=\; f_\theta\bigl(\tilde{x}_\tau,\; o_t,\; l,\; \tau\bigr)
$$

- $\tilde{x}_\tau$：被加了噪声的输入（扩散过程的中间状态）
- $\tau$：去噪的时间步
- $\hat{y}$：模型预测的目标

训练目标极其简单——**一个统一的去噪损失**：

$$
\mathcal{L}_{\text{unified}} \;=\; \mathbb{E}\,\ell(\hat{y},\; y)
$$

> 💡 **这一个 loss 同时教模型两件事**：
> "下一帧画面应该长什么样" + "下一刻动作应该是什么"
> 两者**共享所有梯度**，互相监督。

---

## 三、为什么这样做有道理？(论文第 10–11 页的核心论证)

论文 Sec 3.3 给出了这种设计的核心动机，**这是一个比技术更深的洞察**：

> **预训练视频扩散模型不只是"会生成画面"，它的 backbone 本身就是为"建模时序演化"而生的。**

对比一下：
- **VLM backbone**（OpenVLA、π0 用的）：主要靠 image-text alignment 训练 → 强在**语义对应**，弱在时序
- **Video Diffusion backbone**（CogVideoX、Cosmos 用的）：靠时序 ordered observations 训练 → 强在**运动连续性、时序因果、近似物理动力学**

所以——

> 🔑 **当你把动作生成嵌入到视频去噪过程里，你的 policy 自动继承了一个"擅长跨时间传播约束"的 backbone。**

这就是为什么作者说："*the policy may benefit from a backbone already biased toward propagating constraints across time*"。

⚠️ 但论文也很诚实地补充：**这只是"一个有希望的归纳偏置"**，并非定论。Video-pretrained backbone **不一定**比 VLM backbone 更好——这仍是一个开放的实证问题。

---

## 四、5 个代表作，按"激进程度"排序

论文 Sec 3.3 列了 8 个代表作。我按"对联合训练的拥抱程度"排序，挑 5 个最值得记的：

### ① UVA（Li et al., 2025c）— 早期奠基者

**关键设计**：学一个 video-action 联合 latent 空间，同时监督两个模态。

**聪明之处**：在部署时通过**轻量化的 modality-specific decoder head**，可以让推理**跳过视频生成**，只解码动作——既保留了联合训练的好处，又规避了推理慢的问题。

### ② UWA（Zhu et al., 2025a）— 把扩散过程也合并

**关键设计**：把 video diffusion 和 action diffusion **合并到一个 transformer 里**，但每个模态有自己的 timestep。

**聪明之处**：可以通过控制 timestep "marginalize 掉" visual future（让它处于纯噪声状态），从而把整个模型当作纯 policy 用。

### ③ Cosmos Policy（Kim et al., 2026）— 最优雅的"额外一帧"

**关键设计**：保持预训练 video diffusion 架构**几乎不改动**，把 action / future state / value **作为额外的 latent "frame"** 塞进原有的扩散序列里。

**两种使用模式**：
- **Direct policy mode**：只取 action 输出，直接执行
- **Planning mode**：取 future state + value 输出，给候选轨迹打分

> 🎯 **这是 Single-Backbone 哲学最纯粹的体现：什么都是 frame。**

### ④ DreamZero（Ye et al., 2026b）— 解决长时序漂移

**关键设计**：用 **chunk-wise joint denoising**（分块联合去噪），不一次性生成一长段，而是闭环地一小块一小块生成。

**为什么这么做**：自由生成长视频时误差会爆炸；分块生成可以**用最新观测重新校准**，限制 compounding error。

### ⑤ GigaWorld-Policy（Ye et al., 2026a）— 视觉分支可选

**关键设计**：联合优化 future action 预测和 action-conditioned video 生成，但用**因果设计**让 visual branch 在推理时**完全可选**。

**为什么巧妙**：训练时用视频监督学到丰富的物理先验；推理时只跑 action 分支，**速度和纯 policy 一样快**。

---

## 五、推理时的关键问题：视觉分支还跑不跑？

论文第 12 页有一句话非常关键：

> *"the key difference across these unified methods is not whether they all render full future videos online, but how much of the visual branch remains active during control."*

**翻译**：所有 Single-Backbone 方法在训练时都用了视频监督，但**推理时是否还要跑视频分支**——这才是它们真正的差异点。

### 三种推理策略对比

| 策略 | 推理时干什么 | 代表方法 | 优劣 |
|---|---|---|---|
| **A. 渲染完整视频** | 真的生成未来 RGB | 早期 UVA / Cosmos Policy 的 planning 模式 | 慢但可解释、可用于 planning |
| **B. 跑 latent，但不解码到像素** | 视频分支跑，但跳过最后的解码器 | UVA 的 direct policy 模式 | 中速，保留时序信息 |
| **C. 完全跳过视觉分支** | 推理时只算 action | GigaWorld-Policy、UWA 的 marginalize 模式、Fast-WAM | 最快，和纯 policy 一样 |

> 💡 **趋势**：越新的方法越倾向于 **C**——
> "训练时让视频教我，推理时把视频丢掉。"
> 这是为了在保留 video pretrain 的好处的同时，达到可部署的实时性。

---

## 六、用第 3 课的"切片视角"回看

回忆第 3 课的联合分布：

$$
p\bigl(o_{t+1:t+k},\; a_{t+1:t+k} \;\big|\; o_t,\; l\bigr)
$$

### IDM-Style 的处理（第 4 课）
**链式法则分解**，两步采样、两个独立模型：

$$
p(o, a \mid o_t, l) \;=\; \underbrace{p(o \mid o_t, l)}_{\text{Step 1: WM}} \cdot \underbrace{p(a \mid o, o_t)}_{\text{Step 2: IDM}}
$$

### Single-Backbone 的处理（今天）
**直接对联合分布建模**，一个模型一次性采样：

$$
p(o, a \mid o_t, l) \;=\; f_\theta(o_t, l) \quad \text{(一次前向同时吐 } o \text{ 和 } a \text{)}
$$

> 🎯 **同一个联合分布，IDM-Style 用"分而治之"，Single-Backbone 用"一锅炖"。**
> 数学上等价，工程实现完全不同。

---

## 七、和 IDM-Style 的全面对比表

把上节课和今天的内容并排对比，建议你截屏存手机：

| 维度 | IDM-Style（第 4 课） | Single-Backbone（今天） |
|---|---|---|
| **模型数** | 2 个独立模型 | 1 个共享 backbone |
| **联合分布的处理** | 链式法则两步采样 | 直接联合建模 |
| **训练目标数** | 2 个（WM loss + IDM loss） | 1 个（unified denoising loss） |
| **梯度流动** | WM 和 IDM 互不影响 | 全部参数共享梯度 |
| **推理流程** | 串行：先 WM 再 IDM | 一次前向 |
| **是否能"教" WM 学控制** | ❌ 不行（WM 只学画面分布） | ✅ 行（action loss 反向影响 WM） |
| **预训练 backbone 来源** | VGM（视频扩散模型） | VGM（视频扩散模型） |
| **典型推理瓶颈** | WM 的视频生成步骤 | 看选择哪种推理策略（A/B/C） |
| **可解释性** | 高（能看到 WM 想象的未来） | 中（看选择是否渲染） |

---

## 八、Table 1 第二组的横向对比（论文第 8 页）

| 方法 | 推理时的未来生成 | 耦合方式 |
|---|---|---|
| UVA | Joint latent prediction | Shared backbone |
| UWA | Joint diffusion process | Shared backbone |
| VideoVLA | Joint video rollout | Shared backbone |
| VideoPolicy | Video policy substrate | Shared backbone |
| **Cosmos Policy** | **Parallel action/state/value outputs** | **Shared backbone** |
| DreamZero | Chunk-wise joint rollout | Shared backbone |
| UD-VLA | Synchronous denoising | Shared backbone |
| GigaWorld-Policy | Optional visual branch | Shared backbone |

> 📌 **共同点**：全部都是 VGM backbone + 完全的参数共享
> **差异点**：推理时视觉分支的"存在感"——从必跑（UVA）到可选（GigaWorld-Policy）

---

## 九、优点和缺点

### ✅ 优点（相比 IDM-Style）

1. **联合训练**：动作梯度可以反向影响 video 生成，让 WM 自动学会生成"对决策有用"的画面
2. **接口灵活**：通过 timestep / decoder head / 因果掩码，**同一个模型**能在 "纯 policy / WM / 联合"之间切换
3. **充分利用预训练**：直接复用 video diffusion backbone，不浪费

### ❌ 缺点

1. **训练成本巨大**：一个模型要同时学好两件事，梯度可能打架，对数据量和算力要求极高
2. **架构耦合很死**：视频和动作完全共享参数，无法针对各自的频率/精度需求做差异化优化
   （比如视频是 10Hz、动作要 100Hz，强行用一个 backbone 处理会牺牲一边）
3. **预训练 backbone 的选择限制**：必须用 video diffusion 类的 backbone，不能轻易换成 VLM

> 🔑 **缺点 ② 正是下节课 MoE/MoT 范式要解决的核心问题**——
> "我们能不能既享受联合训练的好处，又保留视频和动作各自的专家化？"

---

## 十、一句话总结今天

> 🎓 **Single-Backbone = 把"未来画面"和"未来动作"塞进同一个生成过程，一个 backbone 通吃。
> 它的核心信念是："video diffusion backbone 自带时序物理先验，把 action 当成额外一帧让它顺手画出来就行。"
> 优雅、紧耦合、能联合训练，但牺牲了视频和动作各自的差异化优化空间。**

---

## ✅ 课后检查（这次建议至少答 Q1 和 Q2，让我看你能否清晰对比两种范式）

### Q1（必答 · 对比题）
请你**用一段话**说清楚：IDM-Style 和 Single-Backbone 在数学上和工程上的核心差异是什么？
（提示：用第 3 课的"联合分布切片"框架来说，效果最好）

### Q2（必答 · 推理题）
论文说 Single-Backbone 的方法越来越倾向于"训练时用视频监督，推理时丢掉视觉分支"（如 GigaWorld-Policy）。
请你想想：
- 这种做法**为什么工程上合理**？
- 这种做法**有什么潜在风险**？（提示：如果丢掉视觉分支，那些"为视频建模学到的能力"还在吗？）

### Q3（选答 · 思辨题）
Cosmos Policy 把 action / future state / value 都当作"额外的 latent frame" 塞进 video diffusion 序列里。
你觉得这种"什么都是 frame"的哲学，**未来还能扩展到什么**？比如能不能塞进去：
- 触觉信号？
- 力反馈？
- 高层规划符号？
- 甚至机器人的"自身状态"（电量、温度、关节扭矩）？
说说你的想法。

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
> -
> -
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -

---

**下一课预告**：
**第 6 课 — 范式 3：MoE/MoT（专家分工）**

下节课你会看到一个介于 IDM-Style 和 Single-Backbone 之间的"中间路线"：
**保留视频专家 + 动作专家的独立性，但让它们通过共享 attention 深度交互。**
代表作：Motus、GE-Act、LingBot-VA、BagelVLA。
看完后你会理解：**为什么 π0 风格的"双专家"设计可以无缝迁移到 video-pretrained 上下文。**
