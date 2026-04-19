## P-<% await tp.system.prompt("问题编号（三位数字，如 037）") %> <% await tp.system.prompt("问题标题") %>

- **症状**：<% await tp.system.prompt("用户/测试观察到的具体现象", "", true, true) %>
- **复现条件**：<% await tp.system.prompt("场景/参数/版本", "", true, true) %>
- **根因**：<% await tp.system.prompt("根本原因分析（可填「待定位」）", "", true, true) %>
- **修复**：<% await tp.system.suggester(["已修复", "进行中", "待修复", "待定位"], ["已修复", "进行中", "待修复", "待定位"], false, "状态") %><% await tp.system.prompt("（补充说明，如版本号 / commit / 责任人）", "", false, false) %>
- **影响范围**：<% await tp.system.prompt("影响哪些模块/场景/客户") %>
- **优先级**：<% await tp.system.suggester(["高", "中", "低"], ["高", "中", "低"], false, "优先级") %>
- **来源**：<% await tp.system.prompt("来源文档路径") %>
- **首次发现**：<% tp.date.now("YYYY-MM-DD") %>

---
