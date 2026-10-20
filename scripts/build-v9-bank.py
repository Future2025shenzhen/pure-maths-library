"""Rebuild the v9 browser bank from reviewed assets; keep question logic separate."""
from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];E=P/'editorial/v9'
bank=json.loads((P/'dist/data/bank.json').read_text());questions=[]
for stage,count in [('P1',270),('P2',245),('P3',255)]:
 qs=json.loads((E/(stage+'-editorial.json')).read_text());assert len(qs)==count and all(q['stage']==stage for q in qs)
 for q in qs:q['solutionRevision']=9
 questions+=qs
assert len(questions)==770 and len({q['id'] for q in questions})==770
bank.update(questions=questions,revision=9,updatedAt='2026-10-21');(P/'dist/data/bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2))
past=json.loads((P/'dist/data/past-bank.json').read_text());mapping=json.loads((E/'past-solutions.json').read_text())
for q in past['questions']:q.update(mapping[q['id']])
(P/'dist/data/past-bank.json').write_text(json.dumps(past,ensure_ascii=False,indent=2));print('Rebuilt770 original and323 structured authentic solutions')
