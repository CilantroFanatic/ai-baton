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

**If an AI is running this quickstart on a user's behalf** (e.g. the user
said "install and try ai-baton"): do `skill install` before creating any
demo project, not after. Once it's installed, re-read it (`Skill:
ai-baton`) and follow its Step 1/2a instead of improvising a demo project
path — that's what puts things in the right place from the start.

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

For driving it directly — CI, scripts, or without an AI in the loop. **If
an AI is setting this up on a user's behalf, this section is not the
procedure to follow** — that's the skill's job (Step 1/2a), and it already
knows to default into the workspace. Copying the bare `my-project` example
below literally, especially before the skill is even installed, is exactly
how a project ends up scaffolded in the wrong place — install the skill
*first*, then let it decide where things go.

```bash
ai-baton list                                    # show projects under ~/ai-baton-workspace (or pass a different dir)
ai-baton init ~/ai-baton-workspace/my-project     # scaffold a project inside the workspace
ai-baton status ~/ai-baton-workspace/my-project   # print PROTOCOL.md + memory/INDEX.md + CURRENT_STATUS.md, in read order
ai-baton validate ~/ai-baton-workspace/my-project # check frontmatter, links, staleness
```

`validate` checks: required directories exist, `PROTOCOL.md` and
`status/CURRENT_STATUS.md` exist and aren't empty, every file under
`memory/` has frontmatter matching `schemas/memory-frontmatter.schema.json`,
internal links resolve, `CURRENT_STATUS.md` isn't more than 30 days stale
(a warning, not a hard failure), none of the protocol's own files match a
well-known credential format (AWS/GitHub/Slack keys, PEM private key
blocks, JWT-looking tokens) per SPEC.md section 6.6 — a heuristic safety
net for obvious cases, not a substitute for not pasting secrets in the
first place — and `memory/` isn't over 50,000 characters (SPEC.md section
6.7; also a warning, not a failure). Every session that reads
`memory/INDEX.md` pays for its size in tokens, so past that threshold
`validate` nudges you to archive stale-but-still-true entries. Override
the threshold per project with a `.ai-baton.json` file at the project
root:

```json
{ "memory_size_warning_chars": 200000 }
```

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
