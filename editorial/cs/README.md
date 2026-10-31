# Computer Science 0478 chapter bank

Adds 692 complete questions from all 84 existing 2019–2024 QP/MS pairs. Original PDFs are retained; records contain rotation-corrected question/official-answer crop coordinates. Old Paper 2 Q1 includes its pre-release context. Every paper retains its full 50 or 75 marks.

Classification uses the 2023–2025 Cambridge syllabus. Chapters 7, 9 and 10 use site subdivisions of the published learning outcomes. Legacy ethics/software-licensing material is separate. Tags are generated from question text and reviewed overrides; mixed questions can appear in several sections. This is not a claim of independent teacher review of every tag.

Rebuild with PyMuPDF 1.26.6:

```
python3 scripts/prepare-igcse-pdfs.py --subject cs --types qp ms
python3 scripts/build-cs-bank.py
node scripts/check-cs-bank.mjs
```

`source-audit.json` retains source hashes and matched QP/MS question boundaries. The normal `npm run check` verifies question IDs, taxonomy references, every paper's total marks, source pairing, crop geometry, pre-release context and representative classification cases. `npm test` and `npm run check` passed. Chromium checks covered desktop/mobile layout, chapter-only and subsection selection, strict/cross-section filtering, reset, direct question links, pre-release context, rotated official MS rendering and archive navigation.

Homepage CS opens `cs-bank.html`; the CS whole-paper catalogue links back to the question bank, including on mobile. Mathematics and Physics bank records are unchanged. CS bookmarks, done records and notes use separate browser storage, matching the existing Physics behavior; they are not cloud-synced.
