# Maintenance Guide

## 1. 修改流程

1. 在本地分支创建新分支，例如 `feature/seo-update`。
2. 检查现有页面结构，优先保持 header/footer、导航和内容布局一致。
3. 修改 HTML 时，只进行增量优化，不删除已有计算逻辑或页面内容。
4. 如果补充 SEO 标签，先在单个页面验证，再批量应用于其余页面。

## 2. 测试流程

- 打开要修改的页面，确认浏览器显示正常
- 检查移动端视图：确保按钮、字体与间距无异常
- 验证 header、footer、canonical 和 meta 信息已正确渲染
- 若增加新页面，检查 `sitemap.xml` 是否需要补充

## 3. Git 提交流程

1. 执行 `git status` 查看改动文件
2. 使用 `git add <files>` 添加改动
3. 使用规范提交信息，例如：
   - `feat: add 404 page and favicon support`
   - `fix: normalize SEO metadata across tool pages`
   - `docs: add maintenance guide and project status`
4. 提交时使用 `git commit -m "<type>: <summary>"`
5. 推送到远程分支：`git push origin <branch>`

## 4. 发布流程

1. 确保 `index.html`, `sitemap.xml`, `robots.txt` 和新增页面已经推送到主分支
2. 如果使用 GitHub Pages，确认仓库设置中启用了 `main` 或 `gh-pages` 分支部署
3. 提交后等待静态站点重新部署
4. 检查线上页面是否正常访问

## 5. 回滚方法

- 若更新存在问题，使用 `git log` 查找最近提交
- 使用 `git revert <commit>` 回滚错误提交
- 或者使用 `git checkout -- <file>` 恢复单个文件
- 再次测试页面显示和内部链接是否恢复正常
