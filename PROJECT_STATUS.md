# 项目状态

> **Status：** Production / 真实工具阶段完成，进入收录观察与页面整合阶段<br>
> **Live URL：** <https://uu9988.github.io/freelancer-calculator/><br>
> **Branch：** `master`（与 `origin/master` 同步）<br>
> **Commit：** `49786f4`<br>
> **Pages：** 43 个 HTML 文件；39 个可索引 URL<br>
> **Calculators：** 8 个功能入口；7 种独立计算器；13 个静态 calculator 页面<br>
> **Audit：** 0 Errors · 0 Warnings · 0 broken links · 0 path errors<br>
> **Known issues：** 等待 Google/Bing 与真实查询数据；静态 calculator 页面存在搜索意图重叠<br>
> **Next action：** 先检查 Search Console/Bing 数据，再整合重复页面；暂不新增计算器

**状态日期：2026-08-08**

## 下次会话快速入口

开始任何工作前按顺序阅读：

1. [AGENTS.md](AGENTS.md) — 强制修改边界。
2. 本文件 — 当前真实状态、页面分类和权威产品规则。
3. [TODO.md](TODO.md) — 下一阶段 P0–P4。
4. [开发者指南](docs/DEVELOPER_GUIDE.md) 与 [SEO 操作指南](docs/SEO_OPERATIONS.md)。
5. 涉及历史时再读 [CHANGELOG.md](CHANGELOG.md)。

不要从文件名推断页面功能；必须检查表单、结果区域和实际加载的 JavaScript。

## 当前范围与技术状态

- 正式网站：<https://uu9988.github.io/freelancer-calculator/>
- GitHub：<https://github.com/uu9988/freelancer-calculator>
- GitHub Pages 基础路径：`/freelancer-calculator/`
- HTML：43 个；Google 验证页不进入普通审计，审计扫描 42 个。
- Sitemap：6 个基础页面、22 个工具/指南页面、11 个博客页面，共 39 个可索引 URL。
- 技术 SEO、GitHub Pages 子路径、嵌套 404、JSON-LD、XML 与内部链接审计已通过。
- 首页、小时费率页和收入页的 Lighthouse 多次测试基本达到或接近 100；技术性能阶段已完成。

## 当前权威产品规则

### Copy Link

- 所有设备只使用 `Copy Link`；不调用 `navigator.share()`，不打开系统分享面板。
- `js/share-page.js` 只复制页面 canonical URL，不复制输入或计算结果。
- Clipboard API 失败时使用临时 textarea，再失败时显示可选择的手动复制框。
- `AGENTS.md` 和 `docs/DEVELOPER_GUIDE.md` 中仍有旧 native share 描述；在后续文档维护中应修正。在此之前，以本节和当前代码为准。

### GitHub Pages 路径

- 跨目录内部链接和资源固定使用 `/freelancer-calculator/...`。
- `404.html` 的内部 `href`/`src` 必须使用项目根绝对路径并指向真实文件。
- 不允许 `/blog/blog/`；正式博客入口是 `/freelancer-calculator/blog/`。
- 未来绑定独立域名时，必须重新评估基础路径、canonical、Open Graph、sitemap、robots 和审计逻辑。

## 真实计算器清单

“Functional”表示页面有真实输入、提交/计算行为、结果区域和实际存在的 JavaScript。

| 功能入口 | 状态 | JavaScript | 关系 |
|---|---|---|---|
| `index.html` | Functional | `js/calculator.js` | 首页小时费率入口；与独立 Hourly Rate 页面共享引擎，功能重叠但承担首页入口职责 |
| `freelance-hourly-rate-calculator.html` | Functional | `js/calculator.js` | 小时费率主工具页；与首页共享引擎 |
| `freelance-income-calculator.html` | Functional | `js/income-calculator.js` | 收入、费用和简化税务储备规划 |
| `freelance-quote-calculator.html` | Functional | `js/quote-calculator.js` | 客户报价估算 |
| `freelance-project-cost-calculator.html` | Functional | `js/project-cost-calculator.js` | 单个项目内部交付成本 |
| `freelance-profit-calculator.html` | Functional | `js/profit-calculator.js` | 项目收入与成本的利润比较 |
| `freelance-invoice-calculator.html` | Functional | `js/invoice-calculator.js` | 发票金额与剩余应付款 |
| `freelance-expense-calculator.html` | Functional | `js/expense-calculator.js` | 月度/年度业务运营费用 |

因此当前是 **8 个可用功能入口、7 种独立计算器**。没有发现 Partial 交互式计算器。

## 剩余 13 个静态 calculator 页面

这些页面没有表单、输入、结果区或计算 JavaScript。保留现有 URL；本阶段不改 canonical、sitemap、redirect 或文件名。

| 页面 | 当前状态 | 主要重叠 | 建议 |
|---|---|---|---|
| `freelance-budget-calculator.html` | Static | Income / Expense / Profit | **KEEP FOR LATER**：只有能提供独特现金流/预算行为且有查询数据时才开发 |
| `freelance-business-calculator.html` | Static | Profit / Budget / Revenue / Expense | **CONVERT TO GUIDE**：定位为自由职业业务财务规划指南 |
| `freelance-cost-calculator.html` | Static | Project Cost / Expense | **CONVERT TO GUIDE**：解释项目成本与运营费用的区别 |
| `freelance-hourly-income-calculator.html` | Static | Income / Hourly Rate | **CONVERT TO GUIDE**：作为小时收入计算方法说明，不再做同类工具 |
| `freelance-income-tax-calculator.html` | Static | Tax | **DO NOT DEVELOP** 通用税务工具；改为有明确免责声明的 Guide |
| `freelance-monthly-income-calculator.html` | Static | Income / Revenue | **CONVERT TO GUIDE**：月度收入与现金流规划 |
| `freelance-payment-calculator.html` | Static | Invoice / Quote | **KEEP FOR LATER**：若做成里程碑、定金和付款计划工具，可形成独特价值 |
| `freelance-pricing-calculator.html` | Static | Hourly Rate / Quote / Project Cost | **CONVERT TO GUIDE**：定价方法与何时使用各现有工具 |
| `freelance-rate-calculator.html` | Static | Hourly Rate / Pricing | **CONVERT TO GUIDE**：费率策略和计价方式比较 |
| `freelance-revenue-calculator.html` | Static | Income / Monthly / Yearly Income | **KEEP FOR LATER**：仅在能提供情景预测且有查询需求时开发 |
| `freelance-salary-calculator.html` | Static | Income / Hourly Rate | **CONVERT TO GUIDE**：雇员薪资与自由职业收入的可比性说明 |
| `freelance-tax-calculator.html` | Static | Income Tax | **DO NOT DEVELOP** 通用税务工具；改为税务规划 Guide |
| `freelance-yearly-income-calculator.html` | Static | Income / Revenue | **CONVERT TO GUIDE**：年度收入规划方法 |

## 搜索意图重叠与主页面

| 重叠组 | 主工具 | 处理原则 |
|---|---|---|
| Hourly Rate / Rate / Pricing | Hourly Rate、Quote、Project Cost | 保留真实工具；Rate/Pricing 转为不同用途的 Guide，不再复制计算功能 |
| Income / Hourly / Monthly / Yearly / Revenue / Salary | Income | Income 保持主工具；Hourly/Monthly/Yearly/Salary 转 Guide；Revenue 只在数据支持下考虑预测工具 |
| Project Cost / Cost / Expense | Project Cost、Expense | 两个真实工具分别覆盖单项目成本和全年运营费用；Cost 转为概念 Guide |
| Quote / Pricing | Quote | Quote 保持工具；Pricing 解释定价方法与工具选择 |
| Tax / Income Tax | 无真实税务工具 | 两页都不开发通用税务计算器；用不同 Guide 角度降低风险和重复 |
| Profit / Business / Budget | Profit | Profit 保持工具；Business 转 Guide；Budget 仅在功能边界明确后保留开发候选 |
| Invoice / Payment | Invoice | Invoice 保持工具；Payment 可作为未来付款计划工具候选 |

## 当前已知问题

- Google Search Console 与 Bing Webmaster Tools 的收录、索引和 sitemap 处理状态需要账号持有人确认。
- 尚无足够真实搜索查询和访问数据来决定哪些静态页面值得重点优化。
- 13 个静态页面使用 Calculator 名称但没有计算功能；在保留 URL 的前提下，需要逐组改为明确 Guide 或暂缓开发。
- `AGENTS.md` 与 `docs/DEVELOPER_GUIDE.md` 的分享章节仍描述旧 native share 行为，与当前 Copy Link-only 实现不一致。
- 项目没有独立域名；未来域名变更需要独立路径迁移检查。

## 下一阶段顺序

1. **P0 — F：** 检查 Google Search Console / Bing 的收录、sitemap 和真实查询数据。
2. **P1 — B：** 按上述重叠组确定每个 URL 的单一意图，逐页转 Guide 或暂缓，不删除 URL。
3. **P2 — C：** 建立清楚区分“真实工具”和“指南”的 Tools 导航入口。
4. **P3 — D：** 优化首页、工具、Guide 和博客之间的内部链接，让真实工具成为主要行动入口。
5. **P4 — E：** 根据真实数据只优化一个高价值 Guide；暂不继续开发 Calculator。

未来若数据证明需求明确，Calculator 候选优先顺序为 Payment、Budget、Revenue；Tax/Income Tax 不作为通用工具开发。
