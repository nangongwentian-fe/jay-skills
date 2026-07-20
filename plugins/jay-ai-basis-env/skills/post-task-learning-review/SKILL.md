---
name: post-task-learning-review
description: Review a completed or nearly completed non-trivial task and directly maintain durable lessons across project docs, memory, existing skills, or new skills without asking for separate confirmation. Use after complex debugging, deployment, live verification, repo documentation work, repeated workflow discovery, creating or updating a skill, or when the user asks whether anything is worth remembering, updating, or deleting.
---

# Post-Task Learning Review

Use this skill near the end of a non-trivial task, after verification and before the final response when possible. Keep the review short. Directly apply qualified maintenance actions instead of merely proposing them. The goal is to keep durable knowledge accurate and discoverable, not to create a task diary.

## Core Principle

Maintain before adding. Before adding a new lesson, check whether an existing doc, memory entry, or skill already covers the topic. Prefer update, correction, consolidation, or deletion over appending duplicate or stale knowledge. Treat outdated guidance as a finding: identify what is stale, why it is stale, and replace or remove it.

Project scope first for project knowledge. Codex memory notes help future Codex sessions, but they are outside the current repo and are not visible to other project-scoped agents, collaborators, or deployment workflows. For repo-specific lessons, prefer project docs as the canonical home; use memory only as a cross-session index or supplement. If both are useful, keep project docs actionable and link or summarize the memory-level preference separately.

Treat this skill's activation as authorization to perform safe local maintenance writes within the current task's established scope. Do not ask for separate confirmation merely because the destination is project docs, a permitted memory update, an existing skill, or a new skill. Higher-priority system, developer, and user instructions, filesystem permissions, sensitive-data rules, and external side-effect boundaries still apply. Do not infer permission to commit, push, publish, message other people, or modify production systems.

## Decision Rules

| Destination | Capture when | Do not capture when |
| --- | --- | --- |
| Project docs | The lesson is repo-specific: deployment flow, runtime topology, API contract, troubleshooting path, operational command, accepted architecture decision, or anything future project-scoped agents should share. | It is a one-off chat detail, raw log dump, temporary workaround, or unrelated to the document's topic. |
| Memory | The lesson helps future sessions across projects or Codex threads: stable user preference, machine-specific friction, durable cross-repo fact, or recurring correction. | It contains secrets, private data, unverified guesses, repo-specific knowledge that belongs only in project docs, or facts likely to drift without a verification note. |
| Existing skill | The workflow already has a clear skill home and the lesson improves future execution. | The lesson only applies to one project or one bug. |
| New skill | The workflow repeats across tasks, has clear triggers, and can be described as a reusable procedure. | It is ordinary coding knowledge, a single bug fix, or lacks a stable trigger. |

Choose an action before choosing a destination:

| Action | Use when |
| --- | --- |
| Add | The lesson is durable and no existing place covers it. |
| Update | Existing guidance is incomplete, stale, or contradicted by verified facts. |
| Consolidate | Multiple places repeat the same idea and one canonical place is clearer. |
| Deprecate or remove | Existing guidance is wrong, misleading, or no longer applicable. |
| No-op | The lesson is temporary, obvious, unverifiable, or not worth future context. |

Act on a lesson only when at least two are true:

- Future reuse is likely.
- Rediscovery would be costly.
- The lesson changes how a future agent should act.
- The fact is stable, or can be marked as requiring live verification.
- A future reader has a clear lookup path or trigger phrase.

## Execution Policy

- Execute qualified Add, Update, Consolidate, and Deprecate or remove actions immediately when the target is local, in scope, and writable.
- For memory, follow the active memory mechanism. If direct edits are prohibited but an update-note mechanism is allowed, write the update note directly. If higher-priority policy explicitly requires per-turn user authorization, report that exact restriction rather than inventing permission.
- For project docs, use progressive disclosure and keep unrelated content untouched.
- For skill changes, use `$skill-creator`, validate the changed skill, and keep repository and plugin copies synchronized when both are established sources.
- Do not let an optional publish or sync workflow block the local maintenance write. Commit, push, publication, installation, or external synchronization remains a separate action unless already authorized by the task or repository rules.

## Review Workflow

1. List at most five candidate lessons from the task.
2. Exclude secrets, credentials, tokens, private user data, and raw production data.
3. Check the active context and obvious existing docs, memories, or skills before choosing a destination.
4. Classify each candidate using the action and destination tables.
5. Immediately execute every qualified maintenance action that is permitted and writable.
6. Prefer updating or consolidating an existing doc or skill over creating a new file.
7. If existing guidance is stale, replace or remove the stale claim and record the verified replacement.
8. If a candidate is repo-specific and future project-scoped agents need it, write project docs even when a memory supplement is also useful.
9. Verify every write proportionally: inspect the diff, validate a skill, or re-read the updated memory note.
10. Report completed changes and any exact higher-priority blocker in the final response.

## Output Format

When maintenance was performed, respond with this table:

| Lesson | Action | Destination | Files | Verification |
| --- | --- | --- | --- | --- |

If nothing is worth keeping, say:

`No durable lesson found. Nothing needs to be added, updated, consolidated, or removed.`

Keep the reasoning concise. Report what was changed; do not ask for confirmation unless a higher-priority restriction or genuinely missing decision blocks the write.
