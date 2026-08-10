# Measuring cross-AI handoff effectiveness

Status: methodology only. None of this is automated yet — see README
"Current status". The point of writing it down now is so the CLI's output
formats (Day 2+) can be designed to make these measurable later, instead of
retrofitting instrumentation after the fact.

## Proposed metrics

1. **Cold-start recovery accuracy** — hand a fresh AI session (a different
   tool, or a new session of the same tool) only the project directory, ask
   it N factual questions about current state/history, score against a
   human-verified answer key.
2. **Turns-to-productive-context** — how many tool calls/messages an AI
   needs before it can correctly state "current status + next step",
   compared between a protocol-structured directory and a raw chat-log
   export baseline.
3. **Fact contradiction rate** — after several AI sessions have edited
   memory, how often `memory/` and `evidence/` disagree. Currently manual;
   could eventually be a `validate` check.
4. **Unflagged-uncertainty rate** — sample `status/`/`memory/` statements
   that lack a traceable `source` or an honest `confidence: unverified`
   tag but should have one.
5. **Update-discipline compliance** — after a significant `evidence/`
   addition, was `status/CURRENT_STATUS.md` updated in the same session?
   Roughly estimable from commit timestamps.
6. **Post-handoff task success (A/B)** — same task handed to a second AI
   two ways: (a) via this protocol's directory, (b) via a raw chat export.
   Does the second AI need to re-ask the user about already-established
   facts?

## First pass

Before automating any of the above, run metric 1 and 2 manually, small
sample (10–20 handoffs), against a real multi-AI-tool project — e.g. the
user's own use of this protocol switching between Claude Code and Codex.
Decide which metrics are worth wiring into the CLI only after that.
