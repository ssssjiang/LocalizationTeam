# trajectory-align-2d-demo

VSLAM 与 RTK 轨迹 3DoF（x, y, yaw）对齐的最小可跑 demo，用于评估通道口（≤ 7 m）短段对齐效果与误差来源。

## 1. 用法

```bash
python align_2d.py \
    --rtk  rtk.tum \
    --slam vslam_pgo.tum \
    --segments 1 2 5 7 \
    --out  align_2d.png
```

输入是 TUM 格式：`t x y z qx qy qz qw`（whitespace-separated）。z / quaternion 列可缺省（仅缺时 yaw 置 0，不影响对齐本身）。

## 2. 算法

- **时间对齐**：RTK 为参考；VSLAM 的 xy 线性插值到 RTK 时间戳；yaw 先 `unwrap` 再插值，避免 ±π 跳变；RTK 时间窗外的样本丢弃，不外推。
- **3DoF 闭式对齐**（scale = 1）：
  - `a_i = src_i - mean(src)`, `b_i = dst_i - mean(dst)`
  - `theta = atan2( Σ(a_x b_y - a_y b_x),  Σ(a_x b_x + a_y b_y) )`
  - `t = mean(dst) - R(theta) · mean(src)`
- **直线可观性**：2D 下 SO(2) 只有 1 个自由度，cross / dot 两项随段长线性放大，直线段仍可解出唯一 theta；只有 src 退化成单点（zero baseline）才奇异。
- **分段**：按累计弧长切前 L 米，避免机器人停顿干扰。

## 3. 输出

- 每个 L 一张子图：黑实线 RTK，红虚线 aligned VSLAM，绿色加粗段表示用于对齐的弧长段。
- 最后一张子图：不同 L 下 pointwise 误差 vs 弧长。
- stdout 表格：`L | N | RMSE_xy | drift | theta`。

## 4. 5 个分析点的预期表现

| 现象 | 看哪里 |
|---|---|
| RTK 波动 | align 段内 RMSE 不为 0；全段误差曲线在 align 段内有抖动地板 |
| VSLAM 角度误差 | align 段外误差近似线性增长（横向漂移 ≈ 距离 × Δθ） |
| 对齐长度影响 | 表中 L vs theta 的稳定性；理论上 theta 噪声 ~ 1/L |
