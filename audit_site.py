import glob
import re

files = sorted(Path('.').rglob('*.html'))
print('file_count', len(files))
for fn in files:
    txt = open(fn, encoding='utf-8').read()
    title = bool(re.search(r'<title>.*?</title>', txt, re.I|re.S))
    desc = bool(re.search(r'<meta[^>]+name=["\']description["\']', txt, re.I))
    canon = bool(re.search(r'<link[^>]+rel=["\']canonical["\']', txt, re.I))
    robots = bool(re.search(r'<meta[^>]+name=["\']robots["\']', txt, re.I))
    og = bool(re.search(r'property=["\']og:', txt, re.I))
    twitter = bool(re.search(r'name=["\']twitter:', txt, re.I))
    schema = bool(re.search(r'<script type=["\']application/ld\+json["\']', txt, re.I))
    header = bool(re.search(r'<header.*?</header>', txt, re.S|re.I))
    footer = bool(re.search(r'<footer.*?</footer>', txt, re.S|re.I))
    related = bool(re.search(r'Related Tools|related tools', txt, re.I))
    print(fn, title, desc, canon, robots, og, twitter, schema, header, footer, related)
