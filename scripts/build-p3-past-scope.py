"""Build the manually reviewed P3 chapter scope and its source fingerprints.

The annotations are question-specific. Do not infer them from keywords, old
primary-chapter tags or which functions happen to occur in a formula.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'

def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def build():
 bank=json.loads((DIST/'data/past-bank.json').read_text())
 old=json.loads((DIST/'data/classification.json').read_text())['questions']
 source=ROOT/'editorial/p3-targeted/requirements.txt'
 annotations={};date=None;number=0
 for line in source.read_text().splitlines():
  if not line.strip() or line.startswith('#'):continue
  if line.startswith('['):date=line[1:-1];number=0;continue
  number+=1;identifier=f'P3-{date}-Q{number:02d}'
  requirements=[]
  for part in line.split(';'):
   chapter,description=part.split(':',1)
   requirements.append({'chapter':int(chapter),'skills':description.split('、')})
  chapters=sorted(item['chapter'] for item in requirements)
  assert chapters and len(chapters)==len(set(chapters)) and all(1<=n<=8 for n in chapters),identifier
  annotations[identifier]={'requiredChapters':chapters,'requirements':requirements}
 questions={q['id']:q for q in bank['questions'] if q['stage']=='P3'}
 assert set(annotations)==set(questions),(set(questions)-set(annotations),set(annotations)-set(questions))
 evidence={};hashes={};changes=[]
 for identifier,annotation in annotations.items():
  q=questions[identifier];paper=next(p for p in bank['papers'] if p['id']==q['paper'])
  sources=[paper['pdf'],paper['markScheme']]
  for path in sources:
   if path not in hashes:hashes[path]=hashlib.sha256((DIST/path).read_bytes()).hexdigest()
  evidence[identifier]={'questionFingerprint':digest({'searchText':q['searchText'],'sourcePages':q['sourcePages'],'marks':q['marks']}),'answerFingerprint':digest(q['markSchemePages']),'questionPdf':paper['pdf'],'questionPages':q['sourcePages'],'markSchemePdf':paper['markScheme'],'markSchemePages':sorted({p.get('sourcePage',p['page']) for p in q['markSchemePages']}),'previousChapters':old[identifier]['chapters']}
  if sorted(old[identifier]['chapters'])!=annotation['requiredChapters']:changes.append({'id':identifier,'before':old[identifier]['chapters'],'after':annotation['requiredChapters']})
 payload={'version':1,'stage':'P3','questionCount':len(annotations),'policy':'Whole-question chapter requirements. Standard differentiation/integration rules and basic prerequisite algebra/trigonometry stay within the calculus chapter; separately assessed identities, addition/double-angle/auxiliary-angle formulae and other P3 chapter skills remain explicit requirements.','questions':annotations}
 (DIST/'data/p3-past-scope.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'editorial/p3-targeted/source-audit.json').write_text(json.dumps({'sourceFileSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'pdfSha256':hashes,'questions':evidence,'changedChapterSets':changes},ensure_ascii=False,indent=2)+'\n')
 print(f'P3 reviewed scope: {len(annotations)} questions; {len(changes)} corrected chapter sets')

if __name__=='__main__':build()
