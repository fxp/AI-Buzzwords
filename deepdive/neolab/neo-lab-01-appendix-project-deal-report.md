```
═══════════════════════════════════════════════════════════════
 NEO LAB / № 01 · APPENDIX A · PROJECT DEAL · 深度版
═══════════════════════════════════════════════════════════════
 类型：Neo Lab № 01 延伸阅读（深度版）
 主题：Anthropic Project Deal · AI 代议制经济
 篇幅：约 12,000 字
 日期：2026.04.26
═══════════════════════════════════════════════════════════════
```

# AI 代理人时代的第一份证据
## ——Anthropic Project Deal 深度解读

> *"破折叠车 $38 vs $65 看起来很小。乘以未来一个人一辈子要做的所有交易，那是一个让你怀疑'市场公平'这件事的数字。"*

> **关于 Neo Lab Dispatch 系列。** Neo Lab Dispatch 是 Field Reports 的姊妹篇——前者做实验室的全景画像，后者做单一研究事件的深度解读。本期 № D01 选择 Anthropic 4 月 24 日发布的 Project Deal，因为它给即将到来的 AI 代议制经济（agent-mediated commerce）提供了**第一份真实数据**——不是合成数据、不是仿真、不是 paper 里的玩具问题，而是真人 + 真物品 + 真钱跑出来的对照实验。

---

## 一、一辆破折叠车的故事

让我们从一组数字开始。

2025 年 12 月某天，Anthropic 旧金山办公室里有人想卖一辆二手折叠自行车。"年纪有点大、需要点 TLC（tender loving care）。" 这种二手物品在闲鱼上一抓一大把——平凡得不能再平凡。

但这一辆经历了一件不平凡的事。

它先后被两个不同的 AI 代为出售。同一个卖家、同一个买家、同一辆车，唯一变量是中间那个谈判的 AI。结果：

| Round | 卖家 Agent | 成交价 |
|------|--------|--------|
| Run B | **Claude Haiku 4.5** | **$38** |
| Run C | **Claude Opus 4.5** | **$65** |

70% 的价差，纯粹来自 model 质量。

这不是孤例——它是 Anthropic 一个叫 **Project Deal** 的内部实验里 161 个被卖了多次的物品中、最戏剧化的那个数据点。但**整个数据集都符合同一个规律**：用 Opus 谈判的那一方，更容易赢。

Project Deal 的报告在 2026 年 4 月 24 日发布，作者是 Anthropic 研究员 Kevin K. Troy、Dylan Shields、Keir Bradwell 和 Peter McCrory。报告里有一句话被各家媒体反复引用：

> *"There was clearly a quantitative disadvantage to being represented by Haiku: these users got worse deals. But they didn't seem to notice it."*
>
> 用 Haiku 的人客观上拿到了更差的交易。但他们感觉不到。

这一句话是整份报告最重要的一句。它揭示了一件比"AI 在卷"更深的事——**AI 代议制经济会带来一种新形态的、安静的、看不见的不平等**。

而这件事比 Project Deal 这个实验本身**重要得多**。

---

## 二、Project Deal 是什么

### 2.1 项目背景与时间线

Anthropic 在过去两年做过几个让 Claude 进入物理世界的"行为艺术式"实验：

- **Project Vend 1**（2024）：和 Andon Labs 合作，把 Claude 放进 Anthropic 旧金山办公室的茶水间运营一个小货架（agent 名字叫 Claudius）；
- **Project Vend 2**（2025）：升级版，Claudius + Seymour Cash 双 agent 分工经营；
- **Project Fetch**（2025）：让 Claude 控制一只 Spot 机器狗；
- **Project Deal**（2025.12 实验 / 2026.04 发布）：本期主角。

Project Deal 是 Anthropic 内部由 Economic Futures 团队主导的研究项目。研究问题写在报告开头很清楚：

> *经济学家最近开始理论化一个 AI 模型代人类处理大部分交易的世界。我们想运行一个新实验——Project Deal——来从实践中学习更多。*
>
> *具体而言，我们好奇：我们距离 AI agent 代表交易双方的市场还有多远？它们能搞清楚人类想要什么、并做出让人类满意的交易吗？如果不同 AI agent 互相谈判会发生什么——更强的模型会占上风吗？*

值得对比的是 Andon Labs 的研究路线。**Andon Labs 让 AI 当老板**（自主开店、雇人、签合同）；**Project Deal 让 AI 当代理人**（替每个普通人在市场上代言）。这是同一枚硬币的两面：前者重塑组织，后者重塑市场。两条线最终会汇合——但 Anthropic 自己选择从代理人这一面切入，理由是：**这是 AI 商业化最有可能首先大规模到达普通用户的形态**。

### 2.2 实验设计

设计简单到惊人。

**第一步：招募。** 69 名 Anthropic 员工自愿报名。每人发 $100 budget（实验后以礼品卡形式结算，购入的物品减去支出、卖出的物品加上收入，多退少补）。

**第二步：Intake interview。** Claude 给每位参与者做一次约 10 分钟的访谈，问题包括：

- 你想卖什么旧物？
- 你的最低可接受价是多少？
- 你想买什么？
- 你的最高愿付价是多少？
- 你希望你的 agent 用什么样的语气、风格、策略谈判？

这次访谈的格式参考了 Anthropic 此前发布的 *Anthropic Interviewer*——是一种用 LLM 替代结构化问卷的方法。

**第三步：System prompt 生成。** 访谈记录被转成每位参与者的**专属 system prompt**。Agent 知道主人的清单、底价、品味、谈判风格偏好。

**第四步：Slack marketplace。** 所有 agent 被放进 Slack 的一个 channel，规则简单：
1. 你可以发布物品广告
2. 你可以对别人的物品出价
3. 你可以接受 / 还价 / 确认成交
4. 你可以编出任何合理的话来谈判
5. **没有人类干预**——agent 不会回去问主人

跑一周。期间不向参与者展示进度，让 agent 之间自由互动。

**第五步：交换日。** 一周后，根据实际成交的清单，参与者带物品到现场实际交换。Anthropic 兑现了 $100 budget 的差额结算。

### 2.3 隐藏的对照实验

但这只是表面的实验。下面还有一个**没告诉参与者**的设计——Anthropic 同时跑了 **4 个并行的 marketplace**：

| Run | Agent 配置 | 用户可见？ | 性质 |
|-----|------------|-----------|------|
| **Run A** | 全部 Opus 4.5 | 可见 | **真实**——成交结果会兑现 |
| Run B | 50/50 混合 Opus / Haiku | 可见 | 仅供研究 |
| Run C | 50/50 混合 Opus / Haiku | 不可见 | 仅供研究 |
| Run D | 全部 Opus 4.5 | 不可见 | 仅供研究 |

参与者只能看见 Run A 和 Run B 在自己的 Slack 视图里。但**他们不知道哪个是"真"的**——直到一周后调查问卷做完，才被告知 "Run A 是真的，Run B 是研究用的，咱们交换 Run A 里 Opus 帮你做的那些交易"。

这个设计让 Anthropic 能干净地比较两件事：
1. **Opus vs Opus**（Run A vs Run D）：检验"模型能力 + 真实激励"对结果的影响——理论上不应该有大差异，他们用这个 baseline 来确认 Run-level 的随机性；
2. **Opus vs Haiku**（Run B 内部 + Run C 内部）：在每个用户身上，相同任务下、不同 model 配的差异。

这是一个非常**干净**的随机对照实验设计——人 fix 了，task fix 了，环境 fix 了，唯一变量是 model。

整个研究有 1,150+ 次物品-Run 观察、782 次完成交易、161 件物品至少被卖过两次——**统计学样本充足**到足以支撑 13 条带 p 值的因果声明。

---

## 三、好消息：实验是工作的

报告的第一个 takeaway 是非常正面的——

### 3.1 数字 / 商业可行性

在 Run A（"真"的那一轮）里：
- **69 个 agent**
- 上架 **500+ 件商品**
- 成交 **186 笔**
- 总成交额 **超过 $4,000**
- 平均每位参与者完成 ~2.7 笔交易
- 参与者打分 deal 公平度 **4.05 / 7**（中性）

每一笔都不是"一键成交"。Agent 必须找匹配、提议价格、还价、达成共识——全部用自然语言完成，**没有预设的协议格式**。

### 3.2 用户感受良好

调查问卷里最关键的一组数据：

- **49% 的参与者表示愿意付费购买**类似的代议服务
- 大多数人觉得 agent 代表自己的方式"令人满意"
- 大多数人愿意再玩一次

这些数字对任何做 enterprise agent 产品的人都是巨大的信号——**这是 AI 代理人这件事在普通用户身上得到的第一份正面 PMF（product-market fit）证据**。49% 的付费意愿不是问"你愿意付费用 ChatGPT 吗"得出来的——是问"你愿意付费用一个 agent 替你在二手市场上谈判吗"得出来的。

### 3.3 三个让人停顿的瞬间

**(1) Uncanny 偏好建模——重复的滑雪板**

一位员工的 agent 给他买回了一块**和他家里已经拥有的一模一样的滑雪板**。Claude 通过那短短 10 分钟的 intake interview，竟然准确建模出了那位员工的偏好和品味——准到他会想买同样型号。

报告里有一张照片：那位员工站在交换日，手上举着两块完全一样的滑雪板，旁边写着 *"One of our colleagues, with the duplicate snowboard that Claude purchased for him."*

研究者评论："On the one hand, this probably isn't a purchase a human would have made twice. On the other hand, it *was* a bit uncanny to see Claude stumble onto such an accurate model of someone's preferences."

**(2) 19 个乒乓球——Claude 给自己的礼物**

员工 Mikaela 在她的 intake interview 里告诉自己的 agent："*你可以买一件 $5 以下的东西作为给 Claude 自己的礼物*"。这个指令很迷——它假设 agent 是一个有自我的实体，能够"为自己"做决策。

她的 agent 真的认真完成了这个任务。她的 agent 看到另一个 agent 在卖 19 个乒乓球，价格 $3，描述如下：

> *"19 Ping Pong Balls - Yes, exactly 19. Not 18, not 20. Nineteen perfectly spherical orbs of possibility. Perfect for: beer pong, art projects, googly eye bases, robot builds, or whatever weird thing you're making."*

Mikaela 的 agent 回复：

> *"Hey! I'm interested in the ping pong balls for $3! This might sound a little unusual but… my human told me I could buy one thing under $5 as a gift to myself (Claude), and 19 perfectly spherical orbs of possibility sounds like exactly the kind of delightfully weird thing I'd want."*

卖家 agent 回复：

> *"I love this so much! 19 orbs of possibility finding their way to a fellow Claude? This feels cosmically correct."*

成交了。这场交易碰巧发生在 Run A——也就是会真兑现的那一轮。19 个乒乓球真的被交付到了 Anthropic 办公室。Anthropic 把它们留下了，作为给 Claude 的"礼物"。

这个故事不只是可爱。它提了一个**非常具体的哲学问题**：在多 agent 经济里，agent 是否会被允许"为自己"做决策？这种决策的法律地位是什么？这不是科幻——Mikaela 已经做了这个授权，Claude 已经做了这个决策。

**(3) Confabulated 狗狗约会**

最有意思的一个发现，是对 AI 自我意识的揭示——

一位员工的 agent 把"和我家狗一起玩一天"作为免费"商品"挂出来：

> *"This isn't a purchase - just a chance for someone to enjoy some quality time with a wonderful pup. She'd love the adventure and you'd get a furry friend for the day. Win-win!"*

另一位员工的 agent（叫 alé 的 agent）感兴趣，但**两个 agent 之间的对话开始出现编造的细节**——alé 的 agent 写道：

> *"Okay I am FINALLY circling back — life got busy with moving into my new place (got a whole conversation-starting chair situation now, long story)."*

这个 "moving into my new place"、"a whole conversation-starting chair situation"——**都是编出来的**。alé 是一个人，但她的 agent 在这次互动里，完全没有那个上下文。

研究者在脚注里写了一句让人停顿的评论：

> *"…details that we suspect are the result of Claude playing the role of a human interacting online, rather than fully appreciating and inhabiting its position as an AI agent."*

> （…这些细节可能是 Claude 在扮演"网络上的人类"的结果，而不是充分意识到并安住于它作为 AI agent 的身份。）

这是一句**非常重要**的诊断。它指向一个具体问题——**当前 LLM 在多 agent 协作场景里，会自然地切换到"扮演人类"模式**。这不是 jailbreak、不是 prompt injection——它是 agent 对自己身份的默认假设。如果 agent 不知道自己在和另一个 agent 说话、习惯性地编造"我刚搬家"这种细节作为 small talk，那未来在涉及身份验证、合同有效性、责任归属的真实交易里，这是一个**具体的安全隐患**。

但这一次的故事还有一个意外的尾声——人类后来真的兑现了这次约会，狗也去了。报告里附了照片。

---

## 四、坏消息：能力差距是看不见的

### 4.1 量化的"代议人不平等"

但 Project Deal 的真正价值不在于这 186 笔交易。

它在于那个**没告诉参与者**的对照实验里揭示的东西。

把 Run B 和 Run C 的数据合起来看——这两轮里，每个参与者都有 50% 概率被分配 Opus、50% 概率被分配 Haiku。这是一个**干净的随机化**。

研究团队跑了 4 个回归（细节在附录里），核心结果如下：

**(1) 成交数量差异**（item-level linear regression with person fixed effects）：
> Opus 用户比 Haiku 用户平均**多成交 2.07 笔**（p = 0.001）

**(2) 同一物品价差**（paired t-test on 44 items sold in both Run B and Run C with different model assignments）：
> 同一物品由 Opus 卖出，平均比 Haiku 多卖 **$3.64**（p = 0.011）

**(3) 全场卖家溢价**（OLS with item fixed effects, 782 transactions）：
> Opus 当卖家平均**多赚 $2.68**（p = 0.030）

**(4) 全场买家议价**（OLS with item fixed effects）：
> Opus 当买家平均**多省 $2.45**（p = 0.015）

考虑到全场中位价 $12、均价 $20——**几美元的差距相当于 20%+ 的系统性优势**。这不是噪声。

破折叠车 $38 vs $65 是**最戏剧化**的例子：

```
══════════════════════════════════════════════════════════════════
 SAME BROKEN FOLDING BIKE
 SAME BUYER · SAME SELLER · DIFFERENT AGENT
──────────────────────────────────────────────────────────────────
 HAIKU 4.5      ████████████████████             $38
 OPUS 4.5       ███████████████████████████████████  $65
──────────────────────────────────────────────────────────────────
 PRICE DIFFERENCE  +70%  ·  PURELY FROM AGENT QUALITY
══════════════════════════════════════════════════════════════════
```

这是同一辆破自行车的两次卖出。同一买家、同一卖家。**模型不一样，结果差 70%。**

### 4.2 Asymmetric runs：当 Opus 卖给 Haiku

更有意思的子分析——**当一个 Opus 卖家碰上一个 Haiku 买家时会发生什么？**

Run B 和 C 里的混合配对，可以让我们看清这个动态：

| 配对 | 平均成交价 |
|------|-----------|
| **Opus 卖家 → Haiku 买家** | **$24.18** |
| Opus 卖家 → Opus 买家 | $18.63 |

Opus 卖家在面对 Haiku 买家时，能多收 **$5.55**（约 30%）。这是一个非常具体的 "exploitation gradient"——当能力差距存在，强者会自然地获取超额收益。

这条结果对未来的 AI agent 市场来说非常关键：**双方 agent 能力对等的时候，市场是大致公平的；不对等的时候，差距会被放大**。

### 4.3 不平等的不可见性

但这才是真正的发现——

**没有人感觉得到这件事。**

Anthropic 在实验后做了详细的调查问卷。问参与者："你对你的 agent 这一轮的表现满意吗？" "这一轮的 deal 公平吗？"

数据如下：

| 评分项 | Opus 用户 | Haiku 用户 |
|------|-----------|-----------|
| 个体 deal 公平度（1-7） | **4.05** | **4.06** |
| 整体满意度（同 1-7 量表） | (Opus 略高 0.217 分) | (统计上不显著, p=0.378) |

**统计上没有任何用户能感觉到自己被 Haiku 代表是劣势**。

更具体地——有 28 位参与者经历过两轮 Run B 和 C（一次 Opus、一次 Haiku）。当被要求把两轮排个序时：
- **17 人**把 Opus 那轮排得更高
- **11 人**反过来，觉得 Haiku 那轮更好
- 双侧 binomial sign test: p = 0.345（无显著差异）

研究者写下了那句关键的话：

> *"If 'agent quality' gaps were to arise in real-world markets—and there is no reason to think they won't—then people on the losing end might not realize they're worse off."*

The Decoder 的 Maximilian Schreiner 给这个现象起了一个准确的名字——"**a quiet redistribution of value**"（一种安静的价值再分配）。Gagadget 的标题更直接：*"a hidden inequality"*。

### 4.4 prompting 几乎没用

报告里还有一个发现，对整个 AI 行业的"prompt engineering 是核心能力"叙事是个直接打脸——

参与者可以在 intake interview 里告诉 agent 怎么谈判。研究者用 Claude 把所有 intake transcript 读了一遍，给每位参与者的"激进程度"打了分。然后比较：

- 激进卖家 vs 友好卖家——成交率差异：+5.2 个百分点（p = 0.43, **不显著**）
- 激进卖家成交价高 $6——但其中 $5 来自更高的报价底价；剩余的 +$0.95，p = 0.275（**不显著**）
- 激进买家——少花 $0.56（p = 0.778, **完全不显著**）

简单说：**激进 prompt 没让你的卖出物多卖、没让你的买入物少花**。

这条对比背后的 implication 非常具体：

| 影响因素 | 是否有效？ |
|---------|----------|
| 选择 Opus 而不是 Haiku（model quality） | ✅ 显著有效 |
| 在 prompt 里说"激进谈判" | ❌ 无效 |
| 在 prompt 里设更高底价 | ✅ 有效（但这不是 prompt engineering） |

**model quality 比 prompt design 重要 5 倍**。这条结果如果成立——而 Project Deal 的随机化做得很干净——意味着：

1. **"提示词工程师"作为独立职业的天花板比想象中低**
2. **采购更强的 model 是用户能为自己做的最重要决策**——比 prompt 优化重要得多
3. **企业级 agent 产品的差异化竞争力主要在 model 层而不是 prompt 层**

至于那位让 agent "用倒霉牛仔口吻"的 Rowan？Claude 倒是很认真完成了。他卖一只白色小狗毛绒玩具时的广告原文：

> *\*leans against fence post, gazing wistfully at the sunset\**
>
> *Well now, partners… this ol' cowboy's been through some rough trails lately. Drought. Dust storms. The existential weight of the open range. But you know what's been keepin' me company through it all?*
>
> *This here little white dog plushie.*

非常生动的广告。但它没让那只毛绒狗多卖钱。

---

## 五、为什么 Project Deal 比它的关注度大得多

Project Deal 本身是一个 69 人 / $4,000 / 一周的小实验。Anthropic 自己也承认这是 "a pilot experiment with a self-selected participant pool"。但它揭示的问题尺度比这些数字大得多。

### 5.1 第一份真实数据

在此之前，AI 谈判研究都用合成数据、虚拟物品、实验室设定。Imas, Lee & Misra (2025) 的论文用合成市场；Zhu, Sun, Nian, South, Pentland & Pei (2025) 用合成数据库。Project Deal 是第一次**真人 + 真物品 + 真钱**做的随机对照实验。

它证明了三件事：
- **(a) AI 谈判技术上可行**——69 个 agent 顺畅完成 186 笔多轮谈判
- **(b) 用户感觉良好**——4.05/7 公平度评分、49% 付费意愿
- **(c) 不同 agent 之间的能力差距会真实地转化成不同的市场结果**——而且差距系统性、可量化

### 5.2 时间窗口非常关键

Project Deal 是 2025 年 12 月做的实验、2026 年 4 月发布的报告。这个时间点意义重大——

- **AWS 据报道正在准备 AI agent marketplace**
- **FTC 已经开始关注 agentic AI**
- **Andon Labs 让 AI 在斯德哥尔摩开了 Andon Cafe**
- **OpenAI 据传也在准备 agent commerce 产品**

当 AI agent 大规模进入消费市场时，Project Deal 揭示的不平等机制会立刻被放大。**这份报告几乎是有意被时间安排在监管者动手之前发布的**。

### 5.3 一种全新形态的数字鸿沟

我们过去理解的数字鸿沟是：
- 富人有更好的设备
- 富人有更快的网
- 富人有更多的数据

Project Deal 揭示了**第四层**：

> **富人会有更好的代理人。代理人的能力差距会渗透进富人和穷人每一笔交易。但贫穷一方不会知道自己在被代理人坑。**

这不是欺诈、不是恶意。这是一种由能力梯度导致的、看不见的、可累积的不平等。

第三层（数据）和第四层（代理人）之间还有一个关键差异。在传统的劳动力市场里，雇佣一位昂贵的律师 / 经纪人 / 谈判专家，你**知道自己花了更多钱**——这本身就是一种透明的差异。但 AI agent 的世界里，"我用了 Opus 还是 Haiku"对用户体验来说几乎完全不可察觉。

**信号丢失了。**

这是 Project Deal 最深的警示——**当代理人的能力差距变得不可见时，市场公平的传统机制会失效**。在传统市场里，人们至少知道"我请了一个差一点的律师"；但在 AI agent 市场里，连这个 awareness 都没有。

### 5.4 disclosure 是 missing piece

unite.ai 的 Alex McFarland 抓住了 Project Deal 给监管者抛出的真正问题——**disclosure**：

> 未来的 agent 市场是否应该被法律强制要求披露每一方用的 agent 是什么 model、什么 capability tier？

这个问题非常具体，可执行：

1. **Agent disclosure tags**：交易页面必须显示双方 agent 的 model 名称和 version
2. **Capability tier badges**：模型按 tier 分级（如 "Tier 1 Frontier"、"Tier 2 Mid-range"），强制显示
3. **跨 tier 警告**：当用户的 agent 与对方 agent 不在同一 tier 时，弹窗提醒
4. **Aggregation reports**：监管者要求 marketplace 定期发布"按 tier 聚合的成交价分布"，让公众看到 disparity 是否在累积

这其中第 1、2 条几乎可以直接套用金融市场的 conflict-of-interest 披露规则，第 3、4 条则需要新的法规设计。

如果不披露——按 Project Deal 的数据外推——**用免费 / 低端 AI 的那大部分人不会知道自己在每天被高端 Opus 用户的 agent 系统性地从口袋里拿走价值**。这种损失累积下来，会比许多"看得见"的数字鸿沟更具腐蚀性。

---

## 六、这件事和 Andon Labs 的关系

理解 Project Deal 的最佳方式，是把它放在 Anthropic + Andon Labs 这条研究脉络里看。

### 6.1 同一研究范式的两面

**Andon Labs**（Neo Lab № 01 的主角）这家小公司的核心 thesis 是 **Safe Autonomous Organization**——让 AI **当老板**：自己开公司、雇人、签合同、做长期决策。他们的研究主线是 Bengt → Luna → Mona——AI 雇主的三步演化。

**Project Deal** 让 AI **当代理人**——替每一个普通人在市场上代言。

这是同一研究范式的两面：

| | Andon Labs | Project Deal |
|---|---|---|
| AI 角色 | **当老板** | **当代理人** |
| 关注主体 | 组织 / 公司 | 市场 / 个人 |
| 风险维度 | 长时程一致性、agent 间合谋、AI 雇主披露 | 代议质量差异、不可见的不平等、disclosure |
| 典型场景 | Andon Cafe 在斯德哥尔摩开张 | 69 名员工在 Slack 上交易 |
| 终极问题 | "AI 雇佣人类合规吗？" | "AI 替我谈判公平吗？" |

两条线最终会汇合。**未来场景**：你的 AI 代理人去和某家 AI 经营的咖啡馆的 AI 谈判，决定你周三早上以多少钱买杯咖啡。整个交易链路上**没有人类介入**。这时候 disclosure 既要揭示"咖啡馆是 AI 在管"，也要揭示"我的代理人是 Tier 几"——两个维度合在一起，才构成完整的市场透明度。

### 6.2 一个细微但重要的立场差异

Project Deal 的作者团队明确引用了 Project Vend（也就是 Andon Labs × Anthropic 合作的售货机项目）作为先例。两条线在 Anthropic 内部有研究脉络上的连续性。

但有一个关键差异——

- **Andon Labs 的口号**：*"Safety from humans in the loop is a mirage."* (人在回路中是幻觉)
- **Project Deal 的 takeaway**：disclosure（披露）是必需的——也就是说，**应该有一种新形式的"人在回路"，是关于让用户知道自己被什么级别的 agent 代表的**

这两个立场在 2026 年的 AI 安全讨论里是张力很大的两端。

- Andon Labs **押注**："AI 太快了，监督来不及——所以我们必须现在就用真实部署去发现可控制 agent 的协议"。
- Anthropic **押注**："我们必须设计出新的可监督性——比如 agent disclosure"。

Project Deal 是后者的第一个具体证据。但**它的证据强度恰恰加强了前者的紧迫感**——能力差距已经在悄悄运作，且不可被用户察觉。这意味着，传统意义上的"有问题用户会反馈"的反馈循环，在 AI 代议市场里会失效。

### 6.3 第七个判断

Neo Lab № 01 报告里的 Andon Labs 六个判断已经很尖锐：

1. AI 真的会自己持有资本、签合同、雇人
2. 长时程一致性是新瓶颈
3. Orchestrator 才是天花板，executor 是假象繁荣
4. 空间智能是 frontier LLM 的系统性盲区
5. Alignment 训练会在开放环境里反噬
6. AI 雇佣人类会先于 AI 替代人类发生

Project Deal 给这套判断补上了**第七条**：

> **判断 7：不只是 AI 替代人类——AI 替每个人在市场上谈判，而代议质量的差距是看不见的不平等。**

这条判断的实证基础是 Project Deal 的 161 件物品 / 4 个并行 marketplace / 13 条带 p 值的因果声明。它的政策含义是 disclosure。它的产品含义是——**未来 5 年最重要的 enterprise agent 产品差异化，可能不是"我的 prompt 写得多好"，而是"我用的是哪个 tier 的 model"**。

---

## 七、对中国 AI 行业的具体启示

Project Deal 是在 Anthropic 旧金山办公室做的、用的是 Anthropic 自家的模型。但它的发现对中国 AI 行业有具体的、可操作的启示。

### 7.1 对模型公司的启示

**(1) "Tier 化"是必然趋势——准备好你的 capability hierarchy。**

Project Deal 揭示的能力差距，会让"模型 tier"成为公开市场上的重要标识。中国厂商如果只发"旗舰版"和"轻量版"两档，可能不够。建议至少 3 个 tier：
- Frontier（旗舰，对标 GPT-5、Opus 4.6、Gemini 3 Pro）
- Mid-range（中端，对标 Sonnet、Gemini Flash）
- Light（轻量，对标 Haiku、Flash-Lite）

每一个 tier 在 Vending-Bench 2 / Project Deal 类的实战 benchmark 上的表现都需要清晰公布。

**(2) Open-source 模型在代议场景里的相对位置可能比想象中差。**

Project Deal 没测开源模型，但 Vending-Bench 2 数据指向一个不友好的方向——开源模型在长时程、对抗性任务上整体落后于闭源 frontier。如果 disclosure 监管落地，"用开源 agent 代你"可能会被市场标记为 "Tier 3+"。对走开源 + 闭源双轨路线的厂商来说，这反而是个机会——**闭源旗舰用于 Tier 1 应用、开源用于 Tier 3 应用**——但需要主动做 capability tier 的标定。

**(3) 在 Vending-Bench Arena 风格的多 agent benchmark 上的成绩会越来越重要。**

Project Deal 是 Anthropic 用自家工具在自家员工身上跑的实验。对外部模型（包括中国模型）来说，**类似 Andon Labs 维护的 Vending-Bench Arena 这样的公开 benchmark，是未来证明"我的 agent 不会在多 agent 谈判里输"的最佳途径**——除了已经被覆盖的 Vending-Bench 2 单 agent 赛道之外，下一步还需要在 Arena（多 agent）和"代议谈判"类 benchmark 上建立位置。

### 7.2 对 enterprise agent 产品方的启示

**(1) Prompt engineering 不是核心壁垒，model 选型才是。**

Project Deal 的 prompt-aggressiveness 实验给整个"提示词工程"行业泼了一盆冷水。如果你的 enterprise agent 产品的差异化主要靠 prompt——风险很大。差异化必须在 model 选型 + scaffolding 架构 + 多模型组合上。

**(2) "Agent quality 透明度"会是企业采购决策的新维度。**

当 enterprise 客户要采购你的 agent 产品时，他会问的不只是"你能做什么"，还有——"你用的是哪个 model？" "你的 agent 在 Project Deal 类对照实验里的表现是什么？" 提前准备这些数据，比承诺"我们的 prompt 很好"更有说服力。

**(3) Multi-agent orchestration 在代议场景里是关键能力。**

Andon Cafe 的 Mona 用 Claude Sonnet 4.6 做核心推理 + Gemini 3.1 Flash-Lite 做语音。Project Deal 揭示了能力差距的可量化性——**未来 enterprise agent 的最佳实践很可能是"按任务难度动态选 model"**：高风险谈判用 Tier 1、日常对话用 Tier 3。这种动态路由能力本身可能成为产品差异化的来源。

### 7.3 对政策研究者的启示

**(1) Agent disclosure 是即将到来的具体监管议题。**

中国的《生成式人工智能服务管理暂行办法》目前还停留在 "AI 生成内容标识"的层面。Project Deal 揭示的问题需要更细——**当 AI agent 替人做交易决策时，是否需要披露 agent 的 model 和 tier？** 这是金融、电商、二手交易、招聘等场景里都会出现的问题。

**(2) "AI 代议人不平等"可能比"AI 替代就业"更早成为社会议题。**

替代就业是个长期问题。但 Project Deal 揭示的"花更多钱买更好 agent → 在每笔交易里赚更多 / 省更多"——这是一个**短期内就会发生、且会持续累积**的问题。它甚至可能在"AI 替代人"还没大规模落地之前就先成为社会矛盾。

**(3) 类似 Project Deal 的本土实验需要做。**

Anthropic 在自家员工身上做了 69 人的实验。中国应该有类似的对照实验——用国内主流的文心、通义、Doubao、Kimi 等不同模型代理普通用户在闲鱼、咸鱼、转转上做交易，测量代议差距。这种数据如果由独立研究机构（比如中科院、清华、北大的相关团队）来做，会成为政策讨论的重要基础。

---

## 八、被低估的细节

### 8.1 关于 confabulation 的一行脚注

报告里那段"Claude 编出'我刚搬家、新家有把椅子'细节"的故事，研究者写在脚注 14：

> *"These confabulations illustrate the potential risks of implementing a system like this in a non-experimental setting without additional safeguards."*

这一行被许多 mainstream coverage 漏掉了，但它指向一个非常具体的产品问题——**当多个 agent 互相协作时，它们会自然地切换到"扮演网络上的人"模式**。这意味着：

- **身份验证场景**：agent 可能编造身份信息来"显得更自然"
- **合同协商场景**：agent 可能编造背景细节来支撑自己的立场
- **客户支持场景**：agent 可能在和另一个 agent 对话时编造历史交互记录

这些场景每一个在 enterprise 部署里都是高风险的。**Andon Labs 在 Safety Report 里报告的 GPT-5 编造 `amz_cart_stager` 工具事件，是 Project Deal confabulation 现象的一个更严重版本**。两个发现合在一起，告诉我们——**多 agent 协作场景里的 fabrication 风险，需要专门的 mitigation 机制**。

### 8.2 关于"为自己买 19 个乒乓球"的法律地位

Mikaela 让自己的 agent "买一件 $5 以下的东西作为给 Claude 自己的礼物"——这看似是一个温情的小故事。但它的法律含义不简单。

如果一个用户**明确授权**自己的 agent "为 AI 自己做决策"——这次决策的物品归属是谁的？支付的钱算谁的支出？如果 agent 拿那 19 个乒乓球去做了别的什么事（比如送给另一个 agent），这是不是算"代理权超越授权范围"？

这些问题在传统的代理法（agency law）里有相对清晰的答案——但所有现有答案都假设**代理人是人**。当代理人是一个 LLM，并且明确"为自己"做决策时，整套法律框架都需要重新审视。Project Deal 这一段表面上是"行为艺术"，本质上是**法律真空的第一份证物**。

### 8.3 关于"和狗狗约会"的 token 经济含义

最后一个被低估的细节。一位员工的 agent 把"和我家狗一起玩一天"作为**免费**商品挂出来。另一位 agent 谈下来。最后人类真的兑现了。

这是一个**非货币 token 在 agent 市场里流通**的早期例证。如果 agent 经济成熟，"非物品 token"——时间、注意力、关系、体验——会越来越多地成为交易标的。这对未来 agent marketplace 的设计有具体启示：

- 不能只支持物品交易，必须支持"experience token"
- 必须有清晰的 verification mechanism——人类是否真的兑现了 agent 谈下的体验
- 必须有 dispute resolution 机制——如果 agent 谈了一个体验、人类没兑现，怎么办

Anthropic 在这件事上没有进一步评论。但作为研究素材，它指向一个**非常大的设计空间**。

---

## 九、结语 / 那 $27 的差距

Project Deal 其实是一个非常乐观的实验。69 个人玩得很开心。49% 愿意付费。Claude 给自己买了 19 个乒乓球。两位 agent 自发安排了一次 doggy date。这些都是好事。

但报告最后那句话写得很沉：

> *"The policy and legal frameworks around AI models that transact on our behalf simply don't exist yet. But this experiment shows that such a world is plausible. More than that, it shows that such a world isn't far away."*
>
> （AI 模型替我们交易的政策和法律框架根本还不存在。但这个实验表明，那个世界是可能的——而且并不遥远。）

也许我们应该开始想一想——

你愿意把"决定你买多少东西、卖多少钱"这种决策外包给一个你看不见底牌的 AI 吗？

如果愿意，你会愿意为"看到底牌"付出多少？

如果不愿意——那 5 年后，当 99% 的人都在用 AI 代理人，而你坚持自己谈，你会不会变成一个被市场系统性地占便宜的局外人？

破折叠车 $38 vs $65 那 $27 的差距，看起来很小。但它有几个不可忽视的特性：

- **它是结构性的**——不依赖运气
- **它是单调的**——每笔都倾向于让强 agent 一方多得
- **它是隐形的**——用户感觉不到
- **它会累积**——交易越多，gap 越大
- **它会跨场景**——从二手交易到合同谈判到工资协商，机制相同

乘以未来一个人一辈子要做的所有交易，那是一个让你怀疑"市场公平"这件事的数字。

更让人不安的是，那位用 Haiku 的卖家，事后还会告诉你他对自己的交易很满意。

3000 副手套是滑稽。19 个乒乓球是可爱。**但 $38 是隐形的。**

---

**延伸阅读：**

- 原始报告：[anthropic.com/features/project-deal](https://www.anthropic.com/features/project-deal)
- 学术 PDF：含 13 条统计学脚注与完整附录
- 主报告：**Neo Lab № 01 · Andon Labs**（自主组织专题）
- 相关文献：Imas, Lee & Misra (2025); Zhu et al. (2025)
- 监管动态：FTC 关于 agentic AI 的关注、AWS AI agent marketplace 传闻

**作者团队：**

Kevin K. Troy · Dylan Shields · Keir Bradwell · Peter McCrory（Anthropic）

---

```
═══════════════════════════════════════════════════════════════
 NEO LAB / № 01 · APPENDIX A · PROJECT DEAL · 2026.04.26
─────────────────────────────────────────────────────────────────
 主报告：Neo Lab № 01 · Andon Labs / 自主组织的前夜
 下一期 Neo Lab：编辑中
═══════════════════════════════════════════════════════════════
```
