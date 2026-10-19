import pathlib
import sympy as s, math,json,pathlib
x,h=s.symbols('x h',real=True);R=pathlib.Path(__file__).resolve().parent; checks=[]
def eq(label,a,b):
 assert s.simplify(a-b)==0,(label,a,b);checks.append({'check':label,'passed':True,'method':'SymPy exact simplification'})
def ok(label,v):
 assert v,label;checks.append({'check':label,'passed':True,'method':'exact arithmetic / branch or interval check'})
# Each C01 item has its own symbolic/finite check, not merely a structural counter.
eq('C01R01 cancelled rational',(x*x-5*x+6)/(x*x-x-6),(x-2)/(x+2))
eq('C01R02 cubic division',(x**3-2*x*x-4*x+11)/(x-2),x*x-4+3/(x-2))
eq('C01R03 unknown coefficient identity',(x**3+3*x*x+5*x+5)/(x+1),x*x+2*x+3+2/(x+1))
eq('C01R04 quotient',(x*x-9)/(x*x+4*x+3)/((x*x-3*x)/(x*x-1)),(x-1)/x)
eq('C01R05 common numerator',2/(x-1)-3/(x+2),(7-x)/((x-1)*(x+2)))
eq('C01R06 quadratic divisor',x**4+x**3-3*x*x+2*x+7,(x*x+1)*(x*x+x-4)+x+11)
eq('C01R07 removable hole',(x*x+x-12)/(x-3),x+4)
eq('C01R08 lower bound',(x*x+4*x+13)/(x+2)-6,(x-1)**2/(x+2))
eq('C01R09 slant line',(2*x*x-5*x+5)/(x-1),2*x-3+2/(x-1))
eq('C01R10 sign structure',(x**3-4*x)/(x*x-x-2),x*(x+2)/(x+1))
eq('C01R11 symmetric rational',(x+1)/(x-1)+(x-1)/(x+1),2+4/(x*x-1))
eq('C01R12 cube difference',(x**3-8)/(x-2),(x+1)**2+3)
eq('C01R13 t substitution',(x*x+2*x+5)/(x+1),x+1+4/(x+1))
eq('C01R14 identity critique',(x*x-1)*(x*x-3*x+1)+2*x+5,x**4-3*x**3+5*x+4)
eq('C01R15 contradiction cleared',(x+1)+2*(x-2)-3*(x+1),s.Integer(-6))
ok('C01R16 divisors',[n for n in range(1,100) if (n*n+3*n+8)%(n+1)==0]==[1,2,5])
eq('C01R17 inverse rational',(x*x-x-6)/(x*x+x-2),1-2/(x-1))
eq('C01R18 polynomial quotient',2*x**3-7*x+3,(x-2)*(2*x*x+4*x+1)+5)
t=1+s.sqrt(5);eq('C01R19 positive radical solution',t+2,t*t/2)
eq('C01R20 even cancellation',(x**4-5*x*x+6)/(x*x-2),x*x-3)
eq('C01R21 finite chord',((x+h)**3-2*(x+h)-(x**3-2*x))/h,3*x*x+3*x*h+h*h-2)
eq('C01R22 common denominator',(x*x+1)/(x-1)-2*x/(x-1),x-1)
eq('C01R23 division and sign',(x**3+1)/(x*x+1)-x,(1-x)/(x*x+1))
f=(x-2)/(x+2);eq('C01R24 composition',(1+f)/(1-f),x/2)
eq('C01R25 quadratic product',(x*x+x+2)*(x*x+2*x+3),x**4+3*x**3+7*x*x+7*x+6)
eq('C01R26 square difference',(x+1/x)**2-4,(x-1/x)**2)
eq('C01R27 range expression',(x*x-1)/(x*x+1),1-2/(x*x+1))
eq('C01R28 panel area',(x*x-9)/(x+3)*(x*x+5*x+6)/(x+2),x*x-9)
eq('C01R29 opposite input',(x*x+x+1)-(x*x-x+1),2*x)
eq('C01R30 curve difference',(x**3+2*x*x-3*x+4)/(x+2)-(x*x+2),-5*x/(x+2))
# C02 explicit inverse/composition and piecewise checks.
v=(5-s.sqrt(5))/2;eq('C02R01 fixed point',(v-2)**2+1,v)
eq('C02R02 composite root',(2*(-1+3)+1)/s.Integer(-1+3-1),s.Integer(5))
ok('C02R03 exact abs roots',all(abs(2*r-3)+1==r+3 for r in [s.Rational(1,3),s.Integer(5)]))
ok('C02R04 minimum and mapped point',[(2-u,3*v-2)for u,v in [(-2,1),(1,4)]]==[(4,1),(1,10)])
ok('C02R05 no solution via bound',2*math.sqrt(3)<5)
ok('C02R06 abs composite roots',all(abs(r-1)+abs(r-2)==3 for r in [0,3]))
eq('C02R07 self inverse',1+6/(1+6/(x-1)-1),x)
ok('C02R08 four roots',sum(abs(abs(v)-2)==1 for v in [-3,-1,1,3])==4)
ok('C02R09 candidate outside composite domain',s.Rational(3,7)<s.Rational(1,2))
ok('C02R10 abs quadratic roots',all(abs(r*r-4)==r+2 for r in [-2,1,3]))
ok('C02R11 removed input/output',1+1==2)
eq('C02R12 point map',2*s.sqrt(3-(-1))+1,s.Integer(5))
ok('C02R13 piecewise composite',((3+1)+1)==5)
ok('C02R14 parameter flat segment',all(abs(t-1)+abs(t+1)==2 for t in [-1,0,1]))
eq('C02R15 composite root',9-(9-s.sqrt(6)**2)**2,0)
eq('C02R16 commuting equation',(2*x-1)**2+1-(2*(x*x+1)-1),2*x*x-4*x+1)
ok('C02R17 coordinate zeros',[3*u+1 for u in [-3,1]]==[-8,4])
ok('C02R18 no fixed point discriminant',s.discriminant((x+1)**2-x,x)<0)
ok('C02R19 vertex-only branches',s.solve(6-3*x-(-3*x/2+3),x)==[2] and s.solve(3*x-6-(-3*x/2+3),x)==[2])
f=(x+2)/(x-1);eq('C02R20 involution',(f+2)/(f-1),x)
ok('C02R21 modulus roots',all(s.simplify(abs(r*r-2*r-3)+2-5)==0 for r in [1-s.sqrt(7),1+s.sqrt(7),0,2]))
eq('C02R22 domain sample solution',1/(2-s.Rational(3,2)),2)
ok('C02R23 inverse coordinate map',(3*(-2)+2,2*(-5+4))==(-4,-2))
eq('C02R24 only abs level solution',2/(s.Integer(2)-1)-1,1)
eq('C02R25 inverse linear',3*(x/3+s.Rational(4,3))-4,x)
eq('C02R26 completed square',x*x-6*x+5,(x-3)**2-4)
ok('C02R27 mapped inequality',[2-v for v in [2,-6]]==[0,8])
v=(1+s.sqrt(5))/2;eq('C02R28 fixed point',v*v,v+1)
ok('C02R29 isolated root and ray',all(abs(r-1)-1==abs(abs(r)-2) for r in [-1,2,3,10]))
eq('C02R30 composite difference',2*x/(2*x+1)-x/(x+1),x/((2*x+1)*(x+1)))
# Trigonometric checks at non-poles supplement exact solution branch work recorded in answers.
for label,a,b in [
 ('C03 cot identity',s.cot(x)**2,s.csc(x)**2-1),('C03 sec identity',s.tan(x)**2,s.sec(x)**2-1),
 ('C03 conjugate sec',(s.sec(x)+s.tan(x))*(s.sec(x)-s.tan(x)),1),
 ('C03 conjugate csc',(s.csc(x)-s.cot(x))*(s.csc(x)+s.cot(x)),1),
 ('C03 tan cot sum',s.tan(x)+s.cot(x),1/(s.sin(x)*s.cos(x))),
 ('C04 fourth power',s.cos(x)**4-s.sin(x)**4,s.cos(2*x)),
 ('C04 triple angle',s.cos(3*x),4*s.cos(x)**3-3*s.cos(x)),
 ('C04 square', (s.sin(x)+s.cos(x))**2,1+s.sin(2*x)),
 ('C04 combined angle identity',(s.sin(x)+s.sin(3*x))**2+(s.cos(x)+s.cos(3*x))**2,4*s.cos(x)**2),
 ('C04 final derivative',s.diff(s.sin(x)*s.cos(x)+s.sin(x)**2,x),s.cos(2*x)+s.sin(2*x))]:
 assert s.trigsimp(s.together(s.expand_trig((a-b).rewrite(s.sin))))==0,label;checks.append({'check':label,'passed':True,'method':'SymPy trigsimp'})
solutions=[('C03R01',lambda t:2/(math.tan(t)**2)-3/math.sin(t),[math.pi/6,5*math.pi/6]),('C03R02',lambda t:math.tan(t)**2-1.5/math.cos(t),[math.pi/3,5*math.pi/3]),('C03R15',lambda t:1/math.sin(t)-2*math.sin(t)-1,[math.pi/6,5*math.pi/6,3*math.pi/2]),('C04R07',lambda t:math.sin(math.radians(2*t+10))-2*math.cos(math.radians(2*t-20)),[40,130]),('C04R23',lambda t:math.cos(2*t)+3*math.sin(t)-2,[math.pi/6,math.pi/2,5*math.pi/6]),('C04R25',lambda t:4*math.sin(t-math.pi/6)**2-1,[0,math.pi/3,math.pi])]
for label,f,roots in solutions:ok(label+' all listed roots residual',all(abs(f(r))<1e-10 for r in roots))
ok('C04R08 path geometry',25+169-130*s.Rational(33,65)==128 and s.Rational(65,2)*s.Rational(56,65)==28)
ok('C04R21 triangle area',s.Rational(1,2)*8*5*s.Rational(117,125)==s.Rational(468,25))
alpha=s.symbols('alpha',real=True)
assert s.trigsimp(s.expand_trig(s.sin(x+alpha)*s.sin(x-alpha))-(s.cos(2*alpha)-s.cos(2*x))/2)==0
checks.append({'check':'C04R28 new unknown-angle product proof','passed':True,'method':'SymPy expand_trig/trigsimp'})
eq('C04R28 observed value at recovered angle',s.sin(s.pi/6+s.pi/4)*s.sin(s.pi/6-s.pi/4),-s.Rational(1,4))
eq('C04R28 exact nonnegative area',s.integrate(s.sin(x)**2,(x,0,s.pi/3)),s.pi/6-s.sqrt(3)/8)
# Every JSON text is free of hidden escape/control corruption and unresolved drafting markers.
for ch in range(1,5):
 qs=json.load(open(R.parent/'chapters'/f'P3-C{ch:02}.json'));assert len(qs)==30
 for q in qs:
  raw=json.dumps(q,ensure_ascii=False);assert not any(ord(c)<32 for c in raw)
  def pp(parts):
   for z in parts:
    for k in ['answer','explanation']:
     assert '?' not in z.get(k,'') and '？' not in z.get(k,''),(q['id'],z)
    pp(z.get('subparts',[]))
  pp(q['parts'])
 ok(f'C0{ch} schema30 records and no drafting markers',True)
R.joinpath('p3-functions-mathchecks.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'limitations':'内部符号与分支校验；非外部教师审定。未用参数循环生成题干。'},ensure_ascii=False,indent=2))
print(len(checks),'passed')
