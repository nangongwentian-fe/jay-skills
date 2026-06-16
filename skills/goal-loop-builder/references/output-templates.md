# Output Templates

Use these shapes as patterns. Replace every placeholder before returning output.

## Chinese-First File-Backed `/goal`

```text
推荐运行方式：Codex 或 Claude Code `/goal`，因为任务有明确完成条件，需要持续推进直到证据证明完成。

已生成 Markdown 文件：
[/absolute/path/to/task.goal.md](/absolute/path/to/task.goal.md)

可复制 /goal prompt：
/goal Read @/absolute/path/to/task.goal.md and execute that run contract. Treat the Markdown file as the source of truth for outcome, verification, boundaries, stop conditions, and pause conditions.

文件内容摘要：
- 目标：[一句话说明结果]
- 验证：[最关键证据]
- 边界：[允许和禁止的写入/操作]
- 停止：[完成证据]
- 暂停：[需要用户决策或权限的情况]
```

## English-Compatible File-Backed `/goal`

```text
/goal Read @/absolute/path/to/task.goal.md and execute that run contract. Treat the Markdown file as the source of truth for outcome, verification, boundaries, stop conditions, and pause conditions.
```

## `goal.md`

```markdown
# Goal Run Contract

## Outcome

[Concrete target outcome. This is the result, not the activity.]

## Inspect First

- [Project scripts, docs, issue, logs, CI config, or relevant files.]

## Verification

- [Command or evidence.]
- [Runtime check, screenshot, API response, file, or PR state.]

## Constraints

- [Behavior/API/data/style/security rule to preserve.]

## Boundaries

- Allowed writes: [paths].
- Forbidden: [paths, systems, actions].

## Iteration Policy

- Work in one focused slice at a time.
- Rerun the smallest relevant check after meaningful changes.
- Inspect logs or outputs before changing strategy.
- After repeated failure, reduce scope or pause with evidence.

## Stop When

- [Evidence proving completion.]

## Pause If

- [Human decision, credential, budget, production, destructive, or compliance blocker.]

## Progress Log

- Append concise progress notes here only when useful for handoff.
```

## Claude `/loop`

```text
推荐运行方式：Claude `/loop`，因为任务是按时间重复观察状态，而不是一次性推进到完成。

可复制命令：
/loop 5m Check [target state]. Inspect [signals/logs/status source]. Report [format]. If nothing changed, say so in one line. Stop or escalate if [failure, timeout, approval need, or human decision].
```

## `.claude/loop.md`

```markdown
# Default Loop Prompt

Run when bare `/loop` invokes this default prompt.

Observe:
- [status source, logs, CI, PR, deployment, queue, or other signal]

Report:
- Current state
- What changed since the previous run
- Evidence or links
- Next expected check

Do nothing else when:
- [no change condition]

Stop or escalate when:
- [failure condition]
- [timeout or repeated no-progress condition]
- [human approval, credential, production, or destructive action is required]

Boundaries:
- Read: [allowed sources]
- Write: [allowed report/log path, or "none"]
- Do not: [forbidden actions]
```
