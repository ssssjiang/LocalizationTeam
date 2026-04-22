# 定位组原始材料梳理约定

> 供 `raw-materials-curation` Skill 在定位组项目中使用。
> Skill 路径：`~/.cursor/skills/raw-materials-curation/SKILL.md`

---

## 1. 目录结构约定

```
teams/<group>/inbox/           ← 原始材料（按来源编号组织）
teams/<group>/modules/<mod>/   ← 结构化输出
  timeline.md
  decisions.md
  problems.md
  gaps.md
  images/
```

当前各组：

- `teams/laser/`：多线激光组
- `teams/fusion/`：融合定位组
- `teams/vision/`：视觉定位组（VSLAM）
- `teams/calibration/`：参数标定组

---

## 2. 三层分类标准


| 层级      | 定义                               | 处理方式                                    |
| ------- | -------------------------------- | --------------------------------------- |
| **A 类** | 含明确设计结论、方案选型、算法架构、传感器对比结论的文档     | 提取进 decisions.md + timeline.md；关键图片命名链接 |
| **B 类** | 工程推进过程记录：测试结论、bug 修复记录、问题排查、验证结果 | 提取进 timeline.md + problems.md           |
| **C 类** | 批量测试数据表格、操作手册步骤、测试截图日志、交叉编译记录    | gaps.md R-xxx 标注，不提取内容                  |


分类不确定时，优先看文档是否有「结论」或「决策」性质的总结句；有则 A/B，无则 C。

---

## 3. 条目格式规范

### timeline.md

```
| 日期 | 事件标题 | 背景/结论摘要 | 来源文档 |
```

- 日期不确定写「待确认」
- 按时间升序排列
- 同一批 bug 修复可合并为一条，标注版本号或 commit 范围

### decisions.md

```markdown
## D-xxx 标题【已定案 / 待确认】

**背景**
...

**选定方案**
...

**理由**
...

**来源** | inbox/文档路径
```

- 编号全模块唯一，不同 inbox 批次追加时接续
- 「待确认」状态需在 gaps.md 新增对应 Q-xxx 条目

### problems.md

```markdown
## P-xxx 问题标题

- **症状**：...
- **根因**：...
- **修复**：...（「已修复（日期）」/「进行中」/「待修复」）
- **来源**：inbox/文档路径
```

### gaps.md


| 类型    | 含义            | 格式要素                |
| ----- | ------------- | ------------------- |
| G-xxx | 外部链接存在但无本地文件  | 文档名 + 飞书链接 + 首次提及来源 |
| Q-xxx | Open 问题，结论待确认 | 问题描述 + 建议确认人 + 优先级  |
| R-xxx | C 类文档，已知可查    | 文档名 + 所在路径 + 一句话说明  |


---

## 4. 图片命名规范

格式：`<module>_<描述>.<ext>`

- `<module>`：当前处理的模块简写（calib / mslam / sensor / fusion 等）
- `<描述>`：英文或拼音，下划线分隔，说明图片主题

示例：

- `calib_aftersale_station.jpeg`（售后标定场地图）
- `mslam_loop_online_phase1.png`（在线回环优化阶段流程图）
- `sensor_mid360_slam_70m.png`（mid360 70m SLAM 效果图）

---

## 5. 历史已处理模块记录

> 每次完成梳理后追加一行


| 日期         | 模块路径                               | inbox 来源                                      | 状态   |
| ---------- | ---------------------------------- | --------------------------------------------- | ---- |
| 2026-04-12 | laser/modules/sensors/             | 003_多线激光/007_外部设备与slam                        | ✓ 完成 |
| 2026-04-12 | laser/modules/mslam/               | 003_多线激光/006_算法文档 等多个目录                       | ✓ 完成 |
| 2026-04-12 | calibration/modules/calibration/   | vision/inbox/003_标定相关（已迁至 calibration/inbox/） | ✓ 完成 |
| 2026-04-12 | calibration/modules/calibration/   | calibration/inbox/006_参数标定                    | ✓ 完成 |
| 2026-04-12 | vision/modules/vslam/              | vision/inbox/005_视觉slam                       | ✓ 完成 |
| 2026-04-12 | fusion/modules/fusion/             | fusion/inbox/004_融合定位（RTK融合定位部分）              | ✓ 完成 |
| 2026-04-12 | fusion/modules/fastlivo/           | fusion/inbox/004_融合定位（Fast-LIVO2全景地图预研部分）     | ✓ 完成 |
| 2026-04-12 | overview/modules/common/           | inbox/（全组通用文档）                                | ✓ 完成 |
| 2026-04-12 | fusion/modules/fusion/ + fastlivo/ | fusion/inbox/0412新增（增量，6 个文件）                 | ✓ 完成 |
| 2026-04-12 | laser/modules/mslam/               | laser/inbox/0412新增（增量，8 个文件）                  | ✓ 完成 |
| 2026-04-13 | overview/modules/common/           | inbox/0413新增/割草机时间戳同步方案设计 + 中间层数据协议（增量，2 个文件）| ✓ 完成 |
| 2026-04-13 | vision/modules/vslam/              | inbox/0413新增/割草机-小场地光电方案预研（增量，1 个文件）          | ✓ 完成 |
| 2026-04-13 | laser/modules/mslam/               | laser/inbox/0413新增（增量，3 个文件）                  | ✓ 完成 |
| 2026-04-13 | overview/modules/common/           | laser/inbox/0413新增（充电站移位策略，跨模块归档）             | ✓ 完成 |
| 2026-04-13 | fusion/modules/fastlivo/ + fusion/ | fusion/inbox/0413新增（增量，3 个文件）                 | ✓ 完成 |
| 2026-04-13 | overview/modules/common/           | inbox/0413新增/双目盲区相关文档（增量，3 个文件）                 | ✓ 完成 |
| 2026-04-14 | fusion/modules/fusion/             | fusion/inbox/0414新增/启动时RTK 信号差讨论.md（增量，1 个文件）  | ✓ 完成 |
| 2026-04-15 | overview/modules/common/           | laser/inbox/0412新增（暂停恢复/局部重定位/断流/重定位条件梳理，专题文档模式） | ✓ 完成 |
| 2026-04-15 | overview/modules/common/           | inbox/0414新增/智能割草机安规策略功能（专题文档模式）             | ✓ 完成 |
| 2026-04-21 | fusion/modules/fastlivo/           | fusion/inbox/0421新增/三维彩色建图补充地图空洞 V1.0（增量，1 个文件） | ✓ 完成 |
| 2026-04-21 | fusion/modules/fastlivo/           | fusion/inbox/0421新增/实景三维地图拼接方案 -- 20260416（增量，1 个文件） | ✓ 完成 |


