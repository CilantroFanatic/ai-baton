# ai-baton

[中文](README.zh-CN.md)

Portable, auditable, file-first handoff protocol for AI assistants.

Lets you move between AI tools — Claude Code, Codex CLI, Cursor, GitHub
Copilot, or anything else that reads/writes files — on the same
long-running project without re-explaining context every time. State
lives in plain Markdown + YAML files in your own repo, readable with
`git diff`. No server, no vector DB, no vendor plugin required.

## When you'd use this

- **Switching tools on the same project.** You worked out an approach in
  Claude Code — tech choices made, dead ends already ruled out — and now
  want to keep going in Cursor, without re-explaining any of it.
- **Bouncing between tools day to day.** Cursor at the office, Claude Code
  at home; or two people on the same repo using different tools. Everyone
  reads the same files instead of re-syncing state by hand.
- **A conversation that's gotten too long to just re-paste.** Starting a
  fresh session — to save tokens, or because quality degrades on very
  long context — shouldn't mean losing everything. A few hundred words of
  distilled state beats re-sending a whole transcript.

## How it works

- `PROTOCOL.md` — the rules this project follows
- `memory/` — durable facts and decisions, one file each, tagged
  `confidence: verified` or `unverified`
- `status/CURRENT_STATUS.md` — what's happening right now (overwritten
  each time, not appended)
- `evidence/` — raw detail worth keeping, append-only
- `handover/` / `archive/` — point-in-time snapshots / superseded plans —
  nothing gets deleted

Install the [Agent Skills](https://agentskills.io/) skill once
(`ai-baton skill install`) and a supporting AI tool follows this
automatically: reads the right files in the right order, asks before
writing, keeps state current — without being reminded every session.

Requires local filesystem access — works with tools that run on your
machine or have been granted access to a folder (Claude Code, Codex CLI,
Cursor, Windsurf, Claude Desktop with a filesystem connector, etc.). Plain
web ChatGPT or web Claude.ai chat can't read `PROTOCOL.md` at all — no
file access, so Agent Skills support doesn't help there.

## Status

Pre-alpha.

**Working:**
- The spec (`SPEC.md`) and CLI — `pip install ai-baton-tool` (the PyPI
  distribution name; an unrelated existing package blocked plain
  `ai-baton`, but the command itself is still `ai-baton`): `init` /
  `validate` / `status` / `list` / `workspace set` / `skill install`
- A default workspace convention — `~/ai-baton-workspace/<project>/`,
  root chosen once and remembered, projects discoverable across
  tools/sessions via `ai-baton list`
- A full worked example (`examples/demo-project/`)
- `validate` flags well-known credential formats (heuristic safety net,
  not a full secrets scanner) and warns when `memory/` is getting large
  enough to cost real tokens every session (threshold configurable per
  project via `.ai-baton.json`)
- Clean error messages on bad paths instead of raw Python tracebacks
- 49 tests passing locally

**Verified live** (real user tests, not just design review): the skill
triggers correctly in Claude Code, Codex CLI, and GitHub Copilot. The
Copilot test directly found — and led to fixing — two real bugs: reading
an unrelated sibling project's files into a brand-new project, and
skipping the required backfill question. Codex CLI's guided-question UI
and canary tag weren't confirmed showing up there; unclear whether that's
a real compliance gap or Codex correctly falling back to plain text.
Not yet tested in Cursor, though Cursor's own docs say it reads skills
from the same locations this tool installs into.

**Not built:** semantic search (by design — see the trade-off below), and
any automated measurement of handoff effectiveness (methodology sketched
in `docs/metrics.md`, nothing wired up yet).

Not the first system aiming at cross-tool AI memory — Mem0, OpenMemory,
and Letta solve overlapping problems with a vector store and/or an agent
runtime. This makes the opposite trade-off: zero infrastructure and
git-native auditability, at the cost of semantic search and automatic
extraction. See [`docs/comparison.md`](docs/comparison.md).

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
