# 第 4 章：训练目标 —— 变分下界（VLB / ELBO）的完整推导

> 本章是扩散模型理论中**最重要、也最数学化**的一章。
> 我们要回答：**怎么训练神经网络 $p_\theta$ 才能让它逆转扩散过程？**
>
> 答案：最大化数据的对数似然 $\log p_\theta(\mathbf{x}_0)$。但它不可直接计算，所以我们退而求其次，最大化它的**变分下界（Variational Lower Bound, VLB）**，也叫 ELBO。

---

## 4.1 我们要最大化什么？

最理想的训练目标是：

$$
\max_\theta \mathbb{E}_{\mathbf{x}_0 \sim q(\mathbf{x}_0)}\big[\log p_\theta(\mathbf{x}_0)\big]
$$

即：让模型对真实数据 $\mathbf{x}_0$ 给出尽可能高的概率（最大似然）。

但是 $p_\theta(\mathbf{x}_0)$ 涉及对**所有中间变量** $\mathbf{x}_{1:T}$ 的积分：

$$
p_\theta(\mathbf{x}_0) = \int p_\theta(\mathbf{x}_{0:T})\,d\mathbf{x}_{1:T}
$$

这个高维积分**无法解析计算**！怎么办？

> **答案**：用 VAE 那一套思路，引入"代理分布" $q$，构造 $\log p_\theta(\mathbf{x}_0)$ 的下界。

---

## 4.2 推导 VLB（方法 1：从 KL 非负出发）

### 4.2.1 基本思路

利用 KL 散度恒非负的性质：

$$
D_{\text{KL}}(q(\mathbf{x}_{1:T} | \mathbf{x}_0) \| p_\theta(\mathbf{x}_{1:T} | \mathbf{x}_0)) \geq 0
$$

下面我们来"利用"这个不等式来构造下界。

### 4.2.2 第 1 步：恒等变形

$$
-\log p_\theta(\mathbf{x}_0) \leq -\log p_\theta(\mathbf{x}_0) + D_{\text{KL}}(q(\mathbf{x}_{1:T} | \mathbf{x}_0) \| p_\theta(\mathbf{x}_{1:T} | \mathbf{x}_0))
$$

（不等号成立因为 KL ≥ 0。）

### 4.2.3 第 2 步：展开 KL 散度

$$
D_{\text{KL}}(q \| p) = \mathbb{E}_q\left[\log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{1:T} | \mathbf{x}_0)}\right]
$$

利用条件概率：$p_\theta(\mathbf{x}_{1:T} | \mathbf{x}_0) = \frac{p_\theta(\mathbf{x}_{0:T})}{p_\theta(\mathbf{x}_0)}$，所以：

$$
\log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{1:T} | \mathbf{x}_0)} = \log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T}) / p_\theta(\mathbf{x}_0)} = \log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})} + \log p_\theta(\mathbf{x}_0)
$$

代入：

$$
-\log p_\theta(\mathbf{x}_0) \leq -\log p_\theta(\mathbf{x}_0) + \mathbb{E}_q\left[\log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})}\right] + \log p_\theta(\mathbf{x}_0)
$$

### 4.2.4 第 3 步：消去 $\log p_\theta(\mathbf{x}_0)$

注意 $\mathbb{E}_q[\log p_\theta(\mathbf{x}_0)] = \log p_\theta(\mathbf{x}_0)$（与 $q$ 的积分变量无关，可以提出来），所以右边第一项和第三项消掉，得：

$$
\boxed{-\log p_\theta(\mathbf{x}_0) \leq \mathbb{E}_{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}\left[\log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})}\right] =: L_{\text{VLB}}^{(\mathbf{x}_0)}}
$$

### 4.2.5 对 $\mathbf{x}_0$ 取期望

定义最终的 VLB 损失：

$$
L_{\text{VLB}} = \mathbb{E}_{q(\mathbf{x}_{0:T})}\left[\log \frac{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})}\right]
$$

由不等式可得：

$$
L_{\text{VLB}} \geq -\mathbb{E}_{q(\mathbf{x}_0)}[\log p_\theta(\mathbf{x}_0)]
$$

也就是：**最小化 $L_{\text{VLB}}$ 就是最大化数据似然的下界**。这就是我们要优化的目标。

---

## 4.3 推导 VLB（方法 2：从 Jensen 不等式出发）—— 选读

也可以直接用 Jensen 不等式得到同样结论：

$$
L_{\text{CE}} = -\mathbb{E}_{q(\mathbf{x}_0)}[\log p_\theta(\mathbf{x}_0)]
$$

代入 $p_\theta(\mathbf{x}_0) = \int p_\theta(\mathbf{x}_{0:T})d\mathbf{x}_{1:T}$，并乘除 $q(\mathbf{x}_{1:T} | \mathbf{x}_0)$：

$$
\log p_\theta(\mathbf{x}_0) = \log \int q(\mathbf{x}_{1:T} | \mathbf{x}_0) \frac{p_\theta(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}d\mathbf{x}_{1:T} = \log \mathbb{E}_{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}\left[\frac{p_\theta(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}\right]
$$

由于 $\log$ 是凹函数，Jensen 不等式给出：

$$
\log \mathbb{E}[X] \geq \mathbb{E}[\log X]
$$

所以：

$$
\log p_\theta(\mathbf{x}_0) \geq \mathbb{E}_q\left[\log \frac{p_\theta(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T} | \mathbf{x}_0)}\right] = -L_{\text{VLB}}^{(\mathbf{x}_0)}
$$

得到同样的下界。✅

---

## 4.4 VLB 的关键变形：拆成 T 个 KL 散度

到目前为止，$L_{\text{VLB}}$ 只是一个抽象的期望。**为了让它"落地"为可计算的损失**，我们需要把它**展开成具体的项**。

### 4.4.1 利用马尔可夫链结构

代入 $q(\mathbf{x}_{1:T} | \mathbf{x}_0) = \prod_{t=1}^T q(\mathbf{x}_t | \mathbf{x}_{t-1})$ 和 $p_\theta(\mathbf{x}_{0:T}) = p(\mathbf{x}_T)\prod_{t=1}^T p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)$：

$$
L_{\text{VLB}} = \mathbb{E}_q\left[\log \frac{\prod_{t=1}^T q(\mathbf{x}_t | \mathbf{x}_{t-1})}{p(\mathbf{x}_T) \prod_{t=1}^T p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)}\right]
$$

把 $\log$ 拆开：

$$
= \mathbb{E}_q\left[-\log p(\mathbf{x}_T) + \sum_{t=1}^T \log \frac{q(\mathbf{x}_t | \mathbf{x}_{t-1})}{p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)}\right]
$$

### 4.4.2 把求和拆成 $t=1$ 和 $t=2,\dots,T$

$$
= \mathbb{E}_q\left[-\log p(\mathbf{x}_T) + \sum_{t=2}^T \log \frac{q(\mathbf{x}_t | \mathbf{x}_{t-1})}{p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)} + \log \frac{q(\mathbf{x}_1 | \mathbf{x}_0)}{p_\theta(\mathbf{x}_0 | \mathbf{x}_1)}\right]
$$

### 4.4.3 关键技巧：用 $q(\mathbf{x}_t | \mathbf{x}_{t-1}, \mathbf{x}_0)$ 替代 $q(\mathbf{x}_t | \mathbf{x}_{t-1})$

**为什么这样做？** 我们的目标是把每一项写成可计算的 KL 散度形式。直接用 $q(\mathbf{x}_t | \mathbf{x}_{t-1})$ 配 $p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)$，方向不对（一个是 $t$ 给 $t-1$，一个是 $t-1$ 给 $t$），无法构成 KL 散度。

利用马尔可夫性：$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = q(\mathbf{x}_t | \mathbf{x}_{t-1}, \mathbf{x}_0)$。再用贝叶斯公式：

$$
q(\mathbf{x}_t | \mathbf{x}_{t-1}, \mathbf{x}_0) = \frac{q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0) \cdot q(\mathbf{x}_t | \mathbf{x}_0)}{q(\mathbf{x}_{t-1} | \mathbf{x}_0)}
$$

代入第二项的求和（$t \geq 2$ 时）：

$$
\sum_{t=2}^T \log \frac{q(\mathbf{x}_t | \mathbf{x}_{t-1})}{p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)} = \sum_{t=2}^T \log \frac{q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)} + \sum_{t=2}^T \log \frac{q(\mathbf{x}_t | \mathbf{x}_0)}{q(\mathbf{x}_{t-1} | \mathbf{x}_0)}
$$

### 4.4.4 第二个求和的"望远镜化简"

$$
\sum_{t=2}^T \log \frac{q(\mathbf{x}_t | \mathbf{x}_0)}{q(\mathbf{x}_{t-1} | \mathbf{x}_0)} = \log q(\mathbf{x}_T | \mathbf{x}_0) - \log q(\mathbf{x}_1 | \mathbf{x}_0)
$$

（中间项全部消掉，这就是望远镜求和。）

### 4.4.5 合并所有项

$$
L_{\text{VLB}} = \mathbb{E}_q\Bigg[-\log p(\mathbf{x}_T) + \sum_{t=2}^T \log \frac{q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)} + \log q(\mathbf{x}_T | \mathbf{x}_0) - \log q(\mathbf{x}_1 | \mathbf{x}_0) + \log \frac{q(\mathbf{x}_1 | \mathbf{x}_0)}{p_\theta(\mathbf{x}_0 | \mathbf{x}_1)}\Bigg]
$$

注意 $\log q(\mathbf{x}_1 | \mathbf{x}_0)$ 出现两次（一次正一次负），抵消！合并：

$$
L_{\text{VLB}} = \mathbb{E}_q\Bigg[\underbrace{\log \frac{q(\mathbf{x}_T | \mathbf{x}_0)}{p(\mathbf{x}_T)}}_{\text{KL 形式}} + \underbrace{\sum_{t=2}^T \log \frac{q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)}}_{\text{KL 形式}} - \log p_\theta(\mathbf{x}_0 | \mathbf{x}_1)\Bigg]
$$

把这些 $\log$-比值按 KL 散度的定义合并（注意期望的边缘化），得到最终结构：

$$
\boxed{L_{\text{VLB}} = \underbrace{D_{\text{KL}}(q(\mathbf{x}_T | \mathbf{x}_0) \| p(\mathbf{x}_T))}_{L_T} + \sum_{t=2}^T \underbrace{\mathbb{E}_q[D_{\text{KL}}(q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0) \| p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t))]}_{L_{t-1}} \underbrace{- \mathbb{E}_q[\log p_\theta(\mathbf{x}_0 | \mathbf{x}_1)]}_{L_0}}
$$

---

## 4.5 三类损失项的含义

### 4.5.1 $L_T$：终点对齐

$$
L_T = D_{\text{KL}}(q(\mathbf{x}_T | \mathbf{x}_0) \| p(\mathbf{x}_T))
$$

- $q(\mathbf{x}_T | \mathbf{x}_0)$：前向过程的终点（接近 $\mathcal{N}(0, \mathbf{I})$）；
- $p(\mathbf{x}_T) = \mathcal{N}(0, \mathbf{I})$：反向过程的起点。

由于 schedule 设计得当时 $\bar{\alpha}_T \approx 0$，这两个分布**几乎完全相同**，$L_T$ 是个接近 0 的常数。

> **训练时直接忽略 $L_T$**，因为它没有可学参数。

### 4.5.2 $L_{t-1}$（$1 \leq t-1 \leq T-1$）：去噪一致性

$$
L_{t-1} = \mathbb{E}_q\big[D_{\text{KL}}(q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0) \| p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t))\big]
$$

- $q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0)$：第 3 章推导的"老师分布"；
- $p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)$：神经网络给出的"学生分布"。

**目标**：让学生模仿老师。由于两者都是高斯，这个 KL 有解析表达式（见 1.5.2 节）。

### 4.5.3 $L_0$：起点重建

$$
L_0 = -\mathbb{E}_q[\log p_\theta(\mathbf{x}_0 | \mathbf{x}_1)]
$$

最后一步：从 $\mathbf{x}_1$（几乎是清晰的图像）生成 $\mathbf{x}_0$。

DDPM 用一个**离散解码器**（把 $\mathbf{x}_0$ 视为 $[-1,1]$ 的 256 个离散像素值）来建模这一项。

---

## 4.6 化简 $L_{t-1}$（与第 5 章衔接）

由于 $q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0)$ 和 $p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t)$ 都是**方差固定**的高斯，且方差相同（DDPM 中 $\boldsymbol{\Sigma}_\theta = \sigma_t^2 \mathbf{I}$），由第 1 章公式：

$$
L_{t-1} = \mathbb{E}_q\left[\frac{1}{2\sigma_t^2}\|\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0) - \boldsymbol{\mu}_\theta(\mathbf{x}_t, t)\|^2\right] + C
$$

其中 $C$ 是不依赖 $\theta$ 的常数。

**这就是要最小化的"均值差的平方"！**

代入第 3 章的两个公式：

$$
\tilde{\boldsymbol{\mu}}_t = \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_t\right)
$$

$$
\boldsymbol{\mu}_\theta(\mathbf{x}_t, t) = \frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha}_t}}\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\right)
$$

二者相减，$\mathbf{x}_t$ 项消掉，只剩噪声差：

$$
\tilde{\boldsymbol{\mu}}_t - \boldsymbol{\mu}_\theta = -\frac{1-\alpha_t}{\sqrt{\alpha_t}\sqrt{1-\bar{\alpha}_t}}(\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t))
$$

平方后：

$$
\|\tilde{\boldsymbol{\mu}}_t - \boldsymbol{\mu}_\theta\|^2 = \frac{(1-\alpha_t)^2}{\alpha_t(1-\bar{\alpha}_t)}\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2
$$

代回 $L_{t-1}$：

$$
\boxed{L_{t-1} = \mathbb{E}_{\mathbf{x}_0, \boldsymbol{\epsilon}}\left[\frac{(1-\alpha_t)^2}{2\sigma_t^2 \alpha_t(1-\bar{\alpha}_t)}\|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t}\boldsymbol{\epsilon}_t, t)\|^2\right]}
$$

> ⭐ **看到了吗？训练损失最终化成了：**
>
> **"网络预测的噪声 $\boldsymbol{\epsilon}_\theta$ 与真实加入的噪声 $\boldsymbol{\epsilon}_t$ 的均方误差！"**
>
> 这就是扩散模型训练的本质：**回归噪声**。

下一章我们会讲 DDPM 进一步把前面的系数也丢掉，得到一个非常简洁的 loss。

---

## 4.7 自检小问题

1. 为什么直接最大化 $\log p_\theta(\mathbf{x}_0)$ 不可行？
2. VLB 是 $\log p_\theta(\mathbf{x}_0)$ 的上界还是下界？我们要最大化它还是最小化它？
3. $L_T$ 为什么训练时可以忽略？
4. $L_{t-1}$ 化简后变成了什么形式？

<details>
<summary>👉 参考答案</summary>

1. 因为 $p_\theta(\mathbf{x}_0)$ 涉及对所有中间隐变量 $\mathbf{x}_{1:T}$ 的积分，无法解析计算。

2. 严格说："负对数似然 $-\log p_\theta(\mathbf{x}_0)$ 的**上界**"等价于 "$\log p_\theta(\mathbf{x}_0)$ 的**下界**"。我们要**最小化** $L_{\text{VLB}}$（等价于最大化对数似然下界）。

3. 因为 $L_T$ 是关于 $q(\mathbf{x}_T | \mathbf{x}_0)$ 和固定的 $p(\mathbf{x}_T) = \mathcal{N}(0,\mathbf{I})$ 的 KL，**不含可学参数 $\theta$**，相当于一个常数。

4. $L_{t-1} = \mathbb{E}\big[w_t \cdot \|\boldsymbol{\epsilon}_t - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\|^2\big]$，即**预测噪声的均方误差**（带一个权重系数 $w_t$）。
</details>

---

✅ 训练目标已经推导完成。下一章我们看 DDPM 怎么把它简化成一个**令人惊讶地简单的 loss 函数**，并给出完整的训练 / 采样算法。

➡️ 下一章：[05-DDPM简化损失与算法.md](./05-DDPM简化损失与算法.md)
