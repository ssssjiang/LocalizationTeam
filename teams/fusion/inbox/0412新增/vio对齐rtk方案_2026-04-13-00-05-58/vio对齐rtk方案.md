# vio对齐rtk方案

## 背景要求

rtk数据不好时，使用视觉递推，rtk恢复后，使用rtk约束视pose.

## 方案介绍

### 1. 约束

a．rtk与vio帧时间的约束

b．vio帧建的位姿态约束

c．vio帧间的尺度和方向一致性约束（变换后相对位置尽可能不变）

含义：两点之间的距离和两点连线之间的方向

![画板 1](images/whiteboard_1_1776009961809.png)

### 2. 流程

类成员变量中有分别保存rtk和vio数据的循环buffer（size固定，进一个出一个），在rtk数据良好时一直存储数据。当rtk数据不好时，先copy循环buffer数据到指定变量，然后使用单帧push数据，这期间rtk值push好的rtk，视觉仍然是每一帧都保存。当达到切换rtk状态时，数据检查通过后（检查fusion的数据量，时间，距离等），开始aligne过程。

![画板 2](images/whiteboard_2_1776009964834.png)

### 3. 现状

基本流程打通，优化权重还没有调整好，角度有问题，如下黄色箭头为调整后的vio pose，与最下面图片中黄色的vio轨迹形状类似。

![Image Token: KMmCbnSHzoQfPGxHJorcro9Knzf](images/KMmCbnSHzoQfPGxHJorcro9Knzf.jpeg)

![Image Token: XRmFbGElmoU9qCxvrbgcQv2LnPe](images/XRmFbGElmoU9qCxvrbgcQv2LnPe.jpeg)

### 4. 问题及后续优化

1.添加rtk外参

2.其他数据验证

3.优化权重调整

### 5. 优化后效果

说明：黄色带箭头轨迹为经过rtk校正后的vio轨迹，桔黄色为原始的多帧对齐后的vio轨迹，绿色为rtk．

| 数据                            | 效果                                                                                                                                                                             | 不使用尺度因子效果                                                                                              | 备注                                                                                                                                                                                                                                       |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| bug487694,时间点32953-32980      | ![Image Token: E0CGbAJu0oKGaRxUNgLcvDBsnlf](images/E0CGbAJu0oKGaRxUNgLcvDBsnlf.jpeg)                                                                                           | ![Image Token: D08PbSkrDoiW3dxuD0ccSLkWnTe](images/D08PbSkrDoiW3dxuD0ccSLkWnTe.jpeg)优化后的vio pose形状变化更大 | 白色框内vio的pose有横移，可以使用rtk的pose校正到合理的位置![Image Token: GkMdbzcKjoh5GixCqFhcK7vnnkd](images/GkMdbzcKjoh5GixCqFhcK7vnnkd.gif)横移是因为vio打滑误判率较高，误判时odom的权重会降低，imu影响更大，积分出来就飘了，已经进优化代码了。                                                           |
| bug470159,&#xA;时间点24700-24800 | ![Image Token: C6TibcGcMoJJtMxwTgrcFwOPnld](images/C6TibcGcMoJJtMxwTgrcFwOPnld.png)                                                                                            | ![Image Token: FEN7bYnCJoBgHyxHxnkc1yzGnOd](images/FEN7bYnCJoBgHyxHxnkc1yzGnOd.jpeg)无差别                | 金黄色优化后箭头更靠近rtk                                                                                                                                                                                                                           |
| bug482646,时间点38281-38307      | ![Image Token: OIxAbIsEAozLrwxXkPlcvctjnLe](images/OIxAbIsEAozLrwxXkPlcvctjnLe.png)                                                                                            | ![Image Token: O7GGbBw7KouEuqxcXqWcFu7GnWg](images/O7GGbBw7KouEuqxcXqWcFu7GnWg.jpeg)对齐后与rtk偏差增加        | 金黄色优化后箭头更靠近rtk                                                                                                                                                                                                                           |
| bug478129,时间点27444-27515      | ![Image Token: IEZkbLGxGoEIRSxXES2cKzeMnGg](images/IEZkbLGxGoEIRSxXES2cKzeMnGg.jpeg)                                                                                           | ![Image Token: K7u6bBASHoZXysxcdp0cs9HVnHc](images/K7u6bBASHoZXysxcdp0cs9HVnHc.jpeg)                   | 保持不变                                                                                                                                                                                                                                     |
| bug478129,时间点27138-27330      | ![Image Token: CBRFb3E9Voo2jhxKRmacRnOAn5f](images/CBRFb3E9Voo2jhxKRmacRnOAn5f.png)调整权重优化后![Image Token: UCKdbFIkoojS34xz8EScWVkwnnd](images/UCKdbFIkoojS34xz8EScWVkwnnd.jpeg) | ![Image Token: WANlbvQHZoAQEUxuDbIcEDJMnNL](images/WANlbvQHZoAQEUxuDbIcEDJMnNL.jpeg)                   | ![Image Token: Ie32bccZko1BhoxOk4mcJQu5nOf](images/Ie32bccZko1BhoxOk4mcJQu5nOf.jpeg)这个绿点rtk时间是在27326，而桔黄色vio\_pose时间点是37324，到这里slam\_paused，上机的话这里的rtk固定解是不应该起作用的（**视觉与rtk时间相差2s以上不使用**），目前仅为了增加测试案例，仿真时还是使用该rtk数据，主要看调整后的效果。去掉尺度因子的效果如上 |
| bug489942时间点21246-21392       | ![Image Token: JX6TbSdowoDDBQx99UMcv59fnWz](images/JX6TbSdowoDDBQx99UMcv59fnWz.jpeg)                                                                                           | ![Image Token: Lef6b00ACoLagHxVQETcVF3mnxf](images/Lef6b00ACoLagHxVQETcVF3mnxf.jpeg)                   |                                                                                                                                                                                                                                          |
| bug48994229305-29337          | ![Image Token: OLGLbVIwuoxr24x1AgHc9dEBnFc](images/OLGLbVIwuoxr24x1AgHc9dEBnFc.jpeg)                                                                                           | ![Image Token: G9k5bUNjfo9q8ixlABhcksUinSg](images/G9k5bUNjfo9q8ixlABhcksUinSg.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊001682号日志时间点25678-25678     | ![Image Token: LAxgbDMHhoBeGtxsNUCckf53nbf](images/LAxgbDMHhoBeGtxsNUCckf53nbf.jpeg)                                                                                           | ![Image Token: TfFSbefZioHrrUxW6qUcgcWrn7f](images/TfFSbefZioHrrUxW6qUcgcWrn7f.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊000526号日志时间点29058-29278     | ![Image Token: ZBIIbxdfjovnBTxfr7dc75kwnWg](images/ZBIIbxdfjovnBTxfr7dc75kwnWg.jpeg)                                                                                           | ![Image Token: HI94bjKvPozZA1xUoyYchYkqn8e](images/HI94bjKvPozZA1xUoyYchYkqn8e.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊001284号日志时间点3460-3606       | ![Image Token: S3w7b4iAZo9KJ8xrQejczPuRnLf](images/S3w7b4iAZo9KJ8xrQejczPuRnLf.jpeg)                                                                                           | ![Image Token: FTxtbN4ehoP12uxFbxVccDNDnfc](images/FTxtbN4ehoP12uxFbxVccDNDnfc.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊000543号日志时间点22354-22718     | ![Image Token: LWmPb4QrWorSQpxHv6kc3qj4n9g](images/LWmPb4QrWorSQpxHv6kc3qj4n9g.jpeg)![Image Token: Z1f8bgha4o0TQzxS2rjc5QD9n5d](images/Z1f8bgha4o0TQzxS2rjc5QD9n5d.jpeg)       | ![Image Token: S2P3bSZ2dotlK1xqypVcQ6JBnPe](images/S2P3bSZ2dotlK1xqypVcQ6JBnPe.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊00572号日志时间点854-1131         | ![Image Token: Xx5Qb9AhUofZerxlFoic8uqtnMh](images/Xx5Qb9AhUofZerxlFoic8uqtnMh.jpeg)原始视觉vio就和rtk匹配误差不大                                                                         | ![Image Token: RBYVbYxqqoPjvTxRhGUcV5SxnPc](images/RBYVbYxqqoPjvTxRhGUcV5SxnPc.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊001573号日志时间点1487-1765       | ![Image Token: O6BcbWoyBoDz3Rx9xsWcJfhknSh](images/O6BcbWoyBoDz3Rx9xsWcJfhknSh.jpeg)原始视觉vio就和rtk匹配误差不大                                                                         | ![Image Token: XDbOb20j2oMnl2xRUmHc1vBlnpF](images/XDbOb20j2oMnl2xRUmHc1vBlnpF.jpeg)                   |                                                                                                                                                                                                                                          |
| 放羊001573号日志时间点1810-1953       | ![Image Token: Hmreb9AC5okA3HxB9tDco9Vyndd](images/Hmreb9AC5okA3HxB9tDco9Vyndd.jpeg)                                                                                           | ![Image Token: QBC6bzx0XosW4jxng0Jcg8S0n3g](images/QBC6bzx0XosW4jxng0Jcg8S0n3g.jpeg)                   |                                                                                                                                                                                                                                          |

**加入尺度相似性约束**，vio优化后的轨迹，仅靠近rtk一定范围内的pose会优化，整体轨迹变化较小;

**无尺度相似性约束**，vio优化后的轨迹，整体变化的可能性大，但具体变动到rtk固定解更近或者更远都有可能，具有偶然性。

