# 数学真题：仅显示官方答案、过程和得分点

范围：原仓库 `5996927` 中真题练习区的 P1/P2/P3 全部 58 套、572 题。题号、题面、图片、分类、分值及原始官方试卷/评分标准均保留；移除此前自编中文解答和摘要，练习页统一显示官方评分表的直接摘录。

每套评分标准按印刷题号重新对应，保留答案表及续页、各小问、官方替代解法和 M/A/B 得分代码。去掉独立 Notes 栏、全宽评分说明、表内 Note 脚注及指向 Notes 的括注，不绘制额外的框或高亮。原评分表的线条、公式、图形与得分代码来自官方 PDF。跨栏公式与无独立得分栏的草图保留；删除说明形成的大块空白在相应行内收紧。

`dist/assets/past-answers-v20/` 是从原件裁取的矢量 PDF，供已有 PDF.js 渲染器显示。点击摘录仍打开原始官方评分标准的对应原页。

- `rebuild_official_answers.py`：可重复重建，需 PyMuPDF 1.26.6。临时表格缓存保存在 `/tmp`，按原件 SHA-256 失效；不在无 PDF 依赖的发布流水线中运行。
- `official-answer-audit.json`：每题原始 PDF、文件 SHA-256、原页、全部拷贝矩形、对应评分行。
- `question-source-fingerprints.json`：改动前全部572题的非答案字段指纹，防止修改题面、题号或分类。
- `validate_official_answers.py` / `pdf-content-audit.json`：直接检查58份输出PDF的全部572题，不含 Note 文字和 PDF 批注，并确认可提取的评分分配不少于题目总分（替代解法可能有额外的一套分配）。
- `scripts/check-v20.mjs`：所有题目只显示官方摘录、原件来源与页号正确、非答案字段保持原样，渲染器没有额外画框逻辑。

验证：`npm run check`、`npm test`、`python3 editorial/v20/validate_official_answers.py`。已对含独立 Notes 栏、合并单元格、草图、双列替代解法、跨页与间隔评分代码的输出做 PDF 图像抽查。
