#!/usr/bin/env python3
"""
Notion API helper script for OpenClaw agent.
Usage:
  python3 notion_api.py search <query>
  python3 notion_api.py get_page <page_id>
  python3 notion_api.py get_db <database_id>
  python3 notion_api.py query_db <database_id> [--filter '{"property":"...","..."}']
  python3 notion_api.py create_page <parent_id> <title> [<markdown_content>]
  python3 notion_api.py append_block <page_id> <markdown_content>
  python3 notion_api.py list_dbs
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.parse

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"
BASE_URL = "https://api.notion.com/v1"


def headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def request(method, path, data=None):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers(), method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "message": e.read().decode()}


def search(query, filter_type=None):
    payload = {"query": query, "page_size": 10}
    if filter_type:
        payload["filter"] = {"value": filter_type, "property": "object"}
    result = request("POST", "/search", payload)
    if "error" in result:
        return result
    items = []
    for r in result.get("results", []):
        obj_type = r.get("object")
        obj_id = r.get("id")
        if obj_type == "page":
            title = _get_title(r)
            items.append({"type": "page", "id": obj_id, "title": title,
                          "url": r.get("url", "")})
        elif obj_type == "database":
            title = _get_db_title(r)
            items.append({"type": "database", "id": obj_id, "title": title,
                          "url": r.get("url", "")})
    return items


def _get_title(page):
    props = page.get("properties", {})
    for prop in props.values():
        if prop.get("type") == "title":
            rich = prop.get("title", [])
            return "".join(t.get("plain_text", "") for t in rich)
    return "(untitled)"


def _get_db_title(db):
    rich = db.get("title", [])
    return "".join(t.get("plain_text", "") for t in rich) or "(untitled)"


def get_page(page_id):
    page = request("GET", f"/pages/{page_id}")
    if "error" in page:
        return page
    blocks = get_blocks(page_id)
    return {"page": page, "blocks": blocks}


def get_blocks(block_id, max_depth=5, depth=0):
    result = request("GET", f"/blocks/{block_id}/children?page_size=100")
    if "error" in result:
        return []
    blocks = []
    for b in result.get("results", []):
        btype = b.get("type", "unknown")
        # Handle synced_block: read from synced_from source if present
        if btype == "synced_block":
            synced_from = b.get("synced_block", {}).get("synced_from")
            if synced_from:
                # Points to another block — read that block's children
                source_id = synced_from.get("block_id")
                if source_id and depth < max_depth:
                    blocks.extend(get_blocks(source_id, max_depth, depth + 1))
            elif b.get("has_children") and depth < max_depth:
                # This IS the original synced block — read its children directly
                blocks.extend(get_blocks(b["id"], max_depth, depth + 1))
            continue
        block = _simplify_block(b)
        if b.get("has_children") and depth < max_depth:
            block["children"] = get_blocks(b["id"], max_depth, depth + 1)
        blocks.append(block)
    return blocks


def _simplify_block(b):
    btype = b.get("type", "unknown")
    content = b.get(btype, {})
    text = ""
    if "rich_text" in content:
        text = "".join(t.get("plain_text", "") for t in content["rich_text"])
    return {"id": b["id"], "type": btype, "text": text}


def blocks_to_markdown(blocks, indent=0):
    lines = []
    prefix = "  " * indent
    for b in blocks:
        btype = b.get("type")
        text = b.get("text", "")
        if btype == "paragraph":
            lines.append(f"{prefix}{text}")
        elif btype.startswith("heading_"):
            level = int(btype[-1])
            lines.append(f"{'#' * level} {text}")
        elif btype in ("bulleted_list_item", "to_do"):
            lines.append(f"{prefix}- {text}")
        elif btype == "numbered_list_item":
            lines.append(f"{prefix}1. {text}")
        elif btype == "code":
            lines.append(f"```\n{text}\n```")
        elif btype == "quote":
            lines.append(f"{prefix}> {text}")
        elif btype == "divider":
            lines.append("---")
        elif text:
            lines.append(f"{prefix}{text}")
        if b.get("children"):
            lines.append(blocks_to_markdown(b["children"], indent + 1))
    return "\n".join(lines)


def get_db(database_id):
    return request("GET", f"/databases/{database_id}")


def query_db(database_id, filter_obj=None, sorts=None, page_size=20):
    payload = {"page_size": page_size}
    if filter_obj:
        payload["filter"] = filter_obj
    if sorts:
        payload["sorts"] = sorts
    return request("POST", f"/databases/{database_id}/query", payload)


def list_dbs():
    result = request("POST", "/search", {"filter": {"value": "database", "property": "object"}, "page_size": 20})
    if "error" in result:
        return result
    return [{"id": r["id"], "title": _get_db_title(r), "url": r.get("url", "")}
            for r in result.get("results", [])]


def markdown_to_blocks(md):
    """Convert simple markdown to Notion blocks."""
    blocks = []
    for line in md.split("\n"):
        if not line.strip():
            continue
        if line.startswith("### "):
            blocks.append({"object": "block", "type": "heading_3",
                           "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}})
        elif line.startswith("## "):
            blocks.append({"object": "block", "type": "heading_2",
                           "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}})
        elif line.startswith("# "):
            blocks.append({"object": "block", "type": "heading_1",
                           "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.startswith("- ") or line.startswith("* "):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.startswith("> "):
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}})
        elif line.strip() == "---":
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        else:
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": [{"type": "text", "text": {"content": line}}]}})
    return blocks


def create_page(parent_id, title, content_md=None):
    """Create a page under a parent page or database."""
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
    }
    if content_md:
        payload["children"] = markdown_to_blocks(content_md)
    return request("POST", "/pages", payload)


def append_block(page_id, content_md):
    blocks = markdown_to_blocks(content_md)
    return request("PATCH", f"/blocks/{page_id}/children", {"children": blocks})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["search", "get_page", "get_db", "query_db",
                                             "create_page", "append_block", "list_dbs"])
    parser.add_argument("args", nargs="*")
    parser.add_argument("--filter", dest="filter_json", default=None)
    parser.add_argument("--type", dest="filter_type", default=None, help="page or database")
    args = parser.parse_args()

    if not NOTION_TOKEN:
        print(json.dumps({"error": "NOTION_API_KEY not set"}))
        sys.exit(1)

    result = None
    if args.command == "search":
        result = search(" ".join(args.args), args.filter_type)
    elif args.command == "get_page":
        data = get_page(args.args[0])
        md = blocks_to_markdown(data.get("blocks", []))
        result = {"id": args.args[0], "markdown": md}
    elif args.command == "get_db":
        result = get_db(args.args[0])
    elif args.command == "query_db":
        f = json.loads(args.filter_json) if args.filter_json else None
        result = query_db(args.args[0], filter_obj=f)
    elif args.command == "create_page":
        content = args.args[2] if len(args.args) > 2 else None
        result = create_page(args.args[0], args.args[1], content)
    elif args.command == "append_block":
        result = append_block(args.args[0], " ".join(args.args[1:]))
    elif args.command == "list_dbs":
        result = list_dbs()

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
