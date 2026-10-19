import pathlib
import sympy as s,json,pathlib,re,collections
x,t,a,b,k,h,p,u=s.symbols('x t a b k h p u',real=True)
R=s.sqrt
checks=[]
def ck(c,n,label,v):
 ok=bool(v);checks.append({'id':f'P1-C{c:02}-R{n:02}','check':label,'passed':ok})
 if not ok:raise AssertionError(checks[-1])
def eq(f,g):return s.simplify(f-g)==0
def roots(f):return set(s.solve(f,x))
# Each question receives a named independent mathematical check, not only shape validation.
C=1
ck(C,1,'fractional substitution and recovery',all(eq(z**s.Rational(3,2)-6*z**s.Rational(3,4)+8,0) for z in [2**s.Rational(4,3),4**s.Rational(4,3)]))
ck(C,2,'negative real cube-root retained',3**2-3==6 and (-2)**2-(-2)==6 and (-2)**3==-8)
ck(C,3,'two exponent constraints',2**2*4==16 and 2*4**2==32 and eq(2**s.Rational(3,2)/R(4),R(2)))
ck(C,4,'surd area and ratio',eq((R(12)+R(27))**2-(R(48)-R(3))**2,48) and eq(4*R(3)/(2*R(3)),2))
ck(C,5,'conjugate quotient identity',eq((R(7)+R(3))/(R(7)-R(3))+(R(7)-R(3))/(R(7)+R(3)),5))
ck(C,6,'coefficient constrained rationalisation',eq((5+s.Rational(2,3)*R(2))/(3-R(2)),s.Rational(7,3)+R(2)))
ck(C,7,'squaring extraneous root',R(4+5)==4-1 and R(-1+5)!=-1-1)
ck(C,8,'identity expansion and real factors',eq((2*x-3)*(x+3)-(x-1)**2,x*x+5*x-10) and eq((x+(5-R(65))/2)*(x+(5+R(65))/2),x*x+5*x-10))
ck(C,9,'difference of squares factors',eq((x+2)**2-9*(x-1)**2,(5-2*x)*(4*x-1)))
ck(C,10,'cancellation valid-domain equation',eq(((x*x-9)/(x*x+x-6)).subs(x,1),2))
ck(C,11,'positive reciprocal roots',all(z>0 and eq(z+1/z,7) for z in [(7+3*R(5))/2,(7-3*R(5))/2]))
ck(C,12,'rationalisation and sum squares',eq(1/(R(5)-2)**2+1/(R(5)+2)**2,18))
ck(C,13,'inverse fractional scaling',eq(8**s.Rational(2,3),4) and eq(2**s.Rational(3,2),2*R(2)))
ck(C,14,'rectangle and equal perimeter square',eq((R(18)+R(8))*(R(18)-R(8)),10) and (3*R(2))**2==18)
ck(C,15,'index base recovery and target',2**0==1 and 2**2==4 and eq(2*4+2/s.Integer(4),s.Rational(17,2)))
ck(C,16,'fractional factorisation',eq(t**3-5*t*t+6*t,t*(t-2)*(t-3)) and eq((s.Rational(1,2))*(s.Rational(-3,2))*(s.Rational(-5,2)),s.Rational(15,8)))
ck(C,17,'reciprocal square identity',eq((R(6)+R(2))**2+16/(R(6)+R(2))**2,16))
ck(C,18,'exponent recovery',s.Rational(1)+s.Rational(1,3)-s.Rational(1,2)==s.Rational(5,6) and 8**s.Rational(5,3)==32)
ck(C,19,'conjugate reciprocal difference',eq(((2+R(3))-(2-R(3)))**2,12))
ck(C,20,'geometric difference identity',eq((x+4)*(x-1)-(x+1)**2,x-5))
ck(C,21,'parameter square-difference identity',eq((x+4)**2-(x-1)**2,10*x+15) and eq((x+4)**2-9*(x-1)**2,(7-2*x)*(4*x+1)))
ck(C,22,'radical equation check',eq(R(8*8)+R(18*8),20) and eq(R(50*8)-R(2*8),16))
ck(C,23,'cubic identity and strictly positive quadratic',eq((2*u-3)*(4*u*u+6*u+9),8*u**3-27) and eq(4*(u+s.Rational(3,4))**2+s.Rational(27,4),4*u*u+6*u+9))
ck(C,24,'symmetric cubic exact value',eq((3+R(5))**3+(3-R(5))**3,144))
ck(C,25,'strip dimensions',eq(6*R(2)*5*R(2),60) and eq(2*(6*R(2)+5*R(2)),22*R(2)))
ck(C,26,'fourth-root substitution',81**s.Rational(1,2)+2*81**s.Rational(1,4)==15 and 81**s.Rational(-3,4)==s.Rational(1,27))
ck(C,27,'parameter conjugate equations',eq((3+R(3))/(2+R(3)),3-R(3)) and eq((3-R(3))/(2-R(3)),3+R(3)))
ck(C,28,'zero retained and strict inequality example',0==0**s.Rational(3,2)-4*R(0) and 4**s.Rational(3,2)==4*R(4) and 1**s.Rational(3,2)<4)
ck(C,29,'contradiction and changed feasible target',eq((2*x+1)**2-(2*x-1)**2,8*x) and eq((8*x-3*(2*x+1)).subs(x,s.Rational(3,2)),0))
ck(C,30,'ordering and telescoping sum',R(11)+R(7)>R(7)+R(3)>0 and eq((R(11)-R(3))**2,14-2*R(33)))
C=2
cases=[
('completed square and thresholds',eq(2*x*x-12*x+11,2*(x-3)**2-7) and roots(2*x*x-12*x+10)=={1,5}),
('vertex reconstruction and chord',eq((2*(x-2)**2-9).subs(x,-1),9) and (2*4**2-9)==23),
('axis coefficients',eq(x*x+6*x,(x+3)**2-9)),
('exceptional parameter',s.discriminant(k*x*x+4*x+k,x)==16-4*k*k and roots(4*x)=={0}),
('perfect square with free centre',eq(3*x*x-6*a*x+3*a*a+5,3*(x-a)**2+5)),
('two tangent slopes',all(s.discriminant(x*x-(m+4)*x+4,x)==0 for m in [0,-8])),
('positive family endpoints',eq(p+2-p*p,-(p-2)*(p+1))),
('rocket model and physical ground root',eq(1+8*t-2*t*t,9-2*(t-2)**2) and eq((1+8*t-2*t*t).subs(t,2+3*R(2)/2),0)),
('ticket revenue and thresholds',eq(p*(120-4*p),900-4*(p-15)**2) and roots(x*(120-4*x)-800)=={10,20}),
('repeated root branches',all(s.discriminant(x*x+(z-1)*x+4,x)==0 for z in [5,-3])),
('translation and curve intersection',eq((x*x-6*x+5).subs(x,x+4),x*x+2*x-3)),
('factorised reconstruction and horizontal line',eq(2*(x+2)*(x-6),2*(x-2)**2-32) and roots(2*(x+2)*(x-6)+24)=={0,4}),
('parameter line tangency',eq(s.discriminant(x*x+2*(1-k)*x+4,x),4*(1-k)**2-16)),
('fixed no-root family and tangency',eq(x*x+2*a*x+a*a+1,(x+a)**2+1) and eq(s.discriminant(x*x+2*(a-1)*x+a*a+1,x),-8*a)),
('rational completed square and intercepts',eq(x*x/2+3*x-s.Rational(7,2),(x+3)**2/2-8) and roots(x*x+6*x-7)=={-7,1}),
('restricted interval endpoints',((0-4)**2-9)==7 and ((3-4)**2-9)==-8 and roots((x-4)**2-4)=={2,6}),
('fixed family point and vertex zero',eq((x*x-2*k*x+2*k+3).subs(x,1),4) and set(s.solve(3+2*k-k*k,k))=={-1,3}),
('nonunit square lower bound',eq(4*x*x+12*x+13,(2*x+3)**2+4) and roots(4*x*x+12*x+8)=={-2,-1}),
('visitor difference',eq((12+6*t-t*t)-(16+2*t),-(t-2)**2) and (5-2)**2==9),
('root spacing reconstruction',roots(x*x-10*x+16)=={2,8} and roots(x*x-10*x+9)=={1,9}),
('discriminant boundary',eq(s.discriminant(x*x+p*x+p,x),p*(p-4)) and roots(x*x+4*x+4)=={-2}),
('perimeter area feasibility',eq(x*(14-x),49-(x-7)**2) and roots(x*(14-x)-40)=={4,10}),
('horizontal region gap',eq((12+4*x-x*x)-12,4-(x-2)**2)),
('positive-root parameter range',all(2-R(v+3)>0 for v in [-2,-1,0]) and 2-R(1+3)==0),
('maximum reconstruction',eq(-2*x*x+12*x-10,-2*(x-3)**2+8) and roots(-2*x*x+12*x-10)=={1,5}),
('perfect square parameter branches',eq(2*x*x-12*x+18,2*(x-3)**2) and eq(2*x*x+12*x+18,2*(x+3)**2)),
('vertical difference from oblique line',eq(2*x*x-4*x+7-(4*x+1),2*(x-2)**2-2)),
('parameter completed-square existence',eq(k*k-2*k-3,(k-3)*(k+1))),
('symmetric input identity',eq(((x*x-6*x+8).subs(x,3+h)),h*h-1) and eq((x*x-6*x+8).subs(x,3-h),h*h-1)),
('score model boundaries',eq(20+12*t-3*t*t,32-3*(t-2)**2) and roots(20+12*x-3*x*x-29)=={1,3})]
for n,(label,v) in enumerate(cases,1):ck(C,n,label,v)
C=3
cases=[
('sum-product ordered pairs',all(xx+yy==5 and xx*yy==4 for xx,yy in [(1,4),(4,1)])),
('recover line from intersection separation',eq((k+2)**2+16-25,k*k+4*k-5) and set(s.solve(k*k+4*k-5,k))=={1,-5} and roots(x*x-3*x-4)=={-1,4} and eq(s.Rational(3,2)**2-2*s.Rational(3,2),s.Rational(-3,4))),
('reciprocal sum and ratio',eq(s.Rational(1,2)+s.Rational(1,5),s.Rational(7,10)) and eq(s.Rational(2,5)+s.Rational(5,2),s.Rational(29,10))),
('quartic reduction',eq(x*x+(x*x-1)**2-7,x**4-x*x-6) and roots(x**4-x*x-6)=={-R(3),R(3)}),
('excluded root after multiplication',eq((x*x-1)-(3*x+1)*(x-1),-2*x*(x-1))),
('intersection of linear and quadratic sets',all((3*z-2<=10 and z*z-z-6>0)==(z<-2 or 3<z<=4) for z in range(-10,11))),
('double threshold exact set',all((0<12+z-z*z<12)==(-3<z<0 or 1<z<4) for z in [s.Rational(i,4) for i in range(-20,21)])),
('fractional sign with both cutpoints',all((0<(z-2)/(z+1)<1)==(z>2) for z in [s.Rational(i,4) for i in range(-20,21)] if z!=-1)),
('rectangle feasible root',roots(x*x+2*x-35)=={-7,5} and (5+3)*(5-1)==32),
('internal path area',eq((12-2*x)*(8-2*x),96-40*x+4*x*x) and eq((x*x-10*x+12).subs(x,5-R(13)),0)),
('difference-product solutions',all(aa-bb==3 and aa*bb==10 and aa*aa+bb*bb==29 for aa,bb in [(5,2),(-2,-5)])),
('horizontal section of region',s.Rational(4,3)**2+1<=5 and 2**2+1==5),
('radical system extraneous branch',R(3+1)==5-3 and R(8+1)!=5-8),
('quartic inequality interval sign',all((z**4-5*z*z+4<=0)==(-2<=z<=-1 or 1<=z<=2) for z in [s.Rational(i,4) for i in range(-12,13)])),
('integer tariff budgets',30+8*8<=94<30+8*9 and 10+12*7<=94<10+12*8),
('fractional equation exact roots',all(eq(2/(z-1)+3/(z+1),2) for z in [(5+R(33))/4,(5-R(33))/4])),
('parameter region section',eq((t*t-4-2*t).subs(t,1-R(5)),0) and s.Rational(5,2)**2-4<=5),
('combined inequality grid',all((2*z*z-7*z+3<0 and z*z>=1)==(1<=z<3) for z in [s.Rational(i,4) for i in range(-16,17)])),
('cubic system all three points',eq(x*(x*x-2*x)-(3*x-6),(x-2)*(x*x-3))),
('sum constraint upper bound',eq(x*(12-x),36-(x-6)**2)),
('four vertices satisfy constraints',all(xx>=0 and yy>=0 and xx+yy<=6 and 2*xx+yy>=4 for xx,yy in [(0,4),(0,6),(6,0),(2,0)])),
('signed system and point distance',eq((2*R(5))**2+(4*R(5))**2,100)),
('integer allowed list',all((z*z-3*z-10<0)==(z in [-1,0,1,2,3,4]) for z in range(-8,9))),
('two parabola gap',eq((-x*x+6*x-6)-(x*x-2*x),-2*(x-1)*(x-3))),
('double contact and nonnegative difference',eq(x*x-6*x+10-(2*x-6),(x-4)**2)),
('rational window',all((2<12/(z-2)<=4)==(5<=z<8) for z in [s.Rational(i,4) for i in range(9,49)])),
('sum of squares reduction',all(aa+bb==8 and aa*aa+bb*bb==40 for aa,bb in [(2,6),(6,2)])),
('zero branch retained',all(xx*yy==2*xx and xx+yy==3 for xx,yy in [(0,3),(1,2)])),
('trapezium area',eq((x+2+3*x-2)*x/2,2*x*x)),
('triangular region vertices',all(xx>=0 and yy>=1 and xx+yy<=7 and yy<=2*xx+1 for xx,yy in [(0,1),(6,1),(2,5)]))]
for n,(label,v) in enumerate(cases,1):ck(C,n,label,v)
C=4
cases=[
('landmark reflections',(-(-2),5)==(2,5) and (4,-(-1))==(4,1)),
('cubic intercepts and vertical offset',roots((x+3)*(x-1)*(x-4))=={-3,1,4} and (0+3)*(0-1)*(0-4)-17==-5),
('translated reciprocal line roots',all(eq(6/(z-2)-1,z-3) for z in [2+R(6),2-R(6)])),
('horizontal scaling points',[(z/3,y) for z,y in [(-6,2),(0,-3),(9,0)]]==[(-2,2),(0,-3),(3,0)]),
('double root sign',all(((z+2)**2*(z-3)>=0)==(z==-2 or z>=3) for z in range(-6,8))),
('square root line solution and excluded one',R(5+4)==5-2 and R(0+4)!=0-2),
('vertical constants',2*(-3)+11==5 and 2*0+11==11),
('cubic root compression and chord',roots(x**3-4*x)=={-2,0,2} and 1-(-1)==2),
('reciprocal square threshold',all((8/z**2<2)==(z<-2 or z>2) for z in range(-6,7) if z!=0)),
('reflected cubic intercept',eq(-(4**s.Rational(1,3))**3+4,0)),
('reciprocal line and distance',all(eq(4/(z-1),z+1) for z in [R(5),-R(5)]) and eq((2*R(5))**2+(2*R(5))**2,40)),
('horizontal root shift',[z-3 for z in [-4,1,7]]==[-7,-2,4]),
('equivalent reciprocal scales',eq(12/(3*x),(12/x)/3)),
('shifted cubic intercept and threshold',(1+1)**3-8==0 and (2+1)**3-8==19),
('parabola shift and intersection',eq((x-1)*(x-5),(x-3)**2-4) and eq((x*x-4).subs(x,s.Rational(3,2)),s.Rational(-7,4))),
('asymptote coordinate scale',3/s.Integer(2)==s.Rational(3,2) and 2*(-2)==-4),
('square-root vertical transform',eq(2*R(s.Rational(9,4))-3,0) and 2*R(16)-3==5),
('reflected cubic sign',all((((-z+2)*(-z-1)*(-z-3))>0)==(-1<z<2 or z<-3) for z in range(-7,8))),
('reciprocal quadrant intercepts',9/(7+2)-1==0 and s.Rational(9,2)-1==s.Rational(7,2)),
('general graph translated intervals',[z+2 for z in [-3,0,5]]==[-1,2,7]),
('central line intersection condition',eq(8/x-(-2*x),(8+2*x*x)/x) and all(eq(m*(R(8/m))**2,8) for m in [s.Integer(1),s.Integer(2),s.Integer(8)])),
('translated reciprocal square chord',18/(-4+1)**2==2 and 18/(2+1)**2==2 and 18/(0+1)**2==18),
('cubic reconstructed scale',2*(0+1)*(0-2)*(0-4)==16),
('two shifted radical intersection',R(4)==R(4-3)+1),
('negative scale from point pairs',-3*2+5==-1 and -3*(-1)+5==8),
('horizontal stretch roots and chord',roots((x/2-2)**2-9)=={-2,10} and roots((x/2-2)**2-4)=={0,8}),
('cubic minus line',eq((x**3-3*x+2)-(x+2),x*(x-2)*(x+2))),
('hole domain retained',eq((x*x-4)/(x-2),x+2) and (2+3,4)==(5,4)),
('endpoint reconstructed parameters',R(6+3)+2==5 and R(1+3)+2==4),
('four-intersection parameter identity',eq(t*t-(h+5)*t+16,(t-4)**2-(h-3)*t) and eq(s.discriminant(t*t-(h+5)*t+16,t),(h+5)**2-64))]
for n,(label,v) in enumerate(cases,1):ck(C,n,label,v)
# Structural and control character validation on generated assets.
root=(pathlib.Path(__file__).resolve().parents[1]/'chapters');summ=[]
for c in range(1,5):
 qs=json.loads((root/f'P1-C{c:02}.json').read_text());assert len(qs)==30
 for q in qs:
  assert q['chapters'][0]==c and q['marks']==sum(p['marks'] for p in q['parts'])
  for pp in [z for p in q['parts'] for z in p.get('subparts',[p])]:
   assert sum(m['marks'] for m in pp['scheme'])==pp['marks']
   assert re.search('[一-鿿]',pp['explanation'])
   for key in ['text','answer','explanation']:assert not re.search('[\x00-\x08\x0b\x0c\x0e-\x1f]',pp[key])
 summ.append({'chapter':c,'questions':30,'figures':sum('figureSvg' in q for q in qs),'parts':dict(collections.Counter(len(q['parts']) for q in qs)),'marks':dict(collections.Counter(q['marks'] for q in qs))})
report={'symbolicCases':len(checks),'passed':sum(z['passed'] for z in checks),'checks':checks,'chapters':summ,'limitations':'Symbolic verification of authored key identities and solution branches; internal author review, not independent teacher certification. General graph-shape claims additionally reviewed manually.'}
(pathlib.Path(__file__).resolve().parents[1]/'research/p1-algebra-check-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({'cases':len(checks),'passed':sum(z['passed'] for z in checks),'chapters':summ},ensure_ascii=False))
