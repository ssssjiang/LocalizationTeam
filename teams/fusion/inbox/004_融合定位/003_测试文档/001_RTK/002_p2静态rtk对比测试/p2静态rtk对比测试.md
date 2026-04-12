# p2静态rtk对比测试

# 1. 简介：

&#x20;  本报主要对 和芯 和 司南 两家做出静态对比测试。

&#x20;  声明：由于五合一无法使用功分器来保证两家gnss收到的信号完全一致，但在测试点位，计算方法和测试时长等细节都保证做到一致。

&#x20; 主要分两种测试，

&#x20;    （1）基站选择理想环境，分别测试移动站在不同层级的典型环境的打点情况。主要目的了解不同环境移动rtk的表现，同时对比两rtk厂家。

&#x20;    （2）移动站选择理想环境。分别放置基站在不同层级的典型环境，同时采集基站和移动站的报文，来了解不同场景基站的安装位置，对移动站rtk的影响，同时也对比两rtk厂家。



本报告所有图标，横坐标表示十个点位，深蓝色为和芯数据，浅蓝色为司南数据。



# 2. 测试结果：

## 2.1 移动站静态：

* 司南在信噪比和固定解率上强于和芯，和芯在搜星数、**cep50和max值**上强于司南。平均误差和误差的方差两家相近

* 司南在八号点位无法固定，差分龄期异常大（司南反馈：Lora没有跳频，可能是受环境干扰导致）

## 2.2 基站静态：

* 司南在差分龄期，平均误差，固定解率，**cep50和max**值上强于和芯。

* 但是司南基站在点位8的表现很差。



# 1 对移动站的测试

真值 ：所有点集的平均 x y 作为真值

测试时间：1小时

原始数据

[ p2静态测试](https://roborock.feishu.cn/wiki/W1REwcnmMiypBmk4JCxclay8nGe?from=from_copylink)

场景图以及简要信息

| 厂家id           | 场景图                                                                                  | 说明                    | 厂家 | 打点图                                                                                 | 星空图                                                                                 |
| -------------- | ------------------------------------------------------------------------------------ | --------------------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 场景1            | ![Image Token: FOIGbPp5voLyfSxvqlJc5ZLDndg](images/FOIGbPp5voLyfSxvqlJc5ZLDndg.jpeg) | 理想环境                  | 和芯 | ![Image Token: Oi7Nbih3PoINPWxsnkccp9GDnjc](images/Oi7Nbih3PoINPWxsnkccp9GDnjc.png) | ![Image Token: DB1ub8a82oUzgJxvaFBclyXwnbg](images/DB1ub8a82oUzgJxvaFBclyXwnbg.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: XFrzbWhtbonZS6xSliJcsDognld](images/XFrzbWhtbonZS6xSliJcsDognld.png) |                                                                                     |
| 场景2            | ![Image Token: I9FmbMqCloIvuQxJDFBcNmZKnnb](images/I9FmbMqCloIvuQxJDFBcNmZKnnb.jpeg) | 树林（105别墅）             | 和芯 | ![Image Token: KxE2bnGozo96dxx41q8cfmbZnHe](images/KxE2bnGozo96dxx41q8cfmbZnHe.png) | ![Image Token: UfBKbwYC8odk89x5g2lcQy3Nngf](images/UfBKbwYC8odk89x5g2lcQy3Nngf.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: DhsnbkEzoomwsHx7qtWcxj9an4g](images/DhsnbkEzoomwsHx7qtWcxj9an4g.png) |                                                                                     |
| 场景3            | ![Image Token: Xhxkb3EOioqilFxrMfFcRNCinTW](images/Xhxkb3EOioqilFxrMfFcRNCinTW.jpeg) | 大面积水边（泳池或湖边）（105别墅）   | 和芯 | ![Image Token: N688bUkJuopQhbx707rcyYoPnvh](images/N688bUkJuopQhbx707rcyYoPnvh.png) | ![Image Token: TVftbKYqIoj9n0xth7zcFP8sn6f](images/TVftbKYqIoj9n0xth7zcFP8sn6f.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: GIa3bjDMyofnNCxHC9wcQZUcnZd](images/GIa3bjDMyofnNCxHC9wcQZUcnZd.png) |                                                                                     |
| 场景4            | ![Image Token: NEArbJf7hoOea1xOQPzc4T3lnx5](images/NEArbJf7hoOea1xOQPzc4T3lnx5.jpeg) | 单边墙 （篱笆）（105别墅）       | 和芯 | ![Image Token: YZPpb9Jk1oKWu8xarHkcjCnHnKh](images/YZPpb9Jk1oKWu8xarHkcjCnHnKh.png) | ![Image Token: GeBlb1AnSoGokJxZOhBcOZW8nwe](images/GeBlb1AnSoGokJxZOhBcOZW8nwe.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: FVjSbTVqhoJ7XCxuGaVcquyznYb](images/FVjSbTVqhoJ7XCxuGaVcquyznYb.png) |                                                                                     |
| 场景5            | ![Image Token: UAtNbHi2moKd8Rx3nHWcEYbxn4f](images/UAtNbHi2moKd8Rx3nHWcEYbxn4f.png)  |  房檐 （78别墅）            | 和芯 | ![Image Token: LaiZb99pjoCmvsxzdVacHtvknDh](images/LaiZb99pjoCmvsxzdVacHtvknDh.png) | ![Image Token: SCPDb1Td3oii6Wx6Fe9cK87SnEb](images/SCPDb1Td3oii6Wx6Fe9cK87SnEb.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: ARhmbXmTsoumeTx8iBHch6gbnpd](images/ARhmbXmTsoumeTx8iBHch6gbnpd.png) |                                                                                     |
| 场景6            | ![Image Token: ZpShbJC2no9rA2xqB51cPNy5nDf](images/ZpShbJC2no9rA2xqB51cPNy5nDf.jpeg) | 单边墙  （围墙 带树林）（105别墅）  | 和芯 | ![Image Token: AKoybRwKQoMNuZxS0x8cIpREnFg](images/AKoybRwKQoMNuZxS0x8cIpREnFg.png) | ![Image Token: TJ4zb8TAxogLrKxNRppcZKalnMe](images/TJ4zb8TAxogLrKxNRppcZKalnMe.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: Wrxbbvmuzo9FkCxEG22cj904neu](images/Wrxbbvmuzo9FkCxEG22cj904neu.png) |                                                                                     |
| 场景7            | ![Image Token: UpeIbNsz4o0NIYxsIg8c1kennGd](images/UpeIbNsz4o0NIYxsIg8c1kennGd.jpeg) | L型角落（一面墙，一面灌木）（105别墅） | 和芯 | ![Image Token: TwXQbFpnookLOLxKafZcU1ZFnff](images/TwXQbFpnookLOLxKafZcU1ZFnff.png) | ![Image Token: NZTrbVktZo8DRjxaI3ucsJacnhc](images/NZTrbVktZo8DRjxaI3ucsJacnhc.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: CNaobioZZosMHSx76jtcM1lCn1d](images/CNaobioZZosMHSx76jtcM1lCn1d.png) |                                                                                     |
| 场景8（比例尺和其他不一致） | ![Image Token: IUYKbGlzio0i3ox0eVWcWJKbn8f](images/IUYKbGlzio0i3ox0eVWcWJKbn8f.jpeg) | L型角落 （两面墙）（5别墅）       | 和芯 | ![Image Token: Eu3wbVJH9ovcZex2wBgcpb82nyc](images/Eu3wbVJH9ovcZex2wBgcpb82nyc.png) | ![Image Token: S5YSbfucGo7ptkxDCePcH3LYnqe](images/S5YSbfucGo7ptkxDCePcH3LYnqe.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: TqC5bcED3ogKJfxKPnFcx1fsnce](images/TqC5bcED3ogKJfxKPnFcx1fsnce.png) |                                                                                     |
| 场景9            | ![Image Token: AqZ3buhXToafURxMGxdcvDzynzb](images/AqZ3buhXToafURxMGxdcvDzynzb.jpeg) | 窄通道（双面竹林）（78别墅）       | 和芯 | ![Image Token: IGDdb2ivyoizp1x5Wijc3p1VneI](images/IGDdb2ivyoizp1x5Wijc3p1VneI.png) | ![Image Token: KoWpbpckboGtw6xKu0zcq2oPnW9](images/KoWpbpckboGtw6xKu0zcq2oPnW9.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: QwEBbksCSoen6zx1lJQcFtIQn0c](images/QwEBbksCSoen6zx1lJQcFtIQn0c.png) |                                                                                     |
| 场景10           | ![Image Token: SHmCbzkczoymcuxuUMEcF7MGnOh](images/SHmCbzkczoymcuxuUMEcF7MGnOh.jpeg) | 窄通道（双面墙）（78别墅）        | 和芯 | ![Image Token: HWeybSfMkoiknwxs07ccYQoLnXd](images/HWeybSfMkoiknwxs07ccYQoLnXd.png) | ![Image Token: G2Svbgefvo4HJYxhYQscdpgbnLf](images/G2Svbgefvo4HJYxhYQscdpgbnLf.png) |
|                |                                                                                      |                       | 司南 | ![Image Token: WJhmb04UooMIy0xnqliclGqmnEf](images/WJhmb04UooMIy0xnqliclGqmnEf.png) |                                                                                     |



&#x20;1信噪比 ：司南的信噪比好于和芯的，

&#x20;

2平均误差 ：两家相差不大。

3 固定率：司南的固定率明显好于和芯的。但是在点位8（L型角），司南无法进入固定解。

4误差的方差：两家相差不大，和芯略微强于司南。

&#x20;

5搜星数目 ：和芯明显比司南的多。

6水平精度因子：和芯强于司南



7 cep50以及最大值：从这两点来看，和芯强于司南。



8差分龄期。差分龄期司南好于和芯，但是和芯都在正常范围内，司南的点位八貌似有问题，这也是这个点位司南表现差的原因。

# 2 对基站的测试

真值 ： 所有点集的平均 x y 作为真值

测试时间：1小时

原始数据

&#x20;[ p2基站理想环境数据](https://roborock.feishu.cn/wiki/QLbCwPR8yij018kyYfPcvgpznPr?from=from_copylink)&#x20;

场景图以及简要信息



| 厂家id | 场景图                                                                                  | 说明                    | 厂家 | 移动打点图                                                                               | 星空图                                                                                 |
| ---- | ------------------------------------------------------------------------------------ | --------------------- | -- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 场景1  | ![Image Token: Mi8lbzCokoQZNbxvW7Tc9m1inoX](images/Mi8lbzCokoQZNbxvW7Tc9m1inoX.jpeg) | 理想环境                  | 和芯 | ![Image Token: LY2XbCpTLodt3wxcNSDcd2G2nBd](images/LY2XbCpTLodt3wxcNSDcd2G2nBd.png) | ![Image Token: OtBybOxLuoC6NRxfiPZcyeSRnrf](images/OtBybOxLuoC6NRxfiPZcyeSRnrf.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: HKX5bsvz2o32MvxcD23cnc4Bn6c](images/HKX5bsvz2o32MvxcD23cnc4Bn6c.png) |                                                                                     |
| 场景2  | ![Image Token: QYwbbmNYmowNutxYK3CcI3wfnfd](images/QYwbbmNYmowNutxYK3CcI3wfnfd.jpeg) | 树林（105别墅）             | 和芯 | ![Image Token: AXU9bXgBgoAswWx89mWcnedKnvc](images/AXU9bXgBgoAswWx89mWcnedKnvc.png) | ![Image Token: TVBrbyRqFoA3Six33VecKVvJnDg](images/TVBrbyRqFoA3Six33VecKVvJnDg.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: LdWYbkZjyokU4dxRzLUc5BVvnuh](images/LdWYbkZjyokU4dxRzLUc5BVvnuh.png) |                                                                                     |
| 场景3  | ![Image Token: EmfabWvY3ovhTBxEGNpcDzEYnAb](images/EmfabWvY3ovhTBxEGNpcDzEYnAb.jpeg) | 大面积水边（泳池或湖边）（105别墅）   | 和芯 | ![Image Token: TaBobDlVLoPwZhxZRAAcCR4dnXc](images/TaBobDlVLoPwZhxZRAAcCR4dnXc.png) | ![Image Token: XFwrb516koVUkFxbzp8cm6dhncc](images/XFwrb516koVUkFxbzp8cm6dhncc.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: L4qIb43QWobDhUxcvQqcKvYynWb](images/L4qIb43QWobDhUxcvQqcKvYynWb.png) |                                                                                     |
| 场景4  | ![Image Token: MLIAbYjZpo9h0XxS6h6cIFqrnfk](images/MLIAbYjZpo9h0XxS6h6cIFqrnfk.jpeg) | 单边墙 （篱笆）（105别墅）       | 和芯 | ![Image Token: Uw1RbFnQHo6MN7xayMOcRhi5nTc](images/Uw1RbFnQHo6MN7xayMOcRhi5nTc.png) | ![Image Token: NCVNbwBLfoyfInxfupUcBfmwned](images/NCVNbwBLfoyfInxfupUcBfmwned.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: DYiubAOVKomYlTxWql1ctzJLn7e](images/DYiubAOVKomYlTxWql1ctzJLn7e.png) |                                                                                     |
| 场景5  | ![Image Token: DpOibN7HUoJbY9xpKmIcXQmSnRe](images/DpOibN7HUoJbY9xpKmIcXQmSnRe.jpeg) |  房檐 （78别墅）            | 和芯 | ![Image Token: CwbPbA3tMomZcuxyrrWcXNDvnZm](images/CwbPbA3tMomZcuxyrrWcXNDvnZm.png) | ![Image Token: MBBoboo6So6p8Kx0eI3cBqx5nSc](images/MBBoboo6So6p8Kx0eI3cBqx5nSc.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: Hnjlb5uzwoBt8IxJwEncpAO4nKb](images/Hnjlb5uzwoBt8IxJwEncpAO4nKb.png) |                                                                                     |
| 场景6  | ![Image Token: HP37b73bNoKL9fx31qkcOv7knrh](images/HP37b73bNoKL9fx31qkcOv7knrh.jpeg) | 单边墙  （围墙 带树林）（105别墅）  | 和芯 | ![Image Token: GrIxb4f3boM46Sx8C4icfV38nzc](images/GrIxb4f3boM46Sx8C4icfV38nzc.png) | ![Image Token: HeLwbMhtkoWuSnxm3pOcHgeUnqc](images/HeLwbMhtkoWuSnxm3pOcHgeUnqc.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: HcVwbwIDloBSsCx47dGc7PQln3e](images/HcVwbwIDloBSsCx47dGc7PQln3e.png) |                                                                                     |
| 场景7  | ![Image Token: ME3Abk6e8oWS4SxCdtBcaCten7c](images/ME3Abk6e8oWS4SxCdtBcaCten7c.jpeg) | L型角落（一面墙，一面灌木）（105别墅） | 和芯 | ![Image Token: WVbWb23CuopFIGxdZp3cuhMRnhg](images/WVbWb23CuopFIGxdZp3cuhMRnhg.png) | ![Image Token: OFDrbAsdsogg0YxRaY1cLIYdnOf](images/OFDrbAsdsogg0YxRaY1cLIYdnOf.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: HYIfb0uZEoZzxaxMt5qcYwV8nad](images/HYIfb0uZEoZzxaxMt5qcYwV8nad.png) |                                                                                     |
| 场景8  | ![Image Token: ReQ6bjF4MoQ6YzxH54zcm5GMnxc](images/ReQ6bjF4MoQ6YzxH54zcm5GMnxc.jpeg) | L型角落 （两面墙）（5别墅）       | 和芯 | ![Image Token: YwIDbX9Olox8Z6xDnnHczdEInmy](images/YwIDbX9Olox8Z6xDnnHczdEInmy.png) | ![Image Token: OwXubQA6Wof023xhKRwcMNXGntd](images/OwXubQA6Wof023xhKRwcMNXGntd.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: VKaSbRqQHozU5ux5fl6crjvanRc](images/VKaSbRqQHozU5ux5fl6crjvanRc.png) |                                                                                     |
| 场景9  | ![Image Token: QWuUbd7QZoHaNOxUO9Uc3MrWnNd](images/QWuUbd7QZoHaNOxUO9Uc3MrWnNd.jpeg) | 窄通道（双面竹林）（78别墅）       | 和芯 | ![Image Token: TLUWbv6uwoKEHZxeXfAcsqVinMc](images/TLUWbv6uwoKEHZxeXfAcsqVinMc.png) | ![Image Token: HBVVbMmIGouk6kxtCdOc02t2nVb](images/HBVVbMmIGouk6kxtCdOc02t2nVb.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: L5rObJOHNopTcRx2BkQcZTpMnqe](images/L5rObJOHNopTcRx2BkQcZTpMnqe.png) |                                                                                     |
| 场景10 | ![Image Token: NBxlbXHm5oowwwxs2tOc36UDnzg](images/NBxlbXHm5oowwwxs2tOc36UDnzg.jpeg) | 窄通道（双面墙）（78别墅）        | 和芯 | ![Image Token: UFQOb3kyhoz24ZxUZ0qco5O9nfe](images/UFQOb3kyhoz24ZxUZ0qco5O9nfe.png) | ![Image Token: SMPDbfxgmoGpzPxSm2ycbuOinBh](images/SMPDbfxgmoGpzPxSm2ycbuOinBh.png) |
|      |                                                                                      |                       | 司南 | ![Image Token: YM2sbicd8o1qIUx3HJycjpbyn4e](images/YM2sbicd8o1qIUx3HJycjpbyn4e.png) |                                                                                     |



1移动站平均误差：除了第八个点位，其他点位司南表现好于 和芯。

2固定率 司南股定率大部分高于和芯，但是第八个点位司南表现很差

3 这个分别都是双方自己给自己打分，标准不一致，但是主观感觉和芯的基站分数更加反应实际情况

4两家卫星的可视率基本反应现场环境，和芯的略微好一点。（计算公式应该是一样的，两家差很多，待确认）



5  从cep50和max值来看，司南强于和芯，但是点位八除外，

6差分龄期 司南好于和芯，但是司南点位八的差分龄期不正常，可能就是司南lora的极限了

