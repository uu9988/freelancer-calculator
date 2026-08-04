# 开发者指南

本指南集中说明项目架构、开发、测试、发布与维护。强制修改边界见 [AGENTS.md](../AGENTS.md)，SEO 专项操作见 [SEO_OPERATIONS.md](SEO_OPERATIONS.md)。

## 1. 项目概览

Freelancer Calculator 是无构建步骤的静态网站，部署在 GitHub Pages 项目路径：

```text
https://uu9988.github.io/freelancer-calculator/
```

当前协作分支为 `master`，基础路径为 `/freelancer-calculator/`。网站使用 HTML、CSS、原生 JavaScript、Chart.js CDN 和 Python 维护脚本，不依赖后端或数据库。

## 2. 文件与目录职责

| 路径 | 职责 |
|---|---|
| `index.html` | 首页、交互式小时费率计算器、分享逻辑和首页 schema |
| `freelance-*.html` | 22 个公开工具或专题 URL |
| `about.html`、`contact.html` 等 | 基础信息与政策页面 |
| `styles.css` | 全站样式、响应式布局和图表容器 |
| `js/calculator.js` | 输入验证、计算公式、结果渲染和 Chart.js 配置 |
| `404.html` | 任意嵌套错误地址显示的自定义 404 |
| `blog/index.html` | 正式博客入口 |
| `blog/*.html` | 博客文章；`post-template.html` 是不可索引模板 |
| `blog.html` | 兼容入口，`noindex,follow` 并 canonical 到 `/blog/` |
| `audit_site.py` | SEO、链接、路径、JSON-LD 和 XML 审计 |
| `scripts/` | 内容生成、SEO 修复和批量维护辅助脚本 |
| `update_site.py` | 旧版站点更新辅助入口；运行后必须审查 diff |
| `sitemap.xml` | Sitemap index |
| `pages-sitemap.xml` | 基础页面 URL |
| `tools-sitemap.xml` | 工具页面 URL |
| `blog/sitemap.xml` | 博客页面 URL |
| `rss.xml` | 博客订阅源，不是 sitemap |

验证文件 `google60c46abce2c0ec23.html` 和 `BingSiteAuth.xml` 由搜索平台使用，不得修改。

## 3. 本地开发

不要直接双击 HTML。必须从项目父目录启动服务器，才能复现 GitHub Pages 子路径解析：

```powershell
cd E:\codex\AI-Projects
python -m http.server 8000
```

打开：

```text
http://localhost:8000/freelancer-calculator/
```

常用代表地址：

- `/freelancer-calculator/`
- `/freelancer-calculator/blog/`
- `/freelancer-calculator/about.html`
- `/freelancer-calculator/freelance-income-calculator.html`
- `/freelancer-calculator/test/not-found.html`（故意不存在，用于观察自定义 404）

## 4. 修改工作流

修改前：

```powershell
git status --short
git diff --stat
```

实施最小范围修改，保留现有正文、URL、文件名和计算逻辑。若运行 `scripts/generate_blog_articles.py`、`scripts/batch_optimize_tools.py`、`scripts/seo_repair.py --apply` 或 `update_site.py`，必须先理解其目标，再逐文件检查生成 diff；不要用生成结果覆盖不相关的人工修改。

修改后：

```powershell
python audit_site.py
git diff --check
git status --short
git diff --stat
```

涉及交互或布局时，再做浏览器测试并检查控制台。

## 5. 新增计算器页面

1. 先确认页面提供真实、独特的计算行为或实用内容，不复制现有页面。
2. 使用稳定的小写文件名；发布后不要更名或改变 URL。
3. 编写唯一的 title、description、H1、canonical 和与页面一致的可见说明。
4. 只有真实交互式应用才使用 `WebApplication`；不要为静态指南伪造应用、评分或评价。
5. 所有跨目录链接使用 `/freelancer-calculator/...`。
6. 从首页、相关工具或文章加入可发现的内链，并链接真正相关的页面。
7. 将正式 URL 加入 `tools-sitemap.xml`；如总数变化，同步状态和审计报告。
8. 运行完整审计，并在桌面和移动视口验证交互。

计算公式集中在 `js/calculator.js`。公式、默认值、单位或输入语义的变更必须有明确需求和独立验证，不能夹带在内容或 SEO 修改中。

## 6. 新增博客文章

1. 以现有文章结构为基准，创建 `blog/<slug>.html`；不要直接发布 `blog/post-template.html`。
2. Canonical 与 `og:url` 使用 `/freelancer-calculator/blog/<slug>.html` 的正式绝对 URL。
3. 导航、favicon、样式、工具链接和文章链接使用项目根绝对路径。
4. 使用唯一 title、description、H1 和主题相关正文；不要虚构作者、组织或评论。
5. 只有页面存在完全一致的可见 FAQ 时，才添加 `FAQPage` JSON-LD。
6. 更新 `blog/index.html`、`blog/sitemap.xml` 和 `rss.xml`，并从相关工具页建立合理内链。
7. 运行审计，确认没有 `/blog/blog/`、孤立页面或错误资源。

`scripts/generate_blog_articles.py` 会调用 SEO 修复流程；生成后仍必须人工审查内容和 diff。

## 7. 计算器、Chart.js 与分享

首页加载 Chart.js，并由 `js/calculator.js` 生成结果图表。配置必须保持：

```javascript
responsive: true
maintainAspectRatio: false
```

Canvas 外层使用有限高度、最大宽度受控的响应式容器；当前目标约为桌面 400px、移动端 300px 高。验证 1920×1080、1536×864、1366×768 和 390×844 时没有横向滚动、导航截断或异常放大。

分享逻辑当前位于 `index.html`：

- Windows、macOS、Linux 桌面浏览器直接复制结果摘要和当前 URL。
- 移动端或紧凑触摸设备在支持时调用 `navigator.share()`。
- `AbortError` 静默结束，其他错误降级为复制。
- 复制先用 `navigator.clipboard.writeText()`，再用隐藏 `textarea` 和 `document.execCommand("copy")`。

分享修复不得改变计算结果、输入处理或状态保存。

## 8. GitHub Pages 路径

跨目录内部链接固定使用：

```text
/freelancer-calculator/...
```

不要使用 `../about.html`、`blog/about.html` 或会解析成 `/blog/blog/` 的相对路径。根目录页面的简单相对资源虽然可能工作，但共享模板和 404 应优先使用项目根绝对路径。

`404.html` 会在任意错误层级渲染，因此其中每个内部 `href` 和 `src` 都必须以 `/freelancer-calculator/` 开头并映射到真实本地文件。

未来绑定独立域名时，应把基础路径迁移作为独立变更，系统复查内部链接、资源、canonical、Open Graph、robots、sitemap、审计脚本和本地测试地址。

## 9. 测试清单

发布前至少确认：

- `python audit_site.py` 为 0 Errors、0 Warnings、0 broken links、0 path errors。
- `git diff --check` 无空白错误。
- 首页计算、输入验证、结果内容和图表正常。
- 桌面端分享直接复制，移动端支持时可打开原生分享，失败会降级复制。
- 首页、博客、代表工具页、基础页面和故意不存在的嵌套 URL 正常。
- 404 有样式，且首页、About、博客和计算器链接能离开 404。
- 390px 移动视口与常见桌面视口没有横向滚动。
- 浏览器控制台没有 JavaScript 错误。
- JSON-LD 可解析，sitemap XML 有效，新增页面可被站内发现。
- 验证文件和未授权核心文件没有变化。

## 10. Git、部署与发布后检查

当前协作分支是 `master`。只有用户明确授权时才提交或推送：

```powershell
git add <明确检查过的文件>
git commit -m "清晰描述本次变更"
git push origin master
```

不要默认使用 `git add .`；先检查 `git status --short`。GitHub Pages 会按仓库当前 Pages 配置发布，变更发布源前应先在仓库 Settings 中确认实际配置。

推送后检查：

1. 等待 GitHub Pages 部署完成。
2. 使用正式 URL 强制刷新首页和代表页面。
3. 检查 `/blog/`、一个工具页和嵌套 404。
4. 复测 CSS、favicon、JavaScript、图表和分享。
5. 重要 SEO 变更按 [SEO 操作指南](SEO_OPERATIONS.md) 检查 sitemap 与搜索平台。

## 11. 回滚与日常维护

已发布提交出现问题时，先定位单一提交和受影响文件。经明确授权后优先使用 `git revert <commit>` 保留历史，再审计和推送；不要使用 `git reset --hard` 或覆盖用户工作区。未提交改动只恢复明确目标文件，并先保存或确认其他人的修改。

日常维护建议：

- 每次内容变更都检查内部链接、canonical 和对应 sitemap。
- 定期查看 GitHub Pages 部署、Search Console/Bing 状态和真实用户性能。
- 保持验证文件不变，保持博客正式入口为 `/blog/`。
- 更新当前状态时只改 [PROJECT_STATUS.md](../PROJECT_STATUS.md)，完成记录只进 [CHANGELOG.md](../CHANGELOG.md)，未来工作只进 [TODO.md](../TODO.md)。
