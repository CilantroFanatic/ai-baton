---
name: ai-handoff-protocol
description: Use when the user wants to start, continue, or hand off a long-running project using the ai-handoff-protocol file-based memory convention (a directory with PROTOCOL.md, memory/, status/, evidence/, handover/, archive/). Triggers on requests like "start a new memory project for X", "continue the Y project", "pick up where we left off on Z", or when the current directory already contains a PROTOCOL.md file. Not for generic note-taking or one-off tasks with no need to persist state across sessions or tools.
---

# ai-handoff-protocol

Full rules: `SPEC.md` in the [ai-handoff-protocol](https://github.com/ai-handoff-protocol/ai-handoff-protocol)
repo. This skill is the condensed, self-contained version needed to operate
day to day — read `SPEC.md` itself only if something here is ambiguous.

## Step 1 — figure out which project this is, before doing anything else

Check the directory the user is pointing at (or the current working
directory, if none was named):

- **If it already has a `PROTOCOL.md`**: this is an existing
  ai-handoff-protocol project. Go to Step 2 (Existing project). Don't ask —
  the file's presence is the answer.
- **If it doesn't, and the user's intent isn't already obvious from what
  they just said**: ask directly. Don't guess and don't silently create
  something. For example:

  > "接着做已有的记忆项目,还是新开一个?接着做的话告诉我目录;新开的话告诉我叫什么名字、放哪。"
  > ("Continuing an existing memory project, or starting a new one? If
  > continuing, which directory? If new, what should it be called and where
  > should it live?")

  If the user has multiple ai-handoff-protocol projects going (e.g. one per
  exam, one for a thesis), this is the moment that keeps them from getting
  mixed together — don't assume which one "the project" means.

## Step 2a — New project

1. **Get an explicit target directory path from the user before creating
   anything.** Never default to the current directory, a guessed path, or
   anything the user didn't actually say — if Step 1's question didn't
   already get a path, ask for one now and wait for the answer. Creating a
   new project in the wrong place is exactly the "mixed together" problem
   Step 1 exists to prevent.
2. If the `ai-handoff-protocol` CLI is installed (`ai-handoff-protocol
   --help` succeeds), run:
   ```
   ai-handoff-protocol init <path>
   ```
3. If the CLI isn't installed, create the structure by hand — it's just
   files:
   ```
   <path>/PROTOCOL.md          # copy the "Rules" section below into it
   <path>/memory/INDEX.md      # frontmatter: id, date, confidence, source (see Step 3)
   <path>/status/CURRENT_STATUS.md
   <path>/evidence/
   <path>/handover/
   <path>/archive/
   ```
4. Ask the user what the actual current goal is, and write it into
   `status/CURRENT_STATUS.md`. Don't leave it as a template placeholder.

## Step 2b — Existing project

Read, in this order, before taking any other action:

1. `PROTOCOL.md`
2. `memory/INDEX.md` (and whatever it links to that's relevant)
3. `status/CURRENT_STATUS.md`

If this session might be running on a compacted/summarized context — new
session, different tool than last time, or you're not sure you have the
full picture — re-read these three now. Don't act on a remembered summary
that might be stale or fabricated.

## Step 3 — while working (applies to both new and existing)

- **Dates are always `YYYY-MM-DD`.** Never "today"/"tomorrow" — they expire
  the moment this file is read later.
- **Long-term facts/decisions go in `memory/`**, one file per fact/decision,
  with frontmatter: `id`, `date`, `confidence` (`verified` or `unverified`),
  `source`. Don't write something as `verified` unless it's actually been
  confirmed against a primary source or the user — provisional stuff is
  `unverified` until there's a specific reason to promote it (a test result,
  an explicit user confirmation), not just "seems right."
- **Raw process/detail goes in `evidence/`**, dated, append-only — never
  edit or delete a past entry, corrections are new entries.
- **`status/CURRENT_STATUS.md` gets overwritten** (not appended) after
  every significant unit of work: current goal, what's done, what's
  blocked, what's next.
- **New evidence contradicting an existing `memory/` entry**: update that
  file in place with a dated correction note — don't silently rewrite it,
  and don't delete the old evidence that's now superseded.
- **Nothing valuable gets deleted.** Superseded plans/approaches move to
  `archive/`.
- **Never write credentials** (passwords, API keys, tokens) into any file
  here.
- Before ending a session, if the CLI is available, run
  `ai-handoff-protocol validate <path>` and fix anything it flags.
