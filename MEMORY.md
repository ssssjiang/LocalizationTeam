# MEMORY.md - 长期记忆

_这是爪爪的长期记忆。只在私聊主会话中加载，不在群聊或共享上下文中读取。_
_内容应保持精简：结论、状态变化、可复用规则、依据。不记录过程。_

---

## 格式约定

每条记忆格式：
```
- [结论/状态/规则]；依据：[来源或日期]
```

按月份分节，新内容追加到最新月份节下。

---

## 收录门槛

仅记录满足以下任一条件的内容：
- 对后续多次协作有帮助
- 代表明确的项目或系统状态变化
- 形成稳定规则、偏好或结论
- 是已验证的问题模式或解决方案
- 是 songshu 明确要求记住的内容

---

## 不写入内容

- 过程性排查细节
- 未验证推断
- 一次性闲聊信息
- 与长期协作无关的临时上下文
- 不应在私聊长期记忆中保留的敏感内容

---

## 变更规则

- 若旧记忆已失效，不保留冲突表述；直接更新为最新状态
- 若同一主题有新进展，优先更新原条目或补充状态，而不是重复新增近义条目
- 若状态尚未确认，可暂不写入，先保留在日记或候选提炼中

---

## 2026-03

### 用户与协作偏好
- songshu 偏好先结论后依据，技术方案结构为：根因判断 → 排查步骤 → 修改建议 → 风险点；依据：USER.md / 2026-03-10
- 沟通风格：中文交流，代码和注释用 English，简洁结构化，不要废话；依据：USER.md
- 技术方案选择默认优先级：可验证性 > 可维护性 > 短期速度；依据：USER.md

### 工具与工作流状态
- OpenClaw workspace 初始化完成（IDENTITY / USER / SOUL / HEARTBEAT / MEMORY）；依据：2026-03-10 配置会话
- Notion MCP 当前未接入；后续接入后，可将结构化输出同步到 Notion；依据：USER.md / 2026-03-10
- `daily_stock_analysis` 和 `paper_insight` 为 songshu 手动触发的本地脚本；爪爪当前职责为读取结果并整理推送，全自动化留待后续开发；依据：2026-03-10 配置会话

### 系统行为边界（已确认）
- 当前运行规则采用：Heartbeat 只读巡检与候选内容生成，不自动执行写入或外发；群聊默认沉默，仅被直接 @ 或明确提问时响应；长期记忆仅在任务阶段性完成或结论稳定后写回；依据：SOUL.md / HEARTBEAT.md / 2026-03-10 配置落地

### 技术问题与解决方案（2026-03-10）
- **股票脚本 Gemini key 污染**：OpenClaw 启动时将 `nano-banana-pro` skill 的 apiKey 注入为全局 `GEMINI_API_KEY` 环境变量，导致股票脚本走直连 Google SDK 而非 AiHubMix fallback。解决：在脚本 `.env` 里加 `GEMINI_API_KEY=`（空值）覆盖。原因分析见 memory/2026-03-10.md；依据：2026-03-10 实际修复
- **ClawHub 限流根本原因与最终解决**：Mihomo 代理的激进 DNS 拦截，api.clawhub.ai 被 fake IP 化（11.18.0.x）。单独加 DIRECT 规则无效。最终解决：Clash Verge GUI → DNS 设置 → fake-ip-filter 加 `*.clawhub.ai`，让该域名走真实 DNS。经验：激进的 DNS fake-ip 拦截需要在 fake-ip-filter 白名单而不是路由规则解决；规则+DNS 配合才稳定；依据：2026-03-10 实际验证
- **Notion skill 自写 vs ClawHub**：ClawHub 限流期间自写 Notion skill，反而更快。特别是 synced_block 处理（Notion 同步块）是现成 skill 可能遗漏的。决策：面对生态限制，小范围自写往往更高效；依据：2026-03-10 部署完成

### PinchTab 浏览器控制服务安装（2026-03-11 20:11）
- **安装完成**：全局安装 pinchtab 0.7.8（12MB Go 二进制），HTTP API 端口 9867；支持有头/无头运行、多实例、token 高效（800 tokens/页面，vs 截图便宜 5-13x）；依据：curl install.sh 安装完成
- **用途**：为 AI agents 提供浏览器自动化控制（导航、快照、点击、输入）；与 OpenClaw 内置 browser 工具相比，更专业更高效；与 Exa search 分工：Exa 做网络搜索，PinchTab 做网页交互；依据：2026-03-11 部署
- **快速启动**：`pinchtab` 启动服务；`curl http://localhost:9867/health` 测试；`pinchtab nav URL` 导航；`pinchtab snap` 快照；依据：TOOLS.md 文档

### VSLAM 项目技术 Leader 角色启动（2026-03-11 18:16）
- **新角色确认**：升任割草机 VSLAM 项目技术 leader，向定位组技术 leader 和 PM 双线汇报；职责范围从原来的建图模块扩展到整个项目（VSLAM + 标定 + 产线 + 售后）；交接周期仅两周（前任即将离职）；依据：vslam-onboarding/ONBOARDING.md / 2026-03-11
- **交接框架已建立**：文件夹结构 vslam-onboarding/（README.md 总览 + ONBOARDING.md 交接计划 + TEAM.md 专家地图 + RISKS.md 风险追踪 + TASKS.md 任务表 + WEEKLY_SNAPSHOT.md 周报摘要 + PROGRESS_HISTORY.md 历史周报）；已集成到 HEARTBEAT 追踪，Day 3/6/8/11/14 检查点；依据：2026-03-11 创建
- **已知关键风险**：交接时间紧（高）、口头承诺遗漏（高）、人员缩减 4-6 人（中）、工程化和产线流程不熟（中）；技术风险：重定位召回率低（<50%）、VIO困难场景精度差、子图优化后精度变差；依据：vslam-onboarding/RISKS.md
- **核心原则**：所有问题只要列出来、梳理关系、找到对应的人和资料，就都会解决；目前的任务是"获取全量清单 → 消化分类 → 结构化确认 → 对外亮相"；依据：vslam-onboarding/ONBOARDING.md

### VSLAM 进度同步文档导入（2026-03-11 20:40）
- **周报存档**：导入 2026 年完整周报（PROGRESS_HISTORY.md，20260112~20260309），包含标定、VIO、全局图、深度学习等模块的所有进展和待办；依据：用户发送 / 2026-03-11
- **关键发现**：当前 26 项任务（P0: 9项，P1: 12项，P2: 5项）；核心风险为重定位召回率低（<50%）、VIO困难场景精度差、子图优化后精度变差；依据：WEEKLY_SNAPSHOT.md 提取
- **关键联系人**：宋姝（全局图建图分支）、测试同学（专用测试支持）、感知组（提点与描述子）、导航组（窄通道消息）；依据：TEAM.md 更新
- **关键文档入口**：CIIQC维护文档、okvis困难场景分析、全局图工作项、Eden VSLAM方案、reloc-self分析等；全部链接在 WEEKLY_SNAPSHOT.md；依据：2026-03-11 整理

---

_Heartbeat 和主会话均可更新此文件，但需遵循上述收录门槛和变更规则。_
