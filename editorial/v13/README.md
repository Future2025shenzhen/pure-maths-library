# V13 simplification

Six radians questions are withdrawn using the reviewed before/after hashes in `withdrawals.json`. Existing saved IDs and old papers remain valid.

`npm test`, `npm run check` and `npm start` automatically run the idempotent release preparation. It regenerates `dist/data/bank.json` from the checked-in V12 source and verifies its exact SHA256 before publication. The normal Pages workflow tests and publishes the prepared bank. This avoids transferring the entire 4 MB generated bank through the upload interface.

`build-layout.py` reconstructs the compact display crops from the unchanged official PDFs; it requires PyMuPDF and Pillow. `layout-audit.json` records the content and omitted stationery pages. All 323 full questions remain available, including two restored continuation diagrams.
