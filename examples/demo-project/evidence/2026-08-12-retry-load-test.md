Date: 2026-08-12

# Load test: adapter retry behavior under connection-pool exhaustion

(Session 3 — back to the tool used in the 2026-08-10 session. Read
`PROTOCOL.md` -> `memory/INDEX.md` -> `status/CURRENT_STATUS.md` first, per
the mandatory read order, since this is a new session picking the project
back up.)

Ran the existing pool-exhaustion load test (previously only exercised
against the v2 client directly) against the adapter built on 2026-08-11.

Result: adapter's translated `retry_policy` produces the same retry count
and backoff timing as v2's `max_retries`/`backoff_base` under exhaustion.
No behavior difference observed across 200 runs.

This is the evidence `../memory/0002-adapter-retry-shape.md` cites for
promoting its `confidence` from `unverified` to `verified`.

(Fictional example content.)
