"""Extract unannotated official Scheme/Marks tables; omit examiner Notes.

No solutions are authored. Each output strip is a clipped vector copy of a
recorded rectangle in the original official PDF. Full originals stay unchanged.
Requires PyMuPDF 1.26.6. Does not run in the dependency-free release pipeline.
"""
import json
import hashlib
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / 'dist'
BANK = DIST / 'data/past-bank.json'
OUT = DIST / 'assets/past-answers-v20'
OUT.mkdir(exist_ok=True)
MARK = re.compile(r'(?<![A-Za-z])[dD]*[MAB]\s*[1-9](?:ft|\*)?')
TOTAL = re.compile(r'^(?:\(?\d+\)?|\(?\d+\s+marks?\)?|Total\s+\d+)\s*$', re.I)
PROSE = re.compile(r'^(?:Attempts?|Condone|May|For reference|This requires|This mark|Allow|Apply|Ignore|You can|You may|NB:|An alternative|As an alternative|Notes?\b|The majority|In these cases)\b', re.I)
bank = json.loads(BANK.read_text())
CACHE_PATH = Path('/tmp/pure-maths-v20-table-cache.json')
cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
audit = []


def tables(doc, page_number):
    key = f'{doc.name}:{page_number}'
    if key not in cache:
        page = doc[page_number - 1]
        cache[key] = []
        for t in page.find_tables().tables:
            if t.bbox[2] - t.bbox[0] <= 350:
                continue
            rows, boxes = [], []
            for text, row in zip(t.extract(), t.rows):
                pairs = [(v, c) for v, c in zip(text, row.cells) if c is not None]
                rows.append([v for v, c in pairs])
                boxes.append([c for v, c in pairs])
            cache[key].append((list(t.bbox), rows, boxes))
    return cache[key]


def table_strips(page, bbox, texts, cells, source_crop, notes_column):
    """Retain rows with an actual independent Marks cell, not full-width notes."""
    mark_rows = [i for i, (row, boxes) in enumerate(zip(texts, cells))
                 if boxes[-1] and boxes[-1][0] > 400 and MARK.search(row[-1] or '')]
    if not mark_rows:
        return [], notes_column
    # A column called Notes sometimes actually holds M/A/B marks (P3 Jan 2023).
    # It is a notes column only when there is a separate Marks column after it.
    for row, boxes in zip(texts[:2], cells[:2]):
        for i, text in enumerate(row[:-1]):
            if (text or '').strip() == 'Notes' and boxes[i] and any('Marks' in (v or '') for v in row[i+1:]):
                notes_column = (boxes[i][0], boxes[i][2])
    label_right = max((c[2] for row in cells for c in row if c[0] <= bbox[0]+2 and c[2] < 145), default=bbox[0])
    strips = []
    for i, (row, boxes) in enumerate(zip(texts, cells)):
        if any((v or '').strip() == 'Scheme' for v in row) and any('Question' in (v or '') for v in row):
            continue
        mark_cell = boxes[-1]
        if not mark_cell or mark_cell[0] <= 400:
            # A sketch may occupy the full Scheme/Marks width above its marks.
            if len(boxes) >= 2 and boxes[0][2] < 145 and boxes[-1][2]-boxes[-1][0] > 200 and re.match(r'^(?:\d|\([a-z])', (row[0] or '').strip(), re.I) and not PROSE.match(row[-1] or ''):
                strips.append({'y0':boxes[-1][1], 'y1':boxes[-1][3],
                               'columns':[(bbox[0],bbox[2])], 'schemeBottom':boxes[-1][3], 'displayHeight':boxes[-1][3]-boxes[-1][1], 'mark':''})
            continue
        if not (MARK.search(row[-1] or '') or TOTAL.fullmatch((row[-1] or '').strip()) or not (row[-1] or '').strip()):
            continue
        y0, y1 = mark_cell[1], mark_cell[3]
        if y1 <= source_crop.y0 or y0 >= source_crop.y1:
            continue
        # Pure explanatory rows have no mark allocation; retain blank allocation
        # rows only when they carry a part label or mathematical continuation.
        scheme_text = '\n'.join(v or '' for v,c in zip(row,boxes) if c[0] >= label_right-1 and c[0] < mark_cell[0]-1).strip()
        if not (row[-1] or '').strip() and PROSE.match(scheme_text):
            continue
        if not (row[-1] or '').strip() and not scheme_text:
            continue
        scheme_bottom = y1
        ranges = [(bbox[0], bbox[2])]
        if notes_column:
            ranges = [(bbox[0], notes_column[0]), (notes_column[1], bbox[2])]
            # Merged Scheme/Notes cells put the explanatory prose underneath
            # the equation. Cut that prose, while keeping the associated mark.
            merged = next((c for c in boxes if c[0] >= label_right-1 and c[0] < notes_column[0] and c[2] >= notes_column[1]-1), None)
            if merged:
                ranges = [(bbox[0], notes_column[1]), (notes_column[1], bbox[2])]
                for block in page.get_text('dict', clip=fitz.Rect(*merged))['blocks']:
                    for line_index, line in enumerate(block.get('lines', [])):
                        text = ''.join(s['text'] for s in line['spans']).strip()
                        if PROSE.match(text):
                            # Include the tops of tall formula glyphs embedded
                            # in the first examiner-note line in the removal.
                            note_top = block['bbox'][1]-.7 if line_index == 0 else line['bbox'][1]-1
                            scheme_bottom = min(scheme_bottom, note_top)
        for word in page.get_text('words', clip=fitz.Rect(bbox[0],y0,mark_cell[0],y1)):
            if re.fullmatch(r'Notes?:?', word[4], re.I):
                # Inline references are removed separately without cutting equations.
                line = page.get_text('text', clip=fitz.Rect(bbox[0],word[1]-1,mark_cell[0],word[3]+1))
                if re.search(r'\bsee\s+notes?\b',line,re.I):
                    continue
                scheme_bottom = min(scheme_bottom, word[1]-1)
        if y1 <= y0 + 2:
            continue
        if scheme_bottom < y0:
            continue
        if scheme_bottom < y1 and len(ranges) == 1:
            ranges = [(bbox[0],mark_cell[0]),(mark_cell[0],bbox[2])]
        mark_top, mark_bottom = y0, y1
        if scheme_bottom < y1:
            mark_words = page.get_text('words', clip=fitz.Rect(*mark_cell))
            if mark_words:
                mark_top = max(y0,min(w[1] for w in mark_words)-2)
                mark_bottom = min(y1,max(w[3] for w in mark_words)+2)
        display_height = max(scheme_bottom-y0,mark_bottom-mark_top)
        strips.append({'y0': y0, 'y1': y1, 'columns': ranges,
                       'schemeBottom': scheme_bottom, 'markTop':mark_top, 'markBottom':mark_bottom,
                       'displayHeight':display_height, 'mark': (row[-1] or '').strip()})
    return strips, notes_column


for paper in bank['papers']:
    questions = sorted((q for q in bank['questions'] if q['paper'] == paper['id']), key=lambda q: q['number'])
    original = fitz.open(DIST / paper['markScheme'])
    source_hash = hashlib.sha256((DIST / paper['markScheme']).read_bytes()).hexdigest()
    hashes = cache.setdefault('_hashes', {})
    if hashes.get(original.name) != source_hash:
        for key in list(cache):
            if key.startswith(original.name+':'):
                del cache[key]
        hashes[original.name] = source_hash
    output = fitz.open()
    notes_column = None
    owned = {q['number']: [] for q in questions}
    current_number = None
    for page_number in range(4, len(original)+1):
        page = original[page_number-1]
        for bbox, texts, cells in tables(original, page_number):
            for row, boxes in zip(texts, cells):
                if boxes[0][0] < 120 and boxes[0][2] < 145:
                    match = re.match(r'^(\d{1,2})\.?(?=\(|[a-z]|$)', re.sub(r'\s+', '', row[0] or ''), re.I)
                    if match and int(match[1]) in owned:
                        current_number = int(match[1])
                        break
            if current_number is not None and any(boxes[-1] and boxes[-1][0] > 400 and MARK.search(row[-1] or '') for row, boxes in zip(texts, cells)):
                owned[current_number].append((page_number, bbox, texts, cells))
    CACHE_PATH.write_text(json.dumps(cache))
    for q in questions:
        refs, records = [], []
        notes_column = None
        for page_number, bbox, texts, cells in owned[q['number']]:
            page = original[page_number-1]
            strips, notes_column = table_strips(page, bbox, texts, cells, page.rect, notes_column)
            if not strips:
                continue
            source = {'page':page_number, 'pdf':paper['markScheme'],
                      'crop':[bbox[0]/page.rect.width,bbox[1]/page.rect.height,
                              (bbox[2]-bbox[0])/page.rect.width,(bbox[3]-bbox[1])/page.rect.height]}
            width = bbox[2]-bbox[0] + 8
            height = sum(s['displayHeight'] for s in strips) + 8
            target = output.new_page(width=width, height=height)
            dest_y = 4
            source_rects = []
            for strip in strips:
                for left, right in strip['columns']:
                    dest_x = 4 + left - bbox[0]
                    bottom = strip['schemeBottom'] if right < bbox[2]-1 or len(strip['columns']) == 1 else strip['y1']
                    if bottom <= strip['y0']:
                        continue
                    top = strip['y0']
                    target_y = dest_y
                    if len(strip['columns']) > 1 and right >= bbox[2]-1:
                        top, bottom = strip['markTop'], strip['markBottom']
                        target_y += (strip['displayHeight']-(bottom-top))/2
                    rect = fitz.Rect(left, top, right, bottom)
                    dest = fitz.Rect(dest_x, target_y, dest_x+rect.width, target_y+rect.height)
                    target.show_pdf_page(dest, original, page_number-1, clip=rect, keep_proportion=False)
                    source_rects.append([round(v, 4) for v in rect])
                dest_y += strip['displayHeight']
            for phrase in ('(see notes for method via substitution)', '(see notes)'):
                for rect in target.search_for(phrase):
                    target.add_redact_annot(rect, fill=(1,1,1))
            if target.first_annot:
                target.apply_redactions(images=0, graphics=0)
            refs.append({'page':len(output), 'pdf':f'assets/past-answers-v20/{paper["id"]}.pdf',
                         'renderFromPdf':True, 'width':round(width*1.55), 'height':round(height*1.55),
                         'crop':[0,0,1,1], 'sourcePdf':paper['markScheme'], 'sourcePage':page_number,
                         'originalRefs':[source]})
            records.append({'sourcePage':page_number, 'rectangles':source_rects,
                            'marks':[s['mark'] for s in strips if s['mark']]})
        if not refs:
            raise ValueError(f'{q["id"]}: no official answer table detected')
        q['markSchemePages'] = refs
        q['officialMarkScheme'] = True
        q['officialSchemeRevision'] = 20
        q['solutionSections'] = []
        q['solutionZh'] = '答案、解题过程及得分点直接摘自本卷官方评分标准。'
        q['verification'] = '答案与过程得分点摘自本卷官方评分标准；已移除 Notes，不添加框线或高亮标注。'
        for key in ('quickCheckZh', 'markCodeLegend', 'manualAnswerReview'):
            q.pop(key, None)
        audit.append({'id':q['id'], 'sourcePdf':paper['markScheme'], 'sourceSha256':source_hash, 'tables':records})
    output.save(OUT / f'{paper["id"]}.pdf', garbage=4, deflate=True)
    output.close()
    original.close()
    print(paper['id'], len(questions), flush=True)
assert len(audit) == 572
BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2)+'\n')
(ROOT/'editorial/v20/official-answer-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
print('Extracted all 572 official answers without annotations.')
