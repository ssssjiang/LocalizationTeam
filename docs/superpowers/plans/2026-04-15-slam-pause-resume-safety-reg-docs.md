# 专题文档生成 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从 5 份原始 inbox 文档生成 2 份结构化专题文档，输出到 `overview/modules/common/`，供同团队接手工程师系统阅读。

**Architecture:** 文档一（SLAM 暂停恢复与重定位机制）整合 4 份激光 SLAM 相关原始文档，按执行流程驱动组织；文档二（整机安规策略功能说明）整合 1 份安规需求文档，按全局汇总表 + 逐类展开组织。两文档在 Lift / 导航触发 / 出边界节点交叉引用。

**Tech Stack:** Markdown，图片复制（shell cp），引用验证（grep）

**Spec:** `docs/superpowers/specs/2026-04-15-slam-pause-resume-safety-reg-design.md`

---

## 文件清单


| 操作        | 路径                                                              |
| --------- | --------------------------------------------------------------- |
| 创建        | `overview/modules/common/slam-pause-resume-reloc-2026-04-14.md` |
| 创建        | `overview/modules/common/safety-regulation-2026-04-14.md`       |
| 复制（重命名）×7 | `overview/modules/common/images/common_safety_*.png`            |
| 修改        | `docs/process/raw-materials-conventions.md`（追加记录）               |


**原始材料路径（只读）：**

- `teams/laser/inbox/0412新增/暂停恢复-定位优化_2026-04-12-23-48-10/暂停恢复-定位优化.md`
- `teams/laser/inbox/0412新增/局部重定位减少对导航静止依赖优化.md`
- `teams/laser/inbox/0412新增/断流情况和逻辑调整1.21讨论.md`
- `teams/laser/inbox/0412新增/重定位条件与流程梳理_2026-04-13-00-02-51/重定位条件与流程梳理.md`
- `inbox/0414新增/智能割草机安规策略功能_2026-04-15-00-27-10/智能割草机安规策略功能.md`

**已有图片（直接引用，无需复制）：**

- `teams/laser/modules/mslam/images/mslam_reloc_condition_flow.png`
- `teams/laser/modules/mslam/images/mslam_cancel_reloc_flow.png`

> 注：文档一中的图片路径需用相对路径指向 mslam/images/，或在 common/images/ 中用符号链接/拷贝。建议直接拷贝到 common/images/ 以保持目录自包含。

---

## Task 1：复制安规图片并验证

**Files:**

- Create: `overview/modules/common/images/common_safety_stop_trigger.png`（及另外 6 张）
- **Step 1：执行图片复制**

```bash
SRC=inbox/0414新增/智能割草机安规策略功能_2026-04-15-00-27-10/images
DST=overview/modules/common/images

cp "$SRC/whiteboard_1_1776184033494.png"  "$DST/common_safety_stop_trigger.png"
cp "$SRC/whiteboard_2_1776184036540.png"  "$DST/common_safety_lift_trigger.png"
cp "$SRC/whiteboard_3_1776184040247.png"  "$DST/common_safety_bumper_trigger.png"
cp "$SRC/whiteboard_4_1776184045227.png"  "$DST/common_safety_tilt_trigger.png"
cp "$SRC/whiteboard_5_1776184050231.png"  "$DST/common_safety_flip_trigger.png"
cp "$SRC/whiteboard_6_1776184055228.png"  "$DST/common_safety_boundary_trigger.png"
cp "$SRC/NES0bgA5soIMCxxyWvgcLnIrnNd.png" "$DST/common_safety_boundary_map_def.png"
```

- **Step 2：复制 mslam 已有图片到 common/images/**

```bash
MSRC=teams/laser/modules/mslam/images
cp "$MSRC/mslam_reloc_condition_flow.png" overview/modules/common/images/
cp "$MSRC/mslam_cancel_reloc_flow.png"    overview/modules/common/images/
```

- **Step 3：验证所有 9 张图片存在**

```bash
ls overview/modules/common/images/common_safety_*.png overview/modules/common/images/mslam_reloc_condition_flow.png overview/modules/common/images/mslam_cancel_reloc_flow.png
```

预期：列出 9 个文件，exit code 0。

---

## Task 2：写文档一 — SLAM 暂停恢复与重定位机制

**Files:**

- Create: `overview/modules/common/slam-pause-resume-reloc-2026-04-14.md`
- **Step 1：写文档正文**

完整内容如下（使用 Write 工具直接写入文件）：

```markdown
# SLAM 暂停恢复与重定位机制

> **本文覆盖范围**：激光 SLAM 定位模块在暂停、恢复、雷达断流、搬动、Lift 等中断场景下的处理策略，包含导航侧触发条件、SLAM 侧响应策略、断流专项逻辑及优化路线图。
>
> **关联文档**：整机安规触发条件详见 [整机安规策略功能说明](safety-regulation-2026-04-14.md)，尤其是 §3（抬起检测机制）。

## 快速索引

| 我遇到的问题 | 去哪节 |
|------------|-------|
| 暂停恢复后定位跑飞 | §3（导航判断）+ §4.2（局部重定位） |
| 雷达断流后几帧点云异常 | §5（断流 predict 逻辑） |
| 搬动机器后重定位失败 | §3 + §4.2 长期方案 |
| Lift 触发了不必要的重定位 | §2.4 + [安规 §3](safety-regulation-2026-04-14.md#3-抬起) |
| 想了解局部重定位不依赖静止的设计 | §4.2 |

---

## 1. 正常定位运行（背景）

机器正常割草时，SLAM 持续接收雷达点云并维持定位状态。与导航的核心接口：

- **`relocate_flag`**：定位模块主动上报，通知导航当前匹配质量差，需要发起重定位。
- **`set_pose`（局部重定位入口）**：导航判断触发条件后调用，传入初始位姿；SLAM 在此基础上做局部匹配修正。`check_pose` 返回 true/false 告知是否成功。
- **全局重定位**：`check_pose` 失败或局部重定位失败后，由导航发起。

---

## 2. 中断分类与触发参数

### 2.1 雷达断流

| 断流时长 | 当前处理 | 状态 |
|---------|---------|------|
| < 500ms | 轮速递推兜底，不暂停，不发起重定位 | ✅ 已实现 |
| > 500ms | 机器暂停（pause）；恢复后导航发起局部重定位 | ✅ 已实现 |
| 断流期间未完全停止 | 不发起局部重定位，靠轮速递推；待停止后仍发起 | ✅ 已实现 |
| 断流期间完全停止 | 导航发起局部重定位 | ✅ 已实现 |

> **后续优化**：轮速兜不住时（依赖匹配度评估），SLAM 主动发起局部重定位；若不行，再发起全局重定位。（⚠️ 方案阶段，参见 §4.3）

### 2.2 用户主动暂停（pause/resume）

| 场景 | 当前处理 | 状态 |
|-----|---------|------|
| 无搬动、无移动 | 轮速递推 | ✅ 已实现 |
| 小位移推动（versa < 60cm, < 1rad；RTK 同） | 导航发起局部重定位；`check_pose` 失败则全局重定位 | ✅ 已实现 |
| 搬动 | 导航发起全局重定位 | ✅ 已实现 |
| 搬动（后续自识别） | SLAM 自识别搬动状态，主动发起 | 🔴 暂缓（搬动中雷达观测需良好） |

> ❓ **位移阈值**：早期为 (40cm, 0.1rad)，当前已调整。versa 机型：暂停/雷达关时位移 > 0.4m 或角位移 > 0.1rad；RTK 机型：暂停时位移 > 0.4m 或角位移 > 1rad。最终联调值待确认。

### 2.3 建图模式

建图模式下，**重定位仅在 prepare 阶段可触发**，遥控开始后无法再触发。

常见风险：
- 建图故障暂停后，雷达一段时间后关闭；故障恢复后定位未恢复，且无报错信息 → 建图异常风险。
- 用户在故障时主动推动机器，定位异常但无报错 → 建图结果可能损坏。

### 2.4 Lift 触发

> **跨文档参考**：Lift 的硬件检测机制（两驱/四驱差异、防抖参数）见 [整机安规策略功能说明 §3](safety-regulation-2026-04-14.md#3-抬起)。

常见误触发场景（由安规文档归纳）：
- 一侧前轮压树枝 → 另一侧被检测到抬起
- 前轮底下有坑 → 该侧触发
- 机器在斜坡上 → 上侧后轮可能触发

**导航侧建议**：使用**双轮同时抬起**作为重定位触发条件，单轮抬起误触发多。

| 机型 | 抬起检测 | 防抖 |
|-----|---------|-----|
| 两驱 | 前轮受力；单轮落空触发 | 300ms |
| 四驱（Monet/Versa） | 后轮减震受力；单侧落空触发 | >20°: 3000ms；10-20°: 1500ms；<10°: 300ms |

### 2.5 重启

机器重启后，定位状态丢失，无条件进入全局重定位流程。

---

## 3. 导航侧判断逻辑

### 3.1 通用触发条件（所有任务）

以下 5 个条件，任意满足即进入重定位状态：

1. **Lift 连续超过 2s**
2. **移动重定位**（见 §2.2 参数表）
3. **重启**
4. **`relocate_flag`**：定位模块主动上报
5. **versa 局部重定位失败**（频率增多因断流兜底逻辑，断流 > 500ms 时暂停后触发局部重定位，存在一定失败概率）

> versa 机型比 RTK 机型更容易触发移动重定位：versa 在遥控割草模式下雷达会停，雷达停了就记位移；RTK 机器遥控时不记位移。

### 3.2 各任务特殊规则

| 任务 | 特殊规则 |
|-----|---------|
| 割草 | 含 `退庄异常结束`（定位未收敛），开始任务后需进重定位 |
| 回充 | 与割草基本一致，无 `退庄异常` 条件 |
| 建图 | 仅 prepare 阶段可触发，遥控开始后不再响应重定位条件 |

### 3.3 重定位状态机流程

![重定位状态机流程图](images/mslam_reloc_condition_flow.png)

### 3.4 导航实现方案（优化方向 1/2）

![导航实现方案流程图](images/mslam_cancel_reloc_flow.png)

> **⚠️ 优化方向（待实现）**：
> - 抬起监控改为单轮抬起 + 姿态变化联合判断（减少建图失败及不必要重定位）
> - 四驱机器加入坡道检测结果
> - 重定位安全检测加入障碍物点云高度判断（防跌落）

---

## 4. SLAM 侧响应策略

### 4.1 轮速递推兜底

适用场景：
- 雷达断流 < 500ms
- 建图 pause/resume（不发起重定位）
- 断流期间未完全停止

限制：
- 轮速不可靠时（打滑等）无特殊处理。（⚠️ 待改进）
- 建图模式下暂停减速问题，由李鹏飞长期跟进。

### 4.2 局部重定位（set_pose）三阶段方案

当导航调用 `set_pose` 触发局部重定位时，SLAM 侧的处理演进如下：

#### ✅ 短期方案（已实现）

`set_pose` 前后加轮速补偿，将静止等待期间的少量运动补偿到 `set_pose` 结果上。

处理框架简单，不改变主流程。

#### ⚠️ 中期方案（方案设计中 — 周士伟负责）

**目标**：消除 `set_pose` 阻塞主线程的延迟。

流程：
1. `set_pose` 触发后，**开启独立线程**执行局部重定位计算
2. 同时，**主线程**继续用当前 pose 进行 SLAM 递推，正常计算和发布（不刷新地图）
3. 局部重定位完成后：
   - **成功** → 修正初始 pose；刷新地图
   - **失败** → 返回 false；导航发起全局重定位

#### 🔴 长期方案（暂缓 — 安全风险未解决）

**目标**：`set_pose` 立即返回 true，让导航不等待直接开始行走。

流程：
1. `set_pose` **立即返回 true**，导航开始行走
2. 独立线程继续计算局部重定位；主线程 SLAM 递推（不刷新地图）
3. 局部重定位完成后：
   - 成功 → 修正 pose；刷新地图
   - 失败 → **主动发起全局重定位**

> ⚠️ **风险**：导航已经开始行走，但 pose 尚未修正，存在定位跑偏期间的安全隐患。当前暂缓，待安全机制补充后再推进。

### 4.3 主动重定位触发 ✅（已实现）

暂停恢复后，若连续多帧匹配率 + 得分均低于阈值，定位模块主动向导航发送重定位请求（`relocate_flag`），导航发起全局重定位流程。

> ❓ 具体阈值参数待联调确认。

---

## 5. 断流专项：predict 两阶段拆分

核心思想：将预测拆为两个独立阶段，在 sync 中做逻辑判断，移除之前的补丁逻辑。

### 5.1 初版方案

| 阶段 | 时间段 | IMU 状态 | 处理方式 |
|-----|-------|---------|---------|
| predict-to-start | `last_lidar_end` → `cur_lidar_start` | 可用 | IMU 积分推算 |
| predict-to-start | `last_lidar_end` → `cur_lidar_start` | 断流 or 上帧 lidar 断流 > 250ms | ODO 递推 |
| predict-to-end | lidar 帧内（start → end） | 连续（无断流 > 25ms） | IMU predict + 去畸变 |
| predict-to-end | lidar 帧内（start → end） | IMU 断流 | ODO predict + 去畸变 |

### 5.2 改进版（sync 重写）

前置条件：上次处理时，`last_end` 之前的 IMU 数据已清空。

改进内容：
1. 增加检测逻辑1：抓取 `last_end` → `cur_lidar_start` 之间的 IMU，判断是否走流程1（predict-to-start）
2. 执行流程1
3. 增加前置逻辑：抓取 `cur_lidar_start` → `cur_lidar_end` 之间的 IMU，判断是否走流程2
4. 执行流程2

**断流判断范围扩展**：不仅是中间有断点算断流，两端时间差过大也算断流——即第一个 IMU 时间戳与 `lastend` 差距较大，也视为断流。

### 5.3 遗留问题

- ⚠️ ODO 不佳（轮速不可靠）时无特殊处理逻辑，需后续补充
- ⚠️ 建图模式下暂停（减速）问题：李鹏飞长期跟进
- ⚠️ 轮速引入后匹配度下降的研究尚未完结（王亚萌跟进）

---

## 6. 场景汇总矩阵

| 场景 | 模式 | 当前处理方式 | 实现状态 |
|-----|------|------------|--------|
| < 500ms 雷达断流 | 定位 | 轮速递推 | ✅ |
| > 500ms 雷达断流，未停止 | 定位 | 轮速递推兜底；后续 SLAM 主动局部重定位 | ✅ / ⚠️ |
| > 500ms 雷达断流，完全停止 | 定位 | 导航发起局部重定位 | ✅ |
| 用户 pause/resume，无移动 | 定位 | 轮速递推 | ✅ |
| 用户 pause/resume，小位移推动 | 定位 | 导航发起局部重定位 | ✅ |
| 用户 pause/resume，搬动 | 定位 | 全局重定位 | ✅ |
| Lift 连续 > 2s | 所有 | 导航进 ExceptionState，执行重定位流程 | ✅ |
| 重启 | 所有 | 全局重定位 | ✅ |
| `relocate_flag` 上报 | 割草/回充 | 全局重定位 | ✅ |
| versa 局部重定位失败 | 割草/回充 | 全局重定位 | ✅ |
| pause/resume，建图 | 建图 | 仅 prepare 阶段可触发重定位 | ✅ |
| set_pose 非阻塞独立线程 | 定位 | 中期方案 | ⚠️ 方案设计中 |
| set_pose 立即返回，导航继续走 | 定位 | 长期方案 | 🔴 暂缓 |

---

## 7. 开放问题

| # | 问题 | 建议确认人 | 优先级 |
|---|-----|----------|-------|
| Q-1 | 暂停后位移阈值最终值（versa: 60cm? 40cm?；角位移: 0.1rad? 1rad?），各机型联调后确认 | 王亚萌 / 周士伟 | 高 |
| Q-2 | 主动重定位门槛参数（匹配率阈值 + 得分阈值） | 王亚萌 | 中 |
| Q-3 | 轮速不可靠场景（打滑等）的补充处理方案 | 李鹏飞 / 王亚萌 | 中 |
| Q-4 | ESKF update 遗漏 cov 问题影响范围评估 | 廖炳鑫 | 中 |
| Q-5 | 中期方案（独立线程局部重定位）联调时间节点 | 周士伟 | 高 |
```

- **Step 2：验证文档写入成功，图片引用完整**

```bash
grep -c "!\[" overview/modules/common/slam-pause-resume-reloc-2026-04-14.md
```

预期：输出 `2`（对应 mslam_reloc_condition_flow.png 和 mslam_cancel_reloc_flow.png）。

```bash
grep "!\[" overview/modules/common/slam-pause-resume-reloc-2026-04-14.md
```

预期：两行，分别包含 `mslam_reloc_condition_flow.png` 和 `mslam_cancel_reloc_flow.png`。

---

## Task 3：写文档二 — 整机安规策略功能说明

**Files:**

- Create: `overview/modules/common/safety-regulation-2026-04-14.md`
- **Step 1：写文档正文**

完整内容如下（使用 Write 工具直接写入文件）：

```markdown
# 整机安规策略功能说明

> **本文覆盖范围**：智能割草机 7 类安全触发场景的安规需求、参数指标及触发逻辑，含各产品差异说明。
>
> **关联文档**：Lift 触发后的 SLAM 重定位响应逻辑见 [SLAM 暂停恢复与重定位机制 §2.4](slam-pause-resume-reloc-2026-04-14.md#24-lift-触发)；导航侧判断详见 [§3](slam-pause-resume-reloc-2026-04-14.md#3-导航侧判断逻辑)。

---

## 1. 全局汇总表

| 触发类型 | 防抖时长 | 切割刹停 | 驱动刹停 | 刹停距离 | 可自主恢复 | 屏幕显示 |
|---------|---------|---------|---------|---------|----------|---------|
| Stop 按键 | 立即 | ≤2s | ≤2s | ≤200mm | 否（需组合键/归桩） | STOP |
| 抬起 | ❓ xms | ≤2s | ≤2s | ≤200mm | 8s 内传感器恢复可继续 | LIFT → STOP |
| 障碍物（Bumper） | ❓ xms | — | t=D/v | — | 取决于产品定义 | — |
| 倾斜 | ❓ xms | ≤2s | ≤2s | ≤200mm | 8s 内角度恢复可继续 | FLIP → STOP |
| 翻转 | ❓ xms | ≤2s | ≤2s | — | 否（须回正后重启） | STOP |
| 出边界 | — | — | 暂停 | — | 重定位恢复后自动运行 | — |
| 蓝牙断连 | T > 2s | ≤2s | ≤200mm | — | 重连后可重启 | — |

> ❓ 表中 xms 防抖时长均为待定值，需与 TUV 协商或由产品定义。

---

## 2. Stop 按键

### 安规需求

- Stop 按键优先级高于任何割草机自主行为和其他控制动作。
- Stop 触发后，除以下操作外，任何操作都不允许机器启动：
  - 整机屏幕按键 **Mow+OK** 或 **Home+OK** 组合按键
  - 手动放置机器至充电站

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 切割刀盘刹停 | 从 Stop 触发至切割刹停 ≤2s |
| 驱动系统刹停 | 从 Stop 触发至驱动刹停 ≤2s，距离 ≤200mm |

### 触发逻辑

![Stop 触发逻辑](images/common_safety_stop_trigger.png)

---

## 3. 抬起

### 安规需求

- 抬起双轮触发持续 xms（防抖）后，切割电机及驱动电机刹停。
- 切割/驱动刹停后，主机尝试恢复：8s 内传感器恢复则继续割草；否则转 STOP 状态。
- 抬起传感器单轮触发，安规不做处理。

### 检测机制（两驱 vs 四驱）

| 机型 | 检测部位 | 触发条件 | 防抖时长 |
|-----|---------|---------|---------|
| 两驱 | 前轮受力 | 单轮落空 | 300ms |
| 四驱（Monet/Versa） | 后轮减震受力 | 单侧落空 | >20°: 3000ms；10-20°: 1500ms；<10°: 300ms |

**常见误触发场景：**
- 两驱：一侧前轮压树枝 → 另一侧触发；前轮底下有坑 → 该侧触发
- 四驱：一侧后轮压树枝 → 另一侧触发；机器在斜坡上 → 上侧后轮可能触发

> ⚠️ **重定位建议**：单轮抬起误触发较多，建议以**双轮同时抬起**作为重定位触发条件（详见 [SLAM 文档 §2.4](slam-pause-resume-reloc-2026-04-14.md#24-lift-触发)）。

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 切割刀盘刹停 | ≤2s |
| 驱动系统刹停 | ≤2s，距离 ≤200mm |
| 自主恢复时间 | 8s 内传感器恢复可继续割草 |

### 触发逻辑

![抬起触发逻辑](images/common_safety_lift_trigger.png)

---

## 4. 障碍物（Bumper / 8S）

### 安规需求

- 在所有运行方向和位置，传感器均处于活跃状态，除非：
  - 切割装置不运行，且运行距离 D ≤ 2×机身长
  - 切割装置运行，且 D ≤ 行进方向前边缘至最近刀尖缘的距离
- 撞击障碍物时：最大动能 ≤5J；最大力 F：50N ≤ F ≤ 260N（0~0.5s），50N ≤ F ≤ 130N（>0.5s）
- 碰撞持续触发 xms 后，驱动刹停：t = D/v（D = 前边缘至最近刀尖缘距离，v = 接近速度）

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 最大动能 | ≤5J |
| 最大撞击力 | 50N ≤ F ≤ 260N（0~0.5s）；50N ≤ F ≤ 130N（>0.5s） |
| 刹停时间 | t = D/v（按各产品计算） |

### 非接触传感器附加条件

若需依赖减速满足撞击力要求，可附加非接触传感器：

- **作为减速补充**：必须能响应圆柱形目标（直径 70±2mm，高 400±5mm，直立，颜色与背景匹配，常温）
- **替代障碍物传感器**：必须能响应圆柱形目标（直径 25±2mm，高 145~150mm，直立，颜色与背景匹配，常温）

> ❓ 检测到障碍物后是否进行减速，需产品定义。
> ❓ 持续检测 3s / 10s 是否需满足碰撞要求，TUV 沟通中。

### 触发逻辑

![障碍物触发逻辑](images/common_safety_bumper_trigger.png)

---

## 5. 倾斜

### 安规需求

- 倾斜触发角度 ≤ 整机最大倾角 - 3°
- 防抖后，切割电机在 2s 内刹停，驱动电机刹停。
- 8s 内传感器恢复（角度满足 ≤ β - 3°），割草机可继续割草。

### 各产品最大倾角

| 产品 | 最大倾角（宣称）| 触发角度（≤ β-3°） | 实际倾翻角 |
|-----|-------------|----------------|---------|
| Butchart | 34° | ≤31° | ~65° |
| Butchart Pro | 34° | ≤31° | ~65° |
| Monet | 45° | ≤42° | ~70° |
| Versa | 45° | ≤42° | ~70° |

> 注：Monet/Versa 定 45° 是考虑宣称 39° + 5° 陀螺仪波动余量。

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 触发角度 | ≤ 整机最大倾角 - 3° |
| 切割刀盘刹停 | ≤2s |
| 驱动系统刹停 | ≤2s，距离 ≤200mm |
| 自主恢复时间 | 8s 内角度恢复可继续割草 |

### 触发逻辑

![倾斜触发逻辑](images/common_safety_tilt_trigger.png)

---

## 6. 翻转

### 安规需求

- 翻转持续触发 xms（防抖）后，切割电机和驱动电机均在 2s 内刹停。
- 整机处于翻转状态时，手动状态下也无法启动，机器**必须回正后**才能手动启动。

> ❓ 防抖时长 xms 待定（原始文档备注"2s 手都给切了"，实际防抖值需与产品/TUV 确认）。

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 切割刀盘刹停 | ≤2s |
| 驱动系统刹停 | ≤2s |

### 触发逻辑

![翻转触发逻辑](images/common_safety_flip_trigger.png)

---

## 7. 出边界

> **跨文档说明**：出边界场景下，定位丢失的判定和最大位移保障由定位模块负责，详见 [SLAM 暂停恢复与重定位机制](slam-pause-resume-reloc-2026-04-14.md)。

### 安规需求

- 机器不得越过边界超过一个机身长度。
- 机器在距边界外 ≤1m 的位置时，可尝试导航回地图；>1m 时机器无法自主运行，暂停原地。
- 若工作区域改变，机器无法自主运动，暂停原地（允许进入手动状态）。
- 若机器丢失边界信息（定位丢失），位移不得超过 1m。
- 机器恢复到地图内定位后，自动运行，切割装置启动（2s 警示音）。

### 地图边界定义

![地图边界定义](images/common_safety_boundary_map_def.png)

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 安规边界 | 边界位置 + 一个机身长度 |
| 允许运动最大边界 | 边界位置 + 1m（与机身长度取最大值） |
| 丢定位最大位移 | 1m |

> ❓ 定位丢失判定阈值：暂定为纯惯导累计行走距离，具体阈值需与 TUV 沟通确定。
> ⚠️ 1m 最大位移保障依赖 Vslam+惯导实际性能，需定位团队确认能力边界。

### 触发逻辑

![出边界触发逻辑](images/common_safety_boundary_trigger.png)

---

## 8. 蓝牙连接

### 安规需求

- 自动模式下，首次连接距离 < 6m。
- 遥控距离：切割装置启用时 < 6m；不启用时 < 20m。
- 不可采用间接重传（须符合蓝牙规范 ≥5.0）。
- App 连接须使用配对或密码解密方式。
- 遥控机器运动时，切割装置不启用。
- 用户释放控制时，机器须立即停止运动。
- 障碍物检测功能、边界检测功能可以停用，但其他传感器功能须保持。
- App 与机器失联 T > 2s：驱动刹停（距离 ≤200mm），切割刹停（时间 ≤2s），恢复后可重启。

### 核心参数指标

| 目标 | 关键指标 |
|-----|---------|
| 首次连接距离 | < 6m |
| 遥控距离（开刀）| < 6m |
| 遥控距离（停刀）| < 20m |
| 断连刹停 | 切割 ≤2s；驱动 ≤200mm |

---

## 9. 补充交互说明

| 事件 | 即时响应 | 持续未恢复 | 屏幕状态 | 上报 APP |
|-----|---------|----------|---------|---------|
| 触发抬起 | 语音"抬起" + 屏幕 LIFT | 8s 未恢复 → 转 STOP | LIFT → STOP | ✅ 超时后 |
| 触发倾斜 | 语音"倾斜" + 屏幕 FLIP | 8s 未恢复 → 转 STOP | FLIP → STOP | ✅ 超时后 |
| 触发翻转 | 立即 STOP + 语音"倾斜" | — | STOP | ✅ |
| 触发 STOP | 语音"STOP" + 屏幕 STOP | — | STOP | ✅ |

**2s 警示音规范**：单个连续音调或多个音调或间歇（频率=2），发声时间 t ≥2s。

手动状态下：障碍物检测功能、边界检测功能可以停用，但其他传感器功能须保持。

---

## 10. 开放问题

| # | 问题 | 建议确认人 / 渠道 | 优先级 |
|---|-----|----------------|-------|
| Q-1 | 各触发类型 xms 防抖时长（Stop/抬起/障碍物/倾斜/翻转均待定） | TUV 协商 + 产品定义 | 高 |
| Q-2 | 翻转防抖时长（原文注"2s 手都给切了"，实际值需确认） | TUV / 产品 | 高 |
| Q-3 | 定位丢失判定阈值（纯惯导累计距离，TUV 沟通中） | TUV + 定位团队 | 高 |
| Q-4 | 出边界 1m 位移保障——Vslam+惯导的实际保障能力边界 | 定位团队 | 高 |
| Q-5 | 非接触避障：检测到障碍物后是否减速（产品决策） | 产品 | 中 |
| Q-6 | 非接触避障：持续 3s/10s 是否需满足碰撞要求 | TUV 沟通中 | 中 |
| Q-7 | RTK 能否直接接 SoC（当前结论：SoC 内置 MCU 不能用于安规认证） | 硬件 / 安规 | 低 |
```

- **Step 2：验证文档写入成功，图片引用完整**

```bash
grep -c "!\[" overview/modules/common/safety-regulation-2026-04-14.md
```

预期：输出 `7`（对应 Stop/抬起/障碍物/倾斜/翻转/出边界触发逻辑图 + 地图边界定义图）。

```bash
grep "!\[" overview/modules/common/safety-regulation-2026-04-14.md
```

预期：7 行，均包含 `images/common_safety_` 前缀的文件名。

---

## Task 4：添加交叉引用并做最终验证

**Files:**

- Verify: `overview/modules/common/slam-pause-resume-reloc-2026-04-14.md`
- Verify: `overview/modules/common/safety-regulation-2026-04-14.md`
- **Step 1：检查交叉引用链接均已存在**

```bash
grep "safety-regulation-2026-04-14.md" overview/modules/common/slam-pause-resume-reloc-2026-04-14.md
grep "slam-pause-resume-reloc-2026-04-14.md" overview/modules/common/safety-regulation-2026-04-14.md
```

预期：各至少 2 行，分别包含对方文档的相对路径链接。

- **Step 2：核查所有图片文件均存在**

```bash
for f in \
  overview/modules/common/images/common_safety_stop_trigger.png \
  overview/modules/common/images/common_safety_lift_trigger.png \
  overview/modules/common/images/common_safety_bumper_trigger.png \
  overview/modules/common/images/common_safety_tilt_trigger.png \
  overview/modules/common/images/common_safety_flip_trigger.png \
  overview/modules/common/images/common_safety_boundary_trigger.png \
  overview/modules/common/images/common_safety_boundary_map_def.png \
  overview/modules/common/images/mslam_reloc_condition_flow.png \
  overview/modules/common/images/mslam_cancel_reloc_flow.png; do
  [ -f "$f" ] && echo "✅ $f" || echo "❌ MISSING: $f"
done
```

预期：9 行全部以 ✅ 开头。

- **Step 3：核查文档中的图片引用与 images/ 目录文件一一对应**

```bash
# 文档一图片引用
grep "!\[" overview/modules/common/slam-pause-resume-reloc-2026-04-14.md

# 文档二图片引用
grep "!\[" overview/modules/common/safety-regulation-2026-04-14.md
```

逐行确认每个 `images/xxx.png` 引用的文件在 Task 1 生成的文件列表中存在。

---

## Task 5：更新 raw-materials-conventions.md

**Files:**

- Modify: `docs/process/raw-materials-conventions.md`
- **Step 1：在历史记录表末尾追加两行**

在 `## 5. 历史已处理模块记录` 表格末尾追加：

```
| 2026-04-15 | overview/modules/common/ | laser/inbox/0412新增（暂停恢复/局部重定位/断流/重定位条件梳理，专题文档模式） | ✓ 完成 |
| 2026-04-15 | overview/modules/common/ | inbox/0414新增/智能割草机安规策略功能（专题文档模式） | ✓ 完成 |
```

- **Step 2：验证追加成功**

```bash
tail -5 docs/process/raw-materials-conventions.md
```

预期：最后两行包含 `2026-04-15` 和 `专题文档模式`。