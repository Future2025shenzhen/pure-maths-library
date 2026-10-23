# V12 review

This pass deliberately does not certify all 770 questions. It individually rewrites 26 items, selects 9 verified textbook originals within those 26, withdraws 11 repetitive items and audits figure presentation across the bank.

`revise-bank.py` deterministically reads the previous release (1224b7b) and writes the bank and review manifest. `replaced-items.json` preserves earlier records; existing IDs remain compatible with the deployed catalog. Old completion flags are not automatically evidence of completing a rewritten question.

The published bank retains 770 historical IDs and has 759 active daily-practice questions. Withdrawals are excluded from ordinary browsing and new composition but remain accessible in pre-existing saved collections and papers.

Sources: Pearson IAL Mathematics 2018 specification P1 1.11–1.12, 3.1–3.3 and P2 6.1–6.2; the preserved 2020–2023 original papers; user-supplied P1/P2 textbooks. Exact selected pages and original E/P labels are stored per question. No answer is represented as an official textbook mark scheme.

Verification: npm test; npm run check; python3 scripts/check-static.py; python3 scripts/verify-v12-maths.py. Figures were rendered for visual review using PyMuPDF; Mathematical validation is not inferred from appearance.

Follow-up (2026-10-24): `refine-p2-marking.py` records a review of the 25 active P2 Chapter 6 items and refines 10 answer-part schemes across R01, R02 and R24. All question statements, answers, marks and IDs are preserved. The manifest records the scope and remaining editing work.
