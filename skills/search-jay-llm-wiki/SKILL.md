---
name: search-jay-llm-wiki
description: "Proactively search the fixed jay-llm-wiki before relevant non-trivial research, architecture, technology selection, complex debugging, or complex implementation tasks when prior Deep Research or reusable engineering knowledge may help. Use even when the user does not explicitly mention LLM Wiki. Invoke $llm-wiki for transport, cite the Wiki paths used, and verify time-sensitive claims with current first-party sources. Skip translation, formatting, simple calculations, one-line commands, casual conversation, and clearly unrelated self-contained tasks."
---

# Search Jay LLM Wiki

Use the personal Wiki as a task-start knowledge source. Keep this workflow read-only. Do not evaluate or perform Wiki write-back at task completion.

## Decide whether to search

Search when prior research, cross-project conclusions, architectural decisions, comparisons, or reusable debugging experience could materially improve the task.

Skip the search when the task is simple and self-contained or the Wiki is clearly unrelated. If uncertain on a substantive task, perform one bounded search rather than asking the user whether to search.

## Run the background check

1. Extract 2–6 specific keywords from the request. Remove credentials, tokens, personal data, private URLs, and other unnecessary sensitive values.
2. Invoke `$llm-wiki` for retrieval against the fixed project root `E:\Code\Personal\jay-llm-wiki`.
3. Prefer an authenticated LLM Wiki MCP or HTTP search when available. If authentication is unavailable or MCP is disabled, use local `rg` and file reads immediately; do not block on configuration.
4. Search in this order:
   - `wiki/index.md` for titles and topic routing;
   - filenames and YAML fields such as `title`, `tags`, `related`, and aliases when present;
   - page bodies under `wiki/`.
5. Read at most five Wiki files in total, including `wiki/index.md`. A normal pass reads the index plus 2–4 relevant pages. Never exceed this cap; stop earlier when the pages answer the background question.
6. Cite each materially used page with its repository-relative path, for example `jay-llm-wiki/wiki/concepts/context-engineering.md`.

Do not send the full user request to Wiki Agent Chat for this background check. Do not run repeated reformulations after one well-formed search returns no useful result.

## Keep evidence roles separate

| Source | Use it for |
|---|---|
| Current repository and runtime | Present implementation, configuration, data, and observed behavior |
| `jay-llm-wiki` | Prior Deep Research, reusable conclusions, comparisons, and engineering experience |
| Context7 | Current official library, framework, SDK, API, CLI, and cloud-service documentation |
| Web search and first-party sites | News, releases, prices, schedules, and other externally changing facts |

Treat Wiki pages as a research starting point, not final proof of current state. Verify versions, product capabilities, recommendations, and other drift-prone claims through current first-party documentation, the current repository, or live runtime evidence. When sources conflict, report the conflict and prefer the current primary source for the present-state claim.

## Continue safely on failure

- No relevant result: continue the original task without treating the absence as evidence.
- Desktop service unavailable, `401`, or MCP disabled: use the fixed-project filesystem fallback once.
- Fixed project missing or unreadable: continue the task and mention the unavailable background source only when it materially limits confidence.
- Never expose secrets in commands, logs, citations, or search terms.
- Do not edit Wiki files, rescan sources, create reviews, or start Wiki Agent Chat as part of this skill.
