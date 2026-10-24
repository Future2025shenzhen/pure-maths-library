"""Rebuild every official-answer crop from its printed question number.

The crop stops at the end of the answer table (before examiner notes), and only
accuracy/independent-answer rows are boxed. Existing question text and metadata
are preserved.
"""
import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
BANK_PATH = ROOT / "dist/data/past-bank.json"
bank = json.loads(BANK_PATH.read_text())
papers = {paper["id"]: paper for paper in bank["papers"]}


def label_match(token, number):
    return re.fullmatch(rf"{number}(?!\d)\.?(?:(?:\([a-ziv]+\))|[a-z])*(?:\.)?", token.strip(), re.I)


def locate_starts(doc, questions):
    """Locate printed question labels inside the official Scheme table headers."""
    headers = []
    candidates = {question["number"]: [] for question in questions}
    for page_number, page in enumerate(doc, 1):
        words = page.get_text("words")
        page_headers = [word[1] for word in words if word[0] < 120 and word[4] == "Question"
                        and any(other[4] == "Scheme" and abs(other[1] - word[1]) < 35
                                for other in words)]
        for header_y in page_headers:
            headers.append((page_number, header_y))
            labelled = []
            for word in words:
                if word[0] >= 80 or not (header_y + 8 <= word[1] <= header_y + 100):
                    continue
                for question in questions:
                    if label_match(word[4], question["number"]):
                        labelled.append((word[1], question["number"]))
            # Only the first numbered cell below this table header is a question
            # label. Later numbers in the Scheme column are mathematical content.
            if labelled:
                label_y, number = min(labelled)
                candidates[number].append((page_number, label_y))

    starts = []
    previous = (3, 0)
    for question in questions:
        choices = sorted(set(position for position in candidates[question["number"]]
                             if position > previous))
        if choices:
            pick = choices[0]
        else:
            # Rare OCR loss of the printed number: retain the already-audited
            # source page and crop top for this one table.
            ref = question["markSchemePages"][0]
            page = doc[ref["page"] - 1]
            pick = (ref["page"], ref["crop"][1] * page.rect.height + 18)
        starts.append(pick)
        previous = pick
    if starts != sorted(starts):
        raise ValueError(f"{questions[0]['paper']}: official scheme tables are out of order: {starts}")
    return starts


def find_table_end(page, start_y):
    """Return the bottom of the scheme table, excluding its following notes."""
    words = page.get_text("words")
    totals = [w[3] for w in words if w[1] > start_y and w[4].strip().lower() == "total"]
    mark_totals = [w[3] for w in words if w[1] > start_y and w[4].strip().lower() == "marks)"]
    ends = totals + mark_totals
    note_words = [w for w in words if w[1] > start_y + 25 and
                  w[4].strip().lower() in {"note", "notes", "note:", "notes:"}]
    explicit_notes = [w[1] for w in note_words if w[0] < 100]
    if ends:
        printed_end = min(ends)
        trailing_notes = [w[1] for w in note_words if w[1] >= printed_end - 5]
        end = printed_end + 13
        return min(end, min(trailing_notes) - 5) if trailing_notes else end

    # Older schemes end the table with “(n marks)” and then begin mark notes in
    # a narrow left column. The “marks)” token is handled above; this fallback
    # catches layouts whose total is a drawing rather than extractable text.
    notes = [w[1] for w in words if w[1] > start_y + 35 and (
        w[4].strip().lower().startswith("notes:") or
        (w[0] < 48 and re.fullmatch(r"(?:d?M\d+|A\d+|B\d+)", w[4].strip()))
    )]
    return min(notes) - 8 if notes else None


def accuracy_boxes(page, top, bottom):
    """Box the scheme row associated with each A/B mark, never M method marks."""
    boxes = []
    width, height = page.rect.width, page.rect.height
    words = page.get_text("words")
    for mark in words:
        token = mark[4].replace(" ", "")
        codes = re.findall(r"(?:A\d+|B\d+)", token)
        if not codes or not (top <= mark[1] <= bottom):
            continue
        row_words = [w for w in words if w[2] < mark[0] - 3 and w[0] > 92
                     and w[1] < mark[3] + 7 and w[3] > mark[1] - 7]
        if row_words:
            left = max(96, min(w[0] for w in row_words) - 5)
            right = min(mark[0] - 7, max(w[2] for w in row_words) + 5)
        else:
            left, right = width * .20, min(mark[0] - 7, width * .78)
        # Formula glyphs are often absent from extracted words, so retain a
        # useful minimum width centred in the Scheme column.
        if right - left < width * .16:
            left, right = width * .20, min(mark[0] - 7, width * .78)
        y0, y1 = max(top, mark[1] - 7), min(bottom, mark[3] + 7)
        box = [left / width, y0 / height, (right - left) / width, (y1 - y0) / height]
        rounded = [round(value, 6) for value in box]
        if not boxes or abs(rounded[1] - boxes[-1]["box"][1]) > .004:
            boxes.append({"kind": "accuracy", "box": rounded})
    return boxes


by_paper = {}
for question in bank["questions"]:
    by_paper.setdefault(question["paper"], []).append(question)

audit = []
for paper_id, questions in by_paper.items():
    questions.sort(key=lambda q: q["number"])
    paper = papers[paper_id]
    doc = fitz.open(ROOT / "dist" / paper["markScheme"])
    starts = locate_starts(doc, questions)
    for index, question in enumerate(questions):
        start_page, start_y = starts[index]
        next_page, next_y = starts[index + 1] if index + 1 < len(starts) else (len(doc) + 1, 0)
        last_page = next_page if next_page == start_page else next_page - 1
        last_page = min(last_page, len(doc))
        refs = []
        for page_number in range(start_page, last_page + 1):
            page = doc[page_number - 1]
            height = page.rect.height
            top_y = max(20, start_y - 20) if page_number == start_page else 20
            next_limit = next_y - 10 if page_number == next_page == start_page else height - 25
            table_end = find_table_end(page, top_y)
            bottom_y = min(next_limit, table_end) if table_end else next_limit
            if bottom_y <= top_y + 25:
                continue
            refs.append({
                "page": page_number,
                "pdf": paper["markScheme"],
                "renderFromPdf": True,
                "width": round(page.rect.width * 1.55),
                "height": round(height * 1.55),
                "crop": [.035, round(top_y / height, 6), .93, round((bottom_y - top_y) / height, 6)],
                "highlights": accuracy_boxes(page, top_y, bottom_y),
            })
            if table_end:
                break
        if not refs:
            raise ValueError(f"{question['id']}: empty official-answer crop")
        question["markSchemePages"] = refs
        question["officialSchemeRevision"] = 19
        question["verification"] = "题号已与本卷官方评分表逐题对应；已移除答案表后的 Notes；粉红框标出答案。"
        audit.append({
            "id": question["id"],
            "printedQuestion": question["number"],
            "start": [start_page, round(start_y, 2)],
            "pages": [ref["page"] for ref in refs],
            "answerBoxes": sum(len(ref["highlights"]) for ref in refs),
        })

assert len(audit) == 572
BANK_PATH.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n")
(ROOT / "editorial/v19/official-answer-audit.json").write_text(
    json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
)
print(json.dumps({"questions": len(audit), "boxed": sum(x["answerBoxes"] for x in audit)}))
