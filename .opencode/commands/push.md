---
description: 将当前 opencode 工作目录（须为 git 仓库）的全部改动一键提交并推送到远端
agent: build
---

任务：把当前 opencode 工作目录里的**全部改动**提交并推送到 GitHub。
`$ARGUMENTS` 可选，作为 commit 说明；为空时自动生成。

流程：

1. 判定工作目录是否属于 git 仓库：
   `git rev-parse --show-toplevel`
   - 失败（fatal: not a git repository）→ 回复「当前目录不是 git 仓库，已跳过」并结束。
   - 成功 → 记下仓库根目录；后续所有 git 命令只在该仓库内执行。

2. 查看改动：`git status -s`
   - 无改动 → 回复「没有需要提交的改动」，结束。

3. 暂存全部改动：`git add -A`（含未跟踪文件；已被 .gitignore 忽略的文件不会进来）。

4. 提交：
   - `$ARGUMENTS` 非空 → `git commit -m "$ARGUMENTS"`。
   - 为空 → 根据 `git diff --cached --stat` 生成**一句简短中文说明**；实在判断不了就用
     `git commit -m "update $(date +%Y-%m-%d)"`。
   - commit 失败要如实报告，不得伪造。

5. 推送：
   - 判断上游：`git rev-parse --abbrev-ref --symbolic-full-name @{u}`
     - 无上游 → `git push -u origin <当前分支>`
     - 有上游 → `git push`
   - 失败则 `sleep 3` **完整重试一次**；仍失败如实报错，不改写远端历史、不做第三次。

6. 收尾报告：仓库根目录、分支、commit 短哈希+说明、推送结果。
