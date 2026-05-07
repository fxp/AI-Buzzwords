# AI Buzzwords · DeepDive Design System
## 视觉系统展示 · v2

> 档案室 × 实验室 × 新闻编辑部 — Editorial · Dense · Warm · Anti-Hype

所有发表文章共享的视觉语言。**这份文档是浏览版**——边看边对照能直接抄走。

| 资源 | 用途 |
|---|---|
| [`colors_and_type.css`](colors_and_type.css) | 中央 token 文件（颜色 / 字体 / 尺度 / 动画 / CJK 规则）|
| [`kit.css`](kit.css) | 长读组件 CSS（`.dd-strip` / `.dd-section` / `.dd-hero` 等）|
| [`design-system.html`](https://fxp.github.io/AI-Buzzwords/design-system.html) | 交互式 HTML 展示 + 主题/明暗切换 |
| [`DESIGN.md`](DESIGN.md) | 严格规范 spec（约束清单）|

**v2 新增**：light mode (parchment) · 全 CJK fallback 链 + per-script 自动切换 · CJK 永不斜体强制 · EB Garamond 加入字体系统 · spacing scale tokens · `colors_and_type.css` 作为 canonical token 文件。

---

## § 01 / 主题色

每篇文章选 **一个** accent。决定 lamp 光晕、cite 链接下划线、pullquote 引号、`<em>` 强调短语、关键 callout 边框。

<table>
<tr>
<th width="120">Token</th>
<th width="120">色块</th>
<th width="120">Hex</th>
<th>使用场景</th>
<th>已用文章</th>
</tr>
<tr>
<td><b>red</b></td>
<td><span style="background:#e84040;display:inline-block;width:64px;height:24px;border-radius:3px;"></span></td>
<td><code>#e84040</code></td>
<td>紧迫 · 时效 · 市场冲击</td>
<td>white-collar · labor-day-2026 · rentahuman · ai-military</td>
</tr>
<tr>
<td><b>signal</b></td>
<td><span style="background:#d1402c;display:inline-block;width:64px;height:24px;border-radius:3px;"></span></td>
<td><code>#d1402c</code></td>
<td>事故 · 泄露 · 单点突发</td>
<td>claude-code-leak</td>
</tr>
<tr>
<td><b>amber</b></td>
<td><span style="background:#f5a524;display:inline-block;width:64px;height:24px;border-radius:3px;"></span></td>
<td><code>#f5a524</code></td>
<td>分析 · 历史 · 结构 · B2B</td>
<td>cybertonia · neolab · palantir-aip · anthropic-enterprise-ai</td>
</tr>
<tr>
<td><b>mint</b></td>
<td><span style="background:#7fb88b;display:inline-block;width:64px;height:24px;border-radius:3px;"></span></td>
<td><code>#7fb88b</code></td>
<td>研究 · 发现 · 技术能力 · 硬件</td>
<td>emotion-vectors · project-deal · prd · protocol</td>
</tr>
</table>

**选不准就用 amber**——它是工作母机，从不显得刺耳。

---

## § 02 / 表面色（不随主题变）

页面背景是温暖的近黑（带红棕底色），不是纯黑。文本是温暖米白，不是纯白。

<table>
<tr><th>Token</th><th>色块</th><th>Hex</th><th>角色</th></tr>
<tr><td><code>bg</code></td><td><span style="background:#0c0a07;display:inline-block;width:48px;height:24px;border:1px solid #444;"></span></td><td><code>#0c0a07</code></td><td>页面背景</td></tr>
<tr><td><code>bg-2</code></td><td><span style="background:#161310;display:inline-block;width:48px;height:24px;border:1px solid #444;"></span></td><td><code>#161310</code></td><td>卡片 / 引语 / 侧栏</td></tr>
<tr><td><code>bg-3</code></td><td><span style="background:#1e1a15;display:inline-block;width:48px;height:24px;border:1px solid #444;"></span></td><td><code>#1e1a15</code></td><td>hover 态卡片（少用）</td></tr>
<tr><td><code>fg</code></td><td><span style="background:#f0ebe0;display:inline-block;width:48px;height:24px;"></span></td><td><code>#f0ebe0</code></td><td>主文本（米白）</td></tr>
<tr><td><code>fg-dim</code></td><td><span style="background:#a09888;display:inline-block;width:48px;height:24px;"></span></td><td><code>#a09888</code></td><td>正文段落（低反差利于长读）</td></tr>
<tr><td><code>fg-mute</code></td><td><span style="background:#6a6058;display:inline-block;width:48px;height:24px;"></span></td><td><code>#6a6058</code></td><td>标签 / 元信息 / footer</td></tr>
<tr><td><code>line</code></td><td><span style="background:rgba(240,235,224,0.10);display:inline-block;width:48px;height:24px;border:1px solid #222;"></span></td><td><code>rgba(240,235,224,0.10)</code></td><td>分隔线（细）</td></tr>
<tr><td><code>line-bright</code></td><td><span style="background:rgba(240,235,224,0.18);display:inline-block;width:48px;height:24px;border:1px solid #222;"></span></td><td><code>rgba(240,235,224,0.18)</code></td><td>strip 分隔 / hover 边</td></tr>
</table>

**回避**：纯黑 `#000` · 纯白 `#fff` · 中性灰。这套配色是有意做暖的。

---

## § 03 / 字体

```
正文 + 标题:  Fraunces (serif, optical-size 9-144) → 'Source Han Serif SC' / Georgia
标签 + 元信息: JetBrains Mono → ui-monospace
```

### 尺度

| 用途 | size | weight |
|---|---|---|
| Hero h1 | `clamp(36px, 9vw, 124px)` | `font-light` (300) |
| Section h2 | `clamp(24px, 6vw, 64px)` | `font-light` (300) |
| Article h3 | `clamp(20px, 4.5vw, 38px)` | `font-normal` (400) |
| 正文 | 15–16px | `font-light` (300) |
| Pullquote | `clamp(20px, 4vw, 38px)` | `font-light` (300) |
| Mono label | 9–11px | `letter-spacing: 0.18-0.22em` 大写 |
| Meta / footer | 10–11px | 同上，颜色更浅 |

### `<em>` 重定义

`<em>`/`<i>` 在系统里 **不再是斜体**——而是「accent emphasis」彩色着色：

```css
em, i { font-style: normal }
em.text-accent { color: var(--accent) }
```

> 用 `<em class="text-accent">` 在段落里 **标出关键短语**——它会染上当前主题色。

斜体只保留给 **pullquote 的署名行**。其他地方一律不用真斜体。

---

## § 04 / 布局

```
max-w-prose:    820px   单列正文 / pullquote
max-w-content: 1020px   hero h1 / 偶尔的宽块
max-w-wrap:    1320px   页面外容器（strip + hero + section 都在这层）
```

外容器统一 padding：`px-[5vw] lg:px-12`（移动端 5vw / 桌面 48px）。

每个 `<section>` 模板：

```html
<section class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-14 lg:py-28 border-b border-line">
  <header class="grid grid-cols-1 lg:grid-cols-[120px_1fr] gap-4 lg:gap-12 items-baseline mb-10 lg:mb-[72px]">
    <div class="cursor font-mono text-[10px] lg:text-[11px] tracking-[0.2em] text-accent
                pt-3 border-t border-accent uppercase">§ 0X / 节标题</div>
    <h2 class="font-serif font-light text-[clamp(24px,6vw,64px)] leading-[1.05] tracking-tight">
      节中文标题<br/><em class="text-accent">关键短语</em>
    </h2>
  </header>
  <div class="lg:ml-[168px] max-w-prose ...">
    <!-- body -->
  </div>
</section>
```

`lg:ml-[168px]` = 120 (label 列) + 48 (gap) ——把 body 与 h2 列对齐。

---

## § 05 / 组件

### TOP STRIP（Pattern A · 唯一）

页面顶部单行 flex 条，所有文章一致：

```
[●] DEEPDIVE / [TOPIC LABEL]  [可选导航徽章]   ····   [LANG]   |  v1 · 2026 · MAY 06 · 更新说明
```

```html
<div class="relative z-[2] border-b border-line">
  <div class="max-w-wrap mx-auto px-[5vw] lg:px-12 py-3 flex items-center gap-4 flex-wrap">
    <span class="lamp mr-1"></span>
    <span class="font-mono text-[9px] lg:text-[10px] tracking-[0.22em] uppercase text-accent">DEEPDIVE</span>
    <span class="text-line-bright font-mono text-[10px]">/</span>
    <span class="font-mono text-[9px] lg:text-[10px] tracking-[0.18em] uppercase text-fg-mute">[TOPIC] · 文章短标题</span>
    <a href="..." class="font-mono text-[9px] lg:text-[10px] tracking-[0.18em] uppercase text-fg-mute
                          hover:text-accent border border-line-bright px-2 py-0.5 transition-colors">导航徽章</a>
    <div data-lang-switcher data-slug="<slug>" style="margin-left:auto"></div>
    <span class="flex-1 h-px bg-line hidden lg:block"></span>
    <span class="font-mono text-[9px] tracking-[0.14em] text-fg-mute">v1 · 2026 · MAY 06 · 更新说明</span>
  </div>
</div>
```

> **lang-switcher 永远在 strip 内部**，靠 `margin-left:auto` 推到右侧。漂浮在 body 顶部 = bug。

---

### Lamp · 动画指示器

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

只搭配 strip 的 `DEEPDIVE` 标签出现，不入正文。

---

### Cursor · 章节标签上的"正在键入"

```html
<div class="cursor font-mono ...">§ 02 / 节标题</div>
```

```css
.cursor::after {
  content: '▋';
  animation: blink 1.1s step-end infinite;
  margin-left: 2px;
  color: var(--accent);
  font-size: 0.7em;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
```

仅用于 `§ 0X / ...` 章节标签，不放正文。

---

### Pullquote · 主题色引号

```html
<div class="relative pullquote-mark lg:ml-[168px] max-w-prose">
  <p class="font-serif text-[clamp(20px,4vw,38px)] font-light leading-[1.2] tracking-tight text-fg">
    引语正文……<em class="text-accent">关键短语</em>。
  </p>
  <p class="font-mono text-[10px] tracking-[0.18em] text-fg-mute uppercase mt-6">
    <a href="..." class="cite">来源人名</a>, 标题 — 2026 年 X 月日期
  </p>
</div>
```

```css
.pullquote-mark::before {
  content: '"';
  font-family: 'Fraunces', Georgia, serif;
  font-size: 6rem; line-height: 0.8;
  color: var(--accent); opacity: 0.25;
  position: absolute; top: -8px; left: -12px;
}
```

引号是 6rem 的 Fraunces `"`，opacity 0.25 不抢戏。

---

### Cite link · 点状下划线

```html
<a href="..." class="cite" target="_blank" rel="noopener">来源标题</a>
```

```css
a.cite {
  color: inherit;
  text-decoration: underline;
  text-decoration-style: dotted;
  text-underline-offset: 3px;
  text-decoration-color: var(--accent-soft);
  transition: color 0.15s;
}
a.cite:hover { color: var(--accent); }
```

> **所有引用必须用 cite 类**——不能裸 `<a>`。点状下划线在静态时低调，hover 时染主题色。

mint 主题文章用 `class="cite-mint"`（同样的样式但着色 mint）。

---

### Synthesis 块 · 综合判断 callout

```html
<div class="synthesis-label max-w-prose mt-8 p-5 lg:p-8 border border-accent-soft bg-accent-soft">
  <p class="text-[15px] lg:text-base text-fg leading-relaxed font-light">综合判断段落……</p>
</div>
```

```css
.synthesis-label::before {
  content: 'SYNTHESIS / 综合判断';
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.2em;
  color: var(--accent);
  margin-bottom: 12px; text-transform: uppercase;
}
```

每篇文章只用 1–2 次。多了贬值。

---

### Section label · 编号章节标题

```html
<div class="cursor font-mono text-[10px] lg:text-[11px] tracking-[0.2em] text-accent
            pt-3 border-t border-accent uppercase">
  § 02 / 反驳之声
</div>
```

`border-t border-accent` 在标签上方画一条主题色细线，整页章节序号一气呵成。

---

### Stats grid · hero 数据网格

```html
<div class="grid grid-cols-2 lg:grid-cols-4 gap-px bg-line border border-line font-mono">
  <div class="bg-bg p-5 lg:p-7">
    <div class="text-[clamp(28px,6vw,52px)] font-serif text-accent leading-none mb-2 tabular-nums">1-5</div>
    <div class="text-[9px] text-fg-mute tracking-[0.14em] uppercase leading-relaxed">年时间线<br/>来源</div>
  </div>
  <!-- 重复 3 个 -->
</div>
```

`gap-px bg-line` 这个组合用线色填充网格 1px 间隙，画出无边框效果的极细分隔线。

---

### Tag pill · 标签

```html
<span class="inline-block border border-line-bright py-0.5 px-2 mr-1
             text-[10px] text-fg-mute font-mono">
  CASE FILE
</span>
```

用于证据卡片的元数据条。**不要在正文里散布。**

---

## § 06 / 动画预算

| 动画 | 时长 | 缓动 | 循环 |
|---|---|---|---|
| Lamp pulse | 2.4s | `ease-in-out` | infinite |
| Cursor blink | 1.1s | `step-end` | infinite |
| Hero fadeUp | 0.7s × 4 stagger (0.05/0.15/0.25/0.35) | `ease` | once |
| Hover 过渡 | 0.15s | default | once |
| Detail panel 展开 | 0.22s | `ease` | once |

> **页面应保持安静。** 多于此 = 噪音。无视差，无滚动触发的渐入（hero-anim 例外）。
> 动画是预算——只花一次。

---

## § 07 / 绝不做

- ✕ **加第 5 个主题色**——如果新文章不属于 red/signal/amber/mint，可能本身就不属于 DeepDive
- ✕ **直接写 hex 工具类**（`bg-[#abc123]`）——必须用 token（`bg-accent`）
- ✕ **署名加 emoji**——正文里 🔴/🟡/🟢/❓ 严重度标签可以，作者行不行
- ✕ **lang-switcher 摆放在 strip 之外**——它是被锁定的 landmark
- ✕ **hero 之外的 page-load 动画**——动画预算只能花一次
- ✕ **正文用真斜体**——`<em>` 重绑为彩色，不倾斜
- ✕ **混用 amber 的两个 hex**：旧版 `#c4850a` vs 新版 `#f5a524`。新文必须用 `#f5a524`，老文 normalize 时迁移

---

## § 08 / Tailwind config（粘贴进文章 `<head>`）

```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg:           '#0c0a07',
        'bg-2':       '#161310',
        'bg-3':       '#1e1a15',
        fg:           '#f0ebe0',
        'fg-dim':     '#a09888',
        'fg-mute':    '#6a6058',
        line:         'rgba(240,235,224,0.10)',
        'line-bright':'rgba(240,235,224,0.18)',
        accent:       'var(--accent)',
        'accent-soft':'var(--accent-soft)',
        'accent-glow':'var(--accent-glow)',
        red:          '#e84040',
        signal:       '#d1402c',
        amber:        '#f5a524',
        mint:         '#7fb88b',
      },
      fontFamily: {
        serif: ["'Fraunces'","'Source Han Serif SC'","Georgia","serif"],
        mono:  ["'JetBrains Mono'","ui-monospace","monospace"],
      },
      maxWidth: { prose: '820px', content: '1020px', wrap: '1320px' },
    }
  }
}
</script>
```

`accent: 'var(--accent)'` 让 `text-accent` / `bg-accent` 等 Tailwind 类自动跟随 `<style id="theme-vars">` 注入的 CSS 变量——主题色切换零 Tailwind 配置改动。

并在 `<head>` 里加上 theme-vars block（由 `normalize_strip.py` 自动注入）：

```html
<style id="theme-vars">
  :root { --accent: #e84040; --accent-glow: rgba(232,64,64,0.30); --accent-soft: rgba(232,64,64,0.10); }
</style>
```

`<body data-theme="red|signal|amber|mint">` 不直接在这里切换；切换是更宏观的级别（如 `design-system.html` 的右上角按钮）。文章页 body 选定一个主题后基本不变。

---

## § 09 / 文件参考

| 文件 | 用途 |
|---|---|
| [`design-system.html`](design-system.html) | 交互式可视化展示页（带主题切换器） |
| [`DESIGN.md`](DESIGN.md) | 严格规范 spec（token 定义、约束清单） |
| `DESIGN-SHOWCASE.md`（本文件） | 浏览版展示页（边看边抄） |
| [`templates/article.html`](templates/article.html) | 黄金模板（含 `{{PLACEHOLDERS}}`） |
| [`templates/_strip.html`](templates/_strip.html) | TOP STRIP 单独组件 |
| [`config/themes.json`](config/themes.json) | 每篇文章 accent + topic_label 注册表 |
| [`scripts/normalize_strip.py`](scripts/normalize_strip.py) | 把现有文章 strip 迁到 Pattern A |
| [`CLAUDE.md`](CLAUDE.md) §13 | 模板使用 + normalize 工作流 |

---

## § 10 / 应用时机

**写新文章**：
1. 复制 `templates/article.html` 起手
2. `config/themes.json` 加一项（accent + topic_label + version_label）
3. 必要时跑 `python3 scripts/normalize_strip.py --slug <new-slug>` 校准 strip

**改老文章 strip 不一致**：
```bash
python3 scripts/normalize_strip.py --dry-run        # 预览
python3 scripts/normalize_strip.py                  # 应用
```

**从微观参考某个组件**：浏览此文，找到对应章节，复制代码块。

**从宏观 review 一致性**：打开 [`design-system.html`](design-system.html)，切换 4 个主题对比。

---

*DeepDive 视觉系统 v1 · 2026-05-07 · 由 [`design-system.html`](design-system.html) 派生而来 · 用 `viewer.html` 看本文 [`?f=DESIGN-SHOWCASE.md`](viewer.html?f=DESIGN-SHOWCASE.md)*
