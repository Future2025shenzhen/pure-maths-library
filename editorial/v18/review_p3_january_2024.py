"""Reviewed P3 January 2024 official answer spans and Chinese mark summaries."""
import json,fitz
from pathlib import Path
root=Path(__file__).resolve().parents[2];file=root/'dist/data/past-bank.json';bank=json.load(open(file))
spans={1:[(7,45,207)],2:[(8,45,330)],3:[(10,45,451)],4:[(12,60,749)],5:[(16,60,395)],6:[(18,30,320)],7:[(19,45,514)],8:[(23,60,210),(24,45,367)],9:[(26,45,291),(27,30,319)]}
qa={
1:('对 f(2x) 将横坐标除以 2（B1）；对 3f(x−1) 将横坐标加 1、纵坐标乘 3（2个 B1）；对 |f(x)| 把负纵坐标取绝对值（B1）。','(a) (−2,−3)；(b) (−3,−9)；(c) (−4,3)。'),
2:('代入 x=2、3 得 f(2)=−3、f(3)=41，写出连续且变号（M1、A1）；从 f(x)=0 整理为题给迭代式（B1）；由 x₁=2 计算 x₂ 和收敛根（M1、2个 A1）。','f(2)=−3，f(3)=41；x₂=2.1179；α=2.1565。'),
3:('用对数法则把模型写为 10¹·⁰⁴(10⁰·³⁸)ᵗ，计算 a、b 至四位有效数字（M1、2个 A1）；令 D=45000 解 T（M1、A1）；代入 t=12 与 £350000 比较（M1、A1）。','D≈10.96(2.399)ᵗ；T≈9.51 月；12 个月约 £400000，能达到目标。'),
4:('因式分解并约去公因式，证明 f(x)=2x/(3x−5)（B1、M1、A1）；求导得负值，并解释分母平方为正（M1、A1、A1）；求 g⁻¹ 时解指数方程并注明定义域（M1、A1、B1）；令 gf(a)=5，取指数并求 a（B1、M1、dM1、A1）。','f′(x)=−10/(3x−5)²<0；g⁻¹(x)=e^((x−3)/2)，x≥3；a=5e/(3e−2)。'),
5:('以 t=0、T=18 求 A（B1）；代入 t=45、T=16 后取对数求 B（M1、dM1、A1）；对模型求导并在 t=2 计算降温速率（M1、A1）；指出模型下限为 10°C，因此不能到 5°C（B1）。','A=8；B≈0.00639；t=2 时 dT/dt≈−0.0505 °C/min；永远不会降至 5°C。'),
6:('读图求精确 x 轴交点（B1）；用乘积法则求导，再用 cos²x=1−sin²x 化为关于 sin x 的二次方程（M1、A1、dM1、A1）；解方程并根据 Q 的位置选择正确横坐标（M1、A1）。','R=(3π/2,0)；3sin²x+sin x−3=0；Q 的 x≈2.131。'),
7:('对含 k 的分式求导并化简（M1、A1）；在 x=1 令导数为 −12，解出两个 k（M1、dM1、A1）；根据 k<3 选 7/3，求点 P 与法线方程（M1、dM1、A1）；换元积分并代入上下限，整理对数商（M1、A1ft、dM1、A1）。','k=7/3 或 11/3；当 k<3 时法线为 12y−x−31=0；λ=16/27。'),
8:('从 y=a−|2x−b| 读出顶点、y 截距和两 x 截距（5个 B1）；画出 y=|x|−1 的 V 形及顶点（2个 B1）；分别代入 x=−3、5 两个交点并联立求 a、b（M1、dM1、ddM1、A1）。','顶点 (b/2,a)，y 截距 (0,a−b)，x 截距 ((b−a)/2,0)、((a+b)/2,0)；a=11，b=3。'),
9:('用 sin2θ、cos2θ 的恒等式把原式化为 3sin2θ−4cos2θ=2（M1、dM1、A1）；写为 5sin(2x−α)=2 并在指定区间筛选解（M1、dM1、A1、ddM1、A1）。','3sin2θ−4cos2θ=2；x≈3.81（3位有效数字）。'),
}
doc=fitz.open(root/'dist/assets/past-papers/p3-jan-2024-ms.pdf')
for q in bank['questions']:
 if q['paper']!='p3-jan-2024':continue
 n=q['number'];refs=[]
 for page_no,top,end in spans[n]:
  page=doc[page_no-1];w,h=page.rect.width,page.rect.height
  refs.append({'page':page_no,'pdf':'assets/past-papers/p3-jan-2024-ms.pdf','renderFromPdf':True,'width':round(w*1.55),'height':round(h*1.55),'crop':[.035,round(top/h,6),.93,round((end-top)/h,6)],'highlights':[]})
 q['markSchemePages']=refs;q['quickCheckZh']={'process':qa[n][0],'answer':qa[n][1]};q['manualAnswerReview']='2026-10-24: question and official scheme checked'
file.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
