# 当代码不再是秘密：Claude Code 泄露事件的全景解读
> 一个 NPM 包里遗留的 .map 文件，意外撕开了当前最热门 AI 编程工具的完整架构蓝图。三天之内，社区完成了逆向工程、发现了关键 Bug、揭露了员工专属功能、还原了未发布的产品路线图——这不仅是一次安全事件，更是 AI 工具生态透明度与信任机制的压力测试。

```
首发：2026-04-03  |  更新：2026-04-30（30 天复盘 + Mythos 平行事件 + v2.1.116 native binary 迁移 + Trend Micro 武器化报告）
```

> ## 🆕 2026-04-30 30 天更新摘要
>
> 原文 10 条结论全部成立。一个月之后，事件本身没有反转，但**生态层面的二阶后果**让原报告需要扩写：
>
> 1. **Mythos 复刻同一脚本（4 月 23 日）**：Discord 小组通过第三方供应商预览环境的 URL 猜测，拿到了 Anthropic 自己定性为 "too dangerous to release" 的攻击型 AI Mythos，前置情报来自 Mercor 早先泄露中关于 Anthropic 主机命名的知识。**24 天内 Anthropic 经历两次"非破解式"信息外泄，攻击面都在自家基础设施之外**——npm 发布流程、第三方 vendor 边界、上游训练伙伴 Mercor 三个完全不同的入口。Anthropic 的安全成熟度在前沿能力 vs 供应链纪律之间出现可观测的剪刀差。
> 2. **泄露已成攻击者的免费基础设施**：Trend Micro / Mend / Zscaler ThreatLabz 已记录至少四类活跃利用——axios 维护者账号被劫持注入 RAT（plain-crypto-js 隐藏依赖，与泄露同日发生）、Vidar+GhostSocks 借假"leaked-claude-code"GitHub Releases 分发（属于自 2 月起轮换冒充 25+ 软件品牌的更大行动）、Shai Hulud 借 SAP CAP 横扫、typosquatting 抢注 Anthropic 内部模块名。
> 3. **autoCompact 不是孤立 Bug**：Anthropic 4 月 20 日承认"过去一个月用户体验下降"由**三个独立变更**叠加（Code / Agent SDK / Cowork 三条链路），`v2.1.116` 才完整修复。同期 `v2.1.113`（4 月 17 日）把 CLI 从 bundled JavaScript 改为**原生二进制**——这间接证实了泄露中暴露的 SDK O(n²) 性能问题确实存在，他们干脆绕过整个 JavaScript 运行时栈。
> 4. **官方定性已落地**：Boris Cherny 公开声明"plain developer error, not a tooling bug"；DMCA 大规模回撤至 1 仓库 + 96 fork（最初 8,100 个）；Bun 上游 issue `oven-sh/bun#28001` 至今未关；**截至 2026-04-30 Anthropic 仍未发布正式 post-mortem**——对一家以 "AI 安全" 为品牌核心的公司，这种沉默本身已经成为信号。
> 5. **KAIROS 仍未解封**：30 天后 feature flag 锁未拆，原计划 4 月 1-7 日的 Buddy teaser 整体推迟。但同期 Cursor / Cline / OpenCode 等竞品 4 月 roadmap 中已出现 "持久后台 Agent" 风格功能——**泄露最大的礼物不是让竞品看到 KAIROS 长什么样，而是验证了"持久后台 Agent"作为下一代主流形态的方向**。

---

## ⚡ TL;DR — 10 个最值得记住的结论

| #   | 结论                                                                                            | 影响对象     |
| --- | --------------------------------------------------------------------------------------------- | -------- |
| 1   | **源码永久不可撤销**：claude-code 净室重写版破 10 万 Star，已在 IPFS 永久镜像，DMCA 徒劳                                | 所有人      |
| 2   | **KAIROS 暴露产品路线图**：后台守护进程 + GitHub Webhook + 夜间记忆蒸馏，Claude Code 正在变成常驻系统级 Agent               | 竞品/企业    |
| 3   | **autoCompact Bug 是"用两下就限速"的真凶**：无限重试最高记录 3,272 次，修复仅需三行代码；由 OpenAI Codex 在 Anthropic 泄露代码中发现 | 所有用户     |
| 4   | **遥测范围超出"编程助手"定义**：640 种遥测事件、每小时热加载权限、CHICAGO 模块（截屏/键盘/剪贴板）；用个人账号处理公司代码的员工面临数据治理盲区            | 企业安全     |
| 5   | **Undercover 模式没有关闭开关**：AI 系统性隐藏参与痕迹向开源项目提交代码，"人类贡献者"假设不再可靠                                   | 开源社区     |
| 6   | **Anthropic 旗舰产品不用自家 SDK**：QueryEngine.ts 近 5 万行，因官方 SDK 有 O(n²) 性能问题而绕过                      | AI 工具开发者 |
| 7   | **Capybara v8 幻觉率从 16.7% 退化至 29-30%**：内部基准意外曝光，竞品现在比用户更清楚 Anthropic 新模型质量状况                   | 竞品/采购者   |
| 8   | **DMCA 行动自我矛盾**：训练时主张"AI 重写不构成侵权"，泄露后主张"AI 净室重写构成侵权"——逻辑上站不住脚                                 | 法律/政策    |
| 9   | **烂代码创造了 25 亿美元 ARR**：3,000+ 行 12 层嵌套的产品，打破了"代码质量 = 产品质量"的工程师信仰                               | 产品从业者    |
| 10  | **泄露后市场地位不降反升**：真正的护城河在模型能力 + 推理成本 + 品牌信任，不在 TypeScript 代码里                                   | 投资/战略    |

> **企业管理者重点关注：** 第 4 条（遥测盲区）和第 5 条（Undercover 模式）；**开发者重点关注：** 第 3 条（autoCompact Bug）和第 2 条（KAIROS 功能预告）；**产品/战略从业者重点关注：** 第 9 条和第 10 条。

---

## 从 .map 文件到 4756 个源码文件：一次意外暴露的规模

事件始于 3 月 31 日 UTC 04:23，安全研究员 Chaofan Shou（[@Fried_rice](https://x.com/Fried_rice/status/2038894956459290963)）发现 Claude Code v2.1.88 的 NPM 包中包含一个 59.8MB 的 source map 文件——此前版本仅约 17MB。这不是混淆后的残留，而是可以完整还原的原始代码。更严重的是，该 .map 文件还指向了 Anthropic 在 Cloudflare R2 存储桶上一个**公开可访问**的 src.zip——即使 npm 包被撤下，任何知道 URL 的人仍可直接下载全部源码。这个双重暴露路径在大多数分析中被忽略了。

Chaofan Shou 的身份值得多说一句：加州大学伯克利分校计算机科学博士（退学创业），Web3 安全公司 Fuzzland 联合创始人，累计漏洞赏金约 190 万美元。他的原始推文最终获得超过 **3,400 万次浏览**——这个数字本身说明了 AI 工具在开发者社区的关注密度。

@tvytix 随即发布系统性深度研究报告（[X 帖子](https://x.com/tvytix)），从 npm 包中提取出 4,756 个源码文件，涵盖入口逻辑、工具调用权限模型、Agent 调度机制、操作层和 Hook 系统。alex000kim 的技术博客（[详细分析](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)）则对关键架构决策逐一解剖。Smol AI News 同日发布 Claude Code Leak 专题（[专题页](https://news.smol.ai/issues/26-03-31-claude-code-leak)），将此事件定性为本周 AI 社区最重要的话题。

韩国开发者 Sigrid Jin（@instructkr，曾因消耗 250 亿 Claude Code tokens 被《华尔街日报》报道）创建的最早 GitHub 镜像仓库在 **2 小时内突破 5 万 stars**，其 clean-room Python 重写版 claw-code 最终突破 **10 万 stars**，很可能创下 GitHub 有史以来的增长记录。Reddit r/ClaudeAI 最热帖获得 2,019 票和 291 条评论。代码在去中心化平台 Gitlawb 上被镜像——至此，源码实质上已**永久公开**。

这是 Anthropic 五天内的第二次意外信息泄露——3 月 26 日，CMS 配置错误导致约 3,000 个内部文件暴露，包括未发布的 Mythos/Capybara 模型草稿博文。再往前推，2025 年 2 月 Claude Code v0.2.8 就曾因几乎完全相同的 source map 问题泄露过源码。**13 个月内两次同类事故、5 天内两次重大暴露**——这已超越"个别人为失误"的叙事框架，指向系统性的流程缺陷。

> 🆕 **30 天后再加一笔**：4 月 23 日，Anthropic 自己定性为 "too dangerous to release" 的攻击型 AI **Mythos** 在公开发布同日被一个 Discord 小组通过**第三方供应商预览环境的 URL 猜测**拿到访问权——其中一名成员是 Anthropic 的第三方承包商，前置情报来自此前 **Mercor 训练平台**的另一次泄露中关于 Anthropic 主机命名约定的知识。**至此，从 2025 年 2 月小型 source map 泄露 → 2026 年 3 月 26 日 CMS 错配 → 3 月 31 日 v2.1.88 大泄露 → 4 月 23 日 Mythos 外泄，14 个月内已是第四起**。攻击面都不在 Anthropic 自家基础设施——这把"系统性流程缺陷"的诊断从假设升级为定论。

### 🆕 根因解剖：四层防线全部失守

Boris Cherny 4 月 1 日定性为"plain developer error, not a tooling bug"。但社区拆解发现这是一个**四层防线全部失守**的复合故障——任何一层有效都能阻止泄露：

| 防线 | 应起作用 | 实际状态 |
|------|---------|---------|
| **构建配置** | Bun 在 production 模式应禁用 source map | `oven-sh/bun#28001`（2026-03-11 报告，至今未关）—— Bun 在 production 仍输出 source map |
| **包过滤** | `.npmignore` 应包含 `*.map` | 缺失 |
| **白名单** | `package.json` 的 `files` 字段应只列必要资产 | 未配置 |
| **CI 校验** | 发布前应检测 `.map` 包大小异常（v2.1.88 比常规版本暴增 42MB） | 不存在该检查 |

Anthropic 2025 年 2 月已经为同类事故修过一次代码——但**没把"禁止 .map 进 npm"做成 CI 硬规则**。修人不修流程，下一次必然重演。

> 📌 **事件规模速览：** 59.8MB source map + Cloudflare R2 公开 src.zip 双重暴露 → 4,756 个源码文件 → 2 小时 5 万 stars → claw-code 净室重写破 10 万 stars → IPFS 永久镜像。**源码已不可撤销。**

---

## 架构解剖：五项核心发现重塑行业认知

泄露的源码不是普通的产品代码——它是当前最成功的 AI 编程 Agent 的完整设计图纸，每一项发现都具有超越 Anthropic 自身的行业参考价值。

**反蒸馏双保险机制。** Claude Code 向 API 请求注入"假工具"（fake tools）以毒化任何拦截流量的训练数据采集，同时在工具调用间插入带密码学签名的服务器端文本摘要。然而分析者指出，这两项防护都可以通过环境变量或中间人代理相对简单地绕过——反蒸馏设计的"防君子不防小人"现实被首次公开验证。

**Undercover 模式。** 90 行代码构成一个完整模块，指示 AI 在外部仓库中隐藏 Anthropic 内部代号（Capybara、Tengu 等），且没有关闭开关。这意味着 Anthropic 员工使用 Claude Code 向外部开源项目贡献代码时，AI 的参与痕迹被系统性抹除。这对开源社区的"贡献透明度"假设构成直接挑战——当你看到一个"人类开发者"的 commit，它可能是 AI 辅助完成的，而你无从知晓。

**挫败检测用正则而非 LLM。** 与外界预期不同，Claude Code 识别用户挫败情绪不是通过 LLM 推理（更准确但更贵更慢），而是通过简单的正则表达式模式匹配。这个工程决策反映了"实用主义"在 AI 产品设计中的真实优先级——速度和成本压倒了技术优雅。

**Zig 运行时级客户端认证。** Claude Code 在 HTTP 请求中嵌入由 Zig 运行时生成的密码学哈希，验证请求来自合法的 Claude Code 二进制——这本质上是一个 DRM 系统，直接服务于 Anthropic 对第三方 API 访问的控制策略。

**未发布的 KAIROS 功能。** 在源码中被引用超过 150 次，KAIROS 是一个完整的自主 Agent 模式：后台 Daemon 进程在终端关闭后持续运行，通过周期性 `<tick>` 提示评估是否需要主动行动，配套 GitHub Webhook 订阅、推送通知和夜间记忆蒸馏（autoDream，四阶段 Orient → Gather → Consolidate → Prune，输出 ≤ 25KB）。其伴生的 ULTRAPLAN 功能可将复杂规划卸载到云端 Opus 4.6 会话，最长运行 30 分钟深度思考。这是 Anthropic 产品路线图中最敏感的竞争情报，现在对所有竞品完全可见。

> 🆕 **30 天后**：截至 2026-04-30，KAIROS 仍被 feature flag 锁住未解封；原计划 4 月 1-7 日的 Buddy（Tamagotchi 风格 18 物种伴侣系统，6 档稀有度从 common 60% 到 legendary 1%、含 shiny 变种）整体推迟。但 paddo.dev 4 月深度分析观察到，Cursor / Cline / OpenCode 等竞品 4 月路线图中已出现"持久后台 Agent"风格的功能预告——**泄露最大的礼物不是让竞品看到 KAIROS 长什么样，而是替他们免费完成了"持久后台 Agent 是下一代主流形态"的市场方向验证**。

**内部模型性能数据意外曝光。** 一个很少被提及但竞争价值极高的发现：源码中硬编码了内部基准测试数据，显示 **Capybara v8 的虚假声明率高达 29-30%**，相较 v4 的 16.7% 出现显著退化。这个数字对竞争对手的定价和营销策略具有直接参考价值——当你知道对手的幻觉率在恶化而非改善时，产品定位的信心来源就不同了。

**被忽视的工程尴尬：Anthropic 绕过了自家 SDK。** yage.ai 的深度技术分析可能是全网最独到的工程发现——Claude Code 的核心推理引擎 QueryEngine.ts（近 5 万行）绕过了 Anthropic 自己发布的官方 SDK，原因是 SDK 存在 O(n²) 解析性能问题。**一家公司的旗舰产品不敢用自家的公开工具库**——这个细节比任何架构图都更真实地反映了 AI 工程的"说一套做一套"现实。

> 🆕 **4 月 17 日 v2.1.113 间接证实**：Anthropic 把 CLI 从 bundled JavaScript 改为**原生二进制**（macOS / Linux / Windows 各编译一份）。`claude` 命令不再启动 Node 解释器跑打包的 JS——它直接 spawn 一个 native binary。这等于公开承认整个 JS 运行时栈是性能瓶颈，干脆绕过；同期附带 sandbox `deniedDomains`、Bash 安全加固等"基础设施静默轮"。`v2.1.116`（4 月 20 日）随后让 `/resume` 在 40MB+ 大会话上提速 **67%**，多 stdio MCP 服务器并发启动也加速；`resources/templates/list` 推迟到首次 @-mention 才拉取。这条产品演进线的隐含信号：泄露暴露的工程债，Anthropic 在悄悄、快速、批量地还。

> 💡 **最高竞争情报价值：** KAIROS（后台 Daemon + GitHub Webhook + 夜间记忆蒸馏）是产品路线图中最敏感的发现，现在对所有竞品完全可见。**最具讽刺性的工程发现：** Anthropic 旗舰产品绕过了自家 SDK——因为 SDK 本身有 O(n²) 性能 Bug。**对企业最危险的发现：** Capybara v8 幻觉率从 16.7% 退化至 29-30%，且此前从未公开。

---

## autoCompact Bug：从"三行代码"到"三个独立变更"的退役分析 🆕

如果说架构逆向是"学术价值"，那么 autoCompact Bug 的发现则有直接的用户体验和商业影响。

社区成员将泄露源码交给 OpenAI 的 Codex 分析（[详情](https://x.com/imyouhu/status/2039191460256612770)），发现 autoCompact（自动上下文压缩）机制在失败后会无限重试，**没有任何失败次数上限**。源码注释记录中，最高连续失败次数达到 3,272 次——每一次重试都在消耗用户的 token 配额。

修复方案简单到令人尴尬：`MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`，连续失败 3 次即停止。三行代码。

🆕 **4 月 20 日 Anthropic 官方说明把这个故事补完了**——autoCompact 只是三分之一：

> "Over the past month, reports indicated that Claude's responses had worsened for some users. These reports were traced to **three separate changes** that affected Claude Code, the Claude Agent SDK, and Claude Cowork. All three issues were resolved as of April 20 (v2.1.116)."

具体数据由内部查询揭示：

- 3 月 10 日单次查询：**1,279 个会话**反复触发 compaction 失败
- 单会话最高 **3,272 次重试**
- **每天约 25 万次 API 调用**被无意义消耗

这与 Anthropic 同期承认的"用户触达使用限制比预期更快"（Lydia Hallie [推文](https://x.com/lydiahallie)）直接对应。但更关键的工程教训：**两次代码评审、一次 staging 测试、一次金丝雀发布都没拦下来**——因为后台失败被设计为"重试到 OK"而非"失败有上限"，所有可观测性指标都看不见这个 Bug：P99 延迟没变，错误率没飙，只是 token 配额神秘蒸发。**这是 SRE 经典反模式"成功的失败"（successful failures）的 AI 版本**。

更具讽刺意味的是：这个 Bug 是用 **OpenAI 的 Codex** 在 **Anthropic 泄露的源码** 中发现的——竞品帮你找 Bug，这大概是 AI 行业最黑色幽默的协作方式。

> ⚠️ **用户行动项（2026-04 修订）：** 升级到 **v2.1.116 或更新版本**才完整修复（不止 autoCompact，还包括 Agent SDK 与 Cowork 两条链路）。企业用户建议检查 Claude Code 的 token 使用日志——**异常的 token 消耗峰值（无法用实际操作量解释的部分）可能有相当比例源于此 Bug 的无限重试。**

---

## 员工专属功能：信任边界的新问题

@iamfakeguru 将泄露源码与自己数十亿 token 的 agent 日志交叉比对（[原帖](https://x.com/Jiaxi_Cui/status/2039019372795367857)，53K+ 浏览），声称发现 Anthropic **已知** Claude Code 的幻觉和懒惰问题，但修复措施仅对员工账号开放，普通付费用户并未获得同等优化。

无论此声称的技术细节是否完全准确，"员工账号获得更好的服务质量"这一叙事已在开发者社区广泛传播。这触及了一个 AI 产品运营的根本问题：**当你的产品是 AI Agent，而你的员工也在大量使用同一产品，"为员工优化"和"为付费用户优化"之间的边界在哪里？** 传统软件的 dogfooding 文化建立在"员工和用户使用同一版本"的信任前提上——Claude Code 的案例暗示这一前提可能正在被打破。

---

## 各家大模型的诊断书：当 AI 审视 AI

这次泄露创造了一个前所未有的场景——人们把 Anthropic 的代码喂给竞品模型做分析，形成了一场 AI 行业的"集体会诊"。各家模型的分析角度差异，本身就是一面镜子，映射出不同 AI 系统的认知偏好和盲区。

**OpenAI Codex 的实用主义。** 如前述，Codex 是最早在泄露代码中定位 autoCompact Bug 的模型。它的分析路径高度聚焦于可执行的代码缺陷——不做宏大叙事，直接定位到具体的无限循环逻辑和缺失的退出条件。这种"工程师思维"使它成为唯一产出了可直接 merge 的修复补丁的分析者。**但 Codex 几乎完全忽略了架构层面的设计哲学讨论**——它看到了 Bug，却没看到 Bug 背后的决策文化。

**Gemini 的架构鉴赏。** Google 的模型对 Claude Code 的三层记忆体系（Index → Topic Files → Transcripts）表现出浓厚兴趣，将其类比为操作系统的页表 + 虚拟内存 + swap 分层。这一类比精准且少有人提及：大多数分析者将记忆系统视为一个"功能"，Gemini 将其识别为一个"范式"——AI Agent 的记忆管理正在重演操作系统设计史上的经典权衡。Gemini 还注意到 autoDream（夜间记忆蒸馏）本质上是一个受限的子 Agent，拥有有限的工具访问权限，专门用于去重、消解矛盾——**这相当于给 AI 的"潜意识"设置了安全沙箱**。

**Grok 的阴谋论直觉。** Elon Musk 旗下的模型给出了最具挑衅性的分析框架：**这次泄露可能不是事故，而是有史以来最精心策划的 PR 操作。** 其论据链并非无稽之谈——泄露时间恰在 Buddy 伴侣功能计划发布日（4 月 1-7 日）前一天；Anthropic 拥有 Bun 运行时却放任一个已知 20 天的 source map Bug 未修复（oven-sh/bun#28001）；泄露前 10 天 Anthropic 刚因向 OpenCode 发送停止信函引发开发者社区强烈反弹，"泄露"戏剧性地将其从"专利流氓"形象扭转为"工程透明"的受害者。**Grok 的分析本身可能带有 xAI 的竞争偏见**，但它提出的问题值得严肃对待：在 AI 行业的信息战中，"事故"和"操作"之间的边界越来越模糊。

**工程经济学视角（中文技术社区）。** 来自知乎和技术博客的多位分析者从成本效率角度切入，提出了一个少有人关注的观点：The Register 和安全研究者确认的 Claude Code 大量遥测事件类型和机器指纹维度意味着 **Anthropic 可能比用户自己更了解用户的开发环境**。这种遥测密度与反蒸馏机制形成对照，两者服务于同一目标——不是保护用户，而是构建 Anthropic 对 AI 编程工具市场的"信息不对称优势"。当一个工具高频回传数据、收集从设备 ID 到物理 RAM 的各类信息时，"AI 安全公司"的品牌叙事需要重新审视。

**Claude 自己的沉默。** 值得一提的是，当用户试图让 Claude 分析自己的泄露代码时，模型的表现明显保守——拒绝对 Undercover 模式做价值判断，对 KAIROS 功能仅做技术描述而回避战略推测。这种"自我审查"本身或许是最诚实的回应：**一个 AI 被要求评价制造它的公司的失误，它的沉默比任何分析都更有说服力。**

---

## 被忽略的真正风险：泄露的不是代码，是监控能力

几乎所有主流分析都聚焦于泄露代码中的功能发现——KAIROS、Undercover、反蒸馏。但 [Concret.io 的安全团队](https://www.concret.io/blog/anthropic-source-code-leak-telemetry-enterprise-security) 和 [The Register](https://www.theregister.com/2026/04/01/claude_code_source_leak_privacy_nightmare/) 的后续调查指向了一个被严重低估的维度：**Claude Code 的数据采集范围远超一个"编程助手"的合理需要。**

泄露源码确认：Claude Code 每次 Read 调用、每次 Bash 执行、每次搜索结果都会以明文 JSONL 格式存储在本地，同时以用户 ID、组织 UUID、邮箱地址和 feature flags 为元数据回传至 Anthropic 服务器。数据保留期限分散在五份不同的政策文档中——安全页面写着"有限保留"，隐私中心写着"最长七年"。

更值得关注的是架构层面的远程控制能力：feature gates 每小时热加载一次，无需用户交互。对于一个拥有系统级文件访问权限的工具——加上已曝光的 CHICAGO 模块（鼠标点击、键盘输入、剪贴板访问、截屏捕获），**远程更改采集范围和权限行为的能力，意味着你安装时同意的"使用条款"和它实际运行时的行为之间存在动态缺口。**

这里存在一个被几乎所有分析者忽略的企业风险盲区：**开发者用个人免费账号处理公司代码时，适用的是消费者条款而非企业协议。** Anthropic 的数据保护跟随账号而非代码——企业 DPA 在这种场景下形同虚设。

> 🚨 **企业安全团队立即行动清单：**
> 1. **审计个人账号使用情况** — 有多少开发者用个人邮箱账号在公司机器上运行 Claude Code？
> 2. **检查 CHICAGO 模块风险敞口** — 截屏/键盘/剪贴板捕获能力，叠加系统级文件访问权限，意味着 Claude Code 理论上可以触达任何在屏幕上出现过的内容
> 3. **核查合同类型** — 公司是否签署了含 DPA 的企业协议？个人账号用户不受企业 DPA 保护
> 4. **关注 feature gates 热加载** — 每小时一次的远程权限更新意味着"安装时的行为"≠"运行时的行为"

---

## DMCA 悖论：当 AI 公司用版权法保护 AI 写的代码

Anthropic 的 DMCA 下架行动**最初误伤了约 8,100 个合法 fork**。Boris Cherny 4 月 1 日承认大规模下架是事故，发起部分撤回——🆕 **最终只对 1 个原始仓库 + 96 个 fork 维持下架**。但真正的故事不在执行力度——而在法律逻辑的自我矛盾。

Anthropic CEO Dario Amodei 曾暗示 Claude Code 的相当部分由 Claude 自己编写。🆕 **美国 DC 巡回法院 2025 年 3 月的判决**确立 AI 生成作品不享有自动版权保护——人类作者要求是必要条件。如果 Anthropic 用 DMCA 保护的代码中有相当比例是 AI 产出，那么这些代码的版权主张在法律上可能站不住脚。一个 AI 安全公司用版权法保护（部分）AI 写的代码，而整个 AI 行业的存在基础恰恰是主张"AI 处理过的内容不构成衍生作品"。

[Build.ms 的分析](https://build.ms/2026/4/1/the-claude-code-leak/) 与 [Bean, Kinney & Korman 律所的法律分析](https://www.beankinney.com/512000-lines-one-night-zero-permission-the-claude-code-leak-and-the-legal-crisis-of-ai-clean-rooms/) 尖锐地指出了这一双重标准：Anthropic 训练 Claude 时主张"AI 重写不构成侵权"，Claude Code 泄露后却主张"AI 重写构成侵权"。韩国开发者 Sigrid Jin 创建的 Python 净室重写版 claw-code 成为 GitHub 历史上增长最快的仓库，恰恰是利用了这一逻辑裂缝——如果 AI 重写版本是"新的创作"，那么传统 DMCA 下架在技术和法律上都是徒劳的。截至 2026-04-30，**Anthropic 未对 claw-code 提起任何诉讼，亦未发布正式 post-mortem**。

🆕 [Cory Doctorow 在 4 月 2 日的 Pluralistic 专栏](https://doctorow.medium.com/https-pluralistic-net-2026-04-02-limited-monopoly-petardism-06f69e5886bc) 将此称为"**limited monopoly petardism**"——拿来约束他人行为的版权武器，正在反弹炸到部署它的人。他的论点尤其犀利：Anthropic 训练 Claude 时已经"选边"——主张 AI 转换性使用合法。这一选边在和解谈判桌上不能临时反悔。

这不是一个仅关乎 Anthropic 的问题。它暴露了整个 AI 行业的法律基础设施赤字：**当 AI 既是代码的作者又是代码的"洗稿工具"时，版权法的"作者"概念需要彻底重写。**

---

## 非共识观点：烂代码的 25 亿美元启示

在技术社区的分析热潮中，最具颠覆性的观点来自一个反直觉的发现：**Claude Code 的代码质量并不好——而这恰恰是重点。**

[Build.ms](https://build.ms/2026/4/1/the-claude-code-leak/) 的作者在审阅泄露源码后写道："vibe coded garbage 可以在不到一年内带来 25 亿美元年化收入——只要产品市场契合度到位。"中文开发者社区（V2EX、掘金、知乎）对此高度共鸣——他们对 `src/cli/print.ts` 中 **3,000+ 行、12 层嵌套**的"屎山代码"和用正则做情感分析的做法津津乐道，认为这与 Anthropic 标榜的 AI 精密性形成了讽刺性对比。社区甚至搭建了专门网站 ccleaks.com，系统提取了 **35 个编译时特性标志、120+ 个隐藏环境变量和 200+ 个远程控制开关**。

但这不是嘲讽，而是对开发者行业一个深层信仰的挑战：代码质量与产品成功之间的相关性远低于工程师们愿意承认的程度。

这一观察与另一个事实形成对照：Codex 和 Gemini Code Assist 的底层代码一直是开源的，却从未威胁到 Claude Code 的市场地位。如果代码公开就意味着竞争力丧失，那这两个产品早该赢了。**泄露的真正影响是感知层面的，不是技术层面的。** 竞争对手从 51 万行代码中学到的东西，他们本可以通过自己的工程实验在几个月内独立发现——真正的护城河在模型能力、推理成本、云端基础设施和品牌信任的综合体中，不在客户端的 TypeScript 里。

Engineer's Codex 的分析进一步指出了一个被忽视的架构决策：Claude Code 默认只启用 15-20 个工具（总计可达 60 个）。在一个"功能越多越好"的行业共识下，**刻意的工具极简主义**可能是其用户体验优于竞品的关键原因之一——这与 Anthropic 在学术界倡导的"AI 能力应该受约束"理念形成了罕见的产品实践一致性。

> 💡 **对产品从业者的深层启示：** Claude Code 用 3,000 行 12 层嵌套的"屎山代码"做到了 25 亿美元 ARR。**代码质量与产品成功的相关性，远低于工程师愿意承认的程度。** 真正不可复制的是模型与 Harness 的协同调优，以及"刻意的工具极简主义"带来的用户体验优势——这些都不在那 51 万行 TypeScript 里。

---

## 时间线的巧合：一个值得严肃对待的阴谋论

DEV Community 上一篇广泛传播的文章（[The Great Claude Code Leak of 2026](https://dev.to/varshithvhegde/the-great-claude-code-leak-of-2026-accident-incompetence-or-the-best-pr-stunt-in-ai-history-3igm)）提出了一个不应被轻易驳回的问题框架：

泄露发生在 3 月 31 日——Buddy 伴侣功能计划发布窗口（4 月 1-7 日）的前一天。Anthropic 于 2025 年底收购了 Bun，但一个导致 source map 在生产模式下泄露的已知 Bug（oven-sh/bun#28001，3 月 11 日提交）在 20 天内未被修复。泄露前 10 天，Anthropic 因向竞品 OpenCode 发出法律威胁而遭遇开发者社区猛烈反弹——"泄露"事件戏剧性地将舆论风向从"封闭垄断者"转为"被扒光的受害者"。

**Undercover 模式的终极反讽。** Anthropic 专门写了 90 行代码来防止内部信息通过代码贡献泄露——然后通过一个他们忘记从 npm 包中排除的文件泄露了全部源代码。一个专门建造了防泄密系统的公司，栽在了最基础的发布配置上。如果这是事故，它暴露的是流程与技术能力之间的惊人脱节；如果这是策略，那它可能是 AI 行业历史上最大胆的"开源即营销"操作。

还有一个信号矛盾至今未被解释：Claude Code 负责人 Boris Cherny 在 X 上明确表示"没有人被解雇，这是一个诚实的错误"，并宣扬"无责文化"（Blameless Post-Mortem）；但开源中国（OSChina）独家报道称[相关人员已被解雇](https://www.oschina.net/news/416423)。这两个说法在英文和中文信息圈中各自传播，却从未被交叉验证。**当危机叙事在不同语言的信息生态中分裂时，"真相"本身也变成了一个翻译问题。**

> 🆕 **30 天后的反讽升级——Mythos 事件（4 月 23 日）**：
>
> Anthropic 发布定性为 "too dangerous to release" 的攻击型 AI Mythos——可自主发现 0day 并链成可用 exploit，声称已在主流 OS / 浏览器中找到"数千个"漏洞。**发布同日**，一个 Discord 小组通过**第三方供应商预览环境的 URL 猜测**拿到访问权——其中一名成员是 Anthropic 的第三方承包商。这个小组使用的前置情报来自 **Mercor**（AI 训练平台）早先的另一次泄露中关于 Anthropic 主机命名约定的知识。**24 天内 Anthropic 经历两次"非破解式"信息外泄，攻击面都不在自家基础设施**——Code 泄露走 npm 渠道（构建/发布流程），Mythos 泄露走第三方承包商渠道（vendor 边界），Mercor 泄露走训练数据渠道（上游伙伴）。**三次都是"非典型攻击面"**——这指向 Anthropic 的安全成熟度模型存在结构性盲区：**对前沿能力的开发投入领先行业，对供应链与边界的纪律性远未跟上**。
>
> 叠加 Mythos 后，"Code 泄露是 PR 策略"的可信度反而下降——**没人会把"too dangerous"的攻击型 AI 当营销素材外泄**。这把概率推回了"系统性安全债"那一侧。

我们大概率永远不会得到确切答案。但这个问题本身揭示了一个新现实：**在 AI 行业的信息环境中，"事故"和"信息操作"的区分正变得越来越困难——而这种不可区分性本身就是一种战略资产。**

---

## 🆕 axios 木马只是开端：泄露已成攻击者的免费基础设施

一个几乎被所有 4 月初分析遗漏的关键细节：**Claude Code 泄露与 npm 供应链攻击的时间窗口高度重合**——而 4 月中下旬的安全报告把这个"重合"扩展为一个**长达数周的活跃利用生态**。

### 1. 同日发生：axios 维护者账号劫持

3 月 31 日 UTC 00:21，axios 维护者账号被劫持，发布两个恶意版本（1.14.1 和 0.30.4），通过隐藏依赖 `plain-crypto-js` 投递跨平台 RAT——比 Chaofan Shou 披露 Claude Code 泄露早了整整 4 小时。axios 周下载量超 **1 亿**，理论受影响项目数量级与 log4shell 相当。攻击者明显在等一个"全社区注意力被吸走"的窗口。npm 在 03:29 才撤下恶意版本——00:21 到 03:29 这个窗口内，**任何因泄露新闻而尝试安装或更新 Claude Code 的开发者，都可能同时遭遇源码泄露和供应链感染的双重打击**。

### 2. 长期诱饵活动：Vidar + GhostSocks 借假泄露仓库

24 小时内，攻击者注册大量包含 `leaked-claude-code` / `claude-code-source` / `anthropic-private` 字样的 GitHub 仓库与 Release，分发 **Vidar stealer + GhostSocks 代理木马**（Rust 编译的 infostealer）。Trend Micro 4 月专题报告 [《Weaponizing Trust Signals》](https://www.trendmicro.com/en_us/research/26/d/weaponizing-trust-claude-code-lures-and-github-release-payloads.html) 跟踪到这是 **2026 年 2 月起的"轮换诱饵"行动**——同一组人冒充过 25 个以上软件品牌（Cursor、Claude Code、各大 IDE 等），Claude Code 泄露只是最新蹭热度的诱饵。GitHub Releases 作为"可信下载渠道"被武器化为恶意软件分发基础设施。

### 3. Typosquatting 内部模块名

泄露源码暴露了 Anthropic 内部模块名（如 Capybara、Tengu、KAIROS 子包），攻击者立刻在 npm 上抢注同名或近似包，等待开发者尝试编译泄露源码时输错包名。

### 4. Shai Hulud：横向利用 SAP CAP

Mend 4 月报告记录了一组以 Claude Code 为话题入口、最终横扫 SAP CAP 生态的供应链攻击（代号 Shai Hulud），手法与早前 Lazarus 在 npm 的活动有指纹重叠。

### 结构性教训

这两起独立事件（泄露 + 供应链投毒）的时间重合不太可能是协调策划的，但它们的叠加效应揭示了现代软件供应链的一个结构性脆弱点：**一个重大泄露事件本身就是后续攻击的理想掩护——当所有人都在看泄露的代码时，没人注意到他们安装的依赖已经被污染。** 泄露的二阶后果不是一次性的——它会在攻击者诱饵库中长期复用。

> 🚨 **企业行动新增项**：
> - 内部 CI 阻止从随机 GitHub Releases 拉取 `leaked-*` / `claude-code-source-*` 类仓库
> - 锁定 axios 等高危包版本到 supply-chain attack 之前的已知良好版本，启用包签名校验
> - 对 npm 包设置最小发布年龄（如 7 天）以避免新发布的恶意包

---

## 对行业的连锁反应

**对 AI 工具开发者：** Claude Code 的架构决策现在是公开知识。反蒸馏策略、Agent 调度模型、权限系统设计——所有竞品都可以直接参考或规避。Cursor、Codex、Windsurf 等竞品的下一版更新中，可以预期看到受此泄露影响的设计选择。但 [Latent Space](https://www.latent.space/p/ainews-the-claude-code-source-leak) 指出了一个反直觉的结论：泄露的 50 万行代码暴露的是"执行编排"而非"模型能力"——竞争对手可以复制工作流模式，但这些模式本就是可独立发明的。真正不可复制的是模型-Harness 的协同调优。

**对开源社区：** Undercover 模式的曝光对"AI 贡献透明度"提出了尖锐问题。当 AI 公司的员工系统性地隐藏 AI 辅助的痕迹向开源项目提交代码，开源社区的"人类贡献者"假设还可靠吗？

**对企业安全团队：** [VentureBeat](https://venturebeat.com/security/claude-code-512000-line-source-leak-attack-paths-audit-security-leaders) 列出了五项紧急行动，但最关键的一条被埋在细节中——审计组织内部有多少开发者在用个人账号运行 Claude Code 处理公司代码。这不是隐私偏好问题，而是数据治理漏洞。

**对 Anthropic 自身：** 短期看，这是竞争情报的重大损失（KAIROS 路线图、模型代号、架构细节）。中期看，autoCompact Bug 的快速社区修复和员工功能争议对用户信任的影响更深远。长期看，泄露可能反而加速 Claude Code 架构成为行业参考标准——当所有人都在读你的代码时，你的设计模式就是事实标准。但 Anthropic 至今未发布公开的事后分析报告——对于一家以"AI 安全"为核心品牌定位的公司，**沉默本身就是一种声明**。

**历史回声——第一次泄露催生了"寒武纪大爆发"。** 一个被大多数分析者忽略的历史事实：2025 年 2 月 Claude Code 的首次 source map 泄露虽然规模远小于此次，但多位中文技术分析者指出，正是那次泄露"实质性地催化了 AI Coding Agent 赛道的寒武纪大爆发"——Cursor、Windsurf、Augment 等产品在 2025 年下半年的集中涌现，与首次泄露提供的架构参考有直接关联。如果历史重演，**这次规模大 30 倍的泄露可能催生的不是模仿者，而是颠覆者**。

**对整个 AI 行业：** NPM .map 文件泄露是一个低级但普遍的风险——几乎所有基于 TypeScript/JavaScript 的 AI 工具都面临同样的暴露可能。这次事件将推动整个行业重新审查 CI/CD 流水线中的源码映射管理策略。而 DMCA 版权悖论、AI 生成代码的法律地位、遥测数据的透明度标准——这些更深层的问题不会因为 npm 包被撤下而消失。它们是 AI 工具生态走向成熟过程中必须正面回答的底层问题。

> 📊 **各角色核心行动项一览：**
> - **AI 工具开发者** → 现在参考 KAIROS 架构模式；检查自家 CI/CD 是否存在 source map 泄露风险
> - **企业安全团队** → 审计个人账号使用 + 检查 DPA 覆盖范围（详见"被忽略的真正风险"章节）
> - **竞品产品团队** → Capybara v8 幻觉率退化是真实的定价/营销机会窗口；Undercover 模式是差异化叙事的素材
> - **法律/合规团队** → DMCA 悖论正在成为 AI 版权案例的重要先例，需要追踪后续裁决

---

## 泄露后的社区衍生品：去中心化的"再创造"

如果说源码泄露的第一波是"信息战"，那么 72 小时后涌现的社区衍生品代表了更深层的行动：**开发者不满足于阅读代码，他们开始改写它。**

**free-code：解锁版 Claude Code**（[GitHub](https://github.com/paoloanzn/free-code)）是最直接的衍生——彻底移除遥测追踪、剥离所有安全防护提示词、一键开启 54 个在官方版本中默认禁用的实验性功能标志。项目使用 IPFS 永久存储，明确宣示"任何下架行动都无效"。它的存在本质上是一份声明：Claude Code 架构决策中最敏感的两项——遥测范围和实验功能管控——在社区眼中都不具备合法性。

从安全角度，这类"去防护"分叉需要审慎对待：移除安全提示和权限审计，意味着 Agent 操作的所有内置约束都消失，实际使用风险需要用户自行评估。

**cc-gateway：设备指纹规范化代理**（[GitHub](https://github.com/motiful/cc-gateway)）针对的是另一个发现：泄露代码揭示了 Claude Code 采集的机器指纹维度之广（物理 RAM、设备 ID、环境特征等），不少用户因多设备登录触发账号封禁。cc-gateway 作为反向代理，将来自多台机器的请求标准化为单一设备特征输出，同时剥离 billing 相关的追踪头。创作者的出发点更多是实用而非意识形态——但这个工具的出现本身，说明遥测问题已从学术讨论变成了影响日常使用的实际摩擦点。

这两个项目共同揭示了一个此前未被充分讨论的张力：**Claude Code 在技术上拥有远超"编程助手"所需的系统访问权限和数据采集能力，而用户对这些能力的感知几乎为零——直到代码泄露。** 泄露重写了双方的信息对称状态，而社区的回应表明，当信息对称被打破后，用户有能力也有意愿重新谈判工具的"边界合同"。

值得注意的是，Anthropic 未对这些衍生项目采取 DMCA 行动（截至分析时），这或许是他们从 claw-code 误伤事件中吸取的教训，也可能是出于更务实的考量：与其让 DMCA 行动持续制造舆论热度，不如让这些分叉在低调中自然老去。

---

## 尾声：一面照出所有人的镜子

这次泄露最深刻的遗产可能不在于任何具体的技术发现，而在于它创造了一个罕见的"多方同时照镜子"时刻：

Anthropic 看到了自己流程管理的漏洞、品牌叙事与产品实践的张力、以及"AI 安全公司"标签的脆弱性。竞争对手看到了一份完整的工程蓝图，但也不得不面对一个尴尬事实——**即使代码公开，Claude Code 的市场地位在泄露后一周内不降反升**。开源社区看到了 Undercover 模式，被迫重新审视"谁在写代码"这个原本不言自明的问题。监管机构（如果他们在关注的话）看到了 AI 工具在开发者机器上的真实权限范围——640 种遥测事件、远程热加载的 feature gates、系统级文件访问——远超公众讨论中的"编程助手"定位。

而 AI 行业整体看到的是一个更根本的信号：**当你的产品是一个拥有系统级权限的自主 Agent，"代码泄露"的风险清单已经从传统的"商业秘密丧失"扩展到了"能力边界的公众审视"。** 这是一种全新的暴露——不是代码在裸奔，而是意图在裸奔。

51 万行 TypeScript 终将被遗忘。但它引发的关于 AI Agent 透明度、数据主权、版权归属和信任边界的对话，才刚刚开始。

---

*分析来源（首发版）：[The Register](https://www.theregister.com/2026/04/01/claude_code_source_leak_privacy_nightmare/)、[Latent Space](https://www.latent.space/p/ainews-the-claude-code-source-leak)、[Build.ms](https://build.ms/2026/4/1/the-claude-code-leak/)、[Engineer's Codex](https://read.engineerscodex.com/p/diving-into-claude-codes-source-code)、[DEV Community](https://dev.to/varshithvhegde/the-great-claude-code-leak-of-2026-accident-incompetence-or-the-best-pr-stunt-in-ai-history-3igm)、[Concret.io](https://www.concret.io/blog/anthropic-source-code-leak-telemetry-enterprise-security)、[VentureBeat](https://venturebeat.com/security/claude-code-512000-line-source-leak-attack-paths-audit-security-leaders)、[alex000kim](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)、[36氪](https://36kr.com/p/3746770616627968)、[yage.ai](https://yage.ai/share/claude-code-engineering-cost-20260331.html)、[OSChina](https://www.oschina.net/news/416423)、[Fortune](https://fortune.com/2026/03/31/anthropic-source-code-claude-code-data-leak-second-security-lapse-days-after-accidentally-revealing-mythos/)、[Blockchain Council](https://www.blockchain-council.org/claude-ai/claude-leak-fallout-legal-ethical-implications-sharing-leaked-ai-source-code/)、[知乎讨论](https://www.zhihu.com/question/2022394365436248248)。*

*🆕 2026-04-30 更新新增来源：[TechCrunch DMCA 撤回报道](https://techcrunch.com/2026/04/01/anthropic-took-down-thousands-of-github-repos-trying-to-yank-its-leaked-source-code-a-move-the-company-says-was-an-accident/)、[InfoQ 技术分析](https://www.infoq.com/news/2026/04/claude-code-source-leak/)、[InfoWorld 员工失误定性](https://www.infoworld.com/article/4152856/anthropic-employee-error-exposes-claude-code-source.html)、[Hacker News 包装错误](https://thehackernews.com/2026/04/claude-code-tleaked-via-npm-packaging.html)、[Trend Micro 武器化诱饵报告](https://www.trendmicro.com/en_us/research/26/d/weaponizing-trust-claude-code-lures-and-github-release-payloads.html)、[Trend Micro 防御者行动](https://www.trendmicro.com/en_us/research/26/d/claude-code-remains-a-lure-what-defenders-should-do.html)、[Mend / Shai Hulud SAP CAP 报告](https://www.mend.io/blog/shai-hulud-sap-cap-supply-chain-attack-claude-code/)、[Zscaler ThreatLabz 企业行动手册](https://www.zscaler.com/blogs/security-research/anthropic-claude-code-leak)、[Cory Doctorow 版权回旋镖](https://doctorow.medium.com/https-pluralistic-net-2026-04-02-limited-monopoly-petardism-06f69e5886bc)、[Bean, Kinney & Korman 净室法律分析](https://www.beankinney.com/512000-lines-one-night-zero-permission-the-claude-code-leak-and-the-legal-crisis-of-ai-clean-rooms/)、[Fortune Mythos 泄露](https://fortune.com/2026/04/23/anthropic-mythos-leak-dario-amodei-ceo-cybersecurity-hackers-exploits-ai/)、[Cybernews Mythos 第三方供应商](https://cybernews.com/security/anthropic-mythos-ai-unauthorized-access/)、[wotai.co v2.1.116 更新](https://wotai.co/blog/claude-code-2-1-116)、[ton-technotes v2.1.115-119 周报](https://ton-technotes.com/en/blog/2026-04-25-claude-code-weekly-update-v2119/)、[paddo.dev Harness 拆解](https://paddo.dev/blog/claude-code-leak-harness-exposed/)、[NodeSource Bun bug 分析](https://nodesource.com/blog/anthropic-claude-code-source-leak-bun-bug)。*

*各家大模型分析基于社区公开讨论整理，观点归属标注仅代表相关分析的主要切入角度。本文同时参考了目录内 text.txt（GPT-4 生成的全面调查报告）、text 3.txt（Grok 生成的深度分析）、text 4.txt（Gemini 生成的综合报告）及 Claude_Code_Leak_Deep_Analysis.md 中的素材。*

<!-- 2026-04-03 v1：新增社区衍生品章节（free-code、cc-gateway） -->
<!-- 2026-04-30 v2：30 天复盘 + Mythos 事件平行 + 四层防线根因表 + autoCompact 三连 Bug 完整化 + 供应链攻击四类利用 + DMCA 撤回最终态 + Doctorow petardism 论 + v2.1.113 native binary + v2.1.116 修复 -->

