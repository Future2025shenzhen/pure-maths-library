"""Accurate monochrome original diagrams. Do not label unknown answers."""
import math,json,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'dist/assets/v16-figures';DEST.mkdir(exist_ok=True)
def svg(name,paths,labels,view='0 0 560 330'):
 body='<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+view+'" role="img" aria-label="'+html.escape(name)+'"><title>'+html.escape(name)+'</title><g fill="none" stroke="#222" stroke-width="1.5" stroke-linejoin="round">'+''.join(paths)+'</g><g fill="#111" font-family="Georgia,serif" font-size="17">'+''.join(f'<text x="{x:.2f}" y="{y:.2f}">{html.escape(t)}</text>' for x,y,t in labels)+'</g></svg>'
 return body
def line(a,b,dash=False):return f'<path d="M{a[0]:.3f},{a[1]:.3f}L{b[0]:.3f},{b[1]:.3f}"'+(' stroke-dasharray="5 4"' if dash else '')+'/>'
def poly(points,close=False,shade=False):return '<path d="'+'M'+'L'.join(f'{x:.3f},{y:.3f}' for x,y in points)+('Z' if close else '')+'"'+(' fill="#f1f1f1"' if shade else '')+'/>'
def arc(c,r,a,b):
 pts=[(c[0]+r*math.cos(a+(b-a)*i/160),c[1]-r*math.sin(a+(b-a)*i/160)) for i in range(161)]
 return poly(pts)
def pt(c,r,t):return(c[0]+r*math.cos(t),c[1]-r*math.sin(t))
def write(n,paths,labels,name):
 f=DEST/f'p1-c07-r{n:02d}.svg';f.write_text(svg(name,paths,labels));return f'assets/v16-figures/{f.name}'
figs={}
# R01: exact first design only; no second-design solution is shown.
c=(280,270);r=155;B=pt(c,r,2*math.pi/3);C=pt(c,r,math.pi/3);A=(125,270);D=(435,270)
figs[1]=write(1,[line(A,B),arc(c,r,math.pi/3,2*math.pi/3),line(C,D),line(D,A),line(c,B,True),line(c,C,True)],[(105,292,'A'),(274,294,'O'),(440,292,'D'),(B[0]-20,B[1]-8,'B'),(C[0]+8,C[1]-8,'C'),(180,315,'x'),(360,315,'x'),(267,235,'π/3'),(169,192,'r'),(389,192,'r')],'Symmetric sector and two congruent triangles')
# R02: outer small sector and inner major sector, not an annular wedge.
c=(260,165);ri=80;ro=150;t=math.pi/6
ia=pt(c,ri,-t);ib=pt(c,ri,t);oa=pt(c,ro,-t);ob=pt(c,ro,t)
figs[2]=write(2,[arc(c,ri,t,2*math.pi-t),arc(c,ro,-t,t),line(ia,oa),line(ib,ob),line(c,oa,True),line(c,ob,True),line(ia,ib,True)],[(250,188,'O'),(292,115,'r'),(350,220,'2r'),(285,170,'θ'),(340,45,'longer-radius arc')],'Different-radius sectors joined on two common rays')
# R08: two representative cells only; an actual full fan would reveal n.
c=(150,265);small=50;large=210;al=.40;be=.72
paths=[]
for start in (0,al+be):
 paths.extend([arc(c,small,start,start+al),line(pt(c,small,start+al),pt(c,large,start+al)),arc(c,large,start+al,start+al+be),line(pt(c,large,start+al+be),pt(c,small,start+al+be))])
paths.extend([line(c,pt(c,small,0),True),line(c,pt(c,large,al+be),True),line(c,pt(c,large,2*(al+be)),True)])
figs[8]=write(8,paths,[(134,288,'O'),(210,275,'2 cm'),(270,165,'8 cm'),(191,246,'α'),(222,207,'β'),(310,40,'detail: two adjacent cells')],'Detail of alternating-radius cells, repeated around O')
# R13: choose an admissible d for geometry, but label d, not the derived value.
de=math.pi/6;om=math.pi-math.asin(11/12);dist=12*math.sin(math.pi-om-de);scale=22;c=(220,140);C=pt(c,6*scale,0);D=pt(c,dist*scale,0);A=pt(c,6*scale,om)
figs[13]=write(13,[arc(c,6*scale,om,2*math.pi),line(C,D),line(D,A),line(c,A,True),line(c,C,True)],[(c[0]-8,c[1]-12,'O'),(C[0]-5,C[1]+23,'C'),(D[0]+8,D[1]+12,'D'),(A[0]-20,A[1]-5,'A'),(210,295,'B'),(280,50,'d'),(D[0]-35,D[1]-8,'π/6'),(c[0]+65,c[1]+22,'6 m')],'Major sector joined to a triangle with D beyond C')
# R20: both possibilities are genuine, shown as two unnumbered outlines without solved angles.
rr=math.sqrt(17)/2;pc=4;paths=[];labels=[]
for k,x in enumerate((2*math.sqrt(3)-.5,2*math.sqrt(3)+.5)):
 c=(195+k*265,170);sc=45;P=(c[0]-pc*sc,c[1]);Q=(P[0]+x*math.cos(math.pi/6)*sc,P[1]-x*.5*sc);T=(c[0]-rr*sc,c[1]);ang=math.atan2(c[1]-Q[1],Q[0]-c[0])
 paths.extend([arc(c,rr*sc,math.pi,2*math.pi+ang),line(P,Q),line(P,T),line(c,Q,True),line(c,T,True)])
 labels.extend([(P[0]-8,P[1]+22,'P'),(c[0]-5,c[1]+22,'C'),(T[0]-2,T[1]+22,'T'),(Q[0]-12,Q[1]-9,'Q')])
# Wider viewport: prevent P in left panel being cut off.
figs[20]=write(20,paths,labels,'Two possible signs; neither triangle is selected in advance')
# R30: show both possible C positions in an auxiliary triangle, preserving both SSA branches.
sc=20;O=(230,180);theta=2*math.pi/3;A=pt(O,3*sc,theta/2);B=pt(O,3*sc,-theta/2)
# Rotate shared base to horizontal for a clearer major-segment / triangle picture.
A=(180,200);B=(180+3*math.sqrt(3)*sc,200);O=((A[0]+B[0])/2,230)
ra=math.atan2(O[1]-A[1],A[0]-O[0]);rb=math.atan2(O[1]-B[1],B[0]-O[0]);paths=[arc(O,3*sc,ra,rb+2*math.pi),line(A,B,True),line(O,A,True),line(O,B,True)];labels=[(A[0]-15,210,'A'),(B[0]+7,210,'B'),(O[0]-7,O[1]+23,'O')]
for i,x in enumerate((4*math.sqrt(3)-math.sqrt(11),4*math.sqrt(3)+math.sqrt(11))):
 # C is an intersection of circles centred at A (AC=x) and B (BC=8).
 ab=3*math.sqrt(3);cx=(x*x+ab*ab-64)/(2*ab);cy=math.sqrt(x*x-cx*cx);C=(A[0]+sc*cx,A[1]-sc*cy)
 paths.extend([line(A,C,bool(i)),line(B,C,bool(i))]);labels.append((C[0]-8,C[1]-8,'C₁' if i==0 else 'C₂'))
figs[30]=write(30,paths,labels,'Major segment with two admissible external triangles')
# R31 / R38: same line family, distinct question, with answers left unlabelled.
def coord(n,a,b,dy,c_y,name):
 sc=15;ox=150;oy=210
 def q(x,y):return(ox+x*sc,oy-y*sc)
 A=q(0,a);D=q(b,dy);E=q(0,c_y);rad=a-c_y;vec=(b,dy-c_y);length=math.hypot(*vec);BB=q(rad*vec[0]/length,c_y+rad*vec[1]/length);ang=math.atan2(vec[1],vec[0]);paths=[line(q(-3,0),q(13,0)),line(q(0,-8),q(0,12)),line(A,D,n==31),line(D,E),arc(E,rad*sc,ang,math.pi/2),line(D,BB),line(A,E,True)]+([line(q(0,0),D)] if n==31 else []);labels=[(A[0]-22,A[1]-6,'A'),(E[0]-24,E[1]+6,'C' if n==31 else 'E'),(D[0]-8,D[1]+22,'B' if n==31 else 'D'),(BB[0]+8,BB[1],'D' if n==31 else 'B'),(ox-20,oy+20,'O'),(ox+203,oy+20,'x'),(ox+8,25,'y')];return write(n,paths,labels,name)
figs[31]=coord(31,6,6,2,-7,'Coordinate circle sector, B inside the circle')
figs[38]=coord(38,8,6,2,-4,'Perpendicular lines and a circle with centre on the y-axis')
# R32: illustrative valid θ, no angle/radius answers are labelled.
c=(140,265);r=220;ang=1.1;A=pt(c,r,ang);B=pt(c,r,0);P=pt(c,r*.55,0)
figs[32]=write(32,[arc(c,r,0,ang),line(c,A),line(c,B),line(A,P)],[(123,287,'O'),(A[0]-16,A[1]-8,'A'),(B[0]+8,B[1]+10,'B'),(P[0]-5,P[1]+22,'P'),(179,245,'θ'),(178,160,'r')],'Sector divided by AP into a triangle and a curved region')
# R34: one local arc/chord detail, so the unknown repetition count is not revealed.
c=(200,220);r=150;A=pt(c,r,0);B=pt(c,r,math.pi/3);C=pt(c,r,2*math.pi/3)
figs[34]=write(34,[line(A,B),arc(c,r,math.pi/3,2*math.pi/3),line(c,A,True),line(c,B,True)],[(185,244,'centre'),(A[0]+6,A[1]+8,'r'),(290,150,'chord r'),(162,50,'retained arc'),(367,290,'local detail only')],'Local chord and adjacent retained arc; total number not shown')
# R37: translate the original line construction; no critical radius is drawn.
sc=9;ox=160;oy=220;a=100/9;cy=a;ey=a-50/3
def q(x,y):return(ox+x*sc,oy-y*sc)
paths=[line(q(-5,0),q(22,0)),line(q(0,-9),q(0,20)),line(q(-4,a+3),q(17,a-12.75)),line(q(-2,ey-8/3),q(18,ey+24))]
figs[37]=write(37,paths,[(q(0,cy)[0]-22,q(0,cy)[1],'C'),(q(0,ey)[0]-22,q(0,ey)[1]+6,'E'),(q(8,a-6)[0]+8,q(8,a-6)[1]-7,'D(8, a−6)'),(ox-21,oy+20,'O'),(ox+207,oy+20,'x'),(ox+10,32,'y'),(320,80,'l₂'),(315,205,'l₁')],'Coordinate lines before constructing the left-hand sector')

doc=json.loads((ROOT/'editorial/v16/p1-radians.json').read_text())
for qu in doc['questions']:
 n=qu['originalNumber']
 if n in figs:qu['stem']+=f'<figure class="rewrite-figure"><img src="{figs[n]}" alt="{html.escape(qu["type"])}" loading="lazy"><figcaption>Diagram not necessarily drawn to scale</figcaption></figure>'
(ROOT/'editorial/v16/p1-radians.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
print('V16 original diagrams',len(figs))
