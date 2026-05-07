# AI-Buzzwords · Agent Workflow Guide

This file is the operational manual for any Claude Code agent working in this repository. It captures the publishing pipeline, the bilingual translation system, the periodic freshness checker, and all hard-won failure modes from the 2026-05 build-out.

> **First-time setup check**: confirm `gh auth status`, `git remote -v` (should be `github.com/fxp/AI-Buzzwords`), and that you're inside `~/Code/AI-Buzzwords/` (NOT the iCloud vault — git in iCloud breaks).

---

## 1. Two-root architecture

| Role | Path | What lives here |
|---|---|---|
| **Writing source** | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/AI Buzzwords/DeepDive/` | User authoring in Obsidian. Chinese folder names with bracket prefixes (`[L3个体·心理] 白领工作终局/`). |
| **Deploy repo** | `~/Code/AI-Buzzwords/` | Public GitHub repo. Lowercase-hyphen slugs (`labor-day-2026/`). All automation lives here. |

Vault → repo is one-way. When migrating an article from vault to repo:
1. Slug-ify the directory name
2. Fix relative paths via sed (see §6)
3. Create `<slug>.meta.json` (schema in §3)
4. Commit + push — Translation Action auto-fires

---

## 2. Two-target deployment

```
git push origin main
        │
        ▼
.github/workflows/deploy.yml
        │
   ┌────┴────┐
   ▼         ▼
GitHub    Cloudflare
Pages     Worker
   │         │
   ▼         ▼
fxp.github   xiaopingfeng
.io/AI-      .com/blog/
Buzzwords/   ai-buzzwords/
```

Worker (`worker.js`) reverse-proxies `xiaopingfeng.com/blog/ai-buzzwords/<path>` → `fxp.github.io/AI-Buzzwords/<path>`. Same content, two URLs.

**Rule**: every deployment report MUST give the user BOTH URLs (`fxp.github.io/...` + `xiaopingfeng.com/...`).

The Worker also handles `?v=N` query params for historical version routing — see §8.

---

## 3. Per-article assets (mandatory)

Every article requires these files, side-by-side in `deepdive/<topic-dir>/`:

| File | Required? | Purpose |
|---|---|---|
| `<slug>.html` | yes | ZH primary article |
| `<slug>.cn.html` | only for sensitive topics | ZH tactful edition (manual, not auto-translated) |
| `<slug>.en.html` | auto-generated | EN translation |
| `<slug>-blog.md` | optional | ZH blog/social-share version |
| `<slug>-blog.en.md` | auto-generated if blog.md exists | EN blog |
| `<slug>.meta.json` | **mandatory** | Versioning, freshness, language tracking |

For panorama-style articles where the topic dir's `index.html` IS the article (e.g. `labor-day-2026/index.html`), the meta file is `index.meta.json` and `slug` field is the topic name (`labor-day-2026`), NOT "index".

### `<slug>.meta.json` schema

```json
{
  "$schema": "../../config/meta.schema.json",
  "slug": "white-collar",
  "topic_dir": "labor-day-2026",
  "title": {
    "zh": "中文标题",
    "zh-cn": "中文婉转版标题",
    "en": null
  },
  "current_version": 1,
  "first_published": "2026-05-01",
  "last_updated": "2026-05-01",
  "freshness_priority": "warm",
  "next_check": "2026-05-31",
  "languages": ["zh"],
  "primary_language": "zh",
  "translations": {},
  "version_log": [
    {
      "v": 1,
      "date": "2026-05-01",
      "git": "<sha>",
      "summary": "首次发布..."
    }
  ],
  "tags": ["..."],

  "blog_filename": "labor-day-blog.md",
  "html_filename": "alternate.html",
  "is_panorama": true,
  "is_index": true,
  "sensitivity": "high",
  "category": "L3-1 劳动市场 / 个体·心理",
  "related": ["other-slug"]
}
```

Last block is optional fields. `blog_filename` overrides default `<slug>-blog.md` (used when blog naming doesn't match slug — e.g. labor-day-2026 panorama uses `labor-day-blog.md`).

`title.en` should be `null` initially — translation Action fills it from the translated `<title>` tag.

### `freshness_priority` — picks scan frequency

| Priority | Cron interval | When to use |
|---|---|---|
| `hot` | 7 days | Time-sensitive (CEO statements, market data, ongoing events) |
| `warm` | 30 days | Default for technical / industry analysis |
| `cold` | 90 days | Historical, conceptual, biographical |

---

## 4. Bilingual translation system

### Configuration: `config/languages.json`

Schema-driven. Adding a new language (e.g. Japanese) is a one-line config change:

```json
{
  "code": "ja",
  "name": "日本語",
  "html_lang": "ja",
  "filename_suffix": ".ja",
  "hreflang": "ja",
  "translate_target": true,
  "translate_source": "zh"
}
```

After adding, push to main; Translation Action will pick up next push and translate all stale articles to ja.

### Glossary: `config/glossary.json`

Bilingual term library with `do_not_translate` flags. Translation Action injects relevant entries into the LLM system prompt. Manual edits OK — read on every run.

When adding new terminology that recurs across articles, add it to glossary BEFORE the next translate run for consistency.

### Translation Action: `.github/workflows/translate.yml`

**Triggers**:
- Push to `main` matching `deepdive/**/*.html`, `**/*-blog.md`, `**/*.meta.json`, `config/glossary.json`, `config/languages.json`, or the workflow file itself
- Manual dispatch with optional `slug` (single article) and `provider` (bigmodel|anthropic) inputs
- Skip-loop guard: commits with `[auto-translate]` in message do not re-trigger

**Behavior**:
- For each `<slug>.meta.json` where `meta.translations[lang].synced_at_version < meta.current_version` (or missing):
  1. Translate `<slug>.html` via `scripts/translate.py`
  2. Translate `<slug>-blog.md` if it exists (or per `blog_filename` override)
  3. Update meta.json's `translations[lang]` entry
  4. Commit batch with `[auto-translate]` tag
  5. Pull --rebase if push fails (handles concurrent runs)
- Slack notification to `#deepdive` (success / no-op / failure)

### Manual dispatch examples

```bash
# Translate one article via default GLM-5.1
gh workflow run translate.yml -f slug=white-collar

# Force Anthropic Claude (for content-filter or oversize cases)
gh workflow run translate.yml -f slug=labor-day-2026 -f provider=anthropic

# Re-run all (no slug = all stale articles)
gh workflow run translate.yml
```

### Provider switch

| Provider | Default model | Strengths | Weaknesses |
|---|---|---|---|
| `bigmodel` (default) | `glm-5.1` | Cheap, fast, good ZH↔EN | **Content filter blocks sensitive topics**; **server times out at ~5min for >50KB HTMLs** |
| `anthropic` (fallback) | `claude-sonnet-4-6` | No content filter, handles 200K context, stable on big inputs | Higher per-call cost |

**Decision rule**: try `bigmodel` first. If it fails with `HTTP 400 contentFilter` or `Remote end closed connection without response`, retry with `provider=anthropic`. Both edge cases observed in production:
- `labor-day-2026` (panorama): GLM content filter triggered on AI×labor terminology
- `white-collar.html` (73KB): GLM server-side 5-min internal timeout

---

## 5. Freshness check system

### `.github/workflows/freshness-check.yml`

**Triggers**:
- Cron `0 9 * * 1` (Monday 09:00 UTC = 17:00 Beijing)
- Manual dispatch with `force_all`, `slug`, `provider` inputs

**Behavior**:
- For each meta.json where `next_check ≤ today` (or `force_all=true`):
  1. **Rule-based checks**: HEAD-request all external `href` URLs (flag 4xx/5xx); extract dates ≥6 months old; extract `X 年内` / `in X years` predictions
  2. **LLM staleness review**: send article + metadata to `UPDATE_AGENT_PROVIDER` (default: `anthropic`/Claude Sonnet 4.6, configurable to bigmodel/openai) for "what claims are likely stale"
  3. Write `_freshness/<topic>/<slug>-<date>.md` report
  4. Open GitHub Issue with severity-tagged checklist
  5. Roll forward `meta.next_check` per priority schedule
- Slack `#deepdive` summary

### Manual freshness check

```bash
gh workflow run freshness-check.yml \
  -f force_all=true \
  -f slug=white-collar \
  -f provider=anthropic
```

### Severity grading in reports

- 🔴 critical (broken link, data clearly outdated)
- 🟡 worth-updating
- 🟢 informational
- ❓ uncertain — needs human verification

---

## 6. Path-fix templates (vault → repo migration)

Vault articles use Chinese folder paths in href. Before deploying to repo:

```bash
# Dimension map back-link
sed -i '' 's|href="\.\./index\.html"|href="dimension-map.html"|g' deployed.html

# Panorama (sibling)
sed -i '' 's|href="\.\./%5B%E5%85%A8%E6%99%AF%5D[^"]*labor-day-2026-neo\.html"|href="index.html"|g' deployed.html

# RentAHuman sibling
sed -i '' 's|href="\.\./\.\./%5BNEWJOB%5D[^"]*\.html"|href="rentahuman.html"|g' deployed.html
```

Verify with: `grep -oE 'href="[^h"][^"]*"' <file> | sort -u` — every internal link should be a sibling relative path.

---

## 7. Lang-switcher injection

`scripts/inject_lang_switcher.py` is idempotent — run after a translation lands to wire up:
- `<script src=".../lang-switcher.js" defer>` in `<head>`
- `<link rel="alternate" hreflang="...">` tags for each available language + `x-default`
- `<div data-lang-switcher data-slug="...">` in the top strip
- `<html lang="...">` updated per file

```bash
python3 scripts/inject_lang_switcher.py --dry-run   # preview
python3 scripts/inject_lang_switcher.py             # apply
```

The switcher reads `meta.json.languages` at runtime, so:
- Articles with only `["zh"]` → switcher hidden
- Articles with `["zh", "en"]` → ZH/EN buttons appear
- Articles with `["zh", "zh-cn", "en"]` → ZH/EN buttons + separate "中文婉转版" pill

---

## 8. Historical version access (`?v=N`)

URL pattern: `https://xiaopingfeng.com/blog/ai-buzzwords/<path>.html?v=N`

`worker.js` flow:
1. Parse `?v=N` from query
2. Fetch `<slug>.meta.json` from current main
3. Look up `version_log[v=N].git_sha`
4. Fetch from `raw.githubusercontent.com` at that sha
5. Inject banner: "📜 您正在查看历史版本 vN · date · summary · [返回当前]"

Falls back to current version + warning banner if v=N not in version_log.

GitHub Pages does NOT support this — only xiaopingfeng.com (Worker) does.

---

## 9. Common failure modes (resolved, but watch for)

### `HTTP 422 Workflow does not have 'workflow_dispatch' trigger`
GitHub hasn't registered the workflow yet. Wait 15s after a push that adds/modifies the workflow file before dispatching.

### `! [rejected] main -> main (non-fast-forward)`
Two translate runs racing — second has stale checkout. Fixed in `translate.yml` with retry-with-rebase loop. If the workflow lacks this fix, push it first before dispatching anything else.

### `HTTP 400 contentFilter` (BigModel)
Switch provider to `anthropic` for that article. Common on labor/political/safety topics.

### `Remote end closed connection without response` (BigModel)
GLM internal 5-min timeout on large HTMLs. Switch provider to `anthropic`. Threshold: ~50KB starts being risky; >70KB almost guaranteed to fail.

### Concurrent dispatches: only 1 pending allowed
Concurrency group `translate-${{ github.ref }}` with `cancel-in-progress: false`. If you queue multiple `gh workflow run` calls in quick succession, the middle ones get cancelled — only first (in_progress) and most recent (pending) survive.

**Use `/tmp/translate-sequential.sh` (or write a similar loop)** to dispatch + wait for each before next.

### Long-running workflow watch
`gh run watch` and Bash 2-min timeout: poll via Monitor tool with `until [ ... = completed ]; do sleep 30; done` pattern. Don't use foreground sleep loops.

### `nothing to commit but untracked files present`
The commit step previously failed when `summary.json` / `translate.log` were untracked but no deepdive/ changes existed. Fixed by `git status --porcelain deepdive/` filter. If you change the commit logic, preserve this filter.

---

## 10. Required GitHub Secrets

Configure at https://github.com/fxp/AI-Buzzwords/settings/secrets/actions:

| Name | Used by | Notes |
|---|---|---|
| `BIGMODEL_API_KEY` | translate.yml (default GLM-5.1) | From open.bigmodel.cn |
| `ANTHROPIC_API_KEY` | translate.yml (provider=anthropic) + freshness-check.yml (default Claude) | |
| `OPENAI_API_KEY` | freshness-check.yml (provider=openai) | Optional |
| `SLACK_WEBHOOK_URL` | translate.yml + freshness-check.yml | Incoming webhook to `#deepdive` |
| `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` | deploy.yml | For Worker deployment |

---

## 11. New article publishing checklist

```bash
# In ~/Code/AI-Buzzwords/

# 1. Stage article + meta + (optional) blog markdown
git add deepdive/<topic>/<slug>.html deepdive/<topic>/<slug>.meta.json
git add deepdive/<topic>/<slug>-blog.md  # if exists

# 2. Sanity-check
grep -rnE 'href="https?://[^/]+/?"' deepdive/<topic>/   # bare-domain refs
grep -rni -E 'zhipu|智谱|glm|z\.ai' deepdive/<topic>/   # signature contamination
grep -oE 'href="[^h"][^"]*"' deepdive/<topic>/*.html | sort -u   # internal link audit

# 3. Commit + push
git commit -m "Add deepdive article: <topic>/<slug>"
git push origin main

# 4. Watch translation:
gh run watch  # auto-translate fires within seconds
# Or for big/sensitive articles, dispatch directly with anthropic:
# gh workflow run translate.yml -f slug=<slug> -f provider=anthropic

# 5. After translation lands:
git pull
python3 scripts/inject_lang_switcher.py
git add deepdive/ && git commit -m "Inject lang-switcher for <slug>" && git push

# 6. Verify both URLs:
echo "https://fxp.github.io/AI-Buzzwords/deepdive/<topic>/<slug>.html"
echo "https://xiaopingfeng.com/blog/ai-buzzwords/deepdive/<topic>/<slug>.html"
```

---

## 12. Naming + content rules

- **No emoji in author signature** (always — see `feedback_no_zhipu.md` in user memory)
- **No `zhipu`/`智谱`/`GLM`/`Z.ai` in author/出品/编辑 lines** (the API itself is OK; just not bylines)
- **Citations must have `<a href>` to original source** (no bare domains like `wsj.com/`)
- **Each article has inline TL;DR block** in HTML (after hero, before §01) — but **no separate `*-tldr.md` file** (deprecated 2026-05)
- **Tactful CN edition** (`*.cn.html`) only for politically/socially sensitive topics — use restrained language, link back to original direct version
- **Article titles in `<title>` tag**: ZH original tag stays Chinese; EN translation puts EN title in tag

See related memory files:
- `feedback_cite_links.md` — citation rules
- `feedback_tactful_edition.md` — CN edition writing guidelines
- `feedback_tldr.md` — TL;DR placement
- `feedback_bilingual.md` — bilingual mandates
- `feedback_no_zhipu.md` — signature contamination check

---

## 13. Article template + style normalization (added 2026-05-07)

Every published article shares a unified chrome — top strip + theme tokens
+ lang-switcher placement. Bespoke hero / sections / footers stay per-article.

### Template files

| File | Purpose |
|---|---|
| `templates/article.html` | Golden template with `{{PLACEHOLDERS}}`. Use as starting point for new articles. |
| `templates/_strip.html` | Drop-in TOP STRIP component (single-row Pattern A). |
| `config/themes.json` | Per-article accent + topic label + version label + nav pill. Edit when adding new article. |

### Theme palette (4 colors only)

| Token | Hex | Use for |
|---|---|---|
| `red` | `#e84040` | Alarming/urgent (labor, military, leaks) |
| `signal` | `#d1402c` | Alarming variant |
| `amber` | `#f5a524` | Analytical/historical (Cybertonia, NeoLab, Palantir) |
| `mint` | `#7fb88b` | Research/discovery (Emotion Vectors, Project DEAL, Buddy) |

Each article picks ONE accent. The body gets `data-theme="<accent>"` and a
`<style id="theme-vars">:root{--accent:...}</style>` block in `<head>`.

**Full reference**:
- Visual showcase (interactive theme + light/dark switcher): [`design-system.html`](https://fxp.github.io/AI-Buzzwords/design-system.html)
- Token spec: [`DESIGN.md`](DESIGN.md) · markdown showcase: [`DESIGN-SHOWCASE.md`](DESIGN-SHOWCASE.md)
- **Canonical token CSS**: [`colors_and_type.css`](colors_and_type.css) — link this in new articles instead of inlining tailwind.config
- **Component CSS**: [`kit.css`](kit.css) — `.dd-strip`, `.dd-section`, `.dd-hero`, `.dd-pullquote` etc.
- **Light/dark toggle**: [`mode-toggle.js`](mode-toggle.js) — drop into `<head>` + `<button data-toggle-mode>...</button>` in strip

When generating a new article: **read `DESIGN.md` first**. v2 (May 2026) adds:
- **Light mode** parchment palette via `<html data-mode="light">` (deepened accents for AA contrast on cream)
- **Full CJK fallback chain** (Noto Serif SC/TC/JP/KR auto-switching per `:lang()`)
- **Hard CJK no-italic enforcement** (`font-synthesis-style: none`)
- **EB Garamond** as Latin body serif (real italics reserved for `<cite lang="en">`)
- **Spacing scale tokens** (`--s-0..9`)

### Normalize existing article (replace strip + apply theme)

```bash
python3 scripts/normalize_strip.py --dry-run             # preview all
python3 scripts/normalize_strip.py --slug <slug> --dry-run
python3 scripts/normalize_strip.py                        # apply all
```

The script:
1. Finds the existing TOP STRIP block (works on Pattern A and Pattern B
   layouts, balances `<div>` nesting properly)
2. Replaces with standardized strip rendered from `templates/_strip.html` +
   `config/themes.json`
3. Removes any stray `<div data-lang-switcher>` placed outside the strip
   (the broken Phase-1 injection)
4. Adds `data-theme="..."` to `<body>`
5. Injects `:root{--accent:...}` CSS variables

Idempotent — re-running on already-normalized files is a no-op.

### Articles excluded from normalize

`SKIP_SLUGS` in `normalize_strip.py` lists articles whose custom CSS would
break with the standardized strip. Currently: `dimension-map` (uses pure
custom CSS, no Tailwind config block).

### Adding a new article — full sequence

```bash
# 1. Author or migrate ZH HTML to deepdive/<topic>/<slug>.html
# 2. Add entry to config/themes.json under "articles"
# 3. Create deepdive/<topic>/<slug>.meta.json (see §3)
# 4. Run normalizer to apply standard strip
python3 scripts/normalize_strip.py --slug <slug>
# 5. Translation + lang-switcher injection happens via Action on push
git add deepdive/<topic>/ config/themes.json
git commit -m "Add article: <slug>" && git push
```

---

## 14. Project structure quick reference

```
~/Code/AI-Buzzwords/
├── CLAUDE.md                     # this file
├── README.md
├── index.html                    # site landing page
├── viewer.html                   # universal markdown viewer (.md → MD via ?f=path)
├── lang-switcher.js              # client-side language switcher
├── worker.js                     # Cloudflare Worker (xiaopingfeng.com proxy + ?v=N history)
├── wrangler.toml                 # Worker config
├── config/
│   ├── languages.json            # multilingual registry
│   ├── glossary.json             # ZH/EN term library
│   └── themes.json               # per-article accent + topic label registry
├── templates/
│   ├── article.html              # golden article template
│   └── _strip.html               # drop-in TOP STRIP component
├── scripts/
│   ├── translate.py              # GLM-5.1 / Claude translation
│   ├── freshness_check.py        # weekly content scan
│   ├── inject_lang_switcher.py   # post-translation switcher injection
│   ├── normalize_strip.py        # unify TOP STRIP across articles
│   ├── llm_client.py             # provider-agnostic LLM caller
│   ├── notify_slack.py           # webhook posting
│   └── publish-md.sh             # legacy md publish helper
├── .github/workflows/
│   ├── deploy.yml                # GitHub Pages + Cloudflare Worker deploy
│   ├── translate.yml             # bilingual translation
│   └── freshness-check.yml       # weekly content review
├── deepdive/
│   └── <topic>/
│       ├── <slug>.html
│       ├── <slug>.cn.html        # optional, sensitive topics
│       ├── <slug>.en.html        # auto-translated
│       ├── <slug>-blog.md
│       ├── <slug>-blog.en.md
│       └── <slug>.meta.json
└── _freshness/                   # archived freshness reports (generated)
    └── <topic>/<slug>-<date>.md
```

---

## 15. Authoring philosophy reminder

This isn't a generic blog. The user maintains opinionated, deeply researched articles on AI/labor/policy topics. When asked to extend, refactor, or add to an article:

- **Verify all data points and links** before adding (use WebSearch/WebFetch)
- **Add context, not noise** — every section earns its place
- **Counter-evidence is a feature** — if you can find someone who disagrees, include them; the article is stronger
- **Track every assertion to a primary source** — no "according to reports"
- **Layer information density**: TL;DR (30s) → blog md (3-5min) → full HTML (10-15min)
- **Tactful CN edition is for sensitive geopolitical topics** — soften assertions, neutralize attribution, but do not erase analysis

When in doubt about scope or quality, the user prefers fewer well-built things over many half-built things. Confirm before significantly expanding scope.
