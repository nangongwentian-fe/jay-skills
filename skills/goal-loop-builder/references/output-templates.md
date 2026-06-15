# Output Templates

Use these shapes as patterns. Replace every placeholder before returning output.

## Chinese-First `/goal`

```text
推荐运行方式：Codex 或 Claude Code `/goal`，因为任务有明确完成条件，需要持续推进直到证据证明完成。

可复制命令：
/goal [具体目标结果]。
验证：[命令、截图、日志、API 响应、PR 状态或产物证据]。
约束：[不能改变的行为、接口、数据、风格、安全或分支规则]。
边界：[允许写入的位置、禁止触碰的路径、工具或环境]。
迭代策略：[一次一个聚焦改动；每次重跑相关检查；失败先读日志；连续失败后换证据来源或缩小复现]。
完成条件：[哪些证据同时成立时停止]。
暂停条件：[需要凭证、付费、生产数据、破坏性操作、法律/医疗/金融判断、版权素材、所有权不清或产品取舍时暂停]。
```

## English-Compatible `/goal`

```text
/goal [Concrete target outcome].
Verification: [commands, screenshots, logs, API responses, PR state, or artifact evidence].
Constraints: [behavior, API, data, style, security, or branch rules that must not change].
Boundaries: [allowed write locations, forbidden paths, tools, or environments].
Iteration policy: [make one focused change at a time; rerun relevant checks; inspect logs before retrying; change evidence source or reduce to a repro after repeated failure].
Stop when: [specific evidence proves completion].
Pause if: [credentials, payments, production data, destructive actions, legal/medical/financial judgment, copyrighted assets, unclear ownership, or product decisions are required].
```

## `goal.md`

```markdown
# Goal Run Contract

## Outcome

[Concrete target outcome.]

## Runtime Command

```text
/goal [same target outcome and contract]
```

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
