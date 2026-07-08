#!/usr/bin/env python3
"""Convert refactoring-study chapter markdown files to standalone HTML.

Self-contained output: inline CSS + Pygments code highlighting, no external
network dependency. Handles tables, fenced code (C++ highlighting),
blockquotes, task lists and admonitions.

Usage:
    python3 scripts/md_to_html.py            # convert the 4 chapters
    python3 scripts/md_to_html.py FILE ...   # convert specific files
"""
from __future__ import annotations

import sys
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "html"

DEFAULT_FILES = [
    "第02章-重构的原则.md",
    "第03章-代码的坏味道.md",
    "第04章-构筑测试体系.md",
    "第05章-介绍重构名录.md",
]

EXTENSIONS = [
    "extra",            # tables, fenced_code, footnotes, etc.
    "codehilite",       # Pygments-based highlighting
    "toc",
    "sane_lists",
    "pymdownx.tasklist",
    "pymdownx.tilde",
    "pymdownx.betterem",
]

EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False, "css_class": "highlight"},
    "toc": {"permalink": False},
    "pymdownx.tasklist": {"custom_checkbox": True},
}

PYGMENTS_CSS = HtmlFormatter(style="friendly").get_style_defs(".highlight")

PAGE_CSS = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei",
    "Noto Sans CJK SC", "Source Han Sans SC", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.75;
  color: #24292f;
  background: #f6f8fa;
}
.wrap {
  max-width: 900px;
  margin: 0 auto;
  padding: 48px 32px 96px;
  background: #ffffff;
  min-height: 100vh;
  box-shadow: 0 0 24px rgba(0,0,0,0.04);
}
h1, h2, h3, h4 { line-height: 1.3; font-weight: 650; }
h1 {
  font-size: 1.9rem;
  border-bottom: 2px solid #d0d7de;
  padding-bottom: .4em;
  margin-top: 0;
}
h2 {
  font-size: 1.45rem;
  border-bottom: 1px solid #eaecef;
  padding-bottom: .3em;
  margin-top: 2.2em;
}
h3 { font-size: 1.2rem; margin-top: 1.8em; }
h4 { font-size: 1.05rem; margin-top: 1.5em; }
p, li { font-size: 1rem; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
code {
  font-family: "JetBrains Mono", "Fira Code", ui-monospace, SFMono-Regular,
    Menlo, Consolas, monospace;
  font-size: .9em;
  background: rgba(175,184,193,.2);
  padding: .15em .4em;
  border-radius: 6px;
}
pre {
  background: #f6f8fa;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 16px 18px;
  overflow: auto;
  line-height: 1.55;
}
pre code { background: none; padding: 0; font-size: .875rem; }
blockquote {
  margin: 1.2em 0;
  padding: .6em 1.1em;
  color: #57606a;
  border-left: 4px solid #d0d7de;
  background: #f6f8fa;
  border-radius: 0 8px 8px 0;
}
blockquote p { margin: .4em 0; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0;
  font-size: .95rem;
  display: block;
  overflow-x: auto;
}
th, td { border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; vertical-align: top; }
th { background: #f0f3f6; font-weight: 650; }
tr:nth-child(even) td { background: #fafbfc; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 2.4em 0; }
ul.task-list { list-style: none; padding-left: 1.2em; }
.task-list-item { list-style: none; }
.task-list-item input { margin-right: .5em; }
.chapter-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px dashed #d0d7de;
}
.chapter-nav a {
  font-size: .85rem;
  padding: 4px 12px;
  border: 1px solid #d0d7de;
  border-radius: 999px;
  color: #57606a;
}
.chapter-nav a.active { background: #0969da; color: #fff; border-color: #0969da; }
@media (prefers-color-scheme: dark) {
  body { color: #c9d1d9; background: #0d1117; }
  .wrap { background: #0d1117; box-shadow: none; }
  h1 { border-color: #30363d; }
  h2 { border-color: #21262d; }
  a { color: #58a6ff; }
  code { background: rgba(110,118,129,.4); }
  pre, blockquote, th { background: #161b22; }
  pre { border-color: #30363d; }
  th, td { border-color: #30363d; }
  tr:nth-child(even) td { background: #161b22; }
  blockquote { color: #8b949e; border-color: #30363d; }
  .highlight { background: #161b22 !important; }
}
"""

NAV_ITEMS = [
    ("第02章-重构的原则", "第 2 章 · 原则"),
    ("第03章-代码的坏味道", "第 3 章 · 坏味道"),
    ("第04章-构筑测试体系", "第 4 章 · 测试"),
    ("第05章-介绍重构名录", "第 5 章 · 名录"),
]


def build_nav(current_stem: str) -> str:
    links = []
    for stem, label in NAV_ITEMS:
        cls = ' class="active"' if stem == current_stem else ""
        links.append(f'<a href="{stem}.html"{cls}>{label}</a>')
    return '<nav class="chapter-nav">' + "".join(links) + "</nav>"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{page_css}
{pygments_css}
</style>
</head>
<body>
<div class="wrap">
{nav}
{body}
</div>
</body>
</html>
"""


def convert_one(src: Path) -> Path:
    md = markdown.Markdown(extensions=EXTENSIONS, extension_configs=EXTENSION_CONFIGS)
    text = src.read_text(encoding="utf-8")
    body = md.convert(text)
    title = src.stem.replace("-", " · ")
    nav = build_nav(src.stem) if src.stem in dict(NAV_ITEMS) else ""
    html = HTML_TEMPLATE.format(
        title=title,
        page_css=PAGE_CSS,
        pygments_css=PYGMENTS_CSS,
        nav=nav,
        body=body,
    )
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / (src.stem + ".html")
    out.write_text(html, encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    files = argv[1:] if len(argv) > 1 else DEFAULT_FILES
    for name in files:
        src = Path(name)
        if not src.is_absolute():
            src = BASE / src
        if not src.exists():
            print(f"[skip] not found: {src}")
            continue
        out = convert_one(src)
        print(f"[ok] {src.name} -> {out.relative_to(BASE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
