# Quickstart

```bash
pip install ai-baton-tool
# or: uvx --from ai-baton-tool ai-baton --help
```

The PyPI distribution is named `ai-baton-tool` (an unrelated existing
package blocked the plain `ai-baton` name) but the command is `ai-baton`
either way.

To work on the code itself instead, install from a local checkout:

```bash
git clone https://github.com/CilantroFanatic/ai-baton
cd ai-baton
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
```

If `import ai_baton` fails right after that with `ModuleNotFoundError`
despite `pip` reporting success, your venv isn't processing `.pth` files
(seen on at least one machine) — use `pip install .` (no `-e`) instead, or
run with `PYTHONPATH=src`.

## Start a new project

```bash
ai-baton init my-project
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
ai-baton status my-project
```

Prints `PROTOCOL.md` + `memory/INDEX.md` + `status/CURRENT_STATUS.md`, in
the order SPEC.md section 4 says any session should read them in. Paste
that (or pipe it) into a fresh session, in Claude Code, Codex CLI, Cursor,
or anything else that can read the resulting files directly off disk —
there's no dependency on any of them specifically.

## Check you haven't broken the protocol's own rules

```bash
ai-baton validate my-project
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
ln -s "$(pwd)/.agents/skills/ai-baton" ~/.claude/skills/ai-baton
ln -s "$(pwd)/.agents/skills/ai-baton" ~/.agents/skills/ai-baton
```

`~/.claude/skills/` is Claude Code's lookup path; `~/.agents/skills/` is
the shared convention Codex CLI also scans. Tested live in Claude Code
(triggers immediately). Not yet tested in Codex or Cursor.

Once installed, the AI notices when a directory already has a
`PROTOCOL.md` and reads it first, or asks whether to start a new project
when that's not obvious — handy if you're running several projects at
once (one per exam, one for a thesis) and don't want them mixed up.

## See it end to end

[`examples/demo-project/`](../examples/demo-project/) is a fictional but
fully worked example — three sessions, two different (fictional) AI tools,
exercising confidence promotion, an in-place correction, and archived
content. Its `README.md` walks through the narrative; running `validate`
against it is what CI does on every push.
