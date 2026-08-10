Date: 2026-08-12

# Correction: one "read-only" module also does a write

While migrating the second module (`payments-webhook`) behind the adapter,
found that it calls the v2 client for a POST (cache invalidation) in
addition to the GET calls the 2026-08-10 audit recorded.

The original audit (`2026-08-10-dependency-audit.md`) classified this
module as one of the "4 of 6... only use the client for read-only GET
calls." That count was wrong for this module.

This doesn't change the migration approach — the adapter already handles
POST — but it does mean `../memory/0001-migration-strategy.md`'s "4 of 6
read-only" detail needs a dated correction rather than being left as
written, per SPEC.md section 6.3 (new evidence contradicting an existing
memory entry gets a dated correction, not a silent rewrite).

