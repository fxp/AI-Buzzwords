# Anthropic 公司全景 · 03｜合作伙伴生态解构：四类合作的真实利益结构

> 一句话提要：Anthropic 不是在卖 API，是在用四类合作关系系统性收购企业认知基础设施控制权——云用算力换毛利分成，咨询用培训换销售外包，数据平台用合同换推理能力，终端客户用工作流换效率。每一类合作都是精心设计的利益交换，但权力天平**没有一类是真正对称的**。

```
日期：2026-05-05
系列：Anthropic 公司全景，共 7 篇
本篇主题：合作伙伴生态
受众：AI 从业者 / 投资人
```

---

## 一、Anthropic 商业模式的真实结构：三个飞轮

外部视角看 Anthropic 的收入模式，比"卖 API"复杂得多。它实际跑着三个相互耦合的飞轮：

**飞轮一：代币经济（占总收入 70-75%）**——按消费量收费，而非席位。客户业务用 AI 增长一倍 = Anthropic 收入增长一倍，无需额外销售动作。这是 ARR 从 90 亿到 300 亿只用 4 个月的根本原因——不是新增客户，是现有客户用量爆炸。

**飞轮二：平台转移**——从 API 供应商系统性向上吃 SaaS 应用层。Cowork、Claude for Financial Services、Claude for Healthcare、Claude 法律插件——这些都是应用层产品，与原来的 API 客户直接竞争。这是 AWS 当年对 SaaS 公司做过的事，Anthropic 正在对 AI SaaS 做同样的事。

**飞轮三：安全叙事**——把"安全"做成进入金融、医疗、政府等高合规行业的准入证。这些行业采购周期长（12-18 个月）、客单价高（$100 万+/年）、替换成本极大——一旦嵌入核心系统，粘性极高。

**外部合作伙伴视角的核心洞察**：

> Anthropic 用投资换算力（云合作），用认证体系换销售渠道（咨询合作），用 API 黏性换数据生态（平台合作），用安全叙事换监管壁垒（行业准入）。每一步棋都服务于同一个终局：**成为不可替代的认知基础设施**。

下面把四类合作伙伴的真实利益结构拆开看。

---

## 二、第一类：云基础设施（AWS / Google / Azure）——最深度、最对称

这是所有合作里最深、利益结构最对称的一类。核心是**算力—资本—分发三角交换**：云用算力和资本换 Anthropic 的计算消耗承诺，Anthropic 用资源训练更好的模型，再通过云平台分发——共生飞轮。

### 三云的承诺规模

| 合作方 | 投资金额 | 算力承诺 | 关键机制 |
|--------|---------|---------|---------|
| **AWS** | 累计最多 $250 亿（[2026-04 追加](https://anthropic.com/news/anthropic-amazon-compute)；其中 **$50 亿在宣布时立即到账**，余额转化为算力信用额度）| 5 GW（Project Rainier）| 50% Bedrock 毛利分成；Trainium 联合研发；10 年 $1000 亿采购承诺 |
| **Google Cloud** | 最多 $400 亿（2026-04 加码）| 5 GW（TPU + Broadcom，2027 年起 3.5GW by Broadcom）| Ironwood TPU 首批客户 |
| **Microsoft + NVIDIA** | $15 亿投资 + $300 亿 Azure 承诺 | 1+ GW Grace Blackwell | 三云全覆盖完成 |

合计 hyperscaler 累计承诺超过 880 亿美元，可见算力承诺超过 10 GW。AWS Project Rainier 截至 2026 年 4 月已激活 2.2 GW，部署近 50 万 Trainium2 芯片。

### 以 AWS 为例的双向交换

| 方向 | 内容 |
|------|------|
| Anthropic → AWS | $1000 亿+ 采购承诺；首要云地位背书；Trainium 芯片联合研发；Bedrock 客户开放所有未来模型；Claude Platform 原生嵌入 AWS 账号体系 |
| AWS → Anthropic | $130 亿+ 投资（股权回报路径）；5 GW 算力容量；10 万+ Bedrock 企业客户分发；约 50% Bedrock 渠道毛利分成 |

AWS 的算盘很清楚：
1. **股权财务回报**：3800 亿估值下，AWS 早期投入已账面回报数倍
2. **云消费收入**：Anthropic 每年在 AWS 消费数十亿美元
3. **渠道分成**：Bedrock 上 Claude 销售毛利 50% 归 AWS
4. **Trainium 验证价值**：靠 Anthropic 证明实用性，吸引更多客户
5. **遏制对手**：绑定 Anthropic 让 OpenAI 在 Azure 的优势减弱

### 权力动态：渐趋平衡

随着 Anthropic 体量增大，主动权在悄悄转移。2026 年宣布"多云战略"实际上是对 AWS 独家地位的稀释——这正是 4 月 AWS 大幅追加 250 亿投资的真实动因，试图重新锁定独家优势。

**当一个客户年消费超过 100 亿美元时，供应商和客户的权力关系会发生根本性逆转。** AWS 与 Anthropic 已经过了这个临界点。

**评估**：条款最清晰 · 收益分成约 50% 毛利 · 权力天平渐趋平衡

---

## 三、第二类：咨询实施（Accenture / Deloitte / Cognizant / PwC / IBM / Infosys）——表面对等、实质不对等

这一类的真相用一句话概括：**Anthropic 用 1 亿美元的 Claude Partner Network，换来了价值数十亿美元的企业销售力量外包**。

### 部署规模与数字

| 合作方 | 规模 | 时间 |
|--------|------|------|
| **Deloitte** | 47 万员工部署，认证 15,000 人 | 2025-10 |
| **Cognizant** | 35 万员工部署 | 2025-11 |
| **Accenture** | Anthropic Business Group，培训 30,000 人 | 2025-12 |
| KPMG / PwC / IBM / Slalom | 多次合作 | 2024-2026 |
| **NEC** | 日本 3 万员工部署 | 2026-04-23（日本首个全球合作伙伴）|
| **Canva** | Claude Design 集成进 Canva Design Engine | 2026-05（ANZ 本地合作伙伴）|
| **Xero** | 财务 SaaS 平台引入 Claude 能力 | 2026-05（ANZ 本地合作伙伴）|

合计承诺投入超过 100 万 Claude 实践者。每培训一名"reinvention deployed engineer"，Anthropic 就增加了一名按纯效果付费的销售代理——此人在客户现场推销 Claude、部署 Claude、帮客户扩大用量。Anthropic 支付的成本是培训资源 + 认证体系 + 联合营销资金。

### 利益交换结构

| 方向 | 内容 |
|------|------|
| 咨询公司 → Anthropic | 数万人的销售实施网络（核心资产）；内部员工大规模 API 消费；Fortune 500 客户推荐与背书；监管行业的信任背书 |
| Anthropic → 咨询公司 | $1 亿 Partner Network 资金池；CCA-F 认证体系；新功能抢先访问；专属工程资源；联合行业方案 IP 共创 |

### 隐藏的权力不对称

合作的商业条款**全部保密**——这本身就是信号。当 Deloitte CCO 说"我们双方都有重大投入"却拒绝披露数字时，意味着 Anthropic 的条款极为有利：**没有给咨询公司任何收益分成**，让它们自行赚取实施服务费用，同时它们的内部员工部署直接成为 Anthropic 的 API 收入来源。

Accenture 的高级 AI 业务在 FY2025 录得 59 亿美元订单（同比翻倍）、27 亿美元营收（同比 3 倍）；但 CEO Sweet 在 FY26 Q1 后停止单独披露高级 AI 指标——AI 已嵌入所有大型转型项目。Deloitte 承诺 2030 年前投资 30 亿美元扩展 GenAI 与 Agentic AI 能力。

**单个 FDE 的年成本约 $25-30 万，但其推动的 Claude API 消费可能是这个数字的数十倍**——对 Anthropic 是极有利的杠杆比例。咨询公司既是 Anthropic 的客户，又是 Anthropic 的分销商——但**不是 Anthropic 的利润分享方**。

### 澳大利亚与新西兰（ANZ）区域扩张

2026 年 4 月 27 日，Anthropic 在悉尼正式开设区域办公室，并任命前 Snowflake 亚太区高级副总裁 **[Theo Hourmouzis](https://anthropic.com/news/theo-hourmouzis-general-manager-australia-new-zealand)** 为澳新区总经理。Theo 曾在 Snowflake 帮助金融服务、零售、航空和政府行业落地 AI 方案，引进后将在本地深化政府与企业客户关系。

**本地合作伙伴生态**：Canva 将 Claude Design 集成入其 Design Engine（Canva 的设计平台用户已可将 Claude Design 输出直接导入编辑）；Xero 将 Claude 能力引入财务工作流平台；YMCA South Australia（Claude for Nonprofits 合作方）在 65+ 个地点、1,250 名员工中部署 Claude 用于数据分析和内容创作。**本地终端企业客户**：Commonwealth Bank、Quantium、Australian National University、Murdoch Children's Research Institute、Garvan Institute of Medical Research、Curtin University。澳大利亚已获批向联邦非企业政府机构供货，是 Anthropic 在亚太地区率先实现政府采购合规的市场。

### 5 月 4 日 PE JV 的隐含张力

最值得关注的张力是 5 月 4 日新成立的 PE JV 与 Accenture / Deloitte 的关系。新 JV 直接做 AI 实施咨询，Anthropic 工程师驻场——文章措辞审慎"extends that delivery capacity further"（扩展现有能力），但当新公司规模扩大，与大型 SI 中端市场业务的重叠不可避免。

**Anthropic 如何维持"平台中立"将是接下来 12-24 个月最微妙的政治考验**。

**评估**：条款完全不透明 · 无收益分成 · 权力天平 Anthropic 主导

---

## 四、第三类：行业数据与平台（Snowflake / Moody's / Salesforce / S&P Global）——商业逻辑最清晰

这一类是所有合作中**利益结构最对称、商业逻辑最清晰**的一类。等式很简单：**数据护城河 + AI 推理能力 = 1+1 > 2 的复合价值**。

### 关键合作伙伴

| 合作方 | 合同规模 | 核心价值 |
|--------|---------|---------|
| **Snowflake** | $2 亿多年期 | 1.26 万企业客户；text-to-SQL 准确率 90%+ |
| **Salesforce** | 多年期（未披露）| Agentforce 360 基础模型；首个在 Salesforce trust boundary 内运行的 LLM |
| **ServiceNow** | 多年期 | Build Agent 默认模型；销售准备时间下降 95%；2.9 万员工部署 |
| **Moody's** | 未披露 | MCP 原生集成；6 亿实体数据嵌入 Claude 环境 |

### Snowflake 视角：必须要做的防御性投资

Snowflake 有 1.26 万家企业客户和治理完善的数据环境，但没有推理能力；Anthropic 有世界一流的推理模型，但没有企业数据访问权限。两者结合，Snowflake Intelligence 让业务人员用自然语言查询复杂数据——这是 Snowflake 单独无法实现的。

**这笔 $2 亿采购对 Snowflake 是必须做的防御性投资**：如果不接入 Claude，Databricks + 某 AI 模型会抢先实现自然语言数据查询，Snowflake 现有客户会流失。它无法自己构建推理能力，只能花钱买。

### Moody's 视角：用数据霸权换 Claude 环境优先位置

Moody's 的 MCP 集成是更主动的战略押注——把 Moody's 数据直接嵌入 Claude 界面，意味着金融机构在 Claude 里工作时，Moody's 数据是默认数据层，竞争对手（S&P Global、FactSet）的数据要花额外步骤才能访问。

**这是用数据霸权换取 Claude 环境中的优先位置**——一个从未在传统 SaaS 时代存在过的"用户界面卡位"机会。

### Claude for Financial Services 数据合作伙伴

围绕 Claude 金融垂直产品，Anthropic 已经把行业头部数据源全部接入：Box、Daloopa、Databricks、FactSet、Morningstar、Palantir、PitchBook、S&P Global、Snowflake、Moody's、LSEG、MSCI——这是金融行业可能遇到的几乎所有结构化数据源。

**评估**：保底收入（合同金额已披露）· 无收益分成 · 权力天平基本对称

---

## 五、第四类：终端企业客户——纯采购但风险最深

这一类合作最简单，也最关键——它是所有前三类合作存在的目的。终端企业按量付费，不谈分成，但是 Anthropic 收入核心来源（80% 收入来自企业客户）。

### 不同落地路径的成本结构

| 路径 | 示例 | 对 Anthropic 的成本 | 对企业的成本 |
|------|------|-------------------|------------|
| 直接 API | Bridgewater、Coinbase | 几乎零销售成本 | API 使用费 |
| 通过云市场 | Pfizer via Bedrock | 让渡 50% 毛利给 AWS | 零摩擦采购 |
| 通过咨询落地 | Banner Health | 部分 Partner Network 资金 | API 费用 + 咨询服务费 |
| 通过平台嵌入 | RBC via Salesforce | 让渡给 Salesforce 的利润 | 隐含在 Salesforce 订阅中 |
| 垂直方案 | NBIM（Claude for Financial Services）| 产品研发 + 支持成本 | Enterprise 定价 + API 量计费 |

**对 Anthropic 而言，路径越短、毛利越高**——这就是为什么直接 API 客户和垂直方案客户被 Anthropic 销售团队重点养护。

### 旗舰案例的"标杆数据"

Anthropic 把这些客户成果做成行业标杆数据，用来吸引下一批：

| 客户 | 成果 |
|------|------|
| NBIM 挪威主权基金（$1.8 万亿 AUM）| 生产力提升 20%，年省 213,000 工时 |
| AIG | 承保审查时间压缩 5 倍以上，数据准确率 75%→90%+ |
| Commonwealth Bank | 客户诈骗损失下降 50%，欺诈事件下降 30%，客服量下降 40% |
| Banner Health（55,000 员工）| BannerWise 标杆案例 |
| Novo Nordisk | 临床研究文档 10+ 周→10 分钟 |

数据和案例形成正反馈循环——这就是 Series F 之后客户加速签约的核心引擎。

### 工作流锁定：终端客户的最大风险

终端企业面临的最大风险是**供应商依赖（Vendor Lock-in）**。当 NBIM 把 670 人团队的工作流全面接入 Claude，当 Banner Health 把 55,000 人的日常建立在 BannerWise 上——切换成本不再是技术问题，是组织重构问题。

Anthropic 的"三云全覆盖"在表面上降低了锁定风险（随时换云），但实际上**工作流锁定比云锁定更深**——员工的工作习惯、企业内的数据集成、定制化的 Prompt 工程——这些都是极难迁移的资产。

---

## 六、依赖程度与议价能力对照表

| 合作伙伴 | 依赖程度 | 议价能力 | 核心原因 |
|---------|---------|---------|---------|
| AWS | 中高 | 中高 | 投资方地位 + 50% 毛利分成；但 $1000 亿采购承诺把 Anthropic 锁死 |
| Google Cloud | 中 | 中 | 早期投资方，与 AWS 竞争使 Anthropic 拥有谈判筹码 |
| Accenture | 高 | 低 | 3 万人培训 + 专属 Business Group = 战略押注无法撤退；无收益分成 |
| Deloitte | 高 | 极低 | 47 万员工部署 = 切换成本极高；条款完全不透明 |
| Snowflake | 中 | 中 | $2 亿合同有一定议价权；但竞争力依赖 Claude 推理 |
| **Thomson Reuters** | **极高** | **极低** | **CoCounsel 用 Claude Agent SDK = 核心产品依赖竞争对手** |
| NBIM / AIG | 极高 | 极低 | 全员工作流重建在 Claude 上 |

### 最危险的处境：Thomson Reuters 的悖论

Thomson Reuters 同时处于三个矛盾位置：

1. **客户**：购买 Claude API 驱动 CoCounsel
2. **竞争对手**：Cowork 法律插件直接竞争，股价单日跌 18%
3. **被颠覆者**：原有 LegalTech 护城河被正面挑战

这是平台战略最典型的困境——**当你的核心产品建立在竞争对手的 API 上，你其实在为竞争对手的平台化战略支付学费**。

但反向地，Thomson Reuters 在披露 CoCounsel 用户突破 100 万后单日**暴涨 11%**——证明"拥有不可替代数据资产的 SaaS 仍可反弹"。Westlaw 法律案例数据库 60+ 年的积累不是 Claude 能轻易替代的。这是 SaaSpocalypse 之后市场的成熟思考。

---

## 七、战略弧线：从分发管道到平台化跃迁

把所有合作放到时间轴上，能清晰看到一条战略弧线：

| 阶段 | 时间 | 核心动作 | 战略目的 |
|------|------|---------|---------|
| 第一阶段 | 2023 | AWS 战略合作 + Bridgewater 首批用户 | 建立分发管道 + 旗舰背书 |
| 第二阶段 | 2024 | Google / Azure 加入，三云全覆盖 | 把分发触达扩到所有主流云 |
| 第三阶段 | 2025 上半年 | Deloitte 47 万员工 · Claude for Financial Services | 行业纵深 + 标杆案例 |
| 第三阶段 | 2025 下半年 | Salesforce / Snowflake / Accenture Business Group | 数据层整合 + 销售军团激活 |
| **第四阶段** | **2026 年初** | **Cowork 法律插件 → SaaSpocalypse** | **平台化跃迁，正式进入应用层** |
| 第四阶段 | 2026 年 4 月 | Moody's MCP · Amazon $250 亿追加 · ARR $300 亿 | 算力强化 + 平台位置确立 |
| **第五阶段** | **2026 年 5 月** | **PE JV 8 家金融机构联合** | **咨询公司经济学进入战略** |

每一步都比上一步更难替代：

| 步骤 | 行动 | 性质 |
|------|------|------|
| 第一步 | 用算力换资本，资本换分发管道 | 触达基础 |
| 第二步 | 用分发管道触达终端，旗舰案例建立信任 | 案例积累 |
| 第三步 | 用咨询解决落地壁垒，行业方案提客单 | 最后一公里 |
| 第四步 | 用数据层强化工作流锁定，MCP 占领界面 | 数据护城河 |
| 第五步 | 直接进入应用层，把依赖自己的 SaaS 变成竞争对手 | 收割中间层利润 |

---

## 八、给四类合作伙伴的判断框架

### 如果你是云服务商
**核心问题**：如何防止 Anthropic 稀释你的独家优势？三云全覆盖让 AWS 从独家变成三分之一。AWS 的应对是**追加投资 + 深化技术绑定**（Trainium 芯片联合研发）。其他云服务商若没有投资关系的独家性，只能靠数据主权（本地化部署）、行业合规、价格竞争维持差异化。

### 如果你是咨询公司
**核心问题**：你是在帮 Anthropic 培养客户，还是建立自己的壁垒？Anthropic 进入应用层（Cowork、垂直方案、PE JV）的趋势不可逆，最终会吃掉部分实施咨询市场。咨询公司的护城河只有两个：**行业 Domain Knowledge** + **客户关系**。专注这两个壁垒，而非技术实施本身。

### 如果你是数据 / SaaS 平台
**核心问题**：你的数据护城河够深到让 Anthropic 不敢绕开你吗？Thomson Reuters 的教训：如果数据可被替代，或产品只是"模型 + 包装"，Anthropic 直接进入是时间问题。**能活下来的是拥有不可复制数据资产的公司**——Moody's 的 6 亿实体、Westlaw 的法律案例库。如果你只是在 Claude API 上包一层 UI，Anthropic 进入应用层只需要发布一个插件。

### 如果你是终端企业客户
**核心问题**：你的工作流锁定程度，是你能承受的吗？NBIM、Banner Health 是"全面押注"的极端案例——在当前阶段是合理效率选择，但需要清醒认识迁移成本。建议：
- 在工作流设计层面保持抽象层（API 网关、中间件）
- 保持多模型评估能力，避免单一供应商
- 避免内部数据资产直接绑定特定供应商
- **锁定可以接受，但要主动管理**

---

## 九、合作伙伴生态的本质

所有合作关系的最终指向是一个问题：**企业在"思考"的时候，调用的是谁的认知基础设施？**

当 NBIM 的分析师在 Claude 里查投资组合，当 Banner Health 的医生用 BannerWise 看病历，当花旗的工程师用 Claude 写代码，当 AIG 的核保人用 Claude 审单——这些工作流的每一次运转，都是对 Claude 认知基础设施的一次调用，都是对 Anthropic 的一笔账单。

但更重要的是：**每一次调用都是一个数据点**，告诉 Anthropic 企业实际工作中需要什么。这是任何竞争对手都无法通过购买数据集复制的优势——它是实时的、生产环境的、有标注的真实需求信号。

**Anthropic 的合作伙伴生态本质**：用"安全"换信任，用"信任"换渗透，用"渗透"换锁定，用"锁定"换定价权。所有合作伙伴，无论是 AWS、Accenture、Snowflake 还是 NBIM，都是这个过程中的一个环节。没有任何一个环节是"利他"行为——但也没有任何一个环节是单方面剥削。这是一场**精密设计的利益共同体建设**。

问题是：当 Anthropic 最终完成平台化、成为不可替代的认知基础设施时，这些合作伙伴的议价能力会在哪里？

这个问题，现在没人有答案。但 Thomson Reuters 的股票图表，已经提前给出了市场的预判。

---

*本系列下一篇：[04 安全与对齐](Anthropic-公司全景-04-安全与对齐.md)——RSP / Constitutional AI / 可解释性如何被做成商业护城河。*

*数据来源：[Anthropic 官方 Blog](https://anthropic.com/news) · [Amazon 计算资源公告](https://anthropic.com/news/anthropic-amazon-compute) · [NEC 合作公告](https://anthropic.com/news/anthropic-nec) · [ANZ 扩张 / Theo Hourmouzis 任命](https://anthropic.com/news/theo-hourmouzis-general-manager-australia-new-zealand) · Snowflake / Moody's / Salesforce 联合公告 · Anthropic Partner Summit · HorsesForSources · Menlo Ventures 2025 State of Generative AI · 行业媒体报道*
