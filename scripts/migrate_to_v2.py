#!/usr/bin/env python3
"""
Migrate articles to Design System v2 — additive-only.

Pattern (validated on palantir-aip 2026-05-08):
  1. Inject <link rel="stylesheet" href="<rel>/colors_and_type.css"> after <title>
  2. Add data-theme="<accent>" to <html> (look up accent in config/themes.json)
  3. Insert <button data-toggle-mode> in top strip right after lang-switcher
  4. Inject <script src="<rel>/mode-toggle.js" defer> next to lang-switcher.js

Strictly additive — does NOT modify the article's existing <style> block,
inline tailwind.config, or per-article custom CSS. Visual behaviour is
preserved; v2 layers on top via cascade. Future deeper cleanup (removing
duplicate .lamp / .cursor / .pullquote-mark) can be done per-article when
each article is touched.

Idempotent: re-running on already-migrated files is a no-op.

Excludes via SKIP_SLUGS:
  - dimension-map (custom CSS, no tailwind.config)
  - the-stall (custom paper-themed design)
  - test-deploy (placeholder)
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEEPDIVE = REPO_ROOT / "deepdive"
THEMES_PATH = REPO_ROOT / "config" / "themes.json"

SKIP_SLUGS = {"dimension-map", "the-stall", "test-deploy"}


def derive_slug(html_path: Path) -> str:
    """white-collar.html → 'white-collar'; index.html → use parent dir name."""
    name = html_path.stem
    name = re.sub(r"\.(en|cn|zh|ja|ko)$", "", name, flags=re.IGNORECASE)
    if name == "index":
        return html_path.parent.name
    return name


def relative_to_repo_root(html_path: Path) -> str:
    """Compute '../' string from the html file to repo root."""
    depth = len(html_path.relative_to(REPO_ROOT).parts) - 1
    return "../" * depth


def load_themes() -> dict:
    return json.loads(THEMES_PATH.read_text(encoding="utf-8"))


def already_migrated(html: str) -> dict:
    """Returns dict of which migration steps already done."""
    return {
        "css_link": 'href="' in html and 'colors_and_type.css' in html,
        "data_theme": re.search(r'<html\b[^>]*\bdata-theme=', html, re.I) is not None,
        "toggle_button": 'data-toggle-mode' in html,
        "toggle_script": 'mode-toggle.js' in html,
    }


def add_css_link(html: str, base: str) -> str:
    """Insert <link> after </title> if not already present."""
    if 'colors_and_type.css' in html:
        return html
    link_tag = (
        f'\n<!-- Design System v2: canonical token CSS (fonts, themes, type, CJK rules) -->\n'
        f'<link rel="stylesheet" href="{base}colors_and_type.css">'
    )
    return re.sub(r'(</title>)', r'\1' + link_tag, html, count=1, flags=re.IGNORECASE)


def add_data_theme(html: str, accent: str) -> str:
    """Add data-theme="<accent>" to <html>. No-op if already present."""
    def repl(m):
        tag = m.group(0)
        if 'data-theme=' in tag:
            return tag
        return tag[:-1].rstrip() + f' data-theme="{accent}">'
    return re.sub(r'<html\b[^>]*>', repl, html, count=1, flags=re.IGNORECASE)


def add_toggle_button(html: str, lang_code: str) -> str:
    """Insert <button data-toggle-mode> right after the lang-switcher div in the strip.

    No-op if button already present.
    """
    if 'data-toggle-mode' in html:
        return html
    is_en = lang_code.startswith("en")
    label_dark = "Dark" if is_en else "暗色"
    label_light = "Light" if is_en else "浅色"
    button_html = (
        f'\n    <button data-toggle-mode aria-pressed="false" '
        f'class="font-mono text-[9px] lg:text-[10px] tracking-[0.18em] uppercase '
        f'text-fg-mute hover:text-accent border border-line-bright px-2 py-0.5 transition-colors" '
        f'style="background:transparent;cursor:pointer" '
        f'data-label-light="{label_light}" data-label-dark="{label_dark}">'
        f'\n      <span data-mode-icon>◐</span> <span data-mode-label>{label_dark}</span>'
        f'\n    </button>'
    )
    # Insert after the <div data-lang-switcher ...></div> line
    pattern = re.compile(r'(<div data-lang-switcher[^>]*>\s*</div>)', re.IGNORECASE)
    if pattern.search(html):
        return pattern.sub(r'\1' + button_html, html, count=1)
    return html


def add_toggle_script(html: str, base: str) -> str:
    """Insert <script src="...mode-toggle.js" defer></script> next to lang-switcher.js.

    No-op if already present.
    """
    if 'mode-toggle.js' in html:
        return html
    pattern = re.compile(
        r'(<script src="[^"]*lang-switcher\.js"[^>]*></script>)',
        re.IGNORECASE,
    )
    if pattern.search(html):
        replacement = r'\1\n  <script src="' + base + r'mode-toggle.js" defer></script>'
        return pattern.sub(replacement, html, count=1)
    return html


def derive_html_lang(html: str) -> str:
    """Read <html lang="..."> attribute, default 'zh'."""
    m = re.search(r'<html[^>]*\blang="([^"]*)"', html, re.I)
    return m.group(1) if m else "zh"


def migrate_one(html_path: Path, themes: dict, dry_run: bool) -> dict:
    """Returns status dict."""
    slug = derive_slug(html_path)
    if slug in SKIP_SLUGS:
        return {"skipped": True, "reason": "skip-slug"}
    if slug not in themes.get("articles", {}):
        return {"skipped": True, "reason": "no-theme-entry"}

    theme_entry = themes["articles"][slug]
    accent = theme_entry.get("accent", themes.get("default_theme", "amber"))

    html = html_path.read_text(encoding="utf-8")
    original = html
    base = relative_to_repo_root(html_path)
    lang_code = derive_html_lang(html)

    before = already_migrated(html)
    html = add_css_link(html, base)
    html = add_data_theme(html, accent)
    html = add_toggle_button(html, lang_code)
    html = add_toggle_script(html, base)
    after = already_migrated(html)

    changed_steps = [k for k in before if not before[k] and after[k]]

    if html == original:
        return {"skipped": True, "reason": "already-migrated"}

    if not dry_run:
        html_path.write_text(html, encoding="utf-8")
    return {"skipped": False, "added": changed_steps, "accent": accent}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--slug", help="Only migrate this slug")
    args = ap.parse_args()

    themes = load_themes()

    results = {"changed": [], "skipped": []}
    for html_path in sorted(DEEPDIVE.rglob("*.html")):
        slug = derive_slug(html_path)
        if args.slug and slug != args.slug:
            continue
        rel = html_path.relative_to(REPO_ROOT)
        result = migrate_one(html_path, themes, args.dry_run)
        if result.get("skipped"):
            results["skipped"].append((str(rel), result.get("reason")))
        else:
            results["changed"].append((str(rel), result["accent"], result["added"]))
            tag = "[would-migrate]" if args.dry_run else "[migrated]"
            print(f"{tag} {rel}  → theme={result['accent']}  added={','.join(result['added']) or 'none'}")

    print(f"\nChanged: {len(results['changed'])}, Skipped: {len(results['skipped'])}")
    if args.dry_run:
        skipped_by_reason = {}
        for path, reason in results["skipped"]:
            skipped_by_reason.setdefault(reason, []).append(path)
        for reason, paths in skipped_by_reason.items():
            print(f"  skip:{reason} → {len(paths)} files")


if __name__ == "__main__":
    main()
