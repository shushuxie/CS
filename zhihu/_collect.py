#!/usr/bin/env python3
"""
_collect.py — Full orchestrator for /collect-zhihu

Usage:  python3 _collect.py [count] [strategy...]
Example: python3 _collect.py 60 auto
"""

import json, os, re, subprocess, sys, time
from pathlib import Path

# ═══════ CONFIG ═══════
ZHIHU = os.path.expanduser("~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu")
PYBIN = os.path.expanduser("~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/python")
WORK  = "/Users/xieshuqiang/Documents/typora"
STATE_F = f"{WORK}/zhihu/.collect-zhihu.state"
LOG_F   = f"{WORK}/zhihu/处理日志.org"
ARCHDIR = f"{WORK}/zhihu/原文"
CATEGORY_LIST = ["技巧", "观点", "科普", "推荐", "故事娱乐", "个人思考"]

os.makedirs(ARCHDIR, exist_ok=True)

TODAY = __import__("datetime").date.today().isoformat()


# ═══════ UTILS ═══════

def run_zhihu(*args, timeout=120):
    r = subprocess.run([ZHIHU]+list(args), capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr, r.returncode


def parse_json_from_cli(raw):
    """Parse JSON from zhihu CLI, extracting bare arrays or 'items' dicts."""
    idx = raw.find('[')
    if idx < 0:
        # Not a bare array; check if it's a {"items":[...]} wrapper
        data = json.loads(raw)
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        return data
    # Bare array — find proper closing bracket
    end = raw.rfind(']', idx)
    if end < 0: end = len(raw)
    return json.loads(raw[idx:end+1])


def fetch_url_token():
    out, _, _ = run_zhihu("auth", "status")
    m = re.search(r'URL token:\s*(\S+)', out)
    return m.group(1) if m else None


def write_state(cid, title, policy):
    Path(STATE_F).write_text(f"{cid}\n{title}\n{policy}\n", encoding="utf-8")


def write_log(line):
    with open(LOG_F, "a", encoding="utf-8") as f:
        f.write(f"[{TODAY}] {line}\n")


# ═══════ INPUT PARSING ═══════

def parse_input(argv):
    batch = 20
    param_policies = []
    pick_flag = False
    stop_flag = False

    for token in argv:
        try:
            v = int(token)
            if v > 0:
                batch = v
                continue
        except ValueError:
            pass
        low = token.lower()
        if low in ("auto", "全部确认", "删除"): param_policies.append("auto")
        elif low in ("keep", "保留"):           param_policies.append("keep")
        elif low in ("ask", "逐条"):             param_policies.append("ask")
        elif low in ("pick", "重选"):            pick_flag = True
        elif low in ("stop", "停止"):            stop_flag = True
        else: print(f"[WARN] Ignoring unknown token: {token}", file=sys.stderr)

    # Read state
    sid = stitle = spolicy = ""
    if os.path.exists(STATE_F):
        lines = Path(STATE_F).read_text(encoding="utf-8").strip().split("\n")[:3]
        if len(lines) >= 1: sid = lines[0].strip()
        if len(lines) >= 2: stitle = lines[1].strip()
        if len(lines) >= 3: spolicy = lines[2].strip()

    # DEL_POLICY
    del_policy = ""
    for p in param_policies:
        if p in ("auto","keep","ask"): del_policy=p; break
    if not del_policy and spolicy: del_policy = spolicy

    switch_strat = "next"
    if stop_flag: switch_strat = "stop"

    return batch, del_policy, switch_strat, pick_flag, sid, stitle, spolicy


# ═══════ COLLECTIONS ═══════

def list_collections(url_token=None):
    args = ["interact", "collect", "list", "--json", "-n", "100"]
    if url_token: args.extend(["-u", url_token])
    out, err, rc = run_zhihu(*args)
    combined = out + err
    try: return parse_json_from_cli(combined)
    except: return []


# ═══════ FETCH ITEMS ═══════

def fetch_items(cid, limit, batch_size):
    out, err, rc = run_zhihu(
        "interact", "collect", "view", cid,
        "--json", "--limit", str(limit), "-n", str(batch_size))
    missing_note = None
    mm = re.search(r'API reported (\d+) total items but only (\d+) were returned \(missing (\d+)\)', err)
    if mm:
        missing_note = (f"可列出 {mm.group(1)} 条，实际返回 {mm.group(2)} 条，"
                        f"{mm.group(3)} 条不可列出（多为已删除回答）")
    try: data = parse_json_from_cli(out)
    except:
        try: data = parse_json_from_cli(out + err)
        except: return [], missing_note
    return data, missing_note


# ═══════ BROWSE / FETCH CONTENT ═══════

def browse_item(url, itype):
    sub_map = {"answer":"answer", "article":"article"}
    if itype in sub_map: sub = sub_map[itype]
    elif "/answer/" in url: sub = "answer"
    elif "/p/" in url or "/article/" in url: sub = "article"
    else: sub = "pin"

    md = ""; author = ""
    for attempt in range(2):
        out, err, rc = run_zhihu("browse", sub, url, "--json", timeout=120)
        if rc != 0:
            if attempt == 0: continue
            break
        txt = out if out.strip() else err
        if '[' in txt:
            try:
                data = parse_json_from_cli(txt)
                if isinstance(data, dict):
                    md = data.get("content_md", "") or data.get("content", "") or ""
                    author = data.get("author_name", "") or ""
                    tgt = data.get("target", {})
                    if not author:
                        author = (tgt.get("author",{}) or {}).get("name","")
                else:
                    md = str(data)
            except:
                if attempt == 0: continue
                break
        else:
            if attempt == 0: continue
            break
    return md, author


# ═══════ MD→ORG ═══════

def md_to_org(md):
    lines = md.split("\n")
    out = []; in_code = in_quote = False
    for line in lines:
        s = line.rstrip()
        stripped = s.strip()
        if stripped.startswith("```"):
            if in_code: out.append("#+end_src"); in_code=False
            else: out.append(f"#+begin_src {stripped[3:].strip() or 'text'}"); in_code=True
            continue
        if stripped.startswith("> ") and not in_code:
            if not in_quote: out.append("#+begin_quote"); in_quote=True
            out.append(stripped[2:])
            continue
        if in_quote and not stripped.startswith(">"):
            out.append("#+end_quote"); in_quote=False
        if in_code: out.append(s); continue
        hm = re.match(r'^(#{1,3})\s+(.*)', stripped)
        if hm: out.append("*"*len(hm.group(1))+" "+hm.group(2)); continue
        nl = re.sub(r'\*\*(.+?)\*\*', r'*\1*', stripped)
        nl = re.sub(r'`([^`]+)`', r'~\1~', nl)
        imgs = re.findall(r'!\[.*?\]\((.*?)\)', nl)
        for img in imgs: out.append(img)
        nl = re.sub(r'!\[.*?\]\([^)]+\)', '', nl)
        out.append(nl)
    if in_code: out.append("#+end_src")
    if in_quote: out.append("#+end_quote")
    return "\n".join(out)


# ═══════ ARCHIVE ═══════

def save_archive(title, url, author, itype, md, archdir):
    safe = re.sub(r'[\\/*?|"<>]', '_', title)[:40]
    fname = f"{TODAY}-{safe}.org"
    path = os.path.join(archdir, fname)
    org = f"#+TITLE: {title}\n#+LINK: {url}\n#+AUTHOR: {author}\n#+TYPE: {itype}\n#+DATE: {TODAY}\n\n"
    org += md if md else "(抓不到正文内容)"
    Path(path).write_text(org, encoding="utf-8")
    return fname


# ═══════ CLASSIFY & SUMMARIZE ═══════

def classify_and_summarize(md, title, itype):
    res = {"main_cat":"个人思考","sub_cats":[],"one_sentence":"",
           "points":[],"quotes":[]}

    if not md:
        res["one_sentence"] = f"{title}（抓不到正文）"; return res

    lower = md.lower()+" "+title.lower()

    patterns = {
        "技巧":   ["教程","步骤","如何","方法","工具","代码","安装","配置","使用",
                   "实现","技巧","操作","command","api","pip","npm","函数","class",
                   "搭建","setup","install","git","docker","nginx","database","sql",
                   "request","post","get","header","middleware","hook","react","vue"],
        "观点":   ["观点","看法","认为","分析","本质","深层原因","为什么","底层逻辑",
                   "趋势","未来","判断","评价","如何看待","社会","文化","经济","政治",
                   "建议","应该","人生","价值","意义"],
        "科普":   ["科学","原理","机制","物理","化学","生物","量子","分子","细胞",
                   "基因","进化","宇宙","数学","定理","解释","事实","数据","实验",
                   "研究","频率","波长","原子","蛋白质","DNA","气候","气象","算法",
                   "复杂度","空间","时间","概率","统计"],
        "推荐":   ["推荐","好书","电影","游戏","产品","app","软件","安利","好物",
                   "清单","合集","排名","榜单","评测","体验","对比","比较","性价比",
                   "值得买","入手","评分","排行榜"],
    }

    scores = {}
    for cat, words in patterns.items():
        c = sum(1 for w in words if w.lower() in lower)
        if c > 0: scores[cat] = c

    # Boost code-heavy content
    if md.count("```")>=2 or md.count("`")>=6:
        scores["技巧"] = scores.get("技巧",0)+3

    cat_sorted = sorted(scores.items(), key=lambda x:-x[1])
    if cat_sorted:
        res["main_cat"] = cat_sorted[0][0]
        res["sub_cats"] = [c for c,_ in cat_sorted[1:3]]

    # Extract quotes (top paragraphs by length)
    paras = [p.strip() for p in md.split("\n\n") if len(p.strip())>20]
    paras.sort(key=len, reverse=True)

    # Points from bullet lines
    bullets = [l.strip().lstrip("-*•▸①②③").strip()
               for l in md.split("\n")
               if re.match(r"^[-*•▸①②③\s]", l) and len(l.strip())>5]
    res["points"] = bullets[:6] if bullets else [p for p in paras[:3] if len(p)>30]
    res["quotes"] = [p for p in paras[:5] if p not in res["points"]]

    meaningful = [p for p in paras if len(p)>30][:1]
    snippet = meaningful[0][:100] if meaningful else ""
    res["one_sentence"] = f"{title}——{snippet}" if snippet else title
    return res


# ═══════ AGGREGATE FILE MANAGEMENT ═══════

def find_latest_part(cat):
    files = sorted(Path(f"{WORK}/zhihu").glob(f"{cat}-part*.org"))
    n = 0
    for f in files:
        m = re.search(r"part(\d+)\.org$", f.name)
        if m: n = max(n, int(m.group(1)))
    return max(n, 1)


def count_entries(filepath):
    if not Path(filepath).exists(): return 0
    cnt = sum(1 for l in Path(filepath).read_text(encoding="utf-8").split("\n")
              if re.match(r'^\* ', l))
    return cnt


def build_entry(item, summary, archive_fname, itype):
    cat = summary["main_cat"]
    subs = ":".join(summary["sub_cats"]) if summary["sub_cats"] else cat
    # Get author from either flat or nested structure
    author = item.get("author_name","") or item.get("author",{}).get("name","")
    title = item.get("title","") if "title" in item else (item.get("target",{}).get("title",""))

    props = [f":PROPERTIES:", f":链接:  {item['url']}", f":作者:  {author}"]
    if archive_fname:
        props.append(f":原文:  [[file:原文/{archive_fname}][打开本地归档]]")
    props.append(f":抓取:  {TODAY}")
    if itype == "pin": props.append(":类型: pin")
    props.append(":END:")

    body = [f"- 一句话概括：{summary['one_sentence']}"]
    if summary["points"]:
        body.append("【方法/论点要点】")
        for pt in summary["points"][:5]:
            body.append(f"- {pt}")
    if summary["quotes"]:
        body.append("【原文摘录】")
        body.append("#+begin_quote")
        for q in summary["quotes"][:4]:
            body.append(q)
        body.append("#+end_quote")
    body.append("【我的想法】")

    headline = f"* {title}  :{subs}:"
    return '\n'.join([headline]+props+body)


def append_to_category(cat, entry_text):
    n = find_latest_part(cat)
    filepath = Path(f"{WORK}/zhihu/{cat}-part{n}.org")
    while count_entries(str(filepath)) >= 50:
        n += 1
        filepath = Path(f"{WORK}/zhihu/{cat}-part{n}.org")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write('\n\n' + entry_text + '\n\n')
    return filepath.name


# ═══════ DELETE BOOKMARK ═══════

def extract_bare_id(url, itype):
    bare = url.rstrip("/")
    if itype == "answer":
        m = re.search(r"/answer/([\w-]+)$", bare)
        return m.group(1) if m else bare.split("/")[-1]
    elif itype == "article":
        m = re.search(r"/p/([\w-]+)$", bare)
        return m.group(1) if m else bare.split("/")[-1]
    else:
        return bare.split("/")[-1]


def delete_bookmark(bare_id, cid, itype):
    ct_map = {"answer":"answer","article":"article","pin":"pin"}
    ct = ct_map.get(itype, "answer")

    py_script = (
        'from zhihu_cli.content.handlers.requests import session\n'
        'r = session.request(\n'
        '    "DELETE",\n'
        f'    "https://www.zhihu.com/api/v4/collections/{cid}/contents/{{bare_id}}"\n'
        f'    "?content_id={{bare_id}}&content_type={ct}")\n'
        'print(r.status_code, r.text[:100])\n'
    ).format(bare_id=bare_id)

    for attempt in range(2):
        r = subprocess.run([PYBIN,"-c",py_script],
                           capture_output=True, text=True, timeout=30)
        if "success" in r.stdout.lower() or r.returncode == 0:
            return True
        if attempt == 0: time.sleep(0.6)
    return False


# ═══════ MAIN ═══════

def main():
    BATCH, DEL_POLICY, SWITCH_STRAT, PICK_FLAG, S_ID, S_TITLE, S_POLICY = parse_input(sys.argv[1:])

    url_token = fetch_url_token()
    collections = list_collections(url_token)

    if not collections:
        print("❌ 无法获取收藏夹列表，请检查 Cookie。")
        write_log("全部收藏夹已空，终止批次"); print("RESULT: deleted=0 kept=0 failed=0 folder= policy=unknown"); return

    # Pick collection
    CID = CTITLE = CCOUNT = None
    switch_msg = ""

    if PICK_FLAG:
        # Will need to ask
        cid_needed = True
    elif S_ID:
        found = False
        for c in collections:
            if c.get("id")==S_ID and c.get("answer_count",0)>0:
                CID=c["id"]; CTITLE=c["title"]; CCOUNT=c["answer_count"]; found=True; break
        if not found:
            cid_needed = True
            switch_msg = f"默认夹「{S_TITLE or S_ID}」已清空 → "
    else:
        cid_needed = True

    if not CID and cid_needed:
        if SWITCH_STRAT == "stop":
            print("所有收藏夹已清空，终止。"); print("RESULT: deleted=0 kept=0 failed=0 folder= policy=none"); return
        best = max(collections, key=lambda c:c.get("answer_count",0))
        if best.get("answer_count",0)>0:
            CID=best["id"]; CTITLE=best["title"]; CCOUNT=best["answer_count"]
        else:
            print("全部收藏夹均已处理完毕"); print("RESULT: deleted=0 kept=0 failed=0 folder= policy=none"); return

    if CID and not switch_msg:
        for c in collections:
            if c.get("id")==CID: CTITLE=c["title"]; CCOUNT=c.get("answer_count",0); break
    if CID:
        switch_msg = switch_msg or f"自动选择最大收藏夹「{CTITLE}」({CID}, {CCOUNT} 条)"

    print(f"本批计划：收藏夹={CTITLE or '?'}({CID})｜删除策略={DEL_POLICY or '待定'}｜夹空策略={SWITCH_STRAT}｜预计 ≤{BATCH} 条")
    if switch_msg: print(switch_msg)

    items, missing_note = fetch_items(CID, 20, BATCH)
    if not items:
        # State collection is empty/unviewable → auto-switch to next largest
        switch_msg = f"默认夹「{CTITLE}」({CID}) 无可用条目 → "
        best = max((c for c in collections if c.get("id")!=CID),
                   key=lambda c:c.get("answer_count",0), default=None)
        if best and best.get("answer_count",0)>0:
            CID=best["id"]; CTITLE=best["title"]; CCOUNT=best["answer_count"]
            switch_msg += f"自动切换到「{CTITLE}」({CID}, {CCOUNT} 条)"
            print(f"本批计划：收藏夹={CTITLE}({CID})｜删除策略={DEL_POLICY or '待定'}｜夹空策略={SWITCH_STRAT}｜预计 ≤{BATCH} 条")
            print(switch_msg)
            items, missing_note = fetch_items(CID, 20, BATCH)
            if not items:
                # Still empty after switch
                print("所有已选收藏夹均已无可用条目，终止。")
                write_log("全部收藏夹无可用条目，终止批次")
                print(f"RESULT: deleted=0 kept=0 failed=0 folder={CID} policy={DEL_POLICY or 'none'}")
                return
        else:
            print("所有收藏夹均已无可用条目，终止。")
            write_log("全部收藏夹无可用条目，终止批次")
            print(f"RESULT: deleted=0 kept=0 failed=0 folder={CID} policy={DEL_POLICY or 'none'}")
            return

    print(f"\n===== 本批将处理 {len(items)} 条 =====")
    for i,it in enumerate(items,1):
        # collect view returns flat items (not wrapped in target)
        if "target" in it:
            tgt=it["target"]; tp=it.get("target_type","pin")
            title=tgt.get("title",""); url=tgt.get("url","")
        else:
            tgt={}; title=it.get("title","无标题"); url=it.get("url","")
            tp=it.get("type","pin")
        print(f"  {i}. [{tp}] {title} ({url})")

    shard_size = 25
    all_deleted=[]; all_kept=[]; all_failed=[]; confirm_rows=[]

    for si in range(0, len(items), shard_size):
        sj = min(si+shard_size, len(items))
        if shard_size>20:
            sn = si//shard_size+1; tn = (len(items)+shard_size-1)//shard_size
            print(f"\n--- 子批 {sn}/{tn}（第 {si+1}-{sj} 条）---")
        for ii in range(si, sj):
            idx = ii+1
            item = items[ii]
            # collect view returns flat items (not wrapped in target)
            if "target" in item:
                tgt=item["target"]; itype=item.get("target_type","pin")
                title=tgt.get("title","无标题"); url=tgt.get("url","")
            else:
                itype=item.get("type","pin")
                title=item.get("title","无标题"); url=item.get("url","")
                tgt={}

            print(f"\n[{idx}/{len(items)}] {itype}: {title}")

            # a. Fetch
            md, author = browse_item(url, itype)
            if not md and itype in ("answer","article"):
                print(f"  ⚠️ 全文抓取失败 → 保留收藏"); all_failed.append(title)
                write_log(f"⚠️ {title}（全文抓取失败）")
                confirm_rows.append({"t":title,"cat":"待分类","s":"failed"})
                continue
            if not author: author = ""

            # a2. Archive
            archive_fname = None
            try:
                archive_fname = save_archive(title, url, author, itype, md, ARCHDIR)
                print(f"  ✓ 已归档为 {archive_fname}")
            except Exception as e:
                print(f"  ⚠️ 归档失败: {e}"); all_failed.append(title)
                write_log(f"⚠️ {title}（归档失败）"); continue

            # b. Classify
            summary = classify_and_summarize(md, title, itype)
            print(f"  📂 {summary['main_cat']} ({summary['sub_cats']})")

            # c. Aggregate
            try:
                entry = build_entry(item, summary, archive_fname, itype)
                pname = append_to_category(summary["main_cat"], entry)
                print(f"  ✓ 已追加到 zhihu/{pname}")
            except Exception as e:
                print(f"  ⚠️ 聚合写入失败: {e}"); all_failed.append(title)
                write_log(f"⚠️ {title}（聚合写入失败: {e}）"); continue

            # d. Delete per policy
            bare_id = extract_bare_id(url, itype)
            cat_label = summary["main_cat"]

            if DEL_POLICY == "keep":
                all_kept.append(title); write_log(f"⏸ {title} → {cat_label}（保留）")
                confirm_rows.append({"t":title,"cat":cat_label,"s":"kept"}); continue

            if DEL_POLICY == "auto":
                ok = delete_bookmark(bare_id, CID, itype)
                if ok: all_deleted.append(title); write_log(f"✅ {title} → {cat_label}")
                else: all_failed.append(title); write_log(f"⚠️ {title}（删除失败）")
                confirm_rows.append({"t":title,"cat":cat_label,"s":"done"})
                continue

            if DEL_POLICY == "ask":
                confirm_rows.append({"t":title,"cat":cat_label,"subs":summary["sub_cats"],
                                     "bid":bare_id,"cid":CID,"tp":itype,"s":"pending"}); continue

            # fallback
            ok = delete_bookmark(bare_id, CID, itype)
            if ok: all_deleted.append(title); write_log(f"✅ {title} → {cat_label}")
            else: all_failed.append(title); write_log(f"⚠️ {title}（删除失败）")

    # Handle pending ask confirmations
    pending = [c for c in confirm_rows if c.get("s")=="pending"]
    if pending:
        print("\n===ASK_CONFIRMATION===")
        for c in pending:
            subs = ":".join(c.get("subs",[]))
            print(f"- {c['t']}  :{c['cat']}:{subs}:")
        print(f"PENDING={len(pending)}")
        print("===END_ASK===")
        for c in pending:
            ok = delete_bookmark(c["bid"], c["cid"], c["tp"])
            if ok: all_deleted.append(c["t"]); write_log(f"✅ {c['t']} → {c['cat']}（确认后删除）")
            else: all_failed.append(c["t"]); write_log(f"⚠️ {c['t']}（删除失败）")

    # Write state
    write_state(CID, CTITLE, DEL_POLICY)

    # Report
    print(f"\n{'='*50}")
    print(f"✅ 已归档并删除: {len(all_deleted)} 条")
    print(f"⏸ 确认保留:     {len(all_kept)} 条")
    print(f"⚠️ 失败待手动:    {len(all_failed)} 条")
    if missing_note: print(f"📎 {missing_note}")
    cats_used = set(c["cat"] for c in confirm_rows if c.get("cat"))
    print(f"落盘文件: {', '.join(f'zhihu/{c}' for c in sorted(cats_used))}")
    new_archives = [f for f in os.listdir(ARCHDIR) if f.startswith(TODAY+"-")]
    if new_archives:
        shown = ", ".join(new_archives[:10])
        extra = "... (+%d)"%(len(new_archives)-10) if len(new_archives)>10 else ""
        print(f"新存原文: {shown}{extra}")

    policy_display = DEL_POLICY or "none"
    print(f"RESULT: deleted={len(all_deleted)} kept={len(all_kept)} failed={len(all_failed)} folder={CID} policy={policy_display}")


if __name__ == "__main__":
    main()
