# ai-handoff-protocol

Portable, auditable, file-first handoff protocol for AI assistants.

Status: **pre-alpha**. The spec and a working CLI MVP exist and pass their
tests locally; nothing has been tagged as a release or published to PyPI
yet. This project defines a convention and a small CLI for sharing
long-term facts, current task state, and historical evidence between
different AI coding assistants — Claude Code, Codex CLI, Cursor, or
anything else that can read and write files — working on the same
long-running project.

## What this is

- A directory/file convention (`SPEC.md`) so that any AI tool with
  filesystem access can pick up a project mid-stream: what's the current
  goal, what's already decided, what's still unverified, what happened and
  when.
- Plain Markdown + YAML frontmatter. No server, no vector database, no
  embeddings, no vendor-specific plugin required to participate.
- Every change is a text diff — reviewable in `git log` / `git blame` /
  a pull request, the same way you'd review code.

## What this is not

- Not the first cross-product AI memory system. [Mem0](https://github.com/mem0ai/mem0),
  [OpenMemory](https://github.com/CaviraOSS/OpenMemory), and
  [Letta](https://github.com/letta-ai/letta) all solve overlapping problems,
  generally via a vector store and/or a running agent runtime. This project
  makes a different, narrower trade-off: zero infrastructure and
  git-native auditability, at the cost of semantic search and automatic
  fact extraction. See [`docs/comparison.md`](docs/comparison.md).
- Not a hosted service, not multi-user, not an agent framework.
- Not finished. See "Current status" below before assuming anything here
  works yet.

## Current status

Implemented:
- [x] `SPEC.md` v0.1 — directory roles, frontmatter schema, read order,
      update discipline.
- [x] `schemas/memory-frontmatter.schema.json`.
- [x] `init` / `validate` / `status` CLI commands (Python, `src/ai_handoff_protocol/`),
      with a pytest suite (13 tests) covering scaffolding, idempotency,
      frontmatter/link/staleness validation, and read-order output.
- [x] CI (`.github/workflows/validate.yml`) runs `pytest` and
      `ai-handoff-protocol validate examples/demo-project` — no longer a
      placeholder, but also not yet exercised on GitHub Actions itself
      (verified locally via a venv; `uv` wasn't available in this
      environment to test the exact CI command path).

Not implemented / not yet true — don't assume otherwise:
- [ ] Not published to PyPI. `uvx ai-handoff-protocol` will not work yet;
      only a local editable install does.
- [ ] `examples/demo-project` is a single static snapshot (one memory
      entry, one evidence entry) that validates cleanly, but it does not
      yet demonstrate an actual multi-session, multi-tool handoff — that
      walkthrough is still planned (Day 3).
- [ ] No semantic search, no automatic fact extraction (by design — see
      `docs/comparison.md` — not a gap to be filled later).
- [ ] Any quantitative handoff-effectiveness measurement (see
      [`docs/metrics.md`](docs/metrics.md) for the planned methodology —
      none of it is automated yet).

## Quick orientation

- [`SPEC.md`](SPEC.md) — the protocol itself.
- [`docs/comparison.md`](docs/comparison.md) — how this differs from
  Mem0 / OpenMemory / Letta / Letta Code, including honest limitations.
- [`docs/metrics.md`](docs/metrics.md) — how we plan to measure whether
  cross-AI handoff actually works, once there's something to measure.
- [`examples/demo-project/`](examples/demo-project/) — a fictional example
  project structured per the spec (skeleton only for now).

## License

MIT — see [`LICENSE`](LICENSE).
