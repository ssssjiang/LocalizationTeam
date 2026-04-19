# Obsidian 配置指南（团队知识库）

> 本文档是 LocalizationTeam 知识库的 Obsidian 使用规范与初始化指南。
> **使用模式**：Cursor 负责整理/重构原始素材，Obsidian 负责阅读、检索与轻量编辑。两者共享同一 vault（即本仓库根目录）。

---

## 一、安装与初始化

### 1. 安装 Obsidian（macOS）

```bash
brew install --cask obsidian
```

### 2. 打开 Vault

启动 Obsidian → "Open folder as vault" → 选择本仓库根目录 `LocalizationTeam/`。

### 3. 关键设置（Settings → ...）

| 设置项 | 推荐值 | 原因 |
|---|---|---|
| Files & Links → New link format | `Relative path to file` | 与标准 markdown 兼容，Cursor / GitHub 都能正确解析 |
| Files & Links → Use [[Wikilinks]] | **关闭** | 强制使用 `[text](path)` 标准链接，避免 Cursor 处理冲突 |
| Files & Links → Default location for new attachments | `In subfolder under current folder` → `images` | 与现有 `inbox/.../images/` 约定一致 |
| Editor → Show line number | 开启 | 与 Cursor 排查行号一致 |
| Editor → Strict line breaks | 开启 | 严格 markdown，避免渲染歧义 |
| Appearance → Theme | Minimal / Things / 默认 | 个人喜好 |
| Core plugins → Templates | 开启 | 配合 Templater 使用 |
| Core plugins → Tag pane | 开启 | 标签导航 |
| Core plugins → Outline | 开启 | 长文档大纲 |
| Core plugins → Backlinks | 开启 | 反向链接面板 |
| Core plugins → Graph view | 开启 | 知识图谱 |

---

## 二、推荐插件清单

> 安装方式：Settings → Community plugins → Browse → 搜索插件名 → Install → Enable。
> 首次启用社区插件需先关闭 "Restricted mode"。

### 🔴 必装（5 个，核心体验）

| 插件 | 作用 | 团队场景 |
|---|---|---|
| **Dataview** | 类 SQL 查询 markdown 元数据，生成动态表格/列表 | 自动汇总 `inbox/` 按日期组织的素材；周报里嵌入查询块 |
| **Templater** | 强大的模板引擎（变量、JS 脚本） | 一键生成「竞品测试笔记」「周报分析」「问题跟踪」模板 |
| **Excalidraw** | 手绘风白板，文件本质是 `.md`（git 友好） | 画 SLAM 架构图、流程图，可与文档双链 |
| **Advanced Tables** | Markdown 表格自动对齐、Tab 跳转、公式 | 竞品对比、人员分工、问题清单等表格场景 |
| **Iconize**（Iconic） | 给文件夹/文件加图标 | `inbox/`、`docs/`、`people/` 一眼区分 |

### 🟡 强烈推荐（知识库扩展能力）

| 插件 | 作用 | 团队场景 |
|---|---|---|
| **Git** | 内置 commit/pull/push，可设置自动同步间隔 | 阅读时顺手提交修改，不用切终端 |
| **Tag Wrangler** | 标签重命名、合并、层级管理 | 库变大后必备，否则标签会失控 |
| **Outliner** | 列表项折叠、上下移动、快捷键操作 | 整理周报要点、做层级化分析 |
| **Kanban** | 看板视图（文件本质仍是 md） | 可视化 `problems.md`、`gaps.md` 的 TODO |
| **Calendar** | 侧边栏日历，点击日期跳转日记 | 与 `inbox/0418新增/` 这种日期组织模式契合 |
| **Periodic Notes** | 配合 Calendar，自动管理日/周/月笔记 | 周报体系直接落地 |
| **Linter** | 保存时自动规范化 markdown 格式 | 统一 Cursor 与 Obsidian 产出的格式 |

### 🟢 按需选装

| 插件 | 适用场景 |
|---|---|
| **Mind Map** | 把大纲一键转思维导图（俯瞰 `tech.md`） |
| **Image Toolkit** | 图片缩放、灯箱预览（竞品截图浏览） |
| **Paste Image Rename** | 粘贴图片自动重命名+落到 `images/` |
| **Better Search Views** | 搜索结果以可折叠树形展示 |
| **Style Settings** | 主题/CSS 变量可视化调节 |
| **Omnisearch** | 全文模糊搜索（含 PDF OCR） |
| **Admonition** | 漂亮的 callout 块（warning/note/tip） |
| **Mermaid Tools** | mermaid 编辑/预览增强 |
| **Citations** + Zotero | 文献管理（如做技术调研） |

### ⚪ 主题推荐

- **Minimal**（极简，配 Style Settings 可玩性高）
- **Things**（仿 Things 3，清爽）
- **Border**（深色党友好）

---

## 三、与 Cursor 的协作约定

```
┌────────────────┐                    ┌──────────────────┐
│ Cursor         │                    │ Obsidian         │
│ - 跑 skills    │   共享 vault       │ - 阅读文档       │
│ - 整理 inbox/  │ ◄─────────────────►│ - 双链/反向链接  │
│ - 批量重构 md  │  (LocalizationTeam)│ - 看板/日历/图谱 │
│ - git 操作     │                    │ - 轻量编辑/标签  │
└────────────────┘                    └──────────────────┘
```

### 分工原则

| 任务类型 | 工具 |
|---|---|
| 处理 `inbox/` 原始素材、跑 skill、批量改写 | **Cursor** |
| 跨文档梳理、生成 `timeline.md` / `decisions.md` 等 | **Cursor** |
| 阅读已整理的文档、查找信息、做笔记 | **Obsidian** |
| 标签整理、双向链接补充、画 Excalidraw | **Obsidian** |
| 日常 git 提交、推送 | 任一（Obsidian Git 插件 or Cursor 终端） |

### 注意事项

1. **不要在 Obsidian 里使用 wikilinks `[[xxx]]`**：会让 Cursor 难以解析。统一用 `[text](relative/path.md)`。
2. **图片路径保持相对**：默认设置已配置为 `In subfolder under current folder` → `images`，与现有约定一致。
3. **`.obsidian/` 目录的提交策略**：
   - **提交**：`.obsidian/community-plugins.json`（插件清单）、`.obsidian/appearance.json`（主题）、`.obsidian/app.json`（基础配置） → 团队共享配置
   - **忽略**：`workspace.json`（个人窗口布局）、`cache`（本机缓存） → 已在 `.gitignore` 中配置

---

## 四、初始化检查清单

新成员接入时按此 checklist 操作：

- [ ] `brew install --cask obsidian`
- [ ] 打开 vault：选择 `LocalizationTeam/` 仓库根目录
- [ ] 关闭 Restricted mode（Settings → Community plugins → Turn on）
- [ ] 按「关键设置」表格调整偏好
- [ ] 安装 🔴 必装的 5 个插件
- [ ] 试用一周后再补 🟡 推荐插件
- [ ] （可选）安装 Git 插件并配置自动 pull
