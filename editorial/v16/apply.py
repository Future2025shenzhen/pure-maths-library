import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
folder=Path(__file__).parent
bankpath=ROOT/'dist/data/bank.json'
bank=json.loads(bankpath.read_text())
active=json.loads((folder/'p1-radians.json').read_text())['questions']
new={q['id']:q for q in active}
reasons={4:'特殊角直接代入，弱于来源且缺少改编深度。',5:'面积差化为一次方程，失去来源的二次建模要求。',6:'弧长差、半径、面积均为直接顺算。',9:'特殊切线设置过简且未找到同族真题来源。',12:'教材底稿没有满足本轮A6的真题来源。',14:'直接代入三段，教材出处不能替代真题来源。',15:'将来源二次尺寸建模降为一次计算，切割延伸不足。',16:'等边设置消除了来源的角度构造。',17:'相似缩放拆成四问而无对应思维增量。',18:'教材固定特殊重叠设置，缺少本轮真题来源。',19:'直角特殊值使各问均为直接计算。',22:'整周比例、周界、三角形面积为独立一步三段。',26:'角差和三角形面积直接代入，缺少边界推理。',27:'给根后的扇形与弓形面积顺算，与R03重复且偏弱。',29:'固定特殊角直接代面积和周界，非前报告所称弧长比问题。',35:'重复R01对称拼接，末问占比计算虚高。',36:'与R23条件及核心路径完全相同，百分比不足以形成新题。'}
result=[];seen=set()
for old in bank['questions']:
 qid=old['id']
 if qid in new:result.append(new[qid]);seen.add(qid)
 elif qid.startswith('P1-C07-'):
  n=int(qid[-2:]);assert n in reasons,qid
  old.update(withdrawn=True,withdrawalReason=reasons[n],editorialRevision=16,contentUpdatedAt='2026-10-24');result.append(old)
 else:result.append(old)
result.extend(q for q in active if q['id'] not in seen)
bank.update(questions=result,version=16,revision=16,updatedAt='2026-10-24',editorialNote='P1 C07 re-audited after user approval: 21 active; other chapters await re-audit.')
assert len(result)==len({q['id'] for q in result})==790
assert sum(not q.get('withdrawn') for q in result)==738
bankpath.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
cp=ROOT/'dist/data/classification.json';classification=json.loads(cp.read_text());classification['version']=16
for q in result:classification['questions'][q['id']]={'stage':q['stage'],'chapters':q['chapters']}
cp.write_text(json.dumps(classification,ensure_ascii=False,indent=2)+'\n')
(ROOT/'dist/version.json').write_text(json.dumps(dict(siteVersion='v16',theme='Minimal',contentRevision=16,date='2026-10-24'),indent=2)+'\n')
print('V16 applied: 790 historical / 738 active; C07 21 active, 17 withdrawn')
