# Code Search

## Tool Restriction

Only use `web_search_exa`.

## When to Use

Use for:
- API usage and syntax
- SDK/library examples
- configuration and setup patterns
- framework how-to
- debugging with authoritative snippets

## Inputs

- `query` (required)
- `numResults` (optional, default 10)

## Query Patterns

- Always include programming language
- Include framework and version when relevant
- Include exact identifiers (function/class/config key/error text)

## Tuning

Tune `numResults` by user intent (aligns with global query strategy):
- "a few examples": 10-20 results
- "comprehensive": 20-50 results
- explicit number: follow user request

## Output

1. Minimal working snippet(s)
2. Version constraints and gotchas
3. Source URLs
