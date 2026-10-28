#!/usr/bin/env python3
"""Fetch one bookmark via Zhihu v4 API, archive as org, print preview.

usage: python3 _b3_fetch.py <idx> <id> <type> <title>
types: answer / article / pin / zvideo
"""
import json, os, re, sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _collect import md_to_org  # noqa: E402

from zhihu_cli.content.handlers.requests import session  # noqa: E402

WORK = os.path.dirname(os.path.abspath(__file__))
ARCHDIR = os.path.join(WORK, "原文")
RAWDIR = "/tmp/b3md"
TODAY = "2026-10-28"
os.makedirs(RAWDIR, exist_ok=True)

try:
    from lxml import html as LH
except Exception:
    LH = None


def inline(el):
    tag = el.tag
    if not isinstance(tag, str):
        return ""
    if tag == "img":
        src = el.get("data-actualsrc") or el.get("data-original") or el.get("src") or ""
        if src.startswith("//"):
            src = "https:" + src
        return f"\n\n![]({src})\n\n" if src else ""
    if tag == "br":
        return "\n"
    if tag in ("strong", "b"):
        return f"**{children(el)}**"
    if tag in ("em", "i"):
        return f"*{children(el)}*"
    if tag == "code":
        return f"`{el.text_content()}`"
    if tag == "a":
        href = el.get("href") or ""
        txt = children(el) or el.get("data-text") or href
        return f"[{txt}]({href})" if href else txt
    if tag == "span" and "ztext-math" in (el.get("class") or ""):
        tex = el.get("data-tex") or el.text_content()
        return f"${tex}$"
    if tag == "sup":
        return f"^{children(el)}"
    if tag == "sub":
        return f"_{children(el)}"
    return children(el)


def children(el):
    out = [el.text or ""]
    for ch in el:
        out.append(block(ch))
        out.append(ch.tail or "")
    return "".join(out)


def block(el):
    tag = el.tag if isinstance(el.tag, str) else ""
    if tag == "p":
        return children(el).strip() + "\n\n"
    if tag in ("h1", "h2", "h3", "h4"):
        lvl = int(tag[1])
        return "#" * min(lvl, 3) + " " + children(el).strip() + "\n\n"
    if tag == "blockquote":
        txt = children(el).strip()
        return "\n".join("> " + l for l in txt.split("\n") if l.strip()) + "\n\n"
    if tag == "pre":
        txt = el.text_content().rstrip()
        lang = ""
        cls = el.get("class") or ""
        m = re.search(r"language-([\w+-]+)", cls)
        if m:
            lang = m.group(1)
        return f"```{lang}\n{txt}\n```\n\n"
    if tag in ("ul", "ol"):
        lines = []
        for i, li in enumerate(el.findall("li"), 1):
            prefix = f"{i}. " if tag == "ol" else "- "
            lines.append(prefix + children(li).strip())
        return "\n".join(lines) + "\n\n"
    if tag == "figure":
        return children(el).strip() + "\n\n"
    if tag == "hr":
        return "\n---\n\n"
    if tag in ("div", "span", "section"):
        return children(el)
    return inline(el)


def html_to_md(h):
    if not h:
        return ""
    if LH is None:
        txt = re.sub(r"<[^>]+>", "", h)
        return re.sub(r"\n{3,}", "\n\n", txt)
    root = LH.fromstring(h)
    md = block(root)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def api_get(url):
    r = session.get(url, skip_app_headers=True)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code} for {url}")
    return r.json()


def fetch(item_id, itype):
    inc = "content,author,voteup_count,created_time,title,question"
    if itype == "answer":
        d = api_get(f"https://www.zhihu.com/api/v4/answers/{item_id}?include={inc}")
        title = (d.get("question") or {}).get("title", "")
    elif itype == "article":
        d = api_get(f"https://www.zhihu.com/api/v4/articles/{item_id}?include={inc}")
        title = d.get("title", "")
    elif itype == "pin":
        d = api_get(f"https://www.zhihu.com/api/v4/pins/{item_id}?include={inc}")
        title = d.get("title") or ""
    else:
        raise RuntimeError("unsupported type " + itype)
    author = (d.get("author") or {}).get("name", "")
    content = d.get("content")
    if isinstance(content, list):
        parts = []
        for b in content:
            t = (b or {}).get("title") or ""
            h = (b or {}).get("content") or (b or {}).get("own_text") or ""
            if t:
                parts.append(f"### {t}")
            parts.append(h)
        content = "\n".join(parts)
    md = html_to_md(content or d.get("excerpt") or "")
    if not title:
        first = next((l.strip() for l in md.split("\n") if l.strip()), "想法")
        title = re.split(r"[|｜]", first)[0].strip()[:30] or "想法"
    return md, author, title


def main():
    idx, item_id, itype = sys.argv[1], sys.argv[2], sys.argv[3]
    title = sys.argv[4] if len(sys.argv) > 4 else ""
    url = sys.argv[5] if len(sys.argv) > 5 else ""
    md, author, real_title = fetch(item_id, itype)
    if not title:
        title = real_title
    rawp = os.path.join(RAWDIR, f"{idx}.md")
    Path(rawp).write_text(f"# {title}\n\n{md}", encoding="utf-8")

    org = md_to_org(md) if md else "(抓不到正文内容)"
    safe = re.sub(r'[\\/*?|"<>]', '_', title)[:40]
    orgname = f"{TODAY}-{safe}.org"
    body = (f"#+TITLE: {title}\n#+LINK: {url}\n#+AUTHOR: {author}\n"
            f"#+TYPE: {itype}\n#+DATE: {TODAY}\n\n{org}\n")
    Path(os.path.join(ARCHDIR, orgname)).write_text(body, encoding="utf-8")

    print(f"TITLE={title}")
    print(f"AUTHOR={author}")
    print(f"ARCHIVE={orgname}")
    print(f"MDLEN={len(md)}")
    heads = [l for l in md.split("\n") if re.match(r"^#{1,3} ", l)]
    print("OUTLINE=" + " | ".join(h.strip() for h in heads[:25]))


if __name__ == "__main__":
    main()
