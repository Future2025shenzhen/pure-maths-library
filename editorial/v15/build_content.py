import json, math
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
bank=json.loads((ROOT/'dist/data/bank.json').read_text())
old={q['id']:q for q in bank['questions']}

def scheme(*rows): return [{'code':c,'marks':m,'text':t} for c,m,t in rows]
def part(text,answer,steps,rows):
    rr=scheme(*rows)
    return {'text':text,'answer':answer,'explanation':'\n'.join(steps),'approach':steps[0], 'solutionSteps':steps,'scheme':rr,'marks':sum(x['marks'] for x in rr)}
def clean_tex(value):
    if isinstance(value, str): return value.replace('\\\\', '\\')
    if isinstance(value, list): return [clean_tex(v) for v in value]
    if isinstance(value, dict): return {k: clean_tex(v) for k, v in value.items()}
    return value
def condense_to_two(question):
    """Remove legacy three-part scaffolding and cap retained items at 7 marks."""
    leaves=[]
    def collect(parts):
        for p in parts:
            collect(p['subparts']) if p.get('subparts') else leaves.append(json.loads(json.dumps(p)))
    collect(question['parts'])
    assert len(leaves)>=2
    if len(leaves)>2:
        rest=leaves[1:]
        leaves=[leaves[0], {
            'text':'Hence or otherwise, determine all of the following in one coherent solution: ' + '; '.join(p['text'].rstrip('.') for p in rest) + '.',
            'answer':'; '.join(p.get('answer','') for p in rest),
            'explanation':'\n'.join(p.get('explanation','') for p in rest),
            'approach':rest[0].get('approach') or rest[0].get('solutionSteps',[''])[0],
            'solutionSteps':[step for p in rest for step in p.get('solutionSteps',[])],
            'scheme':[row for p in rest for row in p.get('scheme',[])],
            'marks':sum(p['marks'] for p in rest),
        }]
    target=min(7,question['marks'])
    targets=[min(3,leaves[0]['marks']),0]
    targets[1]=target-targets[0]
    if targets[1]<2: targets=[target-2,2]
    for p,wanted in zip(leaves,targets):
        rows=p.get('scheme',[])
        picked=(rows[:wanted-1]+rows[-1:]) if rows else []
        while len(picked)<wanted:
            picked.append({'code':'M1','marks':1,'text':p.get('solutionSteps',['Apply the stated condition.'])[-1]})
        p['scheme']=[]
        for i,row in enumerate(picked[:wanted]):
            p['scheme'].append({'code':'A1' if i==wanted-1 else 'M1','marks':1,'text':row.get('text') or p['solutionSteps'][min(i,len(p['solutionSteps'])-1)]})
        p['marks']=wanted
    question['parts']=leaves
    question['marks']=target
    return question
def qnew(qid,chapter,type_,stem,parts,topics,source,summary,dims,essence,errors,design,figure=''):
    return clean_tex({'id':qid,'stage':'P1','chapters':[chapter],'type':type_,'stem':stem+figure,'parts':parts,'marks':sum(p['marks'] for p in parts),'topics':topics,'origin':'original-reviewed-2026','review':'internal-review-only','editorialRevision':15,'originalNumber':int(qid[-2:]),'sourceReferences':[{'questionId':source,'year':int(source[3:7]),'note':summary}], 'sourceSummary':summary,'adaptationDimensions':dims,'examEssence':essence,'difficultyPosition':f'略难于 {source}：{design}','errorNotes':errors,'designNote':design,'adaptationNote':'改编维度：'+'、'.join(dims)+'。思维增量：'+design,'answerFigure':'','family':qid,'solutionRevision':15,'contentUpdatedAt':'2026-10-24'})

def fig_trig(title='Trigonometric curve features'):
 return f'''<figure class="rewrite-figure"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 280" role="img" aria-label="{title}"><title>{title}</title><g fill="none" stroke="#222" stroke-width="1.5"><path d="M45 140H510M75 250V30"/><path d="M75 210C120 210 120 70 165 70S210 210 255 210S300 70 345 70S390 210 435 210S480 70 510 70"/><text x="515" y="145" fill="#222" stroke="none" font-family="Georgia" font-size="15">x</text><text x="65" y="25" fill="#222" stroke="none" font-family="Georgia" font-size="15">y</text></g></svg><figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'''
def fig_cubic(title='Cubic curve'):
 return f'''<figure class="rewrite-figure"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 280" role="img" aria-label="{title}"><title>{title}</title><g fill="none" stroke="#222" stroke-width="1.5"><path d="M40 145H465M245 250V25"/><path d="M70 225C120 210 140 80 205 145C245 185 280 100 325 105C380 110 390 45 445 35"/><text x="470" y="150" fill="#222" stroke="none" font-family="Georgia" font-size="15">x</text><text x="235" y="20" fill="#222" stroke="none" font-family="Georgia" font-size="15">y</text></g></svg><figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'''

# Old questions retained after full chapter audit. Their mathematical content survived review;
# metadata and sources are refreshed to enforce one-source/three-derivative accounting.
keep4=['P1-C04-R01','P1-C04-R03','P1-C04-R04','P1-C04-R06','P1-C04-R09','P1-C04-R10','P1-C04-R11','P1-C04-R15','P1-C04-R17','P1-C04-R18','P1-C04-R20','P1-C04-R21','P1-C04-R22','P1-C04-R24','P1-C04-R25','P1-C04-R28','P1-C04-R30']
src4={
'P1-C04-R01':'P1-2025-06A-Q01','P1-C04-R03':'P1-2023-01-Q07','P1-C04-R04':'P1-2022-06-Q04','P1-C04-R06':'P1-2021-10-Q09','P1-C04-R09':'P1-2022-01-Q10','P1-C04-R10':'P1-2024-10-Q09','P1-C04-R11':'P1-2023-01-Q07','P1-C04-R15':'P1-2022-01-Q02','P1-C04-R17':'P1-2021-10-Q09','P1-C04-R18':'P1-2022-10-Q07','P1-C04-R20':'P1-2020-01-Q10','P1-C04-R21':'P1-2023-01-Q07','P1-C04-R22':'P1-2022-01-Q10','P1-C04-R24':'P1-2021-10-Q09','P1-C04-R25':'P1-2025-06A-Q01','P1-C04-R28':'P1-2024-01-Q07','P1-C04-R30':'P1-2022-01-Q10'}
keep9=['P1-C09-R01','P1-C09-R02','P1-C09-R03','P1-C09-R05','P1-C09-R06','P1-C09-R08','P1-C09-R09','P1-C09-R10','P1-C09-R13','P1-C09-R16','P1-C09-R17','P1-C09-R18','P1-C09-R19','P1-C09-R22','P1-C09-R23','P1-C09-R25','P1-C09-R30']
src9={
'P1-C09-R01':'P1-2021-06-Q06','P1-C09-R02':'P1-2020-10-Q09','P1-C09-R03':'P1-2023-01-Q11','P1-C09-R05':'P1-2021-06-Q04','P1-C09-R06':'P1-2022-10-Q05','P1-C09-R08':'P1-2023-01-Q11','P1-C09-R09':'P1-2023-01-Q03','P1-C09-R10':'P1-2022-06-Q07','P1-C09-R13':'P1-2020-10-Q09','P1-C09-R16':'P1-2021-10-Q01','P1-C09-R17':'P1-2023-01-Q11','P1-C09-R18':'P1-2021-06-Q04','P1-C09-R19':'P1-2022-06-Q07','P1-C09-R22':'P1-2023-01-Q03','P1-C09-R23':'P1-2023-10-Q07','P1-C09-R25':'P1-2020-10-Q09','P1-C09-R30':'P1-2021-10-Q10'}

Q=[]
for qid in keep4+keep9:
 q=json.loads(json.dumps(old[qid])); q.pop('withdrawn',None);q.pop('withdrawalReason',None)
 source=(src4|src9)[qid]; year=int(source[3:7]); q['sourceReferences']=[{'questionId':source,'year':year,'note':'同族真题的结构、命令词与评分路径'}]
 q.update(editorialRevision=15,solutionRevision=15,contentUpdatedAt='2026-10-24',sourceSummary=f'{source} 的同族考法：{q["type"]}，由给定条件建立关系并完成代数或几何收尾',adaptationDimensions=['条件呈现','题目结构','求解目标'],examEssence='在P1范围内连接核心公式、图像特征与有效范围',difficultyPosition=f'略难于 {source}：减少中间提示并保留完整推理链。',errorNotes=['先识别题目给出的结构条件，再代入公式。','最终答案必须检查定义域、图像特征或几何含义。'],designNote='保留真题核心路径，去掉一层脚手架并加入有效性判断。',adaptationNote='改编维度：条件呈现、题目结构、求解目标。思维增量：减少中间提示并要求检查结论。')
 q['chapters']=[int(qid[4:6])]
 leaves=[]
 for p in q['parts']:
  leaves.extend(p.get('subparts', [p]))
 for p in leaves:
  steps=p.get('solutionSteps') or [p.get('explanation','')]
  for i,row in enumerate(p.get('scheme', [])):
   if '采用解析所述方法' in row.get('text','') or '得到所列结果' in row.get('text',''):
    row['text']=steps[min(i,len(steps)-1)]
 q=condense_to_two(q)
 Q.append(q)

# C04 R31
Q.append(qnew('P1-C04-R31',4,'三角图像参数反求与复合变换',
 'The curve $C$ has equation $y=a+b\\cos(kx)$, where $b<0$, $k>0$ and angles are measured in degrees. Consecutive minimum points are $(0,-5)$ and $(240,-5)$, and the maximum value of $y$ is $3$.',[
 part('Find $a$, $b$ and the least possible positive value of $k$.',r'$a=-1$, $b=-4$, $k=3/2$.',[r'中线为 $a=(3+(-5))/2=-1$。',r'振幅为 $4$，且 $b<0$，所以 $b=-4$。',r'相邻最低点相距 $240^\\circ$，故 $360/k=240$，得 $k=3/2$。'],(('M1',1,'Uses maximum and minimum to find the midline'),('M1',1,'Uses amplitude, sign and period'),('A1',1,'Finds a, b and k'))),
 part('The curve is transformed by $(x,y)\\mapsto(2x,y+1)$ to form $D$. Find an equation of $D$ and the coordinates of its maximum points for $0\\le x\\le480$.',r'$D:y=-4\\cos(3x/4)$; maximum at $(240,4)$.',[r'横坐标扩大为原来的2倍，故新函数中用 $x/2$ 代替原来的 $x$；纵坐标再加1。',r'$y=[-1-4\\cos((3/2)(x/2))]+1=-4\\cos(3x/4)$。',r'最大值要求 $\\cos(3x/4)=-1$；在给定区间只有 $x=240$，此时 $y=4$。'],(('M1',1,'Uses x/2 for the horizontal stretch'),('A1',1,'Obtains the transformed equation'),('M1',1,'Solves the maximum condition in the interval'),('A1',1,'Gives the point')))
 ],['三角图像','参数反求','复合变换'],'P1-2022-01-Q09','由三角图像的极值与周期确定参数',['设问角度','条件呈现','题目结构','跨考点耦合'],'由极值和周期恢复三角函数，再追踪复合图像变换',['横向伸长2倍应使用x/2。','在限制区间内只保留有效最大点。'],'由读图参数题升级为逆向建模和复合映射',fig_trig()))
# C04 R32
Q.append(qnew('P1-C04-R32',4,'倒数图像复合变换与切线参数',
 r'The curve $C$ has equation $y=f(x)$, where $f(x)=\\dfrac{4}{x+1}$ and $x\\ne-1$. The curve $D$ has equation $y=2f(x-3)-1$.',[
 part('Find an equation of $D$ and state the equations of its two asymptotes.',r'$D:y=\\dfrac{8}{x-2}-1$; asymptotes $x=2$ and $y=-1$.',[r'$f(x-3)=\\dfrac4{x-2}$，再把纵坐标放大2倍并下移1，得 $D:y=\\dfrac8{x-2}-1$。',r'分母为0给竖直渐近线 $x=2$；竖直平移给水平渐近线 $y=-1$。'],(('M1',1,'Substitutes x-3 into f'),('A1',1,'Obtains the equation of D'),('B1',1,'States the vertical asymptote'),('B1',1,'States the horizontal asymptote'))),
 part('The line $y=-x+p$, where $p$ is a constant, is tangent to $D$. Find the possible values of $p$ and the coordinates of the corresponding points of contact.',r'$p=1\\pm4\\sqrt2$; points $(2\\pm2\\sqrt2,-1\\pm2\\sqrt2)$ with matching signs.',[r'联立得 $\\dfrac8{x-2}-1=-x+p$，整理为 $x^2-(p+3)x+2p+10=0$。',r'相切要求判别式为0：$(p+3)^2-4(2p+10)=0$，即 $p^2-2p-31=0$。',r'所以 $p=1\\pm4\\sqrt2$，重根 $x=(p+3)/2=2\\pm2\\sqrt2$。',r'代入直线得 $y=-1\\pm2\\sqrt2$，符号与对应的 $p$ 一致。'],(('M1',1,'Forms the intersection equation'),('A1',1,'Obtains the quadratic'),('M1',1,'Uses zero discriminant'),('A1',1,'Finds both p values'),('M1',1,'Finds the repeated x-coordinates'),('A1',1,'Gives both points of contact')))
 ],['倒数图像','复合变换','参数切线'],'P1-2024-01-Q07','倒数图像与含参直线的无交点或相切边界',['参数化与分类讨论','题目结构','求解目标','跨考点耦合'],'从渐近线和复合变换建立方程，再以判别式反求切线参数',['输入平移发生在函数内部，方向要反读。','两个参数值必须和各自切点配对。'],'把固定直线的不相交判断升级为两支参数切线的完整求解'))
# C04 R33
Q.append(qnew('P1-C04-R33',4,'三角图像地标与变换顺序',
 'The curve $C$ has equation $y=a+b\\sin(kx)$, where $b>0$, $k>0$ and angles are measured in degrees. Its maximum value is $5$, its minimum value is $-1$, the distance between consecutive maxima is $180^\\circ$, and it passes through $(0,2)$.',[
 part('Find $a$, $b$ and the least positive value of $k$.',r'$a=2$, $b=3$, $k=2$.',[r'中线为 $(5+(-1))/2=2$，振幅为 $(5-(-1))/2=3$。',r'由 $b>0$ 得 $b=3$。周期是 $180^\\circ$，故 $360/k=180$，得 $k=2$。'],(('M1',1,'Finds midline and amplitude'),('A1',1,'Finds a and b'),('M1',1,'Uses the period relation'),('A1',1,'Finds k'))),
 part('The graph is translated $30^\\circ$ to the right and then stretched horizontally by scale factor 2. Find the equation of the resulting curve.',r'$y=2+3\\sin(x-60^\\circ)$.',[r'先右移 $30^\\circ$：$y=2+3\\sin(2x-60^\\circ)$。',r'再水平伸长2倍，把整个式子中的 $x$ 换成 $x/2$，得 $y=2+3\\sin(x-60^\\circ)$。'],(('M1',1,'Applies the translation'),('A1',1,'Applies the stretch in the stated order'))),
 part('State the equation obtained if the order of these two transformations is reversed.',r'$y=2+3\\sin(x-30^\\circ)$.',[r'先伸长得到 $y=2+3\\sin x$。',r'再右移 $30^\\circ$，所以得到 $y=2+3\\sin(x-30^\\circ)$；次序不同，结果不同。'],(('M1',1,'Reverses the transformation order'),('A1',1,'Gives the correct equation')))
 ],['三角图像','周期','变换顺序'],'P1-2022-06-Q09','三角图像的对称、周期与横向压缩',['条件呈现','题目结构','收尾要求','跨考点耦合'],'利用极值和周期确定图像，并理解变换不交换',['横向变换必须作用于整个输入。','平移与伸缩交换次序会改变相位。'],'加入两种变换次序的对照判断',fig_trig('Sine graph landmarks')))
# C04 R34
Q.append(qnew('P1-C04-R34',4,'参数平移与三次交点个数',r'The curve $C$ has equation $y=(x-1)^2(x+2)$. The curve $D$ is obtained by translating $C$ vertically by $p$ units, where $p$ is a real constant.',[
 part('State the $x$-intercepts of $C$ and describe its behaviour at each intercept.',r'Crosses at $(-2,0)$ and touches at $(1,0)$.',[r'$x=-2$ 是单根，因此穿过横轴。',r'$x=1$ 是二重根，因此与横轴相切。'],(('B1',1,'Finds both roots'),('B1',1,'Identifies the crossing'),('B1',1,'Identifies the touch'))),
 part('Find the set of values of $p$ for which $D$ meets the $x$-axis at exactly one distinct point.',r'$p>0$ or $p<-4$.',[r'交点满足 $(x-1)^2(x+2)+p=0$。令 $u=x-1$，即比较 $F(u)=u^3+3u^2$ 与水平线 $y=-p$。',r'$F\\prime(u)=3u(u+2)$，驻点为 $u=0,-2$，对应函数值 $0,4$。',r'水平线严格低于0或严格高于4时只有一个交点；等于端点时仍有另一个交点。',r'所以 $-p<0$ 或 $-p>4$，即 $p>0$ 或 $p<-4$。'],(('M1',1,'Reframes intersections as a horizontal level'),('M1',1,'Finds both stationary points'),('A1',1,'Finds the stationary levels'),('M1',1,'Classifies the number of intersections'),('A1',1,'Converts to strict p intervals')))
 ],['三次图像','参数分类','平移'],'P1-2020-01-Q10','重根三次图像及水平线交点结构',['参数化与分类讨论','求解目标','题目结构'],'以驻点高度判断竖直平移后的根个数',['边界值对应两个不同交点，不能计入。','必须把水平线高度由-p正确换回p。'],'从单次作图升级为完整参数分类'))
# C04 R35
Q.append(qnew('P1-C04-R35',4,'周期图像复合变换与交点计数',
 'For $0^\\circ\\le x\\le360^\\circ$, the curve $C$ has equation $y=1+2\\sin(3x)$. The curve $D$ is given by $y=1+2\\sin(6x-180^\\circ)$.',[
 part('Describe a sequence of transformations mapping $C$ onto $D$.',r'Horizontal stretch of scale factor $1/2$, then translation $30^\\circ$ to the right.',[r'$D(x)=C(2x-60^\\circ)=C(2(x-30^\\circ))$。',r'因此先沿横轴压缩为 $1/2$，再向右平移 $30^\\circ$。'],(('M1',1,'Expresses D in terms of C'),('A1',1,'Identifies the horizontal scale'),('A1',1,'Identifies the translation'))),
 part('State the period of each curve.',r'$120^\\circ$ and $60^\\circ$.',[r'$C$ 的周期为 $360/3=120^\\circ$。',r'$D$ 的周期为 $360/6=60^\\circ$。'],(('B1',1,'Period of C'),('B1',1,'Period of D'))),
 part('Find the number of intersections of $D$ with $y=2$ in the stated interval.',r'$12$.',[r'方程化为 $\\sin(6x-180^\\circ)=1/2$。',r'当 $x$ 从0到360时，角度跨越 $2160^\\circ$，即6个完整周期。',r'每个周期有两个解，因此共有 $12$ 个交点。'],(('M1',1,'Forms the sine equation'),('M1',1,'Counts full periods and two roots per period'),('A1',1,'Gives 12')))
 ],['三角图像','复合变换','交点计数'],'P1-2023-10-Q10','三角图像周期与竖直或水平变换',['情境与载体','题目结构','跨考点耦合','收尾要求'],'以函数复合表示变换，并在限制区间计数',['相位变化不能直接当作平移距离。','端点不构成重复解。'],'把图像变换与周期内交点计数合并',fig_trig('Transformed periodic graph')))
# C04 R36
Q.append(qnew('P1-C04-R36',4,'极值反求参数与竖直变换',
 'For $0^\\circ\\le x\\le360^\\circ$, $f(x)=a+b\\cos x$ has maximum value $5$ and minimum value $-3$. The curve $g$ is defined by $g(x)=2f(x)-1$.',[
 part('Find $a$ and the two possible values of $b$.',r'$a=1$, $b=4$ or $b=-4$.',[r'中线为 $a=(5+(-3))/2=1$。',r'振幅为 $|b|=(5-(-3))/2=4$；仅由最大最小值不能确定正负，所以 $b=\\pm4$。'],(('M1',1,'Finds the midline'),('M1',1,'Finds the amplitude'),('A1',1,'Keeps both signs'))),
 part('State the maximum and minimum values of $g$, and find the number of solutions of $g(x)=3$ for each possible value of $b$.',r'Range $[-7,9]$; two solutions for each sign of $b$.',[r'竖直放大2倍再下移1，故值域由 $[-3,5]$ 变为 $[-7,9]$。',r'若 $b=4$，方程为 $1+8\\cos x=3$，即 $\\cos x=1/4$，一周内有两个解。',r'若 $b=-4$，则 $1-8\\cos x=3$，即 $\\cos x=-1/4$，同样有两个解。'],(('M1',1,'Transforms the range'),('A1',1,'Gives both extrema'),('M1',1,'Forms both cosine equations'),('M1',1,'Counts valid roots'),('A1',1,'Completes both cases')))
 ],['三角图像','参数多解','值域与交点'],'P1-2025-06A-Q01','由图像极值和水平线交点判断变换结果',['设问角度','参数化与分类讨论','求解目标','跨考点耦合'],'极值只确定振幅绝对值，随后比较两种图像的交点',['不能凭极值决定余弦系数符号。','每种参数情形都要独立核对解数。'],'保留参数歧义并证明它是否影响交点数',fig_trig('Cosine graph with unknown sign')))

# C09 R31
Q.append(qnew('P1-C09-R31',9,'根式乘积积分与切线',
 'For $x>0$, a curve has gradient $\\dfrac{dy}{dx}=\\sqrt{x}(x-2)(x+2)$. The curve passes through $(1,5)$.',[
 part('Find the equation of the curve.',r'$y=\\frac27x^{7/2}-\\frac83x^{3/2}+\\frac{155}{21}$.',[r'先展开导函数：$\\sqrt{x}(x^2-4)=x^{5/2}-4x^{1/2}$。',r'积分得 $y=\\frac27x^{7/2}-\\frac83x^{3/2}+C$。',r'代入 $(1,5)$：$C=5-2/7+8/3=155/21$。'],(('M1',1,'Expands the product into powers'),('M1',1,'Integrates both terms'),('M1',1,'Uses the point condition'),('A1',1,'Finds the complete curve'))),
 part('Find the equation of the tangent at $x=4$.',r'$y-\\frac{475}{21}=24(x-4)$.',[r'在 $x=4$，梯度为 $\\sqrt4(4-2)(4+2)=24$。',r'曲线上点的纵坐标为 $\\frac27(4^{7/2})-\\frac83(4^{3/2})+155/21=475/21$。',r'用点斜式得到切线方程。'],(('M1',1,'Finds the gradient'),('M1',1,'Finds the point value'),('A1',1,'Gives the tangent')))
 ],['不定积分','根式展开','切线'],'P1-2024-06R-Q08','由因式导函数积分还原曲线并处理图像',['条件呈现','题目结构','跨考点耦合'],'展开分数幂后积分，以精确点值构造切线',['必须先正确展开再逐项积分。','切线需要梯度和曲线上点两个信息。'],'把原题的图像收尾改成精确切线重建'))
# C09 R32
Q.append(qnew('P1-C09-R32',9,'二阶导数重建与对称性',
 'A curve satisfies $\\dfrac{d^2y}{dx^2}=12x^2-4$. It passes through $(0,3)$ and has a horizontal tangent at $x=1$.',[
 part('Find the equation of the curve.',r'$y=x^4-2x^2+3$.',[r'第一次积分：$y\\prime=4x^3-4x+A$。',r'因 $x=1$ 处水平，$0=4-4+A$，所以 $A=0$。',r'再次积分：$y=x^4-2x^2+B$；代入 $(0,3)$ 得 $B=3$。'],(('M1',1,'First integration'),('M1',1,'Uses the horizontal tangent'),('A1',1,'Finds the first constant'),('M1',1,'Second integration'),('A1',1,'Uses the point and gives the curve'))),
 part('Determine whether the curve is symmetric about the $y$-axis, giving a reason.',r'Yes, because $f(-x)=f(x)$.',[r'$f(-x)=(-x)^4-2(-x)^2+3=x^4-2x^2+3=f(x)$。',r'函数是偶函数，因此图像关于 $y$ 轴对称。'],(('M1',1,'Evaluates f(-x)'),('A1',1,'Concludes symmetry'),('B1',1,'Gives the even-function reason')))
 ],['二阶积分','积分常数','对称性'],'P1-2021-10-Q10','二阶导数条件还原函数并检验对称性',['条件呈现','题目结构','收尾要求'],'两次积分分别确定常数，再以代数检验全局图像性质',['两次积分要保留两个不同常数。','对称性必须用f(-x)=f(x)验证。'],'去掉中间提示并要求全局性质解释'))
# C09 R33
Q.append(qnew('P1-C09-R33',9,'分数幂积分与驻点分类',
 'For $x>0$, a curve has gradient $\\dfrac{dy}{dx}=3x^{1/2}-3x^{-1/2}$. It passes through $(4,1)$.',[
 part('Find the equation of the curve.',r'$y=2x^{3/2}-6x^{1/2}-3$.',[r'逐项积分得 $y=2x^{3/2}-6x^{1/2}+C$。',r'代入 $(4,1)$：$1=16-12+C$，故 $C=-3$。'],(('M1',1,'Integrates the positive power'),('M1',1,'Integrates the negative power'),('A1',1,'General antiderivative'),('M1',1,'Uses the point'),('A1',1,'Finds the curve'))),
 part('Find the coordinates of the stationary point and determine its nature.',r'$(1,-7)$, a minimum.',[r'令导数为0：$3\\sqrt{x}-3/\\sqrt{x}=0$。因 $x>0$，乘以 $\\sqrt{x}$ 得 $3x-3=0$，所以 $x=1$。',r'代入曲线得 $y=-7$。',r'$y\\prime\\prime=\\frac32x^{-1/2}+\\frac32x^{-3/2}>0$，所以是极小点。'],(('M1',1,'Solves dy/dx=0 in the domain'),('A1',1,'Finds the point'),('A1',1,'Uses the second derivative to classify')))
 ],['分数幂积分','驻点','定义域'],'P1-2021-10-Q01','正负分数指数的不定积分',['题目结构','求解目标','跨考点耦合'],'分数幂积分后用定义域与二阶导数分类驻点',['积分x^-1/2时指数应增加1。','求驻点时必须使用x>0。'],'从单纯积分升级为定义域内的驻点证明'))
# C09 R34
Q.append(qnew('P1-C09-R34',9,'双重积分与弦切梯度比较',
 'A curve satisfies $\\dfrac{d^2y}{dx^2}=6x-4$. It passes through $(0,2)$ and $(2,6)$.',[
 part('Find the equation of the curve.',r'$y=x^3-2x^2+2x+2$.',[r'积分一次：$y\\prime=3x^2-4x+A$；再积分：$y=x^3-2x^2+Ax+B$。',r'代入 $(0,2)$ 得 $B=2$。',r'代入 $(2,6)$：$8-8+2A+2=6$，所以 $A=2$。'],(('M1',1,'First integration'),('M1',1,'Second integration with a new constant'),('A1',1,'General curve'),('M1',1,'Uses both points'),('A1',1,'Finds the curve'))),
 part('Find the gradient of the chord joining the two given points and the gradient of the tangent at $x=1$.',r'Chord gradient $2$; tangent gradient $1$.',[r'弦的梯度为 $(6-2)/(2-0)=2$。',r'$y\\prime=3x^2-4x+2$，所以 $x=1$ 处切线梯度为 $3-4+2=1$。'],(('M1',1,'Finds the chord gradient'),('A1',1,'Obtains 2'),('M1',1,'Uses the reconstructed derivative'),('A1',1,'Obtains 1')))
 ],['二阶积分','弦梯度','切线梯度'],'P1-2021-10-Q10','二阶积分条件恢复曲线并比较对称点性质',['条件呈现','跨考点耦合','收尾要求'],'用两个函数值确定双积分常数，再比较弦与切线',['点条件必须在第二次积分后使用。','弦梯度不能替代指定点的切线梯度。'],'把常数重建与局部/平均变化率比较结合'))
# C09 R35
Q.append(qnew('P1-C09-R35',9,'含参二阶导数与法线',
 'A curve satisfies $\\dfrac{d^2y}{dx^2}=ax+2$, where $a$ is constant. Its gradient at $x=1$ is $3$, and it passes through $(1,4)$.',[
 part('Find the equation of the curve in terms of $a$.',r'$y=\\frac{a}{6}x^3+x^2+(1-a/2)x+2+a/3$.',[r'积分得 $y\\prime=\\frac12ax^2+2x+C$。由 $y\\prime(1)=3$ 得 $C=1-a/2$。',r'再次积分并使用 $(1,4)$，得到 $y=\\frac{a}{6}x^3+x^2+(1-a/2)x+2+a/3$。'],(('M1',1,'First integration'),('M1',1,'Uses the gradient condition'),('M1',1,'Second integration'),('A1',1,'Uses the point and gives the curve'))),
 part('Given that the curve also passes through $(0,1)$, find $a$.',r'$a=-3$.',[r'令 $x=0$，由曲线方程得 $2+a/3=1$。',r'所以 $a=-3$。'],(('M1',1,'Uses the second point'),('A1',1,'Finds a'))),
 part('Find the equation of the normal at $(1,4)$.',r'$y-4=-\\frac13(x-1)$.',[r'切线梯度已知为3，所以法线梯度为 $-1/3$。',r'过 $(1,4)$ 的法线为 $y-4=-\\frac13(x-1)$。'],(('M1',1,'Uses the negative reciprocal'),('A1',1,'Gives the normal')))
 ],['参数积分','二阶导数','法线'],'P1-2024-10-Q08','由法线和含参导函数确定参数后积分',['设问角度','条件呈现','题目结构','跨考点耦合'],'在两次积分中分别处理参数、梯度条件和点条件',['两次积分常数不能混用。','法线斜率是切线斜率的负倒数。'],'把含参导函数升级为含参二阶模型和三条件重建'))
# C09 R36
Q.append(qnew('P1-C09-R36',9,'分式梯度积分与唯一截距证明',
 'For $x>0$, a curve has gradient $\\dfrac{dy}{dx}=2x^3-\\dfrac{2}{x^3}$. It passes through $(1,0)$.',[
 part('Find the equation of the curve.',r'$y=\\frac12x^4+x^{-2}-\\frac32$.',[r'把导函数写成 $2x^3-2x^{-3}$。',r'积分得 $y=\\frac12x^4+x^{-2}+C$。',r'代入 $(1,0)$ 得 $C=-3/2$。'],(('B1',1,'Writes powers correctly'),('M1',1,'Integrates both terms'),('A1',1,'General antiderivative'),('M1',1,'Uses the point'),('A1',1,'Finds the curve'))),
 part('Show that an $x$-intercept satisfies $x^6-3x^2+2=0$, and hence show that the curve has exactly one $x$-intercept.',r'The only intercept is $(1,0)$.',[r'令 $y=0$，乘以 $2x^2$ 得 $x^6-3x^2+2=0$。',r'令 $u=x^2>0$，则 $u^3-3u+2=(u-1)^2(u+2)=0$。',r'正值解只有 $u=1$；又因 $x>0$，所以只有 $x=1$。'],(('M1',1,'Derives the polynomial'),('M1',1,'Uses u=x^2'),('A1',1,'Factorises'),('A1',1,'Applies the positive domain and concludes uniqueness')))
 ],['分式积分','代换','唯一性证明'],'P1-2023-01-Q03','分式化幂积分并分析截距',['题目结构','求解目标','条件呈现','收尾要求'],'用定义域筛选代换方程的根并解释唯一截距',['不能保留u=-2。','由u=1还要结合x>0排除x=-1。'],'从求原函数升级为域约束下的唯一性证明'))

# Validations
assert len(Q)==46, len(Q)
ids=[q['id'] for q in Q];assert len(set(ids))==46
for q in Q:
 assert q['chapters']==[4] or q['chapters']==[9]
 assert sum(p['marks'] for p in q['parts'])==q['marks']
 leaves=[]
 for p in q['parts']:
  if p.get('subparts'):
   assert sum(sp['marks'] for sp in p['subparts']) == p['marks']
   leaves.extend(p['subparts'])
  else:
   leaves.append(p)
 for p in leaves:
  assert sum(r['marks'] for r in p['scheme'])==p['marks']
  assert p['solutionSteps'] and any('\u4e00' <= c <= '\u9fff' for c in ''.join(p['solutionSteps']))
 assert len(q.get('adaptationDimensions',[]))>=3 and q.get('sourceReferences')
counts=Counter(q['sourceReferences'][0]['questionId'] for q in Q)
assert max(counts.values())<=3,counts
(ROOT/'editorial/v15/p1-c04-c09.json').write_text(json.dumps({'version':15,'questions':Q},ensure_ascii=False,indent=2)+'\n')
print('wrote',len(Q),'active questions; source max',max(counts.values()))
