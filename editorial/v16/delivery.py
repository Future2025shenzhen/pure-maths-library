import collections,csv,html,json,re,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent
D=ROOT/'editorial/overhaul/re-audit-01';D.mkdir(parents=True,exist_ok=True)
bank=json.loads((ROOT/'dist/data/bank.json').read_text());live=[q for q in bank['questions'] if q['id'].startswith('P1-C07-') and not q.get('withdrawn')]
live.sort(key=lambda q:q['originalNumber']);assert len(live)==21
mapping=json.loads((D/'02-approved-mapping.json').read_text())
for m in mapping:m['status']='executed-after-user-confirmation';m['result']='历史ID继续保留但退出日常练习与组卷' if m['decision']=='删除' else m['nextId']
for n in [37,38]:mapping.append({'oldId':'—','previousState':'not-existing','decision':'新增','nextId':f'P1-C07-R{n}','status':'executed-after-user-confirmation','reason':'按B3补录，独立题稿、单源及分步评分已核查','result':f'P1-C07-R{n}'})
(D/'04-executed-mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
with (D/'04-executed-mapping.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['旧题编号','处置结论','新/保留编号','理由','执行结果'])
 for m in mapping:w.writerow([m['oldId'],m['decision'],m['nextId'] or '—',m['reason'],m['result']])
sources=collections.defaultdict(list)
for q in bank['questions']:
 if not q.get('withdrawn'):
  for s in q.get('sourceReferences',[]):sources[s['questionId']].append(q['id'])
scoped={s:{'usesInChapter':len([i for i in ids if i.startswith('P1-C07-')]),'usesInWholeActiveBank':len(sources[s]),'questionIdsInWholeActiveBank':sources[s]} for s in sorted({q['sourceReferences'][0]['questionId'] for q in live}) for ids in [sources[s]]}
assert max(x['usesInWholeActiveBank'] for x in scoped.values())<=3
(D/'05-source-ledger.json').write_text(json.dumps({'status':'executed','scope':'current chapter sources checked against whole active bank','chapter':scoped,'unreviewedSaturatedSourceCount':sum(len(ids)>3 for ids in sources.values()),'allObservedSources':dict(sorted(sources.items()))},ensure_ascii=False,indent=2)+'\n')
lines=['# 本批来源台账','','每个本章来源均对全库现役题查重，最多3次；未复审旧题的超额引用仍保留为待办，不冒称全库通过。','','|真题来源|本章次数|全库现役次数|全库对应题号|','|---|---:|---:|---|']
for s,d in scoped.items():lines.append(f"|{s}|{d['usesInChapter']}|{d['usesInWholeActiveBank']}|{', '.join(d['questionIdsInWholeActiveBank'])}|")
(D/'05-source-ledger.md').write_text('\n'.join(lines)+'\n')
forms=[dict(id=q['id'],family=q['examFamily'],template=q['questionTemplate'],source=q['sourceReferences'][0]['questionId'],marks=q['marks'],parts=len(q['parts'])) for q in live]
(D/'06-question-form-ledger.json').write_text(json.dumps({'status':'executed','families':dict(collections.Counter(q['examFamily'] for q in live)),'questions':forms,'classicExemptions':[],'crossBatchNote':'P1 C04/C09 prior entries remain provisional until their re-audit; no false claim of a completed global quality audit'},ensure_ascii=False,indent=2)+'\n')
lines=['# 本批问法台账','','|题号|主族|实际设问路线|分值|顶层小问数|','|---|---|---|---:|---:|']
for row in forms:lines.append(f"|{row['id']}|{row['family']}|{row['template']}|{row['marks']}|{row['parts']}|")
lines+=['','配额G1—G6为5/3/4/3/3/3。各族具体模板至少3种；没有A3豁免题。','相邻重复检查：同心逆求/下界/双设计三条路线、重复单元逆求/最大整数/弧弦交替三条路线、坐标长度比/截轴阈值/参数最小值三条路线分别核对，不靠逐题改标题规避重复。']
(D/'06-question-form-ledger.md').write_text('\n'.join(lines)+'\n')
md=['# P1 第7章 Radians · 本批21题与建议评分','','题目为原创变式；来源及难度定位放在答案内。评分点是建议分值，等价正确解法应予认可。']
def figure_paths(s):return s.replace('src="assets/','src="../../../dist/assets/')
for q in live:
 md+=['',f"## {q['id']} · P1 第7章 · {q['type']} · {q['marks']} marks",'',figure_paths(q['stem']),'']
 for i,p in enumerate(q['parts']):md.append(f"**({chr(97+i)})** {p['text']} **[{p['marks']}]**\n")
 md+=['### 答案与解析','',q['difficultyPosition'],'',f"**变式来源：** {q['sourceReferences'][0]['questionId']}。原题大意：{q['sourceSummary']}。",'',f"**改编维度：** {'、'.join(q['adaptationDimensions'])}。",'',f"**保留的考点本质：** {q['examEssence']}。",'']
 for i,p in enumerate(q['parts']):
  md.append(f"**({chr(97+i)}) 答案：** {p['answer']}\n")
  md.extend(f'{j+1}. {s}' for j,s in enumerate(p['solutionSteps']))
  md+=['','建议评分：'+'；'.join(f"{s['code']} [{s['marks']}] {s['text']}" for s in p['scheme'])+'。','']
 md+=['**易错点与命题思路：**','']+[f'- {s}' for s in q['errorNotes']]+['- '+q['designNote'],'']
(D/'QUESTIONS.md').write_text('\n'.join(md)+'\n')
# The standalone teacher HTML has the same authored math, with formula text escaped before HTML parsing.
def esc(s):return html.escape(str(s))
def stem(s):
 pieces=re.split(r'(<figure\b.*?</figure>)',s,flags=re.S)
 return ''.join(x if x.startswith('<figure') else esc(x) for x in pieces)
body=[]
for q in live:
 body.append(f'<section class="question"><h2>{esc(q["id"])} · P1 第7章 · {esc(q["type"])} <span>[{q["marks"]} marks]</span></h2><div lang="en">{stem(q["stem"])}')
 for i,p in enumerate(q['parts']):body.append(f'<p><b>({chr(97+i)})</b> {esc(p["text"])} <b class="marks">({p["marks"]})</b></p>')
 body.append('</div><div class="answer"><h3>答案与建议评分</h3><p>'+esc(q['difficultyPosition'])+'</p><p><b>变式来源：</b>'+esc(q['sourceReferences'][0]['questionId'])+'。'+esc(q['sourceSummary'])+'</p><p><b>改编维度：</b>'+esc('、'.join(q['adaptationDimensions']))+'</p><p><b>保留的考点本质：</b>'+esc(q['examEssence'])+'</p>')
 for i,p in enumerate(q['parts']):
  body.append(f'<h4>({chr(97+i)}) {esc(p["answer"])}</h4><ol>'+''.join('<li>'+esc(s)+'</li>' for s in p['solutionSteps'])+'</ol><p class="scheme">'+'；'.join(esc(f"{s['code']} [{s['marks']}] {s['text']}") for s in p['scheme'])+'</p>')
 body.append('<h4>易错点与命题思路</h4><ul>'+''.join('<li>'+esc(s)+'</li>' for s in q['errorNotes']+[q['designNote']])+'</ul></div></section>')
header='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>P1 Radians · 21 reviewed questions</title><link rel="stylesheet" href="assets/katex/katex.min.css"><style>body{max-width:900px;margin:30px auto;padding:0 24px;color:#111;font:16px/1.8 Georgia,"Noto Sans CJK SC",serif}h1{font-size:26px}h2{font-size:19px;line-height:1.5;border-bottom:1px solid #333;padding-bottom:10px}h2 span,.marks{float:right}figure{text-align:center;margin:20px}figure img,figure svg{max-width:100%;width:460px;max-height:290px}figcaption{font-size:13px}.answer{background:#f7f7f7;padding:20px;margin-top:24px}.scheme{font-size:13px}.question{margin:55px 0}li{margin:6px 0}.katex{font-size:1.05em}@media print{body{margin:0;max-width:none;font-size:11pt}.question{break-before:page;margin:0}.answer{background:white;padding:10px 0}figure{break-inside:avoid}li{break-inside:avoid}h2,h3,h4{break-after:avoid}}@page{size:A4;margin:16mm}</style><h1>P1 Chapter 7 · Radians</h1><p>21 original adapted questions · 198 suggested marks<br>题目英文，答案与分步评分中文；来源真题截至2025年6月。</p>'''
footer='''<script src="assets/katex/katex.min.js"></script><script src="assets/katex/contrib/auto-render.min.js"></script><script>renderMathInElement(document.body,{delimiters:[{left:'$',right:'$',display:false}],throwOnError:true,strict:'ignore'});document.documentElement.dataset.rendered='true';</script></html>'''
EXPORT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/tmp/pure-maths-v16-delivery');EXPORT.mkdir(parents=True,exist_ok=True)
(EXPORT/'teacher.html').write_text(header+''.join(body)+footer)
for asset in ['assets/katex','assets/v16-figures']:
 shutil.copytree(ROOT/'dist'/asset,EXPORT/asset,dirs_exist_ok=True)
for q in live:
 for relative in re.findall(r'src="(assets/[^\"]+)"',q['stem']):
  dest=EXPORT/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'dist'/relative,dest)
for f in D.glob('*'):
 if f.is_file():shutil.copy2(f,EXPORT/f.name)
shutil.copy2(HERE/'p1-radians.json',EXPORT/'p1-radians.json')
shutil.copy2(ROOT/'backend/006-overhaul-catalog.sql',EXPORT/'006-overhaul-catalog.sql')
print('Delivery: mapping, two ledgers, 21 complete questions and standalone teacher HTML')
