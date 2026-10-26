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

SECTION_PATTERNS = {
    '1.1': r'physical quantit|measurement|measuring cylinder|micrometer|vernier|ruler|stopwatch|significant figure|unit of|scalar|vector',
    '1.2': r'\bmotion\b|speed|velocity|acceleration|deceleration|distance.time|speed.time|velocity.time|terminal velocity|free fall',
    '1.3': r'\bmass\b|\bweight\b|gravitational field|centre of (?:mass|gravity)',
    '1.4': r'\bdensity\b|mass per unit volume',
    '1.5': r'\bforce|resultant|newton|spring|elastic|hooke|extension|moment|turning effect|equilibrium|friction|centripetal',
    '1.6': r'momentum|impulse|collision|conservation of momentum',
    '1.7': r'energy|work done|\bpower\b|efficien|kinetic|potential energy|renewable|fossil fuel|energy resource',
    '1.8': r'\bpressure\b|manometer|barometer|hydraulic|force per unit area',
    '2.1': r'particle model|molecule|brownian|solid.*liquid.*gas|gas pressure|random motion|absolute zero',
    '2.2': r'temperature|thermometer|thermal expansion|specific heat|heat capacity|specific latent|melting|boiling|evaporation|internal energy',
    '2.3': r'conduction|convection|thermal radiation|infrared radiation|thermal energ|insulat|cooling|heating',
    '3.1': r'\bwave|wavelength|frequency|amplitude|diffraction|wavefront|ripple tank|transverse|longitudinal',
    '3.2': r'\blight\b|ray of light|mirror|reflection|refraction|refractive|lens|focal|image|optical fibre|total internal|critical angle|prism',
    '3.3': r'electromagnetic spectrum|radio wave|microwave|infra.?red|ultraviolet|x-ray|gamma ray',
    '3.4': r'\bsound\b|echo|ultrasound|loudness|pitch|hearing|microphone',
    '4.1': r'\bmagnet|magnetic field|compass|magnetis|soft iron|permanent magnet',
    '4.2': r'electric charge|charged|electrostatic|\bcurrent\b|potential difference|\bvoltage\b|e\.m\.f|resistance|resistivity|coulomb',
    '4.3': r'\bcircuit|series|parallel|resistor|ammeter|voltmeter|potential divider|thermistor|light.dependent|diode|logic gate',
    '4.4': r'electrical safety|fuse|circuit breaker|earth wire|live wire|neutral wire|three.core|appliance|mains',
    '4.5': r'electromagnetic induction|induced|generator|alternat|transformer|motor|motor effect|relay|solenoid|current.carrying.*magnetic|slip ring|split.ring',
    '5.1': r'nuclear model|nucleus|proton|neutron|electron|atomic number|proton number|nucleon|isotope|alpha.particle scattering|fission|fusion',
    '5.2': r'radioactiv|half.life|background radiation|count rate|ionising|alpha radiation|beta radiation|gamma radiation|decay',
    '6.1': r'solar system|planet|moon|orbit|comet|asteroid|gravitational.*orbit|earth.*sun',
    '6.2': r'\bstar|universe|galaxy|redshift|hubble|big bang|cosmic microwave|light.year|supernova'
}

# Physics papers normally follow the syllabus order. These priors are used only
# where extracted wording has no distinctive topic term (for example a diagram-
# led multiple-choice question).
MCQ_PRIORS = [
    (1, 3, '1.1'), (4, 6, '1.2'), (7, 8, '1.3'), (9, 10, '1.4'),
    (11, 15, '1.5'), (16, 17, '1.6'), (18, 21, '1.7'), (22, 22, '1.8'),
    (23, 24, '2.1'), (25, 26, '2.2'), (27, 28, '2.3'),
    (29, 29, '3.1'), (30, 31, '3.2'), (32, 32, '3.3'), (33, 33, '3.4'),
    (34, 34, '4.1'), (35, 36, '4.2'), (37, 37, '4.3'), (38, 38, '4.5'),
    (39, 40, '5.2')
]


def classify(text, paper_type, number, year):
    clean = re.sub(r'\s+', ' ', text).lower()
    scored = []
    for section, pattern in SECTION_PATTERNS.items():
        hits = re.findall(pattern, clean, re.I)
        if hits:
            scored.append((len(hits), section))
    scored.sort(key=lambda item: (-item[0], float(item[1])))
    if paper_type in (1, 2):
        if scored and scored[0][0] >= 2:
            sections = [scored[0][1]]
        elif scored:
            sections = [scored[0][1]]
        else:
            sections = [next(section for low, high, section in MCQ_PRIORS if low <= number <= high)]
        # Space physics entered these papers from 2023 and occupies the final questions.
        if year >= 2023 and number >= 38 and any(section.startswith('6.') for _, section in scored):
            sections = [next(section for _, section in scored if section.startswith('6.'))]
    else:
        sections = [section for score, section in scored if score >= max(1, scored[0][0] - 1)][:3] if scored else []
        if not sections:
            # Broad fallback follows the official syllabus order without inventing a topic label.
            broad = min(6 if year >= 2023 else 5, max(1, round(number / 2)))
            sections = [f'{broad}.1']
    chapters = sorted({int(section.split('.')[0]) for section in sections})
    return chapters, sorted(set(sections), key=float)


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
            'source': qp_entry['url'], 'markSchemeSource': ms_entry['url'],
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
            chapters, sections = classify(question_text, paper_number, number, qp_entry['year'])
            questions.append({
                'id': f'PHY-{qp_entry["year"]}-{qp_entry["session"].upper()}-{qp_entry["paper"]}-Q{number:02d}',
                'paper': paper_id, 'group': paper_group, 'paperType': paper_number,
                'year': qp_entry['year'], 'session': qp_entry['session'], 'variant': int(qp_entry['paper'][1]),
                'number': number, 'marks': 1 if answer else (int(total.group(1)) if total else None),
                'chapters': chapters, 'sections': sections, 'topics': sections, 'searchText': question_text,
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
