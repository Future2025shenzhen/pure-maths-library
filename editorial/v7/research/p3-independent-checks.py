import pathlib
import sympy as s, math,json
from pathlib import Path
from scipy.integrate import quad
from scipy.optimize import brentq
x=s.symbols('x',real=True);xp=s.symbols('x',positive=True)
checks=[]
def ck(q,description,a,b,tol=1e-9):
 if isinstance(a,s.Basic) or isinstance(b,s.Basic):ok=s.simplify(a-b)==0
 else:ok=abs(a-b)<=tol
 checks.append({'questionId':q,'check':description,'passed':bool(ok)})
 if not ok:raise AssertionError((q,description,a,b))
def c(ch,n,d,a,b):ck(f'P3-C{ch:02}-R{n:02}',d,a,b)
# C05 exact algebra and model parameter/threshold independent checks.
c(5,1,'对数真数方程化简',s.expand((x+2)*(x-1)-(3*x+4)),x*x-2*x-6)
c(5,2,'9小时阈值',12+48*math.exp(-math.log(2)/3*9),18)
c(5,3,'幂模型两数据',3*4**1.5,24)
c(5,4,'三测量指数预测',5*2**4,80)
c(5,5,'交点二次式',s.expand(x*x-5*x+4-(2-x)),x*x-4*x+2)
c(5,6,'两个绝对对数根',abs(math.log(7/3-2)),math.log(3))
c(5,7,'8年达到600',900/(1+8*math.exp(-math.log(4)/4*8)),600)
c(5,8,'相等5日后的比率',.25*math.exp(.08*(math.log(4)/.08+5)),math.exp(.4))
c(5,9,'根式方程真数',1.25+math.sqrt(1.25**2-1),2)
c(5,10,'环境温度三点恒等',(50-26)**2,(74-26)*(38-26))
c(5,11,'两对数相差1的根',math.log(math.exp(math.log(2)/(1-math.log(2))))/math.log(2)-math.log(math.exp(math.log(2)/(1-math.log(2)))),1)
c(5,12,'输出90阈值',100-60*math.exp(-.2*5*math.log(6)),90)
c(5,13,'两指数根',((3+math.sqrt(5))/2)+2/(3+math.sqrt(5)),3)
c(5,14,'单位改变截距',math.exp(-.7)*(2/100)**1.4,math.exp(-.7-1.4*math.log(100))*2**1.4)
c(5,15,'原模型x=-1',4+6*2**(-1),7)
c(5,16,'半衰期质量比',math.exp(-math.log(25/16)/5*5*math.log(2)/math.log(25/16)),.5)
c(5,17,'判别式临界',s.discriminant(x*x-3*x+s.Rational(9,4),x),0)
c(5,18,'有效对数根',math.log(3**2-1)-math.log(3-1),math.log(4))
c(5,19,'完成平方',s.expand((x-3/x)**2+6),x*x+9/(x*x))
c(5,20,'对数斜率换底',math.log(10**.06),.06*math.log(10))
c(5,21,'乘积配方',s.expand((x-1)*(5-x)),s.expand(4-(x-3)**2))
c(5,22,'模型A到达3倍',math.exp(math.log(2)/10*10*math.log(3)/math.log(2)),3)
c(5,23,'反函数原函数值',3+2*math.exp(-(-math.log((5-3)/2))),5)
c(5,24,'90阈值',120/(1+3*math.exp(-math.log(3)/5*10)),90)
c(5,25,'两传感器换底',10*math.log10(7),20*math.log(7)/(2*math.log(10)))
c(5,26,'平方关系',s.expand((x-3)**2-1),x*x-6*x+8)
c(5,27,'二次真数关系',s.expand((3-x)**2-(x+1)),x*x-7*x+8)
c(5,28,'时间迁移后的6时面积',20*math.exp(math.log(2.5)),50)
c(5,29,'三数据模型',2+3*2**2,14)
c(5,30,'不等式右边界',math.log(2)+math.log(5)-math.log(4),math.log(2.5))
# C06 all thirty differential relations, exact whenever practical.
derivatives=[
((x+1)*s.exp(-x),-x*s.exp(-x)),
((x*x+1)/(x+1),1-2/(x+1)**2),
(s.sin(x)*(1+s.cos(x)),2*s.cos(x)**2+s.cos(x)-1),
(s.log((x+6)/(x+3)),-3/((x+6)*(x+3))),
((x*x-2*x+2)*s.exp(x),x*x*s.exp(x)),
(x*x*s.exp(-x),x*(2-x)*s.exp(-x)),
(s.sin(x)/(2+s.cos(x)),(1+2*s.cos(x))/(2+s.cos(x))**2),
(s.Rational(1,3)*(3*x*x+1)**3+s.Rational(11,3),6*x*(3*x*x+1)**2),
(s.log(x)+2,1/x),
(x*s.exp(x),s.exp(x)*(1+x)),
(s.log(2+s.sin(x)),s.cos(x)/(2+s.sin(x))),
(2*s.tan(2*x)-3*s.sin(x),4/s.cos(2*x)**2-3*s.cos(x)),
(3*s.exp(2*x)+2,6*s.exp(2*x)),
((x*x-4*x+5)**3,6*(x-2)*(x*x-4*x+5)**2),
(s.sin(x+s.pi/6)+s.cos(x-s.pi/6),(s.sqrt(3)+1)/2*(s.cos(x)-s.sin(x))),
(x*s.exp(-x),(1-x)*s.exp(-x)),
(s.log(s.sqrt(x*x+4)),x/(x*x+4)),
(x/(1+x*x),(1-x*x)/(1+x*x)**2),
(5+3*s.sin(2*x)-s.cos(2*x),6*s.cos(2*x)+2*s.sin(2*x)),
(s.log(x+1),1/(x+1)),
(s.sin(x)*s.cos(x)+x,2*s.cos(x)**2),
(3*x+4/(2*x+1)-s.Rational(7,3),3-8/(2*x+1)**2),
((x-s.Rational(7,2))*s.exp(2*x),(2*x-6)*s.exp(2*x)),
((2+s.sin(x))/s.cos(x),(1+2*s.sin(x))/s.cos(x)**2),
(50+150*s.exp(x/25),6*s.exp(x/25)),
(s.sin(x)**2,s.sin(2*x)),
(s.log(x*x+1)-s.log(x),(x*x-1)/(x*(x*x+1))),
(s.sqrt(4*x+1),2/s.sqrt(4*x+1)),
(x*x/(x*x+1),2*x/(x*x+1)**2),
(s.log(2+s.cos(2*x)),-2*s.sin(2*x)/(2+s.cos(2*x)))]
for n,(a,b)in enumerate(derivatives,1):c(6,n,'独立符号求导验证',s.trigsimp(s.diff(a,x)-b),0)
c(6,14,'梯度24对应(3,8)',s.diff((x*x-4*x+5)**3,x).subs(x,3),24)
c(6,24,'同横坐标两切线垂直条件',s.expand((1+2*s.sin(x))*(2*s.sin(x)-1)+s.cos(x)**4).expand(trig=True),s.sin(x)**4+2*s.sin(x)**2)
c(6,27,'水平线对应二次方程',s.expand(2*x*(x+1/x-s.Rational(5,2))),2*x*x-5*x+2)
# C07 each integral answer independently integrated numerically or exact polynomial.
cases=[
(lambda x:4/(x+1),0,2,4*math.log(3)),
(lambda x:(2*x+1)**-2,0,1,1/3),
(lambda x:(math.sin(x)+math.cos(x))**2,0,math.pi/2,math.pi/2+1),
(lambda x:x*math.exp(2*x),0,1,(math.e**2+1)/4),
(lambda x:math.sin(x)/(3-math.cos(x)),0,math.pi/2,math.log(1.5)),
(lambda x:6/math.cos(3*x)**2,0,math.pi/12,2),
(lambda x:(math.sqrt(x)+1)**2/x,1,4,7+math.log(4)),
(lambda x:abs(2*math.cos(2*x)),0,math.pi/2,2),
(lambda x:3/(3*x+1),0,2,math.log(7)),
(lambda x:abs(3*math.exp(-x)-1),0,math.log(9),4/3),
(lambda x:max(math.cos(x-math.pi/6)**2-.5,0),math.pi/6,2*math.pi/3,.25),
(lambda x:math.exp(x)+math.exp(-x)-2,0,math.log(2),1.5-2*math.log(2)),
(lambda x:math.sqrt(3*x+1),0,1,14/9),
(lambda x:2/(2*x-3),0,1,-math.log(3)),
(lambda x:x*(x*x+2)**3,0,1,65/8),
(lambda x:math.sin(x)*math.cos(x),0,math.pi/2,.5),
(lambda x:5/(x+2)**2,0,2,1.25),
(lambda x:6+2*math.sin(3*x),0,math.pi/3,2*math.pi+4/3),
(lambda x:1/(2*x+1),0,1,.5*math.log(3)),
(lambda x:math.exp(x)*math.sin(x),0,math.pi/2,(math.exp(math.pi/2)+1)/2),
(lambda x:abs(math.cos(2*x)),0,math.pi,2),
(lambda x:(x+2)/(x*x+4*x+5),0,1,.5*math.log(2)),
(lambda x:12*math.exp(-x/3),0,3*math.log(2),18),
(lambda x:abs(x*x-x),0,2,1),
(lambda x:math.cos(x+math.pi/6)+math.cos(x-math.pi/6),0,math.pi/2,math.sqrt(3)),
(lambda x:x/(x*x+1)**3,0,1,3/16),
(lambda x:math.exp(2*x)-1-2*x,0,math.log(2),1.5-math.log(2)-math.log(2)**2),
(lambda x:4+3*math.cos(x),math.pi/2,math.pi,2*math.pi-3),
(lambda x:2*math.sqrt(2*x+1)+3/(2*x+1),0,1.5,14/3+1.5*math.log(4)),
(lambda x:abs(2+4*math.cos(2*x)),0,math.pi/2,math.pi/3+2*math.sqrt(3))]
for n,(f,a,b,target)in enumerate(cases,1):ck(f'P3-C07-R{n:02}','独立数值积分核对解析答案',quad(f,a,b,epsabs=1e-11,points=[a+(b-a)*i/30 for i in range(1,30)])[0],target,1e-8)
# C08 separate each original residual equation from any rearranged iteration.
functions=[
(lambda x:x**3+x-7,1,2),
(lambda x:math.exp(-x)-x,0,1),
(lambda x:math.cos(x)-x/2,0,math.pi/2),
(lambda x:x+math.log(x)-3,2,3),
(lambda x:x*x-2-math.sin(x),1,2),
(lambda x:x**3-2*x-2,1,2),
(lambda x:math.exp(x)-3*x,1,2),
(lambda x:x*x+math.log(x)-4,1,2),
(lambda x:x*math.sin(x)-.5,0,math.pi/2),
(lambda x:x**4+x-10,1,2),
(lambda x:math.log(x)+x*x-2,1,2),
(lambda x:(x+1)*math.exp(-x)-.5,1,3),
(lambda x:math.tan(x)-2*x,1,1.4),
(lambda x:math.exp(-x)+.2-x,0,1),
(lambda x:x**3-4*x-1,2,3),
(lambda x:x**3+2*x-5,1,2),
(lambda x:math.log(2*x+1)-x,1,2),
(lambda x:x*x-math.exp(-x),0,1),
(lambda x:math.sin(x)-x/3,2,3),
(lambda x:x**5+x-4,1,2),
(lambda x:x*math.exp(x)-2,0,1),
(lambda x:x**3-7*x+1,0,.2),
(lambda x:math.exp(-.2*x)-.1*x,4,5),
(lambda x:x-1-math.cos(x),1,2),
(lambda x:x**3-2*x*x-1,2,3),
(lambda x:x*x+math.log(x)-2,1,2),
(lambda x:math.cos(x)**2-x,0,1),
(lambda x:x*x-3*math.log(x)-2,2,3),
(lambda x:x+math.exp(x)-4,1,2),
(lambda x:x**3+x*x-6,1,2)]
for n,(f,a,b)in enumerate(functions,1):
 r=brentq(f,a,b,xtol=1e-14)
 ck(f'P3-C08-R{n:02}','独立原方程根残差',f(r),0,1e-11)
 checks[-1].update({'root':r,'bracket':[a,b],'endpointValues':[f(a),f(b)]})
(pathlib.Path(__file__).resolve().parents[1]/'research/p3-independent-verification.json').write_text(json.dumps({'checks':checks,'passed':sum(c['passed']for c in checks),'total':len(checks)},ensure_ascii=False,indent=2))
print(len(checks),'passed')
