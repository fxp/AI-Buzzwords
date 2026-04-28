# AI Buzzwords · DeepDive

AI 趋势研究笔记与可视化页面的公开归档。

## 已发布

### NEO LAB
- [№ 01 / ANDON LABS · 自主组织的前夜](deepdive/neolab/index.html) — [深度报告](https://fxp.github.io/AI-Buzzwords/viewer.html?f=deepdive/neolab/report.md)
- [№ 01 · Appendix A / PROJECT DEAL · 看不见的不平等](deepdive/neolab/project-deal.html)

## GitHub Pages

线上访问： https://fxp.github.io/AI-Buzzwords/

## 约定：Markdown 文件通过 viewer 渲染

仓库里**任何位置**的 `.md` 文件都可以通过 `/viewer.html?f=<相对路径>` 在线访问。永远走 viewer，不要直链 raw `.md`。

`viewer.html` 基于 [marked](https://github.com/markedjs/marked) + [highlight.js](https://github.com/highlightjs/highlight.js) + [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) 构建，支持：

- GFM（表格、任务列表、删除线、自动链接）
- 代码语法高亮（明暗自动切换）
- GitHub 原生外观 + 暗色模式
- 自动生成目录、滚动高亮、阅读时长
- 文档内 `.md` 链接会自动改写走 viewer
- 路径白名单（拒绝 `..` 和外部协议）

**示例**：

```
https://fxp.github.io/AI-Buzzwords/viewer.html?f=deepdive/neolab/report.md
https://fxp.github.io/AI-Buzzwords/viewer.html?f=任意/路径.md
```

## 发布新的 markdown

用 `scripts/publish-md.sh` 一行搞定（复制 → 提交 → 推送 → 打印 viewer URL）：

```bash
# 默认放到 deepdive/<filename>/<filename>.md
scripts/publish-md.sh ~/Documents/foo.md

# 指定子目录
scripts/publish-md.sh "/path/to/source.md" deepdive/neolab
```

发布后把脚本输出的 viewer URL 加到 `index.html` 的入口列表，方便首页导航。
