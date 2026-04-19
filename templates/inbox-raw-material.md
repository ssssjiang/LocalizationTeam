# <% tp.file.title %>

> **来源**：<% await tp.system.prompt("来源（如：飞书文档/微信群/会议纪要）") %>
> **录入日期**：<% tp.date.now("YYYY-MM-DD") %>
> **录入人**：<% await tp.system.prompt("录入人") %>
> **涉及组别**：<% await tp.system.suggester(["laser", "fusion", "vision", "calibration", "overview"], ["laser", "fusion", "vision", "calibration", "overview"], false, "选择组别") %>
> **分类（A/B/C）**：<% await tp.system.suggester(["A 类（含决策/方案）", "B 类（过程记录）", "C 类（数据/手册）"], ["A", "B", "C"], false, "三层分类") %>

---

## 原始内容

<%* tR += await tp.system.prompt("（粘贴或描述原始内容；可留空稍后补）", "", true, true) %>

---

## 待提取要点（梳理时填）

- [ ] 决策点 → `decisions.md` D-xxx
- [ ] 时间线条目 → `timeline.md`
- [ ] 问题记录 → `problems.md` P-xxx
- [ ] 待确认问题 → `gaps.md` Q-xxx
- [ ] 外链/未补全文档 → `gaps.md` G-xxx

## 关联文档

- 相关 inbox：
- 相关 module 输出：
