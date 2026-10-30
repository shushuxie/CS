#!/usr/bin/env python3
"""Build zhihu/原文/*.org archives from /tmp/zhihu_b20/*.json and print a manifest."""
import json, re, datetime
from pathlib import Path

ROOT = Path("/Users/xieshuqiang/Documents/typora/zhihu")
ARCH = ROOT / "原文"
ARCH.mkdir(exist_ok=True)
TODAY = datetime.date.today().isoformat()

batch = json.load(open(ROOT / "_batch_now.json"))["items"][:20]
import importlib.util
spec = importlib.util.spec_from_file_location("m", ROOT / "_md2org.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

manifest = []
for i, it in enumerate(batch, 1):
    src = Path(f"/tmp/zhihu_b20/{i:02d}.json")
    if not src.exists():
        print(i, "SKIP(no text)", it["title"][:40]); continue
    d = json.loads(src.read_text(encoding="utf-8"))
    md = d.get("content_md") or ""
    meta = d.get("metadata") or {}
    author = (meta.get("author") or {}).get("name") or it.get("author") or ""
    title = it["title"].strip()
    safe = re.sub(r'[\\/:*?"<>|\n\r\t]', " ", title)
    safe = re.sub(r"\s+", " ", safe).strip()[:40]
    fname = f"{TODAY}-{safe}.org"
    body = m.convert(md)
    header = (f"#+TITLE: {title}\n#+LINK: {it['url']}\n#+AUTHOR: {author}\n"
              f"#+TYPE: {it['type']}\n#+DATE: {TODAY}\n\n")
    (ARCH / fname).write_text(header + body + "\n", encoding="utf-8")
    manifest.append({"n": i, "file": fname, "title": title, "author": author,
                     "type": it["type"], "url": it["url"], "chars": len(body)})

json.dump(manifest, open("/tmp/archives20.json", "w"), ensure_ascii=False, indent=1)
for r in manifest:
    print(r["n"], r["chars"], r["author"], "|", r["file"])
