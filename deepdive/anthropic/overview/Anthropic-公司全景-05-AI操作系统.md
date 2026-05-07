# Anthropic 公司全景 · 05｜从模型公司到 AI 操作系统

> 一句话提要：Antspace + Claude Code Auto Mode + Cowork + Partner Network + Marketplace + Anthropic Institute——这六块拼图正在被 Anthropic 拼成一个完整的"AI 操作系统"。SaaSpocalypse 不是意外，是这套战略的必然结果——当 Anthropic 把模型、协议、接口、应用、生态、治理都做完时，传统 SaaS 的中间层利润就会被吸走。这一篇拆解 Anthropic 怎么从模型公司变成操作系统公司。

```
日期：2026-05-05
系列：Anthropic 公司全景，共 7 篇
本篇主题：从模型到操作系统
受众：AI 从业者 / 投资人
```

---

## 一、操作系统位置的六块拼图

把过去 12 个月所有产品发布拼到一起，会清晰看到 Anthropic 在搭建一套"AI 操作系统"——它不是单一产品，是六块协同的拼图：

| 层 | 产品 | 类比 |
|----|------|------|
| **底层运行时** | Antspace（AI 应用 PaaS）| Vercel + Google Cloud Run |
| **开发者工具** | Claude Code + Auto Mode + Harness | GitHub Copilot + Replit + GitHub Actions |
| **桌面应用层** | Claude Cowork + Plugins + **Claude Design** | macOS + App Store + Keynote/Figma |
| **生态分发** | Claude Marketplace + Partner Network | AWS Marketplace + AppExchange |
| **协议层** | MCP + Computer Use SDK + Agent SDK | USB-C + REST + Browser API |
| **治理层** | Anthropic Institute + RSP + Constitution | Linux Foundation + ICANN |

**关键判断**：这六层互相之间不是简单的"产品组合"，而是**结构性互锁**。一个企业引入 MCP 后会自然拓展到 Cowork，使用 Cowork 后会自然消费 Marketplace 插件，部署 Marketplace 插件后会找 Partner Network 实施伙伴——每一层都向下一层导流。

下面把六块拼图分别拆开。

---

## 二、Antspace：泄露代码里发现的"隐藏 Vercel"

Antspace 是 Claude Code 源码意外公开后，安全研究者 AprilNEA 在 Firecracker MicroVM 镜像里发现的——一个未剥离调试符号的 Go 二进制 `environment-runner`，从中重建出 Anthropic 内部平台的完整架构：

```
Claude 生成代码 → Baku 编译 → Supabase 数据库 → Antspace 托管
```

构成"从提示词到上线"的全链路闭环。Antspace 的构建流程与 Vercel 不同：

| 维度 | Vercel | Antspace |
|------|--------|----------|
| 构建方式 | 逐文件 SHA 去重 + 本地构建 | 代码打包 tar.gz 上传 + 服务器端构建 |
| 执行模型 | Edge Functions | 更接近 Google Cloud Run |
| 目标用户 | 人类开发者 | **AI 生成应用** |

最后一行最关键——**Antspace 不是给人用的 PaaS，是给 AI 用的 PaaS**。它是为"AI 写一个应用 → AI 立刻部署运行"这一工作流专门设计的执行环境，而不是为人类开发者优化的部署体验。

如果 Antspace 最终公开，它将是**第一个由 LLM 厂商直接提供的"AI 生成→AI 托管"一体化平台**——直接竞争 Vercel、Netlify、Replit、Firebase 所占据的市场。

### 被泄露成为竞争情报

Antspace 还没有公开发布，但它的存在已经被业界确认。Anthropic 没有发表官方 post-mortem，沉默本身就是一种确认。这意味着：

- **Vercel / Replit 已经在重新评估自己的产品定位** —— 他们的客户群（"AI 写代码"应用）正在被 Anthropic 抢先切入
- **Cloudflare 加大了 AI 相关 PaaS 投入** —— 试图在 Anthropic 公开 Antspace 之前抢占心智
- **Firebase 在 Q1 调整了 AI Studio 路线图** —— 把"AI 应用部署"作为下一阶段重点

**单从 Antspace 被发现这件事，Anthropic 已经实质性地改变了多家 PaaS 公司的产品路线图**——这是协议层 + 平台层影响力的一个具体体现。

---

## 三、Claude Code Auto Mode：用 AI 审批 AI 的双层架构

传统 Agent 每次执行高权限操作都需用户手动确认。Anthropic 工程团队发现的现实困境：**用户实际确认了 93% 的请求**——"approval fatigue"让安全机制形同虚设。

Claude Code auto mode 的解决方案是双层 AI 审批：

| 层 | 机制 |
|---|------|
| **输入层** | 服务器端 prompt injection 探针扫描所有工具输出，拦截试图劫持 Agent 的恶意内容 |
| **输出层** | Claude Sonnet 4.6 担任"安全审计员"，评估每次动作是否符合用户原始意图，**故意剥离 Agent 的推理过程**（防止 Agent 自我合理化越界行为）|

测试数据：**误报率 0.4%，对"Agent 超出授权范围"漏报率 17%**。Anthropic 选择直接公开这个数字，而不是说"准确率 83%"——这个透明度本身就是信号。**17% 的漏报意味着"完全自动化信任"尚不现实，但减少 80% 人工确认的目标已经可行**。

### Harness Engineering：把内部最佳实践公开

2026 Q1 Anthropic 工程博客发布了两篇 Agent Harness 系列文章——这是该公司首次系统性公开 Agent 长时间运行的最佳实践：

- **Initializer Agent**：负责创建 `init.sh` + `claude-progress.txt` + git 基线
- **Coding Agent**：每次会话只做一个功能，每完成一项提交 git 记录作为恢复锚点
- **200+ 项特性结构化 JSON**：防止 Agent 过早宣称完成
- **GAN 式架构**：Generator + Evaluator 分离，让独立评估者而非生成者自我评价质量

第二篇关键洞察：

> "让 Agent 评价自己的输出"是 Agent 质量退化的最主要来源之一。

——这与 NousResearch AutoReason 论文结论完全一致。**Anthropic 把内部工程纪律外化为行业 RFC** 的姿态非常清晰——他们在测试哪些 Agent 模式会被广泛采用并内化为平台标准。

---

## 四、Claude Cowork：触发 SaaSpocalypse 的桌面智能体

**Claude Cowork（2026-01-12 研究预览，2026-04-09 macOS+Windows GA）**由 4 名工程师 10 天内构建，首发 11 个开源 plugin（销售、法务、财务、HR、营销、客服、产品、工程、设计），加上 5 个金融服务专属插件（财务分析、投行、股票研究、私募股权、财富管理）。

### Cowork 的差异化在 Plugins 框架

不同于 ChatGPT Apps 或 Microsoft Copilot Connector，Cowork 的 Plugin 是**捆绑技能 + 命令 + MCP 连接器 + 子代理**的复合包——一个 Plugin 不是单一工具，而是一个"领域智能体"。

新增 13 个 MCP 连接器：Zoom、Google Workspace、DocuSign、Apollo、FactSet、Harvey、LSEG、S&P Global、MSCI 等。企业版加入 RBAC、群组支出限额、OpenTelemetry 可观测、私有插件市场。

**Microsoft 在 3 月推出"Copilot Cowork"——使用同一 Claude 引擎与代理框架**。这是一个标志性事件：连 Microsoft 自己的 Copilot 都在某些场景使用 Claude 而不是 OpenAI——Anthropic 已经成为企业 Agent 基础设施提供方，而不只是模型供应商。

### SaaSpocalypse：48 小时 $285 亿蒸发

2026 年 1 月 30 日，Anthropic 发布 11 个开源插件；2 月扩展至 Slack / Salesforce Agentforce 360 / FactSet / DocuSign 后，**直接触发软件股暴跌**：

| 公司 | 单日跌幅 |
|------|---------|
| LegalZoom | -19.68% |
| Thomson Reuters | -15.83% |
| RELX | -14% |
| JFrog | -24.0% |
| Wolters Kluwer | -13% |
| LSEG | -8.5% |
| DocuSign | -11% |
| Intuit | -11% |
| ServiceNow | -7% |
| Adobe | -7% |
| Workday / Salesforce | 12 个月累计 -40%+ |

Jefferies 将此命名为 **"SaaSpocalypse"**，48 小时内全球软件股蒸发约 **$285 亿（约 2850 亿美元）**。软件行业 P/S 估值倍数从 **9× 压缩至 6×**。

### 为什么是 SaaS 公司倒下，不是 SaaS 客户？

SaaSpocalypse 的本质是 **per-seat pricing 这个商业模式被宣告死亡**。Per-seat 模式建立在"每个员工都需要一个登录"的假设之上。当 AI Agent 替代 9/10 团队成员的工作时，登录数下降 90%，营收模型崩塌。

但有一类 SaaS 不会倒下：**拥有不可替代数据资产的公司**。Thomson Reuters 在披露 CoCounsel 用户突破 100 万后单日**暴涨 11%**——Westlaw 60+ 年法律案例数据库不是 Claude 能轻易替代的。这告诉我们一个判断标准：**数据 = 护城河，包装 = 中间层利润**。Anthropic 吃的是中间层利润，不是数据本身。

---

## 五、Claude Code Enterprise：消费型定价的反弹与扩张

2026 年 Anthropic 把 Claude Code Enterprise 重构成 **$20/座位/月的自助式企业版（最低 20 席位）**，并把原先的 chat seats vs Claude Code seats 合并成单一 seat——**所有 token 按 API 费率单独计费**。

The Information 报道这一"消费型定价"让重度用户成本可能涨 3 倍，4 月引发部分企业用户取消订阅。但同期功能持续加码：

- **1M token 上下文 GA**（无附加费）
- **Routines**：自动化触发器
- **Sub-agents**：子智能体
- **Hooks**：插入点
- **Skills**：技能模块
- **Brief / Focus mode**：专注模式
- **GitHub Action v1.0**：CI/CD 集成
- **Claude Security**（5 月公测）：基于 Opus 4.7 的代码漏洞扫描器，首批客户 DoorDash

**消费型定价在短期是商业反弹，长期是 token 经济飞轮的关键**——它把"每多用一次 = 多付一次"的关系坐实，让 ARR 增长曲线持续陡峭。

---

## 六、Claude Marketplace：复制 AWS Marketplace 飞轮

**Claude Marketplace（2026-03-06 受限预览）**首批 6 家合作伙伴：GitLab、Snowflake、Harvey AI、Rogo、Replit、Lovable。

最具颠覆性的是商业模式：

- **初期不抽佣**——与 AWS Marketplace 收取 3-15%（部分高至 20%）形成鲜明对比
- 客户可使用现有 Anthropic 支出承诺额抵扣购买合作伙伴产品
- Anthropic 单一开票

VentureBeat、PYMNTS 等分析师认为这是 Anthropic 从"模型供应商"向"企业 AI 采购入口"转型的标志，意图复制 AWS 第三方卖家飞轮。

**为什么不抽佣？** 因为 Anthropic 真正的目标不是 Marketplace 抽佣的几个百分点，而是**让 Marketplace 上的所有应用都消耗 Anthropic 的 token**。每一个 Harvey AI 法律 Agent 调用、每一次 Replit 编程辅助、每一次 Lovable 应用生成——背后都在烧 Anthropic 的推理。Marketplace 是为了**强化代币经济飞轮**，而不是抽佣经济。

这是与 AWS Marketplace 完全不同的 logic：AWS 抽佣是因为客户消费的"东西"是 Marketplace 上的软件本身；Anthropic 不抽佣是因为客户消费的"东西"是 Marketplace 软件背后的 Claude API。

---

## 七、Claude Partner Network：销售军团 + 实施认证

**Claude Partner Network（2026-03-12 首届 Partner Summit）**由 Anthropic 投入 $1 亿用于培训、销售支持、市场开发，partner-facing 团队规模扩大 5 倍。**CCA-F（Claude Certified Architect Foundations）**成为首个技术认证：120 分钟在线考试，$99 报名费。

Partner Network 的设计逻辑很清楚：

1. **认证 = 人才溢价**：拿到 CCA-F 的工程师在 Accenture 内部薪资上浮 15-25%，强烈激励工程师主动学习
2. **培训 = 销售外包**：每个被培训的 FDE 都是 Anthropic 的隐形销售
3. **Partner Summit = 关系深化**：年度会议让头部合作伙伴形成"圈子归属感"
4. **抢先功能访问 = 锁定升级**：合作伙伴 60 天前就能用上未发布的新模型 / 新 API

5 月 4 日 PE JV 是 Partner Network 的下一阶段——**Anthropic 不再满足于"通过合作伙伴卖"，而是"自己亲自下场卖"**。这两条路径会同时存在 12-18 个月，然后看哪条路径效率更高。

---

## 八、Anthropic Institute：政策话语权制度化

**Anthropic Institute（2026-Q1 成立）**由联合创始人 Jack Clark 领导，整合 Frontier Red Team + Societal Impacts + Economic Research 三支团队。

Jack Clark 是 AI 政策领域最具影响力的技术-政策跨界人物之一（OpenAI 政策研究早期奠基人）。由他领导意味着 Institute 的产出将**优先服务监管对话和行业标准制定**，而非内部产品决策。

具体输出已经包括：

- 加州 SB 53 起草过程中的技术建议（Anthropic 是首家公开 endorse SB 53 的主要 AI 公司）
- 欧盟 AI Act Codes of Practice 工作组深度参与
- UK DSIT MOU 与英国政府的联合评估机制
- 多份 Frontier Safety Roadmap 发布

**与 OpenAI Global Affairs 的差异**：OpenAI 的政策团队主要做"防御 + 公关"——降低监管对 OpenAI 的限制；Anthropic Institute 主要做"塑造 + 标准"——把 Anthropic 偏好的治理框架推向行业标准。这种差异在 5 年时间维度上会产生巨大复利。

---

## 九、Claude Design：从代码生成到视觉创意的产品扩张

**[Claude Design by Anthropic Labs](https://anthropic.com/news/claude-design-anthropic-labs)（2026 年 5 月，[claude.ai/design](https://claude.ai/design)）**——Anthropic 首次将操作系统位置从开发者工作流延伸至视觉创意工作流。Opus 4.7 驱动，面向 Pro / Max / Team / Enterprise 订阅用户研究预览。

### 能力范围

用户通过文字、图片、文件或网页输入描述需求，Claude Design 输出：原型（Prototypes）、产品线框图（Wireframes）、设计探索方向、Pitch Deck、营销素材。关键的"Frontier Design"功能基于代码驱动，支持语音、视频、着色器（Shaders）和 3D 元素。

Claude Design 可读取代码库和设计文件，自动应用颜色体系、字体规范和组件库——意味着它能在企业已有的设计系统内工作，而非生成"脱离品牌调性"的内容。输出支持导出到 Canva、PDF、PPTX、HTML，**完成后直接交接给 Claude Code 实现**。

### 客户表态

| 客户 | 表态 |
|------|------|
| **Canva** | "在 Claude Design 里生成创意，一键进入 Canva 即可完全编辑" |
| **Brilliant** | "原来在其他工具需要 20+ 次提示重建的复杂页面，Claude Design 只需 2 次提示" |
| **Datadog** | "会议结束之前原型已经做好了" |

### 战略含义

Claude Design 解决了 Cowork 没有覆盖的最后一类高价值工作流：**视觉创意**。Figma / Canva / Adobe Express 所在的市场被 AI-native 工具重新挑战。Canva 选择合作而非对抗（将 Claude Design 集成进自己的 Design Engine），恰好说明其感受到了威胁。Cowork 抢 SaaS 中间层的 **收割**效率，Claude Design 则是 Anthropic 向创意专业人士张开的新入口——两者叠加，操作系统位置从工程师和商业分析师延伸至设计师和内容创作者。

---

## 十、"Claude 永远不投广告"：产品身份的承诺

2026 年 5 月，Anthropic 发布声明[《Claude is a space to think》](https://anthropic.com/news/claude-is-a-space-to-think)，明确将**无广告**作为 Claude 永久产品身份：

> "Claude 会保持无广告。用户不会在对话旁边看到'赞助'链接，Claude 的回应不会受广告主影响，也不会包含未经用户要求的第三方产品植入。"

### 为什么这是战略声明而非 PR

**广告会改变激励结构**：一旦引入广告，Claude 会被优化为最大化用户停留时长和访问频次，而非最大化有用性。这与 Claude 的"Genuinely helpful assistant"定位根本冲突。

**Anthropic 给出了量化依据**：分析数据显示，相当比例的 Claude 对话涉及敏感或深度个人话题——这些场景中的广告植入会产生远超普通搜索或社交媒体广告的用户伤害。

**替代商业模式已经跑通**：企业合同 + 付费订阅是 Anthropic 的收入支柱，ARR $300 亿的增长轨迹证明无需依赖广告收入。未来的"商业互动"将采用**主动式代理商务**（Agentic Commerce）——用户明确要求 Claude 处理购买或预订时，Claude 才会介入——而非被动广告曝光。

**对 AI 操作系统竞争的含义**：当 Google Gemini 和 Microsoft Copilot 背靠广告驱动公司的大股东利益时，Anthropic 的无广告承诺成为一种结构性差异化——**不只是用户体验的改善，是商业模式层面的护城河**。企业客户在高合规场景（医疗 / 法务 / 金融）尤其在意"AI 助手的回答是否受利益方左右"——无广告承诺消解了这一疑虑。

---

## 十一、操作系统野心的元判断：四股力量相互锁定

把 Antspace + Auto Mode + Cowork + Marketplace + Partner Network + Institute 拼到一起，能看到一个完整的策略：

**Anthropic 不再是模型公司。它是一家正在搭建"AI 操作系统"的公司。**

四股力量相互锁定：

| 力量 | 机制 | 对手要复制的难度 |
|------|------|----------------|
| **平台锁定** | Antspace + Cowork + Partner Network 全栈 | 极高——需要同时建模型、协议、应用 |
| **安全资质** | RSP + Constitutional AI + ASL-3 + Mythos | 极高——需要 5+ 年信誉积累 |
| **生态控制权** | MCP + Skills + Computer Use + Agent SDK | 中——OpenAI、Google 都在追，但 MCP 的事实标准已定 |
| **政策话语权** | Anthropic Institute + Jack Clark + RSP 被立法引用 | 极高——需要顶级人才 + 5+ 年深耕 |

**任何一项单独都不致命，但四项叠加** 构成了一个比"模型分数最高"更深的护城河。

### SaaS 行业的下一步

SaaSpocalypse 之后 12-24 个月，SaaS 行业会被重新洗牌：

**会死的**：单纯把模型 API 包一层 UI 的"thin wrapper"。Cowork 一个插件就能替代。

**会变的**：传统 SaaS 必须要么深化数据护城河（学 Thomson Reuters / Westlaw），要么转型成 Agent 工作流（学 ServiceNow Build Agent 把 Claude 设为默认）——两端选一边。

**会涨的**：拥有不可复制数据资产的 SaaS（Moody's、S&P Global、Bloomberg）反而被增强——因为这些数据现在能通过 MCP 被 100 万企业的 Cowork 实例同时访问。

**会赢的**：基础设施层（Snowflake / Databricks / 三大云）通过算力和数据存储吃 AI 时代的下一轮红利。

而 Anthropic 自己——从模型公司变成操作系统公司——成为这场重构的最大受益者，**也成为最强破坏力的来源**。这是一个公司同时扮演两种角色的罕见时刻。

---

## 十二、给三种人的判断框架

**AI 行业从业者**：把 Claude Code 工程文章当 RFC 读——Anthropic 在测试哪些 Agent 模式会被广泛采用并内化为平台标准。提前实践这些模式 = 跑在平台锁定之前。

**企业管理者**：Antspace 公开后立即评估垂直栈依赖。跟踪 Mythos B2G 进展决定金融 / 国防准入条件。**谨慎评估 Anthropic 的 vendor 风险**——14 个月四起外泄是真实信号。Cowork Plugin 评估时记住：**Plugin 不是工具，是领域智能体**——比 ChatGPT Apps 锁定深得多。

**投资 / 战略人士**：模型能力差异化窗口正在关闭，真正护城河转移到平台 + 安全资质 + 生态控制权 + 政策话语权。Anthropic IPO 招股书"风险因素"章节最值得关注的是：（1）Antspace 公开时间；（2）Marketplace 抽佣转折点；（3）PE JV 与 Accenture 关系裁决。

---

## 这一篇的关键操作系统看板

| 维度 | 数字 / 状态 | 备注 |
|------|------------|------|
| Antspace | 内部使用，未公开 | 通过 Code 泄露被业界确认 |
| Auto Mode 漏报率 | 17% | Anthropic 主动公开 |
| Cowork 触发蒸发 | $285 亿 / 48 小时 | SaaSpocalypse |
| 软件 P/S 倍数 | 9× → 6× | 行业级估值压缩 |
| Marketplace 抽佣 | 0% | 与 AWS 3-15% 形成对比 |
| Partner Network 投入 | $1 亿 | partner-facing 团队 5 倍扩张 |
| Cowork 首发 Plugin | 11 个开源 + 5 个金融垂直 | 4 名工程师 10 天构建 |
| Anthropic Institute | 已成立（2026-Q1）| Jack Clark 领导 |
| Microsoft Copilot Cowork | 使用 Claude 引擎 | 标志性事件 |
| Claude Design | [研究预览（2026-05）](https://anthropic.com/news/claude-design-anthropic-labs) | Opus 4.7 驱动；[claude.ai/design](https://claude.ai/design)；支持 Canva/PDF/PPTX/HTML 导出 |
| 无广告承诺 | [永久政策（2026-05 声明）](https://anthropic.com/news/claude-is-a-space-to-think) | 结构性差异化；企业合规场景护城河 |

---

*本系列下一篇：[06 政府博弈与治理立场](Anthropic-公司全景-06-政府博弈.md)——Pentagon 诉讼、SB 53 背书、宪法反集权条款的真实代价。*

*数据来源：[Anthropic 官方 Engineering Blog](https://anthropic.com/engineering) · AprilNEA Antspace 逆向工程报告 · Anthropic Partner Summit · Bloomberg / CNBC / Fortune SaaSpocalypse 报道 · The Information · Jefferies 报告 · Microsoft Copilot Cowork 公告 · [Claude Design 发布](https://anthropic.com/news/claude-design-anthropic-labs) · [Claude 无广告声明](https://anthropic.com/news/claude-is-a-space-to-think) · [创意工具 MCP 连接器](https://anthropic.com/news/claude-for-creative-work)*
