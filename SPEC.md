# ai-baton — Specification v0.1

Status: DRAFT. This is v0.1 of the protocol — expect breaking changes before v1.0.

## 1. Goals

- Let a person move between different AI assistants (Claude Code, Codex CLI,
  Cursor, or any tool with filesystem read/write) on the same long-running
  project without re-explaining state every time.
- Make every memory change reviewable as plain text: `git diff`-able,
  `git blame`-able, readable by a human without special tooling.
- Keep a permanent, append-only evidence trail so conclusions in long-term
  memory can always be traced back to what actually happened.
- Make it cheap to adopt: no server, no database, no embeddings, no vendor
  SDK. A directory of Markdown/YAML files is the entire runtime dependency.

## 2. Non-goals (v0.1)

- Semantic / vector search. Retrieval is by directory convention + grep, not
  similarity search.
- Automatic fact extraction from chat transcripts. Writing to memory is an
  explicit, attributable action (by a human or by an AI following this spec),
  not a background LLM summarization job.
- Multi-user real-time sync, hosted service, or access control.
- Running or orchestrating AI agents. This spec only defines files and
  conventions; it does not execute anything.

These may be revisited in later versions, but v0.1 is intentionally narrow.

## 3. Directory roles

A conforming project root contains:

```
memory/       long-term facts, decisions, established conventions
status/       CURRENT_STATUS.md — the single current-state source of truth
evidence/     append-only, dated raw records (logs, transcripts, reviews)
handover/     full point-in-time handover snapshots, never pruned
archive/      superseded content, moved here instead of deleted
PROTOCOL.md   the read order + update rules below, copied into the project
```

### 3.1 `memory/`

- One fact/decision/preference per file, or small grouped files by topic.
- Every file carries frontmatter (see §5). Content should be the *distilled*
  version of something established in `evidence/` — not raw transcript.
- Memory files are corrected, not silently rewritten: when new evidence
  contradicts an existing memory file, the file is updated with a dated note
  of what changed and why (see §6.3), not overwritten without a trace.

### 3.2 `status/CURRENT_STATUS.md`

- Exactly one file. It answers: current goal, what's done, what's blocked,
  what's next.
- Overwritten (not appended) after every significant unit of work. This is
  the one file a fresh AI session should trust for "what's happening right
  now."

### 3.3 `evidence/`

- Append-only. Dated entries (`YYYY-MM-DD` in filename or frontmatter).
  Nothing here is deleted or rewritten after the fact — corrections are new
  entries, not edits to old ones.
- This is where raw detail lives: full Q&A, full error output, full review
  notes. `memory/` and `status/` are allowed to be lossy summaries *because*
  the lossless version is always recoverable here.

### 3.4 `handover/`

- Full point-in-time exports of context (e.g., "everything relevant as of
  ending this session"), kept even after later summaries exist. This is the
  layer other layers are allowed to be lossy against.

### 3.5 `archive/`

- Superseded plans, old conventions, retired approaches. Moved here, never
  deleted, so history remains inspectable.

## 4. Mandatory read order

Any AI (or person) picking up a project under this protocol reads, in order,
before taking any action:

1. `PROTOCOL.md` — this file's rules, copied into the project.
2. `memory/` index (a memory file listing/linking the others).
3. `status/CURRENT_STATUS.md`.
4. Files in the directory relevant to the immediate task.

If a session suspects it is operating on a compacted/summarized context
(context window compaction, resumed session, new tool entirely), it must
re-read steps 1–3 before continuing — it must not act on a remembered
summary that might be stale or fabricated.

## 5. Frontmatter schema (memory files)

Validated against `schemas/memory-frontmatter.schema.json`. Required fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Stable identifier for the fact/decision |
| `date` | string (`YYYY-MM-DD`) | When this was established or last revised |
| `confidence` | `verified` \| `unverified` | Whether this has been confirmed against a primary source, or is still provisional |
| `source` | string | Where this came from (evidence file path, user statement, external doc) |

Optional fields: `superseded_by` (id of the memory file that replaces this
one, if any), `tags` (array of strings).

## 6. Update discipline

### 6.1 Absolute dates

Always `YYYY-MM-DD`. Never "today", "yesterday", "next week" — those expire
and become misleading the moment the file is read in a later session.

### 6.2 Unverified content is tagged, not assumed

Anything not confirmed against a primary source or the user is written with
`confidence: unverified`. It is not promoted to `verified` without an
explicit confirmation step, logged in `evidence/`.

### 6.3 Conflict resolution

When new evidence contradicts an existing `memory/` entry: do not delete the
old entry silently. Update the memory file with a dated correction, and
leave the evidence trail (old and new) intact in `evidence/`. The append-only
evidence layer is what makes this auditable after the fact.

### 6.4 Nothing valuable is deleted

Superseded content moves to `archive/`. Deletion is reserved for genuinely
worthless content (duplicates, empty files) — not for anything a future
session might need to reconstruct "why did we do it this way."

### 6.5 No score/status inflation without evidence

If a project tracks any kind of progress/readiness score, changes to that
score must cite a specific `evidence/` entry. "Read about it" / "looked at
the docs" is not evidence of capability; a specific tested outcome is.

### 6.6 Sensitive data

Passwords, API keys, tokens, and other credentials are never written into
any file under this protocol.

## 7. Versioning

This file's version applies to the whole protocol. Breaking changes to
directory roles or required frontmatter fields bump the minor version pre-1.0
and the major version post-1.0. Projects should record which protocol
version they conform to (e.g., in `PROTOCOL.md`'s header).
