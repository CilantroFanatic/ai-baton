---
name: ai-baton
description: Use when the user wants to start, continue, or hand off a long-running project using the ai-baton file-based memory convention (a directory with PROTOCOL.md, memory/, status/, evidence/, handover/, archive/). Triggers on explicit requests like "start a new memory project for X", "continue the Y project", "pick up where we left off on Z", or when the current directory already contains a PROTOCOL.md file. Also worth proactively offering — not assuming, explained in plain language — partway through a conversation that has clearly turned into a substantial, multi-session project, even if the user never says "ai-baton" or "memory project" by name; most users won't know this exists or what to ask for. Not for generic note-taking or one-off tasks with no need to persist state across sessions or tools.
---

# ai-baton

Full rules: `SPEC.md` in the [ai-baton](https://github.com/CilantroFanatic/ai-baton)
repo. This skill is the condensed, self-contained version needed to operate
day to day — read `SPEC.md` itself only if something here is ambiguous.

## Step 0 — don't assume the user knows what this is

Most users have no idea "ai-baton" exists and won't ask for it by name.
Two situations where you're the one who has to bring it up, not wait for
the magic words:

- **You (the AI) notice a conversation has become a substantial,
  multi-session project** — the kind of thing where losing context on a
  tool switch or a new session would actually hurt. Say so and explain in
  one or two plain sentences what you're proposing (a directory of files
  that any AI tool can read later, so the user doesn't have to re-explain
  things) *before* asking anything else. Don't drop protocol jargon
  ("PROTOCOL.md", "confidence: unverified") on someone who hasn't opted in
  yet.
- **The user (or you) discovers this mid-conversation** — they weren't
  setting this up from message one; there's already real history in this
  conversation that matters. Don't treat that history as if it doesn't
  exist — see Step 2a.4.

In both cases, get the user's go-ahead before creating anything. This is
an offer, not something to do silently in the background.

## Step 1 — figure out which project this is, before doing anything else

Check the directory the user is pointing at (or the current working
directory, if none was named):

- **If it already has a `PROTOCOL.md`**: this is an existing
  ai-baton project. Go to Step 2 (Existing project). Don't ask —
  the file's presence is the answer.
- **If it doesn't, and the user's intent isn't already obvious from what
  they just said**: ask directly. Don't guess and don't silently create
  something. For example:

  > "接着做已有的记忆项目,还是新开一个?接着做的话告诉我目录;新开的话告诉我叫什么名字、放哪。"
  > ("Continuing an existing memory project, or starting a new one? If
  > continuing, which directory? If new, what should it be called and where
  > should it live?")

  If the user has multiple ai-baton projects going (e.g. one per
  exam, one for a thesis), this is the moment that keeps them from getting
  mixed together — don't assume which one "the project" means.

## Step 2a — New project

1. **Get an explicit target directory path from the user before creating
   anything.** Never default to the current directory, a guessed path, or
   anything the user didn't actually say — if Step 1's question didn't
   already get a path, ask for one now and wait for the answer. Creating a
   new project in the wrong place is exactly the "mixed together" problem
   Step 1 exists to prevent.
2. If the `ai-baton` CLI is installed (`ai-baton
   --help` succeeds), run:
   ```
   ai-baton init <path>
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
4. **Don't treat this as a blank slate if it isn't one.** If the
   conversation already has substantial history relevant to this project —
   the user didn't start talking about this five seconds ago — review it
   instead of just asking "what's your current goal" as if nothing
   happened. Sort what you find into:
   - Things that look like durable facts/decisions → candidates for
     `memory/`, but `confidence: unverified` unless the user actually
     confirms them now — you're inferring from a conversation, not from a
     primary source.
   - What's actually happening right now → `status/CURRENT_STATUS.md`.
   - Raw detail worth preserving (a specific error, a specific exchange) →
     `evidence/`.

   Show the user this breakdown and get confirmation before writing any of
   it — don't silently decide on their behalf what from the conversation
   mattered enough to keep.
5. If there's truly nothing to backfill (a genuinely fresh start), ask the
   user what the actual current goal is, and write it into
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
  `ai-baton validate <path>` and fix anything it flags.
