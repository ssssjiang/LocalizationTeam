# RTK单点解精度分析

# 1. 结论

1. PSRPOSA报文在固定站开启时可以提供伪距差分解，在完全关闭固定站只保留移动站时提供单点解。

   1. 伪距差分解优于单点解

   | 解类型     | 误差（单位：m） |
   | ------- | -------- |
   | 伪距差分解   | 0.8      |
   | 单点解     | 4.5      |
   | 单点解起点对齐 | 2.27     |

2. 单点解置信度：

   1. 在卫星条件较差的情况下3-sigma误差范围可以覆盖真值

   2. 单点解标准差和星数有相关性，但不单调



# 2. 数据分析

PSRPOSA频率为1Hz，AGRICA频率为10Hz，所以下面距离差（2D Position Error，指RTK结果（AGRICA）和单点结果（PSRPOSA）在xy平面上的位置偏差，单位m）也是经过时间插值的结果。

## 2.1 bug

Bug#462769 - 【产品自测】机器困在通道里

http://192.168.111.52/index.php?m=bug\&f=view\&t=html&=\&bugID=462769

## 2.2 原始结果：

![Image Token: M6Jdb5OFzoiraxxTRkTcO6uNnIb](images/M6Jdb5OFzoiraxxTRkTcO6uNnIb.png)

rtk\_plot.py绘制

## 2.3 整体结果

![Image Token: I6NKbpVjjo3Geyx3tPEctkPBnie](images/I6NKbpVjjo3Geyx3tPEctkPBnie.png)

RTK\_binId13.ASC\_parse2.py绘制

![Image Token: GgeVbVN76ozoeCxd7n6cehyunJf](images/GgeVbVN76ozoeCxd7n6cehyunJf.png)

## 2.4 228850s\~228950s局部结果

![Image Token: ASSJbQPQJoed7jxNKXJcEZACnwG](images/ASSJbQPQJoed7jxNKXJcEZACnwG.png)



![Image Token: K6F2bQZG1oIJYDx0kaxcduH5nbg](images/K6F2bQZG1oIJYDx0kaxcduH5nbg.png)

## 2.5 228895s\~228905s局部结果

![Image Token: E3UGbU7x1o25Usx5LQJctXV2nLg](images/E3UGbU7x1o25Usx5LQJctXV2nLg.png)



![Image Token: VCkfbtxTdodM2xxPUpcctMJpnze](images/VCkfbtxTdodM2xxPUpcctMJpnze.png)



# 3. 纯单点 测试，无rtk基站接收

## 3.1 测试方法&#x20;

使用butchart割草机的rtk定位信息作为真值。把一套单模组放在割草机上（不配对基站），输出psrposa报文，作为单点数据。

![Image Token: Hk9ibrnsYoFWmoxOYTMccJC4nWg](images/Hk9ibrnsYoFWmoxOYTMccJC4nWg.jpeg)

### 3.1.1 psrposa报文：

1. 在无基站环境中，该报文表示纯单点精度，经纬高坐标与AGRICA相同，经纬高标准差与AGRICA移动站相同。

2. 在和基站有通讯的情况下，该报文表示伪距差分的精度（略比单点解高，远差于浮点解和固定解）

3. 供应商不保证该报文的精度。

### 3.1.2 验证脚本：

用来验证在无基站环境中，psrposa报文的经纬高坐标与AGRICA相同。

## 3.2 数据1（星数良好）：





## 3.3 结果1

### 3.3.1 纯psrposa报文的定位轨迹

![Image Token: WKH1b8IZUoC7aDxy2HgcZusCn7c](images/WKH1b8IZUoC7aDxy2HgcZusCn7c.png)

### 3.3.2 rtk固定解跑的轨迹

![Image Token: JvWvb8BFho562wxWGy9ccIlGnor](images/JvWvb8BFho562wxWGy9ccIlGnor.png)

### 3.3.3 evo对比（全局对齐，暂时废弃）

#### 3.3.3.1 剔除建图轨迹的对比   evo -va

![Image Token: Aduxbj51foenHgxdqUKcloCYnEp](images/Aduxbj51foenHgxdqUKcloCYnEp.png)

![Image Token: VCxVbIaZXod1twxDYW4cY3JSnNc](images/VCxVbIaZXod1twxDYW4cY3JSnNc.png)





#### 3.3.3.2 包括建图时候的对比 添加对齐 evo -va

![Image Token: QDd6brw2VoGKUdxVQpXcfLm0nMc](images/QDd6brw2VoGKUdxVQpXcfLm0nMc.png)

&#x20;                    &#x20;

![Image Token: TIpwbxHwRo6iDHxV3NBcHCPrn5d](images/TIpwbxHwRo6iDHxV3NBcHCPrn5d.png)

&#x20;&#x20;



### 3.3.4 evo对比（时间戳对齐）

#### 3.3.4.1 方法：

1. 单模组相对于整机固定站的坐标与整机RTK坐标进行对比。

#### 3.3.4.2 误差来源

1. rtk的坐标原点为基站的中心点，但是基站的经纬度是单点定位精度。

2. 另一个完全独立的gnss模组，收到的经纬度也是单点定位的精度，所以轨迹没对齐是单点定位的误差。

   1. 这一误差也可以反映单点GPS每次启动之间的初始位置误差

   &#x20;   &#x20;

#### 3.3.4.3 结果

![Image Token: JiKXbJ0zzoOxRRxVt80cQ79JnEb](images/JiKXbJ0zzoOxRRxVt80cQ79JnEb.png)

![Image Token: OTVFbeoO1oJAG6xg6LxcuwQHnke](images/OTVFbeoO1oJAG6xg6LxcuwQHnke.png)

### 3.3.5  evo对比（起点对齐）

&#x20; 反映的是单点解相对于初始位置的漂移

&#x20;   &#x20;

![Image Token: JCWybYVgbonz6Qxsmd2czUhEnbg](images/JCWybYVgbonz6Qxsmd2czUhEnbg.jpeg)

&#x20;  &#x20;

![Image Token: Z1q5bq1PnowkXhxsfEGcFlEjnee](images/Z1q5bq1PnowkXhxsfEGcFlEjnee.jpeg)



### 3.3.6 单点解标准差可信程度

#### 3.3.6.1 计算脚本

横坐标是时间，纵坐标是单点解位置和rtk位置的2D平面距离差，和单点解2D位置标准差。这张图用来衡量单点解标准差的可信度

横坐标是周内毫秒数

位置差是共用RTK的基站坐标，换算到ENU坐标系做的差

标准差是ECEF标准差换算到ENU坐标系的标准差

场景  苏州办公室 A栋天台

![Image Token: J0kzbkNFNouGD4xxTHmcQ2AYnwd](images/J0kzbkNFNouGD4xxTHmcQ2AYnwd.jpeg)

&#x20;

#### 3.3.6.2 1-sigma

![Image Token: EyJ4bkB28oWNzjxv0cncyjwGn5d](images/EyJ4bkB28oWNzjxv0cncyjwGn5d.png)

纵坐标放大：

![Image Token: Q21cbI9rSolagQxLKxPcpPpSnbb](images/Q21cbI9rSolagQxLKxPcpPpSnbb.png)

#### 3.3.6.3 2-sigma

也不是稳定可以覆盖真值，主要是开机几秒后的数据

![Image Token: B4ZubDhtJo82PRxJtNVcqs3dnod](images/B4ZubDhtJo82PRxJtNVcqs3dnod.png)

纵坐标放大：

![Image Token: DcIAbi1kyo1sRJxAITLcG5QPnmf](images/DcIAbi1kyo1sRJxAITLcG5QPnmf.png)

#### 3.3.6.4 3-sigma

![Image Token: W5PcbEoQeoJXBoxOZgHci11ZnTf](images/W5PcbEoQeoJXBoxOZgHci11ZnTf.png)

纵坐标放大：

![Image Token: MjAAbTCW6oDHd5x7t6PcScVFnVf](images/MjAAbTCW6oDHd5x7t6PcScVFnVf.png)

### 3.3.7 搜星数目和单点水平标准差的关系

&#x20;  &#x20;

![Image Token: LLf3bdMECoBZH4x71FTcqOujnEe](images/LLf3bdMECoBZH4x71FTcqOujnEe.png)

## 3.4 数据2（星数不好）

场景，苏州办公室 b,c栋五楼中间天台

&#x20;

![Image Token: ZI79bttVZoPnXsxC1mxcMSptnYe](images/ZI79bttVZoPnXsxC1mxcMSptnYe.jpeg)

rtk：



单点：

&#x20;



## 3.5 结果2

### 3.5.1 单点解标准差可信程度

#### 3.5.1.1 1-sigma

![Image Token: L1jZbigpZomndZxWcyLcjN2Knab](images/L1jZbigpZomndZxWcyLcjN2Knab.png)

#### 3.5.1.2 2-sigma

也不是稳定可以覆盖真值，尤其是开机3min的数据

![Image Token: IaFRbz6DDobmgTxSyafcP7Byn4n](images/IaFRbz6DDobmgTxSyafcP7Byn4n.png)

#### 3.5.1.3 3-sigma

3-sigma可以稳定覆盖真值

![Image Token: WRkybUsfAol2ETxAt09cpqOYnre](images/WRkybUsfAol2ETxAt09cpqOYnre.png)

### 3.5.2 搜星数目和单点水平标准差的关系

![Image Token: PSI9bH6W0oNnNpxc8F5c07Fln1g](images/PSI9bH6W0oNnNpxc8F5c07Fln1g.png)

##

# 4. 脚本

## 4.1 单点解位置绘制脚本

