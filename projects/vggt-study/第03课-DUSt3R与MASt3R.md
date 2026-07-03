# 📘 第 03 课：支线 B — DUSt3R & MASt3R（pointmap 回归家族）

> 真实来源：
> - **DUSt3R** [arXiv 2312.14132](https://arxiv.org/abs/2312.14132)（Wang, Leroy, Cabon, Chidlovskii, Revaud, NAVER LABS Europe, CVPR 2024）/ 项目页 [dust3r.europe.naverlabs.com](https://dust3r.europe.naverlabs.com/)；架构与公式引用其 §3.1、Fig. 2、Eq. (1)/(4)
> - **MASt3R** [arXiv 2406.09756](https://arxiv.org/abs/2406.09756)（Leroy, Cabon, Revaud, ECCV 2024）/ [NAVER LABS 博客](https://europe.naverlabs.com/blog/mast3r-matching-and-stereo-3d-reconstruction/)；matching head / InfoNCE / FRM 引用其 §3.2、§3.3
> 学习目标：把 VGGT 最直接的「亲爹」吃透——理解 ① DUSt3R 凭什么能不要相机参数就出 3D（pointmap + 同坐标系这一招）；② 它卡在哪（只能两张 + 要 global alignment）；③ MASt3R 给它补了哪两块（matching head + metric + 快速匹配）。把这节的「死穴」记牢，第 04 课你就能秒懂 VGGT 到底突破了什么。

---

## 开场：先接上第 01 课那根线

第 01 课我们埋了一句话：

> DUSt3R 证明了「前馈直接出 3D 是可行的」，但卡在「只能两张、要靠后优化拼多张」。

这节课就把这句话拆开，讲透每一个字。先讲 DUSt3R（怎么 work + 卡在哪），再讲 MASt3R（怎么补）。

---

## 一、DUSt3R 的核心一招：pointmap + 「都搬到第一台相机的坐标系」

### 先回忆传统怎么出 3D（第 00 课）

传统五步里，3D 点是这么来的：**先求相机参数（内参 + 位姿），再拿同名点三角化**。所以相机参数是「必需前置条件」，没有它就没法 triangulate。

> 📖 DUSt3R 项目页原话点了这个痛：*"these [camera parameters] are usually tedious and cumbersome to obtain, yet they are mandatory to triangulate corresponding pixels in 3D space."*

### DUSt3R 反过来：先不要相机参数，直接回归 3D

DUSt3R 的网络 $f$ 干的事，一句话：

> 💡 **输入两张 RGB 图 $I^1, I^2$，直接前馈输出两张 pointmap $X^{1,1}, X^{2,1}$，外加两张置信度图 $C^{1,1}, C^{2,1}$。**

这里有个**最关键、也最容易绕晕的点**——上标的含义（这是理解整篇的钥匙）：

- pointmap $X^{n,m}$ 读作：「**第 $n$ 张图的 3D 点，表达在第 $m$ 台相机的坐标系里**」。
- 所以 $X^{1,1}$ = 第 1 张图的点云，在第 1 台相机系里（自然）。
- 而 $X^{2,1}$ = **第 2 张图的点云，也表达在第 1 台相机的坐标系里**（注意上标是 1，不是 2！）。

> 📖 来自 DUSt3R §3.1、Eq. (1)：$X^{n,m} = P_m P_n^{-1} h(X^n)$，其中 $P$ 是 world-to-camera 位姿。Fig. 2 caption 明确写：*"the two pointmaps are expressed in the same coordinate frame of the first image $I^1$."*

### 🎯 为什么「都搬到第一台相机系」是神之一手

你停下来想 10 秒——如果两张图的点云**已经在同一个坐标系里**了，那意味着什么？

- 两张图的同名点，**坐标天然就对齐**了（不用再做匹配 + 三角化）。
- 第 2 台相机相对第 1 台的位姿 → 直接能从 $X^{2,1}$ 反解（因为它就是「第 2 张图的点摆在第 1 台系里」，反推一下变换就是相对位姿）。
- 深度、像素匹配 → 也都能从这两张 pointmap 里读出来。

> 🎓 **一张 pointmap（每像素 3D 坐标）+ 两张图共享坐标系 = 把「相机位姿 / 深度 / 匹配」全都隐式编码进去了。** 这就是 DUSt3R 标题 *"Geometric 3D Vision Made Easy"* 的底气：你不再需要先求相机参数，3D 一步到位，相机参数是事后从 pointmap 里「读」出来的。

### DUSt3R 的网络长什么样（够用就行，不背细节）

> 📖 DUSt3R §3.1、Fig. 2：

```
I¹ ─┐                                            ┌─► 回归头 ─► X¹·¹, C¹·¹
    ├─ 共享权重 ViT 编码器 (Siamese) ─► F¹, F² ─┤  两个 decoder 不断 cross-attention 交换信息
I² ─┘                                            └─► 回归头 ─► X²·¹, C²·¹
```

- **编码器**：两张图用**同一个**（权重共享）ViT 编码，得到 token $F^1, F^2$。
- **解码器**：两条分支，每个 decoder block 顺序做 **self-attention（看自己这张）→ cross-attention（看另一张）→ MLP**，两条分支**全程互相交换信息**——这是能输出「对齐的 pointmap」的关键。
- **预训练**：架构源自 **CroCo**（Cross-view Completion，同组的自监督预训练），所以能白嫖 CroCo 的预训练权重。
- **训练 loss**：就是简单的回归 loss（Eq. 4），用置信度加权。

> 你做 SLAM 看到这个 cross-attention 结构应该有亲切感——它在干的事，本质就是「让两张图的特征互相看见，从而把它们摆进同一个 3D 坐标系」。

---

## 二、DUSt3R 的死穴：只能两张图 + 要 global alignment

### 死穴所在

注意上面整套，输入永远是**两张**图。真实场景你有几十上百张图，怎么办？DUSt3R 的答案是：

1. **两两跑**：把图配成很多对，每对各自前馈出一组 pointmap。
2. **global alignment（全局对齐）**：再跑一道**优化**，把所有「成对的、各自坐标系的」pointmap 拼到一个**统一的世界坐标系**里。

> 📖 项目页原话：*"In the case where more than two images are provided, we further propose a simple yet effective global alignment strategy that expresses all pairwise pointmaps in a common reference frame."*

### ⚠️ 注意一个常见误解（你会用得上）

global alignment **不是** bundle adjustment：

- BA 最小化的是 **2D 重投影误差**（在像素平面上）。
- DUSt3R 的 global alignment 直接在 **3D 空间**里最小化 pointmap 的不一致，调整相机位姿和场景几何，并先建一个「成对连通图」按置信度挑可靠的对。

但**对我们这门课，关键不是它和 BA 的区别，而是它和 BA 的共同点**：

> 🎯 **它仍然是一道「前馈之后还得跑的迭代优化」。** 这正是第 00 课说的「痛点 C」：DUSt3R 把主干前馈化了，却没能摆脱「成对处理 → 后优化拼接」这条尾巴。图一多，这条尾巴又慢又是误差来源。

记住这句话，第 04 课 VGGT 的突破点就是冲着这条尾巴来的。

### 还有一个小尾巴：up-to-scale（尺度不确定）

DUSt3R 的 pointmap 是**相差一个全局尺度**的（up-to-scale），即重建出来的形状对，但「真实有多大」不知道。这对需要真实尺度的下游任务（定位、机器人导航）不够用——MASt3R 会补这块。

---

## 三、MASt3R：给 DUSt3R 补两块（matching head + metric + 快速匹配）

MASt3R 的定位很清楚：**不推翻 DUSt3R，而是在它上面打补丁**，把「匹配精度」和「真实尺度」做上去。它甚至直接用 DUSt3R 的权重做初始化。

> 📖 MASt3R 摘要：DUSt3R 基于 pointmap 回归，对极端视角变化**鲁棒**，但**精度有限**。MASt3R 目标是「在保留鲁棒性的前提下提升匹配能力」。

### 补丁 1：加一个 matching head，输出稠密局部特征

> 💡 DUSt3R 只有「回归 pointmap」的头；MASt3R **再加一个头**，输出两张稠密局部特征图 $D^1, D^2 \in \mathbb{R}^{H\times W\times d}$（$d=24$）。

- 训练这个头用的不是回归 loss，而是 **InfoNCE（对比学习）loss**（温度 $\tau=0.07$）：把「真同名点」的特征拉近、「非同名点」推远。
- 总 loss = 回归 loss + $\beta \cdot$ 匹配 loss（$\beta=1$）。

> 🎯 为什么要这个头？因为直接拿 pointmap 反推匹配，精度只能到「粗」的级别。专门学一套局部描述子 + 对比 loss，能把对应关系做到**亚像素级**。这同时让 MASt3R **原生输出 metric（带真实尺度）pointmap**，补掉了 DUSt3R 的 up-to-scale 尾巴。

### 补丁 2：Fast Reciprocal Matching（FRM）—— 解决稠密匹配的平方复杂度

有了稠密特征图，怎么从里面捞出可靠对应？标准做法是找**互相最近邻（mutual nearest neighbor，互为最近邻才算一对）**：

$$
\mathcal{M} = \{(i,j)\ |\ j = \text{NN}_2(D^1_i)\ \text{and}\ i = \text{NN}_1(D^2_j)\}
$$

> 📖 MASt3R §3.3、Eq. (11)。

问题：暴力算这个是 $O(W^2 H^2)$——每个像素要和另一张图所有像素比，稠密图上慢到不可用。

MASt3R 的 **FRM** 用一个很漂亮的迭代采样绕开它：

```
1. 在 I¹ 上规则撒 k 个种子像素（k ≪ W·H）
2. 每个种子映射到 I² 的最近邻 → 再映射回 I¹ 的最近邻
3. 如果绕一圈回到起点（形成 cycle）→ 这就是一个 reciprocal match，收下并移除
4. 没回到起点的「活跃」种子继续迭代，几轮后活跃数迅速归零
```

> 📖 MASt3R §3.3 + 附录 0.F 给了收敛性证明：沿 NN 路径走，相似度单调上升，必然收敛到一个 cycle（reciprocal match）。learnopencv 实测约 **64× 加速**，工程上用 Faiss 存对应。

> 🎯 直觉：不用把整张图所有像素都两两比，只从稀疏种子出发「顺着最近邻往上爬」，爬到的 cycle 就是可靠对应。还有个副作用——FRM 采样偏向「大收敛盆地」，匹配点在图上分布更均匀，反而让 RANSAC 估位姿更稳。

### MASt3R 的成绩（核实数字）

> 📖 ECCV 2024 poster 报告：在极具挑战的 **Map-free localization** 基准上，VCRE Precision **相对提升 230%**，超越当时最好方法。（项目页另给「VCRE AUC 绝对提升 30%」的口径，两者来源不同、指标不同，知道「大幅领先」即可。）

---

## 四、把支线 B 串成一条线（本课收束）

```
CroCo (自监督预训练)
   │  提供 ViT encoder-decoder + 预训练权重
   ▼
DUSt3R (CVPR'24)：两张图 → 两张同坐标系 pointmap
   │  神之一手：pointmap + 共享第一台相机坐标系 → 不要相机参数也能出 3D
   │  死穴：只能两张；多张要 global alignment 后优化；up-to-scale
   ▼
MASt3R (ECCV'24)：DUSt3R + matching head (InfoNCE) + metric + FRM
   │  补精度（亚像素匹配）+ 补尺度（metric）+ 补速度（FRM 绕开 O(W²H²)）
   │  死穴仍在：本质还是「成对处理」，多图依旧要拼
   ▼
（第 04 课）VGGT：一次吃几百张，前馈出全部 3D 属性，彻底不要拼
```

> 🎓 **支线 B 的灵魂是「前馈回归 pointmap，把相机参数从『前置条件』降级成『事后读数』」。DUSt3R 立了这个范式，MASt3R 把精度/尺度/速度补齐——但两者都没跳出「一次两张 + 后续要拼」的框。VGGT 接过这个灵魂，直接把『一次几百张、无需拼』做出来，于是后优化这条尾巴被彻底剪掉。**

---

## 五、一句话总结今天

> 🎓 **DUSt3R 用「pointmap + 同坐标系」证明了不要相机参数也能前馈出 3D，但只能两张图、要 global alignment 拼多张；MASt3R 给它加 matching head（精度）、metric（尺度）、FRM（速度），却仍跳不出成对处理的框。这条尾巴，就是 VGGT 要剪的。**

---

## ✅ 课后检查

### Q1（必答 · 主观题）
DUSt3R 把第 2 张图的 pointmap 也表达在「第 1 台相机的坐标系」里。用你自己的话说：这一招为什么能让「相机位姿 / 深度 / 匹配」都不用再单独算、而是从 pointmap 里直接读出来？

### Q2（必答 · 判断题，说明理由）
- (a)「DUSt3R 的 global alignment 就是 bundle adjustment，都最小化 2D 重投影误差」
- (b)「MASt3R 相比 DUSt3R 的主要新增是一个输出稠密局部特征的 matching head，用 InfoNCE 训练」
- (c)「FRM 之所以快，是因为它不做任何最近邻搜索」

### Q3（选答 · 挑战题 · 结合你的本职）
你做重定位 / 长序列 SLAM。DUSt3R/MASt3R 这种「成对前馈 + global alignment」的范式，如果直接拿来处理你的几百帧长序列，你预计会在哪两个地方最先出问题？（提示：对的数量随帧数怎么涨？误差在拼接时怎么传播？）

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
> - (a)
> - (b)
> - (c)
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -

## 📒 我的笔记（你来填：DUSt3R 一句话 + MASt3R 补了哪三块）

> - DUSt3R:
> - MASt3R 补的三块：

---

**下一课预告**：
**第 04 课 — VGGT 总览：一次前馈出全部 3D 属性，扔掉所有后优化**
两条支线（A 可微 SfM / B pointmap 回归）都讲完了。第 04 课进入正题：VGGT 怎么把支线 B 的「前馈出 3D」从「两张 + 拼」升级成「一次几百张、不要拼」，以及它凭什么在 CVPR 2025 拿 Best Paper。
