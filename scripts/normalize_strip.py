#!/usr/bin/env python3
"""
Normalize TOP STRIP across all article HTMLs.

For each article in deepdive/<topic>/<slug>(.lang)?.html:
  1. Locate the existing TOP STRIP block (Pattern A or Pattern B)
  2. Locate any stray <div data-lang-switcher ...> that landed OUTSIDE the strip
     (the broken Phase 1 injection on Pattern-B articles)
  3. Replace the strip block with the standardized Pattern A strip filled
     from config/themes.json
  4. Add data-theme="<accent>" attribute to <body>
  5. Inject --accent / --accent-glow CSS variables

Idempotent: re-running on already-normalized articles is a no-op.

Usage:
  python scripts/normalize_strip.py [--dry-run] [--slug <slug>]
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEEPDIVE = REPO_ROOT / "deepdive"
THEMES_PATH = REPO_ROOT / "config" / "themes.json"
STRIP_TEMPLATE = REPO_ROOT / "templates" / "_strip.html"


def load_themes():
    return json.loads(THEMES_PATH.read_text(encoding="utf-8"))


def render_strip(template: str, theme_entry: dict, slug: str) -> str:
    nav = theme_entry.get("nav_pill") or {}
    href = nav.get("href", "")
    label = nav.get("label", "")
    out = template
    out = out.replace("{{TOPIC_LABEL}}", theme_entry.get("topic_label", ""))
    out = out.replace("{{SLUG}}", slug)
    out = out.replace("{{VERSION_LABEL}}", theme_entry.get("version_label", ""))
    if href and label:
        out = out.replace("{{NAV_PILL_HREF}}", href).replace("{{NAV_PILL_LABEL}}", label)
    else:
        # Drop the nav-pill <a> entirely if no nav configured
        out = re.sub(
            r'\s*<a href="\{\{NAV_PILL_HREF\}\}"[^>]*>\{\{NAV_PILL_LABEL\}\}</a>\n',
            "\n",
            out,
        )
    return out


STRIP_COMMENT = re.compile(
    r"<!--\s*[═=]*\s*TOP STRIP\s*[═=]*\s*-->",
    re.IGNORECASE,
)


def find_strip_block(html: str):
    """Locate (start, end) of strip = comment + the div block following it.

    Walks divs with proper nesting balance. Handles Pattern A (2-deep) and
    Pattern B (3-deep with grid children) without leaving leftover </div>s.
    Returns None if no strip found.
    """
    m = STRIP_COMMENT.search(html)
    if not m:
        return None
    start = m.start()
    pos = m.end()
    # Skip whitespace then expect <div
    while pos < len(html) and html[pos] in " \n\r\t":
        pos += 1
    if not html.startswith("<div", pos):
        return None
    # Count divs until balance returns to 0
    depth = 0
    i = pos
    while i < len(html):
        next_open = html.find("<div", i)
        next_close = html.find("</div>", i)
        if next_close == -1:
            return None
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + len("<div")
        else:
            depth -= 1
            i = next_close + len("</div>")
            if depth == 0:
                return (start, i)
    return None

# Floating lang-switcher placed at body top (broken Phase 1 injection)
FLOATING_SWITCHER = re.compile(
    r'\s*<div data-lang-switcher[^>]*></div>\s*\n',
    re.IGNORECASE,
)


SKIP_SLUGS = {
    # Custom-CSS pages without standard tailwind.config — normalizing
    # would break their layout. Update manually if needed.
    "dimension-map",
    "the-stall",  # paper-themed research article (light bg, intentional design)
}


def normalize_one(html_path: Path, themes: dict, dry_run: bool) -> bool:
    """Returns True if file was changed (or would be in dry-run)."""
    html = html_path.read_text(encoding="utf-8")
    original = html
    slug = derive_slug(html_path)
    if not slug or slug not in themes["articles"]:
        return False
    if slug in SKIP_SLUGS:
        return False

    theme_entry = themes["articles"][slug]
    accent = theme_entry.get("accent", themes["default_theme"])
    palette = themes["palette"][accent]

    # 1. Replace strip block
    template = STRIP_TEMPLATE.read_text(encoding="utf-8")
    # Strip the leading comment block from template (it's docs-only)
    template_body = re.sub(r"^<!--.*?-->\s*", "", template, count=1, flags=re.DOTALL)
    new_strip = render_strip(template_body, theme_entry, slug).rstrip()

    span = find_strip_block(html)
    if span:
        html = html[:span[0]] + new_strip + html[span[1]:]
    else:
        # No existing TOP STRIP comment — assume custom-design page (e.g.
        # dimension-map). Skip insertion; user can opt in with --insert.
        return False

    # 2. Remove floating lang-switcher BEFORE the new strip (only the body-top one;
    #    keep any switcher inside the new strip we just inserted)
    body_match = re.search(r"<body[^>]*>", html, re.IGNORECASE)
    if body_match:
        body_pos = body_match.end()
        new_strip_pos = html.find(new_strip, body_pos)
        if new_strip_pos > body_pos:
            head_segment = html[body_pos:new_strip_pos]
            cleaned = FLOATING_SWITCHER.sub("\n", head_segment)
            if cleaned != head_segment:
                html = html[:body_pos] + cleaned + html[new_strip_pos:]

    # 3. Set <body data-theme="...">
    def add_theme(m):
        body_tag = m.group(0)
        if 'data-theme=' in body_tag:
            return re.sub(r'data-theme="[^"]*"', f'data-theme="{accent}"', body_tag)
        # Insert before closing >
        return body_tag[:-1].rstrip() + f' data-theme="{accent}">'
    html = re.sub(r"<body[^>]*>", add_theme, html, count=1, flags=re.IGNORECASE)

    # 4. Inject --accent / --accent-glow CSS variables at the top of <head>
    #    (only if not already there)
    css_var_block = (
        f'<style id="theme-vars">'
        f':root{{--accent:{palette["hex"]};--accent-glow:{palette["glow"]};--accent-soft:{palette["soft"]};}}'
        f'</style>'
    )
    if 'id="theme-vars"' in html:
        # Replace existing
        html = re.sub(
            r'<style id="theme-vars">[^<]*</style>',
            css_var_block,
            html,
        )
    else:
        # Insert right after <head>
        html = re.sub(r"(<head[^>]*>)", r"\1\n" + css_var_block, html, count=1, flags=re.IGNORECASE)

    if html == original:
        return False

    if dry_run:
        print(f"[would normalize] {html_path.relative_to(REPO_ROOT)}")
    else:
        html_path.write_text(html, encoding="utf-8")
        print(f"[normalized]     {html_path.relative_to(REPO_ROOT)}")
    return True


def derive_slug(html_path: Path) -> str:
    """white-collar.html → 'white-collar'; index.html → use parent dir name."""
    name = html_path.stem
    # Strip language suffix: white-collar.en → white-collar
    name = re.sub(r"\.(en|cn|zh|ja|ko)$", "", name, flags=re.IGNORECASE)
    if name == "index":
        return html_path.parent.name
    return name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--slug", help="Only normalize this slug")
    args = parser.parse_args()

    themes = load_themes()
    changed = 0
    scanned = 0

    for html_path in sorted(DEEPDIVE.rglob("*.html")):
        if "test-deploy" in str(html_path):
            continue
        slug = derive_slug(html_path)
        if args.slug and slug != args.slug:
            continue
        scanned += 1
        if normalize_one(html_path, themes, args.dry_run):
            changed += 1

    print(f"\nScanned {scanned}, {'would change' if args.dry_run else 'changed'}: {changed}")


if __name__ == "__main__":
    main()
