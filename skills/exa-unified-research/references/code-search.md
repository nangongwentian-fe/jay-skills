# Code Search

## Tool Restriction

Only use `get_code_context_exa`.

## When to Use

Use for:
- API usage and syntax
- SDK/library examples
- configuration and setup patterns
- framework how-to
- debugging with authoritative snippets

## Inputs

- `query` (required)
- `tokensNum` (optional, default around 5000)

## Query Patterns

- Always include programming language
- Include framework and version when relevant
- Include exact identifiers (function/class/config key/error text)

## Tuning

- Focused snippet: 1000-3000
- Typical task: 5000
- Complex integration: 10000-20000

## Output

1. Minimal working snippet(s)
2. Version constraints and gotchas
3. Source URLs
