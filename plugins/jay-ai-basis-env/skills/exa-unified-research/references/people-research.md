# People Research

## Tool Restriction

ONLY use `web_search_advanced_exa`.
Do NOT use `web_search_exa` or other Exa tools.

## Dynamic Tuning

Tune `numResults` to user intent:
- a few: 10-20
- comprehensive: 50-100
- explicit count: match user request
- ambiguous: ask for target count

## Query Variation

Use 2-3 query variations and merge/deduplicate results.

## Categories

- `people`: LinkedIn/public bios (primary discovery)
- `personal site`: portfolio/blog/about pages
- `news`: interviews and public mentions
- no category (`type: "auto"`): broader web context

Recommended flow:
- Start with `category: "people"`
- Expand with `personal site`/`news`/no-category when deeper context is needed

## Category-Specific Filter Restrictions

For `category: "people"`, avoid:
- `startPublishedDate` / `endPublishedDate`
- `startCrawlDate` / `endCrawlDate`
- `includeText` / `excludeText`
- `excludeDomains`
- `includeDomains` except LinkedIn domains when required

For no-category searches, most parameters work.

Universal restriction:
- `includeText` / `excludeText` only support single-item arrays

## LinkedIn

Public LinkedIn discovery via Exa.
Auth-required content should use browser fallback.

## Browser Fallback

Fallback when results are insufficient, auth-gated, or JS-heavy pages block extraction.

## Examples

Role search:
```json
{
  "query": "VP Engineering AI infrastructure",
  "category": "people",
  "numResults": 20,
  "type": "auto"
}
```

Query variations:
```json
{
  "query": "machine learning engineer San Francisco",
  "category": "people",
  "additionalQueries": ["ML engineer SF", "AI engineer Bay Area"],
  "numResults": 25,
  "type": "deep"
}
```

Specific person deep dive:
```json
{
  "query": "Dario Amodei Anthropic CEO background",
  "type": "auto",
  "maxAgeHours": 24,
  "numResults": 15
}
```
