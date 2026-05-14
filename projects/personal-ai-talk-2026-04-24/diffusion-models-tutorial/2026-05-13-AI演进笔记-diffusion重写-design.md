# Spec：AI 演进笔记 — Diffusion 部分重写设计

## 1. 元信息

| 字段 | 值 |
|---|---|
| 设计日期 | 2026-05-13 |
| 目标文件 | `/Users/songshu/Downloads/AI 演进笔记 （2012-2026） _20260512_233948/AI 演进笔记 （2012-2026） _20260512_233948.md` |
| 重写范围 | 替换原 §4 整章；前移原 §6.2 内容到新 §4；§6 仅留 World Models 起源 |
| 风格规则 | `~/.cursor/rules/personal-doc-style.mdc`，§4.3 允许少量教学化（前提：客观、有源、无主观比喻） |
| 重写原因（用户原话） | "没有写出去噪这个重点，以及我问到的推理时如何使用，反而介绍了很多生涩的概念" |

## 2. 已确认的设计决策

| # | 决策 | 结论 | 决策时刻 |
|---|---|---|---|
| 1 | 重写范围 | §4 整章 + §6.2 视频生成 | 23:46 |
| 2 | 整体风格 | 教程化 → 后调整为 personal-doc-style.mdc 优先 | 23:48 → 00:09 |
| 3 | §4 / §6.2 结构 | 合并成新章节 "Diffusion：从图像到视频"；§6 仅留 World Models 起源 | 23:49 |
| 4 | 资产处理 | 保留所有学术引用；公式精简到核心 3-5 个；图选关键 3-5 张 | 23:55 |
| 5 | §4.3 例外 | 允许少量教学化语言（仍需客观、有源、无主观比喻） | 00:09 |

## 3. 新章节骨架

```
## 4. Diffusion 范式：从图像到视频 (2020-2024)
   引子（≤ 2 句）
   ### 4.1 三大主线 (GAN / VAE / Flow)
   ### 4.2 DDPM (2020)
       #### 4.2.1 前向加噪
       #### 4.2.2 训练目标
   ### 4.3 训练 vs 推理：两套接口
       #### 4.3.1 训练阶段
       #### 4.3.2 推理阶段
       #### 4.3.3 五类工作流
   ### 4.4 三个工程问题与解法 (DDIM / CFG / LDM)
       #### 4.4.1 采样加速 → DDIM (2021)
       #### 4.4.2 条件控制 → Classifier guidance / CFG (2021-2022)
       #### 4.4.3 计算降低 → Latent Diffusion (2022)
   ### 4.5 视频生成 (2023-2024)
       #### 4.5.1 Sora 与 Spacetime Patch / DiT
       #### 4.5.2 三种范式
       #### 4.5.3 长 horizon
       #### 4.5.4 与 World Models 收敛
   ### 4.6 产品矩阵 (图像 + 视频)
       #### 4.6.1 图像生成
       #### 4.6.2 视频生成
       #### 4.6.3 路线分化
   ### References
```

## 4. 每节详细设计

### 4.1 三大主线 (GAN / VAE / Flow)

**引子（直接陈述）**：

> 2020 年 DDPM 出现之前，深度生成模型主要沿三条主线发展：GAN[13]、VAE[14]、Normalizing Flow[15]。

**主体**：表格（4 列：模型族 / 核心做法 / 强项 / 卡点），每行带 `[N]` 引用。

**承启句**：

> Diffusion 在 ImageNet FID 上超过 GAN 是 2021 年由 Dhariwal & Nichol 报告的[3]。

**预算**：~150 字
**资产**：表格 ×1；引用 [3][13][14][15]。

---

### 4.2 DDPM (2020)

**引子**：

> DDPM[1] 把图像生成定义为逐步去噪的迭代过程：训练时把真实图 $\mathbf{x}_0$ 加噪到 $\mathbf{x}_T$，模型学习反向预测每步加进去的噪声。

#### 4.2.1 前向加噪

- 公式：$q(\mathbf{x}_t \mid \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t;\, \sqrt{1-\beta_t}\,\mathbf{x}_{t-1},\, \beta_t \mathbf{I})$
- 文字：DDPM 用线性 schedule $\beta_1=10^{-4} \to \beta_T=0.02$[1]
- 公式（nice property）：$\mathbf{x}_t = \sqrt{\bar\alpha_t}\mathbf{x}_0 + \sqrt{1-\bar\alpha_t}\boldsymbol{\epsilon}$
- 文字：T=1000 时，$\bar\alpha_T \to 0$，$\mathbf{x}_T \approx \mathcal{N}(\mathbf{0}, \mathbf{I})$[1]

#### 4.2.2 训练目标

- 公式：$L = \mathbb{E}_{\mathbf{x}_0, t, \boldsymbol{\epsilon}}\!\left[\| \boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t) \|^2\right]$
- 训练伪代码 4 行（Python）
- 文字：网络的输入 $(\mathbf{x}_t, t)$，输出与 $\mathbf{x}_t$ 同形状的预测噪声 $\boldsymbol{\epsilon}_\theta$；损失为 MSE[1]

**承启句**：

> DDPM 训练目标的稳定性使后续工作能在不改训练接口的前提下解决采样速度、条件控制、计算成本等工程问题（详见 §4.4）[2][4][5]。

**与原笔记的删除项**（按规则）：
- 删除"diffusion 现代起点"（强判断词无 `[N]` 锚定）
- 不写"一句话核心" / "残差思想第二次出现"等 agent 主观归纳

**预算**：~400 字
**资产**：公式 ×3；训练伪代码 ×1；图 `images/RDu8bf1ZGodRjWxGKolckxGjnwg.png`；引用 [1]。

---

### 4.3 训练 vs 推理：两套接口（教学锚点节，允许少量教学化）

**引子（客观 + axis 标注）**：

> §4.2 给出 DDPM 的训练目标。本节展开训练 / 推理两阶段的输入输出差异，并按"采样起点 + 条件输入"两个 axis 列出 5 类工作流（无条件生成 / 文生图 / img2img / inpainting / ControlNet）。

#### 4.3.1 训练阶段

- 表格：训练 vs 推理对照（4 列：阶段 / 输入 / 输出 / 是否需要图）
- 训练 4 行伪代码（Python）
- 文字：训练阶段的图 $\mathbf{x}_0$ 仅用于产生监督信号；推理时不参与[1]

#### 4.3.2 推理阶段

- 推理 5 行伪代码（Python）
- 文字：起点 $\mathbf{x}_T = \texttt{torch.randn(...)}$，由 §4.2 nice property 知 $T=1000$ 时 $\mathbf{x}_T \approx \mathcal{N}(\mathbf{0}, \mathbf{I})$，与"任意真实图加噪 $T$ 步"的边缘分布一致[1]

#### 4.3.3 五类工作流

引子标注 axis：

> 5 类工作流按"采样起点 + 条件输入 $\mathbf{c}$"两个 axis 区分。条件版网络从 $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$ 升级为 $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t, \mathbf{c})$，$\mathbf{c}$ 可以是文本嵌入、图像特征或 mask（详见 §4.4.2 / §4.6）。

- 5 工作流表格（5 列：工作流 / 起点 $\mathbf{x}_T$ / 条件 $\mathbf{c}$ / 公开产品 / 引用）
- 文字：img2img 的"强度"对应起点 $t$ 的位置——强度 0.5 起点为 $\mathbf{x}_{500}$，强度 1.0 起点为 $\mathbf{x}_T$（退化为纯文生图）[5]

**与原草稿的删除项**（按规则收紧）：
- 删除 ASCII "采样过程的'起点'决定一切" 抒情图
- 删除"几乎每个学扩散模型的人都会卡住"（代行业发言）
- 删除"指挥棒 / 凝结"等 agent 比喻
- 删除 §4.3.4 "一句话核心" 整段

**预算**：~500 字
**资产**：训练 vs 推理对照表 ×1；5 工作流表 ×1；伪代码 ×2；引用 [1][5][8]。

---

### 4.4 三个工程问题与解法 (DDIM / CFG / LDM)

**引子**：

> DDPM 的训练目标稳定后，2021-2022 年三篇工作分别解决采样速度、条件控制、计算成本三个工程问题：DDIM[2]、Classifier guidance / CFG[3][4]、LDM[5]。

#### 4.4.1 采样加速 → DDIM (2021)

- 文字：DDPM 反向过程 T=1000 步，生成 50k 张 32×32 图约需 20 小时（NVIDIA 2080 Ti），同硬件 GAN 不到 1 分钟[2]
- 文字：DDIM[2] 把反向过程改为确定性 + 非马尔可夫，可跳步采样，常压到 50 步且质量损失可忽略[2]
- 文字：DPM-Solver / EDM 进一步压到 10-20 步
- 文字：DDIM 的确定性映射也是 img2img / SDEdit 的数学基础——保证起点与终点的可控对应[2]

#### 4.4.2 条件控制 → Classifier guidance / CFG (2021-2022)

- 文字（Classifier guidance）：额外训分类器 $p(y \mid \mathbf{x}_t)$，每步在残差上加分类器梯度作为修正[3]
- 公式：$\bar{\boldsymbol{\epsilon}}_\theta = \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t) - \sqrt{1-\bar\alpha_t}\,w\,\nabla_{\mathbf{x}_t}\log p(y \mid \mathbf{x}_t)$
- 文字（CFG）：训练时随机丢弃条件 $\mathbf{c}$，使同一网络同时学条件版与无条件版；采样时线性外推[4]
- 公式：$\bar{\boldsymbol{\epsilon}}_\theta = (1+w)\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t, \mathbf{c}) - w\,\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$
- 文字：CFG 不需要单独分类器；当前所有 text-to-image 模型沿用此做法[4][8][9][10]

#### 4.4.3 计算降低 → Latent Diffusion (2022)

- 文字：LDM[5] 把扩散搬到 VAE encoder 的 latent space（4× 下采样），训练 / 推理算力降到约 1/8[5]
- 图：`images/W6jHbK4qJocDf0x9mUhcHc5Fnuc.png`（LDM 架构）
- 文字：Stable Diffusion (2022-08) 基于 LDM + LAION-5B 训练，是首个 8GB VRAM 消费级 GPU 可跑的 text-to-image 模型[5]
- 文字：开源生态在 1 年内出现 ControlNet (2023-02)、LoRA、ComfyUI 等周边工具

**与原草稿的删除项**：
- 删除"极致简洁"（强判断词无 `[N]`）
- 删除"一句话直觉"小段、§4.4.4 "一句话核心" 整段
- 删除"三个正交维度"、"训练接口稳定不变" 等主观归纳

**预算**：~500 字
**资产**：公式 ×2（Classifier guidance / CFG）；图 ×1（LDM）；引用 [2][3][4][5]。

---

### 4.5 视频生成 (2023-2024)

**引子**：

> 视频 diffusion 的两个路标：Runway GEN-1[6] 把 latent diffusion 扩展到视频；Sora[10] 提出 spacetime patch + DiT[7] 范式。

#### 4.5.1 Sora 与 Spacetime Patch / DiT

- 文字（GEN-1）：把 latent diffusion 扩展到视频，用 depth/structure 作为条件，输入源视频 + 文本/图像 prompt，输出保持原动作结构、appearance 被改造的新视频[6]
- 文字（Sora）：把视频切成 spacetime patch（覆盖若干连续帧 + 局部空间区域），每个 patch 编码为 token；DiT[7] 把扩散网络从 U-Net 换成 Transformer，在 spacetime token 序列上做去噪[10]
- 文字：Sora 在公开技术报告中描述可生成最长 60 秒视频[10]

#### 4.5.2 三种范式

- 表格：Diffusion / Autoregressive / Hybrid（4 列：范式 / 代表 / 特点 / 引用）

#### 4.5.3 长 horizon

- 保留原笔记 quote box（长 horizon 在视频生成 / VLA / World Model 三场景的不同含义）
- 文字：Sora 在长 horizon 一致性上的提升被 OpenAI 在公开技术报告中描述为 "video generation models as world simulators"[10]

#### 4.5.4 与 World Models 收敛

- 文字：视频生成模型可视为 implicit world model；DeepMind Genie 系列把它做成 user-action-controllable；NVIDIA Cosmos 把 video diffusion 放进 world model 工具链
- 指针：→ §6.1 World Models 起源（Ha & Schmidhuber 2018 V+M+C）
- 指针：→ §8 World Models 近期形态（Genie 3 / Cosmos）

**与原草稿的删除项**：
- 删除"核心难点"（强判断词无 `[N]`）
- 删除"显著超过"（无具体数字）
- 删除"本质是 §4.3 img2img 在视频上的应用"（agent 推断），改为 GEN-1 的客观技术陈述

**预算**：~400 字
**资产**：表格 ×1；quote box ×1；引用 [6][7][10]。

---

### 4.6 产品矩阵 (图像 + 视频)

**引子**：

> 2022-2024 间 diffusion 产品按 modality 分图像 / 视频两条线，按 release 时间序列出。

#### 4.6.1 图像生成

- 表格：8 行（DALL-E 2 / SD 1.x / Imagen / Midjourney / SDXL / DALL-E 3 / SD3 / FLUX），5 列（时间 / 产品 / 机构 / 技术核心 / 路线）

#### 4.6.2 视频生成

- 表格：5 行（GEN-1 / SVD / Sora / Veo / Pika+Gen-3），5 列同上

#### 4.6.3 路线分化

- 文字：2022-08 Stable Diffusion 开源后，diffusion 产品分化为闭源 (DALL-E[8] / Sora[10] / Veo[12] / Midjourney) 与开源 (SD / SDXL / SD3 / FLUX) 两条路线
- 文字：闭源主线以 API / SaaS 形式提供；开源主线提供权重 + 周边工具链 (ControlNet / LoRA / ComfyUI)，消费级 GPU 可跑[5]
- 文字：风格上 Midjourney 偏艺术化，DALL-E[8] / Veo[12] 偏写实，SD 因开源更全栈中立

**预算**：~350 字
**资产**：表格 ×2。

---

### References

按 `personal-doc-style.mdc §3.10` paper-style 格式，按"方法与架构 / 系统与产品 / 前置"三组分类，编号 [1]-[15]。

| # | 引用 | 来源 |
|---|---|---|
| [1] | DDPM | Ho et al., NeurIPS 2020. arXiv:2006.11239 |
| [2] | DDIM | Song et al., ICLR 2021. arXiv:2010.02502 |
| [3] | Classifier guidance | Dhariwal & Nichol, NeurIPS 2021. arXiv:2105.05233 |
| [4] | CFG | Ho & Salimans, arXiv 2022. arXiv:2207.12598 |
| [5] | LDM | Rombach et al., CVPR 2022. arXiv:2112.10752 |
| [6] | GEN-1 | Esser et al., ICCV 2023. arXiv:2302.03011 |
| [7] | DiT | Peebles & Xie, ICCV 2023. arXiv:2212.09748 |
| [8] | DALL-E 2 | Ramesh et al., arXiv 2022. arXiv:2204.06125 |
| [9] | Imagen | Saharia et al., NeurIPS 2022. arXiv:2205.11487 |
| [10] | Sora | OpenAI, technical report 2024-02 |
| [11] | SVD | Blattmann et al., arXiv 2023. arXiv:2311.15127 |
| [12] | Veo 3 | Google DeepMind, deepmind.google 2024-12 |
| [13] | GAN | Goodfellow et al., NeurIPS 2014. arXiv:1406.2661 |
| [14] | VAE | Kingma & Welling, ICLR 2014. arXiv:1312.6114 |
| [15] | Flow | Rezende & Mohamed, ICML 2015. arXiv:1505.05770 |

---

## 5. §6 章节调整

### 5.1 §6.2 内容前移

| 原 §6.2 子节 | 处理 | 去向 |
|---|---|---|
| 6.2.1 GEN-1 | 前移 | §4.5.1（开头一段，作为视频 diffusion 早期产品形态） |
| 6.2.2 三种范式 | 前移 | §4.5.2 表格 |
| 6.2.2 Sora 详细 | 前移 | §4.5.1 |
| 6.2.3 长 horizon quote box | 前移 | §4.5.3 |
| 6.2.3 与 World Models 收敛 | 前移 | §4.5.4 |

### 5.2 §6 重命名与时间区间调整

| 原 | 新 |
|---|---|
| `## 6. 第五阶段：World Models 起源 （2018-2023）` | `## 6. 第五阶段：World Models 起源 (2018)` |
| `### 6.1 World Models 2018 (Ha & Schmidhuber)` | （内容不变，编号不变） |
| `### 6.2 Runway GEN-1 与视频生成` | 整节删除 |

时间区间从 (2018-2023) 改为 (2018)，因 GEN-1 等 2023 内容已前移至 §4。

---

## 6. 风险

1. **跨章引用同步**：原笔记 §3.3 / §7.2 等可能 cite "§4.X" 编号，重写后需同步检查（实施时 grep）
2. **图片路径**：原图片在 `images/` 目录下，新 §4 引用相对路径需保持一致
3. **§1 整体趋势时间线**：原 §1 提到 "DDPM (NeurIPS 2020) → Stable Diffusion (2022-08) → Sora (2024-02)" 阶段标签，重写后无需改动（覆盖范围一致）
4. **§6.1.3 路线分歧**：原 §6.1.3 "JEPA vs LLM 主线"段落仍属 World Models 范畴，保留在 §6.1，不参与本次调整

---

## 7. Out of Scope

- §1 (整体趋势)
- §2 (判别式 AI)
- §3 (Transformer 范式)
- §5 (VLM)
- §6.1 (Ha & Schmidhuber 2018 V+M+C)
- §7 (具身 VLA)
- §8 (World Models 近期形态)

---

## 8. Spec Self-Review（按 brainstorming skill §Spec Self-Review）

| 检查项 | 状态 |
|---|---|
| Placeholder 扫描（TBD / TODO / 模糊要求）| ✅ 无 |
| 内部一致性（架构与功能描述匹配）| ✅ §3 骨架与 §4 详细设计逐节对应 |
| 范围检查（聚焦在单次实现）| ✅ 单次实现：仅 §4 重写 + §6 微调 |
| 歧义检查 | §4.5.4 与 §6 的指针表述需在实施时统一格式（"详见 §X" vs "→ §X"） |

修复：实施时统一用 "（详见 §X）" 行内格式。

---

## 9. 用户 Review Gate

按 brainstorming skill 流程，spec 写入后请用户审核。如确认 OK，进入 writing-plans。
