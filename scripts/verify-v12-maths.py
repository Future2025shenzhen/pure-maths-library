"""Independent numerical checks of the newly authored models and full solution sets."""
import math,json
from pathlib import Path
from scipy.optimize import brentq
B=json.loads((Path(__file__).resolve().parents[1]/'dist/data/bank.json').read_text());Q={q['id']:q for q in B['questions']}
def roots(f,lo,hi,n=30000):
 out=[];step=(hi-lo)/n
 for i in range(n):
  a=lo+i*step;b=a+step
  try:
   fa,fb=f(a),f(b)
   if abs(fa)<1e-9:r=a
   elif fa*fb<0:r=brentq(f,a,b)
   else:continue
   if abs(f(r))<1e-6 and (not out or abs(r-out[-1])>1e-5):out.append(r)
  except (ValueError,ZeroDivisionError):pass
 if abs(f(hi))<1e-9 and (not out or abs(hi-out[-1])>1e-5):out.append(hi)
 return out
r=lambda x:math.radians(x)
def check(f,lo,hi,expected,digits,exclude=()):
 got=[x for x in roots(f,lo,hi) if not any(abs(x-e)<1e-6 for e in exclude)]
 assert [round(x,digits) for x in got]==expected,(got,expected)
check(lambda x:4*math.sin(r(3*x-20))-math.sqrt(3),-60,180,[15.2,58.1,135.2,178.1],1)
check(lambda x:3*math.tan(r(x))+5*math.sin(r(x)),0,360,[126.9,180.0,233.1,360.0],1,exclude=[0])
check(lambda x:(4*math.cos(2*x)-math.tan(2*x))*math.cos(2*x)-2,-math.pi/2+1e-8,math.pi/2-1e-8,[-1.069,-0.501,0.317,1.253],3)
check(lambda x:5*math.sin(r(2*x-25))-3*math.cos(r(2*x-25)),-90,180,[-62.0,28.0,118.0],1)
check(lambda x:2*math.sin(x)**3-3*math.sin(x)+4*math.sin(x)*math.cos(x),-math.pi,math.pi,[-3.142,-1.274,0.0,1.274],3,exclude=[math.pi])
check(lambda x:(3*math.sin(r(x))-math.cos(r(x)))**2-1,0,360,[36.9,180.0,216.9],1,exclude=[0,360])
# Textbook factorisation: independently enumerate zero factors and evaluate the original expression.
theta=[math.atan(.25),math.pi,math.pi+math.atan(.25)]
assert all(abs(4*math.sin(t)*math.cos(t)-math.cos(t)**2+4*math.sin(t)-math.cos(t))<1e-12 for t in theta)
assert roots(lambda t:math.tan(t)-2*t,-3*math.pi,3*math.pi).__len__()==7
assert len(roots(lambda t:math.tan(t)-1/t,-4*math.pi+1e-8,3*math.pi-1e-8))==7
# Geometry is recomputed from the stated data, not from stored answers.
a=(math.pi-2)/2;ab=math.sqrt(41-40*math.cos(a));assert round(ab,2)==2.71
assert round(25+20*math.sin(a),1)==35.8;assert round(2*ab+18,1)==23.4
x=-4+4*math.sqrt(6);assert abs(.5*((4+x)**2-16)*.75-30)<1e-12;assert round(6+2.75*x,1)==21.9
assert round(50*2*math.asin(.6),1)==64.4;assert round(20+20*math.asin(.6),1)==32.9
assert round(18*(1-math.sin(1))/(40.5*(4/9-math.sin(4/9))),2)==4.86
assert round(15-10*math.sin(1.5),3)==5.025
assert round(96*math.pi-72*math.sqrt(3))==177
assert 24-6*math.pi+9*math.sqrt(3)>0
print('PASS independent full trigonometric solution sets, exclusions, root counts and new geometry values')
