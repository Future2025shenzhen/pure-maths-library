from pathlib import Path
import json,re,collections,xml.etree.ElementTree as ET,hashlib,shutil
P=Path(__file__).resolve().parents[1];R=P/'editorial/v7';(R/'figures').mkdir(exist_ok=True);old=json.loads((P/'dist/data/bank.json').read_text());past=json.loads((P/'dist/data/past-bank.json').read_text());actual={q['id']:q for q in past['questions']}
expected={f'{st}-C{c["id"]:02d}.json' for st,cs in old['chapters'].items() for c in cs};available={f.name for f in (R/'chapters').glob('*.json')};assert expected<=available,('missing',expected-available)
commands=r'(?:sqrt|dfrac|tfrac|frac|sin|cos|tan|sec|csc|cot|arcsin|arccos|arctan|ln|log|exp|pi|theta|alpha|beta|gamma|delta|lambda|mu|omega|geq?|leq?|ne|neq|infty|in|notin|cup|cap|Rightarrow|Longrightarrow|therefore|because|times|cdot|pm|mp|left|right|mathrm|text|displaystyle|sum|int|ldots|dots|prime|circ|overline|begin|end|quad|qquad|vert|lvert|rvert|binom|choose|lim|to|partial|arccot)(?![A-Za-z])'
def norm(v):
 if isinstance(v,str):
  # Undo only repeated command escapes, preserving deliberate TeX row separators.
  return re.sub(r'\\{2,}(?='+commands+')',lambda m:'\\',v)
 if isinstance(v,list):return [norm(x) for x in v]
 if isinstance(v,dict):return {k:norm(x) for k,x in v.items()}
 return v
questions=[];report=[]
for file in sorted((R/'chapters').glob('*.json')):
 if file.name not in expected:continue
 qs=norm(json.loads(file.read_text()));assert len(qs)==30,file
 for q in qs:
  assert q['id'].startswith(file.stem+'-R')
  for ref in q['sourceReferences']:
   a=actual[ref['questionId']];assert a['stage']==q['stage'] and a['year']==ref['year'] and a['year']<2024
   ref['paper']=a['paper'];ref['number']=a['number'];ref['month']=a['month']
  svg=q.pop('figureSvg','')
  if svg:
   ET.fromstring(svg)
   assert not re.search(r'<(?:script|foreignObject|image)\b|\son\w+\s*=|javascript:',svg,re.I),q['id']
   if 'role=' not in svg:svg=svg.replace('<svg','<svg role="img"',1)
   if 'aria-label' not in svg and '<title' not in svg:svg=svg.replace('<svg','<svg aria-label="Diagram for '+q['id']+'"',1)
   (R/'figures'/(q['id']+'.svg')).write_text(svg)
   q['stem']+='<figure class="rewrite-figure">'+svg+'<figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'
  q.setdefault('answerFigure','');q.setdefault('family',q['id']);q['origin']='original-substantive-adaptation-2026';q['review']='internal-review-only';q['editorialRevision']=7
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in json.dumps(q,ensure_ascii=False))
 questions+=qs
 report.append({'chapter':file.stem,'questions':len(qs),'marks':dict(collections.Counter(q['marks'] for q in qs)),'parts':dict(collections.Counter(len(q['parts']) for q in qs)),'figures':sum('<svg' in q['stem'] for q in qs),'multiChapter':sum(len(q['chapters'])>1 for q in qs),'types':dict(collections.Counter(q['type'] for q in qs))})
assert len(questions)==750;assert set(q['id'] for q in questions)==set(q['id'] for q in old['questions'])
old['questions']=questions;old['revision']=7;old['updatedAt']='2026-10-19';old['editorialNote']='2026原创实质改编；考法参照2024年前真题。每题来源及具体改编说明见答案；未完成外部教师逐题审阅。'
(R/'new-bank.json').write_text(json.dumps(old,ensure_ascii=False,indent=2))
index={'version':7,'questions':{q['id']:{'stage':q['stage'],'chapters':q['chapters']} for q in questions+past['questions']}}
(R/'new-classification.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')))
(R/'research/final-distribution.json').write_text(json.dumps({'questions':750,'chapters':report,'figures':sum(x['figures'] for x in report),'partCounts':dict(collections.Counter(len(q['parts']) for q in questions)),'multiChapter':sum(len(q['chapters'])>1 for q in questions),'marks':dict(collections.Counter(q['marks'] for q in questions))},ensure_ascii=False,indent=2))
shutil.copy2(R/'new-bank.json',P/'dist/data/bank.json');shutil.copy2(R/'new-classification.json',P/'dist/data/classification.json')
print('Integrated750 questions, figures',sum(x['figures'] for x in report))
