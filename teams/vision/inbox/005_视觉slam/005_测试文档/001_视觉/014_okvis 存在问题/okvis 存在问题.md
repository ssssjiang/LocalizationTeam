# okvis 存在问题

# 1. 外在表现

## 1.1 帧率

![Image Token: FjZZbbZWLoFdkyxZbl6cP2jUnaf](images/FjZZbbZWLoFdkyxZbl6cP2jUnaf.png)

![Image Token: RYa8b86AIoitDWxvmdScP5wLntg](images/RYa8b86AIoitDWxvmdScP5wLntg.png)

1. 帧率由后端决定，前端可改等待为输出匹配位姿，但精度无提升

2. X5批测，200-400-200的package间隔，比300-300-300间隔 APE要更低，精度更高

3. **进展：后端锁核后，真实割草场景帧率可达到7Hz**

## 1.2 位姿左右跳动（局部小突起）



![Image Token: LosCbzGMkoDVl4xRfsEcEp5mnBd](images/LosCbzGMkoDVl4xRfsEcEp5mnBd.png)

1. 角度估计偏差（继续分析gyro漂移）左为Twi，右为Twr

![Image Token: SF9GbOxU1oC1FAxlFx2clJaDnqf](images/SF9GbOxU1oC1FAxlFx2clJaDnqf.png)

![Image Token: PVJobgCqrodeqJx5S1ycUQnRnJc](images/PVJobgCqrodeqJx5S1ycUQnRnJc.png)

* **进展：切换为后端输出位姿后，跳动明显变小**

## 1.3 转弯时画圈（换算到Twb位姿）



![Image Token: TaqObT8EzolAPLxvZq0cpY01ntg](images/TaqObT8EzolAPLxvZq0cpY01ntg.png)

1. 从图中观察大约5cm波动

2. 怀疑imu平移外参不准确（标定轨迹缺少画圈等动作），MK2-12，IMU外参无明显偏差

![Image Token: Ixyibs2QloRgqwxHipOcwPrpnvb](images/Ixyibs2QloRgqwxHipOcwPrpnvb.png)

* 继续怀疑场景导致位姿估计误差大（待复测数据，分析表现）

* **进展：偶现问题，近期未发现，后续复现再处理**

## 1.4 弓字间隔大/小（可通过全局图避免累积）

![Image Token: VTiabRX63osmTdxXI35crtGwnUd](images/VTiabRX63osmTdxXI35crtGwnUd.png)

![Image Token: I7TNbwvFNoED4GxVBP5ca6hZnzb](images/I7TNbwvFNoED4GxVBP5ca6hZnzb.png)

1. 按宋姝的测试结果来看，关闭odo+开启在线标定会变好（待批测）

![Image Token: D6rEb7BcBonr65xaIfYcu5XqnEb](images/D6rEb7BcBonr65xaIfYcu5XqnEb.png)

## 1.5 **转弯角度估计误差大**



![Image Token: HYngbv5XHoCK6vxvHUXche5Xnlc](images/HYngbv5XHoCK6vxvHUXche5Xnlc.png)

1. [ okvis转弯角度估计误差大](https://roborock.feishu.cn/docx/YL1ZdmSR2oUFyrxJs8Jc5102nzd)

2. 000687.20250816054739647\_R0005X52700110\_2025081503DEV\_vio\_state\_line

   ![Image Token: K76ZbnwjEoWskdx6YkOcSGz2nDg](images/K76ZbnwjEoWskdx6YkOcSGz2nDg.png)

3. definition\_limit\_corrected\_B1-092\_corrected

   * 离树太近了，无稳定远处约束

   * 10\15Hz容易复现， 5Hz不复现

   * use\_only\_main\_camera: true 效果明显变好，且不再卡顿（卡顿是因为后端耗时明显增大）

     ![Image Token: Rw80b2iTVo1GIpxizAMc3HaZnmf](images/Rw80b2iTVo1GIpxizAMc3HaZnmf.png)



   ![Image Token: LHtQb77ZaoOilkxAoxxcXi7cnSd](images/LHtQb77ZaoOilkxAoxxcXi7cnSd.png)

4. **进展：bg权重问题，调整后已解决**

## 1.6 \*Z轴累积漂移问题



![Image Token: FJrMbt93VopSnjxlqYwceuSynlb](images/FJrMbt93VopSnjxlqYwceuSynlb.png)

1. 与轨迹长度相关，B1机器 10\*8场地可逐渐漂移到3米，MK2-12可到2米，怀疑与外参的pitch角误差相关

   1. 1度偏差，10米距离，对应漂移17cm，10个来回即可达到3.4米

2. 可依靠全局图定位约束偏差

## 1.7 轮速计打滑场景误差大

1. 同slope

2. 需要结合打滑检测，减弱打滑的影响

3. **进展：打滑检测效果提升明显**

## 1.8 \*slope场景误差大



![Image Token: JpuEb9xlSo5j7mxwo71cYe3wnzb](images/JpuEb9xlSo5j7mxwo71cYe3wnzb.png)

![Image Token: WkapbssIXox4kwxgTPMc41dbnrb](images/WkapbssIXox4kwxgTPMc41dbnrb.png)

1. 之前有一版已解决该问题，待进一步分析为何复现（sigma\_v不一致）

![Image Token: SrSDbLHiMopUSvxselpcilMBnIf](images/SrSDbLHiMopUSvxselpcilMBnIf.png)

## 1.9 位姿跑飞

1. [ vslam LOST 判断](https://roborock.feishu.cn/docx/SAvRdGD5rocbzkxBnLMc637pnoc)

2. **进展：已增加异常场景防护，待积累更多可稳定复现跑飞的数据**

## 1.10 后端单次耗时异常大

1. 会导致后续优化跑飞，通过在前端加图像GAP检测来workaround

2. **进展：系统资源问题，后端锁核后近期未复现**

![Image Token: ONobb9kAyoeEKlxlxztcpfMInac](images/ONobb9kAyoeEKlxlxztcpfMInac.png)

## 1.11 \* kf间距过短，尝试通过调整间距，拓宽滑窗范围，提升精度

## 1.12 \* 可视化时有大的重投影误差，应该是对精度有影响

1. 一般是未初始化点，坐标异常。

![Image Token: OnmxbEH2moSAXcxbCX8cMmtXnIr](images/OnmxbEH2moSAXcxbCX8cMmtXnIr.png)

![Image Token: AWwnb72eqoYt3ExR29ncCfm1nOg](images/AWwnb72eqoYt3ExR29ncCfm1nOg.png)

## 1.13 \*  okvis里面的前端、后端trick是否兼容割草机场景的分析

# 2. 算法逻辑

## 2.1 地面草地点观测差

1. 静止时草地点可匹配成功

2. 草地特征点周围环境相似度高

## 2.2 后端异常耗时尖峰

1. 问题规模

   ![Image Token: JueTbAOzfoZYNpxBWRXcBNTKnrd](images/JueTbAOzfoZYNpxBWRXcBNTKnrd.png)

2. 异常处理

   ![Image Token: TFMObkHbjohu4zxc2kkcMramn83](images/TFMObkHbjohu4zxc2kkcMramn83.png)

   ![Image Token: JrTkb6sVio8juAxHgQ3cJPBCn7u](images/JrTkb6sVio8juAxHgQ3cJPBCn7u.png)



## 2.3 强依赖后端优化出的Vw、Ba

1. 需要增加异常防护

# 3. 其他

## 3.1 Replay && X5仿真

[ 端侧仿真/replay模式](https://roborock.feishu.cn/docx/WlvedpzYEo2MUfxlS0IcuXiqnzb)

## 3.2 导航转弯速度

1. 45-60度/秒的旋转速度符合设计

## 3.3 \*Bug

1. 后端realtime中KF队列始终有固定的一个历史帧（第一帧）

