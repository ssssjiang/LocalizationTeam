# Flora项目AiryLite新SDK采集需求 

# 1. 机器

一种lidar可以认为是同一个机器；只对lidar有要求；不能走的话，遥控录制数据即可，机器无需自动走；

# 2. 试采集要求：

1. 前提： 需要驱动同事更新新的sdk; 中间层适配好点云保存（遮挡点统一保存);

2. 试采集：采集一组数据，要求在地面行驶约5分钟，轨迹任意环路，录制激光数据及对应的激光 IMU 数据。

&#x20;采集完成后，请将数据发送给  进验证。验证通过后，可上导轨开始正式采集。



# 3. 基础建图，采集需求：



**数据采集要求：**

* 围绕 60、78、105 三个场地外围，遥控进行数据采集；（每个场景正反方向沿边各走一圈，共6组数据）

* 采集过程中需录制激光数据及激光 IMU 数据；

* **数据**和对应日志，以 “器件-场地号” 形式命名文件夹进行保存发送给&#x20;



# 4. 3500平空旷场地：

**数据采集要求：**

* 转弯的时候速度不要太快

* 采集过程中需录制激光数据及激光 IMU 数据；

* **数据**和对应日志，以 “器件-场地号” 形式命名文件夹进行保存发送给

|      |                                                            |                                                                                                                                                           |
| ---- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 建图需求 | 在场地边界进行一次遥控绕圈采集；                                           | ![Image Token: V3jlbxfseoh513x3MHCcoxFIn1i](images/V3jlbxfseoh513x3MHCcoxFIn1i.png)                                                                   正常  |
| 建图需求 | 在场地中间区域进行 10×10 米的小圈采集，并完成一次遥控绕圈；                          | ![Image Token: DMm2bzmkjocydVxO7HNcYABIn7e](images/DMm2bzmkjocydVxO7HNcYABIn7e.png)                                                                    正常 |
| 定位需求 | 在场地中间区域进行约 30×30 米范围的稀疏写字采集。&#xA;一组横纵都走下吧（井字），尽量多些就行；&#xA; | ![Image Token: KO3ObGyDModuFFxzcS6cIqi1nNg](images/KO3ObGyDModuFFxzcS6cIqi1nNg.png)                                                                    正常 |

#

# 5. 特殊场地&#x20;



采集方法：从距离5m左右位置遥控过来，穿过以下区域，能走环路包围的尽量环路；不能环路的穿过即可；

| 场景描述                             | 场景图片                                                                                 |        结果                                                                                     |   |   |   |
| -------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- | - | - | - |
|  &#xA;大面积水边（泳池或湖边）（105别墅）        | ![Image Token: IHHRbIs76oTDoLxlS0Dc5Hfgnuh](images/IHHRbIs76oTDoLxlS0Dc5Hfgnuh.png)  | ![Image Token: Ye0vbNwGtopIxHx9kClcFo4fnzh](images/Ye0vbNwGtopIxHx9kClcFo4fnzh.png)        正常 |   |   |   |
|                                  |                                                                                      |                                                                                               |   |   |   |
| 单边墙 （篱笆）（105别墅）                  | ![Image Token: LVogbt1WQoBHRNxSfBocPTJBnYg](images/LVogbt1WQoBHRNxSfBocPTJBnYg.png)  | ![Image Token: Q5xMbNm3Po9ooDxsMUUcHVnnnzA](images/Q5xMbNm3Po9ooDxsMUUcHVnnnzA.png)        正常 |   |   |   |
|                                  |                                                                                      |                                                                                               |   |   |   |
| 单边墙 （围墙 带树林）（105别墅）              | ![Image Token: ShaxbwHEgo6h6Gxk1AZcL9ZlnCh](images/ShaxbwHEgo6h6Gxk1AZcL9ZlnCh.jpeg) | ![Image Token: DEMLbhHvfoULfaxunbWcxIGwnic](images/DEMLbhHvfoULfaxunbWcxIGwnic.png)        正常 |   |   |   |
|                                  |                                                                                      |                                                                                               |   |   |   |
|  L型角落（一面墙，一面灌木）（105别墅）           | ![Image Token: D5zHbRK7joITUkx8qpRc2iWFnBf](images/D5zHbRK7joITUkx8qpRc2iWFnBf.jpeg) | ![Image Token: WqNob4BFboQxXUxN43JcGVX6nzh](images/WqNob4BFboQxXUxN43JcGVX6nzh.png)        正常 |   |   |   |
|                                  |                                                                                      |                                                                                               |   |   |   |
| 窄通道（双面竹林）（78别墅）                  | ![Image Token: LrsnbP6ewos91ZxoPTjcFW3kncb](images/LrsnbP6ewos91ZxoPTjcFW3kncb.jpeg) | ![Image Token: LAmybJXSHocqM7xzegdcYWcVn3g](images/LAmybJXSHocqM7xzegdcYWcVn3g.png)        正常 |   |   |   |
|                                  |                                                                                      |                                                                                               |   |   |   |
| 窄通道（双面墙）（78别墅）几个双面墙，单词遥控采集，都穿过即可 | ![Image Token: XstnbbjZCoBEiPxV4M9cdZvOnXF](images/XstnbbjZCoBEiPxV4M9cdZvOnXF.jpeg) |                                                                                               |   |   |   |
| （金字塔上下，几个面都走下）&#xA;坡上（105 栋）     | ![Image Token: VADRbKsLYoj02uxdbQwcJLzzn9c](images/VADRbKsLYoj02uxdbQwcJLzzn9c.png)  |                                                                                               |   |   |   |
| 高反（78 栋）                         | ![Image Token: YxYnbceV6oWZQLxJDqtc6PxynQd](images/YxYnbceV6oWZQLxJDqtc6PxynQd.png)  |                                                                                               |   |   |   |
| 使用 pet 材料搭建的阳光房（60 栋）            | ![Image Token: BpK1bMWAXo5sqBx7wFucAsxYn3b](images/BpK1bMWAXo5sqBx7wFucAsxYn3b.jpeg) |                                                                                               |   |   |   |
| 木栅栏 （105 栋）                      | ![Image Token: O2a1bYDLhoDwjhxGdqgcLqbGnSb](images/O2a1bYDLhoDwjhxGdqgcLqbGnSb.jpeg) |                                                                                               |   |   |   |
| 石头矮墙（60 栋）                       | ![Image Token: WbSSbebFYoyyJjxdtzGcgZuZnOb](images/WbSSbebFYoyyJjxdtzGcgZuZnOb.png)  |                                                                                               |   |   |   |
| 颠簸路面（60 栋）                       | ![Image Token: XDDubAAK6o0qOsxGhlmcp7VgnUe](images/XDDubAAK6o0qOsxGhlmcp7VgnUe.jpeg) |                                                                                               |   |   |   |
| 河边绿色栅栏（60栋）                      | ![Image Token: GYBybaxSYo9oosxkH77cbzQEn5c](images/GYBybaxSYo9oosxkH77cbzQEn5c.png)  |                                                                                               |   |   |   |
| 室内场景 （尽量空旷且面积大一点）                | 沿边走一圈然后走一个稀疏弓字                                                                       |                                                                                               |   |   |   |















#



# 6. 参考文献

1. [ 带雷达罩遮挡风险分析（4mm雷达罩）](https://roborock.feishu.cn/wiki/EiXEwRleMi4HnLkahZQcAbPhnWf)

2. [ Ariy lite不同尺寸保护罩FOV影响](https://roborock.feishu.cn/wiki/JIJDwXYM3iTFZKkZfqQclJKonKg)

3. [ Airy Lite树叶拖点过滤优化测试](https://robosense.feishu.cn/wiki/P6PJwEGd0iOIhWkJoOpcSRpAn1c)





