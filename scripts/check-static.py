from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]/'dist'
a=json.loads((root/'data/bank.json').read_text());b=json.loads((root/'data/past-bank.json').read_text())
assert len(a['questions'])==790
assert len(b['questions'])==323
assert len(b['papers'])==33
assert len({q['id'] for q in a['questions']+b['questions']})==1113
for stage,chapters in a['chapters'].items():
 for c in chapters:
  expected=38 if stage=='P1' and c['id']==7 else 36 if stage=='P1' and c['id'] in [4,9] else 40 if stage=='P3' and c['id']==6 else 35 if stage in ['P2','P3'] and c['id']==7 else 30
  assert sum(q['stage']==stage and q['chapters'][0]==c['id'] for q in a['questions'])==expected, (stage,c['id'],'primary count')
  assert sum(q['stage']==stage and c['id'] in q['chapters'] for q in a['questions'])>=30, (stage,c['id'],'associated count')
 for q in a['questions']:
  if q['stage']==stage:assert q['chapters'] and len(q['chapters'])==len(set(q['chapters'])) and all(any(c['id']==n for c in chapters) for n in q['chapters']),q['id']
index=json.loads((root/'data/classification.json').read_text())['questions']
refs={q['id']:q for q in b['questions']}
for q in a['questions']:
 assert q['editorialRevision'] in [7,8,12,14,15,16] and (q['sourceReferences'] or q.get('textbookSource')) and q['adaptationNote'],q['id']
 assert index[q['id']]['stage']==q['stage'] and set(index[q['id']]['chapters'])==set(q['chapters']),q['id']
 for r in q['sourceReferences']:
  if q['editorialRevision'] in [14,15,16]:assert 2019<=r['year']<=2025,q['id']
  else:assert r['questionId'] in refs and refs[r['questionId']]['stage']==q['stage'] and refs[r['questionId']]['year']==r['year']<2024,q['id']
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
print('PASS: 790 historical originals including 20 additions; 323 pre-2024 questions, 33 complete 75-mark papers; local assets.')


# v9 solution structure and private-note deployment assets.
def leaves(parts):
 for p in parts:
  if p.get('subparts'):yield from leaves(p['subparts'])
  else:yield p
for q in a['questions']:
 for p in leaves(q['parts']):assert p.get('approach') and p.get('solutionSteps'),q['id']
for q in b['questions']:assert q.get('solutionSections'),q['id']
for f in ['note-store.js','question-notes.js','notes-setup.html','notes-setup.js','assets/setup/005-question-notes.sql']:assert (root/f).is_file(),f
