# ai-baton

Portable, auditable, file-first handoff protocol for AI assistants.

Lets you move between AI tools — Claude Code, Codex CLI, Cursor, or
anything else that reads/writes files — on the same long-running project
without re-explaining context every time. State lives in plain Markdown +
YAML files in your own repo: a `memory/` for durable facts and decisions,
a `status/CURRENT_STATUS.md` for what's happening right now, an
append-only `evidence/` trail, `handover/` snapshots, and `archive/` for
superseded plans. No server, no vector DB, no vendor plugin required —
every change is just a git diff.

Not the first system aiming at cross-tool AI memory — Mem0, OpenMemory,
and Letta solve overlapping problems with a vector store and/or an agent
runtime. This makes the opposite trade-off: zero infrastructure and
git-native auditability, at the cost of semantic search and automatic
extraction. See [`docs/comparison.md`](docs/comparison.md).

## Status

Pre-alpha, not on PyPI yet. Working: the spec (`SPEC.md`), the `init` /
`validate` / `status` CLI, a full worked example
(`examples/demo-project/`), and an [Agent Skills](https://agentskills.io/)
skill (`.agents/skills/ai-baton/`) that's been triggered live in
Claude Code but not yet in Codex or Cursor. 16 tests pass locally. Not
built: PyPI packaging, semantic search (by design), and any automated
measurement of handoff effectiveness (methodology sketched in
`docs/metrics.md`, nothing wired up).

## Quick orientation

- [`docs/quickstart.md`](docs/quickstart.md) — install and try it.
- [`SPEC.md`](SPEC.md) — the protocol.
- [`docs/comparison.md`](docs/comparison.md) — vs. Mem0 / OpenMemory /
  Letta / Letta Code.
- [`docs/metrics.md`](docs/metrics.md) — how we'd measure handoff quality.
- [`examples/demo-project/`](examples/demo-project/) — worked example.
- [`.agents/skills/ai-baton/SKILL.md`](.agents/skills/ai-baton/SKILL.md) —
  install once, an AI tool follows the protocol without being reminded.

## License

MIT — see [`LICENSE`](LICENSE).
