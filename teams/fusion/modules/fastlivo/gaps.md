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

- **链接**：https://github.com/hku-mars/FAST-Calib
- **首次提及**：`inbox/0412新增/扫描式多线lidar与camera标定调研总结`（D-008 推荐参考实现）

### G-005 velo2cam_calibration（对比参考实现）

- **链接**：https://github.com/beltransen/velo2cam_calibration
- **首次提及**：`inbox/0412新增/扫描式多线lidar与camera标定调研总结`（2021年，FAST-Calib 对比基准）

---

## Open 问题（结论待确认）

### Q-001 App 端 EDL 渲染器支持进展

- **问题**：EDL shader 手机端开源方案已调研，App 是否已立项支持尚未确认
- **建议确认人**：App 端负责人
- **优先级**：中

### Q-002 地图传输功能方案

- **问题**：全景地图 pcd 约 452MB，传输方案（增量/压缩/分块）未设计
- **建议确认人**：云端/通信模块负责人
- **优先级**：中（当前内存已是瓶颈）

### Q-003 存图触发正式方案确认

- **问题**：`SET_SLAM_MODE` 为临时方案，正式应为 `SLAM_FSM_MOW`；需要确认 controller 初始化时序是否可修改
- **建议确认人**：@王新
- **优先级**：高（临时方案不够健壮）

### Q-004 FAST-LIVO2 硬件加速优先实施方向

- **问题**：D-009 已梳理 11 处候选优化点，但无优先级排序和实施计划；哪些方向优先落地、采用 OpenMP / CUDA / OpenCL 哪条路线尚未明确
- **建议确认人**：刘宏伟（FAST-LIVO2 负责人）
- **优先级**：中（CPU 优化 D-002 已有一轮，硬件加速为下一阶段选项）

---

## 参考文档（C 类，按需查阅）

无 C 类文档（Fast-LIVO2 相关文档均已提取为 A/B 类）