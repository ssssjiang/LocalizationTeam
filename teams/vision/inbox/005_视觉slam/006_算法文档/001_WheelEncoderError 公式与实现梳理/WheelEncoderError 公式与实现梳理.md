# WheelEncoderError 公式与实现梳理

## 1. 引言 (Introduction)

`okvis::ceres::WheelEncoderError` 是一个基于 Ceres Solver 的代价函数（Cost Function），它为视觉惯性SLAM系统提供来自轮式编码器的运动约束。其核心思想是：

1. **预积分（Preintegration）**: 将两个关键帧之间的轮式编码器原始读数（ticks）进行积分，得到一个相对位姿变换的"测量值"  $$T_{B_0B_1,meas}
   $$，以及该测量的不确定性（协方差 `P`）。

2. **构建误差**: 在后端优化时，这个预积分得到的相对位姿会与由优化变量（两个时刻的绝对位姿 $$T_{WB_0}
   $$ 和 $$T_{WB_1}
   $$）计算出的相对位姿 $$T_{B_0B_1,pred}
   $$ 进行比较，构建误差项。

3) **优化**: Ceres Solver 会调整状态量（例如 $$T_{WB_0}
   $$ 和 $$T_{WB_1}
   $$），以最小化这个误差项，从而将轮式编码器的里程计信息融合到整个SLAM系统中。



## 2. 运动学模型 (Kinematic Model)

该实现基于标准的差速驱动模型。假设机器人有两个驱动轮，轮距为 `wheel_base`。

* **输入**: 左右轮的线速度 $$  v_l  $$ 和 $$ 
   v_r  $$。这些速度由单位时间内的车轮转动距离计算得出：

  $$\Delta d_l = \frac{\text{ticks}_l}{\text{scale}} \times \text{perimeter}  ，
  v_l = \frac{\Delta d_l}{\Delta t}$$

  其中 `scale` 是编码器一圈的刻度数，`perimeter` 是车轮周长。

* **状态**: 机器人的中心线速度 $$  v  $$ 和航向角速度（yaw rate） $$\omega 
  $$。

  $$v = \frac{v_r + v_l}{2}  ，
  \omega = \frac{v_r - v_l}{\text{wheel\_base}}$$

  这里的 `wheel_base` 在代码中由 `2.0 * wheelEncoderParameters_.halflength` 定义。



## 3. 预积分 (Preintegration)

预积分的目标是在给定一段时间 $$[t_0, t_1]
$$ 内，仅利用轮速计读数计算出机器人从位姿 $$B_0$$ 到 $$B_1$$ 的相对变换 $$T_{B_0B_1}$$。这个过程在 `redoPreintegration` 和 `integrateEncoderMeasurement` 函数中实现。（**代码中先积分 S 系（wheel 系）的运动，再转换到 B 系下**）

假设：在一个微小时间段 $$\Delta t
$$ 内，假设线速度 $$v$$ 和角速度 $$\omega
$$ 恒定。

### 3.1 姿态积分 (Rotation)

航向角的变化量为：

$$\Delta\theta = \omega \cdot \Delta t $$

由于是平面运动，该旋转发生在Z轴上。对应的四元数增量为：

$$\Delta q = \begin{pmatrix} \cos(\frac{\Delta\theta}{2})  , 0 , 0,  \sin(\frac{\Delta\theta}{2}) \end{pmatrix} $$

姿态的迭代更新为：

$$q_{k+1} = q_k \otimes \Delta q_k $$

### 3.2 位置积分 (Translation)

位置的变化 $$\Delta p$$ 取决于运动形式：

* **直线运动** (当 $$  |\omega|  $$ 接近0时):

  $$\begin{pmatrix} \Delta x  ， \Delta y \end{pmatrix} = \begin{pmatrix} v \cdot \Delta t \cdot \cos(\theta_k) ， v \cdot \Delta t \cdot \sin(\theta_k) \end{pmatrix}$$

  其中 $$  \theta_k  $$ 是当前积分起始点的航向角。

* **圆弧运动** (当 $$  |\omega| \neq 0  $$ 时): 机器人以半径 $$  R = v/\omega  $$ 做圆弧运动。

  $$\begin{pmatrix} \Delta x ，  \Delta y \end{pmatrix} = \begin{pmatrix} \frac{v}{\omega}(\sin(\theta_k + \omega\Delta t) - \sin(\theta_k))，  \frac{v}{\omega}(-\cos(\theta_k + \omega\Delta t) + \cos(\theta_k)) \end{pmatrix}$$

位置的迭代更新为：

$$p_{k+1} = p_k + \Delta p_k $$

积分的最终结果是 `pose_integral_result_`，它代表了在传感器（Sensor）坐标系下的相对变换 $$T_{S_0S_1}$$ 。



## 4. 协方差传播 (Covariance Propagation)

为了量化预积分的不确定性，系统使用扩展卡尔曼滤波（EKF）的思想来传播协方差。

* **状态误差向量**: 定义在切线空间上的6自由度误差向量 $$\delta\xi = [\delta p^T, \delta\phi^T]^T$$，其中 $$  \delta p  $$ 是位置误差， $$  \delta\phi  $$ 是姿态误差。

* **传播公式**:

  $$P_{k+1} = F_k P_k F_k^T + Q_k $$

  其中 $$  P_k  $$ 是协方差矩阵，$$F_k$$ 是状态转移矩阵，$$Q_k$$ 是过程噪声协方差。

* **状态转移矩阵 $$  F_k  $$&#x20;**(State Transition Matrix):

它描述了误差如何随时间演化 $$\delta\xi_{k+1} \approx F_k \delta\xi_k$$。对于一个微小积分步骤，$$F_k$$ 近似为：

$$ 
    F_k = \begin{bmatrix}
    1 & 0 & 0 & 0 & 0 & \frac{\partial \Delta x}{\partial \theta_k} \\
    0 & 1 & 0 & 0 & 0 & \frac{\partial \Delta y}{\partial \theta_k} \\
    0 & 0 & 1 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1
    \end{bmatrix}
     $$

非零的偏导项 $$  \frac{\partial \Delta p_k}{\partial \phi_k}  $$ 体现了当前姿态误差对未来位置误差的影响，其具体形式与上述位置积分公式的求导一致。

* **过程噪声协方差 $$  Q_k  $$&#x20;**(Process Noise Covariance):

它对建模编码器测量中的噪声至关重要。噪声被假设为施加在线速度和角速度上的高斯白噪声，其方差由 `sigma_v` 和 `sigma_omega` 定义。系统采用随机游走（Random Walk）模型：

$$Q_k = \text{diag}(\sigma_v^2\Delta t, \sigma_v^2\Delta t, \epsilon, \epsilon, \epsilon, \sigma_\omega^2\Delta t)$$

* 位置噪声：方差与 $$  \Delta t  $$ 成正比。

* 姿态（yaw）噪声：方差与 $$  \Delta t  $$ 成正比。

* 对于不可观测量（Z 平移、roll 和 pitch 旋转），赋予一个很小的信息值 `unobs_info`（很大的协方差） ($$\epsilon$$)， 为保证数值稳定性目前调参为 1.0。

### 4.1 附录： F\_local 推导

#### 4.11 协方差传播（基于离散模型的雅可比推导）

为了量化预积分的不确定性，计算状态转移矩阵（雅可比矩阵），它描述了误差如何在一个离散的积分步内传播。

#### 4.12 离散状态转移模型

定义预积分量的状态 $$\boldsymbol{\xi}$$ 为其在积分起始坐标系 $$S_0$$ 下的相对位姿。其误差状态 $$\delta\boldsymbol{\xi}$$ 是一个在切线空间上定义的 6 自由度向量：

$$\delta\boldsymbol{\xi} =
\begin{bmatrix}
\delta\mathbf{p} \\
\delta\boldsymbol{\phi}
\end{bmatrix}
\in \mathbb{R}^6$$

在一个积分步 $$k$$ 中，从 $$t$$ 到 $$t+\Delta t$$，离散的状态更新方程可以写为：

$$\boldsymbol{\xi}_{k+1} = f(\boldsymbol{\xi}_k, \mathbf{u}_k)$$

其中 $$\mathbf{u}_k$$ 是控制输入（即计算出的 $$v$$ 和 $$\omega$$）。协方差传播需要计算状态转移矩阵 $$\mathbf{F}_k$$，它来自于误差状态的线性化传播关系：

$$\delta\boldsymbol{\xi}_{k+1} \approx \mathbf{F}_k \delta\boldsymbol{\xi}_k$$

#### 4.2 状态转移矩阵 $$\mathbf{F}_k$$ 推导

通过对名义状态施加微小扰动来推导 $$\mathbf{F}_k$$：

$$\mathbf{F}_k =
\begin{bmatrix}
\frac{\partial \delta\mathbf{p}_{k+1}}{\partial \delta\mathbf{p}_k} & \frac{\partial \delta\mathbf{p}_{k+1}}{\partial \delta\boldsymbol{\phi}_k} \\
\frac{\partial \delta\boldsymbol{\phi}_{k+1}}{\partial \delta\mathbf{p}_k} & \frac{\partial \delta\boldsymbol{\phi}_{k+1}}{\partial \delta\boldsymbol{\phi}_k}
\end{bmatrix}$$

**姿态误差传播：**

1. 名义状态更新：$$\hat{\theta}_{k+1} = \hat{\theta}_k + \omega \Delta t$$

2. 真实状态更新：$$\theta_{k+1} = \theta_k + (\omega + n_\omega)\Delta t$$

3. 令 $$\theta = \hat{\theta} + \delta\theta$$，代入得：$$\hat{\theta}_{k+1} + \delta\theta_{k+1} = (\hat{\theta}_k + \delta\theta_k) + (\omega + n_\omega) \Delta t$$，忽略噪声项，得到：$$\delta\theta_{k+1} \approx \delta\theta_k$$

**位置误差传播：$$\mathbf{p}_{k+1} = \mathbf{p}_k + \Delta\mathbf{p}_k(\theta_k)$$**

1. 代入扰动表达：$$\hat{\mathbf{p}}_{k+1} + \delta\mathbf{p}_{k+1} = (\hat{\mathbf{p}}_k + \delta\mathbf{p}_k) + \Delta\mathbf{p}_k(\hat{\theta}_k + \delta\theta_k)$$

2. 泰勒展开后得：$$\Delta\mathbf{p}_k(\hat{\theta}_k + \delta\theta_k) \approx \Delta\mathbf{p}_k(\hat{\theta}_k) + \frac{\partial \Delta\mathbf{p}_k}{\partial \theta_k} \delta\theta_k$$

3. 从而：$$\delta\mathbf{p}_{k+1} \approx \delta\mathbf{p}_k + \frac{\partial \Delta\mathbf{p}_k}{\partial \theta_k} \delta\theta_k$$

**各分块导数：**

$$\frac{\partial \delta\mathbf{p}_{k+1}}{\partial \delta\mathbf{p}_k} = \mathbf{I}_{3\times3}$$

$$\frac{\partial \delta\boldsymbol{\phi}_{k+1}}{\partial \delta\mathbf{p}_k} = \mathbf{0}_{3\times3}$$

$$\frac{\partial \delta\boldsymbol{\phi}_{k+1}}{\partial \delta\boldsymbol{\phi}_k} = \mathbf{I}_{3\times3}$$

$$\frac{\partial \delta\mathbf{p}_{k+1}}{\partial \delta\boldsymbol{\phi}_k}$$ 仅 $$Z$$ 轴分量非零，对应 $$\delta\theta_k$$；

注：由于是平面运动，只有航向角（yaw, $$\theta_k$$）的误差会对位置产生影响，因此只需要计算位置增量 $$  \Delta p_k = [\Delta x, \Delta y, 0]^T  $$ 对 $$  \theta_k  $$ 的偏导数。这里的 $$  \theta_k  $$ 是积分开始时刻的航向角 `current_yaw`。

1. **直线运动情况 (&#x20;**$$|\omega| < 10^{-6}
   $$**)**

位置增量为：

$$ 
    \Delta x = v \cdot \Delta t \cdot \cos(\theta_k) \\
    \Delta y = v \cdot \Delta t \cdot \sin(\theta_k)
     $$

&#x20;对 $$  \theta_k  $$ 求偏导：

$$ 
    \frac{\partial \Delta x}{\partial \theta_k} = -v \cdot \Delta t \cdot \sin(\theta_k) \\
    \frac{\partial \Delta y}{\partial \theta_k} = v \cdot \Delta t \cdot \cos(\theta_k)
     $$

* **圆弧运动情况**

位置增量为：

$$ 
    \Delta x = \frac{v}{\omega}(\sin(\theta_k + \omega\Delta t) - \sin(\theta_k)) \\
    \Delta y = \frac{v}{\omega}(-\cos(\theta_k + \omega\Delta t) + \cos(\theta_k))
     $$

对 $$  \theta_k  $$ 求偏导：

$$ 
    \frac{\partial \Delta x}{\partial \theta_k} = \frac{v}{\omega}(\cos(\theta_k + \omega\Delta t) - \cos(\theta_k)) \\
    \frac{\partial \Delta y}{\partial \theta_k} = \frac{v}{\omega}(\sin(\theta_k + \omega\Delta t) - \sin(\theta_k))
     $$

因此，状态转移矩阵 $$F_k$$ 的完整形式为：

$$ 
    F_k = \begin{bmatrix}
    1 & 0 & 0 & 0 & 0 & \frac{\partial \Delta x}{\partial \theta_k} \\
    0 & 1 & 0 & 0 & 0 & \frac{\partial \Delta y}{\partial \theta_k} \\
    0 & 0 & 1 & 0 & 0 & 0 \\
    0 & 0 & 0 & 1 & 0 & 0 \\
    0 & 0 & 0 & 0 & 1 & 0 \\
    0 & 0 & 0 & 0 & 0 & 1
    \end{bmatrix}
     $$



## 5. 误差函数与雅可比矩阵 (Error Function and Jacobians)

这部分在 `EvaluateWithMinimalJacobians` 中实现，是Ceres优化的核心。

### 5.1 误差定义 (Error Definition)

1. **坐标系统一**:

   * 预积分结果 $$  T_{S_0S_1, \text{meas}}  $$ 是在传感器（S）坐标系下的。

   * 优化变量位姿 $$T_{WB_0}$$, $$  T_{WB_1}  $$ 是在世界（W）和IMU (body)（B）坐标系下的。

   * 首先，使用 `T_BS` (IMU (body)到传感器的变换) 将预积分测量值转换到IMU (body)坐标系下：

     $$T_{B_0B_1, \text{meas}} = T_{BS} T_{S_0S_1, \text{meas}} T_{BS}^{-1} $$

2. **构建误差**:

   * 从优化变量计算出的"预测"相对位姿为：

     $$T_{B_0B_1, \text{pred}} = T_{WB_0}^{-1} T_{WB_1} $$

   * 误差 `error` ($$e$$) 被定义为"测量值"和"预测值"之间的差异，并映射到 6x1 的切线空间向量：

     $$e = \log(T_{B_0B_1, \text{meas}} \cdot T_{B_0B_1, \text{pred}}^{-1})^\vee $$

     其具体形式为：

     * 位置误差: $$  e_p = p_{B_0B_1, \text{meas}} - p_{B_0B_1, \text{pred}}  $$

     * 姿态误差: $$  e_\phi = 2 \cdot \text{vec}(q_{B_0B_1, \text{meas}} \otimes q_{B_0B_1, \text{pred}}^{-1})  $$

### 5.2 残差 (Residual)

为了使误差的各分量具有一致的尺度，并考虑其不确定性，使用信息矩阵（协方差的逆）进行加权：

$$\text{residual} = \sqrt{I} \cdot e $$

其中信息矩阵 $$I = P^{-1}$$。由于 $$  P  $$ 是在传感器坐标系下计算的，信息矩阵也需要转换到IMU (body)坐标系：

$$I_B = (\text{Ad}_{T_{SB}})^T I_S \text{Ad}_{T_{SB}} $$

其中 $$  \text{Ad}_{T_{SB}}  $$ 是 $$  T_{SB} = T_{BS}^{-1}  $$ 的伴随矩阵。（参考：Joan Solà, "A micro Lie theory for state estimation in robotics"）

### 5.3 雅可比矩阵 (Jacobian Matrix)

雅可比矩阵是残差相对于优化变量（位姿 $$  T_{WB_0}  $$ 和 $$T_{WB_1}$$）的导数。计算遵循链式法则：

$$J = \frac{\partial \text{residual}}{\partial T} = \frac{\partial \text{residual}}{\partial e} \frac{\partial e}{\partial T} = \sqrt{I_B} \frac{\partial e}{\partial T} $$

核心是计算误差 $$  e  $$ 相对于两个位姿的导数。这里位姿的扰动是在其切线空间中定义的。

* **对 $$  T_{WB_0}  $$ 的雅可比&#x20;**$$J_0$$:

  * 位置部分 $$  \frac{\partial e_p}{\partial p_0} = C_{B_0W}  $$

  * 姿态部分见附录，最终形式在 `J_err_T0_minimal` 中给出。

* **对 $$  T_{WB_1}  $$ 的雅可比&#x20;**$$J_1$$:

  * 位置部分 $$  \frac{\partial e_p}{\partial p_1} = -C_{B_0W}  $$

  * 姿态部分同样在 `J_err_T1_minimal` 中给出。

最后，代码使用 `PoseManifold::minusJacobian` 提供的 `J_lift` 矩阵，将切线空间下的雅可比转换到Ceres优化器实际使用的参数化空间中。&#x20;



#### 5.3.1 附录：雅可比姿态部分推导部

在此展开雅可比矩阵姿态部分的公式推导。

**1. 姿态误差定义**

姿态误差 $$e_\phi
$$ 定义为误差四元数 $$\delta q$$ 的向量部分的两倍：

$$e_\phi = 2 \cdot \text{vec}(\delta q) $$

其中，$$  \delta q = q_m \otimes (q_{pred})^{-1} = q_m \otimes (q_0^{-1} \otimes q_1)^{-1} = q_m \otimes q_1^{-1} \otimes q_0  $$

这里，$$q_m$$ 是测量的相对旋转，$$q_0$$ 和 $$q_1$$ 是两个时刻的绝对姿态。



**2. 对 &#x20;**$$T_{WB_0}
$$**&#x20;的求导**

我们对 $$q_0$$ 施加一个微小扰动 $$\delta\phi_0$$，对应的四元数为 $$\delta q_0 \approx [1, \frac{1}{2}\delta\phi_0^T]^T$$，使得新的姿态为 $$q'_0 = q_0 \otimes \delta q_0$$。扰动后的误差四元数为：

$$\delta q' = (q_m \otimes q_1^{-1}) \otimes q'_0 = (q_m \otimes q_1^{-1} \otimes q_0) \otimes \delta q_0 = \delta q \otimes \delta q_0 $$

根据四元数运动学，姿态误差 $$e_\phi$$ 对扰动 $$\delta\phi_0$$ 的导数为：

$$\frac{\partial e_\phi}{\partial (\delta\phi_0)} = C(\delta q) = C(q_m \otimes q_1^{-1} \otimes q_0) $$

其中 $$C(\cdot)$$ 是四元数对应的旋转矩阵。



**3. 对&#x20;**$$T_{WB_1}$$**&#x20;的求导**

同理，对 $$q_1$$ 施加扰动 $$q'_1 = q_1 \otimes \delta q_1$$，误差四元数变为：

$$\delta q' = q_m \otimes (q'_1)^{-1} \otimes q_0 = q_m \otimes (\delta q_1^{-1} \otimes q_1^{-1}) \otimes q_0 = (q_m \otimes \delta q_1^{-1} \otimes q_m^{-1}) \otimes \delta q$$

后半部分就是原始的误差四元数 $$\delta q$$。而前半部分 $$(q_m \otimes \delta q_1^{-1} \otimes q_m^{-1})$$ 是将扰动 $$\delta q_1^{-1}$$ 通过旋转 $$q_m$$ 进行坐标系变换，这正是伴随变换 $$\text{Ad}_{q_m}(\delta q_1^{-1})$$ 的定义。

所以，扰动后的误差可以表示为： $$ 
    \delta q' = \text{Ad}_{q_m}(\delta q_1^{-1}) \otimes \delta q
     $$；

这个表达式的物理意义是：对 $$q_1$$ 的一个微小扰动 $$\delta\phi_1$$，等效于在测量坐标系（由 $$q_m$$ 定义）下施加一个 $$-\delta\phi_1$$ 的扰动，然后这个扰动被左乘到原始的误差四元数 $$\delta q$$ 上。

&#x20;当一个四元数 $$\delta q$$ 被一个微小的旋转 $$\Delta q_{rot}$$ (对应旋转向量 $$\Delta\phi
$$ 左乘时，即 $$\delta q' = \Delta q_{rot} \otimes \delta q$$，其误差向量的一阶变化为 $$\Delta e_\phi \approx \Delta\phi$$。

在我们的情况中，这个微小的左乘旋转向量是 $$\text{Ad}_{q_m}(-\delta\phi_1)$$。根据伴随变换的性质，它等于 $$C(q_m)(-\delta\phi_1)$$。

因此，误差向量的变化量为：

&#x20;$$  \Delta e_\phi \approx C(q_m)(-\delta\phi_1) = -C(q_m)\delta\phi_1  $$

所以，我们得到了理论上的雅可比矩阵：

&#x20; $$  \frac{\partial e_\phi}{\partial (\delta\phi_1)} = -C(q_m)  $$

代码实现 `J_err_T1_minimal` 计算的为 $$-C(\delta q)$$，这是一个在相对旋转较小时的有效近似。



## 6. 参考文献

* &#x20;Joan Solà, "A micro Lie theory for state estimation in robotics". （II-F *The adjoint, and the adjoint matrix*）



