#!/usr/bin/env python3
"""Fetch full text for a batch of items into /tmp/zhihu_b20/<n>.json (parallel)."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ZHIHU = str(Path.home() / "Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu")
OUT = Path("/tmp/zhihu_b20")
OUT.mkdir(exist_ok=True)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20

batch = json.load(open("/Users/xieshuqiang/Documents/typora/zhihu/_batch_now.json"))["items"][:N]


def sub_of(it):
    t = it["type"]
    if t in ("answer", "article"):
        return t
    if "/answer/" in it["url"]:
        return "answer"
    if "/p/" in it["url"] or "/article/" in it["url"]:
        return "article"
    return "pin"


def one(args):
    i, it = args
    for attempt in (1, 2):
        r = subprocess.run([ZHIHU, "browse", sub_of(it), it["url"], "--json"],
                           capture_output=True, text=True, timeout=180)
        txt = r.stdout if r.stdout.strip() else r.stderr
        idx = txt.find("{")
        if idx >= 0:
            try:
                d = json.loads(txt[idx:txt.rfind("}") + 1])
                md = d.get("content_md") or ""
                if md:
                    (OUT / f"{i:02d}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
                    title = it["title"]
                    author = d.get("author_name") or ((d.get("metadata") or {}).get("author") or {}).get("name") or it.get("author") or ""
                    return (i, it["title"], len(md), author)
            except Exception as e:
                pass
    return (i, it["title"], 0, "")


with ThreadPoolExecutor(max_workers=5) as ex:
    res = list(ex.map(one, list(enumerate(batch, 1))))

for i, title, n, author in res:
    print(f"{i:02d} {'OK ' if n else 'FAIL'} {n:6d} {title[:44]}")
