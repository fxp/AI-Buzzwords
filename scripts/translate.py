#!/usr/bin/env python3
"""
Translate DeepDive articles via BigModel GLM-5.1.

Reads:
  - config/languages.json  (which languages exist + which are translate_target)
  - config/glossary.json   (term consistency)
  - deepdive/<topic>/<slug>.meta.json  (per-article state)
  - deepdive/<topic>/<slug>.html       (source HTML)
  - deepdive/<topic>/<slug>-blog.md    (optional source markdown)

Writes:
  - deepdive/<topic>/<slug>.<lang>.html
  - deepdive/<topic>/<slug>-blog.<lang>.md
  - Updated meta.json with translations.<lang>.synced_at_version

Strategy:
  For each (slug, target_lang) where target_lang is missing OR
  meta.translations[target_lang].synced_at_version < meta.current_version,
  translate the source files using GLM-5.1.

Env:
  BIGMODEL_API_KEY        — required
  BIGMODEL_API_ENDPOINT   — optional, defaults to api.z.ai (overseas)
  BIGMODEL_MODEL          — optional, defaults to glm-5.1
  TRANSLATE_DRY_RUN       — if "true", print what would be done, don't call API
  TRANSLATE_FORCE_SLUG    — optional, only process this slug (for testing)

Output:
  Prints one line per translated file. Final line is JSON summary
  (consumed by translate.yml → Slack notification).
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
DEEPDIVE_DIR = REPO_ROOT / "deepdive"

API_KEY = os.environ.get("BIGMODEL_API_KEY", "")
API_ENDPOINT = os.environ.get(
    "BIGMODEL_API_ENDPOINT",
    "https://api.z.ai/api/paas/v4/chat/completions",
)
MODEL = os.environ.get("BIGMODEL_MODEL", "glm-5.1")
DRY_RUN = os.environ.get("TRANSLATE_DRY_RUN", "").lower() == "true"
FORCE_SLUG = os.environ.get("TRANSLATE_FORCE_SLUG", "")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def call_glm(messages, max_retries=3):
    """Call BigModel GLM-5.1 chat completions. Returns content string."""
    if DRY_RUN:
        return "[DRY RUN — no API call]"
    if not API_KEY:
        raise RuntimeError("BIGMODEL_API_KEY not set")

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 32000,
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                API_ENDPOINT, data=body, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')[:500]}"
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = str(e)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"GLM call failed after {max_retries}: {last_err}")


def build_glossary_block(glossary: dict, target_lang: str, source_lang: str) -> str:
    lines = []
    for term, entry in glossary.get("terms", {}).items():
        src = entry.get(source_lang)
        tgt = entry.get(target_lang)
        if not src or not tgt:
            continue
        ctx = entry.get("context", "")
        ctx_str = f"  ({ctx})" if ctx else ""
        do_not = " [keep original]" if entry.get("do_not_translate") else ""
        lines.append(f"  · {src} → {tgt}{do_not}{ctx_str}")
    return "\n".join(lines)


def translate_html(html: str, source_lang: str, target_lang: str, glossary: dict, lang_meta: dict) -> str:
    """Translate full HTML preserving structure."""
    glossary_block = build_glossary_block(glossary, target_lang, source_lang)

    target_lang_obj = next(
        (l for l in lang_meta["languages"] if l["code"] == target_lang), {}
    )
    html_lang = target_lang_obj.get("html_lang", target_lang)

    system_prompt = f"""You are translating a Chinese deep-dive tech article to English while preserving HTML structure exactly.

CRITICAL RULES:
1. NEVER modify HTML tags, attribute values, class names, or URLs.
2. NEVER modify content inside <script>, <style>, <code>, or <pre> tags (except translating string values inside JS string literals if they are user-facing copy — be conservative; default to leaving JS strings alone).
3. Translate ONLY natural-language text content visible to readers (text nodes, alt/title attributes, aria-label, meta description if Chinese).
4. Apply the glossary strictly. When you see a source-language term, use the exact target-language form provided.
5. Replace <html lang="zh"> (or similar) with <html lang="{html_lang}">.
6. Update or add <link rel="alternate" hreflang="..."> tags if you see them in <head>; otherwise do not add new ones.
7. Use natural English punctuation: em-dash (—) instead of ——, straight quotes for English (\" \"), avoid awkward direct word-for-word renderings.
8. Preserve numerical data, dates, percentages, names of papers/companies exactly.
9. Output ONLY the translated HTML — no commentary, no markdown fences, no preamble.

GLOSSARY (apply when relevant):
{glossary_block}
"""

    user_prompt = f"Translate this {source_lang} HTML to {target_lang}:\n\n{html}"

    return call_glm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])


def translate_markdown(md: str, source_lang: str, target_lang: str, glossary: dict) -> str:
    """Translate markdown blog file."""
    glossary_block = build_glossary_block(glossary, target_lang, source_lang)

    system_prompt = f"""Translate this Chinese markdown blog post to English.

RULES:
1. Preserve all markdown syntax: headers (#), lists (-), tables, code fences (```), links ([text](url)), bold/italic.
2. Preserve URLs verbatim. Translate link text only when natural.
3. Preserve frontmatter (--- ... ---) keys; translate values that are user-facing copy.
4. Apply the glossary strictly.
5. Use natural English flow — do not preserve Chinese sentence structures word-for-word.
6. Output ONLY the translated markdown — no commentary.

GLOSSARY:
{glossary_block}
"""
    return call_glm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Translate this {source_lang} markdown to {target_lang}:\n\n{md}"},
    ])


def needs_translation(meta: dict, target_lang: str) -> bool:
    """Returns True if target_lang is missing or stale."""
    if target_lang not in meta.get("languages", []):
        return True
    sync = meta.get("translations", {}).get(target_lang, {})
    synced_v = sync.get("synced_at_version", 0)
    return synced_v < meta["current_version"]


def find_source_files(meta_path: Path):
    """Given meta.json path, find source HTML + optional blog.md."""
    slug = meta_path.stem.replace(".meta", "")  # white-collar.meta.json → white-collar
    topic_dir = meta_path.parent
    html = topic_dir / f"{slug}.html"
    blog_md = topic_dir / f"{slug}-blog.md"
    return slug, topic_dir, html if html.exists() else None, blog_md if blog_md.exists() else None


def translate_one(meta_path: Path, target_lang: str, languages: dict, glossary: dict) -> list:
    """Returns list of translated file paths (relative to repo root)."""
    meta = load_json(meta_path)
    if FORCE_SLUG and meta.get("slug") != FORCE_SLUG:
        return []
    if meta.get("manual_only", False):
        return []
    if not needs_translation(meta, target_lang):
        return []

    source_lang = meta.get("primary_language", "zh")
    slug, topic_dir, html_path, blog_path = find_source_files(meta_path)

    target_lang_obj = next(
        (l for l in languages["languages"] if l["code"] == target_lang), None
    )
    if not target_lang_obj:
        return []
    suffix = target_lang_obj.get("filename_suffix", f".{target_lang}")

    written = []
    print(f"[translate] {slug} → {target_lang}", file=sys.stderr)

    if html_path and html_path.exists():
        out_html = topic_dir / f"{slug}{suffix}.html"
        translated = translate_html(
            html_path.read_text(encoding="utf-8"),
            source_lang,
            target_lang,
            glossary,
            languages,
        )
        if not DRY_RUN:
            out_html.write_text(translated, encoding="utf-8")
        written.append(str(out_html.relative_to(REPO_ROOT)))

    if blog_path and blog_path.exists():
        out_md = topic_dir / f"{slug}-blog{suffix}.md"
        translated = translate_markdown(
            blog_path.read_text(encoding="utf-8"),
            source_lang,
            target_lang,
            glossary,
        )
        if not DRY_RUN:
            out_md.write_text(translated, encoding="utf-8")
        written.append(str(out_md.relative_to(REPO_ROOT)))

    # Update meta.json translation tracking
    if not DRY_RUN and written:
        meta.setdefault("languages", [])
        if target_lang not in meta["languages"]:
            meta["languages"].append(target_lang)
        meta.setdefault("translations", {})
        meta["translations"][target_lang] = {
            "synced_at_version": meta["current_version"],
            "last_translated": time.strftime("%Y-%m-%d"),
            "method": f"auto:{MODEL}",
        }
        # Update title placeholder if still null
        meta.setdefault("title", {})
        if meta["title"].get(target_lang) is None and html_path:
            try:
                title_match = re.search(r"<title>([^<]+)</title>", translated)
                if title_match:
                    meta["title"][target_lang] = title_match.group(1).strip()
            except Exception:
                pass
        save_json(meta_path, meta)

    return written


def main():
    languages = load_json(CONFIG_DIR / "languages.json")
    glossary = load_json(CONFIG_DIR / "glossary.json")

    targets = [l for l in languages["languages"] if l.get("translate_target")]

    all_written = []
    skipped_count = 0

    meta_files = sorted(DEEPDIVE_DIR.rglob("*.meta.json"))
    for meta_path in meta_files:
        for target in targets:
            written = translate_one(meta_path, target["code"], languages, glossary)
            if written:
                all_written.extend(written)
            else:
                skipped_count += 1

    summary = {
        "translated_files": all_written,
        "skipped_count": skipped_count,
        "model": MODEL,
        "dry_run": DRY_RUN,
    }
    # Last line is JSON summary for downstream consumers
    print("---SUMMARY---")
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if all_written or DRY_RUN else 0  # Always 0; absence of work isn't an error


if __name__ == "__main__":
    sys.exit(main())
