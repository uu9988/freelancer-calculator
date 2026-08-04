# AI 与开发者协作规则

本文件是修改本仓库时的强制工作约定，适用于 AI 编程工具和开发者。当前状态见 [PROJECT_STATUS.md](PROJECT_STATUS.md)，实现细节见 [开发者指南](docs/DEVELOPER_GUIDE.md)，SEO 规则见 [SEO 操作指南](docs/SEO_OPERATIONS.md)。

## 修改前

先确认工作区，避免覆盖已有改动：

```powershell
git status --short
git diff --stat
```

只处理用户明确要求的范围。工作区不干净时，先辨认现有改动的归属，不要重置或覆盖。

## 禁止事项

- 未经明确要求修改计算公式、输入逻辑、按钮行为或本地状态保存逻辑。
- 一次批量重写所有页面，或用模板内容覆盖已有正文。
- 修改现有公开 URL、文件名或删除公开页面。
- 修改 `google60c46abce2c0ec23.html` 或 `BingSiteAuth.xml`。
- 添加虚假评分、作者、组织、评论、评价或其他无法验证的信息。
- 生成 `/blog/blog/` 或跳出项目基础路径的内部 URL。
- 在 `404.html` 使用会随错误 URL 层级变化的相对资源路径。
- 未经用户明确许可执行 `git push`；同样不要自行提交、发布或创建标签。

## 核心文件职责

- `index.html`：首页、交互式计算器、分享逻辑和首页结构化数据。
- `js/calculator.js`：输入验证、计算公式、结果渲染和 Chart.js 配置。
- `styles.css`：全站布局、响应式样式和图表容器。
- `404.html`：任意嵌套错误地址使用的自定义 404 页面。
- `blog/index.html`：正式博客入口；`blog.html` 仅为兼容入口。
- `audit_site.py`：SEO、内部链接、结构化数据、XML 和 GitHub Pages 路径审计。
- `sitemap.xml` 与子 sitemap：39 个当前可索引 URL 的发现入口。
- `scripts/` 与 `update_site.py`：内容生成或维护辅助工具；执行后必须检查 diff 并审计。

## GitHub Pages 路径规则

正式网站是项目站点，固定基础路径为：

```text
/freelancer-calculator/
```

跨目录内部链接和资源使用项目根绝对路径，例如：

```html
href="/freelancer-calculator/about.html"
href="/freelancer-calculator/blog/"
src="/freelancer-calculator/js/calculator.js"
```

博客文章链接必须是 `/freelancer-calculator/blog/<slug>.html`。`404.html` 的所有内部 `href` 和 `src` 都必须使用项目根绝对路径，并指向真实文件。

未来绑定独立域名时，必须重新评估 `/freelancer-calculator/` 基础路径、内部链接、canonical、Open Graph URL、sitemap 和 robots 配置，不能直接沿用项目子路径假设。

## 分享功能规则

- 桌面端不调用系统分享窗口，直接复制“结果摘要 + 当前页面 URL”。
- 移动端或紧凑触摸设备在支持时优先调用 `navigator.share()`。
- 用户取消分享时静默结束；其他失败自动降级为复制。
- 复制优先使用 Clipboard API，失败时使用隐藏 `textarea` 与 `document.execCommand("copy")`。
- 当前实现位于 `index.html`；不要为修复分享而改动计算公式。

## 图表规则

- Chart.js 保持 `responsive: true`。
- Chart.js 保持 `maintainAspectRatio: false`。
- Canvas 必须位于有限高度、最大宽度受控的响应式容器中。
- 桌面端和移动端都不得由图表引起横向滚动或导航截断。
- 不要用 `body { overflow-x: hidden; }` 掩盖超宽元素。

## 修改后

必须运行：

```powershell
python audit_site.py
git diff --check
git status --short
git diff --stat
```

同时确认只改动授权文件，浏览器无 JavaScript 错误，计算结果未改变，公开链接和资源可加载。涉及页面布局、分享或 404 时，应从项目父目录启动本地服务器并按 [开发者指南](docs/DEVELOPER_GUIDE.md) 做浏览器抽查。
