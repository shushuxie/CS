#!/usr/bin/env python3
"""Fetch full text for each batch item via zhihu CLI into /tmp/zhihu_batch/."""
import json
import subprocess
from pathlib import Path

ZHIHU = Path.home() / "Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu"
OUT = Path("/tmp/zhihu_batch")
OUT.mkdir(exist_ok=True)
items = json.load(open("/tmp/batch20.json"))

for i, it in enumerate(items, 1):
    dest = OUT / f"{i:02d}.json"
    if dest.exists():
        print(i, "cached")
        continue
    cmd = [str(ZHIHU), "browse", "article" if it["type"] == "article" else "answer",
           it["url"], "--json"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        print(i, "FAIL", it["title"][:30], p.stderr[:200])
        continue
    dest.write_text(p.stdout, encoding="utf-8")
    try:
        d = json.loads(p.stdout)
        md = d.get("content_md", "")
        print(i, "OK", len(md), it["title"][:40])
    except Exception as e:
        print(i, "PARSE_ERR", e, p.stdout[:100])
