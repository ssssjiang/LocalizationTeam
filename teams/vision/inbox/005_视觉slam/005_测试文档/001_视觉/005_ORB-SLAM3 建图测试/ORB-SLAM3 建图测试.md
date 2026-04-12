# ORB-SLAM3 建图测试

# 0. 测试结果

| sequence                 | slam (无闭环) | slam + loopClosing | reload map + slam + loopClosing | reload all traj map + slam + loopClosing | 备注           |
| ------------------------ | ---------- | ------------------ | ------------------------------- | ---------------------------------------- | ------------ |
| MK2-12\_lake2\_0.4m      | 0.194065   | 0.114767 (1次闭环)    | -                               | map rmse: 0.084264                       | 建图给下面两组加载    |
| MK2-12\_lake2\_0.5m      | 0.203743   | 0.135742 (1次闭环)    | 0.103183 (merge)                | 0.097887 (merge)                         |              |
| MK2-12\_normal\_z\_0.8m2 | 0.235567   | 0.260102 (1次闭环)    | 0.119491 (merge)                | 0.213187 (merge)                         | 全轨迹测试merge较晚 |
|                          |            |                    |                                 |                                          |              |
| MK2-12\_normal\_z\_0.4m  | 0.606807   | 0.311789 (2次闭环)    | map rmse: 0.083211              | map rmse: 0.070224                       | 建图给下面两组加载    |
| MK2-12\_normal\_z\_0.5m  | 0.143910   | 0.061494 (2次闭环)    | 0.062784 (merge + 2次闭环)         | 0.066426 (merge)                         |              |
| MK2-12\_normal\_z\_0.8m  | 0.183214   | 0.152108 (1次闭环)    | 0.157501 (merge)                | 0.101127 (merge)                         |              |
|                          |            |                    | 巡边建图                            | 全轨迹建图                                    |              |

okvis

| sequence                 | ORBSLAM3 Tracking thread pose | okvis2 vl\_slam/develop    | okvis2 private/songs/dev  |
| ------------------------ | ----------------------------- | -------------------------- | ------------------------- |
| MK2-12\_lake2\_0.4m      | 0.162099                      | 0.330790                   | 0.164514                  |
| MK2-12\_lake2\_0.5m      | 0.271353                      | 0.399799                   | 0.194985                  |
| MK2-12\_normal\_z\_0.8m2 | 0.300436                      | 0.260838                   | 0.154039                  |
|                          |                               |                            |                           |
| MK2-12\_normal\_z\_0.4m  | 0.427371                      | 0.237612                   | 0.197084                  |
| MK2-12\_normal\_z\_0.5m  | 0.179636                      | 0.235149                   | 0.276453                  |
| MK2-12\_normal\_z\_0.8m  | 0.288198                      | 0.174380                   | 0.191282                  |
| 备注                       | no loopClosing                | use wheel & stereo & calib | no wheel & stereo & calib |

注：evo metric 使用 --project\_to\_plane xy

okvis 参数

```c++
camera_parameters:
  timestamp_tolerance: 0.005
  sync_cameras: [0, 1]
  image_delay: 0.0
  online_calibration: {do_extrinsics: false, do_extrinsics_final_ba: false, sigma_r: 0.001,
                       sigma_alpha: 0.005}
  image_frequency: 12.0
  start_time: 0.0
  
imu_parameters:
  use: true
  a_max: 176.0
  g_max: 7.8
  sigma_g_c: 0.002
  sigma_a_c: 0.02
  sigma_bg: 0.01
  sigma_ba: 0.1
  sigma_gw_c: 2.0e-05
  sigma_aw_c: 0.002
  g: 9.81007
  g0: [0.001, 0.001, 0.002]
  a0: [0.1, -0.04, -0.12]
  T_BS: [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0,
         1.0]
         
wheel_encoder_parameters:
  use: false
  sigma_v: 0.01
  sigma_omega: 0.5
  perimeter: 0.7477
  halflength: 0.1775
  scale: 1194.0
  unobs_info: 1.0
  wheel_delay: 0.0
  max_wheel_delta: 1.0 # maximum wheel distance increment per time step [m]
  T_BS: [0.17190008159725867, -0.00890901354670151, 0.9850741082607248, -0.13789835917882473,
         0.01682632031011766, 0.9998397946759199, 0.006106282453182414, -0.011260197699349845,
         -0.9849706603719728, 0.015525501094798552, 0.1720224528011512, 0.3665219387023511,
         0.0, 0.0, 0.0, 1.0]
         
# frontend parameters
frontend_parameters:
    detection_threshold: 38.0 # detection threshold. By default the uniformity radius in pixels
    absolute_threshold: 20.0
    matching_threshold: 100.0 # BRISK descriptor matching threshold
    octaves: 0
    max_num_keypoints: 600 # restrict to a maximum of this many keypoints per image (strongest ones)
    keyframe_overlap: 0.58
    use_cnn: False
    parallelise_detection: True
    num_matching_threads: 4
    use_only_main_camera: false # if true, only camera0 is used for matchToMap and other operations (except matchStereo)
    max_frame_gap_seconds: 2.0 # maximum frame gap in seconds (trigger deactivation)
    use_detect_async_processing: false # enable asynchronous detection
```



1. 原代码在闭环阈值设置比较严格；需要适当放宽阈值来提高召回率

2. 加载经过Global BA的跨session地图对SLAM有收益

3. 测试参数

   ```yaml
   Camera.fps: 15

   ORBextractor.nFeatures: 600
   ORBextractor.scaleFactor: 1.2
   ORBextractor.nLevels: 4

   # IMU noise
   IMU.NoiseGyro: 0.002
   IMU.NoiseAcc: 0.02
   IMU.GyroWalk: 0.00002
   IMU.AccWalk: 0.002
   IMU.Frequency: 100.0
   ```

4. 详细

| sequence                 | slam (无闭环)                                                                                                                                                                               |                                                                                     | slam + loopClosing                                                                                                                                                                       |                                                                                     | reload map + slam + loopClosing                                                                                                                                                         |                                                                                     | reload all traj map + slam + loopClosing                                                                                                                                                |                                                                                     |                                                                                                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MK2-12\_lake2\_0.4m      |        max      0.454513      mean      0.172721    median      0.163465       min      0.01517&#x37;**&#x20;     rmse      0.194065**       sse      82.440745       std      0.088480  | ![Image Token: S5XFbf7RaoKqAOxzHgrcatV9nzd](images/S5XFbf7RaoKqAOxzHgrcatV9nzd.png) |         max      0.235182      mean      0.107458    median      0.105473       min      0.00457&#x33;**&#x20;     rmse      0.114767**       sse      28.832153       std      0.040300 | ![Image Token: IWYObYthboot14xBs9ZcTQcRntb](images/IWYObYthboot14xBs9ZcTQcRntb.png) | -                                                                                                                                                                                       | -                                                                                   | -                                                                                                                                                                                       | -                                                                                   | ![Image Token: CVYxb4AmboOXrtxOKBgcVmvon3b](images/CVYxb4AmboOXrtxOKBgcVmvon3b.png)                                                                                    |
| MK2-12\_lake2\_0.5m      |        max      0.498221      mean      0.186824    median      0.181442       min      0.00904&#x32;**&#x20;     rmse      0.203743**       sse      121.544369       std      0.081288 | ![Image Token: KWSObRzq0oFkKzxjDLucmxL2nae](images/KWSObRzq0oFkKzxjDLucmxL2nae.png) |        max      0.294392      mean      0.127073    median      0.128078       min      0.00188&#x36;**&#x20;     rmse      0.135742**       sse      53.950867       std      0.047730  | ![Image Token: ZOjCbEkrwoHSBrxjej0ckVnknVh](images/ZOjCbEkrwoHSBrxjej0ckVnknVh.png) |        max      0.351176      mean      0.092890    median      0.088227       min      0.00489&#x36;**&#x20;     rmse      0.103183**       sse      31.173594       std      0.044924 | ![Image Token: TlCwbJM9logNVyxBM94criNSnyh](images/TlCwbJM9logNVyxBM94criNSnyh.png) |        max      0.243599      mean      0.090515    median      0.088089       min      0.00373&#x38;**&#x20;     rmse      0.097887**       sse      28.055873       std      0.037270 | ![Image Token: M509byU9Lo1999x8WOTcwHfFnGc](images/M509byU9Lo1999x8WOTcwHfFnGc.png) | ![Image Token: PHHtbrKSRoat6nxSaATcpznQnLd](images/PHHtbrKSRoat6nxSaATcpznQnLd.png)![Image Token: CPbSbxRQ3oLbkdxkgNGcqmQlnbf](images/CPbSbxRQ3oLbkdxkgNGcqmQlnbf.png) |
| MK2-12\_normal\_z\_0.8m2 |        max      0.413081      mean      0.221037    median      0.216657       min      0.03198&#x39;**&#x20;     rmse      0.235567**       sse      61.873402       std      0.081453  | ![Image Token: AQL8bjBfFoYWbUxxgRNc0kahnkb](images/AQL8bjBfFoYWbUxxgRNc0kahnkb.png) |        max      0.425074      mean      0.245832    median      0.243866       min      0.03845&#x32;**&#x20;     rmse      0.260102**       sse      75.433131       std      0.084970  | ![Image Token: PsSqbkEdzoyQeyx3KCNcCwJOnHb](images/PsSqbkEdzoyQeyx3KCNcCwJOnHb.png) |        max      0.316104      mean      0.106725    median      0.095289       min      0.01844&#x34;**&#x20;     rmse      0.119491**       sse      15.919977       std      0.053737 | ![Image Token: PTLLbDvBjoriWnxHgyOc8xaHnjM](images/PTLLbDvBjoriWnxHgyOc8xaHnjM.png) |        max      0.531114      mean      0.174097    median      0.142906       min      0.01384&#x36;**&#x20;     rmse      0.213187**       sse      50.675183       std      0.123040 | ![Image Token: Pymfbp7EAooI18xwMCNc5qg0n23](images/Pymfbp7EAooI18xwMCNc5qg0n23.png) | ![Image Token: QSRLbyuWKo18nyxYYdJci5jknnb](images/QSRLbyuWKo18nyxYYdJci5jknnb.png)                                                                                    |
|                          |                                                                                                                                                                                          |                                                                                     |                                                                                                                                                                                          |                                                                                     |                                                                                                                                                                                         |                                                                                     |                                                                                                                                                                                         |                                                                                     |                                                                                                                                                                        |
| MK2-12\_normal\_z\_0.4m  |        max      1.464598      mean      0.508093    median      0.368498       min      0.19335&#x36;**&#x20;     rmse      0.606807**       sse      659.471935       std      0.331747 | ![Image Token: J4VYbfDy6oYWH3xMuGscg9Uvnjc](images/J4VYbfDy6oYWH3xMuGscg9Uvnjc.png) |        max      0.746152      mean      0.268973    median      0.207287       min      0.03228&#x30;**&#x20;     rmse      0.311789**       sse      169.441192       std      0.157689 | ![Image Token: QrRqboEOYoBloSxh0vRcDUHYnkh](images/QrRqboEOYoBloSxh0vRcDUHYnkh.png) | -                                                                                                                                                                                       | -                                                                                   | -                                                                                                                                                                                       | -                                                                                   | ![Image Token: CVFxbn4zNonQGbxQ2lLcTjlLnKn](images/CVFxbn4zNonQGbxQ2lLcTjlLnKn.png)z轴漂移                                                                                |
| MK2-12\_normal\_z\_0.5m  |        max      0.512050      mean      0.112657    median      0.083651       min      0.00822&#x35;**&#x20;     rmse      0.143910**       sse      76.461813       std      0.089547  | ![Image Token: EitAbWcG3oHe3SxUjE6cjcJtncc](images/EitAbWcG3oHe3SxUjE6cjcJtncc.png) |        max      0.205546      mean      0.054921    median      0.050354       min      0.00313&#x35;**&#x20;     rmse      0.061494**       sse      13.961351       std      0.027662  | ![Image Token: A1jhbwkxIoiutyxLkFZcGq0Fnrd](images/A1jhbwkxIoiutyxLkFZcGq0Fnrd.png) |        max      0.211512      mean      0.056975    median      0.053099       min      0.00236&#x34;**&#x20;     rmse      0.062784**       sse      14.553423       std      0.026377 | ![Image Token: VZAlbf8FWoezcSxdjjocTn8Pn0e](images/VZAlbf8FWoezcSxdjjocTn8Pn0e.png) |        max      0.209094      mean      0.057627    median      0.049622       min      0.00373&#x37;**&#x20;     rmse      0.066426**       sse      16.290787       std      0.033039 | ![Image Token: UTLTbtlWwoSn6NxsC23cNopfn8c](images/UTLTbtlWwoSn6NxsC23cNopfn8c.png) | ![Image Token: G68Ab6ZSZodQs5xdpUEcyz3Dngb](images/G68Ab6ZSZodQs5xdpUEcyz3Dngb.png)                                                                                    |
| MK2-12\_normal\_z\_0.8m  |        max      0.327210      mean      0.171991    median      0.166263       min      0.02385&#x30;**&#x20;     rmse      0.183214**       sse      60.488328       std      0.063139  | ![Image Token: BbhqbeUxIoN9nXxyXDZchNQmnKb](images/BbhqbeUxIoN9nXxyXDZchNQmnKb.png) |        max      0.239878      mean      0.146830    median      0.148200       min      0.02622&#x36;**&#x20;     rmse      0.152108**       sse      41.692398       std      0.039721  | ![Image Token: Lv6MbeTTqoLzFWxcUgQc7PGZnUb](images/Lv6MbeTTqoLzFWxcUgQc7PGZnUb.png) |        max      0.290467      mean      0.148601    median      0.151418       min      0.02617&#x32;**&#x20;     rmse      0.157501**       sse      44.701182       std      0.052195 | ![Image Token: Sd0ebmd4po1CPcxXrklc8EInntT](images/Sd0ebmd4po1CPcxXrklc8EInntT.png) |        max      0.263088      mean      0.088039    median      0.076489       min      0.00338&#x35;**&#x20;     rmse      0.101127**       sse      18.428280       std      0.049756 | ![Image Token: R8d2blLRSohzGcxxtszczQYcnbf](images/R8d2blLRSohzGcxxtszczQYcnbf.png) |                                                                                                                                                                        |

# 1. 闭环测试

## 1.1 闭环检测

```c++
int nBoWMatches = 20;
int nBoWInliers = 15;
int nProjMatches = 50;
int nSim3Inliers = 20;
int nProjOptMatches = 80;


fabs(phi(0))<0.008f && fabs(phi(1))<0.008f && fabs(phi(2))<0.349)
```

1. DBoW2寻找闭环候选关键帧

2. Sim3Solver RANSAC求解初始相对位姿

3. searhByProjection，投影匹配，优化位姿

4. searhByProjection，更严格的匹配搜索半径与汉明距离，重新引导匹配，优化位姿

5. 多个关键帧有三个通过验证即成功

6. 惯性模式下检查相对位姿变换的pitch和roll夹角足够小

## 1.2 阈值修改

```c++
int nBoWMatches = 20;
int nBoWInliers = 10;
int nProjMatches = 35;
int nSim3Inliers = 15;
int nProjOptMatches = 35;

if (fabs(phi(0))<0.04f && fabs(phi(1))<0.04f && fabs(phi(2))<0.349f)
```

## 1.3 闭环矫正

1. 通过求解的Sim3位姿传播，调整与当前帧相连的关键帧组位姿以及他们观测的地图点坐标

2. 闭环相连关键帧组依次投影到调整过的当前当前关键帧组中的每个关键帧，进行匹配，融合，新增或者替换当前关键中的地图点。

3. 进行本质图优化 (4DoF)，优化本质图中所有关键帧的位姿

4. 新建线程进行全局BA (要求小于200个关键帧，否则不执行)

## 1.4 测试结果

见上表

# 2. 加载地图测试

巡边建图，FullInertialBA，保存，重载地图，地图融合，SLAM

## 2.1 巡边建图/全轨迹建图

使用大圈数据模拟巡边建图效果，保存地图前添加运行一次 FullInertialBA

![Image Token: ACz4bn2bOo2POaxuWofcpXeCncf](images/ACz4bn2bOo2POaxuWofcpXeCncf.png)

## 2.2 地图融合

当前关键帧与非活跃地图（reload 地图）成功检测闭环，则进行地图融合

1. 根据位姿变换，把当前地图变换到融合帧所在地图

2. 如果IMU没有完全初始化，帮助IMU快速优化

3. 地图以旧换新

4. 融合新旧地图，生成树与地图点

5. 对缝合区域窗口进行了welding BA

![Image Token: GzvobyrfxoBZfzxhY8BcQdESnhd](images/GzvobyrfxoBZfzxhY8BcQdESnhd.png)

## 2.3 测试结果

见上表

# 3. 前置工作

[ ORB-SLAM3测试文档 \[Draft\]](https://roborock.feishu.cn/docx/CsHYd67zdopGuoxeWNqcBTAvn6d)

1. ORBSLAM3双目三角化依赖于极线矫正的双目立体匹配，双目行不对齐数据影响测试效果较严重，未加入测试

2. ORBSLAM3初始化时间很长，在IMU第三阶段初始化完成时，存在pose跳变，实验对比使用local map优化过后的全帧率相机pose

3. [Save map crash fix](https://github.com/UZ-SLAMLab/ORB_SLAM3/issues/443#issuecomment-1154814254)















