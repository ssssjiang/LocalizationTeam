# 定位组管理驾驶舱

> 个人管理工作区，用于持续维护对四个方向（多线激光、融合定位、视觉定位、参数标定）和各项目的全局认知。
> 设计思路详见 [DESIGN.md](./DESIGN.md)。

---

## 快速导航

### 全局管控层（overview/）


| 文件                                         | 内容                  | 更新频率 |
| ------------------------------------------ | ------------------- | ---- |
| [overview/org.md](./overview/org.md)       | 组织全貌、角色分工、运行机制、对上接口 | 每月   |
| [overview/tasks.md](./overview/tasks.md)   | 全组任务汇总、关键路径、跨组依赖    | 每周   |
| [overview/risks.md](./overview/risks.md)   | 全组风险汇总、风险状态、升级记录    | 每周   |
| [overview/collab.md](./overview/collab.md) | 跨组/跨项目协同问题、卡点、拍板人   | 按需   |


| [docs/plan-laser-docs-update.md](./docs/plan-laser-docs-update.md)               | 激光文档补充计划（已完成，2026-04-12）    |

### 小组纵深层（teams/）


| 文件                                                           | 内容                     |
| ------------------------------------------------------------ | ---------------------- |
| [teams/laser/tech.md](./teams/laser/tech.md)                 | 多线激光：技术方案框架、指标、瓶颈、优化方向 |
| [teams/laser/people.md](./teams/laser/people.md)             | 多线激光：人员角色、能力、状态、备注     |
| [teams/fusion/tech.md](./teams/fusion/tech.md)               | 融合定位：技术方案框架、指标、瓶颈、优化方向 |
| [teams/fusion/people.md](./teams/fusion/people.md)           | 融合定位：人员角色、能力、状态、备注     |
| [teams/vision/tech.md](./teams/vision/tech.md)               | 视觉定位：技术方案框架、指标、瓶颈、优化方向 |
| [teams/vision/people.md](./teams/vision/people.md)           | 视觉定位：人员角色、能力、状态、备注     |
| [teams/calibration/tech.md](./teams/calibration/tech.md)     | 参数标定：技术方案框架、指标、瓶颈、优化方向 |
| [teams/calibration/people.md](./teams/calibration/people.md) | 参数标定：人员角色、能力、状态、备注     |


**功能模块过程知识（teams//modules/）**


| 文件                                                                                                         | 内容                           |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------- |
| [teams/calibration/modules/calibration/timeline.md](./teams/calibration/modules/calibration/timeline.md)   | 标定模块：时间线                     |
| [teams/calibration/modules/calibration/decisions.md](./teams/calibration/modules/calibration/decisions.md) | 标定模块：关键决策记录                  |
| [teams/calibration/modules/calibration/problems.md](./teams/calibration/modules/calibration/problems.md)   | 标定模块：问题记录                    |
| [teams/calibration/modules/calibration/gaps.md](./teams/calibration/modules/calibration/gaps.md)           | 标定模块：缺失资料 + 待确认事项            |
| [teams/laser/modules/sensors/timeline.md](./teams/laser/modules/sensors/timeline.md)                       | 激光传感器选型：评估时间线                |
| [teams/laser/modules/sensors/decisions.md](./teams/laser/modules/sensors/decisions.md)                     | 激光传感器选型：选型决策记录（速腾/Mid360/禾赛） |
| [teams/laser/modules/mslam/timeline.md](./teams/laser/modules/mslam/timeline.md)                           | 多线激光 SLAM 模块：算法演进时间线         |
| [teams/laser/modules/mslam/decisions.md](./teams/laser/modules/mslam/decisions.md)                         | 多线激光 SLAM 模块：关键决策记录          |
| [teams/laser/modules/mslam/problems.md](./teams/laser/modules/mslam/problems.md)                           | 多线激光 SLAM 模块：问题记录            |
| [teams/laser/modules/mslam/gaps.md](./teams/laser/modules/mslam/gaps.md)                                   | 多线激光 SLAM 模块：缺失资料 + 待确认事项    |


### 项目横切层（projects/）


| 目录                                                               | 内容             |
| ---------------------------------------------------------------- | -------------- |
| [projects/project-placeholder/](./projects/project-placeholder/) | 示例项目结构（重命名后使用） |


### 工作流程（process/）


| 文件                                                                                       | 内容                             |
| ---------------------------------------------------------------------------------------- | ------------------------------ |
| [docs/process/raw-materials-conventions.md](./docs/process/raw-materials-conventions.md) | 原始材料梳理约定：目录结构、分类标准、条目格式、图片命名规范 |


---

## 原始资料（inbox）


| 位置                                                     | 用途                                                          |
| ------------------------------------------------------ | ----------------------------------------------------------- |
| [inbox/](./inbox/)                                     | 全局：跨组会议记录、上级要求、全局性文档                                        |
| [teams/laser/inbox/](./teams/laser/inbox/)             | 多线激光组：周报、设计文档、技术讨论                                          |
| [teams/fusion/inbox/](./teams/fusion/inbox/)           | 融合定位组：周报、设计文档、技术讨论                                          |
| [teams/vision/inbox/](./teams/vision/inbox/)           | 视觉定位组（VSLAM）：周报、设计文档、技术讨论（标定材料已迁至 teams/calibration/inbox/） |
| [teams/calibration/inbox/](./teams/calibration/inbox/) | 参数标定：原始设计文档、测试数据、方案资料                                       |
| projects//inbox/                                       | 各项目：需求文档、里程碑、评审记录                                           |


---

## 占位符说明


| 占位符         | 含义       |
| ----------- | -------- |
| `【待填充】`     | 信息尚未收集   |
| `【待确认】`     | 信息已有但需核实 |
| `【已过期，待更新】` | 信息可能不准确  |
