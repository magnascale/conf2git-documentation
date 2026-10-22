"""Check generated routes, local links/assets, heading anchors, and search coverage."""

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = yaml.safe_load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
BASE = CONFIG["site_url"]
BASE_PATH = urlsplit(BASE).path


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.heading_ids = set()
        self.links = []
        self.content_tag = None
        self.content_depth = 0
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.content_tag == tag:
            self.content_depth += 1
        elif self.content_tag is None and (attrs.get("role") == "main" or tag == "article"):
            self.content_tag = tag
            self.content_depth = 1
        if "id" in attrs:
            self.ids.add(attrs["id"])
            if self.content_tag and tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
                self.heading_ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])

    def handle_endtag(self, tag):
        if tag == self.content_tag:
            self.content_depth -= 1
            if not self.content_depth:
                self.content_tag = None


def public_url(relative):
    relative = relative.as_posix()
    return BASE + (relative[:-10] if relative.endswith("index.html") else relative)


def check(site, baseline=None):
    errors = []
    if not site.is_dir():
        raise SystemExit("Build the site before running this check.")
    documents = {path.relative_to(site): Document(path) for path in site.rglob("*.html")}
    checked_links = 0

    def check_link(source, link):
        nonlocal checked_links
        parsed = urlsplit(urljoin(public_url(source), link))
        if parsed.scheme not in ("http", "https") or parsed.netloc != urlsplit(BASE).netloc:
            return
        if not parsed.path.startswith(BASE_PATH):
            errors.append(f"{source}: link escapes the project base: {link}")
            return
        relative = Path(unquote(parsed.path[len(BASE_PATH):]))
        target = site / relative
        if target.is_dir():
            relative /= "index.html"
            target = site / relative
        if not target.is_file():
            errors.append(f"{source}: missing target: {link}")
        elif parsed.fragment and relative in documents:
            if unquote(parsed.fragment) not in documents[relative].ids:
                errors.append(f"{source}: missing anchor: {link}")
        checked_links += 1

    for relative, document in documents.items():
        for link in document.links:
            check_link(relative, link)

    # CSS font/image URLs are not represented by HTML href/src attributes.
    for path in site.rglob("*.css"):
        for match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)['\"]?\s*\)", path.read_text(encoding="utf-8")):
            check_link(path.relative_to(site), match.group(1))

    markdown = sorted((ROOT / "docs").rglob("*.md"))
    expected_routes = {
        path.relative_to(ROOT / "docs").with_suffix("") / "index.html"
        if path.name != "index.md"
        else path.relative_to(ROOT / "docs").with_suffix(".html")
        for path in markdown
    }
    for route in expected_routes:
        if route not in documents:
            errors.append(f"Missing guide route: {route}")

    search_path = site / "search/search_index.json"
    if not search_path.is_file():
        errors.append("Missing search index")
    else:
        entries = json.loads(search_path.read_text(encoding="utf-8")).get("docs", [])
        if not entries:
            errors.append("Search index has no entries")
        locations = {urlsplit(entry["location"]).path for entry in entries}
        for route in expected_routes:
            location = route.as_posix()[:-10]
            if location not in locations:
                errors.append(f"Guide is missing from search: {route}")
        for entry in entries:
            check_link(Path("index.html"), entry["location"])

    if baseline:
        old_documents = {
            path.relative_to(baseline): Document(path) for path in baseline.rglob("*.html")
        }
        if not old_documents:
            errors.append("Baseline directory contains no HTML pages")
        old_routes = {path for path in old_documents if path.name == "index.html"}
        new_routes = {path for path in documents if path.name == "index.html"}
        if old_routes != new_routes:
            errors.append(f"Guide routes changed: {sorted(old_routes ^ new_routes)}")
        for route in old_routes & new_routes:
            if old_documents[route].heading_ids != documents[route].heading_ids:
                errors.append(f"Heading anchors changed: {route}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(markdown)} guide routes, {len(documents)} HTML pages, "
          f"{checked_links} local URLs/assets/anchors, and full search coverage.")
    if baseline:
        print("PASS: generated guide routes and heading anchors match the baseline.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=ROOT / "site")
    parser.add_argument("--baseline-site", type=Path)
    args = parser.parse_args()
    check(args.site_dir.resolve(), args.baseline_site.resolve() if args.baseline_site else None)
