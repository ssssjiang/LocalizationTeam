# 📘 第 7 课：范式 4 —— Unified VLA（把 WM 内化进 VLA）

> 对应论文章节：**Sec 3.5 + Fig. 4(a) + Table 1 第四组**（第 13–14 页）
> 学习目标：理解一种"反方向"的设计哲学——不在 VLA 旁边加 WM，而是让 VLA 自己长出 WM 的能力。

---

## 0. 30 秒温习前 3 课（一定要先复习一下，否则这节课容易混）

| 范式 | Backbone 来源 | 怎么处理 future prediction |
|---|---|---|
| 第 4 课 IDM-Style | **VGM**（视频扩散模型） | 一个独立的 WM 显式生成未来视频 |
| 第 5 课 Single-Backbone | **VGM** | 一个共享 backbone 同时生成视频和动作 |
| 第 6 课 MoE/MoT | **VGM** | 视频专家 + 动作专家，共享 attention |

注意一个**重要事实**：
> 🎯 **前 3 种范式的 backbone 都是 VGM——也就是说，它们的"母体"是视频生成模型。**

---

## 一、今天范式的"反方向"出发点

第 7 课的 Unified VLA 选择了**完全相反的路线**：

> 🎯 **以 VLA（VLM-based）为母体，把 WM 能力当作"内化的副产品"长出来。**

论文第 13 页 Fig. 4(a) 长这样（我用文字画出来）：

```
                ┌──────────────────────────────────────┐
观察 ──▶│                                                  │
       │       Unified Multimodal Model (UMM/MLLM)        │
指令 ──▶│       例如 LLaVA / Qwen-VL 风格的 backbone        │
       │                                                  │
       └──────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
        Action 输出     Future 图像 / latent    文本推理
        (主任务)        (辅助任务)             (可选)
```

**关键差异**：
1. **Backbone 不是视频扩散模型**，而是 **MLLM**（多模态大模型）
2. **Future prediction 不是必需的输出**，而是**训练时的辅助任务**
3. **WM 不是外挂模块**，而是 **VLA backbone 内部"长出来"的能力**

---

## 二、一句话定义这个范式

> 🎯 **Unified VLA = 让 VLA 在训练时除了学"输出动作"，还学"预测未来"，
> 把这两件事放进同一个 MLLM backbone 里联合优化。**

注意三个关键词：
- **Unified**（统一）：observation / language / action / future 全在同一个模型里
- **VLA-based**：母体是 VLA，不是视频生成模型
- **内化**（internalized）：未来预测是模型的"内在能力"，不是外挂

---

## 三、和前 3 种范式的对比（这节课最重要的一张表）

我把 4 种范式放在一起，让你瞬间看清差异：

| 维度 | 第 4 课 IDM-Style | 第 5 课 Single-Backbone | 第 6 课 MoE/MoT | **第 7 课 Unified VLA（今天）** |
|---|---|---|---|---|
| **Backbone 母体** | VGM | VGM | VGM | **MLLM / VLM** |
| **Future prediction** | 必须显式生成 | 可选生成（联合输出） | 可选生成（专家分工） | **多为训练时辅助 loss** |
| **WM 是外挂还是内化** | 外挂（独立模型） | 强耦合（同一个 backbone） | 半外挂（专家） | **完全内化（VLA 自带能力）** |
| **推理时是否一定跑 WM** | ✅ 必须 | 看选择 | 看选择 | **❌ 通常不必** |
| **训练目标数** | 2 个独立 | 1 个统一 | 1 个统一（多专家） | **2 个 multi-task loss** |
| **典型代表** | UniPi、VPP | Cosmos Policy、UVA | Motus、GE-Act | **GR-1、WorldVLA、UniVLA** |

> 🔑 **一句话区分**：
> - 前 3 课：**"video model + action head"** —— 视频生成是主，动作是辅
> - 第 7 课：**"VLA + future prediction head"** —— 动作是主，未来预测是辅

---

## 四、为什么这种范式有道理？

论文 Sec 3.5 没有给出一个"非这么做不可"的理由，但你可以反推出它的两个核心动机：

### 动机 ①：不浪费已有的 VLA 工程基建
过去 2 年整个领域积累了大量 VLA 工程经验：
- 数据 pipeline（Open X-Embodiment、DROID）
- 训练框架（OpenVLA、LeRobot）
- 评测协议（LIBERO、CALVIN、SIMPLER）

如果你已经有一个能跑的 VLA，**为什么要从头训一个 video diffusion 模型**？
更聪明的做法是：在现有 VLA 上**加一个 future prediction 的 auxiliary loss**——花极小的代价，拿到 WM 的好处。

### 动机 ②：Future prediction 是"免费的监督信号"
机器人数据本身就有"下一帧画面"——你不用额外标注，就有了天然的预测目标。

> 💡 **关键洞察**：
> 你训练 VLA 预测 action 的时候，**反正模型也在看图像**——
> 让它顺手预测一下"这个 action 执行后图像会变成什么"，**几乎不增加成本**。
> 而这个预测任务会强制 backbone 学到 **action-aware** 的表征，反过来又能让 action 预测更准。

这是经典的 **multi-task learning** 思想——一个辅助任务通过共享表征改善主任务。

---

## 五、3 个子类（论文 Sec 3.5 的内部分类）

论文把 Unified VLA 进一步分成 3 个子类，按"未来预测的具体形式"区分：

### 子类 ①：显式未来图像预测（Pixel-level Prediction）

**核心思路**：直接预测**未来的图像**作为辅助任务。

| 方法 | 关键设计 |
|---|---|
| **GR-1**（Wu et al., 2024） | 早期代表。GPT-style transformer，**联合预测 action 和 future image** |
| **UP-VLA**（Zhang et al., 2025c） | 类似 GR-1，但用 future-image prediction 同时改进 action 和**视觉泛化** |
| **WorldVLA**（Cen et al., 2025） | 在一个**自回归框架**里统一 action 和 image 的理解+生成；future-image prediction **主要作为训练信号**，推理时不强制输出 |

> 💡 **WorldVLA 的设计哲学很值得记**：
> "在训练时用 image prediction 强化表征，在推理时把 image 输出关掉以省算力。"
> 这是 multi-task learning 最经典的用法。

### 子类 ②：Latent / 隐式未来建模（Compact Representation）

**核心思路**：不预测像素，而是预测**紧凑的未来表征**。

| 方法 | 关键设计 |
|---|---|
| **DreamVLA**（Zhang et al., 2025e） | 预测**结构化的世界知识**（动态、空间、语义线索），而非像素 |
| **UniVLA**（Wang et al., 2025） | 在**post-training 阶段**加入 world modeling，让模型从大规模视频里吸收因果动力学，不引入额外的外部 WM |
| **CoWVLA**（Yang et al., 2026a） | 预测 **latent motion + 紧凑视觉目标**，而非冗余的 future frames |

> 💡 **为什么很多新工作转向 latent prediction？**
> 像素级预测有 90% 的信息和决策无关（背景、光照），latent 预测**信噪比更高、训练更稳定**、推理也更快。
> （这和第 4 课讲的 IDM-Style 演化阶段 B 是同一种思想）

### 子类 ③：多专家 / 多系统统一模型

**核心思路**：在**任务和训练层面**统一，但**架构内部**保留专家分工。

| 方法 | 关键设计 |
|---|---|
| **F1**（Lv et al., 2025） | 用 MoT 架构，**预测未来视觉状态作为 planning target** |
| **InternVLA-A1**（Cai et al., 2026） | 轻量 latent visual foresight + 联合优化 foresight 和 action |
| **HALO**（Shou et al., 2026） | 推到 **visual subgoal prediction + embodied reasoning** |
| **TriVLA**（Liu et al., 2025d） | 把 grounding / episodic dynamics / control 组织成**协调的子系统** |

> ⚠️ **注意区分**：
> 这个子类**长得很像第 6 课的 MoE/MoT**——都是"多专家"。
> **关键差异**是：第 6 课的 MoE/MoT backbone 是 video diffusion，这里是 MLLM；
> 而且这里的"future prediction"被看作 **VLA 内部的一个 subgoal/foresight 模块**，不是独立的视频生成器。

---

## 六、用第 3 课的"切片视角"回看

第 3 课的联合分布：

$$
p\bigl(o_{t+1:t+k},\; a_{t+1:t+k} \;\big|\; o_t,\; l\bigr)
$$

### Unified VLA 怎么处理这个分布

它**不直接建模这个联合分布**，而是把它**拆成两个 multi-task loss**：

$$
\mathcal{L}_{\text{total}} \;=\; \underbrace{\mathcal{L}_{\text{action}}\bigl(\pi(a \mid o_t, l)\bigr)}_{\text{主任务}} \;+\; \lambda \cdot \underbrace{\mathcal{L}_{\text{future}}\bigl(p(o_{t+1} \mid o_t, l)\bigr)}_{\text{辅助任务}}
$$

注意：
- **主任务**：标准的 VLA action prediction loss
- **辅助任务**：未来预测 loss（pixel / latent / 结构化都可以）
- **$\lambda$**：辅助任务的权重，是个超参数

> 🎯 **这种范式的本质 = multi-task learning + 共享 backbone**：
> 通过共享 backbone 的隐式约束，让 future prediction 和 action prediction 互相改进。
>
> 它**不像** Single-Backbone 那样把 $o$ 和 $a$ 拼接成同一个去噪目标，
> 也**不像** IDM-Style 那样用链式法则两步采样。
> 它更像传统的 **auxiliary task learning**——一个老 trick 被用在了新场景。

---

## 七、和 Single-Backbone 的"长得像但本质不同"

很多人会问：**Unified VLA 和 Single-Backbone 不是都"一个 backbone 通吃"吗？差别在哪？**

我用一张细粒度对比表回答：

| 维度 | Single-Backbone（第 5 课） | Unified VLA（今天） |
|---|---|---|
| Backbone 类型 | Video Diffusion Transformer (DiT) | MLLM / VLM |
| 训练范式 | 一个统一的 denoising loss | Multi-task loss（action + future） |
| Future 和 action 的关系 | 拼接成同一个去噪目标 $x = [z_v; z_a]$ | 两个独立的 head 输出 |
| 推理时输出 | 一次去噪过程同时吐出未来和动作 | 通常只走 action head，future head 关闭 |
| 数学本质 | 直接联合建模 $p(o, a)$ | Multi-task：$\mathcal{L}_a + \lambda \mathcal{L}_o$ |
| 工程哲学 | "把动作当 frame" | "把 future 当辅助监督" |

> 🔑 **一句话区分**：
> - **Single-Backbone**：动作和未来是**同一个生成过程**的两个产物
> - **Unified VLA**：动作是主，未来是**为了让动作学得更好的辅助监督**

---

## 八、Table 1 第四组的横向对比（论文第 8 页）

| 方法 | 推理时的未来生成 | Backbone | 耦合方式 |
|---|---|---|---|
| **GR-1** | Future image prediction | UMM | Joint co-training |
| **UP-VLA** | Future image prediction | UMM | Joint co-training |
| **WorldVLA** | Future image (mainly train-time) | UMM | Joint co-training |
| **DreamVLA** | Structured world knowledge | UMM | Joint co-training |
| **UniVLA** | Latent world modeling | UMM | Joint co-training |
| **CoWVLA** | Latent dynamics | UMM | Joint co-training |
| **F1** | Visual foresight | UMM | Unified MoT |
| **InternVLA-A1** | Latent foresight | UMM | Unified MoT |
| **HALO** | Visual subgoal prediction | UMM | Unified multi-expert |
| **TriVLA** | Episodic dynamics | UMM | Multi-system |

> 📌 **共同点**：全部 backbone 都是 UMM（Unified Multimodal Model）/ MLLM，不是 VGM
> **差异点**：未来预测的"形式"——pixel / latent / 结构化 / subgoal

---

## 九、Unified VLA 的优缺点

### ✅ 优点

1. **复用 VLA 基建**：现有 OpenVLA / π0 工程链可以直接微调
2. **训练成本可控**：不需要从头训 video diffusion，加个辅助 head 就行
3. **推理速度快**：通常推理时只跑 action head，速度和纯 VLA 一样
4. **数据利用率高**：机器人数据本身就有 next-frame，不用额外标注

### ❌ 缺点

1. **Future prediction 能力上限低**：因为是"辅助任务"，所以 future 预测不会非常精细
2. **不适合做 imagination-driven planning**：辅助 loss 只够监督表征，不足以支撑"在脑内 rollout"
3. **依赖 backbone 的能力**：MLLM backbone 不像 video diffusion 自带强时序先验，长时序预测能力较弱
4. **辅助任务权重难调**：$\lambda$ 的取值会显著影响最终效果，缺乏理论指导

> 🔑 **何时该用、何时不该用**：
> - 用：你的目标是**改进 action 预测的精度和泛化**，不需要可解释的"未来视频"
> - 不用：你需要"让机器人在脑内 rollout 多个候选方案"——这种需求请用前 3 课的范式

---

## 十、把 4 种范式放进一张"全景图"

这是过去 4 节课的总结，建议你截屏存手机：

```
─────────────────────────────────────────────────────────────
           按"WM 与 Policy 的耦合程度"排序
─────────────────────────────────────────────────────────────

完全外挂 ───────── 紧耦合 ──────────── 完全内化
   │                  │                      │
IDM-Style    Single-Backbone   MoE/MoT   Unified VLA
(第 4 课)      (第 5 课)       (第 6 课)    (第 7 课)
   │                  │                      │
2 个独立     1 个 backbone   2 个专家     1 个 VLA
模型流水    完全共享参数   共享 attn    + auxiliary loss
   │                  │                      │
VGM          VGM            VGM          MLLM ⭐
(母体)       (母体)         (母体)       (母体不同！)
   │                  │                      │
推理必跑     推理可选       推理可选     推理通常不跑
WM           WM             WM           WM
   │                  │                      │
   └──── 用来 imagination planning ────┘   只用来改进 action
                                          表征
```

⭐ Unified VLA 是唯一**不以 video diffusion 为母体**的范式——这是它的根本特色。

> 🔑 **一个隐藏洞察**：
> 这 4 种范式不是"哪种更好"的问题，而是 **"WM 在你的系统里扮演什么角色"** 的问题：
> - 当 simulator → 选 IDM-Style 或 MoE/MoT
> - 当 controller's other half → 选 Single-Backbone
> - 当 representation regularizer → 选 Unified VLA

---

## 十一、一句话总结今天

> 🎓 **Unified VLA = 不在 VLA 旁边加 WM，而是让 VLA 通过 multi-task learning 内化未来预测能力。
> 它的本质是把"future prediction"当作 auxiliary loss，
> 用极小的工程代价拿到 WM 的核心好处——更好的时序表征、更强的 action 预测。
> 推理时通常不真跑 WM，只把 WM 当作训练时的"免费监督信号"。**

---

## 十二、给你一个"工程感"对比

如果你要落地一个 Unified VLA 系统，工作量大致是这样：

| 工作 | 工作量 | 说明 |
|---|---|---|
| 拿一个现有 VLA（如 OpenVLA） | 小 | HuggingFace 开箱即用 |
| 加一个 future prediction head | 中 | 需要设计 head 结构和 loss |
| 修改训练 pipeline | 中 | 加 next-frame 监督，调 $\lambda$ |
| 训练 / 微调 | 中 | 比纯 VLA 多 30%-50% 计算 |
| 部署推理 | **极小** | 只跑 action head，速度同 VLA |

> 💡 **这是 4 种范式里"投入产出比最划算"的一种**——
> 加 30% 训练成本，换来更好的 action 表征，**推理不变慢**。
>
> 这就是为什么 GR-1 / WorldVLA / UniVLA 这一系列工作能持续涌现，且很多公司项目里都能看到这种设计。

---

## ✅ 课后检查（这次一定要至少答 Q1 和 Q2，因为你已经累积了足够多的范式知识）

### Q1（必答 · 跨范式对比）
请你用**两段话**分别说明：
- (a) Unified VLA 和 IDM-Style（第 4 课）的本质差异是什么？
- (b) Unified VLA 和 Single-Backbone（第 5 课）的本质差异是什么？

（提示：从 backbone、训练目标、推理流程三个维度切入）

### Q2（必答 · 选型题）
现在你是某机器人公司的 ML 工程师，下面这几个项目，你会选哪种范式？说明理由。

- **(a)** 公司已经有一个 OpenVLA 上线，希望"在不增加推理延迟"的前提下提升 5% 成功率
- **(b)** 公司想做一个"机器人脑内 rollout 多种抓取策略，选最优的执行"的 demo
- **(c)** 公司只有少量演示数据，但想充分利用互联网上的大规模视频做预训练
- **(d)** 公司要做一个 200Hz 的高频精确控制系统，每毫秒都不能等

### Q3（选答 · 思辨题）
论文说 Unified VLA 的 future prediction 主要是 **train-time auxiliary loss**，推理时通常关掉。
但这听起来像是"用 future 教模型做表征学习"，**和经典的 self-supervised learning 有什么本质区别吗**？
（提示：考虑预测目标 vs 输入数据、是否需要 action 标签）

---

## 📝 我的回答（你来填）

> Q1:
> - (a)
> - (b)
>
> Q2:
> - (a)
> - (b)
> - (c)
> - (d)
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -

---

**下一课预告**：
**第 8 课 — 范式 5：Latent-Space WM（不画像素，只在表征空间预测）**

下节课你会看到 Sec 3 的最后一种范式——**和今天有点像，但更激进**：
**完全放弃在像素或 latent 视频空间预测，把所有未来建模都搬到 representation space 里做。**
代表作：FLARE、VLA-JEPA、JEPA-VLA、WoG、DIAL。
看完后你会理解：**为什么 Yann LeCun 一直坚持 JEPA 路线，以及它在机器人领域的最新落地方式。**
