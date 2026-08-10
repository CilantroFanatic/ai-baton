---
id: 0002-adapter-retry-shape
date: 2026-08-12
confidence: verified
source: evidence/2026-08-12-retry-load-test.md
tags: [migration, adapter]
---

# Adapter retry/backoff translation is verified correct under pool exhaustion

The adapter (`../evidence/2026-08-11-adapter-implementation.md`) translates
v2's `max_retries`/`backoff_base` options into v3's `retry_policy` object.

**2026-08-12 update:** confirmed via load test
(`../evidence/2026-08-12-retry-load-test.md`) that the translated retry
behavior matches v2 under connection-pool exhaustion. Originally recorded
here as `confidence: unverified` on 2026-08-11 pending this test — promoted
to `verified` now that there's a specific tested outcome, per SPEC.md
section 6.5 (no confidence upgrade without evidence).

(Fictional example content — illustrates SPEC.md section 6.2/6.5: a memory
entry starts `unverified`, and is only promoted to `verified` after a
dated, evidence-backed confirmation, recorded in place rather than as a
new file.)
