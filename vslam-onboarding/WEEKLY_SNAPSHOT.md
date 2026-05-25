# WEEKLY_SNAPSHOT.md - 最新周报摘要

> 数据来源：PROGRESS_HISTORY.md（20260309~）
> 生成日期：2026-03-11

---

## 🎯 本周进展（20260309~）

### 割草机内外参标定与检测
- ✅ MCT行差标定，概率性优化失败问题解决（1天）
- ✅ 售后标定版本脚本输出（0.1天），PR 已提交

### OKVIS-VIO优化
- ✅ odo+gyro递推精度分析完成
- ✅ odo+gyro / VIO / VIO优化版 RMSE对比文档完成

### Okvis全局图与回环检测
- ✅ maplab复用okvis跟踪与landmark（链路3）
- ✅ Okvis score接入，已合入宋姝开发分支
- ✅ 窄通道建图：消息统计完成，导航发删除通道消息问题已解决
- ✅ 单目Mapping调优对比分析完成
- ✅ 在线建图规模缩减 + GTSAM 引入

### 深度学习特征点描述子引入
- ✅ superpoint初步精度优于brisk

---

## ⚠️ 关键待办项（Action）

### P0（本周/近期）

| 模块 | 任务 | 时间估算 | 状态 | 风险 |
|------|------|---------|------|------|
| 标定 | CQIQC代码重构，CR修改 | 0.5天 | 进行中 | - |
| 标定 | MCT双目外参标定联调测试 | - | 进行中 | Bug#459093 |
| 标定 | 售后标定时间缩短至5分钟 | 0.5天 | 自测完成 | 待测试验证 |
| VIO | 同一landmark被一帧观测多次bug | - | PR中 | - |
| VIO | B1-37_7.22_105_lake_corrected精度排查 | - | 进行中 | 困难场景 |
| 全局图 | 子图拼接精度较低排查 | - | 进行中 | 子图大小影响 |
| 全局图 | 重定位召回率低（<50%） | - | 调优中 | 核心问题 |

### P1（本季度）

| 模块 | 任务 | 备注 |
|------|------|------|
| VIO | 深度学习光流（LET-Net）接入okvis | 灰度图测试、批测 |
| VIO | 非弓字精度提升 | 参数调优有限 |
| 全局图 | PGO搬窗口逻辑接入 | 测试整体精度 |
| 全局图 | 回环检测输出给VIO搬窗口 | - |
| 标定 | 二驱标定重投影误差检测 | refine过滤大误差 |
| 其他 | 水下视觉SLAM（泳池机器人） | 图像质量分析完成 |

---

## 🚨 关键风险与问题

### 高优先级风险

1. **重定位召回率低**
   - 大部分数据 < 50%
   - 重定位轨迹精度低
   - 交叉重定位存在多个问题

2. **VIO精度问题**
   - B1-37_7.22_105_lake_corrected：精度变差，草地跟踪差、有效特征点太远
   - 非弓字割草误差大
   - 弓字间隔不均匀

3. **子图优化后精度变差**
   - 子图太小 → 精度低
   - 子图拼接精度较低

4. **标定问题**
   - PC与ARM编译后标定结果差异待排查
   - 模组供应商外参标定TOC误差大（Tci z轴偏大）

### 待验证假设

- odo+gyro递推 vs VIO vs VIO优化版：哪个精度最高？
- 单目 vs 双目建图：精度差异？
- 光流补跟踪对精度的影响：待批测验证

---

## 📊 关键指标

### VIO精度
- 上机压测RMSE约 **1.5%**
- 10m对齐效果最佳，进入评估脚本
- 10m对齐，20m评估

### 重定位
- 召回率：大部分 < 50%（目标：> 80%）
- 精度：低于离线版本VIO+地图观测

### 建图
- 在线建图引入GTSAM后耗时优化
- 单目建图精度低于双目

---

## 👥 关键联系人

| 领域 | 名字 | 角色 |
|------|------|------|
| 技术决策升级 | 李哲 | 定位组技术 leader |
| VIO 优化 | 郭科 | okvis 核心优化 |
| VIO 精度分析 / 售后标定 | 李宝玉 | 困难场景排查、融合预研、售后 |
| odo/仿真/水下 | 白世杰 | 工具链、水下SLAM |
| 全局图建图（在线 Maplab） | 宋姝 | 开发分支维护 |
| 重定位 | 肖鸿飞 | 加载地图重定位、假成功分析 |
| 全局图精度（子图/光流） | 刘博 | 子图优化分析 |
| DL 特征 + Okvis PGO | 陈飞 | superpoint 合入、PGO |
| Maplab PGO + CIIQC 站 | 江建文 | PGO 开发、标定产线 |
| 标定产线执行 | 邱冰冰 | CQIQC、MCT、售后标定 |
| CQIQC 站维护 / 重定位多帧 | 李波 | 产线维护、窄通道需求跟进 |
| 器件组（产线硬件） | 李圳 | MCT 行差问题硬件侧确认 |
| 感知组对接 | ❓ **待询问** | slam.archive、GDC NV12 |
| 导航组对接 | ❓ **待询问** | 窄通道消息接入 |
| PM | ❓ **待询问** | 项目进度、外部承诺截止时间 |

---

## 📁 关键文档入口

### 标定相关
- [CIIQC站维护工作](https://roborock.feishu.cn/wiki/CBdvwlM8xiFEcWkI9zqcIOIunyp)
- [售后标定治具缩小方案测试结果](https://roborock.feishu.cn/wiki/AuGgwEHtui3WZOkuMclcr0QHnBd)

### VIO相关
- [odo+gyro递推精度分析](https://roborock.feishu.cn/wiki/K2kQw2xk1igR9WkDdoQcyUVXnf9)
- [okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)
- [okvis非弓字精度提升](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb)
- [okvis+LET-Net深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

### 全局图相关
- [全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe)
- [Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe)
- [VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe)
- [reloc-self_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e)

### 其他
- [水下视觉slam相关工作](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)
- [泳池机器人okvis测试](https://roborock.feishu.cn/wiki/MF1ewBTbWiUeNUkOKlzcsyJGnEh)

---

## 🔄 下一步行动

### 本周（2026-03-11 ~ 2026-03-13）
- [ ] 确认接手全量清单（与前任对齐）
- [ ] 确认关键Action项的负责人和截止时间
- [ ] 补充专家地图中的具体姓名和联系方式

### 下周（2026-03-14 ~ 2026-03-18）
- [ ] 追踪P0待办项进展
- [ ] 评估重定位召回率低的风险等级
- [ ] 确认VIO精度问题的优先级

### 本月（2026-03-25前）
- [ ] 交接完成，建立自己的任务追踪系统
- [ ] 与PM对齐预期和交付项

---

_后续更新：每周同步周报，更新此摘要_
