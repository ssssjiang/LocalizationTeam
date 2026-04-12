# 多线激光 SLAM — 缺口记录

> 记录两类待跟进事项：
>
> 1. **缺失资料**：文档中引用了飞书链接但尚未导入为本地 markdown 的材料
> 2. **待确认事项**：需要向负责人当面确认的信息
>
> 优先级：`高` / `中` / `低`

---

## 一、缺失资料（需去飞书收集导入）


| #   | 资料名称          | 引用来源文档         | 飞书链接                                                                                               | 优先级 | 备注                                                  |
| --- | ------------- | -------------- | -------------------------------------------------------------------------------------------------- | --- | --------------------------------------------------- |
| G-3 | mid360 远点情况分析 | 割草机slam激光雷达需求  | [RzKKwyiFUieA77k7bZYcKjt6nhS](https://roborock.feishu.cn/wiki/RzKKwyiFUieA77k7bZYcKjt6nhS)         | 中   | 远距离测距验证材料，本地无对应文件                                   |
| G-5 | 回环测试数据云盘目录    | 回环现阶段情况        | [JurUf0UDwlPPSidxF6scETrBnRh](https://roborock.feishu.cn/drive/folder/JurUf0UDwlPPSidxF6scETrBnRh) | 低   | 原始测试数据云盘，按需查阅；无法本地化，知悉即可                            |
| G-6 | 各精度对比测试详细结果   | 激光SLAM精度对比测试结论 | 见测试结论文档中各链接                                                                                        | 中   | 部分子文档已在 `008_测试文档/002_激光SLAM精度对比测试/` 下本地化；待逐一核对哪些仍缺 |
| G-9 | 减少重定位测试需求     | 取消重定位算法流程及测试结果 | [XylFwvZ5QiMHWvkwFm4c55f0nkw](https://roborock.feishu.cn/wiki/XylFwvZ5QiMHWvkwFm4c55f0nkw)         | 中   | 取消重定位功能的配套测试需求文档，本地无对应文件                            |


| G-11 | 激光LiDAR充电桩移位策略（产品需求飞书 wiki） | inbox/011_软件架构/017_激光LiDAR充电桩移位需求分解 | [HiQSwqbC6iYoY5kzV6pc7ixcnXc](https://roborock.feishu.cn/wiki/HiQSwqbC6iYoY5kzV6pc7ixcnXc)         | 中   | 产品需求原始文档，本地无对应文件                                    |
| ~~G-12~~ | ~~VERSA 导航-定位模块交互~~ | 多线组会 | [AqOGwVOuWimt7ykP2oTcSHpYnag](https://roborock.feishu.cn/wiki/AqOGwVOuWimt7ykP2oTcSHpYnag) | ✓ | **已本地化**：teams/laser/inbox/0412新增/VERSA导航-定位模块交互…/VERSA导航-定位模块交互：建图&定位&重定位.md；已整合进 decisions.md D-021 |
| G-13 | 重定位-多线优化 | 多线组会（D-016 / D-017）| [YnMowj2EdinNB3k6VA8cUpcXnEF](https://roborock.feishu.cn/wiki/YnMowj2EdinNB3k6VA8cUpcXnEF) | 高 | 局部重定位改进方案主文档，周报 2026-01 至今持续引用 |
| ~~G-14~~ | ~~暂停恢复-定位优化~~ | 多线组会（D-016）| [SVSVwhOTziKSyekR1X1cOR70n2d](https://roborock.feishu.cn/wiki/SVSVwhOTziKSyekR1X1cOR70n2d) | ✓ | **已本地化**：teams/laser/inbox/0412新增/暂停恢复-定位优化_2026-04-12-23-48-10/暂停恢复-定位优化.md；已整合进 decisions.md D-016 |
| ~~G-15~~ | ~~局部重定位减少对导航静止依赖优化~~ | 多线组会（D-016 / D-017）| [LxeJwCAuViu62tkruz1cDRHBn4d](https://roborock.feishu.cn/wiki/LxeJwCAuViu62tkruz1cDRHBn4d) | ✓ | **已本地化**：teams/laser/inbox/0412新增/局部重定位减少对导航静止依赖优化.md；已整合进 decisions.md D-022 |
| ~~G-16~~ | ~~退化检测算法文档~~ | 多线组会（D-019）| [MYPJwwPE3iGH5NkLyLRchMo9nUg](https://roborock.feishu.cn/wiki/MYPJwwPE3iGH5NkLyLRchMo9nUg) | ✓ | **已本地化**：teams/laser/inbox/0412新增/退化检测算法文档_2026-04-12-23-49-48/退化检测算法文档.md；已整合进 decisions.md D-019 |
| ~~G-17~~ | ~~断流情况和逻辑调整~~ | 多线组会（D-015）| [ShOmwIkCLiB6bik4blscmuxcn5e](https://roborock.feishu.cn/wiki/ShOmwIkCLiB6bik4blscmuxcn5e) | ✓ | **已本地化**：teams/laser/inbox/0412新增/断流情况和逻辑调整1.21讨论.md；已整合进 decisions.md D-015 |
| G-18 | 割草机 lidar 脏污 follow 视觉-遮挡检测 | 多线组会（在研文档列表）| [K6JUweIzAiDez2kw5W1cqZe3nae](https://roborock.feishu.cn/wiki/K6JUweIzAiDez2kw5W1cqZe3nae) | 高 | 脏污/遮挡检测在研主文档，D-020 / Airy lite 脏污方案关联 |
| G-19 | 遮挡检测 2.0 | 多线组会（在研）| [NnCEwg58SiekdVkynBVc3TNznfb](https://roborock.feishu.cn/wiki/NnCEwg58SiekdVkynBVc3TNznfb) | 高 | 新版遮挡检测方案，与 G-18 配套 |
| G-20 | 相机 IMU 可行性分析 | 多线组会（D-018 / 双目 IMU 预研）| [QRQzwJRuLiDmudkSNwOcogEUnhg](https://roborock.feishu.cn/wiki/QRQzwJRuLiDmudkSNwOcogEUnhg) | 中 | 王亚萌/明坤双目 IMU 预研，私包已验证通过，文档尚未导入 |
| G-21 | 回环新逻辑分析与方案设计 | 多线组会（应竞帆）| [Q6YTwz70UiN2y8kgl9BcfjPtnxf](https://roborock.feishu.cn/wiki/Q6YTwz70UiN2y8kgl9BcfjPtnxf) | 中 | 应竞帆负责的回环新逻辑方案，2026-03 仍在引用 |
| G-22 | 回环整理优化 2.0 | 多线组会（回环方向）| [IEDXwUbfki210qkB2RdcbBh0nWf](https://roborock.feishu.cn/wiki/IEDXwUbfki210qkB2RdcbBh0nWf) | 中 | 回环 2.0 版本整理文档，明坤/应竞帆相关 |
| G-23 | localmap 开发 | 多线组会（在研文档，闫冬）| [RXOnw2dZqiSUMoketqKclVrlnzh](https://roborock.feishu.cn/wiki/RXOnw2dZqiSUMoketqKclVrlnzh) | 中 | 闫冬负责的 localmap（小地图）开发主文档 |
| G-24 | 地图缺失下小地图方案对比结果 | 多线组会（闫冬，localmap）| [T2QZwXFmDiDBdAkby7Vc4ktvn8g](https://roborock.feishu.cn/wiki/T2QZwXFmDiDBdAkby7Vc4ktvn8g) | 中 | localmap 方案选型对比结果，G-23 配套 |
| G-25 | local map + 全局修正定位方案及测试 | 多线组会 | [L059wzjdqiHe9GkQuCIc7VX2nTh](https://roborock.feishu.cn/wiki/L059wzjdqiHe9GkQuCIc7VX2nTh) | 中 | localmap 与全局定位结合方案，可能是 G-23 子文档 |
| G-26 | odoparser 存在的问题 | 多线组会（D-009 问题追踪）| [YZJGwVcZai8jJDkWVv5cJ8ZmnVJ](https://roborock.feishu.cn/wiki/YZJGwVcZai8jJDkWVv5cJ8ZmnVJ) | 中 | odoparser 已知问题清单，D-009 补充材料 |
| G-27 | 匹配中退化抑制分析和决策 | 多线组会（退化相关）| [FXQnwgNpai27rEkix97cxFB7n8f](https://roborock.feishu.cn/wiki/FXQnwgNpai27rEkix97cxFB7n8f) | 中 | 退化抑制决策文档，D-019 配套 |
| G-28 | 新器件 Airy lite / ER1 表现 | 多线组会（P-008 相关）| [PvVwwAM2fijGbzkfOrxcDltCn2e](https://roborock.feishu.cn/wiki/PvVwwAM2fijGbzkfOrxcDltCn2e) | 中 | Airy lite 新器件表现评估，P-008 攻坚参考 |
| G-29 | 展会模式 SLAM 改动 | 多线组会（在研）| [ZJZBwv8zmiWuRDkZwlOc4hXVnLd](https://roborock.feishu.cn/wiki/ZJZBwv8zmiWuRDkZwlOc4hXVnLd) | 中 | 展会场景专项 SLAM 改动文档 |
| G-30 | 斜坡定位可接受垂直 FOV 上限 | 多线组会（在研文档）| [S53rdRKcKoi2F4xK4y6ctVpZnPh](https://roborock.feishu.cn/docx/S53rdRKcKoi2F4xK4y6ctVpZnPh) | 低 | 斜坡场景 FOV 约束分析，roll/pitch 约束相关 |
| G-31 | roll pitch 约束 SLAM | 多线组会（在研文档）| [CzLId70SCoQNkuxmwQcc1H2gnCf](https://roborock.feishu.cn/docx/CzLId70SCoQNkuxmwQcc1H2gnCf) | 低 | roll/pitch 约束加入 SLAM 的方案文档 |
| G-32 | 定位抖动问题整理 | 多线组会（定位稳定性）| [U5e2wI7ehitjPEkX8hucWy4dnzy](https://roborock.feishu.cn/wiki/U5e2wI7ehitjPEkX8hucWy4dnzy) | 低 | 定位抖动问题系统性整理，闫冬/周士伟相关 |
| G-33 | 使用 Perf 对 SLAM 算法性能优化 | 多线组会（在研文档）| [TRFKwFRj6in3PokHBnQcGIXOnVd](https://roborock.feishu.cn/wiki/TRFKwFRj6in3PokHBnQcGIXOnVd) | 低 | SLAM 性能调优方法文档（Perf 工具使用）|
| G-34 | 重定位条件与流程梳理 | 暂停恢复-定位优化（参考文档）| [X3A2wYD1sid9QokLm03cMNyBnmd](https://roborock.feishu.cn/wiki/X3A2wYD1sid9QokLm03cMNyBnmd) | 高 | 暂停恢复文档第一条参考链接，梳理所有触发重定位的条件与完整流程，本地无对应文件 |
| G-35 | 版本排期和管理 | 激光割草机slam重点合入问题跟踪（时间表参考）| [QUQPskIyGhiuxLtPofNc8yAtnMh](https://roborock.feishu.cn/sheets/QUQPskIyGhiuxLtPofNc8yAtnMh) | 低 | 各版本合入排期表，sheet 类文档无法本地化，知悉即可 |

---

## 三、本地参考文档（B 类，按需查阅）

| # | 文档名称 | 本地路径 | 说明 |
|---|---------|---------|------|
| R-001 | 激光割草机 SLAM 重点合入问题跟踪 | teams/laser/inbox/0412新增/激光割草机slam重点合入问题跟踪_2026-04-12-23-11-43/激光割草机slam重点合入问题跟踪.md | 近期合入 bug 汇总表（bug #482985 / #492582 / #490853 / #483380 / #481581），对应 P-009/P-013/P-014/P-015 及 timeline |

---

> **已移除的误判条目（本地文件实际存在）：**
>
> - ~~G-1 激光SLAM数据采集规范~~：本地已有 `008_测试文档/002_激光SLAM精度对比测试/006_激光 SLAM 数据采集规范、场景与精度评估说明/`
> - ~~G-2 速腾airy和mid360+禾赛对比分析~~：本地已有 `007_外部设备与slam/002_速腾airy和mid360 +禾赛对比分析/`，已纳入 `modules/sensors/` 模块梳理
> - ~~G-7 雷达断流2.0~~：本地已有 `006_算法文档/015_雷达断流/002_断流2.0/断流2.0.md`，已整合进 `mslam/decisions.md`
> - ~~G-8 重定位-导航交互文档~~：本地已有 `006_算法文档/003_重定位-▶导航交互/重定位-_导航交互.md`，已整合进 `mslam/decisions.md`

---

## 二、待确认事项（需向负责人确认）


| #    | 问题                                         | 涉及文件                                 | 优先级 | 建议确认方式                                                                                              |
| ---- | ------------------------------------------ | ------------------------------------ | --- | --------------------------------------------------------------------------------------------------- |
| Q-1  | 回环方向负责人是谁？（材料中出现 `private/yjf/` 分支）        | tech.md；modules/mslam/ 全部文件          | 高   | 直接问小组长                                                                                              |
| Q-2  | 大场景（>2万平）Z 漂移问题当前最新进展？是否仍在攻坚？              | problems.md P-001；decisions.md D-006 | 高   | 1:1 或组会确认                                                                                           |
| Q-3  | 当前 mslam 主分支名称是什么？                         | tech.md；timeline.md                  | 高   | 问负责人或看代码仓库                                                                                          |
| Q-4  | 前端 IESKF 选型是否有过与其他方案的对比讨论？                 | decisions.md D-002                   | 中   | 问技术骨干                                                                                               |
| Q-5  | 器件选型中禾赛未入选的具体原因（禾赛 JT16 树冠处点云发散，是否还有其他考量）？ | modules/sensors/decisions.md SD-003  | 中   | 问负责人                                                                                                |
| Q-6  | Versa core dump 问题当前状态：已解决 / 仍存在？          | problems.md P-005                    | 中   | 问负责人或看 bug 跟踪系统                                                                                     |
| ~~Q-7~~ | ~~回环现阶段情况本地文档是否与飞书最新版本同步？~~ | ~~006_算法文档/007_回环现阶段情况/回环现阶段情况.md~~ | ✓ 已同步 | 已确认（2026-04-12） |
| Q-8  | 信号流文档中多个接口标注「没有实现」，目前实现状态如何？               | tech.md 第五节；信号流总结                    | 高   | 问小组长或看代码                                                                                            |
| Q-9  | 断流2.0 斜坡补偿缺陷当前是否已有修复方案或排期？                 | problems.md P-007                    | 中   | 问负责人                                                                                                |
| Q-10 | 激光款重定位充电桩时，草坪外局部定位的「建通道距离限制」具体数值是多少？       | inbox/011_软件架构/017_激光LiDAR充电桩移位需求分解  | 中   | 问产品/算法负责人                                                                                           |
| Q-11 | 四驱正运动学：「左后轮速度+左前轮速度」/「右后轮速度+右前轮速度」模型的 w/v 符号如何统一？ | 四驱里程计正运动学模型推导（文末 open Q1） | 中 | 问 odoparser 模块负责人 |
| Q-12 | 四驱正运动学：能否仅通过左前轮速度和左后轮速度确定运动方向，不依赖外部量（如转角）？ | 四驱里程计正运动学模型推导（文末 open Q2） | 中 | 问 odoparser 模块负责人 |
| Q-13 | 应竞帆已离职，回环调试记录（G-21）和回环新逻辑方案（G-22）谁来接手？ | teams/laser/people.md @应竞帆 | 高 | 问组长；确认回环方向文档归档及接手人 |
| Q-14 | ~~刘博当前状态~~（已确认：刘博为 SPM，非激光组算法成员，跨组协作接口人，无需跟踪） | teams/laser/people.md @刘博 | ~~中~~ | 已关闭 |
| Q-15 | 断流 2.0 + 主动重定位导航联调目标 4.13 是否如期完成？当前最新联调状态？ | decisions.md D-016；problems.md P-006 | 高 | 问王亚萌 / 组长 |
| Q-16 | 局部重定位 BBS ±15m 单帧方案（D-017）验证结果如何？当前阻塞在阈值问题上的具体情况？ | decisions.md D-017；problems.md P-010 | 中 | 问周士伟 / 闫冬 |


---

## 待确认：images/ 中的孤立图片

以下图片已复制到 `images/` 但尚未在任何 md 文件中被引用，原始来源和对应章节待确认：


| 文件名                             | 核查结论                                                         | 处理状态               |
| ------------------------------- | ------------------------------------------------------------ | ------------------ |
| ~~`signal_flow_architecture.jpeg`~~ | 来源确认：`004_架构文档/001_信号流总结/信号流总结.md`（原始文件 `Ox3NbWIuAokohexrcihcLZRgnKd.jpeg`） | ✓ 已引用：`tech.md` 第五节「系统接口」 |
| ~~`debug_keyword_filter.png`~~  | 全局扫描 inbox（003_多线激光 + 0412新增）均无 `keyword` 字样，来源无法溯源 | ✓ 已删除（2026-04-12，C 类调试截图，无文档记录，无决策价值） |
