"""Apply individually checked P3 January 2025 answer rows and mark summaries."""
import json,fitz
from pathlib import Path
root=Path(__file__).resolve().parents[2]
bank=json.load(open(root/'dist/data/past-bank.json'))
ends={1:(5,306),2:(6,163),3:(7,232),4:(8,532),5:(10,407),6:(12,381),7:(13,504),8:(15,333),9:(17,319),10:(18,496)}
qa={
1:('在 0.1、0.2 代入 f，写出两端异号且函数连续（M1、A1）；从 f(x)=0 整理为题给迭代式（B1）；从 x₁=0.15 迭代求 x₂ 和收敛值（M1、2个 A1）。','f(0.1)≈−0.39，f(0.2)≈0.24；x₂=0.1629；α=0.1622。'),
2:('令 t=0 得初始面积（B1）；将 A=25 代入 log₁₀A=1+0.03t，移项并除以 0.03（M1、A1）。','初始面积为 10 m²；T=(log₁₀25−1)/0.03≈13.26 周。'),
3:('用商法则或乘积法则求 dy/dx（M1、A1）；令导数大于 0，求出两个临界值并结合 x≠−3 作符号判断（M1、A1、B1、A1）。','曲线递增的范围为 −3<x<5/2。'),
4:('作代数除法或通分比较系数，找到 A、B、C（B1、M1、A1），并由常数项证明 D=0（B1）；逐项积分并保留 ln(x+4) 项（B1ft、M1、A1ft），代入上下限相减（dM1、A1）。','A=4，B=2，C=−13，D=0；定积分=36−13ln2。'),
5:('初值在 t=0 代入（B1）；草图从 304°C 单调下降并渐近于 H=24（M1、A1）；令 H=144，取对数求 t（M1、dM1、A1）；用链式法则求导，再用 H−24=280e⁻⁰·⁰⁵ᵗ 消去指数项（M1、M1、A1）。','初始温度 304°C；渐近线 H=24；H=144 时 t≈16.95 分钟；dH/dt=1.2−0.05H。'),
6:('由 y=(4x+3)/(x−2) 交换 x、y 并解出反函数，注明其定义域（M1、A1、B1）；将 f(x) 代入 f 得复合函数并通分（M1、dM1、A1）；变换 y=2f(3x)+8 使 P 的横坐标除以 3、纵坐标乘 2 后加 8（M1、A1）。','f⁻¹(x)=(2x+3)/(x−4)，x≠4；ff(x)=(19x+6)/(2x+7)；P 映为 (1,38)。'),
7:('两幅图分别给出 V 形、顶点和 y 轴截距，各占 B1；解方程时按绝对值两支讨论，再检验分支范围，舍去不合条件的根（M1、A1）。','(i) 顶点 (a/3,0)、y 截距 (0,a)；(ii) 顶点 (a/3,−b)、y 截距 (0,a−b)；唯一解 x=(a−b)/8。'),
8:('第 (i) 小题先用 cosecθ=1/sinθ 和 sin2θ=2sinθcosθ 化简（B1、M1、A1），在 0<θ<π 内取两个解（M1、A1）；第 (ii) 小题反用正切加法公式整理，再取反正切并考虑 180° 周期（M1、A1、dM1、A1）。','(i) θ≈0.424、1.15 弧度；(ii) x≈24.7°、114.7°。'),
9:('由 ln(4x)=0 求 x 轴交点（B1）；用乘积法则求导（M1、A1），令导数为零求 x 并代回求 y（dM1、2个 A1）；将 f 的最低点乘 −2，得到 g 的最高值（M1、A1ft）。','P 的 x=1/4；Q=(1/(4e²),−6/e)；g 的值域为 (−∞,12/e]。'),
10:('对 x=3cos2y 求导（M1、A1）；取倒数并用 sin²2y+cos²2y=1，依据图像选负号（M1、dM1、A1）；令梯度为 −1/4 求正的 a，再代回曲线求正的 b（M1、A1、dM1、A1）。','dx/dy=−6sin2y；dy/dx=−1/(2√(9−x²))，k=−1/2；a=√5，b=(1/2)arccos(√5/3)。'),
}
for q in bank['questions']:
 if q['paper']!='p3-jan-2025':continue
 n=q['number'];page_no,end=ends[n];pdf='assets/past-papers/p3-jan-2025-ms.pdf';page=fitz.open(root/'dist'/pdf)[page_no-1];w,h=page.rect.width,page.rect.height
 q['markSchemePages']=[{'page':page_no,'pdf':pdf,'renderFromPdf':True,'width':round(w*1.55),'height':round(h*1.55),'crop':[.035,round(25/h,6),.93,round((end-25)/h,6)],'highlights':[]}]
 q['quickCheckZh']={'process':qa[n][0],'answer':qa[n][1]};q['manualAnswerReview']='2026-10-24: question and official scheme checked'
(root/'dist/data/past-bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
