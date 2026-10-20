# Pure Practice · P1 / P2 / P3

网站：https://future2025shenzhen.github.io/pure-maths-library/

当前原创题库：第9版，770道实质改编题：原750题保持不变，P3微分增加10道、P3积分及P2微分各增加5道提高题。每章至少30题。题目英文、答案中文、逐题有2024年前真题考法参照及改编说明，配图重绘。另有33套2020—2023年原卷、323道原题及官方答案，原图原页保持不变。

运行：安装Node.js后，在项目目录执行 `npm start`，打开 http://localhost:4173 。检查执行 `npm run check` 和 `npm test`。前端不需安装依赖；已配置的云端账户需联网。

数据：`dist/data/bank.json`（原创题）、`dist/data/past-bank.json`（真题）、`dist/data/classification.json`（检索分类）。基础题源稿见 `editorial/v7/`，新增提高题源稿与核查记录见 `editorial/v8/`。所有原创题头显示全部关联章节；搜索“提高题”查看新增题。现有数据库需执行 `backend/004-challenge-catalog.sql` 登记20个新题号，方可云端收藏、标记已做及保存含新题的练习卷。账户与管理员开通说明见 `backend/README.md`。

新题库保留题号与历史收藏/已做状态；旧已做不代表已完成新题。所有核查为内部复核，未完成外部教师逐题审阅。网站不提供在线作答或自动判分。

第9版：中文思路与有序解题步骤、47处局部英文措辞规范化、个人文字备注及收藏摘要。题号、阶段与题量保留；三处答案纠错见editorial/v9/corrections.json。重建使用scripts/build-v9-bank.py。云端备注需项目所有者执行backend/005-question-notes.sql，管理员页面notes-setup.html提供复制SQL及状态检查。

当前网站视觉：V10（清澜山G10青云班校园视觉），内容修订仍为V9。美化前V9已固定在提交`925f75d16adf2b40bb58d951a78c13ee47b2709f`及分支`archive/v9-before-tsinglan-design-20261021`，回退说明见releases/README.md。校园图为本地AI意象资源，非实景照片；官网参考与图像说明见design.html。
