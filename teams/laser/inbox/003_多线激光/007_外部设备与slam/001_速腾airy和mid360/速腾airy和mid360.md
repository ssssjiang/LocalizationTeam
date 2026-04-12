# 速腾airy和mid360

## 1. 结论及分析

### 1.1 结论：

通过对速腾和Mid360两款传感器的对比测试，可以得出以下结论：

1. 在点云质量方面，速腾传感器很差，具有非常多的拖影，而Mid360表现正常；

2. SLAM建图性能上，速腾建图质量差，存在明显的重影和漂移问题，而Mid360展现出更好的稳定性和精度；

3. 速腾在倾斜安装（前倾5°）可部分改善高度漂移问题，但由于传感器质量差，建图结果仍不理想

4. 速腾厂商反馈，器件测距原理所致；暂时无法优化：

![Image Token: SrBxb5OFfo67MIxGbx6c1pxOn9g](images/SrBxb5OFfo67MIxGbx6c1pxOn9g.png)

### 1.2 分析：

**点云质量对比分析：**

1. 速腾传感器：点云质量较差，存在明显的运动拖影现象。在25米测距条件下，拖影长度可达1.3米，严重影响点云清晰度。

2. Mid360传感器：表现出优异的点云质量，树木等复杂轮廓的还原度较高，基本未观察到明显拖影现象。

**SLAM建图性能评估**

1. 速腾传感器：建图存在明显缺陷，表现为墙面点云厚度异常增大、稳定性不足、重影现象显著，且存在垂直方向的漂移问题。

2. Mid360传感器：建图质量稳定，无明显分层现象，整体建图精度较高。

**地面点对SLAM系统的影响**

1. &#x20;速腾传感器（无地面点）：系统在高度方向上出现严重漂移，导致建图结果在垂直维度上不一致。

2. 速腾传感器（安装角度-5°，含地面点）：高度漂移问题得到一定程度的改善，但未完全消除。



## 2. 速腾airy联调：我们自己采集的数据：

### 2.1 点云质量问题严重：

#### 2.1.1 内场：玻璃内外出现对称太阳伞：

速腾回复：玻璃lens 镜面鬼影，速腾反馈研发端



![Image Token: D9kUbebQpoq61txML1TcE1l2njb](images/D9kUbebQpoq61txML1TcE1l2njb.png)



![Image Token: PYZSbsri9oYSLmxcz6lcwkR2nUe](images/PYZSbsri9oYSLmxcz6lcwkR2nUe.jpeg)

#### 2.1.2 拖影无处不在

#### -速腾回复 树叶或小间隙的时候，会有概率光斑覆盖几个障碍物，多帧叠加测距在一定范围内波动。&#xA;

![Image Token: P18rb26MHo7JplxL0ZtcRWR5nue](images/P18rb26MHo7JplxL0ZtcRWR5nue.jpeg)

![Image Token: TZSJb7Pk5oqxLWx94zZcX0m6nzg](images/TZSJb7Pk5oqxLWx94zZcX0m6nzg.jpeg)

![Image Token: DvypbkVK8o9QacxUuqZctfAhnCg](images/DvypbkVK8o9QacxUuqZctfAhnCg.jpeg)

![Image Token: PQOob1jFLoixmtxp2iScbxFLnQf](images/PQOob1jFLoixmtxp2iScbxFLnQf.png)

![Image Token: TMNWbFFNro4ctvx4gLKcb919ncf](images/TMNWbFFNro4ctvx4gLKcb919ncf.png)

![Image Token: UCwKbhqOfo99OjxPZO4cfibincf](images/UCwKbhqOfo99OjxPZO4cfibincf.png)



![Image Token: S4igb9N2LoobRlxhdOGcx6VAnRe](images/S4igb9N2LoobRlxhdOGcx6VAnRe.png)



现象：点云的点，沿着和激光雷达的射线，抖成一个线状的团；静止的时候

![Image Token: YVNFbrCE0oSbqKxBQ1Hc8dqgnad](images/YVNFbrCE0oSbqKxBQ1Hc8dqgnad.jpeg)

&#x20;                                                                    扫描视角



速腾：树叶的噪点拖点多是因为激光在多层叶片间反复折射，造成的拖点会比在规则面上多一些



#### 2.1.3 静止数据：

![Image Token: YBmVbMJEhojtHCxp2lXcxxEmnI1](images/YBmVbMJEhojtHCxp2lXcxxEmnI1.png)



### 2.2 slam表现不好：



#### 2.2.1         好多上面的拖影；且slam只能移除40度-90度的线来跑（这线基本是无效的拖影干扰）；

![Image Token: DlIsbTRZgop08hxW95QcSEbinAd](images/DlIsbTRZgop08hxW95QcSEbinAd.png)



#### 2.2.2 墙皮厚重

![Image Token: YTNxbu2o9oJaEvxDukBcBINinqd](images/YTNxbu2o9oJaEvxDukBcBINinqd.png)

![Image Token: Ck55bQTnpoXAJ3xRto8cc72OnDh](images/Ck55bQTnpoXAJ3xRto8cc72OnDh.png)



![Image Token: SMRibUm47oThcdxAlrdcaH72n8g](images/SMRibUm47oThcdxAlrdcaH72n8g.png)



#### 2.2.3 最远测距40几米

速腾需要提供这个场景照片和点云的数据包&#x20;

![Image Token: Y2JVb4BvQoK5fUxlK9OcTQ5Inlh](images/Y2JVb4BvQoK5fUxlK9OcTQ5Inlh.png)

### 2.3 测量误差比

距离车体约25m处，测量误差在1.3m左右

![Image Token: YBKwbgZYmoh3N1xyZbUcB4wFntj](images/YBKwbgZYmoh3N1xyZbUcB4wFntj.jpeg)

![Image Token: RcCRbNQRYo1hTdxuqRZc2hyknGe](images/RcCRbNQRYo1hTdxuqRZc2hyknGe.png)

### 2.4 速腾带地面数据结果（-5°）

当回到起点后发现高度上还是有一定的漂移，但相较于之前不带地面点情况，高度上漂移有所缓解

![Image Token: ExGabWwFDo2U0ixueCHcnORonDg](images/ExGabWwFDo2U0ixueCHcnORonDg.png)

## 3. mid360开源数据：人举着，1m高度；rosbag 整体表现较好

目前仅有开源数据，且mid360有负角度；具体要等我们数据采集到，进一步看

### 3.1 树的轮廓清晰，几乎看不到什么拖影；

![Image Token: O8V7bG4TnoluQ4xf3vrcymqOnQb](images/O8V7bG4TnoluQ4xf3vrcymqOnQb.png)

![Image Token: N44bbHx7moJ0w6xA3ZZc1l8rn9b](images/N44bbHx7moJ0w6xA3ZZc1l8rn9b.png)

![Image Token: JVXHb445LoDDZrxZfUzcD6Yxnjf](images/JVXHb445LoDDZrxZfUzcD6Yxnjf.png)





### 3.2 slam表现正常，测距可达70多米：

![Image Token: EFVSb1Fb0oWeG5xqxlYcvhZ9nsh](images/EFVSb1Fb0oWeG5xqxlYcvhZ9nsh.png)



### 3.3 78号场地

![Image Token: JenHbR8D6oKy87xrKBlcf2zknZg](images/JenHbR8D6oKy87xrKBlcf2zknZg.jpeg)



### 3.4 105号场地

![Image Token: Mu2xbnw7aokiPNxpYOhcOwLin9d](images/Mu2xbnw7aokiPNxpYOhcOwLin9d.jpeg)



### 3.5 其他场地：

![Image Token: Ee3sbonYVoUtvQx5Eptc1vJZnCg](images/Ee3sbonYVoUtvQx5Eptc1vJZnCg.jpeg)



![Image Token: Icy4b3e7Oob84Mx1yEdcF9sAnAh](images/Icy4b3e7Oob84Mx1yEdcF9sAnAh.jpeg)







## 4. mid360 我们数据(外场)：整体表现较好



### 4.1 105建图：

![Image Token: RNBvbkZ9IoNiwbxOVEocpH9EnJg](images/RNBvbkZ9IoNiwbxOVEocpH9EnJg.png)



![Image Token: OF44bOEtloFyLDxSdsTcCcrfn1L](images/OF44bOEtloFyLDxSdsTcCcrfn1L.png)



### 4.2 78场地建图：



![Image Token: U7pnbr5NMoe0bJxK3gQcxkh1nLh](images/U7pnbr5NMoe0bJxK3gQcxkh1nLh.jpeg)





105颠簸数据：比较平稳

![Image Token: U6h8bLKupoPLAjxjN88cigIjnRd](images/U6h8bLKupoPLAjxjN88cigIjnRd.png)









### 4.3 livox-105-定位数据

#### 4.3.1 定位数据1：

建图轨迹：

![Image Token: W7z6bOVkZov5OkxaPRCcUS1pnsh](images/W7z6bOVkZov5OkxaPRCcUS1pnsh.png)

定位轨迹：

![Image Token: TZGcbl78VoJjgRxm4XJcmG5Zngb](images/TZGcbl78VoJjgRxm4XJcmG5Zngb.png)

#### 4.3.2 定位数据2

建图：

![Image Token: WkGbb6uj7oGmofxt4gicloHXnOg](images/WkGbb6uj7oGmofxt4gicloHXnOg.png)

定位：

![Image Token: IEbTbzD9roEhWhxmAGgc1K8Qn6g](images/IEbTbzD9roEhWhxmAGgc1K8Qn6g.png)

livox-105-斜坡

![Image Token: ZnuBbsQHfoatlHxu7mCclTSjnpf](images/ZnuBbsQHfoatlHxu7mCclTSjnpf.png)



### 4.4 livox-78-定位数据

#### 4.4.1 定位1数据：

建图轨迹：

![Image Token: DwUGbVqpHoEj8bxBMYTcf5smnNk](images/DwUGbVqpHoEj8bxBMYTcf5smnNk.png)

定位轨迹：

![Image Token: VR9ibpI4UoRbHTxPsYQcPfuPnzc](images/VR9ibpI4UoRbHTxPsYQcPfuPnzc.png)

#### 4.4.2 定位数据2：

建图轨迹：

![Image Token: F1USbxTEtoMfjYxw1dGcgfdBn7R](images/F1USbxTEtoMfjYxw1dGcgfdBn7R.png)

定位轨迹：

![Image Token: XrUvbh8r9oIWTKxQ7AdcIj0Nnzf](images/XrUvbh8r9oIWTKxQ7AdcIj0Nnzf.png)















