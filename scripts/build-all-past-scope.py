"""Compile question-specific whole-question annotations; never infer scope from keywords."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'dist'; E=ROOT/'editorial/all-targeted'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def read(stage):
 out={};paper=None;n=0
 for line in (E/f'{stage}-requirements.txt').read_text().splitlines():
  line=line.strip()
  if not line or line.startswith('#'):continue
  if line.startswith('['):paper=line[1:-1];n=0;continue
  n+=1;id=f'{stage}-{paper}-Q{n:02d}'
  assert id not in out,id
  if stage=='CS':
   sections=sorted(line.split(','),key=lambda x:tuple(map(int,x.split('.'))));assert len(sections)==len(set(sections)),id
   out[id]={'requiredSections':sections}
  else:
   requirements=[{'chapter':int(p.split(':',1)[0]),'skills':p.split(':',1)[1].split('、')} for p in line.split(';')]
   chapters=sorted(r['chapter'] for r in requirements)
   assert len(chapters)==len(set(chapters)) and all(1<=c<=(9 if stage=='P1' else 8) for c in chapters),id
   out[id]={'requiredChapters':chapters,'requirements':requirements}
 return out

def build():
 maths=json.loads((D/'data/past-bank.json').read_text());cs=json.loads((D/'data/cs-question-bank.json').read_text());tax=json.loads((D/'data/cs-chapters.json').read_text());valid={s['id'] for c in tax['chapters'] for s in c['sections']}
 annotations={};evidence={};hashes={};changes=[]
 old=json.loads((D/'data/classification.json').read_text())['questions']
 for stage in ['P1','P2','CS']:
  ann=read(stage);bank=cs if stage=='CS' else maths;qs={q['id']:q for q in bank['questions'] if stage=='CS' or q['stage']==stage}
  assert set(ann)==set(qs),(stage,set(qs)-set(ann),set(ann)-set(qs))
  for id,a in ann.items():
   q=qs[id];p=next(p for p in bank['papers'] if p['id']==q['paper'])
   if stage=='CS':assert a['requiredSections'] and set(a['requiredSections'])<=valid,id
   before=q['sections'] if stage=='CS' else old[id]['chapters'];after=a.get('requiredSections',a.get('requiredChapters'))
   if sorted(before)!=sorted(after):changes.append({'id':id,'before':before,'after':after})
   paths=[p['qp'],p['ms']] if stage=='CS' else [p['pdf'],p['markScheme']]
   for path in paths:
    if path not in hashes:hashes[path]=hashlib.sha256((D/path).read_bytes()).hexdigest()
   evidence[id]={'questionFingerprint':digest({k:q[k] for k in (['searchText','pages','marks'] if stage=='CS' else ['searchText','sourcePages','marks'])}),'answerFingerprint':digest(q['markSchemePages']),'questionPdf':paths[0],'markSchemePdf':paths[1]}
  payload={'version':1,'questionCount':len(ann),'policy':'Whole question, including all subparts. Basic methods intrinsic to a chapter stay in that chapter; independently assessed chapters/sections are all required. Context and distractors alone do not add requirements.','questions':ann}
  target='cs-past-scope' if stage=='CS' else stage.lower()+'-past-scope'
  (D/f'data/{target}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n');annotations.update(ann)
  print(stage,len(ann))
 (E/'source-audit.json').write_text(json.dumps({'annotationSha256':{s:hashlib.sha256((E/f'{s}-requirements.txt').read_bytes()).hexdigest() for s in ['P1','P2','CS']},'pdfSha256':hashes,'questions':evidence,'changedScopes':changes},ensure_ascii=False,indent=2)+'\n')
 print('Corrected scope sets:',len(changes))
if __name__=='__main__':build()
