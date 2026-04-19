# Templates 模板使用说明

本仓库有**两类**模板，分工明确：


| 类型              | 位置                                                   | 引擎              | 用途                                                                     |
| --------------- | ---------------------------------------------------- | --------------- | ---------------------------------------------------------------------- |
| **Daily 工作流模板** | `workspace/TEMPLATE-daily.md`                        | 纯 markdown（手维护） | 每日 daily.md 的"源真理"骨架                                                   |
| **Daily 自动化**   | `templates/daily-bootstrap.md`                       | Templater (JS)  | **每次启动 Obsidian 自动跑** + 可手动触发；建当天目录 + 顺延未完成跟进项                          |
| **Weekly 自动化**  | `templates/weekly-bootstrap.md`                      | Templater (JS)  | 周五/周一手动触发；聚合本周 daily + 跨模块决策/问题，生成 `weekly/YYYY-Www.md`                |
| **结构化片段**       | `templates/{decision,problem,competitor,inbox}-*.md` | 纯 markdown 骨架   | 在任意文件里快速插入符合 conventions 的章节骨架                                         |


---

## 一、每日开工：daily-bootstrap

### 触发方式

| 场景 | 触发 |
|---|---|
| **早上打开 Obsidian** | ✨ **自动跑**（已在 Templater Settings → Startup Templates 配置） |
| **任何时候手动触发** | `Cmd+P` → `Templater: Create new note from template` → 选 `daily-bootstrap` |

### 它会做什么

1. 在 `workspace/YYYY-MM-DD/` 下建好 `daily.md`、`inbox/`、`images/`
2. 套用 `workspace/TEMPLATE-daily.md` 骨架（替换标题日期）
3. 自动找最近一份 `workspace/<历史日期>/daily.md`，**把「跟进/派发」章节里所有未勾选的 `- [ ]` 项（含子缩进）复制过来**
4. 顺延块前加注释：`> 以下条目从 YYYY-MM-DD 顺延而来`
5. 行为差异：
   - **手动触发**：建好后自动打开新 daily.md，并清理 Templater 中间产物
   - **startup 自动触发**：建好后**安静返回**，不打断你正在看的笔记。如果今天的 daily 已存在，连 Notice 都不弹

### 约定

- 跟进/派发章节统一用 `- [ ]` 复选框（与 Tasks 插件联动）
- 完成的项标 `- [x]`
- 想中止某条但保留记录，可以改成 `- [~]` 或加注释，**只要不是 `- [ ]` 就不会被顺延**
- 「我的工作项」章节**不顺延**（设计上每天重新规划）

### 推荐绑定快捷键（手动触发场景）

`Settings → Templater → Template Hotkeys` → 给 `daily-bootstrap` 绑定（如 `Cmd+Alt+D`）

---

## 一·B、周报：weekly-bootstrap

### 触发方式

`Cmd+P` → `Templater: Create new note from template` → 选 `weekly-bootstrap`

**推荐时机**：
- **周五下班前**跑一次 → 周末品一品 → 周一交
- 或**周一早上**跑一次复盘上周

### 它会做什么

生成 `weekly/YYYY-Www.md`（如 `weekly/2026-W17.md`），自动聚合：

| 章节 | 数据源 | 说明 |
|---|---|---|
| 一、本周已完成 | 本周内所有 daily 的 `- [x]` 项 | 按日期分组 |
| 二、未完成 / 顺延到下周 | 本周末最后一份 daily 的「跟进/派发」未勾选项 | 自动识别"周末" |
| 三、本周新增决策 | 扫所有 `*/modules/*/decisions.md`，找日期落在本周的 D-xxx | 通过条目里的日期字段过滤 |
| 四、本周新增问题 | 扫所有 `*/modules/*/problems.md`，找日期落在本周的 P-xxx | 同上 |
| 五、团队进展（聚合） | 各 daily 的「团队进展」节合并 | 跳过空骨架 |
| 六、排期变动 | 各 daily 的「排期更新」节合并 | 跳过空骨架 |
| 七、知识 & 信息沉淀 | 各 daily 的「知识 & 信息积累」节合并 | 跳过空骨架 |
| 八、本周复盘（手写） | 留白 | 你周末手填：做得好/不好/下周重点/给团队的话 |

### 行为约定

- ISO 周编号（周一为周首），如 `2026-W17` 对应 `2026-04-20 ~ 2026-04-26`
- **如果当周 weekly 文件已存在，不会覆盖**（保护你已写的复盘）—— 想重新聚合请先手动删除
- 决策/问题靠"条目里有日期字段（YYYY-MM-DD）"识别，请保持 conventions：
  - `**决策日期** | YYYY-MM-DD`
  - `**首次发现**：YYYY-MM-DD`

---

## 二、骨架片段：decision / problem / competitor / inbox

### 用法（两种）

**方式 A：在 Obsidian 里插入到当前光标**

1. 用 Obsidian **核心** Templates 插件（不是 Templater）：`Settings → Templates → Template folder` 设为 `templates`
2. 光标定位到目标位置 → `Cmd+P` → `Insert template` → 选骨架

**方式 B：直接复制粘贴**
打开对应的 `templates/xxx.md`，全选复制即可（这些文件本身就是干净 markdown）。

### 骨架清单


| 文件                          | 用途         | 输出位置建议                                               |
| --------------------------- | ---------- | ---------------------------------------------------- |
| `decision-record.md`        | D-XXX 决策记录 | 追加到 `<group>/modules/<mod>/decisions.md`             |
| `problem-record.md`         | P-XXX 问题记录 | 追加到 `<group>/modules/<mod>/problems.md`              |
| `competitor-test-report.md` | 竞品测试完整报告   | `inbox/MMDD新增/<竞品名>-竞品测试/` 下新建                       |
| `inbox-raw-material.md`     | 原始素材录入     | `workspace/YYYY-MM-DD/inbox/` 或 `inbox/MMDD新增/<主题>/` |


### 设计原则

- 严格对齐 `[docs/process/raw-materials-conventions.md](../docs/process/raw-materials-conventions.md)`：D/P/Q/G/R 编号、状态标记（✅⚠️🔴❓）
- 占位符用 HTML 注释 `<!-- ... -->`，渲染时不显示，但提示填什么
- 字段位置统一，便于 Cursor 跑 `raw-materials-curation` skill 时识别

---

## 三、协作模型

```
┌──────────────────────────────────────────────┐
│ workspace/TEMPLATE-daily.md  ← 你手维护      │
│         │                                    │
│         ▼                                    │
│ templates/daily-bootstrap.md (Templater)     │
│         │                                    │
│         ▼                                    │
│ workspace/YYYY-MM-DD/daily.md                │
│   - 含顺延的跟进项                           │
│   - 在里面用 templates/*.md 骨架插决策/问题  │
└──────────────────────────────────────────────┘
                    │
                    ▼ （阶段性）
            Cursor 跑 raw-materials-curation
                    │
                    ▼
        <group>/modules/<mod>/{timeline,decisions,problems,gaps}.md
```

- **Obsidian 端**：daily-bootstrap 一键开工 → 用骨架快速记录
- **Cursor 端**：周期性把 `inbox/` 和 `workspace/*/inbox/` 的素材结构化提取到各模块文档

---

## 四、修改 / 扩展模板

- **改 daily 骨架** → 编辑 `workspace/TEMPLATE-daily.md`（daily-bootstrap 自动读最新版）
- **改片段骨架** → 直接编辑 `templates/*.md`（纯 markdown，所见即所得）
- **改 daily-bootstrap 的逻辑**（如改顺延范围、加新步骤）→ 编辑 `templates/daily-bootstrap.md` 里的 JS

Templater 语法参考：[https://silentvoid13.github.io/Templater/syntax.html](https://silentvoid13.github.io/Templater/syntax.html)