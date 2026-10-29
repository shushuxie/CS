#!/usr/bin/env python3
"""Convert fetched zhihu markdown into an org archive file under zhihu/原文/."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "原文"


def inline(text: str) -> str:
    # images on their own line -> bare link
    text = re.sub(r"!\[[^\]]*\]\(([^)]+)\)", lambda m: f"\n[[{m.group(1)}]]\n", text)
    # markdown links -> org links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f"[[{m.group(2)}][{m.group(1)}]]", text)
    # bold -> org bold (avoid touching list bullets)
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"*\1*", text)
    # inline code
    text = re.sub(r"`([^`]+)`", r"~\1~", text)
    return text


def convert(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_code = False
    in_quote = False
    for raw in lines:
        line = raw.rstrip()
        stripped = line.lstrip()

        # code fence
        m = re.match(r"^\s*```(\w*)", line)
        if m:
            if not in_code:
                if in_quote:
                    out.append("#+end_quote")
                    in_quote = False
                out.append(f"#+begin_src {m.group(1) or 'text'}")
                in_code = True
            else:
                out.append("#+end_src")
                in_code = False
            continue
        if in_code:
            out.append(raw)
            continue

        # blockquote
        if stripped.startswith(">"):
            body = stripped.lstrip(">").strip()
            if not in_quote:
                out.append("#+begin_quote")
                in_quote = True
            out.append(inline(body))
            continue
        if in_quote:
            out.append("#+end_quote")
            in_quote = False

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = min(len(m.group(1)), 3)
            out.append("*" * level + " " + inline(m.group(2).strip()))
            continue

        # hr
        if re.match(r"^\s*([-*_])\s*\1\s*\1[\s\-*_]*$", line):
            out.append("-----")
            continue

        out.append(inline(line))

    if in_quote:
        out.append("#+end_quote")
    if in_code:
        out.append("#+end_src")
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    batch = json.load(open("/tmp/batch20.json"))
    ARCHIVE.mkdir(exist_ok=True)
    results = []
    for i, it in enumerate(batch, 1):
        src = Path(f"/tmp/zhihu_batch/{i:02d}.json")
        title = it["title"].strip()
        safe = re.sub(r'[\\/:*?"<>|\n\r\t]', " ", title)
        safe = re.sub(r"\s+", " ", safe).strip()[:80]
        fname = f"2026-10-29-{safe}.org"
        if i == 1:
            md = ("我认为国足的表现也是辱华的一种 把他们也一起封杀了")
            author = it.get("author") or "旧城"
        else:
            if not src.exists():
                print(i, "MISSING", title[:30])
                continue
            d = json.loads(src.read_text(encoding="utf-8"))
            md = d.get("content_md", "")
            meta = d.get("metadata", {}) or {}
            author = (meta.get("author") or {}).get("name") or it.get("author") or ""
            if not title:
                title = meta.get("title", "")
        body = convert(md)
        header = (
            f"#+TITLE: {title}\n"
            f"#+LINK: {it['url']}\n"
            f"#+AUTHOR: {author}\n"
            f"#+TYPE: {it['type']}\n"
            f"#+DATE: 2026-10-29\n\n"
        )
        dest = ARCHIVE / fname
        dest.write_text(header + body + "\n", encoding="utf-8")
        results.append({"n": i, "file": fname, "author": author, "chars": len(body)})
    json.dump(results, open("/tmp/archives.json", "w"), ensure_ascii=False, indent=1)
    for r in results:
        print(r["n"], r["chars"], r["file"])


if __name__ == "__main__":
    main()
