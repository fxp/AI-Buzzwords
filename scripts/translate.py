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

PROVIDER = os.environ.get("TRANSLATE_PROVIDER", "bigmodel").lower()
DRY_RUN = os.environ.get("TRANSLATE_DRY_RUN", "").lower() == "true"
FORCE_SLUG = os.environ.get("TRANSLATE_FORCE_SLUG", "")

# Provider-specific config
if PROVIDER == "anthropic":
    API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    API_ENDPOINT = os.environ.get(
        "ANTHROPIC_API_ENDPOINT", "https://api.anthropic.com/v1/messages"
    )
    MODEL = os.environ.get("TRANSLATE_MODEL", "claude-sonnet-4-6")
else:
    # bigmodel (GLM) — default
    API_KEY = os.environ.get("BIGMODEL_API_KEY", "")
    API_ENDPOINT = os.environ.get(
        "BIGMODEL_API_ENDPOINT",
        "https://api.z.ai/api/paas/v4/chat/completions",
    )
    MODEL = os.environ.get("TRANSLATE_MODEL") or os.environ.get("BIGMODEL_MODEL", "glm-5.1")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def call_glm(messages, max_retries=2, max_tokens=16000):
    """Call configured LLM provider (BigModel GLM or Anthropic Claude)."""
    if DRY_RUN:
        return "[DRY RUN — no API call]"
    if not API_KEY:
        raise RuntimeError(f"API key for provider '{PROVIDER}' not set")

    if PROVIDER == "anthropic":
        # Anthropic Messages API: separate system from messages, different headers
        system_content = ""
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system_content = m["content"]
            else:
                user_messages.append(m)
        payload = {
            "model": MODEL,
            "max_tokens": max_tokens,
            "system": system_content,
            "messages": user_messages,
        }
        headers = {
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
    else:
        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": max_tokens,
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
    body = json.dumps(payload).encode("utf-8")

    last_err = None
    for attempt in range(max_retries):
        t0 = time.time()
        try:
            req = urllib.request.Request(
                API_ENDPOINT, data=body, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=900) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - t0
            print(f"[llm/{PROVIDER}]  ok in {elapsed:.1f}s ({MODEL})", file=sys.stderr)
            if PROVIDER == "anthropic":
                # content is a list of blocks; first text block is the answer
                for block in data.get("content", []):
                    if block.get("type") == "text":
                        return block.get("text", "")
                return ""
            return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")[:500]
            last_err = f"HTTP {e.code}: {err_body}"
            print(f"[llm/{PROVIDER}] attempt {attempt+1} HTTP {e.code}: {err_body[:200]}", file=sys.stderr)
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = str(e)
            print(f"[llm/{PROVIDER}] attempt {attempt+1} error: {last_err[:200]}", file=sys.stderr)
            time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM call failed after {max_retries}: {last_err}")


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

    raw = call_glm(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=20000,
    )
    return clean_html_output(raw)


def clean_html_output(s: str) -> str:
    """Strip markdown code fences if GLM wrapped output."""
    s = s.strip()
    # Strip leading ```html or ```
    if s.startswith("```"):
        first_nl = s.find("\n")
        if first_nl != -1:
            s = s[first_nl + 1:]
    if s.endswith("```"):
        s = s[:-3].rstrip()
    return s


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
    raw = call_glm(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this {source_lang} markdown to {target_lang}:\n\n{md}"},
        ],
        max_tokens=8000,
    )
    return clean_markdown_output(raw)


def clean_markdown_output(s: str) -> str:
    """Markdown is the natural format — but GLM might wrap with ```markdown."""
    s = s.strip()
    if s.startswith("```markdown"):
        s = s[len("```markdown"):].lstrip("\n")
        if s.endswith("```"):
            s = s[:-3].rstrip()
    elif s.startswith("```"):
        first_nl = s.find("\n")
        if first_nl != -1:
            head = s[:first_nl].strip()
            # Only strip if it's actually a fence (no spaces)
            if head == "```" or head.startswith("```"):
                s = s[first_nl + 1:]
                if s.endswith("```"):
                    s = s[:-3].rstrip()
    return s


def needs_translation(meta: dict, target_lang: str) -> bool:
    """Returns True if target_lang is missing or stale."""
    if target_lang not in meta.get("languages", []):
        return True
    sync = meta.get("translations", {}).get(target_lang, {})
    synced_v = sync.get("synced_at_version", 0)
    return synced_v < meta["current_version"]


def find_source_files(meta_path: Path, meta: dict = None):
    """Given meta.json path, find source HTML + optional blog.md.
    Honors meta.blog_filename override (e.g. for labor-day-2026 panorama
    where slug=index but blog file is labor-day-blog.md)."""
    slug = meta_path.stem.replace(".meta", "")
    topic_dir = meta_path.parent
    html_name = (meta or {}).get("html_filename") or f"{slug}.html"
    blog_name = (meta or {}).get("blog_filename") or f"{slug}-blog.md"
    html = topic_dir / html_name
    blog_md = topic_dir / blog_name
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
    slug, topic_dir, html_path, blog_path = find_source_files(meta_path, meta)

    target_lang_obj = next(
        (l for l in languages["languages"] if l["code"] == target_lang), None
    )
    if not target_lang_obj:
        return []
    suffix = target_lang_obj.get("filename_suffix", f".{target_lang}")

    written = []
    print(f"[translate] {slug} → {target_lang}", file=sys.stderr)

    if html_path and html_path.exists():
        # Output filename: derive by inserting suffix before .html
        out_html_name = html_path.stem + suffix + html_path.suffix
        out_html = topic_dir / out_html_name
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
        out_md_name = blog_path.stem + suffix + blog_path.suffix
        out_md = topic_dir / out_md_name
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
    errors = []
    skipped_count = 0

    meta_files = sorted(DEEPDIVE_DIR.rglob("*.meta.json"))
    print(f"[main] Found {len(meta_files)} articles, {len(targets)} target languages", file=sys.stderr)

    for meta_path in meta_files:
        for target in targets:
            try:
                written = translate_one(meta_path, target["code"], languages, glossary)
                if written:
                    all_written.extend(written)
                else:
                    skipped_count += 1
            except Exception as e:
                slug = meta_path.stem.replace(".meta", "")
                err_msg = f"{slug} → {target['code']}: {str(e)[:300]}"
                errors.append(err_msg)
                print(f"[main] ERROR {err_msg}", file=sys.stderr)
                # Continue with next article — one failure doesn't kill the batch

    summary = {
        "translated_files": all_written,
        "skipped_count": skipped_count,
        "errors": errors,
        "provider": PROVIDER,
        "model": MODEL,
        "dry_run": DRY_RUN,
    }
    print("---SUMMARY---")
    print(json.dumps(summary, ensure_ascii=False))
    # Exit non-zero only if EVERYTHING failed
    return 0 if all_written or DRY_RUN or skipped_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
