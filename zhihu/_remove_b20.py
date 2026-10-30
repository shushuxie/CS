#!/usr/bin/env python3
"""Remove archived+summarized items from the collection, with direct-API fallback."""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path("/Users/xieshuqiang/Documents/typora/zhihu")
ZHIHU = str(Path.home() / "Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu")
PY = str(Path.home() / "Documents/mcp/zhihu-scraper-mcp/.venv/bin/python")
CID = "379223291"

items = json.load(open(ROOT / "_batch_now.json"))["items"][:20]
done = {int(p.stem) for p in (ROOT / "_stage").glob("*.org")}  # 1..20 minus failures

bare = re.compile(r"/(?:p|answer|pin|zvideo)/(\d+)")


def cli_remove(url):
    r = subprocess.run([ZHIHU, "interact", "collect", "remove", url, "-c", CID],
                       capture_output=True, text=True, timeout=90)
    return r.returncode, (r.stdout + r.stderr).strip()[:160]


FALLBACK = """
import sys
from zhihu_cli.content.handlers.requests import session
cid, item, ctype = sys.argv[1], sys.argv[2], sys.argv[3]
r = session.request("DELETE",
    f"https://www.zhihu.com/api/v4/collections/{cid}/contents/{item}"
    f"?content_id={item}&content_type={ctype}")
print(r.status_code, r.text[:100])
"""

results = []
for i, it in enumerate(items, 1):
    if i not in done:
        results.append((i, it["title"], "SKIP(no summary)"))
        continue
    rc, out = cli_remove(it["url"])
    ok = rc == 0 and ("success" in out.lower() or "true" in out.lower() or out == "")
    if not ok:
        m = bare.search(it["url"])
        ctype = it["type"] if it["type"] in ("answer", "article", "pin") else "article"
        r = subprocess.run([PY, "-c", FALLBACK, CID, m.group(1), ctype],
                           capture_output=True, text=True, timeout=90)
        out = (r.stdout + r.stderr).strip()
        ok = "success" in out.lower()
    results.append((i, it["title"], ("OK " if ok else "FAIL ") + out))

for i, t, s in results:
    print(f"{i:02d} {s[:90]} | {t[:34]}")
