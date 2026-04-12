# 传感器选型 — 决策记录

> 记录割草机激光 SLAM 传感器选型的关键决策。
> 格式：每条决策独立一节。
> 状态：`【已定案】` / `【讨论中】` / `【已推翻】`

---

## SD-001 淘汰速腾 Airy：测距原理缺陷无法修复【已定案】

**背景**
第一轮评估时，速腾 Airy 是主要候选器件之一。内场联调后发现点云质量存在严重问题。

**问题现象**
- 拖影：25m 测距条件下，拖影长度约 1.3m，树叶/小间隙均会出现
- 鬼影：玻璃面出现镜面对称的虚像（lens 镜面鬼影）
- SLAM 建图：墙皮厚重、重影显著、Z 轴漂移

**厂商确认**

![速腾厂商回复（测距原理无法优化）](images/sensor_stt_vendor_reply.png)

![速腾厂商回复 v2（第二份对比文档）](images/sensor_stt_vendor_reply_v2.png)

速腾回复：光斑在多帧叠加测距波动，属器件测距原理所致，暂时无法优化。

**25m 测距误差实测**

![25m处误差约1.3m](images/sensor_stt_error_25m.jpeg)

![误差比对图](images/sensor_stt_error_comparison.png)

**调参尝试结论**
安装角度调整为 -5°（引入地面点）后，高度漂移有所缓解，但建图质量根本问题未解决。

**决策**
淘汰速腾 Airy，问题来自硬件原理，软件侧无法规避。

**来源** | 速腾airy和mid360；速腾airy和mid360+禾赛对比分析

---

## SD-002 选定 Mid360：外场验证通过，满足大场景需求【已定案】

**背景**
在速腾 Airy 确认淘汰后，Mid360 成为主要候选，并完成内外场全面验证。

**验证数据**

点云质量（Mid360 树轮廓清晰，几乎无拖影）：

![Mid360 树轮廓清晰点云](images/sensor_mid360_tree_pointcloud.png)

外场 SLAM 性能（测距 70m+，SLAM 正常运行）：

![Mid360 SLAM 测距达70m+](images/sensor_mid360_slam_70m.png)

场地规模验证（78号、105号场地建图稳定）：

![78号场地建图](images/sensor_mid360_field78.jpeg)

![105号场地建图](images/sensor_mid360_field105.jpeg)

**核心指标满足情况**
- 测距：70m+（目标场景 3000m²+ ≈ ~55m 半径，满足）
- 点云质量：树木等复杂轮廓还原度高，无明显拖影
- SLAM 建图：稳定，105场地颠簸数据（斜坡）表现正常
- 负角度支持：有（支持地面点采集）

**决策**
选定 Mid360 为割草机激光 SLAM 主传感器。

**来源** | 速腾airy和mid360；割草机slam激光雷达需求

---

## SD-003 淘汰禾赛 JT16：树冠处点云质量有风险【已定案】

**背景**
在 Mid360 初步确定后，补充评估了禾赛 JT16 作为候选（使用 105 号场地）。

**宏观建图**

![禾赛JT16 105场地建图总览](images/sensor_hesai_jt16_map_overview.jpeg)

宏观轮廓与 Mid360 类似，未发现明显异常。

**微观点云质量问题**

（1）树冠处"发射状"点云：

![树冠处发射状点云](images/sensor_hesai_jt16_tree_scatter.jpeg)

（2）"发射状"误差约 80cm（rviz 测量）：

![误差约80cm](images/sensor_hesai_jt16_error_80cm.jpeg)

（3）激光打到墙上留下的放射线：

![墙面放射线](images/sensor_hesai_jt16_wall_scatter.jpeg)

**Mid360 vs 禾赛 JT16 结论对比（建筑物/树干处）**

![Mid360 vs 禾赛JT16 点云质量对比](images/sensor_mid360_vs_hesai_quality.jpeg)

Mid360 建筑表面点云更均匀，树干和细杆轮廓更清晰。

**决策**
淘汰禾赛 JT16。树冠处点云发散（80cm 误差）与速腾 Airy 类似，引入 SLAM 后存在相同风险。

**未记录的待确认项**
禾赛淘汰是否还有成本/供应链方面的考量？【待确认，见 mslam/gaps.md Q-5】

**来源** | 速腾airy和mid360+禾赛对比分析

---

## 图片归档记录

| 文件名 | 来源 | 引用位置 |
|--------|------|---------|
| `sensor_stt_vendor_reply.png` | 001_速腾airy和mid360/images/SrBxb5... | SD-001 |
| `sensor_stt_error_25m.jpeg` | 001_速腾airy和mid360/images/YBKwb... | SD-001 |
| `sensor_stt_error_comparison.png` | 001_速腾airy和mid360/images/RcCRb... | SD-001 |
| `sensor_mid360_tree_pointcloud.png` | 001_速腾airy和mid360/images/O8V7b... | SD-002 |
| `sensor_mid360_slam_70m.png` | 001_速腾airy和mid360/images/EFVSb... | SD-002 |
| `sensor_mid360_field78.jpeg` | 001_速腾airy和mid360/images/JenHb... | SD-002 |
| `sensor_mid360_field105.jpeg` | 001_速腾airy和mid360/images/Mu2xb... | SD-002 |
| `sensor_stt_vendor_reply_v2.png` | 002_速腾airy+禾赛/images/LaWib... | SD-001（第二份对比文档版本）|
| `sensor_hesai_jt16_map_overview.jpeg` | 002_速腾airy+禾赛/images/RRDzb... | SD-003 |
| `sensor_hesai_jt16_tree_scatter.jpeg` | 002_速腾airy+禾赛/images/PKd7b... | SD-003 |
| `sensor_hesai_jt16_error_80cm.jpeg` | 002_速腾airy+禾赛/images/BFq8b... | SD-003 |
| `sensor_hesai_jt16_wall_scatter.jpeg` | 002_速腾airy+禾赛/images/VHKob... | SD-003 |
| `sensor_mid360_vs_hesai_quality.jpeg` | 002_速腾airy+禾赛/images/UfPOb... | SD-003 |
