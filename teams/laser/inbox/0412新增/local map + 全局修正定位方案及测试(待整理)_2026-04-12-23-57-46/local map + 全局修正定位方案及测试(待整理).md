# local map + 全局修正定位方案及测试(待整理)

# 1. 算法流程图：

![画板 1](images/whiteboard_1_1776009469842.png)

# 2. 测试结论：

## 2.1 第一阶段测试结论：

* &#x20;全局单帧定位，降采样后精度更高（体素大小：0.5m）

* &#x20;场景变化时，加入local map定位轨迹更准确更平滑

# 3. 相关可视化说明：

## 3.1 轨迹图：

黑色：全局单帧匹配定位轨迹

橙黄色：局部里程计＋全局定期修正（单帧到全局匹配）轨迹

亮青色：局部里程计轨迹

![Image Token: Rlh4bHa2IontEPx8kQucl33Vnuh](images/Rlh4bHa2IontEPx8kQucl33Vnuh.png)

## 3.2 点云图：

白色点云：全局地图

红色点云：lidar帧通过 单帧全局匹配修正后 转换到地图系下的点云

绿色点云：lidar帧通过 局部＋全局定期修正后 转换到地图系下的点云

![Image Token: Rxdtb5twjoDGfSxkrLlcmc64nUc](images/Rxdtb5twjoDGfSxkrLlcmc64nUc.png)



# 4. 仿真测试结果：

## 4.1 全局单帧定位降采样影响测试结果：

定位结果：通过连续单帧与地图进行匹配得到的位姿

| 未降采样： 单帧6000个点                                                                      | 降采样： 单帧3000个点                                                                       |
| ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| ![Image Token: JXfmbdPeKoaThQx98gWcskTlnmb](images/JXfmbdPeKoaThQx98gWcskTlnmb.png) | ![Image Token: QBM6b69h5oA7psxXZnaccwHqn1g](images/QBM6b69h5oA7psxXZnaccwHqn1g.png) |
| ![Image Token: XtocbfpcjopgTExJP72csOnVnUf](images/XtocbfpcjopgTExJP72csOnVnUf.png) | ![Image Token: CNF1bHO9vo8jW7xi3pxcqdY9nwi](images/CNF1bHO9vo8jW7xi3pxcqdY9nwi.png) |
| ![Image Token: YXHlbuPcko9CIEx1krTcZLF6nDg](images/YXHlbuPcko9CIEx1krTcZLF6nDg.png) | ![Image Token: VcvYb8WJ9oHWOnxzAKGcSWdrn3c](images/VcvYb8WJ9oHWOnxzAKGcSWdrn3c.png) |



## 4.2 场景变化测试结果：

场景变化：

![Image Token: Ac4QbriOToCzTqxgdtocDnkwnBf](images/Ac4QbriOToCzTqxgdtocDnkwnBf.png)



| 时刻       | 轨迹对比结果                                                                              | 点云对比结果（绿色：局部 + 全局修正）（红色：全局匹配结果）（白色：全局地图）                                            |
| -------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 767.602  | ![Image Token: TRbtbbrdYoJjRaxsk1LcZM4ynsc](images/TRbtbbrdYoJjRaxsk1LcZM4ynsc.png) | ![Image Token: LcOVbLGnJoCudkxtRURcrHBXnyg](images/LcOVbLGnJoCudkxtRURcrHBXnyg.png) |
| 778.846  | ![Image Token: GizUbwLe4ouw58xxX11c6zpgnBd](images/GizUbwLe4ouw58xxX11c6zpgnBd.png) | ![Image Token: OOz5b31nvo5CRWx1XDTcpOQXn9O](images/OOz5b31nvo5CRWx1XDTcpOQXn9O.png) |
| 1056.766 | ![Image Token: I21obaxumoNKIGxBHXec3K2BnsZ](images/I21obaxumoNKIGxBHXec3K2BnsZ.png) | ![Image Token: AahQbMo6doPyjVxCGuSc0teKnZc](images/AahQbMo6doPyjVxCGuSc0teKnZc.png) |

## 4.3 基于local map与全局地图匹配修正测试

蓝色：单帧匹配修正结果

粉色：local map匹配修正结果

| 时刻 | 轨迹对比结果                                                                              |
| -- | ----------------------------------------------------------------------------------- |
|    | ![Image Token: TCBXbe1pXorK5qxi6b5cLf3Gnob](images/TCBXbe1pXorK5qxi6b5cLf3Gnob.png) |
|    | ![Image Token: SAmDbqAJuoRscHxxNSkcCwxPnvc](images/SAmDbqAJuoRscHxxNSkcCwxPnvc.png) |
|    | ![Image Token: Fv0Mbz0EUoVisBxzAqVcqPC5n6c](images/Fv0Mbz0EUoVisBxzAqVcqPC5n6c.png) |
|    | ![Image Token: QKnCb9VvqoyJrjxxEIgcdE5jnDd](images/QKnCb9VvqoyJrjxxEIgcdE5jnDd.png) |
|    | ![Image Token: TlfobwZlNoehtLxuUk1ccB5onmf](images/TlfobwZlNoehtLxuUk1ccB5onmf.png) |
|    | ![Image Token: LnjVbncrGoGlAVxbTjacQQXXnPf](images/LnjVbncrGoGlAVxbTjacQQXXnPf.png) |
|    | ![Image Token: EFyRbTPOqoa4Bcxx80qcbrNsnGb](images/EFyRbTPOqoa4Bcxx80qcbrNsnGb.png) |



## 4.4 增大local to global修正频率对比结果：

| 固定里程触发修正 |   |
| -------- | - |
|          |   |
|          |   |





修正加权处理：

| 加权系数 | diff pose轨迹图                                                                        | 局部误差对比 |
| ---- | ----------------------------------------------------------------------------------- | ------ |
| 0.1  | ![Image Token: XA4nb17MuoBZkPxAc8qc2EYyn6c](images/XA4nb17MuoBZkPxAc8qc2EYyn6c.png) |        |
| 0.3  | ![Image Token: NkiBb9L7Bo7cMuxtdxKcbEsbnhh](images/NkiBb9L7Bo7cMuxtdxKcbEsbnhh.png) |        |
| 1    | ![Image Token: S6qDb82psoCBtvxV7b5cO7Vfnzg](images/S6qDb82psoCBtvxV7b5cO7Vfnzg.png) |        |



## 4.5 弓子割草数据：

用弓子割草数据建图 并基于该图去定位 将二者轨迹进行对比



