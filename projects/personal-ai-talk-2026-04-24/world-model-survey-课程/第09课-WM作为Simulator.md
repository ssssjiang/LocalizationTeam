# 📘 第 9 课：World Model as Simulator（替代真机 RL 与 Policy 评测）

> 对应论文章节：**Sec 4 + Fig. 5 + 公式 (16)–(19)**（第 15–18 页）
> 学习目标：理解从"WM 是 policy 的一部分"到"WM 是 policy 的环境"这个**重大视角转换**；看清 WM 在 RL 和 Evaluation 两种新角色里的设计逻辑。

---

## 0. 重要提醒：今天的视角和前 5 节课**完全不同**

第 4–8 课，我们一直在讨论这个问题：

> "WM 怎么和 policy 耦合，让 policy 表现更好？"

——WM 是 policy 的**一部分**或**辅助**。

但今天 Sec 4 讨论的是一个**完全不同的角色**：

> 🎯 **WM 不再是 policy 的一部分，而是 policy 的"虚拟训练场"和"虚拟考官"。**

这是一个**重大的视角转换**——同样的 WM，扮演完全不同的角色，会带来完全不同的设计哲学。

---

## 一、用一个类比抓住今天的核心

### 前 5 课：WM 是 policy 的"军师"
机器人决策时，有个军师（WM）在旁边告诉它"未来会怎样"。
机器人 = policy，军师 = WM，**两者一起做决策**。

### 今天：WM 是 policy 的"训练场 + 考场"
机器人去虚拟训练场练习（RL），或者去虚拟考场被考核（Evaluation）。
**机器人不知道这是虚拟的，它以为这就是真实世界。**
机器人 = policy，训练场/考场 = WM，**WM 替代了真实物理世界**。

> 🔑 **同一个 WM，前 5 课它是"队友"，今天它是"环境"。**

---

## 二、为什么这个视角转换这么重要？

回答这个问题，你需要先理解一个机器人领域的**长期痛点**：

### 真机 RL 的"四大酸甜苦辣"

| 维度 | 真机 RL | 学习的代价 |
|---|---|---|
| **慢** | 一次真机 rollout 几秒钟 | RL 需要百万次交互，等到天荒地老 |
| **贵** | 机器人坏了要赔钱 | 训练失败可能毁机器人 |
| **难重置** | 物体推到桌外要人去捡 | 没有"reset()" 函数 |
| **危险** | 某些任务可能伤人 | 部署受限 |

而**纯模仿学习**的痛点是：
- 只能模仿已有演示，**学不到失败 → 改正**的经验
- 演示数据采集贵
- 数据天花板锁死性能上限

> 🎯 **这就是 WM as Simulator 的全部动机**：
> **既然真机 RL 又慢又贵又危险，那就在 WM 里做 RL；**
> **既然评估真机 policy 要重复部署，那就在 WM 里做 evaluation。**

WM 在这里扮演的是 **"低成本、可控、可重复、安全"** 的虚拟环境。

---

## 三、Sec 4 的两条主线（Fig. 5）

论文第 16 页 Fig. 5 把今天的内容分成两条主线：

```
Sec 4.1: WM for RL                  Sec 4.2: WM for Evaluation
──────────────────────              ──────────────────────────
                                                  
World Model ←──→ Policy            World Model ←─── Policy
   (作为环境)      (在里面学习)         (作为评估器)    (生成候选动作)
        │              │                  │              │
        └──── update ──┘                  └─── score ────┘
        
"我在 WM 里跑 RL"                  "我用 WM 给 policy 打分"
```

注意 Fig. 5 的关键点：
- **左边**：WM 提供 imagined transitions，policy 根据 reward 更新
- **右边**：policy 提出多个候选 action，WM 分别 rollout 给它们打分

---

## 四、Sec 4.1：WM for Reinforcement Learning

### 一句话定义

> 🎯 **不在真机上做 RL，而在 WM 里做 RL：让 policy 在"想象"中学习。**

### 数学形式（论文公式 (16)）

WM 提供 imagined transitions（论文公式 16）：

$$
(\hat{o}_{t+1},\; \hat{r}_t,\; \hat{d}_t) \;\sim\; p_\phi\bigl(\cdot \mid o_{\le t},\; a_{\le t},\; l\bigr)
$$

各符号含义：
- $\hat{o}_{t+1}$：想象的下一帧观测
- $\hat{r}_t$：想象的奖励信号（**WM 不仅生成画面，还估计奖励**）
- $\hat{d}_t$：想象的终止信号（任务完成 / 失败）
- $p_\phi$：参数化的 WM

注意一个新东西：**WM 不只生成画面，还要估计奖励**。
这是它从"画面预测器"升级为"环境模拟器"的关键。

### 标准 RL 目标

policy 在这个 imagined environment 里**最大化期望回报**：

$$
J(\theta) \;=\; \mathbb{E}_{\hat{\tau} \sim (\pi_\theta,\, p_\phi)} \left[\sum_t \gamma^t \hat{r}_t\right]
$$

或者用 PPO/GRPO-style 的 surrogate loss（论文公式 18）：

$$
\mathcal{L}_{\text{RL}}(\theta) = -\mathbb{E}_t \left[\min\bigl(r_t(\theta) \hat{A}_t,\; \text{clip}(r_t(\theta),\, 1-\epsilon,\, 1+\epsilon) \hat{A}_t\bigr)\right]
$$

> 💡 **不要被这些公式吓到**——它们就是经典 PPO/GRPO，只是 environment 被换成了 WM。
> **WM as Simulator 的核心创新不在 RL 算法，而在 environment 的来源。**

---

## 五、Sec 4.1 的两个发展层级（这是这一节最重要的洞察）

论文 Sec 4.1 把这条主线分成两个发展阶段：

### 第一层级：把 WM 当**固定 simulator** 跑 RL

**核心做法**：先训好一个 WM，然后冻结它，让 policy 在这个静态 WM 里做 RL。

代表作（按时间排序）：

| 阶段 | 方法 | 核心贡献 |
|---|---|---|
| 早期奠基 | **UniSim** (Yang et al., 2024a) | 早期把 video model 当 simulator 的尝试 |
| 早期奠基 | **World-Env** (Xiao et al., 2025) | 标准化"WM + reward generation" 配方 |
| 早期奠基 | **VLA-RFT** (Li et al., 2025b) | 把这个范式系统应用于 VLA 后训练 |
| 拓展 | **DiWA** (Chandra et al., 2025) | 用 frozen WM 做完全 offline 的 diffusion policy 适配 |
| 拓展 | **World4RL** | 用 diffusion world model 做高保真操作精炼 |
| VLA 适配 | **WMPO** (Zhu et al., 2026) | 强调 pixel-space imagination + on-policy GRPO |
| VLA 适配 | **ProphRL** | 适配 flow-based action heads |
| VLA 适配 | **RISE** | 加入 compositional dynamics + progress-value |
| Scale 化 | **GigaBrain-0.5M** (Team et al., 2026) | 把 WM-based RL 推到大规模 VLA 适配 |

**统一特征**：WM 是固定的，policy 自己在里面学。

### 第二层级：WM 也得改进——**Policy 和 WM 协同进化**

**核心洞察**：

> ⚠️ "WM 是固定的"这个假设在实践中**根本站不住脚**。
> WM 训完之后只是一个**当时数据分布上**的近似。
> 当 policy 越学越好，它会去到 WM **从未见过的状态**——这时 WM 的预测就不可信了。

代表作：

| 方法 | 核心创新 |
|---|---|
| **World-VLA-Loop** (Liu et al., 2026b) | **联合预测 future obs + reward**，用 policy 失败的 rollout **反过来 refine simulator** |
| **VLAW** (Guo et al., 2026a) | **迭代修复-改进策略**：交替用真实数据 refine WM，用合成数据 improve VLA |
| **WoVR** (Jiang et al., 2026) | 把 simulator reliability 当作核心瓶颈，提出 controllable action-conditioned video modeling、Keyframe-Initialized Rollouts、和**WM-Policy co-evolution** |

**WoVR 的协同进化公式（论文公式 19）**：

$$
\phi_{k+1} \leftarrow \text{UpdateWM}\bigl(\phi_k,\; \mathcal{D}_{\text{real}} \cup \mathcal{D}_{\text{policy}}(\pi_{\theta_k})\bigr)
$$

$$
\theta_{k+1} \leftarrow \text{UpdatePolicy}\bigl(\theta_k,\; \hat{\mathcal{D}}(\phi_{k+1})\bigr)
$$

**白话翻译**：
- **第 k 轮**：用真实数据 + 当前 policy 跑出的轨迹 → 更新 WM
- **第 k 轮**：用更新后的 WM → 生成想象数据 → 更新 policy
- **第 k+1 轮**：循环往复

> 🎯 **这是 2026 年这一支最新、最热的方向**：
> **WM 和 policy 不再是"老师和学生"，而是"互相教对方的同伴"。**

---

## 六、Sec 4.2：WM for Evaluation（这一节同样重要）

### 一句话定义

> 🎯 **WM 不只用来训练 policy，还用来评估 policy：在执行前先"在脑内试一遍"，看哪个候选最好。**

### 4 种典型的评估方式

#### 方式 ①：基于 rollout 的候选打分

**做法**：
1. policy 提出 N 个候选 action sequence
2. WM 分别 rollout 这 N 个候选，预测各自的未来
3. 选预测最好的那个执行

**代表**：
- **GPC** (Qi et al., 2026) — 不重训 policy，直接给 frozen policy 加一个 WM 在部署时排序候选
- **IRASim** (Zhu et al., 2025b) — 模拟多个候选轨迹，选预测 value 最高的
- **World-in-World** (Zhang et al., 2025a) — 闭环规划：rollout → 评估 → 修正
- **DreamPlan** — 把这套逻辑变成训练信号（构造 preference pairs）

#### 方式 ②：把 WM 当作 MPC 的动力学

**做法**：不只是从几个候选里选，而是用 WM 的可微动力学**主动优化**整段动作序列。

**代表**：
- **TD-MPC2** (Hansen et al., 2024) — latent-space MPC 的代表
- **LeWorldModel** (Maes et al., 2026) — 简化的 JEPA 风格端到端 MPC

> 💡 **这相当于把 WM 从"判官"升级为"导航地图"**——可以在它身上做梯度优化。

#### 方式 ③：把 WM 当作 Policy Evaluator

**做法**：不评估单个动作，而是用 WM **对比不同 policy** 的表现。

**代表**：
- **Veo World Simulator** (Team et al., 2025a) — Google 用 Veo 做 Gemini Robotics 的离线评估
- **WorldEval** (Li et al., 2025e) — 研究 WM 能否作为真机评估的 scalable proxy
- **WorldArena** (Shang et al., 2026) — 把 policy evaluation 列为 WM 的核心下游用途

#### 方式 ④：给 WM 加显式 feedback head

**做法**：WM 不只生成画面，还输出 reward / progress / completion 信号。

**代表**：
- **World-Env** — augment with reward + termination prediction
- **VLA-RFT** — verified rewards on imagined trajectories
- **World-VLA-Loop** — 联合预测 obs + reward
- **RISE** — 引入 progress value model 做 task advancement scoring

---

## 七、一个关键警告：**Action Faithfulness 和 Rollout Reliability**

论文 Sec 4.2 末尾有一段非常重要的提醒，**这是这节课最深刻的洞察**：

> ⚠️ **WM as Evaluator 的有效性，完全取决于它的 imagined rollout 是否"动作忠实 + 长时序可靠"。**
> **如果 WM 的预测看起来很真但根本不响应 action（hallucination），它的评估信号就是垃圾。**

举个例子：
- WM 预测了一段未来：机器人成功抓到了杯子
- 但实际上无论 policy 给什么 action，WM 都会预测"成功抓到杯子"——它**和 action 无关**地输出了乐观的未来
- 在这种 WM 上做评估，所有 policy 都被打高分——**完全无意义**

代表性论证：
- **Ctrl-World** (Guo et al., 2026b) — 论证 action-faithful rollout 才能支持 evaluation
- **WoVR** (Jiang et al., 2026) — 强调 hallucination 不只降低视觉质量，更**直接破坏评估信号**

> 🎯 **这就是为什么第 1 课就反复强调 "action-conditioned" 这个性质——**
> 它不是一个抽象的优雅性质，而是 WM as Simulator 的**实用前提**。

---

## 八、Sec 4 的全景图：WM 在两种角色里的演化

```
═══════════════════════════════════════════════════════════════════
              Sec 4: WM as Simulator 的两条主线
═══════════════════════════════════════════════════════════════════

      Sec 4.1: WM for RL                Sec 4.2: WM for Evaluation
   ────────────────────────         ─────────────────────────────
                                                          
   第一层级：固定 WM + RL          ① Rollout-based candidate scoring
   ────────────────────────             GPC, IRASim, World-in-World
   World-Env, VLA-RFT,                                              
   WMPO, RISE, ...                  ② MPC over WM dynamics
                                        TD-MPC2, LeWorldModel        
                                                                     
   第二层级：协同进化               ③ WM as policy evaluator
   ────────────────────────             WorldEval, Veo Sim, WorldArena
   World-VLA-Loop                                                    
   VLAW                              ④ Explicit feedback head        
   WoVR (公式 19)                       World-Env, VLA-RFT, RISE     
                                                                     
                  ↓
   核心警告：Action Faithfulness + Rollout Reliability
   (Ctrl-World, WoVR)
═══════════════════════════════════════════════════════════════════
```

---

## 九、用第 3 课的"切片视角"回看 Sec 4

回忆第 3 课的联合分布：

$$
p\bigl(o_{t+1:t+k},\; a_{t+1:t+k} \;\big|\; o_t,\; l\bigr)
$$

### Sec 3 的范式 vs Sec 4 的用法

| Sec | 切片角色 | 干啥用 |
|---|---|---|
| **Sec 3** | 利用切片关系**优化 policy 的内部结构** | 让 policy 决策时更"远见" |
| **Sec 4.1** | 用 Controllable WM 切片 $p(o \mid o_t, a)$ + reward 估计 | 当 RL 环境，提供 transition 和 reward |
| **Sec 4.2** | 用 Controllable WM 切片对候选 action **打分** | 评估 policy / 选最优候选 |

> 🎯 **核心差异**：
> Sec 3 关心 **"WM 怎么帮 policy 学得更聪明"**；
> Sec 4 关心 **"WM 怎么替代真机的 environment role"**。
>
> **同一个 controllable world model 切片，在两个 section 里扮演完全不同的角色。**

---

## 十、Sec 4 的优缺点

### ✅ 优点

1. **极度低成本**：一次想象 rollout 比真机便宜千倍
2. **安全**：无论 policy 多差，机器人不会真坏
3. **可重复**：完全相同的初始状态可以反复测试
4. **大规模并行**：可以在云端同时跑几千个 imagined rollout
5. **对评估特别有价值**：避免反复部署到真机

### ❌ 缺点

1. **Sim-to-Real Gap**：WM 学到的不是真实物理，而是"近似物理"
2. **Hallucination 致命**：第七节讲的 action faithfulness 问题
3. **训练 WM 本身贵**：你省了真机 RL 的成本，但欠了训 WM 的成本
4. **WM 必须持续更新**：第二层级的协同进化已经验证了这一点
5. **长时序漂移**：rollout 越长越不准，限制了 horizon

---

## 十一、把第 9 课和前 8 课连起来：WM 的"双重身份"

这是这节课最值得记住的一句话：

> 🔑 **同一个 WM，可以同时扮演两种身份：**
> - **作为 policy 的一部分**（Sec 3，第 4–8 课）：帮 policy 决策
> - **作为 policy 的环境**（Sec 4，今天）：让 policy 学习/被评估
>
> **未来的趋势是这两种身份逐渐融合**——
> 一个 WM 既被用来 augment policy，又被用来 train/evaluate policy。
> 你在 GigaWorld、Cosmos 这种 foundation 工作里已经能看到这种融合。

---

## 十二、一句话总结今天

> 🎓 **WM as Simulator = WM 的"第二种身份"——不是 policy 的一部分，而是 policy 的环境。
> 它替代真机做 RL，也替代真机做评估。
> 第一层级是"WM 是固定 simulator"，第二层级是"WM 和 policy 协同进化"。
> 它的价值不在生成漂亮视频，而在生成"可信任的、动作忠实的、长时序可靠的"未来——
> 这才是真正能替代真机的 simulator 该有的样子。**

---

## ✅ 课后检查（这次至少答 Q1 和 Q2，为下一课做铺垫）

### Q1（必答 · 视角转换题）⭐⭐⭐
请你**用一段话**说清楚：
- Sec 3 里的 WM 和 Sec 4 里的 WM，**用法上**有什么本质区别？
- 同一个 controllable world model，在两个 section 里**扮演的角色**有什么不同？

### Q2（必答 · 设计题）
你公司想做一个"机器人在虚拟环境里 RL 训练"的项目，目标是把训练成本降低 100 倍。
请你回答：
- **(a)** 你会选第一层级（固定 WM + RL）还是第二层级（协同进化）？为什么？
- **(b)** 你会怎么验证你的 WM 是 "action-faithful" 的？给一个具体的检查方法。
- **(c)** 你预计这个项目最大的风险是什么？

### Q3（选答 · 思辨题）
论文 Sec 4.2 引入了一个有趣的视角：**WM 不只能当 RL 环境，还能当 policy evaluator——直接对比不同 policy/checkpoint。**
但如果两个 policy 在同一个 WM 上的相对表现 **真的能反映** 在真机上的相对表现——
那是否意味着我们可以**完全告别真机评测**？还是说这是一个"理想但永远做不到"的目标？

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
**第 10 课 — Robotic Video World Models（视频世界模型的能力进化）**

下节课进入论文 **Sec 5**——专注于"视频世界模型"这个**视觉表达最丰富**的 WM 形式。

我们会顺着论文的 4 个能力进化阶段走一遍：
1. **Imagination engine**：视频生成是想象力发动机
2. **Action-controllable**：让生成的未来真的响应动作
3. **Structure-aware**：加入几何/接触/视角等结构约束
4. **Foundation video WM**：从单一任务模型走向通用 WM 基础设施

代表作：UniPi, Dreamitate, IRASim, Ctrl-World, RoboMaster, TesserAct, Vid2World, Cosmos Predict, GigaWorld-0。
看完后你会理解：**为什么 2026 年的视频世界模型正在从"一个工具"变成"一个平台"。**
