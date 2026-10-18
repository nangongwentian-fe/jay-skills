---
name: git-topic-commit-push
description: "Group authorized Git changes into coherent commits and push when requested. Use for topical commit or commit-and-push workflows."
---

# Git Topic Commit Push

Create honest topic commits from the changes the user authorized. Commit and push are distinct actions: a commit-only request does not authorize pushing. Reuse existing explicit authorization instead of asking again for the same action.

## Inspect and group

Inspect branch/upstream, status, staged and unstaged diffs, relevant untracked files and recent commit conventions. Preserve the user's existing staged work and unrelated edits; a dirty worktree alone is not a reason to stop.

Use one commit per coherent outcome, splitting only independently explainable changes. Prefer paths or reviewed hunks. If unrelated changes overlap so that a safe commit boundary cannot be established, ask for the smallest needed staging decision.

## Stage and commit

- Add only authorized paths or hunks. Do not use a bare `git reset`, `git add .` or `git add -A` to prepare a topic.
- Inspect the complete staged diff before each commit: a normal `git commit` includes everything in the index, including previously staged user work. Do not commit that work unless it is authorized; do not unstage it merely for convenience.
- Use Conventional Commit types and Chinese subjects/bodies unless the user requests another language. Body detail should explain the outcome, with 2–5 bullets when the change warrants them.
- Pass message text as safe arguments or a UTF-8 message file supported by the current shell. Avoid interpolated multiline shell strings.

For a topic with no unrelated staged changes:

```text
git add -- <reviewed-paths>
git diff --cached --stat
git diff --cached
git commit -m "fix: 修复已确认的问题"
```

Inspect the index again before another topic; no blanket reset is needed after a successful commit.

## Verify and push

Check the resulting commit content, branch and remaining worktree status. Apply project-required checks; do not repeat a passed suite solely to create a commit. Report which existing verification supports the change and what was not run.

Push only when authorized. Use the configured upstream; if none exists, use the confirmed remote and branch, setting an upstream when consistent with the request. Resolve an ambiguous destination before writing remotely. Verify the remote result and report partial success accurately if a push fails.

No force push, history rewriting, branch switching, secret commits, user-file cleanup or unrelated changes are authorized by this skill.

Report commit hashes and subjects, push outcome when applicable, relevant verification and remaining user work.
