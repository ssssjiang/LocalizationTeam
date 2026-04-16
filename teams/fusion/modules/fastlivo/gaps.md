# Fast-LIVO2 全景地图预研 — Gaps

> 模块：`teams/fusion/modules/fastlivo/`
> 来源 inbox：`teams/fusion/inbox/004_融合定位/002_算法文档/011_Fast-livo`

---

## 外部链接（本地无对应文件）

### G-001 激光-视觉标定问题（飞书 wiki）

- **链接**：[https://roborock.feishu.cn/wiki/EF4dwzoMRiONYKk1LR8cDKBcnFd](https://roborock.feishu.cn/wiki/EF4dwzoMRiONYKk1LR8cDKBcnFd)
- **首次提及**：003_FAST-LIVO2点云赋色&定位&内存占用 -- 20251203

### G-002 EDL shader 原理&调研（飞书 wiki）

- **链接**：[https://roborock.feishu.cn/wiki/ZhtAwVlkhiiWuWkku8NcOPHXncc](https://roborock.feishu.cn/wiki/ZhtAwVlkhiiWuWkku8NcOPHXncc)
- **首次提及**：004_割草机全景地图预研功能简介

### G-003 FAST-LIVO2 优化（飞书 wiki）

- **链接**：[https://roborock.feishu.cn/wiki/VNmswkWMCinfLukcZP5cQVK3nAf](https://roborock.feishu.cn/wiki/VNmswkWMCinfLukcZP5cQVK3nAf)
- **首次提及**：003_FAST-LIVO2点云赋色&定位&内存占用 -- 20251203

### G-004 FAST-Calib（扫描式 lidar-camera 外参标定开源实现）

- **链接**：[https://github.com/hku-mars/FAST-Calib](https://github.com/hku-mars/FAST-Calib)
- **首次提及**：`inbox/0412新增/扫描式多线lidar与camera标定调研总结`（D-008 推荐参考实现）

### G-005 velo2cam_calibration（对比参考实现）

- **链接**：[https://github.com/beltransen/velo2cam_calibration](https://github.com/beltransen/velo2cam_calibration)
- **首次提及**：`inbox/0412新增/扫描式多线lidar与camera标定调研总结`（2021年，FAST-Calib 对比基准）

---

## Open 问题（结论待确认）

### Q-001 App 端 EDL 渲染器支持进展

- **问题**：EDL shader 手机端开源方案已调研，App 是否已立项支持尚未确认
- **建议确认人**：App 端负责人
- **优先级**：中

### Q-003 存图触发正式方案确认

- **问题**：`SET_SLAM_MODE` 为临时方案，正式应为 `SLAM_FSM_MOW`；需要确认 controller 初始化时序是否可修改
- **建议确认人**：@王新
- **优先级**：高（临时方案不够健壮）

### Q-004 FAST-LIVO2 硬件加速优先实施方向

- **问题**：D-009 已梳理 11 处候选优化点，但无优先级排序和实施计划；哪些方向优先落地、采用 OpenMP / CUDA / OpenCL 哪条路线尚未明确
- **建议确认人**：刘宏伟（FAST-LIVO2 负责人）
- **优先级**：中（CPU 优化 D-002 已有一轮，硬件加速为下一阶段选项）

### Q-007 机器人未到达区域空洞补充方案

- **问题**：机器只走过的区域才有点云，边角/死区存在空洞；坡道空洞根因已确认（见 D-015），但通用补充方案未定
- **坡道特殊情况**：雷达+相机 FOV 在坡面无重叠，从远处平地视角补采可缓解，但不能彻底解决
- **双目填补提议**（丛一鸣）：被李哲否定，认为技术路线不一致、较费劲
- **参考图**：![空洞示例](images/fastlivo_panorama_spatial_hole_example.jpeg)
- **建议确认人**：李哲（2026-04-14 已接 action）
- **优先级**：高（坡道空洞当前已可复现）

### Q-008 阶段二机器实时位置显示的坐标系同步

- **问题**：导航定位算法坐标系 与 实景地图显示坐标系 是独立两套，阶段二若要显示机器实时位置需要对齐；同步方案未设计
- **建议确认人**：刘宏伟
- **优先级**：低（阶段二，当前不需要）

### Q-009 机器端 RAM 容量是否够用

- **问题**：1600㎡ 场地临时存储约 100M，多个区域叠加时 RAM 占用是否超限未验证
- **建议确认人**：刘宏伟
- **优先级**：中

### Q-010 多次割草点云拼接质量

- **问题**：多次出桩/回桩产生多块点云，各块坐标系是否对齐、拼接后是否有可见重影/分层，尚无实测数据
- **计划**：李哲 2026-04-14 决定先采实验数据（60/75/105 场地多次清扫）再评估（见 D-014）
- **建议确认人**：刘宏伟（采数据）+ 李哲（评估结果）
- **优先级**：高（当前最重要的未知项）

### Q-011 导航百分百覆盖率接口

- **问题**：D-011 方案中以"区域覆盖100%"为地图更新终止条件，需要导航模块提供对应接口；接口是否存在、格式未确认
- **背景**：丛一鸣提出，导航知道区域是否百分百覆盖，需要对接
- **建议确认人**：导航团队
- **优先级**：高（影响地图更新策略实现）

### Q-012 ISP 参数对彩色效果的影响边界

- **问题**：若后期想调整点云彩色效果，可能涉及相机 ISP 参数调整；ISP 会影响其他感知识别模块，不能随意修改
- **背景**：李哲 2026-04-14 提出风险，当前彩色效果（路面/草地）丛一鸣认为 ok
- **建议确认人**：感知团队（ISP 影响范围评估）
- **优先级**：低（当前彩色效果可接受，暂不需要改）

---

## 参考文档（C 类，按需查阅）

无 C 类文档（Fast-LIVO2 相关文档均已提取为 A/B 类）