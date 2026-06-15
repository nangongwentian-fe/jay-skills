# Runtime Playbook

Use this reference to choose the right run shape before drafting commands or Markdown.

## Decision Table

| Runtime | Use when | Starts next turn when | Stops when | Output to draft |
|---|---|---|---|---|
| Normal prompt | One short answer or one obvious edit | User prompts again | Current turn ends | Plain prompt |
| Codex `/goal` | One durable outcome needs multi-step work | Previous turn finishes and goal remains active | Completion evidence is satisfied or run is blocked | `/goal ...` plus `goal.md` |
| Claude `/goal` | One completion condition should be checked after each turn | Previous turn finishes and evaluator says not done | Evaluator confirms condition or user clears goal | `/goal ...` plus `goal.md` |
| Claude `/loop` | A prompt should run repeatedly on a timer | Interval elapses | User stops it, session ends, or prompt says to stop/escalate | `/loop <interval> <prompt>` |
| `.claude/loop.md` | Bare `/loop` should use a custom default prompt | Bare `/loop` runs | Same as `/loop` scheduling | One default loop prompt file |

## Codex `/goal`

Draft for a verifiable finish line. Include:

- one outcome and one stopping condition
- project discovery steps before edits when commands are unknown
- concrete verification evidence
- allowed write boundary
- forbidden production, credential, destructive, or unrelated actions
- pause conditions for missing permissions, accounts, secrets, budget, legal/medical/financial judgment, or repeated blockers

Do not use `/goal` for loose backlogs or "keep improving forever".

## Claude Code `/goal`

Draft as a completion condition plus operating contract. Claude checks after every turn whether the condition holds.

Prefer:

- "Run until X is true and proven by Y"
- "Preserve A, B, C"
- "Pause if Z is required"

Avoid:

- conditions based only on model confidence
- broad wording like "finish everything"
- goals with no check Claude can run or inspect

## Claude `/loop`

Draft as a timed prompt. It is for polling and recurring checks, not for proving a single implementation is done.

Include:

- interval or trigger expectation
- what to observe every run
- how to report results
- what to do if nothing changed
- when to stop, alert, escalate, or ask for human input

Good uses:

- check a deploy every 5 minutes
- babysit a PR until CI/reviews change
- poll a long-running build
- write a recurring status report

## `.claude/loop.md`

Use when the user wants bare `/loop` to run a custom default prompt.

Rules:

- Define one default prompt.
- Do not put multiple unrelated scheduled tasks in it.
- Do not rely on the file to set the interval; the `/loop` invocation controls cadence.
- Include observation signals, report format, no-op behavior, and escalation rules.

## `goal.md`

Use when the contract should persist outside the command line.

Keep it short and operational:

- outcome
- runtime command
- context to inspect first
- verification evidence
- constraints and boundaries
- iteration policy
- stop and pause conditions
- progress log location if needed
