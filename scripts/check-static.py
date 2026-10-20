from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]/'dist'
a=json.loads((root/'data/bank.json').read_text());b=json.loads((root/'data/past-bank.json').read_text())
assert len(a['questions'])==770
assert len(b['questions'])==323
assert len(b['papers'])==33
assert len({q['id'] for q in a['questions']+b['questions']})==1093
for stage,chapters in a['chapters'].items():
 for c in chapters:
  assert sum(q['stage']==stage and q['chapters'][0]==c['id'] for q in a['questions'])==(40 if stage=='P3' and c['id']==6 else 35 if stage in ['P2','P3'] and c['id']==7 else 30), (stage,c['id'],'primary count')
  assert sum(q['stage']==stage and c['id'] in q['chapters'] for q in a['questions'])>=30, (stage,c['id'],'associated count')
 for q in a['questions']:
  if q['stage']==stage:assert q['chapters'] and len(q['chapters'])==len(set(q['chapters'])) and all(any(c['id']==n for c in chapters) for n in q['chapters']),q['id']
index=json.loads((root/'data/classification.json').read_text())['questions']
refs={q['id']:q for q in b['questions']}
for q in a['questions']:
 assert q['editorialRevision']==(8 if q.get('difficulty')=='challenge' else 7) and q['sourceReferences'] and q['adaptationNote'],q['id']
 assert index[q['id']]['stage']==q['stage'] and set(index[q['id']]['chapters'])==set(q['chapters']),q['id']
 for r in q['sourceReferences']:assert r['questionId'] in refs and refs[r['questionId']]['stage']==q['stage'] and refs[r['questionId']]['year']==r['year']<2024,q['id']
for q in b['questions']:
 assert q['year']<2024 and q['solutionZh'] and q['pages']
 for p in q['pages']:assert (root/p['image']).is_file()
for p in b['papers']:
 assert (root/p['pdf']).is_file() and (root/p['markScheme']).is_file()
 assert sum(q['marks'] for q in b['questions'] if q['paper']==p['id'])==75
for filename in ['index.html','app.js','past.html','past.js','core.js','style.css']:
 assert 'chatgpt.site' not in (root/filename).read_text()
for q in a['questions']:
 for path in re.findall(r'assets/[^"\s<>]+',q['stem']):assert (root/path).is_file()
print('PASS: 770 originals, 750 base +20 challenges; 323 pre-2024 questions, 33 complete 75-mark papers; local assets.')

