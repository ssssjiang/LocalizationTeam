# 联合OC及盲区管控



# 1. 影响盲区的因素

整机盲区：双目立体垂直视场下边缘到整机bumper最前端的距离。

&#x20;              双目到bumper的距离，双目高度，双目pitch角，双目立体视场角，装配，标定精度

![Image Token: GxDcbQvxnoJO64xvI2ocIhjknXe](images/GxDcbQvxnoJO64xvI2ocIhjknXe.png)

对于模组厂来说，影响因素是双目立体视场角，单模组OC精度和左右目搭配&#x20;

（原始分辨率1280\*1080，OC：640，544）



![                  Left:560   Right：520                       Left :504  Righ:504                           Left :584  Righ:584                                                                         (Token: Y4yWbcftSopQl7xWOBfcUk7jn3d)](images/Y4yWbcftSopQl7xWOBfcUk7jn3d.png)



![情况一：Left :560  Righ:520                         情况二Left :504  Righ:504   小盲区                情况三Left :584  Righ:584  大盲区 (Token: O4AObEzXroyMboxcqe1cDGwXnlf)](images/O4AObEzXroyMboxcqe1cDGwXnlf.png)



![实测数据 (Token: WmhJbgMoRoUcLTxIFawcpnAhn8f)](images/WmhJbgMoRoUcLTxIFawcpnAhn8f.png)



# 2. 联合和舜宇双目内部结构差异

![Image Token: FDEIbLjpUo5BNNxFsDHctv4PnJh](images/FDEIbLjpUo5BNNxFsDHctv4PnJh.jpeg)

# 3. 联合和舜宇生产数据

## 3.1 联合2026.1.23批次

第一批次生产数据OC分布，左目基本在544以下，右目在544以上，但是对于量产工艺来说，单模组Cy分布范围在±40pixel，即108um。 均值并未分布在中心（L：533, R：554）接近情况一

![Image Token: H9D0bYvt0oQKU3xREuucXx5ungg](images/H9D0bYvt0oQKU3xREuucXx5ungg.png)

![Image Token: JSFObOWvsoIlWRxspq9cEcU8nXd](images/JSFObOWvsoIlWRxspq9cEcU8nXd.png)

![Image Token: ALH2bp6bbo0mWaxRJWWcHro1nLg](images/ALH2bp6bbo0mWaxRJWWcHro1nLg.jpeg)

![Image Token: BDB0bRKkloPabtxtkd2cVOIxnnc](images/BDB0bRKkloPabtxtkd2cVOIxnnc.jpeg)



整机versa装机300pcs 盲区统计数据如下，门限0.15  最大值0.11，CPK=3.15

![Image Token: EMwDbyfoDo29BHxb5PmcMNitnOd](images/EMwDbyfoDo29BHxb5PmcMNitnOd.jpeg)



## 3.2 联合 2026.4.9 批次  (596PCS)  重新挑选golden 点检单模组OC

L:522  R:551

![Image Token: VLuib8HpEoD1mMxubG1cVIBCnLh](images/VLuib8HpEoD1mMxubG1cVIBCnLh.png)

![Image Token: Fvwkby8Ppoiiirxeiiyc4KJHnVf](images/Fvwkby8Ppoiiirxeiiyc4KJHnVf.png)

![Image Token: JwcYb2gUQoEeBVxhrdac7AQSnbd](images/JwcYb2gUQoEeBVxhrdac7AQSnbd.jpeg)

![Image Token: Zr96b4xr2o5po3xYTd5cYcU3nDg](images/Zr96b4xr2o5po3xYTd5cYcU3nDg.jpeg)



计划4.14/4.15 上整机monet 会有整机数据

# &#x20;



## 3.3 舜宇  量产 1991pcs

左右目相同，数据分布一致，且平均值居中&#x20;

![Image Token: JjV1bLwiDo9AyOxJXnHcxashnAg](images/JjV1bLwiDo9AyOxJXnHcxashnAg.png)

![Image Token: H1LYblzPNo7k2gxBRHvce4mDneU](images/H1LYblzPNo7k2gxBRHvce4mDneU.png)

L:546  R :544

![Image Token: OV4NbPwV4osFUJxeRQmcZxqmnbb](images/OV4NbPwV4osFUJxeRQmcZxqmnbb.jpeg)

![Image Token: YQ0wbHxIRo9xCDxtFxdcJV1QnPg](images/YQ0wbHxIRo9xCDxtFxdcJV1QnPg.jpeg)





![Image Token: PALsb5cVLot2t5xcrDccVbkSnQe](images/PALsb5cVLot2t5xcrDccVbkSnQe.jpeg)

|                          | 样本量  | OC       | 平均值       |
| ------------------------ | ---- | -------- | --------- |
| 联合第一批次                   | 582  | Left Cy  | 533.04111 |
|                          |      | Rigt Cy  | 554.78219 |
| 联合第二批次（重新挑选golden模组点检OC） | 596  | Left Cy  | 522.14176 |
|                          |      | Right Cy | 551.73164 |
| 舜宇量产                     | 1991 | Left Cy  | 546.20904 |
|                          |      | Right Cy | 554.78219 |

# 4. 结论

以上，联合量产双目工艺，左右目结构约束，并不能共用治具和机台，导致左右目数据不一致，加上联合厂内制程管控因素，且左右目搭配随机，盲区会有批量不良风险。
