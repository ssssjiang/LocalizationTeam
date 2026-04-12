# 融合RTK、VIO逻辑1.0

# check\_insert\_entry()逻辑：观测是否使用

![check\_insert\_entry()逻辑：观测是否使用](images/whiteboard_1_1775977597621.png)



# check\_update\_entry()逻辑：观测是否可用作更新

![check\_update\_entry()逻辑：观测是否可用作更新](images/whiteboard_2_1775977600677.png)

视觉使用策略：

1. rtk固定解时，不使用视觉

2. rtk非固定解超过一定时间长度，使用视觉

3. 使用视觉时，rtk和视觉起点对齐（TODO：轨迹对齐），使用视觉update



# 测试结果

其中视觉的R为Identity()\*0.09 (待修正)

简单说明：绿色为RTK固定解，星数大于20；白色为RTK固定解，星数小于20；红色为非固定解；蓝色为融合后轨迹；红色带箭头轨迹为机器上的结果。

|                | 初版                                                                                      |                                                                                         | 第二版优化                                                                                |                                                                                      |                                                                                      |
| -------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| 数据             | 结果                                                                                      | 对比机器上的结果                                                                                | 舍弃小于21的rtk观测，视觉误差降为1e-4                                                              | 舍弃小于21的rtk观测，视觉误差降为1e-6                                                              | 舍弃小于21的rtk观测，视觉误差降为1e-8                                                              |
| 第一次弓字数据1（6.16） | ![Image Token: PDx8bDo4uo1ivqxyiwhcKYkRnMc](images/PDx8bDo4uo1ivqxyiwhcKYkRnMc.png)     | ![Image Token: XRKdbXIjRos4QQxnNxqcSSBmnNh](images/XRKdbXIjRos4QQxnNxqcSSBmnNh.png)     | ![Image Token: JDNYbt0HRohCBnxAjBHc3qHyndg](images/JDNYbt0HRohCBnxAjBHc3qHyndg.jpeg) | ![Image Token: KBh3bMt4WoRLt2xo1Vyc0cAAnqh](images/KBh3bMt4WoRLt2xo1Vyc0cAAnqh.jpeg) | ![Image Token: Albkb4KthoTcN9xGPLNceu4hn5f](images/Albkb4KthoTcN9xGPLNceu4hn5f.jpeg) |
| 第一次弓字数据2（6.16） | ![Image Token: BFlibNVVnoNTddx9Q9kccpRFnHo](images/BFlibNVVnoNTddx9Q9kccpRFnHo.png)     | ![Image Token: ACEMb2ruqojPJixKSgJcjKYjnaf](images/ACEMb2ruqojPJixKSgJcjKYjnaf.png)     | ![Image Token: ZemZbHuooofbqbxs3bFcVrDLnKd](images/ZemZbHuooofbqbxs3bFcVrDLnKd.jpeg) | ![Image Token: ZwNYbuIkookEgQxNv0zcDHhVnRg](images/ZwNYbuIkookEgQxNv0zcDHhVnRg.jpeg) | ![Image Token: OVCHbpg7uoeQ7FxdibLcpY09ntL](images/OVCHbpg7uoeQ7FxdibLcpY09ntL.jpeg) |
| 直轨测试（6.19）     | ![Image Token: LEKhbVBvSoIYASx6S11ch3xFntf](images/LEKhbVBvSoIYASx6S11ch3xFntf.png)视觉跑飞 | ![Image Token: SrtPbamfYoFCbcx19B0ckMzxnYd](images/SrtPbamfYoFCbcx19B0ckMzxnYd.png)视觉跑飞 |                                                                                      |                                                                                      |                                                                                      |
| 圆轨测试（6.19）     | ![Image Token: K67LbEvXgo9Np9xxVYCcygYwnjc](images/K67LbEvXgo9Np9xxVYCcygYwnjc.png)     | ![Image Token: NKacbtiIyoOMX5xtXecctg21njb](images/NKacbtiIyoOMX5xtXecctg21njb.png)     |                                                                                      |                                                                                      |                                                                                      |
| 第二次弓字数据1（6.23） | ![Image Token: Yg9bbQWHWo11ZCx7O1lc7WWinob](images/Yg9bbQWHWo11ZCx7O1lc7WWinob.png)     | ![Image Token: PfCBbxOrOotTkuxwsv3c5nUhn6g](images/PfCBbxOrOotTkuxwsv3c5nUhn6g.png)     | ![Image Token: WEAqbzpUTownWHxn4lYc1eDInHh](images/WEAqbzpUTownWHxn4lYc1eDInHh.jpeg) | ![Image Token: GFJZbXXLuoL0a1x8Cv5c8EL4n4f](images/GFJZbXXLuoL0a1x8Cv5c8EL4n4f.jpeg) | ![Image Token: IaJRbyTyVomkHxxopSfc2XZtnNe](images/IaJRbyTyVomkHxxopSfc2XZtnNe.jpeg) |
| 第二次弓字数据2（6.23） | ![Image Token: FMarbqSQVoxAEAx14NdcWlQwnkb](images/FMarbqSQVoxAEAx14NdcWlQwnkb.png)     | ![Image Token: ZhGUbqmfqo1bi8xtwdTcDBEDnDb](images/ZhGUbqmfqo1bi8xtwdTcDBEDnDb.png)     | ![Image Token: WYnNboEBkoG1bDxBWImc8mIZnQb](images/WYnNboEBkoG1bDxBWImc8mIZnQb.jpeg) | ![Image Token: PuwZbHkVjoDfY9x1wFwc87WZnCb](images/PuwZbHkVjoDfY9x1wFwc87WZnCb.jpeg) | ![Image Token: Cy0PbnHwionCFjx1rmLcLCoknaf](images/Cy0PbnHwionCFjx1rmLcLCoknaf.jpeg) |
| 圆轨测试（6.23）     | ![Image Token: CsfubMBZ8owhsIxd5AncIUp6nyg](images/CsfubMBZ8owhsIxd5AncIUp6nyg.png)     | ![Image Token: JQ0RbhihroI2OFxnN0ucwblWn2f](images/JQ0RbhihroI2OFxnN0ucwblWn2f.png)     |                                                                                      |                                                                                      |                                                                                      |

# 优化方向

视觉初始化的位置，结合**RTK固定解质量检测**，需要计算在一个信号质量极好的位置作初始化（a. 视觉误差随时间发散状况去判断初始化点的更新和实效，b. 找到这个极好的位置，c. 算法通用性，d. 兜底策略），一个好的初始化点可以很大程度提升精度，比如（第二次弓字数据1（6.23），选择了一个卫星数大于20的位置初始化）：

![Image Token: KYvsbYGz9oKrymxwQPHc5ZgpnuC](images/KYvsbYGz9oKrymxwQPHc5ZgpnuC.png)



# 优化记录

v2: 2025.7.3

1. Vio R矩阵分别设置为1e-8，1e-6，1e-4             ----- 视觉观测的置信程度

2. 星数少于21颗的固定解不参与更新                    ----- 视觉使用的起始点以及大概率质量不好的RTK的舍弃

优化结论: 总体来看，视觉的累计误差比IMUGYRO更小

