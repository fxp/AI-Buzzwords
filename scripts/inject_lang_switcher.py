#!/usr/bin/env python3
"""
Idempotent injection of lang-switcher into existing HTML articles.

For each article HTML in deepdive/, this script:
  1. Adds <script src="<repo-root>/lang-switcher.js" defer></script> to <head> (if not present)
  2. Adds <link rel="alternate" hreflang="..."> tags for each available language
  3. Adds <div data-lang-switcher data-slug="..."></div> to the top strip area
     (after the [TOPIC] / dimension marker, before the version label) — only
     if not already present

Strategy: minimal regex-based edits that respect existing HTML.

Usage:
  python scripts/inject_lang_switcher.py [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEEPDIVE = REPO_ROOT / "deepdive"

DRY_RUN = "--dry-run" in sys.argv


def relative_to_repo_root(html_path: Path) -> str:
    """Compute relative path from this html file to the repo root."""
    depth = len(html_path.relative_to(REPO_ROOT).parts) - 1
    return "../" * depth


def has_switcher_script(html: str) -> bool:
    return "lang-switcher.js" in html


def has_switcher_div(html: str) -> bool:
    return "data-lang-switcher" in html


def inject_head_tags(html: str, base: str, slug: str, languages: list, default_lang: str, current_lang: str, file_url_path: str) -> str:
    """Add script src + hreflang link tags to <head>."""
    additions = []

    # Script tag
    if not has_switcher_script(html):
        additions.append(f'<script src="{base}lang-switcher.js" defer></script>')

    # hreflang tags — one per available language
    for lang in languages:
        suffix = lang.get("filename_suffix", "")
        href = f'{file_url_path.replace(".html", "")}{suffix}.html'
        # Don't add if already there
        if f'hreflang="{lang["hreflang"]}"' in html:
            continue
        additions.append(f'<link rel="alternate" hreflang="{lang["hreflang"]}" href="{href}" />')
    # x-default
    if 'hreflang="x-default"' not in html and any(l.get("default") for l in languages):
        default_obj = next((l for l in languages if l.get("default")), None)
        if default_obj:
            href = f'{file_url_path.replace(".html", "")}{default_obj.get("filename_suffix", "")}.html'
            additions.append(f'<link rel="alternate" hreflang="x-default" href="{href}" />')

    if not additions:
        return html

    block = "\n  " + "\n  ".join(additions)
    # Insert before </head>
    return re.sub(r"</head>", block + "\n</head>", html, count=1, flags=re.IGNORECASE)


def inject_switcher_div(html: str, slug: str) -> str:
    """Add <div data-lang-switcher data-slug="..."></div> to the top strip."""
    if has_switcher_div(html):
        return html

    container = f'<div data-lang-switcher data-slug="{slug}" style="margin-left:auto"></div>'

    # Strategy: find the existing top strip and add switcher right before the version span
    # Patterns to look for (in order of preference):
    # 1. After dimension-map link (white-collar pattern)
    # 2. Before <span class="...flex-1...">  (the spacer)
    # 3. Before the closing div of the strip

    # Match flex-1 spacer span and insert container BEFORE it
    pattern1 = re.compile(r'(<span class="[^"]*flex-1[^"]*"[^>]*></span>)', re.IGNORECASE)
    if pattern1.search(html):
        return pattern1.sub(container + r"\n    \1", html, count=1)

    # Fallback: insert immediately after <body...>
    return re.sub(r"(<body[^>]*>)", r"\1\n" + container, html, count=1, flags=re.IGNORECASE)


def update_html_lang(html: str, lang_code: str) -> str:
    """Set <html lang="..."> based on file's language."""
    return re.sub(r'<html[^>]*lang="[^"]*"', f'<html lang="{lang_code}"', html, count=1)


def derive_lang_from_filename(html_path: Path, languages: list) -> str:
    """white-collar.en.html → en; white-collar.html → default."""
    name = html_path.stem  # white-collar.en or white-collar
    for lang in languages:
        suffix = lang.get("filename_suffix", "")
        if not suffix:
            continue
        sfx_no_dot = suffix.lstrip(".")
        if name.endswith(f".{sfx_no_dot}"):
            return lang["code"]
    # No suffix → default
    return next((l["code"] for l in languages if l.get("default")), "zh")


def find_article_files(deepdive_dir: Path):
    """Yield (html_path, meta) tuples for all articles with meta.json."""
    for meta_path in sorted(deepdive_dir.rglob("*.meta.json")):
        slug = meta_path.stem.replace(".meta", "")
        topic_dir = meta_path.parent
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        # Find all language variants
        for lang_code in meta.get("languages", []):
            # Find the language object from config
            yield meta_path, slug, topic_dir, lang_code, meta


def main():
    languages_cfg = json.loads((REPO_ROOT / "config" / "languages.json").read_text(encoding="utf-8"))
    languages = languages_cfg["languages"]

    changed_count = 0

    meta_files = sorted(DEEPDIVE.rglob("*.meta.json"))
    for meta_path in meta_files:
        slug = meta_path.stem.replace(".meta", "")
        topic_dir = meta_path.parent
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        article_languages = meta.get("languages", ["zh"])

        # Build list of language objects available for THIS article
        available_lang_objs = [l for l in languages if l["code"] in article_languages]

        for lang_code in article_languages:
            lang_obj = next((l for l in languages if l["code"] == lang_code), None)
            if not lang_obj:
                continue
            suffix = lang_obj.get("filename_suffix", "")
            html_file = topic_dir / f"{slug}{suffix}.html"
            if not html_file.exists():
                continue

            html = html_file.read_text(encoding="utf-8")
            base = relative_to_repo_root(html_file)
            file_url_path = f"{slug}{suffix}.html"  # used for hreflang relative URLs

            new_html = update_html_lang(html, lang_obj.get("html_lang", lang_code))
            new_html = inject_head_tags(new_html, base, slug, available_lang_objs, lang_obj.get("default", False), lang_code, f"{slug}.html")
            new_html = inject_switcher_div(new_html, slug)

            if new_html != html:
                changed_count += 1
                rel = html_file.relative_to(REPO_ROOT)
                if DRY_RUN:
                    print(f"[would update] {rel}")
                else:
                    html_file.write_text(new_html, encoding="utf-8")
                    print(f"[updated] {rel}")

    print(f"\nTotal {'would-update' if DRY_RUN else 'updated'}: {changed_count}")


if __name__ == "__main__":
    main()
