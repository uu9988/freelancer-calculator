# Blog Structure Planning

> **Planning reference, not current project status.** As of 2026-08-04 at commit `b646e74`, published articles use flat `blog/<slug>.html` URLs and the official index is `blog/index.html`. Check [PROJECT_STATUS.md](PROJECT_STATUS.md) and [TODO.md](TODO.md) before implementing any item below.

## Existing baseline

- `blog/` contains the official blog index and published posts.
- `blog/post-template.html` is a non-indexable source template, not a public article.
- Tool-to-article internal links support discovery and topic relevance.
- Current content themes include freelance pricing, income planning, tax strategy, budgeting, and business growth.

## Unimplemented concepts

- Year and month archives such as `blog/2026/` and `blog/2026/08/`.
- Tag and category landing pages such as `blog/tags.html` and `blog/category.html`.

These concepts are not approved public URLs. Before implementation, confirm the need from search or navigation data, add the work to [TODO.md](TODO.md), and preserve the `/freelancer-calculator/` base-path rules.
