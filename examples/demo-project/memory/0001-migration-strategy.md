---
id: 0001-migration-strategy
date: 2026-08-12
confidence: verified
source: evidence/2026-08-10-dependency-audit.md
tags: [migration, decision]
---

# Decision: migrate `northwind-api` module by module, not in one pass

We chose an incremental, module-by-module migration from v2 to v3 instead of
a single big-bang rewrite, because the v2 → v3 breaking changes are
concentrated in the HTTP client layer and can be isolated behind an adapter.
The rejected big-bang alternative is kept at
`../archive/0000-rejected-bigbang-plan.md`.

This lets each module be migrated and verified independently, so a partial
migration still leaves the project in a working state.

**2026-08-12 correction:** the original audit's claim that "4 of 6 modules
only use the client for read-only GET calls" was wrong for one module
(`payments-webhook` also does a POST for cache invalidation) — see
`../evidence/2026-08-12-second-module-audit-correction.md`. Doesn't change
the migration approach (the adapter already handles POST), but the "4 of 6
read-only" detail from the original audit should not be trusted as-is.

(Fictional example content — illustrates the expected level of detail for a
`memory/` entry: one decision, the reasoning, a pointer to the evidence it's
based on, and — per SPEC.md section 6.3 — a dated in-place correction when
later evidence contradicts part of it, instead of a silent rewrite.)
