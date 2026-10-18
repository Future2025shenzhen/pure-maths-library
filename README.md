# Pure Maths Library

在线网站：https://future2025shenzhen.github.io/pure-maths-library/
历年真题：https://future2025shenzhen.github.io/pure-maths-library/past.html

## 内容
- 原创750题：P1九章、P2八章、P3八章，每章30题。本轮实质重写68题，另7题作细节校正。
- 真题323题：用户上传的2020—2023年33套原卷，P1 109题、P2 109题、P3 105题。保留原图原页和原题号，附中文分步解答及官方评分标准。
- 2019年5套暂列外部原卷链接，未计入323题，尚未逐题配中文解答。
- 教材阅读、阶段/章节/知识点筛选、收藏、手动已做、随机练习。无在线作答/自动判分。

## 编辑数据
网页与数据分离。dist/data/bank.json 是原创网页题库；rewrite-source.json 是完整编辑格式；past-bank.json 是真题目录和中文解答。修订ID记录见revision-record.json。图像、教材、原卷和本地数学组件均在dist/assets中。

## 运行与发布
安装Node.js，运行 npm start，访问 http://localhost:4173 。不能直接双击HTML读取JSON。
GitHub Pages已启用；更新main分支会自动校验两类题库并发布。日常发布完全使用仓库已有文件，不再运行首次迁移下载脚本，也不依赖chatgpt.site。scripts/migrate.py及migration-manifest.json仅保留首次迁移记录。

## 复核
所有33卷逐题计数与原卷封面一致，各75分；原创25章各30题。浏览器验证323道原题的原页图像与中文公式、筛选、随机练习、收藏/已做持久化和PDF阅读器。原创公式及分值通过数据检查；研究细节见网站research.html。
当前为内部编辑复核稿，尚未有外部教师逐题审定。原卷版权归Pearson，中文解答为编辑内容，非官方产品。中国大陆访问稳定性需要国内网络实测。
