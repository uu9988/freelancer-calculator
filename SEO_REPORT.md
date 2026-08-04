# 最近 SEO 审计报告

> **生成日期：** 2026-08-05<br>
> **对应 commit：** `2728f64`<br>
> **正式地址：** <https://uu9988.github.io/freelancer-calculator/><br>
> **结论：** PASS / 技术性能阶段完成

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

## Lighthouse 与真实浏览器验证

- 首页、小时费率计算器和收入计算器均已多次运行 Lighthouse。
- Performance、Accessibility、Best Practices 和 SEO 多次测试基本达到或接近 100；本报告不虚构或固化具体分数。
- 人工浏览器测试未发现明显横向溢出、图表异常、失败的分享弹窗或 JavaScript 错误。
- 技术性能检查阶段已完成，后续工作转向收录观察、核心页面用户价值和真实数据。

## 仍需外部确认

本地审计和 Lighthouse 实验室测试不能代替搜索平台与真实用户数据。下一阶段需要观察 Google/Bing 收录，优化一个核心计算器页面的用户价值，并获取真实搜索查询和访问数据。
