# 参数标定独立为顶层 Team 目录 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将标定从 `teams/vision/` 中拆分为独立顶层目录 `teams/calibration/`，与 laser/fusion/vision 平级，完成所有文件移动、内容提取和链接更新。

**Architecture:** 纯文件系统迁移任务，无代码变更。按「创建骨架 → 移动 inbox → 移动 modules → 新建 people/tech → 清理 vision → 更新 README」顺序执行，每步独立可验证。

**Tech Stack:** Shell（mv/mkdir）、Markdown 文本编辑

---

### Task 1：创建 calibration 目录骨架

**Files:**
- Create: `teams/calibration/`
- Create: `teams/calibration/inbox/`
- Create: `teams/calibration/modules/`

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p /Users/songshu/Projects/LocalizationTeam/teams/calibration/inbox
mkdir -p /Users/songshu/Projects/LocalizationTeam/teams/calibration/modules
```

- [ ] **Step 2: 验证**

```bash
ls /Users/songshu/Projects/LocalizationTeam/teams/calibration/
```

Expected: 输出 `inbox  modules`

---

### Task 2：迁移原始资料 inbox

**Files:**
- Move: `teams/vision/inbox/003_标定相关/` → `teams/calibration/inbox/003_标定相关/`
- Move: `teams/vision/inbox/006_参数标定/` → `teams/calibration/inbox/006_参数标定/`

- [ ] **Step 1: 移动两个 inbox 目录**

```bash
mv "/Users/songshu/Projects/LocalizationTeam/teams/vision/inbox/003_标定相关" \
   "/Users/songshu/Projects/LocalizationTeam/teams/calibration/inbox/003_标定相关"

mv "/Users/songshu/Projects/LocalizationTeam/teams/vision/inbox/006_参数标定" \
   "/Users/songshu/Projects/LocalizationTeam/teams/calibration/inbox/006_参数标定"
```

- [ ] **Step 2: 验证移动结果**

```bash
ls /Users/songshu/Projects/LocalizationTeam/teams/calibration/inbox/
ls /Users/songshu/Projects/LocalizationTeam/teams/vision/inbox/
```

Expected：
- calibration/inbox/ 下有 `003_标定相关  006_参数标定`
- vision/inbox/ 下这两个目录已不存在

---

### Task 3：迁移已整理的 modules/calibration

**Files:**
- Move: `teams/vision/modules/calibration/` → `teams/calibration/modules/calibration/`

- [ ] **Step 1: 移动 modules/calibration**

```bash
mv "/Users/songshu/Projects/LocalizationTeam/teams/vision/modules/calibration" \
   "/Users/songshu/Projects/LocalizationTeam/teams/calibration/modules/calibration"
```

- [ ] **Step 2: 验证**

```bash
ls /Users/songshu/Projects/LocalizationTeam/teams/calibration/modules/calibration/
ls /Users/songshu/Projects/LocalizationTeam/teams/vision/modules/
```

Expected：
- calibration/modules/calibration/ 下有 `decisions.md  gaps.md  images  problems.md  timeline.md`
- vision/modules/ 下不再有 calibration 目录

---

### Task 4：新建 teams/calibration/people.md

**Files:**
- Create: `teams/calibration/people.md`（内容从 `teams/vision/people.md` 提取邱冰冰部分，标题改为「参数标定组」）

- [ ] **Step 1: 创建 calibration/people.md**

内容如下（将邱冰冰从 vision 人员表提取，调整标题）：

```markdown
# 参数标定组 — 人员地图

> 回答：出了问题找谁；这个人现在状态怎样；有没有单点风险。
> 来源标注格式：`（来源：YYYY-MM-DD 1:1 或周报）`

---

## 一、人员总览

| 姓名 | 当前角色 | 能力特点 | 当前状态 | 培养/风险备注 | 来源 |
|------|---------|---------|---------|-------------|------|
| 邱冰冰 | 标定方向负责人 | 【待填充】 | 【待填充】 | 【待填充】 | 2026-04-12 口述 |

---

## 二、单点依赖风险

> 如果某人离开/请假，哪些工作会立刻卡住？

| 风险点 | 当前唯一依赖人 | 影响范围 | 应对措施 |
|-------|-------------|---------|---------|
| 标定模块全部工作 | 邱冰冰 | 售后标定、侧目标定、Gaia多目适配 | 无备份 |

---

## 三、个人状态备忘

> 1:1 或日常观察到的关键信息，帮助判断真实状态。

### 邱冰冰
- **上次 1:1**：【待填充】
- **主要工作**：售后整机标定、侧目相机标定、Gaia 多目适配
- **真实困难**：【待填充】
- **状态判断**：【待填充】
- **跟进事项**：【待填充】

---

## 四、人员变动记录

| 日期 | 变动类型 | 人员 | 说明 |
|------|---------|------|------|
| 【待填充】 | 入组/离组/调岗 | 【待填充】 | 【待填充】 |
```

将以上内容写入 `teams/calibration/people.md`。

- [ ] **Step 2: 验证**

```bash
head -5 /Users/songshu/Projects/LocalizationTeam/teams/calibration/people.md
```

Expected: 第一行为 `# 参数标定组 — 人员地图`

---

### Task 5：新建 teams/calibration/tech.md

**Files:**
- Create: `teams/calibration/tech.md`（内容从 `teams/vision/tech.md` 提取「方向一：标定」全节，标题改为「参数标定组 — 技术地图」，移除「方向二」前缀，去掉「方向一：」前缀）

- [ ] **Step 1: 创建 calibration/tech.md**

内容：读取 `teams/vision/tech.md` 中从 `# 方向一：标定` 到 `# 方向二：VSLAM 建图定位算法` 之间的全部内容（即标定技术地图全部六节），在顶部替换标题如下：

```markdown
# 参数标定组 — 技术地图

> 回答：方案对不对；方向值不值得投；哪些是主问题。
> 来源标注格式：`（来源：YYYY-MM-DD 文档名）`

---
```

随后完整保留原 `teams/vision/tech.md` 中「方向一：标定」下的六节内容（一、方案框架；二、标定子类型；三、核心指标；四、当前瓶颈；五、优化方向；六、技术依赖与外部接口），不修改任何内容。

- [ ] **Step 2: 验证**

```bash
head -5 /Users/songshu/Projects/LocalizationTeam/teams/calibration/tech.md
grep -c "方向一\|方向二" /Users/songshu/Projects/LocalizationTeam/teams/calibration/tech.md
```

Expected：第一行为 `# 参数标定组 — 技术地图`；grep 输出 `0`（不含「方向一」「方向二」字样）

---

### Task 6：清理 teams/vision/people.md

**Files:**
- Modify: `teams/vision/people.md`

- [ ] **Step 1: 编辑文件**

将 `teams/vision/people.md` 改为：

```markdown
# 视觉定位组（VSLAM）— 人员地图

> 标定方向已独立至 [teams/calibration/](../calibration/people.md)，本文件仅维护 VSLAM 方向人员。
>
> 回答：出了问题找谁；这个人现在状态怎样；有没有单点风险。
> 来源标注格式：`（来源：YYYY-MM-DD 1:1 或周报）`

---

## 一、人员总览

| 姓名 | 当前角色 | 能力特点 | 当前状态 | 培养/风险备注 | 来源 |
|------|---------|---------|---------|-------------|------|
| 【待填充】 | 技术骨干 | 【待填充】 | 正常/压力大/需关注 | 【待填充】 | 【待填充】 |

---

## 二、单点依赖风险

| 风险点 | 当前唯一依赖人 | 影响范围 | 应对措施 |
|-------|-------------|---------|---------|
| 【待填充】 | 【待填充】 | 【待填充】 | 无备份/培养中/已有备份 |

---

## 三、个人状态备忘

### 【姓名占位】
- **上次 1:1**：【待填充】
- **主要工作**：【待填充】
- **真实困难**：【待填充】
- **状态判断**：【待填充】
- **跟进事项**：【待填充】

---

## 四、人员变动记录

| 日期 | 变动类型 | 人员 | 说明 |
|------|---------|------|------|
| 【待填充】 | 入组/离组/调岗 | 【待填充】 | 【待填充】 |
```

- [ ] **Step 2: 验证**

```bash
grep "邱冰冰" /Users/songshu/Projects/LocalizationTeam/teams/vision/people.md
```

Expected: 无输出（邱冰冰已移除）

---

### Task 7：清理 teams/vision/tech.md

**Files:**
- Modify: `teams/vision/tech.md`

- [ ] **Step 1: 编辑文件**

将 `teams/vision/tech.md` 改为（保留完整 VSLAM 占位部分，移除标定内容，顶部加注）：

```markdown
# 视觉定位组 — 技术地图

> 标定方向已独立至 [teams/calibration/tech.md](../calibration/tech.md)，本文件仅维护 VSLAM 建图定位算法方向。
>
> 回答：方案对不对；方向值不值得投；哪些是主问题。
> 来源标注格式：`（来源：YYYY-MM-DD 文档名）`

---

# VSLAM 建图定位算法

## 一、方案框架

| 维度 | 内容 | 来源 |
|------|------|------|
| 解决什么问题 | 【待填充】 | 【待填充】 |
| 主要输入 | 【待填充】 | 【待填充】 |
| 核心链路 | 【待填充】 | 【待填充】 |
| 输出给谁 | 【待填充】 | 【待填充】 |
| 对整体定位系统的价值 | 【待填充】 | 【待填充】 |

---

## 二、核心指标

| 指标名称 | 目标值 | 当前水平 | 差距 | 是否影响产品 | 来源 |
|---------|--------|---------|------|------------|------|
| 【待填充】 | 【待填充】 | 【待填充】 | 【待填充】 | 是/否 | 【待填充】 |

---

## 三、当前瓶颈

1. 【待填充】

---

## 四、优化方向

| 方向 | 当前进展 | 预期收益 | 成本/难度 | 风险 | 优先级 |
|------|---------|---------|---------|------|-------|
| 【待填充】 | 【待填充】 | 【待填充】 | 【待填充】 | 【待填充】 | 【待填充】 |

---

## 五、技术依赖与外部接口

| 依赖项 | 来自哪里 | 当前状态 | 备注 |
|--------|---------|---------|------|
| 【待填充】 | 【待填充】 | 稳定/不稳定/待对齐 | 【待填充】 |
```

- [ ] **Step 2: 验证**

```bash
grep -c "标定" /Users/songshu/Projects/LocalizationTeam/teams/vision/tech.md
```

Expected: 输出 `1`（仅剩顶部那条指向 calibration 的注释行）

---

### Task 8：更新 README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: 更新顶部描述**

将 README.md 顶部 `三个小组（多线激光、融合定位、视觉定位）` 改为 `四个方向（多线激光、融合定位、视觉定位、参数标定）`。

- [ ] **Step 2: 在「小组纵深层」表格末尾新增 calibration 行**

在 vision 的两行之后（`teams/vision/people.md` 行之后），新增：

```markdown
| [teams/calibration/tech.md](./teams/calibration/tech.md)           | 参数标定：技术方案框架、指标、瓶颈、优化方向 |
| [teams/calibration/people.md](./teams/calibration/people.md)       | 参数标定：人员角色、能力、状态、备注         |
```

- [ ] **Step 3: 更新功能模块过程知识表格——将所有 vision/modules/calibration 链接替换为 calibration/modules/calibration**

将以下 4 条链接全部更新路径：
- `teams/vision/modules/calibration/timeline.md` → `teams/calibration/modules/calibration/timeline.md`
- `teams/vision/modules/calibration/decisions.md` → `teams/calibration/modules/calibration/decisions.md`
- `teams/vision/modules/calibration/problems.md` → `teams/calibration/modules/calibration/problems.md`
- `teams/vision/modules/calibration/gaps.md` → `teams/calibration/modules/calibration/gaps.md`

同时将对应行的描述前缀从「标定模块：」保持不变（路径改了，文字不用动）。

- [ ] **Step 4: 更新原始资料 inbox 表格**

将 `teams/vision/inbox/` 条目的说明文字更新，标注「标定材料已迁出至 teams/calibration/inbox/」；并新增一行：

```markdown
| [teams/calibration/inbox/](./teams/calibration/inbox/) | 参数标定：原始设计文档、测试数据、方案资料 |
```

- [ ] **Step 5: 验证无断链**

```bash
grep -o '\./teams/vision/modules/calibration[^)]*' /Users/songshu/Projects/LocalizationTeam/README.md
grep -o '\./teams/vision/inbox/003[^)]*\|./teams/vision/inbox/006[^)]*' /Users/songshu/Projects/LocalizationTeam/README.md
```

Expected: 均无输出（旧路径已全部替换）

---

## 验收检查

完成所有 Task 后，运行以下检查：

```bash
# 1. calibration 结构完整性
find /Users/songshu/Projects/LocalizationTeam/teams/calibration -type f | sort

# 2. vision/inbox 和 vision/modules 不含标定内容
ls /Users/songshu/Projects/LocalizationTeam/teams/vision/inbox/
ls /Users/songshu/Projects/LocalizationTeam/teams/vision/modules/

# 3. README 链接中没有旧路径
grep "vision/modules/calibration\|vision/inbox/003\|vision/inbox/006" \
  /Users/songshu/Projects/LocalizationTeam/README.md
```

Expected：
1. calibration 下有 people.md、tech.md、inbox/（含两个子目录）、modules/calibration/（含5个文件）
2. vision/inbox/ 和 vision/modules/ 为空或仅有空目录
3. grep 无输出
