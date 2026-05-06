# 设计稿（暂存）：用图像 + pose 的极线可视化 验证 fast-livo 外参

**状态**：设计阶段，已就 §1/§2 达成一致；用户暂时搁置实施，待后续 resume。

## 背景

- 数据：`/mnt/data/roborock/chunk_005/`
- 800 张 PNG (640×544) + COLMAP 风格 `cameras.txt` / `images.txt`
- 内参（PINHOLE）：`fx=310.528036 fy=310.429690 cx=321.090706 cy=276.142555`
- `images.txt` 已是「世界 → 相机」的位姿（`qw qx qy qz tx ty tz`）
- 由 fast-livo 优化出的 sensor pose，经 `projects/3dgs-data-prep/slam_to_colmap.py` 中 `T_cam_lidar` 套外参转换写入；怀疑该外参偏，导致图像与 pose 不齐

## 目标

不用别的 ground truth，只用现有 (image_i, pose_i) 之间的几何关系，**目视判断**外参是否准。
最终产物：一组 PNG（每对图像一张），可拍照贴飞书/Slack。

## 已确定的边界（用户已确认）

- pose 的语义：相机系（已含 `T_cam_lidar`）
- 输出形态：可视化为主（不出数值表格）
- 图像对选择：自动，覆盖均衡 + baseline 足够，K=8–12 对

## 选定方案：极线叠加（方案 1）+ 可选附加 stereo-rectify（方案 2）

**核心思路**：
- 由 pose 自身（不要从图像反算 F）算 `R_ji, t_ji → E → F = K^-T E K^-1`
- 在两图之间做朴素特征匹配（SIFT + ratio test），**不再 RANSAC 过滤**，否则会先把不符 pose 的匹配剔掉
- 在右图画对应的极线，按到匹配点的对称距离染色（绿/黄/红）

弃用方案 2 作为主方法的原因：机器人前向运动时 baseline 很小，stereo rectify 会几何退化。

## §1 架构 & 数据流

```
chunk_005/
  cameras.txt   → K
  images.txt    → per image (R_w2c, t_w2c)
  images/<name>.png

[load_data] → 图像列表 + K + 每张图 (R, t)
     ↓
[pair_picker] 选 K=10 对（顺序对、baseline 过滤、轨迹均匀）
     ↓
[feature_match] 每对：SIFT + kNN + ratio(0.8)
     ↓
[epipolar_compute] 由 pose 得 E、F；每个匹配点算到极线的对称距离
     ↓
[render_pair] 左右拼图：左图匹配点；右图极线（按误差染色）+ 匹配点
     ↓
[summary] 每对 PNG / 总览 PNG / 文本指标 TSV
```

## §2 Pair selection 算法

输入：N 张图的 (R, t)，目标 8–12 对。

```
1. 计算每帧 baseline 距离到第 0 帧
2. 候选生成：stride ∈ {5, 10, 20}, 滑窗
3. 过滤：‖t‖ ∈ [0.10, 2.0] m，相对旋转 ≥ 1°（避免静止/无重叠）
4. 沿时间均匀采样 K=10 对
5. 若不够，自动放宽 baseline 下限到 0.05 m
```

## 待定（resume 时继续）

- §3：可视化细节参数（颜色阈值、字体、布局）
- §4：CLI 与输出目录结构
- §5：错误处理（特征过少、退化几何、图像缺失）
- §6：写实施计划（writing-plans skill）

## 实现约束

- 单文件 Python，依赖 `numpy / OpenCV / Pillow`，**不依赖 COLMAP 二进制**，避免环境波动
- 输入接口：`--input <dataset_root>`（含 `cameras.txt`/`images.txt`/`images/`），输出 `<root>/pose_check/`

## 关联讨论上下文（来源会话节选）

- 用户提及怀疑 fast-livo 优化出的 pose 与图像之间存在外参偏差
- 已确认 `images.txt` 已是相机系
- 已选 b（可视化为主）+ d（自动选 8–12 对均衡 baseline）
