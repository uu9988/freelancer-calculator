# 待办事项

本文件只记录尚未完成或尚未由外部平台确认的工作。当前代码基线：commit `49786f4`，2026-08-08。

## P0 — 搜索平台与真实数据

- [ ] 由账号持有人检查 Google Search Console URL-prefix 属性、验证状态、`sitemap.xml` 处理、索引覆盖和真实查询。
- [ ] 由账号持有人检查 Bing Webmaster Tools 验证、主 sitemap、索引状态和 URL Submission 结果。
- [ ] 保存可用于决策的查询、展示、点击和页面数据；不要用本地审计结果代替收录状态。

## P1 — 整理重复页面

- [ ] 按 [PROJECT_STATUS.md](PROJECT_STATUS.md) 的重叠组逐页确认单一搜索意图；一次只处理一组。
- [ ] 将 Rate/Pricing、Income 变体、Cost、Business、Salary 等静态 Calculator 页面转为真正的 Guide 定位，同时保留 URL、文件名和 canonical。
- [ ] Tax 与 Income Tax 不开发为通用计算器；先明确不同 Guide 角度和税务免责声明。
- [ ] 修正 `AGENTS.md` 与 `docs/DEVELOPER_GUIDE.md` 中已过时的 native share 描述，统一为 Copy Link-only。

## P2 — Tools 导航

- [ ] 设计一个精简的 Tools 导航入口，明确列出 7 种真实计算器，并把静态页面标为 Guide 或规划内容。
- [ ] 不创建重复工具，不改变现有公开 URL；实施前先检查页面发现路径和 sitemap 影响。

## P3 — 内部链接

- [ ] 让首页、博客和 Guide 优先链接到与当前问题最相关的真实工具。
- [ ] 减少静态 Calculator 页面之间的模板化交叉链接，避免向用户暗示它们已有计算功能。
- [ ] 保持所有跨目录链接兼容 `/freelancer-calculator/`，运行完整路径审计。

## P4 — 单页高质量 Guide

- [ ] 取得真实查询数据后，只选择一个重叠页面改成高质量 Guide；优先从 Rate/Pricing 或 Income 变体组中选择。
- [ ] 改写时说明何时使用现有真实计算器，不复制工具公式、FAQ 或模板正文。

## Calculator 候选池（暂不开发）

- **Payment：** 只有实现定金、里程碑、付款计划和余额时间表时才值得开发。
- **Budget：** 只有明确区分业务费用、收入、储备和现金流时才值得开发。
- **Revenue：** 只有提供合同收入与不确定管道的情景预测时才值得开发。
- **Tax / Income Tax：** 不开发通用工具，避免所在地规则和税务建议风险。

## Completed（摘要）

- 8 个功能入口、7 种独立计算器已经完成：Hourly Rate、Income、Quote、Project Cost、Profit、Invoice、Expense。
- Copy Link-only、GitHub Pages 子路径、嵌套 404、39 个可索引 URL 和技术审计已完成。
- Lighthouse 技术性能阶段已完成；不再保留重复性能待办。

正式完成历史见 [CHANGELOG.md](CHANGELOG.md)。
