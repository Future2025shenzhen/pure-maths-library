"""Reviewed P3 June 2024 official answer tables and Chinese mark summaries."""
import json,fitz
from pathlib import Path
root=Path(__file__).resolve().parents[2];p=root/'dist/data/past-bank.json';bank=json.load(open(p))
ends={1:(7,240),2:(8,338),3:(10,388),4:(12,383),5:(14,364),6:(16,385),7:(18,347),8:(20,355),9:(22,426)}
qa={
1:('从绝对值函数读出顶点两个坐标（2个 B1）；按 x≤5 与 x≥5 分支解不等式并检验范围（M1、A1）；将顶点横坐标加 2、纵坐标乘 3（2个 B1ft）。','P=(5,10)；不等式解为 x<5/2；变换后 P 映为 (7,30)。'),
2:('用代数除法或恒等式比较系数，逐步求出三个常数（M1、dM1、A1）；把 g(x) 逐项积分，保留 ln|x−2|（M1、A1ft），代入 4、8 并相减（dM1、A1）。','g(x)=2x−1+6/(x−2)；∫₄⁸g(x)dx=44+6ln3。'),
3:('第 (i) 小题取常用对数，整理为直线方程，并标出两个轴截距（3个 B1）；第 (ii) 小题从图求斜率 2 和截距 4，再两边取 3 的幂（B1、M1、A1）。','(i) log₁₀y=6−3log₁₀x，截距 (0,6)、(2,0)；(ii) N=81·9ᵗ。'),
4:('用倍角公式把 f 化为 4sin2x+2cos2x−1（M1、dM1、A1）；比较 Rsin(2x+α) 的系数，求 R、α（B1ft、M1、A1）；由正弦最大值求 f 的最大值，再考虑周期选第二个正 x（B1ft、M1、A1）。','R=2√5，α≈0.464；f 的最大值为 2√5−1；第二个正 x≈3.70。'),
5:('由 2+5ln x=22 求反函数值（M1、A1）；商法则得 g′(x)=10/(2x+1)²>0，证明递增（M1、A1、A1）；交换变量并解出 g⁻¹，同时给出定义域（M1、A1、B1）；由 g(x)∈(0,3) 推出 fg 的值域（M1、A1）。','f⁻¹(22)=e⁴；g⁻¹(x)=(x+2)/(6−2x)，0<x<3；fg 的值域为 (−∞,2+5ln3)。'),
6:('对 y=√(4x−7) 用链式法则求导，在 P(8,5) 求切线梯度并取负倒数，列法线方程（M1、A1、dM1、ddM1、A1）；积分曲线下与法线围出的部分并组合面积（M1、A1、dM1、A1）。','法线 l：5x+2y−50=0；区域 R 的精确面积为 155/6。'),
7:('展开 sin(x+45°) 与 cos(x−60°)，收集 sin x、cos x 并求 tan x（M1、A1、M1、A1）；设 x+45°=2θ，使用前问结果及正切周期求区间内两解（B1、M1、dM1、A1）。','tan x=−2−√3；θ=75°、165°。'),
8:('令 h=0，除去起点 x=0 后取对数求 d（M1、dM1、A1）；对 h 求导、令导数为零并整理成题给迭代式（M1、A1、dM1、A1）；按迭代式求横坐标，再反复迭代求达到最大高度时的水平距离并附单位（M1、2个 A1）。','d≈54.93 m；x₂≈31.43；达到最大高度时的水平距离≈30.88 m。'),
9:('将 y=π/3 代入曲线验证 k（B1）；求 dx/dy=8sin y cos y，再取倒数并以 sin²y=(x+1)/4 化成只含 x 的式子（M1、A1、M1、dM1、ddM1、A1）；由 P 处法线的斜率求 N，再用三角形底乘高的一半（M1、dM1、A1）。','k=2；dx/dy=8sin y cos y；dy/dx=1/[2√(x+1)√(3−x)]；面积=π/3+π²/(36√3)。'),
}
doc=fitz.open(root/'dist/assets/past-papers/p3-jun-2024-ms.pdf')
for q in bank['questions']:
 if q['paper']!='p3-jun-2024':continue
 n=q['number'];page_no,end=ends[n];page=doc[page_no-1];w,h=page.rect.width,page.rect.height
 q['markSchemePages']=[{'page':page_no,'pdf':'assets/past-papers/p3-jun-2024-ms.pdf','renderFromPdf':True,'width':round(w*1.55),'height':round(h*1.55),'crop':[.035,round(25/h,6),.93,round((end-25)/h,6)],'highlights':[]}]
 q['quickCheckZh']={'process':qa[n][0],'answer':qa[n][1]};q['manualAnswerReview']='2026-10-24: question and official scheme checked'
p.write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
