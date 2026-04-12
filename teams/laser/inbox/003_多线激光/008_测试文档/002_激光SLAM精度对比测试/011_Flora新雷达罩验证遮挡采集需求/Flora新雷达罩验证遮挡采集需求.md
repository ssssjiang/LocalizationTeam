# Flora新雷达罩验证遮挡采集需求

# 1. 机器

一种lidar可以认为是同一个机器；只对lidar有要求；不能走的话，遥控录制数据即可，机器无需自动走；

# 2. 试采集要求：

采集一组数据，要求在地面行驶约10分钟，轨迹任意环路，录制激光数据及对应的激光 IMU 数据。

&#x20;采集完成后，请将数据发送给  进验证。验证通过后，可上导轨开始正式采集。



# 3. 基础建图采集，需求：



**数据采集要求：**

* 围绕 60、105 三个场地外围，遥控进行数据采集；

* 采集过程中需录制激光数据及激光 IMU 数据；

* **数据**和对应日志，以 “器件-场地号” 形式命名文件夹进行保存发送给&#x20;



# 4. 基础定位3500平空旷场地，建图定位需求：

**数据采集要求：**

* 转弯的时候速度不要太快

* 采集过程中需录制激光数据及激光 IMU 数据；

* **数据**和对应日志，以 “器件-场地号” 形式命名文件夹进行保存发送给





|      |                                                            |       |   |
| ---- | ---------------------------------------------------------- | ----- | - |
| 建图需求 | 在场地边界进行一次遥控绕圈采集；                                           |       |   |
| 建图需求 | 在场地中间区域进行 10×10 米的小圈采集，并完成一次遥控绕圈；                          |       |   |
| 定位需求 | 在场地中间区域进行约 30×30 米范围的稀疏写字采集。&#xA;一组横纵都走下吧（井字），尽量多些就行；&#xA; | ~~ ~~ |   |

# 5. 极端空旷场景


上面4 的场景去掉围栏后再采集一组（以便更好的看出究竟能接收的“空旷程度”是多少）

![Image Token: HgZsb17iyoCRIPx8NYecJ2cqnPc](images/HgZsb17iyoCRIPx8NYecJ2cqnPc.png)









# 6. 结果：





|                          |                                                                                                                         |    |                                                                                                                                                                                 | 4mm                                                                                                                                                                                | 4mm                              | 4mm                                                                                          | 4mm                                                                                            |   | 5.2mm                                                                                                                     | 5.2mm                                                                                                                                                                                                                                                                                                                     |   |   |   |   |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | - | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | - | - | - | - |
| 测试机 + 版本                 | 测试要求                                                                                                                    |    |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              | 时间同步重采数据后的结果                                                                                   |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
| MK1 + 上层（0083）+ 驱动（0089） | **78外轮廓**                                                                                                               |    | 数据不可用                                                                                                                                                                           |                                                                                                                                                                                    | 遮挡范围不大，可接受，建图点云无明显异常（除了树冠处有点云拖影） |                                                                                              | ![Image Token: JI5qbXBKOol8QKxmPH2cTnJanjh](images/JI5qbXBKOol8QKxmPH2cTnJanjh.png)            |   | ![Image Token: OKqBbEeAGotmZrxGx5ycuAdpnZB](images/OKqBbEeAGotmZrxGx5ycuAdpnZB.png)地图和轨迹无明显异常                             | 抖动和拖影：减少                                                                                                                                                                                                                                                                                                                  |   |   |   |   |
| MK1 + 上层（0083）+ 驱动（0089） | **105外轮廓**                                                                                                              |    | ![Image Token: ABDKbqN05o3oJixfSZscDWRSnRb](images/ABDKbqN05o3oJixfSZscDWRSnRb.png)定位正常                                                                                         | ![Image Token: HtH2b1PmXoMIsJxNCvzcnbafnRf](images/HtH2b1PmXoMIsJxNCvzcnbafnRf.png)![Image Token: AfMTbibWgoRFNWxJEP0c7QdVnoe](images/AfMTbibWgoRFNWxJEP0c7QdVnoe.png)建图过程和结果无明显异常 |                                  | ![Image Token: P2Xbb78J2oMRzwxfcYacVwJHnlh](images/P2Xbb78J2oMRzwxfcYacVwJHnlh.png)看不出明显遮挡区域 | ![Image Token: U6J7bmGc4oOxtUx4bxFcyzmZnNd](images/U6J7bmGc4oOxtUx4bxFcyzmZnNd.png)    建图效果可接受 |   | 数据异常，Bin11和Bin12数据不完整（有的文件在解析前为空，如如下图）![Image Token: Qw4zbp4exoIMxoxqpUecEuY4nDg](images/Qw4zbp4exoIMxoxqpUecEuY4nDg.png) |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
| MK1 + 上层（0083）+ 驱动（0089） | **3500平空旷场地搭建围栏**1. 在场地边界进行一次遥控绕圈采集；2. 在场地中间区域进行10×10米的小圈采集，并完成一次遥控绕圈；3. 在场地中间区域进行约30×30米范围的稀疏写字采集。一组横纵都走下吧（井字），尽量多些就行； |    |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              |                                                                                                |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         | 1  | ![Image Token: VrCxbpp6WoFSAWxK2Pfcg1Tfnfc](images/VrCxbpp6WoFSAWxK2Pfcg1Tfnfc.png)建图点云无明显异常                                                                                    | ![Image Token: AYhkbKxRgooddMxI0PocEF9SnOf](images/AYhkbKxRgooddMxI0PocEF9SnOf.png)                                                                                                |                                  |                                                                                              | ![Image Token: DkhMbgnssoXR2wxXxRncJfZGnhd](images/DkhMbgnssoXR2wxXxRncJfZGnhd.png)            |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         | 2  | ![Image Token: DaxDbewVVoKZUNx8nfGcQ2Eanmc](images/DaxDbewVVoKZUNx8nfGcQ2Eanmc.png)![Image Token: DcndbM82hoHJudxeznPcXgVCnMh](images/DcndbM82hoHJudxeznPcXgVCnMh.png)建图点云无明显异常 | ![Image Token: RVAMbEqVcozK3axmPkyc6PZfn9S](images/RVAMbEqVcozK3axmPkyc6PZfn9S.png)![Image Token: InmvbWfFHo6oHfxyeHxcMVshn3f](images/InmvbWfFHo6oHfxyeHxcMVshn3f.png)             |                                  |                                                                                              | ![Image Token: ZW7WbCBipoO0LxxRpOccusCdndd](images/ZW7WbCBipoO0LxxRpOccusCdndd.png)            |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         | 3  | ![Image Token: JhSebWADaof264xoxQtccztsn1c](images/JhSebWADaof264xoxQtccztsn1c.png)建图点云无明显异常                                                                                    | ![Image Token: Z6NhbbwkJourw0xmD6scqvYqnzh](images/Z6NhbbwkJourw0xmD6scqvYqnzh.png)                                                                                                |                                  |                                                                                              | ![Image Token: G0OnbsZFIoyoc4xxgf7cSQBXn9g](images/G0OnbsZFIoyoc4xxgf7cSQBXn9g.png)使用最新code运行  |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         |    |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              |                                                                                                |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
| MK1 + 上层（0083）+ 驱动（0089） | **极限空旷场地去掉搭建的围栏**1. 在场地边界进行一次遥控绕圈采集；2. 在场地中间区域进行10×10米的小圈采集，并完成一次遥控绕圈；3. 在场地中间区域进行约30×30米范围的稀疏写字采集。一组横纵都走下吧（井字），尽量多些就行； |    |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              | 时间同步后点云更清晰                                                                                     |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         | 1  | ![Image Token: K5Blb4ZLoopENuxYTZsc4LFunZg](images/K5Blb4ZLoopENuxYTZsc4LFunZg.png)                                                                                             |                                                                                                                                                                                    |                                  |                                                                                              | ![Image Token: ERp0b7Vl9omX13xfczAcZrAnndf](images/ERp0b7Vl9omX13xfczAcZrAnndf.png)            |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         | 2  | ![Image Token: UjdkblF67o8B3bxQ1apc264Fn7e](images/UjdkblF67o8B3bxQ1apc264Fn7e.png)                                                                                             |                                                                                                                                                                                    |                                  |                                                                                              | ![Image Token: DgB1bVGFioG76kxY5kwcUurLnkg](images/DgB1bVGFioG76kxY5kwcUurLnkg.png)            |   | ![Image Token: Q2hUbPnyYo3vexx29ELcqXRAn2e](images/Q2hUbPnyYo3vexx29ELcqXRAn2e.png)                                       | 无异常现象                                                                                                                                                                                                                                                                                                                     |   |   |   |   |
|                          |                                                                                                                         | 3  | 数据源本身有问题，没做时间同步                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              | ![Image Token: Ln1fb5jYwom3epxKKT4cO7q6ncb](images/Ln1fb5jYwom3epxKKT4cO7q6ncb.png)使用最新code运行  |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
|                          |                                                                                                                         |    |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              |                                                                                                |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |
| MK1 + 上层（0083）+ 驱动（0089） | 直轨、圆轨测试定位稳定性                                                                                                            |    |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              |                                                                                                |   | ![Image Token: ZAlNbGsIwoV5WTxOmDAcoLjWnJe](images/ZAlNbGsIwoV5WTxOmDAcoLjWnJe.png)                                       | ![Image Token: GpFxbpnLeoGXHjxwJlYcITGHnDd](images/GpFxbpnLeoGXHjxwJlYcITGHnDd.png)【拟合方法】：ransac拟合圆心   : (0.036, 1.982)拟合半径   : 1.951 m平均残差   : 0.00448 m标准差(σ)  : 0.00635 m最大正残差 : 0.02791 m最大负残差 : -0.01903 m2σ区间: \[-0.00917, 0.00870] m, 半宽=0.00894 m3σ区间: \[-0.01486, 0.02686] m, 半宽=0.02086 m内点数量   : 20457 / 20457 |   |   |   |   |
|                          |                                                                                                                         | 圆轨 |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              |                                                                                                |   | ![Image Token: UHqDbj07ZovdHkxrVggcDvN0nGd](images/UHqDbj07ZovdHkxrVggcDvN0nGd.png)                                       | ![Image Token: RYZvb44CYot0rFxjKi1c5qlpnzc](images/RYZvb44CYot0rFxjKi1c5qlpnzc.png)拟合结果：y = 0.0173 \* x + -0.0201RANSAC 内点比例: 98.79%剔除外点数量: 233 / 19271平均误差: 0.010705最大误差: 0.045554最小误差: -0.042125标准差 : 0.013841±2σ 区间: \[-0.023207, 0.024932] 精度为 0.024069±3σ 区间: \[-0.038567, 0.040774] 精度为 0.039670                    |   |   |   |   |
|                          |                                                                                                                         | 直轨 |                                                                                                                                                                                 |                                                                                                                                                                                    |                                  |                                                                                              |                                                                                                |   |                                                                                                                           |                                                                                                                                                                                                                                                                                                                           |   |   |   |   |







# 7. 结论：

遮挡对建图定位不严重，可接受：

1. 建图测试，无明显异常；

2. 远近遮挡不一样，对定位影响有限；

   1. 远近缺点角度，参考tpm评估：

   ![Image Token: HAFmbPIUkoI43JxYq8tcWEcqn5g](images/HAFmbPIUkoI43JxYq8tcWEcqn5g.png)

   * 累计点云情况：

     单个柱子，单帧会有收发，两个缺口；

     多帧拼接，缺点较少；

   ![Image Token: Eh83b0SIZomacLx6Nm3cF7gmnwf](images/Eh83b0SIZomacLx6Nm3cF7gmnwf.jpeg)

   4mm



   ![Image Token: N7WXbcdEmorWA2xtPW7cEBaMn6m](images/N7WXbcdEmorWA2xtPW7cEBaMn6m.png)

   5.2mm       预估，有效遮挡角度： 18.9\*3 = 56.7度；接近versa机器的54度遮挡了；大致能接受





   # 8. 参考文献

   1. [ 带雷达罩遮挡风险分析（4mm雷达罩）](https://roborock.feishu.cn/wiki/EiXEwRleMi4HnLkahZQcAbPhnWf)

   2. [ Ariy lite不同尺寸保护罩FOV影响](https://roborock.feishu.cn/wiki/JIJDwXYM3iTFZKkZfqQclJKonKg)





