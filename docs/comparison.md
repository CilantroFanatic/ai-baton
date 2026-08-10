# Comparison with existing approaches

This project is not the first system aiming at cross-tool AI memory. This
page is an honest comparison, including where existing tools are more
capable than this one.

| | Storage / runtime | How memory is produced | Auditability | Dependencies |
|---|---|---|---|---|
| **Mem0** | Vector store (default Qdrant) + Postgres; library or self-hosted service | LLM auto-extracts "facts" from conversations | Low — memory is vectors + LLM summary, not directly diffable against its original basis | Vector store + DB, or managed cloud |
| **OpenMemory (MCP)** | Local MCP server, Qdrant + SSE | Same extraction as Mem0, exposed to MCP clients (Claude Desktop, Cursor, Windsurf, …) | Medium — local, but still a vector store, not plain text | A locally-running service process + MCP-capable client |
| **Letta (MemGPT)** | Postgres + pgvector; core memory blocks live in the agent's context | The agent calls `core_memory_*` / `archival_memory_*` tools on itself | Low–medium — memory blocks are readable, but scoped to one Letta agent instance, not a portable file set | Letta's agent runtime/server |
| **Letta Code** | Built on Letta; memory bound to one long-lived agent | The agent accumulates memory/skills about a working directory over time | Medium — but scoped to a single Letta agent, not shared across independently-run tools like Claude Code / Codex / Cursor | Letta runtime; it's Letta's own CLI product |
| **ai-handoff-protocol** | Plain text files (Markdown + YAML frontmatter) in a git repo | Explicit writes by a human or an AI following the spec | High — every change is a normal git diff | None (no DB, no vector store, no server) |

## What we give up for that trade-off

- **No semantic search.** Finding a memory is directory convention + grep,
  not similarity search over embeddings. For very large memory stores where
  you don't know what you're looking for, Mem0-style retrieval will beat
  this.
- **No automatic extraction.** Nothing here reads a chat transcript and
  decides what's worth remembering for you. That's deliberate — automatic
  extraction is also automatic, silent, unauditable loss — but it means the
  protocol only works if whoever's driving (human or AI) actually follows
  the update discipline in `SPEC.md` §6.
- **Single machine / single repo by default.** No hosted sync, no
  multi-user access control. Out of scope for v0.1.

## What we're betting on instead

- Zero infrastructure: any tool that can read/write files can participate,
  with no MCP integration, no SDK, no running service.
- Human-reviewable history: you can open a pull request against someone's
  `memory/` change and review it like code, which none of the vector-backed
  systems above support natively.
- Complementary to [AGENTS.md](https://agents.md/): AGENTS.md is a static,
  one-time "how to work in this repo" file; this protocol is the dynamic,
  evolving state/evidence layer AGENTS.md explicitly doesn't cover. A
  project can use both — an `AGENTS.md` that points at this protocol's
  directories.
