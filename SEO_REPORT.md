# 最近 SEO 审计报告

> **生成日期：** 2026-08-04<br>
> **对应 commit：** `b646e74`<br>
> **正式地址：** <https://uu9988.github.io/freelancer-calculator/><br>
> **结论：** PASS

## 审计结果

命令：`python -B audit_site.py`

| 指标 | 结果 |
|---|---:|
| 仓库 HTML 文件 | 43 |
| 审计扫描 HTML | 42 |
| 可索引 sitemap URL | 39 |
| Errors | 0 |
| Warnings | 0 |
| Internal broken links | 0 |
| GitHub Pages path errors | 0 |
| Orphan indexable pages | 0 |
| JSON-LD parse errors | 0 |
| Sitemap/XML parse errors | 0 |

Google 验证页不进入普通 HTML 审计。`404.html`、`blog.html` 和 `blog/post-template.html` 按各自 robots 规则不进入可索引 URL 集合。

## Sitemap 覆盖

| Sitemap | URL 数量 |
|---|---:|
| `pages-sitemap.xml` | 6 |
| `tools-sitemap.xml` | 22 |
| `blog/sitemap.xml` | 11 |
| **总计** | **39** |

`sitemap.xml` 是上述三个子 sitemap 的索引。`rss.xml` 是订阅源，不是 sitemap。

## 当前技术 SEO 状态

- 正式 URL 使用 `https://uu9988.github.io/freelancer-calculator/` 基础地址。
- 正式博客入口是 `/freelancer-calculator/blog/`；兼容页 `blog.html` 为 `noindex,follow` 并 canonical 到正式入口。
- `404.html` 为 `noindex,follow`，不含 canonical；其内部链接和资源使用项目根绝对路径。
- `blog/post-template.html` 为 `noindex,nofollow`，不在 sitemap 和站内公开链接中。
- JSON-LD 全部可解析；当前审计未发现重复或错误路径。
- 内部链接、CSS、JavaScript、favicon 和 sitemap/XML 路径检查通过。

## 仍需外部确认

本地审计不能代替搜索平台和真实用户数据。Google Search Console、Bing Webmaster Tools 的验证与 sitemap 处理状态，以及正式环境 Core Web Vitals，仍需账号持有人在线确认。
