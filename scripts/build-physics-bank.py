"""Build page-accurate Physics question records from official QP/MS pairs.

The generated records reference the original PDFs.  Mark-scheme crops stop before
the Guidance/Notes column, so the question bank contains only official answers,
working and mark points.
"""
from pathlib import Path
import json, re
import fitz

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
PDF_ROOT = DIST / 'assets/igcse'
MANIFEST = DIST / 'data/igcse-online-files.json'
OUTPUT = DIST / 'data/physics-question-bank.json'


def words(page):
    result = []
    for word in page.get_text('words'):
        rect = fitz.Rect(word[:4]) * page.rotation_matrix
        result.append((*rect, word[4]))
    return result


def starts(document, paper, scheme=False):
    candidates = []
    for page_number, page in enumerate(document, 1):
        for x0, y0, x1, y1, text in words(page):
            match = re.match(r'^(\d{1,2})(?:\(|$)', text)
            left_limit = 110 if scheme else 90
            if (scheme or x0 > 35) and x0 < left_limit and 40 < y0 < page.rect.height - 35 and match:
                candidates.append((int(match.group(1)), page_number, y0, x0, text))
    if scheme and paper not in (1, 2):
        beginning = next(i for i, item in enumerate(candidates)
                         if item[0] == 1 and item[4].startswith('1('))
        candidates = candidates[beginning:]
    ordered, expected = [], 1
    for item in candidates:
        if item[0] == expected:
            ordered.append(item)
            expected += 1
    return ordered


def crop_records(document, positions, pdf_path, scheme=False):
    output = []
    for index, (number, start_page, start_y, *_rest) in enumerate(positions):
        if index + 1 < len(positions):
            _, next_page, next_y, *_ = positions[index + 1]
        else:
            next_page, next_y = len(document) + 1, None
        pieces = []
        for page_number in range(start_page, min(next_page, len(document)) + 1):
            page = document[page_number - 1]
            top = max(42, start_y - 8) if page_number == start_page else 42
            bottom = next_y - 8 if page_number == next_page else page.rect.height - 36
            if bottom <= top + 4:
                continue
            right = page.rect.width - 42
            if scheme:
                guidance = [x0 for x0, y0, x1, y1, text in words(page)
                            if text.lower() in ('guidance', 'notes') and y0 < 140]
                if guidance:
                    right = min(right, min(guidance) - 8)
            left = 45
            pieces.append({
                'page': page_number,
                'pdf': pdf_path,
                'renderFromPdf': True,
                'crop': [round(left / page.rect.width, 6), round(top / page.rect.height, 6),
                         round((right - left) / page.rect.width, 6), round((bottom - top) / page.rect.height, 6)]
            })
        output.append(pieces)
    return output


def cropped_text(document, pieces):
    parts = []
    for piece in pieces:
        page = document[piece['page'] - 1]
        x, y, w, h = piece['crop']
        clip = fitz.Rect(x * page.rect.width, y * page.rect.height,
                         (x + w) * page.rect.width, (y + h) * page.rect.height)
        clip = clip * page.derotation_matrix
        parts.append(page.get_text('text', clip=clip, sort=True))
    return '\n'.join(parts).strip()


def session_name(code):
    return {'m': 'February/March', 's': 'May/June', 'w': 'October/November'}[code]


def build():
    files = json.loads(MANIFEST.read_text())['files']
    physics = [entry for entry in files if entry['subject'] == 'physics' and entry['type'] == 'qp']
    index = {entry['filename']: entry for entry in files}
    questions, papers = [], []
    for qp_entry in physics:
        ms_entry = index[qp_entry['filename'].replace('_qp_', '_ms_')]
        paper_number = int(qp_entry['paper'][0])
        qp = fitz.open(PDF_ROOT / qp_entry['filename'])
        ms = fitz.open(PDF_ROOT / ms_entry['filename'])
        qp_starts = starts(qp, paper_number)
        ms_starts = starts(ms, paper_number, scheme=True)
        if len(qp_starts) != len(ms_starts):
            raise ValueError(f'{qp_entry["filename"]}: QP {len(qp_starts)}, MS {len(ms_starts)}')
        qp_path, ms_path = qp_entry['path'], ms_entry['path']
        qp_crops = crop_records(qp, qp_starts, qp_path)
        ms_crops = crop_records(ms, ms_starts, ms_path, scheme=True)
        paper_id = qp_entry['filename'][5:-4].replace('_qp_', '-')
        paper_group = 'mcq-theory' if paper_number in (1, 2, 3, 4) else 'practical'
        papers.append({
            'id': paper_id, 'year': qp_entry['year'], 'session': qp_entry['session'],
            'paper': qp_entry['paper'], 'group': paper_group, 'qp': qp_path, 'ms': ms_path,
            'title': f'{qp_entry["year"]} {session_name(qp_entry["session"])} · Paper {qp_entry["paper"]}'
        })
        for offset, ((number, *_), question_pages, answer_pages) in enumerate(zip(qp_starts, qp_crops, ms_crops), 1):
            question_text = cropped_text(qp, question_pages)
            answer_text = cropped_text(ms, answer_pages)
            answer = None
            if paper_number in (1, 2):
                if re.search(r'Question\s+Discounted', answer_text, re.I):
                    answer = 'Question Discounted'
                match = re.search(rf'\b{number}\s+([A-D])\s+1\b', answer_text)
                if not answer and not match:
                    letters = re.findall(r'\b[A-D]\b', answer_text)
                    match = letters[0] if letters else None
                    answer = match
                elif match:
                    answer = match.group(1)
                if answer not in ('A', 'B', 'C', 'D', 'Question Discounted'):
                    raise ValueError(f'{ms_entry["filename"]} Q{number}: answer key not found')
            total = re.search(r'\[Total:\s*(\d+)\]', question_text, re.I)
            questions.append({
                'id': f'PHY-{qp_entry["year"]}-{qp_entry["session"].upper()}-{qp_entry["paper"]}-Q{number:02d}',
                'paper': paper_id, 'group': paper_group, 'paperType': paper_number,
                'year': qp_entry['year'], 'session': qp_entry['session'], 'variant': int(qp_entry['paper'][1]),
                'number': number, 'marks': 1 if answer else (int(total.group(1)) if total else None),
                'chapters': [], 'sections': [], 'topics': [], 'searchText': question_text,
                'pages': question_pages, 'answer': answer, 'markSchemePages': answer_pages,
                'officialMarkScheme': True,
                'verification': '答案与过程得分点摘自本卷官方评分标准；已移除 Notes/Guidance，不添加自创解析或标注。'
            })
    payload = {
        'version': 1, 'subject': 'Cambridge IGCSE Physics 0625',
        'answerPolicy': 'Official mark schemes only; Notes/Guidance excluded',
        'papers': papers, 'questions': questions
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
    print(f'Built {len(questions)} questions from {len(papers)} official QP/MS pairs')


if __name__ == '__main__':
    build()
