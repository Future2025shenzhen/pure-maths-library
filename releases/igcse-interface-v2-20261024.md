# IGCSE interface v2 — 2026-10-24

UI-only update to physics/CS; the 793 document bytes, source registry, maths content and account flows remain unchanged.

- A fixed filter area and scrollable catalogue group papers by year/session. Paper descriptions identify physics MCQ/theory/practical and Core/Extended, and CS theory/computer-systems versus algorithms/programming.
- Quick paper groups, labelled year/document filters, single-click session selection, optional scope/variant filters, multi-token search, clear/reset controls and explicit missing-year recovery for supplementary reports.
- Main reading toolbar centralises QP/MS selection, previous/next paper, catalogue collapse and fullscreen. Wide desktop screens support independent side-by-side QP/MS readers.
- Per-subject filters, last selected document and preferred QP/MS mode are stored in browser-local storage. Per-document page/zoom are restored independently, capped at 100 records. These are local conveniences, not cloud-synchronised study records or automatic grading.
- Mobile has a full-height catalogue and full-height reader with explicit back/resume controls; changing a filter does not force reading mode. PDF loading is deferred until a paper is opened on mobile.
- Embedded PDF headers no longer repeat the parent toolbar. Fit-width reset and keyboard page/zoom controls are available. Source and explicit PDF download remain in the collapsed provenance panel.

Validation: complete existing npm tests/checks and static checks; actual-browser QP/MS rendering, dual readers, independent page restoration, multi-facet counts, search/reset, subject isolation, next-paper answer mode, report recovery, desktop directory collapse, mobile list/reading transitions and horizontal-overflow checks. No automatic file downloads or external reading requests in browser tests. Screenshots reviewed at 1536px and 390px widths.

Rollback baseline: `1fcfdd4c0619cd384dfaacba3bdc578ee8e4d489`; archive branch `archive/before-igcse-interface-v2-20261024`. Restoring UI files does not change any cloud account or user data.
