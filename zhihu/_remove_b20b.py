#!/usr/bin/env python3
"""Remove archived+summarized items from collection 379223291 (working API form)."""
import json, re
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / "Documents/mcp/zhihu-scraper-mcp/.venv/lib/python3.13/site-packages"))
from zhihu_cli.content.handlers.requests import session

ROOT = Path("/Users/xieshuqiang/Documents/typora/zhihu")
CID = "379223291"
items = json.load(open(ROOT / "_batch_now.json"))["items"][:20]
done = {int(p.stem) for p in (ROOT / "_stage").glob("*.org")}
bare = re.compile(r"/(?:p|answer|pin|zvideo)/(\d+)")

for i, it in enumerate(items, 1):
    if i not in done:
        print(f"{i:02d} SKIP(no content) | {it['title'][:34]}")
        continue
    item = bare.search(it["url"]).group(1)
    ctype = it["type"] if it["type"] in ("answer", "article", "pin") else "article"
    url = f"https://www.zhihu.com/api/v4/collections/{CID}/contents/{item}?content_type={ctype}"
    r = session.request("DELETE", url)
    ok = '"success":true' in r.text.replace(" ", "")
    if not ok:
        r = session.request("DELETE", url)  # one retry
        ok = '"success":true' in r.text.replace(" ", "")
    print(f"{i:02d} {'OK  ' if ok else 'FAIL'} {r.status_code} {r.text[:60].strip()} | {it['title'][:30]}")
