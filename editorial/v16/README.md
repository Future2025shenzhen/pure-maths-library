# V16 · P1 Radians re-audit

User approved the 36-ID disposition map before implementation. This layer contains 21 active questions: 2 unchanged mathematical cores, 5 local revisions, 12 rewrites and 2 additions, after 4 further withdrawals.

Run `python3 editorial/v16/prepare.py` to rebuild this content layer. It imports the legacy release layers only when starting from an older bank, then applies V16 last. `npm start`, `npm test` and `npm run check` use this entry point. The retained V14 source file is an input, not the active student bank.

`math_audit.py` independently reconstructs all 21 geometries and tests parameter boundaries. `scripts/check-v16.mjs` validates sources across the entire active bank, quotas, IDs, mark sums and historical-state compatibility. `browser-check.cjs` checks real rendering with account configuration intercepted as local-only in that test browser; it does not test production authentication or cloud writes.

Full Chinese report, approval mapping, executed mapping, two ledgers and all questions: `../overhaul/re-audit-01/`.

`backend/006-overhaul-catalog.sql` must be executed by the database owner to register overhaul IDs for cloud records. No database administrator connection was available in this session.
