"""Human-reviewed P3 June 2025 scheme spans and Chinese mark summaries."""
import json
import fitz
from pathlib import Path
root=Path(__file__).resolve().parents[2]
base=json.load(open(root/'dist/data/past-bank.json'))
# Page, first/last Y in PDF points. Each span ends at the printed part mark or Total,
# excluding the examiner's prose notes, even when they share the same PDF page.
spans={
 1:[(7,55,249),(8,45,325)],
 2:[(9,50,322)],
 3:[(10,50,157),(11,35,365)],
 4:[(13,50,285),(14,45,197)],
 5:[(15,50,263)],
 6:[(16,50,270),(17,45,193)],
 7:[(18,50,296),(19,45,345)],
 8:[(20,50,334),(22,55,272)],
 9:[(23,50,205),(24,45,253),(26,45,245)],
 10:[(28,50,188),(29,45,167),(30,50,233)],
}
summaries={
 1:('先代入 f(1) 再代入 g（M1）；根据 x≥0 求 f 的值域（2个 B1）；由 y=2x/(3x+1) 换元解出反函数（M1、A1）；令反函数与 f 相等并解方程（M1、A1）。','gf(1)=15/4；f 的值域为 [0,2/3)；f⁻¹(x)=x/(2−3x)；x=0 或 1/3。'),
 2:('比较余弦形式的系数，求 R 和 α（B1、M1、A1）；利用 cos 的最小值 −1 求 g 的最小值（M1、A1），再解 x+α=π+2kπ 并选最小正值（M1、A1）。','R=25，α≈1.287；g 的最小值为 1/33，最小正 x≈0.927。'),
 3:('用两点求 log₁₀y 对 log₁₀x 的斜率与截距（M1、A1）；两边取 10 的幂，并把 10⁻² 与 x 的幂分开（M1、dM1、A1）。','log₁₀y=−(4/7)log₁₀x−2；y=(1/100)x⁻⁴⁄⁷。'),
 4:('把 x²+ x−12 分解成 (x+4)(x−3)，通分约简后展示 f(x)=7x/(x−3)（M1、A1、A1）；再用商法则或重写为 7+21/(x−3) 求导（M1、A1）。','f(x)=7x/(x−3)；f′(x)=−21/(x−3)²。'),
 5:('第 (i) 小题先用 sin²3x=(1−cos6x)/2（M1），再逐项积分并加常数 C（A1）；第 (ii) 小题令 u=x²+4，以 du=2x dx 换元（M1），积分并还原（A1）。','(i) x/2−sin(6x)/12+C；(ii) (x²+4)⁵⁄²/5+C。'),
 6:('代入 t=0、θ=75 求 A（M1、A1）；用 t=5、θ=25 建立指数方程并取对数求 k（2个 M1、A1）；求 dθ/dt，令其为 −9 并用对数求 T（M1、dM1、A1）。','A=54；k≈0.521；T≈2.19 分钟。'),
 7:('用乘积法则、链式法则求导并令导数为零，整理出给定迭代式（M1、A1、dM1、A1）；按式计算 x₂、x₄（M1、2个 A1）；选择函数在 0.4295 与 0.4305 计算异号，证明三位小数（M1、A1）。','x₂=0.4367，x₄=0.4307；驻点横坐标为 0.430（3位小数）。'),
 8:('用 tan(2x+x) 的加法公式和倍角公式证明恒等式（M1、dM1、A1）；代入后用 sec²=1+tan²，化成关于 tan3θ 的二次方程（M1、A1）；解方程并筛选 0<θ<2π 内所有解（dM1、2个 A1）。','tan3x=(3tan x−tan³x)/(1−3tan²x)；θ≈0.37、0.72、1.42。'),
 9:('令 x=0 并结合给定 y 范围，求两个 y 轴交点（M1、2个 A1）；由 x=(2/3)sin(3y+π/4) 求 dx/dy，再取倒数和平方化简（B1、M1、dM1、A1）；用 A 处法线与 B 处切线的梯度列直线方程并联立（B1ft、M1、dM1、A1）。','两个 y 坐标为 π/4、7π/12；dy/dx=(4−9x²)⁻¹⁄²；D 的 x 坐标为 2π/9。'),
 10:('代入 x=0 求 A，令绝对值内为零求顶点（3个 B1）；分别处理 kx−10 的正负两支并解不等式（M1、dM1、A1）；用两条直线产生两个不同交点的条件，求 k 的下界和顶点相交时的上界（B1、M1、2个 A1）。','A 的 y=10+k，P=(10/k,k)；x≤(10−k)/k 或 x≥(10+k)/k；3<k<6。'),
}
for q in base['questions']:
 if q['paper']!='p3-jun-2025':continue
 n=q['number'];pdf='dist/'+base['papers'][next(i for i,p in enumerate(base['papers']) if p['id']==q['paper'])]['markScheme'];doc=fitz.open(root/pdf)
 refs=[]
 for page_no,top,bottom in spans[n]:
  page=doc[page_no-1];pagew,pageh=page.rect.width,page.rect.height
  # Frame only the printed scheme, leaving no examiner note paragraphs.
  refs.append({'page':page_no,'pdf':pdf.removeprefix('dist/'),'renderFromPdf':True,'width':round(pagew*1.55),'height':round(pageh*1.55),'crop':[.035,round(top/pageh,6),.93,round((bottom-top)/pageh,6)],'highlights':[]})
 q['markSchemePages']=refs;q['quickCheckZh']={'process':summaries[n][0],'answer':summaries[n][1]};q['manualAnswerReview']='2026-10-24: question and official scheme checked'
open('/tmp/past-bank-two-reviewed.json','w').write(json.dumps(base,ensure_ascii=False,indent=2)+'\n')
