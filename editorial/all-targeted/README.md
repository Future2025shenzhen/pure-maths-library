# Whole-question targeted practice

P1 (211 questions), P2 (200 questions) and Computer Science 0478 (692 questions) have question-specific scope annotations, including every subpart. P3 continues to use its existing reviewed scope.

`P1-requirements.txt` and `P2-requirements.txt` list chapter requirements and the assessed skills. `CS-requirements.txt` lists the required syllabus sections (including legacy supplement 11.1). Each `[paper]` block is ordered by question number. The compiler rejects missing, duplicated or unknown question IDs and invalid scope values.

A targeted question must have **all** of its required chapters/sections inside the selected set. A question can combine any of the selected chapters. Cross-chapter mode accepts any intersection and can therefore require unselected chapters. The modes are exclusive and targeted is the default, including after reset.

Boundaries follow the textbook/syllabus chapters, rather than every prerequisite operation. P1 trigonometric graph transformations are in chapter 6; ordinary tangent calculations are in differentiation. P2 circle geometry includes chords, tangents and perpendicular bisectors. Separate polynomial, logarithmic, trigonometric, differentiation and area subquestions remain separate requirements.

CS annotations distinguish assessed topics from context and distractors: parity-bit strings do not imply number conversion; flash-memory NAND cells do not imply a logic-gate question; RAM mentioned in the fetch cycle does not imply an independent storage question. Independent storage questions, gate naming, validation, arrays, testing, file operations and database queries remain explicit requirements. Historical QBE grids map to section 9.2 alongside SQL. Original question and answer crops and record IDs are unchanged.

Rebuild with `python3 scripts/build-all-past-scope.py`. `source-audit.json` records source PDF hashes, question/answer fingerprints and changes from the previous tags. `npm test` checks fingerprints, coverage, all maths chapter combinations, all CS chapter combinations, omission of individual required CS sections, corrected examples and fail-closed behavior. Update annotations deliberately when changing source questions; never generate reviewed scope from keyword matches.
