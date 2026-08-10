Date: 2026-08-10

# Dependency audit: northwind-api v2 usage

Raw notes from grepping the fictional codebase for direct `northwind-api`
v2 HTTP client usage, ahead of the v2 → v3 migration.

- Found direct client construction in 6 modules.
- 4 of the 6 only use the client for read-only GET calls — low migration
  risk.
- 2 of the 6 also use v2-specific retry/backoff options that don't exist in
  the v3 client — these need the adapter layer to preserve behavior.

This is the evidence `../memory/0001-migration-strategy.md` cites as its
`source`.

