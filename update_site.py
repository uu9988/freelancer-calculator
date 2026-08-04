import glob
import os
import re
import subprocess
import sys

base_url = "https://uu9988.github.io/freelancer-calculator/"
project_path = "/freelancer-calculator/"

nav_html = f'''    <header class="site-header">
      <div class="container nav">
        <a class="brand" href="{project_path}">Freelancer Calculator Hub</a>
        <nav class="site-nav" aria-label="Main navigation">
          <a href="{project_path}">Home</a>
          <a href="{project_path}#calculator">Calculator</a>
          <a href="{project_path}#tools">Tools</a>
          <a href="{project_path}#faq">FAQ</a>
          <a href="{project_path}about.html">About</a>
        </nav>
      </div>
    </header>'''

footer_html = f'''    <footer class="site-footer">
      <div class="container footer-row">
        <p>© 2026 Freelancer Calculator Hub</p>
        <a href="{project_path}">Home</a>
        <a href="{project_path}#tools">Tools</a>
        <a href="{project_path}about.html">About</a>
        <a href="{project_path}privacy.html">Privacy</a>
        <a href="{project_path}terms.html">Terms</a>
      </div>
    </footer>'''

related_links = {
    'freelance-budget-calculator.html': [
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
        ('Freelance Profit Calculator', 'freelance-profit-calculator.html'),
        ('Freelance Cost Calculator', 'freelance-cost-calculator.html'),
        ('Freelance Project Cost Calculator', 'freelance-project-cost-calculator.html'),
    ],
    'freelance-business-calculator.html': [
        ('Freelance Revenue Calculator', 'freelance-revenue-calculator.html'),
        ('Freelance Cost Calculator', 'freelance-cost-calculator.html'),
        ('Freelance Profit Calculator', 'freelance-profit-calculator.html'),
    ],
    'freelance-cost-calculator.html': [
        ('Freelance Expense Calculator', 'freelance-expense-calculator.html'),
        ('Freelance Project Cost Calculator', 'freelance-project-cost-calculator.html'),
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
    ],
    'freelance-expense-calculator.html': [
        ('Freelance Budget Calculator', 'freelance-budget-calculator.html'),
        ('Freelance Cost Calculator', 'freelance-cost-calculator.html'),
        ('Freelance Profit Calculator', 'freelance-profit-calculator.html'),
    ],
    'freelance-hourly-income-calculator.html': [
        ('Freelance Monthly Income Calculator', 'freelance-monthly-income-calculator.html'),
        ('Freelance Yearly Income Calculator', 'freelance-yearly-income-calculator.html'),
        ('Freelance Hourly Rate Calculator', 'freelance-hourly-rate-calculator.html'),
    ],
    'freelance-hourly-rate-calculator.html': [
        ('Freelance Hourly Rate Guide', 'freelance-hourly-rate-guide.html'),
        ('Freelance Rate Calculator', 'freelance-rate-calculator.html'),
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
    ],
    'freelance-hourly-rate-guide.html': [
        ('Freelance Hourly Rate Calculator', 'freelance-hourly-rate-calculator.html'),
        ('Freelance Rate Calculator', 'freelance-rate-calculator.html'),
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
    ],
    'freelance-income-calculator.html': [
        ('Freelance Monthly Income Calculator', 'freelance-monthly-income-calculator.html'),
        ('Freelance Yearly Income Calculator', 'freelance-yearly-income-calculator.html'),
        ('Freelance Income Tax Calculator', 'freelance-income-tax-calculator.html'),
    ],
    'freelance-income-tax-calculator.html': [
        ('Freelance Tax Calculator', 'freelance-tax-calculator.html'),
        ('Freelance Income Calculator', 'freelance-income-calculator.html'),
        ('Freelance Salary Calculator', 'freelance-salary-calculator.html'),
    ],
    'freelance-invoice-calculator.html': [
        ('Freelance Invoice Generator', 'freelance-invoice-generator.html'),
        ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
        ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
    ],
    'freelance-invoice-generator.html': [
        ('Freelance Invoice Calculator', 'freelance-invoice-calculator.html'),
        ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
        ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
    ],
    'freelance-monthly-income-calculator.html': [
        ('Freelance Yearly Income Calculator', 'freelance-yearly-income-calculator.html'),
        ('Freelance Income Calculator', 'freelance-income-calculator.html'),
        ('Freelance Salary Calculator', 'freelance-salary-calculator.html'),
    ],
    'freelance-payment-calculator.html': [
        ('Freelance Invoice Generator', 'freelance-invoice-generator.html'),
        ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
        ('Freelance Project Cost Calculator', 'freelance-project-cost-calculator.html'),
    ],
    'freelance-pricing-calculator.html': [
        ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
        ('Freelance Rate Calculator', 'freelance-rate-calculator.html'),
        ('Freelance Profit Calculator', 'freelance-profit-calculator.html'),
    ],
    'freelance-profit-calculator.html': [
        ('Freelance Revenue Calculator', 'freelance-revenue-calculator.html'),
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
        ('Freelance Cost Calculator', 'freelance-cost-calculator.html'),
    ],
    'freelance-project-cost-calculator.html': [
        ('Freelance Cost Calculator', 'freelance-cost-calculator.html'),
        ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
        ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
    ],
    'freelance-quote-calculator.html': [
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
        ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
        ('Freelance Invoice Generator', 'freelance-invoice-generator.html'),
    ],
    'freelance-rate-calculator.html': [
        ('Freelance Hourly Rate Calculator', 'freelance-hourly-rate-calculator.html'),
        ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
        ('Freelance Income Calculator', 'freelance-income-calculator.html'),
    ],
    'freelance-revenue-calculator.html': [
        ('Freelance Profit Calculator', 'freelance-profit-calculator.html'),
        ('Freelance Budget Calculator', 'freelance-budget-calculator.html'),
        ('Freelance Income Calculator', 'freelance-income-calculator.html'),
    ],
    'freelance-salary-calculator.html': [
        ('Freelance Income Calculator', 'freelance-income-calculator.html'),
        ('Freelance Yearly Income Calculator', 'freelance-yearly-income-calculator.html'),
        ('Freelance Income Tax Calculator', 'freelance-income-tax-calculator.html'),
    ],
    'freelance-tax-calculator.html': [
        ('Freelance Income Tax Calculator', 'freelance-income-tax-calculator.html'),
        ('Freelance Rate Calculator', 'freelance-rate-calculator.html'),
        ('Freelance Cost Calculator', 'freelance-cost-calculator.html'),
    ],
    'freelance-yearly-income-calculator.html': [
        ('Freelance Monthly Income Calculator', 'freelance-monthly-income-calculator.html'),
        ('Freelance Salary Calculator', 'freelance-salary-calculator.html'),
        ('Freelance Income Calculator', 'freelance-income-calculator.html'),
    ],
}

all_pages = sorted([fn for fn in glob.glob('*.html') if fn != 'google60c46abce2c0ec23.html'])

# helper functions

def slug_to_title(fn):
    if fn == 'index.html':
        return 'Freelance Hourly Rate Calculator - Calculate Your Ideal Rate'
    name = fn.replace('.html', '').replace('freelance-', '').replace('-', ' ').title()
    if 'Calculator' in name or 'Generator' in name or 'Guide' in name:
        return f'Freelance {name}'
    return f'Freelance {name}'


def slug_to_description(fn):
    descriptions = {
        'about.html': 'Learn about Freelancer Calculator Hub, how it helps freelancers estimate rates and plan income goals, and why this toolset exists.',
        'terms.html': 'Review the terms of use for Freelancer Calculator Hub and its calculator tools.',
        'privacy.html': 'Read the privacy policy for Freelancer Calculator Hub and how this freelance calculator site handles data and browser-based calculations.',
        'index.html': 'Free freelance hourly rate calculator to estimate your ideal rate, monthly income goals, and freelance pricing strategy.',
    }
    if fn in descriptions:
        return descriptions[fn]
    label = fn.replace('.html', '').replace('freelance-', '').replace('-', ' ')
    return f'Use this freelance {label} to estimate your {label} and improve your freelance pricing and financial planning.'


def generate_related_section(fn):
    links = related_links.get(fn)
    if not links:
        return ''
    items = '\n'.join([f'              <li><a href="{project_path}{href}">{text}</a></li>' for text, href in links])
    return f'''      <section class="page-section related-section">
        <div class="container content-card">
          <h2>Related Tools</h2>
          <ul class="related-list">
{items}
          </ul>
        </div>
      </section>
'''


def make_meta_tags(title, description, canonical_url):
    return f'''    <meta name="description" content="{description}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{canonical_url}" />
    <meta property="og:site_name" content="Freelancer Calculator Hub" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="robots" content="index,follow" />
    <link rel="canonical" href="{canonical_url}" />
    <link rel="icon" href="{project_path}favicon.svg" type="image/svg+xml" />'''


def normalize_head(head_body, title, description, canonical_url):
    body = re.sub(r'<link[^>]+rel=["\']canonical["\'][^>]*>\s*', '', head_body, flags=re.I)
    body = re.sub(r'<link[^>]+rel=["\']icon["\'][^>]*>\s*', '', body, flags=re.I)
    body = re.sub(r'<meta[^>]+(?:property=["\']og:[^"\']*["\']|name=["\']twitter:[^"\']*["\'])[^>]*>\s*', '', body, flags=re.I)
    body = re.sub(r'<meta[^>]+name=["\']robots["\'][^>]*>\s*', '', body, flags=re.I)
    body = re.sub(r'<meta[^>]+name=["\']description["\'][^>]*>\s*', '', body, flags=re.I)
    body = re.sub(r'<title>.*?</title>\s*', '', body, flags=re.I|re.S)
    if not re.search(r'<meta[^>]+charset=', body, re.I):
        body = '    <meta charset="UTF-8" />\n' + body
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', body, re.I):
        body = re.sub(r'(<meta[^>]+charset=[^>]*>\s*)', r'\1    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n', body, flags=re.I)
    body = f'    <title>{title}</title>\n    <meta name="description" content="{description}" />\n' + body
    body += '\n' + make_meta_tags(title, description, canonical_url) + '\n'
    body = re.sub(r'\n\s*\n', '\n', body)
    return body


def insert_related(text, related_html):
    if related_html and 'Related Tools' not in text:
        if '</main>' in text:
            return text.replace('</main>', related_html + '    </main>', 1)
        if '</body>' in text:
            return text.replace('</body>', related_html + '  </body>', 1)
    return text

changed_files = []
for fn in glob.glob('*.html'):
    if fn == 'google60c46abce2c0ec23.html':
        continue
    path = fn
    content = open(path, encoding='utf-8').read()
    original = content
    title = slug_to_title(fn)
    description = slug_to_description(fn)
    canonical_url = base_url if fn == 'index.html' else base_url + fn

    head_match = re.search(r'(<head[^>]*>)(.*?)(</head>)', content, re.S|re.I)
    if head_match:
        open_tag, body, close_tag = head_match.groups()
        # preserve existing title/desc if present
        title_match = re.search(r'<title>(.*?)</title>', body, re.S|re.I)
        if title_match:
            title = title_match.group(1).strip()
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']', body, re.I)
        if desc_match:
            description = desc_match.group(1).strip()
        if fn == 'index.html':
            title = title or 'Freelance Hourly Rate Calculator - Calculate Your Ideal Rate'
            description = description or 'Free freelance hourly rate calculator to estimate your ideal hourly rate, monthly income goals, and freelance pricing strategy.'
        replacement = normalize_head(body, title, description, canonical_url)
        content = content[:head_match.start(2)] + replacement + content[head_match.end(2):]

    content = re.sub(r'<header.*?</header>', nav_html, content, flags=re.S|re.I)
    content = re.sub(r'<footer.*?</footer>', footer_html, content, flags=re.S|re.I)
    content = re.sub(r'<section class="hero"', '<section id="tools" class="hero"', content, count=1)

    related_html = generate_related_section(fn)
    if related_html:
        content = insert_related(content, related_html)

    if content != original:
        open(path, 'w', encoding='utf-8').write(content)
        changed_files.append(path)

# rewrite sitemap.xml
sitemap_items = ['index.html', 'about.html', 'terms.html', 'privacy.html'] + [fn for fn in sorted(glob.glob('freelance-*.html'))]
urls = []
for fn in sitemap_items:
    url = base_url if fn == 'index.html' else base_url + fn
    urls.append((url, 'weekly' if fn == 'index.html' else 'monthly', '1.0' if fn == 'index.html' else '0.9'))
with open('sitemap.xml', 'w', encoding='utf-8') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fh.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url, cf, pr in urls:
        fh.write('  <url>\n')
        fh.write(f'    <loc>{url}</loc>\n')
        fh.write(f'    <changefreq>{cf}</changefreq>\n')
        fh.write(f'    <priority>{pr}</priority>\n')
        fh.write('  </url>\n')
    fh.write('</urlset>\n')

print('updated', len(changed_files), 'HTML files')
print('\n'.join(changed_files))
subprocess.run([sys.executable, 'scripts/seo_repair.py', '--apply'], check=True)
