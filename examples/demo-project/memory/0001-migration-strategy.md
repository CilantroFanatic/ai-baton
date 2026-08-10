---
id: 0001-migration-strategy
date: 2026-08-10
confidence: verified
source: evidence/2026-08-10-dependency-audit.md
tags: [migration, decision]
---

# Decision: migrate `northwind-api` module by module, not in one pass

We chose an incremental, module-by-module migration from v2 to v3 instead of
a single big-bang rewrite, because the v2 → v3 breaking changes are
concentrated in the HTTP client layer and can be isolated behind an adapter.

This lets each module be migrated and verified independently, so a partial
migration still leaves the project in a working state.

(Fictional example content — illustrates the expected level of detail for a
`memory/` entry: one decision, the reasoning, and a pointer to the evidence
it's based on.)
