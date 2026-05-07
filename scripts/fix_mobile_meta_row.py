#!/usr/bin/env python3
"""
Fix mobile alignment of evidence/case-card meta rows.

Issue: pattern `flex lg:flex-col flex-wrap gap-1.5 lg:gap-0` lacks
items-center, so on mobile the amber title (text-[13px]) and the date
(text-[11px]) baseline-misalign. Tag pills also carry mt-1.5 mr-1 which
double up against the container's gap, causing wrap weirdness.

Fixes:
  1. Add `items-center lg:items-start` (mobile centers row, desktop col stays left)
  2. Change `gap-1.5 lg:gap-0` → `gap-x-2 gap-y-1.5 lg:gap-0` (explicit axis gaps)
  3. Within affected meta blocks, drop `mt-1.5 mr-1` from pill spans
     (replaced by container gap-y/gap-x)

Idempotent. Run after normalize_strip.py / lang-switcher injection.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEEPDIVE = REPO_ROOT / "deepdive"

OLD_CONTAINER = "flex lg:flex-col flex-wrap gap-1.5 lg:gap-0"
NEW_CONTAINER = "flex lg:flex-col flex-wrap items-center lg:items-start gap-x-2 gap-y-1.5 lg:gap-0"

# Pill class fragment to clean inside affected meta divs
PILL_DOUBLE_MARGIN = re.compile(
    r'(<span class="inline-block border border-line-bright )py-0\.5 px-2 mt-1\.5 mr-1 (text-\[10px\])',
)


def find_meta_blocks(html: str):
    """Yield (start, end) spans of <div ...OLD_CONTAINER...>...</div>.

    Walks divs with proper nesting balance.
    """
    i = 0
    while True:
        idx = html.find(OLD_CONTAINER, i)
        if idx == -1:
            return
        # Find the enclosing <div start before idx
        div_start = html.rfind("<div", 0, idx)
        if div_start == -1:
            i = idx + 1
            continue
        # Find > that closes the opening tag
        gt = html.find(">", idx)
        if gt == -1:
            return
        # Walk balanced divs from gt+1
        depth = 1
        pos = gt + 1
        while pos < len(html) and depth > 0:
            next_open = html.find("<div", pos)
            next_close = html.find("</div>", pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
        yield (div_start, pos)
        i = pos


def fix_one(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html
    if OLD_CONTAINER not in html:
        return False

    # Step 1: replace container class string everywhere
    html = html.replace(OLD_CONTAINER, NEW_CONTAINER)

    # Step 2: within the original meta-block spans, remove mt-1.5 mr-1 from pills.
    # We re-discover blocks against the updated html (now with NEW_CONTAINER).
    new_class = NEW_CONTAINER
    cleaned_pieces = []
    last = 0
    i = 0
    while True:
        idx = html.find(new_class, i)
        if idx == -1:
            cleaned_pieces.append(html[last:])
            break
        div_start = html.rfind("<div", 0, idx)
        gt = html.find(">", idx)
        if div_start == -1 or gt == -1:
            i = idx + 1
            continue
        depth = 1
        pos = gt + 1
        while pos < len(html) and depth > 0:
            next_open = html.find("<div", pos)
            next_close = html.find("</div>", pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                pos = next_close + 6
        end = pos
        cleaned_pieces.append(html[last:div_start])
        block = html[div_start:end]
        block = PILL_DOUBLE_MARGIN.sub(r'\1py-0.5 px-2 \2', block)
        cleaned_pieces.append(block)
        last = end
        i = end
    html = "".join(cleaned_pieces)

    if html == original:
        return False
    path.write_text(html, encoding="utf-8")
    return True


def main():
    changed = 0
    scanned = 0
    for path in sorted(DEEPDIVE.rglob("*.html")):
        scanned += 1
        if fix_one(path):
            changed += 1
            print(f"[fixed] {path.relative_to(REPO_ROOT)}")
    print(f"\nScanned {scanned}, fixed: {changed}")


if __name__ == "__main__":
    main()
