# AI-Buzzwords · 结构与命名规范

vault → repo → 公开 URL 的三层映射约定。所有内容创作者和 AI agent 必须遵守。

---

## 1. 三层模型

```
┌─────────────────────────┐    ┌────────────────────────┐    ┌─────────────────────────┐
│ Layer 1 / 写作源         │ →  │ Layer 2 / 发布仓库       │ →  │ Layer 3 / 公开 URL       │
│  (Obsidian Vault)        │    │  (~/Code/AI-Buzzwords)  │    │  (双部署)               │
│                          │    │                         │    │                         │
│  保留中文名 + [TAG]       │    │  全英 lowercase-hyphen  │    │  GitHub Pages           │
│  自由组织                 │    │  按规范固定结构          │    │  + Cloudflare Worker    │
└─────────────────────────┘    └────────────────────────┘    └─────────────────────────┘
        随便写                        slug 化 + 去元                fxp.github.io/AI-Buzzwords/
                                                                     ↕（内容一致）
                                                                xiaopingfeng.com/blog/ai-buzzwords/
```

每层有明确职责，不能互相混淆：
- **Layer 1（vault）** 是写作环境，可以乱、可以中文、可以反复改。**不进 git**（在 iCloud 里）。
- **Layer 2（repo）** 是发布产物，干净、英文 slug、提交历史可追溯。**唯一进 git 的位置**。
- **Layer 3（URL）** 是消费端，所有外部链接必须指向 Layer 3，绝不指向 vault 路径。

---

## 2. Layer 1 / Vault 命名规范

### 2.1 / `[TAG]` 是分类，不是文件名

vault 顶层目录格式：`[TAG] 主题名/`

**TAG 不是文件名的一部分，是分类标签**。一个 TAG 标记这个主题在选题地图里的位置。

| TAG | 范围 | 例 |
|---|---|---|
| `[AGENT]` | Agent 工程、Coding Agent、Agent 经济 | `[AGENT] Agent Economy/` |
| `[ENTERPRISE]` | ToB AI、企业服务、平台化 | `[ENTERPRISE] Palantir AIP/` |
| `[ECONOMY]` | 经济学、宏观、就业、能源税 | `[ECONOMY] ME&E 435/` |
| `[GOV]` | 监管、合规、政治经济 | `[GOV] AI Military/` |
| `[INFRA]` | 基础设施、推理民主化、Cloud | `[INFRA] AI推理民主化/` |
| `[LAB]` | 实验室深度（伞型 topic） | `[LAB] ANTHROPIC/` |
| `[MODELS]` | 模型本身（能力、内部、训练数据） | `[MODELS] 训练数据危机/` |
| `[NEOLAB]` | 小型前沿实验室深度 | `[NEOLAB] AndonLab/` |
| `[NEWJOB]` | 新型就业形态、Agent-as-employer | `[NEWJOB] RentAHuman/` |
| `[POLITICAL]` | 政治人物、地缘 | `[POLITICAL] 硅谷的政治家们/` |
| `[SECURITY]` | 安全、攻防、漏洞 | `[SECURITY] Mythos报告/` |
| `[TOPIC]` | 跨维度大主题（AI×就业 五维矩阵） | `[TOPIC] AI×就业/` |
| `[TRENDS]` | 长线趋势、行业拐点 | `[TRENDS] Cybertonia/` |

允许扩展。新 TAG 出现时同步更新本表。

### 2.2 / 子目录可继续用 `[SUB-TAG]`

伞型 topic（如 `[LAB] ANTHROPIC/`）下面可以继续用 `[SUB-TAG]` 子目录：

```
[LAB] ANTHROPIC/
  ├── [EVENT] Anthropic企业AI服务公司/      ← 事件类专题
  ├── [PRD] Claude Desktop Buddy/           ← 产品分析
  ├── [ANALYSIS] Buddy BLE 协议深潜/         ← 技术深度
  ├── [PRD] Claude 桌面版开发者模式/         ← 产品分析
  └── Anthropic公司全景/                     ← 系列章节（无 [TAG] 表示通用）
```

子 TAG 含义：
- `[EVENT]` — 突发事件 / 新闻锚点
- `[PRD]` — 产品分析（针对具体产品 / 功能）
- `[ANALYSIS]` — 深度分析（技术 / 协议 / 战略）
- `[REPORT]` — 报告 / 综述
- `[INDEX]` — 系列索引

### 2.3 / vault 内不要做 git / iCloud 同步

vault 在 iCloud 里。**禁止 `git init`** —— iCloud + git 同步会冲突。
vault 是只读的素材源；写作完成后通过迁移流程发布到 repo。

---

## 3. Layer 2 / Repo 路径规范

### 3.1 / 顶层结构

```
~/Code/AI-Buzzwords/
├── index.html                     ← 首页（导航 / gating）
├── viewer.html                    ← 通用 markdown 渲染器
├── lang-switcher.js               ← 多语言切换组件
├── README.md                      ← 仓库说明
├── STRUCTURE.md                   ← 本文档（结构规范）
├── LESSONS_LEARNED.md             ← 经验沉淀
├── CLAUDE.md                      ← Claude Code 工作手册
│
├── config/
│   ├── languages.json             ← 语言配置（zh/en/...）
│   └── glossary.json              ← 翻译术语表
│
├── scripts/
│   ├── publish-md.sh              ← markdown 单篇发布助手
│   └── ...                         ← 迁移 / 验证类脚本
│
├── deepdive/
│   ├── <topic-slug>/              ← 一个 topic = 一个目录
│   │   ├── index.html             ← 主页面（HTML 全文）
│   │   ├── <slug>.html            ← 单专题或子专题页面
│   │   ├── <slug>-cn.html         ← 中文婉转版（敏感话题）
│   │   ├── <slug>-blog.md         ← 博客 markdown
│   │   ├── <slug>.meta.json       ← 元数据（freshness / 翻译入口）
│   │   ├── <slug>.en.html         ← EN 自动翻译产物
│   │   └── <other assets>          ← 视频 / 图片 / sub-pages
│   ├── ...
│
└── .github/workflows/
    ├── deploy.yml                 ← Pages + Cloudflare Worker 双部署
    ├── translate.yml              ← GLM-5.1 自动翻译
    └── freshness-check.yml         ← 周一定时巡检
```

### 3.2 / topic-slug 命名规则

- **lowercase-hyphen**：全部小写，多词用 `-` 连接
- **英文优先**：避免拼音；找语义最贴近的英文短语
- **避免起始动词**：`buddy-protocol-deepdive` 而非 `analyze-buddy-protocol`
- **唯一性**：一个 topic 一个 slug，不重名
- **稳定性**：slug 一旦上线**永不更名**（外链不可变）

### 3.3 / topic 类型

| 类型 | 结构 | 例 |
|---|---|---|
| **单篇专题** | `deepdive/<slug>/` 内含 1 主文章 + 1 blog + 1 meta | `cybertonia/` |
| **双子专题** | `deepdive/<slug>/` 内含 2 兄弟 HTML（如姊妹篇） | `claude-desktop-buddy/` (prd + protocol) |
| **系列专题** | `deepdive/<slug>/` 内含 多篇章节 + index.html 门面 | `labor-day-2026/` |
| **伞型大主题** | `deepdive/<slug>/<sub-slug>/<files>` 两级嵌套 | `anthropic/overview/`、`anthropic/buddy-prd/` |

### 3.4 / 文件命名 Convention

每篇文章必须有的资产：

| 资产 | 文件名规则 | 强制？ |
|---|---|---|
| HTML 全文 | `<slug>.html`（或 `index.html` 当作 topic 门面） | ✅ |
| HTML 婉转版 | `<slug>-cn.html` | 仅敏感话题 |
| Blog markdown | `<slug>-blog.md` | ✅ |
| 元数据 | `<slug>.meta.json` | ✅ |
| 内联 TL;DR | （在 `<slug>.html` 内，hero 后 § 01 前） | ✅ — 严禁单独成文 |
| EN 翻译 | `<slug>.en.html` / `<slug>-blog.en.md` | 自动生成（translate.yml） |

---

## 4. Layer 3 / 公开 URL 规范

### 4.1 / 双部署等价 URL

每篇文章有两个 canonical URL，内容完全一致：

```
GitHub Pages:    https://fxp.github.io/AI-Buzzwords/<path>
Cloudflare/xpf:  https://xiaopingfeng.com/blog/ai-buzzwords/<path>
```

**对外分享一律使用 xpf 域名**（短、自有、可版本化通过 `?v=N`）。GitHub URL 留作备份和工程使用。

### 4.2 / 文章 URL 格式

| URL | 指向 | 用途 |
|---|---|---|
| `…/blog/ai-buzzwords/` | 首页 | 总入口 |
| `…/blog/ai-buzzwords/deepdive/<slug>/` | topic 门面（resolve 到 index.html） | 系列首选 |
| `…/blog/ai-buzzwords/deepdive/<slug>/<file>.html` | 具体文章 | 直链 |
| `…/blog/ai-buzzwords/viewer.html?f=deepdive/<slug>/<file>.md` | markdown viewer 包装 | 所有 .md 必须走这个 |
| `…/blog/ai-buzzwords/deepdive/<slug>/<file>.en.html` | 英文版 | 自动翻译 |

### 4.3 / 永远不要做的事

- ❌ 直链 `.md`：`.../<file>.md` → 浏览器渲染为裸文本。必须包 `viewer.html?f=...`。
- ❌ 改已上线文章的 slug：URL 一旦发出去，永不更名。
- ❌ 暴露 vault 路径（中文 / `[TAG]`）到公开 URL：所有外链都用 Layer 3 形态。

---

## 5. 迁移流程：vault → repo → URL

新文章发布 6 步：

1. **写**（vault）：在 `[TAG] 主题名/` 目录下写 `<filename>.md`。中文文件名 OK。
2. **挑 slug**（repo）：决定 lowercase-hyphen 英文 slug。在 `deepdive/` 下查重。
3. **复制**（repo）：vault 文件 → `deepdive/<slug>/<slug>.md` 或 `<slug>.html` + `<slug>-blog.md`。
4. **修路径**（repo）：vault 内的 `[TAG] 中文/` 链接 → 兄弟相对路径。`viewer.html?f=` 包所有 `.md` 链接。
5. **写 meta.json**（repo）：`first_published`、`freshness_priority`、`languages: ["zh"]`。
6. **挂首页**（repo）：在 `index.html` 加条目。

提交：`git add deepdive/<slug>/ index.html && git commit -m "..." && git push origin main`。

后续自动化（无需人工）：
- `translate.yml` 自动生成 `<slug>.en.html`
- `deploy.yml` 双部署到 Pages + Cloudflare
- `freshness-check.yml` 按 `freshness_priority` 周一巡检

---

## 6. 状态机：哪些是 enable，哪些是 Coming Soon

文章在首页可处于三种状态：

| 状态 | 含义 | 首页表现 |
|---|---|---|
| **enabled** | 完成完整 4 资产工作流 + 已审阅 | 高亮，标题可点击，跳转到文章 |
| **coming-soon** | 内容已存在仓库（archive 目录），但未完成发布工作流 | 灰色，不可点击，标 "Coming soon" |
| **draft** | 仅在 vault 里，未进 repo | 不显示在首页（外人看不见） |

状态由首页 `index.html` 的代码 gating 控制 —— 不依赖文件存在与否。

升级路径：`draft → coming-soon → enabled`，单向不可逆（除非显式下线）。

---

## 7. 已发布的 enable 列表（2026-05）

当前以下 7 个 URL 是 enabled 状态，其余皆为 coming-soon：

```
/deepdive/neolab/
/deepdive/neolab/project-deal.html
/deepdive/claude-desktop-buddy/prd.html
/deepdive/claude-desktop-buddy/protocol.html
/deepdive/labor-day-2026/
/deepdive/labor-day-2026/white-collar.html
/deepdive/labor-day-2026/rentahuman.html
```

新文章上线时增补本节，并同步更新 `index.html` 状态。

---

## 8. Design System 占位

页面样式当前还在 Design System 设计阶段。所有 enable 的页面共享同一套 dossier 风格（dark + Fraunces serif + amber/mint/signal 三色系）。

Design System 完成后会整体重排版，**不会改 URL slug**，只动样式。

详见：`AI Buzzwords Design System.md`（vault 内，未来迁出后会替换本节链接）。

---

## 9. 相关文档

- `LESSONS_LEARNED.md` — 经验沉淀（构建过程中踩的坑）
- `CLAUDE.md` — Claude Code agent 工作手册
- `README.md` — 仓库 README（对外说明）
- vault `CLAUDE.md` — vault 端 agent 指针
