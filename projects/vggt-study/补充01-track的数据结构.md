# 📘 补充 01：track 到底用什么数据结构表达？——CoTracker / VGGSfM / VGGT 三家对比

> 真实来源（全部 confirmed，逐条标到 section）：
> - **CoTracker** [arXiv 2307.07635](https://arxiv.org/abs/2307.07635)（§3 Problem definition / Architecture）
> - **VGGSfM** [arXiv 2312.04563](https://arxiv.org/abs/2312.04563)（§3.1 Notation / §3.2 Tracking）
> - **VGGT** [arXiv 2503.11651](https://arxiv.org/abs/2503.11651)（§3.1 / §3.3 Tracking）
> 学习目标：彻底搞清「模型直接输出的 track」是什么数据结构，区分**最终 track**（坐标）和**内部中间表示**（feature / token grid），并把三家放在一张表里对比。

---

## 开场：一句话结论

> 🎯 **这三家模型输出的 track，最终都是同一种东西：一组「2D 图像坐标」，按 (点编号, 帧编号) 双重索引，外加一个「可见性」标志（VGGSfM 还多一个「置信度」）。track 活在图像平面（像素 (u,v)），不是 3D。3D 永远是 track 之后才算的。**

但「模型内部用什么 token / feature 来算 track」三家差别很大——这才是这节要讲细的地方。下面分三层：①统一的逻辑结构 → ②三家各自的具体表达（含内部中间结构）→ ③对比表 + 易混点澄清。

---

## 一、统一的逻辑结构：track = (点 × 帧) → 2D 坐标 + 标志位

抛开实现，三家 track 的"逻辑数据结构"完全一致，可以统一写成：

| 成员 | 含义 | 类型 |
|---|---|---|
| **query（查询）** | 「要追哪个点」：某一帧上的一个 2D 位置（CoTracker 还带"从第几帧开始"） | `(帧索引, 2D 位置)` |
| **位置 position** | 该点在**每一帧**里的 2D 像素坐标 $\mathbf{y}=(u,v)$ | 张量 `[N_点, N_帧, 2]` |
| **可见性 visibility** | 该点在某帧里是否可见（被遮挡/出画 = 0） | 张量 `[N_点, N_帧]`，取值 $\{0,1\}$ |
| **置信度 confidence**（可选） | 对该 (点,帧) 位置预测的把握 | 张量 `[N_点, N_帧]`（VGGSfM 有，见 §3.2） |

> 💡 记住这个骨架：**track ≈ 一个 `[点数 × 帧数 × 2]` 的坐标张量 + 一个 `[点数 × 帧数]` 的可见性张量**。三家都逃不出这个形状，区别只在「怎么指定 query」「内部怎么算」「是否联合预测」。

---

## 二、三家各自的表达（最终结构 + 内部中间结构）

### 2.1 CoTracker：视频里的「时间 × 轨迹」token 网格

CoTracker 面向**视频**（有时序），它的形式化定义最清楚（§3）：

- 视频 $V=(I_t)_{t=1}^T$，要预测 $N$ 条轨迹：
$$
P^i_t = (x^i_t, y^i_t) \in \mathbb{R}^2,\quad t = t^i,\dots,T,\quad i=1,\dots,N
$$
其中 $t^i$ 是第 $i$ 条轨迹的**起始帧**（CoTracker 允许每个点从不同帧开始追）。
- 外加可见性 $v^i_t \in \{0,1\}$。
- **输入** = 视频 + 每条轨迹的起始位置和起始时间 $(P^i_{t^i}, t^i)$；**输出** = 所有 $t \ge t^i$ 的位置估计 $\hat{P}^i_t$ 和可见性 $\hat{v}^i_t$。

**内部中间结构（关键）**：CoTracker 把 track 编码成一个**二维 token 网格** $G^i_t$（§3.1）——

> 📖 §3.1 原文：tracks are encoded as a grid of input tokens $G^i_t$，**一个维度是时间 $t$，一个维度是被追的点 $i$**。

每个 token $G^i_t$ 由四部分拼成（§3.1）：
- 位置（当前估计 $\hat{P}^i_t$ 的正弦位置编码 $\eta$）
- 可见性
- **外观特征** $Q^i_t \in \mathbb{R}^d$（随时间变化，初始化为在起始点采样的图像特征）
- **相关特征** $C^i_t$（RAFT 式 4D cost volume，维度 196）

然后 transformer 在这个网格上做 self-attention，**迭代 $M$ 次**逐步修正：$\hat{P}^{(m+1)} = \hat{P}^{(m)} + \Delta\hat{P}$；可见性在最后一次更新后用 sigmoid 算一次。

> 🎯 CoTracker 的两个标志性设计：
> - **联合（joint）跟踪**：token 网格里轨迹维度互相做 attention，利用"点之间的相关性"（同一物体上的点一起动）。
> - **virtual tracks**：用少量"代表性虚拟轨迹 token"，把虚拟轨迹之间的 self-attention + 虚拟↔真实的 cross-attention 结合，从而单卡能同时追 70k 点。（这个"用少量代表 token 中转"的思路，和第 06 课 VGGT-Ω 的 register attention 是同一种省算力哲学。）

### 2.2 VGGSfM：无序图集、独立轨迹、cost-volume token + 不确定度

VGGSfM 面向 **SfM 的无序图集**（不能假设时序），定义（§3.1）：

- 一条 track 是：
$$
T^j = \bigl((\mathbf{y}^j_1, v^j_1),\dots,(\mathbf{y}^j_{N_I}, v^j_{N_I})\bigr)
$$
即第 $j$ 个点在全部 $N_I$ 帧里的 2D 位置 $\mathbf{y}^j_i \in \mathbb{R}^2$ + 二值可见性 $v^j_i \in \{0,1\}$。

**内部中间结构**（§3.2）：给定某帧 $I_i$ 上 $N_T$ 个查询点 → 双线性采样出 query 描述子 → 每个描述子和**所有 $N_I$ 帧**的多分辨率特征图做相关 → 构成 **cost-volume 金字塔** → 展平成 token：
$$
V \in \mathbb{R}^{N_T \times N_I \times C}
$$
（即「查询点 × 帧 × cost-volume 维度」的 token），喂给 transformer 得到 tracks。

VGGSfM 和 CoTracker 的三点关键差异（§3.2，都 confirmed）：
1. **不假设时序**：无滑窗，所有帧一起 attend（适配 SfM 的自由图集）。
2. **独立预测每条轨迹**（不像 CoTracker 联合）——这样测试时能追更多点、点云更密。
3. **多一个置信度**：用 aleatoric uncertainty 给每个 2D 点预测一个方差 $\sigma^j_i$，置信度 $\propto 1/\sigma^j_i$（对角协方差 → 水平/垂直两个不确定度）。这个置信度对 SfM 至关重要——**用来过滤 outlier 对应点**，免得脏 track 污染后面的三角化和 BA。
4. **coarse-to-fine**：先粗追，再在粗位置周围裁 $P\times P$ patch 重追，拿到亚像素精度。

> 🎯 VGGSfM 的 track（坐标+可见性+置信度）是后续三级（相机初始化 → DLT 三角化 → BA）的**唯一几何输入**。所以它对 track 的要求是"少而准 + 带不确定度"，和 CoTracker"多而密"的取向不同。

### 2.3 VGGT：主干不吐坐标，先吐「稠密特征图」，再由 head 算坐标

VGGT 是三家里最特别的——**主干根本不直接输出 track 坐标**（§3.1）：

- track 的定义还是一样：$T^\star(y_q) = (y_i)_{i=1}^N,\ y_i \in \mathbb{R}^2$。
- 但 transformer $f$ 输出的是每帧一张**稠密跟踪特征图** $T_i \in \mathbb{R}^{C \times H \times W}$（每个像素一个 $C$ 维特征），**不是坐标**。
- 真正算坐标的是一个**独立的 tracking head**（CoTracker2 架构），实现函数：
$$
\mathcal{T}\bigl((y_j)_{j=1}^M, (T_i)_{i=1}^N\bigr) = \bigl((\hat{y}_{j,i})_{i=1}^N\bigr)_{j=1}^M
$$

head 内部流程（§3.3）：在查询帧特征图上**双线性采样**查询点特征 → 和其它所有帧特征图做**相关** → correlation maps → self-attention → 回归出每帧 2D 点。可见性按 CoTracker2 用 BCE 监督。同样**不假设时序**。

> 💡 为什么 VGGT 要这么绕？因为它是个**多任务大模型**：主干只产出"通用稠密特征"$T_i$，深度/点图/track 都从这套特征派生。track 坐标交给轻量 head 算，主干特征还能复用给别的下游任务（第 04 课讲的"VGGT 当 backbone"）。这就是"主干出 feature、head 出坐标"的分工。

---

## 三、对比表 + 易混点澄清

### 3.1 三家 track 表达对比（全部 confirmed）

| 维度 | CoTracker | VGGSfM | VGGT |
|---|---|---|---|
| 面向输入 | 视频（有时序） | 无序图集 | 一到几百张图（不假设时序） |
| 最终 track 坐标 | $\hat{P}^i_t \in \mathbb{R}^2$，`[N点, T帧, 2]` | $\mathbf{y}^j_i \in \mathbb{R}^2$，`[N_T点, N_I帧, 2]` | $\hat{y}_{j,i} \in \mathbb{R}^2$，`[M点, N帧, 2]` |
| 可见性 | $v^i_t \in \{0,1\}$ | $v^j_i \in \{0,1\}$ | BCE 可见性 |
| 置信度 | 无（单独） | **有**（aleatoric $\sigma$，1/σ） | 主要靠深度/点图的不确定度 |
| query 怎么指定 | (起始帧 $t^i$, 起始位置) | (某帧, $N_T$ 个 2D 点) | (查询帧, $M$ 个 2D 点) |
| 是否联合预测 | **联合**（轨迹间 attention） | **独立**（每条单独） | head 内逐查询点相关 |
| 内部中间结构 | **时间×轨迹 的 token 网格** $G^i_t$ | **点×帧 的 cost-volume token** $V\in\mathbb{R}^{N_T\times N_I\times C}$ | **稠密特征图** $T_i\in\mathbb{R}^{C\times H\times W}$（主干）+ head 内相关 |
| 时序假设 | 有（滑窗） | 无 | 无 |

> 🎯 读这张表的"题眼"：**最终 track 三家几乎一样（点×帧×2 + 可见性）；真正分家的是「内部中间结构」**——CoTracker/VGGSfM 都先把 track 显式 token 化成「(点×帧) 网格」，VGGT 偏偏不 token 化 track，而是留稠密特征图、把算坐标外包给 head。

### 3.2 易混点澄清：track / point map / depth 是三种不同的东西

很多人把这几个混在一起，必须分清（都 confirmed）：

| 量 | 维度 | 在哪个空间 | 一句话 |
|---|---|---|---|
| **track（2D）** | 每 (点,帧) 一个 $(u,v)$ | **图像平面** | 同一物理点在不同图里投影到哪个像素 |
| **depth（深度）** | 每像素一个标量 $d$ | 沿相机光轴 | 该像素离相机多远 |
| **point map（点图）** | 每像素一个 $(x,y,z)$ | **3D 世界系**（VGGT/DUSt3R 用第一台相机系） | 该像素对应的 3D 点坐标 |

- **track 是 2D 对应关系**，不含深度、不含 3D。
- 在 VGGSfM 里，3D 点是 track **经过三角化**算出来的（track → DLT → 点云 → BA）。
- 在 VGGT 里，track 和 point map 是**两条并行的输出分支**，都从主干特征派生，互不经过对方。

### 3.3 内部 vs 最终：track 在 pipeline 里的"两副面孔"

最后强调这个最容易绕晕的点：

```
[查询] (帧, 2D点)
   │
   ▼
[内部中间结构]  ← CoTracker: 时间×轨迹 token 网格 / VGGSfM: 点×帧 cost-volume token / VGGT: 稠密特征图
   │  (transformer + 相关/迭代)
   ▼
[最终 track]  每个 (点,帧) → 2D 坐标 (u,v) + 可见性 (+置信度)
```

> 🎓 **一句话收尾**：问"模型用什么数据结构表达 track"，要分两层答——
> **最终 track 三家统一**：`[点 × 帧 × 2]` 的 2D 坐标张量 + `[点 × 帧]` 的可见性（VGGSfM 再加置信度）；
> **内部表达三家不同**：CoTracker 和 VGGSfM 把 track 显式做成「(点 × 帧) 的 token 网格」（前者沿时间联合、后者按帧独立 + cost-volume），VGGT 则不给 track 单独 token，而是主干出稠密特征图、再用一个 CoTracker2 式的 head 做相关回归出坐标。

---

## ✅ 课后检查

### Q1（必答）
有人说「track 就是 3D 点云的轨迹」。这句话错在哪？用「图像平面 / 3D」和「track / point map」把它纠正过来。

### Q2（必答）
CoTracker 的内部 token 网格是「时间 × 轨迹」，VGGSfM 是「点 × 帧 × cost-volume」。这两者本质上都是把 track 做成「(点 × 帧) 网格」。那 VGGT 为什么偏偏不这么做、而是输出稠密特征图 $T_i \in \mathbb{R}^{C\times H\times W}$？（提示：VGGT 是单任务 tracker 还是多任务大模型？）

### Q3（选答 · 串联题）
VGGSfM 的 track 多了一个「置信度 $1/\sigma$」，CoTracker 没单独强调。结合各自的下游用途（VGGSfM 的 track 要喂三角化+BA / CoTracker 就是终点产物），说说为什么 VGGSfM 特别需要置信度。

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -
