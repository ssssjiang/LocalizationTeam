# 📘 补充 03：VGGT 可以用来做什么——应用场景与已验证用例

> 真实来源（全部 confirmed）：
> - **VGGT** [arXiv 2503.11651] §1 Abstract、§4.6、§5
> - **VGGT-Ω** [arXiv 2605.15195] §1 Abstract、§4.4、Related Work §2

---

## 1. 速查结论

VGGT 提供两类可复用能力：

| 能力 | 直接输出 | 已验证延伸应用 |
|---|---|---|
| **3D 几何推断** | 相机参数、深度图、点图、2D tracks | 3DGS 初始化、MVS、SfM 替换 |
| **几何感知特征** | 图像 token 特征、VGGT-Ω 的 scene registers | 点跟踪增强、新视角合成、VLA 机器人、语言对齐 |

---

## 2. 直接 3D 几何输出的应用

### 2.1 多视角相机姿态估计

适用条件：**有 2–数百张同一场景的照片**，不知道相机内外参。

输出：每张图的 FOV（内参）+ 外参（旋转+平移），精度在 CO3Dv2 AUC@30 = 88.2（纯前馈），加 BA 后 91.8；IMC 旅游地标场景 AUC@10° = 84.91（加 BA）。

对比：这套精度已超过 COLMAP (SIFT) 的 44.79，且速度快 **50×+**（0.2s vs >10s）[VGGT §4.1 Table 1/10]。

### 2.2 稠密深度估计 / 点云重建

适用条件：多张重叠图（无需已知相机）。

输出：每帧的稠密深度图 + 稠密点云，且不依赖 GT 相机。在 DTU 基准（不给 GT 相机）Overall Chamfer = **0.382**，追上了大部分需要已知相机的方法 [VGGT §4.2 Table 2]。

实际用途：
- **3D Gaussian Splatting 初始化**：VGGT 输出的相机+点图可作为 3DGS 的位姿初始化和稀疏点初始化，替代 COLMAP SfM 阶段。原文明确提到 pointmap 与 3DGS 的「无缝集成（seamless integration）」[VGGT §E]。
- **MVS 前置**：VGGT 先估相机 + 粗点云，再接 PatchmatchNet 等传统 MVS 细化。

### 2.3 多视角 2D 点跟踪（结构性跟踪）

适用条件：**一组静态场景图片**（不要求时序），给定 query 图上某些像素位置。

输出：这些 query 点在所有其他图里对应的 2D 坐标（rigid tracking）。

VGGT 在 ScanNet-1500 双视角匹配上 AUC@20 = 73.4，超过专用双视图匹配方法 RoMa（70.9），**即使 tracking head 不是为双视图专门训练的** [VGGT §4.4 Table 4]。

### 2.4 单张图 3D 重建

VGGT 的架构天然支持单张图输入（全局 attention 退化为帧内 attention）。没有专门训练单视图任务，但已经表现出「令人惊讶的好效果」（原文措辞 [VGGT §5 Single-view Reconstruction]）。

---

## 3. 以特征骨干（feature backbone）为基础的延伸任务

VGGT 的强项不只是最终输出，还包括**其学到的中间 token 特征**。以下延伸任务均在论文里有量化验证。

### 3.1 动态场景点跟踪（TAP-Vid 基准）

做法：把 CoTracker 的 image encoder backbone 换成 VGGT 预训练骨干，再在 Kubric 数据集上 fine-tune 整个 tracker [VGGT §4.6 Table 8]。

结果：

| 数据集 | CoTracker AJ | CoTracker + VGGT backbone AJ |
|---|---|---|
| Kinetics | 49.6 | **57.2** |
| RGB-S | 67.4 | **72.1** |
| DAVIS | 61.8 | **64.7** |

VGGT 的特征把 CoTracker 在 RGB-S 上的 δvis_avg 从 78.9 提升到 84.0（**+5.1**）。这说明 VGGT 在静态图集上学到的几何特征能迁移到动态视频跟踪任务。

### 3.2 无相机先验的新视角合成（Novel View Synthesis）

做法：在 VGGT 骨干上加 DPT head，用 Plücker rays 编码 target 视角，微调模型直接输出 target 图像 RGB；**输入图不需要提供相机参数** [VGGT §4.6 Table 7]。

结果（GSO 数据集）：

| 方法 | 是否需要输入相机 | PSNR ↑ | SSIM ↑ |
|---|---|---|---|
| LVSM（专为 NVS 训练，全量数据） | ✅ 需要 | 31.71 | 0.957 |
| VGGT-NVS（20% 训练数据） | ❌ **不需要** | 30.41 | 0.949 |

用 20% 训练数据、无相机输入，VGGT 微调版接近用全量数据训练的 LVSM。

### 3.3 机器人具身控制（VLA 任务）——VGGT-Ω 的场景 token

做法（VGGT-Ω §4.4）：从 VGGT-Ω 提取 scene registers（场景 token），直接拼到 OpenVLA-OFT 的输入 token 里，VGGT-Ω **冻结不训练**，只微调 VLA 模型本身 [VGGT-Ω §4.4 Table 3]。

结果（LIBERO 基准，成功率 ↑）：

| 方法 | Spatial | Object | Goal | Long | 平均 |
|---|---|---|---|---|---|
| OpenVLA-OFT | 97.6% | 98.4% | 97.9% | 94.5% | 97.1% |
| OpenVLA-OFT + VGGT-Ω 场景 token | **99.3%** | **99.2%** | **99.0%** | **96.7%** | **98.5%** |

4 个子任务全部提升，Long（长程任务）从 94.5% 提到 96.7%。这验证了 scene register 无监督地捕获了对机器人任务有用的空间信息。

### 3.4 语言对齐（VGGT-Ω）

做法：将 VGGT-Ω 的 scene register 用 CLIP 风格的对比对齐微调，与自然语言描述对齐 [VGGT-Ω §4.4]。

意义：说明从重建任务里学到的 scene token 已经包含足够丰富的语义/空间信息，支持语言对齐，**不需要显式语言监督**就能构成几何感知的语言接口。

---

## 4. 适用与不适用的边界

### 4.1 目前适用的条件（confirmed）

- 相机数：2 帧到约 200 帧（VGGT）/ 1250 帧（VGGT-Ω，单 A100 限制）
- 相机类型：**普通透视相机**（perspective）
- 场景类型：室内、室外、合成场景
- 动态内容：**VGGT-Ω 支持含运动的视频**（刚体+部分非刚体）；原始 VGGT 仅轻微非刚性

### 4.2 目前不适用或精度存疑的条件（confirmed，[VGGT §5]）

- **鱼眼 / 全景摄像头**：当前不支持
- **极端旋转（大基线）**：精度明显下降
- **城市级大规模场景（数千~百万图）**：训练时每场景最多 24 帧，大规模下缺乏系统评估
- **强烈非刚性形变**（例如布料抖动、人体极速动作）：VGGT 会失败

---

### References

- [1] Wang et al., VGGT, CVPR 2025 Best Paper. arXiv:2503.11651
- [2] Wang et al., VGGT-Ω, CVPR 2026 Oral. arXiv:2605.15195
