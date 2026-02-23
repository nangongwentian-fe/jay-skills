# Company Research

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

Use category based on intent:
- `company`: homepages and metadata (headcount/location/funding/revenue when available)
- `news`: press coverage and announcements
- `tweet`: social presence and public commentary
- `people`: LinkedIn-style public profile data
- no category (`type: "auto"`): broader web context

Recommended flow:
- Start with `category: "company"` for discovery
- Then use `news`/`tweet`/`people`/no-category for deeper research

## Category-Specific Filter Restrictions

When using `category: "company"`, avoid:
- `includeDomains` / `excludeDomains`
- `startPublishedDate` / `endPublishedDate`
- `startCrawlDate` / `endCrawlDate`

When searching without a category (or with `news`), domain/date filters generally work.

Universal restriction:
- `includeText` and `excludeText` only support single-item arrays

## LinkedIn

Public profile discovery: `category: "people"`, avoid extra restrictive filters.
Auth-required LinkedIn content: browser fallback.

## Browser Fallback

Fallback to browser when:
- Exa results are insufficient
- content is auth-gated
- dynamic pages require JS rendering

## Examples

Discovery:
```json
{
  "query": "AI infrastructure startups San Francisco",
  "category": "company",
  "numResults": 20,
  "type": "auto"
}
```

Deep dive:
```json
{
  "query": "Anthropic funding rounds valuation 2024",
  "type": "deep",
  "livecrawl": "fallback",
  "numResults": 10,
  "includeDomains": ["techcrunch.com", "crunchbase.com", "bloomberg.com"]
}
```

News:
```json
{
  "query": "Anthropic AI safety",
  "category": "news",
  "numResults": 15,
  "startPublishedDate": "2024-01-01"
}
```

People:
```json
{
  "query": "VP Engineering AI infrastructure",
  "category": "people",
  "numResults": 20
}
```
