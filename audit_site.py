from __future__ import annotations

import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parent
BASE_URL = "https://uu9988.github.io/freelancer-calculator/"
PROJECT_PATH = "/freelancer-calculator/"
PRODUCTION_HOST = "uu9988.github.io"
DUPLICATE_BLOG_PATH = "/blog/" + "blog/"
CHILD_SITEMAPS = ["pages-sitemap.xml", "tools-sitemap.xml", "blog/sitemap.xml"]
XML_FILES = ["sitemap.xml", *CHILD_SITEMAPS, "rss.xml", "BingSiteAuth.xml"]
VERIFICATION_FILES = {"google60c46abce2c0ec23.html", "BingSiteAuth.xml"}
NOINDEX_RULES = {
    "404.html": ("noindex,follow", None),
    "blog.html": ("noindex,follow", BASE_URL + "blog/"),
    "blog/post-template.html": ("noindex,nofollow", None),
}


class Audit:
    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def error(self, location: str, message: str) -> None:
        self.errors.append((location, message))

    def warning(self, location: str, message: str) -> None:
        self.warnings.append((location, message))


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def clean_text(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value)).split())


def tags(text: str, tag_name: str) -> list[str]:
    return re.findall(rf"<{tag_name}\b[^>]*>", text, flags=re.I)


def attr(tag: str, name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*=\s*([\"'])(.*?)\1", tag, flags=re.I | re.S)
    return html.unescape(match.group(2).strip()) if match else ""


def meta_values(text: str, key: str, *, property_attr: bool = False) -> list[str]:
    attribute = "property" if property_attr else "name"
    values = []
    for tag in tags(text, "meta"):
        if attr(tag, attribute).lower() == key.lower():
            values.append(attr(tag, "content"))
    return values


def canonical_values(text: str) -> list[str]:
    return [attr(tag, "href") for tag in tags(text, "link") if attr(tag, "rel").lower() == "canonical"]


def page_url_to_file(url: str) -> Path | None:
    if not url.startswith(BASE_URL):
        return None
    relative = unquote(url[len(BASE_URL) :]).split("?", 1)[0].split("#", 1)[0]
    if not relative:
        return ROOT / "index.html"
    if relative.endswith("/"):
        return ROOT / relative / "index.html"
    return ROOT / relative


def file_to_url(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return BASE_URL
    if relative.endswith("/index.html"):
        return BASE_URL + relative[: -len("index.html")]
    return BASE_URL + relative


def parse_sitemaps(audit: Audit) -> tuple[list[str], dict[str, Path]]:
    for filename in XML_FILES:
        try:
            ET.parse(ROOT / filename)
        except (ET.ParseError, OSError) as exc:
            audit.error(filename, f"XML parse failed: {exc}")

    try:
        root = ET.parse(ROOT / "sitemap.xml").getroot()
    except (ET.ParseError, OSError):
        return [], {}
    if local_name(root.tag) != "sitemapindex":
        audit.error("sitemap.xml", "Root element must be sitemapindex")
    child_urls = [node.text.strip() for node in root.iter() if local_name(node.tag) == "loc" and node.text]
    expected_children = [BASE_URL + filename.replace("\\", "/") for filename in CHILD_SITEMAPS]
    if child_urls != expected_children:
        audit.error("sitemap.xml", f"Child sitemap list differs from expected: {expected_children}")

    urls: list[str] = []
    mapping: dict[str, Path] = {}
    for filename in CHILD_SITEMAPS:
        try:
            child_root = ET.parse(ROOT / filename).getroot()
        except (ET.ParseError, OSError):
            continue
        if local_name(child_root.tag) != "urlset":
            audit.error(filename, "Root element must be urlset")
            continue
        for node in child_root.iter():
            if local_name(node.tag) != "loc" or not node.text:
                continue
            url = node.text.strip()
            urls.append(url)
            path = page_url_to_file(url)
            if path is None:
                audit.error(filename, f"URL is outside the production base path: {url}")
            elif not path.is_file():
                audit.error(filename, f"URL does not map to a file: {url}")
            else:
                mapping[url] = path
    duplicates = [url for url, count in Counter(urls).items() if count > 1]
    if duplicates:
        audit.error("sitemaps", f"Duplicate URLs: {duplicates}")
    for excluded in ["404.html", "blog.html", "blog/post-template.html", "google60c46abce2c0ec23.html"]:
        excluded_url = file_to_url(ROOT / excluded)
        if excluded_url in urls:
            audit.error("sitemaps", f"Excluded page is present: {excluded_url}")
    return urls, mapping


def resolve_reference(source: Path, value: str) -> tuple[Path | None, str]:
    value = html.unescape(value.strip())
    parsed = urlsplit(value)
    if parsed.scheme in {"mailto", "tel", "data", "javascript"}:
        return None, ""
    if parsed.scheme in {"http", "https"}:
        absolute = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if not absolute.startswith(BASE_URL.rstrip("/")):
            return None, parsed.fragment
        target = page_url_to_file(absolute)
        return target, parsed.fragment
    if value.startswith("//"):
        return None, parsed.fragment
    if not parsed.path:
        return source, parsed.fragment
    if parsed.path.startswith("/freelancer-calculator/"):
        target = ROOT / parsed.path[len("/freelancer-calculator/") :]
    elif parsed.path.startswith("/"):
        return None, parsed.fragment
    else:
        target = source.parent / unquote(parsed.path)
    target = target.resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, parsed.fragment


def deployed_page_url(path: Path, *, nested_404: bool = False) -> str:
    """Return the browser base URL used to resolve references on GitHub Pages."""
    if nested_404:
        return BASE_URL + "missing/deep/page.html"
    return file_to_url(path)


def audit_deployed_reference(audit: Audit, path: Path, tag_name: str, value: str) -> None:
    """Simulate browser URL resolution for the GitHub Pages project path."""
    location = path.relative_to(ROOT).as_posix()
    parsed = urlsplit(html.unescape(value.strip()))
    if parsed.scheme in {"mailto", "tel", "data", "javascript"} or value.startswith("//"):
        return

    has_local_path = bool(parsed.path) and not parsed.scheme and not parsed.netloc
    if has_local_path and not parsed.path.startswith(PROJECT_PATH):
        audit.error(location, f"Internal {tag_name} reference must use {PROJECT_PATH}: {value}")

    source_url = deployed_page_url(path, nested_404=location == "404.html")
    resolved = urlsplit(urljoin(source_url, value))
    if resolved.hostname != PRODUCTION_HOST:
        return
    if not resolved.path.startswith(PROJECT_PATH):
        audit.error(location, f"Reference leaves the GitHub Pages project path: {value} -> {resolved.path}")
    if DUPLICATE_BLOG_PATH in resolved.path:
        audit.error(location, f"Reference resolves to a duplicated blog path: {value} -> {resolved.path}")


def audit_404_href_targets(audit: Audit, path: Path, text: str) -> None:
    """Require every 404 href to resolve to a real file in this project."""
    if path.relative_to(ROOT).as_posix() != "404.html":
        return

    hrefs = [attr(tag, "href") for tag in tags(text, "a") if attr(tag, "href")]
    hourly_rate_href = PROJECT_PATH + "freelance-hourly-rate-calculator.html"
    if hrefs.count(hourly_rate_href) != 1:
        audit.error("404.html", f"404 page must link once to {hourly_rate_href}")

    for value in hrefs:
        target, _ = resolve_reference(path, value)
        if target is None:
            audit.error("404.html", f"404 href does not map to a local project file: {value}")
            continue
        try:
            relative_target = target.relative_to(ROOT)
        except ValueError:
            audit.error("404.html", f"404 href escapes the project root: {value}")
            continue
        if not target.is_file():
            audit.error("404.html", f"404 href target does not exist: {value} -> {relative_target}")


def jsonld_blocks(text: str, location: str, audit: Audit) -> list[dict]:
    blocks: list[dict] = []
    for index, match in enumerate(
        re.finditer(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            text,
            flags=re.I | re.S,
        ),
        1,
    ):
        try:
            value = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            audit.error(location, f"JSON-LD block {index} is invalid: {exc}")
            continue
        if not isinstance(value, dict):
            audit.error(location, f"JSON-LD block {index} must contain an object")
            continue
        blocks.append(value)
    return blocks


def nested_types(value) -> list[str]:
    result: list[str] = []
    if isinstance(value, dict):
        if isinstance(value.get("@type"), str):
            result.append(value["@type"])
        for child in value.values():
            result.extend(nested_types(child))
    elif isinstance(value, list):
        for child in value:
            result.extend(nested_types(child))
    return result


def visible_faq(text: str) -> list[tuple[str, str]]:
    return [
        (clean_text(match.group(1)), clean_text(match.group(2)))
        for match in re.finditer(
            r"<details[^>]*>\s*<summary>(.*?)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>",
            text,
            flags=re.I | re.S,
        )
    ]


def schema_faq(blocks: list[dict]) -> list[tuple[str, str]]:
    result = []
    for block in blocks:
        if block.get("@type") != "FAQPage":
            continue
        for item in block.get("mainEntity", []):
            if not isinstance(item, dict):
                continue
            answer = item.get("acceptedAnswer", {})
            if isinstance(answer, dict):
                result.append((clean_text(str(item.get("name", ""))), clean_text(str(answer.get("text", "")))))
    return result


def audit_page(
    audit: Audit,
    path: Path,
    expected_url: str | None,
    indexable: bool,
    incoming: defaultdict[Path, set[Path]],
) -> tuple[str, str]:
    location = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    head_match = re.search(r"<head>(.*?)</head>", text, flags=re.I | re.S)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", text, flags=re.I | re.S)
    if not head_match or not body_match:
        audit.error(location, "Missing head or body element")
        return "", ""
    head = head_match.group(1)
    body = body_match.group(1)

    title_matches = re.findall(r"<title[^>]*>(.*?)</title>", head, flags=re.I | re.S)
    descriptions = meta_values(head, "description")
    canonicals = canonical_values(head)
    robots = meta_values(head, "robots")
    if len(title_matches) != 1 or not clean_text(title_matches[0]) if title_matches else True:
        audit.error(location, "Must contain exactly one non-empty title")
    if len(descriptions) != 1 or not descriptions[0]:
        audit.error(location, "Must contain exactly one non-empty meta description")
    if len(robots) != 1:
        audit.error(location, "Must contain exactly one robots meta")
    if len(meta_values(head, "viewport")) != 1:
        audit.error(location, "Must contain exactly one viewport meta")

    title = clean_text(title_matches[0]) if title_matches else ""
    description = descriptions[0] if descriptions else ""
    if indexable:
        if canonicals != [expected_url]:
            audit.error(location, f"Canonical must be {expected_url!r}, found {canonicals!r}")
        if robots != ["index,follow"]:
            audit.error(location, f"Indexable page robots must be index,follow, found {robots!r}")
    elif location in NOINDEX_RULES:
        expected_robots, expected_canonical = NOINDEX_RULES[location]
        if robots != [expected_robots]:
            audit.error(location, f"Expected robots {expected_robots!r}, found {robots!r}")
        if expected_canonical is None and canonicals:
            audit.error(location, "Temporary template must not contain a canonical")
        if expected_canonical is not None and canonicals != [expected_canonical]:
            audit.error(location, f"Expected canonical {expected_canonical!r}, found {canonicals!r}")

    if indexable or location != "blog/post-template.html":
        required_og = ["og:type", "og:title", "og:description", "og:url", "og:site_name"]
        for key in required_og:
            values = meta_values(head, key, property_attr=True)
            if len(values) != 1 or not values[0]:
                audit.error(location, f"Missing or duplicate {key}")
        for key in ["twitter:card", "twitter:title", "twitter:description"]:
            values = meta_values(head, key)
            if len(values) != 1 or not values[0]:
                audit.error(location, f"Missing or duplicate {key}")
        if meta_values(head, "twitter:card") not in (["summary"], []):
            audit.warning(location, "twitter:card should be summary when no real share image exists")
    if meta_values(head, "twitter:image") or meta_values(head, "og:image", property_attr=True):
        audit.warning(location, "Share image is declared; verify that it exists and is intentional")
    if title and len(title) > 60:
        audit.warning(location, f"Title is {len(title)} characters and may truncate")
    if indexable and description and len(description) < 120:
        audit.warning(location, f"Description is only {len(description)} characters")
    if description and len(description) > 165:
        audit.warning(location, f"Description is {len(description)} characters and may truncate")

    h1 = re.findall(r"<h1\b[^>]*>(.*?)</h1>", body, flags=re.I | re.S)
    if len(h1) != 1:
        audit.error(location, f"Expected one H1, found {len(h1)}")
    heading_levels = [int(match.group(1)) for match in re.finditer(r"<h([1-6])\b", body, flags=re.I)]
    for previous, current in zip(heading_levels, heading_levels[1:]):
        if current > previous + 1:
            audit.error(location, f"Heading hierarchy jumps from H{previous} to H{current}")
            break
    if location == "index.html" and (not h1 or "freelance hourly rate calculator" not in clean_text(h1[0]).lower()):
        audit.error(location, "Homepage H1 must describe the freelance hourly rate calculator")

    blocks = jsonld_blocks(head, location, audit)
    root_types = [str(block.get("@type", "")) for block in blocks]
    duplicates = [name for name, count in Counter(root_types).items() if name and count > 1]
    if duplicates:
        audit.error(location, f"Duplicate root JSON-LD types: {duplicates}")
    all_types = nested_types(blocks)
    if "Organization" in all_types or "Person" in all_types:
        audit.error(location, "Unverified Person or Organization schema is present")
    visible = visible_faq(body)
    structured = schema_faq(blocks)
    if structured and structured != visible:
        audit.error(location, "FAQPage questions/answers do not exactly match all visible FAQ details")
    if visible and indexable and not structured:
        audit.error(location, "Visible FAQ content is missing matching FAQPage schema")
    if location == "index.html":
        for required_type in ["WebSite", "WebApplication", "FAQPage"]:
            if root_types.count(required_type) != 1:
                audit.error(location, f"Homepage requires exactly one {required_type} schema")
    elif location.startswith("freelance-") and indexable:
        if "WebApplication" in root_types:
            audit.error(location, "Non-interactive landing page must not claim WebApplication")
        if "WebPage" not in root_types:
            audit.error(location, "Tool/guide landing page requires WebPage schema")
    elif location.startswith("blog/") and location not in {"blog/index.html", "blog/post-template.html"}:
        if "Article" not in root_types:
            audit.error(location, "Blog post requires Article schema")
        if meta_values(head, "og:type", property_attr=True) != ["article"]:
            audit.error(location, "Blog post og:type must be article")
    if location in NOINDEX_RULES and location in {"404.html", "blog/post-template.html"} and blocks:
        audit.error(location, "404/template page must not contain JSON-LD")

    audit_404_href_targets(audit, path, text)
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', text, flags=re.I))
    for tag_name, attribute in [
        ("a", "href"),
        ("link", "href"),
        ("script", "src"),
        ("img", "src"),
        ("source", "src"),
    ]:
        for tag in tags(text, tag_name):
            value = attr(tag, attribute)
            if not value:
                if tag_name in {"a", "img"}:
                    audit.error(location, f"<{tag_name}> has an empty {attribute}")
                continue
            development_hosts = ("local" + "host", "127" + ".0.0.1")
            if any(host in value.lower() for host in development_hosts):
                audit.error(location, f"Development URL found: {value}")
            if tag_name == "a" and value == "#":
                audit.error(location, "Meaningless href=\"#\" found")
            audit_deployed_reference(audit, path, tag_name, value)
            target, fragment = resolve_reference(path, value)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                audit.error(location, f"Reference escapes the project root: {value}")
                continue
            if not target.is_file():
                audit.error(location, f"Broken internal reference: {value} -> {target.relative_to(ROOT)}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_text = target.read_text(encoding="utf-8")
                target_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', target_text, flags=re.I))
                if fragment not in target_ids:
                    audit.error(location, f"Missing fragment target: {value}")
            if tag_name == "a" and target.suffix.lower() == ".html" and target != path:
                incoming[target].add(path)
    for image_tag in tags(text, "img"):
        if not re.search(r'\balt\s*=\s*(["\']).*?\1', image_tag, flags=re.I | re.S):
            audit.error(location, "Image is missing alt attribute")

    plain_body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.I | re.S)
    word_count = len(re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)*", clean_text(plain_body)))
    if indexable and location.startswith(("freelance-", "blog/")) and location != "blog/index.html" and word_count < 250:
        audit.warning(location, f"Page has only {word_count} visible English words")
    if indexable and location.startswith("freelance-") and not re.search(
        r'href=["\']/freelancer-calculator/blog/', body, flags=re.I
    ):
        audit.error(location, "Tool/guide page does not link to a related blog article")
    if indexable and location.startswith("blog/") and location != "blog/index.html" and not re.search(
        r'href=["\']/freelancer-calculator/freelance-[^"\']+\.html', body, flags=re.I
    ):
        audit.error(location, "Blog article does not link to a related calculator page")
    return title, description


def main() -> int:
    audit = Audit()
    urls, sitemap_mapping = parse_sitemaps(audit)
    public_paths = set(sitemap_mapping.values())
    incoming: defaultdict[Path, set[Path]] = defaultdict(set)
    titles: defaultdict[str, list[str]] = defaultdict(list)
    descriptions: defaultdict[str, list[str]] = defaultdict(list)

    html_files = sorted(ROOT.rglob("*.html"))
    for path in html_files:
        location = path.relative_to(ROOT).as_posix()
        if location in VERIFICATION_FILES:
            continue
        indexable = path in public_paths
        expected_url = file_to_url(path) if indexable else None
        title, description = audit_page(audit, path, expected_url, indexable, incoming)
        if indexable:
            titles[title].append(location)
            descriptions[description].append(location)

    for value, locations in titles.items():
        if value and len(locations) > 1:
            audit.error("titles", f"Duplicate title on {locations}: {value}")
    for value, locations in descriptions.items():
        if value and len(locations) > 1:
            audit.error("descriptions", f"Duplicate description on {locations}: {value}")
    canonical_urls = [file_to_url(path) for path in public_paths]
    if len(canonical_urls) != len(set(canonical_urls)):
        audit.error("canonicals", "Indexable pages do not have unique production URLs")

    for path in sorted(public_paths):
        if path == ROOT / "index.html":
            continue
        if not incoming[path]:
            audit.error(path.relative_to(ROOT).as_posix(), "Orphan page: no incoming link from another local HTML page")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "User-agent: *" not in robots or "Allow: /" not in robots:
        audit.error("robots.txt", "Global crawler access is not allowed")
    main_directive = f"Sitemap: {BASE_URL}sitemap.xml"
    if main_directive not in robots:
        audit.error("robots.txt", "Main sitemap directive is missing or incorrect")
    if re.search(r"^Sitemap:.*rss\.xml", robots, flags=re.I | re.M):
        audit.error("robots.txt", "RSS must not be declared as a Sitemap directive")

    broken_links = sum("Broken internal reference" in message for _, message in audit.errors)
    project_path_errors = sum(
        "GitHub Pages project path" in message or "duplicated blog path" in message
        for _, message in audit.errors
    )
    orphan_pages = sum("Orphan page" in message for _, message in audit.errors)
    jsonld_errors = sum("JSON-LD" in message and "invalid" in message for _, message in audit.errors)
    xml_errors = sum("XML parse failed" in message for _, message in audit.errors)
    print(f"HTML files scanned: {len(html_files) - 1} (Google verification file excluded)")
    print(f"Indexable sitemap URLs: {len(urls)}")
    print(f"Errors: {len(audit.errors)}")
    print(f"Warnings: {len(audit.warnings)}")
    print(f"Internal broken links: {broken_links}")
    print(f"GitHub Pages path errors: {project_path_errors}")
    print(f"Orphan indexable pages: {orphan_pages}")
    print(f"JSON-LD parse errors: {jsonld_errors}")
    print(f"Sitemap/XML parse errors: {xml_errors}")
    if audit.errors:
        print("\nERRORS")
        for location, message in audit.errors:
            print(f"- {location}: {message}")
    if audit.warnings:
        print("\nWARNINGS")
        for location, message in audit.warnings:
            print(f"- {location}: {message}")
    if not audit.errors:
        print("\nSEO AUDIT PASS")
    return 1 if audit.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
