# SLAM change log

***

> 修改日期：2026/03/11
>
> 所属模块：OKVIS
>
> Commit ID： bdbf3e56
>
> BUGID：485327
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* reinit时重置wheel\_before\_pause\_，解决暂停时误触发MovedDuringPause问题

***

> 修改日期：2026/03/04
>
> 所属模块：OKVIS
>
> Commit ID： f3cd1e19
>
> BUGID：482308
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【WI】

* 优化打滑检测，加入倾斜检测

* 上机测试 [ 侧滑以及倾斜检测上机测试](https://roborock.feishu.cn/wiki/GReHwBESyitJBwkUqVrcC5a8nld)；斜坡数据打滑情况分析和benchmark\_v1.0批测 [ 斜坡上轮式侧滑分析](https://roborock.feishu.cn/wiki/CbnHwhWebiz8qtkXsYCcXhQxnih)

***

> 修改日期：2026/02/09
>
> 所属模块：OKVIS
>
> Commit ID： fe591552
>
> BUGID：475686
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* imu的acc\_bias收敛后，才发布视觉位姿

* [ okvis退桩位姿跳变](https://roborock.feishu.cn/docx/AsX8dMGhboVQdMxHw8pcG00mnHb)

***

> 修改日期：2026/02/09
>
> 所属模块：OKVIS
>
> Commit ID： b578a6ab
>
> BUGID：470938
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 修复数据队列逻辑bug导致初始化卡住问题

***

> 修改日期：2026/02/04
>
> 所属模块：OKVIS
>
> Commit ID： 590a6820
>
> BUGID：473682
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 过滤wheel静止时的imu数据，暂停恢复后使用imu和wheel融合递推

* [ 暂停后使用imu和wheel递推上机测试](https://roborock.feishu.cn/wiki/Bfzqw2W4qijMLrkvaljcfQY8nFb)

***

> 修改日期：2026/01/29
>
> 所属模块：OKVIS
>
> Commit ID： fc03b883
>
> BUGID：470976
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 检测imu数据方差，对应调整sigma值，提高颠簸场景位姿精度

* [ 颠簸路段数据分析](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd)

***

> 修改日期：2026/01/29
>
> 所属模块：OKVIS
>
> Commit ID： 4c7b4e7b
>
> BUGID：470973
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 增加基于视觉位姿的打滑检测，提高轮子打滑时位姿精度

* [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

***

> 修改日期：2026/01/29
>
> 所属模块：OKVIS
>
> Commit ID： d8869c1f
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 提高时间戳打印的精度，始终保留三维小数点

***

> 修改日期：2026/01/20
>
> 所属模块：OKVIS
>
> Commit ID： 4e708aa1
>
> BUGID：456841
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 修改`MaxMoveDuringPause`为0.35米，修改关于暂停的仿真代码，暂停后恢复时使用轮式做递推，修复WheelEncoder中sqrt\_info没有赋初值时恢复后偶发core的问题

* [ Bug 456841以及仿真时暂停恢复后轨迹异常的分析](https://roborock.feishu.cn/wiki/V4DpwAoHNivlaFktL4Gc6NOOnAb)

***

> 修改日期：2026/1/12
>
> 所属模块：OKVIS
>
> Commit ID： 1b16fa8b
>
> BUGID：457932
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 将deactivate放进reinit逻辑中

***

> 修改日期：2026/1/12
>
> 所属模块：OKVIS
>
> Commit ID： ee7c666c
>
> BUGID：461790
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* Okvis 官方更改

* [ okvis2官方改动](https://roborock.feishu.cn/docx/SSm6dIaYNom8hgxk8yOcbZSNnqd)

***

> 修改日期：2025/12/29
>
> 所属模块：OKVIS
>
> Commit ID： 0fdbc27f
>
> BUGID：394844
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug】

* 长时间追踪质量差时vslam重新初始化

* [ 当长时间图像追踪失败时重启](https://roborock.feishu.cn/wiki/Um9HwR9LpiGI3fkNFExcNb49nSg)

***

> 修改日期：2025/12/24
>
> 所属模块：OKVIS
>
> Commit ID： 5d2d73cd
>
> BUGID：446290
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【WI】

* 暂停后恢复时，如果特征匹配失败重新初始化时，添加lostcallback和checkinfo

***

> 修改日期：2025/12/23
>
> 所属模块：OKVIS
>
> Commit ID： e73b94d1
>
> BUGID：452237
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 暂停期间轮速计检测到移动则重新初始化

***

> 修改日期：2025/12/19
>
> 所属模块：OKVIS
>
> Commit ID： 90663809
>
> BUGID：446290
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 修复因keypont的index逻辑导致描述子异常的问题

***

> 修改日期：2025/12/17
>
> 所属模块：OKVIS
>
> Commit ID： d8dbf54b
>
> BUGID：446006
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 开opencl宏时，也用同一套描述子pattern，节省内存占用

***

> 修改日期：2025/12/12
>
> 所属模块：OKVIS
>
> Commit ID： a99d744f
>
> BUGID：449067
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【WI】

* 优化打印信息，信息更集中，减少打印

***

> 修改日期：2025/12/12
>
> 所属模块：OKVIS
>
> Commit ID： 76f0c809
>
> BUGID：446290
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【WI】

* 暂停后恢复时，如果特征匹配失败的话重新初始化

***

> 修改日期：2025/12/11
>
> 所属模块：OKVIS
>
> Commit ID： 19578010
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 修复因keypont的index逻辑导致描述子异常的问题

***

> 修改日期：2025/12/11
>
> 所属模块：OKVIS
>
> Commit ID： 7e717538
>
> BUGID：446009
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 增加草地点光流匹配

* 去除了runRansac3d2d

* [ okvis弓字间隔不均匀](https://roborock.feishu.cn/docx/GzePdKl8DojbVLxDVZIcqldoncb)

***

> 修改日期：2025/12/11
>
> 所属模块：OKVIS
>
> Commit ID： 03912a4b
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 将光流算法的源码文件增加到okvis中

***

> 修改日期：2025/12/11
>
> 所属模块：OKVIS
>
> Commit ID： 4e1f49b7
>
> BUGID：446006
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 解决内存缓慢增长问题，合并描述子pattern降低平均内存占用

* [ okvis内存问题分析与优化](https://roborock.feishu.cn/docx/WctyduIppoJKgoxboHgc8aKcnkc)

***

> 修改日期：2025/12/09
>
> 所属模块：OKVIS
>
> Commit ID： a774edb7
>
> BUGID：444201
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 将高频的LOG(INFO)改为VLOG, 使得多数info日志改为debug日志，精简用户端日志。

***

> 修改日期：2025/12/5
>
> 所属模块：OKVIS
>
> Commit ID： 1417b72d
>
> BUGID：441269
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 修复因后端keyframes持续累积导致的oom问题

***

> 修改日期：2025/11/26
>
> 所属模块：OKVIS
>
> Commit ID： 6e472e68
>
> BUGID：438968
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【精度提升】

* 将vz噪声设置和vx一样，解决相机遮挡时偶发z轴跳动大的问题

* [ 遮挡z轴跳动](https://roborock.feishu.cn/wiki/JybvwvouUi1bOhkz2nNcgihznBg)

***

> 修改日期：2025/11/09
>
> 所属模块：OKVIS
>
> Commit ID： 6c1ca212
>
> BUGID：416276
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【精度提升】

* 暂停期间vlsam不更新，节约算力，长时间暂停后vlsam不触发重新初始化

* [ vslam接入暂停消息](https://roborock.feishu.cn/wiki/HgsHwIfDAiGzjsk7DwGcks5nnp5)

***

> 修改日期：2025/11/07
>
> 所属模块：OKVIS
>
> Commit ID： 2938a325
>
> BUGID：428172
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【精度提升】

* 解决imu波动与图像下边沿错误匹配点带来的Z轴快速漂移

* [ Z轴快速漂移](https://roborock.feishu.cn/docx/WrdKduuuqoEmhSxR23FcQtv7nCb)

***

> 修改日期：2025/11/06
>
> 所属模块：OKVIS
>
> Commit ID： 76244235
>
> BUGID：427449
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【精度提升】

* 增加局部地图点，精度提升

* [ 局部特征点地图](https://roborock.feishu.cn/docx/GLQmdegproQVljxdZRFcAymEnwb)

***

> 修改日期：2025/11/04
>
> 所属模块：OKVIS
>
> Commit ID： f08b365c
>
> BUGID：407686
>
> 分支：vl\_slam/develop
>
> 修改人：  &#x20;

【性能优化】

* 双目使用GPU提点，每目cpu下降10%左右

***

> 修改日期：2025/10/27
>
> 所属模块：OKVIS
>
> Commit ID： b1788d80
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 轮速计码盘参数从sensor.yaml中读取

***

> 修改日期：2025/10/15
>
> 所属模块：OKVIS
>
> Commit ID： 097f8dc8
>
> BUGID：407686
>
> 分支：vl\_slam/develop
>
> 修改人：  &#x20;

【性能优化】

* Okvis 右目使用GPU提点，cpu下降约10%

***

> 修改日期：2025/10/14
>
> 所属模块：OKVIS
>
> Commit ID： 9c89fb48
>
> BUGID：415641
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【性能优化】

* 重投影误差在归一化相平面计算

* [ 重投影误差去除畸变模型](https://roborock.feishu.cn/docx/DaE5dsWDLoRDPWxI1uJc7ieqnlb)

***

> 修改日期：2025/10/10
>
> 所属模块：OKVIS
>
> Commit ID： c5348e29
>
> BUGID：413767
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug fix】

* 解决KF生成逻辑bug导致的极端情况下匹配点数量持续为0的问题

***

> 修改日期：2025/09/25
>
> 所属模块：OKVIS
>
> Commit ID： ac06ddd1
>
> BUGID：407389
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【新功能】

* 实现视觉打滑检测，并且在打滑期间降低odo阈值

* [ SlipDetector批测结果](https://roborock.feishu.cn/wiki/MGiwwLYaqiuaPfkjyurcTXehn4g)[ 打滑检测（SlipDetector）算法说明](https://roborock.feishu.cn/wiki/S2U1wCVzgiS6dEkVXkfcYsifnGc)

***

> 修改日期：2025/09/08
>
> 所属模块：OKVIS
>
> Commit ID： 16cb005a
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【调试日志增加】

* vio重启时，创建新的轨迹文件

***

> 修改日期：2025/09/08
>
> 所属模块：OKVIS
>
> Commit ID： 654841c6
>
> BUGID：401934
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【bug解决】

* 修复多次重启vio时的线程冲突

***

> 修改日期：2025/09/08
>
> 所属模块：OKVIS
>
> Commit ID： 5da0cdf3、190049e8
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人：  &#x20;

【参数优化】

* 优化bg sigma的值

* [ 3.75Hz Benchmark 数据运行结果](https://roborock.feishu.cn/wiki/NjKNwNYvviN06HkNPI3cqB2KnDg)

***

> 修改日期：2025/09/08
>
> 所属模块：OKVIS
>
> Commit ID： dd339690、f7329fc3
>
> BUGID：405470
>
> 分支：vl\_slam/develop
>
> 修改人：  &#x20;

【代码静态检查优化】

* 对于cppcheck出来的所有问题进行fix

* 修正cppcheck的版本提示信息

***

> 修改日期：2025/09/08
>
> 所属模块：OKVIS
>
> Commit ID： 85bf54c2、be1fad2d
>
> BUGID：403718
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【进程优先级变更】

* 线程优先级调到-1，减少对其他重要线程的影响

【代码错误fix】

* be1fad2d：detector异步线程参数传递改为值传递



***

> 修改日期：2025/09/05
>
> 所属模块：OKVIS
>
> Commit ID： 85bf54c2
>
> BUGID：402565
>
> 分支：vl\_slam/develop
>
> 修改人：  &#x20;

【可视化优化】

1. rerun升级到0.24.0

2. rerun画图时使用encoded image，减少带宽占用

3. 画图增加landmark id &#x20;

【重大变化】

1. 仿真时rerun要升级到0.24.0

***

> 修改日期：2025/09/04
>
> 所属模块：OKVIS
>
> Commit ID： 85bf54c2
>
> BUGID：402565
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【性能优化】

1. 解决编码器回滚、长时间静止导致VIO重置

***

> 修改日期：2025/09/02
>
> 所属模块：OKVIS
>
> Commit ID： 36aee11b、6313b6e4
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人： &#x20;

【编译优化】

1. 调整对于eigen的依赖，确保编译时使用代码库内的eigen

2. cppcheck调用方式优化

***

> 修改日期：2025/08/29
>
> 所属模块：OKVIS
>
> Commit ID： b8d07b643
>
> BUGID：399633
>
> 分支：vl\_slam/develop
>
> 修改人：   &#x20;

【性能优化】

* 副目提特征点、描述子l\_s\_v\_d1线程固定

* l\_s\_v\_d1绑定到CPU4

* l\_s\_v\_b绑定到CPU5

【后端绑核测试】

> * 将 vslam **后端运算**的主线程**绑定到 core 5&#x20;**&#x540E;，**后端运算耗时显著减少**：
>
> * 后端一次循环处理耗时，由 447ms 减少到 311ms；
>
> * 相同场景的数据上，vslam 帧率由 4.5hz 增加到 6.4hz；
>
> * l\_s\_v\_b 主线程的 cpu 占用，由 70% 增长到 95%；（符合预期）



***

> 修改日期：2025/08/28
>
> 所属模块：OKVIS
>
> Commit ID： a8253b65
>
> BUGID：399693
>
> 分支：vl\_slam/develop
>
> 修改人：&#x20;

【性能优化】

原代码有多处std::cout << "XX" << std::endl，上机时将打印至watchdog.log、引起阻塞，因此将std::cout修改为LOG(INFO)，std::cerr改为LOG(ERROR)

***

> 修改日期：2025/08/11
>
> 所属模块：OKVIS
>
> Commit ID： ed123b1b、192ffe49、f0dcaa21、a4920388
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人：&#x20;

【健壮性优化】

跑飞的检测与上报。

***

> 修改日期：2025/07/23
>
> 所属模块：OKVIS
>
> Commit ID： 0b056f22
>
> BUGID：-
>
> 分支：vl\_slam/develop
>
> 修改人：&#x20;

【结构调整】

okvis\_depend和入okvis，以便内外网同步。

***

[ OKVIS changelog](https://roborock.feishu.cn/wiki/C7UcwTmPXiAJ0akCzXrcxMcfnfa)

