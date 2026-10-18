# Pure Maths Library

P1 / P2 / P3 数学题库的独立静态托管仓库。

现有网站包含 750 道原创题、中文解答、题图及教材阅读。新增历年真题与后续质量修订尚未包含在此迁移版本中。

## 迁移状态

282 个网站文件已完整复制到本仓库，逐文件 SHA-256 校验通过。网页运行及日常部署均不再依赖 chatgpt.site。scripts/migrate.py 和 migration-manifest.json 仅保留为首次迁移记录，不在发布流程中运行。

## 首次启用 GitHub Pages

1. 打开本仓库 Settings → Pages。
2. 在 Build and deployment → Source 选择 **GitHub Actions**。
3. 打开 Actions → Publish maths library → Run workflow → main → Run workflow。
4. 等待成功，在 deploy 的环境链接打开网站。以实际部署输出为准。

连接工具不具备首次创建 Pages 站点的管理权限，因此第 2 步需要仓库所有者操作。此后每次更新 main 分支会自动校验并部署。

预期地址： https://future2025shenzhen.github.io/pure-maths-library/ 。启用并部署成功前，此地址可能返回 404。

## 本地运行

安装 Node.js，执行 npm start，打开 http://localhost:4173 。

## 编辑

- dist/data/bank.json：网页题库
- dist/data/rewrite-source.json：完整编辑数据
- dist/assets/rewrite-figures：题图
- dist/assets/rewrite-books：题册
- dist/assets/p1.pdf、p2.pdf、p3.pdf：教材

所有前端依赖均存放在本站。收藏和已做记录保存在浏览器，域名迁移后旧域名的本地记录不会自动复制过来。

## 访问

GitHub Pages 的中国大陆访问稳定性需使用国内网络实测。
