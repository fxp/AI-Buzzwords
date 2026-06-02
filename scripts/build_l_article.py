#!/usr/bin/env python3
"""
Build a Design System v2 HTML page from an L-level article.md.

Usage:
  python3 scripts/build_l_article.py <slug> <theme> "<title>" "<dek>"

Reads:    deepdive/labor-day-2026/<slug>/article.md
Writes:   deepdive/labor-day-2026/<slug>.html         (ZH)
Also writes meta.json if missing.

Design pattern (mirrors white-collar.html / rentahuman.html lineage):
  - <html data-theme="<theme>"> with red/signal/amber/mint accents
  - colors_and_type.css + kit.css cascade (Design System v2)
  - Tailwind CDN with var(--*) color tokens so light/dark mode flips live
  - Standard TOP STRIP (lang-switcher + mode-toggle + nav back to index)
  - Hero with breadcrumb, title, dek
  - Article body rendered from markdown with serif type
  - Footer with parent-article link

Themes:
  - red    = crisis / disruption  (white-collar uses this)
  - signal = warning / orange    (blue-collar fits)
  - amber  = policy / synthesis  (beyond-ubi fits)
  - mint   = ecology / research  (default)
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import markdown

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPIC_DIR = REPO_ROOT / "deepdive" / "labor-day-2026"

THEME_VARS = {
    "red":    {"accent": "#e84040", "soft": "rgba(232,64,64,0.10)",  "glow": "rgba(232,64,64,0.30)"},
    "signal": {"accent": "#f5663f", "soft": "rgba(245,102,63,0.10)", "glow": "rgba(245,102,63,0.30)"},
    "amber":  {"accent": "#c4850a", "soft": "rgba(196,133,10,0.10)", "glow": "rgba(196,133,10,0.30)"},
    "mint":   {"accent": "#7fb88b", "soft": "rgba(127,184,139,0.12)","glow": "rgba(127,184,139,0.30)"},
}


def md_to_html(md_text: str) -> str:
    """Convert markdown to HTML with extras enabled."""
    return markdown.markdown(
        md_text,
        extensions=["extra", "tables", "sane_lists", "smarty"],
        output_format="html5",
    )


def render_html(slug: str, theme: str, title: str, dek: str, body_html: str,
                level_label: str, axis_label: str) -> str:
    """Wrap rendered body into the full Design System v2 page shell."""
    palette = THEME_VARS[theme]
    accent = palette["accent"]
    glow = palette["glow"]
    soft = palette["soft"]

    return f"""<!DOCTYPE html>
<html lang="zh" data-theme="{theme}">
<head>
<style id="theme-vars">:root{{--accent:{accent};--accent-glow:{glow};--accent-soft:{soft};}}</style>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} — {level_label} · {axis_label}</title>
<meta name="description" content="{dek}" />
<!-- Design System v2: canonical token CSS -->
<link rel="stylesheet" href="../../colors_and_type.css">
<link rel="stylesheet" href="../../kit.css">
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,700&family=JetBrains+Mono:wght@300;400;500;700&display=swap" rel="stylesheet" />
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{
  theme: {{
    extend: {{
      colors: {{
        bg:           'var(--bg)',
        'bg-2':       'var(--bg-2)',
        'bg-3':       'var(--bg-3)',
        fg:           'var(--fg)',
        'fg-dim':     'var(--fg-dim)',
        'fg-mute':    'var(--fg-mute)',
        line:         'var(--line)',
        'line-bright':'var(--line-bright)',
        accent:       'var(--accent)',
        'accent-soft':'var(--accent-soft)',
      }},
      fontFamily: {{
        serif: ["'Fraunces'", "'Source Han Serif SC'", "Georgia", "serif"],
        mono:  ["'JetBrains Mono'", "ui-monospace", "monospace"],
      }},
      maxWidth: {{
        prose:   '820px',
        content: '1020px',
        wrap:    '1320px',
      }},
    }}
  }}
}}
</script>
<style>
em, i {{ font-style: normal }}
body {{ font-feature-settings: 'ss01','ss02','kern'; -webkit-font-smoothing: antialiased }}
body::before {{
  content: ''; position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(240,235,224,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(240,235,224,0.025) 1px, transparent 1px);
  background-size: 60px 60px; pointer-events: none; z-index: 0;
}}
.lamp {{ display: inline-block; width: 6px; height: 6px; border-radius: 50%;
  background: {accent}; box-shadow: 0 0 8px {accent}, 0 0 20px {glow};
  animation: pulse 2.4s ease-in-out infinite; vertical-align: middle; }}
@keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.4}} }}
@keyframes fadeUp {{ from {{ opacity:0; transform:translateY(18px) }} to {{ opacity:1; transform:translateY(0) }} }}
.hero-anim > * {{ animation: fadeUp 0.7s ease both; }}
.hero-anim > *:nth-child(1) {{ animation-delay: 0.05s }}
.hero-anim > *:nth-child(2) {{ animation-delay: 0.15s }}
.hero-anim > *:nth-child(3) {{ animation-delay: 0.25s }}
.hero-anim > *:nth-child(4) {{ animation-delay: 0.35s }}
/* Article body styling */
.article-body {{ font-family: 'Fraunces', 'Source Han Serif SC', Georgia, serif; font-size: 17px; line-height: 1.85; color: var(--fg); }}
.article-body p {{ margin: 0 0 22px; font-weight: 400; }}
.article-body p strong {{ color: var(--fg); font-weight: 500; }}
.article-body p em {{ color: var(--accent); font-style: normal; font-weight: 400; }}
.article-body h2 {{ font-family: 'Fraunces', serif; font-size: 30px; font-weight: 300; letter-spacing: -0.01em; margin: 72px 0 24px; color: var(--fg); border-bottom: 1px solid var(--line); padding-bottom: 14px; }}
.article-body h3 {{ font-family: 'Fraunces', serif; font-size: 22px; font-weight: 400; margin: 48px 0 16px; color: var(--fg); }}
.article-body h4 {{ font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin: 36px 0 12px; }}
.article-body a {{ color: inherit; text-decoration: underline; text-decoration-style: dotted; text-underline-offset: 3px; text-decoration-color: {accent}59; transition: color 0.15s; }}
.article-body a:hover {{ color: var(--accent); }}
.article-body ul, .article-body ol {{ margin: 0 0 22px; padding-left: 24px; }}
.article-body li {{ margin: 8px 0; }}
.article-body blockquote {{ margin: 24px 0; padding: 8px 0 8px 22px; border-left: 3px solid var(--accent); color: var(--fg-dim); font-style: normal; }}
.article-body blockquote strong {{ color: var(--fg); }}
.article-body hr {{ border: 0; border-top: 1px solid var(--line); margin: 56px 0; }}
.article-body table {{ border-collapse: collapse; width: 100%; margin: 24px 0; font-family: 'JetBrains Mono', monospace; font-size: 13px; }}
.article-body th, .article-body td {{ padding: 10px 14px; border: 1px solid var(--line); text-align: left; vertical-align: top; }}
.article-body th {{ background: var(--bg-2); color: var(--fg-mute); font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; font-size: 11px; }}
.article-body code {{ font-family: 'JetBrains Mono', monospace; font-size: 0.88em; background: var(--bg-2); padding: 2px 6px; border-radius: 2px; }}
</style>

<script src="../../lang-switcher.js" defer></script>
<script src="../../mode-toggle.js" defer></script>
<link rel="alternate" hreflang="zh" href="{slug}.html" />
<link rel="alternate" hreflang="en" href="{slug}.en.html" />
<link rel="alternate" hreflang="x-default" href="{slug}.html" />
</head>

<body class="bg-bg text-fg font-sans" style="font-family: 'JetBrains Mono', 'Source Han Sans SC', sans-serif">

<!-- ═══════════════════ TOP STRIP ═══════════════════ -->
<header class="relative z-[3] border-b border-line bg-bg">
  <div class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-3 flex items-center gap-4 lg:gap-6 text-[10px] lg:text-[11px] font-mono tracking-[0.18em] uppercase">
    <div class="flex items-center gap-2 text-fg-mute">
      <span class="lamp"></span>
      <span class="text-fg">DEEPDIVE</span>
      <span class="text-fg-mute hidden lg:inline">/ AI × 就业</span>
    </div>
    <div class="text-fg-mute hidden lg:block">{level_label} · {axis_label}</div>
    <div class="ml-auto flex items-center gap-3 lg:gap-5">
      <a href="dimension-map.html" class="text-fg-mute hover:text-accent transition-colors hidden md:inline">维度地图</a>
      <a href="index.html" class="text-fg-mute hover:text-accent transition-colors">← 返回全景</a>
      <div data-lang-switcher data-slug="{slug}"></div>
      <button data-toggle-mode aria-pressed="false"
        class="font-mono text-[9px] lg:text-[10px] tracking-[0.18em] uppercase text-fg-mute hover:text-accent border border-line-bright px-2 py-0.5 transition-colors"
        style="background:transparent;cursor:pointer"
        data-label-light="浅色" data-label-dark="暗色">
        <span data-mode-icon>◐</span> <span data-mode-label>暗色</span>
      </button>
    </div>
  </div>
</header>

<!-- ═══════════════════ HERO ═══════════════════ -->
<section class="relative z-[2] border-b border-line">
  <div class="max-w-content mx-auto px-[5vw] lg:px-12 pt-16 lg:pt-24 pb-12 lg:pb-16 hero-anim">
    <div class="font-mono text-[10px] tracking-[0.22em] uppercase text-accent mb-6">{level_label} · {axis_label}</div>
    <h1 class="font-serif text-[34px] lg:text-[54px] font-light leading-[1.15] tracking-[-0.01em] text-fg mb-7" style="text-wrap:balance">
      {title}
    </h1>
    <p class="font-serif text-[18px] lg:text-[21px] font-light leading-[1.55] text-fg-dim max-w-[760px]" style="text-wrap:pretty">
      {dek}
    </p>
    <div class="font-mono text-[10px] tracking-[0.16em] uppercase text-fg-mute mt-8 flex flex-wrap items-center gap-x-5 gap-y-2">
      <span>2026 五一劳动 vs AI 系列</span>
      <span class="text-line-bright">/</span>
      <span>2026-06-03 更新</span>
      <span class="text-line-bright">/</span>
      <span>冯小平 + Claude (Opus 4.7)</span>
    </div>
  </div>
</section>

<!-- ═══════════════════ ARTICLE BODY ═══════════════════ -->
<main class="relative z-[2]">
  <article class="max-w-prose mx-auto px-[5vw] lg:px-12 py-16 lg:py-24 article-body">
{body_html}
  </article>
</main>

<!-- ═══════════════════ SERIES NAV ═══════════════════ -->
<section class="relative z-[2] border-t border-line bg-bg-2">
  <div class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-10 lg:py-14">
    <div class="font-mono text-[9px] lg:text-[10px] tracking-[0.2em] uppercase text-fg-mute mb-6">同系列 / 五一劳动 × AI</div>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-px bg-line border border-line">
      <a href="index.html" class="bg-bg p-5 hover:bg-bg-3 transition-colors block">
        <div class="font-mono text-[9px] tracking-[0.16em] uppercase text-fg-mute mb-2">全景 ←</div>
        <div class="font-serif text-base lg:text-xl font-light leading-snug text-fg">劳动的终局，还是转型的前夜？</div>
        <div class="font-mono text-[10px] text-fg-mute mt-3">2026 五一劳动 vs AI 全景</div>
      </a>
      <a href="dimension-map.html" class="bg-bg p-5 hover:bg-bg-3 transition-colors block">
        <div class="font-mono text-[9px] tracking-[0.16em] uppercase text-fg-mute mb-2">导航 ↓</div>
        <div class="font-serif text-base lg:text-xl font-light leading-snug text-fg">15 维度地图</div>
        <div class="font-mono text-[10px] text-fg-mute mt-3">L1 个体 → L5 全球 × 3 轴</div>
      </a>
      <a href="white-collar.html" class="bg-bg p-5 hover:bg-bg-3 transition-colors block">
        <div class="font-mono text-[9px] tracking-[0.16em] uppercase text-fg-mute mb-2">L3 个体·心理 →</div>
        <div class="font-serif text-base lg:text-xl font-light leading-snug text-fg">白领初级岗的终局加速</div>
        <div class="font-mono text-[10px] text-fg-mute mt-3">入职门槛抬高的结构性逻辑</div>
      </a>
    </div>
  </div>
</section>

<!-- ═══════════════════ FOOTER ═══════════════════ -->
<footer class="relative z-[2] border-t border-line">
  <div class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-10 text-[11px] lg:text-[12px] font-mono tracking-[0.12em] uppercase text-fg-mute flex flex-wrap items-center gap-x-6 gap-y-2">
    <span>© 2026 冯小平 · xiaopingfeng.com</span>
    <span class="text-line-bright">/</span>
    <a href="/" class="hover:text-accent transition-colors">DeepDive</a>
    <a href="/blog/ai-buzzwords/" class="hover:text-accent transition-colors">AI Buzzwords</a>
    <span class="ml-auto">设计 v2 · {theme} 主题</span>
  </div>
</footer>

</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="article slug (subdir name under labor-day-2026/)")
    ap.add_argument("theme", choices=THEME_VARS.keys())
    ap.add_argument("title")
    ap.add_argument("dek")
    ap.add_argument("--level", default="L3", help="L1-L5 level label")
    ap.add_argument("--axis", default="个体 · 心理", help="axis label, e.g. '个体 · 心理'")
    args = ap.parse_args()

    article_md = TOPIC_DIR / args.slug / "article.md"
    if not article_md.exists():
        print(f"ERROR: {article_md} not found", file=sys.stderr)
        sys.exit(1)

    md_text = article_md.read_text(encoding="utf-8")
    # Strip the title line if it matches title arg (h1) to avoid duplicate
    md_lines = md_text.split("\n", 2)
    if md_lines and md_lines[0].strip().startswith("# "):
        md_text = md_lines[2] if len(md_lines) > 2 else ""

    body_html = md_to_html(md_text)

    full_html = render_html(
        slug=args.slug,
        theme=args.theme,
        title=args.title,
        dek=args.dek,
        body_html=body_html,
        level_label=args.level,
        axis_label=args.axis,
    )

    # Output filename: slug as folder, then slug.html sitting in topic dir
    # We use the convention: deepdive/labor-day-2026/<slug>.html
    output_path = TOPIC_DIR / f"{args.slug}.html"
    output_path.write_text(full_html, encoding="utf-8")
    print(f"Wrote {output_path.relative_to(REPO_ROOT)}")

    # Create meta.json if missing
    meta_path = TOPIC_DIR / f"{args.slug}.meta.json"
    if not meta_path.exists():
        today = date.today().isoformat()
        meta = {
            "$schema": "../../config/meta.schema.json",
            "slug": args.slug,
            "topic_dir": "labor-day-2026",
            "title": {"zh": args.title, "en": None},
            "current_version": 1,
            "first_published": today,
            "last_updated": today,
            "freshness_priority": "warm",
            "next_check": today,
            "languages": ["zh", "en"],
            "primary_language": "zh",
            "translations": {},
            "manual_only": False,
            "author": "冯小平 + Claude (Opus 4.7)",
            "version_log": [
                {
                    "v": 1,
                    "date": today,
                    "git": "PENDING",
                    "summary": f"首次发布：{args.title}（{args.level} · {args.axis}）",
                }
            ],
            "tags": ["LABOR-DAY-2026", args.level, args.axis.replace(" ", "")],
            "category": f"LABOR · AI×就业 · {args.level}",
        }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {meta_path.relative_to(REPO_ROOT)}")
    else:
        print(f"Meta exists, skipping: {meta_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
