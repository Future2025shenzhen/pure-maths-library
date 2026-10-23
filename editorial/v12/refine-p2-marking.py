"""Concrete marking points after the P2 chapter 6 follow-up review.

Preserves all question statements, answers, marks, IDs and user records.
"""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = '66a2ab0'

def prior(path):
    return json.loads(subprocess.check_output(['git', 'show', f'{BASE}:{path}'], cwd=ROOT))

bank = prior('dist/data/bank.json')
manifest = prior('editorial/v12/review-manifest.json')
points = {
    'P2-C06-R01': [
        [('M1', r'使用$\sin^2x=1-\cos^2x$，得到$2\cos^2x-3\cos x+1=0$。'),
         ('A1', r'正确因式分解为$(2\cos x-1)(\cos x-1)=0$。')],
        [('M1', r'分别考虑$\cos x=1$与$\cos x=1/2$，保留两个因子对应的分支。'),
         ('A1', r'由$\cos x=1/2$得到$60^\circ,300^\circ$。'),
         ('A1', r'由$\cos x=1$得到$0^\circ,360^\circ$；最终四解完整，无额外解。')],
        [('M1', r'在新开区间中计入$60^\circ,300^\circ,420^\circ,660^\circ$以及$360^\circ$，或给出等价的周期计数。'),
         ('A1', r'得到5个解，并排除不属于开区间的$0^\circ,720^\circ$。')],
    ],
    'P2-C06-R02': [
        [('M1', r'代入$\cos^2\theta=1-\sin^2\theta$。'),
         ('A1', r'正确整理得到$4\sin^2\theta+4\sin\theta-3=0$。')],
        [('M1', r'因式分解为$(2\sin\theta-1)(2\sin\theta+3)=0$，得到候选值$1/2,-3/2$。'),
         ('A1', r'指出$-3/2<-1$，违反$-1\le\sin\theta\le1$，所以该分支没有实角。')],
        [('M1', r'使用有效分支$\sin\theta=1/2$，并在指定区间选择第一、第二象限角。'),
         ('A1', r'完整解集为$30^\circ,150^\circ$；负角段$(-180^\circ,0)$无额外解。')],
    ],
    'P2-C06-R24': [
        [('M1', r'把$\sin^2x$替换为$1-\cos^2x$。'),
         ('A1', r'整理得到$(k-1)\cos^2x=1$。')],
        [('M1', r'由原式推出$\cos^2x=1/(k-1)$，并考虑$k=1$无解。'),
         ('A1', r'使用$0<1/(k-1)\le1$，得到$k-1\ge1$。'),
         ('A1', r'给出完整范围$k\ge2$，包括等号。')],
        [('M1', r'$k=2$时得到$\cos^2x=1$，对应$x=0^\circ,180^\circ$。'),
         ('A1', r'计得2个解；$360^\circ$不在半开区间内。')],
        [('M1', r'$k>2$时有$0<1/(k-1)<1$，余弦取正负两个严格介于$-1$与1之间的非零值。'),
         ('A1', r'每个余弦值在一周内各给两个角，合计4个互异解。')],
    ],
}

def leaves(parts):
    for p in parts:
        if 'subparts' in p:
            yield from leaves(p['subparts'])
        else:
            yield p

byid = {q['id']: q for q in bank['questions']}
for qid, schemes in points.items():
    parts = list(leaves(byid[qid]['parts']))
    assert len(parts) == len(schemes), qid
    for part, scheme in zip(parts, schemes):
        assert sum(int(code[1:]) for code, _ in scheme) == part['marks'], qid
        part['scheme'] = [dict(code=code, marks=int(code[1:]), text=text) for code, text in scheme]

def digest(q):
    return hashlib.sha256(json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

manifest['afterHashes'] = {q['id']: digest(q) for q in bank['questions']}
manifest['followupReview'] = {
    'date': '2026-10-24',
    'scope': 'P2 Chapter 6: 25 active questions; statements, answers, interval endpoints and marking clarity',
    'markingRefined': list(points),
    'remainingWork': 'Other generic marking points and low-value subquestion combinations still need individual editing; this is not whole-bank certification.',
}
for path, value in [('dist/data/bank.json', bank), ('editorial/v12/review-manifest.json', manifest)]:
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
print('Refined 10 answer parts across 3 questions; question text, answers and marks unchanged')
