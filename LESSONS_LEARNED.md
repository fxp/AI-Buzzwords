# AI-Buzzwords · 经验沉淀

把构建这个 DeepDive 发布系统过程中真正踩过的坑、踩完后形成的硬性约定记下来。后来者（人或 agent）重复同一个错误是不必要的成本。

---

## 1. 写作环境与发布环境必须分离

**坑**：最初一切都在 vault 里写。后来想加 git history → vault 在 iCloud 里 → iCloud 同步 + git 仓库会持续冲突。

**约定**：
- vault（iCloud Obsidian）只做**写作素材**，永不 git init
- 发布仓库放 `~/Code/`（本地，非 iCloud），独立 git
- vault → repo 是**单向迁移**，repo 不回写到 vault

详见 `STRUCTURE.md §3`。

---

## 2. Markdown 不能直链，必须包 viewer

**坑**：第一版直接给用户 `xxx.md` 的 GitHub Pages URL → 浏览器渲染成裸文本，没有目录、没有暗色模式、没有 GFM。

**修复**：构建 `viewer.html`（marked + highlight.js + github-markdown-css），所有 `.md` URL 必须经过 `viewer.html?f=<path>` 包装。

**关键 bug 学习**：
- `marked@14` 自定义 `renderer.link/image` 会丢失 `this.parser` 绑定 → `parseInline` undefined。改用 `walkTokens` 钩子在解析阶段直接改 token href。
- `highlight.js` 的 `lib/core.min.js + lib/common.min.js` 是 CommonJS 模块，浏览器加载不会暴露 `hljs` 全局。必须用 cdnjs 的预打包浏览器 bundle。

详见 `viewer.html` 注释 + git log。

---

## 3. 第三方 CDN 改完一定要本地实测，不能信 commit

**坑**：第一次修 viewer 报错时，我修完直接推，再次报错。第二次修又推，又报错。原因是 CDN 库的 API 表面我猜的。

**约定**：所有涉及第三方 JS / CDN 的修改，必须：
1. `cd ~/Code/AI-Buzzwords && python3 -m http.server 8765` 起本地 HTTP server（file:// 不行，fetch CORS）
2. 用 `/browse` 工具实际加载 → `console --errors` → `js "document.querySelector(...)"` 验证
3. 只有本地通过才推

详见 `git log --grep="walkTokens\|hljs"`。

---

## 4. TL;DR 不能单独成文，必须内联

**坑**：早期把 TL;DR 写成独立的 `*-tldr.md` 文件 → 维护成本翻倍（HTML 改了 markdown 也要改），搜索引擎看到两个版本不知该指哪一个。

**约定**：TL;DR 必须作为 HTML 内的内联 section，位于 hero 后、§ 01 前。30 秒可读：
- 1 句核心论点（≤30 字）
- 3-6 个核心数据点（带数字优先）
- 1 句反共识洞察

社交分享场景直接截图区块或复制文字，不需要单独 markdown。

详见 `~/.claude/projects/.../memory/feedback_tldr.md`（用户偏好）。

---

## 5. 厂商署名是硬限制，正文是软限制

**坑**：早期发布的 NEOLAB 文章在编辑署名行写了"编辑：智谱 AI 内部研究简报"，被指出后逐处清理。第一次以为全文禁词，后来澄清是只禁署名位置。

**约定**：
- ❌ 作者 / 编辑 / 出品方署名位置出现 zhipu / 智谱 / GLM / Z.ai
- ✅ 正文把这些产品作为客观分析对象（产品对比、benchmark、case study、地缘分析）
- 发布前必跑：`grep -i -E "zhipu|智谱|glm|z\.ai" <files>`，看命中位置而非命中数

详见 `~/.claude/projects/.../memory/feedback_no_zhipu.md`。

---

## 6. 引用必须有原始链接，禁裸域名

**坑**：早期文章里写"据 WSJ 报道"但没链接，或者写 `wsj.com/` 这种裸域名，读者无法验证。

**约定**：
- 凡引用论文 / 研报 / 新闻 / CEO 表态 / 数据点的地方必须有 `<a href>` 指向**原始来源**
- 禁裸域名（如 `wsj.com/`、`gartner.com/`）
- CEO 引语必须可追溯到原始采访 / 推文
- 发布前 `grep -nE 'href="https?://[^/]+/?"$'` 扫裸域名

详见 `~/.claude/projects/.../memory/feedback_cite_links.md`。

---

## 7. 敏感话题必须双版本（直率版 + 中文婉转版）

**坑**：早期 white-collar.html 直接给了"AI 替代白领初级岗"的硬结论，分享时被多次拒绝（讨论氛围、传播友好性问题）。

**约定**：
- 涉及裁员 / AI 失业 / CEO 动机 / 地缘对比的文章，**必交付两版**：
  - `<slug>.html` — 直率版（默认，研究优先）
  - `<slug>-cn.html` — 中文婉转版（措辞替换映射详见 memory）
- 用户可见标签**永远叫"中文婉转版"**，不加英文 TACTFUL EDITION 副标
- **禁用术语**：合规版 / CN EDITION / 合规调整
- Banner 只显示版本名 + 原版链接，**不解释做了什么调整** —— 婉转的核心是不解释自己为什么婉转

详见 `~/.claude/projects/.../memory/feedback_tactful_edition.md`。

---

## 8. 双部署必须返回两个 URL

**坑**：第一次发布完成给了用户一个 `fxp.github.io/...` URL。用户问 "xpf.com 上呢？" 才意识到双部署需要双 URL 报告。

**约定**：任何文章发布完成的回复必须包含两个 URL：

```
GitHub Pages:    https://fxp.github.io/AI-Buzzwords/<path>
xiaopingfeng:    https://xiaopingfeng.com/blog/ai-buzzwords/<path>
```

不要只给其中一个。Cloudflare Worker 反向代理两个 URL 内容完全一致，但用户可能在不同场景需要不同 URL。

详见 `~/.claude/projects/.../memory/project_publishing_workflow.md`。

---

## 9. 双语自动翻译需要 meta.json 触发

**坑**：早期发完中文 HTML 没写 meta.json → translate.yml 不会动 → 没有英文版。

**约定**：每篇新文章必须配套 `<slug>.meta.json`：

```json
{
  "slug": "<slug>",
  "topic_dir": "<parent>",
  "title": { "zh": "中文标题", "en": null },
  "current_version": 1,
  "first_published": "YYYY-MM-DD",
  "freshness_priority": "warm",
  "languages": ["zh"],
  "translations": {}
}
```

`title.en: null` 是关键 → translate.yml 检测到后会自动翻译并填回。

新加语言只改 `config/languages.json` 一行配置即可（`ja`、`ko` 等），不动文章。

详见 `~/.claude/projects/.../memory/feedback_bilingual.md`。

---

## 10. 内容刷新系统：让旧文章不腐烂

**坑**：行业变化快。两个月前写的"Capybara v8 幻觉率 16.7%"今天可能变了，链接腐烂、CEO 已离职。

**约定**：每篇文章按 `freshness_priority` 周一巡检：
- `hot` — 7 天巡检（CEO 表态、市场行情）
- `warm` — 30 天（默认）
- `cold` — 90 天（历史 / 概念性文章）

freshness-check.yml 用规则 + LLM 混合检查（链接腐烂 / 数据漂移 / 预测到期 / staleness review），产出 `_freshness/<topic>/<slug>-<date>.md` + GitHub Issue + Slack 通知。

历史版本通过 `?v=N` 查询参数访问（仅 xiaopingfeng.com，Worker 处理）。

详见 `~/.claude/projects/.../memory/project_freshness_system.md`。

---

## 11. 状态 gating：enable / coming-soon / draft

**坑**：首页早期把所有 vault 已迁文章都挂可点击。结果点开有的是半成品 archive，体验差。

**约定**：首页用三态 gating：
- **enabled**：完成 4 资产 + 已审阅 → 高亮可点击
- **coming-soon**：内容已迁但未完成工作流 → 灰色不可点击 + 标 "Coming soon"
- **draft**：还在 vault 没进 repo → 首页根本看不见

详见 `STRUCTURE.md §6`。

---

## 12. 永远不要做的事（速查）

| ❌ 不要 | ✅ 改用 |
|---|---|
| 在 vault 里 `git init` | 把 vault 当只读源，发布在 `~/Code/AI-Buzzwords/` |
| 直链 `.md` URL | 包 `viewer.html?f=<path>` |
| 改第三方 CDN 后直接推 | 本地起 server + browse 工具实测 |
| 单独写 `*-tldr.md` 文件 | 内联到 HTML 的 hero 后 § 01 前 |
| 在署名行写"编辑：智谱..." | 厂商署名禁词 grep 自检 |
| "据 X 报道" 没链接 | 每个引用必须 `<a href>` 原始来源 |
| 给用户一个 GitHub Pages URL 就完 | 双 URL 同时返回（GH + xpf） |
| 改已上线文章的 slug | URL 不可变；要改起新 slug 做重定向 |
| 跳过 meta.json | 翻译流水线就不会动 → 永远没英文版 |
| 把所有 vault 已迁的都挂可点击 | 三态 gating；只 enable 已完工的 |

---

## 13. 给后来者的建议

如果你（人或 agent）刚接手这个项目：

1. **先读 `STRUCTURE.md`**：理解三层模型 vault → repo → URL
2. **再读 `~/.claude/projects/.../memory/MEMORY.md`**：所有用户偏好规则的索引
3. **改第三方依赖前先建 mental model**：marked v14 ≠ v3，hljs bundle ≠ ESM
4. **任何"复杂步骤后给用户 URL"的回复都用本地实测过的 URL**，不要信 commit
5. **遇到拿不准的内容立场（婉转 / 厂商）问用户**，不要默认中性

最重要的元原则：**修过的坑就是规则**。每个本文档的 §1-§11 都对应一次实际事故。再遇到同类决策时按这里的约定做，不要重新发明。
