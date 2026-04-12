# 通用（全组共用）— Gaps

> 模块：`overview/modules/common/`
> 来源 inbox：`inbox/`（全组通用文档）

---

## 外部链接（本地无对应内容）

### G-001 深蓝学院学习资料
- **链接**：https://roborock.feishu.cn/drive/folder/CiyDf9iOklMmevduM2vcePMtn5e
- **首次提及**：009_技术文档/001_深蓝学院学习资料

### G-002 slamworks 编译流程（飞书 wiki）
- **链接**：https://roborock.feishu.cn/wiki/QGYCwrSA4iZdslkKBsTcQAi6nxc
- **首次提及**：007_通用文档/001_工具文档/001_上层软件包编译与割草机上机流程 / 003_操作文档/001_割草机仿真和上机流程

### G-003 割草机 SLAM 代码、工具权限整理（飞书 wiki）
- **链接**：https://roborock.feishu.cn/wiki/DKZbwZEECiUefykVn4Qcwgxknkc
- **首次提及**：007_通用文档/001_工具文档/001_上层软件包编译与割草机上机流程

### G-004 重装 Ubuntu 后的装机 List（飞书 wiki）
- **链接**：https://roborock.feishu.cn/wiki/JcQfwDRFei3668kWMuMc8u8HnJd
- **首次提及**：007_通用文档/001_工具文档/001_上层软件包编译与割草机上机流程

### G-005 Ubuntu 更换本地软件源 APT 文档（飞书 docx）
- **链接**：https://roborock.feishu.cn/docx/WuEUdTQQSoiN5Mx9lRGcMt8rnlb
- **首次提及**：007_通用文档/001_工具文档/001_上层软件包编译与割草机上机流程

### G-006 rrprofiler 使用说明（飞书 wiki）
- **链接**：https://roborock.feishu.cn/wiki/ZELbwsEwIiAFTlkhKV7cyvNznxh
- **首次提及**：008_分享工具/004_内存占用分析

### G-007 视觉实验室装修申请（飞书 wiki）
- **链接**：https://roborock.feishu.cn/wiki/BBl0wSPKQiYWGDk1au4cml7Fnld
- **首次提及**：007_通用文档/005_实验室管理文档/001_视觉实验室需求

### G-008 Versa 割草机 core dump 问题定位与查询（飞书 wiki）
- **链接**：https://roborock.feishu.cn/wiki/EExSwWXwniLnQOkWuEMcgb3kn1d
- **首次提及**：007_通用文档/003_操作文档/003_多线slam上机：环境配置、出包、刷机流程v2.0

---

## Open 问题（结论待确认）

### Q-001 视觉实验室动捕系统预算
- **问题**：视觉实验室需求文档 TODO 提到"看有没有预算做动捕系统"，当前状态未明确
- **建议确认人**：组长 / 项目经理
- **优先级**：低（不影响当前开发）

---

## 参考文档（C 类，按需查阅）

### R-001 割草机 SLAM 代码、工具权限整理
- **路径**：inbox/002_新员工开发文档/001_割草机SLAM代码、工具权限整理
- **说明**：内网/外网代码库地址、share 目录路径（构建输出/日志/工具）、自动化工具链接

### R-002 VSCode 配置（clangd 安装）
- **路径**：inbox/002_新员工开发文档/002_VSCode配置
- **说明**：clangd ≥16 安装（需手动编译 llvm）、扩展离线安装、内网传输方式

### R-003 上层软件包编译与割草机上机流程
- **路径**：inbox/007_通用文档/001_工具文档/001_上层软件包编译与割草机上机流程
- **说明**：内网机准备 → 权限申请 → slamworks 编译 → 上机部署完整流程

### R-004 Debug 工具记录（ASAN/UBSAN 配置）
- **路径**：inbox/007_通用文档/001_工具文档/002_Debug 工具记录
- **说明**：CMakeLists 中 ASAN 编译宏配置；常用检查项（address/undefined/float）说明

### R-005 上机常用指令脚本（rrtools.sh）
- **路径**：inbox/007_通用文档/001_工具文档/003_上机常用指令脚本
- **说明**：Windows git bash 配置 rt 别名；deploy_algo/pull_log/rr_flash 等指令说明

### R-006 割草机仿真和上机流程
- **路径**：inbox/007_通用文档/003_操作文档/001_割草机仿真和上机流程
- **说明**：Jenkins 出包 → butchart_convertor/data_toolkit 日志转换 → 仿真运行流程

### R-007 割草机手动启动 rr_loader
- **路径**：inbox/007_通用文档/003_操作文档/002_割草机手动启动rr_loader
- **说明**：三条 rradb 指令：killall WatchDoge → 启动 rrlogd → 启动 rr_loader

### R-008 多线 SLAM 上机：环境配置、出包、刷机流程 v2.0
- **路径**：inbox/007_通用文档/003_操作文档/003_多线slam上机：环境配置、出包、刷机流程v2.0
- **说明**：Versa 项目路径汇总（Jenkins/OS/DEVELOPER/FULLTEST）、刷机指令、日志拉取

### R-009 割草机日志仿真
- **路径**：inbox/007_通用文档/003_操作文档/004_割草机日志仿真
- **说明**：Jenkins 出仿真包 → 权限 → 解压 → 运行；tools 仓库 dataset_check 分支配置

### R-010 视觉实验室装修申请（行政文件）
- **路径**：inbox/007_通用文档/005_实验室管理文档/002_视觉实验室装修申请
- **说明**：装修平面图 + 施工细节（墙面/灯具/遮光帘/网口）

### R-011 实验室机器信息统计
- **路径**：inbox/007_通用文档/005_实验室管理文档/003_实验室机器信息统计
- **说明**：在用机器列表（ButchartPro/Butchart/Versa 等），含 SN/TN/机型阶段/IP

### R-012 实验室报废割草机信息记录（20260211）
- **路径**：inbox/007_通用文档/005_实验室管理文档/004_实验室报废割草机信息记录
- **说明**：20260211 报废 8 台（Monet/Versa/Butchart/ButchartPro），含 SN/TN/报废原因

### R-013 割草机 tunning 验收工具
- **路径**：inbox/008_分享工具/001_割草机tunning验收工具
- **说明**：Docker 镜像 tunning_check 安装；输入 YUV 格式规范（AT_高x宽_时间戳_IR0/IR1_0.yuv）

### R-014 图片上传与下载
- **路径**：inbox/008_分享工具/002_图片下载
- **说明**：固件 v5 支持存图自动上传；App 端关闭方式；存图版本说明

### R-015 内存占用分析工具（jemalloc/rrprofiler）
- **路径**：inbox/008_分享工具/004_内存占用分析
- **说明**：编译宏（RR_SW_DEBUG_MEM_PROFILE/ENABLE_JEMALLOC/DEBUG_LOADER_PROFILE）；子进程独立统计方式
