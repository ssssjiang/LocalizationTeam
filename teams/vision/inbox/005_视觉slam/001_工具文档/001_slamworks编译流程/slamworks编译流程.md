# slamworks编译流程

1. 编译准备

   1. 编译器版本：gcc/g++-9

   2. cmake版本：3.25

2. 在slam\_workspace仓库下，切换到分支：vl\_slam/develop

   ```bash
   git submodule update --init --recursive
   ```

如果没权限导致中断，手动下载有权限的代码。

submodule默认url是ssh，需要在gitlab2/gitlab3上配置ssh

* 双目vio代码及多线mlslam分支汇总：

（2026.01.12更新）

| repo                | 分支（割草机、扫地机（双目））          | 地址                                                                                              | 路径（相对于slam\_workspace）                                           |
| ------------------- | ------------------------ | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| slam\_workspace     | vl\_slam/develop         | gitlab3.roborock.com/slam/slam\_workspace                                                       | .                                                                |
| logparser           | vl\_slam/develop         | gitlab2.roborock.com/robot/logparserenkin出外网仿真：                                                 | slam\_workspace/logparser                                        |
| slam\_common        | vl\_slam/develop         | gitlab3.roborock.com/slam/slam\_common                                                          | slam\_workspace/slam\_common                                     |
| eigen               | v3.4.0                   | gitlab3.roborock.com/thirdparty/eigen-git-mirror                                                | slam\_workspace/slam\_common/third\_party/eigen                  |
| googletest          | v1.17.0                  | gitlab3.roborock.com/thirdparty/googletest                                                      | slam\_workspace/slam\_common/third\_party/googletest             |
| eskf                | develop                  | gitlab2.roborock.com/Butchart/Slam/eskf                                                         | slam\_workspace/eskf                                             |
| vslam               | vl\_slam/develop         | gitlab3.roborock.com/slam/vslam                                                                 | slam\_workspace/vslam                                            |
| vslam/okvis         | vl\_slam/develop         | 内网：gitlab3.roborock.com/slam/okvis外网：gitlab5.roborock.com/songshu/okvis                         | slam\_workspace/vslam/slam\_module\_vio/vio\_okvis\_system/okvis |
| RRSLAM              | cleaner/vl\_slam/develop | gitlab3.roborock.com/slam/RRSLAM                                                                | slam\_workspace/rrslam                                           |
| module\_fusion      | develop                  | gitlab2.roborock.com/Butchart/Slam/module\_fusion                                               | slam\_workspace/module\_fusion                                   |
| mlslam              | develop                  | gitlab2.roborock.com/Butchart/Slam/mlslam                                                       | slam\_workspace/mlslam                                           |
| mlslam/mlslam\_core | develop                  | 内网：gitlab2.roborock.com/Butchart/Slam/mlslam\_core外网：gitlab5.roborock.com/RockRobo/mlslam\_core | slam\_workspace/mlslam/mlslam\_core                              |
| Fast-livo2          | develop                  | 内网：gitlab2.roborock.com/robot/Fast-livo2外网：gitlab5.roborock.com/RockRobo/Fast-livo2             | slam\_workspace/Fast-livo2                                       |



* 编译宏

-DENABLE\_RRSLAM=True: 编译激光相关代码（需要有RRSLAM代码权限）

-DENABLE\_VSLAM=True: 编译视觉相关代码（需要有vslam代码权限）

-DENABLE\_FUSION=True: 编译融合相关代码（需要有module\_fusion代码权限）

-DENABLE\_MLSLAM=False: 编译多线激光相关代码（需要有mlslam代码权限）

-DENABLE\_FASTLIVO=False:编译三维重建相关代码（需要有Fast-livo2代码权限）

```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo -DENABLE_RRSLAM=False -DENABLE_VSLAM=True -DENABLE_FUSION=True -DENABLE_MLSLAM=False -DENABLE_RAW_ORDER=False -DENABLE_FASTLIVO=False
make -j10
```

* 配置文件路径：

  1. 内网机：

     * 日志路径：slam\_common/resources/ro/debug\_config.yaml

     NOTE(2025.03.24 tmp): exec: blocked\_cam\_id 改为2   #双目当单目使用

     * alg路径：

       * 在rrslam下编译（slam\_ros\_bridge）：rrslam/resources/ro/configs/alg.yaml

       * 在vslam下编译（slam\_module\_ros\_bridge）: vslam/resources/ro/configs/alg.yaml

     * sensor路径：在日志文件下

  2. jenkin出外网仿真：

     仿真包下：config/ro/

  3. 机器上：

     &#x20;/opt/rockrobo/cleaner/conf/vslam/configs/     (多线激光同vslam)

* 运行ros仿真

  ```c++
  roslaunch slam_ros_bridge slam_ros_bridge_lds.launch // 激光
  roslaunch slam_module_ros_bridge slam_ros_bridge_okvis.launch // 视觉+融合
  ./devel/lib/simulator/simulator --log            // 多线激光无launch
  ```



* Jenkins 出外网仿真

  1. 在内网jenkins网站下选择Mower\_VSlam\_Debug->Build with Parameters

     1. 扫地机：VSlam\_Debug；割草机：Mower\_VSlam\_Debug

  2. 在SLAM\_BRANCH选择分支（repo: slam\_workspace）

     * 注意：本地submodule的修改需要经过git add {submodule}，git commit 和git push origin

     * 在CMAKE\_BUILD\_TYPE下面的地方勾选编译宏ENABLE\_RRSLAM, ENABLE\_VSLAM, ENABLE\_FUSION

  3. 编译成功后，仿真软件包地址：

     1. 扫地机

        带vslam: smb://192.168.111.103/build/VSlam/Debug/BuildRelease

        不带vslam: smb://192.168.111.103/build/Slam/Debug/BuildRelease

     2. 割草机

        带vslam:

        北京：smb://192.168.111.103/mowerbuild/VSlam/Debug/BuildRelease

        苏州：smb://10.250.4.29/build/Mower/VSlam/Debug/BuildRelease

        不带vslam:&#x20;

        北京：smb://192.168.111.103/mowerbuild/Slam/Debug/BuildRelease

        苏州：smb://10.250.4.29/build/Mower/Slam/Debug/BuildRelease

