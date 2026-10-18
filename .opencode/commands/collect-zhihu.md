---
description: 自动清理知乎收藏夹：取全文→原文归档+主类聚合总结→确认后删除收藏（参数：可选每批条数，默认 20，可传任意条数如 50/100）
---

任务：全自动处理知乎收藏夹——不需要用户粘贴链接。Cookie 已缓存在本机
zhihu CLI 里，直接用 CLI 读取收藏、归档、删收藏。

输入：$ARGUMENTS 可以为空或一个正整数（本批处理条数，无参数默认 20，
条数不设上限）：

   /collect-zhihu        → 一批 20 条（默认）
   /collect-zhihu 10     → 一批 10 条
   /collect-zhihu 50     → 一批 50 条
   /collect-zhihu 100    → 一批 100 条

约定本目录：下文 ZHIHU = ~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu

处理流程：

1. 初始化
   - bash 执行 `date +%Y-%m-%d`，记为 $TODAY。
   - 解析 $ARGUMENTS 里的正整数为 BATCH（没有则 20）；不设上限，
     50 / 100 等任意条数都支持。非数字或非正数时提示后回退 20。

2. 列出收藏夹：
   #+begin_src shell
   $ZHIHU interact collect list --json -n 50
   #+end_src
   - 只有一个收藏夹 → 直接用它，不打扰用户
   - 有多个 → 把各收藏夹的名字和条目数列出，用 question 工具
     问用户处理哪一个（不要自己猜）
   - CLI 报「No headers cached / Cookie 过期 / 风控」时提醒用户：
     浏览器复制 cURL（Copy as cURL）后在终端跑
     `pbpaste | $ZHIHU auth paste`（新版 Chrome 把 cookie 放 -b
     参数，需转成 -H 'Cookie: …' 再喂；批量复制的 cURL 合集解析
     不出 Cookie 时同理），然后重试本步骤。

3. 枚举本批条目：
   #+begin_src shell
   $ZHIHU interact collect view <收藏夹ID> --json --limit 20 -n <BATCH>
   #+end_src
   - 必须显式给 `--limit 20`（每页条数），CLI 才会按页瀑布式翻页，
     从而取满 -n 指定的任意条数（实测 -n 50 可返回 50 条）。
   - 解析提示：CLI 会在 JSON 前先打印一行进度（如
     `Fetching collections for …`），直接 json.load 会失败；
     需跳过首个非 JSON 行（例如从第一个 `[` 起截取）再解析。
     第 2 步的 collect list 同理。
   - 不要把 stderr 丢掉（不要 `2>/dev/null`）：当可列出的条目少于
     收藏夹总数时，CLI 会在 stderr 打印
     `API reported X total items but only Y were returned (missing Z)`；
     把这 Z 条如实记为「不可列出（多为已删除回答）」并在汇报中说明。
   - 若返回条数 < BATCH，按实际条数处理，不报错。
   从 JSON 里取每条的 标题、URL、类型（answer/article/pin），
   向用户展示「本批将处理 N 条」的清单。

4. 逐条流水线（每条做完这四步再进下一条）：
   - BATCH ≥ 30 时自动分片：按每 20~25 条一个子批轮转推进
     （子批内逐条跑 a→b→c，子批做完再进下一子批），避免一次性
     把上百篇原文读进上下文；收尾汇报时仍合并为一个「本批」。

   a. 取全文（同 /summary-zhihu 的规则）：
      - 优先 MCP 工具 get_fulltext（zhihu-scraper），回答要传
        /question/<id>/answer/<id> 完整 URL，专栏传 /p/<id>，
        pin（想法）直接传其 URL
      - 失败/风控：重新完整复述调用一次；仍失败则本条记为
        「⚠️ 需手动粘贴全文」，保留收藏，跳到下一条
      - pin 等无正文的内容：拿得到什么就总结什么，不算失败
      - MCP 不可用时用 CLI 兜底：
        #+begin_src shell
        $ZHIHU browse answer <URL> --json
        $ZHIHU browse article <URL> --json
        #+end_src
        解析 JSON 里 content_md。绝对不要凭链接或想象编造内容。

   a2. 原文归档：把抓到的全文转为 org 语法后存到
       zhihu/原文/<YYYY-MM-DD>-<标题简写>.org。markdown 转 org
       规则：代码段 ```…``` → #+begin_src <lang> / #+end_src；
       引用行 > … → #+begin_quote / #+end_quote；一二三级标题 →
       *、**、*** 大纲；**粗体** → *粗体*；`行内代码` → ~code~；
       ![图](url) → 图单独一行 [[url]]。不改写内容、不压缩，保留
       图片链接。文件头 keywords：
       #+begin_example
       #+TITLE: <标题>
       #+LINK: <URL>
       #+AUTHOR: <作者>
       #+TYPE: answer/article/pin
       #+DATE: $TODAY
       #+end_example
       pin 等抓不到正文的，拿得到多少存多少；全文取失败的条目不做
       此步、也直接进「⚠️ 失败待手动」。

   b. 总结（标准与 /summary-zhihu 第 4 步完全一致）：
      - 摘要+摘录约为原文 20~25%，不刻意压缩
      - 一句话概括：讲什么 + 为什么值得收
      - 分类行：主类六选一（技巧 / 观点 / 科普 / 推荐 / 故事娱乐 /
        个人思考）+ 2~3 个自由主题标签；技巧类步骤完整照录，
        观点类每条论点附原文引用支撑
      - 3~6 段原文摘录，用 #+begin_quote / #+end_quote 包裹；
        代码/快捷键一律 ~code~ 或 #+begin_src，不要出现 markdown 标记
        （反引号、``` 围栏、> 引用前缀都不用）

   c. 写入聚合文件（不按日期分文件）：
      - 依据 b 步选定的主类，追加到 zhihu/<主类>.org 的**文件末尾**
        （技巧 / 观点 / 科普 / 推荐 / 故事娱乐 / 个人思考；先读
        原文件，只增不删）
      - 分卷：目标文件条目数 ≥50（或总行数 ≥1000）时，改写入
        zhihu/<主类>-part2.org；part1 保留旧内容不动，新卷按同样
        规则继续接到 part3
      - 单篇 headline 格式（主题标签放行尾，:主题: 形式，不用 #）：

        * <文章标题>  :<主题1>:<主题2>:
          :PROPERTIES:
          :链接:  <URL>
          :作者:  <作者>
          :原文:  [[file:原文/<归档文件名>.org][本地原文]]
          :抓取:  $TODAY
          :END:

          - 本地原文：[[file:原文/<归档文件名>.org][打开本地归档]]
          - 一句话概括：<…>
          【方法/论点要点】
          - <要点，附原文短引用>（“…”）
          【原文摘录】
          #+begin_quote
          <原文段落>
          #+end_quote
          【我的想法】

        没有本地原文归档的条目省略 :原文: 属性；pin 条目加
        :类型: pin 属性。
      - 每篇写入成功后，在 zhihu/处理日志.org 末尾追加一行流水：
        - ✅ <标题> → <主类>.org ／ ⏸ <标题> → <主类>.org（保留）
          ／ ⚠️ <标题>（失败原因）

   d. 删除收藏（逐条确认）：向用户展示刚写入的标题 + 分类标签 +
      要点，问「确认已归档，删除这条收藏？」。本批条目较多时（如
      ≥10 条），可改为先列出全部清单，再用一次 question 总询问
      「全部确认 / 逐条确认 / 全部保留」，避免逐条打扰：
      - 确认 → 执行：
        #+begin_src shell
        $ZHIHU interact collect remove <条目URL> -c <收藏夹ID>
        #+end_src
        若返回 405 / 404（CLI 已知 bug：回答被解析成复合
        content_id「question/answer」且 DELETE 路径缺内容 id 段），
        改用 venv python 直接调 API（session 自带签名）：
        #+begin_src shell
        ~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/python - <<'EOF'
        from zhihu_cli.content.handlers.requests import session
        cid, item = "<收藏夹ID>", "<内容裸ID>"
        r = session.request(
            "DELETE",
            f"https://www.zhihu.com/api/v4/collections/{cid}/contents/{item}"
            f"?content_id={item}&content_type=<answer|article|pin>")
        print(r.status_code, r.text[:100])
        EOF
        #+end_src
        注意：内容 id 用**裸 id**（回答只用 answer id，不带 question
        id；从 URL /answer/<id> 取）；content_type 用单数：
        answer / article / pin。返回 {"success":true} 即成功。
      - 不确认 / 跳过 → 收藏保留，本条记为「确认保留」。
      - 用户说「本批全部确认 / 后面不用问了」→ 其余条目归档成功
        后直接批量 remove，不再逐条询问。
      - remove 失败：完整重试一次；仍失败记为「归档完成但删除
        失败」，不要重复归档、不要重复写入总结条目。删除的前提是
        「总结已写入 + 原文已归档」两者都完成；无论删没删，都要在
        zhihu/处理日志.org 补上该条的流水行。

5. 收尾汇报，统计三类：
   - ✅ 已归档并删除：N 条
   - ⏸ 确认保留在收藏夹：M 条
   - ⚠️ 失败待手动（全文没抓到 / 删除失败）：K 条
   并给出路径：本批条目落进的聚合文件 zhihu/<主类>.org、原文目录
   zhihu/原文/（本批新存文件名）、日志 zhihu/处理日志.org。
