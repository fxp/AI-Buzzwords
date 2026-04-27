# AI Buzzwords · DeepDive

AI 趋势研究笔记与可视化页面的公开归档。

## 已发布

### NEO LAB
- [№ 01 / ANDON LABS · 自主组织的前夜](deepdive/neolab/index.html) — [深度报告](https://fxp.github.io/AI-Buzzwords/viewer.html?f=deepdive/neolab/report.md)
- [№ 01 · Appendix A / PROJECT DEAL · 看不见的不平等](deepdive/neolab/project-deal.html)

## GitHub Pages

线上访问： https://fxp.github.io/AI-Buzzwords/

## 约定：Markdown 文件通过 viewer 渲染

所有部署到 GitHub Pages 的 `.md` 文件**统一通过 `/viewer.html?f=<相对路径>` 访问**，不要直链 `.md` 文件。

`viewer.html` 是基于 [marked](https://github.com/markedjs/marked) + [highlight.js](https://github.com/highlightjs/highlight.js) + [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) 构建的通用 Markdown 阅读器，支持：

- GFM（表格、任务列表、删除线、自动链接）
- 代码语法高亮（明暗自动切换）
- GitHub 原生外观 + 暗色模式
- 自动生成目录、滚动高亮、阅读时长
- 文档内 `.md` 链接会自动改写走 viewer

**示例**： `viewer.html?f=deepdive/neolab/report.md`

新增 markdown 时，在 `index.html` 的入口列表里加上 `viewer.html?f=路径` 链接即可。
