# 设计文档：原始材料梳理流程固化（Skill + 项目约定）

**日期**：2026-04-12
**状态**：已批准，待实施

---

## 背景与目标

通过梳理激光 SLAM（mSLAM/sensors）和标定（calibration）两个模块的原始材料，已逐步形成一套可复用的工作方法。

**核心价值双轨**：
1. **接手知识沉淀**：刚接手新团队时，快速建立全局认知——知道做了什么、结论是什么、项目需要做哪些类型的工作
2. **方法复用**：每次处理新模块的 inbox 时，不从头设计流程，直接调用标准流程

**交付物**：
- `~/.cursor/skills/raw-materials-curation/SKILL.md`（通用 Cursor Skill）
- `docs/process/raw-materials-conventions.md`（定位组专属约定）

---

## 一、Cursor Skill 设计

**路径**：`~/.cursor/skills/raw-materials-curation/SKILL.md`

**触发词**：「梳理原始材料」/「整理 inbox」/「接手新模块」/「onboard new module」/「处理新材料」/「补充梳理」/「增量更新」

**首先确认模式**：
- 用户说「梳理 XXX」/「接手 XXX」→ **全量模式**（首次处理）
- 用户说「我新加了几个文档」/「补充梳理 XXX」/「增量更新」→ **增量模式**（已有梳理文档），询问用户具体哪些文件是新增的

### Skill frontmatter

```yaml
---
name: raw-materials-curation
description: >
  从技术项目的原始材料库（inbox）中提取结构化知识，生成 timeline/decisions/problems/gaps 四类文档。
  适用于接手新团队/模块时建立全局认知，或对已有 inbox 进行系统性梳理。
  触发词：「梳理原始材料」「整理 inbox」「接手新模块」「onboard new module」「处理新材料」
---
```

### Skill 内容结构（五个阶段）

**阶段零：读取项目约定**
- 检查项目根目录下是否有 `docs/process/raw-materials-conventions.md`
- 若有，读取并用于后续阶段的格式和分类判断
- 若无，使用 Skill 内置的默认规则

**阶段一：扫描 + 分层（必须与用户确认后才进入阶段二）**

先确认本次梳理的模式：
- **全量模式**（首次梳理）：处理 inbox 下全部文件
- **增量模式**（已有梳理文档，新增了部分材料）：用户指定本次新增的文件/目录范围，只对这部分扫描，提取结果合并进现有的 timeline/decisions/problems/gaps，避免重复条目

无论哪种模式：
- 列出本次处理范围内所有文件（含 .md、.xlsx、图片等）
- 按三层分类：
  - **A 类**：含明确结论、设计方案、选型决策、算法架构的文档 → decisions.md + timeline.md
  - **B 类**：工程推进过程记录（测试结论、bug 修复、问题排查） → timeline.md + problems.md
  - **C 类**：批量测试数据、操作手册、测试截图 → gaps.md 的 R-xxx 标注（已知可参考）
- **【必须】** 将分层结果和每份文档的内容摘要呈现给用户，等待确认后才进入阶段二
  - 呈现格式参考：[线索梳理] → 用户说 OK → 进入提取
  - 不允许跳过此步骤直接提取，防止分类误判导致重要信息被错误归档

**阶段二：内容提取**

> 增量模式下：提取前先比对现有文档，跳过已有条目，新条目追加到现有文件末尾（D/P 编号接续现有最大编号）

按输出文件分别提取：

- `timeline.md`：项目推进时间节点、算法版本迭代、关键里程碑、功能上线时间、bug 修复合入时间
- `decisions.md`：设计选型（为什么选这个方案）、算法版本对比与选定结论、接口设计决策、传感器参数对比结论；格式 D-xxx（标题/背景/选定方案/理由/来源）
- `problems.md`：已知问题根因 + 修复过程 + 当前状态；格式 P-xxx（症状/根因/修复/来源）
- `gaps.md`：
  - G-xxx：有飞书/外部链接但无本地对应文件
  - Q-xxx：文档中出现但未有明确结论的 open 问题（待向负责人确认）
  - R-xxx：C 类文档，已知存在，按需查阅

**阶段三：图片处理**

判断标准：
- **链接保留**：设计/方案示意图、算法流程图、传感器参数对比图、标定场地/治具设计图、场景规模确认图——一切能帮助理解技术方案的图
- **skip**：批量测试截图、数据表格截图、日志截图

操作：将保留的图片复制到 `modules/<mod>/images/`，用语义化名称命名，在对应的 decisions/problems/timeline 条目中添加 `![描述](images/文件名)` 引用

**阶段四：覆盖率核查**（梳理完成后必做）

1. **Gap 误判核查**：逐条确认 G-xxx 条目——本地目录里是否实际已有对应文件？若有则移除该 gap 并将内容提取到正确文档
2. **文档覆盖率核查**：对照阶段一的文件清单，检查每个 A/B 类文档是否都有至少一条对应的 timeline/decisions/problems 提取记录
3. **图片遗漏核查**：重新扫描 A/B 类文档中的图片，确认关键设计图没有被遗漏

---

## 二、项目约定文档设计

**路径**：`docs/process/raw-materials-conventions.md`

### 内容结构

**1. 目录结构约定**
```
teams/<group>/inbox/           ← 原始材料（按来源编号组织）
teams/<group>/modules/<mod>/   ← 结构化输出
  timeline.md
  decisions.md
  problems.md
  gaps.md
  images/
```

**2. 三层分类标准（定位组版）**

| 层级 | 定义 | 处理方式 |
|------|------|---------|
| A 类 | 含明确设计结论、方案选型、算法架构、传感器对比结论的文档 | 提取进 decisions.md + timeline.md，关键图片链接 |
| B 类 | 工程推进过程记录（测试结论、bug 修复记录、问题排查过程、验证结果） | 提取进 timeline.md + problems.md |
| C 类 | 批量测试数据表格、操作手册步骤、测试截图日志、交叉编译记录 | gaps.md R-xxx 标注，不提取内容 |

**3. 条目格式规范**

时间线条目：`| 日期 | 事件标题 | 背景/结论摘要 | 来源文档 |`

决策条目（D-xxx）：
```
## D-xxx 标题【状态：已定案/待确认】
**背景** ...
**选定方案** ...
**理由** ...
**来源** | 文档路径
```

问题条目（P-xxx）：
```
## P-xxx 问题标题
- **症状**：...
- **根因**：...
- **修复**：...（或"进行中"/"待修复"）
- **来源**：文档路径
```

Gap 条目：
- `G-xxx`：缺失的外部文档（附飞书链接和首次提及来源）
- `Q-xxx`：待确认的 open 问题（附负责人和优先级）
- `R-xxx`：C 类文档标注（已知可参考，不需提取）

**4. 图片命名规范**

格式：`<module>_<描述>.<ext>`

示例：
- `calib_aftersale_station.jpeg`
- `mslam_loop_online_phase1.png`
- `sensor_mid360_slam_70m.png`

**5. 历史已处理模块记录**

| 日期 | 模块 | inbox 来源 | 状态 |
|------|------|-----------|------|
| 2026-04-12 | laser/modules/sensors/ | 003_多线激光/007_外部设备 | ✓ 完成 |
| 2026-04-12 | laser/modules/mslam/ | 003_多线激光/006_算法文档 等 | ✓ 完成 |
| 2026-04-12 | calibration/modules/calibration/ | vision/inbox/003_标定相关 | ✓ 完成 |
| 2026-04-12 | calibration/modules/calibration/ | calibration/inbox/006_参数标定 | 进行中 |

---

## 三、实施操作清单

| 步骤 | 操作 |
|------|------|
| 1 | 创建 `~/.cursor/skills/raw-materials-curation/` 目录 |
| 2 | 写入 `SKILL.md`（含 frontmatter + 五阶段流程） |
| 3 | 创建 `docs/process/` 目录 |
| 4 | 写入 `docs/process/raw-materials-conventions.md` |
| 5 | 更新 `README.md` 在「原始资料」或新建「工作流程」节中引用 conventions 文档 |

---

## 验收标准

- [ ] `~/.cursor/skills/raw-materials-curation/SKILL.md` 存在，包含五阶段流程
- [ ] Skill 触发词包含「补充梳理」/「增量更新」，并在 Phase 1 明确说明两种模式
- [ ] Phase 1 注明「必须与用户确认分层结果后才进入 Phase 2」
- [ ] Phase 2 注明增量模式下的编号接续和去重规则
- [ ] `docs/process/raw-materials-conventions.md` 存在，包含五节约定内容
- [ ] Skill frontmatter 格式与现有 skill 一致（有 name/description/触发词）
- [ ] 约定文档中历史处理记录已填写
