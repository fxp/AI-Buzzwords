# Google Cloud Next 2026：「试点终结」与全栈豪赌

> "The era of AI pilots is over. Every business must now be an AI business."  
> —— Thomas Kurian，Google Cloud CEO，2026 年 4 月

---

2026 年 4 月，拉斯维加斯 Mandalay Bay 会议中心。当 Thomas Kurian 走上 Google Cloud Next 的主舞台，他没有像往年那样秀模型 Benchmark、炫硬件参数。他说的第一句话是：**试点时代结束了。**

这不是一句营销口号。在此之前的六个月，Google Cloud 季度营收突破 $200 亿，同比增长 63%，全年合同积压额达到 $4620 亿。Gemini Enterprise 月活用户环比增长 40%。这些数字背后，是数以万计的企业真的把 AI Agent 部署到了生产环境——不是 Demo，不是 POC，是真实的工作流替代。

Google 在这次 Next 上展示的，正是它为这场「规模化」预备了多年的全栈基础设施：从定制芯片到协议标准，从平台整合到分销战略。每一层都在说同一件事：**我们不是想做 AI，我们就是 AI。**

---

## 一、平台整合：Gemini Enterprise Agent Platform 的诞生

过去两年，Google Cloud 在 AI 应用层堆积了太多品牌：Vertex AI、Agentspace、Agent Development Kit（ADK）、Vertex AI Studio、Model Garden……每个都有自己的控制台，自己的文档，自己的定价。企业客户在销售对话中经常问的一个问题是："这些到底什么关系？"

这个问题在 Next 2026 上得到了正式回答。

Google 将上述产品整体重命名为 **Gemini Enterprise Agent Platform**，统一在同一个 umbrella 品牌之下：

- **Model Garden** → 模型选择与微调入口，覆盖 Gemini 系列及第三方开源模型
- **Agent Development Kit（ADK）** → 开发者构建 Agent 的标准 SDK，支持 Python/Java
- **Agentspace** → 企业内部 Agent 的部署与管理面板，对接 SAP/Salesforce/ServiceNow
- **Vertex AI Studio** → 快速原型与 Prompt 工程工具，保留品牌但纳入统一入口
- **Agent Observability** → 链路追踪、成本监控、异常检测的 AIOps 层

整合的信号不只是品牌层面。Google 同时宣布了 **Workspace Studio**——一个嵌入 Gmail、Docs、Sheets 的无代码 Agent 构建器。非技术用户可以在熟悉的 Office 类界面里直接拖拽连接不同的数据源和 Agent，调用 A2A 协议编排跨系统工作流，不需要写一行代码。

这是 Google 在回答竞争对手的挑战。微软用 Copilot 嵌入 Office 365，Salesforce 用 Agentforce 嵌入 CRM，现在 Google 用 Workspace Studio 嵌入 30 亿用户的生产力工具生态。**分发才是最深的护城河。**

### 机会所在

对 ISV 和系统集成商：Gemini Enterprise Agent Platform 的统一意味着单一认证、单一计费、单一支持体系。过去因为 Vertex AI 文档混乱而绕道 AWS Bedrock 的企业客户，现在有了重新评估的理由。优先在这个平台上做深度适配的合作伙伴，能拿到 $7.5 亿合作伙伴基金的优先分配。

---

## 二、硅层分叉：TPU 8 世代的设计哲学转变

Google 这次发布了两款性格截然不同的 TPU，背后隐藏着一个重要的工程判断：**训练和推理是两种完全不同的计算问题，应该用完全不同的芯片来解决。**

### TPU 8t：训练的极致

TPU 8t（training 版）的核心设计目标是超大规模。

- **9,600 枚芯片**的单个 Pod 配置，配备 2PB HBM 显存
- 相比第七代 TPU，每美元算力提升 **2.8 倍**
- 通过 Virgo 网络，可实现近线性扩展至 **100 万枚芯片**
- 已用于训练 Gemini Ultra 2 系列

"近线性扩展"是这里最重要的技术声明。大多数分布式训练系统在超过数千块 GPU 后会遭遇严重的通信瓶颈，扩展效率断崖式下跌。Google 声称 TPU 8t 可以平滑扩展到百万芯片级别，意味着模型参数量上限几乎不受硬件拓扑限制。

这背后的关键是 **Virgo 网络**：134,000+ 枚芯片互联，总带宽 47 Pb/s，算力密度达到 1.7K ExaFlops。Virgo 采用两层扁平拓扑设计，省去传统 Fat-tree 架构的多跳延迟，芯片间通信接近本地总线水平。这不是软件优化，是物理拓扑的根本性重设计。

### TPU 8i：推理的极致

TPU 8i（inference 版）的问题陈述则完全不同：如何用更低成本、更低延迟服务海量在线请求？

- 片上 SRAM 提升至 **384MB**，是上一代的 3 倍
- 芯片间互联带宽（ICN）达到 **19.2 Tb/s**，是上一代的 2 倍
- 每美元推理性能提升 **80%**
- 专门针对长上下文（1M token）和低延迟 token 生成优化

TPU 8i 的设计思路与 Groq 的 LPU 有一定的哲学共鸣：把 SRAM 做大，减少对 HBM 的依赖，让权重尽量常驻片上，消除内存带宽瓶颈。区别在于 Google 的实现规模更大，生态整合更深。

### 机会所在

两款 TPU 的分离暗示了一个明确的商业信号：**Google 打算把推理成本打下来**。对 API 消费型创业公司来说，这意味着 Google Cloud 的 Gemini API 单价将持续下降。在 Bedrock/Azure OpenAI 之外，多云 LLM 路由策略应该把 Google Cloud 的 TPU 8i 实例纳入优先考量。

---

## 三、协议成熟：A2A v1.2 与互操作性赌局

2025 年，Google 联合微软、Salesforce、SAP 等公司发布了 **Agent-to-Agent（A2A）协议**，用于解决不同厂商 AI Agent 之间的互操作性问题。当时业界对这个协议的反应是审慎乐观——好主意，但没人知道会不会真的被采纳。

一年后，答案来了。

在 Next 2026 上，Google 宣布 A2A 协议升级至 **v1.2**，并披露了惊人的采纳数据：

- **150 家组织**已将 A2A 部署至生产环境
- 微软 Azure AI Foundry、AWS Bedrock 已原生支持 A2A
- Salesforce Agentforce、SAP Joule、ServiceNow 的 Agent 已实现跨平台互调
- A2A 协议已提交 **Linux Foundation** 托管，进入开放治理阶段

v1.2 引入的最重要新能力是 **密码学 Agent Cards**：每个 Agent 会携带由可信机构签发的数字身份证明，包含其能力声明、权限范围、运营方信息。这解决了 A2A 协议此前最大的安全痛点——你无法验证和你通信的另一个 Agent 是否是它声称的那个 Agent。

值得注意的是，A2A 和 Anthropic 主导的 MCP（Model Context Protocol）并不是直接竞争关系。MCP 解决的是"Agent 如何调用工具/API"的问题，A2A 解决的是"Agent 与 Agent 之间如何委托任务"的问题。Google 在 ADK 中同时支持两个协议——这是务实的选择，也是对 MCP 事实标准地位的默认承认。

### Workspace Studio 的 A2A 赌局

Workspace Studio 是 A2A 协议最重要的分发载体。当一个普通 Gmail 用户可以在收件箱里直接创建"帮我整理合同→发给法务 Agent 审核→自动回复对方"的工作流时，A2A 协议就不再是开发者专属的技术讨论，而是 30 亿用户每天都在使用的基础设施。

这是 Google 的经典打法：先做好协议，再用自己的产品生态把协议的使用规模化。

---

## 四、数据与安全：Agentic Data Cloud + Wiz 整合

Agent 落地最常见的两个障碍，一是数据孤岛，二是安全合规。Google 在 Next 2026 上同时打了这两张牌。

### Agentic Data Cloud

**Agentic Data Cloud** 是 Google 对企业数据层的重新定位，核心诉求是：让 Agent 能安全地访问企业跨系统的数据，而不需要把数据都搬到同一个地方。

主要能力：
- **Cross-cloud Lakehouse**：BigQuery 可以直接查询存放在 AWS S3、Azure Data Lake 的数据，无需 ETL
- **Knowledge Catalog**：企业数据资产统一编目，Agent 可以通过自然语言查询"我们有哪些客户投诉数据？格式是什么？谁有权限访问？"
- **Data Science Agent for BigQuery**：自动生成分析代码、执行查询、生成可视化报告——把 Data Analyst 的日常工作自动化

其中 Cross-cloud Lakehouse 是最具战略意味的功能。它意味着企业不需要"all-in Google Cloud"就能使用 Google 的 AI 层——数据留在原地，Google 的 Agent 来读取。这直接消解了"迁移成本"作为竞争壁垒的逻辑，让 Google 可以更容易地进入已经投资了 AWS 或 Azure 的企业账户。

### Wiz 整合：Agentic Defense

2025 年，Google 以 $320 亿收购云安全公司 Wiz，是科技史上最大的安全收购案。很多人当时不理解这个价格。在 Next 2026 上，整合后的战略意图首次完整呈现。

**Agentic Defense** 将 Google Threat Intelligence（基于搜索和 Safe Browsing 多年积累的威胁数据库）与 Wiz 的云资产可视性能力结合，重点解决 Agent 时代的新型安全问题：

- **Agent 权限蔓延**：Agent 在执行任务过程中申请权限后通常不会主动释放，导致权限持续扩张。Wiz 的持续扫描引擎可以检测异常权限累积
- **Prompt Injection 检测**：恶意数据通过 RAG 检索混入 Agent 上下文，诱导其执行非预期操作。Google Threat Intelligence 的语义分析模型可以实时标记
- **跨 Agent 横向移动**：A2A 协议让 Agent 可以调用其他 Agent，也意味着一个被攻破的 Agent 可以成为攻击跳板。Agentic Defense 在 A2A 调用链上部署了流量分析和异常检测

Wiz 的原生能力是多云覆盖——它本来就服务 AWS 和 Azure 的客户。收购之后，Google 并没有把 Wiz 强制绑定在 Google Cloud，而是保持了多云中立性。这让 Agentic Defense 可以覆盖客户在任何云上的 Agent 部署，而不仅仅是 Google 自己的地盘。

### 机会所在

Agentic Data Cloud + Agentic Defense 的组合，是专门为那些"数据在多云、合规要求严格"的企业设计的。金融、医疗、政府这些最难切入的行业，恰恰是这类需求最集中的地方。能在这些行业做深度实施的 SI（系统集成商），在 Google Cloud 的 $7.5 亿合作伙伴基金中将有优先谈判地位。

---

## 五、分销战争：$7.5 亿与 DeployCo 的镜像逻辑

在所有 Next 2026 的公告中，有一条被大多数科技媒体忽略了：**Google Cloud 宣布设立 $7.5 亿合作伙伴基金**，专项用于支持 ISV、SI 和分销伙伴将 Google AI 能力部署到企业客户。

这不是普通的市场支持预算。这是对一个明确战略判断的资本化：**AI 规模化落地的瓶颈不在模型，而在分销。**

就在同一个月，OpenAI 宣布了 DeployCo——与 TPG、贝恩、凯雷等 PE 机构共同设立的 $100 亿合资公司，专门用于通过 1,200+ PE 投资组合企业分发 OpenAI 能力。两件事放在一起看，逻辑是完全对称的：

| | OpenAI DeployCo | Google Cloud 合作伙伴基金 |
|---|---|---|
| **规模** | $100 亿 JV | $7.5 亿基金 |
| **分销渠道** | PE 投资组合企业（1,200+） | ISV/SI/VAR 生态（全球数千家） |
| **部署模型** | Palantir 式"前置工程师" | 传统云合作伙伴激励体系 |
| **覆盖深度** | 垂直渗透，长期驻场 | 水平覆盖，快速规模化 |
| **商业回报** | 17.5% 保证年化回报 | 收入分成 + 认证优先权 |

两种模式都在回答同一个问题：谁来帮企业把 AI 真正用起来？

OpenAI 选择了华尔街的 PE 网络，押注于在已经建立信任关系的投资组合企业中快速拿单；Google 选择了沉淀了三十年的合作伙伴生态，押注于覆盖更广但每单深度相对更浅的分销网络。

这场分销战争的赢家，不一定是技术最强的那个，而是能最高效将 AI 能力转化为企业可操作工作流的那个。

---

## 六、收入现实：$200 亿背后的结构性转变

抛开产品和战略，数字最诚实。

Google Cloud 在 2026 年 Q1 的营收为 **$200 亿**，同比增长 **63%**。这不是小数字——这相当于 Google Cloud 在一个季度内接近完成了 2022 年全年的营收目标。

更重要的是结构：
- **$4620 亿**的合同积压（backlog），意味着未来几年的收入已经基本锁定
- Gemini Enterprise MAU 环比增长 **40%**，且主要来自付费企业客户而非免费试用
- 超过 **60% 的 Fortune 500**企业已经是 Google Cloud 客户
- OpenAI-微软的独家协议到期，OpenAI 开始向 Google Cloud 迁移部分推理工作负载

最后一条细节值得单独拿出来说。OpenAI 与微软之间的排他性云协议在 2025 年底开始松动，OpenAI 宣布可以将工作负载分散到其他云服务商。Google Cloud 是最直接的受益者——它不仅有足够的 TPU 推理算力，还有 OpenAI 迫切需要的地理多样性（数据主权合规）和非美国市场覆盖。

---

## 七、竞争格局：Google 的「四层全栈」主张

Thomas Kurian 在主题演讲中多次提到 Google 的"四层优势"：

1. **自研芯片（Silicon）**：TPU 8t/8i + Virgo，不依赖 NVIDIA 供应链
2. **前沿模型（Models）**：Gemini Ultra 2 系列，在多项 Benchmark 居首
3. **云平台（Platform）**：Gemini Enterprise Agent Platform，端到端的 Agent 开发部署
4. **30 亿用户分发（Distribution）**：Workspace，最大的企业生产力工具生态

这四层都有对手，但没有任何一个对手同时拥有四层：

- 微软有 Office 365 分发，但没有自研芯片，模型依赖 OpenAI
- AWS 有云平台和全球基础设施，但没有自研通用 LLM，也没有消费级分发入口
- OpenAI 有最强的模型品牌，但没有芯片、没有云平台、没有分发渠道（DeployCo 是在补这个短板）
- Anthropic 有最被企业信任的安全模型，但四层都不具备

Google 的四层主张是否成立，取决于每一层是否真的做到了"足够好"而不仅仅是"存在"。Workspace 的 30 亿用户确实是护城河，但用户数 ≠ AI 使用量。Gemini 在 Workspace 的渗透率（有多少用户真正用了 AI 功能）是这个故事能否成立的关键指标，而 Google 目前还没有完整披露这个数字。

---

## 总结：「生产化」才是主语

如果用一句话概括 Google Cloud Next 2026，那就是：**Google 在押注「AI 生产化」是一个多年期的系统性机会，而它拥有比任何人都更完整的工具集来服务这个机会。**

Gemini Enterprise Agent Platform 的整合告诉企业：你不需要再猜哪个 Google AI 产品是正确的选择。TPU 8t/8i 的分叉告诉工程师：Google 理解训练和推理是不同的问题，不打算用一种芯片解决所有问题。A2A v1.2 告诉协议生态：互操作性不是 Google 的让步，是 Google 的战略——因为更大的生态让 Google 的平台更有价值。$7.5 亿合作伙伴基金告诉分销商：Google 知道模型不等于部署，愿意为把 AI 真正装进企业流程的人付钱。

Thomas Kurian 说"试点时代结束了"，这话对企业是一种压力，对 Google Cloud 是一个邀约，对整个生态是一个信号：**接下来几年，真正的战场不是谁的模型更聪明，而是谁能把更多企业从 POC 带进生产。**

---

## 机会所在

**对创业公司：**
A2A v1.2 + Workspace Studio 的组合，意味着"垂直行业 Agent 编排层"是一个值得重点关注的赛道。Google 提供了协议和 UI 框架，但行业知识和工作流设计无法标准化——金融合规 Agent、医疗记录 Agent、制造质检 Agent 的构建，仍然需要懂行业的人来做。

**对企业 IT：**
Agentic Data Cloud 的 Cross-cloud Lakehouse 是一个低风险的切入点——数据不动，先在 BigQuery 上跑 AI 分析。这是一个可以快速见效且不需要大规模迁移的试验场。

**对投资人：**
Google Cloud 的 $4620 亿 backlog 是一个具有参考意义的基准线——它说明企业采购 AI 基础设施不是在等"更好的模型"，而是已经进入了多年期合同锁定的阶段。AI 基础设施的商业化速度快于大多数人的预期。

**对从业者：**
Workspace Studio 的无代码 Agent 构建能力，意味着"会用 AI 工具"的门槛正在进一步降低，而"能设计工作流"的系统思维将变得更值钱。理解 A2A 协议的工程师，在未来两年的企业 AI 项目中会有显著的薪资溢价。

---

## 参考资料

- Google Cloud Next 2026 主题演讲，Thomas Kurian + Sundar Pichai，2026 年 4 月
- [Google Cloud Blog: Gemini Enterprise Agent Platform 发布公告](https://cloud.google.com/blog)
- [Google Cloud Blog: TPU 8th Generation 技术详解](https://cloud.google.com/blog/topics/systems/introducing-trillium)
- [Google Cloud Blog: A2A Protocol v1.2 与 Linux Foundation 治理](https://cloud.google.com/blog/products/ai-machine-learning/a2a-protocol)
- [Google Cloud Blog: Agentic Data Cloud 与 Wiz 整合](https://cloud.google.com/blog/products/data-analytics)
- [Google Cloud Blog: $750M Partner Fund 公告](https://cloud.google.com/blog/topics/partners)
- Alphabet Q1 2026 财报电话会议记录
- [The Verge: Google Cloud Next 2026 综合报道](https://www.theverge.com)
- [TechCrunch: Google TPU 8 世代分析](https://techcrunch.com)
- [GAI Insights: OpenAI DeployCo 与 Google 分销战争对比分析](https://gaiinsights.substack.com)
