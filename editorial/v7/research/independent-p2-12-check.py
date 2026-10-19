import pathlib
import sympy as s,json,pathlib
x,y,k,m,h,t=s.symbols('x y k m h t',real=True)
r=[]
def ck(q,n,a,b=0):
 ok=s.simplify(a-b)==0;r.append({'id':q,'check':n,'passed':bool(ok)})
 if not ok:raise AssertionError(r[-1])
ck('P2-C01-R01','factor and irreducible quotient',(x+2)*(x*x-3*x+6),x**3-x*x+12)
ck('P2-C01-R03','quartic paired factors',(x-1)*(x+1)*(x-2)*(x+2),x**4-5*x*x+4)
ck('P2-C01-R04','nonmonic divisor quotient',(2*x-1)*(x*x+x-3),2*x**3+x*x-7*x+3)
ck('P2-C01-R06','horizontal zero double root',(x-1)**2*(x-4),x**3-6*x*x+9*x-4)
ck('P2-C01-R14','factor and integral',s.integrate(x*(x-2)*(x+2),(x,0,2)),-4)
ck('P2-C01-R15','odd/even difference and quotient',(x-1)*(x*x+2*x-2),x**3+x*x-4*x+2)
ck('P2-C01-R21','horizontal contact and other point',(x+1)*(x-2)**2,x**3-3*x*x+4)
ck('P2-C01-R26','trigonometric substitution polynomial',(x-1)*(2*x-1)*(x+1),2*x**3-x*x-2*x+1)
ck('P2-C01-R27','log/positive exponential admissibility factors',(x+1)*(x-1)*(x-4),x**3-4*x*x-x+4)
ck('P2-C01-R28','integrated polynomial factor',(x-1)*(x*x-x-4),x**3-2*x*x-3*x+4)
ck('P2-C01-R30','positive-region area',s.integrate(x*(x-2)*(x-3),(x,0,2)),s.Rational(8,3))
ck('P2-C02-R03','tangent discriminant',s.discriminant((x-3)**2+(m*(x-10))**2-25,x),4*(25-24*m*m))
ck('P2-C02-R06','equal-radius condition',(h-1)**2+16-((h-7)**2+4),12*h-36)
ck('P2-C02-R07','contact with prescribed tangent',3*5+4*7,43)
ck('P2-C02-R08','circle parabola reduction',x*x+(x*x-2)**2-4,x*x*(x*x-3))
ck('P2-C02-R10','diameter right angle',s.Rational(-1,2)*2,-1)
ck('P2-C02-R13','parameter line discriminant',s.discriminant(2*x*x+(2*k-6)*x+k*k-4*k-3,x),64-4*(k-1)**2)
ck('P2-C02-R14','square tangent intersection',3*3+5,14)
ck('P2-C02-R14','second tangent intersection',-3+3*5,12)
ck('P2-C02-R17','allowed distance-based contact equation',((x-3)**2+(y-1)**2)-((x-8)**2+(y-1)**2),10*x-55)
ck('P2-C02-R17','contact x from known squared distances',10*s.Rational(24,5)-55,9-16)
ck('P2-C02-R19','opposite endpoint tangent',3*(-2)+4*(-6)+30,0)
ck('P2-C02-R21','triangle tangent-external area',s.Rational(1,2)*8*(s.Rational(50,3)-6),s.Rational(128,3))
ck('P2-C02-R24','diameter-circle expansion',(x-t/2)**2+(y-t)**2-5*t*t/4,x*x+y*y-t*x-2*t*y)
ck('P2-C02-R25','left chord tangent at endpoint',-4*(-2)+3*2,14)
ck('P2-C02-R25','right chord tangent at endpoint',4*6+3*2,30)
ck('P2-C02-R26','integrated straight chord area',s.integrate((2+s.sqrt(13))*x/3,(x,0,3)),s.Rational(3,2)*(2+s.sqrt(13)))
ck('P2-C02-R27','parallel but distinct tangent slope',4*s.Rational(5,16)-2,s.Rational(-3,4))
ck('P2-C02-R29','triangle area ratio',s.Rational(12)/(s.Rational(64,3)),s.Rational(9,16))
for n in range(-60,61):
 assert ((n%2==1 and n%3!=0) is False) or (n*n-1)%24==0
 assert (n**4-n*n)%12==0
out={'readAllQuestions':60,'chapters':['P2-C01','P2-C02'],'symbolicChecks':r,'proofExhaustion':'Integer divisibility examples additionally checked n=-60..60; symbolic logical arguments read manually.','definiteMathErrors':[], 'findings':[
 {'severity':'medium','id':'P2-C02-R17','issue':'Answer uses perpendicular vector dot-product identity without deriving it from P2 methods.','fix':'Use CT²=9 and PT²=16, subtract the two distance equations to obtain10x-55=-7, hencex=24/5.','status':'sent to author'},
 {'severity':'low','id':'P2-C02 multiple tangent answers','issue':'Term 半径向量 and immediate normal-vector tangent equations may imply later-stage vector method. Coordinates and final equations are correct.','fix':'Explain using radius slope, perpendicular slope and point-slope line, especiallyR02/R14/R21/R25/R27.','status':'sent to author'},
 {'severity':'low','id':'P2-C01-R24','issue':'Solution uses absolute-value notation in an optional inequality step despite modulus functions belonging toP3.','fix':'Write (x-3)²<1 hence2<x<4 directly.','status':'sent to author'}], 'diagramReview':'All SVG text labels reviewed; no numerical answer-coordinate labels or explicit proof-target leaks found. Some point names are diagram-only but no geometrical ambiguity in mathematical question.', 'limitations':'Internal peer review, not independent qualified-teacher certification. Final author may edit assets after this snapshot; re-run verification after modifications.'}
(pathlib.Path(__file__).resolve().parents[1]/'research/independent-p2-12-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(len(r),'symbolic checks PASS; full60 read;3 scoped findings')
