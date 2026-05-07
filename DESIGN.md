# AI Buzzwords · DeepDive Design System

> 档案室 × 实验室 × 新闻编辑部 — Editorial · Dense · Warm · Anti-Hype
>
> 视觉签名一句话：温暖暗色档案 (`#0c0a07`) + 每页一个 accent lamp (red / signal / amber / mint) + Fraunces light 显示 + EB Garamond 正文 + JetBrains Mono uppercase eyebrows + 发线（无卡片阴影）+ 零圆角 + 中文永不斜体 + `<em class="text-accent">` = 着色而非倾斜。

**Token 真相之源**：[`colors_and_type.css`](colors_and_type.css)（313 行，所有颜色/字体/尺度/动画 tokens）
**组件层**：[`kit.css`](kit.css)（`.dd-strip` / `.dd-section` / `.dd-hero` / `.dd-pullquote` 等 — `@import` colors_and_type.css）
**可视化展示**：[`design-system.html`](design-system.html)（live theme + light/dark toggle）· [xiaopingfeng 镜像](https://xiaopingfeng.com/blog/ai-buzzwords/design-system.html)

---

## 1. Theme palette

Every article picks **exactly one** accent theme. The accent drives: lamp glow, cite link underline, pullquote mark, in-body emphasis (`<em>`), CTA borders, "active" states. Body / surface / text colors stay constant across themes.

| Token | Hex | RGBA glow | RGBA soft | Use for |
|---|---|---|---|---|
| **red** | `#e84040` | `rgba(232,64,64,0.30)` | `rgba(232,64,64,0.10)` | Urgent, time-bound, market shock (labor, layoffs, predictions) |
| **signal** | `#d1402c` | `rgba(209,64,44,0.28)` | `rgba(209,64,44,0.10)` | Incident / leak / breach (sharper than red, less common) |
| **amber** | `#f5a524` | `rgba(245,165,36,0.28)` | `rgba(245,165,36,0.10)` | Analytical, historical, structural (cybernetics, B2B, NEO LAB) |
| **mint** | `#7fb88b` | `rgba(127,184,139,0.28)` | `rgba(127,184,139,0.12)` | Research, discovery, technical capability (interpretability, hardware) |

### Choosing an accent

| Article kind | Theme |
|---|---|
| Labor-market shock, layoff data, urgent prediction | red |
| Security/leak/breach, single-incident report | signal |
| Industry analysis, history piece, B2B strategy, infra | amber |
| Mechanistic interp, capability discovery, dev product | mint |

When unsure: **amber**. It's the workhorse and never feels alarmist.

---

## 2. Surface palette · dark mode (default)

| Token | Hex | Role |
|---|---|---|
| `bg` | `#0c0a07` | Page background — warm near-black with red-brown undertone |
| `bg-2` | `#161310` | Card / sidebar / pull-quote surface (one step lighter) |
| `bg-3` | `#1e1a15` | Hover / focused-card surface (rare) |
| `bg-paper` | `#e8e3d8` | Paper / archive frame around imagery |
| `bg-ink` | `#1a1815` | Ink on paper |
| `fg` | `#f0ebe0` | Primary text — warm bone, never pure white |
| `fg-dim` | `#a09888` | Body paragraph text on `bg` (lower contrast for long-read) |
| `fg-mute` | `#6a6058` | Labels, eyebrows, footer meta |
| `line` | `rgba(240,235,224,0.10)` | Divider / border (subtle) |
| `line-bright` | `rgba(240,235,224,0.18)` | Strip dividers, hover-state borders |

Avoid: pure black (`#000`), pure white (`#fff`), neutral gray. The palette is intentionally warm.

## 2.b · Light mode parchment (opt-in)

Set `<html data-mode="light">` (or `data-theme="light"`) to flip into the **archive parchment** palette. Same brand DNA — just daylight in the archive room instead of warm dark archive. Components reference `var(--bg)` / `var(--fg)` and switch automatically; accent colors deepen for AA contrast on cream.

| Token | Light hex | Role |
|---|---|---|
| `bg` | `#f3ede0` | Cream parchment, never pure white |
| `bg-2` | `#ebe3d2` | Inset / pull-quote surface |
| `bg-3` | `#e2d8c2` | Hover surface |
| `fg` | `#1a1815` | Ink, never pure black |
| `fg-dim` | `#58524a` | Body paragraph |
| `fg-mute` | `#8a8276` | Metadata |
| `line` | `rgba(26,24,21,0.12)` | Hairlines |
| `line-bright` | `rgba(26,24,21,0.22)` | Strip dividers |

**Deepened accent palette in light mode** (AA contrast on cream):

| Token | Dark | Light |
|---|---|---|
| `red` | `#e84040` | `#b8302e` |
| `signal` | `#d1402c` | `#b22a17` |
| `amber` | `#f5a524` | `#b8761a` |
| `mint` | `#7fb88b` | `#4a7a55` |

Accent token (`--accent`) auto-deepens via `[data-mode="light"]` selector. No per-component override needed.

---

## 3. Typography

The system is a **scholarly two-serif pairing + mono**, with full CJK fallback chain at every level. Latin face order + CJK face order live in `colors_and_type.css` as `--display`, `--display-alt`, `--serif`, `--cjk-serif`, `--cjk-sans`, `--mono`, `--sans`.

### Latin faces

| Token | Family | Use |
|---|---|---|
| `--display` | **Fraunces** 300/400/500/700, optical-size 9–144 | Primary headlines (Latin), wordmark, hero h1 |
| `--display-alt` | **Spectral** 300/400/500/600/700 | Alternate display (legacy/preview pages) |
| `--serif` | **EB Garamond** 400/500/600/700 + italic | Latin running text body |
| `--mono` | **JetBrains Mono** 300/400/500/700 | Eyebrows, metadata, code, in-line tags |
| `--sans` | **Inter Tight** 400/500/600 | UI chrome (kept in reserve, rarely used) |

### CJK faces (auto-loaded per `lang` attribute)

- **Noto Serif SC / TC / JP / KR** — canonical CJK serif. The system swaps the script-correct sub-family automatically on `:lang(zh-Hant)`, `:lang(ja)`, `:lang(ko)`.
- **PingFang SC + Hiragino Kaku Gothic ProN + Apple SD Gothic Neo** — native system sans for each East Asian OS.

Every Latin font stack ends with the **full CJK fallback chain** (SC → TC → JP → KR → system) so Han / Kana / Hangul characters always land on a real face.

### Scale

| Use | Token / size | Weight |
|---|---|---|
| Hero h1 | `--t-display` `clamp(36px, 9vw, 124px)` | `300` |
| Section h2 | `--t-h1` `clamp(24px, 6vw, 64px)` | `300` |
| Article h3 | `--t-h2` `clamp(20px, 4.5vw, 38px)` | `400` |
| h4 | `--t-h4` `22px` | `500` |
| Body lg | `--body-lg` `19px` | `300-400` |
| Body | `--body` `16px` | `300-400` |
| Body sm | `--body-sm` `15px` | `300-400` |
| Caption | `--caption` `14px` | normal |
| Eyebrow | `--eyebrow` `11px` mono | normal, uppercase, `0.20em` track |
| Micro | `--micro` `10px` | mono, uppercase |

### CJK-specific typography rules (HARD)

The system enforces upright CJK at three layers — **Han / Kana / Hangul glyphs are never italic anywhere**:

```css
:lang(zh), :lang(zh-Hans), :lang(zh-Hant),
:lang(ja), :lang(ko),
.cjk, .cjk * {
  font-style: normal !important;
  font-synthesis-style: none;        /* block UA-synthesised italics */
  font-feature-settings: "palt" 1;   /* proportional kana/kanji metrics */
}
```

Plus per-script tuning:
- **Body** in CJK: line-height `1.85` (vs Latin 1.65), letter-spacing `0.02em`, `text-spacing-trim: trim-start` (CSS Text 4 — collapses CJK punctuation gutter next to Latin)
- **Headlines** in CJK: line-height `1.1` (`0.95` is too tight for full-em-box squares), letter-spacing `0` (never negative-track CJK)
- **Per-script display** — `:lang(zh-Hant)` → Noto Serif TC, `:lang(ja)` → Noto Serif JP + Hiragino Kaku Gothic, `:lang(ko)` → Noto Serif KR + Apple SD Gothic Neo

### Real italics (only place)

```css
.dd-pull cite:lang(en),
.dd-pull cite[lang^="en"] { font-style: italic; }
```

Pullquote attribution lines tagged `lang="en"` are the **only** place real italics exist in the brand. Everywhere else, `<em>` is repurposed:

```css
em, i { font-style: normal }
em.text-accent, .text-accent { color: var(--accent) }
```

Use `<em class="text-accent">` to mark the *one* word in a sentence that carries the argument — color, not slant.

### Mixed-script utilities

- `<span class="cjk">中文</span>` — inline CJK runs inside an EN container (uses `--cjk-serif`)
- `<span class="cjk-sans">中文</span>` — inline CJK sans
- `<span class="han-punct">、。，：</span>` — `halt` + `palt` features for tight CJK punctuation against Latin

---

## 4. Layout + spacing tokens

### Width tokens (CSS vars)

```
--w-prose    : 820px   (single-column reading width)
--w-content  : 1020px  (hero h1, occasional wide blocks)
--w-wrap     : 1320px  (page outer container, strip + hero + sections)
```

Padding: `5vw` mobile, fixed `48px` desktop. Outer chrome (`.dd-wrap`) maps to `var(--w-wrap)`.

### Spacing scale (8-pt + editorial)

```
--s-0: 0        --s-5: 24px
--s-1: 4px      --s-6: 32px
--s-2: 8px      --s-7: 48px
--s-3: 12px     --s-8: 72px
--s-4: 16px     --s-9: 112px
```

Use these instead of arbitrary px values. Section padding is `--s-8` mobile / `--s-9` desktop. Card padding `--s-5` to `--s-7`. Gap between elements `--s-3` to `--s-5`.

### Section grid

Every `<section>` follows:

```html
<section class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-14 lg:py-28 border-b border-line">
  <header class="grid grid-cols-1 lg:grid-cols-[120px_1fr] gap-4 lg:gap-12 items-baseline mb-10 lg:mb-[72px]">
    <div class="cursor font-mono text-[10px] lg:text-[11px] tracking-[0.2em] text-accent pt-3 border-t border-accent uppercase">§ 0X / 节标题</div>
    <h2 class="font-serif font-light text-[clamp(24px,6vw,64px)] leading-[1.05] tracking-tight">
      节中文标题<br/><em class="text-accent">关键短语</em>
    </h2>
  </header>
  <div class="lg:ml-[168px] max-w-prose ...">
    <!-- body -->
  </div>
</section>
```

The 168px left offset on body (= 120px label + 48px gap) keeps body aligned with the h2 column on desktop.

---

## 5. Components

### TOP STRIP (Pattern A — canonical)

Single-row flex bar at top of every article. Contents:

```
[lamp] DEEPDIVE / [TOPIC LABEL]  [optional nav pill]  ····  [LANG SWITCHER]  | v1 · 2026 · DATE · note
```

```html
<div class="relative z-[2] border-b border-line">
  <div class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-3 flex items-center gap-4 flex-wrap">
    <span class="lamp mr-1"></span>
    <span class="font-mono text-[9px] lg:text-[10px] tracking-[0.22em] uppercase text-accent">DEEPDIVE</span>
    <span class="text-line-bright font-mono text-[10px]">/</span>
    <span class="font-mono text-[9px] lg:text-[10px] tracking-[0.18em] uppercase text-fg-mute">[TOPIC] · 文章短标题</span>
    <a href="..." class="font-mono text-[9px] lg:text-[10px] tracking-[0.18em] uppercase text-fg-mute hover:text-accent border border-line-bright px-2 py-0.5 transition-colors">导航徽章</a>
    <div data-lang-switcher data-slug="<slug>" style="margin-left:auto"></div>
    <span class="flex-1 h-px bg-line hidden lg:block"></span>
    <span class="font-mono text-[9px] tracking-[0.14em] text-fg-mute">v1 · 2026 · MAY 06 · 更新说明</span>
  </div>
</div>
```

The `margin-left:auto` on lang-switcher pushes it to the right. The `flex-1 h-px` span draws the spacer line between switcher and version label.

**Always use this pattern.** Pattern B (the older 4-column grid with FILED date) is deprecated — `scripts/normalize_strip.py` migrates it.

### Lamp (animated indicator)

```html
<span class="lamp"></span>
```
```css
.lamp {
  display: inline-block; width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent), 0 0 20px var(--accent-glow);
  animation: pulse 2.4s ease-in-out infinite;
  vertical-align: middle;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
```

Always paired with the strip's DEEPDIVE label. Never inside body content.

### Cursor (typing indicator on labels)

```html
<div class="cursor font-mono ...">§ 02 / 节标题</div>
```
```css
.cursor::after { content: '▋'; animation: blink 1.1s step-end infinite;
  margin-left: 2px; color: var(--accent); font-size: 0.7em; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
```

Use on section labels (`§ 0X / ...`). Never on body text.

### Hero animation cascade

```html
<div class="hero-anim">
  <p>Eyebrow</p>
  <h1>Title</h1>
  <p>Subtitle</p>
  <div>Stats</div>
</div>
```
```css
@keyframes fadeUp { from { opacity:0; transform:translateY(18px) } to { opacity:1; transform:translateY(0) } }
.hero-anim > * { animation: fadeUp 0.7s ease both; }
.hero-anim > *:nth-child(1) { animation-delay: 0.05s }
.hero-anim > *:nth-child(2) { animation-delay: 0.15s }
.hero-anim > *:nth-child(3) { animation-delay: 0.25s }
.hero-anim > *:nth-child(4) { animation-delay: 0.35s }
```

Each direct child stagger-fades in. Up to 4 children.

### Pullquote

```html
<div class="relative pullquote-mark lg:ml-[168px] max-w-prose">
  <p class="font-serif text-[clamp(20px,4vw,38px)] font-light leading-[1.2] tracking-tight text-fg">
    引语正文...<em class="text-accent">关键短语</em>。
  </p>
  <p class="font-mono text-[10px] tracking-[0.18em] text-fg-mute uppercase mt-6">
    <a href="..." class="cite">来源人名</a>, 标题 — 2026 年 X 月日期
  </p>
</div>
```
```css
.pullquote-mark::before {
  content: '"'; font-family: 'Fraunces', Georgia, serif;
  font-size: 6rem; line-height: 0.8; color: var(--accent); opacity: 0.25;
  position: absolute; top: -8px; left: -12px;
}
```

### Cite link

```html
<a href="..." class="cite" target="_blank" rel="noopener">来源标题</a>
```
```css
a.cite { color: inherit; text-decoration: underline; text-decoration-style: dotted;
  text-underline-offset: 3px; text-decoration-color: rgba(232,64,64,0.35);
  transition: color 0.15s; }
a.cite:hover { color: var(--accent); }
```

For mint-themed articles, use `class="cite-mint"` variant. Inline citations always use this; never bare `<a>`.

### Synthesis / takeaway block

```html
<div class="synthesis-label max-w-prose mt-8 p-5 lg:p-8 border border-accent-soft bg-accent-soft">
  <p class="text-[15px] lg:text-base text-fg leading-relaxed font-light">综合判断段落...</p>
</div>
```
```css
.synthesis-label::before {
  content: 'SYNTHESIS / 综合判断';
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.2em;
  color: var(--accent); margin-bottom: 12px; text-transform: uppercase;
}
```

Marks an opinionated, conclusion-drawing block. Use sparingly — once or twice per article.

### Section label (numbered)

```html
<div class="cursor font-mono text-[10px] lg:text-[11px] tracking-[0.2em] text-accent pt-3 border-t border-accent uppercase">
  § 02 / 反驳之声
</div>
```

The `border-t border-accent` creates the small horizontal line above the label.

### Tag / badge pill

```html
<span class="inline-block border border-line-bright py-0.5 px-2 mt-1.5 mr-1 text-[10px] text-fg-mute font-mono">
  分类标签
</span>
```

For sticky / category tags within evidence blocks. Never decorate body text with these.

### Stats grid (hero)

```html
<div class="grid grid-cols-2 lg:grid-cols-4 gap-px bg-line border border-line font-mono">
  <div class="bg-bg p-5 lg:p-7">
    <div class="text-[clamp(28px,6vw,52px)] font-serif text-accent leading-none mb-2 tabular-nums">1-5</div>
    <div class="text-[9px] text-fg-mute tracking-[0.14em] uppercase leading-relaxed">年时间线<br/>来源</div>
  </div>
  ...
</div>
```

The `gap-px bg-line` trick draws hairline separators by using line color as the gap fill.

---

## 6. Lang switcher

Reads `meta.json.languages` at runtime; renders only languages actually translated for the article.

```html
<div data-lang-switcher data-slug="<slug>" style="margin-left:auto"></div>
<script src="<repo-root>/lang-switcher.js" defer></script>
```

**Position rule**: always inside the top strip, before the `flex-1` spacer. Never floating outside the strip.

The switcher auto-hides if only one language exists (ZH-only article). It shows ZH/EN buttons + an optional "中文婉转版" pill for tactful editions.

---

## 7. Spacing rhythm

| Context | Spacing |
|---|---|
| Outer container vertical | `pt-16 lg:pt-28 pb-16 lg:pb-24` (hero) |
| Section vertical | `py-14 lg:py-28` |
| Hero header → body | `mb-10 lg:mb-[72px]` |
| Body paragraphs | `space-y-6` |
| Evidence cards | `py-7 lg:py-12 border-t border-line` |
| Section divider | `border-b border-line` (between sections) + `border-t border-line` (between cards) |

`gap-4 lg:gap-12` is the default flex/grid gap inside major rows.

---

## 8. Animation budget

| Animation | Duration | Easing | Loop? |
|---|---|---|---|
| Lamp pulse | 2.4s | `ease-in-out` | infinite |
| Cursor blink | 1.1s | `step-end` | infinite |
| Hero fadeUp | 0.7s (cascade 0.05s/0.15s/0.25s/0.35s) | `ease` | once |
| Hover transitions | 0.15s | default | once |
| Detail panel open | 0.22s | `ease` | once |

Keep the page calm. Anything more than these = noise. No parallax. No scroll-triggered reveal beyond hero.

---

## 9. Things to never do

- **Add a 5th theme color**. If a new article doesn't fit red/signal/amber/mint, it probably doesn't belong in DeepDive.
- **Use Tailwind utility classes for hex colors directly** (`bg-[#abc123]`). Always use a token (`bg-accent` etc).
- **Insert emoji in author signature / byline**. Inside body content (e.g. 🔴/🟡/🟢/❓ severity tags) is fine.
- **Use the strip's lang-switcher slot for anything else.** It's a hard-locked landmark; users reach for it.
- **Add page-load animation other than hero-anim cascade.** Animation is a budget; spend it once.
- **Use real italics in body text**. `<em>` rebound to color, not slant. Italics are reserved for pullquote attribution.
- **Mix amber #c4850a with amber #f5a524.** Older articles use the darker brown; newer use the saturated golden. New articles SHOULD use #f5a524 (canonical). Old articles get migrated when touched.

---

## 10. File reference

| File | Use |
|---|---|
| `templates/article.html` | Golden HTML template with `{{PLACEHOLDERS}}` |
| `templates/_strip.html` | Drop-in TOP STRIP component |
| `config/themes.json` | Per-article accent + topic-label registry |
| `lang-switcher.js` | Client-side language switcher component |
| `scripts/normalize_strip.py` | Migrate an existing article's strip to Pattern A + apply theme |
| `design-system.html` | Visual showcase (deployed to Pages) |
| `DESIGN.md` (this file) | Token + component reference (here) |
| `CLAUDE.md §13` | Operational workflow for using the template |

---

## 11. How to wire a new article

Two options — pick by what suits the page's complexity.

### Option A · Drop in canonical CSS (simplest)

Reference the repo-root token file. Two `<link>` lines in `<head>`:

```html
<!DOCTYPE html>
<html lang="zh-Hans" data-theme="amber">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>...</title>
  <link rel="stylesheet" href="../../colors_and_type.css">
  <link rel="stylesheet" href="../../kit.css">  <!-- only if using .dd-* components -->
</head>
<body class="dd-body">
  ...
</body>
</html>
```

`colors_and_type.css` brings: tokens, fonts (Google CDN), CJK rules, `<em>` rebinding, `.lamp` / `.cursor` / `.cite` / `.pullquote-mark` / `.synthesis-label` components. `kit.css` adds page chrome classes (`.dd-wrap`, `.dd-strip`, `.dd-hero`, `.dd-section`, etc.) that compose the long-read layout.

Set theme via `<html data-theme="red|signal|amber|mint">`. Light mode: add `data-mode="light"`.

### Option B · Inline Tailwind (legacy)

Older articles ship their own Tailwind config inline. The minimal block (uses CSS variables so theme auto-tracks):

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: { extend: {
    colors: {
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
      'accent-glow':'var(--accent-glow)',
      red:    '#e84040', signal: '#d1402c', amber: '#f5a524', mint: '#7fb88b',
    },
    fontFamily: {
      serif: ["Fraunces","EB Garamond","Noto Serif SC","Source Han Serif SC","Georgia","serif"],
      mono:  ["JetBrains Mono","ui-monospace","monospace"],
    },
    maxWidth: { prose: '820px', content: '1020px', wrap: '1320px' },
  }}
}
</script>
<link rel="stylesheet" href="../../colors_and_type.css">  <!-- still recommended for CJK rules + light mode -->
```

Even when going inline, **keep the `<link>` to `colors_and_type.css`** — it brings the CJK no-italic enforcement, light-mode palette, and `:lang()` per-script overrides that no inline tailwind config can replicate.

### Theme switcher (light/dark)

Provide a small toggle in the strip; persist via cookie or `localStorage`:

```js
document.querySelector('[data-toggle-mode]').addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-mode');
  document.documentElement.setAttribute('data-mode', cur === 'light' ? '' : 'light');
});
```

Reuse the [`mode-toggle.js`](mode-toggle.js) component when one exists.
