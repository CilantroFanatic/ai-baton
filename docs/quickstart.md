# Quickstart

Not published to PyPI yet (see README "Current status") — for now, install
from a local checkout:

```bash
git clone <this-repo>
cd ai-handoff-protocol
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

If `import ai_handoff_protocol` fails right after that with
`ModuleNotFoundError` despite `pip` reporting success, your venv isn't
processing `.pth` files (seen on at least one machine) — see
`CONTRIBUTING.md`'s note for the `pip install .` (no `-e`) workaround.

## Start a new project

```bash
ai-handoff-protocol init my-project
cd my-project
```

This creates `memory/`, `status/`, `evidence/`, `handover/`, `archive/`,
plus a starter `PROTOCOL.md`, `memory/INDEX.md`, and
`status/CURRENT_STATUS.md`. `init` never overwrites existing files — safe
to re-run.

Fill in `status/CURRENT_STATUS.md` with whatever you're actually doing:

```markdown
Last updated: 2026-08-12
Updated by: you

## Current goal

...

## Next steps

...
```

## Hand a session off (to yourself later, or to a different AI tool)

```bash
ai-handoff-protocol status my-project
```

Prints `PROTOCOL.md` + `memory/INDEX.md` + `status/CURRENT_STATUS.md`, in
the order SPEC.md section 4 says any session should read them in. Paste
that (or pipe it) into a fresh session, in Claude Code, Codex CLI, Cursor,
or anything else that can read the resulting files directly off disk —
there's no dependency on any of them specifically.

## Check you haven't broken the protocol's own rules

```bash
ai-handoff-protocol validate my-project
```

Checks: required directories exist, `PROTOCOL.md` and
`status/CURRENT_STATUS.md` exist and aren't empty, every file under
`memory/` has frontmatter matching `schemas/memory-frontmatter.schema.json`
(see SPEC.md section 5), internal Markdown links resolve, and
`status/CURRENT_STATUS.md` isn't more than 30 days stale (a warning, not a
hard failure — dates it, doesn't guess at what "stale" should mean for
your project).

## Let an AI follow the protocol without being reminded

Symlink the skill (not a copy — one canonical file, no drift between
installed locations) into wherever [Agent Skills](https://agentskills.io/)-
compatible tools look for it, user-wide so it works across every project:

```bash
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$(pwd)/.agents/skills/ai-handoff-protocol" ~/.claude/skills/ai-handoff-protocol
ln -s "$(pwd)/.agents/skills/ai-handoff-protocol" ~/.agents/skills/ai-handoff-protocol
```

`~/.claude/skills/` is Claude Code's own lookup path; `~/.agents/skills/`
is the newer shared convention Codex CLI (and reportedly others) scan too.
Installing both costs nothing and doesn't assume either one is redundant.

**Verified vs. not verified:** the `~/.claude/skills/` install was tested
live in an actual Claude Code session — calling the skill picked it up
immediately, no restart needed. The `~/.agents/skills/` path for Codex CLI
is only confirmed by documentation research, not by actually running Codex
here. If you try it in Codex and it doesn't trigger, that's a real gap to
report, not a misunderstanding on your end.

With this installed, the AI should, on its own: notice when you're working
in a directory that already has a `PROTOCOL.md` and read it first, or ask
whether to start a new ai-handoff-protocol project when it's not obvious
which one you mean — useful if you keep several going at once (one per
exam, one per thesis, etc.) and don't want them bleeding into each other.

## See it end to end

[`examples/demo-project/`](../examples/demo-project/) is a fictional but
fully worked example — three sessions, two different (fictional) AI tools,
exercising confidence promotion, an in-place correction, and archived
content. Its `README.md` walks through the narrative; running `validate`
against it is what CI does on every push.
