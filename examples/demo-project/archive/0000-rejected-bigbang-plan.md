---
id: 0000-rejected-bigbang-plan
date: 2026-08-10
confidence: verified
source: evidence/2026-08-10-dependency-audit.md
superseded_by: 0001-migration-strategy
tags: [migration, rejected]
---

# Rejected: single-pass "big bang" migration

Before deciding on the module-by-module approach
(`../memory/0001-migration-strategy.md`), a single-pass rewrite of all
`northwind-api` v2 usage to v3 in one PR was considered.

Rejected because the dependency audit found 2 of 6 modules rely on
v2-specific retry/backoff options with no v3 equivalent — a big-bang PR
would have shipped all 6 modules at once with no way to verify the
retry-dependent modules independently before the others went live.

Kept here (not deleted) per SPEC.md section 3.5/6.4 — it's the reasoning
trail for why the current approach was chosen, not just the current
approach itself.

(Fictional example content.)
