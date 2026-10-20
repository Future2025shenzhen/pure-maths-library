"""Rebuild v8 from the reviewed v7 bank snapshot and v8 question assets."""
from pathlib import Path
import json,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parents[1];R=P/'editorial/v8'
bank=json.loads((P/'dist/data/bank.json').read_text());base=[q for q in bank['questions'] if q.get('difficulty')!='challenge'];assert len(base)==750
past=json.loads((P/'dist/data/past-bank.json').read_text());refs={q['id']:q for q in past['questions']};extra=[]
for f in ['p3-diff.json','selected.json']:
 for q in json.loads((R/f).read_text()):
  for r in q['sourceReferences']:
   a=refs[r['questionId']];assert a['stage']==q['stage'] and a['year']<2024;r.update(year=a['year'],paper=a['paper'],number=a['number'],month=a['month'])
  svg=q.pop('figureSvg','')
  if svg:
   ET.fromstring(svg);q['stem']+='<figure class="rewrite-figure">'+svg+'<figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'
  q.update(origin='original-substantive-adaptation-2026',review='internal-review-only',editorialRevision=8,difficulty='challenge');q.setdefault('answerFigure','');q.setdefault('family',q['id']);extra.append(q)
assert len(extra)==20
bank.update(questions=base+extra,revision=8,updatedAt='2026-10-20')
(P/'dist/data/bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2))
(P/'dist/data/classification.json').write_text(json.dumps({'version':8,'questions':{q['id']:{'stage':q['stage'],'chapters':q['chapters']} for q in base+extra+past['questions']}},ensure_ascii=False,separators=(',',':')))
print('Rebuilt 770 originals and1093 classifications')
