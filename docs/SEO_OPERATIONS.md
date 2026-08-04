# SEO 操作指南

本指南记录长期有效的 SEO 配置和搜索平台操作。最近一次审计数据见 [SEO_REPORT.md](../SEO_REPORT.md)。

## 1. 正式 URL 与 canonical

正式基础地址：

```text
https://uu9988.github.io/freelancer-calculator/
```

- 首页 canonical 指向基础地址本身。
- 其他可索引页面 canonical 指向各自唯一的正式绝对 URL。
- 正式博客入口是 `/freelancer-calculator/blog/`。
- `blog.html` 仅为兼容入口，保持 `noindex,follow`，canonical 指向正式博客入口。
- 不创建 `/blog/blog/`，不让内部链接跳出 `/freelancer-calculator/`。

绑定独立域名时，必须重新评估全部 canonical、Open Graph URL、基础路径、sitemap 和 robots，不能只替换域名。

## 2. robots 与特殊页面

`robots.txt` 允许正常抓取，并声明正式 sitemap：

```text
https://uu9988.github.io/freelancer-calculator/sitemap.xml
https://uu9988.github.io/freelancer-calculator/pages-sitemap.xml
https://uu9988.github.io/freelancer-calculator/tools-sitemap.xml
https://uu9988.github.io/freelancer-calculator/blog/sitemap.xml
```

规则：

- `404.html` 保持 `noindex,follow`，不添加 canonical 或应用 schema。
- `blog/post-template.html` 保持 `noindex,nofollow`，不加入 sitemap 或公开内链。
- Google/Bing 验证文件不作为普通页面优化，也不加入 sitemap。
- `rss.xml` 是订阅源，不得作为 `Sitemap:` 指令。

## 3. Sitemap 结构

`sitemap.xml` 是 sitemap index，包含三个真实子 sitemap：

| 文件 | 内容 | 当前 URL 数量 |
|---|---|---:|
| `pages-sitemap.xml` | 首页与基础页面 | 6 |
| `tools-sitemap.xml` | 工具页面 | 22 |
| `blog/sitemap.xml` | 正式博客入口与文章 | 11 |
| **总计** | **可索引 URL** | **39** |

新增、删除或改变索引状态时，应同步对应子 sitemap，并确认：

- URL 使用正式 HTTPS 地址和 `/freelancer-calculator/` 基础路径。
- 不包含 404、兼容入口、模板、测试文件或验证文件。
- XML 可解析，文件中每个 URL 都真实存在且可索引。
- 不为同一 URL 在多个子 sitemap 中重复建项。

## 4. Google Search Console

1. 使用 URL-prefix 属性：`https://uu9988.github.io/freelancer-calculator/`。
2. 通过现有 `google60c46abce2c0ec23.html` 验证；不要编辑或重命名该文件。
3. 通常只需提交主 `sitemap.xml`，它会发现全部子 sitemap。
4. 检查 sitemap 状态、页面索引、抓取错误、结构化数据和 Core Web Vitals。
5. 对少量新页面或重要修复可使用 URL Inspection 请求索引；不要反复批量提交全部 URL。

Search Console 的“已发现”“已抓取”“已索引”不是即时同步。发布后应等待平台处理并记录实际状态，不要把本地审计通过等同于已经收录。

## 5. Bing Webmaster Tools 与 URL Submission

1. 添加同一正式站点并通过 `BingSiteAuth.xml` 验证；不得修改该文件。
2. 提交主 `sitemap.xml`，检查抓取与索引报告。
3. URL Submission 仅用于少量新增或重大更新 URL，不重复提交未变化的大量页面。
4. 提交前先确认页面返回正常、canonical 自引用、存在站内入口且已进入 sitemap。

## 6. IndexNow 当前原则

仓库当前没有 IndexNow 密钥或自动提交流程。除非站点所有者明确决定启用，并能安全管理有效密钥、公开 key 文件和提交逻辑，否则不要添加占位代码、伪密钥或无效 API 调用。

若未来启用，应作为独立变更：使用官方规范、限制为真实新增或更新 URL、记录提交失败并避免重复轰炸接口。启用后仍保留 sitemap；IndexNow 不能替代 sitemap 和内部链接。

## 7. 结构化数据与元数据

- Schema 必须与页面类型和可见内容一致。
- FAQPage 仅在页面真实显示完全一致的问题与答案时使用。
- 不添加虚假 `Person`、`Organization`、`AggregateRating`、Review 或评分。
- 没有真实可访问的分享图片时，不添加 `og:image` 或 `twitter:image`；无图片时使用 `twitter:card=summary`。
- 基础信息和政策页面不使用 `WebApplication`。
- 404、模板和兼容入口遵守各自 noindex 规则。

## 8. SEO 修改后的检查流程

本地先运行：

```powershell
python audit_site.py
git diff --check
git status --short
git diff --stat
```

再检查：

1. 修改页面的 title、description、canonical、Open Graph、Twitter 和 H1 是否唯一且自然。
2. JSON-LD 是否可解析，并与可见内容一致。
3. 内部链接和资源是否在 GitHub Pages 子路径下正确解析。
4. 对应 sitemap 是否只包含真实、可索引 URL。
5. `/blog/`、代表工具页和嵌套 404 是否正常。
6. 发布后用正式 URL 检查响应和页面源，再由账号持有人观察 Google/Bing 处理结果。

不要因为一次内容更新重复提交全部 URL，也不要用搜索平台提交代替本地审计。
