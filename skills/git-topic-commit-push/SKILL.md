---
name: git-topic-commit-push
description: "Commit and push each completed topic immediately after required checks pass. Use throughout Git implementation tasks and when delivering existing changes by topic; do not defer delivery until the end of a multi-topic task."
---

# Git Topic Commit Push

For authorized Git changes, the user's standing preference is to commit and push each completed topic without another request. Apply this workflow throughout implementation, not only when the user asks for a final commit. An explicit instruction to avoid committing or pushing, or to commit only, overrides this default.

## Topic completion gate

Treat one coherent, independently explainable outcome as one topic. Include its required tests, current-state documentation and decision records in the same commit. Do not split incomplete work just to increase commit frequency, or accumulate completed topics into a large final batch.

As soon as a topic is ready, complete this sequence before starting the next independent topic or reporting completion:

1. Run the required checks for that topic.
2. Synchronize with the remote and review the exact changes to include.
3. Create one topic commit.
4. Push it immediately and verify that the destination branch contains the commit.
5. Report the commit and confirmed push status briefly, then continue.

A local commit alone does not complete delivery. Track each topic as checked, committed and remotely verified; before ending the task, reconcile these states against Git rather than relying on memory. For an existing backlog, identify coherent topics and deliver each in this same sequence.

## Inspect and group

Inspect branch/upstream, status, staged and unstaged diffs, relevant untracked files, recent commit conventions and existing unpushed commits. Preserve the user's existing staged work and unrelated edits; a dirty worktree alone is not a reason to stop. A push also publishes earlier commits on the branch: inspect that range and do not silently include unrelated work whose publication is not authorized.

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

Apply project-required checks before committing; do not repeat a passed suite solely to create a commit. If synchronization changes the validated content, rerun affected checks. Check the resulting commit content, branch and remaining worktree status.

Use the configured upstream; if none exists, use the confirmed remote and branch, setting an upstream when consistent with the request. Resolve an ambiguous destination before writing remotely. Fetch and inspect remote changes before committing; fast-forward when safe or integrate under repository policy without overwriting user work or rewriting history. If integration cannot be completed safely, report the specific blocker.

Push the topic immediately using an explicit remote and destination branch. Verify with a fresh fetch or remote-ref query that the pushed commit is at the remote tip or is its ancestor; a clean worktree or local commit hash is not evidence of a successful push.

If push fails or remote verification is unavailable, state **committed locally; push failed** or **committed locally; remote delivery unverified**, with the commit hash, destination and cause. Resolve recoverable failures within existing authorization and retry after the cause is addressed; do not loop blindly. If still blocked, stop accumulating further topic commits, report what is needed to unblock delivery, and do not claim completion. Resume by resolving outstanding delivery before starting another topic.

No force push, history rewriting, branch switching, secret commits, user-file cleanup or unrelated changes are authorized by this skill.

For every topic, report commit hash and subject, remote/branch and verified push outcome, relevant checks and any remaining work. If the user explicitly requested local-only work, report **not pushed (as requested)**. Never leave the user to infer whether a commit reached the remote.
