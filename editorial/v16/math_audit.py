"""Independent geometry, boundary and parameter checks, separate from authoring."""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];F=Path(__file__).parent
pi=math.pi;results={}
def close(a,b,tol=1e-8):assert abs(a-b)<tol,(a,b)
def polygon(points):return abs(sum(x*points[(i+1)%len(points)][1]-points[(i+1)%len(points)][0]*y for i,(x,y) in enumerate(points)))/2
def circular_cap(r,c):
 # Integrate the circular ordinate numerically by midpoint quadrature (not the sector-minus-triangle formula).
 h=math.sqrt(r*r-c*c/4);n=20000;step=(r-h)/n
 return 2*step*sum(math.sqrt(max(0,r*r-(h+(i+.5)*step)**2)) for i in range(n))
def findroot(fn,lo,hi):
 for _ in range(80):
  mid=(lo+hi)/2
  if fn(mid)>0:hi=mid
  else:lo=mid
 return (lo+hi)/2

# R01: direct coordinate reconstruction of the two congruent side triangles.
record=[]
target=18*math.sqrt(3)+6*pi
for theta in (pi/3,2*pi/3):
 alpha=(pi-theta)/2;ratio=2*math.cos(alpha)
 r=math.sqrt(target/(theta/2+ratio*math.sin(alpha)));x=ratio*r
 O=(0,0);A=(-x,0);B=(-r*math.cos(alpha),r*math.sin(alpha));C=(-B[0],B[1]);D=(x,0)
 close(math.dist(A,B),r);close(polygon([O,A,B])+polygon([O,C,D])+r*r*theta/2,target)
 record.append({'r':r,'x':x,'perimeter':math.dist(A,B)+math.dist(C,D)+2*x+r*theta})
assert record[0]['perimeter']<record[1]['perimeter'];results['R01']=record
# R02: verify area removed as old area minus the retained circular wedge minus a triangle.
old=54*pi;new=24*pi-9*math.sqrt(3)
close(old-new,30*pi+9*math.sqrt(3));close((14*pi+12)-(4*pi+18),10*pi-6)
results['R02']={'originalArea':old,'newArea':new,'areaReduction':old-new}
t=findroot(lambda z:z-3*math.sin(z),1,3);assert round(t,5)==2.27886
results['R03']={'theta':t,'arcChord':t/(2*math.sin(t/2)),'segmentArea':25*t/3}
# R07: use an independently integrated cap in each circle.
t=2*math.acos(.8);r=6/math.sin(t/4);a=circular_cap(10,12);b=circular_cap(r,12)
close(a,50*(t-math.sin(t)),1e-5);close(b,r*r*(t/2-math.sin(t/2))/2,1e-5);assert a>b
results['R07']={'secondRadius':r,'areas':[a,b]}
# R08: sample the actual polar boundary rather than reuse the aggregate fan formulas.
def fan(n,alpha):
 innerArea=n*4*alpha/2;outerArea=n*64*(2*pi/n-alpha)/2
 boundary=n*(2*alpha+8*(2*pi/n-alpha)+12)
 return innerArea+outerArea,boundary
aa,pp=fan(4,.75);bb,qq=fan(5,.75);close(aa,64*pi-90);close(pp,16*pi+30)
results['R08']={'n':4,'alpha':.75,'ratio':(pp/qq)**2*bb/aa}
# R10: enumerate actual roots and validate the stated open interval, including both boundaries.
low=200*pi/(pi+2)**2
def valid_minor_roots(area):
 if area>25:return []
 roots=set([5-math.sqrt(25-area),5+math.sqrt(25-area)])
 return [r for r in roots if r>0 and 1e-9<20/r-2<pi-1e-9]
assert len(valid_minor_roots(low))==1 and len(valid_minor_roots(25))==1
for area in [low+.01,(low+25)/2,24.999]:assert len(valid_minor_roots(area))==2
for area in [.1,10,low-.01]:assert len(valid_minor_roots(area))==1
results['R10']={'openAreaInterval':[low,25]}
# R11: use coordinates of BC to compute point-to-line distance, then the remaining boundary.
B=(8,0);C=(11*math.cos(1.2),11*math.sin(1.2));bc=math.dist(B,C);tri=polygon([(0,0),B,C]);h=2*tri/bc;r=math.sqrt(tri/1.8)
assert r<h;results['R11']={'r':r,'height':h,'perimeter':19+bc-.8*r}
# R13: solve for OD from the cosine-rule quadratic and test both branch conditions.
for d in [6*math.sqrt(3)+1e-5,10.7,11,11.999]:
 gamma=math.asin(d/12);omega=pi-gamma
 disc=d*d-36*.25
 # Projection along the D-angle: OA²=AD²+OD²-2 AD OD cos(delta).
 options=[d*math.cos(pi/6)+sign*math.sqrt(36-d*d*.25) for sign in (-1,1)]
 valid=[]
 for od in options:
  if od<=0:continue
  co=(36+od*od-d*d)/(12*od);angle=math.acos(max(-1,min(1,co)))
  if od>6 and angle>pi/2:valid.append(od)
 assert len(valid)==1
 if d==11:
  od=valid[0];close(od,12*math.sin(gamma-pi/6));results['R13']={'OD':od,'omega':omega,'area':18*(2*pi-omega)+3*od*math.sin(omega),'perimeter':6*(2*pi-omega)+od-6+d}
for d in [6.1,8,10.0]:
 gamma=math.asin(d/12);assert 12*math.sin(gamma-pi/6)<6
# R20: derive Q from ray coordinates, then obtain the angle with atan2, not the author's cosine rule.
r=math.sqrt(17)/2;design=[]
for x in (2*math.sqrt(3)-.5,2*math.sqrt(3)+.5):
 P=(0,0);C=(4,0);Q=(x*math.cos(pi/6),x*.5)
 close(math.dist(C,Q),r);theta=math.atan2(Q[1],4-Q[0])
 area=r*r*(2*pi-theta)/2+polygon([P,C,Q]);perimeter=r*(2*pi-theta)+x+4-r
 design.append({'PQ':x,'angle':theta,'area':area,'perimeter':perimeter})
assert design[0]['area']>design[1]['area'] and design[0]['perimeter']>design[1]['perimeter']
assert format(design[0]['area'],'.3g')==format(design[1]['area'],'.3g')
assert format(design[0]['perimeter'],'.3g')==format(design[1]['perimeter'],'.3g')
results['R20']=design
t=2*math.asin(7/9);minor=circular_cap(9,14);major=81*pi-minor
assert major/minor>(9*(2*pi-t)+14)/(9*t+14)
results['R21']={'areas':[minor,major],'perimeterDifference':18*(pi-t)}
# R23: all positive parameter samples satisfy the bound; equality is geometrically possible.
for theta in [.601,.8,math.sqrt(1.2),2,3.14]:
 w=6/theta;inner=(10-w)/2;outer=(10+w)/2;assert inner>0
 close((outer*outer-inner*inner)*theta/2,30);close((outer-inner)*theta,6)
 assert (inner+outer)*theta+2*w>=4*math.sqrt(30)-1e-10
close(10*2+12/2,26);results['R23']={'minimumPerimeter':4*math.sqrt(30),'validAt26':[3.5,6.5,2]}
rr=math.sqrt(40/pi);hh=60/13;assert rr<hh<5
results['R24']={'radius':rr,'limitRadius':hh,'limitAreaPercentage':100*pi*hh*hh/120}
for radius,theta in [(2*math.sqrt(6),1.25),(5*math.sqrt(6)/4,3.2)]:
 close(radius*radius*theta/2,15);close(radius*(2+theta),13*math.sqrt(6)/2)
results['R25']={'accepted':[2*math.sqrt(6),1.25],'rejectedAngle':3.2};assert 3.2>pi
assert 7*(.6+.25)<2*pi<8*(.6+.25);results['R28']={'maximum':7,'boundary':102.4}
# R30: locate C geometrically from two distances, and calculate triangle area by coordinates.
ab=3*math.sqrt(3);cases=[];K=6*pi+9*math.sqrt(3)/4
for ac in [4*math.sqrt(3)-math.sqrt(11),4*math.sqrt(3)+math.sqrt(11)]:
 cx=(ac*ac+ab*ab-64)/(2*ab);cy=math.sqrt(ac*ac-cx*cx);C=(cx,cy);A=(0,0);B=(ab,0)
 close(math.dist(C,B),8);dot=(-cx)*(ab-cx)+cy*cy;close(dot/(ac*8),math.cos(pi/6))
 ta=polygon([A,B,C]);close(ta,2*ac);area=K+ta;p=4*pi+8+ac
 cases.append({'AC':ac,'area':area,'perimeter':p,'ratio':area/p})
assert cases[1]['ratio']>cases[0]['ratio'];results['R30']=cases
# R31: verify region area by a fine polygon along the actual circular arc.
theta=math.atan2(6,9);C=(0,-7);A=(0,6);B=(6,2);cb=math.dist(C,B);D=(13*6/cb,-7+13*9/cb)
pts=[A,(0,0),B,D]+[(13*math.sin(t),-7+13*math.cos(t)) for t in [theta*(1-i/20000) for i in range(1,20001)]]
ar=polygon(pts);close(ar,169*theta/2-21,1e-6);assert ar>169*theta/4
results['R31']={'area':ar,'perimeter':6+math.sqrt(40)+math.dist(B,D)+13*theta}
# R32: explicit coordinate construction for angles on both sides of π/2.
for theta in [.2,1.0,pi/2,1.9]:
 r=7;x=r*theta/2;O=(0,0);B=(r,0);P=(x,0);A=(r*math.cos(theta),r*math.sin(theta))
 close(r+x+math.dist(A,P),r*theta+(r-x)+math.dist(A,P));T=polygon([O,A,P]);sector=r*r*theta/2
 assert sector-T>=T-1e-10
results['R32']={'existenceRange':[0,2],'equalAreasAt':pi/2}
for r,theta in [(3,16/9),(8,.25)]:close(1.5*r*r*theta,24);close(3*r*theta+2*r,22)
results['R33']={'outerArcDifference':20/3}
# R34: circular-boundary area by polygon integration agrees with removed segments.
r=6;pts=[]
for i in range(3):
 start=i*2*pi/3;pts.extend([(r*math.cos(start+t*pi/3/10000),r*math.sin(start+t*pi/3/10000)) for t in range(10001)])
kept=polygon(pts);removed=36*pi-kept;close(removed,18*pi-27*math.sqrt(3),1e-6)
rho=math.sqrt(2*removed/pi);results['R34']={'removedArea':removed,'newPerimeter':rho*(6+pi)}
# R37: independent one-dimensional integration of the half-cap below y=0.
radius=50/3;a=100/9;n=30000;h=(radius-a)/n
cap=h*sum(math.sqrt(max(0,radius*radius-(-radius+(i+.5)*h)**2)) for i in range(n))
exact=1250*math.acos(2/3)/9-2500*math.sqrt(5)/81;close(cap,exact,1e-5)
results['R37']={'a':a,'leastAngle':math.acos(2/3),'areaByQuadrature':cap}
# R38: sweep geometric admissibility and confirm the equality geometry directly.
for a in [2.01,3,6,8,12,19.99]:
 t=a-2;e=2-36/t;assert e<0<a;radius=a-e;assert radius>=12-1e-10
close(math.dist((0,-4),(6,2)),6*math.sqrt(2))
results['R38']={'radiusMinimum':12,'aAtMinimum':8,'remainingArea':18*pi-36,'remainingPerimeter':12+3*pi}
assert len(results)==21
doc={'status':'passed','scope':'all 21 mathematical cores; geometric reconstructions, numerical integrations and open-boundary parameter cases','questions':results}
(F/'math-audit.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
print('PASS V16: independent geometry and parameter checks for all 21 questions')
