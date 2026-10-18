from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]/'dist'
a=json.loads((root/'data/bank.json').read_text());b=json.loads((root/'data/past-bank.json').read_text())
assert len(a['questions'])==750
assert len(b['questions'])==323
assert len(b['papers'])==33
assert len({q['id'] for q in a['questions']+b['questions']})==1073
for stage,chapters in a['chapters'].items():
 for c in chapters:assert sum(q['stage']==stage and c['id'] in q['chapters'] for q in a['questions'])==30
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
print('PASS: 750 originals, 25x30 chapters; 323 pre-2024 questions, 33 complete 75-mark papers; local assets.')
