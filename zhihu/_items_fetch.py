#!/usr/bin/env python3
"""Fetch collection items via /items endpoint (the /contents endpoint now returns empty)."""
import json
import sys

from zhihu_cli.content.handlers.requests import session


def fetch(cid: str, max_items: int | None = None) -> list[dict]:
    url = f"https://www.zhihu.com/api/v4/collections/{cid}/items?offset=0&limit=20"
    out: list[dict] = []
    totals = None
    seen = set()
    while url and url not in seen:
        seen.add(url)
        r = session.get(url)
        if r.status_code != 200:
            print(f"HTTP {r.status_code}: {r.text[:200]}", file=sys.stderr)
            break
        d = r.json()
        totals = d.get("paging", {}).get("totals", totals)
        data = d.get("data", [])
        if not data:
            break
        for it in data:
            c = it.get("content", {})
            ttype = c.get("type", "unknown")
            if ttype == "answer":
                q = c.get("question", {})
                title = q.get("title", "")
                url_ = f"https://www.zhihu.com/question/{q.get('id')}/answer/{c.get('id')}"
            else:
                title = c.get("title", "")
                url_ = c.get("url", "")
            out.append({
                "type": ttype,
                "id": c.get("id"),
                "url": url_,
                "title": title,
                "author_name": (c.get("author") or {}).get("name", ""),
                "voteup_count": c.get("voteup_count", 0),
                "comment_count": c.get("comment_count", 0),
                "collected_at": it.get("created", ""),
            })
            if max_items is not None and len(out) >= max_items:
                return out
        url = d.get("paging", {}).get("next")
        if d.get("paging", {}).get("is_end"):
            break
    if totals is not None and len(out) < totals:
        print(f"API reported {totals} total items but only {len(out)} were returned "
              f"(missing {totals - len(out)})", file=sys.stderr)
    return out


if __name__ == "__main__":
    cid = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else None
    items = fetch(cid, n)
    print(json.dumps(items, ensure_ascii=False, indent=1))
