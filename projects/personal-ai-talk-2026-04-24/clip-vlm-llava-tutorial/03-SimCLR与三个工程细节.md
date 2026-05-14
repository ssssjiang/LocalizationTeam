# 📘 第 3 课：SimCLR 与三个反直觉的工程细节

> 学习目标：通过 SimCLR 看一个**完整对比学习管线**长什么样；
> 吃透三个反直觉但极其重要的工程细节，它们直接被 CLIP 继承。
>
> 预计阅读时间：30 分钟。读完本章，**第 4 章 CLIP 你只需要把"图-图"换成"图-文"**。

---

## 一、SimCLR 是什么、为什么重要

**SimCLR** = A **Sim**ple Framework for **C**ontrastive **L**earning of Visual **R**epresentations
（Chen et al., 2020.02, Google Brain）

它的历史地位：

> 2020 年初，SimCLR 用纯对比学习，在 ImageNet 上达到与监督学习**几乎持平**的精度（76.5% vs 76.5%）。
> 这是自监督学习首次在大规模视觉任务上**追平监督学习**——**"自监督的春天"**从此开始。

但 SimCLR 真正的重要性不在于 SOTA，而在于：

> **它是对比学习史上"最干净"的范式——没有 momentum encoder、没有 memory queue、没有花哨技巧，全靠暴力 batch size 和精心设计的 augmentation。**

理解了 SimCLR，你就理解了 CLIP（CLIP 几乎 1:1 复用 SimCLR 的训练管线，只是把"图-图对比"换成"图-文对比"）。

---

## 二、SimCLR 完整管线

### 一张图看懂全流程

```
                  ┌─── 原图 x ───┐
                  │              │
              augment t₁      augment t₂        ← 两次独立的随机数据增强
                  │              │
                  ▼              ▼
                 x̃₁             x̃₂           ← 同一原图的两个视图
                  │              │
                  │  encoder f   │              ← 共享权重的 ResNet
                  ▼              ▼
                  h₁             h₂           ← representation（用于下游任务）
                  │              │
                  │  projection g│              ← 2 层 MLP（带 ReLU）
                  ▼              ▼
                  z₁             z₂           ← projection（用于对比损失）
                  │              │
                  └──── 拉近 ────┘
                         ↕
                  与同 batch 内
                所有其他 z 拉远
                         ↓
                    InfoNCE Loss
```

### 训练循环（Pseudo-code）

```python
# SimCLR 训练循环（极简版）
for batch in dataloader:
    # batch.shape = [N, C, H, W]，N 是 batch size

    # 1. 对每张图做两次独立增强
    x1 = augment(batch)   # [N, C, H, W]
    x2 = augment(batch)   # [N, C, H, W]

    # 2. encoder 提取表征
    h1 = encoder(x1)      # [N, 2048]
    h2 = encoder(x2)      # [N, 2048]

    # 3. projection head
    z1 = projection_head(h1)   # [N, 128]
    z2 = projection_head(h2)   # [N, 128]
    z1 = F.normalize(z1, dim=1)  # L2 归一化
    z2 = F.normalize(z2, dim=1)

    # 4. 拼成 2N × 2N 相似度矩阵
    z_all = torch.cat([z1, z2], dim=0)   # [2N, 128]
    sim_matrix = z_all @ z_all.T / tau   # [2N, 2N]

    # 5. 对每一行，正确"类别"是它对应的另一视图
    # （第 i 行的 positive 是第 (i + N) % 2N 列）
    labels = torch.cat([torch.arange(N, 2*N), torch.arange(0, N)])

    # 6. 排除自己（对角线置 -inf）
    sim_matrix.fill_diagonal_(-float('inf'))

    # 7. 标准 cross entropy
    loss = F.cross_entropy(sim_matrix, labels)

    loss.backward()
    optimizer.step()
```

> 看，SimCLR 的全部代码就这么多。**整个管线在 PyTorch 里 30 行能写完。**
>
> 如果你看懂了这段代码，你已经理解了 SimCLR 的全部精髓。

### 一个 batch 的对比关系

设 batch size $N = 4$，那么 $z_{\text{all}}$ 是 $[8, 128]$，相似度矩阵是 $8 \times 8$：

```
            z1[0] z1[1] z1[2] z1[3] z2[0] z2[1] z2[2] z2[3]
z1[0]   [   -∞   -    -    -    ⭐    -    -    -   ]   ← positive: z2[0]
z1[1]   [   -    -∞   -    -    -    ⭐    -    -   ]   ← positive: z2[1]
z1[2]   [   -    -    -∞   -    -    -    ⭐    -   ]
z1[3]   [   -    -    -    -∞   -    -    -    ⭐  ]
z2[0]   [   ⭐    -    -    -    -∞   -    -    -   ]   ← positive: z1[0]
z2[1]   [   -    ⭐    -    -    -    -∞   -    -   ]
z2[2]   [   -    -    ⭐    -    -    -    -∞   -   ]
z2[3]   [   -    -    -    ⭐    -    -    -    -∞  ]
```

每行的"正确答案"是它对应的另一视图（⭐ 标记）；每行的"干扰项"是 batch 内其他 6 个样本的两个视图。

→ batch size = 4 → 每个样本对比 (2N - 2) = 6 个负例。
→ batch size = 4096 → 每个样本对比 8190 个负例。**这就是为什么要拉大 batch。**

---

## 三、第一个反直觉细节：必须用**强**数据增强

### 实验观察

SimCLR 论文的 Figure 5 给了一张极重要的图：**测试 7 种 augmentation 单独用、两两组合用**对最终精度的影响。

结论触目惊心：

> **用单一 augmentation 训练效果**：~30% top-1 (随机猜还多点)
> **用 2 个 augmentation 组合训练效果**：~70% top-1
>
> **从弱到强 augmentation：精度差 40 个百分点。**

### SimCLR 的"标准 augmentation 组合"

```
1. 随机裁剪（Random Crop）+ 缩放回 224×224  ← 最重要
2. 颜色抖动（Color Jitter）：亮度/对比度/饱和度/色相        ← 第二重要
3. 随机翻转（Random Flip）
4. 高斯模糊（Gaussian Blur）
5. 灰度化（Grayscale，10% 概率）
```

### 为什么必须强 augmentation？反直觉的解释

直觉上，"augmentation 越温和，模型越容易学" → 错。

**对比学习的本质是"让模型学会忽略表面变化"**。如果增强太弱：

- $x_1$ 和 $x_2$ 几乎一模一样
- 模型可以靠"匹配像素"轻松识别它们是同源
- → 学到的"表征"实际上还是像素层面的，而不是语义层面的

只有当 $x_1$ 和 $x_2$ **看起来差异很大、但语义不变**时，模型才会被迫学到**对增强不变**的语义级表征。

### 一个具体例子

| augmentation 强度 | 模型学到什么 |
|---|---|
| 极弱（只翻转） | "这张图大致就是这个像素分布" — 学到的是模板 |
| 中等（翻转 + 轻裁剪） | "中心区域大致一样" — 学到的是中心物体的颜色 |
| 强（裁剪 + 颜色抖动 + 模糊） | "无论怎么变，这都是一只猫" — 学到的是**语义** |

> 🎯 **关键洞察**：augmentation 的强度，决定了表征的抽象层级。
>
> 强 augmentation **=** 困难任务 **=** 高质量表征。

### 这条洞察如何被 CLIP 继承

CLIP 没有传统意义的"两次 augmentation"——它的"两个视图"就是**图本身 + 配套的文本描述**。但精神是一样的：

- 同一概念（"小猫"）的图像和文本，在像素和字符层面**差异极大**，但语义相同
- 让模型在这种"巨大表面差异 + 语义一致"的对里学习 → 逼模型学到**跨模态的语义表征**

→ CLIP 的"图-文对"是对比学习"强 augmentation"思想的**终极版本**。

---

## 四、第二个反直觉细节：projection head（投影头）的存在

### 现象

回去看上面的管线图。注意 encoder 之后还有一个叫 **projection head** 的 MLP：

```
原图 → augmented → encoder (ResNet) → h ─┬─→ projection (MLP) → z → InfoNCE Loss
                                          │
                                          └─→ h 被用于下游任务（分类、检索）
```

**反直觉的点**：

> 训练时用 $z$ 算 loss，但下游任务用 $h$（**而不是 $z$**）。
>
> 这等于"训练完之后把 projection head 扔掉"。

——这件事看起来很奇怪。为什么不直接用最终的 $z$？为什么训练时要"绕一圈"？

### 实验观察

SimCLR 论文的 Table 1 / Figure 8 对比：

| 表征来源 | ImageNet top-1 (linear probe) |
|---|---|
| 直接用 encoder 输出 $h$ | **65.6%** |
| 用 projection head 输出 $z$ | 57.2% |
| 加一层 MLP projection | **66.9%** |

> **加 projection head 比不加好；但下游用 $h$ 比用 $z$ 好 8 个百分点。**

### 为什么会这样？反直觉的解释

关键直觉：

> **InfoNCE 损失会"破坏"一些下游任务有用的信息。**

具体来说，对比学习目标是"对增强不变"——所以 InfoNCE 会推动表征**忽略**所有跟"识别同源"无关的信息：

- 颜色信息？被 color jitter 破坏 → InfoNCE 推动表征忽略颜色
- 朝向信息？被 flip 破坏 → 推动忽略朝向
- 局部细节？被 crop 破坏 → 推动忽略

但是这些信息对**下游任务**可能很重要！比如分类"红绿灯"，颜色就是核心特征。

**projection head 的作用**：在 encoder 和 loss 之间架一个**缓冲层**。让 InfoNCE 的"忽略"压力作用在 projection head 上，而不是直接破坏 encoder 学到的特征。

```
    encoder h (信息丰富)
         │
         │  projection head g 在这里"消化"
         │  InfoNCE 的破坏性压力
         ▼
    projection z (只保留对比所需的信息)
         │
         ▼
    InfoNCE Loss
```

下游用 $h$ → 得到信息丰富的表征。
训练时用 $z$ → 让 InfoNCE 在 $z$ 这一层完成它的"信息压缩"工作。

### 一个比喻

想象你雇了一个翻译，让他把英文小说翻译成日文。如果你**直接用翻译过的日文**做下游任务（比如分析人物动机），会丢失原作的很多 nuance。

更好的做法：让翻译同时给你**翻译稿（z）**和**翻译时的笔记/原文摘录（h）**。下游分析用笔记/摘录，翻译稿只是"翻译这个动作"的副产品。

### 这条洞察如何被 CLIP 继承

CLIP 的图像编码器 ViT-L/14 输出 1024 维特征 → 经过一层线性投影到 768 维（共享空间维度）→ 再 L2 归一化算 InfoNCE。

但**下游用 CLIP 做特征提取时，主流做法是用 ViT 倒数第二层的 [CLS] token**（也就是投影前的表征），而不是投影后的最终向量——同样的原理。

---

## 五、第三个反直觉细节：batch size 必须巨大

### 实验观察

SimCLR 论文 Figure 9：

```
ImageNet linear eval top-1
70% ┤              ╱━━━━━
    │           ╱╱
65% ┤        ╱╱
    │     ╱╱
60% ┤   ╱
    │ ╱
55% ┤
    └────┬────┬────┬────┬────────
         256  512 1024 2048  4096   batch size
```

batch size 从 256 → 4096：精度提升 **8 个百分点**。

更夸张的：训练 epoch 数也影响，但 **batch size 影响远大于 epoch 数**。

### 为什么？

回到第 2 章的核心直觉：

> 负样本越多 → InfoNCE 分母候选越多 → 分类任务越难 → 表征越好。

batch size $N$ 的 SimCLR：每个样本对比 $2N - 2$ 个负例。
- $N = 256$：每个样本对比 ~510 个负例
- $N = 4096$：每个样本对比 ~8190 个负例

负例数差 16 倍——精度差 8 个百分点。

### 工程难题

batch size = 4096 + ResNet-50 + 224×224 图像，这件事**非常贵**：

- 显存：单 GPU 装不下，必须多 GPU 数据并行
- BatchNorm：跨 GPU 同步（**Sync BN**）
- 梯度通信：4096 个样本的梯度累加，通信开销大
- 学习率：要按 batch size 线性放缩（lr = 0.3 × N/256）

SimCLR 论文用了 **128 个 TPU**训练 1000 epoch。家用 GPU 跑 SimCLR 几乎是绝望的。

### 后续工作如何"绕过"这个限制？

**MoCo（Momentum Contrast, He et al., 2020）**给出了一个机巧解法：

```
                   query encoder       (普通编码器)
                        │
                        ▼
                       q
                        │
                        ↓
                  ┌─────┴─────┐
                  │           │
                  ▼           ▼
              positive    negatives ←── Queue (size = 65536)
                  ↑           ↑              ↑
                  │           │              │
              key encoder    历史 batch 的    momentum update:
              (slow update)  k 们都缓存在    θ_k ← m·θ_k + (1-m)·θ_q
                             这个队列里
```

核心思想：

1. 维护一个 **memory queue**，大小可以是 65536（远大于任何能放进 GPU 的 batch）。
2. 每个 batch 用 query encoder 算 $q$，用 key encoder 算 $k^+$。
3. 把这一 batch 的 $k^+$ 加入 queue，把最老的 batch 弹出。
4. **整个 queue 都作为负例参与对比**。

这样不需要拉大 batch size 也能有 65536 个负例。代价是 key encoder 必须用 momentum 缓慢更新（不然 queue 里的旧表征和新表征不兼容）。

### 这条洞察如何被 CLIP 继承

CLIP 选择了"老老实实拉大 batch size"的路：

> **CLIP batch size = 32768。**

这是 SimCLR 4096 的 8 倍。OpenAI 用了几百张 V100 训了 12 天。

为什么 CLIP 不用 MoCo 的 queue？我猜（论文没明说）：

- 图-文对比涉及两个模态，queue 设计更复杂
- OpenAI 算力充足，直接暴力拉 batch 简单可靠
- 32K batch + 4 亿训练对，已经是当时见过最大规模

---

## 六、把三个细节串起来

```
                    ┌──────────────────────────────────┐
                    │        SimCLR 三大支柱            │
                    └──────────────────────────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            ▼                     ▼                     ▼
     强 augmentation       projection head        large batch size
            │                     │                     │
       让任务变难，         让 InfoNCE 的破坏性     让负样本足够多，
     逼模型学语义级表征     压力作用在 projection     互信息下界更紧
                            上，而不是 encoder
            │                     │                     │
            └─────────────────────┴─────────────────────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │ 高质量视觉表征   │
                        └─────────────────┘
```

这三个细节本质上都在解决同一个问题：

> **如何让 InfoNCE 这个"简单的 softmax"真的学到好的表征？**

- augmentation 决定**任务难度**
- projection head 决定**信息保留**
- batch size 决定**对比规模**

CLIP 把这三件事原封不动地搬过去，只是把"图-图"换成了"图-文"。

---

## 七、本章一句话总结

> 🎓 **SimCLR = 强 augmentation + projection head + large batch + InfoNCE。**
>
> 这是对比学习的"最小完整范式"，CLIP 的训练管线就是它的图文版。

---

## 八、为下一章铺路

下一章我们正式进入 **CLIP**。在你打开第 4 章前，先在脑子里做这个**思想实验**：

> 想象 SimCLR 的 batch 不是"同一张图的两个增强视图"，而是"一张图 + 描述这张图的一段文字"。
>
> - $x_1$ = 图像 → $z_1$ = 图像表征
> - $x_2$ = 文本 → $z_2$ = 文本表征
> - InfoNCE：让"图 i 的表征"和"文 i 的表征"靠近、与其他文的表征远离

**就这一行思想替换，你已经懂了 CLIP 的全部核心。**

第 4 章会做的事：
1. 解释为什么这个替换有意义（→ 解决 ImageNet 范式的封闭词表困境）
2. 讲对称损失（i2t + t2i 双向）的细节
3. 解读著名的 N×N 矩阵图（CLIP 论文 Figure 1）

---

## ✅ 课后检查

### Q1（必答 · 理解题）
为什么"弱 augmentation 训练效果差"？这个观察怎样反过来支持了 CLIP 的"图文对"作为终极强 augmentation？

### Q2（必答 · 设计题）
SimCLR 论文里发现"projection head 是 2 层 MLP 比 1 层好"。如果让 projection head 加到 5 层呢？你猜会发生什么？为什么？

### Q3（必答 · 推理题）
MoCo 用 queue 模拟大 batch size，这种做法在"图-图对比"里 work，但在 CLIP 这种"图-文对比"里复杂度会变高。你能想到为什么吗？

### Q4（选答 · 综合题）
回顾第 1-3 章，对比学习的范式有 3 个关键 ingredients：
1. 用"同物近、异物远"作为训练信号
2. 用 InfoNCE 把它包装成 (N+1) 类分类
3. 用 augmentation + projection head + large batch 让它真的 work

如果让你自己设计一个**视频对比学习**的方法，你会怎么定义 positive 和 negative？

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
>
> Q3:
>
> Q4:

## 🤔 我的疑问（你来填）

> -
> -

---

## 📋 参考答案

<details>
<summary>点开看 Q1 参考</summary>

**为什么弱 aug 不好**：弱 augmentation 下，$x_1$ 和 $x_2$ 在像素层面就很相似，模型可以靠"匹配像素"就完成"识别同源"任务，根本不需要学到语义。结果学到的表征停留在低层次（颜色直方图、边缘分布），下游任务用不上。

**对 CLIP 的支持**：CLIP 的"图-文对"是 augmentation 的终极版——图像和文本在像素和字符层面**差异巨大**（一张图的像素和"a photo of a cat"这串字符没有任何浅层相似性），但语义一致。这种"巨大表面差异 + 语义一致"逼模型学到**纯粹的语义表征**，效果远超传统的图像增强。

可以这样类比：
- SimCLR 的 augmentation 强度：60 分
- CLIP 的"图-文对"作为 augmentation：100 分
</details>

<details>
<summary>点开看 Q2 参考</summary>

**5 层 projection head 会怎样？**

可能效果反而变差。原因：

1. **过度参数化**：projection head 越深，能力越强，能"完美"消化 InfoNCE 的破坏性压力——但代价是 encoder 学到的表征也开始"变形"以配合 projection head（梯度反传时 projection 会反过来塑造 encoder）。
2. **训练不稳定**：深层 MLP 训练 dynamics 复杂，可能 collapse。
3. **缓冲过度**：太深的 head 会让 InfoNCE 的信号"消失"在 projection 内部，encoder 可能学不到任何有用信息。

SimCLR 论文实测 1 层 vs 2 层 vs 3 层，2 层最好（66.9% > 65.5% > 65.0%）。3 层之后开始下降。

→ projection head 是个"恰到好处"的设计，**过浅信息消化不掉、过深训练失控**。
</details>

<details>
<summary>点开看 Q3 参考</summary>

MoCo 的 queue 在图-图对比里只需要存**一个模态**（图像）的表征。CLIP 是双模态的，至少有两个复杂性：

1. **要存两套 queue**：一个图像 queue、一个文本 queue。
2. **对称损失需要双向对比**：
   - 图 query 要对所有文本 key 做 InfoNCE
   - 文 query 要对所有图 key 做 InfoNCE
   - 两个 queue 必须同步更新
3. **momentum encoder × 2**：图像和文本都需要 momentum encoder 维护慢速更新。

这种复杂度让 OpenAI 直接选了"暴力拉大 batch"的简单路线。后来确实有人做了 MoCo 风格的图-文对比（如 ALBEF, Li et al. 2021），但工程复杂度比 CLIP 高得多。

→ 设计哲学：**如果有钱，简单暴力总比复杂巧妙更可靠**。
</details>

<details>
<summary>点开看 Q4 参考</summary>

视频对比学习的几种合理设计：

**方案 A：同视频不同时刻为 positive**
- positive：从同一视频中采两个不同时刻的 clip
- negative：其他视频的 clip
- 学到的：时序不变性（同一场景在不同时刻应有相似表征）
- 代表工作：CVRL (Qian et al., 2021)

**方案 B：同视频不同 view 为 positive**
- positive：同一视频，做时间裁剪 + 空间裁剪 + 颜色抖动
- 完全类比 SimCLR
- 代表工作：VideoMoCo

**方案 C：跨模态（视频 + 文本/音频）**
- positive：视频片段和它对应的字幕/解说音频
- 学到的：跨模态对齐
- 代表工作：MIL-NCE (Miech et al., 2020), VATT (Akbari et al., 2021)

无论哪种方案，3 个核心 ingredients 都是一致的：
1. 用某种"自然成对关系"定义 positive（同视频不同时刻、视频和字幕…）
2. InfoNCE 损失
3. 强 augmentation + projection head + large batch

→ 你能在新问题上**重新发明 SimCLR 的范式**了。
</details>

---

## 🎉 阶段性里程碑

恭喜，你完成了**对比学习预热**（第 1-3 章）。现在你应该能：

- ✅ 用一句话讲清"对比学习为什么会出现"
- ✅ 写出 InfoNCE 公式并解释每一项
- ✅ 解释 SimCLR 的三个工程细节（强 aug、projection head、large batch）
- ✅ 在脑子里把"图-图对比" → "图-文对比"的思想替换走一遍

下一章正式进入 **CLIP** 主线。所有铺垫到位，CLIP 的核心思想会让你有"水到渠成"的感觉。

---

**下一课预告**：

➡️ [`04-CLIP核心思想与架构.md`](./04-CLIP核心思想与架构.md)

我们会回答 CLIP 的三个核心问题：

1. **它要解决什么？** → ImageNet 范式的封闭词表困境
2. **它的关键设计是什么？** → 双塔 + 对称 InfoNCE + 巨型图文数据集
3. **它的 N×N 矩阵图（论文 Figure 1）每一项在算什么？**
