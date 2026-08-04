# TODO

Last reviewed: 2026-08-03

## Completed in the current SEO pass

- [x] Optimize the homepage title, description, canonical, Open Graph, Twitter Card, H1 and introductory copy
- [x] Add valid homepage WebSite and WebApplication Schema
- [x] Match all FAQPage Schema questions and answers to visible FAQ content
- [x] Give all 39 indexable pages unique titles, descriptions and canonical URLs
- [x] Correct Schema types for tools, articles, policy pages, About, Contact and Changelog
- [x] Remove unverified Person, Organization, review and rating data
- [x] Fix broken internal links, favicon paths and Blog navigation
- [x] Use `/freelancer-calculator/` project-root paths for all internal HTML and local asset references
- [x] Simulate nested GitHub Pages 404 URL resolution in the site audit
- [x] Add topic-relevant links between calculator pages and blog articles
- [x] Remove duplicate blog indexing signals while preserving the existing `blog.html` URL
- [x] Exclude 404, verification files, the blog alias and the post template from sitemaps
- [x] Remove the RSS Feed from robots Sitemap directives
- [x] Validate sitemap XML, RSS XML and all JSON-LD blocks
- [x] Repair and expand `audit_site.py`
- [x] Add an idempotent SEO repair workflow in `scripts/seo_repair.py`
- [x] Confirm `js/calculator.js` and Google/Bing verification files remain unchanged

## Deployment and search console

- [ ] Deploy the current workspace changes to GitHub Pages
- [ ] Verify live HTTP status codes for the homepage, representative pages, `/blog/`, `blog.html` and `404.html`
- [ ] Submit `https://uu9988.github.io/freelancer-calculator/sitemap.xml` to Google Search Console
- [ ] Submit the same sitemap to Bing Webmaster Tools
- [ ] Monitor coverage, duplicate canonical and structured-data reports after recrawling

## Manual quality checks

- [ ] Test the calculator with representative inputs in desktop and mobile browsers
- [ ] Run Lighthouse or PageSpeed Insights after deployment and review Core Web Vitals
- [ ] Visually inspect the five representative pages listed in `SEO_REPORT.md`
- [ ] Confirm the contact email remains active and monitored
- [ ] Recheck privacy disclosures before enabling any future analytics or advertising service

## Optional future improvements

- [ ] Create a real social sharing image before adding `og:image` or `twitter:image`
- [ ] Group the long homepage tool list into clearer categories without changing existing URLs
- [ ] Add additional calculators only when they provide real interactive behavior or clearly labeled planning guidance
- [ ] Review keyword performance and refresh article content based on Search Console query data
