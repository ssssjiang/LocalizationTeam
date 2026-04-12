# 地面点对slam影响实验

# 1. 结论：

基于当前测试场景下具有显著结构特征的数据分析表明，在去除地面点前后SLAM轨迹表现存在明显差异。通过对比实验可观察到以下现象：

（1）Z轴方向轨迹出现明显跳变现象；

（2）Z轴方向产生约20-50cm的漂移误差。

实验结果表明，地面点的去除会显著影响SLAM系统在高度方向的定位精度，导致Z轴轨迹稳定性下降，漂移误差增大。

| 传感器类型    | [Velodyne VLP-16](https://ouster.com/products/hardware/vlp-16) （最近扫描点距离车体水平距离2.5m）(bag时长：380s) （场景大小： 140 \* 70） | mid360（最近地面扫描点距离车体水平距离5.0m）(bag时长：122s)                                             |
| -------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 带地面点建图结果 | ![Image Token: J32Bb15EAoXQ30xZ39kcEKJknNb](images/J32Bb15EAoXQ30xZ39kcEKJknNb.png)                              | ![Image Token: OlUSb8RJGoWmBmx70nqcjUARnEg](images/OlUSb8RJGoWmBmx70nqcjUARnEg.png) |
| 无地面点建图结果 | ![Image Token: F7AUbXmcKoZ9tbxn2kjcVFKQnPg](images/F7AUbXmcKoZ9tbxn2kjcVFKQnPg.png)                              | ![Image Token: Jz5dbBTTjo1WU4xenJVccpBCn9c](images/Jz5dbBTTjo1WU4xenJVccpBCn9c.png) |
| 轨迹变化图：   | ![Image Token: K4SzbLpCEo3WxnxUYcwcf6cWnng](images/K4SzbLpCEo3WxnxUYcwcf6cWnng.png)                              | ![Image Token: UzyKbELB9oXakSxBklNcgfGRnpd](images/UzyKbELB9oXakSxBklNcgfGRnpd.png) |







# 2. 仰角和0度激光高度关系；



## 2.1 7度

打地高度变化，x轴距离，y轴高度：

![Image Token: Nl2GbUgSXopJakxtn9AcbpiNnU1](images/Nl2GbUgSXopJakxtn9AcbpiNnU1.png)

## 2.2 5度

![Image Token: GvEnbg0jzoJhZfx7m7cc7lJMnig](images/GvEnbg0jzoJhZfx7m7cc7lJMnig.png)



## 2.3 3度

![Image Token: Vq3KbvUyboKeqyxxXiUcFtginPb](images/Vq3KbvUyboKeqyxxXiUcFtginPb.png)





&#x20;Distance d (m)  Height h = d \* tan(7°) (m)

&#x20;             0                       0.000

&#x20;             3                       0.368

&#x20;             6                       0.737

&#x20;             9                       1.105

&#x20;            12                       1.473

&#x20;            15                       1.842

&#x20;            18                       2.210

&#x20;            21                       2.578

&#x20;            24                       2.947

&#x20;            27                       3.315





&#x20;Distance d (m)  Height h = d \* tan(5°) (m)

&#x20;             0                       0.000

&#x20;             3                       0.262

&#x20;             6                       0.525

&#x20;             9                       0.787

&#x20;            12                       1.050

&#x20;            15                       1.312

&#x20;            18                       1.575

&#x20;            21                       1.837

&#x20;            24                       2.100

&#x20;            27                       2.362





&#x20;Distance d (m)  Height h = d \* tan(3°) (m)

&#x20;             0                       0.000

&#x20;             3                       0.157

&#x20;             6                       0.314

&#x20;             9                       0.472

&#x20;            12                       0.629

&#x20;            15                       0.786

&#x20;            18                       0.943

&#x20;            21                       1.101

&#x20;            24                       1.258

&#x20;            27                       1.415



# 3. 基于角度过滤地面点的开源数据分析：

从对比结果可以看出，随着地面点数量减少，定位高度、Roll和Pitch角均发生显著变化。当地面点经过过滤（剔除Pitch角小于-13°的数据）后，定位结果趋于稳定。测试数据集中，机器高度为0.7m；按比例换算至0.35m高度时，机器人理论倾斜角度应约为-7°。



通过角度过滤地面点效果如下表，定位轨迹如下：

| 过滤的pitch角度    | -8 / -10 /-12 / -13 /-30                                                            | -1.5 / -3.5 /-5                                                                     |
| ------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 平移            | ![Image Token: SQo9bCc1Pon73axp6blcEO18n6d](images/SQo9bCc1Pon73axp6blcEO18n6d.png) | ![Image Token: A4Jebjd4uo4gzHxV4mbctV69neh](images/A4Jebjd4uo4gzHxV4mbctV69neh.png) |
| 姿态            | ![Image Token: OeY1bFReJox7cNx1GSFchfNcnUe](images/OeY1bFReJox7cNx1GSFchfNcnUe.png) | ![Image Token: SxUBbdoy3ooSduxmgVkcigoan9g](images/SxUBbdoy3ooSduxmgVkcigoan9g.png) |
| 存在完全过滤后算法跑飞现象 |                                                                                     |                                                                                     |

| 角度值（°） | 单帧效果                                                                                |
| ------ | ----------------------------------------------------------------------------------- |
| 正常     | ![Image Token: MJL8bflPSo5NEIxpggwck1D1n6f](images/MJL8bflPSo5NEIxpggwck1D1n6f.png) |
| -13    | ![Image Token: RDzYbtzR7omVAQxZfJ8cNJMOnf4](images/RDzYbtzR7omVAQxZfJ8cNJMOnf4.png) |
| -12    | ![Image Token: SxnTbm01hoAywDxyJnncHizBnob](images/SxnTbm01hoAywDxyJnncHizBnob.png) |
| -10    | ![Image Token: AaQlbkU0Sosw3cxFGVmcXAL3nYf](images/AaQlbkU0Sosw3cxFGVmcXAL3nYf.png) |
| -8     | ![Image Token: KCX5bf2k1ojca3xfoP2cfN9Snke](images/KCX5bf2k1ojca3xfoP2cfN9Snke.png) |
| -5     | ![Image Token: Ko34bRSvtoeEZWxVDu6c9lLTnNf](images/Ko34bRSvtoeEZWxVDu6c9lLTnNf.png) |
| -3.5   | ![Image Token: KR9obkjlVoxaLnxXqPJcsBZhnpd](images/KR9obkjlVoxaLnxXqPJcsBZhnpd.png) |
| -1.5   | ![Image Token: EsFibyX6UoRQ5jxPMbqc9e1Snhf](images/EsFibyX6UoRQ5jxPMbqc9e1Snhf.png) |











