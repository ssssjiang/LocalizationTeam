# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## QMD - 本地搜索引擎

全局安装 qmd 2.0.1，索引了 workspace、skills、memory 目录。

**快速命令**：
```bash
# Keyword 搜索（最快）
qmd search "cron workflow"

# 向量语义搜索
qmd vsearch "how to debug VIO"

# 混合搜索 + LLM reranking（最好）
qmd query "skill development patterns"

# 查看某个文档
qmd get qmd://workspace/memory.md

# 查看索引状态
qmd status
```

**Collections**：
- `skills` — OpenClaw skills（SKILL.md）
- `memory` — 长期记忆（MEMORY.md + memory/ 目录）
- `workspace` — 整个 workspace 配置

**更新索引**（新增文件后）：
```bash
qmd embed  # 重新生成向量（约 1 分钟）
```

**GPU 加速**：已启用 Vulkan（RTX 4070），向量搜索快。

---

## Exa MCP Server - 网络搜索

已配置全球搜索引擎（web search + code search + company research）。

**配置细节**：
- API Key: `13dbd550-0ed8-4f6e-aad5-07ec5f8a565f`
- 环境变量：`EXA_API_KEY`（已写入 ~/.zshrc）
- MCP 配置：`.mcp.json` 中配置为 HTTP 服务（https://mcp.exa.ai/mcp）

**快速搜索**（Agent 中可用）：
```bash
exa.search("SLAM research papers 2024")
exa.search("Python async patterns", search_type="code")
exa.research_company("OpenAI")
```

**与 QMD 的分工**：
- **QMD**：本地 workspace + memory 搜索（快）
- **Exa**：全网络搜索（新信息、研究资料）

---

## PinchTab - 浏览器控制服务

全局安装 pinchtab 0.7.8，为 AI agents 提供无头浏览器控制能力。

**快速启动**：
```bash
# 启动服务器（默认 localhost:9867）
pinchtab

# 测试连接
curl http://localhost:9867/health

# 命令行操作
pinchtab nav https://example.com         # 导航到网页
pinchtab snap                             # 获取当前页面快照
pinchtab click "button text"              # 点击按钮
pinchtab type "input text"                # 输入文本
```

**HTTP API（Agent 推荐）**：
```bash
# 通过 HTTP API 控制
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

curl http://localhost:9867/snapshot | jq .text
```

**特性**：
- 12MB Go 二进制，零外部依赖
- Token 高效：~800 tokens/页面（vs 截图 5-13x 贵）
- 支持有头/无头运行
- 多实例并行，隔离 profiles
- Accessibility-first（稳定元素引用，无坐标脆弱性）
- ARM64 优化（Raspberry Pi 友好）

**与 OpenClaw browser 工具的区别**：
- **OpenClaw browser**：内置简易浏览器工具
- **PinchTab**：专业级浏览器控制，token 更高效，功能更完整

**适用场景**：
- 网页自动化测试
- 数据采集（vs Exa 的搜索）
- 复杂交互流程
- 长会话维护

**文档**：https://pinchtab.com
