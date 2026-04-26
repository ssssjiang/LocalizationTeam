# AI Talk 稿件扩写到 60 min · 第一次分享只讲前 4 阶段 · 设计文档

**日期**：2026-04-27
**目标稿件**：`projects/personal-ai-talk-2026-04-24/05-full-script.md`
**演讲时间**：2026-04-24 周五 19:30–21:30（已过；本设计为后续重新安排的"分两次讲"做准备的第一次稿件版本）
**作者**：Songshu（本人讲）+ AI 协作整理

---

## 1. 背景与决策

第一次分享的处理时间有限，本次只覆盖前 4 阶段（开场 + 一/二/三/四 + 收尾），扩展点（推理大模型 / 具身 VLA / World Models 突破）留到下次。

**已锁定决策**（brainstorming 全过）：

| 决策 | 内容 |
|---|---|
| 总时长 | 60 min = 我讲 50 min + 讨论 10 min |
| 内容范围 | 只讲前 4 阶段；3 个扩展点下次讲 |
| 扩写方向 | 方案 X 均衡偏二/三：开场 +1 / 一 +1 / 二 +4 / 三 +4 / 四 +3 / 收尾 -2 |
| 扩写性质 | **技术深度优先**——不加新闻/release，加机制讲解 |
| 技术深度档 | **机制档**：核心机制 + 关键公式骨架，不展开推导 |
| 阶段四走法 | **A：保守加深**（V+M+C / GEN-1 / JEPA 各加机制段，结尾留钩子）|
| 收尾国内段 | 全文保留（含具身一线点名）|
| 讨论 Q3 | 原 Q3 全文保留（"VLA / 传统控制 / JEPA"路径之争）|
| 风险缓冲 | 收尾开头加一句过渡，预先解释"为什么点到了今晚没讲的内容" |

---

## 2. 时长账

| 段 | 原 | 新 | Δ |
|---|---|---|---|
| 开场 | 3 | 4 | +1 |
| 阶段一 判别式 AI | 6 | 7 | +1 |
| 阶段二 Transformer + LLM | 10 | 14 | +4 |
| 阶段三 Diffusion + VLM | 8 | 12 | +4 |
| 阶段四 World Models 起源 | 7 | 10 | +3 |
| 收尾 | 5 | 3 | -2 |
| **合计（我讲）** | **39** | **50** | **+11** |
| 讨论 | 15 | 10 | -5 |
| **总计** | **54** | **60** | **+6** |

注：原稿"我讲"实际是 39 min（开场 3 + 一 6 + 二 10 + 三 8 + 四 7 + 延伸 9 + 收尾 5 - 延伸 9 = 39，因为延伸段属于"我讲"但今晚不讲了，所以从基线扣掉）。

---

## 3. 各段扩写设计

### Section 1：开场（3 → 4 min）

**目的**：管理预期 + 修改"不讲公式"承诺。

**改动**：

1. 新增"今晚的范围声明"约 30 秒：明确说"只讲前 4 阶段，3 个新方向下次讲"
2. 修改"不讲公式"承诺：从"细节都不讲"改成"不推公式，但会写出几个**关键公式骨架**用于解释直觉，承诺不展开推导"

**事实/数据**：无新增引用。

---

### Section 2：阶段一 判别式 AI（6 → 7 min，+1 min）

**目的**：从"AI 史普及"升级为机制讲解。

**新增**：

- **A. CNN 机制段（+40s）**：卷积核 = 局部连接 + 权重共享 / 层级特征 = 感受野叠加 / 引用 Zeiler & Fergus 2013 可视化
- **B. ResNet 机制加深（+20s 净增）**：替换"恒等映射保底"的不严谨说法 → 改为"梯度反传角度"，写出
  ```
  ∂L/∂x = ∂L/∂y · (1 + ∂F/∂x)
  ```
  讲清 +1 让梯度有"高速公路"
- **C. RNN 失败的精确化（+15s 净增）**：梯度消失真实来源 = `∏ Wᵗ` / LSTM cell state 加法路径类似残差 / "事后看的相似性"——明确说明 LSTM 1997 ≠ ResNet 2015 的引用关系

**新增公式骨架**：1 行（ResNet 梯度）

**新增引用**：
- Zeiler & Fergus — Visualizing and Understanding CNNs (ECCV 2014): https://arxiv.org/abs/1311.2901
- Hochreiter & Schmidhuber — LSTM (1997): https://www.bioinf.jku.at/publications/older/2604.pdf

**待核查**：
1. AlexNet 26.2% → 15.3%（已在原稿，复核）
2. ResNet 152 层 / 3.57% top-5（复核）
3. seq2seq + Bahdanau 2014（复核）

---

### Section 3：阶段二 Transformer + LLM（10 → 14 min，+4 min）

**目的**：本场技术峰值。讲清 self-attention / scaling law / SSM 三套机制。

**新增**：

- **A. self-attention 机制段（+90s）**：Q/K/V 三角色比喻 / 写出公式
  ```
  Attention(Q, K, V) = softmax( QKᵀ / √d_k ) · V
  ```
  讲清 QKᵀ 是相似度 / √d_k 防 softmax 饱和 / softmax·V 是软查表 / multi-head 一句话 / 位置编码外挂一句话

- **B. Transformer 整体架构（+60s）**：encoder–decoder vs decoder-only / causal mask / **Add & Norm 残差连接回扣阶段一 ResNet**——这是阶段一→二的机制连接，全场最重要伏笔回收之一

- **C. Scaling Law 机制段（+60s）**：写出
  ```
  L(N, D, C) ≈ A · N^(-α) + B · D^(-β) + L_∞
  ```
  讲清幂律可预测性 / **Chinchilla 修正**（数据和模型应同步 scale）/ **Schaeffer 2023 涌现质疑论文**（NeurIPS 2023 Outstanding Paper：Are Emergent Abilities a Mirage？）

- **D. Mamba / SSM 机制段（+30s）**：写出
  ```
  h_t = A·h_{t-1} + B·x_t
  y_t = C·h_t
  ```
  讲清这就是控制论的状态空间模型 / Mamba 关键 = ABC 输入相关（selective）/ "attention 是软查表精确但 O(n²)，SSM 是状态压缩高效但有损"

**新增公式骨架**：3 行（attention + scaling law + SSM）

**新增引用**：
- Hoffmann et al. — Chinchilla (DeepMind 2022): https://arxiv.org/abs/2203.15556
- Schaeffer et al. — Are Emergent Abilities a Mirage? (NeurIPS 2023): https://arxiv.org/abs/2304.15004
- Gu & Dao — Mamba (2023): https://arxiv.org/abs/2312.00752

**待核查**：
1. **Vaswani 2017 §3.2.1 √d_k scaling 解释**——核 paper 原文
2. **Chinchilla 70B / 1.4T token 训练比例**——核数据点
3. **Schaeffer 2023 论文是否真为 NeurIPS 2023 Outstanding Paper**——核会议奖项
4. **Mamba selective SSM 中 ABC 是否真"输入相关"**——核 Mamba paper §3
5. **GPT-3 175B / Llama-3 70B 用 15T token**——核 Llama-3 训练数据量

**国内 LLM 副线**（Qwen / GLM / Kimi）：完全保留原稿，不动。

---

### Section 4：阶段三 Diffusion + VLM（8 → 12 min，+4 min）

**目的**：讲清 Diffusion 为什么稳 / CLIP 怎么训 / 两者怎么合体造 text-to-image。

**新增**：

- **A. Diffusion 机制段（+90s）**：
  - forward 任意 t 步可一步采样：`x_t = √α_t · x_0 + √(1-α_t) · ε`
  - 写出训练目标：
    ```
    L_simple = E[ ‖ ε - ε_θ(x_t, t) ‖² ]
    ```
  - 讲清 L2 回归极简 / 为什么预测 ε 不预测 x_0 / 为什么稳（无 min-max）
  - 采样加速：DDIM / DPM-Solver
  - **Latent Diffusion**：SD 在 64×64 latent 上扩散，不在 512×512 像素上——SD 工业落地的真正机制核心

- **B. CLIP 对比学习机制段（+60s）**：N×N 相似度矩阵 / InfoNCE 直觉（N 选 1 分类）/ 4 亿对的负样本质量 / 零样本 ImageNet 76% top-1 = ResNet-50

- **C. Diffusion + CLIP 合体段（+60s）**：text-to-image 流程拆开：CLIP encoder → cross-attention → diffusion U-Net / **classifier-free guidance** 公式 `ε_cond - ε_uncond` 解释 SD 的 "CFG scale 7.5" 参数由来

- **D. GAN/VAE 失败的精确化（+30s）**：GAN min-max 没单一 loss 可监控 / VAE L2 = 高斯假设强行单峰平均 / Diffusion 把生成转成单步噪声回归避开两者痛点

**新增公式骨架**：1 行（DDPM L_simple）

**新增引用**：
- Rombach et al. — Latent Diffusion Models (CVPR 2022): https://arxiv.org/abs/2112.10752
- Song et al. — DDIM (ICLR 2021): https://arxiv.org/abs/2010.02502
- Ho & Salimans — Classifier-Free Diffusion Guidance (2022): https://arxiv.org/abs/2207.12598

**待核查**：
1. **DDPM L_simple = ‖ε - ε_θ‖²**——核 Ho 2020 §3.2
2. **forward 累积公式 √α_t / √(1-α_t)**——核 paper 中 α 是 ᾱ 的累积版本
3. **CLIP zero-shot ImageNet 76% top-1 = ResNet-50**——核 Radford 2021
4. **CLIP 4 亿对训练数据**——已在原稿，复核
5. **Stable Diffusion 2022.08 开源**——已在原稿，复核
6. **Latent Diffusion = Rombach 2022 CVPR**——核会议年份

---

### Section 5：阶段四 World Models 起源（7 → 10 min，+3 min）

**目的**：讲清 V+M+C 怎么 work / GEN-1 时间一致性怎么解 / JEPA 之争是什么。

**新增**：

- **A. V+M+C 机制段（+75s）**：
  - V (VAE) 64×64 RGB → 32 维 latent
  - M (MDN-RNN) 输出 P(z_{t+1} | z_t, a_t)——**关键是分布而非单值**
  - C 用 CMA-ES 演化算法训，参数极少
  - 写出函数签名：
    ```
    C : (z_t, h_t) → a_t
    ```
  - "在梦里训练" 的真实含义：M 模拟 latent 序列、C 在里面训、放回真实环境 zero-shot 跑通 CarRacing
  - **为什么 6 年没 scale**：< 10M 参数 / 32 维 latent 表达力小 / 需要 LLM 时代基础设施——**这是给下次扩展 3 留的钩子**

- **B. GEN-1 视频时间一致性（+60s）**：
  - 难点 = 时间一致性（物体跨帧不漂）
  - Esser 2023 解法：structure（深度图）+ content（文本/参考图）解耦 / temporal attention 插入 spatial attention 之后 / 微调而非从头训
  - 直觉："2D U-Net 拉伸成 3D"
  - 现状对照：Sora / Veo / Veo 3 是同范式工业化

- **C. JEPA / 自回归之争（+45s）**：
  - LLM 自回归本质 = `P(x_t | x_<t)`
  - LeCun 反对：像素级预测浪费容量 / 多峰分布强制单点 = 模糊回避
  - JEPA 解法：x 和 y 都过 encoder，预测 `s_y` 在表示空间里的状态——**不是像素级预测**
  - 直觉："LLM 预测下一个词，JEPA 预测下一个抽象状态"
  - 现状（坦诚的钩子）：JEPA 至今没爆点产品，但概念吸引力强；Genie 3 / Cosmos / GR00T N1.6 是这条路 2025-2026 的落地——**下次讲扩展 3 时展开**
  - **不站队**：SLAM 视角的人讲这段刚好两边都不偏

- **D. 阶段四收尾钩子（+20s）**：保留"它们指出了下一个阶段会爆发的方向"，加一句承诺"下次会展开讲推理 / VLA / WM 突破，把今晚埋的种子全部展开"

**新增公式骨架**：1 行（V+M+C 函数签名，非数学公式）

**新增引用**：
- Assran et al. — I-JEPA (CVPR 2023): https://arxiv.org/abs/2301.08243
- Bardes et al. — V-JEPA (Meta 2024): https://ai.meta.com/research/publications/v-jepa/
- LeCun 2022 — A Path Towards Autonomous Machine Intelligence: https://openreview.net/pdf?id=BZ5a1r-kVsf

**待核查**：
1. **V+M+C 32 维 latent / CarRacing 任务细节**——核 Ha & Schmidhuber 2018
2. **GEN-1 structure = depth map / temporal layer 插入位置**——核 Esser 2023
3. **Sora 2024.02 / Veo 2024.05 / Veo 3 2025**——核具体时间
4. **V-JEPA Meta 2024.02 发布**——核时间
5. **I-JEPA CVPR 2023**——核会议
6. **VICReg ICLR 2022**——核会议年份

---

### Section 6：收尾（5 → 3 min，**-2 min**）

**目的**：4 阶段总结 + 国内格局判断 + 3 个讨论问题。

**改动**：

1. **删除**："3 个新方向回收成 agent" 整段（约 -2 min）——今晚不讲扩展点，回收会违和
2. **替换为**：4 阶段单独总结约 60s
   - 一 = 学会感知
   - 二 = 学会规模化
   - 三 = 学会创造与跨模态
   - 四 = 学会想象世界（玩具阶段）
   - 承诺下次讲扩展 3
3. **加一句过渡（约 5s）**：
   > "下面我提到的国内具身、VLA 这些点——今天没展开讲，留到下次；这里点出来只是为了让大家先看到 2026 年完整的格局。"
   作用：预先解释收尾段为什么会出现"今晚没讲"的内容，降低追问压力。
4. **国内格局判断**：**全文保留**（含 LLM 一线 + 具身一线点名 GraspVLA / 智元 GO-1 / 宇树 UnifoLM-VLA-0）
5. **3 个讨论问题**：
   - Q1：scaling 的尽头（保留）
   - Q2：开源 vs 闭源的格局（保留）
   - Q3：具身智能的路径之争（**全文保留**——含 VLA / 传统机器人控制 / LeCun JEPA 路径之争）

---

## 4. 全场公式骨架清单

机制档允许的全部公式骨架，共 **5 行**，分布如下：

| 段 | 公式 | 用途 |
|---|---|---|
| 阶段一 ResNet | `∂L/∂x = ∂L/∂y · (1 + ∂F/∂x)` | 解释残差为什么帮助优化 |
| 阶段二 Attention | `Attention(Q,K,V) = softmax(QKᵀ/√d_k)·V` | 全场技术峰值 |
| 阶段二 Scaling Law | `L(N,D,C) ≈ A·N^(-α) + B·D^(-β) + L_∞` | 解释幂律可预测性 |
| 阶段二 SSM | `h_t = A·h_{t-1} + B·x_t; y_t = C·h_t` | 解释 Mamba 线性复杂度 |
| 阶段三 Diffusion | `L_simple = E[‖ε - ε_θ(x_t,t)‖²]` | 解释训练为什么稳 |
| 阶段四 V+M+C | `C : (z_t, h_t) → a_t` | 函数签名（非数学公式）|

---

## 5. 风险点登记

1. **收尾段会点名今晚没讲的内容**（国内具身 / VLA）—— 已用"过渡句"缓冲
2. **Q3 涉及今晚没讲的术语**（VLA、JEPA）—— JEPA 阶段四 C 段会讲；VLA 没讲到，但 Q3 是讨论环节，可以现场用一句话解释 "VLA = 视觉语言动作模型，下次展开"
3. **公式骨架共 5 行**——已修改开场承诺，从"不讲公式"改为"不推公式只给关键骨架"，承诺一致
4. **Schaeffer 2023 涌现质疑 / Chinchilla 修正**——讲了人设值高，但需要周一晚学到能 sustain 一个追问
5. **JEPA 路线**——技术上较抽象，能否讲透取决于学习时间

---

## 6. 待核查事实总清单（**生稿前完成**）

新增引用 / 数据点共 **20 项**待核：

**阶段一（3 项）**
1. AlexNet 26.2% → 15.3% top-5
2. ResNet 152 层 / 3.57% top-5
3. seq2seq + Bahdanau 2014

**阶段二（5 项）**
4. Vaswani 2017 §3.2.1 √d_k scaling
5. Chinchilla 70B / 1.4T token 比例
6. Schaeffer 2023 是否 NeurIPS 2023 Outstanding Paper
7. Mamba selective SSM ABC 是否真输入相关
8. Llama-3 70B / 15T token 训练

**阶段三（6 项）**
9. DDPM L_simple §3.2
10. forward 累积公式 √α_t / √(1-α_t)
11. CLIP zero-shot ImageNet 76% = ResNet-50
12. CLIP 4 亿对
13. Stable Diffusion 2022.08 开源
14. Latent Diffusion CVPR 2022 / Rombach et al.

**阶段四（6 项）**
15. V+M+C 32 维 latent / CarRacing
16. GEN-1 structure = depth / temporal layer 位置
17. Sora 2024.02 / Veo 2024.05 / Veo 3 2025
18. V-JEPA Meta 2024.02
19. I-JEPA CVPR 2023
20. VICReg ICLR 2022

核查方式：web 搜索（multi-source 优先官方/论文/会议），结果汇入 `09-fact-check-log.md`，所有冲突先停笔询问。

---

## 7. 实施顺序

1. **核查待核事实清单（20 项）**——w eb 搜索，更新 `09-fact-check-log.md`
2. **生稿**：按本设计修改 `05-full-script.md`（开场 + 一 + 二 + 三 + 四 + 收尾，共 6 段）
3. **审稿**：用户审定稿
4. **同步更新**：
   - `06-reading-list.md`：补 8 个新引用
   - `07-qa-bank.md`：补阶段二/三/四新增机制对应的追问 Q&A
   - `09-fact-check-log.md`：所有新增数据点入档
   - `README.md`：节奏从"4 晚学习"改为"按新版前 4 阶段重新组织"
5. **commit + push**

---

## 8. 设计审核 checkpoint

完成本设计后，下一步：

1. 用户审本 design doc
2. 通过后，**先做事实核查**（步骤 1），把所有 20 项核完，列冲突供决策
3. 核完后再生稿
4. 生稿后再交付审稿
