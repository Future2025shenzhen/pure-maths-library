"""Checked P3 October 2024 question/official-scheme pairs and answer summaries."""
import json
from pathlib import Path

import fitz

root = Path(__file__).resolve().parents[2]
bank_file = root / 'dist/data/past-bank.json'
bank = json.loads(bank_file.read_text())
scheme_path = 'assets/past-papers/p3-oct-2024-ms.pdf'
doc = fitz.open(root / 'dist' / scheme_path)

# Printed answer tables only. The surrounding examiner notes are deliberately excluded.
spans = {1: (7, 45, 220), 2: (9, 50, 284), 3: (11, 50, 694),
         4: (13, 45, 290), 5: (15, 50, 467), 6: (17, 45, 357),
         7: (19, 45, 408), 8: (21, 45, 474), 9: (23, 90, 634)}

answers = {
    1: ('用 tan²θ=sec²θ−1 化为 3sec²θ+7secθ−6=0（M1、A1）；因式分解得 secθ=2/3 或 −3，前者因 |secθ|≥1 舍去（dM1）；在指定范围找两个角并取一位小数（2个 A1）。',
        'θ=109.5°、250.5°。'),
    2: ('先对 x=2y²+5y−6 求 dx/dy，再取倒数求 dy/dx（M1、A1）；竖直切线须满足 dx/dy=0，得到 y=−5/4（M1）；代回原曲线求 x（dM1、A1）。',
        '(a) dy/dx=1/(4y+5)；(b) P=(−73/8,−5/4)。'),
    3: ('令 u=|x|≥0，解 2u²−10u=48，并把 u=8 还原为正负两个 x；u=−3 不合定义（B1、M1、A1）。不等式分别比较 f(x)=5x/2 和 f(x)=−5x/2 两条边界（M1、dM1），找到 15/4、25/4 后用图像或分段判断区间（2个 A1）。',
        '(a) x=−8、8；(b) x≤15/4 或 x≥25/4。'),
    4: ('令 t=0 算 N=10²（B1）；对 log₁₀N=.35t+2 两边取 10 的幂，拆成 10²(10^.35)ᵗ 并把底数取两位小数（M1、dM1、A1）；对所得模型求导并代 t=5（M1、A1）。',
        '(a) 100；(b) N=100(2.24)ᵗ；(c) 约 4548 个/小时（4530–4550 可接受）。'),
    5: ('用 sin(2x+x) 展开，代入倍角公式并用 cos²x=1−sin²x，逐步得到三倍角式（M1、dM1、2个 A1）；代回方程后先提出 sinθ=0 的分支，再解 4cos²θ−5cosθ−1=0，检查 0<θ≤360°（M1、dM1、2个 A1）。',
        '(a) P=3，Q=−4，即 sin3x=3sinx−4sin³x；(b) θ=100.1°、180°、259.9°、360°。'),
    6: ('先求 f(2)=3，再算 g(3)（M1、A1）；交换 x、y 并解分式方程求反函数，利用 f 在 x≥0 上的值域确定反函数定义域（M1、A1、B1）；把 gg(x)=126 化为 (x²+5)²=121，注意 x²+5 必为正，再解 x²=6（M1、dM1、A1）。',
        '(a) gf(2)=14；(b) f⁻¹(x)=3(x+1)/[2(6−x)]，定义域 −1≤x<6；(c) x=±√6。'),
    7: ('对 x³√(4x+7) 用乘积及链式法则，通分化简得 k=7（M1、A1、dM1、A1）；驻点 x=−3/2 代回求 P（M1、A1）；用最小值 −27/8 变换得 g 的上界（M1、A1）；Q 横坐标右移 3/2，纵坐标乘 40 再减 8（M1、A1）。',
        '(a) k=7；(b) P=(−3/2,−27/8)；(c) g(x)≤27/2；(d) Q 映至 (2,7)。'),
    8: ('代 t=0 求初始值、令 t→∞ 求长期值（各 B1）；求 dH/dt=−8e⁻⁰·²ᵗ+18e⁻⁰·⁹ᵗ，令导数为零并解 4e⁰·⁷ᵗ=9（M1、A1、dM1、M1、A1）；把 H=37 整理成 e⁻⁰·²ᵗ=(1+4e⁻⁰·⁹ᵗ)/8，再取对数得到迭代式（M1、A1）；代 t₁=10 求 t₂，继续迭代至四位小数稳定（M1、2个 A1）。',
        '(a) 52 bpm；(b) 32 bpm；(c) T=1.158 分钟；(d) t=5ln[8/(1+4e⁻⁰·⁹ᵗ)]；(e) t₂=10.3947，M=10.3955 分钟。'),
    9: ('用商法则并化简导数（M1、2个 A1）；代 x=2 求切线斜率 16/5，取负倒数 −5/16 写出法线（M1、dM1、A1）；长除或比较系数得 A=3、B=1/2、D=−5/2（B1、M1、A1）；积分 3x+1/2−5/[2(2x+1)]，代曲线截点 −1/3 与 P 的横坐标 2，再加法线与 x 轴构成的三角形面积（M1、A1ft、dM1、M1、A1）。',
        '(a) f′(x)=(12x²+12x+8)/(2x+1)²；(b) 16y+5x=106；(c) f(x)=3x+1/2−5/[2(2x+1)]；(d) 面积=964/15−(5/4)ln3。'),
}

reviewed = []
for question in bank['questions']:
    if question['paper'] != 'p3-oct-2024':
        continue
    number = question['number']
    page_number, top, bottom = spans[number]
    page = doc[page_number - 1]
    height = page.rect.height
    question['markSchemePages'] = [{
        'page': page_number, 'pdf': scheme_path, 'renderFromPdf': True,
        'width': round(page.rect.width * 1.55), 'height': round(height * 1.55),
        'crop': [.035, round(top / height, 6), .93, round((bottom - top) / height, 6)],
        'highlights': [],
    }]
    question['quickCheckZh'] = {'process': answers[number][0], 'answer': answers[number][1]}
    question['manualAnswerReview'] = '2026-10-24: original question and official answer table checked'
    clip = page.get_text(clip=fitz.Rect(20, top, 570, bottom))
    assert 'Total' in clip and 'Notes:' not in clip, (number, clip)
    reviewed.append(question['id'])

assert len(reviewed) == 9, reviewed
bank_file.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + '\n')
