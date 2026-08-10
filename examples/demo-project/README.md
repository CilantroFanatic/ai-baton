# demo-project (fictional example)

**Status: structure only.** This directory shows the shape a project takes
under `ai-handoff-protocol` v0.1 — it is not yet a complete, runnable
walkthrough. Filling it in with a full multi-session scenario is Day 3 work
(see `docs/PHASE1_DESIGN.md` in the repo root).

## Scenario

Entirely fictional, for demonstration only: a small team is migrating a
library called `northwind-api` from v2 to v3 across several sessions,
switching between two different AI coding assistants. This is a stand-in
for "any long-running project handed between AI tools" — it is not based on
any real project or real data.

## What's here so far

- `PROTOCOL.md` — the read-order/update rules a session should follow in
  this project.
- `memory/` — one example long-term-memory entry, plus an index.
- `status/CURRENT_STATUS.md` — one example current-state snapshot.
- `evidence/` — one example dated evidence entry.
- `handover/`, `archive/` — present per spec, currently empty (no snapshot
  or superseded content exists yet in this fictional timeline).

Once the CLI's `validate` command exists (Day 2), this directory becomes the
thing CI runs `validate` against, so the spec and the example can't drift
apart silently.
