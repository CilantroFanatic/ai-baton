# Quickstart

Two commands, once, ever:

```bash
pip install ai-baton-tool
ai-baton skill install
```

(`ai-baton-tool` is the PyPI distribution name — an unrelated existing
package blocked plain `ai-baton` — but the command is `ai-baton` either
way. `skill install` writes `SKILL.md` into `~/.claude/skills/ai-baton/`
and `~/.agents/skills/ai-baton/`, the lookup paths Claude Code and Codex
CLI scan — the actual path resolution is cross-platform (Python's
`Path.home()`), so this correctly lands under `C:\Users\<you>\...` on
Windows. The shell *examples* throughout these docs are Unix/macOS syntax,
though, and haven't been tried on Windows cmd/PowerShell — if you hit
something that doesn't translate, that's a real gap to report.)

That's it. From here you just talk to your AI tool normally.

## Using it

Say something like "start a new memory project for my thesis" or "pick up
where we left off on the exam-prep project." The AI — per the skill it
just read — checks `~/ai-baton-workspace/` for existing projects (via
`ai-baton list`), asks which one you mean or offers to start a new one,
then runs `ai-baton init` / `validate` / `status` on your behalf. You
shouldn't need to type any of those commands yourself; they're what the AI
runs, not what you run.

Every project gets its own named subdirectory under the workspace —
`~/ai-baton-workspace/thesis/`, `~/ai-baton-workspace/ielts-prep/`, and so
on — never dumped loose into the workspace root or into some other
general-purpose folder you already use for other things. A real early user
had `ai-baton init` pointed straight at their whole `~/Documents`, which
mixed protocol files in with every other unrelated project sitting there;
fixed by making the workspace convention explicit in the skill (SKILL.md
Step 1 and Step 2a.1).

Verified live in Claude Code: install the skill, ask it to start or
continue a project, and it follows the read-order/update rules
automatically. Not yet tested in Codex CLI or Cursor.

If your AI tool doesn't have shell access to run the CLI itself, or
`ai-baton` isn't installed yet, the skill tells it to create the
`memory/`/`status/`/`evidence/`/`handover/`/`archive/` structure by hand
instead — same result either way.

## Manual / scripted use

For driving it directly — CI, scripts, or without an AI in the loop:

```bash
ai-baton list                   # show projects under ~/ai-baton-workspace (or pass a different dir)
ai-baton init my-project        # scaffold the structure
ai-baton status my-project      # print PROTOCOL.md + memory/INDEX.md + CURRENT_STATUS.md, in read order
ai-baton validate my-project    # check frontmatter, links, staleness
```

`validate` checks: required directories exist, `PROTOCOL.md` and
`status/CURRENT_STATUS.md` exist and aren't empty, every file under
`memory/` has frontmatter matching `schemas/memory-frontmatter.schema.json`,
internal links resolve, and `CURRENT_STATUS.md` isn't more than 30 days
stale (a warning, not a hard failure).

`skill install` also accepts explicit paths instead of the two global
defaults, e.g. to scope it to one project:

```bash
ai-baton skill install my-project/.agents/skills
```

To work on ai-baton's own code instead of just using it, install from a
local checkout:

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

## See it end to end

[`examples/demo-project/`](../examples/demo-project/) is a fictional but
fully worked example — three sessions, two different (fictional) AI tools,
exercising confidence promotion, an in-place correction, and archived
content. Its `README.md` walks through the narrative; running `validate`
against it is what CI does on every push.
