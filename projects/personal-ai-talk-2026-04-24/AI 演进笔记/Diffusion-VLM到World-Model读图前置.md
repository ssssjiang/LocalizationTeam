# Diffusion、DiT 与 VLM：读图前置

## 1. 先区分两类能力

视觉模型在 2020 年之后分出两条主线：一条负责生成视觉内容，一条负责理解视觉内容。Diffusion / DiT 属于生成路线；CLIP / VLM / LLaVA 属于理解路线。

| 路线 | 解决的问题 | 典型输入 | 典型输出 |
|---|---|---|---|
| **Diffusion / DiT** | 怎么生成图像或视频 | 噪声、文本、图像、结构条件 | 图像、视频、latent |
| **CLIP / VLM / LLaVA** | 怎么把视觉信息接入语言语义空间 | 图像、文本问题、语言指令 | embedding 或文本回答 |
| **VLA / Policy** | 怎么把视觉语言输入接到动作输出 | 图像、语言指令、机器人状态 | action token 或连续动作 |

读图时先判断模块在做哪件事：生成、理解，还是动作输出。这个判断会比模型名字更稳定。

---

## 2. Diffusion：为什么从去噪开始

图像生成可以被写成“从随机变量生成一张图”。早期深度生成模型沿 GAN、VAE、Normalizing Flow 三条路线发展，但各自有训练稳定性、样本质量或网络结构约束的问题。Diffusion 选择另一种做法：不让模型一步从噪声跳到图像，而是把生成拆成很多个小的去噪步骤[1]。

### 2.1 一步生成为什么难

从随机噪声一步生成图像，模型要同时决定物体类别、形状、纹理、光照和背景布局。这个映射跨度很大，训练时容易不稳定。

| 生成路线 | 做法 | 主要约束 |
|---|---|---|
| GAN | 生成器和判别器对抗训练 | 训练不稳定，容易模式坍塌 |
| VAE | 编码到 latent，再从 latent 解码 | 图像质量常受代理目标限制 |
| Normalizing Flow | 学可逆变换 | 网络结构必须可逆，设计受限 |
| Diffusion | 把生成拆成多步去噪 | 采样慢，但训练目标稳定 |

Diffusion 的关键选择是：先定义一条“容易构造”的加噪路径，再学习它的反方向。

### 2.2 Diffusion 的核心拆法

训练时，真实图像被逐步加噪，最后变成接近高斯噪声的样本。这个前向过程是固定规则，不需要学习。

推理时，模型从随机噪声出发，反复预测并去掉噪声，逐步得到图像。

```text
训练：真实图像 → 加噪 → 带噪图像 → 训练模型预测噪声
推理：随机噪声 → 反复去噪 → 生成图像
```

<!-- 图：建议补 DDPM 论文 forward / reverse process 图。用途：先让读者看到“加噪 / 去噪”这条主线。来源：Ho et al., Denoising Diffusion Probabilistic Models, NeurIPS 2020. -->

这套设计的好处是：模型不用一次学会“从无到有生成图像”，而是反复解决一个更局部的问题——当前带噪样本里还剩多少噪声。

### 2.3 加噪过程

DDPM 定义一步加噪：

$$
q(x_t \mid x_{t-1}) =
\mathcal{N}(x_t;\sqrt{1-\beta_t}x_{t-1},\beta_t I)
$$

$\beta_t$ 是第 $t$ 步的噪声强度。每一步都保留一部分原图信号，再加入一点高斯噪声[1]。

训练时可以直接采样任意时间步的带噪图：

$$
x_t = \sqrt{\bar{\alpha}_t}x_0 + \sqrt{1-\bar{\alpha}_t}\epsilon,\quad \epsilon \sim \mathcal{N}(0,I)
$$

$x_0$ 是真实图像，$x_t$ 是加噪后的图像，$\epsilon$ 是真实加入的噪声[1]。

### 2.4 训练目标

模型学习预测噪声：

$$
L =
\mathbb{E}_{x_0,t,\epsilon}
\left[
\|\epsilon - \epsilon_\theta(x_t,t)\|^2
\right]
$$

输入是带噪图 $x_t$ 和时间步 $t$，输出是预测噪声 $\epsilon_\theta(x_t,t)$。训练目标是让预测噪声接近真实噪声 $\epsilon$[1]。

这一步是后面所有 diffusion 系统的共同底座。区别只在于：带噪对象是什么，条件输入是什么，去噪网络是什么。

---

## 3. Diffusion 的使用方式

Diffusion 不是单一的“文生图模型”。它是一套可被不同条件控制的去噪接口。不同应用主要改两个位置：采样起点和条件输入。

### 3.1 无条件生成

无条件生成从随机噪声开始，不接收文本或图像条件：

```text
x_T ~ N(0, I)
  ↓ denoising
image
```

它从训练分布中采样新图像。DDPM 原始实验主要展示这种形式[1]。

### 3.2 文生图

文生图仍从随机噪声开始，但每一步去噪都接收文本条件：

```text
text prompt → text embedding
                      ↓
x_T ~ N(0, I) → denoising → image
```

文本不是最后才影响结果，而是在每一步噪声预测里改变采样方向。

条件版去噪器可以写成：

$$
\epsilon_\theta(x_t,t,c)
$$

$c$ 是条件输入，可以是文本 embedding、图像条件、深度图、动作条件或任务指令。

Classifier-Free Guidance (CFG) 用同一个网络同时预测无条件噪声和有条件噪声，采样时做线性组合[2]：

$$
\epsilon =
\epsilon_{\text{uncond}} +
w(\epsilon_{\text{cond}}-\epsilon_{\text{uncond}})
$$

$w$ 控制条件强度。这个公式说明：条件信息通过每一步去噪改变生成方向。

<!-- 图：建议补 Latent Diffusion / Stable Diffusion 的 text-to-image 架构或样例图。用途：解释文本 embedding 如何作为条件进入去噪过程。来源：Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, CVPR 2022. -->

### 3.3 img2img

img2img 不是从纯随机噪声开始，而是先把输入图加噪到中间时间步：

```text
input image
  ↓ add noise to x_t
noisy input
  ↓ denoising with prompt
edited image
```

加噪越多，输出越偏离原图；加噪越少，输出越保留原图结构。SDEdit 用这个接口把草图、粗糙编辑或低质量图像转成更真实的图像[12]。

<!-- 图：建议补 SDEdit Figure 1。用途：解释 img2img：输入草图 / 粗糙图先加噪，再沿条件去噪成更真实的新图。来源：Meng et al., SDEdit, ICLR 2022. -->

### 3.4 inpainting

Inpainting 固定已知区域，只重绘 mask 区域：

```text
image + mask + optional prompt
        ↓
denoise masked region
        ↓
completed / edited image
```

这里的条件不只是文本，还包括 mask。模型只需要在缺失区域采样，非 mask 区域作为约束保留[3][13]。

<!-- 图：建议补 RePaint 或 Latent Diffusion inpainting 示例图。用途：解释 mask 区域被重新生成，非 mask 区域保持。来源：Lugmayr et al., RePaint, CVPR 2022；或 Rombach et al., Latent Diffusion, CVPR 2022. -->

### 3.5 ControlNet

ControlNet 把边缘、姿态、深度、分割图等结构条件接入去噪网络[14]：

```text
prompt + control map
        ↓
controlled denoising
        ↓
image following structure
```

普通文生图主要控制语义；ControlNet 额外控制结构。它让“生成一张骑马的人”变成“按这个姿态 / 边缘 / 深度结构生成一张骑马的人”。

<!-- 图：建议补 ControlNet Figure 1。用途：解释 Canny edge / pose / depth 作为结构条件控制生成结果。来源：Zhang & Agrawala, Adding Conditional Control to Text-to-Image Diffusion Models, ICCV 2023. -->

### 3.6 小结

| 使用方式       | 采样起点                        | 条件输入         | 输出关系             |
| ---------- | --------------------------- | ------------ | ---------------- |
| 无条件生成      | $x_T \sim \mathcal{N}(0,I)$ | 无            | 从训练分布中采样新图像      |
| 文生图        | $x_T \sim \mathcal{N}(0,I)$ | 文本 embedding | 文本条件影响每一步噪声预测    |
| img2img    | 输入图加噪到中间时间步                 | 文本或图像条件      | 保留部分输入图结构，再沿条件去噪 |
| inpainting | 已知区域固定，缺失区域从噪声开始            | mask 与可选文本条件 | 只更新 mask 指定区域    |
| ControlNet | $x_T$ 或图像相关起点               | 边缘、姿态、深度等控制图 | 结构条件通过额外网络进入去噪过程 |

---

## 4. VAE、Latent Diffusion 与 DiT

DDPM 说明了“逐步去噪”这件事。后续大模型系统主要改两个地方：在什么空间里去噪，用什么网络去噪。

### 4.1 VAE：图像压缩器和解压器

VAE (Variational Autoencoder) 在这里先按“图像压缩器 + 图像解压器”理解。它不负责逐步去噪，也不是 DiT；它负责把 RGB 图像压成 latent，再把 latent 解回 RGB 图像[3]。

```text
image x
  ↓ encoder
latent z
  ↓ decoder
reconstructed image x'
```

经典 VAE 不直接输出一个固定 latent，而是输出一个分布：

$$
q(z \mid x) = \mathcal{N}(\mu(x), \sigma(x)^2)
$$

然后从这个分布里采样：

$$
z = \mu(x) + \sigma(x)\epsilon,\quad \epsilon \sim \mathcal{N}(0,I)
$$

训练时有两个目标：重建图像要接近原图，latent 分布不要偏离标准高斯太远。这里不展开 VAE 推导，只保留它在视觉生成系统里的作用：

```text
VAE encoder：把图像压成 latent
VAE decoder：把 latent 解回图像
Diffusion / DiT：在 latent 上做去噪生成
```

<!-- 图：建议补 Latent Diffusion 论文中的 autoencoder / latent diffusion 架构图。用途：解释 VAE encoder、latent diffusion、decoder 三段式。来源：Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, CVPR 2022. -->

### 4.2 Latent Diffusion

Latent Diffusion 先用 VAE 把图像压到 latent space，再在 latent 上做 diffusion[3]：

```text
image x
  ↓ encoder
latent z
  ↓ diffusion denoising
generated latent z'
  ↓ decoder
generated image x'
```

<!-- 图：建议补 Latent Diffusion 架构图。用途：解释 VAE encoder / latent diffusion / decoder 三段式。来源：Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, CVPR 2022. -->

这一步降低了高分辨率图像生成的计算成本。读图时看到 `VAE encoder`、`latent z`、`latent diffusion`、`decoder`，就可以按这个三段式理解。

### 4.3 DiT

DiT (Diffusion Transformer) 把 diffusion 里的去噪网络从 U-Net 换成 Transformer[4]。Diffusion 是生成过程，Transformer / DiT 是去噪网络。

```text
Diffusion：怎么生成
    从噪声逐步去噪

Transformer / DiT：谁来去噪
    用 self-attention 处理 latent tokens
```

<!-- 图：建议补 DiT 架构图。用途：解释 latent patch tokens + Transformer block + diffusion timestep conditioning。来源：Peebles & Xie, Scalable Diffusion Models with Transformers, ICCV 2023. -->

视频生成里，输入不再是一张图，而是一段视频的 latent tokens：

```text
video clip
  ↓ video VAE / tokenizer
video latent tokens
  ↓ add noise
noisy video latent tokens
  ↓ video DiT / expert transformer
denoised video latent tokens
  ↓ decoder
video
```

Latte 和 CogVideoX 都属于这条线：把视频表示成 token / latent，再用 Transformer 类结构在时空维度上建模[5][6]。

<!-- 图：建议补 Latte 或 CogVideoX 架构图。用途：解释 video latent tokens + Transformer / expert transformer。来源：Latte arXiv:2401.03048；CogVideoX arXiv:2408.06072. -->

---

## 5. CLIP：图像和语言如何对齐

CLIP 解决的是图文对齐。它使用两个 encoder：image encoder 编码图像，text encoder 编码文本。两者输出到同一个 embedding space，再计算相似度[7]。

<!-- 图：建议补 CLIP Figure 1。用途：解释 image encoder / text encoder / N×N contrastive learning。来源：Radford et al., Learning Transferable Visual Models From Natural Language Supervision, ICML 2021. -->

### 5.1 相似度矩阵

CLIP 对一个 batch 内的所有图文组合计算相似度：

$$
S_{ij} = \frac{I_i^\top T_j}{\tau}
$$

$I_i$ 是第 $i$ 张图的 embedding，$T_j$ 是第 $j$ 段文本的 embedding，$S_{ij}$ 是它们的匹配分数[7]。

训练目标是让匹配图文对位于相似度矩阵的对角线。

### 5.2 对称损失

CLIP 的损失同时约束两个方向：

$$
L_{\text{CLIP}} =
\frac{1}{2}(L_{\text{i2t}} + L_{\text{t2i}})
$$

$L_{\text{i2t}}$ 要求“图能找对文本”，$L_{\text{t2i}}$ 要求“文本能找对图”。这一步让视觉特征获得开放词表语义。

### 5.3 能力边界

CLIP 的输出是 embedding，不是回答。它擅长图文匹配、检索和零样本分类，但不会基于图像生成开放式回答。

```text
image
  ↓ CLIP image encoder
image embedding

text
  ↓ CLIP text encoder
text embedding

similarity(image, text)
```

---

## 6. 从 CLIP 到 LLaVA：几种常见桥接方式

后续 VLA / WM 图里经常出现 `CLIP`、`SigLIP`、`BLIP-2`、`LLaVA-style projector`。它们都在解决“视觉特征如何进入语言或动作模型”这个问题，但位置不同。

| 模型 / 模块    | 在图里常见位置                                 | 主要作用                                                           | 读图时怎么理解                 |
| ---------- | --------------------------------------- | -------------------------------------------------------------- | ----------------------- |
| **CLIP**   | vision encoder / image encoder          | 把图像和文本对齐到同一 embedding space                                    | 提供开放词表视觉语义特征            |
| **SigLIP** | vision encoder / SigLIP encoder         | CLIP 类图文对齐模型，用 sigmoid loss 替代 CLIP 的 softmax 对比损失[15]         | 常作为更强或更稳定的 CLIP 替代视觉编码器 |
| **BLIP-2** | Q-Former / query tokens / bridge module | 用 Q-Former 从 frozen image encoder 中抽取少量视觉 token，再喂给 frozen LLM | 视觉到语言的“压缩桥接器”           |
| **LLaVA**  | projector / MLP / visual tokens         | 用 projector 把 CLIP 视觉 token 映射到 LLM token space                | 最简单的视觉 token 接 LLM 方案   |

<!-- 图：建议补 BLIP-2 Figure 1。用途：解释 frozen image encoder、Q-Former、frozen LLM 三段式桥接。来源：Li et al., BLIP-2, ICML 2023. -->

BLIP-2 和 LLaVA 的区别可以先按“是否压缩视觉 token”理解：

```text
BLIP-2:
image encoder → Q-Former 抽取少量 query tokens → LLM

LLaVA:
image encoder → projector 映射视觉 patch tokens → LLM
```

BLIP-2 更强调用 Q-Former 作为桥接模块，减少视觉 token 数量；LLaVA 更强调极简 projector，让 LLM 自己处理投影后的视觉 token[10][8]。

---

## 7. LLaVA：视觉 token 如何接入 LLM

LLaVA 把 CLIP 的视觉特征接到 LLM，让语言模型可以基于图像生成回答[8]。

<!-- 图：建议补 LLaVA 架构图。用途：解释 CLIP vision encoder + projector + LLM。来源：Liu et al., Visual Instruction Tuning, NeurIPS 2023. -->

### 7.1 投影器

CLIP-ViT 输出视觉 token $H_v$。这些 token 不能直接喂给 LLM，需要投影到 LLM token space：

$$
Z_v = W H_v
$$

$W$ 是投影器，$Z_v$ 是投影后的视觉 token。LLM 的输入变成：

```text
[visual tokens Z_v] + [text question tokens]
```

### 7.2 LLaVA 解决的问题

LLaVA 把“图像 embedding”变成“语言模型能读的视觉 token”。模型因此可以从：

```text
image + question
  ↓
text answer
```

CLIP 只解决图文对齐；LLaVA 进一步解决看图回答。

### 7.3 VLM 到 VLA

VLA 把 VLM 的输出空间从文本扩展到动作[9]：

$$
\pi(a_{t+1:t+k}\mid o_t,l)
$$

$o_t$ 是当前观测，$l$ 是语言指令，$a_{t+1:t+k}$ 是未来 action chunk。

常见做法有两类：

| 路线                     | 输出方式                                                      | 代表                 |
| ---------------------- | --------------------------------------------------------- | ------------------ |
| action token           | 把动作离散化成 token，由 VLM 自回归输出                                 | RT-2               |
| continuous action head | VLM / MLLM 提供语义上下文，再由 diffusion / flow action head 输出连续动作 | π0、GR00T、部分 VLA 系统 |

<!-- 图：建议补 RT-2 架构图。用途：解释 VLM 输出从 text token 扩展到 action token。来源：Brohan et al., RT-2, arXiv 2023. -->

---

## 8. 读图检查清单

每看到一张 Diffusion / VLM / VLA 相关架构图，先问 6 个问题：

| 问题 | 看哪里 |
|---|---|
| 图像或视频怎么被压缩？ | VAE、video tokenizer、vision encoder |
| 文本怎么进入模型？ | text encoder、LLM、prompt tokens |
| 视觉特征怎么接到语言模型？ | projector、adapter、Q-Former、visual tokens |
| 生成过程在哪里？ | U-Net、DiT、expert transformer、denoising blocks |
| 输出是文本还是动作？ | LLM head、action token、action head |
| 模型是在理解还是生成？ | 输入输出关系：image/text → answer，还是 noise/condition → image/video |

到这里为止，只需要保留 3 个结论：

1. **Diffusion / DiT 是视觉生成接口**：从噪声或 latent 出发，逐步去噪生成图像 / 视频。
2. **CLIP / VLM / LLaVA 是视觉语言接口**：把图像接入语言语义空间，让 LLM 能基于图像回答。
3. **VLA 是动作接口**：把视觉语言输入接到机器人动作输出。

---

## References

- [1] Ho et al., Denoising Diffusion Probabilistic Models, NeurIPS 2020. arXiv:2006.11239
- [2] Ho & Salimans, Classifier-Free Diffusion Guidance, arXiv 2022. arXiv:2207.12598
- [3] Rombach et al., High-Resolution Image Synthesis with Latent Diffusion Models, CVPR 2022. arXiv:2112.10752
- [4] Peebles & Xie, Scalable Diffusion Models with Transformers, ICCV 2023. arXiv:2212.09748
- [5] Ma et al., Latte: Latent Diffusion Transformer for Video Generation, arXiv 2024. arXiv:2401.03048
- [6] Yang et al., CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer, ICLR 2025. arXiv:2408.06072
- [7] Radford et al., Learning Transferable Visual Models From Natural Language Supervision, ICML 2021. arXiv:2103.00020
- [8] Liu et al., Visual Instruction Tuning, NeurIPS 2023. arXiv:2304.08485
- [9] Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, arXiv 2023. arXiv:2307.15818
- [10] Li et al., BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models, ICML 2023. arXiv:2301.12597
- [11] NTU MARS et al., World Model for Robot Learning: A Comprehensive Survey, arXiv 2026. arXiv:2605.00080v1
- [12] Meng et al., SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations, ICLR 2022. arXiv:2108.01073
- [13] Lugmayr et al., RePaint: Inpainting using Denoising Diffusion Probabilistic Models, CVPR 2022. arXiv:2201.09865
- [14] Zhang & Agrawala, Adding Conditional Control to Text-to-Image Diffusion Models, ICCV 2023. arXiv:2302.05543
- [15] Zhai et al., Sigmoid Loss for Language Image Pre-Training, ICCV 2023. arXiv:2303.15343
