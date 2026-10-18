from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1] / "dist"
for relative in ["index.html", "app.js", "core.js", "style.css", "data/bank.json", "assets/p1.pdf", "assets/p2.pdf", "assets/p3.pdf", "assets/pdfjs/pdf.mjs", "assets/pdfjs/pdf.worker.mjs"]:
    assert (root / relative).is_file(), "Missing file: " + relative
bank = json.loads((root / "data/bank.json").read_text())
assert len(bank["questions"]) >= 750, "Incomplete question bank"
for question in bank["questions"]:
    for path in re.findall(r'assets/[^"\s<>]+', question.get("stem", "")):
        assert (root / path).is_file(), "Missing question image: " + path
for filename in ["index.html", "app.js", "core.js", "style.css"]:
    assert "chatgpt.site" not in (root / filename).read_text(), "Unexpected dependency on former hosting"
print("Static website verified:", len(bank["questions"]), "questions.")
