# RTK假固定原始数据分析

目的：通过分析diffage、std\_e、std\_n、sats和假固定之间的关系，计算参数模型识别假固定



【第一步】找数据（人工）

| 数据                        | 轨迹                                                                                  |   |
| ------------------------- | ----------------------------------------------------------------------------------- | - |
| 屋檐下停留20s数据                | ![Image Token: DXLtbfW5VoUqmaxshdGcnoLCnad](images/DXLtbfW5VoUqmaxshdGcnoLCnad.png) |   |
| 弓字测试第二组                   | ![Image Token: V33NbWX2ioSVoRxleTjcBbTWnEh](images/V33NbWX2ioSVoRxleTjcBbTWnEh.png) |   |
| 弓字测试第一组                   | ![Image Token: R2YmbNGNiogSL0xQE0fciQgbnAc](images/R2YmbNGNiogSL0xQE0fciQgbnAc.png) |   |
| RTK固定解跳变bug(旧版本log，脚本不好使) | ![Image Token: Zocmb83ABoFgkZxv7sacSQ4zn5f](images/Zocmb83ABoFgkZxv7sacSQ4zn5f.png) |   |
| Bug: 387157               |                                                                                     |   |
| Bug: 377353               | ![Image Token: IaYGb22nso4KzFxpfDScASUenDh](images/IaYGb22nso4KzFxpfDScASUenDh.png) |   |



【第二步】提取数据（人工+脚本），保存到csv: &#x20;

1\) 使用**plotjuggler**根据rtk\_pose\_full.txt的轨迹，找出假固定的时间戳，存放到：data\_all.csv；

2\) 使用脚本(  ) 提取出AGRICA里面对应的数据，同一目录下；

3\) 根据时间戳对应关系，每一行增加：

| stdn | stde | stdu | diffage |
| ---- | ---- | ---- | ------- |



【第三步】简单分析数据（1036），找到阈值组合（人工+excel）

\*min(stde) = **0.0117**;&#x20;

![Image Token: H89IbvLASoDYLhxym9acYj3JnBb](images/H89IbvLASoDYLhxym9acYj3JnBb.png)

\*min(stdn) = **0.0098**;&#x20;

\*min(stdu) = **0.0288**;

\*max(diffage) = **6**;  min(diffage) = **0.8**;   # 无规律

\*sats～\[**8:37**];       # 无规律

![Image Token: BDuubriBAofOAHx9SKFclowEn4g](images/BDuubriBAofOAHx9SKFclowEn4g.png)









【第四步】**增加非假固定数据**（人工44279，☹**）**，分析数据（机器学习），找到最优阈值组合（准召率最优）

**1036/1 （假固定）    v.s.   44279/0（理论上99%真固定）  ：&#x20;**&#x20;

guess range (0.01-0.05 , 0.01-0.05 ~~, 5-40,  5.0-10.0~~)

Init guess (0.01, 0.01, ~~10, 5.0~~)

std分析：标签1样本同时大于双阈值的比例（红色热图），标签0样本同时小于双阈值的比例（蓝色热图）

![Image Token: WzzJbzZl5o2iI5xrZxEcfa6JnQc](images/WzzJbzZl5o2iI5xrZxEcfa6JnQc.png)

diffage分析：

![Image Token: JwowbJl81oW7bVxLCPpcE03CnTc](images/JwowbJl81oW7bVxLCPpcE03CnTc.png)

sats分析：

![Image Token: Mx4Fbd3dxouOIXxrjWQcoguunld](images/Mx4Fbd3dxouOIXxrjWQcoguunld.png)





**最低阈值0.01示例**如下表：

| 数据          | 轨迹                                                                                  | stde<=0.01 | stdn<=0.01 | total | 位置示例                                                                                                                                                                        |
| ----------- | ----------------------------------------------------------------------------------- | ---------- | ---------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7.22-78lake | ![Image Token: KYirbLIXCorGHYx9voScMtjSn1f](images/KYirbLIXCorGHYx9voScMtjSn1f.png) | 14289      | 14460      | 15636 | ![Image Token: KWYnbrH0ho3ofRxY6TocOuQwn75](images/KWYnbrH0ho3ofRxY6TocOuQwn75.png)                                                                                         |
| 105-forest  | ![Image Token: ZLaWbMm8NoIDkQx0g27cUdpFnLc](images/ZLaWbMm8NoIDkQx0g27cUdpFnLc.png) | 9769       | 9140       | 12578 | ![Image Token: YTPFbNJnZozyfAx9X8qcYJbmnge](images/YTPFbNJnZozyfAx9X8qcYJbmnge.png)删除尾巴：![Image Token: H52ubf8qIodd7Qx1w4icjPKdn2c](images/H52ubf8qIodd7Qx1w4icjPKdn2c.png) |
| 105-lake    | ![Image Token: MrgfbcgXDolOFSxEnQLc4eqznof](images/MrgfbcgXDolOFSxEnQLc4eqznof.png) | 15159      | 15203      | 16281 | ![Image Token: ARTybaTS9oL55cxRl1QcEpPdnUg](images/ARTybaTS9oL55cxRl1QcEpPdnUg.png)                                                                                         |
