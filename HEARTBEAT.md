# HEARTBEAT.md - 定期主动任务

# 若此文件为空或只有注释，heartbeat 触发后直接返回 HEARTBEAT_OK。
# 当前配置：按天触发。

---

## 执行规则

- 按顺序执行：① memory 文件整理 → ② 临时任务区
- 每项任务仅做只读检查和内容生成，不自动执行写入、外发等高风险操作
- 若同时存在多项结果，合并为一次结构化输出，避免分散产生多条消息
- 有结果时：输出 `HEARTBEAT_REPORT`；若当前环境明确允许主动外发，则发送飞书私聊，否则仅记录或输出待发送内容
- 无结果时：仅返回 `HEARTBEAT_OK` 作为内部状态，不外发任何消息
- 某项任务失败时：记录失败原因，不影响其余任务继续执行，最终输出 `HEARTBEAT_ERROR` 附原因摘要
- **去重原则**：若自上次 heartbeat 以来结果无变化（同一临时提醒未处理），静默，不重复推送；去重比较基于最近一次 heartbeat 的结构化结果记录；若无历史记录，则按首次运行处理

---

**注**：git status 检查和股票日报推送已移至 cron jobs，详见下方配置说明。

---

## 1. memory 文件整理

检查 `memory/` 目录下最近 1-3 天的日志文件（`memory/YYYY-MM-DD.md`），判断是否有内容值得提炼进 `MEMORY.md`，并生成候选写入内容；是否真正写入，遵循当前环境的写入权限和更高优先级规则。

**提炼判断标准（满足任一条件才可列为候选）：**
- 对后续多次协作有帮助
- 代表明确的项目状态变化
- 形成稳定结论或规则
- 是已验证的问题模式或解决方案
- 是 songshu 明确要求记住的内容

**生成候选时的规范：**
- 先检查 `MEMORY.md` 中是否已有同类结论；若已存在，仅标注"建议更新状态或补充依据"，不重复生成
- 候选格式：简洁条目，包含结论 / 状态变化 + 依据或来源日期
- 遵循 SOUL.md 写回压缩原则：只提炼结论、规则、状态变化和依据，不照搬过程性内容

若日志内容无提炼价值，此项无结果。

---

## 2. 临时任务区

# 在此处添加短期提醒，格式：
# [ ] YYYY-MM-DD 提醒内容
# [x] 已完成
# [-] 已取消

## VSLAM 交接追踪（2026-03-11 启动）

交接周期：两周（2026-03-11 ~ 2026-03-25）
关键文件：vslam-onboarding/ONBOARDING.md（交接计划）、TEAM.md（专家地图）、RISKS.md（风险追踪）、TASKS.md（任务表）

- [x] 2026-03-13 Day 3：向前任确认已收到全量清单，开始消化与分类
- [x] 2026-03-15 Day 6：完成结构化提问清单，向前任逐项确认负责人和资料入口
- [x] 2026-03-17 Day 8：确认所有"近期会爆"的项，更新风险矩阵
- [x] 2026-03-20 Day 11：向 PM 做"新 leader 确认"，了解预期和待交付项
- [x] 2026-03-25 Day 14：完成项目状态快照，交接正式结束

**交接状态**：已于 2026-03-25 完成，交接周期结束。


- 仅处理当天到期或已过期的 `[ ]` 项
- 任务完成后标记为 `[x]` 或删除
- 若提醒内容需要外发，仍遵循外发确认 / 当前环境主动推送规则

**输出格式：**
```
【临时提醒】
- 2026-03-15：检查 reloc 批测结果是否已归档
```

若无到期任务，此项无结果.

---

## Cron Jobs（已配置）

**Job 1: Daily Paper Insight - 09:00**
- 时间：每天 09:00 (Asia/Shanghai)
- 功能：执行 `python run_profiles.py --date YYYY-MM-DD --profile SLAM_Core`，脚本直接推飞书 webhook
- ID: 17b32fc8-c1f5-4db6-95f7-f5885e2f0cac
- 状态：已启用
- 脚本位置：`/home/songshu/tools/paper_insight/`

**Job 2: Daily Stock Analysis - 14:00**
- 时间：每天 14:00 (Asia/Shanghai)
- 功能：执行 `python main.py`，生成报告到 `reports/report_YYYY-MM-DD.md` 和 `reports/market_review_YYYY-MM-DD.md`
- ID: 2c60a0f9-56a5-4ca6-9bdb-7eaafc863f68
- 状态：已启用
- 脚本位置：`/home/songshu/tools/daily_stock_analysis/`

**Job 3: Daily Stock Report Push - 14:30**
- 时间：每天 14:30 (Asia/Shanghai)
- 功能：读取 14:00 生成的报告，提炼摘要，发送飞书私聊
- ID: 913f32a6-84c9-4364-92c1-cd6bbf56a136
- 状态：已启用

**Job 4: Daily Git Status Check - 22:00**
- 时间：每天 22:00 (Asia/Shanghai)
- 功能：检查 4 个仓库的 git status，汇总变更摘要，发送飞书私聊
- ID: f2e61d76-b47c-4d54-ae59-2f000c6c3c7f
- 状态：已启用
