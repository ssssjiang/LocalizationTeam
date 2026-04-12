# 融合定位 — Gaps

> 模块：`teams/fusion/modules/fusion/`
> 来源 inbox：`teams/fusion/inbox/004_融合定位`

---

## 外部链接（本地无对应文件）

### G-001 割草机时间戳同步方案设计

- **链接**：https://roborock.feishu.cn/docx/FmeadwBfvodJ7GxXFQKc6r56nUe
- **首次提及**：001_架构文档/003_时间同步方案/时间同步方案.md

### G-002 架构文档（飞书会议录像）

- **链接**：https://roborock.feishu.cn/minutes/embed/obcn5z94sz27ebh7e28e918q
- **首次提及**：001_架构文档/架构文档.md

### G-003 RTK 初始化方案（语雀）

- **链接**：https://cinderella.yuque.com/unxgtt/yzvmqo/md1zwtcgsnexn3nx
- **首次提及**：002_算法文档/算法文档.md

### G-004 定位&重定位策略（产品策略，小倩）

- **链接**：https://roborock.feishu.cn/wiki/J87lwBzQdiqfYZk48nZc5RNAn8c
- **首次提及**：002_算法文档/008_重定位/001_导航-slam重定位接口

### G-005 四驱里程计方案与验证

- **链接**：https://roborock.feishu.cn/wiki/FUjyw5u1qigfmAkqMHickKPAnBb
- **首次提及**：周报 2025-09-17 @范超（Monet odo 处理策略）

### G-006 轨迹平滑策略

- **链接**：https://roborock.feishu.cn/wiki/SoTgwEbsQi2XIbkxn31c0qM9n1b
- **首次提及**：周报 2025-12-04 @李岩（降低轨迹横向抖动）

### G-007 RTK 脱困（卡困）检测算法

- **链接**：https://roborock.feishu.cn/wiki/Jfb8w2xRhiJwdJk7n1pcslJgnWg
- **首次提及**：周报 2025-11-06 @范超（卡困检测算法进度，P0）

### G-008 窄通道测试结果与分析（2026-03）

- **链接**：https://roborock.feishu.cn/wiki/AekGwrNKViAgV3keY2lcO4Man4f
- **首次提及**：周报 2026-03-05 @刘宏伟

### ~~G-009 通道外 RTK 假固定判断方案~~

> ✓ 本地已有：`inbox/0412新增/通道外假固定判断_2026-04-13-00-07-56/通道外假固定判断.md`；内容已提取到 `decisions.md D-025`

### G-010 多帧对齐问题分析与回归

- **链接**：https://roborock.feishu.cn/wiki/Xft3wcBRHiiagiky4u5c4Khznpc
- **首次提及**：周报 2026-03-05 @刘宏伟（多帧对齐 BUG 回归）

### ~~G-011 搬动重定位工作计划与自测~~

> ✓ 本地已有：`inbox/0412新增/搬动重定位融合模块_2026-04-13-00-06-54/` + `搬动重定位自测_2026-04-13-00-07-12/`；内容已提取到 `decisions.md D-026`、`timeline.md`

### ~~G-012 VIO 对齐 RTK 方案~~

> ✓ 本地已有：`inbox/0412新增/vio对齐rtk方案_2026-04-13-00-05-58/vio对齐rtk方案.md`；内容已提取到 `decisions.md D-027`

---

## Open 问题（结论待确认）

### Q-001 视觉初始化位置选择策略

- **问题**：v1.0 优化方向提出「找到卫星信号极好的位置作初始化」，结合视觉误差发散判断初始化点更新/失效；具体策略和阈值尚未明确成文
- **建议确认人**：融合定位算法负责人
- **优先级**：高（直接影响视觉辅助精度，P-002 的根本解法）

### Q-002 RTK 建图中搬动恢复方案的专利风险

- **问题**：草坪边界对齐方案存在专利风险，当前未明确规避路径
- **建议确认人**：法务 / 专利工程师
- **优先级**：中（影响方案落地时间）

### Q-003 非搬动重定位中 vslam 重定位能力

- **问题**：方案文档中提到「比如当前阶段 vslam 没有重定位能力」，当前 vslam 是否已支持重定位尚不明确
- **建议确认人**：vslam 模块负责人
- **优先级**：高（影响重定位方案完整可用性）

### Q-004 和芯 vs 司南 RTK 最终选型结论

- **问题**：动态/静态对比测试各有优劣，未见最终选型决策文档
- **建议确认人**：硬件负责人 / 产品
- **优先级**：中

### Q-005 nRTK 多供应商区域账号池匹配策略

- **问题**：SR-ID-03 要求「根据用户区域匹配对应供应商账号池」，文档标注 TBD，具体区域划分规则和账号分配逻辑尚未明确
- **建议确认人**：IoT 平台负责人 / 产品
- **优先级**：中（影响国际化部署）

---

## 参考文档（C 类，按需查阅）

### R-001 RTK 测试方案（10 个典型场景手册）

- **路径**：teams/fusion/inbox/004_融合定位/003_测试文档/001_RTK/003_RTK测试方案/RTK测试方案.md
- **说明**：空旷/树林/水边/单边墙/房檐/窄通道等 10 个标准测试场景定义和布置说明

### R-002 RTK debug 日志分析工具使用手册

- **路径**：teams/fusion/inbox/004_融合定位/005_工具文档/001_RTK debug日志分析工具/RTK debug日志分析工具.md
- **说明**：下载日志（RTK_binId13）→ Win 工具分析；单点解与 RTK 解对比脚本；驱动工具说明

### R-003 RR_TOOL 分析 RTK 数据使用方法

- **路径**：`teams/fusion/inbox/0412新增/RR_TOOL分析RTK数据使用方法_2026-04-12-20-17-00/RR_TOOL分析RTK数据使用方法.md`
- **说明**：RR-Mower-Tools.exe 工具操作手册；支持 RTK_BinId13 数据分析、定位曲线绘制、差分龄期/卫星数统计、海导M4协议和LoRa协议解析（V1.1.2~V1.1.5，2025-12~2026-03）

### R-004 割草机融合模块版本记录（xlsx）

- **路径**：`teams/fusion/inbox/0412新增/割草机融合模块版本_20260412_230325.xlsx`
- **说明**：融合模块版本历史记录表，按需查阅

---

## 融合组周报飞书链接（2025-07~2026-04）

### ESKF & IMU 递推（李岩）

### G-013 互补滤波数据测试

- **链接**：https://roborock.feishu.cn/wiki/X3gKwFnz1ioXgwkzCyrcwhe0nXf
- **首次提及**：融合组开发进展周报

### G-014 自测结果优化：1211

- **链接**：https://roborock.feishu.cn/wiki/O0iNwNGRIidrG0klRZvcpo1GnUp
- **首次提及**：融合组开发进展周报

### G-015 航向角收敛测试

- **链接**：https://roborock.feishu.cn/wiki/ULMTwPVy9irtjykFtggcKv9Xnfb
- **首次提及**：融合组开发进展周报

### G-016 Rtk-odo align仿真

- **链接**：https://roborock.feishu.cn/wiki/T1jkwJurriX5EUkylAPcFDgynih
- **首次提及**：融合组开发进展周报

### G-017 IMU 递推和 lidar pose比较

- **链接**：https://roborock.feishu.cn/wiki/UkcuwghdTi2rVwkxdGncjoA5nhc
- **首次提及**：融合组开发进展周报

### G-018 割草机 IMU 递推和 lidar pose比较（欠科学版）

- **链接**：https://roborock.feishu.cn/wiki/MaCfwzTlYigfmzk1kExc7Q78n9F
- **首次提及**：融合组开发进展周报

### G-019 高温70度\_imu\_bias统计

- **链接**：https://roborock.feishu.cn/wiki/CufYwOTwdi8QgkkKTQccu92Vnic
- **首次提及**：融合组开发进展周报

### G-020 Tof + IMU 跑家徒四壁场景问题及解决方案设计 20251217   持续更新ing

- **链接**：https://roborock.feishu.cn/wiki/KYe5wcfN1ihuw6k6wDxcCLEXnbd
- **首次提及**：融合组开发进展周报

### G-021 IMU递推

- **链接**：https://roborock.feishu.cn/wiki/OUSmwqEK1il1e1kf49cc0nMrnpe
- **首次提及**：融合组开发进展周报

### G-022 FAST-LIVO2跑 Tof + IMU 数据

- **链接**：https://roborock.feishu.cn/wiki/FQYywQT2VijRzKkPIqwcG81Vnch
- **首次提及**：融合组开发进展周报

### G-023 FAST-LIVO2跑ToF + IMU

- **链接**：https://roborock.feishu.cn/wiki/IXsuwoWNriV0YckfM9ec3E8Ln9d
- **首次提及**：融合组开发进展周报

### G-024 IMU Propagation Doc

- **链接**：https://roborock.feishu.cn/wiki/MLMjwwwzHiiCsRkiRS7cyQu8nSe
- **首次提及**：融合组开发进展周报

### G-025 双IMU调研

- **链接**：https://roborock.feishu.cn/wiki/XIeZwXbe2i2bGfk6RF2cH3TknFe
- **首次提及**：融合组开发进展周报

### G-026 rtk-odo align改进自测

- **链接**：https://roborock.feishu.cn/wiki/SFYwwf9nAi2tFYkpPqvc7s2VnJf
- **首次提及**：融合组开发进展周报

### G-027 ~~ imu\_prop~~

- **链接**：https://roborock.feishu.cn/wiki/CKZLwu8htif7h0kNM9qcHf20nHd
- **首次提及**：融合组开发进展周报

### G-028 IMU噪声标定

- **链接**：https://roborock.feishu.cn/wiki/RT4Tw060viMh1jk9TiscaVubnPd
- **首次提及**：融合组开发进展周报

### G-029 imu\_jiaoyan

- **链接**：https://roborock.feishu.cn/wiki/LzbOwfnxOisf3MkjrqycvtQEnGc
- **首次提及**：融合组开发进展周报

### G-030 基于数据（imu v.s. odom）一致性的机器状态判断

- **链接**：https://roborock.feishu.cn/wiki/XvlJwbDFli4jMmkviN7c4K6Knje
- **首次提及**：融合组开发进展周报

### 通道内外假固定（李岩）

### G-031 通道外假固定判断

- **链接**：https://roborock.feishu.cn/wiki/LMzVwFLuGinsa6k58TCcxv5onrh
- **首次提及**：融合组开发进展周报

### G-032 假固定处理5.0

- **链接**：https://roborock.feishu.cn/wiki/J4FXwrgZeieaWckzDSvcqwz8nIc
- **首次提及**：融合组开发进展周报

### G-033 假固定处理4.0

- **链接**：https://roborock.feishu.cn/wiki/CON8wZyytiuvLvkwFQfcIF55nRg
- **首次提及**：融合组开发进展周报

### G-034 窄通道建图回充测试 20260306

- **链接**：https://roborock.feishu.cn/wiki/B2KWwVn1KihuijkPAhncEIghnad
- **首次提及**：融合组开发进展周报

### G-035 RTK 假固定解判定方法研究与实验分析（基于标准差阈值与机器学习） -- 20260123v1

- **链接**：https://roborock.feishu.cn/wiki/M1TzwA4xEibGUdkMxpIcrQ0HnIe
- **首次提及**：融合组开发进展周报

### G-036 固定解分数测试结果

- **链接**：https://roborock.feishu.cn/wiki/QkhrwpnB9i6WlAkYKMVcdgfknPg
- **首次提及**：融合组开发进展周报

### G-037 rtk固定解过滤new

- **链接**：https://roborock.feishu.cn/wiki/Q0b1whI4jigXSWkBdE1cy22Mntg
- **首次提及**：融合组开发进展周报

### G-038 rtk固定解跳变检测

- **链接**：https://roborock.feishu.cn/wiki/VAsxwda5DidB8RkzucocFvJRn9e
- **首次提及**：融合组开发进展周报

### G-039 RTK假固定原始数据分析

- **链接**：https://roborock.feishu.cn/wiki/ZAo1wOkN7iOo4qkaDJacc0rHnne
- **首次提及**：融合组开发进展周报

### G-040 RTK假固定解处理方案

- **链接**：https://roborock.feishu.cn/wiki/DJyQw02iFiopsmkhO6dczkVEntd
- **首次提及**：融合组开发进展周报

### 搬动重定位 & 阴影区（范超）

### G-041 阴影区出桩V2.0-融合模块

- **链接**：https://roborock.feishu.cn/wiki/YZUMwEqAkiDua2kWkv8cEctTnMg
- **首次提及**：融合组开发进展周报

### G-042 搬动重定位自测

- **链接**：https://roborock.feishu.cn/wiki/DtpQw66E5iMa02kM5h9cZJo5nAf
- **首次提及**：融合组开发进展周报

### G-043 RTK阴影区两段退桩定位-导航接口

- **链接**：https://roborock.feishu.cn/wiki/F02CwiiTbimDNrkpDfccmrAxntf
- **首次提及**：融合组开发进展周报

### G-044 RTK阴影区出桩初始化自测

- **链接**：https://roborock.feishu.cn/wiki/R4zWw8ix8iBYdAkheZdc4lnHnKc
- **首次提及**：融合组开发进展周报

### G-045 搬动优化工作计划表

- **链接**：https://roborock.feishu.cn/wiki/T1mhwx6L9iv82tkwhnvc9wZAndd
- **首次提及**：融合组开发进展周报

### 多帧/单帧对齐 & Bug 分析（刘宏伟）

### G-046 欧区禅道3469、3470 bug分析归档

- **链接**：https://roborock.feishu.cn/wiki/NI1EwoxbViJNU5kf72HcpMyUnWb
- **首次提及**：融合组开发进展周报

### G-047 群话题BUG分析

- **链接**：https://roborock.feishu.cn/wiki/MgZLwflx7iO3UQkliPbcofC5nEc
- **首次提及**：融合组开发进展周报

### G-048 多线重定位Bug分析归档 -- 20260410

- **链接**：https://roborock.feishu.cn/wiki/XU7owdQ8LigQh5k24HzcLK6SnPh
- **首次提及**：融合组开发进展周报

### G-049 BUG 478697 & 多帧对齐优化回归

- **链接**：https://roborock.feishu.cn/wiki/AD8Nw1XeHipgghkpVFccXET3nIh
- **首次提及**：融合组开发进展周报

### G-050 减少建图重定位1.0

- **链接**：https://roborock.feishu.cn/wiki/KTPuwqzrmie1makTZ55cvcq6njM
- **首次提及**：融合组开发进展周报

### G-051 1米、2米对齐、单帧对齐对比评估

- **链接**：https://roborock.feishu.cn/wiki/HOzCwmCSfiKJ9okJ7sVcXM4mnnm
- **首次提及**：融合组开发进展周报

### G-052 bug分析记录

- **链接**：https://roborock.feishu.cn/wiki/XcpVwZtfri2gtckr8ntcSTcinOf
- **首次提及**：融合组开发进展周报

### G-053 vio对齐rtk方案

- **链接**：https://roborock.feishu.cn/wiki/GNhLw62IeiBy1ukF85Zc5SCxnKb
- **首次提及**：融合组开发进展周报

### G-054 多帧对齐问题

- **链接**：https://roborock.feishu.cn/wiki/IojpwZIxYiPxSSkBtfQcvszznSb
- **首次提及**：融合组开发进展周报

### G-055 多帧对齐回归数据测试

- **链接**：https://roborock.feishu.cn/wiki/HOevwsvVliMGmykrzZdcRi7Knxc
- **首次提及**：融合组开发进展周报

### FAST-LIVO2 & 三维重建（刘宏伟）

### G-056 Flora 5.2mm雷达罩是否影响融合三维重建 20260402

- **链接**：https://roborock.feishu.cn/wiki/XH77wGL0FiVHAUkMPeucBwfanQb
- **首次提及**：融合组开发进展周报

### G-057 FAST-LIVO2 硬件加速

- **链接**：https://roborock.feishu.cn/wiki/DEdlw2gmTils8ikoTzPcydnSnud
- **首次提及**：融合组开发进展周报

### G-058 点云渲染调研

- **链接**：https://roborock.feishu.cn/wiki/RGj9wY4Qwi8oM6kni8BciPypn3d
- **首次提及**：融合组开发进展周报

### G-059 FAST-LIVO2 存图及使用时机

- **链接**：https://roborock.feishu.cn/wiki/WYaFwJqa0iH0vwkXxuPc8MQMnbe
- **首次提及**：融合组开发进展周报

### G-060 PCD转图片

- **链接**：https://roborock.feishu.cn/wiki/PE4kw1ypPidAmTkAzegcW6NcnXf
- **首次提及**：融合组开发进展周报

### G-061 雷达罩是否影响融合彩色建图 -- 20260311

- **链接**：https://roborock.feishu.cn/wiki/CskFwTMkGiZ0olkMl5kcJBCrnEe
- **首次提及**：融合组开发进展周报

### G-062 三维重建雷达数据和双目gdc彩图采集需求

- **链接**：https://roborock.feishu.cn/wiki/KfwSwJ5QFisjuBk8pm4cSjkLngf
- **首次提及**：融合组开发进展周报

### G-063 Flora &amp; VersaPro三维重建效果摸底 - 20260128

- **链接**：https://roborock.feishu.cn/wiki/OaURwWtKqirMuFkj8GxcAB8dnyh
- **首次提及**：融合组开发进展周报

### G-064 FAST-LIVO2使用不同的策略去降低内存

- **链接**：https://roborock.feishu.cn/wiki/HtNwwdMwvi0qlEkfvvNckRuonIb
- **首次提及**：融合组开发进展周报

### G-065 外场60栋三维重建得到的原始点云及降采样后点云

- **链接**：https://roborock.feishu.cn/wiki/Yn7kwpSoLi1gwwkRkdbcnv7nngc
- **首次提及**：融合组开发进展周报

### G-066 三维重建 -- 彩色点云降采样方案 20251216

- **链接**：https://roborock.feishu.cn/wiki/KilxwRXrEisNe6kaWFVc9bYsnBg
- **首次提及**：融合组开发进展周报

### G-067 跑FAST-LIVO2遇到了问题

- **链接**：https://roborock.feishu.cn/wiki/WGGmwSJp3ic6tnkgDWhctJZAnHg
- **首次提及**：融合组开发进展周报

### G-068 FAST-LIVO2 算法流程&融合原理&方案分析

- **链接**：https://roborock.feishu.cn/wiki/Qr6bwvOVVi1BUokCxhRcD3W6nNg
- **首次提及**：融合组开发进展周报

### G-069 FAST-LIVO2

- **链接**：https://roborock.feishu.cn/wiki/Tzshw314xixA0vklLuLcfOsRnrf
- **首次提及**：融合组开发进展周报

### G-070 FAST-LIVO2激光数据集适配与纯LIO模式运行说明

- **链接**：https://roborock.feishu.cn/wiki/RXjswXFpAi5xXAk0SZrciGEOndb
- **首次提及**：融合组开发进展周报

### nRTK & RTK 信号质量（茹毅超）

### G-071 NRTK定位导航对接需求

- **链接**：https://roborock.feishu.cn/wiki/L9DKw6ym9iCO9xkKQI8cbcOjnAe
- **首次提及**：融合组开发进展周报

### G-072 nrtk测试结果

- **链接**：https://roborock.feishu.cn/wiki/WYfwwPXLFicqV9kZ7kqccaMPnub
- **首次提及**：融合组开发进展周报

### G-073 平滑操作对位置恢复的影响

- **链接**：https://roborock.feishu.cn/wiki/NjPxwYPJNiXDTjkXmvKclthVnUc
- **首次提及**：融合组开发进展周报

### G-074 960E标志位测试专项

- **链接**：https://roborock.feishu.cn/wiki/HlGHwgiwCiSakLkH2E2cuwqlnuh
- **首次提及**：融合组开发进展周报

### G-075 960e场景采集

- **链接**：https://roborock.feishu.cn/wiki/For0wS97Ni8cvskqVnhc7liMnq2
- **首次提及**：融合组开发进展周报

### G-076 960E标志位分析

- **链接**：https://roborock.feishu.cn/wiki/QpB9wuoemiUCjEkAfqRcqKOsncg
- **首次提及**：融合组开发进展周报

### G-077 NRTK 半双工测试

- **链接**：https://roborock.feishu.cn/wiki/Mp1fwzaPUiw8CAkiaACczn72n1f
- **首次提及**：融合组开发进展周报

### G-078 nrtk经纬高转东北天

- **链接**：https://roborock.feishu.cn/wiki/APb9wK91ti1sQykoodtcEWkUnwe
- **首次提及**：融合组开发进展周报

### G-079 nrtk启动会议内容

- **链接**：https://roborock.feishu.cn/wiki/IghFwEXBkigfN0kOExAc1I1lnxd
- **首次提及**：融合组开发进展周报

### G-080 nRTK测试计划

- **链接**：https://roborock.feishu.cn/wiki/BOyMwU5Bii0xE3klwbVc5KFknlg
- **首次提及**：融合组开发进展周报

### G-081 RTK差分龄期统计

- **链接**：https://roborock.feishu.cn/wiki/WP6qwyE9tiEf5BkLqEscpJ3Rn7g
- **首次提及**：融合组开发进展周报

### G-082 手动配置nrtk示例

- **链接**：https://roborock.feishu.cn/wiki/Plicw8ZLniW3klkqTn1cqSOpnEh
- **首次提及**：融合组开发进展周报

### 真值评测 & 工具（林子越/范超）

### G-083 轨迹好坏量化评价v1.0

- **链接**：https://roborock.feishu.cn/wiki/OLDowfwLOirn7Bkih3QczcCgnqc
- **首次提及**：融合组开发进展周报

### G-084 Benchmark表格

- **链接**：https://roborock.feishu.cn/base/NkuabkuL5aD5EJsnQVZcd6AwnQh
- **首次提及**：融合组开发进展周报

### G-085 多线融合仿真

- **链接**：https://roborock.feishu.cn/wiki/JF1YwOm6biXAVWkZbbocIGtanHc
- **首次提及**：融合组开发进展周报

### 其他

### G-086 ZYF176数据分析

- **链接**：https://roborock.feishu.cn/wiki/J6Gmw7UujideOGkNdzKcgpnvnBe
- **首次提及**：融合组开发进展周报

### G-087 AI在SLAM工作中用法分享

- **链接**：https://roborock.feishu.cn/wiki/Hq0yw4wKsiQpxEkDY7BcaZKfnkg
- **首次提及**：融合组开发进展周报

### G-088 3dgs在 ubuntu20 配置手册

- **链接**：https://roborock.feishu.cn/wiki/FSS1wfJFHiJ4J6kmBgycA0SSnQg
- **首次提及**：融合组开发进展周报

### G-089 Slam和3dgs调研

- **链接**：https://roborock.feishu.cn/wiki/OoJ1wp5I9iQF2Mk0QS2cZqiknVf
- **首次提及**：融合组开发进展周报

### G-090 近期 BUG 汇总

- **链接**：https://roborock.feishu.cn/wiki/IXDFwP2A1iz8NWkjTNEcoPqen4c
- **首次提及**：融合组开发进展周报

### G-091 0311-0313测试

- **链接**：https://roborock.feishu.cn/wiki/SLiVwJeROiQgmfkPUUMc80gCnqh
- **首次提及**：融合组开发进展周报

### G-092 GAIA三种rtk模式

- **链接**：https://roborock.feishu.cn/wiki/UC6gwUFbPiydrZkbBlwcoSX9nQg
- **首次提及**：融合组开发进展周报

### G-093 扫描式多线lidar与camera标定调研总结

- **链接**：https://roborock.feishu.cn/wiki/Lhiow9AuvitpeVkU9sSc5cPenNb
- **首次提及**：融合组开发进展周报

### G-094 BUG 470958

- **链接**：https://roborock.feishu.cn/wiki/E6SLwFNKtiJl6ckqAAMcfiwynHd
- **首次提及**：融合组开发进展周报

### G-095 versa轨迹平滑

- **链接**：https://roborock.feishu.cn/wiki/KM4AwgojtiJbnckAJmscFBbrnt8
- **首次提及**：融合组开发进展周报

### G-096 融合组开发进展（2025-07-24\~2026-02-05）

- **链接**：https://roborock.feishu.cn/wiki/A6zLweX7Ri92tPk5RwNcXPbhniR
- **首次提及**：融合组开发进展周报

### G-097 观测延迟更新对融合输出位姿的影响

- **链接**：https://roborock.feishu.cn/wiki/BJwEw7838ilyspkv3Meci8dSnge
- **首次提及**：融合组开发进展周报

### G-098 rtk降频对融合定位的影响

- **链接**：https://roborock.feishu.cn/wiki/AG7ywC3tNiwN6wk6vxucD2renoh
- **首次提及**：融合组开发进展周报

### G-099 BUG #468220、#464633 复现分析

- **链接**：https://roborock.feishu.cn/wiki/JxCGwK9hSivrbkku5Uvcx3WjnGc
- **首次提及**：融合组开发进展周报

### G-100 RTK单点解精度分析

- **链接**：https://roborock.feishu.cn/wiki/SMPSwqeyViHux8k8ENlcseKangf
- **首次提及**：融合组开发进展周报

### G-101 BUG # 461208 存档

- **链接**：https://roborock.feishu.cn/wiki/ACC9wYv0ViqAXSk7ponc1xslnsd
- **首次提及**：融合组开发进展周报

### G-102 Versa放羊统计

- **链接**：https://roborock.feishu.cn/wiki/OAzkwoNdWi5IwXkrqmecp7lxnWh
- **首次提及**：融合组开发进展周报

### G-103 B2极限机激光SLAM测试评估报告

- **链接**：https://roborock.feishu.cn/wiki/MtSKwRgfliTropktkfMcWvmlnDd
- **首次提及**：融合组开发进展周报

### G-104 rtk添加fix\_pro和real\_time时间字段

- **链接**：https://roborock.feishu.cn/wiki/HFZdwI8tMi3sJFkfvsIcIjG3nKg
- **首次提及**：融合组开发进展周报

### G-105 Rtk新版本测试需求

- **链接**：https://roborock.feishu.cn/wiki/TBSzwydhei9XmhkLBK7cEn7vngc
- **首次提及**：融合组开发进展周报

### G-106 自研rtk同步跟进

- **链接**：https://roborock.feishu.cn/wiki/Hx3qwD24RisSOJkRLnDcq3rfnLb
- **首次提及**：融合组开发进展周报

### G-107 10.18自研rtk测试结果

- **链接**：https://roborock.feishu.cn/wiki/J10Gw2ONkisf2ykBj2CcuO2Znwg
- **首次提及**：融合组开发进展周报

### G-108 EDL shader 原理&amp;调研

- **链接**：https://roborock.feishu.cn/wiki/ZhtAwVlkhiiWuWkku8NcOPHXncc
- **首次提及**：融合组开发进展周报

### G-109 【机器人为操作，融合位姿变化】测试

- **链接**：https://roborock.feishu.cn/wiki/EA0NwnIfNiHjfdkCgUpcF8VKnPb
- **首次提及**：融合组开发进展周报

### G-110 RTK初始对准

- **链接**：https://roborock.feishu.cn/wiki/RoGmwgrU7ipJoRkB3JdcPbn9nlb
- **首次提及**：融合组开发进展周报

### G-111 odoparser测试优化

- **链接**：https://roborock.feishu.cn/wiki/HhuxwAhczinga1kuoZAcYw6jnDb
- **首次提及**：融合组开发进展周报

### G-112 四驱里程计问题分析

- **链接**：https://roborock.feishu.cn/wiki/IceQwZeQoiKcFBkikAFcugjFnuD
- **首次提及**：融合组开发进展周报

### G-113 四驱里程计正运动学模型推导

- **链接**：https://roborock.feishu.cn/wiki/AU8OwiBBriiN7dkOXEoc6dOZnEb
- **首次提及**：融合组开发进展周报

### G-114 滤波器更新问题分析

- **链接**：https://roborock.feishu.cn/wiki/NxqcwHX6ki2pqWkzBMhcp0x6nAd
- **首次提及**：融合组开发进展周报

### G-115 在线标定算法测试

- **链接**：https://roborock.feishu.cn/wiki/OIxFwQ0Y4iNr3kk1cwnc9SmCnNd
- **首次提及**：融合组开发进展周报

### G-116 火焰图分析

- **链接**：https://roborock.feishu.cn/wiki/WXeCwlfqDiYOhXkFQrpc8irknld
- **首次提及**：融合组开发进展周报

### G-117 ~~ bug418893~~

- **链接**：https://roborock.feishu.cn/wiki/Velewr8zhiqPqvk0rIKcg6DAnSd
- **首次提及**：融合组开发进展周报

### G-118 ~~ Gyro bias测试~~

- **链接**：https://roborock.feishu.cn/wiki/S8wPwBjL0iMdcnk6dylcY4pbn3f
- **首次提及**：融合组开发进展周报

### G-119 滤波器更新分析11-11

- **链接**：https://roborock.feishu.cn/wiki/DrHxw3PVriLaaSkb0vFcEoaknGd
- **首次提及**：融合组开发进展周报

### G-120 Rework

- **链接**：https://roborock.feishu.cn/wiki/XurXwkmUeiIrNEkUJm5cq9mSndc
- **首次提及**：融合组开发进展周报

### G-121 rtk\_添加更多信息

- **链接**：https://roborock.feishu.cn/wiki/Oldjw8Alei6KNDktsC5cQOlKnEf
- **首次提及**：融合组开发进展周报

### G-122 整机基站打分对比测试结果

- **链接**：https://roborock.feishu.cn/wiki/DFQBwgmXoijZXMkMtdAc8s35nSf
- **首次提及**：融合组开发进展周报

### G-123 四驱里程计验证(二)

- **链接**：https://roborock.feishu.cn/wiki/FAdXw5f0QiwLQLkXKvscIFHRn7v
- **首次提及**：融合组开发进展周报

### G-124 IQC交接文档

- **链接**：https://roborock.feishu.cn/wiki/B6NowREM3icgb5kubcbcHipHnwb
- **首次提及**：融合组开发进展周报

### G-125 本周处理过的融合 BUG 一览

- **链接**：https://roborock.feishu.cn/wiki/UMz1w333Gi9mRokuunYcJtQ3nBd
- **首次提及**：融合组开发进展周报

### G-126 融合速度处理

- **链接**：https://roborock.feishu.cn/wiki/KEoFwWra7i0L9FkoOMHcVCTpn1e
- **首次提及**：融合组开发进展周报

### G-127 视觉激光融合 -- 标定问题检测 & 系统性能评估

- **链接**：https://roborock.feishu.cn/wiki/AdQfwaK01isPYzkPkGjcfc9Mnkd
- **首次提及**：融合组开发进展周报

### G-128 融合位置跳变 & 机器行为异常分析

- **链接**：https://roborock.feishu.cn/wiki/HtrmwtOMtis6wPkUYlJcxogOnjc
- **首次提及**：融合组开发进展周报

### G-129 Versa项目视觉激光数据转换成rosbag形式

- **链接**：https://roborock.feishu.cn/wiki/MXREwmcHBi3gqWkPhfrcJzFwnJf
- **首次提及**：融合组开发进展周报

### G-130 上/下桩策略（持续更新中）

- **链接**：https://roborock.feishu.cn/wiki/AmWfwXiOMi8H8Gkv67QcmeIXnEb
- **首次提及**：融合组开发进展周报

### G-131 视觉激光融合方案初版方案分析

- **链接**：https://roborock.feishu.cn/wiki/BmuPwJTNDixHJekSK7scnXDQnId
- **首次提及**：融合组开发进展周报

### G-132 视觉-激光融合方案 V1.0

- **链接**：https://roborock.feishu.cn/wiki/WpXFwUNt1iiC4gkyV6JckUqLnOd
- **首次提及**：融合组开发进展周报

### G-133 LVI-SAM 算法流程&融合原理&方案分析

- **链接**：https://roborock.feishu.cn/wiki/LBZdwybOfiOiZsk82bhcyBKDn3g
- **首次提及**：融合组开发进展周报

### G-134 导航-slam重定位接口

- **链接**：https://roborock.feishu.cn/wiki/WIv4wDCv7i9yBMkxH2ecJadEnEb
- **首次提及**：融合组开发进展周报

