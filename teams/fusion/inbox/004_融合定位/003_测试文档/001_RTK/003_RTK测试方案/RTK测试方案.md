# RTK测试方案

# 简介：

&#x20;   分别关闭北斗和qzss卫星。模拟国外的卫星环境。

&#x20;        分别测试 和芯 和司南的两家自建rtk 模组。

&#x20;        两家分别提供两个rtk模组，一个配置成基站，另一个配置成移动站。

&#x20;        通过移动站和基站的输出报文来比较两家的rtk好坏。

## &#x20;静态测试的十个典型场景

&#x20;     1 空旷                                  6  单边墙  （围墙 带树林）

&#x20;     2 树林                                  7  L型角落（一面墙，一面灌木）

&#x20;     3 大面积水边（泳池或湖边）   8  L型角落 （两面墙）

&#x20;     4 单边墙 （篱笆）                 9   窄通道（双面竹林）

&#x20;     5 单边墙（房檐）                  10  窄通道（双面墙）

# 一 、测试场景

1 空旷（105别墅）

![Image Token: ZvP7bycdroVKWAxINzHcDudonbd](images/ZvP7bycdroVKWAxINzHcDudonbd.jpeg)

2 树林（105别墅）

![Image Token: CpWUbUvIRo4MhOx6bwicJwhOnYy](images/CpWUbUvIRo4MhOx6bwicJwhOnYy.jpeg)



3 大面积水边（泳池或湖边）（105别墅）

![Image Token: JJPrbM0tyoz45CxhxbPc6KuSnzf](images/JJPrbM0tyoz45CxhxbPc6KuSnzf.jpeg)

4 单边墙 （篱笆）（105别墅）

![Image Token: QBz9b04XpoR3xUx7LixcR9RinUf](images/QBz9b04XpoR3xUx7LixcR9RinUf.jpeg)

5 房檐 （78别墅）

![Image Token: F0FsbvLQno1WhLxJs55cTQarnOc](images/F0FsbvLQno1WhLxJs55cTQarnOc.jpeg)

6 单边墙  （围墙 带树林）（105别墅）

![Image Token: GORKbRzQwoMscfxSEmkcHXFgnOs](images/GORKbRzQwoMscfxSEmkcHXFgnOs.jpeg)

7  L型角落（一面墙，一面灌木）（105别墅）

![Image Token: DkrqbMhpkomSUzxePfBcaWmrnSc](images/DkrqbMhpkomSUzxePfBcaWmrnSc.jpeg)

8 L型角落 （两面墙）（5别墅）

![Image Token: GspJbQybqorH4Nxg8lxcvmWdnLc](images/GspJbQybqorH4Nxg8lxcvmWdnLc.jpeg)

9  窄通道（双面竹林）（78别墅）

![Image Token: WFm2brg8mojDvpxgmLyc0pk8nUf](images/WFm2brg8mojDvpxgmLyc0pk8nUf.jpeg)



10 窄通道（双面墙）（78别墅）

![Image Token: EwMFbW3cyoOAT7x6yHjcumURnC8](images/EwMFbW3cyoOAT7x6yHjcumURnC8.jpeg)

# 二 、统计数据

# 1. 基站：

1. 配置指令：
   &#x20;司南：log gpgga ontime  0.1 &#x20;
   &#x20;         log sysrts  ontime   0.1

2. 报文 &#x20;
   &#x20;  sysrts 和gpgga 提供 参与计算卫星数 &#x20;
   &#x20;   基站遮挡率和移动站遮挡率
   &#x20;   基站的搜星数
   &#x20;   基站质量信号评分
   &#x20;   基站信噪比和移动站信噪比（厂家自己的计算方法）

![Image Token: I4jbbX77No0zaCxSXDncOzfAnIb](images/I4jbbX77No0zaCxSXDncOzfAnIb.png)

&#x20;

![Image Token: J36tbRUscon4RrxyGONceu0rnee](images/J36tbRUscon4RrxyGONceu0rnee.png)

![Image Token: Bq0Zb6rzPoB1Vqx5vwFc73WDnZg](images/Bq0Zb6rzPoB1Vqx5vwFc73WDnZg.png)

![Image Token: E9zobCX5aoXOv6x7a92clCEHnEh](images/E9zobCX5aoXOv6x7a92clCEHnEh.png)



* 直接拿到参与计算卫星，遮挡系数和信号质量，然后统计均值。


&#x20;    &#x20;



## 1.1 移动站：

1. 配置指令：
   &#x20;gpgga 0.1
   &#x20;agrica 0.1
   &#x20;gpgsv 0.1

2. 报文+报文内容 &#x20;
   gngga agrica  gpgsv&#x20;
   1  gngga   这个报文提供
   &#x20;   hdop 水平精度因子
   &#x20;   age  差分龄期
   &#x20;   sats 参与计算的卫星数目

&#x20;
&#x20; &#x20;


![Image Token: InDDbQbwooSRKvx5a06cJAPcnyb](images/InDDbQbwooSRKvx5a06cJAPcnyb.png)

![Image Token: QuVjbf1lgo5GLaxN2jpc821dnyb](images/QuVjbf1lgo5GLaxN2jpc821dnyb.png)

&#x20; gpgsv

&#x20;   CN0 信噪比

&#x20;  sats   可视卫星数目

&#x20; &#x20;

![Image Token: AzkLbnC0Yoaq5jxmlqwcaKdnnof](images/AzkLbnC0Yoaq5jxmlqwcaKdnnof.png)

&#x20;agrica

&#x20;   postype   解类型

&#x20;   x y     相对于基站东北天坐标系下的 x y z

&#x20;   std\_x std\_y   xy的标准差

&#x20;  base\_lat  base\_lon 基站的经纬度

&#x20;   GPS  BD  GLA  GOL 四大系统的搜星之和

&#x20; &#x20;

&#x20;

![Image Token: De3Ib266Zo4jaPxT9NYcpRDBnb7](images/De3Ib266Zo4jaPxT9NYcpRDBnb7.png)

![Image Token: V5BJburynouPbnxI2wuc4felnXe](images/V5BJburynouPbnxI2wuc4felnXe.png)

![Image Token: A81eb5D5wopFKPxb62qcQ49Pnyh](images/A81eb5D5wopFKPxb62qcQ49Pnyh.png)

* 用了什么，怎么用的



&#x20;         1 根据东北天的xy和解状态 统计量（rtk被动输出精度相关数据）

&#x20;                 平均误差，误差方差， 固定解率，cep，max

&#x20;                 计算方法：根据agrica报文里面东北天的xy，

&#x20;                 根据不同的测试选择合适的真值计算方法，最重要的指标

&#x20;         2 输出数据统计（rtk主动输出精度相关数据）

&#x20;                 HDOP，STD，

&#x20;                提取方法：从gpgga和agrica报文中得到供应商自己表示精度的指标，展示出来。

&#x20;                参与解算的卫星 （gpgga报文），

&#x20;          可见卫星

&#x20;            共视卫星 \*

&#x20;                        注释： 可见卫星  （gsv报文）  >    参与解算卫星  （gga报文，）   >      共视卫星 （919报                                       文或者debug报文里面，不方便统计）

&#x20;                信噪比（gpgsv）：

&#x20;                信号和噪声的比例，信噪比越大，表示信号在噪声中的区分度越高，使用gpgsv报·             文中的信                  噪比信心来统计，统计一帧gpgsv（很多行，表示某一个时刻）所有卫星的平均信噪比，

&#x20;                然后在统计  这一时间段的平均信噪比

&#x20;                差分龄期

&#x20;                移动站进行rtk解算时候于基站最新的rtcm报文的时间差，正常范围4秒以内，
&#x20;                可以反应lora的能力，时间过长（超过4秒）会影响定位效果.

&#x20;            &#x20;

# 三 测试项目

## &#x20;  1 静态

&#x20;   真值系统：所有点的输出的平均 东北天 xy作为真值。

&#x20;   误差定义：当前点到真值点的距离作为当前点的误差。从而统计平均误差和误差的方差。

&#x20;   测试时长  1小时&#x20;

### &#x20;  （1）基站理想 ，移动站分别放在选定的十个点位 采集1小时数据

&#x20;     目的：为了模仿真实割草机上rtk的定位 情况

&#x20; &#x20;

### &#x20;  （2）移动站理想，基站分别放在选定的十个点位 采集 1 小时数据

&#x20;    目的：为了模仿客户放置基站的位置，对rtk移动站的影响。

## &#x20;  2 动态

&#x20;       速度档次  0.1米/秒 0.5米/秒 1米/秒

&#x20;       时长  0.5小时    每一个速度测试0.5小时。

### &#x20;     （1）直线

![Image Token: RXdEbZ3sgoEXB6x2beBct5ninQd](images/RXdEbZ3sgoEXB6x2beBct5ninQd.png)

&#x20;      &#x20;

&#x20;    真值：把所有点集拟合的直线作为真值，计算当前点到理想圆心的距离和半径的差当做误差。

&#x20;        点位：找了不同档次五个点位来测试，包括理想开阔  和  狭窄通道 的五个档次。

&#x20;        基站位置：两家使用相同的基站位置，基站位置为理想环境。

&#x20;   测试过程，分别对两家，在三个速度(0.1m/s，0.5m/s 1m/s) 档次采集移动站的数据报文，&#x20;

### &#x20;     （2）圆形

![Image Token: CIesbbIcOoEmR5xAQOJcePhWnp6](images/CIesbbIcOoEmR5xAQOJcePhWnp6.jpeg)



&#x20;        真值：把所有点集拟合的圆作为真值，计算当前点到理想圆心的距离和半径的差当做误差。

&#x20;        点位：找了不同档次五个点位来测试，包括理想开阔和房屋后面的五个档次。

&#x20;        基站位置：两家使用相同的基站位置，基站位置为理想环境。

&#x20;   测试过程，分别对两家，在三个速度(0.1m/s，0.5m/s 1m/s)档次采集移动站的数据报文，



&#x20;       &#x20;

&#x20;       &#x20;

## 3  专项测试 （TBD）

&#x20;         分别找 好 中 差三个档次的点位做统计。

## &#x20;    （1）rtk热启动时间。

&#x20;      测试目的，客户经常使用的时候，最多的启动方式就是热启动。

&#x20;      说明：如果rtk模组保存了 时间和星历信息的话，就是热启动。经常使用的rtk开机都是热启动。

&#x20; 测试方法：收到第一个报文作为起始时间，到出第一个固定解报文的时间差。

&#x20;       &#x20;

## &#x20;    （2）rtk 冷启动时间

&#x20;      测试目的：客户第一次使用rtk产品，基本都是冷启动

&#x20; 说明：相比热启动，如果rtk模组 没有保存正确的 时间和星历信息的话，就是冷启动。rtk第一次使用或者         无备用电源后，星历过期后再开机使用为冷启动

&#x20;       测试方法：

&#x20;        司南：从输入一个 冷启动 指令到重新收到固定解的时间差。

## &#x20;    （3） 重新固定时间

&#x20;       测试目的，测试供应商卫星失锁后，重新达到固定解的能力

&#x20;       测试方法：

&#x20;        1 首先确认可以收到固定解

&#x20;        2 同时使用铁皮锡箔纸，屏蔽基站和移动站，退出rtk固定解，

&#x20;        3  扯开屏蔽作为开始的时间到 重新收到固定解的时间差。

## &#x20;    （4） 基站移动距离测试

&#x20;        测试目的：得到基站移动多少距离可以被发现。

&#x20;             测试方法。使用供应商提供的报文，多场景多次移动不同的距离，查看一般移动多少距离，提供的报文                              可以发出基站移动报警。



## &#x20;   （5） 长周期测试（ 12小时测试）

&#x20;             测试目的，卫星的简单周期为12小时，12小时静态测试来检查全时间段的rtk的表现。

&#x20;             测试方法：同静态测试，

#

&#x20;              &#x20;

&#x20;              &#x20;

#



&#x20;      &#x20;
