import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT / 'dist/data/bank.json'
CLASSIFICATION = ROOT / 'dist/data/classification.json'
CONTENT = ROOT / 'editorial/v14/p1-radians.json'

active = json.loads(CONTENT.read_text())['questions']
active_by_id = {q['id']: q for q in active}
deleted_reasons = {
    'P1-C07-R04': '与同章题的设问和图形高度重复，思维路径不足。',
    'P1-C07-R05': '只替换数值，未形成真题级改编。',
    'P1-C07-R06': '步骤过短且与相邻题重复。',
    'P1-C07-R09': '线性三步结构过直，缺少有效判断。',
    'P1-C07-R12': '难度低于真题基线，改编维度不足。',
    'P1-C07-R14': '图形和问法与章内既有题高度同质。',
    'P1-C07-R16': '只考直接代公式，卷位与分值不匹配。',
    'P1-C07-R17': '与固定模板重复且没有新的思维增量。',
    'P1-C07-R18': '把参数与证明要求简化成直接计算。',
    'P1-C07-R19': '组合图形训练流程与相邻题重复。',
    'P1-C07-R22': '情境变化未改变解题路径。',
    'P1-C07-R26': '设问单一，未达到真题难度。',
    'P1-C07-R29': '与弧长比例题结构近乎相同，缺少独立价值。',
}

bank = json.loads(BANK.read_text())
seen = set()
rebuilt = []
for old in bank['questions']:
    qid = old['id']
    if qid in active_by_id:
        rebuilt.append(active_by_id[qid])
        seen.add(qid)
    else:
        if qid in deleted_reasons:
            old['withdrawn'] = True
            old['withdrawalReason'] = deleted_reasons[qid]
            old['editorialRevision'] = 14
            old['contentUpdatedAt'] = '2026-10-24'
        rebuilt.append(old)

for q in active:
    if q['id'] not in seen:
        rebuilt.append(q)

bank['questions'] = rebuilt
bank['version'] = 14
bank['updatedAt'] = '2026-10-24'
bank['editorialNote'] = 'P1 Chapter 7 Radians fully reviewed against 21 P1 papers through June 2025.'

ids = [q['id'] for q in rebuilt]
assert len(ids) == len(set(ids)) == 776
chapter = [q for q in rebuilt if q['stage'] == 'P1' and q['id'].startswith('P1-C07-')]
assert len(chapter) == 36
assert {q['id'] for q in chapter if q.get('withdrawn')} == set(deleted_reasons)
assert len([q for q in chapter if not q.get('withdrawn')]) == 23
assert len([q for q in rebuilt if not q.get('withdrawn')]) == 758
BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')

classification = json.loads(CLASSIFICATION.read_text())
classification['version'] = 14
for q in active:
    classification['questions'][q['id']] = {'stage': q['stage'], 'chapters': q['chapters']}
CLASSIFICATION.write_text(json.dumps(classification, ensure_ascii=False, indent=2) + '\n')
print('applied V14: 776 historical, 758 active, P1 Radians 23 active / 13 withdrawn')
