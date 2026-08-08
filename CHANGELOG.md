# 变更记录

本文件按仓库真实提交历史记录已经完成的正式修改，不使用额外版本号。

## 2026-08-08

### `49786f4` — add functional freelance expense calculator

- 将静态 Expense 页面开发为真实的月度与年度业务费用计算器。
- 新增费用、年度总额、运营费用率和每可计费小时费用计算与验证。
- 保留 canonical Copy Link、FAQ schema、GitHub Pages 路径和响应式布局。

## 2026-08-05

### `c71ed23`、`59026a0`、`f59359c`、`9a93342` — add functional planning calculators

- 将 Income、Quote、Project Cost 和 Profit 页面开发为真实交互式计算器。
- 为每个工具增加独立 JavaScript、字段验证、结果区域、示例和与页面一致的 FAQ。

### `5ac9940`、`a014a2d` — add and complete functional invoice calculator

- 将 Invoice 页面开发为真实发票金额与剩余应付款计算器。
- 完成付款、付清和多付款状态，以及输入验证、Copy Link 和响应式结果布局。

### `74aad72`、`f9d444c`、`85cf22e` — simplify sharing and harden calculator interactions

- 移除不可靠的原生系统分享，只保留复制页面 canonical URL 的 Copy Link。
- 增强计算器验证、分享回退和无障碍状态，避免分享与计算状态互相覆盖。

## 2026-08-04

### `b646e74` — fix desktop sharing and responsive chart layout

- 桌面端分享改为复制结果摘要与当前 URL，避免失败的系统分享窗口。
- 保留移动端原生分享，并提供复制降级。
- 为 Chart.js 设置受控的响应式容器和尺寸，消除图表导致的横向溢出。

### `d65c6ef` — fix share fallback and hourly calculator link

- 修正自定义 404 页的小时费率计算器链接。
- 为分享操作增加 Clipboard API 与兼容复制降级。
- 增强审计脚本对 404 链接真实目标的检查。

### `7028e65` — fix technical SEO and GitHub Pages paths

- 统一 GitHub Pages 项目基础路径下的内部链接和资源路径。
- 修复博客导航、嵌套 404、canonical、社交元数据、结构化数据与 sitemap。
- 扩展审计脚本，检查内部链接、孤立页面、JSON-LD、XML 和项目路径错误。
- 更新工具页、博客页及维护脚本，使重新生成内容时保留正确路径与 SEO 规则。

## 2026-08-02

### `ef13e84` — add bing verification file

- 添加 Bing Webmaster Tools 验证文件 `BingSiteAuth.xml`。

### `31a7e68` — initial release

- 建立静态 Freelancer Calculator 网站、首页计算器、工具页面和博客内容。
- 加入站点样式、客户端计算脚本、站点地图、robots、RSS 和基础维护脚本。
- 配置 GitHub Pages 项目站点所需的公开文件。
