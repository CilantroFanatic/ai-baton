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

Copy the skill somewhere an [Agent Skills](https://agentskills.io/)-compatible
tool looks for it — globally (works across every project you point the tool
at):

```bash
mkdir -p ~/.agents/skills
cp -r .agents/skills/ai-handoff-protocol ~/.agents/skills/
```

or per-project, if you'd rather scope it to one place:

```bash
mkdir -p /path/to/some/project/.agents/skills
cp -r .agents/skills/ai-handoff-protocol /path/to/some/project/.agents/skills/
```

With this installed, a tool that supports Agent Skills (Claude Code, Codex
CLI, Cursor, and others as of 2026 — see `docs/comparison.md`) should, on
its own: notice when you're working in a directory that already has a
`PROTOCOL.md` and read it first, or ask whether to start a new
ai-handoff-protocol project when it's not obvious which one you mean —
useful if you keep several going at once (one per exam, one per thesis,
etc.) and don't want them bleeding into each other.

This hasn't been exercised in an actual Claude Code/Codex/Cursor session
yet — only frontmatter-checked by `tests/test_skill.py`. If it doesn't
trigger the way this describes, that's a real gap to report, not a
misunderstanding on your end.

## See it end to end

[`examples/demo-project/`](../examples/demo-project/) is a fictional but
fully worked example — three sessions, two different (fictional) AI tools,
exercising confidence promotion, an in-place correction, and archived
content. Its `README.md` walks through the narrative; running `validate`
against it is what CI does on every push.
