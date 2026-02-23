# X/Twitter Tweet Search

## Tool Restriction

ONLY use `web_search_advanced_exa` with `category: "tweet"`.

## Filter Restrictions

For `tweet`, avoid:
- `includeText`
- `excludeText`
- `includeDomains`
- `excludeDomains`
- `moderation`

## Supported Inputs

- Core: `query`, `numResults`, `type`
- Date: `startPublishedDate`, `endPublishedDate`, `startCrawlDate`, `endCrawlDate`
- Extraction: highlights/summary/context controls
- Additional: `additionalQueries`, `livecrawl`, `livecrawlTimeout`

## Examples

Recent tweets:
```json
{
  "query": "Claude Code MCP experience",
  "category": "tweet",
  "startPublishedDate": "2025-01-01",
  "numResults": 20,
  "type": "auto",
  "livecrawl": "preferred"
}
```

Keyword-focused:
```json
{
  "query": "launching announcing new open source release",
  "category": "tweet",
  "startPublishedDate": "2025-12-01",
  "numResults": 15,
  "type": "auto"
}
```
