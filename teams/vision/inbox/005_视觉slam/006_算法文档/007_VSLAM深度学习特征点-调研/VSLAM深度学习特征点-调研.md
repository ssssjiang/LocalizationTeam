# VSLAM深度学习特征点-调研

## 1. ORBSLAM3 + SuperPoint

只用特征点+描述子，没用匹配

https://zhuanlan.zhihu.com/p/1924501214256689633

https://arxiv.org/pdf/2506.13089



## 2. Light-SLAM

https://arxiv.org/abs/2407.02382

Light-SLAM: A Robust Deep-Learning Visual SLAM System Based on LightGlue under Challenging Lighting Conditions

只做前后两帧的track。

&#x20;



## 3. A real-time, robust and versatile visual-SLAM framework based on deep learning networks

也是前后两帧track

&#x20;



## 4. LIFT-SLAM: A deep-learning feature-based monocular visual SLAM method

只用描述子

https://www.sciencedirect.com/science/article/abs/pii/S0925231221007803

&#x20;



## 5. DK-SLAM: Monocular Visual SLAM with Deep Keypoint Learning, Tracking, and Loop Closing

只用描述子

https://www.mdpi.com/2076-3417/15/14/7838

&#x20;



## 6. Deep Learning for Visual SLAM: The State-of-the-Art and Future Trends

&#x20;



## 7. SL-SLAM

SL-SLAM: A robust visual-inertial SLAM based deep feature extraction and matching

https://arxiv.org/pdf/2405.03413v2

1. 前后帧track，coarse pose估计，使用关联上的观测优化当前帧位姿

2. 局部建图线程，当前关键帧与共视关键帧2D-2D匹配三角化新的地图点（多次推理）



## 8. Practical Deep Feature-Based Visual-Inertial Odometry

https://www.scitepress.org/Papers/2024/123202/123202.pdf?utm\_source=chatgpt.com

前后帧track，把LightGlue作为VINS-Mono的特征跟踪/匹配模块（前端替换）



## 9. AirVO: An Illumination-Robust Point-Line Visual Odometry

https://arxiv.org/pdf/2212.07595

1. 与上一个关键帧匹配

2. 关键帧双目匹配



## 10. SuperVINS: A Real-Time Visual-Inertial SLAM Framework for Challenging Imaging Conditions

https://arxiv.org/pdf/2407.21348

前后帧track

