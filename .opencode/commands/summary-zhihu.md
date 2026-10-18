---
description: 抓取知乎文章总结（分类标签+原文摘录）存档到 zhihu/ 主类聚合文件（参数：链接）
---

任务：总结知乎收藏的文章，存档到笔记仓库的 zhihu/ 目录。

输入：$ARGUMENTS，约定格式（只需要链接，cookie 已配置在本机 zhihu CLI）：

   /summary-zhihu <链接1> [链接2 ...]

处理流程：

1. 解析 $ARGUMENTS：以 http 开头的片段 = 文章链接（可多个，专栏
   zhuanlan.zhihu.com 或回答页均可）。若没有任何链接，只回复使用方法
   （贴下面的 example），不要做其他操作。
   #+begin_example
   /summary-zhihu https://www.zhihu.com/question/N/answer/M
   #+end_example

2. 先用 bash 执行 `date +%Y-%m-%d` 获取今天日期，记为 $TODAY。

3. 对每个知乎链接，用 MCP 工具 get_fulltext（zhihu-scraper）取全文：
   - 传完整正文 URL（回答要带 /question/<id>/answer/<id>，专栏是
     /p/<id>），要点正文就传它，不要只传问题页
   - get_fulltext 返回「> 作者：… | 来源：…」加正文 Markdown，
     直接总结
   - 若提示「单篇获取失败/风控」：优先重新完整复述调用一次；仍失败
     该篇标记「⚠️ 需手动粘贴全文」，继续下一篇
   绝对不要凭链接或想象编造文章内容。
   - 非知乎链接（微信公众号、infoq 等域）改用 webfetch 直接抓。
   - 兜底：MCP 不可用时（见状态提示 needs authentication/failed），
     可用 zhihu CLI 直取：
   #+begin_src shell
   ~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu browse answer <URL> --json
   ~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu browse article <URL> --json
   #+end_src
   解析 JSON 里的 content_md 字段。CLI 报「No headers cached / Cookie
   过期 / 风控」时提醒用户：浏览器复制 cURL（Copy as cURL）后在终端
   跑 `pbpaste | ~/Documents/mcp/zhihu-scraper-mcp/.venv/bin/zhihu auth
   paste`（新版 Chrome 把 cookie 放 -b 参数，需转成 -H 'Cookie: …'
   再喂；批量复制的 cURL 合集解析不出 Cookie 时同理），然后继续。
   - 取到全文后先做**原文归档**：把全文转为 org 语法后存到
     zhihu/原文/<YYYY-MM-DD>-<标题简写>.org（不改写不压缩，保留
     图片链接），markdown 语法按以下规则转 org：
     代码段 ```…``` → #+begin_src <lang> / #+end_src；引用行
     > … → #+begin_quote / #+end_quote；一二三级标题 →
     *、**、*** 大纲；**粗体** → *粗体*；`行内代码` → ~code~；
     ![图](url) → 图单独一行 [[url]]。文件头 keywords：
     #+begin_example
     #+TITLE: <标题>
     #+LINK: <URL>
     #+AUTHOR: <作者>
     #+TYPE: answer/article/pin
     #+DATE: $TODAY
     #+end_example

4. 每篇按「要点+摘录」总结（摘要+摘录总量约为原文 20~25%，
   不要刻意压到只言片语；总结要引用足够的原文，而不是纯转述）：
   - 一句话概括：讲什么 + 为什么值得收藏
   - 分类：主类六选一（技巧 / 观点 / 科普 / 推荐 / 故事娱乐 /
     个人思考），它与主题标签一起写在 headline 行尾（:主题: 形式，
     不用 #）。选主类标准：全文以可执行步骤/操作清单为主 → 技巧；
     以论证、评论、立场为主 → 观点；解释原理/机制 → 科普；安利
     书籍/工具/博主 → 推荐；叙事、段子、图片 → 故事娱乐；作者
     个人经历与感悟 → 个人思考
   - 【方法/论点要点】把论点或步骤展开（通常 3~6 条）：观点类
     每条论点必须附一段原文引用做支撑，不能只靠转述
   - 【原文摘录】3~6 段原文引用，用 org 的 #+begin_quote /
     #+end_quote 块包裹（不要用 markdown 的 > 前缀），选最关键、
     最有味道的段落；若主类是「技巧」，操作步骤（快捷键、参数、
     流程等）必须完整照录、不做压缩——这类收藏的目标是「能照着做」
   - 涉及代码/快捷键一律用 org 标记：行内 ~code~，代码段
     #+begin_src，不要出现 markdown 的反引号或 ``` 围栏
   - 【我的想法】留空，留给用户自己补充

5. 落盘：按第 4 步判定的主类，把单篇追加到聚合文件
   zhihu/<主类>.org 的**文件末尾**（不存在则新建；先读原文件，
   只增不删）。不按日期分文件——日期记在 :抓取: 属性里即可。
   分卷：目标文件条目数 ≥50（或总行数 ≥1000）时改写入
   zhihu/<主类>-part2.org（part1 保留旧内容）。单篇格式：

     * <文章标题>  :<主题1>:<主题2>:
       :PROPERTIES:
       :链接:  <URL>
       :作者:  <作者>
       :原文:  原文/<归档文件名>.org
       :抓取:  $TODAY
       :END:

       - 一句话概括：<…>
       【方法/论点要点】
       - <要点 1，附原文短引用>（“…”）
       - <要点 2>（“…”）
       【原文摘录】
       #+begin_quote
       <原文段落 1>

       <原文段落 2>
       #+end_quote
       【我的想法】

   没有本地原文归档的条目省略 :原文: 属性；pin 条目加 :类型: pin。
   同时在 zhihu/处理日志.org 末尾记一行：日期 + 标题 + 落到哪个
   聚合文件 + 新存的原文文件名。

6. 全部完成后向用户汇报：
   总结了哪几篇、各自落进哪个聚合文件（zhihu/<主类>.org）、原文
   归档到 zhihu/原文/ 的哪几个
   文件、哪几篇失败需要手动补全文。
