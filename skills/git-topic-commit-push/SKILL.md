---
name: git-topic-commit-push
description: Create one or more Git commits grouped by coherent change topic, then push the current branch. Use when the user asks to commit and push, submit by topic, split current changes into topical commits, or do "按照主题提交 commit 并 push"; especially when a worktree has mixed staged, unstaged, or untracked changes that need honest commit boundaries before `git push`.
---

# Git Topic Commit Push

Group the current worktree into honest topic commits, create them non-interactively, and push the current branch.

## Workflow

1. Collect Git context:
   - `git status --short --branch`
   - `git diff --name-status`
   - `git diff --stat`
   - `git branch --show-current`
   - `git log --oneline -10`
   - `git remote -v`

2. Inspect enough diff to classify changes by topic.
   - Prefer `git diff -- <paths>` and `git diff --cached -- <paths>`.
   - Include untracked files in the classification.
   - Treat generated caches, traces, dumps, logs, secrets, local env files, and large temporary artifacts as non-commit candidates unless the user explicitly asks to track them.

3. Decide commit boundaries.
   - Create one commit when all changes have one coherent purpose.
   - Create multiple commits when changes are independently explainable and can be staged cleanly by path or reviewed hunks.
   - If one file contains unrelated topics and clean non-interactive staging is not safe, ask before forcing a split.
   - Do not invent vague commits such as `update files` to hide unrelated changes.

4. Stage and commit each topic.
   - Stage only the files or hunks for the current topic.
   - Use Conventional Commit subjects: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `build`.
   - Use 2-5 body bullets that describe behavior or outcome, not only file names.
   - Prefer stable non-interactive commands. In PowerShell, use multiple `-m` flags instead of shell heredocs.

5. Verify before pushing.
   - Run `git status --short --branch`.
   - Run `git log --oneline -5`.
   - Confirm the branch is ahead by the expected number of commits and the worktree is clean, or explain any remaining uncommitted files.

6. Push.
   - If the branch already tracks a remote, run `git push`.
   - If there is no upstream, run `git push -u origin <branch>` when `origin` exists.
   - If no suitable remote exists, stop and report the exact blocker.

## Commit Commands

Use this PowerShell-safe pattern:

```powershell
git add -- path/to/file-a path/to/file-b
git commit -m "feat: concise topic subject" `
  -m "- Result or behavior change 1" `
  -m "- Result or behavior change 2"
```

For a second topic, repeat with a fresh staged set:

```powershell
git reset
git add -- docs/example.md scripts/example.mjs
git commit -m "docs: update deployment workflow" `
  -m "- Clarify the production package command" `
  -m "- Document the required environment defaults"
```

## Safety Rules

- Do not run destructive commands such as `git reset --hard`, `git checkout --`, or force push unless the user explicitly asks.
- Do not amend, rebase, squash, or rewrite existing commits unless requested.
- Do not commit secrets from `.env`, credentials, tokens, private keys, or copied production config.
- Do not run tests by default; this skill is for commit and push. If tests were not run, say so in the final response.
- Do not delete user files while preparing commits. If a temporary artifact should not be committed, leave it untracked or add an ignore rule only when that rule is clearly appropriate.

## Final Response

Report:

- Commit hashes and subjects.
- Push target and result.
- Remaining worktree status.
- Tests or validation commands that were run, or state that tests were not run.
