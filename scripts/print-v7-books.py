from pathlib import Path
import json,html,re,asyncio,shutil
from playwright.async_api import async_playwright
import fitz
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'editorial/v7';P=ROOT/'dist';OUT=ROOT/'exported-v7';OUT.mkdir(exist_ok=True,parents=True);(OUT/'分章题册').mkdir(exist_ok=True)
D=json.loads((P/'data/bank.json').read_text());TMP=P/'print-v7';TMP.mkdir(exist_ok=True)
def fmt(s):return re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',lambda m:html.escape(m[0]),str(s))
def part(p,i,answer=False,sub=False):
 label='('+(['i','ii','iii','iv','v'][i] if sub else chr(97+i))+')'
 if p.get('subparts'):
  return f'<section class="group"><p><b>{label}</b> {fmt(p["text"])}</p>'+''.join(part(a,j,answer,True) for j,a in enumerate(p['subparts']))+'</section>'
 if not answer:return f'<div class="part"><b>{label}</b><div>{fmt(p["text"])}</div><span>({p["marks"]})</span></div>'
 return f'<section class="apart"><h3>{label} · {p["marks"]} marks</h3><p class="final">{fmt(p["answer"])}</p><p>{fmt(p["explanation"])}</p><table>'+''.join(f'<tr><td>{r["code"]}</td><td>{fmt(r["text"])}</td></tr>' for r in p['scheme'])+'</table></section>'
CSS='''@page{size:A4;margin:17mm 17mm 19mm}*{box-sizing:border-box}body{margin:0;font:12pt/1.7 Georgia,"Noto Serif CJK SC",serif;color:#111}h1,h2,h3,p{margin:0}.cover{break-before:page;break-after:page;padding-top:35mm}.cover h1{font-size:25pt;font-weight:400;margin:8mm 0}.cover p{margin:5mm 0}.q,.answer{break-before:page}.qhead{display:flex;justify-content:space-between;border-bottom:1px solid #666;padding-bottom:3mm;margin-bottom:5mm;font:9pt Arial}.qhead b{font-size:12pt}.stem{margin-bottom:4mm}.part{display:flex;gap:3mm;align-items:baseline;margin:5mm 0;break-inside:avoid}.part>b{flex:0 0 7mm;font-weight:400}.part>div{flex:1}.part>span{margin-left:3mm}.group{margin-top:5mm}.group>.part,.group>.apart{margin-left:7mm}.group>p{margin-bottom:3mm}.total{text-align:right;font-size:10pt;margin-top:5mm}.rewrite-figure{margin:5mm auto;text-align:center;break-inside:avoid}.rewrite-figure svg{display:block;width:100%;max-width:150mm;max-height:62mm;height:auto;margin:auto}.rewrite-figure figcaption{font-size:9pt;color:#555}.stem table{border-collapse:collapse;width:100%;text-align:center;margin:4mm 0}.stem td,.stem th{border:1px solid #777;padding:2mm}.answer{font:10pt/1.8 "Noto Serif CJK SC",Georgia,serif}.answer h3{font-size:11pt;margin:4mm 0 2mm}.apart{margin:4mm 0;break-inside:avoid}.final{font-size:12pt;margin-bottom:2mm}.apart table{border-collapse:collapse;width:100%;font-size:9pt;margin-top:2mm}.apart td{border-top:1px solid #ddd;padding:1mm 2mm;vertical-align:top}.apart td:first-child{width:12mm}.provenance{font-size:9pt;color:#444;border-bottom:1px solid #bbb;margin:0 0 5mm;padding-bottom:3mm}.katex{font-size:1em}.katex-display{overflow:visible}.stem,.part{overflow-wrap:anywhere}'''
books=[]
for st,cs in D['chapters'].items():
 for ch in cs:
  key=f'{st}-C{ch["id"]:02d}';qs=[q for q in D['questions'] if q['stage']==st and q['chapters'][0]==ch['id']];assert len(qs)==30
  body=f'<section class="cover"><p>Pure Mathematics {st[-1]} · Original adaptations · 2026</p><h1>Chapter {ch["id"]}<br>{ch["title"]}</h1><p>{ch["zh"]} · 30 questions with Chinese solutions</p><p>Answer all parts. Show sufficient working.<br>Give exact answers unless a degree of accuracy is requested.<br>Diagrams are not necessarily drawn to scale.</p><p>考法参照2024年前历年真题，题目与配图实质改编。<br>本册不是Pearson原卷；建议评分点非官方评分标准。<br>第7版 · 内部检查稿，未完成外部教师逐题审阅。</p></section>'
  for q in qs:
   body+=f'<section class="q"><header class="qhead"><b>{q["originalNumber"]}.</b><span>{q["id"]} · {st} Chapter {ch["id"]}</span></header><div class="stem">{fmt(q["stem"])}</div>'+''.join(part(a,i) for i,a in enumerate(q['parts']))+f'<p class="total">Total for Question {q["originalNumber"]}: {q["marks"]} marks</p></section>'
  body+='<section class="cover"><h1>Answers and Suggested<br>Mark Schemes</h1><p>中文答案、解析与原创建议评分点</p></section>'
  for q in qs:
   refs='；'.join(f'{r["questionId"]}（{r["year"]}）：{r.get("note","")}' for r in q['sourceReferences'])
   body+=f'<section class="answer"><header class="qhead"><b>Answer {q["originalNumber"]}</b><span>{q["id"]}</span></header><p class="provenance">原创改编（2026） · 主要考点：{html.escape("、".join(q["topics"]))}<br>考法参照：{html.escape(refs)}<br>{html.escape(q["adaptationNote"])}</p>'+''.join(part(a,i,True) for i,a in enumerate(q['parts']))+'</section>'
  page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>'+key+'</title><link rel="stylesheet" href="../assets/katex/katex.min.css"><script src="../assets/katex/katex.min.js"></script><script src="../assets/katex/contrib/auto-render.min.js"></script><style>'+CSS+'</style><body>'+body+'<script type="module">import {improveMath,renderMath} from "../math-format.js";for(const e of document.querySelectorAll(".stem,.part>div,.group>p,.apart"))e.innerHTML=improveMath(e.innerHTML);renderMath(document.body);document.documentElement.dataset.ready="yes";</script></body></html>'
  (TMP/(key+'.html')).write_text(page);books.append({'stage':st,'chapter':ch['id'],'key':key,'zh':ch['zh']})
async def run():
 async with async_playwright() as p:
  browser=await p.chromium.launch(**({'executable_path':'/usr/bin/chromium'} if Path('/usr/bin/chromium').exists() else {}),headless=True,args=['--no-sandbox']);sem=asyncio.Semaphore(3)
  async def one(b):
   async with sem:
    page=await browser.new_page();await page.goto('http://localhost:4173/print-v7/'+b['key']+'.html');await page.wait_for_selector('html[data-ready=yes]');await page.evaluate('document.fonts.ready');assert await page.locator('.q').count()==30;assert await page.locator('.answer').count()==30;assert await page.locator('.katex-error').count()==0
    path=OUT/'分章题册'/(b['key']+'-'+b['zh']+'.pdf');await page.pdf(path=str(path),format='A4',print_background=True,prefer_css_page_size=True);await page.close();doc=fitz.open(path);text='\n'.join(p.get_text() for p in doc);assert len(re.findall(r'P[123]-C\d{2}-R\d{2}',text))==60,(b['key'],'ID count');b['pages']=len(doc);doc.close();shutil.copy2(path,P/'assets/rewrite-books'/(b['key']+'.pdf'));print(b['key'],b['pages'],'pages',flush=True)
  await asyncio.gather(*(one(b) for b in books));await browser.close()
asyncio.run(run())
for st in D['chapters']:
 doc=fitz.open();toc=[]
 for b in books:
  if b['stage']!=st:continue
  toc.append([1,f'Chapter {b["chapter"]}',len(doc)+1]);src=fitz.open(OUT/'分章题册'/(b['key']+'-'+b['zh']+'.pdf'));doc.insert_pdf(src);src.close()
 doc.set_toc(toc);path=OUT/(st+'-全部章节题目与解答.pdf');doc.save(path,garbage=4,deflate=True);doc.close();shutil.copy2(path,P/'assets/rewrite-books'/(st+'.pdf'))
(R/'research/pdf-v7-checks.json').write_text(json.dumps(books,ensure_ascii=False,indent=2));shutil.rmtree(TMP);print('25 chapter PDFs and3 stage PDFs complete')
