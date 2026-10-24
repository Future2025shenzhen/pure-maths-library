Cambridge IGCSE 2019–2024 物理和计算机科学真题
整理日期：2026-10-24

本包是下载工具和清单，不是已经包含全部 PDF 的小压缩包。

Windows 使用方法：
1. 下载压缩包。右键 → 全部解压；不要在压缩包内直接双击运行。
2. 打开解压后的文件夹，双击 START-DOWNLOAD.cmd。
3. 保持联网和黑色窗口开启。无需安装 Python，也无需管理员权限。
4. 程序会在 Windows 当前用户的桌面（兼容系统登记的 OneDrive 桌面）建立：
   Cambridge-IGCSE-2019-2024
5. 按科目 → 年份 → 考季 → 资料类型保存，完成后自动打开此文件夹。
6. 双击桌面文件夹里的 index.html，可搜索和打开已下载文件。
7. 中断或失败后再次运行即可；已通过校验的文件会跳过。失败详情在 download-log.csv。

总计793个文件，约578 MB原始文件，建议预留1 GB空间。
Physics 0625：251份题卷、251份评分标准，以及67份辅助资料，共569份PDF。
Computer Science 0478：84份题卷、84份评分标准，以及56份辅助资料，共224个文件。
两科共335份题卷及335份匹配评分标准。辅助资料包括已找到的实验说明、历史预发布材料、考官报告和分数线，辅助资料不保证每季齐全。
范围为2019至2024年，包含2024年；按已找到的Feb/March、May/June、Oct/Nov及variant整理。

重要缺口：
0625_s20_qp_33.pdf 与 0625_s20_ms_33.pdf 未在核对的公开存档中找到，发布情况未确认，不把它们算作已收集。
若你说的“2024年之前所有”还包括2018年及更早，本次尚未包含；本次按2019–2024这个明确区间整理。
本包假定课程代码为Physics 0625和Computer Science 0478，不是9–1课程代码0972/0984，也不是A Level 9702/9618。

文件名：
m=Feb/March，s=May/June，w=Oct/Nov；19–24=年份。
qp=Question Paper题卷；ms=Mark Scheme评分标准。
pm=Pre-release Material历史预发布材料；ci=Confidential Instructions实验准备说明。
er=Examiner Report考官报告；gt=Grade Threshold分数线。
例如0625_s24_qp_42.pdf：2024年夏季物理Paper 4 Variant 2题卷。

课程变动：
计算机2023年起取消Paper 2的pre-release assessment，旧版材料仍可练习，但不能当成现行卷型。
Cambridge官方说明：https://help.cambridgeinternational.org/hc/en-gb/articles/23007179810194-When-will-the-pre-release-material-for-IGCSE-Computer-Science-be-available-and-how-do-I-access-it

来源与检查：
公开镜像：Upppllld/OpenPastPapers、edgeituploads/0625、edgeituploads/0478、iiVertex/IG-Wizard、Sam-SSTU/IGCSE-and-ALEVEL-Materials-for-study等GitHub存档。
每个文件的来源固定提交、URL、大小和SHA-256见manifest.json及file-list.csv。
已下载并检查PDF能解析、ZIP能读取，按文件名配对QP/MS；不是逐题审校官方答案。未宣称已在你的Windows实机运行过工具。
剔除了3个实际为网站登录页的错误物理文件。3份计算机2022年夏季预发布资料实际是PDF但存档扩展名为ZIP，保存时改为.pdf，内容字节保持原样。
原试卷版权归Cambridge相关权利人，个人复习使用；本包不是Cambridge官方发行版。

工具说明：
脚本只下载清单中的PDF/ZIP，校验SHA-256并保存日志，不执行下载的资料。
START-DOWNLOAD.cmd中的ExecutionPolicy Bypass仅作用于本次PowerShell进程，不永久修改系统设置。
不需要账户、密码、Token；程序不读取浏览器或网站账户。
网络不可达时会列出失败，不会把未完成显示成全部完成。
如果学校电脑策略阻止脚本，请不要关闭全局防护，改用完整PDF压缩包，或请学校IT协助。
