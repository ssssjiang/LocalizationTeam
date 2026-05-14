# 第 5 章：DDPM 简化损失与训练 / 采样算法

> 上一章我们推出了 $L_{t-1}$ 的具体形式：一个带权重的"预测噪声"均方误差。
> 这一章会给出 DDPM 的**最终简化 loss**（仅一行代码！），以及完整的训练和采样算法。

---

## 5.1 从 $L_t$ 到 $L_t^{\text{simple}}$：扔掉权重

回顾上一章末尾：

$$
L_t = \mathbb{E}_{\mathbf{x}_0, \boldsymbol{\epsilon}_t}\left[\frac{(1-\alpha_t)^2}{2\sigma_t^2 \alpha_t(1-\bar{\alpha}_t)}\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2\right]
$$

**Ho et al. (2020) 实证发现**：去掉这个复杂的权重系数，**训练效果反而更好**！直接用：

$$
\boxed{L_t^{\text{simple}} = \mathbb{E}_{t \sim [1,T],\, \mathbf{x}_0,\, \boldsymbol{\epsilon}_t}\big[\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2\big]}
$$

其中：

$$
\mathbf{x}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon}_t
$$

> ⭐ **这就是 DDPM 的核心 loss！**
>
> 一个学生如果只看这一行公式，也能照着实现一个能用的扩散模型。

### 为什么扔掉权重反而更好？

直觉：
- 原始权重对**小 $t$**（噪声少）赋很大的权重；
- 但实际上**大 $t$**（噪声多）的去噪任务更难，**更值得被关注**；
- 扔掉权重相当于让所有 $t$ 同等重要，反而平衡了任务难度。

最终 loss 是 $L_{\text{simple}} = L_t^{\text{simple}} + C$，其中 $C$ 是与 $\theta$ 无关的常数（包括 $L_T$ 和 $L_0$ 的部分），训练时可忽略。

---

## 5.2 训练算法（Algorithm 1）

```
重复执行：
  1. 从训练集采一个真实数据 x₀ ~ q(x)
  2. 采一个时间步 t ~ Uniform({1, 2, ..., T})
  3. 采一个噪声 ε ~ N(0, I)
  4. 计算 x_t = √(ᾱ_t) x₀ + √(1-ᾱ_t) ε
  5. 让网络预测噪声 ε_θ(x_t, t)
  6. 计算 loss = ||ε - ε_θ(x_t, t)||²
  7. 反向传播，更新 θ
```

**伪代码**（Python 风格）：

```python
def train_step(x_0, model, betas):
    T = len(betas)
    alpha_bars = compute_alpha_bars(betas)  # ᾱ_t 累乘

    t = randint(1, T+1)                      # 步 2
    eps = randn_like(x_0)                    # 步 3
    a_bar = alpha_bars[t-1]
    x_t = sqrt(a_bar) * x_0 + sqrt(1 - a_bar) * eps  # 步 4

    eps_pred = model(x_t, t)                 # 步 5
    loss = mse(eps, eps_pred)                # 步 6
    return loss
```

**关键点**：
- 每次只**随机选一个 $t$**，而不是把所有 $T$ 步都跑一遍 —— 大幅节省计算。
- $\mathbf{x}_t$ 直接用 nice property 一步采样到，不用迭代。
- 网络的输入是 $(\mathbf{x}_t, t)$，输出和 $\boldsymbol{\epsilon}$ 同形状（一张图）。
- 时间步 $t$ 通常用**正弦位置编码**或**学到的嵌入**输入网络。

---

## 5.3 采样算法（Algorithm 2）

训练完后，怎么生成新图像？

```
1. 采一个起点：x_T ~ N(0, I)
2. 对 t = T, T-1, ..., 1：
     a) 采噪声 z ~ N(0, I)（如果 t > 1，否则 z = 0）
     b) x_{t-1} = (1/√α_t) * (x_t - (1-α_t)/√(1-ᾱ_t) * ε_θ(x_t, t)) + σ_t * z
3. 返回 x_0
```

公式形式：

$$
\boxed{\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\right) + \sigma_t \mathbf{z}, \quad \mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})}
$$

其中 $\sigma_t$ 取 $\sqrt{\beta_t}$ 或 $\sqrt{\tilde{\beta}_t}$（DDPM 实验表明两者效果差不多）。

### 拆开来看，每一步采样在做什么？

1. **预测噪声** $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$：网络看到当前嘈杂图，猜出"当时加进去的噪声大概长啥样"；
2. **去掉噪声**：$\mathbf{x}_t - (\text{比例})\cdot \boldsymbol{\epsilon}_\theta$，得到一个更干净的版本；
3. **重新缩放** $\frac{1}{\sqrt{\alpha_t}}$：补偿前向过程的缩小因子；
4. **加点新噪声** $\sigma_t \mathbf{z}$：因为反向过程也是随机的（除非 $t=1$）。

> 注意：DDIM（第 8 章）会把这个**最后一步的噪声去掉**，让采样变成**确定性**的。

**伪代码**：

```python
def sample(model, betas, shape):
    T = len(betas)
    alphas = 1 - betas
    alpha_bars = compute_alpha_bars(betas)

    x = randn(shape)                                 # x_T ~ N(0, I)
    for t in range(T, 0, -1):
        eps = model(x, t)
        a_t, a_bar_t = alphas[t-1], alpha_bars[t-1]
        coef = (1 - a_t) / sqrt(1 - a_bar_t)
        mean = (1 / sqrt(a_t)) * (x - coef * eps)
        if t > 1:
            sigma = sqrt(betas[t-1])
            x = mean + sigma * randn_like(x)
        else:
            x = mean
    return x
```

---

## 5.4 Variance schedule 的选择

DDPM 中 $\beta_t$ 是**线性 schedule**：

$$
\beta_t \in [\beta_1=10^{-4},\ \beta_T=0.02], \quad T = 1000
$$

后续工作（Improved DDPM, Nichol & Dhariwal 2021）发现**余弦 schedule** 在低分辨率任务（如 64×64）上表现更好：

$$
\bar{\alpha}_t = \frac{f(t)}{f(0)}, \quad f(t) = \cos^2\left(\frac{t/T + s}{1+s}\cdot \frac{\pi}{2}\right)
$$

其中小偏移 $s$ 防止 $\beta_t$ 在 $t \to 0$ 时过小。

**比较图（线性 vs 余弦）**：余弦 schedule 在中间区域呈现**接近线性的下降**，而在两端（$t=0, t=T$）变化平缓 —— 这样不会"过早失去信号"也不会"过晚才开始变成噪声"。

---

## 5.5 进阶：是否要学习反向方差 $\boldsymbol{\Sigma}_\theta$？

DDPM 把 $\boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t)$ 固定为 $\sigma_t^2 \mathbf{I}$（不学）。Improved DDPM 提出让网络也输出方差：

$$
\boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t) = \exp\big(\mathbf{v}\log\beta_t + (1-\mathbf{v})\log\tilde{\beta}_t\big)
$$

其中 $\mathbf{v}$ 是网络输出的混合系数，把 $\beta_t$ 和 $\tilde{\beta}_t$ 之间做插值（在 log 空间内插值）。

**问题**：$L_{\text{simple}}$ 不依赖 $\boldsymbol{\Sigma}_\theta$，这样网络拿不到方差的训练信号。

**解决**：构造 hybrid loss：

$$
L_{\text{hybrid}} = L_{\text{simple}} + \lambda L_{\text{VLB}}
$$

其中 $\lambda$ 很小（如 $10^{-3}$），且对 $\boldsymbol{\mu}_\theta$ 在 $L_{\text{VLB}}$ 项中**停止梯度**（stop-grad），让 $L_{\text{VLB}}$ 只引导方差学习。

**效果**：能显著降低 NLL（log-likelihood），与其他似然模型可比。

---

## 5.6 训练实操要点（深入浅出）

如果你打算自己写一个扩散模型，请注意：

1. **图像归一化**到 $[-1, 1]$（因为 $\mathbf{x}_T$ 是标准高斯，取值范围匹配）。
2. **网络架构**：通常用 U-Net（带时间步嵌入），第 9 章详讲。
3. **时间步嵌入**：$t$ 转成正弦位置编码，喂给网络的每一层（通过 FiLM 或加法）。
4. **batch size**：相对小即可（DDPM 用 128），训练时间长（百万步起步）。
5. **EMA**（指数滑动平均）：维护一份模型参数的 EMA 版本用于采样，效果显著更好。
6. **采样慢**：T=1000 一张图要跑 1000 次前向，第 8 章会讲怎么加速。

---

## 5.7 一图总结

```
┌─────────────────────────────────────────────────────────────┐
│             训练 (Algorithm 1)                              │
│                                                             │
│   x₀ (真实图)                                               │
│      │                                                      │
│      ├──> 采样 t、ε                                         │
│      ▼                                                      │
│   x_t = √ᾱ_t x₀ + √(1-ᾱ_t) ε  (前向 nice property)         │
│      │                                                      │
│      ▼                                                      │
│   ε_θ(x_t, t) ──预测──> 应该 ≈ ε                            │
│      │                                                      │
│      ▼                                                      │
│   loss = ||ε - ε_θ(x_t, t)||²  (MSE)                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│             采样 (Algorithm 2)                              │
│                                                             │
│   x_T ~ N(0, I)  (纯噪声起点)                              │
│   for t = T, T-1, ..., 1:                                  │
│       预测 ε_θ(x_t, t)                                      │
│       x_{t-1} = (1/√α_t)(x_t - β_t/√(1-ᾱ_t) ε_θ) + σ_t z  │
│   返回 x_0  (生成的图)                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 5.8 自检小问题

1. DDPM 的 simple loss 是什么？为什么扔掉权重反而效果更好？
2. 训练时为什么每次只随机选一个 $t$，而不是 $1$ 到 $T$ 全跑一遍？
3. 采样为什么要 T 步？能不能跳步？
4. 如果让网络预测 $\mathbf{x}_0$ 而非 $\boldsymbol{\epsilon}$，loss 长什么样？

<details>
<summary>👉 参考答案</summary>

1. $L_{\text{simple}} = \mathbb{E}\|\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta\|^2$。扔掉权重相当于让所有 $t$ 同等重要，避免网络只关注小 $t$（容易但不重要）的样本。

2. 因为 $L_t^{\text{simple}}$ 本身就是对 $t$ 取期望的形式，蒙特卡洛估计每个 batch 采一些 $t$ 即可。这样做让训练 cost 与 $T$ 无关，否则 $T=1000$ 的话每步训练要算 1000 次前向，不可行。

3. T 步是 DDPM 默认设定。**可以跳步**！DDIM、Progressive Distillation 等就是干这件事的，详见第 8 章。

4. 如果让网络预测 $\mathbf{x}_0$，loss 是 $\mathbb{E}\|\mathbf{x}_0 - \mathbf{x}_{0,\theta}(\mathbf{x}_t, t)\|^2$，本质等价（因为 $\boldsymbol{\epsilon}$ 与 $\mathbf{x}_0$ 通过 nice property 一一对应），但实践中预测噪声效果更稳。
</details>

---

✅ **DDPM 主线全部讲完！** 你已经能看懂大部分扩散模型论文的训练算法了。

下一章（第 6 章）我们换个视角，从 **score-based 模型**重新看扩散模型，会发现两条路径在数学上是等价的。

➡️ 下一章：[06-Score-based模型联系.md](./06-Score-based模型联系.md)
