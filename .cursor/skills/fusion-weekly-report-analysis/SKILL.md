---
name: fusion-weekly-report-analysis
description: >
  从融合组周报（融合组开发进展）中提取结构化知识，分发到 people.md、tech.md、timeline.md、decisions.md、problems.md、gaps.md。
  适用于新一批周报到来时的增量更新，或首次接手时的全量梳理。
  触发词：「梳理周报」「处理周报」「融合组周报」「开发进展文档」「周报梳理」
---

# 融合组周报分析

## 激活条件

- 用户提及「融合组周报」「梳理周报」「开发进展」文档 → **增量模式**（接续现有文档编号）
- 首次处理某批周报 → 全量提取，同上流程

---

## 一、周报文档结构

**路径格式**：`teams/fusion/inbox/<日期>新增/融合组开发进展（<时间范围>）/<文件名>.md`

**内部结构**（三层）：

```
# **YYYY-MM-DD**          ← 周次标题（逆序排列，最新周在最前）
## `@姓名`                ← 人员 section（每人一个）
  - 工作项 1 (Done)
  - 工作项 2
```

**DONE 标记识别**：`Done` / `DONE` / `已完成` / `已合入` / `合入` / `已pr` / `✅` / `完成\b`

**跳过**：含 `TODO` / `待` / `未完成` / `暂未` / `还没` / `进行中` 的行

---

## 二、人员归属规则

### 融合组成员（有 `## @姓名` section，提取工作内容）

| 姓名   | 角色   | 主要方向                          |
| ---- | ---- | ----------------------------- |
| 林子越  | 负责人  | 团队管理、真值评估、仿真工具、CI              |
| 李岩   | 算法   | ESKF、IMU递推、RTK速度更新、假固定识别       |
| 刘宏伟  | 算法   | 重定位对齐（单/多帧）、Bug分析、FAST-LIVO2   |
| 孙新   | 算法   | Bug分析、VIO对齐RTK、Pose Graph研究    |
| 范超   | 算法   | 系统架构（dispatch/pause/resume）、搬动重定位 |
| 茹毅超  | 算法   | nRTK接入、RTK固件信号质量、slip检测        |

### 跨组协作（仅 @提及，不提取工作内容，不记入融合组文档）

| 姓名  | 所属          |
|-----|-------------|
| 周晓旭 | SPM         |
| 李威  | SPM         |
| 李欢  | 导航组负责人      |
| 乔平平 | 器件组         |
| 陈云舸 | 其他组         |

> **判断方式**：有独立 `## @姓名` section → 融合组成员；仅在其他人工作项中被 @提及 → 跨组协作

---

## 三、信息 → 目标文档映射

| 信息类型 | 目标文档 | 条件 |
|---|---|---|
| DONE 项 + 明确完成/合入时间 | `timeline.md` | 取**最早**出现该 DONE 的周次作为日期 |
| Bug 根因分析 / 问题归档 | `problems.md` | 有症状+根因描述；已修复写修复方式，未修复写「进行中」 |
| 方案选定结论（对比后确定某方案） | `decisions.md` | 有明确「结论：xxx 最优」或「选定方案 xxx」表述 |
| 飞书 wiki 链接（本地无对应文件） | `gaps.md` G-xxx | 先确认本地是否有对应文档，无则记录为 gap |
| 人员首次出现 / 离开 | `people.md` § 四 | 以周报日期作为变动时间参考 |
| 人员持续负责的工作方向 | `people.md` § 一、三 | 按人归纳，更新能力特点和状态备忘 |
| 系统整体方向（tech.md 瓶颈/优化方向） | `tech.md` | 新增/变更明显时更新 |

### fastlivo 子模块

刘宏伟的 FAST-LIVO2 / 三维重建相关工作 → `modules/fastlivo/timeline.md` 和 `modules/fastlivo/decisions.md`，其余融合组成员的工作 → `modules/fusion/`

---

## 四、提取规则细则

**日期去重**：同一 DONE 条目可能在多个周次 carry-over。以最早出现该 DONE 标记的周次日期写入 timeline，不重复记录。

**飞书链接判断**：
1. 在 `teams/fusion/inbox/` 下搜索同名文件
2. 若有本地对应 → 跳过 G-xxx，将来梳理该文档时提取
3. 若无 → 记录为 G-xxx，附链接和首次提及人

**图片处理**：周报内嵌图片（`images/融合组开发进展-图片.png`）**全部跳过**，不复制到 modules/images/

**「初步完成/review中」**：不算 DONE，需要下一周出现明确 Done 标记

**人员变动识别**：
- 某人在周报中首次出现 → 判断入组时间（以首次出现周次为参考）
- 某人连续多周消失 → 可能离组，标 `[待确认]`

---

## 五、提取流程

```
1. 读取周报文件，确认覆盖时间范围
2. 读取各目标文档当前最大编号（D-xxx / P-xxx / G-xxx / Q-xxx）
3. Python 提取（见下）→ 生成分类条目草稿
4. 向用户展示「线索摘要」（分 fusion / fastlivo / people / gaps 四组），等待确认
5. 用户确认后写入各目标文档，接续现有编号
6. 检查新出现飞书链接是否有本地对应文件
```

---

## 六、Python 提取脚本

```python
import re

def extract_weekly(fpath, fusion_members=None):
    """
    从单个周报文件提取各人员 DONE 条目，返回 list of (date, person, content)
    """
    if fusion_members is None:
        fusion_members = {"林子越", "李岩", "刘宏伟", "孙新", "范超", "茹毅超"}

    DONE_PAT = re.compile(
        r'Done|DONE|已完成|已合入|合入|已pr|✅|完成\b', re.IGNORECASE)
    SKIP_PAT = re.compile(r'TODO|待|未完成|暂未|还没|进行中')

    with open(fpath) as f:
        content = f.read()

    results = []
    week_blocks = re.split(r'^# \*\*(\d{4}-\d{2}-\d{2})\*\*',
                           content, flags=re.MULTILINE)

    i = 1
    while i < len(week_blocks) - 1:
        week_date = week_blocks[i]
        week_content = week_blocks[i + 1]
        i += 2

        person_blocks = re.split(
            r'^## `@([^`]+)`', week_content, flags=re.MULTILINE)

        j = 1
        while j < len(person_blocks) - 1:
            person = person_blocks[j].strip()
            body = person_blocks[j + 1]
            j += 2

            if person not in fusion_members:
                continue

            for line in body.split('\n'):
                s = line.strip()
                if not s or s.startswith('#'):
                    continue
                if DONE_PAT.search(s) and not SKIP_PAT.search(s):
                    clean = re.sub(r'<[^>]+>', '', s)
                    clean = re.sub(r'\s+', ' ', clean).strip()
                    if len(clean) > 10:
                        results.append((week_date, person, clean[:160]))

    return sorted(results, key=lambda x: x[0])
```

用法：

```python
items = extract_weekly("teams/fusion/inbox/0412新增/融合组开发进展（2026-02-26~）/融合组开发进展（2026-02-26~）.md")
for date, person, content in items:
    print(f"[{date}] @{person}: {content}")
```

---

## 七、输出写入约定

- timeline 条目格式：`| YYYY-MM-DD | 事件标题 | 背景/结论摘要 | 周报 YYYY-MM-DD @姓名 |`
- problems 条目：P-xxx，来源字段写 `周报 YYYY-MM-DD @姓名`
- decisions 条目：D-xxx（fusion）或 D-xxx（fastlivo），来源同上
- gaps G-xxx：附飞书链接 + 首次提及人
- people.md 人员变动：日期写 `~YYYY-MM`（月粒度估计），来源写「周报首次出现」

---

## 参考

- 人员详情：`teams/fusion/people.md`
- 模块文档：`teams/fusion/modules/fusion/` 和 `teams/fusion/modules/fastlivo/`
- 梳理约定：`docs/process/raw-materials-conventions.md`
