#!/usr/bin/env python3
"""
Deeper v2 migration: rewrite inline tailwind.config color tokens to use
CSS variables so Tailwind utility classes (text-amber, bg-bg, etc.) track
[data-mode="light"] dynamically.

Why: scripts/migrate_to_v2.py was additive-only — it added <link> to
colors_and_type.css and the toggle button, but left each article's inline
`tailwind.config` with hard-coded hex (`bg:'#0a0908'`). When a reader
clicks the dark/light toggle, --bg flips but `bg-bg` utility resolves to
the original hex, so the page doesn't visibly change.

This script rewrites the tailwind.config color block:
  bg:'#0a0908'             →  bg:'var(--bg)'
  'bg-2':'#111110'         →  'bg-2':'var(--bg-2)'
  fg:'#ebe6dc'             →  fg:'var(--fg)'
  amber:'#f5a524'          →  amber:'var(--amber)'
  signal:'#d1402c'         →  signal:'var(--signal)'
  mint:'#7fb88b'           →  mint:'var(--mint)'
  red:'#e84040'            →  red:'var(--red)'
  accent:'#xxxxxx'         →  accent:'var(--accent)'
  'accent-soft':'rgba(...)'→  'accent-soft':'var(--accent-soft)'
  'accent-glow':'rgba(...)'→  'accent-glow':'var(--accent-glow)'
  'amber-soft':'rgba(...)' →  'amber-soft':'var(--accent-soft)'
  'amber-glow':'rgba(...)' →  'amber-glow':'var(--accent-glow)'
  line:'#2b2823'           →  line:'var(--line)'
  'line-bright':'#443f37'  →  'line-bright':'var(--line-bright)'

Preserves existing whitespace and quoting style. Idempotent — re-running
on already-migrated files is a no-op.

Skips:
  - dimension-map / the-stall / test-deploy (per SKIP_SLUGS)
  - files without an inline `tailwind.config` block
"""
import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEEPDIVE = REPO_ROOT / "deepdive"

SKIP_SLUGS = {"dimension-map", "the-stall", "test-deploy", "vending-reverse"}

# Map token name → CSS var name. Order matters for replace correctness.
TOKEN_MAP = [
    ("bg-2",         "--bg-2"),
    ("bg-3",         "--bg-3"),
    ("bg-paper",     "--bg-paper"),
    ("bg-ink",       "--bg-ink"),
    ("bg",           "--bg"),
    ("fg-dim",       "--fg-dim"),
    ("fg-mute",      "--fg-mute"),
    ("fg",           "--fg"),
    ("line-bright",  "--line-bright"),
    ("line",         "--line"),
    ("accent-soft",  "--accent-soft"),
    ("accent-glow",  "--accent-glow"),
    ("accent",       "--accent"),
    ("amber-soft",   "--accent-soft"),
    ("amber-glow",   "--accent-glow"),
    ("amber",        "--amber"),
    ("mint-soft",    "rgba(127,184,139,0.12)"),  # keep static for cross-theme contrast
    ("mint-glow",    "rgba(127,184,139,0.25)"),
    ("mint",         "--mint"),
    ("signal",       "--signal"),
    ("red",          "--red"),
    ("paper",        "--bg-paper"),
    ("ink",          "--bg-ink"),
]


def derive_slug(html_path: Path) -> str:
    name = html_path.stem
    name = re.sub(r"\.(en|cn|zh|ja|ko)$", "", name, flags=re.IGNORECASE)
    if name == "index":
        return html_path.parent.name
    return name


def find_tailwind_config_block(html: str):
    """Return (start, end) of the inline `tailwind.config = {...}` JS object
    so we limit our regex replacements to that block only."""
    start_match = re.search(r"tailwind\.config\s*=\s*\{", html)
    if not start_match:
        return None
    # Scan forward, balancing braces
    depth = 0
    i = start_match.end() - 1  # at the opening {
    while i < len(html):
        c = html[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return (start_match.start(), i + 1)
        i += 1
    return None


def replace_token(block: str, token: str, var_value: str) -> tuple:
    """Replace `<token>: <ws> '<hex_or_rgba>'` with `<token>: <ws> 'var(--*)'` (or static).
    Returns (new_block, count). Preserves quotes (' or ") and key formatting.
    """
    # Match the token key (bare or quoted), then `: <ws>`, then a string literal value
    # We capture: prefix ($1 = key + colon + whitespace + opening quote), value ($2)
    if var_value.startswith("--"):
        replacement_value = f"var({var_value})"
    else:
        replacement_value = var_value

    # Two patterns: bare key (e.g. `bg:`) and quoted key (e.g. `'bg-2':`)
    # The hex value is `#xxxxxx` (3, 6, or 8 hex digits) OR an `rgba(...)` literal
    # We only replace if value LOOKS like a color literal (not already var(...))
    patterns = [
        # bare key: `bg : '#abc'` or `bg: '#abc'` (no quotes around key)
        rf"(\b{re.escape(token)}\b\s*:\s*['\"])(?!var\()(#[0-9a-fA-F]{{3,8}}|rgba?\([^)]+\))(['\"])",
        # quoted key: `'bg-2': '#xxx'`
        rf"(['\"]\s*{re.escape(token)}\s*['\"]\s*:\s*['\"])(?!var\()(#[0-9a-fA-F]{{3,8}}|rgba?\([^)]+\))(['\"])",
    ]

    total_count = 0
    for pat in patterns:
        new_block, n = re.subn(pat, lambda m: f"{m.group(1)}{replacement_value}{m.group(3)}", block)
        block = new_block
        total_count += n
    return block, total_count


def migrate_one(html_path: Path, dry_run: bool) -> dict:
    slug = derive_slug(html_path)
    if slug in SKIP_SLUGS:
        return {"skipped": True, "reason": "skip-slug"}

    html = html_path.read_text(encoding="utf-8")
    span = find_tailwind_config_block(html)
    if not span:
        return {"skipped": True, "reason": "no-tailwind-config"}

    block = html[span[0]:span[1]]
    original_block = block
    total_replacements = 0
    per_token = {}
    for token, var_target in TOKEN_MAP:
        block, n = replace_token(block, token, var_target)
        if n > 0:
            per_token[token] = n
            total_replacements += n

    if total_replacements == 0:
        return {"skipped": True, "reason": "already-vars"}

    new_html = html[:span[0]] + block + html[span[1]:]

    if not dry_run:
        html_path.write_text(new_html, encoding="utf-8")

    return {
        "skipped": False,
        "replacements": total_replacements,
        "per_token": per_token,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--slug", help="only this slug")
    args = ap.parse_args()

    changed = 0
    for html_path in sorted(DEEPDIVE.rglob("*.html")):
        slug = derive_slug(html_path)
        if args.slug and slug != args.slug:
            continue
        result = migrate_one(html_path, args.dry_run)
        if result.get("skipped"):
            if args.slug:  # be loud when targeting a specific slug
                print(f"[skip] {html_path.relative_to(REPO_ROOT)}: {result['reason']}")
            continue
        changed += 1
        tag = "[would-deepen]" if args.dry_run else "[deepened]"
        n = result["replacements"]
        toks = ",".join(result["per_token"].keys())
        print(f"{tag} {html_path.relative_to(REPO_ROOT)}  ({n} replacements: {toks})")

    print(f"\n{'Would change' if args.dry_run else 'Changed'}: {changed}")


if __name__ == "__main__":
    main()
