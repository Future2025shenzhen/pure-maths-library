import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK = ROOT / 'dist/data/bank.json'
CLASSIFICATION = ROOT / 'dist/data/classification.json'
CONTENT = ROOT / 'editorial/v15/p1-c04-c09.json'

active = json.loads(CONTENT.read_text())['questions']
active_by_id = {q['id']: q for q in active}

deleted_reasons = {
    **{qid: '章内题型或图形高度重复，改编维度不足，不能提供独立训练价值。' for qid in [
        'P1-C04-R02','P1-C04-R05','P1-C04-R07','P1-C04-R08','P1-C04-R12',
        'P1-C04-R13','P1-C04-R14','P1-C04-R16','P1-C04-R19','P1-C04-R23',
        'P1-C04-R26','P1-C04-R27','P1-C04-R29']},
    **{qid: '积分路径过直或与章内题重复，难度和设问结构未达到真题级标准。' for qid in [
        'P1-C09-R04','P1-C09-R07','P1-C09-R11','P1-C09-R12','P1-C09-R14',
        'P1-C09-R15','P1-C09-R20','P1-C09-R21','P1-C09-R24','P1-C09-R26',
        'P1-C09-R27','P1-C09-R28','P1-C09-R29']},
    **{qid: '主要考查图像变换，且与本批新题同族重复，移出三角比章节后停用。' for qid in [
        'P1-C06-R12','P1-C06-R17','P1-C06-R26','P1-C06-R30']},
}

bank = json.loads(BANK.read_text())
seen = set()
rebuilt = []
for old in bank['questions']:
    qid = old['id']
    if qid in active_by_id:
        rebuilt.append(active_by_id[qid])
        seen.add(qid)
        continue

    if qid in deleted_reasons:
        old['withdrawn'] = True
        old['withdrawalReason'] = deleted_reasons[qid]
        old['editorialRevision'] = 15
        old['contentUpdatedAt'] = '2026-10-24'

    # Chapter 4 now contains only questions whose primary assessment intent is
    # graph transformation. This also fixes historical sidebar/filter drift.
    if old['stage'] == 'P1' and not qid.startswith('P1-C04-') and 4 in old.get('chapters', []):
        old['chapters'] = [c for c in old['chapters'] if c != 4]
        old['editorialRevision'] = 15
        old['contentUpdatedAt'] = '2026-10-24'
    rebuilt.append(old)

for q in active:
    if q['id'] not in seen:
        rebuilt.append(q)

bank['questions'] = rebuilt
bank['version'] = 15
bank['updatedAt'] = '2026-10-24'
bank['editorialNote'] = ('P1 Chapters 4 and 9 fully reviewed against P1 papers through June 2025; '
                         'graph-transformation cross-topic placement normalised.')

ids = [q['id'] for q in rebuilt]
assert len(ids) == len(set(ids)) == 788
active_questions = [q for q in rebuilt if not q.get('withdrawn')]
assert len(active_questions) == 740
for chapter_id in (4, 9):
    chapter = [q for q in rebuilt if q['stage'] == 'P1' and q['id'].startswith(f'P1-C{chapter_id:02d}-')]
    assert len(chapter) == 36
    assert len([q for q in chapter if not q.get('withdrawn')]) == 23
c6 = [q for q in rebuilt if q['stage'] == 'P1' and q['id'].startswith('P1-C06-')]
assert len(c6) == 30 and len([q for q in c6 if not q.get('withdrawn')]) == 26
assert len([q for q in rebuilt if q.get('withdrawn')]) == 48
BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')

classification = json.loads(CLASSIFICATION.read_text())
classification['version'] = 15
classification['questions'].update({
    q['id']: {'stage': q['stage'], 'chapters': q.get('chapters', [])}
    for q in rebuilt
})
CLASSIFICATION.write_text(json.dumps(classification, ensure_ascii=False, indent=2) + '\n')
print('applied V15: 788 historical, 740 active; P1 C04/C09 23 active each; 48 withdrawn total')
