# 专题文档生成 — 设计规格

**日期**：2026-04-15  
**作者**：songshu  
**状态**：待实现

---

## 1. 目标与范围

从以下 5 份原始文档生成 **2 份独立专题文档**，两文档在关键节点交叉引用。

### 原始材料


| #   | 文档路径                                                                    | 内容                       | 归属  |
| --- | ----------------------------------------------------------------------- | ------------------------ | --- |
| 1   | `teams/laser/inbox/0412新增/暂停恢复-定位优化_2026-04-12-23-48-10/暂停恢复-定位优化.md`   | SLAM 各场景下暂停/恢复的定位支撑策略    | 文档一 |
| 2   | `teams/laser/inbox/0412新增/局部重定位减少对导航静止依赖优化.md`                          | 局部重定位三阶段优化方案             | 文档一 |
| 3   | `teams/laser/inbox/0412新增/断流情况和逻辑调整1.21讨论.md`                           | IMU/雷达断流 predict 两阶段拆分方案 | 文档一 |
| 4   | `teams/laser/inbox/0412新增/重定位条件与流程梳理_2026-04-13-00-02-51/重定位条件与流程梳理.md` | 导航侧重定位触发条件 + 优化方向 + 实现方案 | 文档一 |
| 5   | `inbox/0414新增/智能割草机安规策略功能_2026-04-15-00-27-10/智能割草机安规策略功能.md`           | 整机安全触发策略需求规格（7 类触发）      | 文档二 |


### 目标读者

同团队接手工程师（激光 SLAM / 导航联调）。要求：读完后能独立定位 bug、理解设计决策、知道哪些功能已上线 / 哪些仍在开发。

---

## 2. 输出文件

```
overview/modules/common/
  slam-pause-resume-reloc-2026-04-14.md       ← 文档一
  safety-regulation-2026-04-14.md             ← 文档二
  images/
    （已有，补引用）
    mslam_reloc_condition_flow.png
    mslam_cancel_reloc_flow.png
    （从安规 inbox 复制并重命名）
    common_safety_stop_trigger.png            ← whiteboard_1_1776184033494.png
    common_safety_lift_trigger.png            ← whiteboard_2_1776184036540.png
    common_safety_bumper_trigger.png          ← whiteboard_3_1776184040247.png
    common_safety_tilt_trigger.png            ← whiteboard_4_1776184045227.png
    common_safety_flip_trigger.png            ← whiteboard_5_1776184050231.png
    common_safety_boundary_trigger.png        ← whiteboard_6_1776184055228.png
    common_safety_boundary_map_def.png        ← NES0bgA5soIMCxxyWvgcLnIrnNd.png
```

---

## 3. 内容状态标注约定

在两份文档中，统一用以下标记区分实现状态，确保读者一眼识别：


| 标记            | 含义                 |
| ------------- | ------------------ |
| `✅ 已实现`       | 已合入，可依赖            |
| `⚠️ 方案设计中`    | 方案已定，未合入或联调中       |
| `🔴 暂缓 / 待启动` | 有设计但明确延后，或有安全风险未处理 |
| `❓ 待确认`       | 参数/结论尚未确定          |


---

## 4. 文档一：SLAM 暂停恢复与重定位机制

**文件**：`overview/modules/common/slam-pause-resume-reloc-2026-04-14.md`

### 4.1 章节结构

```
# SLAM 暂停恢复与重定位机制

## 0. 导读
  - 本文覆盖范围说明
  - 与安规文档的关系（交叉引用 safety-regulation-2026-04-14.md §3）
  - 快速索引表：触发场景 → 对应章节

## 1. 正常定位运行（背景）
  - SLAM 定位模式下的状态机简述
  - 与导航的核心接口（relocate_flag / set_pose / check_pose）

## 2. 中断分类与触发参数
  - 2.1 雷达断流
      - < 500ms：轮速兜底，不暂停
      - > 500ms：机器暂停（pause），恢复后触发局部重定位
  - 2.2 用户主动暂停（pause/resume）
      - 无搬动：轮速递推
      - 小位移推动：导航发起局部重定位（versa 位移阈值 / RTK 位移阈值）
      - 搬动：全局重定位
  - 2.3 断流期间未完全停止 vs 完全停止的区别处理
  - 2.4 Lift 触发
      - 两驱 / 四驱检测机制差异
      - 单轮 / 双轮触发建议（建议用双轮作为重定位触发条件）
      - ❓ 防抖时长（两驱 300ms；四驱按角度分级：>20° 3000ms, 10-20° 1500ms, <10° 300ms）
  - 2.5 重启

## 3. 导航侧判断逻辑
  - 通用触发条件（所有任务）：lift 2s / 移动重定位 / 重启 / relocate_flag / versa 局部重定位失败
  - 机型差异参数表：
      | 条件 | versa | RTK |
      | 位移阈值 | 0.4m | 0.4m |
      | 角位移阈值 | 0.1rad（暂停/雷达关） | 1rad（暂停时） |
  - 建图模式特殊限制：仅 prepare 阶段可触发
  - 各任务触发条件对比（割草 / 回充 / 建图 差异说明）
  - 优化方向：单轮抬起 + 姿态变化联合判断（⚠️ 待实现）；坡道检测引入四驱（⚠️ 待实现）
  - 重定位流程图（![重定位状态机流程图](images/mslam_reloc_condition_flow.png)）
  - 导航实现方案流程图（images/mslam_cancel_reloc_flow.png）

## 4. SLAM 侧响应策略
  - 4.1 轮速递推兜底
      - 适用场景（断流未完全停止 / 500ms 内 / 建图 pause/resume）
      - 限制：轮速不可靠时无特殊处理（⚠️ 待改进）
  - 4.2 局部重定位（set_pose）三阶段方案
      - ✅ 短期：set_pose 前后加轮速补偿，处理静止等待期间少量运动
      - ⚠️ 中期（方案设计中，周士伟负责）：
          - 独立线程执行局部重定位
          - 主线程继续 SLAM 递推（不刷新地图）
          - 成功 → 修正 pose + 刷新地图；失败 → false → 导航发起全局重定位
      - 🔴 长期（暂缓，安全风险）：
          - set_pose 立即返回 true，导航开始行走
          - 独立线程计算，完成后修正；失败 → 主动发起全局重定位
          - 风险：导航已经开始行走，位姿未修正
  - 4.3 主动重定位触发（✅ 已实现）
      - 连续多帧匹配率 + 得分低于阈值 → 定位主动通知导航 → 全局重定位

## 5. 断流专项：predict 两阶段拆分
  - 5.1 原始方案（初版）
      - predict-to-start：无 IMU / 断流 >250ms → ODO 递推；否则 IMU 积分
      - predict-to-end：帧内 IMU 断流 >25ms → ODO predict + 去畸变；否则 IMU predict
  - 5.2 改进版（sync 重写）
      - 前置条件：上次处理时 last_end 之前 IMU 已清空
      - 增加检测逻辑：抓取 last_end → cur_start 之间的 IMU 判断是否走流程1
      - 断流判断范围：不仅是中间断流，两端时间差过大（首个 IMU 与 lastend 差距大）也算断流
  - ⚠️ 遗留问题：odo 不佳时无特殊处理；建图模式暂停减速问题（李鹏飞长期跟进）

## 6. 场景汇总矩阵
  | 场景 | 当前处理 | 实现状态 |
  覆盖：建图/定位各 pause/resume 场景 × 处理方式

## 7. 开放问题
  - 暂停后位移阈值最终值（60cm? 1rad? 待联调确认）
  - 主动重定位门槛参数（匹配率 + 得分阈值）
  - 轮速不可靠场景的补充处理方案
  - ESKF update 遗漏 cov 问题（廖炳鑫跟进）
```

### 4.2 图片引用


| 图片                                      | 来源                        | 使用位置         |
| --------------------------------------- | ------------------------- | ------------ |
| `images/mslam_reloc_condition_flow.png` | 已有（mslam/images/ 拷贝或符号引用） | §3 重定位状态机流程  |
| `images/mslam_cancel_reloc_flow.png`    | 已有                        | §3 导航实现方案5.1 |


> 注：原始 inbox 文档中的 whiteboard 图（whiteboard_1_1776008893661.png 等）本地 inbox 目录无实体文件；mslam/images/ 中现有同主题图片视为已处理版本，直接引用。

---

## 5. 文档二：整机安规策略功能说明

**文件**：`overview/modules/common/safety-regulation-2026-04-14.md`

### 5.1 章节结构

```
# 智能割草机安规策略功能

## 0. 导读
  - 安规触发事件与 SLAM 重定位的关系
  - 交叉引用：slam-pause-resume-reloc-2026-04-14.md §2.4（Lift）/ §3（导航判断）

## 1. 全局汇总表
  | 触发类型 | 防抖时长 | 切割刹停 | 驱动刹停 | 刹停距离 | 可自主恢复 | 屏幕显示 |
  | Stop | 立即 | ≤2s | ≤2s | ≤200mm | 否（需组合键/归桩） | STOP |
  | 抬起 | ❓ xms | ≤2s | ≤2s | ≤200mm | 8s内恢复可继续 | LIFT→STOP |
  | 障碍物 | ❓ xms | - | t=D/v | - | - | - |
  | 倾斜 | ❓ xms | ≤2s | ≤2s | ≤200mm | 8s内角度恢复可继续 | FLIP→STOP |
  | 翻转 | ❓ xms | ≤2s | ≤2s | - | 否（需回正） | STOP |
  | 出边界 | - | - | 暂停 | - | 重定位后自动恢复 | - |
  | 蓝牙断连 | T>2s | ≤2s | ≤200mm | - | 重连后可重启 | - |

## 2. Stop 按键
  - 安规需求：最高优先级，覆盖所有自主行为
  - 参数指标：切割/驱动刹停 ≤2s，驱动距离 ≤200mm
  - 解锁条件：Mow+OK / Home+OK 组合键 或 手动放置充电站
  - 触发逻辑图（images/common_safety_stop_trigger.png）

## 3. 抬起
  - 检测机制：
      - 两驱：前轮受力，单轮落空即触发；防抖 300ms
      - 四驱（Monet/Versa）：后轮减震受力；角度分级防抖
  - 常见误触发场景（树枝 / 坑 / 斜坡）
  - ⚠️ 重定位建议：单轮抬起误触发多，建议以双轮同时抬起作为重定位触发条件
  - 8s 自主恢复逻辑：8s内传感器恢复 → 继续割草；超时 → 转 STOP 状态
  - 触发逻辑图（images/common_safety_lift_trigger.png）

## 4. 障碍物（Bumper / 8S）
  - 安规需求：最大动能 ≤5J，撞击力 50N~260N（0~0.5s）/ 50N~130N（>0.5s）
  - 刹停时间：t = D/v（D = 前缘至最近刀尖距离，v = 接近速度）
  - 非接触传感器附加条件：
      - 减速补充：圆柱直径 70±2mm，高 400±5mm
      - 替代障碍物传感器：圆柱直径 25±2mm，高 145-150mm
  - ❓ 非接触避障：检测到障碍物后是否减速，需产品定义
  - ❓ 持续接触 3s / 10s 是否需符合碰撞要求，TUV 沟通中
  - 触发逻辑图（images/common_safety_bumper_trigger.png）

## 5. 倾斜
  - 各产品最大倾角：
      - Butchart / Butchart Pro：34°（实际倾翻 65°）
      - Monet / Versa：45°（实际倾翻 70°，含 5° 陀螺仪波动余量）
  - 触发角度 = 最大倾角 - 3°
  - 8s 自主恢复逻辑（同抬起）
  - 触发逻辑图（images/common_safety_tilt_trigger.png）

## 6. 翻转
  - 翻转后切割/驱动均刹停
  - ❓ xms 防抖后刹停（原文"2s手都给切了"，防抖时长待定）
  - 手动状态下也禁止启动，必须回正才能重启
  - 触发逻辑图（images/common_safety_flip_trigger.png）

## 7. 出边界
  - 地图边界定义图（images/common_safety_boundary_map_def.png）
  - 边界规则：
      - 距边界外 ≤1m：尝试导航回地图
      - 距边界外 >1m：暂停原地（允许手动状态）
      - 工作区域改变：无法自主运动，暂停原地
  - 丢定位规则：❓ 纯惯导累计行走距离阈值待定（TUV 沟通中）
  - 丢定位最大位移：1m（依赖 Vslam+惯导性能，⚠️ 待确认具体保障能力）
  - 恢复后：自动运行，切割装置启动（2s 警示音）
  - 触发逻辑图（images/common_safety_boundary_trigger.png）

## 8. 蓝牙连接
  - 自动模式首次连接距离 < 6m
  - 遥控距离：开刀 <6m / 停刀 <20m
  - 规范要求：蓝牙 ≥ 5.0，不可间接重传；App 连接需配对或密码解密
  - 断连（T>2s）：驱动刹停 ≤200mm，切割刹停 ≤2s，恢复后可重启
  - 遥控运动时切割装置不启用；用户释放控制立即停止

## 9. 补充交互说明
  - LIFT 状态：语音报"抬起" + 屏幕 LIFT；8s 未恢复 → 转 STOP + 上报 APP
  - FLIP 状态：语音报"倾斜" + 屏幕 FLIP；8s 未恢复 → 转 STOP + 上报 APP
  - 翻转：立即转 STOP + 语音报"倾斜" + 上报 APP
  - STOP：语音报 STOP + 屏幕 STOP + 上报 APP
  - 2s 警示音规范：单/多音调或间歇（频率=2），持续 ≥2s

## 10. 开放问题
  - 各触发类型 xms 防抖时长（多处待定，需与 TUV 协商或产品定义）
  - RTK 能否直接接 SoC（当前结论：SoC 内置 MCU 不能用于安规认证）
  - 丢定位判定阈值（纯惯导累计距离，TUV 沟通中）
  - 非接触避障持续检测 3s/10s 的处理方式（TUV 待沟通）
```

### 5.2 图片处理


| 源文件                                                                                  | 目标文件                                                            | 操作  |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------- | --- |
| `inbox/0414新增/智能割草机安规策略功能_2026-04-15-00-27-10/images/whiteboard_1_1776184033494.png` | `overview/modules/common/images/common_safety_stop_trigger.png` | 复制  |
| `whiteboard_2_1776184036540.png`                                                     | `common_safety_lift_trigger.png`                                | 复制  |
| `whiteboard_3_1776184040247.png`                                                     | `common_safety_bumper_trigger.png`                              | 复制  |
| `whiteboard_4_1776184045227.png`                                                     | `common_safety_tilt_trigger.png`                                | 复制  |
| `whiteboard_5_1776184050231.png`                                                     | `common_safety_flip_trigger.png`                                | 复制  |
| `whiteboard_6_1776184055228.png`                                                     | `common_safety_boundary_trigger.png`                            | 复制  |
| `NES0bgA5soIMCxxyWvgcLnIrnNd.png`                                                    | `common_safety_boundary_map_def.png`                            | 复制  |


---

## 6. 交叉引用约定


| 引用位置              | 引用目标                                              |
| ----------------- | ------------------------------------------------- |
| 文档一 §2.4（Lift 触发） | → `safety-regulation-2026-04-14.md` §3（抬起检测机制）    |
| 文档一 §3（导航侧触发条件）   | → `safety-regulation-2026-04-14.md` §1（全局汇总表）     |
| 文档二 §0（导读）        | → `slam-pause-resume-reloc-2026-04-14.md` §2 / §3 |
| 文档二 §7（出边界，丢定位）   | → `slam-pause-resume-reloc-2026-04-14.md`（定位模块负责） |


---

## 7. 实现步骤

1. 复制安规 7 张图片到 `overview/modules/common/images/`（重命名）
2. 写文档一：按 §4.1 章节结构，内联所有原始文档内容，补图片引用
3. 写文档二：按 §5.1 章节结构，内联所有安规内容，补图片引用
4. 在两文档指定节点添加交叉引用链接
5. 更新 `docs/process/raw-materials-conventions.md`（追加本次处理记录）

---

## 8. 不在本次范围内

- 不修改已有 `teams/laser/modules/mslam/decisions.md` 等结构化文档
- 不修正 G-34 gap（单独处理，不在专题文档生成范围内）
- 不生成 decisions/gaps/problems 条目（本次输出目标是专题文档）

