#!/usr/bin/env python3
"""Convert /tmp/zh_md/*.md into zhihu/原文/2026-11-01-*.org archives."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "原文"
sys.path.insert(0, str(ROOT))
from _md2org import convert  # noqa: E402

META = [
    ("01", "Excel中多个工作簿（工作表）如何合并为1个工作簿（工作表）？", "雷一鸣",
     "https://zhuanlan.zhihu.com/p/68931729", "article", ""),
    ("02", "Ctrl+H这么好用，为什么我现在才知道！", "蓝婉清",
     "https://zhuanlan.zhihu.com/p/63592250", "article", ""),
    ("03", "色块在PPT中的5种神奇玩法，你都学会了嘛？", "利兄",
     "https://zhuanlan.zhihu.com/p/64815687", "article", ""),
    ("04", "这绝对是PPT里最神的操作", "张博",
     "https://zhuanlan.zhihu.com/p/65827938", "article", ""),
    ("05", "2024年加湿器选购攻略：小米、科西、airX、352 怎么选", "家电人老王",
     "https://zhuanlan.zhihu.com/p/31758742", "article", ""),
]

def fix_bold_lines(text: str) -> str:
    """A standalone **bold** line converts to *text*, which org reads as a headline."""
    fixed = []
    for line in text.splitlines():
        hm = re.match(r"^(\*{1,3} )(.*)$", line)
        if hm and "*" in hm.group(2):
            inner = re.sub(r"\*([^*]+)\*", r"\1", hm.group(2)).strip()
            fixed.append(hm.group(1) + inner)
            continue
        m = re.match(r"^\*([^*].*[^*])\*$", line)
        if m:
            fixed.append(" " + line)     # standalone bold -> paragraph, keep emphasis
        else:
            fixed.append(line)
    return "\n".join(fixed)


out = []
for n, title, author, url, ttype, suffix in META:
    md = Path(f"/tmp/zh_md/{n}.md").read_text(encoding="utf-8")
    body = fix_bold_lines(convert(md))
    safe = re.sub(r'[\\/:*?"<>|\n\r\t]', " ", title)
    safe = re.sub(r"\s+", " ", safe).strip()[:80]
    fname = f"2026-11-01-{safe}.org"
    header = (
        f"#+TITLE: {title}\n"
        f"#+LINK: {url}\n"
        f"#+AUTHOR: {author}\n"
        f"#+TYPE: {ttype}\n"
        f"#+DATE: 2026-11-01\n\n"
    )
    dest = ARCHIVE / fname
    dest.write_text(header + body + "\n", encoding="utf-8")
    out.append({"n": n, "file": fname, "title": title, "author": author,
                "url": url, "chars": len(body)})

json.dump(out, open("/tmp/archives_today.json", "w"), ensure_ascii=False, indent=1)
for r in out:
    print(r["n"], r["chars"], r["file"])
