# 速腾airy和mid360 +禾赛对比分析

## 1. 结论及分析

### 1.1 结论：

通过对速腾和Mid360两款传感器的对比测试，可以得出以下结论：

1. 在点云质量方面，速腾传感器很差，具有非常多的拖影，而Mid360表现正常；

2. SLAM建图性能上，速腾建图质量差，存在明显的重影和漂移问题，而Mid360展现出更好的稳定性和精度；

3. 速腾在倾斜安装（前倾5°）可部分改善高度漂移问题，但由于传感器质量差，建图结果仍不理想

4. 速腾厂商反馈，器件测距原理所致；暂时无法优化：

![Image Token: LaWibzvXfoR8Z0xpZVpcxLg5nnb](images/LaWibzvXfoR8Z0xpZVpcxLg5nnb.png)

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



![Image Token: NMfGbDpmkoUgW2xD0DacyqqCn8c](images/NMfGbDpmkoUgW2xD0DacyqqCn8c.png)



![Image Token: A9Swbs3NAoMcSFxIJF8cr3Annzb](images/A9Swbs3NAoMcSFxIJF8cr3Annzb.jpeg)

#### 2.1.2 拖影无处不在

#### -速腾回复 树叶或小间隙的时候，会有概率光斑覆盖几个障碍物，多帧叠加测距在一定范围内波动。&#xA;

![Image Token: E90LbHwmRofYsIxr8yscHkILnQc](images/E90LbHwmRofYsIxr8yscHkILnQc.jpeg)

![Image Token: V4zUbeI2koYMr1xlD16cAQXYnac](images/V4zUbeI2koYMr1xlD16cAQXYnac.jpeg)

![Image Token: StxMbnfkMoP1AQx4okTchwY3nre](images/StxMbnfkMoP1AQx4okTchwY3nre.jpeg)

![Image Token: Luw7bmyo0oGnO5xvBj9cW8JTnSc](images/Luw7bmyo0oGnO5xvBj9cW8JTnSc.png)

![Image Token: FWiubOpvFo0XO7xBVm0c1Dtfn2c](images/FWiubOpvFo0XO7xBVm0c1Dtfn2c.png)

![Image Token: L0xrbNFgYoF7BJxwId6cYeVsnhI](images/L0xrbNFgYoF7BJxwId6cYeVsnhI.png)



![Image Token: STIDb6jr9o2VSYxWWH8cChUAnqJ](images/STIDb6jr9o2VSYxWWH8cChUAnqJ.png)



现象：点云的点，沿着和激光雷达的射线，抖成一个线状的团；静止的时候

![Image Token: J8TtbKhT6oDlpZx8HnWcJrzynoi](images/J8TtbKhT6oDlpZx8HnWcJrzynoi.jpeg)

&#x20;                                                                    扫描视角



速腾：树叶的噪点拖点多是因为激光在多层叶片间反复折射，造成的拖点会比在规则面上多一些



#### 2.1.3 静止数据：

![Image Token: MLheb7eTZomW0PxBMujcn3zvnPt](images/MLheb7eTZomW0PxBMujcn3zvnPt.png)



### 2.2 slam表现不好：



#### 2.2.1         好多上面的拖影；且slam只能移除40度-90度的线来跑（这线基本是无效的拖影干扰）；

![Image Token: Nl75buYI4os4iMxLS4lcLXT6n7c](images/Nl75buYI4os4iMxLS4lcLXT6n7c.png)



#### 2.2.2 墙皮厚重

![Image Token: KcnmbBX34owNo8xSHAAcQvV9nec](images/KcnmbBX34owNo8xSHAAcQvV9nec.png)



![Image Token: LlixbtnfSo1oVkxbO8FcgYGDnvZ](images/LlixbtnfSo1oVkxbO8FcgYGDnvZ.png)



![Image Token: OUu4bmKtOoGwuJxqu5dcJYTjnld](images/OUu4bmKtOoGwuJxqu5dcJYTjnld.png)



#### 2.2.3 最远测距40几米

速腾需要提供这个场景照片和点云的数据包&#x20;

![Image Token: Fxnobz2Y3omcJPxXkBBcVuHinab](images/Fxnobz2Y3omcJPxXkBBcVuHinab.png)

### 2.3 测量误差比

距离车体约25m处，测量误差在1.3m左右

![Image Token: H1wCb3Y9locCKCx1DgOcEF1vnAg](images/H1wCb3Y9locCKCx1DgOcEF1vnAg.jpeg)

![Image Token: ALpdb1RcVoG3zYx46pEcgRB7nph](images/ALpdb1RcVoG3zYx46pEcgRB7nph.png)

### 2.4 速腾带地面数据结果（-5°）

当回到起点后发现高度上还是有一定的漂移，但相较于之前不带地面点情况，高度上漂移有所缓解

![Image Token: Rj9tbvKDRooXddxzzG8cAi0unKc](images/Rj9tbvKDRooXddxzzG8cAi0unKc.png)

## 3. mid360开源数据：人举着，1m高度；rosbag 整体表现较好

目前仅有开源数据，且mid360有负角度；具体要等我们数据采集到，进一步看

### 3.1 树的轮廓清晰，几乎看不到什么拖影；

![Image Token: WqOtbYOv8o6XPFxdhjncZ2Uinlh](images/WqOtbYOv8o6XPFxdhjncZ2Uinlh.png)

![Image Token: KDoVbfrtToW32ZxCXlgcPqBfnie](images/KDoVbfrtToW32ZxCXlgcPqBfnie.png)

![Image Token: UMgPbCHxGoPWpwx9BhFc12I9nVh](images/UMgPbCHxGoPWpwx9BhFc12I9nVh.png)





### 3.2 slam表现正常，测距可达70多米：

![Image Token: LuzLbAa1noTWrQxnTIfcw0U5nhg](images/LuzLbAa1noTWrQxnTIfcw0U5nhg.png)



### 3.3 78号场地

![Image Token: KYsrbPaW4o5CF9xXCQocMYNgnud](images/KYsrbPaW4o5CF9xXCQocMYNgnud.jpeg)



### 3.4 105号场地

![Image Token: UwVXbMXWKob2wNxpDbgc7waknmc](images/UwVXbMXWKob2wNxpDbgc7waknmc.jpeg)



### 3.5 其他场地：

![Image Token: YZtrbYgmoou6zExbnk6c0pmPncg](images/YZtrbYgmoou6zExbnk6c0pmPncg.jpeg)



![Image Token: V3NJbmeUXokKRzxY8xqc8nRfnVc](images/V3NJbmeUXokKRzxY8xqc8nRfnVc.jpeg)







## 4. mid360 我们数据(外场)：整体表现较好



### 4.1 105建图：

![Image Token: T6O7bl9lroyzDZxW3rHcRHYDn5w](images/T6O7bl9lroyzDZxW3rHcRHYDn5w.png)



![Image Token: HPivbLttOolAvXxdsNEcWNoHnyW](images/HPivbLttOolAvXxdsNEcWNoHnyW.png)



### 4.2 78场地建图：



![Image Token: NCHPbX5J6oCw7fxqxWucbGuRnib](images/NCHPbX5J6oCw7fxqxWucbGuRnib.jpeg)





105颠簸数据：比较平稳

![Image Token: GjRrbBwfjoWO6NxvpV9cgxFMnIe](images/GjRrbBwfjoWO6NxvpV9cgxFMnIe.png)









### 4.3 livox-105-定位数据

#### 4.3.1 定位数据1：

建图轨迹：

![Image Token: EQtabAedcoLFv6xZlFpcA4W0nqd](images/EQtabAedcoLFv6xZlFpcA4W0nqd.png)

定位轨迹：

![Image Token: MPKtbVIp1oJkeLxyyZucK7shn0c](images/MPKtbVIp1oJkeLxyyZucK7shn0c.png)

#### 4.3.2 定位数据2

建图：

![Image Token: PsU7bplwrouqeixfQmfcxKl3nbc](images/PsU7bplwrouqeixfQmfcxKl3nbc.png)

定位：

![Image Token: I02vbivF8oE9wYxvujFcVhK2nBe](images/I02vbivF8oE9wYxvujFcVhK2nBe.png)

livox-105-斜坡

![Image Token: VzWdbdXEEomz5SxmuXocDfqMnZt](images/VzWdbdXEEomz5SxmuXocDfqMnZt.png)



### 4.4 livox-78-定位数据

#### 4.4.1 定位1数据：

建图轨迹：

![Image Token: YDczbKuLqoJWy6xZ2iAcXP0vnxd](images/YDczbKuLqoJWy6xZ2iAcXP0vnxd.png)

定位轨迹：

![Image Token: StWHbsccyoq33FxkN4ic6i6gnzd](images/StWHbsccyoq33FxkN4ic6i6gnzd.png)

#### 4.4.2 定位数据2：

建图轨迹：

![Image Token: HRxkbaHI2o0jWdxGKHIclsHrnOb](images/HRxkbaHI2o0jWdxGKHIclsHrnOb.png)

定位轨迹：

![Image Token: IML3bByWroEqAhxS8vCcX3rdnYe](images/IML3bByWroEqAhxS8vCcX3rdnYe.png)

### 4.5 mid360与禾赛JT16建图对比

&#x20; 我们使用105场地，来观测禾赛JT16在该场景下的建图效果如下所示：

![Image Token: RRDzbLgfIoXo8LxsC9tc8iuanKe](images/RRDzbLgfIoXo8LxsC9tc8iuanKe.jpeg)

宏观上看，轮廓和mid360建图类似，我们将其放大，观测其点云质量较差，有风险：

（1）在树冠处，可以明显看出禾赛JT的点云数据也有类似速腾Ariy的“发射状”现象：

![Image Token: PKd7b5tXHoOHlvx7j0KcubEEnWc](images/PKd7b5tXHoOHlvx7j0KcubEEnWc.jpeg)

（2）进一步放大“发射状”点云，通过rviz上的测量工具可以测出其“长度”（error）达到80cm左右：

![Image Token: BFq8b4locoZRfkxQvAgch0L6nUe](images/BFq8b4locoZRfkxQvAgch0L6nUe.jpeg)

（3）JT16激光打到墙上留下的放射线：

![Image Token: VHKobSSZJowKDVx3LO9c9HytnDf](images/VHKobSSZJowKDVx3LO9c9HytnDf.jpeg)



（4）进一步寻找最容易体现点云细节和形状的建筑物以及户外设施，可以看到JT16的点云质量：

![Image Token: UfPObxH6dobiYfxD7Aac5XihnHh](images/UfPObxH6dobiYfxD7Aac5XihnHh.jpeg)

可以看出：mid360在建筑物表面上点云更均匀，树干处和单杠处轮廓清晰的多。更有利于后续的目标检测以及物体识别等功能的开发。











