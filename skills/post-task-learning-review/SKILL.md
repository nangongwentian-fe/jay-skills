---
name: post-task-learning-review
description: Review a completed or nearly completed non-trivial task and maintain durable lessons across project docs, memory, existing skills, or new skills. Use after complex debugging, deployment, live verification, repo documentation work, repeated workflow discovery, creating or updating a skill, or when the user asks whether anything is worth remembering, updating, or deleting.
---

# Post-Task Learning Review

Use this skill near the end of a non-trivial task, after verification and before the final response when possible. Keep the review short. The goal is to maintain durable lessons in the right place, not to create a task diary.

## Core Principle

Maintain before adding. Before adding a new lesson, check whether an existing doc, memory entry, or skill already covers the topic. Prefer update, correction, consolidation, or deletion over appending duplicate or stale knowledge. Treat outdated guidance as a finding: identify what is stale, why it is stale, and where it should be updated or removed.

Project scope first for project knowledge. Codex memory notes help future Codex sessions, but they are outside the current repo and are not visible to other project-scoped agents, collaborators, or deployment workflows. For repo-specific lessons, prefer project docs as the canonical home; use memory only as a cross-session index or supplement. If both are useful, keep project docs actionable and link or summarize the memory-level preference separately.

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

## Review Workflow

1. List at most five candidate lessons from the task.
2. Exclude secrets, credentials, tokens, private user data, and raw production data.
3. Check the active context and obvious existing docs, memories, or skills before recommending a new place.
4. Classify each candidate using the action and destination tables.
5. Prefer updating or consolidating an existing doc or skill over creating a new file.
6. If existing guidance is stale, name the stale claim and the verified replacement.
7. If a candidate is repo-specific and future project-scoped agents need it, recommend project docs even if a Codex memory note is also useful.
8. If writing project docs, use progressive disclosure: common path first, details later, and no unrelated history.
9. If writing memory, follow the active memory policy. When direct edits are not allowed, propose or write an approved update note instead of rewriting history.
10. If creating or updating a skill, use `$skill-creator`; after a skill change, ask whether to sync it with `$sync-skill-to-jay`.

## Output Format

When reviewing, respond with this table:

| Lesson | Action | Destination | Reason | Next Step |
| --- | --- | --- | --- | --- |

If nothing is worth keeping, say:

`No durable lesson found. Nothing needs to be added, updated, consolidated, or removed.`

Keep the reasoning concise. Do not write files unless the user requested or approved that write.
