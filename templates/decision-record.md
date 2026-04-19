## D-<% await tp.system.prompt("决策编号（三位数字，如 042）") %> <% await tp.system.prompt("决策标题") %>【<% await tp.system.suggester(["已定案", "待确认"], ["已定案", "待确认"], false, "状态") %>】

**背景**

<% await tp.system.prompt("为什么需要这个决策？当前问题是什么？", "", true, true) %>

**选定方案**

<% await tp.system.prompt("最终采用的方案描述", "", true, true) %>

**理由**

<% await tp.system.prompt("为什么选这个方案，而不是替代方案", "", true, true) %>

**替代方案（可选）**

- 方案 A：[描述] —— 弃用原因：[...]
- 方案 B：[描述] —— 弃用原因：[...]

**影响范围**

- 受影响模块：
- 受影响接口/参数：

**来源** | <% await tp.system.prompt("来源文档路径，如 inbox/0418新增/xxx.md") %>

**决策日期** | <% tp.date.now("YYYY-MM-DD") %>

---
