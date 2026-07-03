# 📘 第 1 课：三种 policy 表示对比（explicit / implicit / diffusion）

> 对应论文章节：**Sec 1 + Sec 4.4 + Fig 1**，公式 (6)–(8)
> 学习目标：承接第 0 课的 multimodal 痛点，把历史上解决它的三条路线摆在一起，搞清 explicit / implicit 各自怎么死，从而理解 diffusion 为什么是更好的解。
> 衔接：本课终点（diffusion 只学 score、绕开归一化常数 $Z$）就是第 2 课 DDPM 的入口。

---

## 一、先看全景（论文 Fig 1）

第 0 课确认了核心病症：**multimodal**——同一观测下多个动作都对，朴素回归输出均值会出错。

怎么治？论文 Fig 1 把历史上的三条路线并排画出来：

| 路线 | 怎么表示策略 | 一句话 |
|---|---|---|
| **(a) Explicit** | 直接学映射 $a = f_\theta(o)$ | 输入观测，直接吐动作 |
| **(b) Implicit** | 学能量函数 $E_\theta(o,a)$，动作 = $\arg\min_a E$ | 给每个动作打"能量分"，挑能量最低的 |
| **(c) Diffusion** | 学动作分布的**梯度场**，从噪声迭代去噪成动作 | 不直接给动作，给"往哪个方向改"，反复迭代 |

本课讲清 (a)(b) 各自的死法，第 2 课专门讲 (c)。

---

## 二、Explicit policy：直接回归这条路

### 2.1 它是什么

最朴素的策略：网络输入观测，直接输出动作，用 MSE 监督，**一次前向出结果，快**。这是第 0 课那个朴素想法。

### 2.2 为表达多峰的几个变体（论文 Sec 8）

| 变体 | 做法 | 死法 |
|---|---|---|
| Scalar 回归 | 直接回归连续动作 | 多峰取均值 → 撞上去（第 0 课） |
| Categorical（离散化） | 把动作空间切 bin，回归变分类 | bin 数随维度**指数爆炸**（7 维不可行） |
| Mixture of Gaussians (MoG/MDN) | 输出 K 个高斯的混合 | 要预设模数 K、易 mode collapse、对超参敏感 |

> 🎯 共同问题：explicit policy 想表达"一个观测对应多个动作"，要么取均值取错，要么靠离散化/混合分布硬凑，都付出代价（维度灾难、模数难定、训练不稳）。

---

## 三、Implicit policy / EBM：能量地形这条路

### 3.1 思路转变：不预测动作，预测"动作好不好"

Implicit policy（代表作 IBC, Florence 2021）不直接输出动作，而是学一个能量函数 $E_\theta(o,a)$ 给"观测-动作"对打分，推理时搜索能量最低的动作：

$$
a^* = \arg\min_a E_\theta(o, a)
$$

写成概率就是 **Energy-Based Model (EBM)**（论文公式 6）：

$$
p_\theta(a\mid o) = \frac{e^{-E_\theta(o,a)}}{Z(o,\theta)}, \qquad Z(o,\theta) = \int e^{-E_\theta(o,a)}\,da
$$

### 3.2 为什么它天然能表达多峰

EBM 的能量地形上**可以有多个低谷**。Push-T 的"向左""向右"就是两个能量低谷，模型不取均值，两谷都保留。

> SLAM 类比：像一个**非凸代价地形**，有多个局部极小。EBM 如实保留多谷结构，不强行压成单峰。

### 3.3 它的死法：归一化常数 Z

分母 $Z(o,\theta)=\int e^{-E_\theta(o,a)}\,da$——**对所有可能动作积分，算不出来（intractable）**。

最大似然训练时损失含 $\log Z$，其梯度需要**从模型当前分布采样**（negative samples）。论文用 InfoNCE 损失（公式 7）：

$$
L_{\text{InfoNCE}} = -\log \frac{e^{-E_\theta(o,a)}}{e^{-E_\theta(o,a)} + \sum_{j=1}^{N_{neg}} e^{-E_\theta(o,\tilde a_j)}}
$$

那堆 $\tilde a_j$ 就是估计 $Z$ 的负样本。

> 🎯 死因：**负样本采不准 → $Z$ 估不准 → 训练不稳。** 论文 Fig 6 实锤：IBC 训练 loss 平滑下降，但动作预测精度不升反震荡，评测成功率剧烈抖动，checkpoint 没法选（Florence 2021 只能每个 checkpoint 都上真机测）。

> SLAM 类比：把"采负样本估 $Z$"想成蒙特卡洛估高维积分——维度一高，方差爆炸，梯度方向不可靠。

---

## 四、Diffusion policy：绕开 Z 的那一手（本课高潮 + 第 2 课入口）

### 4.1 关键观察：要的不是 Z，是 score

EBM 推理找能量最低点，本质需要的是**梯度方向**。动作分布的对数梯度（**score function**）是（论文公式 8）：

$$
\nabla_a \log p(a\mid o) = -\nabla_a E_\theta(a,o) - \underbrace{\nabla_a \log Z(o,\theta)}_{= 0}
$$

最后一项：$Z(o,\theta)$ 只和 $o,\theta$ 有关，**不含 $a$**，对 $a$ 求梯度 = 0：

$$
\boxed{\nabla_a \log p(a\mid o) = -\nabla_a E_\theta(a,o) \approx -\varepsilon_\theta(a,o)}
$$

> 🎯 **整篇最优雅的一步**：直接学这个 score（梯度场），就**彻底不需要算 $Z$**——因为 $Z$ 对动作的梯度天然为零。EBM 被 $Z$ 卡死的训练，diffusion 直接绕过去。

### 4.2 学到 score 之后怎么用

有了"每个点该往哪改"的梯度场，从随机噪声出发**反复沿梯度走小步**，逐步逼近高概率动作——Langevin dynamics / 去噪迭代。第 2 课专门讲这个迭代。

> SLAM 类比：你很熟这个 mental model——**不直接解出最优解，而是给梯度场迭代下降**。高斯牛顿/LM 也是"每步给下降方向、迭代逼近"。Diffusion 的 $\varepsilon_\theta$ 就是"梯度提供者"，只不过学的是带噪分布的 score。

### 4.3 为什么同时拿下三个优点

| 优点 | 来自哪里 |
|---|---|
| **表达多峰** | score/Langevin 能采样任意可归一化分布；随机初始化 + 随机采样让不同 rollout 落进不同峰（Fig 3：每次坚定选一个峰） |
| **训练稳定** | 绕开 $Z$，不需要负样本 |
| **高维输出** | 借用 diffusion 在图像生成上验证过的高维扩展性 → 一次预测整段动作序列（第 4 课） |

---

## 五、三条路线对照小结

| | Explicit | Implicit (EBM) | Diffusion |
|---|---|---|---|
| 表示 | $a=f_\theta(o)$ | 能量 $E_\theta(o,a)$ | score（梯度场）$\varepsilon_\theta$ |
| 推理 | 一次前向 | 搜能量最低点 | 从噪声迭代去噪 |
| 多峰 | 难（均值/维度灾难） | 天然可以 | 天然可以 |
| 训练稳定性 | 稳但表达弱 | **不稳（$Z$/负样本）** | **稳（绕开 $Z$）** |
| 推理成本 | 最低 | 中（要优化搜索） | 高（K 步迭代，第 7 课讲加速） |

> 🎓 **本课一句话**：Explicit 简单但表达不了多峰；Implicit/EBM 能表达多峰但被归一化常数 $Z$ 卡得训练不稳；Diffusion 通过"只学 score、不碰 $Z$"，同时拿到多峰表达和训练稳定——代价是推理要迭代多步。

---

## ✅ 课后检查

### Q1（必答 · 概念题）
EBM（implicit policy）明明理论上也能表达多峰，为什么实践中训练不稳？请点名是哪个量、它为什么难算、导致了什么后果。

### Q2（必答 · 理解题）
公式 (8) 里 $\nabla_a \log Z(o,\theta) = 0$ 这一步是怎么来的？为什么它对 diffusion policy 这么关键？

### Q3（选答 · 类比题）
"学一个梯度场，从随机起点迭代下降逼近解"——这个 mental model 和你做 SLAM 优化时的什么过程最像？diffusion 的 $\varepsilon_\theta$ 对应你那里的什么？

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -

---

**下一课预告**：
**第 2 课 — DDPM 到底在干什么（去噪 = 带噪梯度下降）**
我们会把"反复去噪"这件事拆开，用你最熟的"带噪声的梯度下降"（公式 1↔公式 2）来理解 DDPM，讲清加噪、去噪、训练目标三件事，把本课结尾的 score 接到具体的迭代公式上。
