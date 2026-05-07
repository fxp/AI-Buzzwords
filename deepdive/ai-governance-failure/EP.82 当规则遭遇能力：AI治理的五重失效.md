# 当规则遭遇能力：AI治理的五重失效

> 这周发生的五件事，彼此似乎毫无关联：NSA 违规使用 Anthropic 的限制级模型、Atlassian 悄然开启数据收集、Notion 的邮箱漏洞四年未修、Claude Desktop 静默注册浏览器权限、Tesla 隐瞒数千起自动驾驶事故。但把它们放在一起，你会看到同一个模式：**每一次技术进步，都在某个监管盲区留下了一道新裂缝**。问题不是规则不够多，而是能力的扩张速度让规则永远在追赶。

---

## 技术需求压倒合规限制：NSA 与 Mythos 的矛盾

五角大楼将 Anthropic 列入"供应链风险"黑名单之后，理论上所有政府机构都应停止使用其产品。但 [Axios 的独家报道](https://www.reuters.com/business/us-security-agency-is-using-anthropics-mythos-despite-blacklist-axios-reports-2026-04-19/)揭示：NSA 内部正广泛使用 Anthropic Mythos Preview，不仅没有收敛，规模还在扩大。

这件事本身并不令人意外——政府机构绕过采购规则使用好用工具，历史上屡见不鲜。真正值得关注的是背后的逻辑：**当一个工具的能力足够强大，内部需求就会自动生成绕过限制的动机**。Mythos 能在 Linux 内核中自主发现 27 年未被发现的安全漏洞；面对这样的工具，任何安全官员都很难真正说"不"。

这个逻辑并不局限于政府。每一个企业 IT 合规团队都面临同样的张力：能力越强的工具，往往也是合规争议最大的工具。Copilot、Claude Code、Cursor——每一个都曾遭遇"禁止使用"的内部规定，每一个也都在工程师的默默使用中活了下来。

[关于 AI 战争中"人在回路"的幻觉（MIT Technology Review，Apr 16）](https://www.technologyreview.com/2026/04/16/1136029/humans-in-the-loop-ai-war-illusion/)提出了一个更深层的问题：当 AI 系统的决策速度远超人类审批速度，"人类监督"本身就成了一个仪式性存在。合规框架的设计假设人类有足够时间介入——但 AI 的速度已经让这个假设失效。

对企业中高管的启示：**禁止令很少真正有效，能力评估和受控试点远比硬性封锁更能管理风险**。

---

## 数据主权的系统性侵蚀：从 Atlassian 到 Notion

同一周内，两个完全不同的数据隐私事件，指向同一个更大的问题。

[Atlassian 悄然开启 Jira 和 Confluence 的数据收集](https://letsdatascience.com/news/atlassian-enables-default-data-collection-to-train-ai-f71343d8)用于训练其 AI 模型，关闭入口被故意隐藏。这不是第一次——Zoom、Slack、LinkedIn 都走过类似路径。"默认同意"已经成为 SaaS 平台的标准操作，因为每一次用户真正反弹的案例都证明：大部分用户不会采取任何行动。

与此同时，[Notion 的公开页面漏洞](https://twitter.com/weezerOSINT/status/2045849358462222720)——任何人无需认证即可获取编辑者全名和邮箱——自 2022 年已被报告，四年后仍未修复。这不是技术无能，更可能是优先级判断：修复这个漏洞需要成本，而大多数受影响的用户不知道也不在乎。

两件事合在一起，揭示了企业数据主权面临的核心困境：**你无法控制你不了解的事情**。企业把最敏感的内部信息——产品规划、客户数据、工程文档——存在 SaaS 工具里，但对这些工具的数据使用条款，大多数企业连读都没有认真读过。

AI 训练数据需求的急迫性只会让这个问题更严重。SaaS 平台现在有了比以往任何时候都更强的动机去扩大数据权，因为内部 AI 产品的竞争力直接依赖于此。用户的选择越来越少——要么接受，要么迁移到竞争对手那里（而竞争对手大概率有同样的条款）。

---

## 静默扩张的边界：Claude Desktop 与 Vercel

[Claude Desktop 在安装时静默注册浏览器 Native Messaging 主机](https://www.thatprivacyguy.com/blog/anthropic-spyware/)，赋予自己读取浏览器状态和操作 DOM 的权限——这是为了实现浏览器集成功能，但全程没有显式提示用户。同一周，[Vercel 确认一起安全事件](https://www.bleepingcomputer.com/news/security/vercel-confirms-breach-as-hackers-claim-to-be-selling-stolen-data/)，攻击通过第三方 AI OAuth 集成的薄弱环节发动，部分客户数据受影响。

这两件事指向 AI 平台扩张中一个新的风险面：**AI 工具获取权限的速度，正在超过企业安全团队理解和审计的速度**。

Claude Desktop 的情况尤其典型。Anthropic 的意图是善意的——集成浏览器能让 Claude 更好地服务用户。但"善意动机 + 未经告知的权限扩张"的组合，在隐私工具社区的标准里就是问题所在。更重要的是，企业 IT 部门在部署 Claude Desktop 时，大概率没有人检查过它对每台员工电脑上的 Chromium 浏览器做了什么。

Vercel 的事件则代表了另一类风险：AI 开发平台的高价值目标属性。开发者在 AI 开发平台上存储的不仅是代码，还包括 API 密钥、数据库连接、用于 AI 测试的生产数据样本。任何一个第三方 OAuth 集成如果安全审计不严，都是整个平台的薄弱入口。

---

## 商业价值的三重裂缝：CEO、Uber、Figma

以上谈的都是安全和治理层面的裂缝，但这周还有另一组数据，指向 AI 商业价值本身的质疑。

[针对 6000 名高管的调查](https://fortune.com/article/why-do-thousands-of-ceos-believe-ai-not-having-impact-productivity-employment-study/)显示近 90% 认为 AI 三年来未对生产力产生实质影响，高管每周使用 AI 仅 1.5 小时；[Uber 投入 34 亿美元的 AI 合作](https://finance.yahoo.com/sectors/technology/articles/ubers-anthropic-ai-push-hits-223109852.html)，Eats 部门的 AI 文案被一致评为"无实际效果"；[Claude Design 的发布](https://martinalderson.com/posts/figmas-woes-compound-with-claude-design/)让 Figma 陷入一个荒谬处境：用自己支付的 API 成本为竞争对手输送能力，而竞争对手的边际成本几乎为零。

这三个案例看似独立，但共同指向一个问题：**AI 的技术展示与商业价值之间，存在一条至今尚未被系统跨越的鸿沟**。Mythos 能找到 27 年未发现的安全漏洞，Claude Design 能让非设计师"在几分钟内探索十几个设计方向"，这些都是真实的技术成就。但大多数企业领导者在日常工作中感知不到这种能力，因为：

第一，**能力与工作流之间存在集成成本**。AI 再强，如果没有合适的应用场景包装和流程嵌入，高管就看不到它。  
第二，**多工具疲劳掩盖了单一工具的价值**。当员工同时被要求使用五种 AI 工具时，每一种都显得"没什么用"。  
第三，**商业 ROI 的可测量性本身是个工程问题**，大多数企业根本没有建立衡量 AI 贡献的数据基础设施。

---

## 从五重失效到一个建议

回望这一周：NSA 违规用 Mythos，Atlassian 静默开启数据收集，Notion 漏洞四年未修，Claude Desktop 静默注册浏览器权限，Tesla 隐瞒自动驾驶事故——每一件事背后都不是坏人，而是**在快速前进的技术浪潮中，规则制定者和规则执行者共同失去了节奏**。

这对 AI 行业从业者和企业管理者意味着什么？

与其等待完善的监管框架（它永远在追赶），不如把以下三件事作为当下优先级：

**① 数据主权清单**：列出所有使用中的 SaaS 工具，确认每个工具的 AI 训练数据条款，关闭不需要的数据共享选项。  
**② 权限可见性审计**：在企业范围内确认所有 AI 工具安装后获取了哪些系统权限，是否与官方文档一致。  
**③ AI 价值可量化化**：对当前使用的 AI 工具，建立哪怕最粗糙的 before/after 测量框架——哪怕只是任务完成时间，也好过"感觉没什么用"的模糊判断。

治理不一定要等制度完善，它可以从组织内部的可见性开始。

<!-- 自动分析于 2026-04-21 00:00 -->
