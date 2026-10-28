#!/usr/bin/env python3
"""Append one entry (read from /tmp/b3entry.txt) to its category file,
write the log line, and delete the bookmark.

usage: python3 _b3_put.py <idx> <cat> <cid> <item_id> <type> <title>
"""
import os, re, subprocess, sys
from pathlib import Path

WORK = os.path.dirname(os.path.abspath(__file__))
LOG_F = os.path.join(WORK, "处理日志.org")
TODAY = "2026-10-28"
PYBIN = os.path.expanduser("~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/python")
ENTRY = "/tmp/b3entry.txt"


def find_latest_part(cat):
    n = 0
    for f in Path(WORK).glob(f"{cat}-part*.org"):
        m = re.search(r"part(\d+)\.org$", f.name)
        if m:
            n = max(n, int(m.group(1)))
    return max(n, 1)


def count_entries(p):
    if not Path(p).exists():
        return 0
    return sum(1 for l in Path(p).read_text(encoding="utf-8").split("\n")
               if re.match(r"^\* ", l))


def nlines(p):
    if not Path(p).exists():
        return 0
    return len(Path(p).read_text(encoding="utf-8").split("\n"))


def append(cat, text):
    n = find_latest_part(cat)
    p = Path(WORK) / f"{cat}-part{n}.org"
    while count_entries(p) >= 50 or nlines(p) >= 1000:
        n += 1
        p = Path(WORK) / f"{cat}-part{n}.org"
    with open(p, "a", encoding="utf-8") as f:
        f.write("\n\n" + text.strip() + "\n\n")
    return p.name


def log(line):
    with open(LOG_F, "a", encoding="utf-8") as f:
        f.write(f"[{TODAY}] {line}\n")


def delete(cid, item_id, itype):
    ct = {"answer": "answer", "article": "article", "pin": "pin"}.get(itype, itype)
    script = f'''
from zhihu_cli.content.handlers.requests import session
r = session.request("DELETE",
    "https://www.zhihu.com/api/v4/collections/{cid}/contents/{item_id}"
    "?content_id={item_id}&content_type={ct}", skip_app_headers=True)
print(r.status_code, r.text[:120])
'''
    for attempt in range(2):
        try:
            r = subprocess.run([PYBIN, "-c", script], capture_output=True, text=True, timeout=30)
        except subprocess.TimeoutExpired:
            return False, "timeout"
        out = (r.stdout + r.stderr).strip()
        if "success" in out.lower():
            return True, out
    return False, out


def main():
    idx, cat, cid, item_id, itype, title = sys.argv[1:7]
    text = Path(ENTRY).read_text(encoding="utf-8")
    pname = append(cat, text)
    print(f"APPENDED → {cat}/{pname}")
    ok, out = delete(cid, item_id, itype)
    if ok:
        log(f"✅ {title} → {pname}")
        print("DELETED ok")
    else:
        log(f"⚠️ {title} → {pname}（删除失败: {out}）")
        print("DELETE FAILED:", out)


if __name__ == "__main__":
    main()
