# Diffusion Inpainting：非 mask 区域一致性 Q&A

整理自 2026-04-24 talk 分享会的追问。配套阅读：`Diffusion-VLM到World-Model读图前置.md`、`Diffusion-VLM到World-Model读图前置-QA.md`。

## 0. 问题

**DDPM 针对 mask 部分的生成，如何保证非 mask 部分的图像和原图一致？**

## 1. 结论先行

**DDPM 本身不保证。** 需要额外机制。两种主流做法分别从「**训练**」和「**推理**」两个层面解决：

| 方法 | 解决层面 | 一致性保证机制 | 像素级严格一致 |
|---|---|---|---|
| **SD-Inpainting** | 训练 | 改 U-Net 输入通道，让模型「学到」要与上下文一致 | 否（需后处理） |
| **RePaint** | 推理 | 每步强制把非 mask 区域 blend 成原图加噪版 | 是（latent 域严格） |

工程上**两种都建议加最后一步像素空间 paste-back** 才能真正 byte-level 一致。

## 2. SD-Inpainting：靠训练学到一致性

### 2.1 核心思路

**改 U-Net 输入通道，让模型在训练时见过大量「mask + 上下文」数据，自己学会与未 mask 区域一致。**

### 2.2 模型改动

U-Net 第一层从 4 通道扩到 9 通道：

```text
普通 SD U-Net 输入：
  conv_in.weight.shape = [320, 4, 3, 3]
  输入 = [noisy latent (4)]

SD-Inpainting U-Net 输入：
  conv_in.weight.shape = [320, 9, 3, 3]    ← 多出 5 通道
  输入 = [noisy latent (4)] + [mask (1)] + [masked image latent (4)]
                                  ↑                ↑
                          下采样到 latent 分辨率   原图被 mask 后过 VAE encoder
```

新增的 5 通道权重在初始化时设为 0，再 fine-tune（保证从 base SD 平滑过渡）。

### 2.3 训练数据

需要专门构造数据：

```text
训练样本: (x_0, mask, text_prompt)
  x_0:             真实图
  mask:            随机生成的 mask（覆盖任意区域）
  masked_image:    x_0 × (1 - mask)   ← mask 区域置 0
```

训练目标仍是预测噪声 ε：

```text
loss = || ε - ε_θ([noisy_latent, mask, masked_image_latent], t, text_emb) ||²
```

### 2.4 推理流程

```text
1. 把原图过 VAE encoder → image_latent
2. masked_image_latent = image_latent · (1 - mask)
3. z_T ~ N(0, I)
4. for t in [T, ..., 1]:
       9 通道输入 = [z_t, mask, masked_image_latent]
       ε_θ = unet(9 通道输入, t, text_emb)
       z_{t-1} = denoise_step(z_t, ε_θ, t)
5. 解码：generated_image = VAE_decoder(z_0)
```

**起点是纯噪声**，非 mask 区域的信息通过 `masked_image_latent` 这条通道一直注入 U-Net。

### 2.5 一致性保证程度

| 维度 | 是否保证 |
|---|---|
| 语义一致（生成内容和上下文协调） | ✓ 训练让模型学到了 |
| 边界平滑（mask 边界连贯） | ✓ 训练让模型学到了 |
| 像素级严格一致 | ✗ **不严格** |

**为什么不严格**：

- VAE encode → decode 有重建误差（即使非 mask 区域也会有轻微像素偏移）
- latent 空间的 blending 投回像素空间会有偏差
- 模型可能轻微「重画」非 mask 区域（即使不该改）

### 2.6 工程上要严格一致

部署时常加一步 **像素空间 paste-back**：

```python
output = mask * generated + (1 - mask) * original_image
```

Diffusers 的 `StableDiffusionInpaintPipeline` 也支持这种后处理（参数 `mask_blur`、`original_image`）。

### 2.7 出处

- 模型架构：Rombach et al. 2022, *Latent Diffusion Models*, CVPR 2022, arXiv:2112.10752
- 9 通道实现细节：RunwayML SD-Inpainting 模型卡（`runwayml/stable-diffusion-inpainting`）
- SDXL 版本：Stability AI SDXL-Inpainting 模型卡（`diffusers/stable-diffusion-xl-1.0-inpainting-0.1`）
- 代码：HuggingFace Diffusers `prepare_mask_latents` + `StableDiffusionInpaintPipeline`

## 3. RePaint：靠推理流程强制一致

### 3.1 核心思路

**完全不改模型、不需要训练。直接复用预训练 unconditional / 文生图 DDPM，每步去噪时把非 mask 区域强制对齐到原图加噪版。**

### 3.2 模型改动

**没有**。直接用预训练 DDPM，U-Net 一个参数都不动。

> 这是 RePaint 最大的优势：**任何预训练 diffusion 都能立刻拿来做 inpainting**。

### 3.3 推理流程（关键）

每个去噪步 t 都做两件事：

```text
for t in [T, T-1, ..., 1]:
    
    # Step A: 已知区域 → 用原图前向加噪
    x_{t-1}^known = √(α̅_{t-1}) · x_0 + √(1-α̅_{t-1}) · ε
                    ↑                         ↑
              已知 x_0 是原图          ε ~ N(0, I) 新采的
    
    # Step B: 未知区域 → 用模型反向去噪
    ε̂ = unet(x_t, t)
    x_{t-1}^unknown = denoise_formula(x_t, ε̂, t)
    
    # Step C: 用 mask 合并
    x_{t-1} = mask ⊙ x_{t-1}^unknown + (1-mask) ⊙ x_{t-1}^known
              └─────────────────┘     └───────────────────┘
              mask 区域：模型生成       非 mask 区域：永远来自原图加噪版
```

**关键点**：非 mask 区域**永远来自原图前向加噪**，从 t=T 一路 blend 到 t=0。最终 t=0 时，`√α̅_0 = 1, √(1-α̅_0) = 0`，所以非 mask 区域 = `1 · x_0 + 0 · ε = x_0`，**严格等于原图**。

### 3.4 一致性保证程度（严格）

| 维度 | 是否保证 |
|---|---|
| 语义一致 | △ 不一定（模型生成区域可能不太协调） |
| 边界平滑 | △ 可能不连贯，需要 resampling 缓解 |
| **像素级严格一致** | ✓ **严格保证**（公式上 t=0 时直接 = x_0） |

**为什么边界容易不连贯**：

模型预测 mask 区域时，看到的 `x_t` 包含「自己上一步预测的 mask 区域 + 强制塞回去的非 mask 加噪版」。两部分可能不协调，导致模型预测的 mask 区域和强行塞回的非 mask 区域之间出现「拼贴感」。

### 3.5 Resampling：解决边界不连贯

RePaint 引入 **resampling** 来让模型有机会调整：

```text
做 K 步去噪（t: 273 → 272 → ... → 263）
然后跳回去（forward 加噪到 t=273）
再重做 K 步（t: 273 → 272 → ... → 263）
反复几次
```

伪代码（论文 Algorithm 1）：

```text
for t in schedule:
    x_{t-1} = 上面的 Step A + Step B + Step C
    
    if 需要 resampling:
        x_t = x_{t-1} + 加噪 1 步   ← undo step
        # 然后下次循环又会 denoise 一次
```

代价是**推理慢 10 倍**（典型 `jump_n_sample=10`）。

### 3.6 RePaint 的论文图

RePaint 论文（Lugmayr et al. 2022）有 Figure 2 的方法 overview，但**不是网络架构图**——因为它不改网络。它画的是「每步 blend」的推理流程。

完整伪代码在论文 Figure 11，包含 resampling 的 schedule。

### 3.7 出处

- 论文：Lugmayr et al. 2022, *RePaint: Inpainting using Denoising Diffusion Probabilistic Models*, CVPR 2022, arXiv:2201.09865
- 关键章节：Sec. 4.1 (Conditioning on the known Region) + Sec. 4.2 (Resampling)
- Diffusers 实现：`RePaintPipeline` + `RePaintScheduler`（参数 `jump_length`、`jump_n_sample`）

## 4. 对比总结

### 4.1 一致性保证机制对比

```text
SD-Inpainting:                          RePaint:

  原图 + mask                              原图 + mask
       ↓                                       ↓
  VAE encode                              （不改模型，直接用）
       ↓                                       ↓
  9 通道输入注入 U-Net                     纯噪声起步
  （masked_image_latent 一直陪着 z_t）       每步 blend 已知区域 = 原图前向加噪
       ↓                                       ↓
  训练时学到「与上下文一致」              t=0 时已知区域严格 = x_0
       ↓                                       ↓
  推理生成                                推理生成

  机制：训练让模型「自己学到」             机制：推理「强制对齐」
  保证：语义/边界一致，像素近似一致       保证：像素严格一致，但边界靠 resampling
```

### 4.2 详细对照表

| 维度 | SD-Inpainting | RePaint |
|---|---|---|
| 是否需要训练 | 需要 | 不需要（training-free） |
| 模型改动 | U-Net 输入通道 4→9 | 无 |
| 训练数据 | 需要 (image, mask, prompt) 三元组 | 不需要 |
| 推理起点 | `x_T ~ N(0,I)` | `x_T ~ N(0,I)` |
| 非 mask 区域信息怎么进 | 训练时通过 9 通道输入注入 | 每步推理 blend 进去 |
| 像素级一致性 | 不严格（latent 近似 + VAE 重建误差） | 严格（latent 域上每步对齐） |
| 边界质量 | 通常自然（训练学到边界平滑） | 易不连贯，需 resampling |
| 推理速度 | 标准（和文生图一样） | 慢约 10 倍（resampling） |
| 灵活性 | 只能用专门训练的 inpainting 模型 | 任何预训练 diffusion 都能用 |
| 适用场景 | 生产环境、复杂内容补全 | 没条件训新模型、需严格像素一致、原型快速验证 |

### 4.3 一图记住核心区别

```text
                    SD-Inpainting              RePaint
                    ─────────────              ───────
谁负责一致性       训练好的模型               推理时的 blend 公式
代价              要训练新模型               推理慢 10 倍
能不能像素严格     不能（需 paste-back）      能（公式保证）
能不能换模型用     不能（绑定 inpainting ckpt）能（任何 ddpm）
```

## 5. 工程选型建议

### 5.1 决策树

```text
有专门训练的 inpainting 模型可用？
├── 是 → 优先用 SD-Inpainting
│         （质量好、速度快、边界自然）
│         需要严格像素一致 → 加 paste-back
│
└── 否 → 用 RePaint
          （任何预训练 diffusion 都能立刻用）
          边界不好 → 增加 resampling 次数
          严格像素一致 → 公式自动保证（latent 域）
                       + paste-back（pixel 域）
```

### 5.2 严格像素级一致的工程实践

**无论用哪种方法**，最终建议都加一步：

```python
import numpy as np

def paste_back(generated_image, original_image, mask):
    """
    Args:
        generated_image: diffusion 模型生成的图
        original_image: 原图
        mask: 二值 mask，1=要重画，0=保留
    Returns:
        非 mask 区域严格等于 original_image
    """
    mask = mask[..., None]  # 增加通道维
    return mask * generated_image + (1 - mask) * original_image
```

这一步**和模型无关，在 pixel 空间做**，能 byte-level 保证非 mask 区域一致。

### 5.3 边界平滑技巧

Paste-back 可能在 mask 边界处产生硬边，可以加 **mask blur** 软化过渡：

```python
import cv2

def paste_back_smooth(generated, original, mask, blur_radius=5):
    mask_blurred = cv2.GaussianBlur(mask.astype(float),
                                     (blur_radius*2+1, blur_radius*2+1), 0)
    mask_blurred = mask_blurred[..., None]
    return mask_blurred * generated + (1 - mask_blurred) * original
```

Diffusers `StableDiffusionInpaintPipeline` 的 `mask_blur` 参数就是做这个。

## 6. 一句话总收

> DDPM 本身不保证非 mask 区域一致。**SD-Inpainting 改 U-Net 输入通道 + 训练**让模型学到一致；**RePaint 不改模型，每步推理把非 mask 区域强制 blend 成原图加噪版**保证一致。前者快但需后处理，后者慢但 latent 域严格一致。工程上**两种都建议最后加一步 pixel 空间 paste-back**才能 byte-level 一致。

## 7. References

- [1] Lugmayr et al., *RePaint: Inpainting using Denoising Diffusion Probabilistic Models*, CVPR 2022, arXiv:2201.09865
  - Sec. 4.1: Conditioning on the known Region（核心 blend 公式）
  - Sec. 4.2: Resampling（解决边界不连贯）
  - Figure 2: 方法 overview
  - Figure 11: 完整推理伪代码
- [2] Rombach et al., *High-Resolution Image Synthesis with Latent Diffusion Models*, CVPR 2022, arXiv:2112.10752
  - 提供 SD-Inpainting 的基础架构
- [3] RunwayML, `runwayml/stable-diffusion-inpainting` 模型卡
  - 说明 9 通道修改和零初始化 fine-tune 流程
- [4] Stability AI, `diffusers/stable-diffusion-xl-1.0-inpainting-0.1` 模型卡
  - SDXL inpainting 版本细节
- [5] HuggingFace Diffusers `StableDiffusionInpaintPipeline` 源码
  - `prepare_mask_latents` 实现 mask + masked image 的 9 通道 concat
- [6] HuggingFace Diffusers `RePaintPipeline` + `RePaintScheduler` 源码
  - `jump_length` / `jump_n_sample` 参数实现 resampling
