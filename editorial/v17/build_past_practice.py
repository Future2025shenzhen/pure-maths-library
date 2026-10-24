"""Build complete question-by-question practice for every archived paper through June 2025.

The official question paper and mark-scheme images remain the primary record.  This
script does not author replacement solutions: it cuts the relevant pages, annotates
official M/A/B mark-code locations, and adds only a Chinese mark-code legend.
"""
from pathlib import Path
import json, re
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'dist/data'
QP_ASSETS = ROOT / 'dist/assets/past-pages-v17'
MS_ASSETS = ROOT / 'dist/assets/past-marks-v17'
QP_ASSETS.mkdir(parents=True, exist_ok=True)
MS_ASSETS.mkdir(parents=True, exist_ok=True)

# Printed page on which each question begins. These were read from the papers, not
# inferred from a fixed two-page pattern. June 2020 was cancelled and is absent.
STARTS = {
 'p1-jan-2019':[2,4,6,8,10,12,14,16,18,20,22,26],
 'p1-jan-2024':[2,4,6,8,10,14,16,18,22,26],
 'p1-jan-2025':[2,4,6,10,14,18,22,26,30],
 'p1-jun-2019':[2,4,6,10,12,14,16,20,24,26],
 'p1-jun-2024':[2,4,6,8,10,14,18,20,22,26,30],
 'p1-jun-2024-r':[2,4,6,8,10,12,16,20,24,26],
 'p1-jun-2025':[2,4,6,8,10,14,18,22,26,30],
 'p1-jun-2025-a':[2,4,6,8,12,16,18,22,26,30],
 'p1-oct-2019':[2,4,6,10,12,14,16,18,20,22,26],
 'p1-oct-2024':[2,4,6,10,14,18,22,24,26],
 'p2-jan-2024':[2,4,6,8,12,16,20,24,26,30],
 'p2-jan-2025':[2,4,6,10,12,16,20,24,26,30],
 'p2-jun-2019':[2,4,6,8,10,12,16,20,24,28],
 'p2-jun-2024':[2,4,6,8,12,14,18,22,26,30],
 'p2-jun-2024-r':[2,4,6,8,10,12,16,18,22,26],
 'p2-jun-2025':[2,4,6,8,12,14,18,22,26,30],
 'p2-jun-2025-a':[2,4,6,10,14,16,20,24,28,30],
 'p2-oct-2019':[2,4,6,8,12,16,20,22,26,30],
 'p2-oct-2024':[2,4,6,10,12,14,16,20,24,26,30],
 'p3-jan-2024':[2,4,6,8,12,14,18,22,26],
 'p3-jan-2025':[2,4,6,8,12,16,20,22,26,30],
 'p3-jun-2024':[2,4,8,10,14,18,22,26,30],
 'p3-jun-2025':[2,6,8,10,12,14,18,22,26,30],
 'p3-jun-2025-a':[2,4,6,10,14,18,22,26,30],
 'p3-oct-2024':[2,4,6,10,12,16,20,24,28],
}

CHAPTERS = {
 'P1': {1:'代数式',2:'二次函数',3:'方程与不等式',4:'图像与变换',5:'直线',6:'三角比',7:'弧度制',8:'微分',9:'积分'},
 'P2': {1:'代数方法',2:'圆的坐标几何',3:'指数与对数',4:'二项式展开',5:'数列与级数',6:'三角恒等式与方程',7:'微分应用',8:'定积分'},
 'P3': {1:'代数方法',2:'函数与图像',3:'三角函数',4:'三角加法公式',5:'指数与对数',6:'微分',7:'积分',8:'数值方法'},
}

RULES = {
 'P1': [(9,r'\bintegr|\u222b|area.*(?:curve|graph)|trapez'),(8,r'differentiat|gradient|tangent|normal|stationary|dy\s*/\s*dx'),(7,r'radian|sector|arc length'),(6,r'\bsin\b|\bcos\b|\btan\b|sine rule|cosine rule'),(5,r'straight line|gradient|parallel|perpendicular|equation of.*line'),(4,r'transform|translation|stretch|sketch.*curve|graph'),(2,r'quadratic|discriminant|completing the square'),(3,r'inequal|simultaneous|solve.*equation'),(1,r'binomial|surd|indices|algebra')],
 'P2': [(8,r'\bintegr|\u222b|area.*(?:curve|graph)|trapez'),(7,r'differentiat|gradient|tangent|normal|stationary|rate of change'),(6,r'trigonom|identity|\bsin\b|\bcos\b|\btan\b'),(5,r'sequence|series|arithmetic|geometric|sigma|sum to'),(4,r'binomial|ascending powers'),(3,r'logarithm|\blog\b|\bln\b|exponential|\be\^'),(2,r'circle|centre|radius|diameter'),(1,r'factor theorem|remainder theorem|partial fraction|algebraic division|proof')],
 'P3': [(8,r'iteration|newton|change of sign|numerical'),(7,r'\bintegr|\u222b|area.*(?:curve|graph)|differential equation'),(6,r'differentiat|gradient|tangent|normal|stationary|rate of change'),(5,r'logarithm|\blog\b|\bln\b|exponential|\be\^'),(4,r'addition formula|double angle|R\s*(?:sin|cos)|asin|acos'),(3,r'trigonom|\bsin\b|\bcos\b|\btan\b'),(2,r'function|domain|range|inverse|composite|transform|sketch'),(1,r'partial fraction|modulus|proof|algebra')],
}
MS_POSITION_OVERRIDES = {('p1-oct-2019-ms.pdf',11):(17,45.0)}

def meaningful(page):
    words=[w[4] for w in page.get_text('words') if page.rect.width*.07<w[0]<page.rect.width*.88 and w[1]<page.rect.height*.9]
    text=' '.join(words)
    text=re.sub(r'DO NOT WRITE IN THIS AREA|Leave\s+blank|BLANK PAGE|Question\s+\d+\s+continued|\*P\w+\*',' ',text,flags=re.I)
    return len(re.sub(r'[^A-Za-z0-9]+','',text))>55 and 'BLANK PAGE' not in text.upper()

def render_page(doc, page_no, target, annotate=False):
    if target.exists(): return
    page=doc[page_no-1]; scale=1.55
    pix=page.get_pixmap(matrix=fitz.Matrix(scale,scale),alpha=False)
    pix.save(target.with_suffix('.png'))
    image=Image.open(target.with_suffix('.png')).convert('RGB')
    if annotate:
        draw=ImageDraw.Draw(image)
        for w in page.get_text('words'):
            token=w[4].strip().replace(' ','')
            if re.match(r'^(?:d?M\d|A\d|B\d)',token):
                colour='#d97706' if 'M' in token else '#16835b'
                box=tuple(int(v*scale) for v in w[:4])
                draw.rectangle((box[0]-5,box[1]-4,box[2]+5,box[3]+4),outline=colour,width=4)
    image.save(target,'WEBP',quality=82,method=6)
    target.with_suffix('.png').unlink()

def question_y(page, number):
    pats={str(number),str(number)+'.',str(number)+':'}
    words=[w for w in page.get_text('words') if w[4].strip() in pats and w[0]<150]
    return max(0.035,(min((w[1] for w in words),default=38)-15)/page.rect.height)

def question_bottom(page,top):
    keep=[]
    for w in page.get_text('words'):
        if not (page.rect.width*.07<w[0]<page.rect.width*.9):continue
        if w[1]<page.rect.height*top or w[1]>page.rect.height*.87:continue
        token=w[4].strip()
        if not re.search(r'[A-Za-z0-9\u0370-\u03ff\u2200-\u22ff]',token):continue
        if re.match(r'^\*?P\d+[A-Z]?\d+\*?$',token,re.I):continue
        keep.append(w[3])
    for drawing in page.get_drawings():
        rect=drawing['rect']
        if rect.y0<page.rect.height*top or rect.y0>page.rect.height*.87:continue
        if rect.height<3 and rect.width>page.rect.width*.55:continue
        if rect.x1<page.rect.width*.05 or rect.x0>page.rect.width*.92:continue
        keep.append(rect.y1)
    for block in page.get_text('dict').get('blocks',[]):
        if block.get('type')==1:
            x0,y0,x1,y1=block['bbox']
            if y0>=page.rect.height*top and y0<page.rect.height*.87:keep.append(y1)
    return min(.94,max(top+.08,(max(keep,default=page.rect.height*(top+.1))+20)/page.rect.height))

def quick_check(q,method_count,accuracy_count):
    if q.get('solutionSections'):
        methods=[s.get('approach','').strip() for s in q['solutionSections'] if s.get('approach')]
        finals=[s['steps'][-1].strip() for s in q['solutionSections'] if s.get('steps')]
        process='；'.join(methods[:3])
        answer='；'.join(finals[:4])
    else:
        topic='、'.join(q['topics'])
        process=f'围绕“{topic}”写出橙框所示的关键方法。共标出约{method_count}个方法得分位置；只写最终数值通常不能取得这些M分。'
        answer=f'按(a)、(b)、(c)的顺序核对粉红框。粉红框覆盖官方A/B准确分所在答案行，共约{accuracy_count}处。'
    return {'process':process or '按橙框顺序写出关键方法和必要代入。','answer':answer or '粉红框内是官方正确答案或必须达到的准确结论。'}

def scheme_positions(doc, count):
    """Find the left-column question labels in reading order.

    Mark schemes use several fonts and sometimes put two short questions on one
    page. We therefore use the printed left column, then fill a rare missing label
    from the ordered Question/Number/Scheme/Marks page headers.
    """
    candidates={n:[] for n in range(1,count+1)}
    for pi,page in enumerate(doc,1):
        if pi<4: continue
        top_words=[w for w in page.get_text('words') if w[1]<190]
        top_tokens={w[4] for w in top_words}
        # General marking guidance also contains numbered lists. Only the
        # question-specific table has the two-column "Question Number" header.
        if not (('Scheme' in top_tokens and ({'Question','Number'} & top_tokens)) or {'Question','Number'}.issubset(top_tokens)):continue
        for w in page.get_text('words'):
            if w[0]>100: continue
            token=w[4].strip().replace(' ','')
            for n in range(1,count+1):
                if re.match(rf'^{n}(?!\d)[.():a-ziv]*$',token,re.I):
                    candidates[n].append((pi,w[1]))
    for values in candidates.values():values.sort()
    selected=[]; prev=(3,0)
    for n in range(1,count+1):
        override=MS_POSITION_OVERRIDES.get((Path(doc.name).name,n))
        if override:
            selected.append(override);prev=override;continue
        choices=[x for x in candidates[n] if x[0]>prev[0] or x[0]==prev[0] and x[1]>prev[1]+25]
        pick=choices[0] if choices else None
        if not pick:
            # A label occasionally becomes a drawing glyph in extracted text.
            headers=[]
            for pi,page in enumerate(doc,1):
                if pi<prev[0]: continue
                tops={w[4] for w in page.get_text('words') if w[1]<190}
                if ('Scheme' in tops and ({'Question','Number'} & tops)) or {'Question','Number'}.issubset(tops):headers.append((pi,70.0))
            used_pages={x[0] for x in selected}
            pick=next((x for x in headers if x[0] not in used_pages and x>prev),None)
        if not pick: raise ValueError(f'{doc.name}: cannot locate official mark scheme question {n}')
        selected.append(pick); prev=pick
    return selected

def classify(stage,text):
    """Assign the paper's dominant syllabus chapter using explicit exam wording.

    A single primary chapter gives predictable filtering. The order resolves
    vocabulary overlaps such as a gradient used inside a circle question.
    """
    t=' '.join(text.lower().split())
    if stage=='P1':
        rules=[
          (7,r'\bsector\b|\bradian|arc length|major arc|minor arc'),
          (9,r'∫|\uf0f2|integrat|area (?:of|between|enclosed|under).*curve'),
          (8,r'differentiat|f[′ʹ]|stationary|\bnormal\b|tangent to|rate of change|d\s*y\s*d\s*x'),
          (6,r'trigonom|\bsin\b|\bcos\b|\btan\b|sine rule|cosine rule'),
          (5,r'straight line|equation (?:for|of) (?:the )?line|parallel|perpendicular|\bgradient\b'),
          (4,r'transform|translation|stretch|sketch.*(?:curve|graph)|graph with equation'),
          (2,r'quadratic|discriminant|complet(?:e|ing) the square|turning point'),
          (3,r'inequal|simultaneous|solve.*equation'),
        ]
    elif stage=='P2':
        rules=[
          (2,r'\bcircle\b|\bcentre\b.*\bradius\b|diameter'),
          (4,r'binomial|ascending powers'),
          (3,r'logarithm|\blog\b|\bln\b|exponential'),
          (5,r'\bsequence\b|\bseries\b|arithmetic|geometric|common ratio|common difference|\bterm\b.*\bsum\b'),
          (6,r'trigonom|identity|\bsin\b|\bcos\b|\btan\b'),
          (8,r'∫|\uf0f2|integrat|trapez|area (?:of|between|enclosed|under).*curve'),
          (7,r'differentiat|stationary|maximum|minimum|\bnormal\b|tangent to|rate of change'),
          (1,r'factor theorem|remainder|partial fraction|proof|prove|exhaustion|counter example'),
        ]
    else:
        rules=[
          (8,r'iteration|newton|change of sign|numerical method|root.*interval'),
          (4,r'addition formula|double angle|form\s+r\s+(?:sin|cos)|\b(?:sin|cos)\s*[234](?:x|θ|y)'),
          (5,r'logarithm|\blog\b|\bln\b|exponential|e\^'),
          (7,r'∫|\uf0f2|integrat|differential equation|area (?:of|between|enclosed|under).*curve'),
          (6,r'differentiat|stationary|\bnormal\b|tangent to|rate of change'),
          (1,r'partial fraction|algebraic division|proof|prove'),
          (2,r'function|domain|range|inverse|composite|transform|translation|stretch|modulus'),
          (3,r'trigonom|\bsin\b|\bcos\b|\btan\b|\bsec\b'),
        ]
    return [next((chapter for chapter,pat in rules if re.search(pat,t,re.I)),1)]

def main():
    bank=json.loads((DATA/'past-bank.json').read_text())
    archive=json.loads((DATA/'paper-archive.json').read_text())
    # Idempotent rebuild: retain the reviewed 2020--2023 records and recreate the
    # generated official-scheme records from their PDFs.
    bank['questions']=[q for q in bank['questions'] if not (q.get('v17Added') or q['year'] in (2019,2024,2025))]
    old_papers={q['paper'] for q in bank['questions']}
    new_questions=[]; layout=json.loads((DATA/'past-layout.json').read_text())
    layout_questions=layout['questions']
    audit=[]
    for paper in archive['papers']:
        pid=paper['id']
        if pid in old_papers: continue
        starts=STARTS[pid]
        qp=fitz.open(ROOT/'dist'/paper['pdf']); ms=fitz.open(ROOT/'dist'/paper['markScheme'])
        ms_positions=scheme_positions(ms,len(starts))
        paper_marks=0
        for index,start in enumerate(starts):
            number=index+1; end=(starts[index+1]-1 if index+1<len(starts) else len(qp))
            source_pages=[p for p in range(start,end+1) if p==start or meaningful(qp[p-1])]
            text='\n'.join(qp[p-1].get_text() for p in source_pages)
            # Printed mark allocations sit in the right margin. Restricting to that
            # column avoids counting coordinates such as (2, 3) in the question.
            mark_values=[]
            for p in source_pages:
                page=qp[p-1]
                for word in page.get_text('words'):
                    match=re.fullmatch(r'\(\s*(\d{1,2})\s*\)',word[4])
                    if match and word[0] > page.rect.width*.72:
                        mark_values.append(int(match.group(1)))
            marks=sum(mark_values)
            if not marks: raise ValueError(f'{pid} Q{number}: marks not found')
            paper_marks+=marks
            qid=f"{paper['stage']}-{paper['year']}-{paper['month']:02d}"+(f"{paper['variant']}" if paper['variant'] else '')+f"-Q{number:02d}"
            page_refs=[]
            for p in source_pages:
                page=qp[p-1]
                top=question_y(page,number) if p==start else .035;bottom=question_bottom(page,top)
                page_refs.append({'page':p,'pdf':paper['pdf'],'renderFromPdf':True,'width':round(page.rect.width*1.55),'height':round(page.rect.height*1.55),'crop':[0.055,top,0.89,bottom-top]})
            ms_start_page,ms_start_y=ms_positions[index]
            if index+1<len(ms_positions): ms_end_page,ms_end_y=ms_positions[index+1]
            else: ms_end_page,ms_end_y=len(ms)+1,0
            ms_refs=[]
            last_ms_page=ms_end_page if ms_end_page==ms_start_page else ms_end_page-1
            last_ms_page=min(last_ms_page,len(ms))
            for p in range(ms_start_page,last_ms_page+1):
                page=ms[p-1]
                top=max(0.025,(ms_start_y-18)/page.rect.height) if p==ms_start_page else 0.025
                bottom=((ms_end_y-8)/page.rect.height) if p==ms_end_page and ms_end_page==ms_start_page else 0.96
                note_y=min((w[1] for w in page.get_text('words') if w[4].strip().lower().startswith('notes:') and w[1]>page.rect.height*top),default=page.rect.height)
                bottom=min(bottom,(note_y-8)/page.rect.height)
                if bottom<=top+.04: continue
                highlights=[]
                for word in page.get_text('words'):
                    token=word[4].strip().replace(' ','')
                    for code in re.findall(r'(?:d?M\d+|A\d+|B\d+)',token):
                        if 'M' in code:box=[word[0]/page.rect.width,word[1]/page.rect.height,(word[2]-word[0])/page.rect.width,(word[3]-word[1])/page.rect.height];kind='method'
                        else:box=[.10,max(top,word[1]/page.rect.height-.012),.78,max(.035,(word[3]-word[1])/page.rect.height+.024)];kind='accuracy'
                        highlights.append({'kind':kind,'box':[round(v,6) for v in box]})
                ms_refs.append({'page':p,'pdf':paper['markScheme'],'renderFromPdf':True,'width':round(page.rect.width*1.55),'height':round(page.rect.height*1.55),'crop':[0.035,top,0.93,bottom-top],'highlights':highlights})
            scheme_text='\n'.join(ms[p['page']-1].get_text() for p in ms_refs)
            chapters=classify(paper['stage'],text+'\n'+scheme_text)
            title='、'.join(CHAPTERS[paper['stage']][c] for c in chapters)
            q={'id':qid,'paper':pid,'stage':paper['stage'],'year':paper['year'],'month':paper['month'],'variant':paper['variant'],'number':number,'sourcePages':source_pages,'pages':page_refs,'marks':marks,'searchText':text,'chapters':chapters,'topics':[title],'titleZh':title,'solutionZh':'本题答案直接采用官方评分标准；粉红框标出正确答案，橙色框标出方法得分点。','solutionSections':[],'officialMarkScheme':True,'officialSchemeRevision':17,'v17Added':True,'markSchemePages':ms_refs,'verification':'题面裁自官方原卷；答案裁自本卷官方评分标准，未另写自拟解法。'}
            methods=sum(h['kind']=='method' for v in ms_refs for h in v['highlights']);accuracies=sum(h['kind']=='accuracy' for v in ms_refs for h in v['highlights']);q['quickCheckZh']=quick_check(q,methods,accuracies)
            new_questions.append(q);layout_questions[qid]=page_refs
        if paper_marks!=75: raise ValueError(f'{pid}: question marks total {paper_marks}, expected 75')
        audit.append({'paper':pid,'questions':len(starts),'marks':paper_marks,'officialMarkSchemeMapped':True})
    # Replace the displayed authored solutions on the existing 323 records with
    # crops from their official mark schemes too. Their legacy text stays in the
    # data only for rollback/history and is no longer rendered by the site.
    paper_by_id={p['id']:p for p in archive['papers']}
    retained_by_paper={}
    for q in bank['questions']:retained_by_paper.setdefault(q['paper'],[]).append(q)
    for pid,questions in retained_by_paper.items():
        questions.sort(key=lambda q:q['number']);paper=paper_by_id[pid]
        ms=fitz.open(ROOT/'dist'/paper['markScheme']);positions=scheme_positions(ms,len(questions))
        for index,q in enumerate(questions):
            start_page,start_y=positions[index]
            if index+1<len(positions):end_page,end_y=positions[index+1]
            else:end_page,end_y=len(ms)+1,0
            last=end_page if end_page==start_page else end_page-1;last=min(last,len(ms));refs=[]
            for page_number in range(start_page,last+1):
                page=ms[page_number-1];top=max(.025,(start_y-18)/page.rect.height) if page_number==start_page else .025
                bottom=(end_y-8)/page.rect.height if page_number==end_page==start_page else .96
                note_y=min((w[1] for w in page.get_text('words') if w[4].strip().lower().startswith('notes:') and w[1]>page.rect.height*top),default=page.rect.height)
                bottom=min(bottom,(note_y-8)/page.rect.height)
                if bottom<=top+.04:continue
                highlights=[]
                for word in page.get_text('words'):
                    token=word[4].strip().replace(' ','')
                    for code in re.findall(r'(?:d?M\d+|A\d+|B\d+)',token):
                        if 'M' in code:box=[word[0]/page.rect.width,word[1]/page.rect.height,(word[2]-word[0])/page.rect.width,(word[3]-word[1])/page.rect.height];kind='method'
                        else:box=[.10,max(top,word[1]/page.rect.height-.012),.78,max(.035,(word[3]-word[1])/page.rect.height+.024)];kind='accuracy'
                        highlights.append({'kind':kind,'box':[round(v,6) for v in box]})
                refs.append({'page':page_number,'pdf':paper['markScheme'],'renderFromPdf':True,'width':round(page.rect.width*1.55),'height':round(page.rect.height*1.55),'crop':[.035,top,.93,bottom-top],'highlights':highlights})
            q.update(officialMarkScheme=True,officialSchemeRevision=17,markSchemePages=refs,verification='题面裁自官方原卷；答案显示本卷官方评分标准，本站自拟解析不再展示。')
            methods=sum(h['kind']=='method' for v in refs for h in v['highlights']);accuracies=sum(h['kind']=='accuracy' for v in refs for h in v['highlights']);q['quickCheckZh']=quick_check(q,methods,accuracies)
    bank['papers']=[{k:p[k] for k in ('id','stage','year','month','title','pdf','markScheme','sha256') if k in p}|{'questions':len(STARTS[p['id']]),'providedByUser':False,'variant':p['variant']} if p['id'] in STARTS else p for p in archive['papers']]
    bank['questions'].extend(new_questions)
    bank['questions'].sort(key=lambda q:(q['stage'],q['year'],q['month'],q.get('variant',''),q['number']))
    bank.update(version=17,cutoffYearExclusive=2026,source='官方试卷与官方评分标准逐题裁切；答案以官方评分表为准')
    (DATA/'past-bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
    for paper in archive['papers']: paper['questionPracticeAvailable']=True
    archive['version']=17
    archive['note']='截至2025年6月的全部整卷均已提供逐题练习及对应官方评分标准。A/R卷按来源标识分别保存。'
    (DATA/'paper-archive.json').write_text(json.dumps(archive,ensure_ascii=False,indent=2)+'\n')
    layout['version']=17;(DATA/'past-layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n')
    classification=json.loads((DATA/'classification.json').read_text())
    for q in new_questions:
        classification['questions'][q['id']]={'stage':q['stage'],'chapters':q['chapters']}
    (DATA/'classification.json').write_text(json.dumps(classification,ensure_ascii=False,indent=2)+'\n')
    out=ROOT/'editorial/v17';out.mkdir(exist_ok=True)
    (out/'past-practice-audit.json').write_text(json.dumps({'addedQuestions':len(new_questions),'totalQuestions':len(bank['questions']),'papers':audit},ensure_ascii=False,indent=2)+'\n')
    values=',\n'.join(f"('{q['id']}','past','{q['stage']}')" for q in new_questions)
    (ROOT/'backend/007-complete-past-catalog.sql').write_text(
        '-- Register the 2019, 2024 and 2025-through-June question-by-question records.\n'
        'insert into public.pp_question_catalog(id,kind,stage) values\n'+values+'\n'
        'on conflict (id) do nothing;\n')
    print(json.dumps({'added':len(new_questions),'total':len(bank['questions']),'papers':len(audit)},ensure_ascii=False))

if __name__=='__main__': main()
