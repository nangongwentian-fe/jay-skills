# Personal Site Search

## Tool Restriction

ONLY use `web_search_advanced_exa` with `category: "personal site"`.

## Filter Support

This category supports domain/date/text filters.

Array-size restriction:
- `includeText` / `excludeText` must be single-item arrays

## Supported Inputs

- Core: `query`, `numResults`, `type`
- Domain: `includeDomains`, `excludeDomains`
- Date: `startPublishedDate`, `endPublishedDate`, `startCrawlDate`, `endCrawlDate`
- Text: `includeText`, `excludeText` (single-item arrays)
- Extraction: highlights/summary/context controls
- Additional: `additionalQueries`, `maxAgeHours`, `livecrawlTimeout`, `subpages`, `subpageTarget`

## Examples

Technical blog discovery:
```json
{
  "query": "building production LLM applications lessons learned",
  "category": "personal site",
  "numResults": 15,
  "type": "deep",
  "enableSummary": true
}
```

Recent posts:
```json
{
  "query": "Rust async runtime comparison",
  "category": "personal site",
  "startPublishedDate": "2025-01-01",
  "numResults": 10,
  "type": "auto"
}
```

Exclude aggregators:
```json
{
  "query": "startup founder lessons",
  "category": "personal site",
  "excludeDomains": ["medium.com", "substack.com"],
  "numResults": 15,
  "type": "auto"
}
```
