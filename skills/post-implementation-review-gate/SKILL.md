---
name: post-implementation-review-gate
description: "Review completed changes with material compatibility, security or behavioral risk before handoff. Use an independent reviewer for the risk signals below."
---

# Post-Implementation Review Gate

Catch concrete defects before declaring a risky implementation complete. This skill does not apply to planning, diagnosis-only work, trivial text edits or mechanical formatting.

## Select the review level

Use an independent reviewer for changes to:

- public APIs, schemas, shared contracts or compatibility;
- persistence, migrations, authentication, authorization or secrets;
- deployment behavior, routing or consequential environment configuration;
- concurrency, cancellation, lifecycle, data integrity or complex algorithms/control flow;
- cross-module behavior, generated/runtime coupling, or UI interaction and state behavior with material regression risk.

A small, bounded implementation with no risk signal and direct passing behavioral verification needs only a proportional local review. An ordinary spacing or color adjustment does not trigger independent review merely because it is rendered UI. If a concrete risk remains uncertain, use an independent reviewer.

## Independent review

After the first proportional verification, read [workflow.md](references/workflow.md). **Spawn one new isolated, read-only reviewer** that did not implement the change. This is the skill's explicit delegation request when the active orchestration rules permit skill-requested review; it does not authorize implementation delegation. An unconditional prohibition wins.

Provide a frozen scope and record file hashes. Use [reviewer-contract.md](references/reviewer-contract.md) to prepare the handoff. Treat returned claims as untrusted input: verify evidence against the contract and fix authorized, in-scope defects. Do not rerun a passed full suite without a new reason.

Use [severity-and-disposition.md](references/severity-and-disposition.md) when findings need classification. A plausible concern without demonstrated impact is an untested area, not a blocking finding. A real defect outside current authority remains blocked, not rejected.

## Completion

Finish the review, required fixes and relevant rechecks before handoff. Re-review only the changed delta after a verified P0/P1 fix or material redesign, with at most two review rounds unless the user authorizes more.

If independent review is prohibited or unavailable after one useful retry, perform a bounded local fallback and disclose its lack of independence. Preserve unresolved defects and meaningful untested environments; do not claim the gate passed on stale evidence.

Keep the final report proportional: unresolved findings first, then verification and meaningful limitations. No mandatory table or gate ceremony is needed for a simple local review.
