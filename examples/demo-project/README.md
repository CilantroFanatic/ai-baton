# demo-project (fictional example)

A worked, multi-session example of `ai-baton` v0.1, entirely
fictional: a small team migrating a library called `northwind-api` from v2
to v3, handed between two different AI coding assistants across three
sessions. Not based on any real project or real data.

Validate it yourself:

```bash
ai-baton validate examples/demo-project
ai-baton status examples/demo-project
```

## The narrative

**Session 1 — 2026-08-10 (tool A).** Audits the codebase
(`evidence/2026-08-10-dependency-audit.md`), considers and rejects a
big-bang rewrite (`archive/0000-rejected-bigbang-plan.md`), decides on a
module-by-module migration behind an adapter
(`memory/0001-migration-strategy.md`).

**Session 2 — 2026-08-11 (tool B, a different AI tool).** Picks the project
up cold — in a real session this would start with `ai-baton
status .`, which prints `PROTOCOL.md` + `memory/INDEX.md` +
`status/CURRENT_STATUS.md` in the order SPEC.md section 4 requires. Builds
the HTTP client adapter (`evidence/2026-08-11-adapter-implementation.md`),
but isn't sure the retry/backoff translation is correct under connection
pool exhaustion, so records that as `confidence: unverified` rather than
asserting it
(`memory/0002-adapter-retry-shape.md`). Leaves a full point-in-time
handover snapshot before the session ends
(`handover/2026-08-11-session-end-snapshot.md`).

**Session 3 — 2026-08-12 (back to tool A).** Re-reads the mandatory files,
runs the load test that was flagged as missing, confirms the adapter's
retry behavior is correct
(`evidence/2026-08-12-retry-load-test.md`), and promotes
`memory/0002-adapter-retry-shape.md` from `unverified` to `verified` —
*in place*, with a dated note, not as a new file. While migrating the
second module, finds the original audit undercounted which modules do
writes (`evidence/2026-08-12-second-module-audit-correction.md`) and
appends a dated correction to `memory/0001-migration-strategy.md` instead
of silently rewriting it, per SPEC.md section 6.3.

## What this demonstrates

- Cross-tool handoff via `status/CURRENT_STATUS.md` +
  `memory/INDEX.md`, not shared chat history.
- `confidence: unverified` → `verified` promotion gated on a specific
  tested outcome (SPEC.md §6.2/§6.5), not "looked fine to me."
- Conflicting new evidence correcting an existing `memory/` entry in place,
  with the old evidence kept intact (SPEC.md §6.3).
- `archive/` holding a rejected approach instead of deleting it (SPEC.md
  §3.5/§6.4).
- `handover/` holding a full point-in-time snapshot, separate from the
  terser `status/CURRENT_STATUS.md`.

Once the CLI's `validate` command runs in CI, this directory is what CI
checks against, so the spec and the example can't drift apart silently.
