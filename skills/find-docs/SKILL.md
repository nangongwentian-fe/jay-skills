---
name: find-docs
description: "Look up current library, API and CLI syntax, configuration or version-specific behavior with Context7. Use for documentation-dependent development questions."
---

# Current Documentation Lookup

Use Context7 for specific library, framework, SDK, API, CLI or cloud-service contracts. Refactoring, business-logic debugging, code review and general programming concepts do not require a lookup unless a concrete external contract is uncertain.

## Query

Run requests outside the default Codex sandbox. Use the official library name and a focused, non-sensitive query:

```text
npx ctx7@latest library "<official library name>" "<specific documentation question>"
npx ctx7@latest docs <returned-library-id> "<one concept or interaction>"
```

- Resolve with `library` first unless the user supplies an ID such as `/org/project` or `/org/project/version`. Never invent an ID.
- Select by exact name, relevance, source reputation, coverage and benchmark score. Prefer official sources; refine an ambiguous search within the query budget.
- Use a version-specific ID returned by the resolver when that version matters. If the requested version is unavailable, disclose the mismatch.
- Run at most three Context7 commands per question. Use a separate `docs` query per distinct concept unless the question concerns their interaction. Reuse relevant results within the task.
- Base the answer on the fetched documentation and link to the supporting source. Distinguish documented behavior from inference; do not present search snippets as verified contracts.

## Failure handling

- If a request was accidentally run inside the sandbox and fails with DNS or network errors, retry outside it instead of repeating the same blocked environment. Never bypass an approval denial.
- On quota exhaustion, report it and suggest `npx ctx7@latest login` or `CONTEXT7_API_KEY` for higher limits. Do not expose credentials or start a login without authorization.
- If retrieval still fails or coverage is insufficient, say what remains unverified. Use accessible official documentation or local source where permitted; never silently substitute remembered API details.

This workflow does not install project dependencies or change configuration. API keys, passwords, private source and personal data must not appear in queries.

## Maintenance provenance

Imported into jay-skills from the user's existing standalone `find-docs` installation during the September 2026 instruction audit. No upstream repository or license was recorded for that installation; do not invent one. The maintained source is now this directory, and installed copies are derived artifacts.
