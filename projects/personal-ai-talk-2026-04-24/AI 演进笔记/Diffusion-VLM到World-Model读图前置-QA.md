# Diffusion 推理与训练 Q&A

整理自 2026-04-24 talk 后续的追问对话，按主题分组。所有结论均给出出处或佐证。配套阅读：`Diffusion-VLM到World-Model读图前置.md`。

## 1. 基础概念

### 1.1 DDPM 是什么？

DDPM = Denoising Diffusion Probabilistic Models，是 **Ho et al. 2020** 这一篇具体论文（arXiv:2006.11239），不是泛称。它定义了：

- 一条具体的前向加噪过程（高斯噪声叠加）
- 一个具体训练目标（噪声预测 MSE loss）
- 一个具体推理算法（Algorithm 2 Sampling）

严格意义上，「DDPM 推理」**只覆盖无条件生成**。其他用法（文生图、img2img、ControlNet 等）都是基于 DDPM 框架的扩展或变体。

工业界口语常把 DDPM 泛用为「diffusion 类生成模型」的统称，但写文档时按具体方法名引用更准确。

### 1.2 5 种应用都能叫「DDPM 推理」吗？

严格说不能。术语层级：

```text
Diffusion Models（最广泛）
    ├── DDPM (Ho et al. 2020)                ← 无条件生成
    │   + 条件机制                            ← 文生图（GLIDE / Latent Diffusion）
    │   + 推理流程改造（SDEdit / RePaint）    ← img2img / training-free inpainting
    │   + 改 U-Net 输入通道                   ← SD-Inpainting
    │   + 加分支                              ← ControlNet
    │
    ├── DDIM (Song et al. 2021)               ← 确定性采样加速
    ├── Latent Diffusion (Rombach et al. 2022)
    └── DiT (Peebles & Xie 2023)
```

更准确的统称：「**基于 diffusion 模型的图像生成 / 编辑**」。

## 2. 训练机制

### 2.1 训练时是从 x_T ~ N(0, I) 开始吗？

**不是。** 训练和推理的起点完全不同：

| 阶段 | 起点 | 是否走完 T 步 |
|---|---|---|
| 训练 | 真实图 x_0 + 随机一个时间步 t | 否，每次只学一步 |
| 推理 | x_T ~ N(0, I) | 是，反向走完所有 T 步 |

训练的核心是**闭式公式**：

$$
x_t = \sqrt{\bar\alpha_t} \cdot x_0 + \sqrt{1-\bar\alpha_t} \cdot \epsilon
$$

无论 t=1 还是 t=1000，**一次乘加就能跳到 x_t**，不需要顺序走 t 步。

**出处**：Ho et al. 2020 Algorithm 1 (Training)。

### 2.2 训练 loss 怎么算？用什么减什么？

DDPM 默认是 **ε-prediction**：

$$
L = \| \epsilon - \epsilon_\theta(x_t, t) \|^2
$$

- `ε`：训练时自己 sample 的噪声 tensor（**已知 ground truth**）
- `ε_θ`：U-Net 预测的噪声
- 两者形状都和原图相同（如 `[B, 3, H, W]`），**逐元素 MSE**

**不是图减图**，是**噪声减噪声**。

完整一次 iteration：

```text
1. 采样 x_0（一张真实图）
2. 随机采样 t（比如 t=473）
3. 随机采样 ε ~ N(0, I)
4. 闭式公式算 x_t（1 次乘加）
5. U-Net forward: ε_θ = unet(x_t, t)（1 次 forward）
6. loss = || ε - ε_θ ||²
7. backward + optimizer.step()
```

**整个 iteration 只跑 U-Net 1 次**。

理论上也可以用 x_0-prediction（让 U-Net 直接输出干净图），数学上等价。但 ε-prediction 经验上训练更稳定（不同 t 的 loss 量级一致）。

**出处**：Ho et al. 2020 Eq. 14。

### 2.3 训练 1 次 vs 推理 T 次，是否矛盾？

**不矛盾。** 这是三个独立维度：

|  | 物理上 U-Net 几个 | 训练 1 iter 调用几次 | 推理生成 1 张图调用几次 |
|---|---|---|---|
| 数量 | **1 个**（1 套参数） | **1 次** | **T 次** |

```text
训练高效（每 iter 1 次）：得益于前向加噪的闭式公式
推理慢（每张图 T 次）：反向去噪没有闭式公式，必须顺序走
```

## 3. 推理机制

### 3.1 U-Net 输出是噪声，那「去噪」在哪发生？

U-Net **直接输出预测噪声 ε_θ，不是干净图**。

「去噪」发生在 U-Net 之后的**确定性公式**里（DDPM Eq. 11）：

$$
x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}} \epsilon_\theta(x_t, t)\right) + \sigma_t z
$$

直觉上：

```text
x_{t-1} ≈ x_t − (一部分预测噪声) + (一点新噪声)
```

U-Net 是「**噪声预测器**」，外部公式才执行真正的去噪。整套系统叫 denoising diffusion，不是 U-Net 自己叫 denoiser。

### 3.2 推理是 T 个 U-Net 串联吗？

**不是，只有 1 个 U-Net 反复跑 T 次。**

LDM 论文 Figure 3 那个循环箭头和 `×(T-1)` 标注，意思是「同一个 U-Net 重复 T-1 次」。

```text
unet = UNet2DConditionModel(...)    # 物理上只构造 1 次
for t in [T, T-1, ..., 1]:
    eps = unet(z, t)                # 同一个 unet
    z = denoise_step(z, eps, t)
```

t 通过 **timestep embedding** 注入 U-Net，让同一个网络在不同 t 下表现不同行为。

参数量验算：SD v1.5 U-Net 约 860M 参数，如果真有 1000 个串联就是 860 GB，显然不可能。

### 3.3 推理为什么没有闭式公式？

**因为反向过程依赖未知的数据分布 p_data(x_0)。**

| 方向 | 是否有闭式 | 原因 |
|---|---|---|
| 前向（加噪） | **有** | 我们自己设计的高斯叠加，高斯叠加性保证「多步加噪 = 一步加噪」 |
| 反向（去噪） | **没有** | 反向需要知道 `p(x_{t-1})` 和 `p(x_t)`，这些依赖 `p_data(x_0)`（所有自然图像的分布），无法解析表达 |

DDPM 的做法是用神经网络**近似**反向过程，每步靠 U-Net 估计 + 公式合成，多步迭代不收敛到闭式。

后续 DDIM、DPM-Solver、Consistency Models 都在试图缩短推理步数（1000 → 50 → 10 → 1 步），但都是近似优化，**不是真正的闭式解**。

### 3.4 推理输入是纯噪声，去噪后不就变成白图了吗？

**不会**，关键澄清：

> **ε_θ ≠ x_T**。模型基于训练学到的图像先验，预测的不是「x_t 全是噪声」，而是「在图像分布下，应该被当作噪声减掉的部分」。

数值直觉：

- t=T 时，ε_θ 确实**非常接近**但**不完全等于** x_T
- 微小差异方向 = 模型猜测的「图像信号」
- 多步迭代累积，把微小差异放大成完整图像

```text
t = T:    几乎全噪声 → 第一步去噪后是模糊低频
t = T-300: 开始有物体轮廓
t = 0:    完整清晰图像
```

**图像是从噪声里「挖出来」的，不是「保留下来」的**。模型每步把 x_t 推向训练数据的高密度区。

## 4. 五种应用对照

### 4.1 推理时是否需要加噪？规律是什么？

**判断准则**：模型是否有专门通道接收该类条件？

- **没有** → 信息必须编码进采样起点（加噪输入图）
- **有** → 走条件通道，起点用纯噪声即可

5 种用法对照：

| 用法 | 起点 | 推理是否加噪 | 原因 |
|---|---|---|---|
| 无条件生成 | `x_T ~ N(0,I)` | 否 | 无输入图 |
| 文生图 | `x_T ~ N(0,I)` | 否 | 文本走 cross-attention 通道 |
| **img2img / SDEdit** | **输入图加噪到 x_t** | **是** | **「输入图整体 layout」没有专门通道，只能编码进起点** |
| inpainting (RePaint) | 起点是噪声，**每步对非 mask 区域 blend 原图加噪版** | 部分是 | 训练-free，靠推理 blend 保证非 mask 区域一致 |
| inpainting (SD-Inpainting) | `x_T ~ N(0,I)` | 否 | mask 信息走训练扩展的 9 通道输入 |
| ControlNet | `x_T ~ N(0,I)` | 否 | edge/pose/depth 走 ControlNet 分支 |

### 4.2 是否需要重新训练？规律是什么？

**判断准则**：是否改了模型的输入通道数或网络结构？

- **改了** → 必须重新训
- **没改**（只改推理流程）→ 直接复用预训练模型

5 种用法对照：

| 用法 | 是否需要训 | 训练相比文生图改了什么 | 出处 |
|---|---|---|---|
| 无条件生成 | 自己一套（无条件 DDPM） | 没有条件输入 | Ho et al. 2020 |
| 文生图 | 自己一套（条件 DDPM + CFG） | 加文本条件 `ε_θ(x_t, t, c)`，训练时随机 drop condition 支持 CFG | Ho & Salimans 2022 (CFG)；Rombach et al. 2022 (LDM) |
| img2img / SDEdit | **不需要** | 直接复用文生图模型，只改推理起点 | Meng et al. 2022 (SDEdit) |
| inpainting (RePaint) | **不需要** | 直接复用预训练 unconditional 模型 | Lugmayr et al. 2022 (RePaint) |
| inpainting (SD-Inpainting) | 需要 | U-Net 输入通道扩到 9：`noisy latent(4) + mask(1) + masked image latent(4)` | RunwayML / Stability 模型卡 |
| ControlNet | 需要 | 主 U-Net 冻结，新增一支 ControlNet 分支 | Zhang & Agrawala 2023 |

### 4.3 SDEdit vs ControlNet：风格迁移两条路径

**误解澄清**：SDEdit 风格迁移**仍然在保留原图信息**——保留的是 layout、构图、低频结构，被改变的是风格、纹理、细节。

两条风格迁移路径对照：

| 维度 | SDEdit | ControlNet |
|---|---|---|
| 保留什么 | 输入图的整体 layout、构图、低频结构 | 用户**显式**指定的结构（edge、pose、depth） |
| 信息怎么进网络 | 编码进**采样起点** | 通过**专门训练的条件分支** |
| 是否需要训练 | 不需要 | 需要训 ControlNet 分支 |

> **本质规律不是「是否保留输入图」，而是「该类条件有没有专门通道」**。

## 5. 具体方法澄清

### 5.1 SDEdit「先加噪再去噪」原文佐证

**论文**：Meng et al. 2022, *SDEdit*, ICLR 2022, arXiv:2108.01073

abstract 第一句直接表述：

> "SDEdit first adds noise to the input, then subsequently denoises the resulting image through the SDE prior to increase its realism."

Algorithm 1 (VE-SDE) 也是两步：

```text
Step 1: x ~ N(x^(g), σ²(t_0) · I)   ← 起步加噪到 t_0
Step 2: 从 t_0 反向运行 SDE 到 t=0   ← 再去噪
```

严格说 SDEdit 基于 score-based SDE（Song et al. 2021），但和 DDPM 数学等价（DDPM 是 VP-SDE 的离散化），用来代表 diffusion 类「noise-then-denoise」流程是站得住的。

### 5.2 RePaint vs SD-Inpainting

| 维度 | RePaint | SD-Inpainting |
|---|---|---|
| 是否需要训练 | 不需要，training-free | 需要专门训练 |
| 模型改动 | 无，直接用预训练 unconditional / 文生图模型 | U-Net 输入通道扩到 9（noisy latent 4 + mask 1 + masked image latent 4） |
| 保证非 mask 区域一致 | 推理时每步强制 blend 原图加噪版 | 训练时模型学到与上下文一致 |
| 像素级一致性 | 严格一致（已知区域是 x_0 直接前向加噪） | 不严格（latent 空间近似 + VAE 编解码有损） |
| 推理速度 | 慢（resampling 10 次 ≈ 10 倍） | 标准速度 |
| 生成质量 | 边界容易不连贯，需 resampling | 通常更自然 |
| 灵活性 | 任何预训练 diffusion 都能直接做 | 只能用专门训过的 inpainting 模型 |
| 出处 | Lugmayr et al. 2022, CVPR 2022 | Rombach et al. 2022 + RunwayML 模型卡 |

**工程上严格像素级一致**：去噪完成后在像素空间 paste-back：

```python
output = mask * generated + (1 - mask) * original_image
```

### 5.3 各方法论文图的情况

| 方法 | 是否有官方架构图 | 哪里找 |
|---|---|---|
| DDPM | 没有专门架构图（U-Net 是通用结构） | 论文 Algorithm 1 + Algorithm 2 |
| Latent Diffusion / SD | 有 | Rombach et al. 2022 Figure 3 |
| SDEdit | 有方法 overview 图 | Meng et al. 2022 Figure 2 + Algorithm 1 |
| RePaint | **有 Figure 2 方法流程图，但不是网络架构图**（不改网络） | Lugmayr et al. 2022 Figure 2 + 伪代码 Figure 11 |
| SD-Inpainting | **没有专门架构图**（只是 LDM 改 U-Net 输入通道再 fine-tune） | 看 Latent Diffusion Figure 3 + Diffusers `prepare_mask_latents` 源码 |
| ControlNet | 有 | Zhang & Agrawala 2023 Figure 2 |
| DiT | 有 | Peebles & Xie 2023 Figure 3 |

## 6. SDEdit 更新公式细节

针对 SDEdit Algorithm 1 (VE-SDE)：

```text
x ← x + ε² · s_θ(x, t) + ε · z
```

### 6.1 这看起来是闭式公式，是吗？

**不是闭式解**。`s_θ(x, t)` 是 **score 神经网络**，每步循环都要调用一次。

判别准则：

- 算法里有 `for` 循环 → 不是闭式
- 含神经网络标记（`θ`、`ε_θ`、`s_θ`）→ 不是闭式

SDEdit 推理仍然是「**迭代算法 + N 次神经网络 forward**」，只是把 DDPM 1000 步压成 N=20-50 步。

真正的闭式解长这样：`x_t = √α̅_t · x_0 + √(1-α̅_t) · ε`——一行、无循环、无网络。

### 6.2 `ε² · s_θ(x, t) + ε·z` 是预测噪声的负数吗？

**直觉对了一半。** 拆成两部分：

```text
x ← x + ε² · s_θ(x, t) + ε · z
        └─────────────┘   └────┘
        确定性去噪项      随机注入项
```

**确定性项 `ε² · s_θ(x, t)`**：在 VE-SDE 下，`s_θ ≈ -ε_θ / σ(t)`，所以这一项**确实是把预测噪声按比例往负方向减**（不是简单负数，多了一个 `1/σ(t)` 缩放）。

**随机项 `+ ε · z`**：每步重新采的新噪声，**不是噪声预测**，目的是保证采样多样性。

所有 diffusion 反向公式的统一结构：

```text
新 x = 当前 x − (按比例减预测噪声) + (注入新噪声)
                └──────────────┘     └─────────┘
                去噪部分             随机性部分（DDIM 这里为 0）
```

判别项的小技巧：

| 项 | 含义 |
|---|---|
| 含 `s_θ` 或 `ε_θ` | 去噪部分 |
| 含 `z ~ N(0,I)` | 随机性注入（DDIM 没有） |
| 其他系数（`α`、`σ`） | 调度参数 |

## 7. References

- [1] Ho et al., *Denoising Diffusion Probabilistic Models*, NeurIPS 2020, arXiv:2006.11239
- [2] Ho & Salimans, *Classifier-Free Diffusion Guidance*, arXiv 2022, arXiv:2207.12598
- [3] Rombach et al., *High-Resolution Image Synthesis with Latent Diffusion Models*, CVPR 2022, arXiv:2112.10752
- [4] Meng et al., *SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations*, ICLR 2022, arXiv:2108.01073
- [5] Lugmayr et al., *RePaint: Inpainting using Denoising Diffusion Probabilistic Models*, CVPR 2022, arXiv:2201.09865
- [6] Zhang & Agrawala, *Adding Conditional Control to Text-to-Image Diffusion Models*, ICCV 2023, arXiv:2302.05543
- [7] Song et al., *Score-Based Generative Modeling through SDEs*, ICLR 2021, arXiv:2011.13456
- [8] Song et al., *Denoising Diffusion Implicit Models* (DDIM), ICLR 2021, arXiv:2010.02502
- [9] Peebles & Xie, *Scalable Diffusion Models with Transformers* (DiT), ICCV 2023, arXiv:2212.09748
- [10] HuggingFace Diffusers `StableDiffusionInpaintPipeline` 源码：`prepare_mask_latents` 实现 9 通道 concat
