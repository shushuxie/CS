#!/usr/bin/env python3
"""Delete batch items from their collections via the signed session workaround."""
import json
import re
import sys
import time

sys.path.insert(0, "/Users/xieshuqiang/Documents/mcp/zhihu-scraper-mcp/.venv/lib/python3.13/site-packages")
from zhihu_cli.content.handlers.requests import session  # noqa: E402

batch = json.load(open("/tmp/batch20.json"))
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else len(batch)

for i, it in enumerate(batch, 1):
    if i < start or i > end:
        continue
    url, cid = it["url"], it["folder"]
    if "/answer/" in url:
        item, ctype = re.search(r"/answer/(\d+)", url).group(1), "answer"
    elif "/p/" in url:
        item, ctype = re.search(r"/p/(\d+)", url).group(1), "article"
    elif "/pin/" in url:
        item, ctype = re.search(r"/pin/(\d+)", url).group(1), "pin"
    else:
        print(i, "SKIP unknown url", url)
        continue
    u = (f"https://www.zhihu.com/api/v4/collections/{cid}/contents/{item}"
         f"?content_id={item}&content_type={ctype}")
    try:
        r = session.request("DELETE", u)
        ok = r.status_code == 200
        print(i, "OK" if ok else "FAIL", r.status_code, r.text[:80].replace("\n", " "), it["title"][:30])
    except Exception as e:
        print(i, "ERR", e, it["title"][:30])
    time.sleep(0.8)
