#!/usr/bin/env python3
"""Fetch collection contents with a plain HTTP client (bypasses broken zse signing)."""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Documents/mcp/zhihu-scraper-mcp/.venv/lib/python3.13/site-packages"))
from zhihu_cli.content.handlers.requests import session as zs  # noqa: E402

COOKIE = zs.headers["cookie"]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


def get(url):
    req = urllib.request.Request(url, headers={"user-agent": UA, "cookie": COOKIE})
    with urllib.request.urlopen(req, timeout=30) as f:
        return json.load(f)


def fetch(cid, want=200):
    url = f"https://www.zhihu.com/api/v4/collections/{cid}/contents?offset=0&limit=20"
    items, seen = [], set()
    total = None
    while url and len(items) < want:
        d = get(url)
        paging = d.get("paging", {})
        if total is None:
            total = paging.get("totals")
        for it in d.get("data", []):
            iid = (it.get("type"), it.get("id"))
            if iid in seen:
                continue
            seen.add(iid)
            ttype = it.get("type")
            title = (it.get("question") or {}).get("title") if ttype == "answer" else it.get("title")
            items.append({
                "type": ttype,
                "id": it.get("id"),
                "title": title or "",
                "url": it.get("url", ""),
                "author": (it.get("author") or {}).get("name", ""),
                "collect_time": it.get("collect_time"),
            })
        url = None if paging.get("is_end") else paging.get("next")
    return total, items


if __name__ == "__main__":
    cid = sys.argv[1]
    want = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    total, items = fetch(cid, want)
    print(json.dumps({"cid": cid, "totals_reported": total, "count": len(items), "items": items},
                     ensure_ascii=False, indent=1))
