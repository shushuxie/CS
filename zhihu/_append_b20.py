#!/usr/bin/env python3
"""Append staged entries (zhihu/_stage/*.org) to the right category part file."""
import re, datetime
from pathlib import Path

ROOT = Path("/Users/xieshuqiang/Documents/typora/zhihu")
STAGE = ROOT / "_stage"
TODAY = datetime.date.today().isoformat()
LOG = ROOT / "处理日志.org"

MAX_ENTRIES = 50
MAX_LINES = 1000


def latest_part(cat):
    n = 0
    for f in ROOT.glob(f"{cat}-part*.org"):
        m = re.search(r"part(\d+)\.org$", f.name)
        if m:
            n = max(n, int(m.group(1)))
    return max(n, 1)


def stats(p):
    if not p.exists():
        return 0, 0
    text = p.read_text(encoding="utf-8")
    return sum(1 for l in text.split("\n") if l.startswith("* ")), text.count("\n")


def headline(path_text):
    for l in path_text.split("\n"):
        if l.startswith("* "):
            return l[2:].strip()
    return "?"


def strip_head(text):
    """Organize headline: entry starts at the first '* ' line."""
    i = text.find("\n* ")
    return text[i + 1:]


report = []
for f in sorted(STAGE.glob("*.org"), key=lambda p: int(p.stem)):
    raw = f.read_text(encoding="utf-8")
    cat = re.search(r"^#\+CAT:\s*(\S+)", raw, re.M).group(1)
    body = strip_head(raw).strip("\n")
    n = latest_part(cat)
    target = ROOT / f"{cat}-part{n}.org"
    cnt, lines = stats(target)
    incoming = body.count("\n") + 1
    if cnt >= MAX_ENTRIES or lines >= MAX_LINES:
        target = ROOT / f"{cat}-part{n + 1}.org"
        cnt, lines = stats(target)
    with open(target, "a", encoding="utf-8") as fh:
        if fh.tell() > 0 or target.stat().st_size > 0:
            fh.write("\n")
        fh.write(body + "\n")
    report.append((f.stem, cat, target.name, headline(body)))

with open(LOG, "a", encoding="utf-8") as fh:
    for _, cat, name, head in report:
        fh.write(f"[{TODAY}] ✅ {head} → {name}\n")

for r in report:
    print(f"{r[0]:>2} {r[1]} -> {r[2]} | {r[3][:50]}")
