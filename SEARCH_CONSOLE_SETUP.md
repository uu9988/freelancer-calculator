# Search Console Setup

This document explains how to submit the Freelancer Calculator Hub site to Google Search Console and Bing Webmaster Tools.

## 1. Google Search Console

### 1.1 Property setup
1. Go to https://search.google.com/search-console.
2. Sign in with your Google account.
3. Click `Add property`.
4. Choose `URL prefix` and enter the exact site URL:
   - `https://uu9988.github.io/freelancer-calculator/`
5. Verify ownership by one of these methods:
   - HTML file upload (preferred for GitHub Pages) by uploading the provided verification file.
   - HTML tag added to the `<head>` of `index.html`.
   - Google Analytics or Google Tag Manager if already installed.

### 1.2 Submit sitemap
1. After verification, open the property dashboard.
2. Choose `Sitemaps` from the left menu.
3. Enter:
   - `https://uu9988.github.io/freelancer-calculator/sitemap.xml`
4. Click `Submit`.
5. Confirm the status shows `Success` or `Pending`.

### 1.3 Recommended follow-up steps
- Use `URL Inspection` to test the home page and key blog pages.
- Check `Coverage` for indexing issues after sitemap submission.
- Use `Mobile Usability` to identify any responsive display problems.
- Monitor `Enhancements` for structured data warnings or errors.

## 2. Bing Webmaster Tools

### 2.1 Site setup
1. Go to https://www.bing.com/webmasters.
2. Sign in with your Microsoft account.
3. Click `Add site`.
4. Enter the site URL:
   - `https://uu9988.github.io/freelancer-calculator/`
5. Verify ownership using one of the supported methods:
   - XML file authentication by uploading the provided verification file.
   - Add the META tag to the homepage `<head>` section.
   - Add the CNAME record if using a custom domain.

### 2.2 Submit sitemap
1. In Bing Webmaster Tools, navigate to `Sitemaps`.
2. Enter the sitemap index URL:
   - `https://uu9988.github.io/freelancer-calculator/sitemap.xml`
3. Submit the sitemap.
4. Optionally add the direct blog sitemap URL:
   - `https://uu9988.github.io/freelancer-calculator/blog/sitemap.xml`

### 2.3 Recommended follow-up steps
- Use `URL Submission` to request indexing for the homepage and top blog posts.
- Review `Sitemaps` status and resolve any warnings.
- Check `SEO Reports` for mobile or crawl issues.

## 3. Sitemap structure for this site
The site now includes separate sitemap categories to help search engines understand content:
- `https://uu9988.github.io/freelancer-calculator/sitemap.xml` — sitemap index.
- `https://uu9988.github.io/freelancer-calculator/pages-sitemap.xml` — core site pages such as Home, About, Contact, Privacy, Terms, and Changelog.
- `https://uu9988.github.io/freelancer-calculator/tools-sitemap.xml` — all calculator and tool pages.
- `https://uu9988.github.io/freelancer-calculator/blog/sitemap.xml` — blog listing and article pages.
- `https://uu9988.github.io/freelancer-calculator/rss.xml` — RSS feed for the latest blog articles.

## 4. Notes
- Keep the sitemap index updated whenever new pages, tools or blog posts are added.
- Ensure `robots.txt` points to the active sitemap locations.
- Perform periodic checks for indexing and mobile usability in both Search Console and Bing Webmaster.
