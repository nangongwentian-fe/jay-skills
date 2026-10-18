# Independent review workflow

Use this only for a review-triggering implementation after its first verification.

1. Check the active delegation rule, including any skill exception. Follow the explicit reviewer request in SKILL.md when allowed; otherwise perform the disclosed local fallback.
2. Freeze the user objective, acceptance criteria, repository, changed scope, stable contracts, tests already run and unrelated dirty work. Record a commit/diff hash or hashes of every target file.
3. Give a new reviewer a self-contained minimal context using the reviewer contract. Request read-only investigation with no edits or external actions. Do not reuse an implementation participant as an independent reviewer.
4. Keep its work bounded. If spawning fails, retry once with a smaller scope when useful. A timeout warrants inspecting partial evidence before deciding whether that one retry would help. Never retry when delegation is prohibited.
5. Avoid changing the review scope while it runs. After return, compare the frozen hashes and review any new delta; old evidence cannot pass changed files.
6. Keep the reviewer identity, scope packet and raw findings traceable in task context. Do not add review transcripts to the repository unless requested.
7. Verify each claim using the cited code, affected consumers and the smallest useful reproduction. Record severity, location, broken contract, evidence, disposition and verification. Reject unsupported claims with evidence rather than deference.
8. Fix verified defects within the current authorization and rerun affected checks. An outside-scope defect requires the smallest missing decision while independent work continues.
9. Re-review only the fix delta after P0/P1 or a material redesign, subject to the two-round limit. Finish with actual outcomes, unresolved findings and material verification gaps.

If the reviewer asks for user input, route it through the primary agent. If independent review cannot run, perform the same bounded evidence checks locally and describe the result accurately.
