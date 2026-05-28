# Social Discussion & Sentiment Search

Search for social media discussion, reactions, and sentiment — primarily X/Twitter content and broader public discourse.

## Limitation

The Exa MCP tool does **not** support `category: "tweet"`. The best available approach is `category: "news"` with domain filtering, which often returns articles *about* tweets rather than tweet content itself. Document this gap honestly in your output notes.

## Tool Restriction

Use `web_search_advanced_exa` with `category: "news"` and `includeDomains: ["x.com", "twitter.com"]`.

If domain filtering returns insufficient individual tweets (common), note this as a coverage gap and recommend the user try a dedicated X/Twitter API or browser-based access for primary tweet data.

## Filter Restrictions

For social discussion searches:
- `includeText` and `excludeText` — avoid (unreliable for short-form content)
- `excludeDomains` — avoid
- `moderation` — avoid
- Do **not** use `category: "tweet"` — it will cause an API error

Supported parameters:
- Core: `query`, `numResults`, `type`
- Domain: `includeDomains` (use `["x.com", "twitter.com"]`)
- Date: `startPublishedDate`, `endPublishedDate`, `startCrawlDate`, `endCrawlDate`
- Extraction: highlights/summary/context controls
- Additional: `additionalQueries`, `maxAgeHours`, `livecrawlTimeout`

## Fallback Strategy

1. First attempt: `category: "news"` + `includeDomains: ["x.com", "twitter.com"]`
2. If results are primarily articles about tweets (not actual tweets): expand to `category: "news"` without `includeDomains`, and flag the coverage gap in your output notes
3. For sentiment analysis where individual tweets are essential: note the limitation and suggest alternative data sources (dedicated X API, browser-based access)

## Tuning

Tune `numResults` to user intent:
- a few mentions: 10-15
- comprehensive scan: 20-50
- explicit count: match user request

## Query Patterns

- Include platform name: "X" or "Twitter" in queries
- Include topic/entity keywords: "OpenAI o1 reaction", "Claude Code sentiment"
- Use `additionalQueries` for query variation

## Examples

Social media discussion (X/Twitter focused):
```json
{
  "query": "Claude Code MCP experience",
  "category": "news",
  "includeDomains": ["x.com", "twitter.com"],
  "startPublishedDate": "2025-01-01",
  "numResults": 20,
  "type": "auto",
  "livecrawlTimeout": 5000
}
```

Broader public sentiment (fallback):
```json
{
  "query": "OpenAI o1 reasoning model reaction Twitter",
  "category": "news",
  "numResults": 20,
  "startPublishedDate": "2025-12-01",
  "type": "auto"
}
```

Keyword-focused:
```json
{
  "query": "LLM reasoning breakthrough announcement",
  "category": "news",
  "includeDomains": ["x.com", "twitter.com"],
  "startPublishedDate": "2025-12-01",
  "numResults": 15,
  "type": "auto",
  "additionalQueries": ["chain-of-thought reasoning Twitter reaction", "o3 reasoning model sentiment"]
}
```