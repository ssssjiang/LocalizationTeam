# p2动态rtk对比测试

# 1. 简介：

&#x20;  本报主要对 和芯 和 司南 两家做出动态对比测试。

&#x20;  声明：

&#x20;       1由于五合一无法使用功分器来保证两家gnss收到的信号完全一致，但在测试点位，计算方法和测试时长等细节都保证做到一致。

&#x20;       2 由于无法得到真值，在计算误差项的时候用到了高斯牛顿优化来拟合直线和圆，所有误差也会包含轨道布置的时候，直线不够直和圆形轨道不够圆等轨迹变形问题（计算当做理想直线和理想圆，但是实际轨道精度有误差），但是可以反应情况。

&#x20;        &#x20;

&#x20; 主要分两种测试，

&#x20; 1 移动站在直线导轨上，采集移动站数据，基站两家放在相同的并且理想的环境。

&#x20; 2 移动站在圆形导轨上，采集移动站数据，基站两家放在相同的并且理想的环境。

&#x20;&#x20;



本报告所有图标，横坐标表示十个点位，深蓝色为和芯数据，浅蓝色为司南数据。



# 2. 测试结果：

## 2.1 直线动态：

* 和芯在**平均误差，cep50，标准差，max** 这些重要指标强于司南。司南在搜星数，HDOP差分龄期和固定解率都强于司南

* 司南在双面墙环境，表现较差

## 2.2 圆形动态： &#x20;

* 司南在**平均误差，cep50，标准差**，HDOP，固定解率，搜星数目和差分龄期强于和芯，和芯在**最大值**方面略强于司南

* 司南在点位1（环境最恶劣）表现较差，差分龄期过大



# 1直线动态

原始数据统计

[ p2直线rtk对比测试](https://roborock.feishu.cn/sheets/OH8BsxEmkhb0yttHCjDcZ3YnnIZ?from=from_copylink)

误差统计方式：所有点集拟合出一条直线，然后每个点到直线的距离作为当前点的误差。

测试时长：每一个速度测试半小时。

| 场景id | 场景图                                                                                  | 说明   | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | ---- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位1  | ![Image Token: CfffbZZu4oy5rVxmLBTcBB6inkd](images/CfffbZZu4oy5rVxmLBTcBB6inkd.jpeg) | 理想环境 | 0.1     | 和芯 | ![Image Token: W7LubuKLXo88K5xf4eycoXE7nMr](images/W7LubuKLXo88K5xf4eycoXE7nMr.png) | ![Image Token: GwvcbMyY8oQbTUxvSvmclVuynnO](images/GwvcbMyY8oQbTUxvSvmclVuynnO.png) |
|      |                                                                                      |      |         | 司南 | ![Image Token: EF6QbnzwcoMJ0FxuNbFcGNNwnYf](images/EF6QbnzwcoMJ0FxuNbFcGNNwnYf.png) |                                                                                     |
|      |                                                                                      |      | 0.5     | 和芯 | ![Image Token: RP0bbZ6evoDbCUxMQn0cA3sqnKg](images/RP0bbZ6evoDbCUxMQn0cA3sqnKg.png) |                                                                                     |
|      |                                                                                      |      |         | 司南 | ![Image Token: BY8nbkLWpocil9xQ5xdcMEg1nwb](images/BY8nbkLWpocil9xQ5xdcMEg1nwb.png) |                                                                                     |
|      |                                                                                      |      | 1       | 和芯 | ![Image Token: IbLbbRGyEoHnIPx7OJQceILZnHe](images/IbLbbRGyEoHnIPx7OJQceILZnHe.png) |                                                                                     |
|      |                                                                                      |      |         | 司南 | ![Image Token: XqllbWLqUoKTdrxfofFchGAmnFb](images/XqllbWLqUoKTdrxfofFchGAmnFb.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明  | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | --- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位2  | ![Image Token: O6IGbdIx4o2R1PxxJwtcVGIZn5d](images/O6IGbdIx4o2R1PxxJwtcVGIZn5d.jpeg) | 双面墙 | 0.1     | 和芯 | ![Image Token: O6GhbllfCof4dCxVbvNcr3pZnCc](images/O6GhbllfCof4dCxVbvNcr3pZnCc.png) | ![Image Token: ZSdDbmGA8obAh4xorTAc2PNTnrh](images/ZSdDbmGA8obAh4xorTAc2PNTnrh.png) |
|      |                                                                                      |     |         | 司南 | ![Image Token: Pr95bOR5AoeF3ixv6R6cDl2PnFc](images/Pr95bOR5AoeF3ixv6R6cDl2PnFc.png) |                                                                                     |
|      |                                                                                      |     | 0.5     | 和芯 | ![Image Token: S9SjbCW8fogrEAxu4wIchbWcndf](images/S9SjbCW8fogrEAxu4wIchbWcndf.png) |                                                                                     |
|      |                                                                                      |     |         | 司南 | ![Image Token: Xu5NbDPVPox5Jhxl6qDcLlVAnDh](images/Xu5NbDPVPox5Jhxl6qDcLlVAnDh.png) |                                                                                     |
|      |                                                                                      |     | 1       | 和芯 | ![Image Token: E03Sb1IHKo6JiPx4GOgcHFePnyc](images/E03Sb1IHKo6JiPx4GOgcHFePnyc.png) |                                                                                     |
|      |                                                                                      |     |         | 司南 | ![Image Token: OrXfbSuedoZfa4xRaNDcgCvmnoe](images/OrXfbSuedoZfa4xRaNDcgCvmnoe.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明  | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | --- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位3  | ![Image Token: JWf7bx5LJorMarxOwXVcivXunBb](images/JWf7bx5LJorMarxOwXVcivXunBb.jpeg) | 密林下 | 0.1     | 和芯 | ![Image Token: N5cXbe9dSoDCIhx1Mf7cFgcPnmd](images/N5cXbe9dSoDCIhx1Mf7cFgcPnmd.png) | ![Image Token: KPgBb0J7HoKgsJxu4JWcHcSQnSc](images/KPgBb0J7HoKgsJxu4JWcHcSQnSc.png) |
|      |                                                                                      |     |         | 司南 | ![Image Token: N21lbLzQUoRcoAxRtY4cLXtgnQf](images/N21lbLzQUoRcoAxRtY4cLXtgnQf.png) |                                                                                     |
|      |                                                                                      |     | 0.5     | 和芯 | ![Image Token: PL5VbV4TpoeCFfxbfrGcMUuxnXd](images/PL5VbV4TpoeCFfxbfrGcMUuxnXd.png) |                                                                                     |
|      |                                                                                      |     |         | 司南 | ![Image Token: RZO8bKSEwoxHZaxTHnZcV8NtnVO](images/RZO8bKSEwoxHZaxTHnZcV8NtnVO.png) |                                                                                     |
|      |                                                                                      |     | 1       | 和芯 | ![Image Token: XeVAbD2nyoxy0qxoTLQcvc4OnQW](images/XeVAbD2nyoxy0qxoTLQcvc4OnQW.png) |                                                                                     |
|      |                                                                                      |     |         | 司南 | ![Image Token: EI0Jbc91XoDNBaxWimEcddaynnc](images/EI0Jbc91XoDNBaxWimEcddaynnc.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明     | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | ------ | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位4  | ![Image Token: VQgGbL9Q2ob7BWxLyrCc1qbsnCf](images/VQgGbL9Q2ob7BWxLyrCc1qbsnCf.jpeg) | 单面墙+篱笆 | 0.1     | 和芯 | ![Image Token: WrewbrlgxohC33xMBsMcHY6AnIf](images/WrewbrlgxohC33xMBsMcHY6AnIf.png) | ![Image Token: Xel3bhZgaoWfYhxE5r0ccD1Ynxd](images/Xel3bhZgaoWfYhxE5r0ccD1Ynxd.png) |
|      |                                                                                      |        |         | 司南 | ![Image Token: DKMGb9jpioh52Axek0bcT0XDnNf](images/DKMGb9jpioh52Axek0bcT0XDnNf.png) |                                                                                     |
|      |                                                                                      |        | 0.5     | 和芯 | ![Image Token: TvKmbvh0Xo0A3gx3i8rcQVL0nYd](images/TvKmbvh0Xo0A3gx3i8rcQVL0nYd.png) |                                                                                     |
|      |                                                                                      |        |         | 司南 | ![Image Token: D11bb8crKopNglxskf1cZvgjnXf](images/D11bb8crKopNglxskf1cZvgjnXf.png) |                                                                                     |
|      |                                                                                      |        | 1       | 和芯 | ![Image Token: QN1Qbw2OBoZjXoxTrP2cTLkqnCd](images/QN1Qbw2OBoZjXoxTrP2cTLkqnCd.png) |                                                                                     |
|      |                                                                                      |        |         | 司南 | ![Image Token: TsMabbrAVoPzLSxXU9xcHTYQnKg](images/TsMabbrAVoPzLSxXU9xcHTYQnKg.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明        | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | --------- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位5  | ![Image Token: GHyQbFGGno65iRxdTPlcxGHYnlf](images/GHyQbFGGno65iRxdTPlcxGHYnlf.jpeg) | 建筑物 车库铁门边 | 0.1     | 和芯 | ![Image Token: Mr4DbmI7YoIgoqxEOlVcnkuRnSg](images/Mr4DbmI7YoIgoqxEOlVcnkuRnSg.png) | ![Image Token: Bg9zbetvpoy8S0xFjdxcEy1Ungg](images/Bg9zbetvpoy8S0xFjdxcEy1Ungg.png) |
|      |                                                                                      |           |         | 司南 | ![Image Token: BPsAbxfgDoWr7Ex4Bl6cUWMYn7f](images/BPsAbxfgDoWr7Ex4Bl6cUWMYn7f.png) |                                                                                     |
|      |                                                                                      |           | 0.5     | 和芯 | ![Image Token: On7DbO2xAogzv1xVicacDu4qn1u](images/On7DbO2xAogzv1xVicacDu4qn1u.png) |                                                                                     |
|      |                                                                                      |           |         | 司南 | ![Image Token: Tdftbi4tIoD1hBxSkoMcG5f9nNe](images/Tdftbi4tIoD1hBxSkoMcG5f9nNe.png) |                                                                                     |
|      |                                                                                      |           | 1       | 和芯 | ![Image Token: UELcbSihZomVzVxltN0c6iYLn8e](images/UELcbSihZomVzVxltN0c6iYLn8e.png) |                                                                                     |
|      |                                                                                      |           |         | 司南 | ![Image Token: MuSKb6BVUoAOFNxcaD4cK6IWnPe](images/MuSKb6BVUoAOFNxcaD4cK6IWnPe.png) |                                                                                     |





1 平均误差作为最重要的指标，和芯强于司南，在点位2（双面墙） 和点位4（单面墙）的低速差场景的情况下，和芯的表现更好，但是在点位4的高速表现不如司南，其他点位和芯也略强。

2 固定解率，司南略强于和芯，但是在点位2（双面墙）的位置，司南表现很差，

3 误差标准差，和芯强于司南。

4 cep50 和max值 ，双方都互有优劣，和芯略强于司南

&#x20;5 搜星数来看，司南大部分点位比和芯多

6 差分龄期 司南强于和芯，但是在差环境下，表现突破5秒，不可接受。这可能也是司南这个点位表现差的原因。

7  水平精度因子，司南表现强于和芯。

# 2圆形动态

&#x20;原始数据统计

[ p2圆形rtk](https://roborock.feishu.cn/sheets/FebKslk6OhcgRNtLK6wcSStYnOU?from=from_copylink)

&#x20;误差统计方式：所有点的集合拟合成一个圆，当前点到圆形的距离和圆半径的差，作为当前点的误差。

&#x20;测试时长：每一个速度测试半小时。

&#x20;&#x20;

| 场景id | 场景图                                                                                  | 说明           | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | ------------ | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位1  | ![Image Token: LxP1b5j3uosGUbxzSGncJOdAn4d](images/LxP1b5j3uosGUbxzSGncJOdAn4d.jpeg) | 最难的场景类 L l角落 | 0.1     | 和芯 | ![Image Token: MNHRbLZb1okd5axVm2acWJngnfh](images/MNHRbLZb1okd5axVm2acWJngnfh.png) | ![Image Token: EH1dbX9fNorSidxEpPUcHXxsnHg](images/EH1dbX9fNorSidxEpPUcHXxsnHg.png) |
|      |                                                                                      |              |         | 司南 | ![Image Token: NTo5bn3x5os4HMxbK5XcUxb2n8d](images/NTo5bn3x5os4HMxbK5XcUxb2n8d.png) |                                                                                     |
|      |                                                                                      |              | 0.5     | 和芯 | ![Image Token: QKbxbe42eozTrCxOIGbcrJv3nUe](images/QKbxbe42eozTrCxOIGbcrJv3nUe.png) |                                                                                     |
|      |                                                                                      |              |         | 司南 | ![Image Token: AFe4b7OfLo3A23xFENDccK3Dnge](images/AFe4b7OfLo3A23xFENDccK3Dnge.png) |                                                                                     |
|      |                                                                                      |              | 1       | 和芯 | ![Image Token: QBQ5bTNfvoeIuzxbY0PcEslUnmd](images/QBQ5bTNfvoeIuzxbY0PcEslUnmd.png) |                                                                                     |
|      |                                                                                      |              |         | 司南 | ![Image Token: Yyo8btAvWookK7xJdmpcIHisnCc](images/Yyo8btAvWookK7xJdmpcIHisnCc.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明        | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | --------- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位2  | ![Image Token: H7PBbHA1Vo4jvnxD4hGcv8xEnkg](images/H7PBbHA1Vo4jvnxD4hGcv8xEnkg.jpeg) | 一面墙，另一面竹林 | 0.1     | 和芯 | ![Image Token: IPYPbcVGQobhGNxcCDIcOpNlnid](images/IPYPbcVGQobhGNxcCDIcOpNlnid.png) | ![Image Token: Xfzfb0JGLo94dJxJ8wOcl9b8njh](images/Xfzfb0JGLo94dJxJ8wOcl9b8njh.png) |
|      |                                                                                      |           |         | 司南 | ![Image Token: EMzNb1UNToh8LNx5eY4cidilnEe](images/EMzNb1UNToh8LNx5eY4cidilnEe.png) |                                                                                     |
|      |                                                                                      |           | 0.5     | 和芯 | ![Image Token: XSATb3VxsonRDAxBeH6clpwYnWd](images/XSATb3VxsonRDAxBeH6clpwYnWd.png) |                                                                                     |
|      |                                                                                      |           |         | 司南 | ![Image Token: NDtlbK2TioT2eCx4KhEcGkQNngg](images/NDtlbK2TioT2eCx4KhEcGkQNngg.png) |                                                                                     |
|      |                                                                                      |           | 1       | 和芯 | ![Image Token: YpL2bgmBio0p7lxHFCAcIFJEnNh](images/YpL2bgmBio0p7lxHFCAcIFJEnNh.png) |                                                                                     |
|      |                                                                                      |           |         | 司南 | ![Image Token: GlKUb1Cu7oAmhvxv1Hjcfq5anwc](images/GlKUb1Cu7oAmhvxv1Hjcfq5anwc.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明   | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | ---- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位3  | ![Image Token: JfH0bV6Eno7QMVx5b0zcfyVZnng](images/JfH0bV6Eno7QMVx5b0zcfyVZnng.jpeg) | 理想环境 | 0.1     | 和芯 | ![Image Token: YrsLb51lCoHyCGxsESZcgunWnob](images/YrsLb51lCoHyCGxsESZcgunWnob.png) | ![Image Token: FjPsb7iBTowfLwx2b3XcyzO0nib](images/FjPsb7iBTowfLwx2b3XcyzO0nib.png) |
|      |                                                                                      |      |         | 司南 | ![Image Token: VgtEbvrLTovvJzxTdtNcJ5KOnfh](images/VgtEbvrLTovvJzxTdtNcJ5KOnfh.png) |                                                                                     |
|      |                                                                                      |      | 0.5     | 和芯 | ![Image Token: EHXBbLcdWo6652xYySlcRvvOnUb](images/EHXBbLcdWo6652xYySlcRvvOnUb.png) |                                                                                     |
|      |                                                                                      |      |         | 司南 | ![Image Token: UQVSbebDTo8hpAxfig0cPY4dnqb](images/UQVSbebDTo8hpAxfig0cPY4dnqb.png) |                                                                                     |
|      |                                                                                      |      | 1       | 和芯 | ![Image Token: H4JPb5uhAoY3Rax0luAcEndDn4d](images/H4JPb5uhAoY3Rax0luAcEndDn4d.png) |                                                                                     |
|      |                                                                                      |      |         | 司南 | ![Image Token: HCBJbILa8ojGtlxUKpPcn6AQn3J](images/HCBJbILa8ojGtlxUKpPcn6AQn3J.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明    | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | ----- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位4  | ![Image Token: F6KLbFJOWoIf0oxb20TcCP73nMF](images/F6KLbFJOWoIf0oxb20TcCP73nMF.jpeg) | 高大树木下 | 0.1     | 和芯 | ![Image Token: XY3JbRlryoXkg0xjOq6cxC7Sn2c](images/XY3JbRlryoXkg0xjOq6cxC7Sn2c.png) | ![Image Token: Fyo6bx2DqoVDiMxneTkcVe3jn5e](images/Fyo6bx2DqoVDiMxneTkcVe3jn5e.png) |
|      |                                                                                      |       |         | 司南 | ![Image Token: AvJ2bqt2DoeVkbxJ8RwcFgMknaf](images/AvJ2bqt2DoeVkbxJ8RwcFgMknaf.png) |                                                                                     |
|      |                                                                                      |       | 0.5     | 和芯 | ![Image Token: JLAKbqadPodIqjxFyD5crBgMnmd](images/JLAKbqadPodIqjxFyD5crBgMnmd.png) |                                                                                     |
|      |                                                                                      |       |         | 司南 | ![Image Token: Fub4b5gIHoB1K7xNmHdcTApynjG](images/Fub4b5gIHoB1K7xNmHdcTApynjG.png) |                                                                                     |
|      |                                                                                      |       | 1       | 和芯 | ![Image Token: F55BbWLbnoKfqTx48rWc5dHzn0f](images/F55BbWLbnoKfqTx48rWc5dHzn0f.png) |                                                                                     |
|      |                                                                                      |       |         | 司南 | ![Image Token: EpbtbEWOZoAO4oxFeaWcaJ9Tnyb](images/EpbtbEWOZoAO4oxFeaWcaJ9Tnyb.png) |                                                                                     |

| 场景id | 场景图                                                                                  | 说明  | 速度（m/s） | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | --- | ------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 点位5  | ![Image Token: JEPibmt7NoURIrxBS55cp173nLc](images/JEPibmt7NoURIrxBS55cp173nLc.jpeg) | 密林下 | 0.1     | 和芯 | ![Image Token: NVRmboq9aoYKpXxUD7EcqRtvnGe](images/NVRmboq9aoYKpXxUD7EcqRtvnGe.png) | ![Image Token: VWHgbZ28uoXoAcxyg2gcGWuVnRg](images/VWHgbZ28uoXoAcxyg2gcGWuVnRg.png) |
|      |                                                                                      |     |         | 司南 | ![Image Token: Ufacb9h3HoyddcxR7Mxctdunnch](images/Ufacb9h3HoyddcxR7Mxctdunnch.png) |                                                                                     |
|      |                                                                                      |     | 0.5     | 和芯 | ![Image Token: RXiCbTUE7ou9MSx7EaYcSpONn7e](images/RXiCbTUE7ou9MSx7EaYcSpONn7e.png) |                                                                                     |
|      |                                                                                      |     |         | 司南 | ![Image Token: P9eJbxWdFoMDS5xttqlcsHbhn1f](images/P9eJbxWdFoMDS5xttqlcsHbhn1f.png) |                                                                                     |
|      |                                                                                      |     | 1       | 和芯 | ![Image Token: IBIFbRbsRoiVzkxldYkc9nrRnSB](images/IBIFbRbsRoiVzkxldYkc9nrRnSB.png) |                                                                                     |
|      |                                                                                      |     |         | 司南 | ![Image Token: HU6Hb5EzNoMjxOxbYGfc0NcknZd](images/HU6Hb5EzNoMjxOxbYGfc0NcknZd.png) |                                                                                     |



1 平均误差看起来 司南略强一点，但是和芯在最差的点位1的低速挡，表现很亮眼。

2 固定解率 司南略强于和芯

3 两家相差不大。司南整体略强一点，和芯在最差的点位一的最低挡，表现很好，



4 司南略好于和芯

&#x20;5 最大值，两家相差不大。两家都有几个表现不好的点位

6 司南的搜星数目比和芯略多。

&#x20;7 差分龄期，司南大部分好于和芯，但是在恶劣环境下，司南的lora貌似表现很差，超过5秒就是无法忍受的，

司南略好于和芯

