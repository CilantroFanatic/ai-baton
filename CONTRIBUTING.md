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

This project targets Python + `uv`. Once the CLI package exists:

```bash
uv sync
uv run pytest
```

(Not wired up yet — see README "Current status".)
