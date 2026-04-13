# FAST-LIVO2 硬件加速

* LIO 残差搜索与点面匹配：BuildResidualListOMP() 已经有 OpenMP 框架，但默认不生效；之前把openmp的线程数锁死为1了。

* LIO 状态估计主循环：点协方差、世界系变换、Jacobian/Hessian 组装都在大循环里，适合 OpenMP/TBB、Eigen 向量化、甚至 GPU batched linear algebra。

  * FAST-LIVO2/src/voxel\_map.cpp:372 FAST-LIVO2/src/voxel\_map.cpp:403&#x20;

  &#x20;    FAST-LIVO2/src/voxel\_map.cpp:446

* LIO 小规模特征值分解：平面初始化里大量 3x3 特征分解，适合换成 SelfAdjointEigenSolver、批量 SIMD，量大时也能做 GPU batched eigensolver。FAST-LIVO2/src/voxel\_map.cpp:49 FAST-LIVO2/src/

* 视觉直接法 EKF 更新：updateState() ，按点、按 patch 做双线性采样、梯度、残差、Jacobian，适合 CPU 多线程 + SIMD，也很适合 CUDA/OpenCL/VPI。FAST-LIVO2/src/vio.cpp:1650

FAST-LIVO2/src/vio.cpp:1689 FAST-LIVO2/src/vio.cpp:1748

* 视觉逆向组合更新：updateStateInverse() 同样是 patch 级密集计算，和上面一样适合 SIMD / GPU。FAST-LIVO2/src/vio.cpp:1538

* patch 提取与仿射 warp：getImagePatch()、warpAffine()、precomputeReferencePatches() 都是规则内存访问和插值运算，适合 SSE/AVX/NEON，也适合交给 OpenCV CUDA。FAST-LIVO2/src/vio.cpp

* 图像 resize / 灰度转换 / 去畸变：标准 OpenCV 操作，直接切到 cv::cuda / VPI / ISP/NPU 路线。FAST-LIVO2/src/vio.cpp:2254 FAST-LIVO2/src/vio.cpp:2059

* 图像金字塔：当前 createImgPyramid() 用 vk::halfSample 手工逐层降采样，能直接替换成 OpenCV/IPP/CUDA/VPI 后端。FAST-LIVO2/src/frame.cpp:56

* 第三方直接法梯度：rpg\_vikit 里已经有 cv::Sobel，这一类梯度图构建可直接吃 OpenCV 的硬件后端。FAST-LIVO2/3rdparty/rpg\_vikit/vikit\_common/src/img\_align.cpp:337

* IMU 传播：UndistortPcl\_not\_ros() 前半段 IMU 积分和协方差传播是固定维矩阵运算，适合 Eigen 向量化。FAST-LIVO2/src/IMU\_Processing.cpp:258

* IMU 去畸变点云：后半段对每个点反向补偿， per-point 并行，适合 OpenMP/SIMD/GPU。FAST-LIVO2/src/IMU\_Processing.cpp:356

* 颜色体素图批处理：YUV→RGB、颜色平滑、补洞、导出都在大循环里，适合 CPU 多线程或 GPU kernel，但它更像后处理，不是主里程计。FAST-LIVO2/include/colorVoxelMap.hpp:393 FAST-LIVO2/include/

colorVoxelMap.hpp:477 FAST-LIVO2/include/colorVoxelMap.hpp:540

* PCD 分块写出：这是 I/O，不是算力瓶颈，但如果频繁写盘，可异步线程化。FAST-LIVO2/include/colorVoxelMap.hpp:360
