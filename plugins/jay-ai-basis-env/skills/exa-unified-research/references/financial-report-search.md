# Financial Report Search

## Tool Restriction

ONLY use `web_search_advanced_exa` with `category: "financial report"`.

## Known Restriction

- `excludeText` is not supported

## Supported Inputs

- Core: `query`, `numResults`, `type`
- Domain: `includeDomains`, `excludeDomains`
- Date: `startPublishedDate`, `endPublishedDate`, `startCrawlDate`, `endCrawlDate`
- Text: `includeText` (single-item arrays only)
- Extraction: highlights/summary/context controls
- Additional: `additionalQueries`, `maxAgeHours`, `livecrawlTimeout`, `subpages`, `subpageTarget`

## Examples

SEC filings:
```json
{
  "query": "Anthropic SEC filing S-1",
  "category": "financial report",
  "numResults": 10,
  "type": "auto"
}
```

Recent earnings:
```json
{
  "query": "Q4 2025 earnings report technology",
  "category": "financial report",
  "startPublishedDate": "2025-10-01",
  "numResults": 20,
  "type": "auto"
}
```

10-K on SEC:
```json
{
  "query": "10-K annual report AI companies",
  "category": "financial report",
  "includeDomains": ["sec.gov"],
  "startPublishedDate": "2025-01-01",
  "numResults": 15,
  "type": "deep"
}
```
