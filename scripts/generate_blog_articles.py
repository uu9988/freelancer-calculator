from pathlib import Path
import json
import subprocess
import sys

BASE_URL = 'https://uu9988.github.io/freelancer-calculator/'
PROJECT_PATH = '/freelancer-calculator/'
BLOG_DIR = Path('blog')
BLOG_DIR.mkdir(exist_ok=True)

posts = [
    {
        'slug': 'freelance-calculator-guide',
        'title': 'Freelance Calculator Guide: How to Estimate Income, Rates, Taxes, and Invoices',
        'description': 'A practical guide to using freelance calculator tools for income, hourly rate, tax, and invoice planning.',
        'topic': 'freelance calculator',
        'links': [
            ('Freelance Hourly Rate Calculator', 'freelance-hourly-rate-calculator.html'),
            ('Freelance Income Calculator', 'freelance-income-calculator.html'),
            ('Freelance Invoice Calculator', 'freelance-invoice-calculator.html'),
        ],
        'faq': [
            ('What is the best way to use a freelance calculator?', 'Start with your income goals, add business costs, and compare the output to your available billable hours.'),
            ('Do freelance calculators replace professional advice?', 'No. They are planning tools that help you estimate figures, but professional advice is useful for complex tax and legal decisions.'),
            ('How often should I update my calculator assumptions?', 'Review your assumptions whenever your rates, workload, expenses, or tax situation changes.'),
        ],
    },
    {
        'slug': 'freelance-income-planning',
        'title': 'Freelance Income Planning: Build Reliable Earnings with Calculator Insights',
        'description': 'Learn how freelance income planning helps you build reliable earnings and stay profitable with calculator-backed scenarios.',
        'topic': 'freelance income',
        'links': [
            ('Freelance Income Calculator', 'freelance-income-calculator.html'),
            ('Freelance Monthly Income Calculator', 'freelance-monthly-income-calculator.html'),
            ('Freelance Yearly Income Calculator', 'freelance-yearly-income-calculator.html'),
        ],
        'faq': [
            ('Why should freelancers plan income annually?', 'Annual planning helps you set realistic goals, save for taxes, and manage irregular cash flow.'),
            ('Can income planning improve my pricing?', 'Yes. When you know your income target, you can price your services to meet that goal consistently.'),
            ('What if my income goal changes mid-year?', 'Update your plan and recalculate based on new assumptions to stay on track and adjust as needed.'),
        ],
    },
    {
        'slug': 'hourly-rate-strategy',
        'title': 'Hourly Rate Strategy for Freelancers: Set a Sustainable Freelance Rate',
        'description': 'A strategy guide for freelancers on setting sustainable hourly rates with clear planning and calculator support.',
        'topic': 'hourly rate',
        'links': [
            ('Freelance Hourly Rate Calculator', 'freelance-hourly-rate-calculator.html'),
            ('Freelance Rate Calculator', 'freelance-rate-calculator.html'),
            ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
        ],
        'faq': [
            ('How do I choose an hourly rate as a freelancer?', 'Start by estimating your income needs, business expenses, and the realistic hours you can bill each week.'),
            ('Should I adjust my rate based on clients?', 'Yes. You can offer different rates for different client types while keeping your baseline sustainable rate in mind.'),
            ('What if my hours differ week to week?', 'Use the calculator to model multiple scenarios and choose a rate that works for average billable time.'),
        ],
    },
    {
        'slug': 'freelancer-tax-basics',
        'title': 'Freelancer Tax Basics: Estimate and Plan Your Self-Employment Obligations',
        'description': 'Understand the basics of freelancer taxes and how calculators can help you estimate self-employment obligations.' ,
        'topic': 'freelancer tax',
        'links': [
            ('Freelance Income Tax Calculator', 'freelance-income-tax-calculator.html'),
            ('Freelance Tax Calculator', 'freelance-tax-calculator.html'),
            ('Freelance Expense Calculator', 'freelance-expense-calculator.html'),
        ],
        'faq': [
            ('What taxes do freelancers need to estimate?', 'Freelancers usually estimate income tax, self-employment tax, and any local or sales tax obligations.'),
            ('How much should I set aside for taxes?', 'A common starting point is 20-30% of net income, but your actual rate depends on your location and deductions.'),
            ('Can I use a calculator for quarterly payments?', 'Yes, calculators help you estimate how much to set aside and when to pay estimated taxes.'),
        ],
    },
    {
        'slug': 'invoice-best-practices',
        'title': 'Invoice Best Practices for Freelancers: Charge Right and Get Paid Faster',
        'description': 'Learn invoice best practices for freelancers, including how to estimate, present, and manage billing with confidence.',
        'topic': 'invoice',
        'links': [
            ('Freelance Invoice Calculator', 'freelance-invoice-calculator.html'),
            ('Freelance Invoice Generator', 'freelance-invoice-generator.html'),
            ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
        ],
        'faq': [
            ('What makes an invoice effective?', 'An effective invoice is clear, accurate, and includes payment terms, due dates, and itemized service details.'),
            ('Should freelancers charge tax on invoices?', 'If you are required to collect sales or VAT, include the tax line clearly on the invoice.'),
            ('How can I reduce payment delays?', 'Use clear terms, follow up professionally, and consider deposits or milestone payments.'),
        ],
    },
    {
        'slug': 'freelance-billing-growth',
        'title': 'Freelance Billing Growth: Use Your Calculator to Scale Income',
        'description': 'A practical guide to scaling freelance billing and revenue using calculator insights and structured planning.',
        'topic': 'freelance billing',
        'links': [
            ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
            ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
            ('Freelance Revenue Calculator', 'freelance-revenue-calculator.html'),
        ],
        'faq': [
            ('How can billing tools help freelancers grow?', 'Billing tools help you understand cash flow, set better client terms, and plan for more consistent revenue.'),
            ('Is it better to bill hourly or by project?', 'It depends on the work type, but using a calculator helps you compare and choose the right model for your goals.'),
            ('Can I use the same process for new clients?', 'Yes. Apply the same planning steps to quote and bill each client with confidence.'),
        ],
    },
    {
        'slug': 'freelance-budgeting-tips',
        'title': 'Freelance Budgeting Tips: Balance Income, Expenses, and Tax Planning',
        'description': 'A budgeting guide for freelancers that explains how to balance income goals, expenses, and tax planning with calculators.',
        'topic': 'freelance budgeting',
        'links': [
            ('Freelance Budget Calculator', 'freelance-budget-calculator.html'),
            ('Freelance Expense Calculator', 'freelance-expense-calculator.html'),
            ('Freelance Business Calculator', 'freelance-business-calculator.html'),
        ],
        'faq': [
            ('Why is budgeting important for freelancers?', 'Budgeting helps freelancers keep track of income, prepare for slow periods, and avoid spending surprises.'),
            ('Can I use budgeting with income estimates?', 'Yes. Combining budgeting with income estimates gives you a more complete financial plan.'),
            ('What expenses should I track?', 'Track both fixed costs and variable business expenses like software, marketing, insurance, and travel.'),
        ],
    },
    {
        'slug': 'hourly-rate-calculation-methods',
        'title': 'Hourly Rate Calculation Methods: Compare Project, Day, and Hourly Pricing',
        'description': 'Explore hourly rate calculation methods and compare project, daily, and hourly pricing approaches for freelancers.',
        'topic': 'hourly rate calculation',
        'links': [
            ('Freelance Hourly Rate Calculator', 'freelance-hourly-rate-calculator.html'),
            ('Freelance Rate Calculator', 'freelance-rate-calculator.html'),
            ('Freelance Pricing Calculator', 'freelance-pricing-calculator.html'),
        ],
        'faq': [
            ('What is the easiest rate calculation method?', 'Using your target income divided by billable hours gives a practical baseline rate.'),
            ('How do I compare hourly and project pricing?', 'Estimate your hourly rate first, then use that baseline to price fixed projects based on scope.'),
            ('Should I change rates for different services?', 'Yes, adjust your pricing to reflect the value, complexity, and client budget of each service.'),
        ],
    },
    {
        'slug': 'tax-deduction-checklist',
        'title': 'Tax Deduction Checklist for Freelancers: Track Deductible Expenses and Improve Cash Flow',
        'description': 'A freelancer tax deduction checklist that helps you track deductible expenses and improve cash flow with simple planning.',
        'topic': 'freelancer tax deductions',
        'links': [
            ('Freelance Tax Calculator', 'freelance-tax-calculator.html'),
            ('Freelance Income Tax Calculator', 'freelance-income-tax-calculator.html'),
            ('Freelance Expense Calculator', 'freelance-expense-calculator.html'),
        ],
        'faq': [
            ('What counts as a deductible expense?', 'Common deductible expenses include software, office supplies, equipment, travel, and marketing costs related to your freelance work.'),
            ('How do deductions affect cash flow?', 'Deductions lower your taxable income and can reduce the amount you owe, freeing up more cash for your business.'),
            ('Can calculators help with deductions?', 'Yes, calculators help you estimate your net income after expense deductions and taxes.'),
        ],
    },
    {
        'slug': 'invoice-payment-workflow',
        'title': 'Invoice and Payment Workflow for Freelancers: Estimate Payments and Manage Cash Flow',
        'description': 'A workflow guide for freelancers that explains how to estimate payments and manage cash flow from invoice to receipt.',
        'topic': 'invoice workflow',
        'links': [
            ('Freelance Invoice Generator', 'freelance-invoice-generator.html'),
            ('Freelance Payment Calculator', 'freelance-payment-calculator.html'),
            ('Freelance Quote Calculator', 'freelance-quote-calculator.html'),
        ],
        'faq': [
            ('What is a freelancer payment workflow?', 'It is a process for estimating, invoicing, tracking, and collecting client payments.'),
            ('How do I reduce payment delays?', 'Set clear terms, send timely invoices, and follow up promptly when payments are late.'),
            ('Should I use milestones for large projects?', 'Yes, milestone payments help maintain cash flow and reduce risk for both you and the client.'),
        ],
    },
]

BLOG_LINKS = [
    ('Freelance Calculator Guide', 'blog/freelance-calculator-guide.html'),
    ('Freelance Income Planning', 'blog/freelance-income-planning.html'),
    ('Hourly Rate Strategy', 'blog/hourly-rate-strategy.html'),
    ('Freelancer Tax Basics', 'blog/freelancer-tax-basics.html'),
    ('Invoice Best Practices', 'blog/invoice-best-practices.html'),
    ('Freelance Billing Growth', 'blog/freelance-billing-growth.html'),
    ('Freelance Budgeting Tips', 'blog/freelance-budgeting-tips.html'),
    ('Hourly Rate Calculation Methods', 'blog/hourly-rate-calculation-methods.html'),
    ('Tax Deduction Checklist', 'blog/tax-deduction-checklist.html'),
    ('Invoice and Payment Workflow', 'blog/invoice-payment-workflow.html'),
]

CALCULATOR_PAGES = {
    'Freelance Hourly Rate Calculator': 'freelance-hourly-rate-calculator.html',
    'Freelance Income Calculator': 'freelance-income-calculator.html',
    'Freelance Invoice Calculator': 'freelance-invoice-calculator.html',
    'Freelance Income Tax Calculator': 'freelance-income-tax-calculator.html',
    'Freelance Tax Calculator': 'freelance-tax-calculator.html',
    'Freelance Invoice Generator': 'freelance-invoice-generator.html',
    'Freelance Payment Calculator': 'freelance-payment-calculator.html',
    'Freelance Quote Calculator': 'freelance-quote-calculator.html',
    'Freelance Budget Calculator': 'freelance-budget-calculator.html',
    'Freelance Expense Calculator': 'freelance-expense-calculator.html',
    'Freelance Monthly Income Calculator': 'freelance-monthly-income-calculator.html',
    'Freelance Yearly Income Calculator': 'freelance-yearly-income-calculator.html',
    'Freelance Rate Calculator': 'freelance-rate-calculator.html',
    'Freelance Pricing Calculator': 'freelance-pricing-calculator.html',
    'Freelance Business Calculator': 'freelance-business-calculator.html',
    'Freelance Cost Calculator': 'freelance-cost-calculator.html',
    'Freelance Revenue Calculator': 'freelance-revenue-calculator.html',
    'Freelance Salary Calculator': 'freelance-salary-calculator.html',
    'Freelance Project Cost Calculator': 'freelance-project-cost-calculator.html',
    'Freelance Rate Calculator': 'freelance-rate-calculator.html',
}


def page_head(title, description, canonical, url):
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <link rel="canonical" href="{canonical}" />
    <link rel="icon" href="{PROJECT_PATH}favicon.svg" type="image/svg+xml" />
    <meta property="og:title" content="{title}" />
    <meta property="og:description" content="{description}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{url}" />
    <meta property="og:site_name" content="Freelancer Calculator Hub" />
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:site" content="@FreelancerCalcHub" />
    <link rel="stylesheet" href="{PROJECT_PATH}styles.css" />
'''


def breadcrumb_schema(name, url):
    data = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE_URL},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': f'{BASE_URL}blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': name, 'item': url},
        ]
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def article_schema(title, description, url, date='2026-08-03'):
    data = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'mainEntityOfPage': {'@type': 'WebPage', 'id': url},
        'headline': title,
        'description': description,
        'author': {'@type': 'Person', 'name': 'Freelancer Calculator Hub'},
        'publisher': {
            '@type': 'Organization',
            'name': 'Freelancer Calculator Hub',
            'logo': {
                '@type': 'ImageObject',
                'url': f'{BASE_URL}favicon.svg'
            }
        },
        'datePublished': date,
        'dateModified': date,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def faq_schema(faq_items):
    data = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': item[0],
                'acceptedAnswer': {'@type': 'Answer', 'text': item[1]},
            }
            for item in faq_items
        ]
    }
    return json.dumps(data, indent=2, ensure_ascii=False)


def page_footer(root_link):
    return f'''    <footer class="site-footer">
      <div class="container footer-row">
        <div class="footer-nav">
          <a href="{PROJECT_PATH}">Home</a>
          <a href="{PROJECT_PATH}blog/">Blog</a>
          <a href="{PROJECT_PATH}about.html">About</a>
          <a href="{PROJECT_PATH}contact.html">Contact</a>
          <a href="{PROJECT_PATH}privacy.html">Privacy</a>
          <a href="{PROJECT_PATH}terms.html">Terms</a>
        </div>
        <p>© 2026 Freelancer Calculator Hub</p>
      </div>
    </footer>
  </body>
</html>
'''


def render_related_tools(links):
    items = '\n'.join([f'            <li><a href="{PROJECT_PATH}{href}">{text}</a></li>' for text, href in links])
    return f'''      <section class="page-section">
        <div class="container content-card">
          <h2>Related Tools</h2>
          <p>Use these calculator pages to apply the ideas from this article directly.</p>
          <ul class="related-list">
{items}
          </ul>
        </div>
      </section>
'''


def article_body(post):
    intro = f"<p>Freelancers who use a {post['topic']} must often balance income goals with expenses and client expectations. This guide explains how to think clearly about those tradeoffs, what assumptions matter most, and how the right tools can make planning repeatable and confidence-building.</p>"
    problem = f"<p>The challenge for many independent professionals is that raw earnings do not tell the whole story. Without a simple model, it is hard to know whether hourly rates cover taxes, whether invoices reflect real costs, or whether income targets are achievable with available work hours.</p>"
    solution = f"<p>The solution is to use a structured approach: identify your goals, map expenses and taxes, and then compare the result to realistic work capacity. The example calculators on Freelancer Calculator Hub are designed to make those steps clear, practical, and easy to update as your business changes.</p>"
    example = f"<p>For example, a freelancer targeting $70,000 a year may use a calculator to test whether that goal is realistic with 35 billable hours per week and a 25% tax assumption. A single change in expense or billable hours can shift the required rate by tens of dollars, which is why modeling multiple scenarios is useful.</p>"
    closing = f"<p>By grounding decisions in data, you can avoid surprise gaps between your income and your costs. That makes it easier to price your services, plan invoices, and keep cash flow steady as you grow your freelance business.</p>"
    faq_blocks = ''
    for q, a in post['faq']:
        faq_blocks += (
            '          <details>\n'
            '            <summary>' + q + '</summary>\n'
            '            <p>' + a + '</p>\n'
            '          </details>\n'
        )
    return (
        '      <section class="page-section">\n'
        '        <div class="container content-card">\n'
        '          <h1>' + post['title'] + '</h1>\n'
        '          <h2>Introduction</h2>\n'
        '          ' + intro + '\n'
        '          <h2>Problem</h2>\n'
        '          ' + problem + '\n'
        '          <h2>Solution</h2>\n'
        '          ' + solution + '\n'
        '          <h2>Example</h2>\n'
        '          ' + example + '\n'
        '          <h2>FAQ</h2>\n'
        + faq_blocks +
        '          <h2>Next Steps</h2>\n'
        '          <p>Once you understand this process, apply it to the calculators linked below and refine your plan based on your own goals and business context.</p>\n'
        '        </div>\n'
        '      </section>\n'
    )


def write_article(post):
    filename = BLOG_DIR / f"{post['slug']}.html"
    canonical = f'{BASE_URL}blog/{post["slug"]}.html'
    url = canonical
    head = page_head(post['title'], post['description'], canonical, url)
    breadcrumb = breadcrumb_schema(post['title'], url)
    article = article_schema(post['title'], post['description'], url)
    faq = faq_schema(post['faq'])
    body_sections = article_body(post)
    links = render_related_tools(post['links'])
    content = f'''{head}    <script type="application/ld+json">
{breadcrumb}
    </script>
    <script type="application/ld+json">
{article}
    </script>
    <script type="application/ld+json">
{faq}
    </script>
  </head>
  <body>
    <header class="site-header">
      <div class="container nav">
        <a class="brand" href="{PROJECT_PATH}">Freelancer Calculator Hub</a>
        <nav class="site-nav" aria-label="Main navigation">
          <a href="{PROJECT_PATH}">Home</a>
          <a href="{PROJECT_PATH}blog/">Blog</a>
          <a href="{PROJECT_PATH}about.html">About</a>
          <a href="{PROJECT_PATH}contact.html">Contact</a>
          <a href="{PROJECT_PATH}terms.html">Terms</a>
          <a href="{PROJECT_PATH}privacy.html">Privacy</a>
        </nav>
      </div>
    </header>

    <main>
{body_sections}
{links}    </main>
{page_footer('../')}
'''
    filename.write_text(content, encoding='utf-8')
    return filename


def write_blog_index():
    title = 'Freelancer Calculator Blog — Insights for Freelance Income, Rates, Taxes, and Invoices'
    description = 'Read the Freelancer Calculator Hub blog for practical advice on freelance calculators, income planning, hourly rates, taxes, invoices, and more.'
    canonical = f'{BASE_URL}blog/'
    url = canonical
    blog_items = ''.join([
        '            <li><a href="' + PROJECT_PATH + post[1] + '">' + post[0] + '</a></li>\n'
        for post in BLOG_LINKS
    ])
    head = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '  <head>\n'
        '    <meta charset="UTF-8" />\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        '    <title>' + title + '</title>\n'
        '    <meta name="description" content="' + description + '" />\n'
        '    <link rel="canonical" href="' + canonical + '" />\n'
        '    <link rel="icon" href="' + PROJECT_PATH + 'favicon.svg" type="image/svg+xml" />\n'
        '    <meta property="og:title" content="' + title + '" />\n'
        '    <meta property="og:description" content="' + description + '" />\n'
        '    <meta property="og:type" content="website" />\n'
        '    <meta property="og:url" content="' + url + '" />\n'
        '    <meta property="og:site_name" content="Freelancer Calculator Hub" />\n'
        '    <meta name="twitter:card" content="summary" />\n'
        '    <meta name="twitter:title" content="' + title + '" />\n'
        '    <meta name="twitter:description" content="' + description + '" />\n'
        '    <meta name="twitter:site" content="@FreelancerCalcHub" />\n'
        '    <link rel="stylesheet" href="' + PROJECT_PATH + 'styles.css" />\n'
        '    <script type="application/ld+json">\n'
        + json.dumps({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE_URL},{'@type':'ListItem','position':2,'name':'Blog','item':canonical}]}, indent=2, ensure_ascii=False) + '\n'
        '    </script>\n'
        '  </head>\n'
        '  <body>\n'
        '    <header class="site-header">\n'
        '      <div class="container nav">\n'
        '        <a class="brand" href="' + PROJECT_PATH + '">Freelancer Calculator Hub</a>\n'
        '        <nav class="site-nav" aria-label="Main navigation">\n'
        '          <a href="' + PROJECT_PATH + '">Home</a>\n'
        '          <a href="' + PROJECT_PATH + 'blog/">Blog</a>\n'
        '          <a href="' + PROJECT_PATH + 'about.html">About</a>\n'
        '          <a href="' + PROJECT_PATH + 'contact.html">Contact</a>\n'
        '          <a href="' + PROJECT_PATH + 'terms.html">Terms</a>\n'
        '          <a href="' + PROJECT_PATH + 'privacy.html">Privacy</a>\n'
        '        </nav>\n'
        '      </div>\n'
        '    </header>\n'
        '    <main>\n'
        '      <section class="hero">\n'
        '        <div class="container hero-grid">\n'
        '          <div>\n'
        '            <p class="eyebrow">BLOG</p>\n'
        '            <h1>Freelancer Calculator Hub Blog</h1>\n'
        '            <p class="hero-copy">Explore practical articles for freelancers on calculators, income planning, hourly rates, taxes, invoices, and business growth.</p>\n'
        '          </div>\n'
        '        </div>\n'
        '      </section>\n'
        '      <section class="page-section">\n'
        '        <div class="container content-card">\n'
        '          <h2>Latest articles</h2>\n'
        '          <ul class="blog-list">\n'
        + blog_items +
        '          </ul>\n'
        '        </div>\n'
        '      </section>\n'
        '    </main>\n'
        + page_footer('../')
    )
    (BLOG_DIR / 'index.html').write_text(head, encoding='utf-8')


def write_root_blog_page():
    title = 'Freelancer Calculator Blog — Insights for Freelance Income, Rates, Taxes, and Invoices'
    description = 'Read the Freelancer Calculator Hub blog for practical advice on freelance calculators, income planning, hourly rates, taxes, invoices, and more.'
    canonical = f'{BASE_URL}blog.html'
    url = canonical
    blog_items = ''.join([
        '            <li><a href="' + PROJECT_PATH + item[1] + '">' + item[0] + '</a></li>\n'
        for item in BLOG_LINKS
    ])
    head = (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '  <head>\n'
        '    <meta charset="UTF-8" />\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
        '    <title>' + title + '</title>\n'
        '    <meta name="description" content="' + description + '" />\n'
        '    <link rel="canonical" href="' + canonical + '" />\n'
        '    <link rel="icon" href="' + PROJECT_PATH + 'favicon.svg" type="image/svg+xml" />\n'
        '    <meta property="og:title" content="' + title + '" />\n'
        '    <meta property="og:description" content="' + description + '" />\n'
        '    <meta property="og:type" content="website" />\n'
        '    <meta property="og:url" content="' + url + '" />\n'
        '    <meta property="og:site_name" content="Freelancer Calculator Hub" />\n'
        '    <meta name="twitter:card" content="summary" />\n'
        '    <meta name="twitter:title" content="' + title + '" />\n'
        '    <meta name="twitter:description" content="' + description + '" />\n'
        '    <meta name="twitter:site" content="@FreelancerCalcHub" />\n'
        '    <link rel="stylesheet" href="' + PROJECT_PATH + 'styles.css" />\n'
        '    <script type="application/ld+json">\n'
        + json.dumps({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE_URL},{'@type':'ListItem','position':2,'name':'Blog','item':f'{BASE_URL}blog.html'}]}, indent=2, ensure_ascii=False) + '\n'
        '    </script>\n'
        '  </head>\n'
        '  <body>\n'
        '    <header class="site-header">\n'
        '      <div class="container nav">\n'
        '        <a class="brand" href="' + PROJECT_PATH + '">Freelancer Calculator Hub</a>\n'
        '        <nav class="site-nav" aria-label="Main navigation">\n'
        '          <a href="' + PROJECT_PATH + '">Home</a>\n'
        '          <a href="' + PROJECT_PATH + 'blog/">Blog</a>\n'
        '          <a href="' + PROJECT_PATH + 'about.html">About</a>\n'
        '          <a href="' + PROJECT_PATH + 'contact.html">Contact</a>\n'
        '          <a href="' + PROJECT_PATH + 'terms.html">Terms</a>\n'
        '          <a href="' + PROJECT_PATH + 'privacy.html">Privacy</a>\n'
        '        </nav>\n'
        '      </div>\n'
        '    </header>\n'
        '    <main>\n'
        '      <section class="hero">\n'
        '        <div class="container hero-grid">\n'
        '          <div>\n'
        '            <p class="eyebrow">BLOG</p>\n'
        '            <h1>Freelancer Calculator Hub Blog</h1>\n'
        '            <p class="hero-copy">Explore practical articles for freelancers on calculators, income planning, hourly rates, taxes, invoices, and business growth.</p>\n'
        '          </div>\n'
        '        </div>\n'
        '      </section>\n'
        '      <section class="page-section">\n'
        '        <div class="container content-card">\n'
        '          <h2>Featured articles</h2>\n'
        '          <ul class="blog-list">\n'
        + blog_items +
        '          </ul>\n'
        '        </div>\n'
        '      </section>\n'
        '    </main>\n'
        + page_footer('')
    )
    Path('blog.html').write_text(head, encoding='utf-8')


def write_post_template():
    template = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Blog Post Template | Not for Indexing</title>
    <meta name="description" content="Internal template used to prepare future Freelancer Calculator Hub blog posts." />
    <meta name="robots" content="noindex,nofollow" />
    <link rel="icon" href="{PROJECT_PATH}favicon.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="{PROJECT_PATH}styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="container nav">
        <a class="brand" href="{PROJECT_PATH}">Freelancer Calculator Hub</a>
        <nav class="site-nav" aria-label="Main navigation">
          <a href="{PROJECT_PATH}">Home</a>
          <a href="{PROJECT_PATH}blog/">Blog</a>
          <a href="{PROJECT_PATH}about.html">About</a>
          <a href="{PROJECT_PATH}contact.html">Contact</a>
          <a href="{PROJECT_PATH}terms.html">Terms</a>
          <a href="{PROJECT_PATH}privacy.html">Privacy</a>
        </nav>
      </div>
    </header>
    <main>
      <section class="page-section">
        <div class="container content-card">
          <h1>{{POST_TITLE}}</h1>
          <h2>Introduction</h2>
          <p>[INTRODUCTION]</p>
          <h2>Problem</h2>
          <p>[PROBLEM]</p>
          <h2>Solution</h2>
          <p>[SOLUTION]</p>
          <h2>Example</h2>
          <p>[EXAMPLE]</p>
          <h2>FAQ</h2>
          [FAQ_BLOCKS]
          <h2>Related Tools</h2>
          <ul>
            [RELATED_LINKS]
          </ul>
        </div>
      </section>
    </main>
    <footer class="site-footer">
      <div class="container footer-row">
        <div class="footer-nav">
          <a href="{PROJECT_PATH}">Home</a>
          <a href="{PROJECT_PATH}blog/">Blog</a>
          <a href="{PROJECT_PATH}about.html">About</a>
          <a href="{PROJECT_PATH}contact.html">Contact</a>
          <a href="{PROJECT_PATH}privacy.html">Privacy</a>
          <a href="{PROJECT_PATH}terms.html">Terms</a>
        </div>
        <p>© 2026 Freelancer Calculator Hub</p>
      </div>
    </footer>
  </body>
</html>
'''
    (BLOG_DIR / 'post-template.html').write_text(template, encoding='utf-8')


def write_blog_sitemap():
    sitemap_items = [
        f'  <url>\n    <loc>{BASE_URL}blog/{post["slug"]}.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>'
        for post in posts
    ]
    sitemap_items.insert(0, f'  <url>\n    <loc>{BASE_URL}blog/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>')
    sitemap_items.insert(0, f'  <url>\n    <loc>{BASE_URL}blog.html</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>')
    content = '<xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(sitemap_items) + '\n</urlset>\n'
    (BLOG_DIR / 'sitemap.xml').write_text(content, encoding='utf-8')


def update_root_sitemap():
    path = Path('sitemap.xml')
    txt = path.read_text(encoding='utf-8')
    new_urls = [
        f'  <url>\n    <loc>{BASE_URL}blog.html</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>',
        f'  <url>\n    <loc>{BASE_URL}blog/</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.9</priority>\n  </url>'
    ]
    for post in posts:
        new_urls.append(f'  <url>\n    <loc>{BASE_URL}blog/{post["slug"]}.html</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>')
    if '</urlset>' in txt:
        txt = txt.replace('</urlset>', '\n'.join(new_urls) + '\n</urlset>')
    path.write_text(txt, encoding='utf-8')


def update_robots():
    path = Path('robots.txt')
    txt = path.read_text(encoding='utf-8')
    if 'Sitemap:' not in txt:
        txt += f'\nSitemap: {BASE_URL}sitemap.xml\nSitemap: {BASE_URL}blog/sitemap.xml\n'
    else:
        if f'Sitemap: {BASE_URL}blog/sitemap.xml' not in txt:
            txt = txt.strip() + f'\nSitemap: {BASE_URL}blog/sitemap.xml\n'
    path.write_text(txt, encoding='utf-8')


def update_audit_script():
    path = Path('audit_site.py')
    txt = path.read_text(encoding='utf-8')
    txt = txt.replace("files = sorted(glob.glob('*.html'))", "files = sorted(Path('.').rglob('*.html'))")
    Path('audit_site.py').write_text(txt, encoding='utf-8')


def main():
    for post in posts:
        write_article(post)
    write_blog_index()
    write_root_blog_page()
    write_post_template()
    write_blog_sitemap()
    update_root_sitemap()
    update_robots()
    update_audit_script()
    subprocess.run(
        [sys.executable, str(Path(__file__).with_name('seo_repair.py')), '--apply'],
        check=True,
    )
    print('generated blog content and updated sitemap/robots/audit')


if __name__ == '__main__':
    main()
