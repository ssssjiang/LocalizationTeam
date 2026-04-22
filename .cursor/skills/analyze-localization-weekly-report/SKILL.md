---
name: analyze-localization-weekly-report
description: >-
  分析定位组（视觉 & 标定子组）周报，将周报信息结构化地写入团队文档体系。
  触发场景：用户说「处理周报」「分析 VSLAM 进度同步」「把周报整理进 people/tech/decisions 等文件」
  「提取周报里的里程碑/决策/人员分工」时激活。
---

# 定位组周报分析（视觉 & 标定）

## 目标

将周报（进度同步文档）中的信息，按信息类型分发到 7 个目标文件：

| 目标文件 | 存放内容 |
|---------|---------|
| `people.md` | 工作模块 × 负责人（人视角：Section 一总览 + Section 三个人备忘） |
| `tech.md` | 技术方案框架、指标、瓶颈、优化方向 × 负责人 |
| `decisions.md` | 已定案的设计结论（架构选型、行为策略、量化结论） |
| `problems.md` | 已知问题根因与修复状态 |
| `timeline.md` | 完成事件里程碑（合入/发版/测试通过） |
| `gaps.md` | 飞书链接（无本地文件）→ G-xxx |

---

## 周报结构特征

视觉 & 标定组周报（如 `VSLAM 进度同步 -2026.md`）固定格式：

```
# YYYYMMDD                    ← 日期锚点（最新周在前）
* **工作模块名称**              ← 工作 track（信噪分离的关键）
  > 本周进展                  ← 【信号区】已发生的事实
    * 具体内容 @person
  * Action                   ← 【噪声区】下周待做（不提取）
  * 其他待办                  ← 【噪声区】长期 TODO（不提取）
```

**已知工作 Track 及路由**

| 工作 Track | 路由到哪个模块 |
|-----------|-------------|
| 割草机内外参标定与检测 | `calibration/modules/calibration/` |
| OKVIS-VIO 优化 | `vision/modules/vslam/` |
| 深度学习特征点描述子引入 | `vision/modules/vslam/` |
| Okvis 全局图与回环检测 | `vision/modules/vslam/` |

---

## 人 × 信息 关系规则

### 规则 1：@person + Done/已合入 → 里程碑归属（弱绑定）

```
> * Flora 适配完成，测试通过 @白世杰   → timeline.md 事件
```
`@person` 写入 timeline 的「负责人」列，但不强制；重点是事件本身。

### 规则 2：@person + 进行中工作项（非 Done）→ 当前分工（强绑定）

```
* Maplab 重定位精度测试 @宋姝  (无 Done/已合入)
```
→ 写入 `people.md` Section 三该人的「**当前负责工作**」字段。

若同一 Track 的工作项只有一个人，该人即为 **模块负责人**，写入 `people.md` Section 一总览表的「负责工作模块」列。

### 规则 3：同一工作项跨多周重复出现 → 只看最新一周（不重复提取）

Action 列表在多周反复出现直到完成。扫描时：
- 只提取「本周进展」块中的内容
- 忽略「Action」「其他待办」块
- 跨周相同事件：以最新日期为准，合并为一条

### 规则 4：技术结论密度低，重点识别「明确结论」标志词

| 标志词 | 对应目标文件 |
|--------|-----------|
| Done / 已合入 / 已发版 / 测试通过 / 验证完成 | `timeline.md` |
| 根因是 / 发现 / 结论: / 量化结论 | `decisions.md` 或 `problems.md` |
| 不如 / 优于 / 比较 / 选定 / 选型 | `decisions.md` |
| 失败 / 问题 / OOM / 偏差 / 召回率低 | `problems.md` |
| 飞书链接（无本地文件） | `gaps.md` G-xxx |

---

## 执行步骤

### 步骤 0：读取现有文档，确认编号上限

```python
# 检查各模块当前最大 D/P/G/timeline 编号
grep "^## D-" decisions.md | tail -3
grep "^## P-" problems.md | tail -3
grep "^| G-" gaps.md | tail -3
tail -3 timeline.md
```

### 步骤 1：扫描周报，分类结果（⚠️ 必须与用户确认）

1. 统计周报的**日期跨度**和**工作 Track 列表**
2. 逐 Track 扫描「本周进展」块，跳过「Action / 其他待办」
3. 统计飞书链接数量，和现有 gaps.md 做去重
4. 给出分类摘要（每条：Track、内容摘要、目标文件、@person）

**等用户确认后才进入步骤 2。**

### 步骤 2：写入各目标文件

按以下优先级写入：

**people.md**（先写，人员信息最稳定）
- Section 一 总览表：补充姓名 + 负责工作模块列
- Section 二 单点风险：Track 只有一人负责时记录
- Section 三 个人备忘：每人加「**当前负责工作**」字段（第一行）
- `能力特点 / 状态 / 1:1 内容` 不从周报提取，保留 `【待填充】`

**tech.md**
- Section 四 优化方向：已在周报出现的方向 + 负责人列
- Section 三 当前瓶颈：「失败/低/差」类结论
- Section 六 风险判断：`> 【判断】` 块留空，由用户手动填写

**decisions.md / problems.md**（有明确结论才写）
- decisions：选型结论、策略定案、量化发现
- problems：有症状 + 根因的已知问题

**timeline.md**
- 只写「Done / 合入 / 发版 / 通过」类完成事件
- 格式：`| YYYY-MM-DD | 事件标题 | 背景摘要 | 来源 |`

**gaps.md**
- 所有飞书链接（去重后）按方向分组追加 G-xxx
- 用 Python 写入防止 `!` 被 bash history expansion 吃掉

### 步骤 3：去重验证

```python
# 检查新写入的 timeline 事件是否与现有 change log 类文件重叠
# 检查 decisions 新条目是否和现有 D-xxx 重复
grep "关键词" decisions.md problems.md timeline.md
```

---

## 噪声过滤规则

跳过以下内容（不提取）：

| 内容类型 | 原因 |
|---------|------|
| `Action` / `其他待办` 块 | 瞬态，下周再出现直到完成 |
| 空白进展（`> *` 无内容）| 无实质信息 |
| 同一内容跨多周重复出现 | 只取最新 |
| 大量 SLAM 轨迹效果图 / 批量测试截图 | 不链接到结构化文档 |
| 跨团队依赖讨论（@感知 @导航）| 仅记录结论，不记录讨论过程 |

---

## 飞书链接处理规则

1. 用 Python 提取所有 `[title](https://roborock.feishu...)` 链接并去重
2. 对比现有 gaps.md 中已有 URL，只处理新增链接
3. 按工作方向分组（通道建图 / 重定位 / 精度分析 / 项目系统 / …）
4. 标定 Track 的链接 → `calibration/gaps.md`；其余 → `vslam/gaps.md`

**写入脚本模板**（防 `!` 被 bash 扩展）：

```python
with open(gaps_path, 'a') as f:
    f.write(new_content)
    f.flush()
    import os; os.fsync(f.fileno())
```

---

## 已知边界情况

**人员信息的局限性**：周报只能填充「负责工作模块」和「当前状态」的工作维度；能力特点、真实困难、1:1 备忘无法从周报推断，需要保留 `【待填充】`。

**跨模块链接**：某些飞书链接（如`产线MCT整机外参标定数据统计`）出现在 VSLAM Track 但属于标定内容，按**内容主题**而非**出现位置**路由。

**多人协作项目**：Tech.md 优化方向的负责人列可填多人（空格分隔），不强求单点。

**周报时间倒序**：最新周在文件最前，扫描时注意最新状态优先于历史状态。

---

## 快速参考：内容分发矩阵

```
本周进展 > Done/合入/发版     → timeline.md
本周进展 > 根因/结论/选型     → decisions.md 或 problems.md
本周进展 > @person + 进行中  → people.md（负责工作字段）
本周进展 > 飞书链接           → gaps.md（G-xxx）
进行中方向 × 负责人           → tech.md Section 四
失败/低/差的量化结论          → tech.md Section 三 + problems.md
```
