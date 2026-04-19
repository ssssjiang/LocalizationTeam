# Templates 模板使用说明

本目录为 [Templater 插件](https://silentvoid13.github.io/Templater/) 模板。模板严格遵循团队已有规范，详见 [`docs/process/raw-materials-conventions.md`](../docs/process/raw-materials-conventions.md) 和 [`docs/process/special-report-template.md`](../docs/process/special-report-template.md)。

---

## 模板清单

| 模板文件 | 用途 | 输出位置建议 |
|---|---|---|
| `inbox-raw-material.md` | 录入新的原始素材（飞书/微信/会议纪要） | `inbox/MMDD新增/<主题>/<主题>.md` |
| `decision-record.md` | 单条决策记录（D-xxx 格式） | 追加到 `<group>/modules/<mod>/decisions.md` |
| `problem-record.md` | 单条问题记录（P-xxx 格式） | 追加到 `<group>/modules/<mod>/problems.md` |
| `competitor-test-report.md` | 竞品测试报告（含建图/定位/边界场景对比） | `inbox/MMDD新增/<竞品名>-竞品测试/` |
| `weekly-note.md` | 周报梳理入口（汇总各组进展） | `weekly/YYYY-Www.md`（配合 Periodic Notes） |

---

## 使用方式

### 方法 1：命令面板（推荐）

1. `Cmd+P` 打开命令面板
2. 输入 `Templater: Open Insert Template modal`（或 `Templater: 创建新文件`）
3. 选择模板 → 按提示输入参数

### 方法 2：快捷键

可在 `Settings → Templater → Template Hotkeys` 为常用模板（如 `inbox-raw-material`）绑定快捷键。

### 方法 3：文件夹自动应用

在 `Settings → Templater → Folder Templates` 中可配置：
- `inbox/` → 自动应用 `inbox-raw-material.md`
- `weekly/` → 自动应用 `weekly-note.md`

这样在对应文件夹新建文件时，会自动套用模板并弹出参数输入框。

---

## 模板设计原则

1. **严格对齐 conventions**：D-xxx / P-xxx / Q-xxx / G-xxx / R-xxx 编号体系，✅⚠️🔴❓ 状态标记
2. **强制写关键字段**：用 `tp.system.prompt` 让用户在创建时就填好来源、日期、负责人，避免事后补
3. **预留 TODO checklist**：原始素材模板里嵌入「待提取要点」清单，方便后续 Cursor 跑 `raw-materials-curation` skill 时识别
4. **与 Cursor 协作**：所有模板产出的都是标准 markdown，Cursor 跑 skill 时无需特殊处理

---

## 修改模板

直接编辑本目录下的 `.md` 文件即可。Templater 语法参考：https://silentvoid13.github.io/Templater/syntax.html

常用变量：
- `<% tp.date.now("YYYY-MM-DD") %>` — 当前日期
- `<% tp.file.title %>` — 当前文件名
- `<% await tp.system.prompt("提示语") %>` — 弹窗输入
- `<% await tp.system.suggester(["显示A","显示B"], ["返回值A","返回值B"]) %>` — 下拉选择
