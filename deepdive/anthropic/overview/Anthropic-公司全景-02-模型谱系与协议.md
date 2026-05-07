# Anthropic 公司全景 · 02｜模型谱系与协议层创新

> 一句话提要：28 个月 17 次模型发布，从 Claude 3 Opus 的 86.8% MMLU 到 Opus 4.7 的 87.6% SWE-bench Verified——这是模型迭代速度。但 Anthropic 真正改变行业的不是模型本身，是它在协议层做的三件事：MCP（捐给 Linux Foundation 之后已成 Agent 时代事实标准）、Computer Use（OSWorld 从 22% 到 72.5%）、Mythos（自主发现 27 年 OpenBSD 零日）。

```
日期：2026-05-05
系列：Anthropic 公司全景，共 7 篇
本篇主题：模型谱系与协议层创新
受众：AI 从业者 / 投资人
```

---

## 一、Claude 模型谱系：17 次发布的能力跃迁

把 28 个月里所有 Claude 模型版本列出来，能直接看到 Anthropic 的迭代节奏从"季度一次"加速到"月度一次"：

| 时间 | 版本 | 关键指标 | 行业意义 |
|------|------|---------|---------|
| 2024-03 | Claude 3 系列（Opus / Sonnet / Haiku）| MMLU 86.8% / HumanEval 84.9% | 首次三档命名 + 视觉多模态 |
| 2024-06 | Claude 3.5 Sonnet | SWE-bench Verified 49.0% | Opus 1/5 价格 + 2 倍速度反超 + Artifacts 工作区 |
| 2024-10 | Claude 3.5 Sonnet v2 + Computer Use | OSWorld 22.0% | **业界首个商用 computer use** |
| 2024-10 | Claude 3.5 Haiku | SWE-bench 40.6% | 小模型逼近 Claude 3 Opus |
| 2025-02 | **Claude 3.7 Sonnet + Claude Code** | SWE-bench 70.3% | **首个 hybrid reasoning + Claude Code 起点** |
| 2025-05 | **Claude 4 系列** | SWE-bench 72.5%/72.7% | Interleaved thinking + **首个 ASL-3 模型** |
| 2025-08 | Sonnet 4 1M context | 75K+ 行代码 | 长上下文进入实用 |
| 2025-09 | **Sonnet 4.5** | SWE-bench 77.2% / OSWorld 61.4% | 30+ 小时持续任务 |
| 2025-10 | Haiku 4.5 | SWE-bench 73.3% | 小模型获得 Extended Thinking |
| 2025-11 | **Opus 4.5** | **SWE-bench 80.9%** | **首破 80% + 定价砍 67%** |
| 2026-02 | **Opus 4.6 / Sonnet 4.6** | OSWorld 72.5%（Sonnet）| 1M context GA + Adaptive Thinking + Agent Teams |
| 2026-04 | **Opus 4.7** | **SWE-bench 87.6%** | xhigh effort + Task Budgets + 3.75MP 视觉 |
| 2026-04 | **Mythos Preview** | 自主发现数千个 0day | **Project Glasswing 11 家合作伙伴定向预览** |

把这条线性化看，2025 Q1 是第一个分水岭（3.7 Sonnet + Claude Code），2025 Q3-Q4 是第二个（Opus 4.5 破 80%），2026 Q1-Q2 是第三个（4.6/4.7 配合 Cowork 平台化）。每一次分水岭都不只是"分数变化"，而是**伴随着新的产品形态从模型层涌出**。

---

## 二、Hybrid Reasoning：把"推理"从模型分裂回归整合

2025 年 2 月 Claude 3.7 Sonnet 发布时，Anthropic 做了一个对行业判断有深远影响的选择——拒绝 OpenAI 的"o1 / o3 单独推理模型"路径，走"hybrid reasoning"：**同一个模型既能做标准回答也能做深度推理，开发者通过 API 设置思考预算**（最高 128K tokens）。

这背后的态度声明很清楚：

> "推理应该是前沿模型的整合能力，而非独立模型。"

这条路径选择一年后看回去，Anthropic 是对的。Extended Thinking 框架已经走完了四代演进：

1. **Claude 3.7 Sonnet（2025-02）**：二元启用模式
2. **Claude 4（2025-05）**：Interleaved thinking——推理过程中可以调用工具
3. **Opus 4.5（2025-11）**：Effort 参数（low / medium / high）显式控制
4. **Opus 4.6 / Sonnet 4.6（2026-02）**：Adaptive thinking——模型自决是否深度思考
5. **Opus 4.7（2026-04）**：xhigh effort 等级 + Task Budgets

每一代都把推理控制粒度做得更细。OpenAI 的 o 系列被迫在 2025 年底也把"推理 + 标准"合并到 GPT-5 系列里——本质上是采纳了 Anthropic 的判断。**这是 Anthropic 在产品哲学层面赢的一仗**。

---

## 三、MCP：从一家公司的协议到 Linux Foundation 治理的事实标准

2024 年 11 月 25 日，Anthropic 发布 Model Context Protocol（MCP），基于 JSON-RPC 2.0，被业界很快比作"AI 的 USB-C"。它解决的是传统 N×M 集成困境——每个 LLM 应用都要为每个数据源单独写连接器，协议层的统一让这个矩阵变成 N+M。

MCP 的关键采纳节点是 2025 年中：

- **2025-03-26**：OpenAI 全面集成 MCP；Sam Altman 公开表态 "People love MCP"——这是 MCP 从一家公司协议变成行业协议的转折点
- **2025-04**：Google DeepMind 集成；Hassabis 称其"rapidly becoming an open standard"
- **2025-05 Build**：Microsoft 全面集成至 Copilot Studio、Semantic Kernel、Azure OpenAI

规范在 2025 年陆续吸收企业级要求：3 月加入 OAuth 2.1 + PKCE 与 Streamable HTTP；6 月强制 RFC 8707 Resource Indicators；11 月引入 CIMD 取代动态客户端注册。最关键的一步在 **2025 年 12 月 9 日**：

> Anthropic 把 MCP 捐赠给 Linux Foundation 旗下新成立的 Agentic AI Foundation（AAIF）。

AAIF 由 Anthropic、Block、OpenAI 共同奠基，AWS、Google、Microsoft、Cloudflare、Bloomberg 提供支持。同时进入 AAIF 的还有 Block 的 goose 与 OpenAI 的 AGENTS.md。**这是 OpenAI 与 Anthropic 第一次在协议层共同发起治理实体**——意义不亚于早年 Linux Foundation 接管 Kubernetes。

MCP 的增长指标在 2026 年初已经压不住：

- **月度 SDK 下载量约 9700 万次**（16 个月内）
- **10,000+ 官方注册服务器**，社区估算 16,000-18,000+
- 一线客户端支持：ChatGPT、Claude、Cursor、Gemini、Microsoft Copilot、VS Code

**[2026 年 5 月：创意工具 MCP 连接器群集发布](https://anthropic.com/news/claude-for-creative-work)**——Anthropic 在金融（FactSet / Morningstar / Bloomberg）、法律（Harvey / LSEG）之后，将 MCP 生态纵深推进至创意专业领域。8 个官方连接器密集上线：Blender（官方 MCP，自然语言操作 Python API，支持整个场景的分析调试与批量脚本）、Autodesk Fusion（对话式 3D 建模）、Ableton Live（实时控制音频工作流）、Adobe Creative Cloud（Photoshop / Premiere / Express 等 50+ 工具）、Affinity by Canva（批量图像处理与层操作自动化）、SketchUp（对话生成 3D 建模起点）、Splice（音频样本自然语言搜索）、Resolume Arena（VJ 实时视觉控制）。Anthropic 向 Blender Foundation 提供一次性捐款支持 Python API 开发，同时与 Rhode Island School of Design、Ringling College、Goldsmiths University of London 合作开展 AI 创意教育项目。这标志着 MCP 生态从 **"DevOps 工具集"向"跨专业领域操作系统"** 的跨越。

**捐赠的战略含义**：Anthropic 用"放弃单家治理权"换取"事实标准地位"。当 MCP 不再是 Anthropic 的协议时，反而所有人都更愿意采用——这是开放标准最经典的反直觉策略。同时 MCP 的核心代码、维护者、文档生态依然由 Anthropic 主导，**协议捐赠 ≠ 影响力让渡**。

---

## 四、Computer Use：OSWorld 从 22% 到 72.5%

2024 年 10 月 Claude 3.5 Sonnet v2 发布时，Anthropic 做了一件让人意外的事——**业界首次商用 computer use**。Claude 可以看屏幕截图、点鼠标、敲键盘、操作普通桌面应用，无需专门的 API 集成。

Computer Use 的进化曲线很陡：

| 版本 | OSWorld 得分 | 时间 |
|------|-------------|------|
| Claude 3.5 Sonnet v2 | 22.0%（含工具）| 2024-10 |
| Sonnet 4.5 | **61.4%** | 2025-09 |
| Sonnet 4.6 | **72.5%** | 2026-02 |

OSWorld 是评估 AI 在真实操作系统中完成任务的基准。从 22% 到 72.5%，**18 个月翻 3.3 倍**。这条曲线带来的产品衍生是：

- **Claude in Chrome（2025-08）**：Computer Use 在浏览器内的具象
- **Claude Cowork（2026-01）**：Computer Use 在桌面端的具象
- **Claude for Excel（2026-Q1 beta）**：垂直办公工具的具象

**Computer Use 是 Anthropic 跨越"API → 应用层"门槛的关键技术**。如果没有它，Anthropic 只能做更好的 Chatbot；有了它，Anthropic 可以直接在用户的工作环境里"接管"应用——这是 SaaSpocalypse 能发生的技术前提。

---

## 五、Mythos / Project Glasswing：能力溢出的 B2G 入场券

2026 年 4 月 Anthropic 发布 **Mythos Preview**——一个仅向 11 家网络安全 / 关键基础设施合作伙伴（AWS、Apple、Broadcom、Cisco、CrowdStrike、Google、JPMorgan Chase、Linux Foundation、Microsoft、NVIDIA、Palo Alto Networks）开放的研究预览。Mythos 的能力指标震动整个行业：

- **数周内自主发现数千个零日漏洞**
- **27 年 OpenBSD 零日 / 23 年 Linux / 17 年 FreeBSD**
- **单次利用成本 $50-$2,000、零人工干预**
- **所有主流操作系统和浏览器都中招**

Anthropic 的官方表述是"too dangerous to release"——明确表示**不打算通用发布**。这一叙事本身就是营销：把 Mythos 与"普通 LLM"的客户群完全隔离开，定价 $20K/次扫描，与 Palantir / Booz Allen / Mandiant 的 B2G 工具直接对标。

随后的 **[Project Glasswing](https://anthropic.com/glasswing)** 才是真正的战略动作：12 家核心合作伙伴 + 40 家扩展访问 + $1 亿使用额度 + $400 万开源捐款。这不是产品发布，是**联盟构建**——拿到这 12+40 家的关系网，就等于拿到了金融基础设施 / 关键开源项目 / 国防承包商的入门券。

**白宫从恐惧到采购的 ~3 周转向**记录如下：

```
Mythos 发布 + Cybench 100% 饱和
    ↓
~2 周内：财长 + 美联储紧急召集华尔街 CEO（系统性金融风险）
        DC Circuit 维持五角大楼"供应链风险"标签
    ↓
2026-04-16：白宫向联邦机构开放 Mythos（Project Glasswing）
        OpenAI 同步：$10M 给开源安全 + GPT-5.4-Cyber 开放给 BoA / Goldman / CrowdStrike
```

转向逻辑很简单：限制政府使用 Mythos 不能让漏洞消失，**只会让政府防御能力落后于已经能用类似工具的攻击者**。

---

## 六、API 能力时间线：把 token 经济做厚

模型能力之外，Anthropic 在 API 层面做了一系列让企业用得起的事：

| 时间 | 关键能力 | 商业含义 |
|------|---------|---------|
| 2024-04 | Tool Use GA | 启动 Agent 经济 |
| 2024-08 | Prompt Caching | 最高降本 90% |
| 2024-10 | Batch API | 50% 折扣 |
| 2025-01 | Citations | 企业合规要求 |
| 2025-02 | Extended Thinking + 128K output | 推理可控 |
| 2025-05 | Code Execution + MCP Connectors + Files API | Agent 进入工作流 |
| 2025-05 | Web Search API | $10 / 千次 |
| 2025-08 | 1M context | 大型文档场景 |
| 2025-11 | Structured Outputs | 程序化集成 |
| 2026-02 | 1M context GA（无溢价）| 把"长上下文溢价"标准化掉 |
| 2026-03 | 300K batch output | 大批量场景 |

每一次 API 升级都伴随着定价下调，Anthropic 的策略很明确：**用 API 价格降低对冲单 token 推理成本上升**。Opus 4.5 把价格从 $15/$75 砍到 $5/$25（降幅 67%）就是最直接的例子——一边靠模型能力上 SWE-bench 80%，一边靠定价让中型企业敢用 Opus。

**这是经典的 AWS 经济学**：单位成本下降速度快于销量增长速度时，毛利反而扩大。Anthropic 正在把 token 价格降到一个让企业重度部署都能接受的水平，同时靠 Trainium / TPU 自研芯片把推理成本压缩——两端剪刀差就是利润空间。

---

## 七、Agent SDK 与多 Agent 系统

2025 年 6 月 Anthropic 工程博客发布了一篇被业界广泛引用的研究：**多 Agent 系统比单 Agent Claude Opus 4 在研究任务上提升 90.2%**。给出的关键模式是 Orchestrator-Worker：Opus 4 作为"领导者"分解任务，多个 Sonnet 4 作为 subagents 并行执行。

更早的 2024 年 12 月《Building effective agents》定义了行业广泛引用的 5 种核心模式：

1. **Prompt chaining**（顺序链）
2. **Routing**（路由）
3. **Parallelization**（并行）
4. **Orchestrator-Workers**（编排-工人）
5. **Evaluator-Optimizer**（评估-优化）

这两篇文章配合 Claude Agent SDK 的开源，让"如何构建可靠的 Agent"从黑魔法变成可复制的工程实践。配合 Harness Engineering 系列（2026-Q1 发布的两篇）——Initializer Agent + Coding Agent + Generator-Evaluator 分离——Anthropic **把自家工程组的内部经验完整外化**，作为行业最佳实践推送。

**关键洞察是反直觉的**：

> "让 Agent 评价自己的输出"是 Agent 质量退化的最主要来源之一。

——所以需要 Generator + Evaluator 分离，让独立评估者而非生成者自我评价质量。这一观点与 NousResearch AutoReason 论文结论一致，在 Q1 末几乎成为多 Agent 设计的共识。

---

## 八、技术战略的元判断：能力下沉，价值上移

把这一篇所有线索整合成一个判断：**模型能力本身已不是护城河**。

理由很简单：

- Opus 4.7 SWE-bench Verified 87.6%，但 OpenAI GPT-5.5 已经 88.7%（晚 7 天发布）
- 2024 年初 Claude 3 Opus 与 GPT-4 的差距 ~6 个月，2026 年中 Anthropic 与 OpenAI 的差距压缩到 ~7 天
- 顶级模型的基准分数差异已经压缩到个位数百分点

但 Anthropic 不靠"模型分数最高"竞争。它把价值往三层上移：

**协议层**（MCP）：捐给 Linux Foundation 之后反而成为事实标准
**接口层**（Computer Use / Computer Use SDK / Agent SDK）：提供模型的"操作系统接口"
**应用层**（Claude Code / Cowork / 行业垂直）：直接面向终端工作流

**这三层都比"模型层"门槛更高、迁移成本更大**。当一个企业把 MCP 接入了 Claude、把 Claude Code 装进了开发流程、把 Cowork 跑成日常工作面板，模型层切换的成本就被层层放大——这才是真正的护城河，而不是 SWE-bench 多 1 个百分点。

技术上看，Anthropic 已经过了"靠模型分数赢"的时代——它在赌**协议、接口、应用三层叠加的复合锁定**比单纯模型领先更难被超过。这一判断如果对，下一个十年的赢家就是建立操作系统位置的公司，而非每周发新模型分数的公司。

---

## 这一篇的关键技术看板

| 维度 | 数字 | 备注 |
|------|------|------|
| 模型版本累计 | 17 | 2024-03 Claude 3 → 2026-04 Mythos Preview |
| Opus 4.7 SWE-bench Verified | **87.6%** | 与 GPT-5.5 88.7% 仅差 1.1 个百分点 |
| Sonnet 4.6 OSWorld | **72.5%** | Computer Use 18 个月翻 3.3 倍 |
| MCP 月下载量 | **9700 万次** | 16 个月内 |
| MCP 治理 | Linux Foundation AAIF | 2025-12-09 捐赠 |
| Mythos 联盟 | 12+40 家 | Project Glasswing |
| 多 Agent 任务提升 | **+90.2%** | vs 单 Agent Opus 4 |
| 行业 5 种 Agent 模式 | Anthropic 2024-12 论文定义 | 已成行业引用最高的 Agent 工程指南 |
| 创意 MCP 连接器 | **8 个**（Blender / Adobe / Ableton / Autodesk 等）| [2026-05 发布](https://anthropic.com/news/claude-for-creative-work)，创意行业首次系统性 MCP 覆盖 |
| Opus 4.7 选举政策合规率 | **100%** | [600 条提示测试](https://anthropic.com/news/election-safeguards-update)；Sonnet 4.6 99.8%；方法论开源 |
| Opus 4.7 政治中立评分 | **95%** | Vanderbilt / Foundation for American Innovation / Collective Intelligence Project [第三方验证](https://anthropic.com/news/election-safeguards-update) |

---

*本系列下一篇：[03 合作伙伴生态解构](Anthropic-公司全景-03-合作伙伴生态.md)——三云 / 咨询 / 数据平台 / 终端客户四类合作的真实利益结构与战略弧线。*

*数据来源：[Anthropic 官方 Blog](https://anthropic.com/news) & Engineering · [Linux Foundation / AAIF](https://lfaidata.foundation/) · GitHub Blog · TechCrunch / The New Stack / InfoQ · BenchLM / Vellum / Morphllm 多维度基准对比 · [Creative Work MCP 连接器发布](https://anthropic.com/news/claude-for-creative-work) · [选举安全保障更新](https://anthropic.com/news/election-safeguards-update)*
