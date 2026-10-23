"""Individually authored revisions. No number-substitution template generation."""
from pathlib import Path
import json,math,re,hashlib,copy,subprocess
ROOT=Path(__file__).resolve().parents[2]
bank=json.loads(subprocess.check_output(['git','show','1224b7b9d7d8061b5249e36bde9b27f5d23279b4:dist/data/bank.json'],cwd=ROOT,text=True));before=copy.deepcopy(bank);byid={q['id']:q for q in bank['questions']};changes={}
def part(text,answer,steps,scheme):
 return dict(text=text,answer=answer,explanation='\n'.join(steps),approach=steps[0],solutionSteps=steps,scheme=[dict(code=c,marks=int(c[1:]),text=t) for c,t in scheme],marks=sum(int(c[1:]) for c,t in scheme))
def revise(id,typ,stem,parts,topics,chapters=None,ref=None,book=None,answerFigure=''):
 q=byid[id];old=copy.deepcopy(q);q.update(type=typ,stem=stem,parts=parts,marks=sum(p['marks'] for p in parts),topics=topics,chapters=chapters or [int(id[4:6])],editorialRevision=12,solutionRevision=12,answerFigure=answerFigure,contentUpdatedAt='2026-10-23')
 if book:
  q.update(origin='textbook-selected',textbookSource=book,sourceReferences=[],adaptationNote='经筛选的用户提供教材原题；题文与原有分值保留，配图重绘，中文解答和评分点由本站编写。')
 else:
  q.update(origin='original-reviewed-2026',adaptationNote='2026-10-23逐题重写：'+typ+'。重新设计条件、设问和分值；非考试原题。')
  if ref:q['sourceReferences']=[dict(questionId=ref,year=int(ref[3:7]),note=typ)]
 q.pop('textbookSource',None) if not book else None
 changes[id]=dict(kind='textbook-selection' if book else 'individual-rewrite',reason=typ,before=old)
 return q
def fig(body,desc):return '<figure class="rewrite-figure"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 290" role="img" aria-label="'+desc+'"><title>'+desc+'</title><g fill="none" stroke="#222" stroke-width="1.6">'+body+'</g></svg><figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'
def txt(x,y,t):return f'<text x="{x}" y="{y}" fill="#222" stroke="none" font-family="Georgia,serif" font-size="16">{t}</text>'
def plot(fn,xmin,xmax,ymin,ymax,xticks=(),yticks=(),label='C',extra=None):
 X=lambda x:48+(x-xmin)/(xmax-xmin)*438;Y=lambda y:245-(y-ymin)/(ymax-ymin)*210
 ox=X(0) if xmin<=0<=xmax else 48;oy=Y(0) if ymin<=0<=ymax else 245
 body=f'<path d="M40 {oy}H506 M{ox} 254V20"/>'+txt(511,oy+5,'x')+txt(ox+8,20,'y')
 for x,l in xticks:body+=f'<path d="M{X(x)} {oy-4}v8"/>'+txt(round(X(x)-9,1),round(oy+22,1),l)
 for y,l in yticks:body+=f'<path d="M{ox-4} {Y(y)}h8"/>'+txt(round(ox-31,1),round(Y(y)+5,1),l)
 for k,f in enumerate([fn]+([extra] if extra else [])):
  pieces=[];cur=[];last=None
  for i in range(801):
   x=xmin+(xmax-xmin)*i/800
   try:y=f(x)
   except:y=float('nan')
   if not math.isfinite(y) or y<ymin or y>ymax or last is not None and abs(y-last)>(ymax-ymin)*.3:
    if len(cur)>1:pieces.append(cur)
    cur=[];last=None;continue
   cur.append(f'{X(x):.2f},{Y(y):.2f}');last=y
  if len(cur)>1:pieces.append(cur)
  for points in pieces:body+='<polyline points="'+' '.join(points)+'"'+(' stroke-dasharray="6 4"' if k else '')+'/>'
 body+=txt(425,25,label)
 return fig(body,'Coordinate sketch of the supplied curve'+(' and dashed reference line' if extra else ''))
def source(unit,page,exercise,number,marker,pdfpage):return dict(unit=unit,page=page,exercise=exercise,question=number,marker=marker,pdfPage=pdfpage,pdf='assets/'+unit.lower()+'.pdf')
# P1 trigonometric graphs: unknown parameters, symmetry, end points and root counting.
revise('P1-C06-R11','三角图像参数与区间交点',r'The curve $C$ has equation $y=a\cos(bx)+c$, where $a,b>0$ and $x$ is measured in degrees. Its maximum value is 7 and its minimum value is $-1$. Consecutive maxima occur at $x=0$ and $x=240$.',[
 part(r'Find $a$, $b$ and $c$.',r'$a=4,\ b=3/2,\ c=3$.',[r'振幅为极差的一半，中心线为最大值与最小值的平均值。',r'$a=(7-(-1))/2=4,\ c=(7+(-1))/2=3$。',r'周期为$240^\circ$，所以$b=360/240=3/2$。'],[('B1','振幅4及中心线3'),('M1',r'使用周期$360/b=240$'),('A1',r'$b=3/2$')]),
 part(r'State the number of distinct intersections of $C$ with $y=k$ in $0\le x\le480$ in each case: (i) $-1<k<7$, (ii) $k=7$, (iii) $k=-1$.',r'(i) 4; (ii) 3; (iii) 2.',[r'区间恰含两个完整周期。中间高度每周期穿过两次；端点必须按同一横坐标只计一次。',r'最大点在$x=0,240,480$，最小点在$x=120,360$。'],[('B1','中间高度4个交点'),('B1','最大高度3个交点，含两个端点'),('B1','最小高度2个交点')])],['三角图像参数','周期','交点个数'],ref='P1-2021-10-Q05')
revise('P1-C06-R14','正切图像与斜直线交点',r'The curves $C:y=\tan x$ and $l:y=2x$ are considered for $-\pi<x<\pi$. Angles are measured in radians. On the central branch the line $l$ crosses $C$ at three points. On every complete outer branch there is one intersection.',[
 part(r'Sketch $C$ and $l$ on the same axes in this interval, marking the vertical asymptotes of $C$ and all points where $C$ meets the $x$-axis. Do not calculate the non-zero intersections.',r'渐近线$x=\pm\pi/2$，零点$(0,0)$；中央支与直线相交3次，两侧截断支各无交点。',[r'先画周期为$\pi$的正切图像，再画过原点的斜直线。',r'中央支由下方穿过直线、在原点穿回、再穿过一次。两侧剩余半支与$2x$异号。'],[('B1',r'正切三支形状及渐近线$\pm\pi/2$'),('B1','原点和直线位置正确'),('B1','中央3个交点，外侧半支不相交')]),
 part(r'Using the same graphs and periodicity, state the number of distinct roots of $\tan x=2x$ in (i) $-3\pi<x<3\pi$, (ii) $-20\pi<x<20\pi$.',r'(i) 7; (ii) 41.',[r'中央支贡献3根；除中央支外，每个完整支贡献1根。两端截断半支均不贡献根。',r'$(-N\pi,N\pi)$内共有$2N-2$个完整外支，因此根数为$3+(2N-2)=2N+1$。'],[('B1','第一问7根'),('B1','第二问41根')])],['正切图像','区间交点计数'],ref='P1-2023-01-Q09',answerFigure=plot(math.tan,-math.pi,math.pi,-5,5,[(-math.pi,'−π'),(-math.pi/2,'−π/2'),(math.pi/2,'π/2'),(math.pi,'π')],label='y = tan x',extra=lambda x:2*x))
revise('P1-C06-R15','有限区间的余弦交点计数',r'The curve $C$ has equation $y=\cos(2x)$ for $0\le x\le270$, where $x$ is measured in degrees.',[
 part(r'Sketch $C$, showing the coordinates of all maximum and minimum points and all intersections with the $x$-axis.',r'最大点$(0,1),(180,1)$；最小点$(90,-1),(270,-1)$；零点$x=45,135,225$。',[r'周期为$180^\circ$，该区间含一个半周期。',r'每半周期端点依次为最大、最小、最大、最小，零点在其间。'],[('B1','一个半周期形状正确'),('B1','极值点完整'),('B1','零点完整')]),
 part(r'Find the set of values of $k$ for which $\cos(2x)=k$ has exactly three distinct solutions in this interval.',r'$-1<k<1$.',[r'水平线在最大值与最小值之间时，每一段单调半周期恰有一次相交。',r'$k=1$或$-1$均只有两个交点；范围外没有交点。'],[('M1','正确考虑水平线及端点例外'),('A1',r'$-1<k<1$')])],['草图','交点个数','端点'],ref='P1-2021-10-Q05',answerFigure=plot(lambda x:math.cos(math.radians(2*x)),0,270,-1.4,1.4,[(90,'90°'),(180,'180°'),(270,'270°')],[(-1,'−1'),(1,'1')]))
# Selected original textbook questions, preserving their authentic E/P markers and marks.
revise('P1-C06-R13','教材E/P：相位与非唯一参数',r'The graph shows the curve with equation $y=\sin(x+k)$, $-360^\circ\le x\le360^\circ$, where $k$ is a constant.'+plot(lambda x:math.sin(math.radians(x+60)),-360,360,-1.3,1.3,[(-240,'−240°'),(-60,'−60°'),(120,'120°'),(300,'300°')],[(-1,'−1'),(1,'1')],label='y = sin(x + k)'),[
 part(r'Find one possible value for $k$.',r'$k=60^\circ$.',[r'图像在$x=-60^\circ$向上穿过横轴，因此可取$x+k=0$。',r'$-60+k=0$，得$k=60^\circ$。'],[('M1','识别向上穿过零点的位置'),('A1',r'$60^\circ$或任一等价值')]),
 part(r'Is there more than one possible answer to part (a)? Give a reason for your answer.',r'是；$k=60^\circ+360^\circ n,\ n\in\mathbb Z$.',[r'正弦函数的周期为$360^\circ$。',r'在相位上加任意整数个周期不会改变图像。'],[('B1','说明不唯一'),('B1','用周期解释并给出等价参数')])],['相位','周期','图像识别'],book=source('P1',129,'6G',8,'E/P',140))
revise('P1-C06-R16','教材E：余弦平移的截距',r'The graph shows the curve $y=\cos(x+30^\circ)$, $-360^\circ\le x\le360^\circ$.'+plot(lambda x:math.cos(math.radians(x+30)),-360,360,-1.3,1.3,[(-270,'−270°'),(-90,'−90°'),(90,'90°'),(270,'270°')],[(-1,'−1'),(1,'1')],label='C'),[
 part(r'Write down the coordinates of the points where the curve crosses the $x$-axis.',r'$(-300,0),(-120,0),(60,0),(240,0)$.',[r'余弦为零时$x+30=90+180n$，因此$x=60+180n$。',r'只保留给定区间内四个横坐标，并写成坐标对。'],[('B1','找到四个正确横坐标，允许一个遗漏'),('B1','全部坐标正确且无多余值')]),
 part(r'Find the coordinates of the point where the curve crosses the $y$-axis.',r'$(0,\sqrt3/2)$.',[r'令$x=0$，$y=\cos30^\circ=\sqrt3/2$。'],[('B1',r'$(0,\sqrt3/2)$')])],['余弦图像','平移','截距'],book=source('P1',129,'6G',7,'E',140))
revise('P1-C06-R23','教材E/P：坐标几何与三角面积',r'The three points $A$, $B$ and $C$, with coordinates $A(0,1)$, $B(3,4)$ and $C(1,3)$ respectively, are joined to form a triangle.',[
 part(r'Show that $\cos\angle ACB=-\frac45$.',r'$-4/5$.',[r'先计算三条边的平方：$AC^2=5,\ BC^2=5,\ AB^2=18$。',r'余弦定理给出$\cos C=(5+5-18)/(2\sqrt5\sqrt5)=-4/5$。'],[('M1','用坐标距离公式求边长平方'),('A1','5、5、18全部正确'),('M1','余弦定理中使用对边AB'),('A1','分母10，分子−8'),('A1',r'得到$-4/5$，推导清楚')]),
 part(r'Calculate the area of $\triangle ABC$.',r'$3\text{ units}^2$.',[r'内角$C$位于$(0,180^\circ)$，所以$\sin C=\sqrt{1-16/25}=3/5$。',r'面积$=\frac12\sqrt5\sqrt5(3/5)=3$。'],[('M1',r'面积公式及$\sin C=3/5$'),('A1','面积3')])],['坐标距离','余弦定理','三角形面积'],chapters=[6,5],book=source('P1',130,'Chapter review 6',7,'E/P',141))
revise('P1-C06-R28','教材E/P：水深模型与草图',r'The variation in the depth of water in a rock pool can be modelled using the function $y=\sin(30t)$, where $t$ is the time in hours and $0\le t\le6$. Angles are measured in degrees.',[
 part(r'Sketch the function for the given interval.',r'通过$(0,0),(3,1),(6,0)$的正弦半波。',[r'自变量角$30t$从$0^\circ$变化到$180^\circ$。',r'$t=3$时达到最大值1，两个端点均为零。'],[('B1','正弦半波形状及端点正确'),('B1','峰值$(3,1)$正确')]),
 part(r'If $t=0$ represents midday, during what times will the rock pool be at least half full?',r'下午1时至下午5时，含两个时刻。',[r'在这一模型中，半满对应$y\ge1/2$。',r'$30^\circ\le30t\le150^\circ$，即$1\le t\le5$。',r'从中午12时起算，得到13:00至17:00。'],[('M1','以水平线1/2确定两次相交'),('A1',r'$1\le t\le5$'),('A1','正确转成时钟时间且含端点')])],['正弦草图','模型','区间'],book=source('P1',129,'6G',9,'E/P',140),answerFigure=plot(lambda t:math.sin(math.radians(30*t)),0,6,-.2,1.3,[(3,'3'),(6,'6')],[(1,'1')],label='water-depth model'))
revise('P1-C06-R18','正切与倒数曲线的区间交点',r'The curve $C$ has equation $y=\tan x$ and the curve $D$ has equation $y=\frac1x$, where angles are measured in radians.',[
 part(r'On the same axes, sketch $C$ and $D$ for $-\pi\le x\le\pi$, omitting points at which a function is undefined. State the number of intersections.',r'交点2个，分别位于$(-\pi/2,0)$及$(0,\pi/2)$。',[r'正切在中央支单调增加，倒数在每一侧单调减少。',r'正半中央支从0增至无穷，倒数从无穷降至正数，恰交一次；负半由对称性也交一次。',r'外侧半支中两个函数异号，没有交点。'],[('B1','两条曲线形状及渐近线正确'),('B1','两个交点及其所在半支正确'),('B1','用符号或单调性说明没有其他交点')]),
 part(r'Using the same graphs and periodicity, state the number of solutions of $\tan x=\frac1x$ in (i) $0<x<5\pi$, (ii) $-4\pi<x<3\pi$.',r'(i) 5; (ii) 7.',[r'正区间每段$(n\pi,n\pi+\pi/2)$恰有一根，负区间关于原点对应。',r'第一问5个正根；第二问4个负根与3个正根。$x=0$不在定义域。'],[('B1','5个根'),('B1','7个根且不计0')])],['正切图像','倒数图像','交点计数'],chapters=[6,4],ref='P1-2021-06-Q09')
revise('P1-C06-R24','三角函数对称关系与横向伸缩',r'It is given that $\sin\alpha=p$, where $0^\circ<\alpha<90^\circ$.',[
 part(r'Write down, in terms of $p$, (i) $2\sin(180^\circ-\alpha)$, (ii) $\sin(180^\circ+\alpha)$, (iii) $3-\sin(-\alpha)$.',r'(i) $2p$; (ii) $-p$; (iii) $3+p$.',[r'利用正弦图像关于$90^\circ$对称、半周期变号及关于原点对称。',r'$\sin(180-\alpha)=p,\ \sin(180+\alpha)=-p,\ \sin(-\alpha)=-p$。'],[('B1',r'$2p$'),('B1',r'$-p$'),('B1',r'$3+p$')]),
 part(r'Sketch $y=\sin(2x)$ for $0^\circ\le x\le180^\circ$. Hence find, in terms of $\alpha$, the $x$ coordinates of all intersections with $y=p$ in this interval.',r'$x=\alpha/2,\ 90^\circ-\alpha/2$.',[r'横向压缩后，一个完整周期为$180^\circ$。',r'一个周期内$2x=\alpha$或$180^\circ-\alpha$，分别除以2。'],[('B1','完整正弦周期，零点0、90、180及极值位置正确'),('M1','两个正确的角关系'),('A1','两个横坐标正确且无其他解')])],['正弦对称','草图','横向伸缩'],ref='P1-2022-06-Q09')
# Radians: composite boundaries and inverse design, rather than repeated s=r theta drills.
revise('P1-C07-R01','扇形与两侧三角形的舞台设计',r'A stage consists of a sector $OBC$ and two congruent triangles $OAB$ and $OCD$. The points $A,O,D$ lie on a straight line in that order. The triangles are on the opposite side of their common radii from the interior of the sector. The radius of the sector is 5 m, $\angle BOC=2$ radians, and $OA=OD=4$ m. The stage boundary is $AB$, arc $BC$, $CD$ and the straight line $DA$.',[
 part(r'Show that $\angle AOB=\frac{\pi-2}{2}$ radians and calculate the length $AB$, in metres, to 3 significant figures.',r'$\angle AOB=(\pi-2)/2;\quad AB=2.71\text{ m}$ (3 s.f.).',[r'直线上方三个角的和为$\pi$，两侧角相等，故每个侧角为$(\pi-2)/2$。',r'余弦定理：$AB^2=4^2+5^2-2(4)(5)\cos((\pi-2)/2)$。',r'计算得到$AB=2.709457\ldots$。'],[('B1','侧角关系正确'),('M1','余弦定理正确代入'),('A1','长度正确，3位有效数字')]),
 part(r'Find the total area and the total perimeter of the stage, giving each answer to 3 significant figures.',r'面积$35.8\text{ m}^2$；周长$23.4\text{ m}$.',[r'扇形面积为$\frac12(5^2)(2)=25$；两个三角形总面积为$2\cdot\frac12(4)(5)\sin((\pi-2)/2)$。',r'总面积$=35.806\ldots$。',r'外边界不含内部半径：周长$=2AB+5(2)+8=23.418915\ldots$。'],[('M1','扇形与两个三角形面积相加'),('A1','面积35.8及单位'),('M1','周长只计外边界'),('A1','周长23.4及单位')])],['弧度制','组合图形','外周界'],chapters=[7,6],ref='P1-2023-01-Q06')
revise('P1-C07-R02','环形扇区的反向尺寸设计',r'A curved planting bed is an annular sector with centre $O$, inner radius 4 m and outer radius $(4+x)$ m, where $x>0$. The inner arc has length 3 m and the area of the bed is $30\text{ m}^2$.',[
 part(r'Show that $x^2+8x-80=0$. Hence find $x$.',r'$x=-4+4\sqrt6=5.7979\ldots\text{ m}$.',[r'先用内弧求中心角：$\theta=3/4$。',r'$\frac12[(4+x)^2-4^2](3/4)=30$，整理为$x^2+8x-80=0$。',r'两个根为$-4\pm4\sqrt6$，因$x>0$只保留正根。'],[('B1',r'$\theta=3/4$'),('M1','两扇形面积相减'),('A1','二次式正确'),('M1','解二次式并筛选'),('A1','正根正确')]),
 part(r'Find the total perimeter of the bed, giving your answer in metres to 3 significant figures.',r'$21.9\text{ m}$.',[r'外弧为$(4+x)(3/4)$，另外有内弧3及两条径向边$x$。',r'$P=3+(4+x)(3/4)+2x=6+11x/4=21.944\ldots$。'],[('M1','包括内外弧与两条直边'),('A1','21.9 m')])],['环形扇区','面积反求','二次方程'],chapters=[7,2],ref='P1-2023-10-Q09')
revise('P1-C07-R08','矩形切除圆弓形的组合区域',r'A circle has centre $O$ and radius 10 cm. A chord $AB$ of length 12 cm cuts off a minor segment. A rectangle of width 12 cm and height 4 cm is attached to $AB$ on the opposite side from the minor segment. The outside boundary consists of the minor arc $AB$ and the other three sides of the rectangle.',[
 part(r'Show that the angle subtended by the minor arc at $O$ is $1.287$ radians, to 4 significant figures.',r'$\theta=2\arcsin(3/5)=1.287002\ldots$.',[r'将等腰三角形$OAB$平分，半弦为6、斜边为10。',r'$\sin(\theta/2)=6/10$，因此$\theta=2\arcsin(0.6)$。'],[('M1','使用半弦与半角关系'),('A1','1.287 radians')]),
 part(r'Calculate the total area and perimeter of the combined region, giving your answers to 3 significant figures.',r'面积$64.4\text{ cm}^2$；周长$32.9\text{ cm}$.',[r'中心到弦距离为$\sqrt{10^2-6^2}=8$，三角形面积为$\frac12(12)(8)=48$。',r'组合面积$=12(4)+50\theta-48=50\theta=64.350\ldots$。',r'周长$=10\theta+12+2(4)=32.870\ldots$。'],[('M1','矩形加扇形减三角形'),('A1','面积64.4及单位'),('M1','弧加其余三条直边'),('A1','周长32.9及单位')])],['圆弓形','组合面积','周界'],chapters=[7,6],ref='P1-2020-01-Q04')
revise('P1-C07-R10','等面积扇形的周界约束',r'Two minor sectors have the same area. Sector $S$ has radius 6 cm and angle $\theta$ radians. Sector $T$ has radius 9 cm and angle $\phi$ radians. The perimeter of $T$ is 4 cm greater than the perimeter of $S$.',[
 part(r'Find the exact values of $\theta$ and $\phi$.',r'$\theta=1,\quad\phi=4/9$.',[r'相同面积给出$36\theta=81\phi$，所以$\phi=4\theta/9$。',r'周界关系为$18+9\phi=12+6\theta+4$。',r'代入得$2=2\theta$，因此$\theta=1,\phi=4/9$。'],[('M1','面积关系正确'),('M1','周长关系正确'),('A1','两个精确角均正确')]),
 part(r'Find the ratio of the area of the minor segment in $S$ to the area of the minor segment in $T$, giving your answer in the form $k:1$, where $k$ is correct to 3 significant figures.',r'$4.86:1$.',[r'圆弓形面积为$\frac12 r^2(\text{中心角}-\sin\text{中心角})$。',r'$A_S=18(1-\sin1)$，$A_T=\frac{81}{2}(4/9-\sin(4/9))$。',r'取比值得$4.863124\ldots:1$。'],[('M1','分别建立两弓形面积'),('A1','正确计算比值及精度')])],['等面积','联立条件','圆弓形比'],ref='P1-2022-01-Q05')
revise('P1-C07-R12','教材P：圆弧边截面的面积',r'The cross-section $ABCD$ of a glass prism has $AD=BC=4$ cm, with both $AD$ and $BC$ at right angles to $DC$. The curve $AB$ is the minor arc of a circle, centre $O$ and radius 6 cm. The points $A$ and $B$ are the upper and lower endpoints of the arc, and the arc bulges towards $DC$. It is given that $\angle AOB=2\theta$ radians and the perimeter of the cross-section is $2(7+\pi)$ cm.',[
 part(r'Show that $2\theta+2\sin\theta-1=\frac\pi3$.',r'$12\theta+12\sin\theta+8=14+2\pi$.',[r'弧长$AB=6(2\theta)=12\theta$。',r'弦长$AB=12\sin\theta$，等于$DC$。',r'周长$12\theta+12\sin\theta+8=14+2\pi$，除以6整理。'],[('M1','弧长与弦长正确'),('M1','正确周界方程'),('A1','得到指定等式')]),
 part(r'Verify that $\theta=\frac\pi6$.',r'$2(\pi/6)+2(1/2)-1=\pi/3$.',[r'直接代入$\theta=\pi/6$，使用$\sin(\pi/6)=1/2$。'],[('B1','准确代入验证')]),
 part(r'Find the area of the cross-section.',r'$24-6\pi+9\sqrt3\text{ cm}^2$.',[r'矩形的面积为$4\cdot12\sin(\pi/6)=24$。',r'弓形面积为扇形减三角形：$\frac12(6^2)(\pi/3-\sin(\pi/3))=6\pi-9\sqrt3$。',r'弧向矩形内部凸出，所以截面为矩形减去该弓形。'],[('M1','矩形面积24'),('M1','弓形面积正确'),('A1','正确相减及精确答案')])],['弧度制','弦长','组合边界'],book=source('P1',147,'Chapter review 7',12,'P',158))
revise('P1-C07-R14','教材E/P：扇形半径证明与弓形',r'The diagram shows the sector $OAB$ of a circle of radius $r$ cm. The area of the sector is $15\text{ cm}^2$ and $\angle AOB=1.5$ radians. The segment $R$ is enclosed by arc $AB$ and the straight line $AB$.',[
 part(r'Prove that $r=2\sqrt5$.',r'$r^2=20,\ r=2\sqrt5$.',[r'$\frac12r^2(1.5)=15$，所以$r^2=20$。',r'半径为正，故$r=2\sqrt5$。'],[('M1','正确建立扇形面积方程'),('A1','取正根并得精确结果')]),
 part(r'Find, in cm, the perimeter of the sector $OAB$.',r'$7\sqrt5\text{ cm}$.',[r'弧长为$1.5r=3\sqrt5$，两条直边总长$2r=4\sqrt5$。',r'总周长为$7\sqrt5$。'],[('M1','求出弧长'),('M1','加两条半径'),('A1','精确周长及单位')]),
 part(r'Calculate, to 3 decimal places, the area of $R$.',r'$5.025\text{ cm}^2$.',[r'用扇形面积减去两半径与弦构成的三角形面积：$A_R=15-\frac12(20)\sin1.5=15-10\sin1.5$。',r'计算器使用弧度制，得$5.025050\ldots$。'],[('M1','扇形减三角形面积'),('A1','5.025及单位')])],['扇形面积反求','精确值','圆弓形'],book=source('P1',147,'Chapter review 7',9,'E/P',158))
revise('P1-C07-R18','教材P：等半径两圆重叠区域',r'Two circles $C_1$ and $C_2$, both of radius 12 cm, have centres $O_1$ and $O_2$ respectively. $O_1$ lies on the circumference of $C_2$; $O_2$ lies on the circumference of $C_1$. The circles intersect at $A$ and $B$ and enclose the common region $R$.',[
 part(r'Show that $\angle AO_1B=\frac{2\pi}{3}$.',r'$2\pi/3$.',[r'$O_1O_2=O_1A=O_2A=12$，上方三角形为等边三角形，下方同理。',r'中心角由两个$\pi/3$组成，所以为$2\pi/3$。'],[('M1','识别两个等边三角形'),('A1','中心角证明完整')]),
 part(r'Hence write down, in terms of $\pi$, the perimeter of $R$.',r'$16\pi\text{ cm}$.',[r'公共区域边界是两条半径12、中心角$2\pi/3$的弧。',r'$P=2(12)(2\pi/3)=16\pi$。'],[('B1',r'$16\pi$及单位')]),
 part(r'Find the area of $R$, giving your answer to 3 significant figures.',r'$177\text{ cm}^2$.',[r'两个相同弓形构成公共区域。',r'$A=2\cdot\frac12(12^2)(2\pi/3-\sin(2\pi/3))=96\pi-72\sqrt3$。',r'$A=176.884\ldots$，取3位有效数字为177。'],[('M1','两个扇形减去两个三角形'),('A1','精确式正确'),('A1','177及单位')])],['重叠圆','圆弓形','周界'],book=source('P1',147,'Chapter review 7',13,'P',158))
# P2: substantial complete interval-solving questions.
revise('P2-C06-R07','复合角区间与全部解',r'In this question you must show all stages of your working. Angles are measured in degrees.',[
 part(r'Solve $4\sin(3x-20^\circ)=\sqrt3$ for $-60^\circ<x\le180^\circ$, giving your answers to one decimal place.',r'$x=-44.8^\circ,15.2^\circ,58.1^\circ,135.2^\circ,178.1^\circ$.',[r'设$u=3x-20^\circ$，区间变为$-200^\circ<u\le520^\circ$。',r'参考角$\alpha=\arcsin(\sqrt3/4)=25.6589\ldots^\circ$。',r'$u=\alpha+360n$或$180-\alpha+360n$。区间内为$-205.659$不符合，保留$-180-\alpha=-205.659$也不符合；应逐支列举符合的角。',r'符合的$u$为$-180-\alpha$不符合下界，$\alpha,180-\alpha,360+\alpha,540-\alpha$。另一个负解为$\alpha-360$不符合。因此仅4解：$x=15.2,58.1,135.2,178.1$。'],[('M1','正确变换区间'),('M1','建立正弦两支周期通解'),('A1','所有符合区间的角正确'),('A1','最终四个x正确、无多余值')]),
 part(r'Hence, or otherwise, find the smallest positive solution of $4\sin(6t+10^\circ)=\sqrt3$.',r'$t=2.6^\circ$ (1 d.p.).',[r'最小正$t$使$6t+10$达到第一个正参考角$25.6589\ldots$。',r'$t=(25.6589\ldots-10)/6=2.6098\ldots$。'],[('M1','选择正确最早相位'),('A1','2.6°')])],['三角方程','复合自变量','区间筛选'],ref='P2-2023-01-Q08')
# Correct the authored working before writing; a rejected trial value is never shown to students.
q=byid['P2-C06-R07'];q['parts'][0]['answer']=r'$x=15.2^\circ,58.1^\circ,135.2^\circ,178.1^\circ$.';q['parts'][0]['solutionSteps']=[r'设$u=3x-20^\circ$，原区间对应$-200^\circ<u\le520^\circ$。',r'$\alpha=\arcsin(\sqrt3/4)=25.658906\ldots^\circ$。',r'$u=\alpha+360n$或$180^\circ-\alpha+360n$；筛选后$u=25.6589\ldots,154.3410\ldots,385.6589\ldots,514.3410\ldots$。',r'由$x=(u+20)/3$得到四个解，最后统一保留1位小数。'];q['parts'][0]['explanation']='\n'.join(q['parts'][0]['solutionSteps'])
revise('P2-C06-R08','正切正弦方程与最小正解',r'In this question you must show detailed reasoning. Solutions relying entirely on calculator technology are not acceptable.',[
 part(r'Solve $3\tan\theta+5\sin\theta=0$ for $0^\circ<\theta\le360^\circ$, giving non-exact answers to one decimal place.',r'$\theta=126.9^\circ,180^\circ,233.1^\circ,360^\circ$.',[r'原式要求$\cos\theta\ne0$；乘以$\cos\theta$得$\sin\theta(3+5\cos\theta)=0$。',r'保留$\sin\theta=0$这一分支，在区间内为$180^\circ,360^\circ$。',r'$\cos\theta=-3/5$给出$126.8698\ldots^\circ,233.1301\ldots^\circ$。',r'全部解在原式有定义；端点0被排除，360被包括。'],[('M1','乘余弦并正确因式分解'),('A1','保留正弦零因子分支'),('M1','求负余弦对应两个象限角'),('A1','所有四解及端点正确'),('A1','精度正确且无未定义角')]),
 part(r'Hence find the smallest positive solution of $3\tan(2x+35^\circ)+5\sin(2x+35^\circ)=0$.',r'$x=45.9^\circ$ (1 d.p.).',[r'最小正$x$对应相位$2x+35=126.8698\ldots$。',r'$x=(126.8698\ldots-35)/2=45.9349\ldots$。'],[('M1','选择第一个大于35°的相位'),('A1','45.9°')])],['三角方程','零因子','定义域','最小正解'],ref='P2-2023-10-Q03')
revise('P2-C06-R09','三角恒等式化二次与弧度区间',r'In this question angles are measured in radians.',[
 part(r'Show that $(4\cos\theta-\tan\theta)\cos\theta=2$ may be written as $4\sin^2\theta+\sin\theta-2=0$.',r'$4(1-\sin^2\theta)-\sin\theta=2$.',[r'当原式有定义时，$\tan\theta\cos\theta=\sin\theta$。',r'展开得$4\cos^2\theta-\sin\theta=2$，再代入$\cos^2\theta=1-\sin^2\theta$。',r'移项即得$4\sin^2\theta+\sin\theta-2=0$。'],[('M1','展开并消去正切商'),('M1','用平方恒等式'),('A1','完整得到指定二次式')]),
 part(r'Hence solve $(4\cos(2x)-\tan(2x))\cos(2x)=2$ for $-\frac\pi2\le x\le\frac\pi2$, giving answers to 3 decimal places.',r'$x=-1.069,-0.501,0.317,1.253$.',[r'令$s=\sin(2x)$，得$s=(-1\pm\sqrt{33})/8$，两个根均在$[-1,1]$内。',r'相位区间为$-\pi\le2x\le\pi$。',r'对正根设$\alpha=\arcsin((-1+\sqrt{33})/8)$，则$2x=\alpha,\pi-\alpha$。',r'对负根设$\beta=\arcsin((-1-\sqrt{33})/8)$，则$2x=\beta,-\pi-\beta$。',r'除以2；检查所有解的$\cos(2x)\ne0$，并在最后取3位小数。'],[('M1','解二次式并保留两个可行根'),('A1','两个正弦值正确'),('M1','完整相位区间及每根两支'),('A1','所有四个x正确'),('B1','不引入未定义点，精度正确')])],['恒等式','二次三角方程','弧度区间'],ref='P2-2022-10-Q05')
revise('P2-C06-R17','教材E：因式分解引导完整三角方程',r'In this question angles are measured in radians.',[
 part(r'Factorise $4xy-y^2+4x-y$.',r'$(y+1)(4x-y)$.',[r'分组得$4x(y+1)-y(y+1)$。',r'提出公因式$y+1$，得$(y+1)(4x-y)$。'],[('M1','正确分组'),('A1','完全因式分解')]),
 part(r'Solve the equation $4\sin\theta\cos\theta-\cos^2\theta+4\sin\theta-\cos\theta=0$, in the interval $0\le\theta\le2\pi$.',r'$\theta=\arctan(1/4),\ \pi,\ \pi+\arctan(1/4)$.',[r'由(a)令$x=\sin\theta,y=\cos\theta$，得$(1+\cos\theta)(4\sin\theta-\cos\theta)=0$。',r'$\cos\theta=-1$给出$\theta=\pi$。',r'另一因子给出$\tan\theta=1/4$，对应第一、三象限。',r'两端点0、$2\pi$均不满足原式，$\cos\theta=0$也不是遗漏根。'],[('M1','正确代换并保留两因子'),('A1',r'$\theta=\pi$'),('M1','正切方程及周期'),('A1','另外两解正确'),('A1','区间与定义域检查完整')])],['因式分解','三角方程','完整区间解'],book=source('P2',134,'Chapter review 6',9,'E',145))
revise('P2-C06-R19','平移三角方程与两支周期解',r'Angles are measured in degrees. Show all stages of your working.',[
 part(r'Solve $5\sin(2x-25^\circ)=3\cos(2x-25^\circ)$ for $-90^\circ<x\le180^\circ$, giving answers to one decimal place.',r'$x=-62.0^\circ,28.0^\circ,118.0^\circ$.',[r'若$\cos(2x-25)=0$，左边为$\pm5$而右边为0，故此类角不是解。',r'因此可除余弦，得$\tan(2x-25)=3/5$。',r'相位区间$-205^\circ<u\le335^\circ$，参考角$\arctan(3/5)=30.9637\ldots^\circ$。',r'$u=-149.0362\ldots,30.9637\ldots,210.9637\ldots$，再由$x=(u+25)/2$求解。'],[('M1','化正切且处理余弦为零'),('M1','使用180°周期及正确相位区间'),('A1','完整三个相位'),('A1','最终三个解及精度')]),
 part(r'Find the number of solutions of the same equation in $-450^\circ<x\le450^\circ$.',r'10.',[r'对$x$的周期为$90^\circ$。',r'该左开右闭区间长$900^\circ$，恰含10个周期，每周期一个根。'],[('M1','确定对x的周期90°'),('A1','10根')])],['平移自变量','正切周期','完整区间解'],ref='P2-2022-01-Q07')
revise('P2-C06-R20','乘积展开后的三角方程',r'In this question you must show all stages of your working.',[
 part(r'Show that $2\sin^3\theta=3\sin\theta-4\sin\theta\cos\theta$ can be written as $\sin\theta(2\cos^2\theta-4\cos\theta+1)=0$.',r'$\sin\theta[2(1-\cos^2\theta)-3+4\cos\theta]=0$.',[r'将所有项移到一边后提出$\sin\theta$，不除去它。',r'用$\sin^2\theta=1-\cos^2\theta$整理，并把整体乘以$-1$。'],[('M1','保留正弦因子'),('M1','平方恒等式及整理'),('A1','得到目标式')]),
 part(r'Hence solve the equation for $-\pi\le\theta<\pi$, giving non-exact answers in radians to 3 decimal places.',r'$\theta=-\pi,-1.274,0,1.274$.',[r'$\sin\theta=0$给出$-\pi,0$；$\pi$被右端点排除。',r'余弦二次式的根为$1\pm\sqrt2/2$，大于1的根舍去。',r'设$\alpha=\arccos(1-\sqrt2/2)=1.2735\ldots$，另两解为$\pm\alpha$。'],[('B1','正弦零因子解完整'),('M1','解余弦二次并舍不可能根'),('M1','余弦两支与给定区间匹配'),('A1','四解完整及精度')])],['恒等式','保留零因子','二次方程'],ref='P2-2021-06-Q08')
revise('P2-C06-R27','教材E/P：二倍角正切方程',r'Given that $2\sin2\theta=\cos2\theta$,',[
 part(r'Show that $\tan2\theta=0.5$.',r'$\tan2\theta=1/2$.',[r'$\cos2\theta=0$时原式两边不相等，故所有解都可除以$\cos2\theta$。',r'于是$2\tan2\theta=1$。'],[('B1','正确化为正切方程')]),
 part(r'Hence find the values of $\theta$, to 3 significant figures, in the interval $0\le\theta\le2\pi$ for which $2\sin2\theta=\cos2\theta$.',r'$\theta=0.232,1.80,3.37,4.94$.',[r'相位区间为$0\le2\theta\le4\pi$。',r'$2\theta=\arctan(1/2)+n\pi$，其中$n=0,1,2,3$。',r'$\theta=0.2318238\ldots,1.8026201\ldots,3.3734164\ldots,4.9442127\ldots$。',r'注意3位有效数字与3位小数不同。'],[('M1','建立相位区间'),('M1','180°或π周期通解'),('A1','四个未舍入值正确'),('A1','全部按3位有效数字作答')])],['二倍自变量','正切方程','弧度'],book=source('P2',134,'Chapter review 6',11,'E/P',145))
revise('P2-C06-R28','平方三角方程的符号分支',r'Angles are measured in degrees.',[
 part(r'Solve $\tan^2(2x+15^\circ)=3$ for $-90^\circ\le x<90^\circ$.',r'$x=-67.5^\circ,-37.5^\circ,22.5^\circ,52.5^\circ$.',[r'平方等于3意味着$\tan u=\sqrt3$或$-\sqrt3$，不能只取正根。',r'$u=2x+15$的范围为$-165^\circ\le u<195^\circ$。',r'区间内相位为$-120,-60,60,120$，对应四个$x$。'],[('M1','正负两个分支'),('M1','正确相位区间'),('A1','完整四个相位'),('A1','正确四个x及端点')]),
 part(r'Solve $(3\sin\theta-\cos\theta)^2=1$ for $0^\circ<\theta<360^\circ$, giving non-exact answers to one decimal place.',r'$\theta=36.9^\circ,180^\circ,216.9^\circ$.',[r'展开并利用$\sin^2\theta+\cos^2\theta=1$，得$8\sin^2\theta-6\sin\theta\cos\theta=0$。',r'因式分解为$2\sin\theta(4\sin\theta-3\cos\theta)=0$。',r'第一分支给出$180^\circ$；第二分支给出$\tan\theta=3/4$，为$36.8698\ldots^\circ,216.8698\ldots^\circ$。',r'0与360均不在开区间内。'],[('M1','正确展开及平方恒等式'),('M1','保留正弦因子'),('A1','180°这一根正确'),('M1','正切分支两解'),('A1','完整三解与精度')])],['平方方程','恒等式','完整区间解'],ref='P2-2021-10-Q10')
# P1 transformations: meaningful sketching, parameter constraints and distinct roots.
revise('P1-C04-R01','已知特征图像的伸缩与交点',r'The curve $y=f(x)$ has a maximum at $A(-2,5)$, a minimum at $B(4,-1)$ and horizontal asymptote $y=2$. The line $y=1$ meets the curve at exactly three distinct points.',[
 part(r'For the curve $y=-2f(x)$, state the coordinates of its maximum and minimum and the equation of its horizontal asymptote.',r'最大点$(4,2)$，最小点$(-2,-10)$，渐近线$y=-4$.',[r'纵坐标乘以$-2$，横坐标不变；负号使极大与极小互换。',r'渐近线纵坐标也乘以$-2$。'],[('B1','两个极值类型及坐标正确'),('B1','渐近线y=−4')]),
 part(r'State the number of solutions of $f(3x) = 1$. Explain your answer by describing a transformation.',r'3个；横向伸缩比例$1/3$保持交点数。',[r'变换将每个横坐标$x$对应到$x/3$，不同点仍不同。',r'水平线高度1不变，所以原来的三个交点各对应一个解。'],[('B1','根数3'),('B1','以横向伸缩说明一一对应')])],['图像变换','极值对应','交点个数'],ref='P1-2022-06-Q04')
revise('P1-C04-R20','重根三次图像及逆向变换',r'The curve $C$ has equation $y=(x+2)(x-3)^2$.',[
 part(r'Sketch $C$, showing the coordinates of every point where it crosses or touches a coordinate axis.',r'横轴交点$(-2,0)$为穿过，$(3,0)$为相切；纵轴交点$(0,18)$。左下至右上。',[r'一次因子对应穿过横轴，二重因子对应接触横轴。',r'令$x=0$得18，最高次项系数为正确定两端方向。'],[('B1','三次曲线正确形状与两个根的接触类型'),('B1','三个截距坐标正确'),('B1','左右端方向正确')]),
 part(r'The curve is stretched parallel to the $x$-axis with scale factor 2. Write down the equation of its image, and state the coordinates of its points on the $x$-axis.',r'$y=(x/2+2)(x/2-3)^2$；$(-4,0),(6,0)$.',[r'横向伸缩比例2意味着用$x/2$替换原式中的$x$。',r'两个原横坐标分别乘以2，接触类型不变。'],[('M1','正确替换x为x/2'),('A1','方程正确'),('B1','两个新根坐标正确')])],['三次函数','重根','横向伸缩'],ref='P1-2020-01-Q10')
# Supplied sketch supports inference, without stating the intersection counts.
q=byid['P1-C06-R14']
q['stem']=r'The diagram shows $C:y=\tan x$ and the dashed line $l:y=2x$ for $-\pi<x<\pi$. Angles are measured in radians.'+plot(math.tan,-math.pi,math.pi,-5,5,[(-math.pi,'−π'),(-math.pi/2,'−π/2'),(math.pi/2,'π/2'),(math.pi,'π')],label='C; dashed line l',extra=lambda x:2*x)
q['parts'][0]=part(r'State the period of $C$ and the equations of its vertical asymptotes in the given interval.',r'周期$\pi$；渐近线$x=\pm\pi/2$。',[r'正切每隔$\pi$重复，并在$\cos x=0$时无定义。'],[('B1','周期π'),('B1','两条渐近线正确')])
q['parts'][1]=part(r'Using the diagram and periodicity, state the number of distinct roots of $\tan x=2x$ in (i) $-\pi<x<\pi$, (ii) $-3\pi<x<3\pi$, (iii) $-20\pi<x<20\pi$.',r'(i) 3; (ii) 7; (iii) 41.',[r'从图中读出中央支有3个交点，两端截断半支没有交点。',r'向外延伸时，每增加一个完整正切支就增加一个交点。',r'$(-N\pi,N\pi)$内有$2N-2$个完整外支，因此共有$2N+1$个根。'],[('B1','3'),('B1','7'),('B1','41')])
q['marks']=5;q['answerFigure']=''
# Diagram-specific construction, with geometry matching the stated configuration.
def polygon(points,labels,extra=''):
 body='<path d="M'+' L'.join(f'{x:.2f} {y:.2f}' for x,y in points)+' Z"/>'
 for x,y,label in labels:body+=txt(x,y,label)
 return fig(body+extra,'Geometric configuration with only supplied lengths and labels')
def replacefigure(id,diagram):
 q=byid[id];q['stem']=re.sub(r'<figure.*?</figure>','',q['stem'],flags=re.S)+diagram
 if id not in changes:changes[id]=dict(kind='diagram-redraw',reason='按实际边角、方位和内部点重绘，替换通用三角形。',before=copy.deepcopy(q))
replacefigure('P1-C06-R01',polygon([(100,240),(260,240),(220,32.15)],[(80,260,'A'),(265,260,'B'),(218,22,'C'),(177,265,'x'),(127,140,'x + 2'),(267,140,'2√7'),(130,221,'60°')]))
replacefigure('P1-C06-R02',polygon([(90,245),(360,245),(177.12,194.70)],[(70,265,'B'),(365,265,'A'),(168,182,'C₁'),(411,53,'C₂'),(215,270,'10 cm'),(130,235,'30°')],'<path d="M90 245L407.53 61.67L360 245" stroke-dasharray="6 4"/>'+txt(402,158,'7 cm')))
replacefigure('P1-C06-R06',polygon([(90,230),(240,230),(202.5,35.14)],[(65,255,'H'),(245,250,'A'),(207,30,'B'),(145,253,'6 km'),(170,125,'9 km'),(90,24,'N'),(95,120,'030°')],'<path d="M90 230V30" stroke-dasharray="6 4"/>'))
replacefigure('P1-C06-R19',polygon([(65,210),(290,210),(365,80)],[(45,230,'A'),(275,230,'B'),(365,65,'C'),(165,236,'9'),(345,150,'6'),(225,194,'120°'),(460,232,'D')],'<path d="M290 210H465"/>'))
replacefigure('P1-C06-R20',polygon([(80,240),(246.28,144),(400,240)],[(60,260,'A'),(243,130,'B'),(405,260,'C'),(203,260,'D'),(132,180,'6'),(135,267,'4'),(300,267,'6'),(130,225,'30°')],'<path d="M246.28 144L208 240"/>'))
replacefigure('P1-C06-R25',polygon([(180,100),(253.54,38.29),(295.70,237.89)],[(155,110,'O'),(251,24,'A'),(298,258,'B'),(175,18,'N'),(228,56,'8 km'),(282,180,'15 km'),(209,83,'050°'),(210,130,'140°')],'<path d="M180 100V28" stroke-dasharray="6 4"/><path d="M180 75A25 25 0 0 1 199.15 83.93 M180 60A40 40 0 0 1 205.71 130.64"/>'))
# Composite stage: side triangles share radii with the circular sector.
a=(math.pi-2)/2;O=(270,240);scale=32
B=(O[0]-5*scale*math.cos(a),O[1]-5*scale*math.sin(a));C=(O[0]+5*scale*math.cos(a),O[1]-5*scale*math.sin(a));A=(O[0]-4*scale,O[1]);D=(O[0]+4*scale,O[1])
replacefigure('P1-C07-R01',fig(f'<path d="M{A[0]} {A[1]}L{B[0]} {B[1]}A160 160 0 0 1 {C[0]} {C[1]}L{D[0]} {D[1]}Z"/><path d="M{B[0]} {B[1]}L270 240L{C[0]} {C[1]}" stroke-dasharray="6 4"/>'+txt(A[0]-15,261,'A')+txt(270,264,'O')+txt(D[0]+5,261,'D')+txt(B[0]-20,B[1]-5,'B')+txt(C[0]+8,C[1]-5,'C')+txt(242,128,'2 rad')+txt(182,205,'5 m')+txt(173,280,'4 m')+txt(325,280,'4 m'),'Sector joined to two congruent side triangles'))
replacefigure('P1-C07-R02',fig('<path d="M120 220L440 220A320 320 0 0 0 354.1 1.8L237 110.9A160 160 0 0 1 280 220Z"/>'+txt(100,240,'O')+txt(195,240,'4 m')+txt(346,240,'x')+'<path d="M120 220H280" stroke-dasharray="6 4"/>','Annular sector with unknown outer radial extension'))
# Rebuild this annular sector within the view box, with a smaller visible angle.
replacefigure('P1-C07-R02',fig('<path d="M100 240H450A350 350 0 0 0 367.7 14.5L237.7 124A180 180 0 0 1 280 240Z"/><path d="M100 240H280" stroke-dasharray="6 4"/>'+txt(78,260,'O')+txt(180,265,'4 m')+txt(356,265,'x'),'Annular sector with labelled inner radius and radial width'))
replacefigure('P1-C07-R08',fig('<path d="M150 100A200 200 0 0 1 390 100L390 180H150Z"/><path d="M150 100H390 M150 100L270 260L390 100" stroke-dasharray="6 4"/>'+txt(128,99,'A')+txt(395,99,'B')+txt(260,282,'O')+txt(245,95,'12 cm')+txt(398,155,'4 cm')+txt(172,204,'10 cm'),'Minor circular segment attached to a rectangle'))
replacefigure('P1-C07-R12',fig('<path d="M238.56 70H345.23V230H238.56A160 160 0 0 0 238.56 70Z"/><path d="M238.56 70L100 150L238.56 230 M238.56 70V230" stroke-dasharray="6 4"/>'+txt(78,157,'O')+txt(218,55,'A')+txt(218,253,'B')+txt(355,75,'D')+txt(355,237,'C')+txt(270,57,'4 cm')+txt(270,253,'4 cm')+txt(155,95,'6 cm')+txt(155,215,'6 cm')+txt(133,155,'2θ'),'Rectangle with a circular segment removed from its left side'))
replacefigure('P1-C07-R14',fig('<path d="M270 250L133.67 103.66A200 200 0 0 1 406.33 103.66Z"/><path d="M133.67 103.66H406.33"/>'+txt(260,275,'O')+txt(108,103,'A')+txt(416,103,'B')+txt(265,85,'R')+txt(175,180,'r')+txt(355,180,'r')+txt(246,204,'1.5'),'Sector and the segment bounded by its chord'))
replacefigure('P1-C07-R18',fig('<circle cx="220" cy="145" r="110"/><circle cx="330" cy="145" r="110"/><path d="M220 145L275 49.74L330 145L275 240.26Z M220 145H330" stroke-dasharray="6 4"/>'+txt(202,166,'O₁')+txt(331,166,'O₂')+txt(270,36,'A')+txt(270,263,'B')+txt(270,143,'R')+txt(228,102,'12 cm'),'Two equal circles whose centres lie on each other'))
# Archive repetitive introductory items, retaining their IDs for saved history only.
for id,reason in {
 'P1-C07-R04':'仅把已知直角扇形与等边三角形面积直接相加，与多道题训练重复。',
 'P1-C07-R06':'仅联立两条弧长，无新增核心思维；保留更完整的环形区域题。',
 'P1-C07-R17':'比例尺基础步骤过多，四问结构被用来拆分单一方法。',
 'P1-C07-R19':'已知直角三角形面积反求半径后重复套公式。',
 'P1-C07-R22':'把整圆按固定比拆分后分别代入公式，与已有题高度重复。',
 'P1-C07-R26':'两个已知角同半径的面积差，后续重复套公式。',
 'P2-C06-R03':'与R08、R16重复保留零因子的基础训练，保留较完整的区间题。',
 'P2-C06-R04':'在R01与多道二次恒等式题之间重复，删除附加求和小问。',
 'P2-C06-R06':'与R28及教材二倍角方程重复，缺乏新的设问价值。',
 'P2-C06-R22':'与R28平方正切方程训练重复，后续求余弦平方只是重复换写。',
 'P2-C06-R30':'两次代入求常数后只回到平方恒等式，偏离本章完整解方程重点。',
}.items():
 old=copy.deepcopy(byid[id]);byid[id].update(withdrawn=True,withdrawalReason=reason);changes[id]=dict(kind='withdrawn',reason=reason,before=old)
# Full-bank diagram audit: move answer sketches out of question statements.
for id in ['P1-C04-R02','P1-C04-R09','P3-C02-R08','P3-C03-R08']:
 q=byid[id];figures=re.findall(r'<figure.*?</figure>',q['stem'],re.S)
 if figures:
  changes.setdefault(id,dict(kind='diagram-separation',reason='题目要求作出的图不应提前展示。',before=copy.deepcopy(q)))
  q['answerFigure']=''.join(figures)+q.get('answerFigure','');q['stem']=re.sub(r'<figure.*?</figure>','',q['stem'],flags=re.S)
# A solved tangent was labelled in the question diagram: retain it only with the solution.
id='P3-C07-R27';q=byid[id];figures=re.findall(r'<figure.*?</figure>',q['stem'],re.S)
if figures:
 changes[id]=dict(kind='answer-leak-fix',reason='图中预先画出了待求切线且标出1+2x。',before=copy.deepcopy(q));q['answerFigure']=''.join(figures);q['stem']=re.sub(r'<figure.*?</figure>','',q['stem'],flags=re.S).replace(' Figure 1 illustrates the curves in this question.','')
# Parameter curves cannot be illustrated by an arbitrary solved curve before parameters are found.
for id in ['P1-C08-R27','P2-C01-R21','P3-C06-R36']:
 q=byid[id]
 if '<figure' in q['stem']:
  changes.setdefault(id,dict(kind='parameter-diagram-removal',reason='避免参数未知时先绘出已求解曲线，泄露或误导条件。',before=copy.deepcopy(q)))
  q['stem']=re.sub(r'<figure.*?</figure>','',q['stem'],flags=re.S).replace(' The diagram shows the curve.','')
# The entire figure set is normalized to exam-style monochrome, unique IDs and readable labels.
visual=[]
for q in bank['questions']:
 for key in ['stem','answerFigure']:
  s=q.get(key,'')
  if '<svg' not in s:continue
  old=s
  def neutral(m):
   attr,col=m.group(1),m.group(2).lower()
   if attr=='stroke':return 'stroke="#222"'
   if col in ['#fff','#ffffff']:return 'fill="#fff"'
   code=col[1:]
   if len(code)==3:code=''.join(c*2 for c in code)
   light=sum(int(code[i:i+2],16) for i in (0,2,4))/3
   return 'fill="'+('#eee' if light>140 else '#222')+'"'
  s=re.sub(r'stroke="(?:#bf7956|#b45309|#99633d|#8b4422)"', 'stroke="#222" stroke-dasharray="6 4"',s)
  s=re.sub(r'(stroke|fill)="(#[0-9a-fA-F]{3,8})"',neutral,s)
  for ident in set(re.findall(r'\bid="([^"]+)"',s)):
   safe=q['id']+'-'+key+'-'+ident;s=s.replace('id="'+ident+'"','id="'+safe+'"').replace('url(#'+ident+')','url(#'+safe+')')
  s=s.replace('green: ','solid: ').replace('brown: ','dashed: ')
  q[key]=s
  if s!=old:visual.append(q['id'])
# Remove a misleading impossible triangle sketch. The existence test needs no purported triangle.
q=byid['P1-C06-R22'];q['stem']=re.sub(r'<figure.*?</figure>','',q['stem'],flags=re.S).replace('Triangle $ABC$ has','A proposed triangle $ABC$ would have')
# Explicit provenance on every content revision, without claiming external teacher approval.
bank.update(revision=12,updatedAt='2026-10-23')
(ROOT/'dist/data/bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
index=json.loads((ROOT/'dist/data/classification.json').read_text())
for q in bank['questions']:index['questions'][q['id']]['chapters']=q['chapters']
(ROOT/'dist/data/classification.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
# Retain a reviewable before/after record and immutable before hashes for every original record.
def digest(q):return hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
manifest={'date':'2026-10-23','priorCommit':'1224b7b9d7d8061b5249e36bde9b27f5d23279b4','revisions':[{k:v for k,v in dict(id=id,**entry).items() if k!='before'} for id,entry in changes.items()],'monochromeFigureIds':sorted(set(visual)),'beforeHashes':{q['id']:digest(q) for q in before['questions']},'afterHashes':{q['id']:digest(q) for q in bank['questions']}}
(ROOT/'editorial/v12/review-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(ROOT/'editorial/v12/replaced-items.json').write_text(json.dumps({id:e['before'] for id,e in changes.items()},ensure_ascii=False,indent=2)+'\n')
print('Individually rewritten',sum(e['kind'] in ['individual-rewrite','textbook-selection'] for e in changes.values()),'including textbook',sum(e['kind']=='textbook-selection' for e in changes.values()),'withdrawn',sum(e['kind']=='withdrawn' for e in changes.values()),'diagram adjustments',len(set(visual)))
