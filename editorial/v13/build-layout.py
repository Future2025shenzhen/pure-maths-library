"""Build display-only crops. Original PDFs, images and question data stay intact."""
import json, re
from pathlib import Path
import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
bank = json.loads((DIST / 'data/past-bank.json').read_text())
layout, audit = {}, {}

def content(page):
    boxes = []
    for block in page.get_text('dict')['blocks']:
        if block['type'] == 1:
            r = fitz.Rect(block['bbox'])
            if r.x0 >= 40 and r.x1 <= 518 and r.y0 >= 42 and r.y1 <= 790:
                boxes.append(r)
            continue
        for line in block.get('lines', []):
            for span in line['spans']:
                text = span['text'].strip()
                r = fitz.Rect(span['bbox'])
                if not text or r.x0 < 40 or r.x0 > 512 or r.y0 < 42 or r.y1 > 790:
                    continue
                if re.fullmatch(r'[_\s]+', text) or text in ['Leave', 'blank', 'END']:
                    continue
                if re.search(r'DO NOT WRITE|Turn over|Question \d+ continued|TOTAL FOR PAPER|\(Total .*marks\)|^Q\d+$', text):
                    continue
                # Stray printer/answer-line glyphs are not mathematical content.
                if len(text) > 40 and set(text) <= set('_v '):
                    continue
                boxes.append(r)
    for drawing in page.get_drawings():
        r = drawing['rect']
        # Exclude the exam stationery frame, margin rules and writing lines.
        if r.x0 < 42 or r.x1 > 518 or r.y0 < 42 or r.y1 > 790:
            continue
        if r.height < 1.2 and r.width > 390:
            continue
        boxes.append(r)
    return boxes

for paper in bank['papers']:
    doc = fitz.open(DIST / paper['pdf'])
    cache = {}
    for q in [q for q in bank['questions'] if q['paper'] == paper['id']]:
        slices, retained, excluded = [], [], []
        for n in q['sourcePages']:
            page = doc[n-1]
            if n not in cache:
                cache[n] = content(page)
            boxes = cache[n]
            if not boxes:
                excluded.append(n)
                continue
            intervals = []
            for r in sorted(boxes, key=lambda r: r.y0):
                top, bottom = max(40, r.y0-4), min(792, r.y1+4)
                if intervals and top <= intervals[-1][1]+12:
                    intervals[-1][1] = max(bottom, intervals[-1][1])
                else:
                    intervals.append([top, bottom])
            # A consistent horizontal crop preserves font size across all slices.
            left = min(50, min(r.x0 for r in boxes)-4)
            right = max(512, max(r.x1 for r in boxes)+4)
            src = next((v for v in q['pages'] if v['page'] == n), None)
            if src is None:
                # Two supplied papers have a continuation diagram not included in
                # the old page-image index. Preserve it in the compact view too.
                name = f'assets/past-content/{paper["id"]}-page-{n:02}.webp'
                target = DIST / name
                target.parent.mkdir(exist_ok=True)
                pix = page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8))
                im = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
                im.save(target, 'WEBP', quality=90)
                src = dict(page=n, image=name, width=pix.width, height=pix.height)
            for top, bottom in intervals:
                crop = [round(left/page.rect.width, 6), round(top/page.rect.height, 6), round((right-left)/page.rect.width, 6), round((bottom-top)/page.rect.height, 6)]
                slices.append({**src, 'crop': crop})
            for r in boxes:
                assert any(top <= r.y0 and bottom >= r.y1 for top, bottom in intervals), (q['id'], n, r)
            retained.append(n)
        assert slices, q['id']
        layout[q['id']] = slices
        audit[q['id']] = {'contentPages': retained, 'omittedStationeryPages': excluded, 'slices': len(slices)}
    doc.close()

(DIST/'data/past-layout.json').write_text(json.dumps({'version':13, 'questions':layout}, ensure_ascii=False, separators=(',', ':'))+'\n')
(ROOT/'editorial/v13/layout-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
print(f'Built compact crops for {len(layout)} whole questions; source question text, images and PDFs unchanged.')
