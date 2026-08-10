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

**How you ask matters as much as what you ask.** If your environment
offers a structured/interactive question mechanism (multiple-choice with
a free-text fallback, buttons, whatever your host supports) — use it
instead of a plain open paragraph, every time you ask the user something
in this skill: Step 1's new-vs-existing question, the project name/goal
in Step 2a, the backfill confirmation in Step 2a.4. This holds even when
the real answer is open-ended (e.g. "what do you want to track") — offer
a few illustrative categories (thesis, exam prep, job search, whatever
fits the conversation) as quick picks, with "something else" as an
explicit option that lets them type freely. A guided pick-one-or-type-
your-own beats a blank prompt, especially for someone who's never heard of
this before (that's the whole point of Step 0). If your environment has no
such mechanism, plain text is fine — this is about using what's
available, not requiring a specific tool.

**Never create a throwaway "demo" or "example" project just to show the
tool working** — even if the user literally said "install this and try
it out." That's not a reason to invent fake content; it's an opening to
ask what they'd actually want to track, and set *that* up for real. The
trial run and the first real project should be the same thing. (If they
want to see a worked example first, point them at
[`examples/demo-project/`](https://github.com/CilantroFanatic/ai-baton/tree/main/examples/demo-project)
in the repo instead of building a new one.)

## Step 1 — figure out which project this is, before doing anything else

If the user named or is obviously pointing at a specific directory, check
that directory for `PROTOCOL.md` and skip to the outcome below. Otherwise,
don't guess and don't ask blind — **check the default workspace first**:

```
ai-baton list
```

(scans `~/ai-baton-workspace/` — cross-platform, resolved by the CLI, not
something you need to construct by hand. No CLI available? List that
directory yourself the same way: subdirectories containing `PROTOCOL.md`
are existing projects.)

- **The workspace has one or more projects**: show them to the user (name
  + whatever current-goal line `list` printed) and ask which one, or
  whether this is a new one. This is what lets someone switch to a
  different AI tool later and actually find their existing projects
  instead of having to remember and retype a path.
- **The workspace is empty or doesn't exist yet, and a specific directory
  wasn't named**: this is a new project. Go to Step 2a — it defaults new
  projects into the workspace automatically.
- **A `PROTOCOL.md` was found** (in a named directory, or picked from the
  workspace list): existing project. Go to Step 2b. Don't ask — the file's
  presence is the answer.
- **None of the above resolved it** (e.g. multiple candidates and the
  user's intent still isn't clear): ask directly, don't guess. For
  example:

  > "接着做已有的记忆项目,还是新开一个?接着做的话告诉我是哪个;新开的话告诉我叫什么名字。"
  > ("Continuing an existing memory project, or starting a new one? If
  > continuing, which one? If new, what should it be called?")

  If the user has multiple ai-baton projects going (e.g. one per exam, one
  for a thesis), this is the moment that keeps them from getting mixed
  together — don't assume which one "the project" means.

## Step 2a — New project

1. **Default new projects to `~/ai-baton-workspace/<project-name>/`** —
   pick or confirm `<project-name>` with the user (short, descriptive:
   `ielts-prep`, `thesis`, not "project" or "new-project"). The workspace
   itself is never a project — it's a container, and every project gets
   its own named subdirectory inside it, one per thing the user is
   tracking (`~/ai-baton-workspace/ielts-prep/`,
   `~/ai-baton-workspace/thesis/`, etc.), the same way Step 1's `ai-baton
   list` finds them later. Never write `PROTOCOL.md` directly into the
   workspace root.
1a. **Only deviate from the workspace default if the user explicitly wants
   somewhere else** — e.g. "put it inside this repo I'm working on" is a
   legitimate reason to use a different path. But if they name a general-
   purpose folder they already use for other things ("put it in
   Documents," "in my home folder"), don't scaffold directly into that
   folder either — it already has unrelated stuff in it (other projects,
   `node_modules/`, whatever), and dumping `PROTOCOL.md` straight into it
   pollutes it and breaks `validate`/`skill` scripting for everything else
   living there. Create a project-named subdirectory inside whatever they
   named instead, same principle as the workspace default.
1b. **Don't hardcode a Unix-style path (`~/...`, `/Users/...`) and assume
   it's right.** Home directories and separators differ by OS (Windows:
   `C:\Users\<name>\...`). If you're running `ai-baton` commands, this is
   handled for you (the CLI resolves the actual home directory itself). If
   you're constructing a path yourself in prose or a manual fallback,
   confirm the real path for the user's actual OS instead of assuming
   macOS/Linux conventions.
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
- **If `validate` warns that `memory/` is getting large** (SPEC.md §6.7):
  review it, but don't ask the user to approve archiving one entry at a
  time — that doesn't scale past a handful of items. Propose a batch: list
  the candidates (still true, just rarely relevant) with one line of
  reasoning each, get one combined go-ahead, then move them to `archive/`.
  Don't evict by recency alone — a fact being rarely referenced doesn't
  mean it's unimportant. If the project genuinely needs a bigger active
  index, raising the threshold in `.ai-baton.json` is a legitimate answer
  too, not just archiving.
- Before ending a session, if the CLI is available, run
  `ai-baton validate <path>` and fix anything it flags.
