from pathlib import Path
import re
import json
import subprocess
import sys

BASE_URL = 'https://uu9988.github.io/freelancer-calculator/'
PROJECT_PATH = '/freelancer-calculator/'

PAGE_LINKS = [
    ('Budget Calculator', 'freelance-budget-calculator.html'),
    ('Business Calculator', 'freelance-business-calculator.html'),
    ('Cost Calculator', 'freelance-cost-calculator.html'),
    ('Expense Calculator', 'freelance-expense-calculator.html'),
    ('Hourly Income Calculator', 'freelance-hourly-income-calculator.html'),
]

DESCRIPTION_TEMPLATES = [
    ('hourly rate', 'Use this {keyword} to estimate your sustainable hourly rate based on income goals, expenses, and billable hours.'),
    ('income tax', 'Use this {keyword} to estimate tax burden, quarterly payments, and realistic self-employment tax planning.'),
    ('invoice', 'Use this {keyword} to estimate invoice totals, client billing amounts, and project fee decisions.'),
    ('pricing', 'Use this {keyword} to estimate sustainable service rates and freelance pricing strategy.'),
    ('project cost', 'Use this {keyword} to estimate freelance project expenses before you quote work to a client.'),
    ('salary', 'Use this {keyword} to estimate annual freelance income, salary-equivalent goals, and earnings planning.'),
    ('revenue', 'Use this {keyword} to estimate freelance revenue potential, business income targets, and growth planning.'),
    ('rate calculator', 'Use this {keyword} to estimate a sustainable hourly or project rate based on your desired income and expenses.'),
    ('income calculator', 'Use this {keyword} to estimate annual and monthly freelance earnings with practical assumptions.'),
    ('cost calculator', 'Use this {keyword} to estimate your business costs, overhead, and expense planning.'),
    ('tax calculator', 'Use this {keyword} to estimate freelance taxes, deductions, and how much to set aside for payments.'),
    ('quote calculator', 'Use this {keyword} to estimate quote amounts and pricing for freelance proposals.'),
]

FAQ_TEMPLATES = [
    ('How does this calculator help freelancers?', 'It helps freelancers estimate pricing, revenue, taxes, and costs so they can make more confident business decisions.'),
    ('Is this tool free to use?', 'Yes. All tools on Freelancer Calculator Hub are free and provided for informational purposes.'),
    ('What should I include when planning with this tool?', 'Include your target income, business expenses, taxes, and realistic billable hours to get a useful estimate.'),
]


def parse_keyword_map(path: Path):
    data = {}
    current = None
    with path.open(encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('## '):
                title = line[3:].strip()
                current = {'display_name': title, 'main_keyword': '', 'long_tail': [], 'file': ''}
                data[title] = current
            elif current is None:
                continue
            elif line.startswith('- Page:'):
                current['file'] = line.split('`')[1]
            elif line.startswith('- Main keyword:'):
                current['main_keyword'] = line.split(':', 1)[1].strip()
            elif line.startswith('  - '):
                current['long_tail'].append(line[4:].strip())
    return {entry['file']: entry for entry in data.values() if entry.get('file')}


def title_case(text: str):
    return text[0].upper() + text[1:] if text else text


def build_description(main_keyword: str):
    key = main_keyword.lower()
    for matcher, template in DESCRIPTION_TEMPLATES:
        if matcher in key:
            return template.format(keyword=main_keyword)
    return f'Use this {main_keyword} to estimate freelance income, pricing, expenses, and business planning assumptions.'


def build_faq_items(display_name: str, main_keyword: str, long_tail: list):
    items = [dict(question=q, answer=a) for q, a in FAQ_TEMPLATES]
    if long_tail:
        question = f'How do I use this {main_keyword}?' if 'calculator' in main_keyword else f'How do I use this {display_name}?'
        items.append({'question': question, 'answer': f'This tool helps you plan {main_keyword} by using your income, expenses, and business assumptions to produce a practical estimate.'})
        if len(long_tail) >= 1:
            items.append({'question': f'What does it mean to {long_tail[0]}?', 'answer': f'It means using the calculator to compare your goals and assumptions so you can arrive at a clear freelance pricing or income target.'})
    return items[:5]


def build_faq_section(faq_items):
    details = ''.join([
        f'          <details>\n'
        f'            <summary>{item["question"]}</summary>\n'
        f'            <p>{item["answer"]}</p>\n'
        f'          </details>\n' for item in faq_items
    ])
    return f'''      <section class="page-section">
        <div class="container content-card">
          <h2>How it works</h2>
          <p>This section explains how the calculator works and how it helps freelancers estimate their results.</p>
          <h2>Calculation Formula</h2>
          <p>The formula combines your target income, business expenses, and billable time to estimate a sustainable freelance rate or target figure.</p>
          <h2>Example</h2>
          <p>For example, a freelancer targeting $60,000 per year with realistic billable hours can see what rate is required to cover take-home income, taxes, and expenses.</p>
          <h2>FAQ</h2>\n{details}        </div>
      </section>\n'''


def build_faq_schema(faq_items):
    schema = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': item['question'],
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': item['answer'],
                },
            } for item in faq_items
        ]
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)


def replace_or_insert(regex, replacement, text, insert_before=None):
    if re.search(regex, text, flags=re.I|re.S):
        return re.sub(regex, replacement, text, flags=re.I|re.S)
    if insert_before:
        return text.replace(insert_before, replacement + insert_before)
    return text


def normalize_page(filepath: Path, data: dict):
    txt = filepath.read_text(encoding='utf-8')
    main_keyword = data['main_keyword']
    display_name = data['display_name']
    description = build_description(main_keyword)
    canonical_url = BASE_URL + filepath.name
    faq_items = build_faq_items(display_name, main_keyword, data['long_tail'])
    faq_schema_text = build_faq_schema(faq_items)

    # Title
    txt = replace_or_insert(r'<title>.*?</title>', f'<title>{display_name} | Freelancer Calculator Hub</title>', txt)
    # Description
    txt = replace_or_insert(r'<meta[^>]+name=["\"]description["\"][^>]*?>', f'<meta name="description" content="{description}" />', txt)
    # Canonical
    txt = replace_or_insert(r'<link[^>]+rel=["\"]canonical["\"][^>]*?>', f'<link rel="canonical" href="{canonical_url}" />', txt)
    # Favicon
    if not re.search(r'<link[^>]+rel=["\"]icon["\"]', txt, re.I):
        head_close = '</head>'
        txt = txt.replace(head_close, f'    <link rel="icon" href="{PROJECT_PATH}favicon.svg" type="image/svg+xml" />\n' + head_close)
    # OG and Twitter
    og_tags = f'''    <meta property="og:title" content="{display_name} | Freelancer Calculator Hub" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{canonical_url}" />
    <meta property="og:site_name" content="Freelancer Calculator Hub" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{display_name} | Freelancer Calculator Hub" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:site" content="@FreelancerCalcHub" />'''
    if re.search(r'<meta[^>]+property=["\"]og:title["\"]', txt, re.I):
        txt = re.sub(r'<meta[^>]+property=["\"]og:title["\"][^>]*?>', f'<meta property="og:title" content="{display_name} | Freelancer Calculator Hub" />', txt, flags=re.I)
        txt = re.sub(r'<meta[^>]+property=["\"]og:description["\"][^>]*?>', f'<meta property="og:description" content="{description}" />', txt, flags=re.I)
        txt = re.sub(r'<meta[^>]+property=["\"]og:url["\"][^>]*?>', f'<meta property="og:url" content="{canonical_url}" />', txt, flags=re.I)
        txt = re.sub(r'<meta[^>]+name=["\"]twitter:title["\"][^>]*?>', f'<meta name="twitter:title" content="{display_name} | Freelancer Calculator Hub" />', txt, flags=re.I)
        txt = re.sub(r'<meta[^>]+name=["\"]twitter:description["\"][^>]*?>', f'<meta name="twitter:description" content="{description}" />', txt, flags=re.I)
    else:
        head_end = '</head>'
        txt = txt.replace(head_end, og_tags + '\n' + head_end)
    # Breadcrumb
    breadcrumb = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE_URL},
            {'@type': 'ListItem', 'position': 2, 'name': f'{display_name} | Freelancer Calculator Hub', 'item': canonical_url},
        ]
    }
    breadcrumb_text = json.dumps(breadcrumb, indent=2, ensure_ascii=False)
    if re.search(r'"@type"\s*:\s*"BreadcrumbList"', txt):
        txt = re.sub(r'<script type=["\"]application/ld\+json["\"][^>]*>.*?BreadcrumbList.*?</script>', f'<script type="application/ld+json">\n{breadcrumb_text}\n    </script>', txt, flags=re.I|re.S)
    else:
        head_end = '</head>'
        txt = txt.replace(head_end, f'    <script type="application/ld+json">\n{breadcrumb_text}\n    </script>\n' + head_end)

    # FAQ schema
    faq_schema_block = f'    <script type="application/ld+json">\n{faq_schema_text}\n    </script>\n'
    if re.search(r'"@type"\s*:\s*"FAQPage"', txt):
        txt = re.sub(r'<script type=["\"]application/ld\+json["\"][^>]*>.*?FAQPage.*?</script>', faq_schema_block, txt, flags=re.I|re.S)
    else:
        insert_point = txt.rfind('</head>')
        txt = txt[:insert_point] + faq_schema_block + txt[insert_point:]

    # H1
    if re.search(r'<h1>.*?</h1>', txt, re.I|re.S):
        txt = re.sub(r'<h1>.*?</h1>', f'<h1>{display_name}</h1>', txt, flags=re.I|re.S)
    else:
        main_start = re.search(r'<main>', txt, re.I)
        if main_start:
            pos = main_start.end()
            txt = txt[:pos] + f'\n      <section class="page-section">\n        <div class="container content-card">\n          <h1>{display_name}</h1>\n        </div>\n      </section>\n' + txt[pos:]

    # Standard page section with headings
    if not re.search(r'<h2>How it works</h2>', txt, re.I) or not re.search(r'<h2>Calculation Formula</h2>', txt, re.I) or not re.search(r'<h2>Example</h2>', txt, re.I) or not re.search(r'<h2>FAQ</h2>', txt, re.I):
        section = build_faq_section(faq_items)
        if '<section class="related-tools">' in txt:
            txt = txt.replace('<section class="related-tools">', section + '    <section class="related-tools">')
        elif '</main>' in txt:
            txt = txt.replace('</main>', section + '</main>')

    # Ensure related tools section has 5 items
    if '<section class="related-tools">' not in txt:
        rel_html = '    <section class="related-tools">\n      <div class="container content-card">\n        <h2>Related tools</h2>\n        <p>Browse other freelance calculator pages that help with pricing, income planning, and business costs.</p>\n        <ul class="related-list">\n'
        for name, link in PAGE_LINKS:
            rel_html += f'          <li><a href="{PROJECT_PATH}{link}">{name}</a></li>\n'
        rel_html += '        </ul>\n      </div>\n    </section>\n'
        if '</main>' in txt:
            txt = txt.replace('</main>', rel_html + '</main>')
    else:
        existing = re.findall(r'<li><a href="([^"]+)">([^<]+)</a></li>', txt)
        if len(existing) < 5:
            new_list = '\n'.join([f'            <li><a href="{PROJECT_PATH}{link}">{name}</a></li>' for name, link in PAGE_LINKS])
            txt = re.sub(r'(<section class="related-tools">.*?<ul class="related-list">)(.*?)(</ul>.*?</section>)', lambda m: m.group(1) + '\n' + new_list + '\n' + m.group(3), txt, flags=re.I|re.S)

    filepath.write_text(txt, encoding='utf-8')
    return True


if __name__ == '__main__':
    keyword_map = parse_keyword_map(Path('keyword-map.md'))
    updates = []
    for path in sorted(Path('.').glob('freelance-*.html')):
        name = path.name
        data = keyword_map.get(name)
        if not data:
            print(f'SKIP {name} no keyword-map entry')
            continue
        success = normalize_page(path, data)
        updates.append(name)
        print(f'updated {name}')
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name('seo_repair.py')), '--apply'],
        check=True,
    )
    print(f'updated {len(updates)} pages')
