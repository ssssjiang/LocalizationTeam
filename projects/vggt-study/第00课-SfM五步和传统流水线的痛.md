# 📘 第 00 课：这条线到底在解决什么问题？

> 真实来源：传统 SfM 流程的标准描述（COLMAP, Schönberger & Frahm, CVPR 2016）；以及 **VGGSfM 论文** [arXiv 2312.04563](https://arxiv.org/abs/2312.04563) 引言段、**VGGT 论文** [arXiv 2503.11651](https://arxiv.org/abs/2503.11651) 引言段对传统流水线痛点的描述。
> 学习目标：搞清楚 SfM 到底在算什么、传统流水线哪五步、每一步「痛」在哪。把这五步刻在脑子里，后面三棒（VGGSfM / VGGT / VGGT-Ω）都是在**改这五步里的某几步**。

---

## 一、先用大白话说清 SfM 在干嘛

你（做 SLAM 的）对这个其实最熟，但我们先把语言对齐，因为后面三篇论文都拿它当靶子。

一句话：

> 💡 **SfM（Structure from Motion）= 给我一堆从不同角度拍同一个场景的照片，我反推出「每张照片是从哪儿、朝哪个方向拍的」（相机位姿）+「场景长什么样」（3D 结构）。**

输入输出摆出来：

| | 内容 | 术语 |
|---|---|---|
| 输入 | 一堆无序的 2D 照片 $\{I_1, I_2, \dots, I_N\}$ | unconstrained images |
| 输出 1 | 每张照片的相机内参 + 外参 | camera parameters（intrinsics + extrinsics / pose） |
| 输出 2 | 场景的 3D 点 | 3D structure（sparse point cloud） |

> 你在重定位 / 建图里天天接触的就是它的产物：相机轨迹 + 地图点。

---

## 二、传统怎么做？记住这「五步流水线」

这是整个课程的**地基**。VGGSfM 论文引言里把传统 SfM 概括成一条**增量式（incremental）**流水线，正好五步：

```
① 检测关键点      detect keypoints      （SIFT / ORB …）
② 匹配关键点      match keypoints       （跨图找同名点）
③ 注册相机        register images       （一张一张地把新图加进来求位姿）
④ 三角化 3D 点    triangulate points    （同名点 + 两个位姿 → 3D 坐标）
⑤ 光束平差        bundle adjustment(BA) （联合优化所有位姿 + 3D 点，最小化重投影误差）
```

> 📖 这五步就是 COLMAP 那套（Schönberger & Frahm, CVPR 2016）的标准增量式 SfM；VGGSfM 论文引言原话是：*"Classical frameworks solve this problem in an incremental manner by detecting and matching keypoints, registering images, triangulating 3D points, and conducting bundle adjustment."*

### 一个非常关键的词：**incremental（增量式）**

注意第 ③ 步——**一张一张地**把图加进来。先用两张图初始化，求出一个小重建，然后每次挑一张新图，求它的位姿，三角化新点，再 BA 一次……如此循环，直到所有图都加完。

> 🎯 **「一张一张加、每加一张就要重新优化一次」——这个 incremental 的特性，是后面所有痛点的根源。记住它。**

---

## 三、这五步「痛」在哪？（三篇论文都在攻这里）

我把痛点分三类，对应后面三棒各自要解决的东西。

### 痛点 A：每一步都不可微，没法端到端训练

⑤ 步里每一步都是「人手设计的算法模块」：SIFT 是手工特征，RANSAC 是采样几何验证，BA 是非线性最小二乘。它们**拼在一起不可微**。

后果：

- 你没法像训神经网络那样，用一个 loss 把整条流水线端到端优化。
- 深度学习这些年只能**替换其中某一个零件**（比如用 SuperPoint 换 SIFT、用 SuperGlue 换匹配），但流水线整体骨架还是那条非可微的老路。

> ⚠️ 这正是 **VGGSfM（第 02 课）** 要攻的：能不能让**每一步都可微**，从头到尾用一个 loss 训出来？

---

### 痛点 B：增量式 = 慢 + 容易崩 + 误差累积

「一张一张加」带来三个具体麻烦：

1. **慢**：N 张图要循环 N 次，每次都可能要重跑 BA。几百张图能跑几分钟到几十分钟。
2. **脆**：匹配（②步）一旦在某些图上失败（弱纹理、重复纹理、视角差太大），这张图就注册不进来，或者注册错了把整个重建带歪。
3. **漂移**：误差沿着「加图顺序」一步步累积，长序列尾部容易漂。

> 你做长序列 SLAM 对②脆、③漂这两点应该深有体会。

> ⚠️ 这是 **VGGT（第 03–04 课）** 要攻的：能不能**所有图一起看、一次 forward 出结果**，根本不做 incremental 循环？

---

### 痛点 C：BA 后优化又慢又是「必需品」

即便有了 DUSt3R 这种前馈方法（第 01 课会讲），它们当时还是要在后面接一道**昂贵的迭代后优化**（global alignment / BA）才能拿到能用的结果。

> 📖 VGGT 论文引言原话点名：*"This is a substantial departure from DUSt3R, MASt3R, or VGGSfM, which still require costly iterative post-optimization to obtain usable results."*
> （翻译：这跟 DUSt3R、MASt3R、VGGSfM 都很不一样——那些方法仍然需要昂贵的迭代后优化才能拿到可用结果。）

> ⚠️ 这是 **VGGT** 最炸的点、也是它拿 Best Paper 的核心：**连后优化都扔掉，前馈直接出结果，还更准。**

---

## 四、把三棒和五步对上号（本课程的「地图」）

现在你已经有了五步流水线这把尺子，我把这条线上的所有方法都排好，让你心里有张地图。注意——通往 VGGT 其实有**两条平行支线**，最后并到 VGGT 里：

| 方法 | 对五步做了什么 | 后优化(BA / global alignment)还在吗？ |
| --- | --- | --- |
| **传统 SfM**（COLMAP） | 五步全是手工模块，不可微，增量式 | 在，且是核心 |
| **VGGSfM**（CVPR'24）〔支线 A：可微 SfM〕 | 五步**全换成可微模块**，所有相机**同时**恢复（不再 incremental） | **还在**，但变成可微的 BA layer |
| **DUSt3R / MASt3R**（CVPR'24 / ECCV'24）〔支线 B：pointmap 回归〕 | 干脆**跳过 SfM 骨架**，前馈直接回归 pointmap；但一次只吃**两张图** | **还在**：靠 global alignment 后优化把成对结果拼成多视图一致 |
| **VGGT**（CVPR'25） | 一个 Transformer 一次吃**几百张**，前馈出位姿/深度/点图/track | **不需要**（前馈结果直接可用；可选再叠 BA 能**小幅**提精度） |
| **VGGT-Ω**（CVPR'26） | 在 VGGT 基础上做 **scaling**（省显存、上大数据、扩到动态场景） | **不需要**（与 VGGT 的差异在 scaling，不在 BA） |

> 🎓 看出主线了吗？**「优化（后处理）在流水线里的地位一路下降」**：
> 传统里是核心 → VGGSfM 里降成可微的一环 → DUSt3R/MASt3R 把主干前馈化但仍要 global alignment 拼多视图 → **VGGT 把后优化彻底删掉**（一次吃几百张，不需要拼）→ VGGT-Ω 把这套前馈范式 scale 到极致。
>
> 两条支线（A 可微 SfM / B pointmap 回归）最后都被 VGGT 收编：VGGT 借了支线 B「前馈出 3D」的灵魂，又干掉了它「只能成对 + 要后优化」的死穴。**所以 DUSt3R/MASt3R 是 VGGT 更直接的「亲爹」，第 03 课专门讲。**

---

## 五、一句话总结今天

> 🎓 **传统 SfM 是「检测→匹配→注册→三角化→BA」的增量式流水线；它的三宗罪是「不可微 / 增量慢且脆 / 后优化贵」。接下来三棒，就是分别把这三宗罪一个个干掉的故事。**

---

## ✅ 课后检查（请你回答，我看你答的程度再决定第 01 课讲多细）

### Q1（必答 · 主观题）
用你自己的话说一遍：传统增量式 SfM 的「增量（incremental）」具体指什么？它带来的最致命的一个问题是什么？（结合你做长序列 SLAM 的经验答更好）

### Q2（必答 · 判断题，说明理由）
下面三句话，哪句对哪句错？
- (a)「深度学习已经让传统 SfM 流水线端到端可微了」
- (b)「VGGSfM 不再一张一张加图，而是所有相机一起恢复」
- (c)「VGGT 仍然需要在最后跑一遍 bundle adjustment 才能用」

### Q3（选答 · 挑战题）
你觉得「所有图一起看、一次 forward 出结果」（VGGT 的路子）相比「一张一张加」（传统），在**工程上最大的代价**是什么？
（提示：想想显存、想想图的数量 N 变大时 attention 的复杂度——这正好是第 05 课 VGGT-Ω 要解决的）

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

## 📒 我的笔记（你来填，用自己的话重述五步 + 三宗罪）

> 

---

**下一课预告**：
**第 01 课 — 背景棋盘：理解三棒站在谁肩上**
我们会快速过三块积木：① point tracking（CoTracker，VGGSfM 用它替代「匹配」那步）；② pointmap regression（DUSt3R 范式，VGGT 的前馈思路从这来）；③ DINOv2 backbone（VGGT 的眼睛）。把这三块认全，第 02 课开始就能直接进 VGGSfM 本体了。
