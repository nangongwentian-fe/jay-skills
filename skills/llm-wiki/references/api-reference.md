# LLM Wiki 0.6.4 API Reference

Base URL: `http://127.0.0.1:19828/api/v1`

All endpoints except `/health` require the configured token unless the user enabled unauthenticated access. API v1 exposes no Markdown create, update, or delete route.

## Endpoints

| Method | Path | Contract |
|---|---|---|
| GET | `/health` | Returns status, version, API/MCP/auth state, and `agent: { chat, streaming }`. |
| GET | `/projects` | Returns registered projects and `currentProject`. |
| GET | `/projects/{id}/files` | Query: `root=wiki|sources|all`, `recursive`, `maxFiles`. |
| GET | `/projects/{id}/files/content` | Query: project-relative `path`; text files only. |
| GET | `/projects/{id}/reviews` | Query: `status=unresolved|resolved|all`, optional `type`, optional `limit`. |
| POST | `/projects/{id}/search` | Body: `query`, optional `topK`, `includeContent`; returns ranked results and retrieval mode. |
| POST | `/projects/{id}/chat` | Body: `message` plus optional session, mode, retrieval, tool, and project-skill settings. |
| POST | `/projects/{id}/chat/{sessionId}/cancel` | Cancels an active backend Agent session. |
| GET | `/projects/{id}/graph` | Query: optional `q`, `nodeType`, `limit`. |
| POST | `/projects/{id}/sources/rescan` | Rescans configured sources and returns queued or changed work. |

`{id}` accepts `current`, a UUID, or a URL-encoded absolute project path. Project names must be resolved through `/projects`.

## Reviews

Review items can include:

- `id`, `type`, `title`, `description`;
- `sourcePath`, `affectedPages`, `searchQueries`;
- action options;
- resolution state and creation time.

The API and bundled MCP server expose review reads, not review-resolution mutations.

## Agent chat

Request fields supported by the 0.6.4 client:

```json
{
  "message": "question",
  "sessionId": "optional",
  "persistSession": true,
  "mode": "optional",
  "topK": 8,
  "includeContent": false,
  "tools": {
    "wiki": true,
    "web": false,
    "anytxt": false
  },
  "skills": []
}
```

The response includes `projectId`, `sessionId`, `mode`, an assistant `message`, `references`, `toolEvents`, raw `events`, and usage counts. Respect `/health.agent.streaming`; version 0.6.4 on this machine reports streaming disabled.

## Bundled MCP tools

The installed MCP server exposes:

- `llm_wiki_status`
- `llm_wiki_projects`
- `llm_wiki_files`
- `llm_wiki_read_file`
- `llm_wiki_reviews`
- `llm_wiki_search`
- `llm_wiki_chat`
- `llm_wiki_graph`
- `llm_wiki_rescan_sources`

Chat cancellation is available through HTTP but is not exposed as a bundled MCP tool in 0.6.4.

## Status handling

| Status | Response |
|---|---|
| 400 | Fix invalid input; do not retry unchanged. |
| 401 | Configure or correct authentication. |
| 403 | Stop; the requested path or operation is forbidden. |
| 404 | Re-resolve the project or route. |
| 405 | Correct the HTTP method. |
| 413 | Narrow a large body, tree, or file request. |
| 415 | Use a supported UTF-8 text file. |
| 429 | Back off for at least one second. |
| 500 | Report and stop automatic retries. |
| 503 | If disabled, enable the API; if busy, reduce concurrency and retry after a delay. |

