# 📘 第 02 课：支线 A — VGGSfM（端到端可微 SfM）

> 真实来源：**VGGSfM** [arXiv 2312.04563](https://arxiv.org/abs/2312.04563)（Wang, Karaev, Rupprecht, Novotny, CVPR 2024 Highlight）/ 项目页 [vggsfm.github.io](https://vggsfm.github.io/) / [github](https://github.com/facebookresearch/vggsfm)。架构引用 §3.2–3.4 与 Fig. 1/2；数字引用 Tab. 1/2/3/6 与附录。
> 学习目标：理解 VGGSfM 怎么把第 00 课的「五步流水线」逐步替换成**可微模块**，关键抓住三件事——① 用 point tracking 替掉「检测+匹配」；② 用一个 Transformer **同时**恢复所有相机（不再一张张 register）；③ 它**仍然保留了 bundle adjustment**，只是做成了可微的。学完你要能说清：VGGSfM 解决了第 00 课三宗罪里的哪两宗、留了哪一宗给 VGGT。

---

## 开场：VGGSfM 的一句话定位

第 00 课画的地图里，VGGSfM 是「支线 A」：

> 💡 **VGGSfM = 把传统 SfM 那条五步流水线，每一步都换成可微的神经网络模块，于是整条流水线能用一个 loss 端到端训练；同时它不再「一张张加图」，而是一次性把所有相机恢复出来。但流水线的最后一棒——bundle adjustment——它保留了，只是做成可微的。**

对照第 00 课三宗罪：

| 第 00 课三宗罪 | VGGSfM 怎么处理 |
|---|---|
| A. 不可微，没法端到端训练 | ✅ **解决**：四个模块全可微，一个 loss 训到底 |
| B. 增量式（一张张加）→ 慢且脆 | ✅ **解决**：所有相机**同时**恢复，非增量 |
| C. 后优化（BA）又慢又是必需品 | ❌ **没解决**：BA 还在 loop 里（只是变可微了）|

> 🎯 把这张表记住。VGGSfM 干掉了前两宗罪，第三宗（BA）留给了 VGGT。这就是为什么我们叫它「过渡形态」。

---

## 一、VGGSfM 的四个可微模块（对着五步看）

VGGSfM 整条 pipeline 是一个函数 $f_\theta$，由四个模块串成。我把它和第 00 课的五步对齐：

```
传统五步：  ①检测 ②匹配      ③注册        ④三角化      ⑤BA
              │    │            │            │            │
VGGSfM：   ┌──┴────┴──┐    ┌────┴───┐    ┌───┴────┐   ┌───┴────┐
           │ 深度2D    │    │ 可学习  │    │ 可学习  │   │ 可微    │
           │ point     │──► │ 相机     │──►│ 三角化  │──►│ bundle  │
           │ tracking  │    │ 初始化器 │    │ 器      │   │ adjust. │
           └───────────┘    └─────────┘    └────────┘   └─────────┘
              §3.2            §3.3           §3.3         §3.4
```

下面逐个讲，每个都点明「替了五步的哪步、为什么这么设计」。

---

## 二、模块 1：深度 2D point tracking（替掉「检测 + 匹配」）

第 01 课讲过 point tracking 的直觉，这里看 VGGSfM 怎么用它。

### 它做什么

> 💡 先在一张**query 帧**上选一批查询点（用 SuperPoint / SIFT 选，因为「有辨识度的点」跟得更准），然后 tracker 把这些点**在所有输入帧里一起跟踪**，输出每个点的 2D 轨迹 + 一个置信度。

三个关键设计（都对 SfM 很重要）：

1. **不假设时间连续**（§3.2）：它不像视频跟踪那样用 sliding window，而是**一次 attend 所有帧**。因为 SfM 的输入是无序图片集，不是连续视频。
2. **带置信度（aleatoric uncertainty）**：每个 track 点除了位置 $y_i^j$，还预测一个方差 $\sigma_i^j$，置信度 $\propto 1/\sigma$。SfM 里**滤掉 outlier 对应**至关重要，这个置信度后面用来筛点。
3. **coarse-to-fine（粗到细）**：先在全图特征上粗跟，再在粗估位置周围裁 $P\times P$ patch 精跟，做到**亚像素**精度。消融里去掉 fine tracker，IMC 的 AUC@10 从 73.92% 掉到 62.30%（§4.3）——SfM 对精度极敏感。

### 🎯 为什么这一步是「替掉检测+匹配」的关键

传统②匹配靠「两两配对 + 链式传递」，不可微、还累积误差。VGGSfM 的 tracker：

- **直接给一个点跨所有帧的完整轨迹**，绕开链式传递；
- **全程可微** → 训练 loss 的梯度能一路回传到 tracker，让它和后面的相机/三角化模块「协同进化」。

> 📖 消融（Tab. 4）：把 VGGSfM 的 tracks 和顶尖匹配器 SP+SG（SuperPoint+SuperGlue）对比喂给 COLMAP 系，tracks 还略好一点（70.62 vs 70.47）；而把 SP+SG 的匹配喂给 VGGSfM 反而掉点——因为 SP+SG 不参与联合训练，丢了「协同」这个好处。

---

## 三、模块 2：可学习相机初始化器（替掉「注册」，且不再增量）

这是 VGGSfM **最反传统**的一步，也是它干掉「增量式」这宗罪的地方。

### 传统怎么做 vs VGGSfM 怎么做

- 传统③：**一张张** register——先两张图初始化，再逐个把新图加进来求位姿（incremental）。这是第 00 课说的「慢且脆 + 漂移」的根源。
- VGGSfM：用一个 Transformer $\mathfrak{T}_\mathcal{P}$，**一次性、同时**预测所有相机的位姿。

> 📖 §3.3 原话：*"we register all cameras and reconstruct all scene points collectively in a non-incremental differentiable fashion."*

### 它怎么预测（够用版）

$\mathfrak{T}_\mathcal{P}$ 吃三样东西，输出所有相机参数：

1. 每张图的全局特征 $\phi(I_i)$（用 ResNet50 提，注意这里**没用 DINO**——论文说 DINO 和其他模块联合训练时更难收敛，§附录）；
2. 上一步 tracker 给的 **track 描述子**（携带「图间对应」信息，是位姿估计的 grounding）；
3. 一个用 **8-point 算法**从 track 算出的**初步相机**（相当于给网络一个粗初值）。

> 这里有个工程小聪明：8-point 通常配 RANSAC 滤噪。VGGSfM 用「批量 8-point」——并行跑 20 组各 50 个点对，按 Sampson 极线误差数 inlier，选 inlier 最多的那组，避免了 RANSAC 的 for 循环（§附录）。

### 相机怎么参数化（记一下，VGGT 会对比）

每个相机 **8 自由度**：旋转四元数 $q(R)\in\mathbb{R}^4$ + 平移 $t\in\mathbb{R}^3$ + **焦距的对数** $\ln(\mathfrak{f})\in\mathbb{R}$。主点固定在图像中心。

> 🎯 **这一步把「注册」从 incremental 改成 collective（一次全出）**。它和经典的「global SfM」神似（都一次性出所有相机、只 BA 一次），但有两点不同：global SfM 还是靠 pairwise matching + 旋转/平移平均，而 VGGSfM 用 tracks + 一个学出来的网络（§附录 B）。

---

## 四、模块 3：可学习三角化器（替掉「三角化」）

有了所有相机 + 2D tracks，要出 3D 点云。

> 💡 VGGSfM 先用经典闭式 **DLT（Direct Linear Transform）多视图三角化**算一个**初步点云** $\bar{X}$，再用一个 Transformer $\mathfrak{T}_X$ 在这个初步点云上「精修」，输出初始点云 $\hat{X}$。

为什么不直接用 DLT 就完？因为 DLT 是纯几何闭式解，对噪声敏感；外面套一个可学习 Transformer，能利用 track 特征把它修得更准、也保持可微。

> 📖 消融（Tab. 5）：把这个三角化器换成纯 DLT，IMC AUC@10 从 73.92% 掉到 69.42%。

---

## 五、模块 4：可微 bundle adjustment（保留了第五步，但变可微）

到这里 VGGSfM 有了：tracks $\mathcal{T}$、初始相机 $\hat{\mathcal{P}}$、初始点云 $\hat{X}$。最后一棒——**bundle adjustment**——它**保留**了。

### BA 在干什么（一句话）

> 💡 BA = 联合微调所有相机和所有 3D 点，使「3D 点投影回各相机」和「实际 track 点」之间的**重投影误差**最小：

$$
X,\mathcal{P} = \arg\min_{X,\mathcal{P}} \sum_{i}\sum_{j} v_i^j \,\bigl\|P_i(x^j) - y_i^j\bigr\|
$$

> 📖 §3.4 Eq. (6)。$P_i(x^j)$ 是 3D 点 $x^j$ 投到相机 $P_i$ 的像素位置，$y_i^j$ 是 track 实际观测，$v_i^j$ 是可见性权重。低置信度 / 低可见性 / 重投影误差过大的点会被滤掉。

这个你做 SLAM 太熟了——就是经典的 BA。

### VGGSfM 的关键改动：让 BA 可微

传统 BA 用 Levenberg-Marquardt（LM）二阶优化器解，**这是个嵌套优化循环，默认不可微**，梯度没法穿过它回传。VGGSfM 怎么办？

> 📖 §3.4：用 **Theseus 库**，靠**隐函数定理（implicit function theorem）**，让梯度能穿过「带嵌套优化循环的 BA」回传到前面所有模块。

> 🎯 **这是「支线 A 仍保留优化」的精确含义**：VGGSfM 没有删掉 BA，而是把这道经典优化做成可微的一环，缝进端到端训练里。第 00 课三宗罪的第三宗（后优化），它没解决，只是「驯化」了。

### BA 到底有多重要？看这个消融

> 📖 Tab. 6（IMC AUC@10）：
> - 完整 VGGSfM：**73.92%**
> - 去掉 BA（w/o BA）：**18.34%** ⚠️
> - 不滤 outlier（w/o Filtering）：**2.31%**

> 🎯 去掉 BA 直接崩到 18%。**说明对 VGGSfM 而言，前馈模块只是给了好初值，真正把精度顶上去的还是那道 BA。** 这恰恰反衬出 VGGT 的激进——它敢把这根「定海神针」整个拿掉，还能更准（第 04 课）。

---

## 六、整体串一遍 + 为什么要端到端

四个模块（tracking → 相机初始化 → 三角化 → BA）全可微，于是能用一个 loss $\mathcal{L}$ 端到端训练。

### 端到端训练有多重要？

> 📖 Tab. 1/2 消融（Ours w/o Joint vs Ours）：
> - Co3D AUC@30：70.7% → **74.0%**
> - IMC AUC@10：68.35% → **73.92%**

> 🎯 单独训各模块也能用，但**让它们联合训练、互相适配**，才到 SOTA。这就是「fully differentiable」的回报——模块之间产生协同。

### 成绩与定位（核实数字）

> 📖 §4：
> - **Co3D**（宽 baseline，物体环拍，传统 COLMAP 很吃力）：VGGSfM 大幅领先（各指标 +9 个点左右）。
> - **IMC Phototourism**（视角重叠好，COLMAP 的主场）：VGGSfM 在 AUC@10 / AUC@5 上超过所有方法，AUC@3 第二——说明**宽窄 baseline 都能打**。
> - **ETH3D**（三角化精度）：accuracy 和 completeness 都超过此前最好。
> - CVPR24 IMC Challenge 相机位姿（Rot&Trans）拿了**第 1**（github README）。

---

## 七、VGGSfM 的死穴：处理不了成千上万张图

这是理解「为什么会有 VGGT」的最后一块拼图。

> 📖 §5 结论原话：*"it currently lacks the capability to process thousands of images as in traditional SfM frameworks."*

为什么？因为它的相机初始化器、三角化、BA 都是「把所有帧一起塞进去算」。帧数一多，计算和显存吃不消。传统 COLMAP 靠 incremental 反而能慢慢啃完上千张图——VGGSfM 用「一次全出」换来了简单和可微，代价是**规模上不去**。

> 🎯 **VGGSfM 留下两个尾巴交给后面：① BA 还在 loop 里（慢、是必需）；② 处理不了大规模图集。** VGGT 用「纯前馈、一次吃几百张、不要 BA」一并冲这两个尾巴；VGGT-Ω 再用 scaling 把「图更多、显存更省」推到极致。

---

## 八、一句话总结今天

> 🎓 **VGGSfM 把传统 SfM 五步全做成可微模块（point tracking → 同时恢复所有相机 → 可学习三角化 → 可微 BA），干掉了「不可微」和「增量式」两宗罪；但它保留了 bundle adjustment 当定海神针（去掉就崩到 18%），也还处理不了上千张图。这两个尾巴，是 VGGT 的出发点。**

---

## ✅ 课后检查

### Q1（必答 · 主观题）
VGGSfM 号称「非增量（non-incremental）」。用你自己的话说：它的「相机初始化器」相比传统「一张张 register」，到底改变了什么？这对第 00 课说的「漂移 / 脆弱」有什么好处？

### Q2（必答 · 判断题，说明理由）
- (a)「VGGSfM 已经把 bundle adjustment 彻底删掉了，全靠前馈出结果」
- (b)「VGGSfM 的 point tracker 用 sliding window 假设输入是连续视频」
- (c)「消融实验里，去掉 BA 后 VGGSfM 的精度只是小幅下降」

### Q3（选答 · 挑战题 · 结合你的本职）
论文说去掉 BA 后 AUC@10 从 73.92% 崩到 18.34%。这说明 VGGSfM 的前馈模块本质上扮演的是什么角色（提示：相对 BA 而言）？如果让你预测——一个想「完全不要 BA」的方法（VGGT），它必须在哪件事上做得比 VGGSfM 的前馈模块强得多，才可能不崩？

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

## 📒 我的笔记（你来填：四个模块各替了五步的哪步 + VGGSfM 留下的两个尾巴）

> - 四模块 ↔ 五步:
> - 两个尾巴:

---

**下一课预告**：
**第 04 课 — VGGT 总览：一次前馈出全部 3D 属性，扔掉所有后优化**
（注：支线 A=VGGSfM 第 02 课、支线 B=DUSt3R/MASt3R 第 03 课已就位，按编号读 02 → 03 → 04。）
第 04 课进入正题：VGGT 怎么同时甩掉 VGGSfM 的两个尾巴——既能一次吃几百张图，又敢把 BA 整个拿掉，还在 CVPR 2025 拿下 Best Paper。
