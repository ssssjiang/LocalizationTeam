# 标定模块 — 信息缺口

> 记录两类缺口：
>
> 1. **待补充材料**：原始文档中出现过的飞书链接/引用，尚未保存为本地 Markdown
> 2. **待确认事项**：需要向负责人确认的信息点
>
> 处理方式：去飞书收集文档 → 保存到 `teams/vision/inbox/003_标定相关/` → 更新此文件

---

## 一、待补充材料（飞书链接尚未本地化）


| #     | 文档名称        | 飞书链接                                                                                       | 引用自                | 优先级 | 备注                                                           |
| ----- | ----------- | ------------------------------------------------------------------------------------------ | ------------------ | --- | ------------------------------------------------------------ |
| G-002 | 售后整机标定方案-初版 | [JLaHwA1BVi3jj4kfQjSc7lrCnBe](https://roborock.feishu.cn/wiki/JLaHwA1BVi3jj4kfQjSc7lrCnBe) | 售后标定设计文档.md（第189行） | 低   | 当前本地已有后续版本（003_售后整机标定方案/），初版是另一份早期文档，可用于追溯早期决策演变；如设计无重大变化可暂缓 |


---

> **已移除的误判条目：**
>
> - ~~G-001 docker环境配置和代码包更新~~：本地已有 `005_标定与IQC站QA/001_整机二维码标定台操作流程/001_docker环境配置和代码包更新/docker环境配置和代码包更新.md`，内容为 Docker 镜像替换和代码包解压步骤，属纯工具操作文档，**显式标注 skip**（管理价值低，不需进入结构化文档）

---

## 二、待确认事项


| #     | 问题                                                                    | 背景                                         | 找谁确认 | 优先级 |
| ----- | --------------------------------------------------------------------- | ------------------------------------------ | ---- | --- |
| Q-001 | Tci（IMU 到左目外参）最终是如何补齐的？补齐时间？                                          | 2025-10-23 会议记录标注此项缺失，口述确认已完成，但补齐方式未记录     | 邱冰冰  | 中   |
| Q-002 | 标定台操作流程中「联系软件同事」的人员归口是谁？                                              | 操作流程文档在 AT 指令失败 / 行差标定失败时提示联系具体人员，但脱敏未填姓名  | 邱冰冰  | 低   |
| Q-003 | Gaia 多相机标定适配当前具体进展？预计完成时间？                                            | 口述为「正在进行中」（前视双目 + 侧目左右 + 后目共3目）；无书面任务状态    | 邱冰冰  | 高   |
| Q-004 | MCT / IQC 标定功能完成度确认：是否有书面验收记录或测试报告？                                   | 当前仅口述确认「已完成」，缺少对应文档                        | 邱冰冰  | 低   |
| Q-005 | 标定模块当前主要维护代码分支名称？                                                     | 原始材料未提及分支管理信息                              | 邱冰冰  | 中   |
| Q-006 | 开发时的两个 open items 最终是否落地：① APP 能否获取标定成功/失败状态？② 标定结果是否需要上传（数据通路是否已打通）？ | 来自售后整机标定方案-时间计划 §其他项，功能完成时的最终处理方式不可从现有材料确认 | 邱冰冰  | 低   |


---

## 三、图片归档记录

以下图片已从原始材料复制至 `modules/calibration/images/`，并在梳理文档中引用：


| 文件名                                | 来源                                                | 引用位置               |
| ---------------------------------- | ------------------------------------------------- | ------------------ |
| `calib_overall_flow.png`           | 售后标定设计文档/images/whiteboard_1_1775975856719.png    | timeline.md 时间线首图  |
| `calib_param_input_type_1.png`     | 售后标定设计文档/images/Tr2db6OSbovgbgxYEclc8S4BnEf.png   | problems.md P-005  |
| `calib_param_input_type_2.png`     | 售后标定设计文档/images/QSlwbC7hao0iFLx3mlPcihOLn2f.png   | problems.md P-005  |
| `calib_tcrcl_json.jpeg`            | 双目行差方案/images/LZ33bRR5zoGeInxcF9DcyNtCnmb.jpeg    | decisions.md D-004 |
| `calib_ba_bundle_adjuster.png`     | 双目基线标定开发计划/images/JaJ0bxg99oySbyxF1WWcsC64nsF.png | decisions.md D-003 |
| `calib_board_single_sideview.png`  | 售后标定板摆放要求/images/Jq7fbmyz6o9cJtxn0CJc3tO7nad.png  | decisions.md D-002 |
| `calib_board_ab_topview.png`       | 售后标定板摆放要求/images/ZmrmbAjlZoj0nXxXeS2ckq0hn5c.png  | decisions.md D-002 |
| `calib_station_setup.png`          | 售后整机标定方案/images/S7nCb3x2eokgOHx69gJcIWHdnGd.png   | decisions.md D-001 |
| `calib_station_topview.png`        | 售后整机标定方案/images/whiteboard_1_1775975893898.png    | decisions.md D-001 |
| `calib_mct_machine_placement.jpeg` | MCT操作流程/images/Iw3PbUfRfoyv4hxRbKmcfBRWnQb.jpeg   | decisions.md D-001 |


**跳过（批量测试结果类，保留原始材料）：**

- `MCT&IQC Q&A/images/` 下全部4张（打滑检测/遮挡检测/外参失败/result.json截图）
- `整机二维码标定台操作流程/images/` 中3张文件目录及校验结果截图（LX02, F9jAb8, MVfjb）

---

## 已知存在、未提取内容（C 类测试记录，按需查阅）


| 编号    | 文档路径（相对 inbox/006_参数标定/）  | 内容说明                    | 备注              |
| ----- | ------------------------- | ----------------------- | --------------- |
| R-001 | `008_售后标定缩小二维码测试`         | 缩小二维码对标定结果的影响测试         | 测试记录，可按需查阅      |
| R-002 | `011_测试两侧加单目输入图像对标定结果的影响` | 侧目单目图像加入后的标定结果对比测试      | 测试记录            |
| R-003 | `012_侧目鱼眼相机标定数据集测试`       | 侧目鱼眼相机数据集采集与标定测试        | 测试记录            |
| R-004 | `013_售后标定数据集测试`           | 售后标定多数据集验证              | 测试记录            |
| R-005 | `015_售后标定交叉编译测试`          | 售后标定程序交叉编译环境验证          | 测试记录            |
| R-006 | `019_售后标定筛掉lidar掉头路线的数据`  | 筛除 lidar 掉头路线数据对结果的影响测试 | 测试记录            |
| R-007 | `020_售后标定二维码测试`           | 不同二维码配置的标定效果测试          | 测试记录            |
| R-008 | `001_割草机标定操作整理`           | 割草机标定完整操作流程（操作手册类）      | 操作手册，管理价值低，按需查阅 |


---

## 待确认问题（新增）


| 编号    | 问题                                                                       | 来源                             | 负责人 | 优先级 |
| ----- | ------------------------------------------------------------------------ | ------------------------------ | --- | --- |
| Q-007 | 产线遮挡检测最终选用哪个方案（方案一/二/三）？当前文档只有 pros/cons 对比，无最终选型结论。                     | `021_产线遮挡检测设计方案`（见 D-012）      | 邱冰冰 | 中   |
| Q-008 | prebuild/develop 当前是否还有售后标定未解决的 open bug？`018` 文档记录截止 2026-04-02，之后状态未知。 | `018_售后标定合入prebuild dev的bug列表` | 邱冰冰 | 低   |

---

## 五、周报飞书引用（G-003 起，来自 VSLAM 进度同步 -2026 标定模块）

> 来源：`teams/vision/inbox/0412新增/VSLAM 进度同步 -2026`（2026-01 ~ 2026-04 周报，标定方向）

| # | 文档名称 | 飞书链接 | 优先级 |
|---|---------|---------|-------|
| G-003 | 割草机相机标定流程梳理 | [链接](https://roborock.feishu.cn/wiki/LjGuwdGxCiLegzkyjEWcrtt1nUh) | 中 |
| G-004 | Butchart 双目 tuning 结果确认 | [链接](https://roborock.feishu.cn/wiki/QezWw3AcoitBgpkQHSycc6jrnXc) | 中 |
| G-005 | 售后标定耗时优化 | [链接](https://roborock.feishu.cn/wiki/HYFswArkjipUUgkQCKecQei3nPf) | 高 |
| G-006 | 售后标定二维码测试 | [链接](https://roborock.feishu.cn/wiki/Sdalwi7QTiX1czk3orscAMNjnHg) | 中 |
| G-007 | 售后标定一致性分析 | [链接](https://roborock.feishu.cn/wiki/VGE4wvbR8izr1LkMfymcGLehnez) | 中 |
| G-008 | 标定内存优化 | [链接](https://roborock.feishu.cn/wiki/U0MFwFFaIiZQmJkOFE7cLtfwn9d) | 中 |
