# Vslam 跑极线校正图像

# 1. 调内参

| 原图                   | ![Image Token: LoA1bnKfsok2WIxUrZGcyBBvn5c](images/LoA1bnKfsok2WIxUrZGcyBBvn5c.png) |
| -------------------- | ----------------------------------------------------------------------------------- |
| Dualcamra json校正     | ![Image Token: R2THbkzq1osmy4xoNVecvj9Anof](images/R2THbkzq1osmy4xoNVecvj9Anof.png) |
| 去畸变                  | ![Image Token: MUi2bVrY3oy0FjxUg29cqvwHnye](images/MUi2bVrY3oy0FjxUg29cqvwHnye.png) |
| 对Dualcamra json的P矩阵： | ![Image Token: DJ28bA2qRocIDrxKdhXcPDGjn3b](images/DJ28bA2qRocIDrxKdhXcPDGjn3b.png) |

# 2. 数据集

从benchmark结果，使用原图比校正图略好：

1. rmse略低

2. 平均Landmark track (strek mean) 略长

3. 平均Landmark观测次数 (lifetime mean) 略多

备注：FOV没有调到最大

| **sequence**                                    | **origin/rmse** | **rectify/rmse** | **statistic**                                                                       |
| ----------------------------------------------- | --------------- | ---------------- | ----------------------------------------------------------------------------------- |
| B1-37\_7.22\_105\_lake\_corrected               | 0.308612        | 0.537695         | ![Image Token: GCZrbGXsGojExmx01HuccqDkncf](images/GCZrbGXsGojExmx01HuccqDkncf.png) |
| B1-37\_7.22\_78\_lake\_corrected                | 0.303803        | 0.435623         | ![Image Token: OpJLbN4HaozbDRxlVKTcgbfDnwd](images/OpJLbN4HaozbDRxlVKTcgbfDnwd.png) |
| B1-037\_105\_forest\_400\_2\_new\_corrected     | 0.874523        | 0.592185         | ![Image Token: AhWtblOwMoOzXwx4o5tcIywTnDg](images/AhWtblOwMoOzXwx4o5tcIywTnDg.png) |
| MK2-12\_circle                                  | 0.233877        | 0.163025         | ![Image Token: POqUbz8cso7AApxYCuhcU67Fn4d](images/POqUbz8cso7AApxYCuhcU67Fn4d.png) |
| MK2-12\_lake2\_0.5m                             | 0.290658        | 0.210443         | ![Image Token: DhuzbfMTdoithfxIO37c4pDVnzh](images/DhuzbfMTdoithfxIO37c4pDVnzh.png) |
| MK2-12\_normal\_z\_0.5m                         | 0.209537        | 0.313094         | ![Image Token: CIzobnPJFoKuy5x3mRPcCeZ0nLh](images/CIzobnPJFoKuy5x3mRPcCeZ0nLh.png) |
| MK2-12\_normal\_z\_0.8m                         | 0.238728        | 0.107122         | ![Image Token: UvKjbYPGqo0WA2x9Id6ctSsknid](images/UvKjbYPGqo0WA2x9Id6ctSsknid.png) |
| MK2-12\_normal\_z\_0.8m2                        | 0.188587        | 0.186926         | ![Image Token: MEJKbVnVGo0H2AxAqpGcbWZ4nPf](images/MEJKbVnVGo0H2AxAqpGcbWZ4nPf.png) |
| MK2-12\_slip                                    | 0.093326        | 0.082981         | ![Image Token: XBUebdd4YosJ4BxEKxqcersWnFk](images/XBUebdd4YosJ4BxEKxqcersWnFk.png) |
| MK2-33\_78\_lake2\_sunshine                     | 0.311187        | 0.386802         | ![Image Token: NeB4boTeGoMEGvxwirdcAQ43ndq](images/NeB4boTeGoMEGvxwirdcAQ43ndq.png) |
| MK2-43\_105\_slope1\_10x8\_sunlight             | 0.488466        | 0.879922         | ![Image Token: HsUvbyVWbojRqOxc5gZc5blHnob](images/HsUvbyVWbojRqOxc5gZc5blHnob.png) |
| MK2-50\_78\_lake2\_sunlight                     | 0.312475        | 0.317633         | ![Image Token: HTVibMaRBow1LCx9gqpczxYQntf](images/HTVibMaRBow1LCx9gqpczxYQntf.png) |
| definition\_limit\_corrected\_B1-092\_corrected | 0.503735        | 0.311742         | ![Image Token: DmiDbWHfDoyakTxh4VUc4tIMnmc](images/DmiDbWHfDoyakTxh4VUc4tIMnmc.png) |
| definition\_limit\_corrected\_B1-138\_corrected | 0.283571        | 0.276899         | ![Image Token: YBnPb9I1pokHnDxl2tPcFCu2nxd](images/YBnPb9I1pokHnDxl2tPcFCu2nxd.png) |
| definition\_limit\_corrected\_B1-L2\_corrected  | 0.512727        | 0.824832         | ![Image Token: FIrhbOol3o2O9yxi8DjcGiiYnob](images/FIrhbOol3o2O9yxi8DjcGiiYnob.png) |
| ydiff\_corrected\_B1-138\_corrected             | 0.287569        | 0.418089         | ![Image Token: Fh80b9InuoAQtvx2hQUcJdRhnqc](images/Fh80b9InuoAQtvx2hQUcJdRhnqc.png) |
| ydiff\_corrected\_B1-L1\_corrected              | 0.424722        | 0.526897         | ![Image Token: SihgbW7XUowPc0xCMCUca9a5nfg](images/SihgbW7XUowPc0xCMCUca9a5nfg.png) |
| ydiff\_corrected\_B1-L2\_corrected              | 0.382975        | 0.550278         | ![Image Token: WSakbKckZoVZbNx5zUBcqIQJn1b](images/WSakbKckZoVZbNx5zUBcqIQJn1b.png) |
| MK2-12\_105\_forest\_400\_3                     | 3.719914        | 2.951379         | ![Image Token: PS4bbfEhEoTUvwxL1MocIdQgnyg](images/PS4bbfEhEoTUvwxL1MocIdQgnyg.png) |
| MK2-12\_105\_lake\_400\_2\_new                  | 1.201922        | 1.482288         | ![Image Token: FCPYbeOCfoasa6x8o52cZWAhnwd](images/FCPYbeOCfoasa6x8o52cZWAhnwd.png) |
| ~~MK2-12\_105\_pothelo\_400\_3~~                | ~~-~~           | ~~-~~            | ~~-~~                                                                               |





# 3. FOV影响分析与解决方案

现在看，stereo\_rectify的FOV损失太大了。并且不太好自动化地去调。

1. stereorectify

   * 通过调stereorectify的控制FOV的参数不是很合适再往大调y方向会有黑色区域。

   * 手工调投影矩阵的话没有批量自动化的能力。

2. undistort

   * 通过去畸变方式，能够有现成的方法，不过图像的局部缩放系数会有点大

3. 映射到DS或其他简单模型

   1. rt8 -> DS，图像预期将没有大量变化，并且可以从原始图像gdc映射过来，提升画面质量。

      1. 现在slam的1/2图其实就是用gdc转的，可以把转1/2图的那一路gdc改成这种映射不同相机模型的方式

![去畸变与极限校正的FOV变化 (Token: QJgSbEDdzovuBcxk1SNc4kNqnSe)](images/QJgSbEDdzovuBcxk1SNc4kNqnSe.jpeg)



![去畸变后图像的局部缩放率 (Token: MgnTbGGLUoI5nqxaEebcoNTinwc)](images/MgnTbGGLUoI5nqxaEebcoNTinwc.jpeg)
