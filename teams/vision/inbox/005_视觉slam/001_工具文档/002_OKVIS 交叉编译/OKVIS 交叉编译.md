# OKVIS 交叉编译

## 工具链（toolchain）

* 工程 build ：

  * 内网：ssh://git@gitlab2.roborock.com:10022/Butchart/build.git

  * 外网：https://gitlab1.roborock.com/Butchart/toolchain

* 在此工程下有 `aarch64-mr527-linux-gnu.cmake`



## 依赖的第三方库交叉编译（不包含在okvis/external中的）

* 代码库：

  * https://gitlab5.roborock.com/libaoyu/okvis\_depend

* 编译：

  ```plain&#x20;text
  cd third_party
  # 修改 do_prebuild_mr527.sh 中 toolchain 的路径
  ./do_prebuild_mr527.sh
  ```

* 交叉编译的第三方库会 `install` 至 `toolchain/aarch64-mr527-linux-gnu/aarch64-mr527-linux-gnu/sysroot/usr/lib `目录下

## OKVIS 交叉编译

* 代码库：

  * https://gitlab5.roborock.com/songshu/okvis，分支 vl\_slam/develop

* 编译：

  ```shell
  mkdir build_arm
  cd build_arm
  cmake ../  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo -DUSE_RERUN=OFF -DCMAKE_TOOLCHAIN_FILE=../aarch64-mr527-linux-gnu.cmake

  ```



## OKVIS 运行

*

* okvis 在编译完成后 build\_arm 目录下，存在可执行文件 `okvis_app_synchronous` 和运行时需读取的文件 `small_voc.yml.gz`；

* 用  toolchain 中提供的 strip 可以裁剪可执行文件： （如果觉得可执行文件太大，不方便）

  ```shell
  /path/to/build/toolchain/aarch64-mr527-linux-gnu/aarch64-mr527-linux-gnu/bin/strip --strip-unneeded okvis_app_synchronous
  ```

* 将下列文件拷贝到板子上可运行程序的目录下；（eg. /mnt/data/rockrobo/rrlog）

  1. `okvis_app_synchronous`

  2. `small_voc.yml.gz`

  3. 数据集：

  4. mower.yaml 文件；

  5. `toolchain/aarch64-mr527-linux-gnu/aarch64-mr527-linux-gnu/sysroot/usr/lib ` 目录；



     ```plain&#x20;text
     # 用 tar 打包文件夹可以保留软链接关系
     toolchain/aarch64-mr527-linux-gnu/aarch64-mr527-linux-gnu/sysroot/usr/lib 
     # 压缩
     tar cvzf xxx.tar xxx/
     # 解压缩
     tar xzvf xxx.tar
     ```

* 运行前：

  1. 配置拷贝的动态库可链接：

     ```shell
     export LD_LIBRARY_PATH=/mnt/data/rockrobo/rrlog/lib/:${LD_LIBRARY_PATH}
     ```

* 运行命令：

  ```shell
  ./okvis_app_synchronous ./mower.yaml ./0317_fence_night_50
  ```

