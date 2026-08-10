Date: 2026-08-11

# HTTP client adapter: implementation notes

(Session 2 — different AI tool than the 2026-08-10 session, picked up via
`ai-baton status .`)

Built the adapter described in
`../memory/0001-migration-strategy.md`, wrapping the v3 client's HTTP
methods behind the v2 client's interface.

Open question: the v3 client's retry/backoff options don't map 1:1 to v2's
(`max_retries` + `backoff_base`, vs v3's `retry_policy` object). Wrote a
translation layer, but haven't tested it under connection-pool exhaustion —
the one case where v2's backoff behavior actually mattered in production
before. Recording this as `confidence: unverified` in
`../memory/0002-adapter-retry-shape.md` rather than assuming the
translation is correct.

