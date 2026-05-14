# 第 6 章：扩散模型与 Score-based 模型的联系

> 本章我们换一个视角。
>
> Song & Ermon (2019) 从一个完全不同的角度出发，提出了 **NCSN（Noise-Conditioned Score Network）**。
>
> 你会惊奇地发现：**它和 DDPM 在数学上其实是同一件事！** 两条独立发展的路径在这里汇合。

---

## 6.1 什么是 score？

定义：分布 $p(\mathbf{x})$ 的 **score function** 是其对数密度函数的梯度：

$$
\boxed{s(\mathbf{x}) := \nabla_\mathbf{x} \log p(\mathbf{x})}
$$

**直观理解**：在每个点 $\mathbf{x}$，score 告诉你"概率密度增大最快的方向"。

> 类比：把 $-\log p(\mathbf{x})$ 想成"势能函数"，则 score 就是"力场"，指向高密度区域（"凹陷处"）。

### 6.1.1 高斯分布的 score

如果 $\mathbf{x} \sim \mathcal{N}(\boldsymbol{\mu}, \sigma^2 \mathbf{I})$，那么：

$$
\log p(\mathbf{x}) = -\frac{1}{2\sigma^2}\|\mathbf{x} - \boldsymbol{\mu}\|^2 + \text{const}
$$

$$
\nabla_\mathbf{x} \log p(\mathbf{x}) = -\frac{\mathbf{x} - \boldsymbol{\mu}}{\sigma^2}
$$

如果用重参数化 $\mathbf{x} = \boldsymbol{\mu} + \sigma\boldsymbol{\epsilon}$（$\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$）：

$$
\boxed{\nabla_\mathbf{x} \log p(\mathbf{x}) = -\frac{\boldsymbol{\epsilon}}{\sigma}}
$$

> ⭐ **关键观察**：高斯分布的 score 等于"噪声 $\boldsymbol{\epsilon}$ 除以负的标准差"。
> 这是连接 DDPM 和 NCSN 的核心桥梁。

---

## 6.2 Langevin 动力学：用 score 采样

如果你知道某个分布 $p(\mathbf{x})$ 的 score，**仅靠 score** 就能从 $p(\mathbf{x})$ 采样！方法是 **Langevin 动力学**：

$$
\boxed{\mathbf{x}_t = \mathbf{x}_{t-1} + \frac{\delta}{2}\nabla_\mathbf{x}\log p(\mathbf{x}_{t-1}) + \sqrt{\delta}\,\boldsymbol{\epsilon}_t, \quad \boldsymbol{\epsilon}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})}
$$

其中 $\delta$ 是步长。

**直观理解**：
- 第二项 $\frac{\delta}{2}\nabla\log p$：朝着"概率高"的方向走（梯度上升）；
- 第三项 $\sqrt{\delta}\boldsymbol{\epsilon}_t$：加上点随机扰动，避免陷入局部最优。

> 这其实就是带噪声版本的"梯度上升法"。

当 $T \to \infty, \delta \to 0$，$\mathbf{x}_T$ 服从 $p(\mathbf{x})$。这给了我们一个采样思路：**只要能学到 score，就能从分布中采样**！

---

## 6.3 Score Matching：怎么学 score？

定义一个 score 网络 $\mathbf{s}_\theta(\mathbf{x}) \approx \nabla_\mathbf{x}\log q(\mathbf{x})$。损失函数（最朴素的版本）：

$$
\mathcal{L}_{\text{SM}} = \mathbb{E}_{q(\mathbf{x})}\left[\|\mathbf{s}_\theta(\mathbf{x}) - \nabla_\mathbf{x}\log q(\mathbf{x})\|^2\right]
$$

**问题**：我们不知道 $\nabla_\mathbf{x}\log q(\mathbf{x})$（这正是要学的）！

### 6.3.1 解决方法：denoising score matching

Vincent (2011) 给出一个巧妙的等价形式：先给数据加点小噪声，记 $\tilde{\mathbf{x}} = \mathbf{x} + \sigma\boldsymbol{\epsilon}$，扰动后的分布 $q_\sigma(\tilde{\mathbf{x}})$ 的 score 可以这样估计：

$$
\mathcal{L}_{\text{DSM}} = \mathbb{E}_{q(\mathbf{x}, \tilde{\mathbf{x}})}\left[\|\mathbf{s}_\theta(\tilde{\mathbf{x}}) - \nabla_{\tilde{\mathbf{x}}}\log q_\sigma(\tilde{\mathbf{x}}|\mathbf{x})\|^2\right]
$$

由 6.1.1 节的结果，对 $q_\sigma(\tilde{\mathbf{x}}|\mathbf{x}) = \mathcal{N}(\tilde{\mathbf{x}}; \mathbf{x}, \sigma^2\mathbf{I})$：

$$
\nabla_{\tilde{\mathbf{x}}}\log q_\sigma(\tilde{\mathbf{x}}|\mathbf{x}) = -\frac{\tilde{\mathbf{x}} - \mathbf{x}}{\sigma^2} = -\frac{\boldsymbol{\epsilon}}{\sigma}
$$

所以：

$$
\mathcal{L}_{\text{DSM}} = \mathbb{E}\left[\left\|\mathbf{s}_\theta(\tilde{\mathbf{x}}) + \frac{\boldsymbol{\epsilon}}{\sigma}\right\|^2\right]
$$

> 看，**denoising score matching 本质就是在让网络预测"负的归一化噪声"**。

---

## 6.4 NCSN：多尺度 score matching

### 6.4.1 流形假设的困难

真实数据通常分布在**低维流形**上（哪怕看起来高维）。流形外的区域几乎没有数据，score 估计不可靠。

**NCSN 的解决思路**（Song & Ermon, 2019）：用**多个不同尺度的噪声**扰动数据，覆盖整个空间。

### 6.4.2 多尺度训练

设一系列噪声尺度 $\sigma_1 > \sigma_2 > \dots > \sigma_L$，对每个 $\sigma_i$ 学一个 score：

$$
\mathbf{s}_\theta(\mathbf{x}, \sigma_i) \approx \nabla_\mathbf{x}\log q_{\sigma_i}(\mathbf{x})
$$

训练时**每个尺度的 loss 加权求和**：

$$
\mathcal{L}_{\text{NCSN}} = \sum_{i=1}^L \lambda(\sigma_i) \mathbb{E}\left[\left\|\mathbf{s}_\theta(\tilde{\mathbf{x}}, \sigma_i) + \frac{\boldsymbol{\epsilon}}{\sigma_i}\right\|^2\right]
$$

### 6.4.3 Annealed Langevin Dynamics 采样

采样时从大噪声 $\sigma_1$ 开始，跑几步 Langevin；然后切到 $\sigma_2$，再跑几步……直到最小的 $\sigma_L$。

> **类比退火**：先用大温度做粗略搜索，再用小温度做精细优化。

---

## 6.5 ⭐ NCSN 与 DDPM 的等价性

我们现在来揭示：**NCSN 的多噪声尺度等价于 DDPM 的扩散步**。

### 6.5.1 把 DDPM 翻译成 score 的语言

回顾 nice property：

$$
q(\mathbf{x}_t | \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t}\mathbf{x}_0,\, (1-\bar{\alpha}_t)\mathbf{I})
$$

它的 score 是：

$$
\nabla_{\mathbf{x}_t}\log q(\mathbf{x}_t | \mathbf{x}_0) = -\frac{\mathbf{x}_t - \sqrt{\bar{\alpha}_t}\mathbf{x}_0}{1-\bar{\alpha}_t} = -\frac{\boldsymbol{\epsilon}_t}{\sqrt{1-\bar{\alpha}_t}}
$$

（用了 $\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\boldsymbol{\epsilon}_t$）

对 $\mathbf{x}_0$ 取期望（边缘化）也是同形式：

$$
\nabla_{\mathbf{x}_t}\log q(\mathbf{x}_t) = \mathbb{E}_{q(\mathbf{x}_0|\mathbf{x}_t)}\left[-\frac{\boldsymbol{\epsilon}}{\sqrt{1-\bar{\alpha}_t}}\right]
$$

### 6.5.2 DDPM 的 $\boldsymbol{\epsilon}_\theta$ 等价于 NCSN 的 score

如果把 DDPM 的预测噪声 $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$ 变成 NCSN 风格：

$$
\boxed{\mathbf{s}_\theta(\mathbf{x}_t, t) = -\frac{\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)}{\sqrt{1-\bar{\alpha}_t}}}
$$

> ⭐ **关键结论**：DDPM 的"预测噪声 $\boldsymbol{\epsilon}_\theta$"和 NCSN 的"预测 score $\mathbf{s}_\theta$"，**通过一个简单的尺度因子相互转换**！
>
> 它们本质上是同一个网络，只是输出语义不同。

### 6.5.3 损失函数也等价

把 $\mathbf{s}_\theta = -\boldsymbol{\epsilon}_\theta / \sqrt{1-\bar{\alpha}_t}$ 代入 NCSN 的 DSM loss：

$$
\left\|\mathbf{s}_\theta + \frac{\boldsymbol{\epsilon}}{\sqrt{1-\bar{\alpha}_t}}\right\|^2 = \frac{1}{1-\bar{\alpha}_t}\|\boldsymbol{\epsilon}_\theta - \boldsymbol{\epsilon}\|^2
$$

—— 与 DDPM 的 $\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta\|^2$ 仅差一个权重系数！加权后就是 VLB；不加权则是 simple loss。

---

## 6.6 统一视角：扩散模型 = SDE

Yang Song 等 (2021) 进一步把扩散模型推广到**连续时间 SDE（随机微分方程）**框架：

**前向 SDE**：

$$
d\mathbf{x} = f(\mathbf{x}, t)dt + g(t)d\mathbf{w}
$$

**反向 SDE**（Anderson 1982 的经典结果）：

$$
d\mathbf{x} = \big[f(\mathbf{x}, t) - g(t)^2 \nabla_\mathbf{x}\log p_t(\mathbf{x})\big]dt + g(t)d\bar{\mathbf{w}}
$$

> 反向过程只需要知道 **score $\nabla\log p_t$**！这就是为什么扩散模型的本质是学 score。
>
> DDPM、NCSN、SDE-based 模型都是这个统一框架的特例。

这部分是更高级的内容，本教程不深入。如果你感兴趣，强烈推荐 [Yang Song 的 score-based blog](https://yang-song.github.io/blog/2021/score/)。

---

## 6.7 这个等价性有什么实际意义？

1. **可以用 score-based 的 SDE 工具**改进采样（比如 ODE solver、Predictor-Corrector）；
2. **DDIM**（第 8 章）就是把扩散过程视为 ODE 的产物；
3. **Classifier Guidance**（第 7 章）的核心也是基于 score：

$$
\nabla\log p(\mathbf{x}|y) = \nabla\log p(\mathbf{x}) + \nabla\log p(y|\mathbf{x})
$$

直接用 score 的语言一下就理解了。

---

## 6.8 自检小问题

1. 什么是 score？高斯分布的 score 长什么样？
2. Langevin 动力学的更新公式是什么？为什么它能从分布中采样？
3. DDPM 的 $\boldsymbol{\epsilon}_\theta$ 和 score $\mathbf{s}_\theta$ 之间是什么关系？
4. 为什么 NCSN 要用多个噪声尺度？

<details>
<summary>👉 参考答案</summary>

1. score $= \nabla_\mathbf{x}\log p(\mathbf{x})$。对 $\mathcal{N}(\boldsymbol{\mu}, \sigma^2\mathbf{I})$，score $= -(\mathbf{x}-\boldsymbol{\mu})/\sigma^2 = -\boldsymbol{\epsilon}/\sigma$。

2. $\mathbf{x}_t = \mathbf{x}_{t-1} + \frac{\delta}{2}\nabla\log p + \sqrt{\delta}\boldsymbol{\epsilon}$。它是带噪声的梯度上升，趋近高密度区域；噪声项确保最终分布等于 $p$。

3. $\mathbf{s}_\theta(\mathbf{x}_t, t) = -\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t) / \sqrt{1-\bar{\alpha}_t}$。

4. 真实数据集中在低维流形，单一噪声尺度下 score 估计在低密度区域不准；多尺度让噪声覆盖整个空间，从大尺度（噪声多）到小尺度（接近真实）逐步退火，提升采样质量。
</details>

---

✅ 至此你已经完全掌握了扩散模型的两个理论视角（DDPM / score-based）。

下一章我们进入应用层：**怎么让扩散模型生成"特定类别"或"特定文字描述"的图像？**

➡️ 下一章：[07-条件生成.md](./07-条件生成.md)
