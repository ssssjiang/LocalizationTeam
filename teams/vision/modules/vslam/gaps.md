# VSLAM 模块 — 信息缺口记录

> 来源：`teams/vision/inbox/005_视觉slam`
> 最后更新：2026-04-12

---

## 一、G-xxx：有飞书链接但无本地文件


| ID    | 名称                     | 飞书链接                                                                                                              | 首次提及来源           | 优先级 | 备注                                |
| ----- | ---------------------- | ----------------------------------------------------------------------------------------------------------------- | ---------------- | --- | --------------------------------- |
| G-001 | 0122 室内数据对比分析          | [Abi3wee5piKDaqkzO7kc12U6nBe](https://roborock.feishu.cn/wiki/Abi3wee5piKDaqkzO7kc12U6nBe)                        | OKVIS 转变方向说明     | 低   | OKVIS vs 自研 VSLAM 室内对比原始数据分析      |
| G-002 | 室外 Benchmark 对比表格      | [NkuabkuL5aD5EJsnQVZcd6AwnQh](https://roborock.feishu.cn/base/NkuabkuL5aD5EJsnQVZcd6AwnQh?table=blkXS8l9amkVoJiY) | OKVIS 转变方向说明     | 低   | OKVIS vs 自研 VSLAM 割草机数据 benchmark |
| G-003 | 宽弓字建图时重定位方案            | [S3xNwyqEoidzRZkOVcXc9AZJnKd](https://roborock.feishu.cn/wiki/S3xNwyqEoidzRZkOVcXc9AZJnKd)                        | Eden VSLAM 算法方案  | 高   | 建图过程中重定位的核心方案设计                   |
| G-004 | okvis 建图逻辑             | [LgebwqB1MiEmQEkDlCJck4Junvc](https://roborock.feishu.cn/wiki/LgebwqB1MiEmQEkDlCJck4Junvc)                        | Eden VSLAM 算法方案  | 中   | OKVIS 建图流程的完整说明                   |
| G-005 | 全局图工作项                 | [L6X0wbVW6iqeHFkKc0DcGBxYnKe](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe)                        | 建图+重定位 changelog | 中   | 全局图功能工作项列表                        |
| G-006 | Mapping Interface 接口文档 | [H4fQdAc8Co0HnRx2jPscKdzFn1l](https://roborock.feishu.cn/docx/H4fQdAc8Co0HnRx2jPscKdzFn1l)                        | 建图+重定位 changelog | 中   | 建图模块对外接口设计                        |
| G-007 | 地图优化前后精度及重定位效果         | [A3n1w39UjiOfmUk8plIcKYohnFf](https://roborock.feishu.cn/wiki/A3n1w39UjiOfmUk8plIcKYohnFf)                        | okvis&maplab 对比  | 中   | Maplab 地图优化前后的精度和重定位成功率对比         |
| G-008 | 1.4调优后整图光流两米弓字建图       | [O2WswDZ8eiHqrckNrkncbyACn0c](https://roborock.feishu.cn/wiki/O2WswDZ8eiHqrckNrkncbyACn0c)                        | 整图建图对沿边建图        | 低   | 调优后的整图建图精度参考基线                    |
| G-009 | 侧滑及倾斜检测上机测试            | [GReHwBESyitJBwkUqVrcC5a8nld](https://roborock.feishu.cn/wiki/GReHwBESyitJBwkUqVrcC5a8nld)                        | SLAM change log  | 中   | 打滑+倾斜检测上机测试结果                     |
| G-010 | 斜坡上轮式侧滑分析              | [CbnHwhWebiz8qtkXsYCcXhQxnih](https://roborock.feishu.cn/wiki/CbnHwhWebiz8qtkXsYCcXhQxnih)                        | SLAM change log  | 中   | 斜坡场景打滑情况分析 + benchmark_v1.0 批测    |
| G-011 | okvis退桩位姿跳变（文档）        | [AsX8dMGhboVQdMxHw8pcG00mnHb](https://roborock.feishu.cn/docx/AsX8dMGhboVQdMxHw8pcG00mnHb)                        | SLAM change log  | 低   | 退桩跳变问题的详细分析文档（bug 已修复）            |


---

## 二、Q-xxx：文档中有但无明确结论的 Open 问题


| ID    | 问题描述                                                                 | 来源                             | 建议确认人     | 优先级 |
| ----- | -------------------------------------------------------------------- | ------------------------------ | --------- | --- |
| Q-001 | OKVIS 前端在草地上特征点匹配极少（vs 光流法），当前版本是否已通过引入光流前端解决？目前草地场景前端效果如何？          | OKVIS 转变方向说明（二期计划项）            | VSLAM 负责人 | 高   |
| Q-002 | IMU 100_32 vs 200_64 vs 1000_116 动态 VSLAM 数据实验的最终结论？对定位精度的实际收益是否已验证？ | IMU 采样频率分析（§后续 action）         | VSLAM 负责人 | 中   |
| Q-003 | Eden 项目 okvis+maplab 技术路线当前进展？建图过程中重定位功能是否已落地？                       | Eden VSLAM 算法方案                | VSLAM 负责人 | 高   |
| Q-004 | VSLAM 深度学习特征点调研（SuperPoint 等）后续是否有推进计划？还是已放弃？                        | `006_算法文档/007_VSLAM深度学习特征点-调研` | VSLAM 负责人 | 低   |


---

## 三、R-xxx：C 类文档（已知存在，按需查阅）


| ID    | 文档路径                                                            | 内容说明                                            |
| ----- | --------------------------------------------------------------- | ----------------------------------------------- |
| R-001 | `001_工具文档/001_slamworks编译流程`                                    | slamworks 编译步骤手册（gcc/g++-9, cmake 3.25）         |
| R-002 | `001_工具文档/002_OKVIS 交叉编译`                                       | OKVIS 交叉编译工具链配置（Butchart 平台）                    |
| R-003 | `001_工具文档/003_Podman with ros melodic (ubuntu 22.04)`           | Podman 容器 + ROS melodic 环境配置                    |
| R-004 | `002_架构文档/003_Butchart数据有效验证性自动化需求`                             | 数据有效性自动化检测脚本需求（服务器部署）                           |
| R-005 | `004_需求文档/001_X5 tuning验收需求`                                    | 相机 ISP tuning 验收需求（色彩/Shading/Color shading）    |
| R-006 | `004_需求文档/002_双目二供 - X5 tuning验收需求`                             | 双目二供相机调试需求                                      |
| R-007 | `004_需求文档/003_割草机TR3动态拍图需求`                                     | TR3 动态数据采集需求（双目+IMU+ODO+RTK）                    |
| R-008 | `004_需求文档/004_割草机静态拍图分析结果（定位需求）`                                | 静态拍图场地布置和分析方法（Aprilgrid 30x30cm）                |
| R-009 | `004_需求文档/005_TR4定位数据采集需求整理`                                    | TR4 定位测试需求与优先级列表                                |
| R-010 | `005_测试文档/001_视觉/005_ORB-SLAM3 建图测试`                            | ORB-SLAM3 建图效果批测数据                              |
| R-011 | `005_测试文档/001_视觉/006_内参变化`                                      | 相机内参变化测试记录                                      |
| R-012 | `005_测试文档/001_视觉/008_内测帧率分析`                                    | VSLAM 内测帧率分析数据                                  |
| R-013 | `005_测试文档/001_视觉/009_Deep Image Matching`                       | 深度学习图像匹配对比测试                                    |
| R-014 | `005_测试文档/001_视觉/011_VSLAM数据传输`                                 | VSLAM 数据传输性能测试                                  |
| R-015 | `005_测试文档/001_视觉/012_2993、daily、3029版本丢帧情况对比`                   | 多版本丢帧率对比批测                                      |
| R-016 | `005_测试文档/001_视觉/013_Vslam 跑极线校正图像`                             | 极线校正图像验证测试                                      |
| R-017 | `005_测试文档/001_视觉/015_冒烟测试结果统计/001_Monet 冒烟测试结果分析0912`           | Monet 项目冒烟测试 0912                               |
| R-018 | `005_测试文档/001_视觉/015_冒烟测试结果统计/002_ButchartPro冒烟测试结果分析0912`      | ButchartPro 冒烟测试 0912                           |
| R-019 | `005_测试文档/001_视觉/016_Rebase后重定位分支的benchmark批测`                  | 重定位分支 rebase 后 benchmark 批测                     |
| R-020 | `005_测试文档/001_视觉/017_benchmark跨序列重定位结果`                         | 跨序列重定位 benchmark 数据                             |
| R-021 | `005_测试文档/001_视觉/018_12.30-建图+重定位误差分布直方图统计`                     | 建图+重定位误差分布统计                                    |
| R-022 | `005_测试文档/001_视觉/019_Terramow测试Case`                            | Terramow 竞品测试 Case 文档                           |
| R-023 | `005_测试文档/001_视觉/020_单精度优化精度批测`                                 | 单精度浮点优化对精度影响批测                                  |
| R-024 | `005_测试文档/004_融合模块打滑测试/001_打滑脱困日志整理`                            | 融合模块打滑测试日志                                      |
| R-025 | `005_测试文档/005_数据采集/001_Butchart 定位数据采集需求汇总 20250310`            | Butchart 定位数据采集需求（2025-03-10）                   |
| R-026 | `005_测试文档/005_数据采集/002_视觉定位困难场景数据采集`                            | 困难场景（弱光/重复纹理等）数据采集需求                            |
| R-027 | `005_测试文档/005_数据采集/003_VSLAM定位数据采集需求-1014`                      | VSLAM 定位数据采集需求（1014版）                           |
| R-028 | `005_测试文档/005_数据采集/004_照度采集数据`                                  | 环境照度采集数据                                        |
| R-029 | `006_算法文档/004_Maplab 建图 & 重定位/001_跑通Maplab 建图 & 重定位`            | Maplab 建图+重定位板测耗时数据                             |
| R-030 | `006_算法文档/004_Maplab 建图 & 重定位/002_PC端benchmarks建图效果和耗时`         | PC 端 benchmark 建图效果与耗时记录                        |
| R-031 | `006_算法文档/004_Maplab 建图 & 重定位/003_全局图工作项`                       | 全局图工作项跟踪列表                                      |
| R-032 | `006_算法文档/004_Maplab 建图 & 重定位/005_双目沿边建图精度测试`                   | 双目沿边建图精度测试数据                                    |
| R-033 | `006_算法文档/011_VSLAM使用JPG测试`                                     | JPG（95质量）vs PNG 格式对比测试（结论：JPG 前端跟踪轻微降低，RMSE 略低） |
| R-034 | `009_视觉定位组项目会议跟踪记录`                                             | 视觉定位组周例会/节点 Review 会跟踪记录                        |
| R-035 | `006_算法文档/004_Maplab 建图 & 重定位/009_VSLAM窄通道建图需求/001_窄通道视觉数据采集需求` | 窄通道场景数据采集需求                                     |
| R-036 | `006_算法文档/004_Maplab 建图 & 重定位/009_VSLAM窄通道建图需求/003_窄通道竞品测试需求`   | 窄通道竞品测试需求                                       |


---

## 四、周报飞书引用（G-012 起，来自 VSLAM 进度同步 -2026）

> 以下条目均为周报（2026-01 ~ 2026-04）中出现的飞书链接，尚无对应本地 Markdown 文件。
> 来源：`teams/vision/inbox/0412新增/VSLAM 进度同步 -2026/VSLAM 进度同步 -2026.md`

### OKVIS-VIO 优化方向


| #     | 文档名称                 | 飞书链接                                                              | 所属方向   |
| ----- | -------------------- | ----------------------------------------------------------------- | ------ |
| G-012 | okvis困难场景数据分析        | [链接](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc) | VIO 精度 |
| G-013 | vio上机压测精度分析          | [链接](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd) | VIO 精度 |
| G-014 | 光流追踪与描述子匹配融合算法调研     | [链接](https://roborock.feishu.cn/wiki/LKysw3ioJi1ZADkF3K6cMhQRnkf) | 前端     |
| G-015 | okvis+LET-Net 深度学习光流 | [链接](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf) | 前端     |


### 深度学习特征点方向


| #     | 文档名称           | 飞书链接                                                              | 所属方向   |
| ----- | -------------- | ----------------------------------------------------------------- | ------ |
| G-016 | okvis应用alike-n | [链接](https://roborock.feishu.cn/docx/DrNjdpBDMo9QaJxZgLHcj1Ksntc) | 特征点    |
| G-017 | mapping接入浮点描述子 | [链接](https://roborock.feishu.cn/wiki/D6sVw0ketiX70ZkXE2FcIWTUn2c) | 特征点+建图 |


### 通道建图方向


| #     | 文档名称                | 飞书链接                                                              | 所属方向       |
| ----- | ------------------- | ----------------------------------------------------------------- | ---------- |
| G-018 | VSLAM窄通道建图需求        | [链接](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe) | 通道建图 HF2.2 |
| G-019 | okvis通道建图仿真分析       | [链接](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL) | 通道建图       |
| G-020 | 通道建图测试              | [链接](https://roborock.feishu.cn/wiki/PUAtw4HsNikT2Vk7XYMc7q8onSf) | 通道建图       |
| G-021 | 通道视觉建图接口对齐 - 4.7    | [链接](https://roborock.feishu.cn/wiki/WCwvwhc9ziLdvPkCfAFcoKePnRc) | 通道建图接口     |
| G-022 | OKVIS 通道建图仿真分析与问题修复 | [链接](https://roborock.feishu.cn/wiki/JFZNwjVH3imNuekEHkFc9IThnif) | 通道建图       |


### 全局图与地图合并方向


| #     | 文档名称                        | 飞书链接                                                              | 所属方向       |
| ----- | --------------------------- | ----------------------------------------------------------------- | ---------- |
| G-023 | 通道多 Session 地图合并设计          | [链接](https://roborock.feishu.cn/wiki/GpaNwZthmiWwubkwYwocExx1nNc) | 地图合并 HF3.0 |
| G-024 | 地图合并与 RelocAndBuild 新状态的加入  | [链接](https://roborock.feishu.cn/wiki/XTlhw0D6jiZIG9kg5oOcj6O6nNc) | 地图合并       |
| G-025 | 地图合并实验                      | [链接](https://roborock.feishu.cn/wiki/Ah30wXIbniPDVPkfs9fcSjy1npc) | 地图合并算法     |
| G-026 | isam_PGO开发记录                | [链接](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb) | PGO        |
| G-027 | 基于折返约束的子图切分策略优化与实验分析        | [链接](https://roborock.feishu.cn/wiki/KQnKwXlHqilLDlknVQycMMDjnmd) | 子图划分       |
| G-028 | VIO 与 Gyro 作为旋转先验的跟踪与建图效果分析 | [链接](https://roborock.feishu.cn/wiki/U2jHwSOXlixRBmk0oDUcSHznnBh) | 建图优化       |
| G-029 | 桩点移除                        | [链接](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn) | 地图清理       |
| G-030 | 3m滑轨重构代码运行结果对比              | [链接](https://roborock.feishu.cn/wiki/FWSnwUlwKiopWEkj7bRcK5UWnNZ) | 建图优化       |
| G-031 | 链路3：地图点复用设计文档               | [链接](https://roborock.feishu.cn/wiki/MIqPwfRP5imDp4kcCfVcH1MpnIq) | 地图点复用      |
| G-032 | 建图分支提交整理                    | [链接](https://roborock.feishu.cn/wiki/Yxyhw9HTUismwfkYaMzcQPH4nFh) | 建图维护       |
| G-033 | 单精度优化建图                     | [链接](https://roborock.feishu.cn/wiki/ZZftwtLOiiWyhakBN73cidqjn9c) | 建图优化       |
| G-034 | 子图大小对单子图精度影响分析              | [链接](https://roborock.feishu.cn/wiki/Z3GMwy9FFiIFqAkqXY0cgZTunNa) | 子图划分       |
| G-035 | 单子图内部折返对局部轨迹优化精度的影响         | [链接](https://roborock.feishu.cn/wiki/LowgwwlSNi7Tq2kcAPPcq3tCn7d) | 子图划分       |
| G-036 | maplab加入光流补跟踪补充测试           | [链接](https://roborock.feishu.cn/wiki/FZ80wQE2zimufZkRmm8cFI99nOg) | 建图优化       |
| G-037 | PGO功能测试                     | [链接](https://roborock.feishu.cn/docx/P5qCdhxLHoYxkSxMSvic1GH3nkd) | PGO        |
| G-038 | 整图建图耗时优化                    | [链接](https://roborock.feishu.cn/wiki/PnomwN0a1ipQnVkL5pTcoXhanef) | 建图耗时       |
| G-039 | 找回环时间优化                     | [链接](https://roborock.feishu.cn/wiki/VeOKwHh1PibM3ukNYp3caovRnbd) | 回环检测       |
| G-040 | OKVIS 跟踪与地图点复用总结            | [链接](https://roborock.feishu.cn/wiki/B3jzwtkF1i6pCpk1s63cn7mbnzb) | 建图优化       |
| G-041 | 建图耗时优化分析报告                  | [链接](https://roborock.feishu.cn/wiki/WpMcw4zAWiEkPMk7nZQcC0Obn4c) | 建图耗时       |
| G-042 | 多帧校验：多帧匹配修正 T_map_vio       | [链接](https://roborock.feishu.cn/wiki/NuIRww6ITihflCkmCcicYts7nMf) | 多帧回环       |
| G-043 | 建图规模缩减                      | [链接](https://roborock.feishu.cn/wiki/RgS8wgliei1hBGktpMecq2yMnHc) | 建图优化       |
| G-044 | 建图规模缩减 - 3.9                | [链接](https://roborock.feishu.cn/wiki/R0ekwyL7tiaDBdkv8uxcANBQnsf) | 建图优化       |
| G-045 | 单精度优化精度批测                   | [链接](https://roborock.feishu.cn/wiki/OWoLwl4eOiw9GqkULKbcEwhqntg) | 建图优化       |
| G-046 | 光流补跟踪对整图精度与建图收益的影响分析        | [链接](https://roborock.feishu.cn/wiki/I5r4wAHAuijgi7kotjgcmIAfndd) | 建图优化       |
| G-047 | Online Maplab 精度 - 3.9      | [链接](https://roborock.feishu.cn/wiki/ZRZbwYGpLi82CakuVflcEpDzn8e) | 在线建图       |
| G-048 | vimap online mapping - 3.2  | [链接](https://roborock.feishu.cn/wiki/ATmjwX2DLizcHIkYWYNcvIeunAh) | 在线建图       |
| G-049 | vimap online mapping        | [链接](https://roborock.feishu.cn/wiki/Lb97wrA7ii9ur1kPlVKcSj4NnNe) | 在线建图       |
| G-050 | 后续工作计划                      | [链接](https://roborock.feishu.cn/wiki/EcmcwX3nGiTB6zkiVErcVsUxnV7) | 建图规划       |


### 重定位方向


| #     | 文档名称                     | 飞书链接                                                              | 所属方向   |
| ----- | ------------------------ | ----------------------------------------------------------------- | ------ |
| G-051 | reloc-self_analysis      | [链接](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e) | 重定位    |
| G-052 | Relocalization analysis  | [链接](http://roborock.feishu.cn/wiki/PtlzwEmNHiYYTqk8ZuxcULFinwb)  | 重定位    |
| G-053 | Eden数据错误重定位分析            | [链接](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb) | 重定位    |
| G-054 | okvis多线程重定位测试            | [链接](https://roborock.feishu.cn/wiki/YsX4wM6daiFgWYkIeeRcVA5Vnpe) | 重定位    |
| G-055 | benchmark跨序列重定位结果        | [链接](https://roborock.feishu.cn/wiki/Lafkwp7vpiVGzVkFn7CcLYGbnCb) | 重定位    |
| G-056 | Rebase后重定位分支的benchmark批测 | [链接](https://roborock.feishu.cn/wiki/F6iqwJcruiJmu2kFA9WcuBEmngd) | 重定位    |
| G-057 | 重定位问题数据分析                | [链接](https://roborock.feishu.cn/wiki/MVnnqhXX)                    | 重定位    |
| G-058 | 12.30-建图+重定位误差分布直方图统计    | [链接](https://roborock.feishu.cn/wiki/LxotwaPiyiFj0ckd1GvcBUpUnSe) | 重定位精度  |
| G-059 | 12.01 版本benchmarks 建图效果  | [链接](https://roborock.feishu.cn/wiki/ErpbwgAo5ir9KMkjHXPc5Yk3n8c) | 建图基准   |
| G-060 | Okvis 闭环检测效果分析           | [链接](https://roborock.feishu.cn/wiki/JdEdwnYMsiJVb8kBAnPc7yeHnyh) | 回环     |
| G-061 | 单目 vs 双目 算法对比分析          | [链接](https://roborock.feishu.cn/wiki/Pdn1wmFJ0iboaBkwh5icvgFYnQc) | 建图方案对比 |


### 精度分析与优化方向


| #     | 文档名称                                 | 飞书链接                                                              | 所属方向   |
| ----- | ------------------------------------ | ----------------------------------------------------------------- | ------ |
| G-062 | odo+gyro递推精度分析                       | [链接](https://roborock.feishu.cn/wiki/K2kQw2xk1igR9WkDdoQcyUVXnf9) | 精度分析   |
| G-063 | odo+gyro / VIO / VIO优化版 — 三者 RMSE 对比 | [链接](https://roborock.feishu.cn/wiki/Iwd3wHDCPi7nZNk3N0ucZKOQnRg) | 精度对比   |
| G-064 | okvis非弓字精度提升                         | [链接](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb) | VIO 精度 |
| G-065 | 调整打滑检测平移和旋转阈值                        | [链接](https://roborock.feishu.cn/wiki/EmK9wiaudiEoTakElgUcPKWfnge) | 打滑检测   |
| G-066 | 颠簸路段数据分析                             | [链接](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd) | 鲁棒性    |
| G-067 | 视觉初始化优化                              | [链接](https://roborock.feishu.cn/wiki/IJOLw6PHEiFEkwkeP03cvZainBe) | 初始化    |
| G-068 | 下采样精度变化                              | [链接](https://roborock.feishu.cn/wiki/E6NgwGciCi9IOCkbEkwcTwhMnSe) | 建图优化   |
| G-069 | X5批测与PC批测精度对比                        | [链接](https://roborock.feishu.cn/docx/Y2VGd4y78oOm64xdBRWcy4NFnBW) | 精度对比   |
| G-070 | okvis弓字间隔不均匀                         | [链接](https://roborock.feishu.cn/docx/GzePdKl8DojbVLxDVZIcqldoncb) | VIO 精度 |
| G-071 | okvis2官方改动                           | [链接](https://roborock.feishu.cn/docx/SSm6dIaYNom8hgxk8yOcbZSNnqd) | 框架跟踪   |
| G-072 | 斜坡数据采集需求                             | [链接](https://roborock.feishu.cn/wiki/QMF7w1hh1izzJ8kAOrKcBjBLnZW) | 鲁棒性    |
| G-073 | 0112测试结果                             | [链接](https://roborock.feishu.cn/docx/CpordUL5Jop2OgxQpK4c7eUdnrR) | 批测记录   |


### 项目与系统方向


| #     | 文档名称                     | 飞书链接                                                              | 所属方向        |
| ----- | ------------------------ | ----------------------------------------------------------------- | ----------- |
| G-074 | Eden VSLAM算法方案           | [链接](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) | Eden 项目     |
| G-075 | Eden VSLAM视觉建图摸底同步       | [链接](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd) | Eden 项目     |
| G-076 | 全局图工作项                   | [链接](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) | 全局图规划       |
| G-077 | Butchart 低优先级TODO        | [链接](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme) | Butchart 项目 |
| G-078 | cf-交接文档                  | [链接](https://roborock.feishu.cn/docx/VQsEddxQNoReMaxJiVnch4KfnFd) | 交接          |
| G-079 | CIIQC（相机来料质量控制）站维护工作     | [链接](https://roborock.feishu.cn/wiki/CBdvwlM8xiFEcWkI9zqcIOIunyp) | IQC 站       |
| G-080 | Let-vins                 | [链接](https://roborock.feishu.cn/wiki/CLeOwfqOgiJGHmk0WMMcam1on3e) | 竞品调研        |
| G-081 | 水下视觉slam相关调研             | [链接](https://roborock.feishu.cn/wiki/Wuu2wsnZsikeyrk9obdcLg0Snxe) | 调研          |
| G-082 | 定位组-售后双目基线标定开发计划         | [链接](https://roborock.feishu.cn/wiki/PdAWwAtQNipZLlkrmBucqwxPneF) | 标定×VSLAM    |
| G-083 | 产线MCT整机外参标定数据统计          | [链接](https://roborock.feishu.cn/wiki/B51KwQTpqiM0ETkxfOScduRinFX) | 标定×VSLAM    |
| G-084 | 泳池机器人图像质量分析              | [链接](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh) | 泳池项目        |
| G-085 | 泳池机器人okvis测试             | [链接](https://roborock.feishu.cn/wiki/MF1ewBTbWiUeNUkOKlzcsyJGnEh) | 泳池项目        |
| G-086 | 售后标定筛掉lidar掉头路线的数据       | [链接](https://roborock.feishu.cn/wiki/V5dDwFHtkiobsLkBjb3c01axn0b) | 标定×VSLAM    |
| G-087 | 售后标定合入prebuild dev的bug列表 | [链接](https://roborock.feishu.cn/wiki/TQmawZ0FJiHEgbkJAXicX6GPnsh) | 标定×VSLAM    |
| G-088 | 割草机 RGBD 数据采集表（飞书 wiki） | [链接](https://roborock.feishu.cn/wiki/NaxUwrkQhiMkxwkQdBcclXLOnuf?sheet=921f6d) | 小场地预研 |
| G-089 | 割草机 RGBD 数据采集 bag 包存储（飞书云盘） | [链接](https://roborock.feishu.cn/drive/folder/LTiNf1wYIlN659dajKbcAQUPn8d) | 小场地预研 |


---

## 五、Q-xxx：小场地预研 Open 问题（来自 0413新增）

> 来源：`inbox/0413新增/割草机-小场地光电方案预研（双目_RGBD）_2026-04-13-10-56-27`

| ID    | 问题描述 | 来源 | 建议确认人 | 优先级 |
| ----- | ------- | ---- | --------- | --- |
| Q-005 | 小场地光电方案 RGBD vs 双目实测对比结论（3.4 数据分析、3.5 对比结论章节均为空白，数据采集中） | 小场地预研文档 §3.4/3.5 | 视觉/小场地负责人 | 高 |
| Q-006 | RGB-D 方案参数最终定版（第 4 章空白）——量程/分辨率/帧率最终选型未完成 | 小场地预研文档 §4 | 视觉/小场地负责人 | 高 |
| Q-007 | 小场地模组开发计划（第 5 章空白）——开发排期/里程碑未填写 | 小场地预研文档 §5 | 项目/小场地负责人 | 中 |
