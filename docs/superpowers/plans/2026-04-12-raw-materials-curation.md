# 原始材料梳理流程固化 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 `raw-materials-curation` Cursor Skill 和定位组项目约定文档，将已沉淀的原始材料梳理方法论固化为可复用工具。

**Architecture:** 两个独立文件（Skill + 项目约定），通过「阶段零：读取项目约定」桥接。实施顺序：先写两个主文件，最后更新 README。

**Tech Stack:** Markdown 文件写入

---

### Task 1：创建 Cursor Skill 目录并写入 SKILL.md

**Files:**

- Create: `~/.cursor/skills/raw-materials-curation/SKILL.md`
- **Step 1: 创建目录**

```bash
mkdir -p ~/.cursor/skills/raw-materials-curation
```

- **Step 2: 写入 SKILL.md**

完整内容如下（精确写入，不修改任何文字）：

```markdown
---
name: raw-materials-curation
description: >
  从技术项目的原始材料库（inbox）中提取结构化知识，生成 timeline/decisions/problems/gaps 四类文档。
  适用于接手新团队/模块时建立全局认知，或对已有 inbox 进行系统性梳理。
  触发词：「梳理原始材料」「整理 inbox」「接手新模块」「onboard new module」「处理新材料」「补充梳理」「增量更新」
---

# Raw Materials Curation（原始材料结构化梳理）

## 何时激活

- 用户说「梳理原始材料」「整理 inbox」「接手新模块」「处理新材料」→ **全量模式**
- 用户说「补充梳理」「增量更新」「我新加了几个文档」→ **增量模式**
- 用户接手新团队/模块，需要快速建立全局认知时

## 何时不激活

- 只需查询某个具体技术问题（直接回答即可）
- 只更新单个文档的某一条目（不需要走完整 pipeline）

---

## 梳理目的（Why）

本流程服务于两个核心目标：

1. **接手知识沉淀**：刚接手新团队/模块时，从原始材料中快速提炼全局认知——做了哪些工作、形成了哪些关键结论、哪些决策已经分析和确定
2. **方法复用**：将「项目需要做哪些类型工作」沉淀为结构化参考，不在每次梳理时从头设计

---

## 阶段零：读取项目约定

1. 检查项目根目录下是否有 `docs/process/raw-materials-conventions.md`
2. 若有，读取全文，用于后续阶段的目录结构、分类标准、条目格式判断
3. 若无，使用本 Skill 内置的默认规则（见各阶段说明）

---

## 阶段一：扫描 + 分层（⚠️ 必须与用户确认后才进入阶段二）

**首先确认模式：**
- **全量模式**（首次梳理）：处理指定 inbox 目录下全部文件
- **增量模式**（已有梳理文档，新增了部分材料）：询问用户具体哪些文件/目录是新增的，只对这部分扫描；提取结果合并进现有的 timeline/decisions/problems/gaps，避免重复条目

**扫描步骤：**
1. 列出本次处理范围内所有文件（.md / .xlsx / 图片 / 其他）
2. 对每个文档读取前 40 行，判断内容性质
3. 按三层分类：
   - **A 类**：含明确结论、设计方案、选型决策、算法架构的文档 → 主要进 decisions.md + timeline.md
   - **B 类**：工程推进过程记录（测试结论、bug 修复、问题排查） → 主要进 timeline.md + problems.md
   - **C 类**：批量测试数据表格、操作手册、测试截图日志 → gaps.md 的 R-xxx 标注

**【必须】** 将分层结果整理为「线索摘要」呈现给用户：
- 每个文档列出分类（A/B/C）+ 一句话说明内容
- 标注哪些文档将提取进哪些输出文件
- 等待用户确认（「OK」或调整）后，才进入阶段二
- 禁止跳过此步骤直接提取，防止分类误判导致重要信息被错误归档

---

## 阶段二：内容提取

> **增量模式补充规则：** 提取前先读取现有文档，跳过已有条目；新条目追加到文件末尾，D/P/G/Q/R 编号接续现有最大编号

### timeline.md

提取：项目推进时间节点、算法版本迭代、关键里程碑、功能上线时间、bug 修复合入时间

格式：
```

| 日期 | 事件标题 | 背景/结论摘要 | 来源文档 |

```

日期不确定时写「待确认」，不留空。

### decisions.md

提取：设计选型（为什么选这个方案）、算法对比与选定结论、接口设计、传感器参数对比结论

格式：
```markdown
## D-xxx 标题【已定案 / 待确认】

**背景**
...

**选定方案**
...

**理由**
...

**来源** | inbox 文档路径
```

### problems.md

提取：已知问题根因 + 修复过程 + 当前状态

格式：

```markdown
## P-xxx 问题标题

- **症状**：...
- **根因**：...
- **修复**：...（或「进行中」/「待修复」）
- **来源**：inbox 文档路径
```

### gaps.md

三类条目：

- `G-xxx`：有飞书/外部链接但无本地对应文件（附链接和首次提及来源）
- `Q-xxx`：文档中出现但无明确结论的 open 问题（附建议确认人和优先级）
- `R-xxx`：C 类文档，已知存在，按需查阅（不提取内容）

---

## 阶段三：图片处理

**保留并链接（复制到 `modules/<mod>/images/`）：**

- 设计/方案示意图、算法流程图
- 传感器参数对比图
- 标定场地/治具设计图
- 场景规模确认图
- 一切能帮助理解技术方案而非记录测试过程的图

**跳过（skip）：**

- 批量测试截图、数据表格截图、日志截图、SLAM 轨迹效果图（大量）

**操作：**

1. 将保留图片复制到 `modules/<mod>/images/`
2. 命名规范：`<module>_<描述>.<ext>`（如 `calib_aftersale_station.jpeg`）
3. 在对应的 decisions/problems/timeline 条目中添加 `![描述](images/文件名)` 引用

---

## 阶段四：覆盖率核查（梳理完成后必做）

1. **Gap 误判核查**：逐条检查 G-xxx 条目，确认本地是否实际存在对应文件；若有则移除该 gap 并将内容提取到正确文档
2. **文档覆盖率核查**：对照阶段一的文件清单，确认每个 A/B 类文档都有至少一条对应的 timeline/decisions/problems 提取记录
3. **图片遗漏核查**：重新扫描 A/B 类文档中的所有图片，确认关键设计图没有遗漏

核查完成后，向用户汇报：

- 发现并修正的误判 gap 数量
- 覆盖率（已处理 A/B 类文档数 / 总 A/B 类文档数）
- 补充链接的图片数量

```

- [ ] **Step 3: 验证**

```bash
head -5 ~/.cursor/skills/raw-materials-curation/SKILL.md
grep -c "阶段" ~/.cursor/skills/raw-materials-curation/SKILL.md
```

Expected: 第一行为 `---`；grep 输出 `5`（五个阶段）

---

### Task 2：创建项目约定文档

**Files:**

- Create: `/Users/songshu/Projects/LocalizationTeam/docs/process/raw-materials-conventions.md`
- **Step 1: 创建目录**

```bash
mkdir -p /Users/songshu/Projects/LocalizationTeam/docs/process
```

- **Step 2: 写入约定文档**

完整内容如下：

```markdown
# 定位组原始材料梳理约定

> 供 `raw-materials-curation` Skill 在定位组项目中使用。
> Skill 路径：`~/.cursor/skills/raw-materials-curation/SKILL.md`

---

## 1. 目录结构约定

```

teams//inbox/           ← 原始材料（按来源编号组织）
teams//modules//   ← 结构化输出
  timeline.md
  decisions.md
  problems.md
  gaps.md
  images/

```

当前各组：
- `teams/laser/`：多线激光组
- `teams/fusion/`：融合定位组
- `teams/vision/`：视觉定位组（VSLAM）
- `teams/calibration/`：参数标定组

---

## 2. 三层分类标准

| 层级 | 定义 | 处理方式 |
|------|------|---------|
| **A 类** | 含明确设计结论、方案选型、算法架构、传感器对比结论的文档 | 提取进 decisions.md + timeline.md；关键图片命名链接 |
| **B 类** | 工程推进过程记录：测试结论、bug 修复记录、问题排查、验证结果 | 提取进 timeline.md + problems.md |
| **C 类** | 批量测试数据表格、操作手册步骤、测试截图日志、交叉编译记录 | gaps.md R-xxx 标注，不提取内容 |

分类不确定时，优先看文档是否有「结论」或「决策」性质的总结句；有则 A/B，无则 C。

---

## 3. 条目格式规范

### timeline.md

```

| 日期 | 事件标题 | 背景/结论摘要 | 来源文档 |

```

- 日期不确定写「待确认」
- 按时间升序排列
- 同一批 bug 修复可合并为一条，标注版本号或 commit 范围

### decisions.md

```markdown
## D-xxx 标题【已定案 / 待确认】

**背景**
...

**选定方案**
...

**理由**
...

**来源** | inbox/文档路径
```

- 编号全模块唯一，不同 inbox 批次追加时接续
- 「待确认」状态需在 gaps.md 新增对应 Q-xxx 条目

### problems.md

```markdown
## P-xxx 问题标题

- **症状**：...
- **根因**：...
- **修复**：...（「已修复（日期）」/「进行中」/「待修复」）
- **来源**：inbox/文档路径
```

### gaps.md


| 类型    | 格式                  | 含义            |
| ----- | ------------------- | ------------- |
| G-xxx | 文档名 + 飞书链接 + 首次提及来源 | 外部链接存在但无本地文件  |
| Q-xxx | 问题描述 + 建议确认人 + 优先级  | Open 问题，结论待确认 |
| R-xxx | 文档名 + 所在路径 + 一句话说明  | C 类文档，已知可查    |


---

## 4. 图片命名规范

格式：`<module>_<描述>.<ext>`

- `<module>`：当前处理的模块简写（calib / mslam / sensor / fusion 等）
- `<描述>`：英文或拼音，下划线分隔，说明图片主题

示例：

- `calib_aftersale_station.jpeg`（售后标定场地图）
- `mslam_loop_online_phase1.png`（在线回环优化阶段流程图）
- `sensor_mid360_slam_70m.png`（mid360 70m SLAM 效果图）

---

## 5. 历史已处理模块记录

> 每次完成梳理后追加一行


| 日期         | 模块路径                             | inbox 来源                                       | 状态   |
| ---------- | -------------------------------- | ---------------------------------------------- | ---- |
| 2026-04-12 | laser/modules/sensors/           | 003_多线激光/007_外部设备与slam                         | ✓ 完成 |
| 2026-04-12 | laser/modules/mslam/             | 003_多线激光/006_算法文档 等多个目录                        | ✓ 完成 |
| 2026-04-12 | calibration/modules/calibration/ | vision/inbox/003_标定相关（已迁移至 calibration/inbox/） | ✓ 完成 |
| 2026-04-12 | calibration/modules/calibration/ | calibration/inbox/006_参数标定                     | 进行中  |


```

- [ ] **Step 3: 验证**

```bash
head -3 /Users/songshu/Projects/LocalizationTeam/docs/process/raw-materials-conventions.md
grep -c "^##" /Users/songshu/Projects/LocalizationTeam/docs/process/raw-materials-conventions.md
```

Expected: 第一行为 `# 定位组原始材料梳理约定`；grep 输出 `5`（5个二级标题）

---

### Task 3：更新 README.md

**Files:**

- Modify: `/Users/songshu/Projects/LocalizationTeam/README.md`
- **Step 1: 在「快速导航」中新增「工作流程」节**

在 README.md 的「原始资料（inbox）」节之前，插入以下内容：

```markdown
### 工作流程（process/）

| 文件 | 内容 |
| ---- | ---- |
| [docs/process/raw-materials-conventions.md](./docs/process/raw-materials-conventions.md) | 原始材料梳理约定：目录结构、分类标准、条目格式、图片命名规范 |
```

- **Step 2: 验证**

```bash
grep "raw-materials-conventions" /Users/songshu/Projects/LocalizationTeam/README.md
```

Expected: 有输出（链接已存在）

---

## 验收检查

完成所有 Task 后运行：

```bash
# 1. Skill 存在且包含五阶段
grep -c "阶段" ~/.cursor/skills/raw-materials-curation/SKILL.md

# 2. 增量模式和强制确认步骤存在
grep "增量模式\|必须" ~/.cursor/skills/raw-materials-curation/SKILL.md | wc -l

# 3. 约定文档存在且包含五节
grep -c "^## [0-9]" /Users/songshu/Projects/LocalizationTeam/docs/process/raw-materials-conventions.md

# 4. README 已更新
grep "raw-materials-conventions" /Users/songshu/Projects/LocalizationTeam/README.md
```

Expected：

1. `5`
2. `≥ 2`
3. `5`
4. 有输出

