# Daily Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在项目根目录创建 `workspace/` 个人日粒度工作空间，包含今日目录、inbox、daily.md 模板，并更新 DESIGN.md。

**Architecture:** 顶层新增 `workspace/YYYY-MM-DD/` 子目录，每日包含 `inbox/`（原始材料）和 `daily.md`（加工输出）。与现有 `teams/`、`overview/` 平级，纯增量，不修改现有文件（DESIGN.md 除外）。

**Tech Stack:** Markdown、shell（mkdir/touch）、git

---

### Task 1: 创建今日 workspace 目录和 daily.md 模板

**Files:**
- Create: `workspace/2026-04-14/inbox/.gitkeep`
- Create: `workspace/2026-04-14/daily.md`

- [ ] **Step 1: 创建今日目录结构**

```bash
cd /Users/songshu/Projects/LocalizationTeam
mkdir -p workspace/2026-04-14/inbox
touch workspace/2026-04-14/inbox/.gitkeep
```

`.gitkeep` 让空 inbox 目录可以被 git 追踪。

- [ ] **Step 2: 创建今日 daily.md，写入模板**

创建文件 `workspace/2026-04-14/daily.md`，内容如下：

```markdown
# 2026-04-14

## 待办
- [ ] 

## 团队进展
| 成员 | 组 | 进展/状态 | 待跟进 |
|------|---|---------|--------|
|      |   |         |        |

## 排期更新
- 

## 知识 & 信息积累
- 

## 原始材料
- 
```

- [ ] **Step 3: 验证目录结构正确**

```bash
find workspace/ -type f | sort
```

预期输出：

```
workspace/2026-04-14/daily.md
workspace/2026-04-14/inbox/.gitkeep
```

- [ ] **Step 4: Commit**

```bash
git add workspace/
git commit -m "feat: add daily workspace scaffold for 2026-04-14"
```

---

### Task 2: 更新 DESIGN.md，将 workspace/ 纳入官方结构说明

**Files:**
- Modify: `DESIGN.md`（第二节「整体结构」的目录树）

- [ ] **Step 1: 在 DESIGN.md 第二节目录树中添加 workspace/**

找到第二节的代码块，在 `projects/` 块之后追加：

```
└── workspace/                   ← TL 个人日粒度工作空间
    └── YYYY-MM-DD/
        ├── inbox/               ← 当日原始材料，直接拖入，不加工
        └── daily.md             ← 当日加工输出（待办 / 团队进展 / 排期 / 知识积累）
```

- [ ] **Step 2: 在第七节「维护节奏建议」的频率表中补充每日条目**

在表格末尾添加一行：

```markdown
| 每日 | 新建 `workspace/$(date +%F)/inbox/`，拖入当天材料；有时间时填 `daily.md` |
```

- [ ] **Step 3: 验证 DESIGN.md 无语法问题**

打开文件确认 Markdown 表格和代码块格式正确，无多余空行或缩进错误。

- [ ] **Step 4: Commit**

```bash
git add DESIGN.md
git commit -m "docs: document workspace/ in DESIGN.md structure and maintenance rhythm"
```

---

### Task 3: 创建通用 daily.md 模板文件（可复用）

**Files:**
- Create: `workspace/TEMPLATE-daily.md`

每次新建一天时，从这个模板复制，避免手动重写。

- [ ] **Step 1: 创建模板文件 `workspace/TEMPLATE-daily.md`**

```markdown
# YYYY-MM-DD

## 待办
- [ ] 

## 团队进展
| 成员 | 组 | 进展/状态 | 待跟进 |
|------|---|---------|--------|
|      |   |         |        |

## 排期更新
- 

## 知识 & 信息积累
- 

## 原始材料
- 
```

- [ ] **Step 2: 验证文件存在**

```bash
ls workspace/TEMPLATE-daily.md
```

预期输出：`workspace/TEMPLATE-daily.md`

- [ ] **Step 3: Commit**

```bash
git add workspace/TEMPLATE-daily.md
git commit -m "feat: add daily.md template for reuse"
```

---

## 快速创建新一天的命令（备忘）

```bash
# 在项目根目录执行：
D=$(date +%F)
mkdir -p workspace/$D/inbox
cp workspace/TEMPLATE-daily.md workspace/$D/daily.md
sed -i '' "s/YYYY-MM-DD/$D/" workspace/$D/daily.md
touch workspace/$D/inbox/.gitkeep
echo "Created workspace/$D/"
```
