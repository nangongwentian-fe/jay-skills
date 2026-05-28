# Research Paper Search

## Tool Restriction

ONLY use `web_search_advanced_exa` with `category: "research paper"`.

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
- Additional: `userLocation`, `moderation`, `additionalQueries`, `livecrawl`, `subpages`

## Examples

Recent papers:
```json
{
  "query": "transformer attention mechanisms efficiency",
  "category": "research paper",
  "startPublishedDate": "2024-01-01",
  "numResults": 15,
  "type": "auto"
}
```

Venue-targeted:
```json
{
  "query": "large language model agents",
  "category": "research paper",
  "includeDomains": ["arxiv.org", "openreview.net"],
  "includeText": ["LLM"],
  "numResults": 20,
  "type": "deep"
}
```
