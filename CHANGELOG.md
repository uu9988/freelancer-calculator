# 变更记录

本文件按仓库真实提交历史记录已经完成的正式修改，不使用额外版本号。

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
