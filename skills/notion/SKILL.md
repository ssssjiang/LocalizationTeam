---
name: notion
description: |
  Notion 工作区操作工具。支持搜索、读取页面/数据库、创建页面、追加内容。

  **当以下情况时使用此 Skill**：
  (1) 需要在 Notion 中搜索页面或数据库
  (2) 需要读取某个 Notion 页面的内容
  (3) 需要查询 Notion 数据库的记录
  (4) 需要在 Notion 中创建新页面或追加内容
  (5) 用户提到"Notion"、"笔记"、"知识库"、"第二大脑"
metadata:
  openclaw:
    requires:
      env:
        - NOTION_API_KEY
    primaryEnv: NOTION_API_KEY
---

# Notion Skill

工作区：shu song's Notion

## 环境变量

`NOTION_API_KEY` 已配置（Integration Token）

## 脚本路径

`{skillDir}/scripts/notion_api.py`

调用格式：
```bash
NOTION_API_KEY=<token> python3 {skillDir}/scripts/notion_api.py <command> [args]
```

---

## 工具索引

| 意图 | 命令 | 示例 |
|------|------|------|
| 搜索页面/数据库 | `search <关键词>` | `search SLAM` |
| 只搜索页面 | `search <关键词> --type page` | `search 项目规划 --type page` |
| 只搜索数据库 | `search <关键词> --type database` | `search 任务 --type database` |
| 读取页面内容 | `get_page <page_id>` | `get_page abc123` |
| 列出所有数据库 | `list_dbs` | `list_dbs` |
| 查询数据库记录 | `query_db <db_id>` | `query_db abc123` |
| 创建页面 | `create_page <parent_id> <title> [内容]` | `create_page abc123 "今日复盘"` |
| 追加内容到页面 | `append_block <page_id> <markdown>` | `append_block abc123 "# 新章节"` |

---

## 常用操作示例

### 搜索并读取页面

```bash
# 搜索
NOTION_API_KEY=$NOTION_API_KEY python3 {skillDir}/scripts/notion_api.py search "OKVIS"

# 读取（返回 Markdown 格式内容）
NOTION_API_KEY=$NOTION_API_KEY python3 {skillDir}/scripts/notion_api.py get_page <page_id>
```

### 列出所有数据库

```bash
NOTION_API_KEY=$NOTION_API_KEY python3 {skillDir}/scripts/notion_api.py list_dbs
```

### 创建页面

```bash
NOTION_API_KEY=$NOTION_API_KEY python3 {skillDir}/scripts/notion_api.py create_page <parent_page_id> "标题" "# 正文内容"
```

### 追加内容

```bash
NOTION_API_KEY=$NOTION_API_KEY python3 {skillDir}/scripts/notion_api.py append_block <page_id> "## 新增章节\n- 要点1\n- 要点2"
```

---

## Page ID 格式说明

Notion 页面 URL 格式：
```
https://www.notion.so/Page-Title-<32位ID>
```

从 URL 中提取最后 32 位字符（可加连字符也可不加）作为 page_id。

---

## 注意事项

- Integration 需要有权限访问对应页面（在 Notion 页面里 Share → Invite Integration）
- `get_page` 返回 Markdown 格式，最多递归 2 层子块
- `query_db` 默认返回 20 条记录，可加 `--filter` 参数过滤
