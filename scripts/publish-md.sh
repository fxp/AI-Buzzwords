#!/usr/bin/env bash
# Publish any markdown file to the AI-Buzzwords repo and print the viewer URL.
#
# Usage:
#   scripts/publish-md.sh <source.md> [dest-subdir]
#
# Examples:
#   scripts/publish-md.sh ~/Documents/foo.md
#       → deepdive/foo/foo.md
#
#   scripts/publish-md.sh "~/.../[NEOLAB] AndonLab/report.md" deepdive/neolab
#       → deepdive/neolab/report.md
#
# Behavior:
#   - Copies <source.md> into <dest-subdir>/<basename> (default subdir = deepdive/<basename-no-ext>)
#   - git add + commit + push on the main branch
#   - Prints the GitHub Pages viewer URL on success
#
# Pages convention: never link the .md directly. Always go through viewer.html?f=<path>.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PAGES_BASE="https://fxp.github.io/AI-Buzzwords"

if [ "${1:-}" = "" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  sed -n '2,/^set -/p' "$0" | sed 's/^# \{0,1\}//; /^set -/d'
  exit 0
fi

src="$1"
[ -f "$src" ] || { echo "✗ source not found: $src" >&2; exit 1; }

basename="$(basename "$src")"
ext="${basename##*.}"
[ "$ext" = "md" ] || { echo "✗ source must be a .md file: $src" >&2; exit 1; }

stem="${basename%.md}"
subdir="${2:-deepdive/$stem}"
# strip any leading ./ or repo-root prefix
subdir="${subdir#./}"
subdir="${subdir#$REPO_ROOT/}"

dest_dir="$REPO_ROOT/$subdir"
dest="$dest_dir/$basename"

mkdir -p "$dest_dir"
cp "$src" "$dest"

cd "$REPO_ROOT"
git add "$subdir/$basename"

if git diff --cached --quiet; then
  echo "ℹ no changes (file identical to current HEAD)"
else
  git commit -m "Publish $subdir/$basename" \
             -m "Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>" >/dev/null
  git push --quiet
  echo "✓ committed & pushed"
fi

viewer_url="$PAGES_BASE/viewer.html?f=$subdir/$basename"
echo
echo "Viewer URL:"
echo "  $viewer_url"
