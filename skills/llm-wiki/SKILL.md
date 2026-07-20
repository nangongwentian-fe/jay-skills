---
name: llm-wiki
description: "Operate the user's locally running LLM Wiki desktop app and its project files. Use when the user explicitly names LLM Wiki, my wiki, 知识库, a Wiki page/project, graph, review queue, Wiki Agent chat, or source rescan; also use when another skill such as search-jay-llm-wiki requests LLM Wiki retrieval or authorized filesystem maintenance. Covers LLM Wiki 0.6.4 health, projects, file listing/read, reviews, hybrid search, Agent chat and cancellation, graph navigation, source rescan, and the fixed jay-llm-wiki filesystem fallback. Do not trigger for Obsidian, Notion, generic notes, or unrelated knowledge tools."
---

# LLM Wiki Operations

Use the desktop app's localhost API or MCP for retrieval and Agent operations. Use direct filesystem access only for an explicitly selected project and authorized Markdown maintenance.

## Choose the transport

| Situation | Action |
|---|---|
| LLM Wiki MCP tools are callable | Prefer MCP for supported reads, search, reviews, chat, graph, and rescan. |
| HTTP API is enabled and authenticated | Call `http://127.0.0.1:19828/api/v1` with JSON. |
| API auth is unavailable and the target is the fixed `jay-llm-wiki` project | Fall back to local `rg` and file reads; allow writes only when the calling workflow authorizes them. |
| Another project requires protected API access | Ask the user to configure a token or enable the MCP server. |

Read [references/api-reference.md](references/api-reference.md) before using reviews, chat, cancellation, or handling API errors. Read [references/examples.md](references/examples.md) when command syntax is needed.

## Probe health without secrets

Always call `GET /health` before protected API operations. Version 0.6.4 reports API, MCP, and Agent state, including `agent.chat`.

- Use `LLM_WIKI_API_TOKEN` or the token stored by the desktop app.
- Prefer `Authorization: Bearer <token>`.
- Never echo, log, paste, or place the token in a URL.
- If `authConfigured: false` and unauthenticated access is disabled, use the fixed-project filesystem fallback when applicable. Do not block a file-based knowledge pass.

## Resolve the project

- Use `current` when the user explicitly means the project open in the desktop app.
- Use the UUID when supplied.
- Use a URL-encoded absolute path when a workflow fixes the project path.
- Resolve a project name through `GET /projects`; do not pass a name as `{id}`.
- Cache the resolved project for the current task and re-resolve if the user changes projects.

## Retrieve grounded knowledge

1. Search with `POST /projects/{id}/search`, normally with `topK: 5..10`.
2. Read promising files with `GET /projects/{id}/files/content?path=...` or use `includeContent: true`.
3. Treat relative ranking, retrieval mode, and page content as context rather than final proof.
4. Cite every Wiki path that materially supports the answer.

For a mandatory background check from `$search-jay-llm-wiki`, prefer local keyword search or `/search`. Do not send the full user prompt to `/chat` by default.

## Use 0.6.4 Agent and review capabilities

- List unresolved or filtered review items with `GET /projects/{id}/reviews`.
- Ask the backend Wiki Agent with `POST /projects/{id}/chat`; it can return references, tool events, session state, and usage.
- Cancel an active Agent session with `POST /projects/{id}/chat/{sessionId}/cancel`.
- Enable backend web or AnyTXT tools only when the user request and data boundary justify them.
- Do not claim streaming support when `/health` reports `agent.streaming: false`.

## Maintain files without inventing APIs

LLM Wiki API v1 has no endpoint for creating or updating Wiki Markdown. Direct filesystem edits are the write path for an authorized project. `POST /sources/rescan` only rescans configured source folders and queues changed source work; it is not a general Wiki write endpoint.

When editing the fixed personal Wiki:

1. Resolve `JAY_LLM_WIKI_ROOT`, defaulting to `E:\\Code\\Personal\\jay-llm-wiki`.
2. Read its `AGENTS.md`, `purpose.md`, and `schema.md`.
3. Inspect Git status and target diffs before editing.
4. Preserve unrelated work and existing raw sources.
5. Validate on disk and cite the changed paths.

## Failure handling

- Connection failure: tell the user the desktop app is not reachable, then use the fixed-project fallback if possible.
- `401`: token missing or wrong; do not retry in a loop.
- `403`: path is outside the allowed API scope; do not retry the same path.
- `404`: re-resolve the project or route.
- `413`/`415`: narrow the request or use an allowed text source.
- `429`/busy `503`: back off and reduce concurrency.
- Other `5xx`: report the error and stop retrying.
