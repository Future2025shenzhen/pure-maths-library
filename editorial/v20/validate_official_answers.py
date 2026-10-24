"""Audit the actual extracted PDFs, not just their JSON mappings (PyMuPDF)."""
import hashlib
import json
import re
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[2]
bank=json.loads((ROOT/'dist/data/past-bank.json').read_text())
audit={r['id']:r for r in json.loads((ROOT/'editorial/v20/official-answer-audit.json').read_text())}
docs={}
source_hashes={}
results=[]
for q in bank['questions']:
    record=audit[q['id']]
    source=ROOT/'dist'/record['sourcePdf']
    if str(source) not in source_hashes:
        source_hashes[str(source)]=hashlib.sha256(source.read_bytes()).hexdigest()
    assert source_hashes[str(source)]==record['sourceSha256'],q['id']+' source changed'
    text=''
    for ref in q['markSchemePages']:
        if ref['pdf'] not in docs:
            docs[ref['pdf']]=fitz.open(ROOT/'dist'/ref['pdf'])
        page=docs[ref['pdf']][ref['page']-1]
        assert not page.first_annot,q['id']+' PDF annotation'
        text+=page.get_text()
    assert not re.search(r'\bNotes?\b',text,re.I),q['id']+' remaining Note text'
    allocations=sum(int(n) for n in re.findall(r'[MAB]\s*(\d)',text))
    # Alternatives may contain another complete set of allocations. The lower
    # bound catches missing score rows, including ddM1 and spaced "A 1" labels.
    assert allocations>=q['marks'],(q['id'],allocations,q['marks'])
    assert re.search(r'[MAB]\s*\d',text),q['id']+' no official scoring codes'
    results.append({'id':q['id'],'pages':len(q['markSchemePages']),
                    'markAllocationsAtLeastQuestionTotal':True,'notesAbsent':True,'annotationsAbsent':True})
assert len(results)==572
(ROOT/'editorial/v20/pdf-content-audit.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(results)} answers across {len(docs)} extracted official PDFs; no Notes, no annotations, no missing mark allocations; original source hashes match.')
