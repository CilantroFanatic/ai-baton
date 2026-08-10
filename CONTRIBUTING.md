# Contributing

This project is pre-alpha: the spec is more stable than the code, because
there isn't much code yet. A few ground rules while that's true:

- Changes to `SPEC.md` are the highest-leverage (and highest-risk) changes
  in this repo — they affect every project that adopts the protocol.
  Propose spec changes as their own PR/issue, separate from CLI changes,
  with the reasoning written out.
- Don't claim a feature is implemented in `README.md` until it actually is.
  The "Current status" checklist in the README is the source of truth for
  what exists; keep it in sync with reality.
- Keep the CLI's dependency footprint small. The whole point of this
  protocol is that it doesn't require infrastructure — a CLI with a heavy
  dependency tree undermines that.
- `examples/demo-project` must stay fictional. Don't use real personal or
  proprietary data as example content, even if it's convenient.

## Development

This project targets Python + `uv`:

```bash
uv sync
uv run pytest
uv run ai-handoff-protocol validate examples/demo-project
```

If `uv` isn't available, a plain venv works too:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install . pytest   # not -e — see note below
pytest
```

**Editable installs (`pip install -e .`) may silently fail to import** on
some setups: the CLI package uses hatchling's default editable mode, which
relies on a `.pth` file adding `src/` to `sys.path`. On at least one tested
machine (a conda-derived `venv`), `.pth` files placed in that venv's
`site-packages` were never processed by the `site` module — verified by
testing a trivial unrelated `.pth` file, not specific to this package — so
`import ai_handoff_protocol` failed even though `pip install -e .` reported
success. If you hit `ModuleNotFoundError: No module named
'ai_handoff_protocol'` right after an editable install, use a regular
install (`pip install .`, no `-e`) instead, or run with `PYTHONPATH=src`.
