"""Approved P1 C07 re-audit. Only this chapter is authored here."""
import copy,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
OLD={q['id']:q for q in json.loads((ROOT/'editorial/v14/p1-radians.json').read_text())['questions']}
Q=[]
def p(text,answer,steps,marks):
    # One mark per substantive criterion; no marks for merely copying a target.
    return dict(text=text,answer=answer,approach=steps[0],solutionSteps=steps,explanation='\n'.join(steps),scheme=[dict(code=c+'1',marks=1,text=t) for c,t in marks],marks=len(marks))
def add(n,title,stem,parts,family,source,summary,dims,essence,increment,errors,template):
    q=dict(id=fr'P1-C07-R{n:02d}',stage='P1',chapters=[7],type=title,stem=stem,parts=parts,marks=sum(x['marks'] for x in parts),topics=['弧度制',title],origin='original-reviewed-2026',review='internal-review-only',editorialRevision=16,solutionRevision=16,originalNumber=n,sourceReferences=[dict(questionId=source,year=int(source.split('-')[1]),note=summary)],sourceSummary=summary,adaptationDimensions=dims,examEssence=essence,difficultyPosition=fr'略难于 {source}：{increment}',adaptationNote='变式来源见下；实质改编维度：'+'、'.join(dims)+'。思维增量：'+increment+'。',errorNotes=errors,designNote=increment+'。保留来源题的'+essence+'。',contentUpdatedAt='2026-10-24',family=fr'P1-C07-R{n:02d}',examFamily=family,questionTemplate=template,answerFigure='')
    Q.append(q)

# G1: inverse symmetric geometry, not a numerical safety-rule appendage.
A=18*math.sqrt(3)+6*math.pi
rnew=math.sqrt(A/(math.pi/3+math.sqrt(3)/2))
P1=24+2*math.pi;P2=rnew*(2+2*math.pi/3+2*math.sqrt(3))
add(1,'对称拼接的逆向条件与等面积比较',
r'A stage consists of a sector $OBC$ and two congruent triangles $OAB$ and $OCD$, attached outside the sector. The points $A,O,D$ lie on a straight line in that order, $OA=OD=x$ m and $OB=OC=r$ m, where $x,r>0$. The angle $BOC$ is $\pi/3$ radians and $AB=CD=r$. The total area is $(18\sqrt3+6\pi)\text{ m}^2$.',[
p(r'Find the exact values of $r$ and $x$.',r'$r=x=6$.',[
r'先由直线角及对称性求侧角：$\angle AOB=(\pi-\pi/3)/2=\pi/3$。',r'余弦定理和 $AB=r$ 给出 $r^2=x^2+r^2-xr$，故 $x(x-r)=0$。因 $x>0$，只能 $x=r$。',r'总面积为 $\frac12r^2(\pi/3)+2(\frac12r^2\sin(\pi/3))=r^2(\pi/6+\sqrt3/2)$。',r'与给定面积比较得 $r^2=36$；两长度均为正，故 $r=x=6$。'],[('B','由对称和直线角确定侧角'),('M','把AB=r代入余弦定理'),('A','排除x=0并得x=r'),('M','建立完整面积方程'),('A','取得正确的正半径和侧边')]),
p(r'A second design has $\angle BOC=2\pi/3$ radians. It has the same total area and again satisfies $AB=CD=r$, but its values of $r$ and $x$ may differ. Determine which design has the smaller perimeter, giving each perimeter to 3 significant figures.',fr'第一种周界 $={P1:.3g}$ m；第二种 $={P2:.3g}$ m，第一种较小。',[
r'第二种侧角为 $\pi/6$；余弦定理给 $x=2r\cos(\pi/6)=\sqrt3r$。',r'面积条件变为 $r^2(\pi/3+\sqrt3/2)=18\sqrt3+6\pi$，由此求第二种正半径。',r'周界只含两斜边、圆弧和底边，统一为 $P=2r+r\theta+2x$，不含两条内部半径。',fr'第一种 $P=24+2\pi={P1:.6f}\ldots$；第二种正半径为 ${rnew:.6f}\ldots$，周界为 ${P2:.6f}\ldots$。',r'按未舍入值比较，并将两个周界各取3位有效数字。'],[('M','从新角度重新得到x与r的关系'),('M','按相同总面积反求新的尺度'),('M','正确构造外周界'),('A','两个周界正确'),('B','比较方向及3位有效数字正确')])],
'G1','P1-2024-06R-Q06','扇形与全等侧三角形：证明角、求外周界和面积',
['设问角度','条件呈现','求解目标','题目结构','跨考点耦合'], '对称角关系、余弦定理和拼接后真正的外边界', '用相等边的隐含条件重建尺寸，再在同面积约束下重新缩放第二种几何设计', ['AB=r并不意味着可以直接假定x=r，须证明并排除零长度。','第二种设计的半径会改变，不能直接比较圆心角。'], '等边界条件逆求尺寸后作等面积设计比较')

# G4: the two-radius platform in the actual source, reversed and cut by a chord.
add(2,'同心组合扇形的逆求与边界替换',
r'A platform consists of a major sector of radius $r$ cm and angle $2\pi-\theta$, joined to a minor sector of radius $2r$ cm and angle $\theta$, where $r>0$ and $0<\theta<\pi$. Their centres are both $O$ and the two radial directions are common. The two sectors have disjoint interiors. The longer-radius arc has length $4\pi$ cm and the total area is $54\pi\text{ cm}^2$.',[
p(r'Find $r$ and $\theta$, giving exact answers.',r'$r=6\text{ cm},\quad\theta=\pi/3$.',[
r'长半径的弧满足 $2r\theta=4\pi$，即 $r\theta=2\pi$。',r'两部分面积相加：$54\pi=\frac12r^2(2\pi-\theta)+\frac12(2r)^2\theta=\pi r^2+\frac32r^2\theta$。',r'消去 $\theta$ 后得 $r^2+3r-54=(r+9)(r-6)=0$。',r'负半径舍去；$r=6$，继而 $\theta=\pi/3$，确在指定范围。'],[('M','由外弧长建立方程'),('M','建立不重叠组合面积方程'),('M','消元并求二次方程'),('A','选择正根并给正确角')]),
p(r'The major arc of the smaller circle is replaced by the straight chord joining its endpoints. The boundary using the larger-radius arc is retained. Find the exact reductions in the area and in the perimeter of the platform.',r'面积减少 $(30\pi+9\sqrt3)\text{ cm}^2$；周界减少 $(10\pi-6)\text{ cm}$。',[
r'替换的原弧为小圆的大弧，角为 $5\pi/3$；新弦长为 $2(6)\sin(\pi/6)=6$。',r'周界其余部分不变，减少量是 $6(5\pi/3)-6=10\pi-6$。',r'被截去的是大弓形，而非小弓形：面积为大扇形加对应等腰三角形。',r'$\Delta A=\frac12(6)^2(5\pi/3)+\frac12(6)^2\sin(\pi/3)=30\pi+9\sqrt3$。'],[('M','正确求替代弦长'),('A','正确的周界减少量'),('B','识别被去掉的是大弓形'),('M','大扇形与三角形相加'),('A','正确的精确面积减少量')])],
'G4','P1-2024-01-Q08','同心不同半径的扇形平台：由弧长及比例求半径、完整周界与面积',
['设问角度','条件呈现','求解目标','题目结构','收尾要求'], '不同半径对应的角、组合面积及两段径向边界', '逆用整体面积和外弧条件求尺度，再识别大弧换弦实际切掉的大弓形', ['两扇形面积相加，不是同角的外扇形减内扇形。','换掉大弧时，面积损失是大弓形，不能使用小弓形公式。'], '同心异角双半径逆求后截去大弓形')

# G5: the actual alternating-radius fan, with unknown repetition count.
P=16*math.pi+30;area=64*math.pi-90;scale=P/(16*math.pi+37.5);aratio=scale**2*(64*math.pi-112.5)/area
add(8,'双半径风扇的单元数反求与等周缩放',
r'A flat fan is made from $n$ identical angular cells arranged around a common centre, with no gaps between cells. Each cell consists of a sector of radius $2$ cm and angle $\alpha$, followed by a sector of radius $8$ cm and angle $\beta$, where $\alpha,\beta>0$ and $\alpha+\beta=2\pi/n$. The cells form one connected shape. Its area is $(64\pi-90)\text{ cm}^2$ and its perimeter is $(16\pi+30)$ cm.',[
p(r'Determine $n$ and $\alpha$. Explain why your values describe a valid fan.',r'$n=4,\quad\alpha=3/4$；$\beta=\pi/2-3/4>0$.',[
r'利用 $n\beta=2\pi-n\alpha$，面积方程为 $2n\alpha+32n\beta=64\pi-90$，故 $n\alpha=3$。',r'每个单元外露两弧及两条长 $8-2=6$ 的径向阶差；公共的内侧半径在内部。',r'周界为 $2n\alpha+8n\beta+12n=16\pi-6n\alpha+12n$。',r'代入 $n\alpha=3$ 及给定周界，得 $n=4$，$\alpha=3/4$。',r'验证 $n$ 为正整数且 $\beta=\pi/2-3/4>0$，整周角条件确实满足。'],[('M','正确写出重复单元总面积'),('A','由面积得到nα=3'),('M','识别每单元两段径向阶差'),('M','建立完整周界方程'),('A','解得n及α'),('B','核查整数和正角条件')]),
p(r'A second fan has five cells and the same value of $\alpha$. Before scaling, its two radii are also $2$ cm and $8$ cm. It is then scaled uniformly so that its perimeter equals that of the first fan. Find the ratio of its final area to the area of the first fan, giving your answer in the form $k:1$, where $k$ is correct to 3 significant figures.',fr'${aratio:.3g}:1$.',[
r'五单元方案有 $n\alpha=15/4$，其未缩放面积为 $64\pi-112.5$，周界为 $16\pi+37.5$。',r'等周界的线性缩放因子为 $s=(16\pi+30)/(16\pi+37.5)$；面积须乘 $s^2$。',fr'所求比值 $k=s^2(64\pi-112.5)/(64\pi-90)={aratio:.8f}\ldots$。',r'验证五单元的另一个角 $2\pi/5-3/4>0$，并按要求给出面积比。'],[('M','重建五单元方案面积与周界'),('M','用周界确定线性缩放因子'),('M','对面积使用缩放因子的平方'),('A','正确面积比及有效方案')])],
'G5','P1-2022-06-Q08','两种半径的重复扇形风扇：由整周关系求弧长、总周界和总面积',
['设问角度','条件呈现','求解目标','参数化与分类讨论','跨考点耦合'], '重复单元的整周角、不同半径面积和外露的径向阶差', '将已知单元数改为由面积与周界同时反求，并比较改变单元数后等周缩放的面积', ['内部半径不属于外边界，但每次高低半径交替产生的6 cm边必须计入。','统一缩放时，面积乘s²而不是s。'], '未知重复数联立反求与等周缩放比较')

# G2: discriminate all minor sectors rather than merely solve the old quadratic.
add(10,'固定周界下两种小扇形的面积范围',
r'A minor sector has radius $r$ cm, angle $\theta$ radians, perimeter $20$ cm and area $A\text{ cm}^2$, where $r>0$ and $0<\theta<\pi$.',[
p(r'Show that $A\le25$ and find the radius and angle when equality holds.',r'$A\le25$；等号时 $r=5,\theta=2$.',[
r'周界条件给 $r\theta=20-2r$，所以 $A=\frac12r(r\theta)=10r-r^2$。',r'配方得 $A=25-(r-5)^2\le25$。',r'等号时 $r=5$，由周界得 $\theta=2$；该角在 $(0,\pi)$ 内。'],[('M','从周界消去角得到面积表达式'),('M','通过配方证明上界'),('A','等号时两参数正确并满足minor范围')]),
p(r'Find the exact range of $A$ for which two distinct minor sectors have this perimeter and this area. Justify both ends of your range.',r'$\displaystyle\frac{200\pi}{(\pi+2)^2}<A<25$.',[
r'由 $0<20/r-2<\pi$ 得 $20/(\pi+2)<r<10$。',r'当 $A<25$ 时，两个可能半径为 $5-\sqrt{25-A}$、$5+\sqrt{25-A}$。',r'要两根都可用，较小根必须严格大于 $20/(\pi+2)$；较大根随后自动小于10。',r'令边界较小根为 $20/(\pi+2)$，相应 $A=r(10-r)=200\pi/(\pi+2)^2$。',r'下界使一解角等于π，已不再是minor；上界两根合并，故两端均不取。'],[('M','取得半径的几何有效区间'),('M','表达二次方程的两根'),('M','将两根可用化为较小根的严格限制'),('A','精确面积下界正确'),('B','解释两端均须排除')])],
'G2','P1-2019-01-Q10','给定扇形面积和周界，建立角的二次方程并找全部半径与角的配对',
['求解目标','条件呈现','参数化与分类讨论','收尾要求'], '同时使用扇形面积和完整周界，保留并检验所有几何解', '把一次求两根升级为整段面积参数的双解分类，并处理π边界和重根', ['二次方程有两个正根，不等于有两个有效minor sectors。','A=25只有一个扇形；较小角的相应根配对不能弄反。'], '固定周界的面积参数双解区间')

# G1: determine exactly when the obtuse-angle major-sector diagram exists.
delta=math.pi/6;d=11;omega=math.pi-math.asin(d/12);angA=math.pi-omega-delta;s=12*math.sin(angA)
per=6*(2*math.pi-omega)+(s-6)+d;area13=18*(2*math.pi-omega)+3*s*math.sin(omega)
add(13,'大扇形平台的存在范围与钝角取舍',
r'A platform is formed from a major sector of a circle, centre $O$ and radius $6$ m, joined to triangle $AOD$. Points $O,C,D$ lie on one ray in that order, $OC=OA=6$ m, $AD=d$ m and $\angle ADO=\pi/6$. The angle $AOD$ must be obtuse. The major arc from $A$ to $C$ is denoted by arc $ABC$. The outside boundary is arc $ABC$, $CD$ and $DA$.',[
p(r'Find the complete range of $d$ for which this platform exists. Your answer must take account of both the obtuse angle and the order of $O,C,D$.',r'$6\sqrt3<d<12$.',[
r'正弦定理给 $\sin\angle AOD=d/12$。取钝角时 $\angle AOD=\pi-\sin^{-1}(d/12)$，且 $d<12$，不能把直角端点包括进来。',r'令 $\gamma=\sin^{-1}(d/12)$，则 $\angle OAD=\gamma-\pi/6$。',r'由正弦定理，$OD=12\sin(\gamma-\pi/6)$。要求 $D$ 在 $C$ 外侧，即 $OD>6$。',r'三角形存在须有 $\angle OAD>0$；在此范围内 $0<\gamma-\pi/6<\pi/3$，正弦递增；$OD>6$ 等价于 $\gamma-\pi/6>\pi/6$。',r'故 $\gamma>\pi/3$，即 $d>12\sin(\pi/3)=6\sqrt3$；结合上界得所求严格区间。'],[('M','用正弦定理并选择钝角支'),('A','钝角给出严格上界'),('M','将共线顺序转化为OD>6'),('M','正确比较角或构造边界三角形'),('A','取得完整严格区间')]),
p(r'For $d=11$, find the total area and the perimeter of the platform, giving each answer to 3 significant figures.',fr'面积 ${area13:.1f}\text{{ m}}^2$；周界 ${per:.3g}$ m。',[
fr'取钝角 $\omega=\pi-\sin^{{-1}}(11/12)={omega:.8f}\ldots$。',fr'$OD=12\sin(\pi-\omega-\pi/6)={s:.8f}\ldots$，确大于6。',r'大扇形角为 $2\pi-\omega$；三角形与大扇形的内部互不重叠。',fr'$A=18(2\pi-\omega)+3OD\sin\omega={area13:.8f}\ldots$。',fr'$P=6(2\pi-\omega)+(OD-6)+11={per:.8f}\ldots$；公共半径OA及OC不计。'],[('M','正确选择所需钝角'),('A','取得OD的正确长度'),('M','正确构造大扇形和三角形总面积'),('A','总面积正确'),('M','正确构造外弧及两段直边'),('A','周界正确并按3位有效数字作答')])],
'G1','P1-2021-01-Q05','正弦定理选择钝角，求大弧长及三角形与扇形的组合面积',
['求解目标','条件呈现','参数化与分类讨论','题目结构','收尾要求'], 'SSA的角支选择、大扇形及共线部分边界', '先证明平台存在的完整参数区间，尤其增加OD大于半径的非退化限制，再完成有效设计的面积周界', ['只写d<12会漏掉D必须在C外侧的限制。','下界OD=OC使D和C重合，上界使AOD为直角，两端均不可取。'], '带共线顺序的SSA几何存在区间')

# G1: two genuine SSA signs with inverse data, no numerical threshold appendage.
rr=math.sqrt(17)/2;design=[]
for x in (2*math.sqrt(3)-.5,2*math.sqrt(3)+.5):
 th=math.acos((16+17/4-x*x)/(8*rr));aa=17/8*(2*math.pi-th)+x;pp=rr*(2*math.pi-th)+x+4-rr;design.append((x,th,aa,pp))
add(20,'标志的两种逆向设计与未舍入比较',
r'A sign consists of triangle $CPQ$ joined to a major sector of a circle with centre $C$. The sector has radius $CQ=\sqrt{17}/2$ m. A point $T$ lies on $CP$ with $CT=CQ$, and the major sector has endpoints $Q$ and $T$. The triangle and sector have disjoint interiors. Given that $PC=4$ m and $\angle QPC=\pi/6$, the outside boundary is $PQ$, $PT$ and the major arc $QT$.',[
p(r'Find both possible exact lengths of $PQ$ and explain why both give valid signs.',r' $PQ=2\sqrt3-1/2$ m 或 $2\sqrt3+1/2$ m；两种均有效。',[
r'设 $PQ=x$。余弦定理为 $17/4=16+x^2-8x\cos(\pi/6)$，即 $x^2-4\sqrt3x+47/4=0$。',r'配方得 $(x-2\sqrt3)^2=1/4$，故两根为 $2\sqrt3\pm1/2$。',r'两正根都满足三角形不等式；$CQ=\sqrt{17}/2<PC=4$，所以两种设计的T均在线段CP内部。',r'由两根各求得的角 $PCQ$ 均在 $(0,\pi)$，相应大扇形与三角形可位于共边的两侧，不能无理由删去一根。'],[('M','正确建立逆向余弦定理二次方程'),('M','正确解出两根'),('A','两条精确长度正确'),('B','验证三角形及T在线段内'),('B','解释两种角及大扇形均有效')]),
p(r'Determine which sign has the greater area and which has the greater perimeter. Give each area and perimeter to 3 significant figures, but use unrounded values to make your comparisons.',fr'$PQ=2\sqrt3-1/2$ 的面积及周界都较大；两方案面积依次为 ${design[0][2]:.3g},\ {design[1][2]:.3g}\text{{ m}}^2$，周界依次为 ${design[0][3]:.3g},\ {design[1][3]:.3g}$ m。',[
r'对每个x分别由余弦定理求 $\theta=\angle PCQ$，而不是把一组角代入另一组。',r'总面积 $A=\frac{17}{8}(2\pi-\theta)+x$；外周界 $P=(\sqrt{17}/2)(2\pi-\theta)+x+4-\sqrt{17}/2$。',fr'当 $x=2\sqrt3-1/2$：$\theta={design[0][1]:.9f}\ldots$，$A={design[0][2]:.9f}\ldots$，$P={design[0][3]:.9f}\ldots$。',fr'当 $x=2\sqrt3+1/2$：$\theta={design[1][1]:.9f}\ldots$，$A={design[1][2]:.9f}\ldots$，$P={design[1][3]:.9f}\ldots$。',r'按未舍入值比较：较短PQ的方案两项都较大；周界在3位有效数字下会相同，不能据此判为实际相等。'],[('M','分别求两种圆心角'),('M','构造正确总面积'),('M','排除共边并构造正确完整周界'),('A','两组数值及精度正确'),('B','用未舍入值作出两个正确比较')])],
'G1','P1-2025-06A-Q09','三角形与大扇形标志：求半径、证明角度、求总面积与周界',
['设问角度','求解目标','条件呈现','题目结构','收尾要求'], '三角形确定大扇形角及共边之外的外周界', '把已知半径改为反求两种三角形设计，并比较舍入后周界相同但实际不同的两种有效方案', ['给定半径和角不保证PQ唯一。','较长的PQ并不保证整体周界更长；3位有效数字相同不能判相等。'], '逆向余弦双解及两种大扇形设计比较')

# G4: proof of a perimeter bound and a root rejected by geometric validity.
add(23,'环形面积弧差约束下的周界下界',
r'An annular sector has inner radius $r$ cm, outer radius $R$ cm and angle $\theta$ radians, where $0<r<R$ and $0<\theta<\pi$. Its area is $30\text{ cm}^2$ and its outer arc is $6$ cm longer than its inner arc. Its complete perimeter is $P$ cm.',[
p(r'Show that $R+r=10$ and that $P=10\theta+12/\theta$. State the possible range of $\theta$.',r'$R+r=10$；$P=10\theta+12/\theta$；$3/5<\theta<\pi$.',[
r'弧长差给 $(R-r)\theta=6$。面积差给 $\frac12(R-r)(R+r)\theta=30$，故 $R+r=10$。',r'令宽度 $w=R-r=6/\theta$。完整周界含两弧和两宽度，故 $P=(R+r)\theta+2w=10\theta+12/\theta$。',r'$r=(10-w)/2>0$ 要求 $w<10$，故 $\theta>3/5$；并与题设minor范围相交。'],[('M','结合面积差和弧长差'),('A','正确求出半径和'),('M','完整周界表达式正确'),('A','有效角度范围正确且严格')]),
p(r'Prove that $P\ge4\sqrt{30}$ and find the radii and angle when equality holds.',r'等号时 $\theta=\sqrt{6/5}$，$R=(10+\sqrt{30})/2$，$r=(10-\sqrt{30})/2$.',[
r'由于 $\theta>0$，$P-4\sqrt{30}=10(\theta-\sqrt{6/5})^2/\theta\ge0$。',r'等号当且仅当 $\theta=\sqrt{6/5}$，此时宽度 $w=6/\theta=\sqrt{30}$。',r'由和与差求两半径；$0<r<R$ 且 $3/5<\sqrt{6/5}<\pi$，所以下界确可达到。'],[('M','利用非负平方证明周界下界'),('A','取得等号时角及半径'),('B','核查等号设计确在几何有效范围内')]),
p(r'When $P=26$, find every valid design. Explain why any other algebraic solution is rejected.',r'$\theta=2,\ r=7/2,\ R=13/2$；$\theta=3/5$使内半径为0，舍去。',[
r'$10\theta+12/\theta=26$ 化为 $(5\theta-3)(\theta-2)=0$。',r'当 $\theta=3/5$ 时宽度为10而半径和也为10，故r=0，已不是环形扇区。',r'当 $\theta=2$ 时宽度为3，得 $r=7/2,R=13/2$；各约束均满足。'],[('M','找全角度的两个代数根'),('B','用r=0明确舍去边界根'),('A','给出唯一有效设计')])],
'G4','P1-2023-10-Q09','环形扇区由内弧确定内半径，再由面积建立宽度二次方程并求完整周界',
['设问角度','求解目标','条件呈现','参数化与分类讨论','收尾要求'], '环形面积差、内外弧长及两条径向宽度', '由面积和弧差提取不变量，证明可达到的周界下界，并排除二次方程的退化几何根', ['r=0的根虽满足形式方程，却不满足annular sector。','完整周界中的两条径向边长度是R−r，不是R。'], '环形不变量与周界下界及退化解排除')

# G2: a compact six-mark inverse question based on an actual five-mark opener.
add(25,'精确周界逆求与小扇形舍根',
r'A minor sector has area $15\text{ cm}^2$ and perimeter $13\sqrt6/2$ cm. Its radius is $r$ cm and its angle is $\theta$ radians, where $r>0$ and $0<\theta<\pi$.',[
p(r'Find the exact values of $r$ and $\theta$, explaining why there is only one admissible sector.',r'$r=2\sqrt6\text{ cm},\quad\theta=5/4$.',[
r'联立 $\frac12r^2\theta=15$ 与 $r(2+\theta)=13\sqrt6/2$。',r'消去角后得 $2r^2-(13\sqrt6/2)r+30=0$。',r'两正半径为 $2\sqrt6$ 和 $5\sqrt6/4$，均须先保留。',r'分别代回面积条件，角为 $5/4$ 和 $16/5$。',r'$16/5=3.2>\pi$，不满足minor条件；$5/4\in(0,\pi)$，故只保留第一组。'],[('M','正确建立两条件'),('M','消元得到二次方程'),('M','解出两个半径'),('A','两组精确半径角配对正确'),('B','以θ>π舍去第二组'),('A','给出唯一有效的精确答案')])],
'G2','P1-2019-10-Q01','由已知扇形角和面积求精确半径，再求最简精确周界',
['设问角度','求解目标','条件呈现','题目结构','收尾要求'], '精确根式运算、扇形面积与完整周界', '撤去已知角，反用两个整体量重建所有解，再用minor条件保留唯一解', ['两个半径都是正数，因此不能用“半径正”作为唯一舍根理由。','平方根及θ必须一一配对，不能从不同方案拼接答案。'], '精确整体量逆求及大角伪解排除')

# G3: both SSA choices and an exact comparison, retaining the source's real difficulty.
K=6*math.pi+9*math.sqrt(3)/4;L=4*math.pi+8
add(30,'大弓形与两种三角形的精确比较',
r'A circle has centre $O$, radius $3$ cm and chord $AB=3\sqrt3$ cm. Triangle $ABC$ lies on the opposite side of $AB$ from $O$, with $BC=8$ cm and $\angle ACB=\pi/6$. There is no further restriction on the position of $C$. A region is formed by joining triangle $ABC$ to the major segment bounded by $AB$ and the major arc $AB$.',[
p(r'Find both possible exact areas of the region. Make clear why both triangles must be considered.',r'$\displaystyle 6\pi+\frac{41\sqrt3}{4}\pm2\sqrt{11}\text{ cm}^2$.',[
r'余弦定理在圆心三角形给 $\cos\angle AOB=(9+9-27)/18=-1/2$，故小圆心角为 $2\pi/3$。',r'大弓形面积为大扇形加中心三角形：$K=\frac12(9)(4\pi/3)+\frac12(9)\sin(2\pi/3)=6\pi+9\sqrt3/4$。',r'令 $AC=x$。在ABC内以C为夹角用余弦定理：$27=x^2+64-8\sqrt3x$。',r'解得 $x=4\sqrt3\pm\sqrt{11}$。两者均为正且满足三角形不等式；题目未规定A为锐角，不能删去一种。',r'三角形面积 $\frac12(8)x\sin(\pi/6)=2x$。',r'总面积 $K+2x=6\pi+41\sqrt3/4\pm2\sqrt{11}$。'],[('M','由弦反求正确小圆心角'),('M','大弓形须用大扇形加三角形'),('A','大弓形精确面积正确'),('M','正确建立SSA的边长二次方程'),('M','取得两个可能边长'),('B','解释两三角形均有效'),('M','将三角形与大弓形面积相加'),('A','两种精确面积正确')]),
p(r'Determine which design has the greater ratio of area to perimeter. Prove your conclusion without using rounded values.',r'$AC=4\sqrt3+\sqrt{11}$ 的设计面积/周界比更大。',[
r'外周界不含公共弦AB，故 $P=4\pi+8+x=L+x$；面积为 $K+2x$。',r'设两边长为 $x_+>x_-$。两个比相减的分子为 $(x_+-x_-)(2L-K)$，分母为 $(L+x_+)(L+x_-)>0$。',r'$2L-K=2\pi+16-9\sqrt3/4>0$，例如用 $\sqrt3<2$ 即得严格正下界。',r'因此较大的x对应较大的面积/周界比，结论不依赖任何舍入。'],[('M','建立正确的完整周界和面积比'),('M','作精确交叉相乘比较'),('B','证明比较式严格为正'),('A','正确判定设计')])],
'G3','P1-2022-10-Q08','大扇形、中心三角形及外接三角形：精确弧形量、弦长和正弦定理组合面积',
['设问角度','求解目标','条件呈现','题目结构','参数化与分类讨论','收尾要求'], '弦确定圆心角、大扇形面积与SSA三角形的组合', '撤掉四问脚手架并保留SSA的两种真实三角形，再将求值升级为面积与周界比的精确证明', ['大弓形等于大扇形加三角形，不能相减。','没有图示额外限制时，SSA的两根均要检验，不能默认只用较大的三角形。'], '两种SSA大弓形设计的精确比值证明')

# G6: three distinct routes share one legitimate coordinate-sector source (cap = 3).
theta=math.atan(2/3);radius=13;cb=3*math.sqrt(13)
area31=.5*169*theta-21;per31=6+math.sqrt(40)+(13-cb)+13*theta
add(31,'坐标半径比逆求与扇形区域比较',
r'The line $l_1$ passes through $A(0,6)$ and $B(b,2)$, where $b>0$. The line $l_2$ is perpendicular to $l_1$ at $B$ and meets the $y$-axis at $C$. A circle with centre $C$ passes through $A$, and the ray $CB$ meets the circle at $D$. Given that $CB:CA=3:\sqrt{13}$, and that $O$ is the origin.',[
p(r'Find $b$, the coordinates of $C$ and an equation of $l_2$.',r'$b=6,\ C=(0,-7),\ l_2:y-2=\frac32(x-6)$.',[
r'$l_1$斜率为 $-4/b$，故 $l_2:y-2=(b/4)(x-b)$，$C=(0,2-b^2/4)$。',r'$CA=4+b^2/4=(b^2+16)/4$，而 $CB=b\sqrt{b^2+16}/4$。',r'由 $CB/CA=b/\sqrt{b^2+16}=3/\sqrt{13}$，得 $13b^2=9b^2+144$。',r'因b>0，取b=6；所以 $C=(0,-7)$，垂线方程为 $y-2=3(x-6)/2$。'],[('M','正确构造垂线及其截距'),('M','由坐标表达两长度'),('M','正确使用半径比消元'),('A','取得正b及正确C'),('A','垂线方程正确')]),
p(r'The region bounded by $OA$, $OB$, $BD$ and the minor arc $DA$ has perimeter $P$ and area $S$. Find $P$ to 3 significant figures and determine whether $S$ is greater than half the area of the sector $ACD$.',fr'$P={per31:.3g}$；$S={area31:.6f}\ldots$，大于扇形面积的一半。',[
r'由坐标得 $CA=13,CB=3\sqrt{13}$；$\tan\theta=6/9=2/3$，其中 $\theta=\angle ACD$。',r'外周界为 $6+\sqrt{40}+(13-3\sqrt{13})+13\theta$，不含内部的OC和CB。',r'扇形面积 $=169\theta/2$；三角形OCB面积 $=7\times6/2=21$。目标面积是扇形减该三角形。',fr'于是 $S={area31:.8f}\ldots$；半个扇形面积 ${169*theta/4:.8f}\ldots$，所以S较大。'],[('M','正确构造角、半径及BD'),('M','外周界四段正确'),('A','周界数值及精度正确'),('M','不靠题干提示重建面积差'),('A','正确比较与半个扇形面积的大小')])],
'G6','P1-2021-06-Q07','直线截距与垂线重建半径，求扇形弧长及坐标三角形的精确组合面积',
['设问角度','条件呈现','求解目标','题目结构','跨考点耦合'], '垂线、坐标长度、弧度角及扇形与三角形的面积组合', '由几何长度比反推未知横坐标，撤去长度与面积拆分提示，再作面积比例判断', ['CB不是圆半径，B在圆内而D在圆上。','不能沿用来源的面积相加：本题的目标区域须减去OCB。'], '坐标长度比反求后构造弧形边界')

# G2: a proof about arbitrary angle and equal region perimeters.
add(32,'等周界分区的存在范围与面积证明',
r'A sector $OAB$ has radius $r>0$ and angle $\theta$ radians, where $0<\theta<\pi$. A point $P$ lies strictly between $O$ and $B$. The line $AP$ divides the sector into triangle $OAP$ and a curved region. The two regions have equal perimeters.',[
p(r'Show that such a point $P$ exists if and only if $0<\theta<2$.',r'$OP=r\theta/2$；严格在线段内当且仅当 $0<\theta<2$.',[
r'令 $OP=x$。三角形周界为 $r+x+AP$，曲边区域周界为 $r\theta+(r-x)+AP$。',r'两周界相等，共用的AP抵消，得 $2x=r\theta$。',r'$P$严格在线段内要求 $0<x<r$，等价于 $0<\theta<2$；满足此范围时取 $x=r\theta/2$ 即能构造P，故必要性和充分性均成立。'],[('M','正确写出两区周界'),('M','消去共边得到OP'),('A','证明必要且充分的严格范围')]),
p(r'For all the valid values of $\theta$, prove that the curved region has area at least as great as that of the triangle. Find the value of $\theta$ when the two areas are equal.',r'曲边区域面积不小于三角形；等号当且仅当 $\theta=\pi/2$.',[
r'三角形面积 $T=\frac12rx\sin\theta=\frac14r^2\theta\sin\theta$。',r'扇形面积为 $F=\frac12r^2\theta$，所以 $T/F=\sin\theta/2\le1/2$。',r'曲边区域为 $F-T$，故 $F-T\ge T$。',r'等号要求 $\sin\theta=1$；在 $0<\theta<2$ 中唯一为 $\theta=\pi/2$，且确满足存在范围。'],[('M','用等周界条件表达三角形面积'),('A','正确取得三角形占扇形的比例'),('M','利用sinθ≤1证明两区面积次序'),('A','等号角及有效性正确')])],
'G2','P1-2024-10-Q05','扇形被直线分区：给定面积比反求分割点及分割线长度',
['设问角度','求解目标','条件呈现','参数化与分类讨论','题目结构','收尾要求'], '扇形和三角形分区的面积与真实边界', '用等周界的隐含条件替代已知面积比，证明分割点存在的充要条件，并对全部有效角证明面积次序及等号情形', ['共边AP在比较周界时抵消，但不能从每区周界中直接漏掉。','θ=2时P=B，违反strictly between，不能包括端点。'], '等周分区的充要范围与面积次序证明')

# G5: infer the repetition count from circular geometry before reconstructing cutouts.
rho=6*math.sqrt(1-3*math.sqrt(3)/(2*math.pi));p34=rho*(6+math.pi)
add(34,'弧弦交替图形的单元数逆求',
r'A shape is cut from a circular disc of radius $r$ cm. Its outside boundary consists of $n$ equal minor arcs alternating with $n$ equal chords, all with endpoints on the disc. The arcs and chords occur in this order around the circumference, and the cut-outs are the minor segments between the chords and the original circle. Each chord has length $r$. The total length of the retained arcs is half the circumference of the original disc. The perimeter of the shape is $(6\pi+18)$ cm.',[
p(r'Show that $n=3$ and find $r$.',r'$n=3,\quad r=6\text{ cm}$.',[
r'弦与两半径形成等边三角形，所以每个切去弓形对应小圆心角为 $\pi/3$。',r'保留弧占半周，剩下的n段被弦替代的原弧也占半周，因此 $n(\pi/3)=\pi$，得n=3。',r'保留弧总长 $\pi r$，三条外露弦共长3r；没有外露的半径边。',r'由 $r(\pi+3)=6\pi+18$ 得r=6。'],[('B','由弦等于半径得π/3'),('M','利用半周条件确定单元数'),('M','正确建立弧与弦组成的外周界'),('A','取得n和正半径')]),
p(r'Three congruent minor sectors, each of angle $\pi/3$, have total area equal to the material removed from the disc. Find the sum of their perimeters, giving your answer to 3 significant figures.',fr'${p34:.3g}$ cm。',[
r'被切去总面积为 $3[\frac12(6)^2(\pi/3-\sin(\pi/3))]=18\pi-27\sqrt3$。',r'设新扇形半径为ρ，三扇形总面积为 $3(\frac12\rho^2\pi/3)=\pi\rho^2/2$。',r'令面积相等，得 $\rho=6\sqrt{1-3\sqrt3/(2\pi)}$，取正根。',r'三个扇形是三个独立图形，须各计两条半径；总周界 $=3\rho(2+\pi/3)=\rho(6+\pi)$。',fr'代入未舍入的半径得 ${p34:.8f}\ldots$ cm，取3位有效数字。'],[('M','正确构造重复弓形的移除总面积'),('A','精确移除面积正确'),('M','从相等面积逆求新正半径'),('M','计入三个独立扇形的全部径向边'),('A','总周界数值及精度正确')])],
'G5','P1-2022-06-Q08','重复圆弧单元组成的风扇：整周关系、外边界和重复单元总面积',
['设问角度','条件呈现','求解目标','题目结构','跨考点耦合','收尾要求'], '重复单元的整周分配、圆弧与径向边界和面积', '先由弦长及半周条件反推单元数量，再将切除弓形总面积逆向转成独立扇形的完整周界', ['原图形的圆心连线都是内部辅助线，不能加进周界。','新扇形互相独立，六条半径必须计入，不能沿用原图的边界规则。'], '弧弦交替单元逆求后由切除面积重构独立扇形')

# NEW R37: clipping a coordinate sector; no repetition of the inverse length-ratio route.
u=math.acos(2/3);cap=1250*u/9-2500*math.sqrt(5)/81
add(37,'坐标扇形的截轴临界角与面积',
r'The line $l_1$ has equation $3x+4y=4a$, where $a$ is a positive constant. It meets the $y$-axis at $C$. The point $D(8,a-6)$ lies on $l_1$. The line $l_2$ is perpendicular to $l_1$ at $D$ and meets the $y$-axis at $E$. The origin $O$ lies strictly between $E$ and $C$. The area of triangle $ODE$ is one third of the area of triangle $CDE$.',[
p(r'Find $a$ and the radius of the circle with centre $C$ passing through $E$.',r'$a=100/9$，半径 $CE=50/3$.',[
r'垂线斜率为4/3，故 $l_2:y-(a-6)=4(x-8)/3$，$E=(0,a-50/3)$；$C=(0,a)$。',r'因此 $CE=50/3$ 与a无关。两三角形以y轴上的边为底，同高8，面积比等于 $OE:CE$。',r'因E在原点下方，$OE=50/3-a$；由 $(50/3-a)/(50/3)=1/3$，得 $a=100/9$。',r'验证 $E_y=-50/9<0<C_y=100/9$，半径为50/3。'],[('M','求垂线的截距'),('A','取得不随a改变的半径'),('M','以共同高把面积比转为有向长度条件'),('A','解得a并核对原点位置')]),
p(r'A sector with centre $C$ and radius $CE$ lies to the left of the $y$-axis. Starting from ray $CE$, its angle is $\theta$ radians, where $0<\theta<\pi$. Find the least value of $\theta$ for which this sector contains the whole part of the left half-disc lying below the $x$-axis. Find the area of that part, giving your answer to 3 significant figures.',fr'最小角 $=\cos^{{-1}}(2/3)={u:.6f}\ldots$ rad；面积 ${cap:.3g}$ 平方单位。',[
r'设圆与负x轴交于X。临界位置是扇形末端半径CX恰经过X；在这之后，左半圆盘中x轴以下的部分全部包含在扇形内。',r'$\cos\angle ECX=CO/CE=(100/9)/(50/3)=2/3$，故最小角为 $u=\cos^{-1}(2/3)$。',r'横向距离 $OX=\sqrt{(50/3)^2-(100/9)^2}=50\sqrt5/9$。',r'目标区域面积为扇形CEX减三角形COX，即 $\frac12(50/3)^2u-\frac12(100/9)(50\sqrt5/9)$。',fr'所得面积 $={cap:.8f}\ldots$ 平方单位；临界角属于(0,π)，可实际达到。'],[('B','识别临界半径经过负x轴交点'),('M','通过坐标垂距构造临界角'),('A','临界角及可达到性正确'),('M','自行构造扇形减三角形的截轴面积'),('A','面积与3位有效数字正确')])],
'G6','P1-2021-06-Q07','坐标直线及垂线截距确定扇形半径，求弧长与组合区域精确面积',
['设问角度','求解目标','条件呈现','参数化与分类讨论','题目结构','收尾要求'], '坐标截距和垂线重建半径，再将扇形与三角形面积相连', '由三角形面积比反求平移参数，再构造扇形包含截轴区域的最小角及截轴面积', ['E_y为负，OE=−E_y，不能把有向坐标直接当长度。','x轴下方区域是扇形减三角形，不是半个整扇形。'], '坐标面积比反求与截轴包含临界角')

# NEW R38: parameter minimum proved without calculus, then a cancellation in the boundary.
add(38,'含参垂线的最小半径与剩余边界',
r'The line $l_1$ passes through $A(0,a)$ and $D(6,2)$, where $a>2$. The line $l_2$ is perpendicular to $l_1$ at $D$ and meets the $y$-axis at $E$. The origin $O$ lies strictly between $E$ and $A$. A circle with centre $E$ passes through $A$.',[
p(r'Find the permitted range of $a$. Without differentiation, prove that the circle has radius at least $12$, and find $a$ when equality holds.',r'$2<a<20$；半径 $\ge12$，等号当 $a=8$.',[
r'令 $t=a-2>0$。垂线斜率为 $6/t$，故 $E_y=2-36/t$。',r'原点在线段EA内部要求 $E_y<0$，因此 $t<18$，即 $2<a<20$。',r'半径 $EA=a-E_y=t+36/t$。',r'因为 $t>0$，$EA-12=(t-6)^2/t\ge0$；不需要用微分。',r'等号在t=6即a=8成立，且该a在允许区间内。'],[('M','正确表达垂线截距'),('A','求出严格参数范围'),('M','正确构造半径的含参表达式'),('M','用非负平方证明最小值'),('A','等号参数及有效性正确')]),
p(r'For this minimum-radius circle, ray $ED$ meets the circle at $B$. A region is bounded by $AD$, $DB$ and the minor arc $BA$. Find the exact area and perimeter of this region.',r'面积 $18\pi-36$ 平方单位；周界 $12+3\pi$ 单位。',[
r'此时 $A=(0,8),E=(0,-4),D=(6,2)$，$EA=12$；ED方向的横纵增量均为6，所以 $\angle AEB=\pi/4$。',r'扇形面积 $=\frac12(12)^2(\pi/4)=18\pi$。三角形AED面积 $=\frac12(12)(6)=36$；目标为两者之差。',r'$AD=ED=6\sqrt2$；D在圆内，故 $DB=12-6\sqrt2$。',r'周界三段之和 $AD+DB+\text{arc }BA=6\sqrt2+(12-6\sqrt2)+12(\pi/4)=12+3\pi$。'],[('B','由坐标确定π/4角'),('M','构造正确的面积差'),('A','精确面积正确'),('M','用D在圆内识别DB并构造边界'),('A','化简得到精确周界')])],
'G6','P1-2021-06-Q07','直线与垂线的截距给出扇形半径，再求圆弧与三角形组合面积',
['设问角度','求解目标','条件呈现','参数化与分类讨论','题目结构','收尾要求'], '垂直斜率、截距、圆半径和三角形与扇形的组合', '把固定直线改为几何有效区间中的参数族，用平方证明最小半径，再自行确定圆内线段和弧形剩余边界', ['必须先验证t>0才能将非负平方除以t。','DB=EB−ED，不能把ED直接作为外边界。'], '坐标参数族的无微分最小半径证明')

# Seven cores approved for retention/local editing, not a re-authoring shortcut.
families={3:'G3',7:'G3',11:'G1',21:'G3',24:'G1',28:'G5',33:'G4'}
templates={3:'面积比隐式方程与弧弦无量纲比',7:'同弦异圆反求半径与弓形比较',11:'面积比反求半径并证明整扇形内含',21:'大小弓形周界差证明及面积周界比比较',24:'内扇形包含条件与相切极限',28:'重复环形叶片的最大整数数量',33:'面积周界逆求两种环形设计'}
for n,f in families.items():
 q=copy.deepcopy(OLD[fr'P1-C07-R{n:02d}']);q['editorialRevision']=q['solutionRevision']=16;q['examFamily']=f;q['questionTemplate']=templates[n];q['contentUpdatedAt']='2026-10-24'
 if n==3:
  q['stem']=q['stem'].replace('radius $r$','radius $r$ cm, where $r>0$,')
  q['parts'][2]['answer']=r'$19.0\text{ cm}^2$.'
 if n in (7,21):
  q['sourceReferences']=[dict(questionId='P1-2022-01-Q05',year=2022,note='半圆弓形：证明圆心角、求弓形面积和弦弧周界')]
  q['sourceSummary']='半圆内给定边角关系求圆心角，再求弓形面积和含弦周界'
  if n==7:
   q['parts'][2]['answer']=r'半径 $19.0$ cm（3 s.f.）；第一个小弓形面积较大（$16.4>7.83$）。'
   q['parts'][2]['text']=q['parts'][2]['text'].replace('Find the radius of the second circle','Find the radius of the second circle to 3 significant figures')
   inc='由弦逆求角，再对同一弦在第二个圆中的半角构造反求新半径，比较两弓形'
  else:
   inc='由弦逆求角，证明同弦大小弓形的周界差，并比较面积比与周界比'
  q['difficultyPosition']='略难于 P1-2022-01-Q05：'+inc
  q['adaptationDimensions']=['设问角度','求解目标','条件呈现','收尾要求']
  q['adaptationNote']='变式来源已按本轮审查更正；改编维度：设问角度、求解目标、条件呈现、收尾要求。思维增量：'+inc+'。'
  q['designNote']=inc+'；不将半角的范围选择误称为正弦定理SSA钝角取舍。'
 if n==28:q['parts'][1]['text']+=' Give your answer to 3 significant figures.'
 if n==33:
  q['parts'][2]['scheme']=[dict(code='M1',marks=1,text='用2rθ表达并比较两外弧'),dict(code='A1',marks=1,text='两外弧和精确差值20/3正确'),dict(code='B1',marks=1,text='说明较大r对应的θ下降使乘积更小')]
  q['parts'][2]['marks']=3;q['marks']=8
  q['parts'][2]['answer']=r'$r=3$的设计外弧较长，相差 $20/3$ cm。$r=8$的设计角较小，因此其外弧较短。'
 Q.append(q)

Q.sort(key=lambda q:q['originalNumber'])
assert len(Q)==21
from collections import Counter
assert Counter(q['examFamily'] for q in Q)==dict(G1=5,G2=3,G3=4,G4=3,G5=3,G6=3)
assert max(Counter(q['sourceReferences'][0]['questionId'] for q in Q).values())<=3
for q in Q:
 assert len(q['adaptationDimensions'])>=3
 assert q['marks']==sum(p['marks'] for p in q['parts'])
 assert all(p['marks']==sum(s['marks'] for s in p['scheme']) for p in q['parts'])
 assert all(ord(c)>=32 or c in '\n\t' for c in json.dumps(q,ensure_ascii=False))
pages={'P1-2024-06R-Q06':12,'P1-2024-01-Q08':18,'P1-2022-06-Q08':22,'P1-2019-01-Q10':20,'P1-2021-01-Q05':14,'P1-2025-06A-Q09':26,'P1-2023-10-Q09':24,'P1-2019-10-Q01':2,'P1-2022-10-Q08':20,'P1-2021-06-Q07':22,'P1-2024-10-Q05':14,'P1-2022-01-Q05':12,'P1-2024-06-Q05':10,'P1-2020-10-Q03':8}
for q in Q:
 ref=q['sourceReferences'][0];_,year,month,_=ref['questionId'].split('-')
 suffix='-r' if 'R' in month else '-a' if 'A' in month else ''
 mon={'01':'jan','06':'jun','10':'oct'}[month[:2]]
 ref['paperPdf']=f'assets/past-papers/p1-{mon}-{year}{suffix}.pdf#page={pages[ref["questionId"]]}'
 ref['markSchemePdf']=f'assets/past-papers/p1-{mon}-{year}{suffix}-ms.pdf'
(OUT/'p1-radians.json').write_text(json.dumps({'version':16,'questions':Q},ensure_ascii=False,indent=2)+'\n')
print('V16 authored',len(Q),'questions;',dict(Counter(q['marks'] for q in Q)),'total marks',sum(q['marks'] for q in Q))
