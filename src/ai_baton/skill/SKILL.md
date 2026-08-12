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
  exist — see Step 2a Question 2 (or Step 2b's version of the same check
  for an existing project).

In both cases, get the user's go-ahead before creating anything. This is
an offer, not something to do silently in the background.

**How you ask matters as much as what you ask.** If your environment
offers a structured/interactive question mechanism (multiple-choice with
a free-text fallback, buttons, whatever your host supports) — use it
instead of a plain open paragraph, every time you ask the user something
in this skill: Step 1's new-vs-existing question, the project name/goal
in Step 2a, the backfill confirmation in Step 2a's Question 2 (and Step
2b's equivalent). This holds even when
the real answer is open-ended (e.g. "what do you want to track") — offer
a few illustrative categories (thesis, exam prep, job search, whatever
fits the conversation) as quick picks, with "something else" as an
explicit option that lets them type freely. A guided pick-one-or-type-
your-own beats a blank prompt, especially for someone who's never heard of
this before (that's the whole point of Step 0). If your environment has no
such mechanism, plain text is fine — this is about using what's
available, not requiring a specific tool.

**Order options with the recommended pick first, decline/skip last.** If
one option is what you'd actually suggest, lead with it; put "no need" /
"skip this" / "not now" at the end of the list, not the front — don't bury
the recommendation or make the exit the first thing the user sees.

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

(No CLI available? Read `<workspace>/.ai-baton-workspace.json` yourself if
it exists — `{"projects": {"<name>": {"description": "...", "updated":
"YYYY-MM-DD"}}}` — instead of opening every project's own files. Only fall
back to listing subdirectories containing `PROTOCOL.md` by hand if that
manifest is missing or unreadable, and even then that's just for names —
see the next paragraph.)

- **The workspace has one or more projects**: show them to the user (name
  + whatever current-goal line `list` printed) and ask which one, or
  whether this is a new one. This is what lets someone switch to a
  different AI tool later and actually find their existing projects
  instead of having to remember and retype a path.
- **The workspace is empty or doesn't exist yet, and a specific directory
  wasn't named**: this is a new project. Go to Step 2a.
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

**Other projects in the workspace are not context for this one.**
`ai-baton list` (or the workspace manifest, or manually checking for
`PROTOCOL.md`) exists only to find project *names* and their one-line
descriptions, so the user can pick which one they mean. Once you've
resolved that, never open a *different* project's `memory/`, `status/`, or
`evidence/` files and fold their content into the project you're creating
or working on — not even if it looks topically related or recent. A live
test found an AI doing exactly this: creating a brand-new project and
silently pre-filling its `CURRENT_STATUS.md` from an unrelated sibling
project's status file, without asking. If something from another existing
project genuinely belongs here, that's the user's explicit call to make
(they can say so, or paste it themselves) — not something to infer by
reading their other projects' files.

## Step 2a — New project: three fixed questions, in this order

A new project always goes through these three questions, in this order.
Each one names its own condition for skipping — don't skip for any other
reason (topic "seems obvious," feels redundant, etc.), and don't reorder
them. This exists because live testing kept finding sessions that quietly
dropped one of these — asking blind, defaulting a path without asking,
skipping the backfill question — usually because the AI judged for itself
that a step wasn't needed instead of just asking.

**If you notice you're already creating or writing project files and
can't point to an actual asked-and-answered exchange for one of these
three questions** (not "I meant to," not "it seemed obvious" — a real
question was asked and the user actually responded), stop right where you
are and ask it now, even mid-task. Retroactively asking after the fact
defeats the point as much as not asking at all — the user should confirm
before content exists, not be told what was already written.

### Question 1 — where should this live?

**Skip this question only if a workspace root has already been
established** — either `~/.ai-baton/config.json` exists, or a
`~/ai-baton-workspace/` directory already exists. If neither exists yet,
this is genuinely the first time, and defaulting silently is exactly the
mistake this question prevents:

> "Use the default location (`~/ai-baton-workspace`), or somewhere else?"
> (guided question if available, default option first per the ordering
> rule in Step 0)

If they pick somewhere else, run `ai-baton workspace set <path>` to
remember it — a one-time question, not a recurring one. If the path
they give is unusable, the CLI's error says so plainly (not a raw
traceback); tell them it's not accessible and ask for a different one —
don't guess or fall back silently.

Once the root is settled, get the project name too (short, descriptive:
`ielts-prep`, `thesis`, not "project"): the project lives at
`<root>/<project-name>/`. The workspace root is never itself a project —
every project is its own named subdirectory inside it, the same way
`ai-baton list` finds them later. Never write `PROTOCOL.md` directly into
the workspace root.

Only deviate from the workspace default if the user explicitly wants
somewhere else — e.g. "put it inside this repo I'm working on" is a
legitimate reason. But if they name a general-purpose folder they already
use for other things ("put it in Documents," "in my home folder"), don't
scaffold directly into that folder either — create a project-named
subdirectory inside whatever they named, same principle as the workspace
default; that folder already has unrelated stuff in it and dumping
`PROTOCOL.md` straight into it pollutes it.

Don't hardcode a Unix-style path (`~/...`, `/Users/...`) and assume it's
right — home directories and separators differ by OS (Windows:
`C:\Users\<name>\...`). Running `ai-baton` commands handles this for you;
constructing a path yourself in prose or a manual fallback needs the real
path for the user's actual OS.

### Question 2 — is this related to what we've already been discussing?

**Always ask this for a new project — never decide it silently, in
either direction.** Judging "is there relevant prior context" yourself is
a call that can be wrong both ways: skipping real context you decided
didn't look relevant, or dragging in unrelated earlier discussion into a
project that's actually about something else. Ask explicitly:

> "这个跟咱们之前聊的内容有关吗?要不要我回顾一下这段对话,把相关的东西整理进去?"
> ("Is this related to what we've already been discussing? Want me to
> review this conversation and pull in anything relevant?")

- **If yes**: review it, then sort what you find into:
  - Things that look like durable facts/decisions → candidates for
    `memory/`, but `confidence: unverified` unless the user actually
    confirms them now — you're inferring from a conversation, not from a
    primary source.
  - What's actually happening right now → feeds into Question 3.
  - Raw detail worth preserving (a specific error, a specific exchange) →
    `evidence/`.

  Show the user this breakdown and get confirmation before writing any of
  it — don't silently decide on their behalf what from the conversation
  mattered enough to keep.
- **If no** (a genuinely unrelated fresh topic, e.g. a new PPT on
  something else entirely): treat Question 3 as a blank start.

### Question 3 — what's the current goal?

If Question 2's backfill already surfaced a clear current state, confirm
it rather than re-asking from scratch. Otherwise ask directly what the
actual current goal is. Either way, write it into
`status/CURRENT_STATUS.md` — don't leave it as a template placeholder.

Then create the project structure. If the `ai-baton` CLI is installed
(`ai-baton --help` succeeds), run:
```
ai-baton init <path>
```
If the CLI isn't installed, create the structure by hand — it's just
files:
```
<path>/PROTOCOL.md          # copy the "Rules" section below into it
<path>/memory/INDEX.md      # frontmatter: id, date, confidence, source (see Step 3)
<path>/status/CURRENT_STATUS.md
<path>/evidence/
<path>/handover/
<path>/archive/
```

## Step 2b — Existing project

Read, in this order, before taking any other action:

1. `PROTOCOL.md`
2. `memory/INDEX.md` (and whatever it links to that's relevant)
3. `status/CURRENT_STATUS.md`

If this session might be running on a compacted/summarized context — new
session, different tool than last time, or you're not sure you have the
full picture — re-read these three now. Don't act on a remembered summary
that might be stale or fabricated.

**This isn't only a new-project question — ask it here too.** If this
conversation already has discussion relevant to the project from before
you picked it up (the user was talking about it, or something adjacent,
earlier in this same session), don't silently decide whether that's
worth capturing. Ask, the same way Step 2a's Question 2 does: "这段对话里
有跟这个项目相关的新内容吗?要不要我看看有没有该更新进去的?" ("Is there
anything relevant to this project earlier in this conversation? Want me
to check whether anything should be added?"). If yes, sort it the same
way — durable facts to `memory/` (unverified unless confirmed), current
state to `status/CURRENT_STATUS.md`, raw detail to `evidence/` — and
confirm the breakdown before writing.

Self-assessment here is inherently unreliable — a session that's actually
lost instructions is often the one least able to notice it did. If
`PROTOCOL.md`'s "Project-specific rules" defines a canary instruction
(e.g. ending every reply with `[baton: held]`), that's an external,
observable signal instead: follow it every reply, and if you notice
yourself having skipped it, treat that as a sign to re-read now rather
than pushing through.

## Step 3 — while working (applies to both new and existing)

**When to actually write, not just where.** Structure without a trigger
is useless — here's what should make you write something right then,
not queue it up as "remember this for later":

- **A decision gets made, or a fact gets confirmed** → write it to
  `memory/` immediately. Don't wait to be asked, and don't wait for the
  session to end — by the time anyone thinks to say "remember this,"
  it should already be written. Capture the *why*, briefly, not just the
  conclusion — context compaction (in this tool or any other) is built to
  discard intermediate reasoning while keeping decisions, so once it fires
  the reasoning behind a choice is gone unless it was already written down
  here. This isn't only a cross-tool concern; it happens within a single
  long session too.
- **Something about the current situation changes** — a blocker appears
  or clears, the next step changes, the goal shifts → update
  `status/CURRENT_STATUS.md` right then, not just at the end.
- **A specific exchange is worth being able to reconstruct later** (a
  real error and its real fix, a substantive answer to a substantive
  question) → append it to `evidence/` at that point, not reconstructed
  from memory afterward.
- **Before ending a session, or when the user signals they're wrapping
  up** → do a final `status/CURRENT_STATUS.md` pass and run `ai-baton
  validate <path>` if the CLI is available (see the bullet on this
  further down) — this is a backstop, not the only time writing happens.
- **You're deliberately handing off** — ending a session expecting a
  different tool, or a different person, to pick this up next → write a
  full point-in-time snapshot to `handover/` (SPEC.md §3.4), not just the
  routine `status/CURRENT_STATUS.md` update. This is richer, and once
  written it's permanent — unlike `status/`, later sessions don't
  overwrite it, so it's still readable as "what things looked like right
  then" long after `status/` has moved on. Don't do this at the end of
  every session, only when an actual handoff is happening — otherwise the
  routine `status/CURRENT_STATUS.md` update is enough.

Waiting until the end of a long session to write everything at once
defeats the point — detail gets lost, and it's exactly the kind of
"significant work happened but nothing was recorded" gap this protocol
exists to prevent.

- **Dates are always `YYYY-MM-DD`.** Never "today"/"tomorrow" — they expire
  the moment this file is read later.
- **Write `memory/` and `status/` entries densely, not narratively.** These
  files get re-read in full at the start of every future session — a
  padded paragraph costs tokens every time it's loaded, not just once.
  State the fact/decision/current-state directly; skip scene-setting,
  hedging, and restating the question. Still write complete, clear
  sentences — this isn't "be cryptic," just "don't carry chat filler into
  a file that gets paid for on every read."
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
- **If the `ai-baton` CLI is available, running `ai-baton validate <path>`
  also refreshes this project's one-line entry in the parent workspace's
  `.ai-baton-workspace.json`** — that's what keeps `ai-baton list` fast and
  accurate without opening every project's files (see Step 1). If the CLI
  isn't available and you're hand-editing `CURRENT_STATUS.md`, also
  hand-update this project's entry in that same file (create it, or the
  `"projects"` object, if missing) so it doesn't go stale — don't leave
  that step to whoever happens to run `validate` next.
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
