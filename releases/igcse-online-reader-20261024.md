# IGCSE same-origin online paper reader — 2026-10-24

Before this update, the physics/CS catalogue mainly linked external archive pages and the PDF reader required a manual source URL. The homepage now opens an online paper browser; selecting a paper shows its original PDF directly using the site's local PDF.js library. QP/MS switching, page navigation, zoom, standalone reading, fullscreen and mobile catalogue navigation are supported.

The build downloads 793 pinned, SHA-256-verified source files into `dist/assets/igcse/` and includes them in the Pages artifact. The PDFs are not Git blobs; their verified source metadata is in `dist/data/igcse-online-files.json`. A missing or changed source fails the build before deployment, leaving the previous production site available. The generated directory is Git-ignored. Current static output is approximately 758.5 MiB, below the Pages 1 GiB site limit; the script refuses outputs at or above 950 MiB.

Includes 251 physics and 84 computer-science QP/MS pairs, plus collected supplementary documents. Physics `0625_s20_qp_33.pdf` and its mark scheme have not been located; supplementary reports are incomplete. This update does not assert a complete archive of every document ever published. Three mislabeled CS pre-release PDFs use corrected `.pdf` extensions with unchanged content bytes. Three erroneous archived login-page PDFs are excluded.

Checks: complete existing npm tests/checks and static checks; all resource hashes; sample build downloads including a corrected extension; browser checks for both homepage entries, actual PDF canvas rendering, QP/MS switching, navigation, zoom, subject/year filters, empty results, examiner reports and mobile list, with no external network requests or automatic file downloads during reading. Local browser homepage tests mock the public account configuration; this is not a new production authentication flow.

Maths content, stable question IDs, user accounts, records and private notes are unchanged.

Rollback baseline: `d2dff62971d01d31b31604b0f95a32adb37c9e85`. Restore this release's changed files or that baseline as appropriate; do not overwrite newer unrelated changes or revert the database.
