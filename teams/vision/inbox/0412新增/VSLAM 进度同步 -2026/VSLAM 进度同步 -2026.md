～表示已经清理掉截止日期的进展情况。可以继续自行更新进展，周会同步。

# 20260406 \~

# 20260406

* **割草机内外参标定与检测**

  > **本周进展**
  >
  > * 售后标定超时 & 内存优化分支； `@邱冰冰` `@李波`
  >
  >   * 通过标准：耗时 ～ 5min，内存消耗 < 500M；测试要求：售后标定通过，机器正常割草；
  >
  >   * 完成连调，已发版；
  >
  >     Bug#492211 - Butchart-售后标定模块-耗时 & 内存占用过多 - Butchart
  >
  >     http://192.168.111.52/index.php?m=bug\&f=view\&t=html&=\&bugID=492211
  >
  > * 相机分辨率问题：售后标定后内参数据异常（W1088,H1280 vs MCT W640,H544），根因是售后标定只更新外参，内参仍用原厂数据 ；
  >
  >   * 结论：驱动 `@宗志勇` 写入 e2 时，图像长宽交换，分辨率除 2；[ 割草机相机标定流程梳理](https://roborock.feishu.cn/wiki/LjGuwdGxCiLegzkyjEWcrtt1nUh)
  >
  > * Flore MK2 相机参数配置； Done `@邱冰冰`
  >
  >   * [消息链接](https://applink.feishu.cn/client/message/link/open?token=Amk6d869gkvTadH7T36AzMY%3D)；
  >
  > * GAIA 适配双目标定：MCT 中屏蔽遮挡检测，遮挡检测前置；
  >
  >   * [消息链接](https://applink.feishu.cn/client/message/link/open?token=Amj4oU8xR0AEadH%2BBGpADMc%3D) 装备组 `@杨承川` 接手代码和功能，分两步：
  >
  >     * 新品导入，由装备组符合遮挡检测；
  >
  >     * 老品目前仍由 MCT 做遮挡检测，后续会做老品改造；
  >
  > * &#x20;lumos 适配双目标定； Done  `@邱冰冰`
  >
  > * Flora 欧菲模组 tuning 验证； `@白世杰`
  >
  >   * [ Butchart 双目tuning结果确认](https://roborock.feishu.cn/wiki/QezWw3AcoitBgpkQHSycc6jrnXc?sheet=Z9zq1B\&table=tbl8Gq5BYS0ueMBq\&view=vewOUFEBLC)
  >
  >   * 标定板夜间数据不再需要评估； [消息链接](https://applink.feishu.cn/client/message/link/open?token=AmnKVGcoAgy%2Bacp4Zh0BC7g%3D)

  * Action

    * GAIA MCT 前视双目标定验证； `@邱冰冰` &#x20;

      1. threshold\_config\*.json 配适；

      2. 新 8 字轨迹配适；

      3. 标定结果验证；

    * GAIA MCT 后目及侧目标定配适；`@邱冰冰` &#x20;

      1. 验证后目侧目内参；

      2. 后目及侧目标定配适；

      3. 支持仅标定外参，输出到  result.json（装备卡控阈值），不写入 e2；

    * Flore MK2 行差大，标定失败； `@邱冰冰`

    * 售后标定：`@邱冰冰`

      * 降本治具验证； &#x20;

        * 私包（不使用地面 marker 的版本）验证；

    * CIIQC 站维护； `@江建文`

    * CQIQC 站维护；`@李波`

    * 其他待办：

      * <span style="color: rgb(143,149,158); background-color: inherit">MCT\IQC 后续再尝试降低计算时间/数据量；</span>

      * 售后标定：

        * 耗时优化：

          * &#x20;[ 售后标定耗时优化](https://roborock.feishu.cn/wiki/HYFswArkjipUUgkQCKecQei3nPf)中列出 todo 优化方案；

        * 降本方案治具验证：[ 售后标定二维码测试](https://roborock.feishu.cn/wiki/Sdalwi7QTiX1czk3orscAMNjnHg)

          * 窄距三行版本，一致性下降原因分析；&#x20;

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查 （数值差异）

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

        * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

          * 最终的 refine 去掉重投影误差大的数据（TODO）

          * 代码合入

            * Monet B3, versa B2

* **OKVIS-VIO 优化**

  > **本周进展**
  >
  > *

  * 持续优化 okvis `@郭科`

    * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

    * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)

      * 转弯区域精度变低（偏差 10cm 以内）

      * 序号 3 的尺度偏差问题分析；

  * 其他待办：

    * 先光流，后描述子匹配补点方法 （设计方案） `@白世杰` （存档）

      * [ 光流追踪与描述子匹配融合算法调研](https://roborock.feishu.cn/wiki/LKysw3ioJi1ZADkF3K6cMhQRnkf)&#x20;

      * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * VIO 初始化逻辑：启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias `@郭科`

    * 跟丢的逻辑设计&#x20;

* **深度学习特征点描述子引入**

  > **本周进展**
  >
  > * alike 引入 VIO  `@郭科`
  >
  >   * [ okvis应用alike-n](https://roborock.feishu.cn/docx/DrNjdpBDMo9QaJxZgLHcj1Ksntc)
  >
  >   * 精度：感知提供原版端侧后处理库，测试结果和感知对齐；（7HZ 情况下可对齐）
  >
  >   * 耗时：前端处理一帧 1s -> 简化逻辑，减少耗时，对精度影响不大，前端匹配耗时缩减到 60 - 70 ms；
  >
  >   * Maplab + alike  建图重定位测试（跨视角，跨季节）；`@白世杰`[ mapping接入浮点描述子](https://roborock.feishu.cn/wiki/D6sVw0ketiX70ZkXE2FcIWTUn2c)
  >
  >     * 打通建图 & 重定位测试；
  >
  >     * 批量测试中；

  * Action

    * alike 引入 VIO  `@郭科`

      * [ okvis应用alike-n](https://roborock.feishu.cn/docx/DrNjdpBDMo9QaJxZgLHcj1Ksntc)

      * <span style="color: inherit; background-color: rgba(255,246,122,0.8)">匹配效果：和感知对齐； alike 点的可重复性，匹配召回率，不如 brisk</span>

      * （低优先级）量化模型差异：评估板子上精度的退化；（板子上还可能有 bug ）

    * Maplab + alike  建图重定位测试（跨视角，跨季节）；`@白世杰`

      * 测试重定位精度 & 召回率的提升；（进行中）

      * 代码提 pr；

      * 分析在线建图 & 离线建图结论差异的成因；

        * 离线建图 alike & brisk 相近（参数没有更新到最优）

        * 在线建图 alike 表现更好；

      [ mapping接入浮点描述子](https://roborock.feishu.cn/wiki/D6sVw0ketiX70ZkXE2FcIWTUn2c)

  * TODO

    * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图；

* **Okvis 全局图与回环检测**

  > **本周进展**
  >
  > * 通道建图需求 ，HF2.2`@李波`[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink)&#x20;
  >
  >   * [ 通道建图测试](https://roborock.feishu.cn/wiki/PUAtw4HsNikT2Vk7XYMc7q8onSf?from=from_copylink) bug 分析；
  >
  > * 通道数据采集：`@李波` `@刘博`
  >
  >   * 2 组连续  3 次正反穿过通道的数据；
  >
  >   * 2 组连续建 3 个不同的通道，再反向穿过的数据；
  >
  >   * 跟进数据解析问题 `@刘博` `@黄亮`

  * 通道建图需求 ，HF2.2`@李波`[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink) [ 通道建图测试](https://roborock.feishu.cn/wiki/PUAtw4HsNikT2Vk7XYMc7q8onSf?from=from_copylink)

    * 发布 7hz 的建图轨迹；

    * 建图失败的情况下，不发布轨迹，导航需记录通道属性，vslam / rtk 通道，打印日志，以便后续建图算法优化；

    * 导航连调测试；

    * [ 通道视觉建图接口对齐 - 4.7](https://roborock.feishu.cn/wiki/WCwvwhc9ziLdvPkCfAFcoKePnRc)

  * 通道建图需求 ，HF3.0 [ 通道多 Session 地图合并设计](https://roborock.feishu.cn/wiki/GpaNwZthmiWwubkwYwocExx1nNc)

    * 支持用 vimap 做重定位，省去转 sumamry map； `@刘博`

      1. relocMapRootDir\_ / 独立 reloc 数据集根目录；（pr 中

      2. 重定位 TUM 输出 T\_G\_R = T\_G\_I \* T\_IR；使得重定位结果可以直接和 rtk 轨迹做 evo 评估；（pr 中

      3. 地图合并的版本上，清理生成 summary map，简化逻辑；（pr 中

    * 地图合并：  &#x20;

      1. 地图合并频率；    `@刘博`  （pr 中

         1. 重定位效果决策是否新建地图；

      2. RelocAndBuild 新状态的加入； `@刘博` （pr 中
         [ 地图合并与 RelocAndBuild 新状态的加入](https://roborock.feishu.cn/wiki/XTlhw0D6jiZIG9kg5oOcj6O6nNc)

      3. 地图合并算法；Done     `@江建文`  [ 地图合并实验](https://roborock.feishu.cn/wiki/Ah30wXIbniPDVPkfs9fcSjy1npc)

      4. 地图更新算法；`@刘博` `@江建文`

  * TODO

    * Maplab PGO （存档）  `@江建文`[ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)

    * Maplab Mapping & relocal 持续优化

      * 子图划分方案：判断回头进行子图划分 ( 存档）

        * [ 基于折返约束的子图切分策略优化与实验分析](https://roborock.feishu.cn/wiki/KQnKwXlHqilLDlknVQycMMDjnmd)

      * maplab 跟踪中加入光流，测试开光流的效果 （存档）

        * [ VIO 与 Gyro 作为旋转先验的跟踪与建图效果分析](https://roborock.feishu.cn/wiki/U2jHwSOXlixRBmk0oDUcSHznnBh)

    * 重定位效果的优化： `@刘博`

      1. maplab + 光流；（可以做快速的验证） &#x20;

      2. 评估单目建图是否可行；&#x20;

      3. 评估重定位结果对 vio 精度的影响；

    * 在线 Maplab 建图 `@宋姝`

      * 子图内部 100 关键帧数测试；`@宋姝`

      * 重定位精度、召回率精度测试  [ reloc-self\_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e) [ Relocalization analysis](http://roborock.feishu.cn/wiki/PtlzwEmNHiYYTqk8ZuxcULFinwb)（调优中）

        * 交叉 reloc 存在多个问题，需要进一步分析：

          * 重定位召回率低；（大部分 < 50%）

          * 重定位轨迹精度低；（参数，landmark 质量）

          * 考虑轨迹的方向，类别（弓字 / edge）&#x20;

      * Todo: online relocalization; `@宋姝`

    * 全局图工作项： [ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * maplab mapping 优化

      * 创建地图评分机制，区域分块好特征点评分

      * Faiss 的码表固定

      * 地图质量检测

        * 上报优化成功/失败

        * 场地过于空阔，有效点特别远

    * 轻量化，解决多地图、支持灵活的增、删区域

    [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)





# 20260330

* **割草机内外参标定与检测**

  > **本周进展**
  >
  > * 售后标定：`@邱冰冰` `@宋姝`
  >
  >   * 超时问题：[ 售后标定耗时优化](https://roborock.feishu.cn/wiki/HYFswArkjipUUgkQCKecQei3nPf) [ 售后标定一致性分析](https://roborock.feishu.cn/wiki/VGE4wvbR8izr1LkMfymcGLehnez)
  >
  >     * 限制 local ba 窗口大小后，耗时明显下降；（已合入 master)
  >
  >     * 三次标定一致性符合期望；
  >
  >     * 调参方案：影响 marker 精度，不可用； [消息链接](https://applink.feishu.cn/client/message/link/open?token=Amj4oU8xR0AEacn4P0WBTMI%3D)
  >
  >       `params.maxVisibleFramesPerMarker = 30;`
  >
  >       `params.minBaseLine = 0.07`
  >
  >   * Versa OOM 问题：
  >
  >     * Lidar 标定是大头（双目：lidar = 600M : 1.x G）
  >
  >     * 双目标定优化：[ 标定内存优化](https://roborock.feishu.cn/wiki/U0MFwFFaIiZQmJkOFE7cLtfwn9d)
  >
  >       * 当前售后标定，内存消耗 ～ 400M，相较 versa-OOM 测试（建图中，600M)，有明显下降；
  >
  >   * 降本方案治具验证：[ 售后标定二维码测试](https://roborock.feishu.cn/wiki/Sdalwi7QTiX1czk3orscAMNjnHg) `@邱冰冰` [yaw 误差 vio 精度影响的估计](https://applink.feishu.cn/client/message/link/open?token=Amj4oU8xR0AEacqNwxqADMs%3D)
  >
  >     * 三行 yaw 极差 1 degree&#x20;
  >
  >     * 两行极差 1.5 deg
  >
  >     * 两行 + ground 极差 < 1deg
  >
  >     * <span style="color: inherit; background-color: rgba(255,246,122,0.8)">窄距三行：1.3 deg  </span>
  >
  > * 解析数据工具更新 ； done `@邱冰冰`
  >
  >   * `@姚远` 新工具兼容旧格式；

  * Action

    * 售后标定：`@邱冰冰`

      * 超时 & 内存优化分支，<span style="color: inherit; background-color: rgba(255,246,122,0.8)">联调测试中</span>； &#x20;

        * <span style="color: inherit; background-color: rgba(255,246,122,0.8)">出包，提供测试版本；</span> `@邱冰冰` &#x20;

        * 测试要求：售后标定通过，机器正常割草；

        * 通过标准：耗时 ～ 5min，内存消耗 < 500M；

        * TODO: [ 售后标定耗时优化](https://roborock.feishu.cn/wiki/HYFswArkjipUUgkQCKecQei3nPf)中列出 todo 优化方案；

      * 相机分辨率问题：售后标定后内参数据异常（W1088,H1280 vs MCT W640,H544），根因是售后标定只更新外参，内参仍用原厂数据 ；

        * 方案讨论中

      * 降本方案治具验证：[ 售后标定二维码测试](https://roborock.feishu.cn/wiki/Sdalwi7QTiX1czk3orscAMNjnHg)

        * 窄距三行版本，一致性下降原因分析；&#x20;

    * Flore MK2 相机参数配置；`@邱冰冰`&#x20;

      * Bug#493489 - 【WI】【MK2】【设变】MK2相对MK1的结构参数适配 双目上位机标定文件推送&#x20;

      http://192.168.111.52/index.php?m=bug\&f=view\&t=html&=\&bugID=493489

    * GAIA & lumos 适配双目标定； `@邱冰冰` &#x20;

      1. 新机型配适；

      2. MCT 床尺寸、运动轨迹变更：

         1. 持续跟进，验证双目标定效果；

         2. MCT 中屏蔽遮挡检测，遮挡检测前置；

    * CIIQC 站维护； `@江建文`

    * CQIQC 站维护；`@李波`

    * Flora 欧菲模组 tuning 验证； `@白世杰`

      * [ Butchart 双目tuning结果确认](https://roborock.feishu.cn/wiki/QezWw3AcoitBgpkQHSycc6jrnXc?sheet=Z9zq1B\&table=tbl8Gq5BYS0ueMBq\&view=vewOUFEBLC)

      * （确认夜间数据是否需要评估，<span style="color: inherit; background-color: rgba(255,246,122,0.8)">感知</span> @王锐 & 定位）

    * 其他待办：

      * <span style="color: rgb(143,149,158); background-color: inherit">MCT\IQC 后续再尝试降低计算时间/数据量；</span>

      * 售后标定方案

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查 （数值差异）

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

        * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

          * 最终的 refine 去掉重投影误差大的数据（TODO）

          * 代码合入

            * Monet B3, versa B2

* **OKVIS-VIO 优化**

  > **本周进展**
  >
  > *

  * 持续优化 okvis `@郭科`

    * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

    * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)

      * 转弯区域精度变低（偏差 10cm 以内）

      * 序号 3 的尺度偏差问题分析；

  * 其他待办：

    * 先光流，后描述子匹配补点方法 （设计方案） `@白世杰` （存档）

      * [ 光流追踪与描述子匹配融合算法调研](https://roborock.feishu.cn/wiki/LKysw3ioJi1ZADkF3K6cMhQRnkf)&#x20;

      * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * VIO 初始化逻辑：启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias `@郭科`

    * 跟丢的逻辑设计&#x20;

* **深度学习特征点描述子引入**

  > **本周进展**
  >
  > * alike 引入 VIO 排期 `@郭科`[ okvis应用alike-n](https://roborock.feishu.cn/docx/DrNjdpBDMo9QaJxZgLHcj1Ksntc)
  >
  >   * 打通 alike 接入和板端测试；
  >
  > * Maplab + alike  建图重定位测试（跨视角，跨季节）；`@白世杰`[ mapping接入浮点描述子](https://roborock.feishu.cn/wiki/D6sVw0ketiX70ZkXE2FcIWTUn2c)
  >
  >   * 打通 maplab + alike 建图测试（离线接入描述子）；
  >
  >   * 初步测试精度提升；

  * Action

    * alike 引入 VIO 排期 `@郭科`

      * 精度：感知提供原版端侧后处理库，先把测试结果和感知对齐；

      * 耗时：前端处理一帧 1s -> <span style="color: inherit; background-color: rgba(255,246,122,0.8)">简化逻辑，减少耗时，</span>但待分析对精度的影响；

        * 描述子量化成  2 值描述子，预期精度下降；

      * （低优先级）量化模型差异：评估板子上精度的退化；（板子上还可能有 bug ）

    * Maplab + alike  建图重定位测试（跨视角，跨季节）；`@白世杰`

      * 多找几组数据验证；

      * 测试重定位精度 & 召回率的提升；

      * 代码提 pr；

  * TODO

    * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图；

* **Okvis 全局图与回环检测**

  > **本周进展**
  >
  > * 通道建图需求 ，HF2.0`@李波`[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink)
  >
  >   [ 通道建图测试](https://roborock.feishu.cn/wiki/PUAtw4HsNikT2Vk7XYMc7q8onSf?from=from_copylink)
  >
  >   * 建图时发出请求，并接收融合发布的  TRti；定位模式，出通道发布 ~~TRG~~；<span style="color: rgb(216,57,49); background-color: inherit">TRV</span>
  >
  >   * vio/vslam flag：重定位连续成功 3 次（vio 和 vslam 一致）后，切换为 vslam 状态。
  >
  > * 支持用 vimap 做重定位，省去转 sumamry map；`@刘博`

  * 通道建图需求 ，HF2.0`@李波`[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink)

    * 发布 7hz 的建图轨迹；

    * 建图失败的情况下，不发布轨迹，导航需记录通道属性，vslam / rtk 通道，打印日志，以便后续建图算法优化；

    * 通道数据采集：`@李波` `@刘博`

      * 2 组连续  3 次正反穿过通道的数据；

      * 2 组连续建 3 个不同的通道，再反向穿过的数据；

      * 跟进数据解析问题 `@刘博` `@黄亮`

    * 导航连调测试；

      * 通道 ID  bug；

      * 待和导航讨论：回桩通道 发送 离开信号；（回桩点发送信号）

  * 通道建图需求 ，HF3.0 [ 通道多 Session 地图合并设计](https://roborock.feishu.cn/wiki/GpaNwZthmiWwubkwYwocExx1nNc)

    * 支持用 vimap 做重定位，省去转 sumamry map； `@刘博`

      1. relocMapRootDir\_ / 独立 reloc 数据集根目录；（pr 中

      2. 重定位 TUM 输出 T\_G\_R = T\_G\_I \* T\_IR；使得重定位结果可以直接和 rtk 轨迹做 evo 评估；（pr 中

      3. 地图合并的版本上，清理生成 summary map，简化逻辑；（ debug

    * 地图合并：  &#x20;

      1. 地图合并频率；    `@刘博`  （开发中

         1. 重定位效果决策是否新建地图；

      2. RelocalizeAndBuild 新状态的加入； `@刘博`（开发中

      3. 地图合并算法；     `@江建文` （优化中

         1. 逻辑框架已实现，效果需要调优；

      4. 地图更新算法；`@刘博` `@江建文`

  * TODO

    * Maplab PGO （存档）  `@江建文`[ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)

    * Maplab Mapping & relocal 持续优化

      * 子图划分方案：判断回头进行子图划分 ( 存档）

        * [ 基于折返约束的子图切分策略优化与实验分析](https://roborock.feishu.cn/wiki/KQnKwXlHqilLDlknVQycMMDjnmd)

      * maplab 跟踪中加入光流，测试开光流的效果 （存档）

        * [ VIO 与 Gyro 作为旋转先验的跟踪与建图效果分析](https://roborock.feishu.cn/wiki/U2jHwSOXlixRBmk0oDUcSHznnBh)

    * 重定位效果的优化： `@刘博`

      1. maplab + 光流；（可以做快速的验证） &#x20;

      2. 评估单目建图是否可行；&#x20;

      3. 评估重定位结果对 vio 精度的影响；

    * 在线 Maplab 建图 `@宋姝`

      * 子图内部 100 关键帧数测试；`@宋姝`

      * 重定位精度、召回率精度测试  [ reloc-self\_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e) [ Relocalization analysis](http://roborock.feishu.cn/wiki/PtlzwEmNHiYYTqk8ZuxcULFinwb)（调优中）

        * 交叉 reloc 存在多个问题，需要进一步分析：

          * 重定位召回率低；（大部分 < 50%）

          * 重定位轨迹精度低；（参数，landmark 质量）

          * 考虑轨迹的方向，类别（弓字 / edge）&#x20;

      * Todo: online relocalization; `@宋姝`

    * 全局图工作项： [ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * maplab mapping 优化

      * 创建地图评分机制，区域分块好特征点评分

      * Faiss 的码表固定

      * 地图质量检测

        * 上报优化成功/失败

        * 场地过于空阔，有效点特别远

    * 轻量化，解决多地图、支持灵活的增、删区域

    * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn)&#x20;

      * 多子图

      * 开启的时候 coredump

      * 去掉桩点问题数据后重定位 `@肖鸿飞`

    [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260323

* 割草机内外参标定与检测

  > **本周进展**
  >
  > * 售后治具验证；（降本方案）[ 售后标定二维码测试](https://roborock.feishu.cn/wiki/Sdalwi7QTiX1czk3orscAMNjnHg)
  >
  >   * 三行 yaw 极差 1 degree&#x20;
  >
  >   * 两行极差 1.5 deg
  >
  >   * 两行 + ground 极差 < 1deg
  >
  >   * 结论：暂定选用 3行 tag 或者两行 + 地上一列的方案；
  >
  > * 产线检测站问题排查
  >
  >   * CCIQC 代码重构，（PR 76） review 代码`@李波` [ 3m滑轨重构代码运行结果对比](https://roborock.feishu.cn/wiki/FWSnwUlwKiopWEkj7bRcK5UWnNZ?from=from_copylink)
  >
  >     * 代码正常，重构前后数值差异小；
  >
  >   * bug fix: 补充点云平面距离判定，并找 B2 B3 产线数据测试； done
  >
  > * 售后双目之间外参标定`@邱冰冰`
  >
  >   * <span style="color: rgb(222,120,2); background-color: inherit">Toi 按列输出问题，修复代码已合入；</span> <span style="color: rgb(222,120,2); background-color: inherit">https://applink.feishu.cn/client/message/link/open?token=Amj4oU8xR0AEab%2FKPOEADLI%3D</span>
  >
  > * 售后标定方案`@邱冰冰` 缩短售后标定时间在 5 分钟内：
  >
  >   * 合入轨迹文件 config.txt，根据不同项目 install 不同 config.txt，参考 prebuild/aarch64-mr527-linux-gnu/as\_calib 下的 thresh\_config.json 的安装方式。
  >
  >   * 过滤数据 [<u>PR 83</u>](https://gitlab5.roborock.com/libaoyu/butchartcalibandcheck/-/merge_requests/83)&#x20;
  >
  > * 工厂标定算法优化
  >
  >   * Flora 接入 bin 文件标定：[<u>BUG #486030 【WI】【装备需求】【FLora】【Lumos】【Gaia】MCT双目标定参数打包成bin</u>](http://192.168.111.52/index.php?m=bug\&f=view\&bugID=486030)<u> </u> `@邱冰冰`
  >
  > * CIIQC 站维护； `@江建文`
  >
  >   * 欧菲 IMU 模组频率不稳定；
  >
  > * CQIQC 站维护；`@李波`
  >
  >   * 欧菲模组相机模糊（内部脏污）

  * Action

    * 售后双目之间外参标定`@邱冰冰`

      * <span style="color: rgb(222,120,2); background-color: inherit">Toi 按列输出问题，修复代码已合入，联调测试中；</span> （测试要求：售后标定通过，机器正常割草）

      * 售后治具验证；（降本方案）[ 售后标定二维码测试](https://roborock.feishu.cn/wiki/Sdalwi7QTiX1czk3orscAMNjnHg)

        * 验证窄距三行的版本；

          &#x20;

    * 售后标定方案`@邱冰冰` 缩短售后标定时间在 5 分钟内&#x20;

      * 超时问题：激光的标定加入，多线程运行之后，导致的运行速度下降；

      * 测试耗时，给出阈值；

    * flora MK2 相机参数配置；`@邱冰冰`

    * CIIQC 站维护； `@江建文`

    * CQIQC 站维护；`@李波`

    * 解析数据工具更新；

      * `@姚远`需提供适配新老版本的工具，催 spm

    * 其他待办：

      * <span style="color: rgb(143,149,158); background-color: inherit">MCT\IQC 后续再尝试降低计算时间/数据量；</span>

      * 售后标定方案

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查 （数值差异）

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

        * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

          * 最终的 refine 去掉重投影误差大的数据（TODO）

          * 代码合入

            * Monet B3, versa B2

* OKVIS-VIO 优化

  > **本周进展**
  >
  > * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)
  >
  >   * 400 度转弯可偏 1-3 度（序号 9，单组数据）done
  >
  > * 补光灯切换时 reset + 1  MR181 `@白世杰`
  >
  > * 先光流，后描述子匹配补点方法 （设计方案） `@白世杰` （存档）
  >
  >   * [ 光流追踪与描述子匹配融合算法调研](https://roborock.feishu.cn/wiki/LKysw3ioJi1ZADkF3K6cMhQRnkf)&#x20;

  * 持续优化 okvis `@郭科`

    * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

    * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)

      * 转弯区域精度变低（偏差 10cm 以内）

      * 序号 3 的尺度偏差问题分析；

  * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

    * 先光流，后描述子匹配补点方法 （设计方案） `@白世杰`

    *

  * 其他待办：

    * 先光流，后描述子匹配补点方法 （设计方案） `@白世杰` （存档）

      * [ 光流追踪与描述子匹配融合算法调研](https://roborock.feishu.cn/wiki/LKysw3ioJi1ZADkF3K6cMhQRnkf)&#x20;

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * VIO 初始化逻辑：启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias `@郭科`

    * 跟丢的逻辑设计&#x20;

* 深度学习特征点描述子引入

  > **本周进展**

  * Action

    * alike 引入 VIO 排期 `@郭科`

    * Maplab + alike  建图重定位测试（跨视角，跨季节）；`@白世杰`

    * TODO

      * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图；

* Okvis 全局图与回环检测

  > **本周进展**
  >
  > * 窄通道建图需求
  >
  >   * 重定位失败问题 debug；[ OKVIS 通道建图仿真分析与问题修复](https://roborock.feishu.cn/wiki/JFZNwjVH3imNuekEHkFc9IThnif)；`@刘博`
  >
  >   * 关闭多次建图结果的 merge - 正反向独立维护地图；
  >
  >   * 地图优化不阻塞建图：optimizationThread\_ 修改为改为持久线程 + 任务队列 ；
  >
  >   * &#x20;建图结束后，生成 7hz 轨迹 ；（需上报给导航）
  >
  >   * &#x20;pause & vio reset 状态机：建图失败，地图清除；
  >
  >   * &#x20;保存 TRG 到地图，重定位成功后，发布 RTK 世界系下的 vslam pose；
  >
  > * Maplab Mapping & relocal 持续优化
  >
  >   * 子图划分方案：判断回头进行子图划分 ( 存档）
  >
  >     * [ 基于折返约束的子图切分策略优化与实验分析](https://roborock.feishu.cn/wiki/KQnKwXlHqilLDlknVQycMMDjnmd)
  >
  >   * maplab 跟踪中加入光流，测试开光流的效果 （存档）
  >
  >     * [ VIO 与 Gyro 作为旋转先验的跟踪与建图效果分析](https://roborock.feishu.cn/wiki/U2jHwSOXlixRBmk0oDUcSHznnBh)
  >
  > * Maplab PGO （存档）  `@江建文`[ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)
  >
  >   * 板端耗时分析；  &#x20;
  >
  >   * PR 160 中 ；

  * 通道建图需求 ，HF2.0`@李波`[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink)

    * 建图时发出请求，并接收融合发布的  TRti；定位模式，出通道发布 ~~TRG~~；<span style="color: rgb(216,57,49); background-color: inherit">TRV</span>

    * vio/vslam flag：重定位连续成功 5 次（vio 和 vslam 一致）后，切换为 vslam 状态。

    * 发布 7hz 的建图轨迹；

    * 建图失败的情况下，不发布轨迹，导航需记录通道属性，vslam / rtk 通道，打印日志，以便后续建图算法优化；（导航期望：建图失败也统一发一串轨迹，正常建图失败应该需要提醒用户重建）

    * 通道数据采集：

      * 2 组连续  3 次正反穿过通道的数据；

      * 2 组连续建 3 个不同的通道，再反向穿过的数据；

    * 导航连调测试；

  * 通道建图需求 ，HF3.0 [ 通道多 Session 地图合并设计](https://roborock.feishu.cn/wiki/GpaNwZthmiWwubkwYwocExx1nNc)

    * 支持用 vimap 做重定位，省去转 sumamry map，pr 中； `@刘博`

    * 地图合并：  &#x20;

      1. 地图合并频率；    `@刘博`

      2. 地图合并算法；     `@江建文`

      3. RelocalizeAndBuild 新状态的加入； `@刘博`

      4. 地图更新算法；`@刘博` `@江建文`

  * TODO

    * Maplab PGO （存档）  `@江建文`[ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)

    * Maplab Mapping & relocal 持续优化

      * 子图划分方案：判断回头进行子图划分 ( 存档）

        * [ 基于折返约束的子图切分策略优化与实验分析](https://roborock.feishu.cn/wiki/KQnKwXlHqilLDlknVQycMMDjnmd)

      * maplab 跟踪中加入光流，测试开光流的效果 （存档）

        * [ VIO 与 Gyro 作为旋转先验的跟踪与建图效果分析](https://roborock.feishu.cn/wiki/U2jHwSOXlixRBmk0oDUcSHznnBh)

    * 重定位效果的优化： `@刘博`

      1. maplab + 光流；（可以做快速的验证） &#x20;

      2. 评估单目建图是否可行；&#x20;

      3. 评估重定位结果对 vio 精度的影响；

    * 在线 Maplab 建图 `@宋姝`

      * 子图内部 100 关键帧数测试；`@宋姝`

      * 重定位精度、召回率精度测试  [ reloc-self\_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e) [ Relocalization analysis](http://roborock.feishu.cn/wiki/PtlzwEmNHiYYTqk8ZuxcULFinwb)（调优中）

        * 交叉 reloc 存在多个问题，需要进一步分析：

          * 重定位召回率低；（大部分 < 50%）

          * 重定位轨迹精度低；（参数，landmark 质量）

          * 考虑轨迹的方向，类别（弓字 / edge）&#x20;

      * Todo: online relocalization; `@宋姝`

    * 全局图工作项： [ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * maplab mapping 优化

      * 创建地图评分机制，区域分块好特征点评分

      * Faiss 的码表固定

      * 地图质量检测

        * 上报优化成功/失败

        * 场地过于空阔，有效点特别远

    * 轻量化，解决多地图、支持灵活的增、删区域

    * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn)&#x20;

      * 多子图

      * 开启的时候 coredump

      * 去掉桩点问题数据后重定位 `@肖鸿飞`

    [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260316&#x20;

* 割草机内外参标定与检测

  > * 本周进展
  >
  >   * MCT 行差标定，概率性优化失败，问题解决 1 天，PR 87 已合入 （Done）
  >
  >   * 售后标定方案`@邱冰冰`
  >
  >     * 实现脚本出：售后标定版本 0.1 天    （Done）
  >
  >       * 提 PR 86  已合入
  >
  >   * 进行测试，确定是否能够解决 Bug#459093  `@邱冰冰`
  >
  >     * 确定行差本身就小的原因：跑 MCT，确实 3.4+
  >
  >     * 和吴俊杰对齐极线校正脚本；
  >
  >     * 修复售后标定更新参数未正常使用的问题，待测试；
  >
  >   * CIIQC 站维护`@江建文`
  >
  >     * [ CIIQC（相机来料质量控制）站维护工作](https://roborock.feishu.cn/wiki/CBdvwlM8xiFEcWkI9zqcIOIunyp?open_in_browser=true)
  >
  >   * 售后标定方案`@邱冰冰` 缩短售后标定时间在 5 分钟内 0.5 天 &#x20;
  >
  >     * 文档记录删后的轨迹和 RTK 机型轨迹的区别[ 售后标定筛掉lidar掉头路线的数据](https://roborock.feishu.cn/wiki/V5dDwFHtkiobsLkBjb3c01axn0b)
  >
  >   * 工厂标定算法优化 `@邱冰冰`
  >
  >     * MCT 写入 tcrcl 到 dualcamera\_calibration.json&#x20;

  * Action

    * 产线检测站问题排查

      * CCIQC 代码重构，（PR 76） review 代码`@李波`&#x20;

      * bug fix: 补充点云平面距离判定，并找 B2 B3 产线数据测试；

    * 售后双目之间外参标定`@邱冰冰`

      * 联调支持、多机稳定性测试；

      * 进行测试，确定是否能够解决 Bug#459093；&#x20;

      * &#x20;block: 测试不 work，运行超时，正在核对原因；

    * 售后标定方案`@邱冰冰` 缩短售后标定时间在 5 分钟内 0.5 天 &#x20;

      * 自测完成后再找测试多测`@邱冰冰`（测试 block，处理中）

      * 合入轨迹文件 config.txt，根据不同项目 install 不同 config.txt，参考 prebuild/aarch64-mr527-linux-gnu/as\_calib 下的 thresh\_config.json 的安装方式。`@邱冰冰`

      * 不同规模机器运行时间测试；（根因追查）

    * 工厂标定算法优化

      * 产线代码更新，`@邱冰冰`出包；（旧的机型需主动找 spm 排期更新）；`@宋姝`

      * Flora 接入 bin 文件标定 `@邱冰冰`

    * CQIQC 站维护`@李波`

    * CIIQC 站维护`@江建文`

    * 其他 TODO

      * <span style="color: rgb(143,149,158); background-color: inherit">MCT\IQC 后续再尝试降低计算时间/数据量</span> <span style="color: rgb(143,149,158); background-color: inherit">；</span>

      * 售后标定方案

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查 （数值差异）

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

        * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

          * 最终的 refine 去掉重投影误差大的数据（TODO）

          * 代码合入

            * Monet B3, versa B2

    * odo 数据格式变了，解析数据工具更新；`@宋姝`

* OKVIS-VIO 优化

  > * 本周进展
  >
  >   * [ odo+gyro递推精度分析](https://roborock.feishu.cn/wiki/K2kQw2xk1igR9WkDdoQcyUVXnf9)`@白世杰`
  >
  >     * [ odo+gyro / VIO / VIO优化版 — 三者 RMSE 对比](https://roborock.feishu.cn/wiki/Iwd3wHDCPi7nZNk3N0ucZKOQnRg)
  >
  >     * 结论：rte 评估，vio 轨迹精度更高，vio rmse% 1.17%，gyro + odo rmse% 2.23%；
  >
  >     * odo + gyro rte 精度存档，夜间无视觉时使用；
  >
  >   * 持续优化 okvis `@郭科`
  >
  >     * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)
  >
  >       * 结论：dev+草丛+非草丛区域光流算法补点，无普适优化效果，暂不合入；
  >
  >     * 同一个 landmark 被一个帧观测多次的 bug 解决 `@郭科`
  >
  >       * PR 151  done
  >
  >   * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd) 待进一步分析；
  >
  >   * [ okvis非弓字精度提升](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb)&#x20;
  >
  >     * 结论：短平快的调整无效，文档归档；
  >
  >   * 前端、LBA 代码精调 `@郭科`&#x20;
  >
  >     * 窗口扩大无效；

  * Action

    * 持续优化 okvis `@郭科`

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

      * 同一个 landmark 被一个帧观测多次的 bug 解决 `@郭科`

        * PR 151 中 done

      * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)

        * 400 度转弯可偏 1-3 度（序号 9，单组数据）

        * 转弯区域精度变低（偏差 10cm 以内）

        * 序号 3 的尺度偏差问题分析；

    * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

      * 先光流，后描述子匹配补点方法 （设计方案） `@白世杰`

    * [ odo+gyro递推精度分析](https://roborock.feishu.cn/wiki/K2kQw2xk1igR9WkDdoQcyUVXnf9)`@白世杰`

      * Debug RTK 插值对齐方案；

    * 其他待办：

      * VIO 初始化逻辑：启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias `@郭科`

      * 跟丢的逻辑设计&#x20;

* 深度学习特征点描述子引入

  > * 本周进展
  >
  >   * superpoint 引入 VIO 排期：`@陈飞`[ cf-交接文档](https://roborock.feishu.cn/docx/VQsEddxQNoReMaxJiVnch4KfnFd)`@刘博`
  >
  >     * finetune 后接入批测；
  >
  >     * float 描述子匹配的分支给出；
  >
  >     * 代码合入  vl\_slam/develop；

  * Action

    * superpoint 引入 VIO 排期

      * Maplab + sp  建图重定位测试（跨视角，跨季节）；`@刘博`

    * TODO

      * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图；

* 其他工作项

  > * 本周进展

  * Action

    * &#x20;水下视觉 slam 相关工作  `@白世杰`

      * 完成所有图像质量分析[ 泳池机器人图像质量分析](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)。 &#x20;

      * 完成 okvis 在泳池数据集上适当优化，并给出初步结论。[ 泳池机器人okvis测试](https://roborock.feishu.cn/wiki/MF1ewBTbWiUeNUkOKlzcsyJGnEh) &#x20;

      * 完成 letvins 在泳池数据集上跑通和优化，并给出初步结论。 &#x20;

      * 看噪点大的问题，是否能够比较好的过滤掉

***

* Okvis 全局图与回环检测

  > * 本周进展
  >
  >   * 窄通道建图需求`@李波`
  >
  >     * [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink)
  >
  >   * 加载地图重定位`@肖鸿飞`[ 多帧校验：多帧匹配修正 T\_map\_vio](https://roborock.feishu.cn/wiki/NuIRww6ITihflCkmCcicYts7nMf)
  >
  >     * 定位精度低于离线版本 VIO+地图观测；
  >
  >     * 多帧回环过滤精度变差分析；
  >
  >   * 单精度建图优化测试[ 单精度优化建图](https://roborock.feishu.cn/wiki/ZZftwtLOiiWyhakBN73cidqjn9c)
  >
  >   * Maplab PGO `@江建文`[ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)
  >
  >     * &#x20;gtsam  加入 prebuild，支持板端测试； &#x20;
  >
  >     * &#x20;4dof 精度与 6dof 相当，且耗时减少 15% ～ 20%；  &#x20;
  >
  >     * &#x20;支持 switchable constraints；
  >
  >   * Maplab Mapping & relocal `@刘博`
  >
  >     * 子图内部优化后精度变差原因分析[ 子图大小对单子图精度影响分析](https://roborock.feishu.cn/wiki/Z3GMwy9FFiIFqAkqXY0cgZTunNa)
  >
  >       * 结论：单个 mission 中存在多个 弓字弯，产生的会回环，有利于提升建图精度；
  >
  >     * 子图划分方案：判断回头进行子图划分 [ 单子图内部折返对局部轨迹优化精度的影响](https://roborock.feishu.cn/wiki/LowgwwlSNi7Tq2kcAPPcq3tCn7d)
  >
  >     * maplab 跟踪中加入光流，测试开光流的效果[ maplab加入光流补跟踪补充测试](https://roborock.feishu.cn/wiki/FZ80wQE2zimufZkRmm8cFI99nOg)
  >
  >     * &#x20;交接深度学习特征点相关工作：
  >
  >       * 代码 rebase `vl_slam/develop`；
  >
  >       * 支持感知组需求；
  >
  >   * Okvis 全局 PGO `@陈飞`
  >
  >     1. 搬窗口逻辑接入，realTimeGraph 的修改接入，测试整体精度 [ PGO功能测试](https://roborock.feishu.cn/docx/P5qCdhxLHoYxkSxMSvic1GH3nkd)
  >
  >     2. 确定 PGO 本身的准确性：使用 RTK Pose 插值作为 PGO 约束
  >
  >     3. 与 maplab 测试集对齐`@陈飞`
  >
  >     4. 代码形成分支
  >
  >   * 重定位多帧校验`@李波`
  >
  >     * 在线建图版本可视化信息加入，分析重定位效果。`@肖鸿飞`
  >
  >     * 对假阳、假阴进行分析。[ 多帧校验：多帧匹配修正 T\_map\_vio](https://roborock.feishu.cn/wiki/NuIRww6ITihflCkmCcicYts7nMf)`@肖鸿飞`

  * Action

    * 全局图工作项： [ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * 窄通道建图需求`@李波`[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) [ okvis通道建图仿真分析](https://roborock.feishu.cn/wiki/QI1FwUzGZicm7ykQ9Z3cVM4qnyL?from=from_copylink)

      * 分析当前重定位失败的原因；（建图质量 & 重定位调试）

      * 正反建通道无法合并；

      * 窄通道建图连调；

    * 在线 Maplab 建图 `@宋姝`

      * 子图内部 100 关键帧数测试；`@宋姝`

      * 重定位精度、召回率精度测试  [ reloc-self\_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e) [ Relocalization analysis](http://roborock.feishu.cn/wiki/PtlzwEmNHiYYTqk8ZuxcULFinwb)（调优中）

        * 交叉 reloc 存在多个问题，需要进一步分析：

          * 重定位召回率低；（大部分 < 50%）

          * 重定位轨迹精度低；（参数，landmark 质量）

          * 考虑轨迹的方向，类别（弓字 / edge）&#x20;

      * Todo: online relocalization; `@宋姝`

    * Maplab PGO `@江建文`[ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)

      * 板端耗时分析；  &#x20;

      * PR 160 中 ；

    * Maplab Mapping & relocal `@刘博`

      * 子图划分方案：判断回头进行子图划分[ 单子图内部折返对局部轨迹优化精度的影响](https://roborock.feishu.cn/wiki/LowgwwlSNi7Tq2kcAPPcq3tCn7d)

      * maplab 跟踪中加入光流，测试开光流的效果[ maplab加入光流补跟踪补充测试](https://roborock.feishu.cn/wiki/FZ80wQE2zimufZkRmm8cFI99nOg)

    * TODO

      * maplab mapping 优化

        * 创建地图评分机制，区域分块好特征点评分

        * Faiss 的码表固定

        * 地图质量检测

          * 上报优化成功/失败

          * 场地过于空阔，有效点特别远

      * 轻量化，解决多地图、支持灵活的增、删区域

      * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn)&#x20;

        * 多子图

        * 开启的时候 coredump

        * 去掉桩点问题数据后重定位 `@肖鸿飞`

      [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260309

* 割草机内外参标定与检测

  > * 本周进展
  >
  > * 代码整理，售后标定、售后行差标定都要能够正常运行 1 天   （Done）
  >
  >   * 初步：售后标定不输出 Tcrcl，行差标定输出，调用一个算法代码。
  >
  >     * Double \[6] = {0};
  >
  >     * Bool is\_caliab = false;
  >
  > * 售后标定治具缩小测试结果[ 售后标定治具缩小方案测试结果](https://roborock.feishu.cn/wiki/AuGgwEHtui3WZOkuMclcr0QHnBd?open_in_browser=true)，通过
  >
  > * 输出售后标定的错误制造方法
  >
  > * MCT 行差标定，概率性优化失败，问题解决 1 天&#x20;
  >
  >   * Tcrcl 优化有可能失败
  >
  >   * 优化函数的数据没有做过滤
  >
  > * 进行测试，确定是否能够解决 Bug#459093 &#x20;
  >
  >   * 行差 1.6->0.2
  >
  > * Flora 适配完成，测试通过
  >
  > * 缩短售后标定时间在 5 分钟内 0.5 天 &#x20;
  >
  >   * 自测完成
  >
  > * 实现脚本出：售后标定版本 0.1 天    开发完成待合入
  >
  > * 治具缩小后 Toi 标定失败的原因分析 1 天 &#x20;
  >
  >   * 失败是因为板子太厚，z 轴检测通不过
  >
  >   * 固定 Z 轴
  >
  > * thresh\_config，vendor07 适配 PR 中`@李宝玉`
  >
  >   * 合入完成

  * Action

    * 产线检测站问题排查

      * CQIQC 代码重构，CR 修改`@邱冰冰` 0.5 天 &#x20;

    * MCT 站双目之间外参标定`@邱冰冰`

      * 联调支持、多机稳定性测试

      * MCT 行差标定，概率性优化失败，问题解决 1 天&#x20;

      * 进行测试，确定是否能够解决 Bug#459093 &#x20;

        * 行差 1.6->0.2

        * 确定行差本身就小的原因`@邱冰冰`

          * 跑 MCT

          * 如果 MCT 也小，联系`@李圳`

    * CIIQC 站维护`@江建文`

      * [ CIIQC（相机来料质量控制）站维护工作](https://roborock.feishu.cn/wiki/CBdvwlM8xiFEcWkI9zqcIOIunyp?open_in_browser=true)

    * CQIQC 站维护`@李波`

    * 售后标定方案`@邱冰冰`

      * 缩短售后标定时间在 5 分钟内 0.5 天  `@李宝玉`

        * 过滤数据

        * 自测完成后再找测试多测

      * 实现脚本出：售后标定版本 0.1 天   &#x20;

        * 提 PR 合入

      * 分析定位 PC 与 ARM 编译后，标定结果的差异排查

    * 工厂标定算法优化

      * MCT 写入 tcrcl 到 dualcamera\_calibration.json `@邱冰冰` &#x20;

      * 打滑检测优化

        * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

    * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

      * 最终的 refine 去掉重投影误差大的数据（TODO）

      * 代码合入

        * Monet B3, versa B2

    * <span style="color: rgb(143,149,158); background-color: inherit">联合模组供应商模组内外参标定结果审查</span>

      * <span style="color: rgb(143,149,158); background-color: inherit">内参标定成功，但是外参标定 TOC 误差大，和联合标定结果对比</span>`@李宝玉`

        * <span style="color: rgb(143,149,158); background-color: inherit">Tci，z 轴偏大</span>

    * 其他 TODO

      * <span style="color: rgb(143,149,158); background-color: inherit">MCT\IQC 后续再尝试降低计算时间/数据量</span>

* OKVIS-VIO 优化

  > * 本周进展
  >
  >   * RTK\&VIO 多帧对齐，尾端会差一点`@郭科`
  >
  >     * 风险较高，变化不大，权重调整不进入评估脚本
  >
  >     * 10m 对齐效果最佳，进入评估脚本
  >
  >     * 10m 对齐，20m 评估
  >
  >   * 持续优化 okvis `@郭科`
  >
  >     * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`
  >
  >       * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)普遍精度 RMSE 约 1.5%
  >
  >     * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)
  >
  >   * 打点（坡度、badImu）Done `@郭科`
  >
  >   * [ okvis非弓字精度提升](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb)
  >
  >     * 纯 OKVIS 本身参数调整，没法调的更好
  >
  >     * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)误差变大，适配方法更新后
  >
  >   1. 斜坡测试和合入`@白世杰`   合入完成
  >
  >      1. [ 侧滑以及倾斜检测上机测试](https://roborock.feishu.cn/wiki/GReHwBESyitJBwkUqVrcC5a8nld)

  * Action

    * 持续优化 okvis `@郭科`

      * 分析通道内数据对齐后的精度情况

        * 融合方式预研 时间安排`@李宝玉`

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

        * B1-37\_7.22\_105\_lake\_corrected 继续排查精度变差的问题`@李宝玉`

      * 同一个 landmark 被一个帧观测多次的 bug 解决 `@郭科`

        * PR 中

      * [ okvis非弓字精度提升](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb)

        * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

          * 灰度图测试

          * 代码接入 okvis，批测

        * dev+草丛+非草丛区域光流算法补点

        * 先光流，后描述子匹配补点方法

        * 前端、LBA 代码精调 `@李宝玉`排期

    1. [ odo+gyro递推精度分析](https://roborock.feishu.cn/wiki/K2kQw2xk1igR9WkDdoQcyUVXnf9)`@白世杰`

       1. 确定样条插值是不是局部选控制点

       2. 补充 VIO 的轨迹对齐结果

* 深度学习特征点描述子引入

  > * 本周进展
  >
  >   * superpoint 初步精度优于 brisk

  * Action

    * superpoint 引入 VIO 排期

      * finetune 后接入批测

    * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图

    * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`

      * 代码合入 vl\_slam/develop

* 其他工作项

  > * 本周进展

  * Action

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * &#x20;水下视觉 slam 相关工作  `@白世杰`

      * 完成所有图像质量分析[ 泳池机器人图像质量分析](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)。 &#x20;

      * 完成 okvis 在泳池数据集上适当优化，并给出初步结论。[ 泳池机器人okvis测试](https://roborock.feishu.cn/wiki/MF1ewBTbWiUeNUkOKlzcsyJGnEh) &#x20;

      * 完成 letvins 在泳池数据集上跑通和优化，并给出初步结论。 &#x20;

      * 看噪点大的问题，是否能够比较好的过滤掉

***

* Okvis 全局图与回环检测`@肖鸿飞`

  > * 本周进展
  >
  >   * maplab 复用 okvis 跟踪与 landmark [ 链路3：地图点复用设计文档](https://roborock.feishu.cn/wiki/MIqPwfRP5imDp4kcCfVcH1MpnIq)
  >
  >     * Okvis score 接入
  >
  >     * 已合入宋姝开发分支
  >
  >     * 整理一下修改项目，提出可调参数[ 建图分支提交整理](https://roborock.feishu.cn/wiki/Yxyhw9HTUismwfkYaMzcQPH4nFh)
  >
  >   * 窄通道建图需求[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) `@李波` `@陈飞`
  >
  >     * 消息基本统计完成[ 通道建图测试](https://roborock.feishu.cn/wiki/PUAtw4HsNikT2Vk7XYMc7q8onSf?from=from_copylink)
  >
  >     * 很快到达建图起点，会自动生成通道，会发结束建通道消息，但是后续导航认为通道不存在。没有发删除通道。Push 导航发删除通道消息。已解决。
  >
  >     * 内存增长太大 PGO 会耗时过长：
  >
  >       * 单目 Mapping 调优 `@宋姝` [ 单目 vs 双目 算法对比分析](https://roborock.feishu.cn/wiki/Pdn1wmFJ0iboaBkwh5icvgFYnQc)（Done）
  >
  >     * 排查子图拼接精度较低；[ Online Mapping 精度 - 3.9](https://roborock.feishu.cn/wiki/ZRZbwYGpLi82CakuVflcEpDzn8e)
  >
  >       * 缩减建图规模 + 引入 GTSAM ：[ 建图规模缩减 - 3.9](https://roborock.feishu.cn/wiki/R0ekwyL7tiaDBdkv8uxcANBQnsf)
  >
  >         * 优化后二次 keyframe 筛选；
  >
  >         * 冗余 mission 删除（且在 PGO 后执行）
  >
  >     * 重定位精度、召回率精度测试  [ reloc-self\_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e)（调优中）
  >
  >       * reloc-self 验证 online mapping landmark 可用 & 重定位逻辑打通
  >
  >       * 重定位召回率较低，继续调优
  >
  >     * Maplab PGO `@江建文` `@李宝玉`
  >
  >       * [ 后续工作计划](https://roborock.feishu.cn/wiki/EcmcwX3nGiTB6zkiVErcVsUxnV7?open_in_browser=true)
  >
  >       * [ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)
  >
  >       * 上板子批测，整理 prebuild
  >
  >       * 分子图参数与`@宋姝`保持一致
  >
  >     * Maplab Mapping & relocal `@刘博`
  >
  >       * 子图内部优化后精度变差原因分析[ 子图大小对单子图精度影响分析](https://roborock.feishu.cn/wiki/Z3GMwy9FFiIFqAkqXY0cgZTunNa)
  >
  >         * 子图内部小的话，精度低
  >
  >     * 加载地图重定位`@肖鸿飞`
  >
  >       * 定位精度低于离线版本 VIO+地图观测
  >
  >       * 多帧回环过滤精度变差分析

  * Action

    * &#x20;[ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * 窄通道建图需求[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) `@李波` `@陈飞`

      * 用路程来判定，确定是否建立桩到区域的 bug

      * 建图质量、VIO 在地图重定位精度分析 `@宋姝` `@肖鸿飞`

      * 异步优化

    * 在线 Maplab 建图 `@宋姝`

      * 子图内部 100 关键帧数测试

      * 重定位精度、召回率精度测试  [ reloc-self\_analysis](https://roborock.feishu.cn/wiki/WJLhwUbBdiUskEkAu28cWYJbn8e)（调优中）

        * reloc-self 验证 online mapping landmark 可用 & 重定位逻辑打通；

        * 交叉 reloc 存在多个问题，需要进一步分析：

          * 重定位召回率低；（大部分 < 50%）

          * 重定位轨迹精度低；（参数，landmark 质量）

          * 考虑轨迹的方向，类别（弓字 / edge）&#x20;

      * Todo: online relocalization; `@宋姝` `@李宝玉`

      * Todo 回环检测输出给 VIO 进行搬窗口

      * 加载地图重定位`@肖鸿飞`

        * 定位精度低于离线版本 VIO+地图观测

        * 多帧回环过滤精度变差分析

    * Maplab PGO `@江建文`

      * [ 后续工作计划](https://roborock.feishu.cn/wiki/EcmcwX3nGiTB6zkiVErcVsUxnV7?open_in_browser=true)

      * [ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)

      * 上板子批测，整理 prebuild

      * 错误闭环处理（动态调整回环边权重），继续批测，接入更大规模数据测试

    * Maplab Mapping & relocal `@刘博`

      * 子图内部优化后精度变差原因分析[ 子图大小对单子图精度影响分析](https://roborock.feishu.cn/wiki/Z3GMwy9FFiIFqAkqXY0cgZTunNa)

        * 回头跑与精度的区别测试

        * 子图划分方案：判断回头进行子图划分

      * maplab 跟踪中加入光流，测试开光流的效果[ 光流补跟踪对整图精度与建图收益的影响分析](https://roborock.feishu.cn/wiki/I5r4wAHAuijgi7kotjgcmIAfndd)

      * 创建地图评分机制，区域分块好特征点评分

      * Faiss 的码表固定

    3. 全局 PGO `@陈飞`

       1. 搬窗口逻辑接入，realTimeGraph 的修改接入，测试整体精度 [ PGO功能测试](https://roborock.feishu.cn/docx/P5qCdhxLHoYxkSxMSvic1GH3nkd)

       2. 确定 PGO 本身的准确性：使用 RTK Pose 插值作为 PGO 约束

       3. 与 maplab 测试集对齐`@陈飞`

       4. 代码形成分支

    * 重定位多帧校验`@李波`

      * 在线建图版本可视化信息加入，分析重定位效果。`@肖鸿飞`

      * 对假阳、假阴进行分析。[ 多帧校验：多帧匹配修正T\_map\_vio](https://roborock.feishu.cn/wiki/NuIRww6ITihflCkmCcicYts7nMf)`@肖鸿飞`

      * 问题集确定。

    * TODO

      2. VIO 初始化逻辑 `@郭科`

         * 优化

           1. 启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias

      * Okvis 版本多帧回环方案设计与实现`@李波`

      * 跟丢的逻辑设计&#x20;

      * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn)&#x20;

        * 多子图

        * 开启的时候 coredump

        * 去掉桩点问题数据后重定位 `@肖鸿飞`

      * 地图质量检测

        * 上报优化成功/失败

        * 场地过于空阔，有效点特别远

      * 轻量化，解决多地图、支持灵活的增、删区域

      * VIO 边缘轨迹精度差，是否会影响割草机建图&#x20;

        * 闭合的瞬间，要很快地输出回环检测结果

        * 闭合后，要能够输出闭环优化后的轨迹

      * 假成功的分析与处理，bug fix（基于新采集数据，多帧数据交叉验证）`@肖鸿飞`[ Eden数据错误重定位分析](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb)

      [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260302

* 割草机内外参标定与检测

  > * 本周进展
  >
  >   * MCT 不转静态标定
  >
  >   * 售后标定双目之间外参标定：自测完成
  >
  >     * [ 定位组-售后双目基线标定开发计划](https://roborock.feishu.cn/wiki/PdAWwAtQNipZLlkrmBucqwxPneF?open_in_browser=true)
  >
  >     * 检查 linediff
  >
  >     * 确定标定 37 分钟的版本是 DEBUG 还是 RelWithDebguInfo `@丁毅`  （Done）
  >
  >   * MCT 维护：统计相机与 odo 反向的比例，简化 debug。`@邱冰冰`  ( Done)&#x20;
  >
  >   * 维护近期合入 prebuild dev 的 bug 列表`@邱冰冰`[ 售后标定合入prebuild dev的bug列表](https://roborock.feishu.cn/wiki/TQmawZ0FJiHEgbkJAXicX6GPnsh)

  * Action

    * 产线检测站问题排查

      * CQIQC 代码重构，CR 修改`@邱冰冰` 0.5 天 &#x20;

    * MCT 站双目之间外参标定`@邱冰冰`

      * 联调支持、多机稳定性测试

      * 代码整理，售后标定、售后行差标定都要能够正常运行 1 天   P0

        * 初步：售后标定不输出 Tcrcl，行差标定输出，调用一个算法代码。

          * Double \[6] = {0};

          * Bool is\_caliab = false;

        * 售后标定也做行差标定，行差缩小一定范围，才运用

      * 进行测试，确定是否能够解决 Bug#459093 &#x20;

        * 机器拿回工区

    * CIIQC 站维护`@江建文`

      * [ CIIQC（相机来料质量控制）站维护工作](https://roborock.feishu.cn/wiki/CBdvwlM8xiFEcWkI9zqcIOIunyp?open_in_browser=true)

    * CQIQC 站维护`@李波`

    * 售后标定方案`@邱冰冰`

      * 缩短售后标定时间在 5 分钟内 0.5 天 &#x20;

        * 过滤数据

      * 实现脚本出售后标定版本 0.1 天  &#x20;

      * 治具缩小后 Toi 标定失败的原因分析 1 天 &#x20;

      * 分析定位 PC 与 ARM 编译后，标定结果的差异排查

    * 工厂标定算法优化

      * thresh\_config，vendor07 适配 PR 中`@李宝玉`

        * 结构参数还未在外参文档更新完成

      * MCT 写入 tcrcl 到 dualcamera\_calibration.json `@邱冰冰` &#x20;

      * 打滑检测优化

        * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

    * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

      * 最终的 refine 去掉重投影误差大的数据（TODO）

      * 代码合入

        * Monet B3, versa B2

    * <span style="color: rgb(143,149,158); background-color: inherit">联合模组供应商模组内外参标定结果审查</span>

      * <span style="color: rgb(143,149,158); background-color: inherit">内参标定成功，但是外参标定 TOC 误差大，和联合标定结果对比</span>`@李宝玉`

        * <span style="color: rgb(143,149,158); background-color: inherit">Tci，z 轴偏大</span>

    * 其他 TODO

      * <span style="color: rgb(143,149,158); background-color: inherit">MCT\IQC 后续再尝试降低计算时间/数据量</span>

* OKVIS-VIO 优化

  > * 本周进展
  >
  >   * [ okvis非弓字精度提升](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb)`@郭科`
  >
  >     * [ okvis+LET-Net 深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)
  >
  >   1. 以补光灯的开关状态确定对外是否输出姿态 `@白世杰`  （Done）
  >
  >      1. 第一次收到关灯不处理；
  >
  >      2. 接到开灯消息后，不发姿态；
  >
  >      3. 接到关灯消息后，统计开灯时长，大于 3s 的情况下，1 分钟开始发姿态。否则关灯就发姿态。
  >
  >   2. 内存踩踏分析 `@白世杰`  （后续发现再展开）
  >
  >      1. 出 asan 割草机版本
  >
  >      2. x5 测试 asan 版本长期跑
  >
  >   3. slam 接入状态机的 RESET `@白世杰` （Done）
  >
  >      1. 代码完成时间：状态机改完 +1
  >
  >   * 尺度问题分析 `@肖鸿飞`，475408 代码已合入。

  * Action

    * 多帧对齐，尾端会差一点`@郭科`

      * 确定对齐长度，5m。umiyama 对齐时考虑姿态。

        * 确定对齐有没有更好的方案：考虑~~姿态角~~、权重。重复点剔除。

        * 确定最佳对齐长度、对齐候选点的选择方式。评估为 20m 距离。

    * 持续优化 okvis `@郭科`

      * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`

        * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

        * B1-37\_7.22\_105\_lake\_corrected 继续排查精度变差的问题

      * 同一个 landmark 被一个帧观测多次的 bug 解决 `@郭科`

      * 打点（坡度、badImu）

      * [ okvis非弓字精度提升](https://roborock.feishu.cn/docx/Yr0UdlAn4ojgqcxsfFWcY307nlb)

        * [ okvis+LET-Net深度学习光流](https://roborock.feishu.cn/docx/QVtMdLsEVo1uxyxmjNDcIb3Untf)

        * dev+草丛+非草丛区域光流算法补点

        * 先光流，后描述子匹配补点方法

        * 前端、LBA 代码精调 `@李宝玉`排期

    1. 斜坡测试和合入`@白世杰`  &#x20;

       1. [ 侧滑以及倾斜检测上机测试](https://roborock.feishu.cn/wiki/GReHwBESyitJBwkUqVrcC5a8nld)

* 深度学习特征点描述子引入

  > * 本周进展
  >
  >   * 给感知组输出 rerun 可视化的分析结果

  * Action

    * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图

    * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`

      * 代码合入 vl\_slam/develop

* 其他工作项

  > * 本周进展

  * Action

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * &#x20;水下视觉 slam 相关工作  `@白世杰`

      * 完成所有图像质量分析[ 泳池机器人图像质量分析](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)。 &#x20;

      * 完成 okvis 在泳池数据集上适当优化，并给出初步结论。[ 泳池机器人okvis和let vins测试](https://roborock.feishu.cn/wiki/MF1ewBTbWiUeNUkOKlzcsyJGnEh) &#x20;

      * 完成 letvins 在泳池数据集上跑通和优化，并给出初步结论。 &#x20;

      * 看噪点大的问题，是否能够比较好的过滤掉

***

* Okvis 全局图与回环检测`@肖鸿飞`

  > * 本周进展
  >
  >   * 窄通道建图需求[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) `@李波` `@陈飞`
  >
  >     * 代码逻辑写完
  >
  >     * 测试过程中[ 通道建图测试](https://roborock.feishu.cn/wiki/PUAtw4HsNikT2Vk7XYMc7q8onSf?from=from_copylink)
  >
  >     * 窄通道暂停功能消息接入`@李宝玉` `@李波`
  >
  >     * 充电桩通道无法结束，所以不建充电桩通道`@李宝玉`
  >
  >       * 退桩发开始建通道
  >
  >       * 很快到达建图起点，会自动生成通道，会发结束建通道消息，但是后续导航认为通道不存在。没有发删除通道。
  >
  >     * [ vimap online mapping - 3.2](https://roborock.feishu.cn/wiki/ATmjwX2DLizcHIkYWYNcvIeunAh)
  >
  >     * ceres2.3.0 单精度与 2.2.0 耗时对比`@肖鸿飞`[ 单精度优化精度批测](https://roborock.feishu.cn/wiki/OWoLwl4eOiw9GqkULKbcEwhqntg)
  >
  >       * 耗时无明显变化
  >
  >     * [ 多帧校验：多帧匹配修正T\_map\_vio](https://roborock.feishu.cn/wiki/NuIRww6ITihflCkmCcicYts7nMf)`@肖鸿飞`
  >
  >     * 回环检测时间[ Okvis 闭环检测效果分析](https://roborock.feishu.cn/wiki/JdEdwnYMsiJVb8kBAnPc7yeHnyh#share-DXb9dhr8Fo2L8BxIwjRc8XXUnMP)

  * Action

    * &#x20;[ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * 窄通道建图需求[ VSLAM窄通道建图需求](https://roborock.feishu.cn/wiki/SOMLwWwDkidugJk3bytc4Xv6nVe?open_in_browser=true) `@李波` `@陈飞`

      * 继续 debug

      * 异步优化

      * 很快到达建图起点，会自动生成通道，会发结束建通道消息，但是后续导航认为通道不存在。没有发删除通道。Push 导航发删除通道消息。

    * 在线 Maplab 建图 `@宋姝`[ vimap online mapping](https://roborock.feishu.cn/wiki/Lb97wrA7ii9ur1kPlVKcSj4NnNe)

      * 排查子图拼接精度较低 [ vimap online mapping - 3.2](https://roborock.feishu.cn/wiki/ATmjwX2DLizcHIkYWYNcvIeunAh)

      * 缩减建图规模：[ 建图规模缩减](https://roborock.feishu.cn/wiki/RgS8wgliei1hBGktpMecq2yMnHc) （进行中）

        * 优化后二次 keyframe 筛选；

        * 冗余 mission 删除；

      * 内存增长太大 PGO 会耗时过长：

        * 单目 Mapping 调优 `@宋姝` [ 单目 vs 双目 算法对比分析](https://roborock.feishu.cn/wiki/Pdn1wmFJ0iboaBkwh5icvgFYnQc)

        * 降低问题规模+引入 GTSAM

      * 重定位精度、召回率精度测试&#x20;

      * Todo 回环检测输出给 VIO 进行搬窗口

    * Maplab PGO `@江建文`

      * [ 后续工作计划](https://roborock.feishu.cn/wiki/EcmcwX3nGiTB6zkiVErcVsUxnV7?open_in_browser=true)

      * [ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?open_in_browser=true)

      * 错误闭环处理，继续批测，接入更大规模数据测试，分子图参数与`@宋姝`保持一致

    * Maplab Mapping & relocal `@刘博`

      * 子图内部优化后精度变差原因分析[ 子图大小对单子图精度影响分析](https://roborock.feishu.cn/wiki/Z3GMwy9FFiIFqAkqXY0cgZTunNa)

        * 是否因为没有光流，测试开光流的效果
          光流补充跟踪流程已打通，测试了一个数据集，精度无明显变化，good 地图点数量会明显增加，待增加调试打印后进一步分析、批测和整理文档

      * maplab 复用 okvis 跟踪与 landmark [ 链路3：地图点复用设计文档](https://roborock.feishu.cn/wiki/MIqPwfRP5imDp4kcCfVcH1MpnIq)

        * Okvis score 接入

        不额外计算 score，相信 OKVIS 结果

      * 整理一下修改项目，提出可调参数[ 建图分支提交整理](https://roborock.feishu.cn/wiki/Yxyhw9HTUismwfkYaMzcQPH4nFh)

      * 创建地图评分机制，区域分块好特征点评分

      * Faiss 的码表固定，以加速

    3. 全局 PGO `@陈飞`

       1. 搬窗口逻辑接入，realTimeGraph 的修改接入，测试整体精度 [ PGO功能测试](https://roborock.feishu.cn/docx/P5qCdhxLHoYxkSxMSvic1GH3nkd)

       2. 确定 PGO 本身的准确性：使用 RTK Pose 插值作为 PGO 约束

       3. 与 maplab 测试集对齐`@陈飞`

    * 重定位多帧校验`@李波`

      * 在线建图版本可视化信息加入，分析重定位效果。`@肖鸿飞`

      * 对假阳、假阴进行分析。[ 多帧校验：多帧匹配修正T\_map\_vio](https://roborock.feishu.cn/wiki/NuIRww6ITihflCkmCcicYts7nMf)`@肖鸿飞`

      * 问题集确定。

    * TODO

      2. VIO 初始化逻辑 `@郭科`

         * 优化

           1. 启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias

      * Okvis 版本多帧回环方案设计与实现`@李波`

      * 跟丢的逻辑设计 `@李宝玉`

      * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn) `@李宝玉`

        * 多子图

        * 开启的时候 coredump

        * 去掉桩点问题数据后重定位 `@肖鸿飞`

      * 地图质量检测

        * 上报优化成功/失败

        * 场地过于空阔，有效点特别远

      * 轻量化，解决多地图、支持灵活的增、删区域

      * VIO 边缘轨迹精度差，是否会影响割草机建图 `@李宝玉`

        * 闭合的瞬间，要很快地输出回环检测结果

        * 闭合后，要能够输出闭环优化后的轨迹

      * 假成功的分析与处理，bug fix（基于新采集数据，多帧数据交叉验证）`@肖鸿飞`[ Eden数据错误重定位分析](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb)

      [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260202

* 割草机内外参标定与检测

  * 相机-整机标定算法

    > * 本周进展
    >
    >   * CQIQC 代码重构 （PR 中）`@李宝玉`
    >
    >   * MCT 站双目之间外参标定开发中
    >
    >     * 采图出现问题
    >
    >       * 测试同学刷包异常
    >
    >   * 售后标定 BUG
    >
    >     * z 轴不 fix，导致 Toi 计算错误，标定失败
    >
    >   * thresh\_config，vendor07 PR 中

    * Action

      * 产线检测站问题排查

        * CQIQC 代码重构 `@李宝玉`

        * <span style="color: rgb(143,149,158); background-color: inherit">TODO 后续再尝试降低计算时间/数据量</span>

      * MCT 站双目之间外参标定

        * [ 售后双目基线标定开发计划](https://roborock.feishu.cn/wiki/PdAWwAtQNipZLlkrmBucqwxPneF?open_in_browser=true)

      * 检查 linediff `@邱冰冰`

      * 售后标定方案`@邱冰冰`

        * z 轴 fix，关闭侧目标定，进 hotfix `@李宝玉`

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查

        * 维护近期合入 prebuild dev 的 bug 列表，提出合入 Hotfix 的建议 `@邱冰冰`

      * 工厂标定算法优化

        * thresh\_config，vendor07 适配 PR 中`@李宝玉`

        * MCT 写入 tcrcl 到 dualcamera\_calibration.json `@李宝玉`

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

      * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测</span>`@邱冰冰`

        * 最终的 refine 去掉重投影误差大的数据（TODO）

        * 代码合入`@李宝玉`确定时间点

          * Monet B3, versa B2

      * <span style="color: rgb(143,149,158); background-color: inherit">联合模组供应商模组内外参标定结果审查</span>

        * <span style="color: rgb(143,149,158); background-color: inherit">内参标定成功，但是外参标定 TOC 误差大，和联合标定结果对比</span>`@李宝玉`

          * <span style="color: rgb(143,149,158); background-color: inherit">Tci，z 轴偏大</span>

* OKVIS-VIO 优化

  > * 本周进展
  >
  >   * OpenCL 增加打印，上机测试完成后合入 `@刘博` `@李宝玉`（Done）
  >
  >   * 本周更新 benchmark `@肖鸿飞`
  >
  >     * sftp://roborock@10.2.18.25/mnt/nvme1/benchmark\_v2.0/
  >
  >     * sftp://roborock@10.2.18.25/mnt/nvme1/benchmark\_v2.0\_vslam/
  >
  >   * Eden：确定回环检测原理，如果回环检测依赖初值，采集数据如下（Done， 暂时不采集数据）
  >
  >     * 进行数据采集，关 bumper 1、3、5、7、9s
  >
  >     * 确定是否 GAIA 用电流 bumper
  >
  >       * GAIA 不用电流 bumper
  >
  >     * 当前版本 okvis 回环检测不依赖初始位姿。回环是直接通过 Bow 查询的相似的历史关键帧，再通过关键帧和当前帧做 3d2d 匹配尝试回环 `@李波`
  >
  >   * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`[ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)
  >
  >     * 弓子间隔误差大，非弓字割草误差大
  >
  >     * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)
  >
  >       * B1-37\_7.22\_105\_lake\_corrected 继续排查精度变差的问题
  >
  >       * 草地跟踪差、有效特征点太远
  >
  >   * [ 颠簸路段数据分析](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd)
  >
  >     * RTK 异常，开 bug 给`@乔平平`&#x20;
  >
  >   * 内存踩踏分析 `@白世杰` &#x20;
  >
  >     * 0129 至今 asan 运行正常
  >
  >   * VIO Ceres master 单精度测试 `@肖鸿飞` [ 单精度优化精度批测](https://roborock.feishu.cn/wiki/OWoLwl4eOiw9GqkULKbcEwhqntg?open_in_browser=true)
  >
  >     * VIO 部分不合入，在建图的子图优化部分测试，有效果合入

  * Action

    * 持续优化 okvis `@郭科`

      * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`

        * [ vio上机压测精度分析](https://roborock.feishu.cn/docx/DjAqdqI2qomWUIxqx4DczjiOnOd)

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

        * B1-37\_7.22\_105\_lake\_corrected 继续排查精度变差的问题

    * 同一个 landmark 被一个帧观测多次的 bug 解决 `@郭科`

    2. VIO 初始化逻辑 `@郭科`

       1. 目标：定位稳定后输出姿态

       2. 确认：以后退桩的速度、轨迹 `@李欢`

       3. 初版：简单的过滤 &#x20;

          1. [ 视觉初始化优化](https://roborock.feishu.cn/wiki/IJOLw6PHEiFEkwkeP03cvZainBe?open_in_browser=true)

          2. [ okvis退桩位姿跳变](https://roborock.feishu.cn/docx/AsX8dMGhboVQdMxHw8pcG00mnHb)

       4. 优化

          1. 启动时做 SFM，得到初始化时间段内的姿态、速度、姿态角、Bias

    * 以补光灯的开关状态确定对外是否输出姿态 `@白世杰` &#x20;

      1. 第一次收到关灯不处理；

      2. 接到开灯消息后，不发姿态；

      3. 接到关灯消息后，统计开灯时长，大于 3s 的情况下，1 分钟开始发姿态。否则关灯就发姿态。

    - 暂停恢复逻辑 `@白世杰`&#x20;

      1. 优化：使用 gyro+odo 进行递推

    - 斜坡测试和合入`@白世杰`  &#x20;

      * [ 侧滑以及倾斜检测上机测试](https://roborock.feishu.cn/wiki/GReHwBESyitJBwkUqVrcC5a8nld)

    - 内存踩踏分析 `@白世杰` &#x20;

      1. 出 asan 割草机版本`@李宝玉`

  * VIO Ceres master 单精度测试 `@肖鸿飞` &#x20;

* 深度学习特征点描述子引入

  > * 本周进展

  * Action

    * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图

    * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`

      * 代码合入 vl\_slam/develop

* 其他工作项

  > * 本周进展
  >
  >   * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`
  >
  >     * 代码交接完成
  >
  >     * Push 侧目遮挡检测的数据采集，收到数据后再行开发， 交给交接同学推进
  >
  >   * &#x20;水下视觉 slam 相关工作  `@白世杰`
  >
  >     * 看看曝光时间是否存在与 AT 指令的文件上，看看有无大的波动。
  >
  >       * 画面亮度变化大和曝光时间无关。

  * Action

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * &#x20;[ Let-vins](https://roborock.feishu.cn/wiki/CLeOwfqOgiJGHmk0WMMcam1on3e)let vins 在割草机数据上测试  `@白世杰`P2

      * 更精细的引入 let-net

    * &#x20;水下视觉 slam 相关工作  `@白世杰`

      * 完成所有图像质量分析[ 泳池机器人图像质量分析](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)。 &#x20;

      * 完成 okvis 在泳池数据集上适当优化，并给出初步结论。 &#x20;

      * 完成 letvins 在泳池数据集上跑通和优化，并给出初步结论。 &#x20;

      * 看噪点大的问题，是否能够比较好的过滤掉

***

* Okvis 全局图与回环检测`@肖鸿飞`

  > * 本周进展
  >
  >   * 直接存 vimap、加载 VIMap，读入到 maplab。`@肖鸿飞`&#x20;
  >
  >     * 存图代码完成，debug 过程中发现加载、优化有问题
  >
  >   * Okvis 回环结果引入局部 BA`@郭科`
  >
  >     * 代码完成
  >
  >   3. 全局 PGO `@陈飞`
  >
  >      1. 搬窗口逻辑接入，realTimeGraph 的修改接入，测试整体精度 [ PGO功能测试](https://roborock.feishu.cn/docx/P5qCdhxLHoYxkSxMSvic1GH3nkd)
  >
  >   4. Okvis 版本多帧回环方案设计与实现`@李波`
  >
  >      1. [ Okvis 闭环检测效果分析](https://roborock.feishu.cn/wiki/JdEdwnYMsiJVb8kBAnPc7yeHnyh)
  >
  >   * 在线 Maplab 建图 `@宋姝`[ vimap online mapping](https://roborock.feishu.cn/wiki/Lb97wrA7ii9ur1kPlVKcSj4NnNe)
  >
  >     * 存 vimap，引入 okvis 的关键帧逻辑。代码完成。批测完成。
  >
  >     * Vimap 子图 merge 调试 （Done）
  >
  >     * 异步优化（Done）
  >
  >     * 地图分子图保存（Done）
  >
  >     * Okvis->Maplab 筛帧逻辑（Done）
  >
  >   * Maplab PGO `@江建文`
  >
  >     * [ isam\_PGO开发记录](https://roborock.feishu.cn/wiki/NqRDwmvreihQW3k1338cpusrnzb?from=auth_notice\&hash=dd6ba421bb9baea2d65d040079573ac0)
  >
  >   * Maplab Mapping & relocal `@刘博`
  >
  >     * maplab 复用 okvis 跟踪与 landmark
  >
  >       * 链路 0 1 2 打通，3 基本代码完成

  * Action

    * &#x20;[ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * 直接存 vimap、加载 VIMap，读入到 maplab。`@肖鸿飞`   确定开发周期

      * 形成单元测试

      * only\_optimize 调通

      * Ceres 单精度测试

    3. 全局 PGO `@陈飞`

       1. 搬窗口逻辑接入，realTimeGraph 的修改接入，测试整体精度 [ PGO功能测试](https://roborock.feishu.cn/docx/P5qCdhxLHoYxkSxMSvic1GH3nkd)

       2. 确定 PGO 本身的准确性：使用 RTK Pose 插值作为 PGO 约束

       3. 与 maplab 对齐`@陈飞`

    * Okvis 版本多帧回环方案设计与实现`@李波`

      * 回环检测时间[ Okvis 闭环检测效果分析](https://roborock.feishu.cn/wiki/JdEdwnYMsiJVb8kBAnPc7yeHnyh?from=from_copylink)

    * 在线 Maplab 建图 `@宋姝`[ vimap online mapping](https://roborock.feishu.cn/wiki/Lb97wrA7ii9ur1kPlVKcSj4NnNe)

      * 密集弓字、乱走、走坡数据测试

    * 窄通道建图需求`@李宝玉`

    * Maplab PGO `@江建文`

      * [ 后续工作计划](https://roborock.feishu.cn/wiki/EcmcwX3nGiTB6zkiVErcVsUxnV7?open_in_browser=true)

    * Maplab Mapping & relocal `@刘博`

      * maplab 复用 okvis 跟踪与 landmark

      * [ 整图建图耗时优化](https://roborock.feishu.cn/wiki/PnomwN0a1ipQnVkL5pTcoXhanef)

        * 整理一下修改项目，提出可调参数

      * 创建地图评分机制，区域分块好特征点评分

      * Fassi 的码表固定，以加速

    * 重定位多帧校验`@李波`

      * 问题集确定

    * TODO

      * 跟丢的逻辑设计 `@李宝玉`

      * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn) `@李宝玉`

        * 多子图

        * 开启的时候 coredump

        * 去掉桩点问题数据后重定位 `@肖鸿飞`

      * 地图质量检测

        * 上报优化成功/失败

        * 场地过于空阔，有效点特别远

      * 轻量化，解决多地图、支持灵活的增、删区域

      * VIO 边缘轨迹精度差，是否会影响割草机建图 `@李宝玉`

        * 闭合的瞬间，要很快地输出回环检测结果

        * 闭合后，要能够输出闭环优化后的轨迹

      * 假成功的分析与处理，bug fix（基于新采集数据，多帧数据交叉验证）`@肖鸿飞`[ Eden数据错误重定位分析](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb)（Pending）

      [ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260126

* 割草机内外参标定与检测

  * 相机-整机标定算法

    > * 本周进展
    >
    >   * CQIQC 代码重构完成，5 个数据测试完成后，小数点后三位完全一致（Done）
    >
    >   * 欧菲模组测试 3 个不过
    >
    >     * CIIQC，不通过的项`@邱冰冰`
    >
    >   * 欧菲 MCT 测试不通过问题
    >
    >     * 走 8 字卡顿，导致轮子半径、轴距标定不通过
    >
    >     * IMU 参数有变化，需要适配
    >
    >   * 数据问题：
    >
    >     * Push `@丁毅` `@黄亮`解决标定失败时的数据无法保存的问题 `@邱冰冰`已解决

    * Action

      * 产线检测站问题排查

        * CQIQC 代码重构 `@李宝玉`

        * <span style="color: rgb(143,149,158); background-color: inherit">TODO 后续再尝试降低计算时间/数据量</span>

      * MCT 站双目之间外参标定

      * 检查 linediff

      * 售后标定方案`@邱冰冰`

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

      * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测，提升优先级 </span>`@邱冰冰`

        * 最终的 refine 去掉重投影误差大的数据（TODO）

        * 代码合入`@李宝玉`确定时间点

          * Monet B3, versa B2

      * <span style="color: rgb(143,149,158); background-color: inherit">联合模组供应商模组内外参标定结果审查</span>

        * <span style="color: rgb(143,149,158); background-color: inherit">内参标定成功，但是外参标定 TOC 误差大，和联合标定结果对比</span>`@李宝玉`

          * <span style="color: rgb(143,149,158); background-color: inherit">Tci，z 轴偏大</span>

* OKVIS 调优

  > * 本周进展
  >
  >   * 颠簸问题 `@郭科`
  >
  >     * 滤波方案，效果较差
  >
  >     * okvis pr 138 增大噪声应对颠簸场景
  >
  >       * IMU 波动大，实现 Gyro + ODO 递推
  >
  >         * [ 颠簸路段数据分析](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd)
  >
  >     * okvis pr 139 增加视觉打滑检测应对卡困打滑场景

  * Action

    * 持续优化 okvis `@郭科`

      * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

        * B1-37\_7.22\_105\_lake\_corrected 继续排查精度变差的问题

      * [ 颠簸路段数据分析](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd)

        * RTK 异常，开 bug 给`@乔平平`

      * Eden：确定回环检测原理，如果回环检测依赖初值，采集数据如下

        * 进行数据采集，关 bumper 1、3、5、7、9s

        * 确定是否 GAIA 用电流 bumper

      * tracklost 逻辑优化 `@李宝玉`

    * 斜坡数据分析与调优：现在机器可能从斜坡桩出

      * 本周更新 benchmark `@李宝玉`

    * OpenCL 增加打印，上机测试完成后合入 `@李宝玉`

* 深度学习特征点描述子引入

  > * 本周进展
  >
  >   * okvis 接入感知提点与描述子 so 的 PC 版本，仿真测试完成
  >
  >   * 上机打包出 slam.archive 中，感知同学需要用 GDC NV12
  >
  >     * 目前给感知原图彩图
  >
  >   * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`，Done
  >
  >     * Rebase 最新 vl\_slam/develop

  * Action

    * 打包出上机的 slam.archive，感知同学需要用 GDC NV12，目前给感知原图彩图

    * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`

      * 代码合入 vl\_slam/develop

* 其他工作项

  > * 本周进展
  >
  >   * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`
  >
  >     * 确定探照灯对补光灯的影响，是否合理。补光灯算法问题，交由 `@汪浩然`解决
  >
  >     * 检测算法代码（包含侧目检测）整理给`@汪浩然`由他们维护
  >
  >     * 修改 SLAM 初始化时机 （Done）
  >
  >   * Feature map 转为灰度图 -> 之后给 okvis `@白世杰`https://roborock.feishu.cn/wiki/KM0ewRxXQit4t1kQ1LJcsIPfn6h
  >
  >   * [ 泳池机器人测试0116](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)

  * Action

    * 以补光灯的开关状态确定对外是否输出姿态 `@李宝玉`

    * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`

      * Push 侧目遮挡检测的数据采集，收到数据后再行开发

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * &#x20;[ Let-vins](https://roborock.feishu.cn/wiki/CLeOwfqOgiJGHmk0WMMcam1on3e)let vins 在割草机数据上测试

      * 更精细的引入 let-net

      * [ 水下视觉slam相关调研](https://roborock.feishu.cn/wiki/Wuu2wsnZsikeyrk9obdcLg0Snxe)

      * [ 泳池机器人测试0116](https://roborock.feishu.cn/wiki/Jei0wKqzvimvRekqAqAc0ynWneh)

      * 看看曝光时间是否存在与 AT 指令的文件上，看看有无大的波动

      * 看噪点大的问题，是否能够比较好的过滤掉

***

* Okvis 全局图与回环检测`@肖鸿飞`

  > * 本周进展
  >
  >   * LoopClosure 结果复用[ 找回环时间优化](https://roborock.feishu.cn/wiki/VeOKwHh1PibM3ukNYp3caovRnbd)
  >
  >     * Faiss 的聚类码本训练：可以固定
  >
  >     * Database 按照码本散列：不可固定
  >
  >       * Database 中所有描述子和 query 帧的描述子，都可省下索引码本的时间；
  >
  >     * 描述子 KNN serch 因为数据库会变化、导致不可复用：不可固定
  >
  >   * Okvis FeatureTrack 结果利用[ OKVIS 跟踪与地图点复用总结](https://roborock.feishu.cn/wiki/B3jzwtkF1i6pCpk1s63cn7mbnzb)
  >
  >   * 直接存 vimap、加载 VIMap。`@肖鸿飞`   确定开发周期
  >
  >     * 描述子、特征位置写完成
  >
  >     * okvis->vimap 其他部分未完成
  >
  >     * 读入到 maplab
  >
  >   * Okvis 回环引入局部 BA 的方案整理
  >
  >     * 代码完成
  >
  >     * 回环时，能够搬动窗口
  >
  >     * 小回环（弓子时），只搬位姿不搬点
  >
  >     * 支持回环检测后姿态纠正（Done）
  >
  >   * 整理 okvis 现有的全局图优化流程，确定修改方案  &#x20;
  >
  >     * 解决 fullGraph coredump 问题，能够做 PGO Done
  >
  >     * PGO 的结果同步入 realtimeGraph Done
  >
  >     * Static point 对 PGO 的影响
  >
  >     * 支持运行过程中回环检测、触发全局图优化 Done
  >
  >   * Okvis 版本多帧回环方案设计与实现`@李波`
  >
  >     * 多线程回环检测打通
  >
  >     * 重定位姿态精度统计（同一份数据，看看 vio 输出的姿态，和重定位的姿态的差别） 初步统计完成
  >
  >   * 补测重定位数据 `@肖鸿飞`
  >
  >     * 105-3 还未完成，密集弓子和 2m 弓子 90°，已让补采，完成
  >
  >     * 补测重定位数据，加入 benchmark （Done）
  >
  >   * 在线 Maplab 建图
  >
  >     * Online vimap 构建完成
  >
  >     * Online KF 筛选，生成子图
  >
  >     * Vimap 子图 merge，额外两个子图之间查、加回环边

  * Action

    * &#x20;[ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * 直接存 vimap、加载 VIMap，读入到 maplab。`@肖鸿飞`   确定开发周期

      * 形成单元测试

      * only\_optimize 调通

    * Okvis 回环引入局部 BA 的方案整理。`@郭科` &#x20;

      * 支持加载地图后重定位

    3. 全局 PGO `@陈飞`

       1. 搬窗口逻辑接入，realTimeGraph 的修改接入，测试整体精度

    * Okvis 版本多帧回环方案设计与实现`@李波`

      * 回环检测时间

      ![](<images/VSLAM 进度同步 -2026-image.png>)

    * 地图质量检测

      * 上报优化成功/失败

      * 场地过于空阔，有效点特别远

    * 轻量化，解决多地图、支持灵活的增、删区域

    * VIO 边缘轨迹精度差，是否会影响割草机建图 `@李宝玉`

      * 闭合的瞬间，要很快地输出回环检测结果

      * 闭合后，要能够输出闭环优化后的轨迹

  * 建图 Action

    * 在线 Maplab 建图

      * 存 vimap，引入 okvis 的关键帧逻辑

      * Vimap 子图 merge 调试

      * 异步优化

      * 地图分子图保存

    * Maplab Mapping & relocal `@刘博`

      * maplab 复用 okvis 跟踪与 landmark

        * Okvis->Maplab 筛帧逻辑

      * 发现问题（todo）

        * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn) `@李宝玉`

          * 多子图

          * 开启的时候 coredump

        * [ 整图建图耗时优化](https://roborock.feishu.cn/wiki/PnomwN0a1ipQnVkL5pTcoXhanef)

          * 整理一下修改项目，提出可调参数，准备 PR[ 建图耗时优化分析报告](https://roborock.feishu.cn/wiki/WpMcw4zAWiEkPMk7nZQcC0Obn4c)

        * PGO

        * 创建地图评分机制，区域分块好特征点评分

  * 重定位 Action&#x20;

    * 去掉桩点问题数据后重定位 `@肖鸿飞`

    * 重定位多帧校验`@李波`

      * 问题集确定

    * 假成功的分析与处理，bug fix（基于新采集数据，多帧数据交叉验证）`@肖鸿飞`[ Eden数据错误重定位分析](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb)（Pending）

[ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260119

* 割草机内外参标定与检测

  * 相机-整机标定算法

    * 本周进展

      * CQIQC（滑轨站）三点位行差统计结果[ 产线MCT整机外参标定数据统计](https://roborock.feishu.cn/wiki/B51KwQTpqiM0ETkxfOScduRinFX?sheet=Aepdig)

        &#x20;

        * 三个位置的行差差别，最大 0.3 像素。

        * 三个点位的行差大小，具备一致性。

      * CIIQC 中的 gyro 检测部分重构完成`@邱冰冰`

      * 欧菲光双目模组导入支持

        * CIIQC 数据收到部分，直接跑会 core，正在排查`@邱冰冰`

        * MCT 站捋了一下代码

          * 算法代码不需要更新

          * 测试同学的脚本需要更新

          * threshold.json 适配

          * 读取 config

    * Action

      * 欧菲光双目模组导入支持

        * IQC 站支持`@邱冰冰`

        * MCT 标定适配`@邱冰冰`

        * Tuning 结果验收`@肖鸿飞`

      * 产线检测站问题排查

        * CIIQC

        * CQIQC 代码重构 `@李宝玉`

        * <span style="color: rgb(143,149,158); background-color: inherit">TODO 后续再尝试降低计算时间/数据量</span>

      * MCT 站双目之间外参标定 `@李宝玉`

      * 售后标定方案`@邱冰冰`

        * 数据问题：

          * Push `@丁毅` `@黄亮`解决标定失败时的数据无法保存的问题 `@邱冰冰`

        * 拉分支，保存当前产线版本状态

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

      * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测，提升优先级 </span>`@邱冰冰`

        * 最终的 refine 去掉重投影误差大的数据（TODO）

        * 代码合入`@李宝玉`确定时间点

          * Monet B3, versa B2

      * <span style="color: rgb(143,149,158); background-color: inherit">联合模组供应商模组内外参标定结果审查</span>

        * <span style="color: rgb(143,149,158); background-color: inherit">内参标定成功，但是外参标定 TOC 误差大，和联合标定结果对比</span>`@李宝玉`

          * <span style="color: rgb(143,149,158); background-color: inherit">Tci，z 轴偏大</span>

* OKVIS 调优

  * 本周进展

    * 要测试同学，专门跑 VSLAM 版本`@李宝玉`

      * 要到了专用测试同学，先跑 VIO 看漏割情况

      * 已收集 5-6 组数据

    * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)更新

      * 颠簸有几个预期的方案

      * 打滑需要采集数据，验证回环成功率

    * [ X5批测与PC批测精度对比](https://roborock.feishu.cn/docx/Y2VGd4y78oOm64xdBRWcy4NFnBW)

      * 看一下跑机时的实际丢帧

    * 收集夜间数据，排查夜间的图像特点，输出夜间的上报 vslam 轨迹精度不佳的功能

      * 以补光灯的开关状态确定对外是否输出姿态

  * Action

    * 持续优化 okvis `@郭科`

      * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`

      * [ okvis弓字间隔不均匀](https://roborock.feishu.cn/docx/GzePdKl8DojbVLxDVZIcqldoncb)

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

        * bumper 拔掉

        * 手拉

        * 37\_7.22\_105\_lake\_corrected，效果变差、阈值参数分析

      * [ 颠簸路段数据分析](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd)

        1. 感知识别鹅卵石

        2. 滤波方案

        3. Gyro + ODO 递推方案

        4. 高频 IMU 方案

      * 确定回环检测原理，如果回环检测依赖初值，采集数据如下

        * 进行数据采集，关 bumper 1、3、5、7、9s

      * tracklost 逻辑优化

    * 斜坡数据分析与调优：现在机器可能从斜坡桩出

      * 斜坡数据采集完成后更新 benchmark+精度指标

        * `@郭科`加入困难场景数据

        * `@白世杰`加入斜坡场景数据

      * Benchmark 筛选`@郭科`目标 30 个数据以内

    * OpenCL 增加打印，上机测试完成后合入 `@李宝玉`

* 深度学习特征点描述子引入

  * 本周进展

    * okvis 接入感知提点与描述子 so 的 PC 版本，仿真测试完成后进行上机测试，接入完成

  * Action

    * okvis 接入感知提点与描述子 so 的 PC 版本，仿真测试完成后进行上机测试

    * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`

      * 代码结构调整

      * Rebase 最新 vl\_slam/develop

    * 模型精度测试跟进

      * Xfeat pc 测试

      * 板端测试（xfeat）

      * 测试 brisk+nn（优先级低）

* 其他工作项

  * 本周进展

    * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`

      * 测试采集排队中

  * Action

    * 以补光灯的开关状态确定对外是否输出姿态 `@李宝玉`

    * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`

      * Push 侧目遮挡检测的数据采集，收到数据后再行开发

      * Push 导航，修改代码版本，复测

      * 修改 SLAM 初始化时机

      * 确定探照灯对补光灯的影响，是否合理

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * &#x20;[ Let-vins](https://roborock.feishu.cn/wiki/CLeOwfqOgiJGHmk0WMMcam1on3e)let vins 在割草机数据上测试

      * Feature map 转为灰度图 -> 之后给 okvis `@白世杰`

      * [ 水下视觉slam相关调研](https://roborock.feishu.cn/wiki/Wuu2wsnZsikeyrk9obdcLg0Snxe)

***

* Okvis 全局图与回环检测`@肖鸿飞`

  * 本周进展

    * 直接存 vimap、加载 VIMap，读入到 fullGraph。

      * frame 内描述子，特征点已经序列化完成

    * Okvis 回环引入局部 BA 的方案整理。`@郭科` &#x20;

    * Okvis 版本多帧回环方案设计与实现`@李波`

      * 初步打通，目前在前端发起回环检测

    * Maplab Mapping & relocal `@刘博`

      * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn)

  * Action

    * &#x20;[ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)&#x20;

    * 直接存 vimap、加载 VIMap，读入到 fullGraph。`@肖鸿飞`   确定开发周期

      * 形成单元测试

    * Okvis 回环引入局部 BA 的方案整理。`@郭科` &#x20;

      * 只保存一份全局图

      * 支持加载地图后重定位

      * 支持运行过程中回环检测、触发全局图优化

      * 支持回环检测后姿态纠正

    3. 全局 PGO `@陈飞`

       * 整理 okvis 现有的全局图优化流程，确定修改方案  &#x20;

    * Okvis 版本多帧回环方案设计与实现`@李波`

      * 确定开发周期 &#x20;

      * 重定位姿态精度统计（同一份数据，看看 vio 输出的姿态，和重定位的姿态的差别）

      * 打通多线程的 okvis 回环检测

      1. 输出回环检测结果至输出队列

    * 地图质量检测

      * 上报优化成功/失败

      * 场地过于空阔，有效点特别远

    * 轻量化，解决多地图、支持灵活的增、删区域

    * VIO 边缘轨迹精度差，是否会影响割草机建图 `@李宝玉`

      * 闭合的瞬间，要很快地输出回环检测结果

      * 闭合后，要能够输出闭环优化后的轨迹

    * 补测重定位数据 `@肖鸿飞`

      * 105-3 还未完成，密集弓子和 2m 弓子 90°，已让补采，完成

  * 建图 Action

    * Maplab Mapping & relocal `@刘博`

      * 实现接口：去掉桩点[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn) `@李宝玉`

        * 优化完成后删除

      * 发现问题（todo）

        * [ 整图建图耗时优化](https://roborock.feishu.cn/wiki/PnomwN0a1ipQnVkL5pTcoXhanef)

          * 整理一下修改项目，提出可调参数，准备 PR[ 建图耗时优化分析报告](https://roborock.feishu.cn/wiki/WpMcw4zAWiEkPMk7nZQcC0Obn4c)

        * LoopClosure 结果复用

        * Okvis FeatureTrack 结果利用

        * Okvis->Maplab 筛帧逻辑

        * PGO

        * 创建地图评分机制，区域分块好特征点评分

  * 重定位 Action

    * 去掉桩点问题数据后重定位[ 桩点移除](https://roborock.feishu.cn/wiki/Rz0ow8HeBiUeo7kmtsccdnUJnOn)

    * 补测重定位数据，加入 benchmark`@肖鸿飞`

    * 重定位多帧校验`@李波`（Pending）

      * 问题集确定

    * 假成功的分析与处理，bug fix（基于新采集数据，多帧数据交叉验证）`@肖鸿飞`[ Eden数据错误重定位分析](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb)

[ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

# 20260112

* 割草机内外参标定与检测

  * 相机-整机标定算法

    * 本周进展

    * Action

      * 产线检测站问题排查

        * CIIQC、CQIQC 代码重构

        * <span style="color: rgb(143,149,158); background-color: inherit">TODO 后续再尝试降低计算时间/数据量</span>

      * 售后标定方案`@邱冰冰`

        * 数据问题：

          * Push `@丁毅` `@黄亮`解决标定失败时的数据无法保存的问题 `@邱冰冰`

        * 拉分支，保存当前产线版本状态

        * 分析定位 PC 与 ARM 编译后，标定结果的差异排查

      * 工厂标定算法优化

        * 打滑检测优化

          * 第二阶段：起始、终止时刻，VSLAM 轨迹与 Odo 递推轨迹起点和终点的差

      * <span style="color: rgb(143,149,158); background-color: inherit">二驱标定算法检测重投影误差检测，提升优先级 </span>`@邱冰冰`

        * 最终的 refine 去掉重投影误差大的数据（TODO）

        * 代码合入`@李宝玉`确定时间点

          * Monet B3, versa B2

      * <span style="color: rgb(143,149,158); background-color: inherit">联合模组供应商模组内外参标定结果审查</span>

        * <span style="color: rgb(143,149,158); background-color: inherit">内参标定成功，但是外参标定 TOC 误差大，和联合标定结果对比</span>`@李宝玉`

          * <span style="color: rgb(143,149,158); background-color: inherit">Tci，z 轴偏大</span>

* OKVIS 调优

  * 本周进展

    * RTKImageChecker 内存泄漏检查`@林子越`组排查

    * Reinit 多个连续重新初始化导致卡住，代码已 PR，上机测试中`@郭科`

    * [ X5批测与PC批测精度对比](https://roborock.feishu.cn/docx/Y2VGd4y78oOm64xdBRWcy4NFnBW)

    * [ okvis2官方改动](https://roborock.feishu.cn/docx/SSm6dIaYNom8hgxk8yOcbZSNnqd)

    * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

    * 放羊版本不带光流的问题：鸿飞出的一个包，把光流去掉了，后续又被覆盖回来了，RTM 分支上确定有光流&#x20;

    * 斜坡数据分析与调优：现在机器可能从斜坡桩出[ 斜坡数据采集需求](https://roborock.feishu.cn/wiki/QMF7w1hh1izzJ8kAOrKcBjBLnZW)`@白世杰`

      * 确定 benchmark 有没有侧滑问题，图像看不出来，从测试同学反馈是存在的

        * 针对侧滑，排查打滑检测针对侧滑是否能够有优化 [ 斜坡上轮式侧滑分析](https://roborock.feishu.cn/wiki/CbnHwhWebiz8qtkXsYCcXhQxnih)

      * [ 斜坡上轮式侧滑分析](https://roborock.feishu.cn/wiki/CbnHwhWebiz8qtkXsYCcXhQxnih)

      * benchmark 斜坡数据，做坡度计算效果无提升，排查原因 [ 调整打滑检测平移和旋转阈值](https://roborock.feishu.cn/wiki/EmK9wiaudiEoTakElgUcPKWfnge)

        * 加入光流后，结合坡度检测精度提升明显

  * Action

    * 持续优化 okvis `@郭科`

      * 找研发测试，先跑 RTK+VIO 看漏割情况 `@郭科`

      * [ okvis弓字间隔不均匀](https://roborock.feishu.cn/docx/GzePdKl8DojbVLxDVZIcqldoncb)

      * [ okvis困难场景数据分析](https://roborock.feishu.cn/docx/Dm9idLBnNovt3IxORvgcvxclnfc)

        * bumper 拔掉

        * 手拉

        * 37\_7.22\_105\_lake\_corrected，效果变差、阈值参数分析

      * [ 颠簸路段数据分析](https://roborock.feishu.cn/wiki/DTKdwdixGiR0c9kgi1pc9lkinhd)

      * [ X5批测与PC批测精度对比](https://roborock.feishu.cn/docx/Y2VGd4y78oOm64xdBRWcy4NFnBW)

        * 看一下跑机时的实际丢帧

      * 收集夜间数据，排查夜间的图像特点，输出夜间的上报 vslam 轨迹精度不佳的功能

      * 要测试同学，专门跑 VSLAM 版本`@李宝玉`

        * 先跑 VIO 看漏割情况

    * 斜坡数据分析与调优：现在机器可能从斜坡桩出

      * 互补滤波接入`@李岩` `@林子越`

      * 斜坡数据采集完成后更新 benchmark+精度指标

        * `@郭科`加入困难场景数据

        * `@白世杰`加入斜坡场景数据

    * OpenCL 增加打印，上机测试完成后合入

* 深度学习特征点描述子引入

  * 本周进展

    * 使用深度学习描述子的版本，Rebase 最新的 develop

    * okvis 接入感知 so 的 x5 版本完成，PC 版本待完成

  * Action

    * okvis 接入感知提点与描述子 so 的 PC 版本，仿真测试完成后进行上机测试

    * 代码整理，看看能否和入现在的 dev，通过参数配置选择 pipeline `@陈飞`

      * 代码结构调整

      * Rebase 最新 vl\_slam/develop

    * 模型精度测试跟进

      * Xfeat pc 测试

      * 板端测试（xfeat）

      * 测试 brisk+nn（优先级低）

* 其他工作项

  * 本周进展

    * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`

      * 双目收敛后，侧目还没收敛，导致侧目的检测没完成

      * 分享算法给感知同学

      * 雷达启动 12s，SLAM 之后才能初始化，导致补光灯消息接受不到，导致夜间误判

  * Action

    * [<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">404111 </span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)">Butchart WI 遮挡检测初版开发</span>**<span style="color: rgb(36,91,219); background-color: rgb(242,243,245)"> </span>](http://pms.rockrobo.internal/index.php?m=bug\&f=view\&bugID=404111)`@李波`

      * Push 侧目遮挡检测的数据采集，收到数据后再行开发

      * Push 导航，修改代码版本，复测

      * 修改 SLAM 初始化时机

      * 确定探照灯对补光灯的影响，是否合理

    * 仿真数据生成`@白世杰`

      * 尝试做成割草机的硬件结构

      * 房子、盆景的简单点的环境

      * 割草机参数配置入仿真程序，生成一组数据

    * &#x20;[ Let-vins](https://roborock.feishu.cn/wiki/CLeOwfqOgiJGHmk0WMMcam1on3e)let vins 在割草机数据上测试

      * Feature map 转为灰度图 -> 之后给 okvis `@白世杰`

***

* Okvis 全局图与回环检测`@肖鸿飞`

  * 本周进展

    * 加上帧间相对约束的建图结果[ 1.4调优后整图光流两米弓子建图](https://roborock.feishu.cn/wiki/O2WswDZ8eiHqrckNrkncbyACn0c)

    * 单目关键帧建图[ 下采样精度变化](https://roborock.feishu.cn/wiki/E6NgwGciCi9IOCkbEkwcTwhMnSe)+帧间约束+ceres 优化加速[ 整图建图耗时优化](https://roborock.feishu.cn/wiki/PnomwN0a1ipQnVkL5pTcoXhanef)

    * 全局图重定位多线程策略设计与实现`@李波`[ okvis多线程重定位测试](https://roborock.feishu.cn/wiki/YsX4wM6daiFgWYkIeeRcVA5Vnpe?from=from_copylink)（Done）

    * 补测重定位数据 `@肖鸿飞`

      * 105-2 补采完成

      * 105-3 还未完成，密集弓子和 2m 弓子 90°，已让补采

    * [ 12.30-建图+重定位误差分布直方图统计.](https://roborock.feishu.cn/wiki/LxotwaPiyiFj0ckd1GvcBUpUnSe?open_in_browser=true) [ 重定位问题数据分析](https://roborock.feishu.cn/wiki/JGZjwVASmiZrdukzHlGccMVnnqh#share-P61hdw0LDoBpzvx9mFqcXjwbn7N)问题排查 `@李波`

    * 颠簸数据

  * Action

    * Action 整理 [ 全局图工作项](https://roborock.feishu.cn/wiki/L6X0wbVW6iqeHFkKc0DcGBxYnKe) [ Eden VSLAM算法方案](https://roborock.feishu.cn/wiki/G945wXkCriO7vwkIqzdcVw9DnJe) [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd) `@李宝玉`

    * 直接存 vimap、加载 VIMap，读入到 fullGraph。`@肖鸿飞`   确定开发周期

      * 形成单元测试

    * Okvis 回环引入局部 BA 的方案整理。`@郭科` &#x20;

      * 只保存一份全局图

      * 支持加载地图后重定位

      * 支持运行过程中回环检测、触发全局图优化

      * 支持回环检测后姿态纠正

    3. 全局 BA 优化 or PGO `@陈飞`

       * 整理 okvis 现有的全局图优化流程，确定修改方案  &#x20;

    * Okvis 版本多帧回环方案设计与实现`@李波`

      * 确定开发周期 &#x20;

      * 重定位姿态精度统计（同一份数据，看看 vio 输出的姿态，和重定位的姿态的差别）

      * 打通多线程的 okvis 回环检测

      1. 输出回环检测结果至输出队列

    * 地图质量检测

      * 上报优化成功/失败

      * 场地过于空阔，有效点特别远

    * 轻量化，解决多地图、支持灵活的增、删区域

    * 确定建图时，VIO 边缘轨迹精度差，是否会影响建图 `@李宝玉`

  * 建图 Action

    * Maplab Mapping & relocal `@刘博`

      * 实现接口：去掉桩点

      * 发现问题（todo）

        * [ 整图建图耗时优化](https://roborock.feishu.cn/wiki/PnomwN0a1ipQnVkL5pTcoXhanef)

          * 整理一下修改项目，提出可调参数，准备 PR

        * 尝试把 loop\_closure::FrameToMatches frame\_matches；弄成一个 static 变量，或者成员变量（能提供 clear 接口释放内存）

        * 创建地图评分机制，区域分块好特征点评分

        * 序列化功能，减小 IO 压力（对算法无影响）

        * 地图尺度问题

          * 期望缩短 2m 弓字与边界的距离更新进 [ Eden VSLAM视觉建图摸底同步](https://roborock.feishu.cn/wiki/UBCOwSfbNiAmSCkAIYNcTx1anhd)`@刘博`

        * Pending 子图拼接有不成功或者跳变的可能

          * 构建优化问题增加约束进行子图拼接

          * 按时间顺序建立多子图块，区块有更新后重新进行拼接尝试

          * 更改子图拼接策略，先找区域最大的，然后找共视高的开始拼接

          * 考虑可以沿用之前 okvis 子图的位姿变化

  * 重定位 Action

    * 补测重定位数据 `@肖鸿飞`

      * 105-3 还未完成，密集弓子和 2m 弓子 90°，已让补采

    * 重定位多帧校验`@李波`（Pending）

      * 问题集确定

    * 假成功的分析与处理，bug fix（基于新采集数据，多帧数据交叉验证）`@肖鸿飞`[ Eden数据错误重定位分析](https://roborock.feishu.cn/wiki/UEdnwwD1gi6wlTkLD2zcYDvVnHb)

    * 全局图重定位多线程策略设计与实现`@李波`[ okvis多线程重定位测试](https://roborock.feishu.cn/wiki/YsX4wM6daiFgWYkIeeRcVA5Vnpe?from=from_copylink)

      * 调整，使用 kf 进行重定位，基于 kf+时间，降频

    * 重定位问题持续分析解决

      * [ 重定位问题数据分析](https://roborock.feishu.cn/wiki/JGZjwVASmiZrdukzHlGccMVnnqh#share-P61hdw0LDoBpzvx9mFqcXjwbn7N)

        * 周三后开始提 PR 合入 `@李波`

      * [ benchmark跨序列重定位结果](https://roborock.feishu.cn/wiki/Lafkwp7vpiVGzVkFn7CcLYGbnCb)问题排查解决`@肖鸿飞`

        * 加载地图反而精度变差

      * [ 12.01 版本benchmarks 建图效果](https://roborock.feishu.cn/wiki/ErpbwgAo5ir9KMkjHXPc5Yk3n8c)里面列的问题`@肖鸿飞`

        * 发现轨迹弯折

      * [ Rebase后重定位分支的benchmark批测](https://roborock.feishu.cn/wiki/F6iqwJcruiJmu2kFA9WcuBEmngd)

        * 发现错误重定位

        * 上机和仿真重定位结果不一致

      * [ 0112测试结果](https://roborock.feishu.cn/docx/CpordUL5Jop2OgxQpK4c7eUdnrR)轨迹跳变

      * [ 地图优化前后精度及重定位效果](https://roborock.feishu.cn/wiki/A3n1w39UjiOfmUk8plIcKYohnFf?open_in_browser=true)

      * 割草过程中有较长时间未成功重定位

      * 北京石头大厦上机运行，数据误差大的根因分析`@肖鸿飞`

[ Butchart 低优先级TODO](https://roborock.feishu.cn/docx/MCeudNAjOo8E7DxcjJhcUs9unme)

