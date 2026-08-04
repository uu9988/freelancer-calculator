# Changelog

## Phase 1 - 2026-07-18
- Created the initial static homepage structure for the Freelancer Calculator Hub
- Added the first tool page layout, FAQ, privacy page, and responsive styling
- Prepared the project for future calculator logic and SEO enhancements

## Phase 2 - 2026-07-18
- Added the calculator logic in a separate JavaScript file
- Implemented the required input fields, calculation formulas, result rendering, and basic validation
- Added a simple income composition chart using Chart.js

## Phase 3 - 2026-08-02
- Added project documentation files: PROJECT_STATUS.md, TODO.md, MAINTENANCE.md
- Updated project structure documentation and future maintenance guidance
- Confirmed no HTML/JS logic changes during documentation updates

## Phase 4 - 2026-08-03
- Batch optimized all freelance tool pages with standardized SEO sections, FAQPage schema, OG/Twitter metadata, canonical links, and related tool links
- Added responsive mobile improvements for buttons, inputs, tables, and navigation
- Updated keyword map to include the payment calculator page
- Ran site audit to verify SEO consistency across updated pages

## Phase 5 - 2026-08-03
- Completed a full SEO audit across all public HTML pages, internal links, local assets, Schema, sitemaps, and robots directives
- Optimized the homepage title, description, social metadata, introductory copy, WebSite schema, WebApplication schema, and visible FAQ mapping
- Reclassified non-interactive tool landing pages from WebApplication to WebPage and preserved WebApplication only on the interactive homepage
- Replaced generic tool-page planning sections with topic-specific methods, formulas, examples, related tools, and related article links
- Reworked ten template-heavy blog articles with distinct topic-specific introductions, problems, solutions, examples, and next steps
- Removed unverified Person and Organization data from Article schema and aligned every FAQPage block with visible page content
- Consolidated the duplicate blog entry by keeping `/blog/` indexable and retaining `blog.html` as a noindex compatibility page
- Fixed broken blog article links, footer links, favicon paths, and inconsistent Blog/Changelog navigation
- Set `404.html` and the blog template to noindex and removed inappropriate structured data
- Removed invalid Google Analytics and AdSense placeholder scripts without changing calculator logic
- Removed RSS from robots Sitemap directives and verified the sitemap index plus 6 page, 22 tool, and 11 blog URLs
- Rebuilt `audit_site.py` and added the idempotent `scripts/seo_repair.py` maintenance workflow
- Final local audit result: 39 indexable URLs, 0 errors, 0 warnings

## Phase 6 - 2026-08-03
- Converted internal HTML links and local asset references to the GitHub Pages project-root path `/freelancer-calculator/`
- Fixed blog navigation and article links that could duplicate the blog directory segment
- Made every 404 page link, stylesheet, and favicon path safe when GitHub Pages renders the page for a nested missing URL
- Updated blog generation and maintenance scripts so regenerated pages retain project-root paths
- Expanded `audit_site.py` to simulate browser URL resolution and reject project-path escapes, duplicated blog paths, relative 404 references, and missing local assets
- Verified the project with the parent-directory local server, browser navigation tests, and a final 0-error/0-warning audit
