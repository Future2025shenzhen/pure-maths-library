import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
base=json.loads((ROOT/'dist/data/bank.json').read_text())
old={q['id']:q for q in base['questions']}

def scheme(*rows):
    return [{'code':c,'marks':m,'text':t} for c,m,t in rows]
def part(text,answer,steps,rows,approach=''):
    rows = rows if not rows or isinstance(rows[0], dict) else scheme(*rows)
    return {'text':text,'answer':answer,'explanation':'\n'.join(steps),'approach':approach or steps[0],
            'solutionSteps':steps,'scheme':rows,'marks':sum(r['marks'] for r in rows)}
def fig(kind,title):
    pre=f'<figure class="rewrite-figure"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 300" role="img" aria-label="{title}"><title>{title}</title><g fill="none" stroke="#222" stroke-width="1.6">'
    post='</g></svg><figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'
    text=lambda x,y,s:f'<text x="{x}" y="{y}" fill="#222" stroke="none" font-family="Georgia,serif" font-size="16">{s}</text>'
    shapes={
      'sector':f'<path d="M270 245L120 125A192 192 0 0 1 420 125Z"/><path d="M120 125L420 125" stroke-dasharray="6 4"/>{text(263,268,"O")}{text(98,120,"A")}{text(428,120,"B")}',
      'annular':f'<path d="M270 245L130 125A184 184 0 0 1 410 125L340 185A92 92 0 0 0 200 185Z"/><path d="M200 185L340 185" stroke-dasharray="6 4"/>{text(263,268,"O")}{text(112,120,"A")}{text(418,120,"B")}{text(183,183,"D")}{text(347,183,"C")}',
      'symmetric':f'<path d="M80 245L135 125A180 180 0 0 1 405 125L460 245Z"/><path d="M80 245H460"/><path d="M135 125L270 245L405 125" stroke-dasharray="6 4"/>{text(62,265,"A")}{text(120,115,"B")}{text(263,270,"O")}{text(412,115,"C")}{text(465,265,"D")}',
      'chord':f'<circle cx="270" cy="155" r="115"/><path d="M170 98L370 98M270 155L170 98M270 155L370 98"/>{text(263,178,"O")}{text(150,94,"A")}{text(380,94,"B")}',
      'rectseg':f'<path d="M150 105A130 130 0 0 1 390 105L390 245H150Z"/><path d="M150 105H390" stroke-dasharray="6 4"/><path d="M270 215L150 105M270 215L390 105" stroke-dasharray="6 4"/>{text(263,238,"O")}{text(130,100,"A")}{text(398,100,"B")}',
      'triangle':f'<path d="M90 245L435 245L210 65Z"/><path d="M90 245L245 175A170 170 0 0 1 90 75Z" transform="rotate(0 90 245)"/>{text(72,268,"A")}{text(445,268,"B")}{text(203,55,"C")}',
      'major':f'<circle cx="280" cy="155" r="110"/><path d="M280 155L185 100M280 155L385 125"/><path d="M185 100L95 235L385 125"/>{text(273,178,"O")}{text(168,92,"A")}{text(393,120,"C")}{text(78,255,"D")}',
      'semicircle':f'<path d="M100 225A170 170 0 0 1 440 225M100 225H440M270 225L210 66M270 225L395 112"/>{text(82,248,"A")}{text(448,248,"B")}{text(263,248,"O")}{text(197,56,"C")}',
      'partition':f'<path d="M270 245L120 125A192 192 0 0 1 420 125Z"/><path d="M195 185A96 96 0 0 1 345 185"/><path d="M120 125L420 125" stroke-dasharray="6 4"/>{text(263,268,"O")}{text(102,120,"A")}{text(428,120,"B")}{text(180,180,"C")}{text(352,180,"D")}',
      'fan':f'<path d="M270 150L270 35A115 115 0 0 1 360 78L315 114A58 58 0 0 0 270 92Z"/><path d="M270 150L385 150A115 115 0 0 1 342 240L306 195A58 58 0 0 0 328 150Z"/><path d="M270 150L270 265A115 115 0 0 1 180 222L225 186A58 58 0 0 0 270 208Z"/><path d="M270 150L155 150A115 115 0 0 1 198 60L234 105A58 58 0 0 0 212 150Z"/>{text(263,173,"O")}',
      'coordinate':f'<path d="M70 245H470M140 275V35"/><path d="M140 70L350 210"/><path d="M140 235L350 77"/><path d="M140 70A175 175 0 0 1 420 145"/><path d="M140 235L350 210L140 150Z" stroke-dasharray="6 4"/>{text(125,64,"A")}{text(357,218,"B")}{text(123,257,"C")}{text(424,145,"D")}{text(123,148,"O")}',
      'sign':f'<path d="M110 245L280 155L195 75Z"/><path d="M280 155A120 120 0 1 1 195 75"/><path d="M110 245L235 178" stroke-dasharray="6 4"/>{text(92,266,"P")}{text(180,65,"Q")}{text(287,160,"C")}{text(226,196,"T")}',
      'arcs':f'<circle cx="270" cy="155" r="120"/><path d="M270 155L160 108M270 155L280 35M270 155L382 112"/>{text(263,178,"O")}{text(140,105,"A")}{text(273,27,"B")}{text(390,110,"C")}'
    }
    return pre+shapes[kind]+post

def question(id,type_,stem,parts,topics,source,summary,dims,essence,errors,design,figure='',chapters=[7,6],classic=False):
    n=int(id[-2:])
    return {'id':id,'stage':'P1','chapters':chapters,'type':type_,'stem':stem+figure,'parts':parts,
      'marks':sum(p['marks'] for p in parts),'topics':topics,'origin':'original-reviewed-2026','review':'internal-review-only',
      'editorialRevision':14,'originalNumber':n,'sourceReferences':[{'questionId':source,'year':int(source[3:7]),'note':summary}],
      'sourceSummary':summary,'adaptationDimensions':dims,'examEssence':essence,
      'difficultyPosition':f'略难于 {source}：{design}','errorNotes':errors,'designNote':design,
      'adaptationNote':('真题固定套路，按原貌保留；' if classic else '')+'改编维度：'+'、'.join(dims)+'。思维增量：'+design,
      'answerFigure':'','family':id,'solutionRevision':14,'contentUpdatedAt':'2026-10-24'}

Q=[]
# R01 strengthened classic routine
alpha=r'(\pi-2)/2'
Q.append(question('P1-C07-R01','对称扇形拼接与设计判断',
 'A stage consists of a sector $OBC$ and two congruent triangles $OAB$ and $OCD$. The points $A,O,D$ lie on a straight line. The radius of the sector is $5$ m, $\\angle BOC=2$ radians and $OA=OD=4$ m. The outside boundary is $AB$, arc $BC$, $CD$ and $DA$.',[
 part(r'Show that $\angle AOB=\dfrac{\pi-2}{2}$ radians and find $AB$ to 3 significant figures.',r'$\angle AOB=(\pi-2)/2$, $AB=2.71$ m.',[r'Angles on the same side of the straight line give $2\angle AOB+2=\pi$.',r'$AB^2=4^2+5^2-2(4)(5)\cos((\pi-2)/2)$, so $AB=2.709\ldots$.'],scheme(('B1',1,'Uses the straight-line angle relation'),('M1',1,'Applies the cosine rule with the derived angle'),('A1',1,'Obtains 2.71 m to 3 significant figures'))),
 part('Find the total area and the total perimeter of the stage, giving each answer to 3 significant figures.',r'Area $=35.8\text{ m}^2$; perimeter $=23.4\text{ m}$.',[r'$A=\tfrac12(5)^2(2)+2[\tfrac12(4)(5)\sin((\pi-2)/2)]=35.806\ldots$.',r'$P=2AB+5(2)+8=23.418\ldots$; the two radii are internal.'],scheme(('M1',1,'Combines the sector with both triangle areas'),('A1',1,'Gives 35.8 m²'),('M1',1,'Uses only the outside boundary'),('A1',1,'Gives 23.4 m'))),
 part('A safety rule requires the numerical value of the area to be at least $1.5$ times the numerical value of the perimeter. Determine whether the stage satisfies the rule.',r'Yes, since $35.806\ldots>1.5(23.418\ldots)=35.128\ldots$.',[r'Use unrounded values from part (b).',r'$35.806\ldots-1.5(23.418\ldots)=0.678\ldots>0$, so the rule is satisfied.'],scheme(('M1',1,'Compares the unrounded area with 1.5 times the perimeter'),('A1',1,'States the correct conclusion with evidence')))
 ],['弧度制','余弦定理','组合面积','边界判断'],'P1-2024-06R-Q06','扇形与两个全等侧三角形：证明侧角、求周界和面积',['题目结构','收尾要求','跨考点耦合'],'识别直线角、弧长、扇形面积及真正外边界','最后一问若使用已四舍五入数值可能误判；两条公共半径不属于外周界。'.split('；'),'在固定套路末尾加入必须使用未舍入值的设计判断',fig('symmetric','Sector joined to two congruent triangles'),classic=True))

# R02 annular inverse
Q.append(question('P1-C07-R02','环形扇区的反向尺寸设计',
 'An annular sector has centre $O$, inner radius $r$ cm, outer radius $2r$ cm and angle $\theta$ radians, where $0<\theta<\pi$. The outer arc is $4$ cm longer than the inner arc and the area of the annular sector is $48\text{ cm}^2$.',[
 part('Find $r$ and $\theta$.',r'$r=8$ cm and $\theta=0.5$ radians.',[r'The arc-length difference is $(2r-r)\theta=4$, so $r\theta=4$.',r'$48=\tfrac12((2r)^2-r^2)\theta=\tfrac32r^2\theta=6r$.',r'Hence $r=8$ and $\theta=4/8=0.5$.'],scheme(('M1',1,'Forms the arc-length difference'),('M1',1,'Forms the annular area equation'),('A1',1,'Finds r=8'),('A1',1,'Finds θ=0.5'))),
 part('Find the complete perimeter of the annular sector.',r'$28$ cm.',[r'The two arcs have lengths $4$ and $8$ cm.',r'The two radial edges each have length $2r-r=8$ cm, so $P=4+8+16=28$.'],scheme(('M1',1,'Includes both arcs and both radial edges'),('A1',1,'Obtains 28 cm'))),
 part('The angle is increased by $20\%$, while the area and the ratio of the radii remain unchanged. Find the new inner radius to 3 significant figures.',r'$7.30$ cm.',[r'With outer radius twice the inner radius, area is proportional to $r^2\theta$.',r'$r_{new}^2(1.2\theta)=8^2\theta$, so $r_{new}=8/\sqrt{1.2}=7.302\ldots$.'],scheme(('M1',1,'Keeps r²θ constant'),('M1',1,'Forms the scale relation'),('A1',1,'Obtains 7.30 cm')))
 ],['环形扇区','反向建模','比例变化'],'P1-2024-01-Q08','不同半径的同心扇区：由比例关系求尺寸、周界与面积',['设问角度','条件呈现','参数化与分类讨论','收尾要求'],'同时使用弧长差和面积差确定尺度，再判断参数变化','把外半径误当作宽度；改变角度后仍把半径保持不变。'.split('；'),'由正向计算改为双条件反求，并加入保持面积的参数变化',fig('annular','Annular sector with radii r and 2r'),chapters=[7,2]))

# R03 retained but metadata/mark scheme refined
q=old['P1-C07-R03'];q={**q,'withdrawn':False};q.pop('withdrawalReason',None)
q.update(editorialRevision=14,solutionRevision=14,contentUpdatedAt='2026-10-24',difficultyPosition='略难于 P1-2022-01-Q05：由面积关系自行建立非线性方程，并在给根后完成弧弦比和弓形面积。',sourceSummary='半圆内弓形：证明圆心角、求弓形面积及含弧周界',adaptationDimensions=['设问角度','求解目标','条件呈现','题目结构'],examEssence='弧度制下扇形面积、三角形面积、弦长与弓形面积的连接',errorNotes=['方程中的正弦角是 θ，而弦长公式使用 θ/2。','给定数值根并不免除前问建立方程的过程。'],designNote='把给角计算改成由面积比反推隐式方程，并加入无量纲弧弦比。',adaptationNote='改编维度：设问角度、求解目标、条件呈现、题目结构。思维增量：由面积比反推隐式方程，再处理弧弦比。')
q['parts'][0]['scheme']=scheme(('M1',1,'Equates the sector area to three times the triangle area'),('A1',1,'Cancels the valid non-zero factor and obtains θ=3 sin θ'))
q['parts'][1]['scheme']=scheme(('M1',1,'Uses arc rθ and chord 2r sin(θ/2)'),('A1',1,'Obtains 1.25:1 to 3 significant figures'))
q['parts'][2]['scheme']=scheme(('M1',1,'Uses 1/2 r²(θ−sinθ)'),('A1',1,'Substitutes r=5 and the supplied root'),('A1',1,'Obtains 19.0 square units to 3 significant figures'))
Q.append(q)

# R07 chord and second circle
th=math.acos(7/25); seg1=50*(th-math.sin(th)); k=6/math.sin(th/4); seg2=.5*k*k*(th/2-math.sin(th/2))
Q.append(question('P1-C07-R07','同弦在两圆中的弓形比较',
 'In a circle with centre $O$, $OA=OB=10$ cm and the chord $AB$ has length $12$ cm. The minor angle $AOB$ is $\theta$ radians.',[
 part(r'Show that $\cos\theta=\dfrac7{25}$ and find $\theta$ to 3 decimal places.',r'$\cos\theta=7/25$, $\theta=1.287$ radians.',[r'By the cosine rule, $12^2=10^2+10^2-2(10)(10)\cos\theta$.',r'Hence $\cos\theta=56/200=7/25$ and $\theta=1.287\ldots$.'],scheme(('M1',1,'Applies the cosine rule'),('A1',1,'Obtains cos θ=7/25'),('A1',1,'Obtains θ=1.287 radians'))),
 part('Find the area of the minor segment bounded by $AB$ and the minor arc.',f'${seg1:.3g}\\text{{ cm}}^2$.',[r'$A_{segment}=\tfrac12(10)^2(\theta-\sin\theta)$.',f'This gives ${seg1:.6f}\ldots\text{{ cm}}^2$.'],scheme(('M1',1,'Subtracts the isosceles triangle from the sector'),('A1',1,'Uses the unrounded angle'),('A1',1,'Gives the correct area to 3 significant figures'))),
 part(r'In a second circle the same chord $AB$ subtends the angle $\theta/2$. Find the radius of the second circle and determine which minor segment has the greater area.',f'Radius $={k:.3g}$ cm; the first segment is larger (${seg1:.3g}>{seg2:.3g}$).',[r'For the second circle, $12=2R\sin(\theta/4)$, so $R=6/\sin(\theta/4)$.',f'$R={k:.6f}\ldots$ cm and $A_2=\tfrac12R^2(\theta/2-\sin(\theta/2))={seg2:.6f}\ldots$.',f'Compare with the first segment area ${seg1:.6f}\ldots$.'],scheme(('M1',1,'Builds the half-angle chord equation'),('A1',1,'Finds the second radius'),('M1',1,'Calculates the second segment area'),('A1',1,'Makes the correct comparison')))
 ],['弦长','余弦定理','弓形比较'],'P1-2024-06-Q05','扇形、三角形角度与组合面积',['条件呈现','求解目标','跨考点耦合','收尾要求'],'由弦确定圆心角，再连接弓形面积','弦公式使用半圆心角；第二个圆半径较大并不保证弓形面积较大。'.split('；'),'加入同弦异圆的反向半角模型和面积比较',fig('chord','A chord in a circle')))

# R08 rectangle plus segment inverse
th=2*math.asin(.6); seg=50*(th-math.sin(th)); h=(71.2-seg)/12; per=10*th+12+2*h; pct=100*seg/71.2
Q.append(question('P1-C07-R08','由总面积反求矩形高度',
 'A circle has centre $O$, radius $10$ cm and chord $AB=12$ cm. A rectangle of width $12$ cm and height $h$ cm is attached to $AB$ on the opposite side from the minor segment. The combined region consists of the rectangle and the minor segment and has area $71.2\text{ cm}^2$.',[
 part('Show that the angle subtended by the minor arc is $1.287$ radians to 4 significant figures.',r'$\theta=2\sin^{-1}(6/10)=1.287\ldots$.',[r'Bisect the chord and the central angle.',r'$\sin(\theta/2)=6/10$, hence $\theta=2\sin^{-1}(0.6)=1.287\ldots$.'],scheme(('M1',1,'Uses the half-chord right triangle'),('A1',1,'Shows 1.287 radians'))),
 part('Find $h$, giving your answer to 3 significant figures.',f'${h:.3g}$ cm.',[r'The minor segment area is $50(\theta-\sin\theta)$.',f'$12h+50(\theta-\sin\theta)=71.2$, so $h={h:.6f}\ldots$.'],scheme(('M1',1,'Forms the minor segment area'),('M1',1,'Uses the combined-area condition'),('A1',1,'Obtains h to 3 significant figures'))),
 part('Find the perimeter of the combined region to 3 significant figures.',f'${per:.3g}$ cm.',[r'The outside boundary is the minor arc, the opposite side of the rectangle and its two heights.',f'$P=10\theta+12+2h={per:.6f}\ldots$ cm.'],scheme(('M1',1,'Identifies the correct outside boundary'),('M1',1,'Uses arc length 10θ'),('A1',1,'Gives the perimeter to 3 significant figures'))),
 part('The curved segment is removed by cutting along $AB$. Find the percentage of the original area that is removed.',f'${pct:.3g}\%$.',[f'The removed area is the minor segment, ${seg:.6f}\ldots\text{{ cm}}^2$.',f'Percentage removed $=100({seg:.6f}\ldots)/71.2={pct:.6f}\ldots\%$.'],scheme(('M1',1,'Uses the segment area as the removed area'),('A1',1,'Obtains the correct percentage')))
 ],['弓形面积','反向条件','真实周界'],'P1-2020-01-Q04','矩形与大扇形组合：证明角度、求面积和外周界',['设问角度','条件呈现','题目结构','收尾要求'],'从弦长建立圆心角并分辨弓形和矩形的外边界','组合面积包含弓形而不是整个扇形；公共弦AB不是最终外周界。'.split('；'),'用总面积反求未知高度，再以切割后的面积损失收尾',fig('rectseg','Rectangle joined to a circular segment'),chapters=[7,2]))

# R10 strengthened inverse pair
q=old['P1-C07-R10'];q.pop('withdrawn',None);q.pop('withdrawalReason',None)
q.update(editorialRevision=14,solutionRevision=14,contentUpdatedAt='2026-10-24',marks=7,difficultyPosition='略难于 P1-2019-01-Q10：由两扇形的面积与周界条件联立，随后比较两个弓形。',sourceReferences=[{'questionId':'P1-2019-01-Q10','year':2019,'note':'由扇形面积与周界条件建立方程并判断两组有效解'}],sourceSummary='给定扇形面积和周界，建立二次方程并求两组半径与角',adaptationDimensions=['情境与载体','条件呈现','求解目标','收尾要求'],examEssence='同时使用 A=1/2 r²θ 与 P=2r+rθ 反求参数',errorNotes=['等面积条件中的半径必须平方。','求出角后仍要检查两个扇形均为minor sector。'],designNote='把单扇形二次方程改为两个扇形联立，并以弓形面积比收尾。',adaptationNote='改编维度：情境与载体、条件呈现、求解目标、收尾要求。思维增量：双扇形联立并检查有效范围。')
q['parts'][0]=part('Find the exact values of $\theta$ and $\phi$, and verify that both sectors are minor sectors.',r'$\theta=1$, $\phi=4/9$; both lie in $(0,\pi)$.',[r'Equal areas give $36\theta=81\phi$, so $\phi=4\theta/9$.',r'The perimeter condition gives $18+9\phi=12+6\theta+4$.',r'Hence $\theta=1$ and $\phi=4/9$; both are between $0$ and $\pi$.'],scheme(('M1',1,'Forms the equal-area equation'),('M1',1,'Forms the perimeter-difference equation'),('A1',1,'Finds both exact angles'),('A1',1,'Checks the minor-sector range')))
q['parts'][1]=part(q['parts'][1]['text'],q['parts'][1]['answer'],[r'$A_S=18(1-\sin1)$ and $A_T=\tfrac{81}{2}(4/9-\sin(4/9))$.',r'The ratio is $4.863\ldots:1=4.86:1$.'],scheme(('M1',1,'Forms both segment areas'),('M1',1,'Divides in the required order'),('A1',1,'Gives 4.86:1')))
Q.append(q)

# R11 inverse sector within triangle
ang=1.2; r2=(220/9)*math.sin(ang); rr=math.sqrt(r2); BC=math.sqrt(8**2+11**2-2*8*11*math.cos(ang)); alt=88*math.sin(ang)/BC; P=19+BC-.8*rr
Q.append(question('P1-C07-R11','面积比反求内扇形半径',
 'Triangle $ABC$ has $AB=8$ cm, $AC=11$ cm and $\angle BAC=1.2$ radians. A sector with centre $A$, radius $r$ cm and angle $1.2$ radians is removed from the corner. The area left is twice the area of the sector.',[
 part(r'Show that $r^2=\dfrac{220}{9}\sin1.2$ and find $r$ to 3 significant figures.',f'$r={rr:.3g}$ cm.',[r'The triangle area is $\tfrac12(8)(11)\sin1.2=44\sin1.2$.',r'Triangle area minus sector area equals twice the sector area, so $44\sin1.2=3(0.6r^2)$.',f'Hence $r^2=\dfrac{{220}}{{9}}\sin1.2$ and $r={rr:.6f}\ldots$.'],scheme(('M1',1,'Forms the triangle and sector areas'),('M1',1,'Uses the stated area ratio'),('A1',1,'Obtains the required expression and radius'))),
 part('Find the perpendicular distance from $A$ to $BC$ and hence justify that the complete sector lies inside the triangle.',f'Distance $={alt:.3g}$ cm, which is greater than $r$, so the sector lies inside.',[f'$BC=\sqrt{{8^2+11^2-2(8)(11)\cos1.2}}={BC:.6f}\ldots$.',f'Using $\tfrac12BC\,h=44\sin1.2$ gives $h={alt:.6f}\ldots$ cm.',f'Since $r={rr:.6f}\ldots<h$ and $r<8,11$, the arc does not cross any side.'],scheme(('M1',1,'Finds BC and uses triangle area to obtain the altitude'),('A1',1,'Obtains the perpendicular distance'),('A1',1,'Gives a valid containment justification'))),
 part('Find the perimeter of the remaining region to 3 significant figures.',f'${P:.3g}$ cm.',[r'The exposed straight lengths are $(8-r)+(11-r)+BC$.',f'Add the new arc $1.2r$: $P=19+BC-0.8r={P:.6f}\ldots$.'],scheme(('M1',1,'Identifies the two shortened sides, BC and the new arc'),('M1',1,'Forms the complete perimeter'),('A1',1,'Gives the perimeter to 3 significant figures')))
 ],['面积比','内含判断','组合周界'],'P1-2024-06-Q05','扇形、三角形角度与组合面积',['设问角度','条件呈现','跨考点耦合','收尾要求'],'扇形与三角形面积、余弦定理和真实边界','面积比是“余下:扇形=2:1”；只检查r小于两邻边不足以证明圆弧不越过BC。'.split('；'),'由面积比反求半径，并要求用垂距证明几何内含',fig('triangle','A sector removed from a triangle')))

# R13 major sector plus triangle, A3 routine extension
O=math.pi-math.asin(2*math.sin(.4)); A=math.pi-O-.4; OD=14*math.sin(A)/math.sin(O); major=2*math.pi-O; area=.5*49*major+.5*7*OD*math.sin(O); per=7*major+(OD-7)+14
Q.append(question('P1-C07-R13','钝角取舍与大扇形平台',
 'A platform consists of a major sector $ACBA$ of a circle with centre $O$ and radius $7$ m, joined to triangle $AOD$. Points $O,C,D$ are collinear in that order. Given $AD=14$ m, $\angle ADC=0.4$ radians and $\angle AOD$ is obtuse,',[
 part('find $\angle AOD$ to 3 decimal places.',f'${O:.3f}$ radians.',[r'By the sine rule, $\sin\angle AOD/14=\sin0.4/7$, so $\sin\angle AOD=2\sin0.4$.',f'The calculator gives an acute angle and the required obtuse angle is $\pi-\sin^{{-1}}(2\sin0.4)={O:.6f}\ldots$.'],scheme(('M1',1,'Uses the sine rule correctly'),('M1',1,'Selects the obtuse alternative'),('A1',1,'Gives the angle to 3 decimal places'))),
 part('find $OD$ and the length of the major arc $ACB$, giving each to 3 significant figures.',f'$OD={OD:.3g}$ m; arc $ACB={7*major:.3g}$ m.',[f'$\angle OAD=\pi-{O:.6f}\ldots-0.4={A:.6f}\ldots$.',f'$OD/\sin\angle OAD=14/\sin\angle AOD$, giving $OD={OD:.6f}\ldots$.',f'The major angle is $2\pi-\angle AOD={major:.6f}\ldots$, so the arc is $7({major:.6f}\ldots)$.'],scheme(('M1',1,'Finds the third triangle angle and uses the sine rule'),('A1',1,'Finds OD'),('A1',1,'Uses the major angle for the arc'))),
 part('find the total area of the platform to 3 significant figures.',f'${area:.3g}\text{{ m}}^2$.',[r'Add the major-sector area and the triangle area.',f'$A=\tfrac12(7)^2({major:.6f}\ldots)+\tfrac12(7)({OD:.6f}\ldots)\sin({O:.6f}\ldots)={area:.6f}\ldots$.'],scheme(('M1',1,'Uses the major-sector area'),('M1',1,'Finds the triangle area'),('A1',1,'Gives the total area'))),
 part('find the perimeter of the platform, stating which given length is not part of the outside boundary.',f'${per:.3g}$ m; $OC=7$ m is internal.',[r'The outside boundary is major arc $ACB$, $CD=OD-7$, and $DA=14$.',f'$P=7({major:.6f}\ldots)+({OD:.6f}\ldots-7)+14={per:.6f}\ldots$.'],scheme(('B1',1,'States that the shared radius OC is internal'),('M1',1,'Forms the correct perimeter'),('A1',1,'Gives the perimeter to 3 significant figures')))
 ],['正弦定理两解','大扇形','组合面积与周界'],'P1-2021-01-Q05','正弦定理钝角取舍、大弧长及平台组合面积',['参数数值设计','题目结构','收尾要求'],'钝角取舍决定大弧、小弧和整体边界','直接采用反正弦主值会选错角；大弧角为2π减圆心角。'.split('；'),'真题固定流程上增加未知边和完整外周界判断',fig('major','Major sector joined to a triangle'),classic=True))

# R15 strengthened cut annular
q=old['P1-C07-R15'];q.pop('withdrawn',None);q.pop('withdrawalReason',None)
q.update(editorialRevision=14,solutionRevision=14,contentUpdatedAt='2026-10-24',marks=7,difficultyPosition='略难于 P1-2023-10-Q09：除反求角和面积外，还要重建不等分切割后的两套边界。',sourceSummary='环形扇区：证明内半径、建立尺寸方程并求完整周界',adaptationDimensions=['设问角度','题目结构','求解目标','收尾要求'],examEssence='环形面积、双弧长和切割后新增边界',errorNotes=['环形扇区的径向边长度是外半径减内半径。','切开后公共切口在两块材料上各出现一次。'],designNote='把二等分改成1:2分割，要求解释两块周长之和为何增加。',adaptationNote='改编维度：设问角度、题目结构、求解目标、收尾要求。思维增量：切割后需重新识别每一块的真实边界。')
q['parts']=[
 part(r'Show that $\theta=\dfrac65$ and find the area of the annular sector.',r'$\theta=6/5$; area $=27\text{ cm}^2$.',[r'$24=9\theta+6\theta+2(9-6)=15\theta+6$, so $\theta=6/5$.',r'$A=\tfrac12(9^2-6^2)(6/5)=27\text{ cm}^2$.'],scheme(('M1',1,'Forms the complete perimeter equation'),('A1',1,'Shows θ=6/5'),('A1',1,'Finds the annular area'))),
 part('A radial cut divides the angle in the ratio $1:2$. Find the perimeter of each piece and explain why their sum is greater than $24$ cm.',r'Perimeters $12$ cm and $18$ cm; the sum is $6$ cm greater because the cut creates two new edges of length $3$ cm.',[r'The angles are $0.4$ and $0.8$ radians.',r'Each piece has two radial edges of length $3$, so $P_1=15(0.4)+6=12$ and $P_2=15(0.8)+6=18$.',r'The original perimeter contains two end edges; after cutting, four such edges are exposed, adding $2(3)=6$ cm overall.'],scheme(('M1',1,'Finds the two angles'),('M1',1,'Builds the first new perimeter'),('A1',1,'Obtains both perimeters'),('A1',1,'Explains the 6 cm increase')))
]
Q.append(q)

# R20 major-sector sign classic
PQ=.8;PC=2.4;pa=.9;rad=math.sqrt(PQ**2+PC**2-2*PQ*PC*math.cos(pa)); ca=math.asin(PQ*math.sin(pa)/rad); maj=2*math.pi-ca; ar=.5*rad*rad*maj+.5*PQ*PC*math.sin(pa); pe=rad*maj+PQ+(PC-rad); ratio=ar/pe
Q.append(question('P1-C07-R20','三角形与大扇形标志',
 'A sign is formed by triangle $CPQ$ joined to a major sector with centre $C$. The sector shares the side $CQ$ with the triangle. Point $T$ lies on $CP$ with $CT=CQ$. Given $PQ=0.8$ m, $PC=2.4$ m and $\angle QPC=0.9$ radians,',[
 part('find the radius $CQ$ to 3 decimal places.',f'$CQ={rad:.3f}$ m.',[r'$CQ^2=0.8^2+2.4^2-2(0.8)(2.4)\cos0.9$.',f'Hence $CQ={rad:.6f}\ldots$ m.'],scheme(('M1',1,'Applies the cosine rule'),('A1',1,'Gives the radius to 3 decimal places'))),
 part('hence find $\angle PCQ$ to 3 decimal places.',f'${ca:.3f}$ radians.',[r'Use $\sin\angle PCQ/0.8=\sin0.9/CQ$.',f'This gives $\angle PCQ={ca:.6f}\ldots$ radians.'],scheme(('M1',1,'Uses the sine rule or an equivalent cosine-rule method'),('A1',1,'Gives the angle to 3 decimal places'))),
 part('find the total area of the sign to 3 significant figures.',f'${ar:.3g}\text{{ m}}^2$.',[f'The major-sector angle is $2\pi-{ca:.6f}\ldots={maj:.6f}\ldots$.',f'Add $\tfrac12CQ^2({maj:.6f}\ldots)$ and $\tfrac12(0.8)(2.4)\sin0.9$ to obtain ${ar:.6f}\ldots$.'],scheme(('M1',1,'Uses the major-sector angle'),('M1',1,'Adds sector and triangle areas'),('A1',1,'Gives the total area'))),
 part('find the total perimeter of the sign to 3 significant figures.',f'${pe:.3g}$ m.',[r'The shared radius $CQ$ is internal; the exposed straight lengths are $PQ$ and $PT=PC-CQ$.',f'$P=CQ(2\pi-\angle PCQ)+0.8+(2.4-CQ)={pe:.6f}\ldots$.'],scheme(('M1',1,'Identifies PT and excludes shared CQ'),('A1',1,'Gives the perimeter'))),
 part('A display rule requires area/perimeter to exceed $0.95$ m. Determine whether the sign satisfies the rule.',f'Yes; the ratio is ${ratio:.3f}$ m.',[f'$A/P={ar:.6f}\ldots/{pe:.6f}\ldots={ratio:.6f}\ldots>0.95$.'],scheme(('B1',1,'Uses unrounded values and states the correct conclusion')))
 ],['余弦定理','大扇形','真实边界'],'P1-2025-06A-Q09','三角形与大扇形标志：求半径、证明角、面积及周界',['情境与载体','参数数值设计','收尾要求'],'由三角形确定扇形半径和角度，并排除共享边','大扇形角不是已求小角；直线边PT是PC−CQ。'.split('；'),'保留真题固定结构，并追加无提示的设计比值判断',fig('sign','Triangle joined to a major sector'),classic=True))

# R21 ambiguity and major arc
O=math.pi-math.asin(2*math.sin(.4)); A=math.pi-O-.4;OD=14*math.sin(A)/math.sin(O);maj=2*math.pi-O; arcl=7*maj; area=.5*49*maj+.5*7*OD*math.sin(O); per=arcl+(OD-7)+14
# distinct numbers already R13; avoid duplicate by make R21 segment comparison instead based on source ambiguity
r=9; chord=14; theta=2*math.asin(chord/(2*r)); minor=.5*r*r*(theta-math.sin(theta)); majorseg=math.pi*r*r-minor; pdiff=r*(2*math.pi-2*theta)
Q.append(question('P1-C07-R21','同弦大小弓形的选择与证明',
 'A chord $AB$ of a circle of radius $9$ cm has length $14$ cm. It divides the circle into a minor segment $S$ and a major segment $T$. Let the minor angle $AOB$ be $\theta$ radians.',[
 part('Find $\theta$ to 3 decimal places and explain why the other solution of $\sin(\theta/2)=7/9$ is not used for the minor angle.',f'$\theta={theta:.3f}$ radians; the other value gives an angle greater than $\pi$.',[r'$14=2(9)\sin(\theta/2)$, so $\sin(\theta/2)=7/9$.',f'The minor solution gives $\theta={theta:.6f}\ldots<\pi$; the supplementary half-angle would give $\theta>\pi$.'],scheme(('M1',1,'Forms the half-angle chord equation'),('A1',1,'Finds the minor angle'),('A1',1,'Rejects the non-minor alternative correctly'))),
 part('Find the areas of $S$ and $T$, giving each to 3 significant figures.',f'$S={minor:.3g}\text{{ cm}}^2$, $T={majorseg:.3g}\text{{ cm}}^2$.',[f'$A_S=\tfrac12(9)^2(\theta-\sin\theta)={minor:.6f}\ldots$.',f'$A_T=81\pi-A_S={majorseg:.6f}\ldots$.'],scheme(('M1',1,'Finds the minor segment area'),('M1',1,'Subtracts from the circle area'),('A1',1,'Gives both areas to 3 significant figures'))),
 part(r'Show that the difference between the perimeters of $T$ and $S$ is $18(\pi-\theta)$, and find this difference.',f'$18(\pi-\theta)={pdiff:.3g}$ cm.',[r'The common chord cancels when the two perimeters are subtracted.',r'The arc-length difference is $9(2\pi-\theta)-9\theta=18(\pi-\theta)$.',f'Substitution gives ${pdiff:.6f}\ldots$ cm.'],scheme(('B1',1,'Recognises that the chord cancels'),('M1',1,'Subtracts major and minor arc lengths'),('A1',1,'Obtains the stated form and numerical value'))),
 part('Determine whether the area ratio $T:S$ is greater than the perimeter ratio $P_T:P_S$.',r'Yes; compare the two ratios using unrounded values.',[f'$T:S={majorseg/minor:.6f}\ldots$.',f'$P_T:P_S={(9*(2*math.pi-theta)+14)/(9*theta+14):.6f}\ldots$, so the area ratio is greater.'],scheme(('M1',1,'Forms both ratios with the common chord included in each perimeter'),('A1',1,'States the correct comparison')))
 ],['大小弓形','多解取舍','证明'],'P1-2021-01-Q05','正弦定理的钝角取舍与大弧选择',['设问角度','求解目标','条件呈现','收尾要求'],'角的有效范围决定大小弧与弓形','求弦长反角时需检查minor范围；比较周长时弦在两边都必须保留。'.split('；'),'把钝角取舍转化为半角多解判断，并比较面积比与周长比',fig('chord','Minor and major segments cut by one chord')))

# R23 concentric partition
x=4*math.sqrt(3); innerarc=x*1.1; outerarc=13.2; Pann=outerarc+innerarc+2*(12-x); chord=2*x*math.sin(.55); reduction=innerarc-chord
Q.append(question('P1-C07-R23','面积比例分割扇形',
 'A sector $OAB$ has radius $12$ cm and angle $1.1$ radians. A concentric arc $CD$ of radius $x$ cm divides it into an inner sector and an outer annular region. The area of the outer region is twice the area of the inner sector.',[
 part(r'Show that $x=4\sqrt3$ cm.',r'$x=4\sqrt3$ cm.',[r'$\tfrac12(12^2-x^2)(1.1)=2[\tfrac12x^2(1.1)]$.',r'Hence $144-x^2=2x^2$, so $x^2=48$ and $x=4\sqrt3$ since $x>0$.'],scheme(('M1',1,'Forms the area-ratio equation'),('A1',1,'Obtains the positive exact radius'))),
 part('Find the complete perimeter of the outer annular region to 3 significant figures.',f'${Pann:.3g}$ cm.',[r'The boundary contains outer arc $12(1.1)$, inner arc $x(1.1)$ and two radial widths $12-x$.',f'$P=13.2+1.1(4\sqrt3)+2(12-4\sqrt3)={Pann:.6f}\ldots$.'],scheme(('M1',1,'Includes both arcs and both radial widths'),('M1',1,'Substitutes the exact radius'),('A1',1,'Gives the perimeter'))),
 part('The inner arc $CD$ is replaced by its chord. Find the reduction in the perimeter of the outer region to 3 significant figures.',f'${reduction:.3g}$ cm.',[r'The chord is $2x\sin(1.1/2)=8\sqrt3\sin0.55$.',f'The reduction is $1.1x-2x\sin0.55={reduction:.6f}\ldots$ cm.'],scheme(('M1',1,'Uses the half-angle chord formula'),('M1',1,'Subtracts chord from arc in the correct order'),('A1',1,'Gives the reduction'))),
 part('State, with a reason, whether replacing the arc changes the area ratio of the two original regions.',r'Yes. The chord transfers the inner segment from the inner region to the outer region.',[r'The chord does not follow the original dividing arc.',r'The circular segment between chord and arc changes ownership, so the original $2:1$ area ratio is not preserved.'],scheme(('B1',1,'Identifies the transferred segment'),('B1',1,'States the correct conclusion with a geometric reason')))
 ],['面积比','同心分割','弧弦替换'],'P1-2024-10-Q05','扇形按面积比例分割，反求分割线并处理周界',['设问角度','题目结构','跨考点耦合','收尾要求'],'面积比例反求半径并区分弧与弦对边界和面积的影响','外环边界必须包含内弧；把内弧换成弦会改变两区面积而不仅改变周长。'.split('；'),'从求分割尺寸扩展到弧弦替换及面积比是否保持的判断',fig('partition','A sector divided by a concentric arc')))

# R24 limiting contained sector
r=math.sqrt(40/math.pi);lim=60/13;prem=13+(12-r)+(5-r)+r*math.pi/2;pct=100*(math.pi*lim*lim/4)/30
Q.append(question('P1-C07-R24','内扇形面积比与极限半径',
 'Triangle $OAB$ is right-angled at $O$, with $OA=12$ cm and $OB=5$ cm. A sector with centre $O$, angle $\pi/2$ and radius $r$ lies inside the triangle. The area of the sector is one third of the area of the triangle.',[
 part('Find $AB$ and the perpendicular distance from $O$ to $AB$.',r'$AB=13$ cm; distance $=60/13$ cm.',[r'$AB=\sqrt{12^2+5^2}=13$.',r'Equating $\tfrac12(12)(5)=\tfrac12(13)h$ gives $h=60/13$.'],scheme(('M1',1,'Uses Pythagoras and the triangle-area relation'),('A1',1,'Obtains both required lengths'))),
 part(r'Show that $r=\sqrt{40/\pi}$ and verify that the complete sector lies inside the triangle.',f'$r=\sqrt{{40/\pi}}={r:.3f}\ldots<60/13$.',[r'The triangle area is $30$, so the sector area is $10$.',r'$\tfrac12r^2(\pi/2)=10$, hence $r=\sqrt{40/\pi}$.',r'Since $r<60/13$ (and also $r<5$), the arc cannot cross $AB$ or either adjacent side.'],scheme(('M1',1,'Uses the one-third area condition'),('A1',1,'Obtains the exact radius'),('M1',1,'Compares with the perpendicular distance'),('A1',1,'Gives a complete containment justification'))),
 part('Find the perimeter of the part of the triangle outside the sector, giving your answer to 3 significant figures.',f'${prem:.3g}$ cm.',[r'$P=AB+(12-r)+(5-r)+r\pi/2$.',f'Substitution gives ${prem:.6f}\ldots$ cm.'],scheme(('M1',1,'Identifies all exposed straight sections and the arc'),('M1',1,'Forms the perimeter expression'),('A1',1,'Gives the perimeter'))),
 part('The radius is increased until the arc just touches $AB$. Find the percentage of the triangle area then occupied by the sector.',f'${pct:.3g}\%$.',[r'At the limiting position, the radius equals the perpendicular distance $60/13$.',f'Percentage $=100[\pi(60/13)^2/4]/30={pct:.6f}\ldots\%$.'],scheme(('M1',1,'Uses the altitude as the limiting radius'),('A1',1,'Obtains the percentage')))
 ],['内含证明','面积比例','极限位置'],'P1-2020-10-Q03','扇形与全等三角形组合：由面积反求角并求面积、周界',['设问角度','条件呈现','跨考点耦合','收尾要求'],'用面积和最短距离验证扇形是否真正位于三角形内','只比较r与两条直角边不能证明不穿过斜边；剩余区域的周界含新圆弧。'.split('；'),'加入最短距离的内含证明和“刚好相切”的极限情形',fig('triangle','A sector inside a right-angled triangle')))

# R25 retained metadata and precise schemes
q=old['P1-C07-R25'];q.pop('withdrawn',None);q.pop('withdrawalReason',None)
q.update(editorialRevision=14,solutionRevision=14,contentUpdatedAt='2026-10-24',difficultyPosition='略难于 P1-2022-01-Q05：同时处理半圆内两条弦、Thales直角和两块弓形的合并面积。',sourceSummary='半圆内弓形：证明角、求弓形面积和弦弧周界',adaptationDimensions=['情境与载体','求解目标','跨考点耦合','题目结构'],examEssence='半圆角、弦长半角公式和半圆减内接三角形',errorNotes=['CB对应的圆心角是π−0.8。','面积可整体做半圆减三角形，不必分别算两个弓形。'],designNote='把单个弓形扩展为半圆内相邻两弦，并要求识别Thales直角。',adaptationNote='改编维度：情境与载体、求解目标、跨考点耦合、题目结构。思维增量：两弦与Thales定理共同决定合并区域。')
q['parts'][0]['scheme']=scheme(('B1',1,'Uses the straight angle of a semicircle'),('A1',1,'Obtains π−0.8'))
q['parts'][1]['scheme']=scheme(('M1',1,'Uses chord=2r sin(central angle/2)'),('A1',1,'Obtains AC'),('A1',1,'Obtains CB'))
q['parts'][2]['scheme']=scheme(('M1',1,'Uses semicircle area minus triangle ACB'),('M1',1,'Finds the right-triangle area'),('A1',1,'Obtains 41.8 square units'))
Q.append(q)

# R27 retained metadata and precise schemes
q=old['P1-C07-R27'];q.pop('withdrawn',None);q.pop('withdrawalReason',None)
q.update(editorialRevision=14,solutionRevision=14,contentUpdatedAt='2026-10-24',difficultyPosition='略难于 P1-2022-01-Q05：由弧弦差逆向建立隐式方程，给根后再区分扇形和弓形。',sourceSummary='半圆内弓形：证明角、求弓形面积和弦弧周界',adaptationDimensions=['设问角度','条件呈现','题目结构','收尾要求'],examEssence='弧长与半角弦长共同建立圆心角方程',errorNotes=['弦长为2r sin(θ/2)，不是r sinθ。','第二问求的是扇形面积，第三问才扣除三角形。'],designNote='把已知角改成弧弦差约束；给出根以保持在P1考纲内。',adaptationNote='改编维度：设问角度、条件呈现、题目结构、收尾要求。思维增量：先建立不能直接求解的弧弦方程，再使用给根完成几何计算。')
q['parts'][0]['scheme']=scheme(('M1',1,'Uses arc 15θ and chord 30sin(θ/2)'),('A1',1,'Obtains θ−2sin(θ/2)=0.4'))
q['parts'][1]['scheme']=scheme(('M1',1,'Uses 1/2 r²θ with the supplied root'),('A1',1,'Obtains 244 m²'))
q['parts'][2]['scheme']=scheme(('M1',1,'Subtracts 1/2r²sinθ from the sector'),('M1',1,'Uses the unrounded supplied root'),('A1',1,'Obtains 151 m²'))
Q.append(q)

# R28 repeated blades with parameter classification
th=.6;gap=(2*math.pi-4*th)/4;boundary=4*(12*th+4*th+16);nmax=math.floor(2*math.pi/(th+.25));gap7=(2*math.pi-nmax*th)/nmax
Q.append(question('P1-C07-R28','重复环形叶片与最大数量',
 'A fan has four identical non-overlapping blades. Each blade is an annular sector with inner radius $4$ cm, outer radius $12$ cm and angle $\theta$ radians. The total area of the four blades is $153.6\text{ cm}^2$. The four gaps are equal.',[
 part('Show that $\theta=0.6$.',r'$\theta=0.6$ radians.',[r'Total blade area is $4[\tfrac12(12^2-4^2)\theta]=256\theta$.',r'$256\theta=153.6$, so $\theta=0.6$.'],scheme(('M1',1,'Forms the total annular-sector area'),('A1',1,'Shows θ=0.6'))),
 part('Find the angle of each gap to 3 significant figures.',f'${gap:.3g}$ radians.',[r'The blade and gap angles sum to one complete turn.',f'Each gap is $(2\pi-4(0.6))/4={gap:.6f}\ldots$.'],scheme(('M1',1,'Uses the complete angle 2π'),('A1',1,'Obtains the gap angle'))),
 part('Find the total length of all blade boundaries.',f'${boundary:.3g}$ cm.',[r'One blade has outer arc $12\theta$, inner arc $4\theta$ and two radial edges of length $8$.',r'For four blades the total is $4(16\theta+16)=102.4$ cm.'],scheme(('M1',1,'Builds one complete blade boundary'),('M1',1,'Accounts for four separate blades'),('A1',1,'Obtains 102.4 cm'))),
 part('A redesign uses the same blade angle but requires every equal gap to be at least $0.25$ radians. Find the greatest possible number of blades and the corresponding gap angle.',f'$7$ blades; gap $={gap7:.3g}$ radians.',[r'For $n$ blades, $n(0.6+0.25)\le2\pi$.',f'$n\le {2*math.pi/.85:.6f}\ldots$, so the greatest integer is $7$.',f'The equal gap is $(2\pi-7(0.6))/7={gap7:.6f}\ldots$ radians, which is at least $0.25$.'],scheme(('M1',1,'Forms the non-overlap inequality'),('A1',1,'Selects the greatest integer n=7'),('M1',1,'Finds the resulting equal gap'),('A1',1,'Checks the minimum-gap condition')))
 ],['重复扇区','整周约束','参数分类'],'P1-2022-06-Q08','多个相同扇形组成整体：证明弧长、求总周界和总面积',['设问角度','参数化与分类讨论','条件呈现','收尾要求'],'重复单元的面积、每个真实边界和2π整周限制','总周长要保留每片的两条径向边；最大数量必须取满足不等式的整数。'.split('；'),'由固定四片计算升级为带最小间隙的最大整数分类',fig('fan','Four annular-sector fan blades'),chapters=[7,2]))

# R30 adjacent arcs inverse
areaABC=12.5*(math.sin(.9)+math.sin(1.3)-math.sin(2.2)); AC=10*math.sin(1.1);height=2*areaABC/AC
Q.append(question('P1-C07-R30','相邻圆弧与内接三角形',
 'Points $A,B,C$ lie consecutively on a circle of radius $5$ cm with centre $O$. The minor arc $AC$ through $B$ has length $11$ cm, and the arc lengths $AB:BC=9:13$.',[
 part('Find $\angle AOB$ and $\angle BOC$.',r'$0.9$ radians and $1.3$ radians.',[r'The total angle is $11/5=2.2$ radians.',r'Divide $2.2$ in the ratio $9:13$ to obtain $0.9$ and $1.3$.'],scheme(('M1',1,'Converts total arc length to central angle'),('A1',1,'Divides in the correct ratio'))),
 part('Find $AB$, $BC$ and $AC$ in terms of sines.',r'$AB=10\sin0.45$, $BC=10\sin0.65$, $AC=10\sin1.1$.',[r'For a chord subtending angle $u$, chord length is $2r\sin(u/2)$.',r'Apply this to $0.9$, $1.3$ and $2.2$ radians.'],scheme(('M1',1,'Uses the half-angle chord formula'),('A1',1,'Obtains AB and BC'),('A1',1,'Obtains AC'))),
 part('Find the area of triangle $ABC$ to 3 significant figures.',f'${areaABC:.3g}\text{{ cm}}^2$.',[r'$[ABC]=[OAB]+[OBC]-[OAC]$.',f'$[ABC]=12.5(\sin0.9+\sin1.3-\sin2.2)={areaABC:.6f}\ldots$.'],scheme(('M1',1,'Uses the signed area decomposition'),('M1',1,'Uses all three central angles correctly'),('A1',1,'Gives the area'))),
 part('Find the perpendicular distance from $B$ to chord $AC$, giving your answer to 3 significant figures.',f'${height:.3g}$ cm.',[f'$AC=10\sin1.1={AC:.6f}\ldots$ cm.',f'Using $[ABC]=\tfrac12AC\,h$ gives $h=2({areaABC:.6f}\ldots)/AC={height:.6f}\ldots$ cm.'],scheme(('M1',1,'Uses triangle area with base AC'),('A1',1,'Obtains the perpendicular distance')))
 ],['弧长比','弦长','面积拆分'],'P1-2024-06-Q05','扇形与三角形：由角和边长求组合面积',['条件呈现','设问角度','跨考点耦合','收尾要求'],'弧长、圆心角、半角弦公式和有向面积拆分','AC使用总圆心角2.2；面积关系中OAC必须减去。'.split('；'),'先由总弧长和比例反求两个角，再以三角形高收尾',fig('arcs','Three consecutive points on a circle')))

# NEW R31 coordinate/radian coupling
C=(0,-2.5);theta=math.atan2(6,4.5);arc=12.5*theta;sector=.5*12.5**2*theta;tri=7.5;region=sector-tri;per=10+math.sqrt(40)+5+arc
Q.append(question('P1-C07-R31','坐标直线与扇形边界',
 'The line $l_1$ passes through $A(0,10)$ and $B(6,2)$. The line $l_2$ is perpendicular to $l_1$ at $B$ and meets the $y$-axis at $C$. A circle with centre $C$ passes through $A$. The ray $CB$ meets the circle at $D$, and $O$ is the origin.',[
 part('Find an equation of $l_2$ and the coordinates of $C$.',r'$l_2:y-2=\frac34(x-6)$; $C=(0,-5/2)$.',[r'The gradient of $l_1$ is $-8/6=-4/3$, so the perpendicular gradient is $3/4$.',r'$y-2=\tfrac34(x-6)$; at $x=0$, $y=-5/2$.'],scheme(('B1',1,'Finds the perpendicular gradient'),('M1',1,'Forms the line through B'),('A1',1,'Obtains C'))),
 part('Show that $CB=7.5$ and $CA=12.5$. Hence find $BD$.',r'$CB=7.5$, $CA=12.5$, $BD=5$.',[r'$CB=\sqrt{6^2+4.5^2}=7.5$ and $CA=10-(-2.5)=12.5$.',r'$CD=CA=12.5$, so $BD=CD-CB=5$.'],scheme(('M1',1,'Calculates both distances'),('A1',1,'Uses the radius to obtain BD'))),
 part('Find $\angle ACD$ and the length of arc $AD$, giving each to 3 significant figures.',f'$\angle ACD={theta:.3g}$ radians; arc $AD={arc:.3g}$.',[r'The angle from the positive vertical direction to $CB$ satisfies $\tan\theta=6/4.5$.',f'$\theta={theta:.6f}\ldots$ and arc $=12.5\theta={arc:.6f}\ldots$.'],scheme(('M1',1,'Builds the angle from the coordinate differences'),('A1',1,'Finds the angle'),('A1',1,'Finds the arc length'))),
 part('The region bounded by $OA$, $OB$, $BD$ and arc $DA$ is the sector $ACD$ with triangle $OCB$ removed. Find its area and perimeter to 3 significant figures.',f'Area $={region:.3g}$ square units; perimeter $={per:.3g}$ units.',[f'Sector area $=\tfrac12(12.5)^2({theta:.6f}\ldots)={sector:.6f}\ldots$.',r'Triangle $OCB$ has area $\tfrac12(2.5)(6)=7.5$.',f'Region area $={sector:.6f}\ldots-7.5={region:.6f}\ldots$.',f'Perimeter $=OA+OB+BD+\text{{arc}}=10+\sqrt{{40}}+5+{arc:.6f}\ldots={per:.6f}\ldots$.'],scheme(('M1',1,'Finds sector area'),('M1',1,'Subtracts triangle OCB'),('M1',1,'Builds the four-part boundary'),('A1',1,'Gives both requested values')))
 ],['坐标几何','垂线','扇形面积与周界'],'P1-2021-06-Q07','坐标直线与垂线构造圆半径，再求弧长和精确面积',['情境与载体','条件呈现','题目结构','跨考点耦合'],'坐标直线提供圆心、半径和角度，随后进入弧度几何','垂线斜率应为3/4；区域是扇形减三角形而不是相加。'.split('；'),'去掉真题中的部分坐标脚手架，并要求同时重建面积和四段边界',fig('coordinate','Coordinate construction of a sector'),chapters=[7,5]))

# NEW R32 inverse basic sector
Q.append(question('P1-C07-R32','单扇形双解与几何比较',
 'A sector has radius $r$ cm and angle $\theta$ radians, where $0<\theta<\pi$. Its area is $24\text{ cm}^2$ and its perimeter is $20$ cm.',[
 part(r'Show that $r^2-10r+24=0$.',r'$r^2-10r+24=0$.',[r'From the area, $\tfrac12r^2\theta=24$, so $r\theta=48/r$.',r'The perimeter condition gives $2r+48/r=20$; multiply by $r$ and divide by $2$.'],scheme(('M1',1,'Eliminates θ using the area condition'),('M1',1,'Uses the perimeter condition'),('A1',1,'Obtains the required quadratic'))),
 part('Hence find both possible pairs $(r,\theta)$.',r'$(4,3)$ and $(6,4/3)$.',[r'$(r-4)(r-6)=0$, so $r=4$ or $6$.',r'Using $\theta=48/r^2$ gives $3$ or $4/3$ radians; both satisfy $0<\theta<\pi$.'],scheme(('M1',1,'Solves the quadratic'),('A1',1,'Finds both angles and checks the range'))),
 part('For the two sectors, compare their arc lengths and chord lengths. State which sector has the longer chord.',r'Arc lengths are $12$ cm and $8$ cm; the $(r,\theta)=(4,3)$ sector also has the longer chord.',[r'Arc length is $r\theta$, giving $12$ and $8$.',r'Chord lengths are $8\sin1.5$ and $12\sin(2/3)$.',r'$8\sin1.5=7.98\ldots>12\sin(2/3)=7.42\ldots$.'],scheme(('M1',1,'Finds both arc lengths'),('M1',1,'Uses the half-angle chord formula for both'),('A1',1,'Makes the correct comparison')))
 ],['扇形双解','二次方程','弧弦比较'],'P1-2019-01-Q10','给定扇形面积和周界，建立二次方程并求两组半径与角',['题目结构','求解目标','收尾要求'],'面积和周界条件可能产生两组均有效的扇形','二次方程的两个正根都必须保留；较长的弧不应凭直觉判断弦也较长。'.split('；'),'保留双解套路，在末问加入弧长与弦长不单调对应的比较',fig('sector','A sector with unknown radius and angle'),chapters=[7,2],classic=True))

# NEW R33 annular two-solution design
Q.append(question('P1-C07-R33','环形扇区的两组设计',
 'An annular sector has inner radius $r$ cm, outer radius $2r$ cm and angle $\theta$ radians. Its area is $24\text{ cm}^2$ and its complete perimeter is $22$ cm.',[
 part(r'Show that $r^2-11r+24=0$.',r'$r^2-11r+24=0$.',[r'$24=\tfrac12(4r^2-r^2)\theta=\tfrac32r^2\theta$, so $r\theta=16/r$.',r'The two arcs total $3r\theta=48/r$ and the radial edges total $2r$.',r'$48/r+2r=22$ gives $r^2-11r+24=0$.'],scheme(('M1',1,'Uses the annular area'),('M1',1,'Builds the complete perimeter'),('A1',1,'Obtains the quadratic'))),
 part('Find both possible designs $(r,\theta)$.',r'$(3,16/9)$ and $(8,1/4)$.',[r'$(r-3)(r-8)=0$.',r'Using $\theta=16/r^2$ gives $16/9$ and $1/4$; both angles lie between $0$ and $\pi$.'],scheme(('M1',1,'Solves for both positive radii'),('A1',1,'Finds both angles'))),
 part('Determine which design has the longer outer arc and find the difference between the two outer arc lengths.',r'The $r=3$ design; difference $=20/3$ cm.',[r'Outer arc length is $2r\theta=32/r$.',r'The lengths are $32/3$ and $4$, so the first exceeds the second by $20/3$ cm.'],scheme(('M1',1,'Expresses the outer arc in terms of r'),('M1',1,'Evaluates both designs'),('A1',1,'Gives the correct design and exact difference'))),
 part('Explain why the design with the larger inner radius can nevertheless have the shorter outer arc.',r'Its angle is much smaller; arc length depends on the product radius × angle.',[r'The radius changes from $3$ to $8$, but the angle falls from $16/9$ to $1/4$.',r'The product $2r\theta$ therefore decreases.'],scheme(('B1',1,'Refers to the product rθ'),('B1',1,'Explains the competing changes correctly')))
 ],['环形扇区','二次方程','多解判断'],'P1-2023-10-Q09','环形扇区：由面积关系建立尺寸方程并求完整周界',['设问角度','参数化与分类讨论','求解目标','收尾要求'],'环形面积与完整边界共同产生两组有效设计','周界含两条弧和两条宽度；大半径不必对应大弧长。'.split('；'),'把单一尺寸改成双解参数问题，并要求解释反直觉的弧长比较',fig('annular','An annular sector with two possible designs'),chapters=[7,2]))

# NEW R34 repeated blade and filled gaps
theta=(2*math.pi-1.2)/6; bladearea=6*.5*(81)*theta; addarea=6*.5*81*math.sin(.2); totalarea=bladearea+addarea; outerper=6*9*theta+6*18*math.sin(.1)
Q.append(question('P1-C07-R34','重复扇形与填充间隙',
 'Six congruent sectors of radius $9$ cm are arranged around a common centre. Between each adjacent pair is an equal gap of angle $0.2$ radians. The sectors and gaps together make one complete turn.',[
 part(r'Show that the angle $\theta$ of each sector is $\dfrac{2\pi-1.2}{6}$ radians.',r'$\theta=(2\pi-1.2)/6$.',[r'Six sector angles and six gap angles sum to $2\pi$.',r'$6\theta+6(0.2)=2\pi$, giving the stated result.'],scheme(('M1',1,'Uses all six sectors and gaps'),('A1',1,'Obtains the stated exact angle'))),
 part('Find the total area of the six sectors to 3 significant figures.',f'${bladearea:.3g}\text{{ cm}}^2$.',[r'Total area is $6[\tfrac12(9)^2\theta]$.',f'Substitution gives ${bladearea:.6f}\ldots\text{{ cm}}^2$.'],scheme(('M1',1,'Forms the area of all six sectors'),('A1',1,'Gives the total area'))),
 part('Each gap is filled by the isosceles triangle formed by the two radii and the chord joining their endpoints. Find the new total area.',f'${totalarea:.3g}\text{{ cm}}^2$.',[r'One added triangle has area $\tfrac12(9)^2\sin0.2$.',f'Add six such triangles to the sector area: total $={totalarea:.6f}\ldots$.'],scheme(('M1',1,'Finds one gap-triangle area'),('M1',1,'Accounts for all six gaps'),('A1',1,'Gives the new total area'))),
 part('After filling the gaps, the outside boundary consists only of the six sector arcs and the six new chords. Find its length to 3 significant figures.',f'${outerper:.3g}$ cm.',[r'The six arcs total $6(9\theta)$.',r'Each gap chord is $18\sin0.1$, so the six chords total $108\sin0.1$.',f'The boundary length is ${outerper:.6f}\ldots$ cm.'],scheme(('M1',1,'Finds the total arc length'),('M1',1,'Uses the half-angle formula for all six chords'),('M1',1,'Excludes the now-internal radii'),('A1',1,'Gives the boundary length'))),
 part('Explain why the sum of the original six sector perimeters is not the perimeter found in part (c).',r'The twelve radii become internal edges when the pieces are joined; the six gap chords become the new exposed edges.',[r'Perimeters of separate pieces count edges that are no longer outside the completed design.',r'Only exposed arcs and chords belong to the final perimeter.'],scheme(('B1',1,'Identifies the internal radii'),('B1',1,'Identifies the new exposed chords')))
 ],['重复单元','弦长','真实外边界'],'P1-2022-06-Q08','多个相同扇形构成整体：弧长、总周界和总面积',['条件呈现','题目结构','跨考点耦合','收尾要求'],'整周角、重复面积和拼接后边界变化','六个间隙的总角是1.2而不是0.2；拼接后半径边不再属于外周界。'.split('；'),'加入用弦填充间隙，使面积和外周界都必须重新建模',fig('fan','Six sectors separated by equal gaps')))

# NEW R35 symmetric inverse area
alpha=(math.pi-1.6)/2;x=(50-.5*36*1.6)/(6*math.sin(alpha));side=math.sqrt(x*x+36-12*x*math.cos(alpha));per=2*side+9.6+2*x;tri_pct=100*(50-28.8)/50
Q.append(question('P1-C07-R35','由总面积反求侧边长度',
 'A stage consists of a sector $OBC$ of radius $6$ m and angle $1.6$ radians, joined to two congruent triangles $OAB$ and $OCD$. Points $A,O,D$ are collinear, $OA=OD=x$ m, and the total area is $50\text{ m}^2$.',[
 part(r'Show that $\angle AOB=\dfrac{\pi-1.6}{2}$.',r'$\angle AOB=(\pi-1.6)/2$.',[r'The three adjacent angles above the straight line are equal side angles with $1.6$ between them.',r'$2\angle AOB+1.6=\pi$.'],scheme(('M1',1,'Uses the straight-line angle sum'),('A1',1,'Obtains the exact expression'))),
 part('Use the area condition to find $x$ to 3 significant figures.',f'$x={x:.3g}$ m.',[r'The sector area is $\tfrac12(6)^2(1.6)=28.8$.',r'The two triangle areas total $2[\tfrac12(x)(6)\sin((\pi-1.6)/2)]$.',f'Set their sum equal to $50$ to obtain $x={x:.6f}\ldots$.'],scheme(('M1',1,'Separates sector and triangle areas'),('M1',1,'Forms the total-area equation'),('A1',1,'Finds x'))),
 part('Find the complete perimeter of the stage to 3 significant figures.',f'${per:.3g}$ m.',[r'By the cosine rule, $AB^2=x^2+6^2-12x\cos((\pi-1.6)/2)$.',f'Thus $AB=CD={side:.6f}\ldots$ m.',f'$P=2AB+6(1.6)+2x={per:.6f}\ldots$ m.'],scheme(('M1',1,'Uses the cosine rule for a sloping side'),('A1',1,'Finds the side length'),('M1',1,'Builds the outside boundary'),('A1',1,'Gives the perimeter'))),
 part('A design rule says that the two triangles together must contribute less than $45\%$ of the total area. Determine whether the rule is satisfied.',f'Yes; the triangles contribute ${tri_pct:.3g}\%$.',[r'The triangle area is $50-28.8=21.2$.',r'$100(21.2/50)=42.4\%<45\%$, so the rule is satisfied.'],scheme(('M1',1,'Finds the combined triangle contribution'),('A1',1,'Calculates the percentage'),('A1',1,'States the correct conclusion')))
 ],['反向面积条件','余弦定理','组合周界'],'P1-2020-10-Q03','扇形连接两个全等三角形：由面积反求角并求周界',['设问角度','条件呈现','求解目标','收尾要求'],'对称角关系、扇形与三角形面积及外周界','总面积条件只含一次x；外周界包含AD=2x但不含OB、OC。'.split('；'),'固定套路改为由整体面积反求侧边参数，并加入设计占比判断',fig('symmetric','Symmetric stage with unknown side length'),classic=True))

# NEW R36 partition and chord replacement
x=4*math.sqrt(3); inner=1.1*x; outer=13.2; pann=outer+inner+2*(12-x); red=inner-2*x*math.sin(.55)
Q.append(question('P1-C07-R36','分割扇形的边界优化',
 'A sector of radius $12$ cm and angle $1.1$ radians is divided by a concentric arc of radius $x$ cm. The outer annular part has twice the area of the inner sector.',[
 part(r'Show that $x=4\sqrt3$.',r'$x=4\sqrt3$ cm.',[r'$\tfrac12(144-x^2)(1.1)=2[\tfrac12x^2(1.1)]$.',r'Hence $x^2=48$ and the positive radius is $4\sqrt3$.'],scheme(('M1',1,'Forms the correct area-ratio equation'),('A1',1,'Obtains the exact radius'))),
 part('Find the sum of the lengths of the two circular arcs that bound the outer part.',f'${outer+inner:.3g}$ cm.',[r'The arc sum is $12(1.1)+x(1.1)=1.1(12+4\sqrt3)$.',f'This equals {outer+inner:.6f}\ldots cm.'],scheme(('M1',1,'Includes both the inner and outer arcs'),('A1',1,'Obtains the arc sum'))),
 part('Find the complete perimeter of the outer part to 3 significant figures.',f'${pann:.3g}$ cm.',[r'Add the two radial widths $2(12-x)$ to the two arcs.',f'$P=1.1(12+x)+2(12-x)={pann:.6f}\ldots$ cm.'],scheme(('M1',1,'Includes both radial widths'),('M1',1,'Forms the complete boundary'),('A1',1,'Gives the perimeter'))),
 part('The inner arc is replaced by its chord. Find the percentage reduction in the complete perimeter.',f'${100*red/pann:.3g}\%$.',[r'The chord length is $2x\sin(1.1/2)$.',f'The perimeter reduction is $x(1.1)-2x\sin0.55={red:.6f}\ldots$ cm.',f'Percentage reduction $=100({red:.6f}\ldots)/{pann:.6f}\ldots$.'],scheme(('M1',1,'Finds the replacement chord'),('M1',1,'Finds the reduction'),('A1',1,'Divides by the original complete perimeter'),('A1',1,'Gives the percentage')))
 ],['面积分割','双弧周界','百分比变化'],'P1-2024-10-Q05','扇形面积比例分割并逆求分割线长度',['题目结构','求解目标','跨考点耦合','收尾要求'],'同心面积比和环形区域的完整边界','外部区域被内弧围住，因此内弧必须计入；百分比以替换前完整周长为分母。'.split('；'),'在面积比例反求后加入完整周界与弧换弦的百分比优化',fig('partition','A sector divided into two regions')))

# Validate and save
byid={q['id']:q for q in Q}
def merge(qid,i,j,text):
    q=byid[qid];a,b=q['parts'][i],q['parts'][j]
    q['parts'][i]={'text':text,'answer':a['answer']+' '+b['answer'],'explanation':a['explanation']+'\n'+b['explanation'],
      'approach':a.get('approach',''),'solutionSteps':a['solutionSteps']+b['solutionSteps'],
      'scheme':a['scheme']+b['scheme'],'marks':a['marks']+b['marks']}
    q['parts'].pop(j);q['marks']=sum(p['marks'] for p in q['parts'])
merge('P1-C07-R08',2,3,'Find the perimeter of the combined region to 3 significant figures. The curved segment is then removed by cutting along $AB$. Find the percentage of the original area that is removed.')
merge('P1-C07-R13',2,3,'Find the total area and the perimeter of the platform, giving each to 3 significant figures. State which given length is not part of the outside boundary.')
merge('P1-C07-R20',3,4,'Find the total perimeter of the sign to 3 significant figures. A display rule requires area/perimeter to exceed $0.95$ m. Determine whether the sign satisfies the rule.')
merge('P1-C07-R21',2,3,r'Show that the difference between the perimeters of $T$ and $S$ is $18(\pi-\theta)$, and find this difference. Hence determine whether the area ratio $T:S$ is greater than the perimeter ratio $P_T:P_S$.')
merge('P1-C07-R23',2,3,'The inner arc $CD$ is replaced by its chord. Find the reduction in the perimeter of the outer region to 3 significant figures and state, with a reason, whether this changes the original area ratio.')
merge('P1-C07-R24',2,3,'Find the perimeter of the part of the triangle outside the sector. The radius is then increased until the arc just touches $AB$. Find the percentage of the triangle area then occupied by the sector.')
merge('P1-C07-R28',0,1,r'Show that $\theta=0.6$ and hence find the angle of each gap to 3 significant figures.')
merge('P1-C07-R30',2,3,'Find the area of triangle $ABC$ and hence the perpendicular distance from $B$ to chord $AC$, giving each answer to 3 significant figures.')
merge('P1-C07-R33',2,3,'Determine which design has the longer outer arc and find the difference between the two outer arc lengths. Explain why the design with the larger inner radius can nevertheless have the shorter outer arc.')
merge('P1-C07-R34',1,2,'Find the total area of the six sectors. Each gap is then filled by the isosceles triangle formed by the two radii and the chord joining their endpoints. Find the new total area, giving both answers to 3 significant figures.')
merge('P1-C07-R36',1,2,'Find the sum of the two circular arc lengths and hence the complete perimeter of the outer part, giving each to 3 significant figures.')
def clean_controls(value):
    if isinstance(value,str):
        return value.translate({7:r'\a',8:r'\b',9:r'\t',11:r'\v',12:r'\f',13:r'\r'})
    if isinstance(value,list): return [clean_controls(v) for v in value]
    if isinstance(value,dict): return {k:clean_controls(v) for k,v in value.items()}
    return value
Q=clean_controls(Q)
for q in Q:
    # This is the Radians chapter bank. Cross-topic coupling is documented in
    # topics/metadata without making the chapter filter hide its own questions.
    q['chapters']=[7]
assert len(Q)==23
ids=[q['id'] for q in Q];assert len(set(ids))==23
for q in Q:
 assert sum(p['marks'] for p in q['parts'])==q['marks']
 for p in q['parts']:
  assert sum(s['marks'] for s in p['scheme'])==p['marks']
 assert len(q.get('adaptationDimensions',[]))>=3
 assert q['sourceReferences']
# source max three
from collections import Counter
c=Counter(q['sourceReferences'][0]['questionId'] for q in Q)
assert max(c.values())<=3,c
out=ROOT/'editorial/v14/p1-radians.json';out.write_text(json.dumps({'version':14,'questions':Q},ensure_ascii=False,indent=2)+'\n')
print('wrote',len(Q),'active questions; source max',max(c.values()),dict(c))
