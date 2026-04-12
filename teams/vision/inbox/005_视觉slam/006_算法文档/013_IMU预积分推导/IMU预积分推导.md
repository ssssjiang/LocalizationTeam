# IMU预积分推导

# 1. 预积分原始论文

https://zhuanlan.zhihu.com/p/635496502

1. 状态递推公式

![Image Token: KSIVbAk7Eou3vxxiMJecTMYynTf](images/KSIVbAk7Eou3vxxiMJecTMYynTf.png)

* 将状态量提出到等式一边，等式两边等价，记为相对运动增量

  1. 这个公式可以这么理解

     1. 公式各个部分表示的都是相对运动增量

     2. 左边是新起的表示运动增量的符号

     3. 中间是状态量推出的相对运动增量

     4. 右边是观测量推出的相对运动增量

     5. 状态和观测可以形成残差

![Image Token: SKBNbHUWLoLYuzx93Oaccb1unsQ](images/SKBNbHUWLoLYuzx93Oaccb1unsQ.png)

* 将观测量推出的相对运动增量展开

![Image Token: FnsHbd5xBoCJMixfYPScwj7rnnd](images/FnsHbd5xBoCJMixfYPScwj7rnnd.png)

![Image Token: DP8Vb9lRFod1pqxhEdgcbi1jnRb](images/DP8Vb9lRFod1pqxhEdgcbi1jnRb.png)

![Image Token: G780b5WiJopA6HxaTfTcNpEunwc](images/G780b5WiJopA6HxaTfTcNpEunwc.png)

* 观测模型可以得到

  1. 左边为使用观测数据地推出来的相对运动

  2. 右边为状态量做差得到的相对运动以及噪声项

![Image Token: F73Vb6qfJo1buTxaHfncNEk1nLb](images/F73Vb6qfJo1buTxaHfncNEk1nLb.png)

* 噪声项展开（为后面噪声递推做准备）

![Image Token: KfubbJ8FGoLbWIxrgOgcMkPrn1f](images/KfubbJ8FGoLbWIxrgOgcMkPrn1f.png)

![Image Token: YRTybStyAoLPxUxSmLUcczbDnKb](images/YRTybStyAoLPxUxSmLUcczbDnKb.png)

![Image Token: EnDsbJuwXoa0AaxHKgJcfusSnlc](images/EnDsbJuwXoa0AaxHKgJcfusSnlc.png)

* 观测模型的“使用观测数据地推出来的相对运动”与bg相关，拆分为bg的增量形式（vins也用了这个技术，避免bias变化时重新递推）

![Image Token: Vedrb02k6oHkw0xiU2hcGmZHnAf](images/Vedrb02k6oHkw0xiU2hcGmZHnAf.png)

* IMU边的定义

![Image Token: P0YjbHY2noEE3xxsmcscYXDPnAd](images/P0YjbHY2noEE3xxsmcscYXDPnAd.png)

* 噪声传播公式（为了计算IMU边的协方差）

![Image Token: EkT7bXCJio71t2x8V8lcSTbon6b](images/EkT7bXCJio71t2x8V8lcSTbon6b.png)

![Image Token: DDprbZUu9o0svnxhDKlcdfUonrd](images/DDprbZUu9o0svnxhDKlcdfUonrd.png)

![Image Token: WO3Ub3oocoyQyPx9XLycvBnonHc](images/WO3Ub3oocoyQyPx9XLycvBnonHc.png)

# 2. OKVIS2

&#x20;

okvis2的imu边继承自okvis，okvis是2014年的论文，预积分原始论文还没发表。论文声称借鉴的是这个论文。即MSCKF。但是实现和MSCKF也不一样。https://docs.openvins.com/propagation\_discrete.html



![Image Token: WuQgbEiRoozGNvxlLYLcOYw3nJf](images/WuQgbEiRoozGNvxlLYLcOYw3nJf.png)

p对q部分的导数，实现的是状态的传播，而不是误差状态的传播。并且对于旋转用的左扰动。

而且有些代码实现不明所以。

# 3. vins\_mono

推导过程与深蓝学院VIO课程完全一致。

![Image Token: SwpJbFBNRoi4MixlgsVcRMHgnkg](images/SwpJbFBNRoi4MixlgsVcRMHgnkg.png)



&#x20;

# 4. vins\_mono VS 预积分原始论文

使用了中值积分，公式更复杂一些。

预积分原始论文只推导了欧拉积分。

