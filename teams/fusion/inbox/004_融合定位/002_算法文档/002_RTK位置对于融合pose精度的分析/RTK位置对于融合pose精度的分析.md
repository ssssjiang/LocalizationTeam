# RTK位置对于融合pose精度的分析

# RTK观测模型：

$$z = f(R_{nb}, P_{nb})=P_{nr}= R_{nb}P_{br} + P_{nb},$$

$$\frac{dz}{d\widetilde{R_{nb}}} = -R_{nb}[P_{br}]_\times$$

$$\frac{dz}{d\widetilde{P_{nb}}}=I$$

# 外参对pose精度的影响分析

# 外参验证

原地旋转，验证外参3.6cm合理

![Image Token: Xxl3bMJaxolWeWxc5NFchhYSnId](images/Xxl3bMJaxolWeWxc5NFchhYSnId.png)

# 仿真数据产生

产生仿真传感器数据真值，用传感器数据跑算法，比较估计的yaw角和真值直接的RMSE

需要产生RTK，gyro和odo传感器数据

## 场景

1. 原地旋转

   让机器原地旋转，保持角速度不变

2. 绕固定半径旋转，保持角速度不变

## 外参

在仿真中，imu的外参保持固定，只改变RTK的外参

![Image Token: PeGHbC6NwoWss5xV87hcwlEAn7f](images/PeGHbC6NwoWss5xV87hcwlEAn7f.png)

## 输出格式

```c++
imu:
# timestamp(ms) imu acc_x acc_y acc_z w_x w_y w_z q_x q_y q_z q_w
odo:
# timestamp(ms) rawgyroodo acc_x acc_y acc_z w_x w_y w_z roll pitch yaw timestamp cnt_left(累加值) cnt_right(累加值)  current_x current_y
```

RTK:timestamp   sol（4） position xyz pos\_std

![Image Token: ZN3VbXa3eoiqjXxyUXacGZahnlb](images/ZN3VbXa3eoiqjXxyUXacGZahnlb.png)



## 仿真数据示例

E.G. 时长600s, lever\_arm = \[0.25; 0; 0]m,  欧拉角转四元数按 'ZYX' 顺序转换（x和w不为0）

|         | 真值v.s.添加噪音                                                                          | 噪音类型                                |
| ------- | ----------------------------------------------------------------------------------- | ----------------------------------- |
| RTK     | ![Image Token: GLlVb4K4loymwXxEF5cc1PiknGe](images/GLlVb4K4loymwXxEF5cc1PiknGe.png) | N(0,0.01²)高斯白噪声, 标准差0.01m，E向和N向独立   |
| GYRO\_Z | ![Image Token: HZWEbufWaomlpUxN5GJcwzUlnzf](images/HZWEbufWaomlpUxN5GJcwzUlnzf.png) | N(0,0.005²)高斯白噪声(rad/s) + 20Hz 高频干扰 |

## 仿真数据结果

**结论：（根据仿真结果）**

1. **杆臂对位置影响不大**

2. **杆臂越大，角度RMSE越小，原地旋转会影响大一点，其他情况无太明显的差别**

3. **打滑是位置会有偏差，如误差过大（速度快或打滑时间长），需要增加策略判断**

4. 原地旋转打滑（在RTK有噪音的情况下）：外侧轮子打滑，3.6cm的杆臂，位置受影响不大，角度会RMSE会增加到1.514247（deg）；25cm的杆臂位置和角度影响都不到。

| 场景                        | rtk外参x(m)  | evo\_rpe （平移部分） |                                                                                     | evo\_rpe（旋转部分 -r angle\_deg）  |                                                                                                                                                                        |
| ------------------------- | ---------- | --------------- | ----------------------------------------------------------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|                           |            | RMSE            | 图                                                                                   | RMSE                          | 图                                                                                                                                                                      |
|                           | 0.036      | 0.003062        | ![Image Token: CN8ZbsZmgoqWMZxEsUhcVVtYnWg](images/CN8ZbsZmgoqWMZxEsUhcVVtYnWg.png) | 0.429967                      | ![Image Token: IeGzbQeSIotjIWxWibMcRcZfnRb](images/IeGzbQeSIotjIWxWibMcRcZfnRb.png)                                                                                    |
|                           | 0.1        | 0.003028        | ![Image Token: QBTbbfyhdoZdIPxw9a7cLOWnnSc](images/QBTbbfyhdoZdIPxw9a7cLOWnnSc.png) | 0.252970                      | ![Image Token: V6z2b2rl5oEwebx8QDZcEPLbnIR](images/V6z2b2rl5oEwebx8QDZcEPLbnIR.png)                                                                                    |
|                           | 0.175      | 0.003011        | ![Image Token: PZOCbbeg8opJ7txeLU0cfSugnEb](images/PZOCbbeg8opJ7txeLU0cfSugnEb.png) | 0.205626                      | ![Image Token: XBTWbZgblo1ya9x2q5Ac6nsCnig](images/XBTWbZgblo1ya9x2q5Ac6nsCnig.png)                                                                                    |
|                           | 0.25       | 0.003023        | ![Image Token: TxZBbF4ELoaHKfx9VABcwLMsnFe](images/TxZBbF4ELoaHKfx9VABcwLMsnFe.png) | 0.183446                      | ![Image Token: EXNLbdhoioQKOIxjx7Pcg3AjnHh](images/EXNLbdhoioQKOIxjx7Pcg3AjnHh.png)                                                                                    |
| 1.1. 原地旋转，右轮打滑            | 0.036      | 0.003054        | ![Image Token: OCrDbJXfPozawtxvKaHcKSbqnCc](images/OCrDbJXfPozawtxvKaHcKSbqnCc.png) | 1.514247                      | ![Image Token: CSs7bsSRpoyfkkxK1q0cyxyfn1d](images/CSs7bsSRpoyfkkxK1q0cyxyfn1d.png)                                                                                    |
|                           | 0.25       | 0.003055        | ![Image Token: AWgubMgqDoheD6xOn5ucQ9Qgn8Z](images/AWgubMgqDoheD6xOn5ucQ9Qgn8Z.png) | 0.186547                      | ![Image Token: Qu6ub7pEQodJeAxzE6BcsQDknsf](images/Qu6ub7pEQodJeAxzE6BcsQDknsf.png)![Image Token: NI9sbbtjHoNEvnxORHlcEYgvnNg](images/NI9sbbtjHoNEvnxORHlcEYgvnNg.png) |
| 1.2. 原地旋转，右轮打滑，**无RTK噪音** | 0.036      | 0.000077        | ![Image Token: FWk3bwIy0o8tUJx18p5chFiQnkg](images/FWk3bwIy0o8tUJx18p5chFiQnkg.png) | 0.009063                      | ![Image Token: Z2yPbm3EJoaI52xRwlicv1QanKf](images/Z2yPbm3EJoaI52xRwlicv1QanKf.png)                                                                                    |
|                           | 0.25       | 0.000077        | ![Image Token: EJULbVNSxoSzlRxxsQacDJlRnHH](images/EJULbVNSxoSzlRxxsQacDJlRnHH.png) | 0.008555                      | ![Image Token: YYkYbl28wo0mJLxMNZdcTvNXnSe](images/YYkYbl28wo0mJLxMNZdcTvNXnSe.png)                                                                                    |
|                           | 0.036去除初始化 | 0.003321        | ![Image Token: RduHbp2xaoTUW4xOqdjcO0vfneg](images/RduHbp2xaoTUW4xOqdjcO0vfneg.png) | 0.166349                      | ![Image Token: BxhSbSS95odXNlxSyilcvWN9n2c](images/BxhSbSS95odXNlxSyilcvWN9n2c.png)                                                                                    |
|                           | 0.1去除初始化   | 0.003273        | ![Image Token: Prf7bHZBqoBQB3xtmTicvKHnn5e](images/Prf7bHZBqoBQB3xtmTicvKHnn5e.png) | 0.164058                      | ![Image Token: IrjbbxYZnoEZMJx9FL6c7ZjSnHf](images/IrjbbxYZnoEZMJx9FL6c7ZjSnHf.png)                                                                                    |
|                           | 0.175去除初始化 | 0.003187        | ![Image Token: Mn8FbVZTRoMRaBxpsCccRZUVn5e](images/Mn8FbVZTRoMRaBxpsCccRZUVn5e.png) | 0.160081                      | ![Image Token: Ef3HbjpoUo5FjhxyBQxcohhFnhc](images/Ef3HbjpoUo5FjhxyBQxcohhFnhc.png)                                                                                    |
|                           | 0.25去除初始化  | 0.003128        | ![Image Token: TFPUbS94Zos203xAx8McC8sBnZf](images/TFPUbS94Zos203xAx8McC8sBnZf.png) | 0.159212                      | ![Image Token: Yt1GbQsj8oSBrYxnl5qc6v41nIb](images/Yt1GbQsj8oSBrYxnl5qc6v41nIb.png)                                                                                    |
|                           | 0.036去除初始化 | 0.000242        | ![Image Token: Gh2XbO3NWouRq6xsZ3ycArSrnSg](images/Gh2XbO3NWouRq6xsZ3ycArSrnSg.png) | 0.008878                      | ![Image Token: NrFcbtRYSoKzTCx2hu7cKbNWn7a](images/NrFcbtRYSoKzTCx2hu7cKbNWn7a.png)                                                                                    |
|                           | 0.1去除初始化   | 0.000242        | ![Image Token: Ja1zb7MrCogrVnx996hcFqPMnre](images/Ja1zb7MrCogrVnx996hcFqPMnre.png) | 0.008858                      | ![Image Token: RP1EbL1CuoLNWqxQyk8cRN0knAe](images/RP1EbL1CuoLNWqxQyk8cRN0knAe.png)                                                                                    |
|                           | 0.175去除初始化 | 0.000241        | ![Image Token: GF0ublLIVoCRVbxN8ykc7W4envb](images/GF0ublLIVoCRVbxN8ykc7W4envb.png) | 0.008515                      | ![Image Token: B36obykiDoW0zixDVK8cCijOnQS](images/B36obykiDoW0zixDVK8cCijOnQS.png)                                                                                    |
|                           | 0.25去除初始化  | 0.000241        | ![Image Token: YVqxbvRznoYKPXx9ccJcZBsPnKh](images/YVqxbvRznoYKPXx9ccJcZBsPnKh.png) | rmse        0.008605          | ![Image Token: KNh2bqs1xow0W4x5e58cQ5G1nwc](images/KNh2bqs1xow0W4x5e58cQ5G1nwc.png)                                                                                    |
|                           | 0.036      | 0.000686        | ![Image Token: WIGabXinZoFusix9nR2cVvUrnSh](images/WIGabXinZoFusix9nR2cVvUrnSh.png) | 0.009628                      | ![Image Token: AJWZbB3xKoLtvTxB2mVcZoiFneg](images/AJWZbB3xKoLtvTxB2mVcZoiFneg.png)                                                                                    |
|                           | 0.1        | 0.000686        | ![Image Token: XJHpbeV9zoe9rLxo1iwcBgFtngc](images/XJHpbeV9zoe9rLxo1iwcBgFtngc.png) | 0.009469                      | ![Image Token: VVS1b5bHmomFKsxeiArcs6Pinjg](images/VVS1b5bHmomFKsxeiArcs6Pinjg.png)                                                                                    |
|                           | 0.175      | 0.000686        | ![Image Token: MkihbOw2mo36XgxXFg4cGEstnFg](images/MkihbOw2mo36XgxXFg4cGEstnFg.png) | 0.009327                      | ![Image Token: XwefbDT3Jo6XfUxzOGWcR99dn2f](images/XwefbDT3Jo6XfUxzOGWcR99dn2f.png)                                                                                    |
|                           | 0.25       | 0.000686        | ![Image Token: VdnYbZJFVofljDxKy9VcXfA8n9e](images/VdnYbZJFVofljDxKy9VcXfA8n9e.png) | 0.009152                      | ![Image Token: IdDubondaolC1FxekZ4cdxfZnuf](images/IdDubondaolC1FxekZ4cdxfZnuf.png)                                                                                    |

