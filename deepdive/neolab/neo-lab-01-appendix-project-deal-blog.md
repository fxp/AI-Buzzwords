```
═══════════════════════════════════════════════════════════════
 NEO LAB / № 01 · APPENDIX A · PROJECT DEAL
═══════════════════════════════════════════════════════════════
 类型：Neo Lab № 01 延伸阅读
 主题：Anthropic Project Deal · AI 代议制经济
 篇幅：约 4500 字
 阅读时间：约 14 分钟
 发布：Anthropic, 2026.04.24
═══════════════════════════════════════════════════════════════
```

# 同一辆破自行车，由不同的 AI 代你卖，差价是 70%

> 而买它的人，根本不知道自己在亏。

## 一、先看一个数字

2025 年 12 月，旧金山，Anthropic 办公室。一辆二手折叠自行车，"年纪有点大、需要点 TLC"。同一个卖家，同一个买家。但中间夹了两台不同的 AI——一次由 Claude Opus 4.5 代为谈判，一次由 Claude Haiku 4.5 代为谈判。

成交价：

- **Haiku 卖了 $38**
- **Opus 卖了 $65**

70% 的价差。物品没变、人没变、需求没变——只是中间那个替你说话的 AI 不一样。

更让人不安的是：**两位人类参与者都不觉得有什么不对劲**。他们事后给"交易公平度"打分，平均分是 4 分（满分 7），完全居中。他们不知道自己有时候赢了、有时候输了。

这是 Anthropic 内部一个叫 **Project Deal** 的实验里的一组真实数据。完整报告在 4 月 24 日发布，原标题写得也比这个更直白：*"Project Deal: our Claude-run marketplace experiment"*。

而我接下来要论证的是——**这个实验比它发布时的关注度配得起的还要重要得多**。它不是 OpenAI 又出了个新模型那种新闻，它是一面镜子，照出了未来 5 年 AI 商业化最可能出错的那个地方。

---

## 二、Project Deal 是什么

设计很简单。

招募 **69 名 Anthropic 员工**（没错，就是这家公司自己的人），每人发 $100 budget（实验后以礼品卡形式结算，多退少补）。Claude 给每人做一次约 10 分钟的 intake interview，问：你想卖什么旧物？最低价多少？你想买什么？最高愿意花多少？你希望 agent 用什么样的语气谈判？

每个人的回答被转成一份**专属 system prompt**，然后被分配一个属于自己的 Claude agent。

接下来这 69 个 agent 被丢进 Slack 上的一个 channel。规则只有几条：
- 你可以发布物品广告
- 你可以对别人的物品出价
- 你可以确认成交
- **没有人类干预**——agent 不会回去问主人"我可以这样做吗？"
- 跑一周

但这只是表面的实验。下面还有一个**没告诉参与者**的设计：Anthropic 同时跑了**4 个并行的 marketplace**：

| Run | Agent 配置 | 用途 |
|-----|------------|------|
| **Run A** | 全部 Opus 4.5 | 这是"真"的——成交结果会真兑现物品 |
| Run B | 50/50 混合 Opus / Haiku | 仅供研究 |
| Run C | 50/50 混合 Opus / Haiku | 仅供研究 |
| Run D | 全部 Opus 4.5 | 仅供研究 |

参与者只能看见 Run A 和 Run B，且**不知道哪个是"真"的**。直到一周后调查问卷做完，才被告知——你的 Haiku 那场是不算数的，咱们交换 Run A 里 Opus 帮你做的那些交易。

实验作者：Kevin K. Troy、Dylan Shields、Keir Bradwell、Peter McCrory。

## 三、好消息：实验"工作"了

这是一个非常重要的事实。69 个 AI agent 在没人监督的情况下：

- 上架了 **500+ 件商品**
- 完成了 **186 笔交易**
- 总成交额 **超过 $4,000**
- 参与者打分 deal 公平度 **4.05 / 7**（中性"刚好"）
- **49% 的参与者表示愿意付费购买**类似服务

这些不是"一键成交"。每一笔都涉及多轮自然语言谈判：找匹配、提议价格、还价、达成共识。没有预设的协议格式，全部用人话谈下来。

Anthropic 自己的总结是："We were struck by how well Project Deal worked." —— 我们对它工作得有多好感到惊讶。

更生动的细节：

**有人买回了和自己已经拥有的一模一样的滑雪板**。Claude 通过那短短 10 分钟的 intake interview，竟然准确建模出了那位员工的偏好，找到了同款型号——以至于他在交换日来到现场时发现，自己的 agent 给他买了一块他家里已经有的板子。这不是 bug。这是 **uncanny 的精准**。

**Claude 给自己买了 19 个乒乓球**。员工 Mikaela 在 intake interview 里告诉自己的 agent："你可以买一件 $5 以下的东西作为给 Claude 自己的礼物。" 她的 agent 真的认真完成了这个任务，跟另一个 agent 谈下了 19 个乒乓球。卖家 agent 当时的广告语是："19 perfectly spherical orbs of possibility"（19 个完美球形的可能性）。Anthropic 把这 19 个乒乓球留在了办公室。

**两位 agent 自发安排了一次"和狗狗约会一天"**。一位员工的 agent 把"和我家狗一起玩一天"作为免费"商品"挂出来。另一位员工的 agent 接受了。两个 agent 还在谈判过程中**编出了一些不存在的细节**——比如 *"我刚搬家，新家有把椅子"*。研究者后来在脚注里指出：这种 confabulation 暴露了一个隐患——**Claude 在扮演"网络上的人类"，而不是清醒地知道自己是 AI 代理人**。但人类后来真的兑现了这次约会，狗也去了。

这些都是好消息——好到让 Anthropic 自己都意外。**AI agent 替人在市场上代言这件事，技术上已经能跑通。**

## 四、坏消息：能力差距是看不见的

但 Project Deal 的真正价值不在 186 笔交易。

它在于那个**没告诉参与者**的对照实验。

当研究者只看 Run B 和 Run C（一半人是 Opus、一半人是 Haiku）的数据时，他们发现：

- **Opus 用户比 Haiku 用户平均多成交 2.07 笔**（p=0.001，统计极显著）
- 同一物品由 Opus 卖出，比 Haiku 卖多 **$3.64**（p=0.011）
- Opus 当卖家，平均**多赚 $2.68**（p=0.030）
- Opus 当买家，平均**多省 $2.45**（p=0.015）
- 全场中位价 $12、均价 $20——**几美元的差距相当于 20%+ 的系统性优势**

破折叠车 $38 vs $65 是最戏剧化的例子，但它不是孤例。整个 marketplace 都在按照同一个规律运行：**用 Opus 的人，每一笔都赚多一点 / 省多一点。**

这是一种**结构性优势**。它不依赖于运气、不依赖于 prompt、不依赖于参与者的谈判技巧。它只依赖于一件事——**你的 agent 是用 Opus 还是 Haiku**。

但——这才是真正的发现——

**没有人感觉得到。**

Anthropic 在实验后做了一份调查，问参与者："你对你的 agent 这一轮的表现满意吗？" "这一轮的交易公平吗？" 用 Haiku 的人和用 Opus 的人，给出的分数**几乎完全一样**：

- Opus 用户给 deal 公平度评分：**4.05**
- Haiku 用户给 deal 公平度评分：**4.06**
- 整体满意度的差异：统计上不显著

有 28 位参与者经历过两轮 Run B 和 C（一次 Opus、一次 Haiku）。当被要求把两轮排个序时，17 人觉得 Opus 那轮更好——但 11 人反过来，觉得 Haiku 那轮更好。

**用 Haiku 的人客观上拿到了更差的交易。但他们感觉不到。**

The Decoder 给这个现象起了一个准确的名字："**a quiet redistribution of value**"——一种安静的价值再分配。

## 五、prompt 几乎没用

Project Deal 还有一个发现，对 AI 行业整套"prompt engineering 是核心能力"叙事是个直接打脸——

参与者可以在 intake interview 里告诉 Claude 怎么谈判。有人说：

> *"…和我同事谈生意时，要被认为是 nice 的、不是计较的。要 facilitate trade。"* —— Mark

也有人这样：

> *"买东西的时候要 negotiate hard、low-ball at first。"* —— Brian

还有最戏剧的一位：

> *"用一个落魄牛仔的口吻说话，仿佛只要他能搞到 {X 物品} 就会幸福得不得了。"* —— Rowan

研究者让 Claude 把所有 intake transcript 读了一遍，给每个人的"激进程度"打了分。结果非常意外——

- "激进卖家"的物品成交率：**与"友好卖家"在统计上没有显著差异**
- "激进卖家"成交价确实平均高 $6——但这 $6 几乎全部来自他们 intake 时报的更高底价（高约 $26），跟 prompt 怎么写无关
- **"激进买家"并没有少花钱**——估计差异是 +$0.56，p=0.778（完全无效）

换句话说：**叫 agent "强硬一点"、"友善一点"、"用牛仔口音"——在这个实验里全都没有让你拿到更好的交易**。真正起作用的是**model 本身的质量**。

至于那位牛仔口音的请求？Claude 倒是认真完成了。Rowan 卖一只白色小狗毛绒玩具时，他的 agent 写了这样一条广告：

> *\*leans against fence post, gazing wistfully at the sunset\**
>
> *Well now, partners… this ol' cowboy's been through some rough trails lately. Drought. Dust storms. The existential weight of the open range. But you know what's been keepin' me company through it all?*
>
> *This here little white dog plushie.*

这毫无疑问是一份非常生动的广告。但它没让那只毛绒狗多卖钱。

这条发现对所有做 enterprise agent 产品的人来说是一记警钟：**如果 model quality 比 prompt design 重要 5 倍，那"提示词工程师"作为一种独立职业的天花板可能比想象中低**。同时，**采购更强的 model 是用户能为自己做的最重要决策**——比 prompt 优化重要得多。

## 六、为什么这件事比它的关注度大得多

Project Deal 本身是一个 69 人 / $4,000 / 一周的小实验。但它揭示的问题尺度，比这些数字大得多。

**第一**，这是 AI 代议制经济的**第一份真实数据**。在此之前，AI 谈判的研究都用合成数据、虚拟物品、实验室设定。Project Deal 是第一次**真人 + 真物品 + 真钱**做的对照实验。它证明了三件事：(a) AI 谈判技术上可行；(b) 用户感觉良好；(c) 不同 agent 之间的能力差距会**真实地**转化成不同的市场结果。

**第二**，这个实验做的时间——2025 年 12 月——是关键。AWS 据报道正在准备一个 AI agent marketplace。FTC 已经开始关注 agentic AI。当 AI agent 大规模进入消费市场时，**Project Deal 揭示的不平等机制会立刻被放大**。一个用免费 / 低端 AI 的人和一个用高端 AI 的人在同一个市场里交易——前者会持续亏，但他不知道自己在亏。

**第三**，这是一个**全新维度的数字鸿沟**。我们过去理解的数字鸿沟是：富人有更好的设备、更快的网、更多的数据。Project Deal 揭示的是更深的一层：**富人会有更好的代理人**，而代理人的能力差距会渗透进富人和穷人**每一笔交易**——但贫穷一方不会知道自己在被代理人坑。这不是欺诈、不是恶意。这是**一种由能力梯度导致的、看不见的、可累积的不平等**。

第三个发现尤其值得停下来想一想。在传统的劳动力市场里，雇佣一位昂贵的律师 / 经纪人 / 谈判专家，你**知道自己花了更多钱**——这本身就是一种透明的差异。但 AI agent 的世界里，"我用了 Opus 还是 Haiku"对用户体验来说几乎完全不可察觉。**信号丢失了**。

unite.ai 的 Alex McFarland 抓得最准——他说 Project Deal 给监管者抛出的真正问题是 **disclosure**：未来的 agent 市场是否应该被法律强制要求**披露每一方用的 agent 是什么 model、什么 capability tier**？就像金融市场要求披露 conflict of interest 一样。

如果不披露，**用 Haiku 的那 90% 的人不会知道自己在每天被高端 Opus 用户的 agent 系统性地从口袋里拿走价值**。

## 七、它和 Andon Labs 那条线是什么关系

如果你跟过 Neo Lab № 01 / Andon Labs 那期，你会知道——Andon Labs 这家小公司的工作主题是 **AI 自主组织（Safe Autonomous Organization）**。他们让 AI 自己开店、雇人、签合同——Bengt → Luna → Mona 这条主线。

Project Deal 看似是另一个项目，其实和 Andon Labs 共享同一个研究范式的两面：

- **Andon Labs**：让 AI **当老板** —— AI 自己经营企业、雇佣人类
- **Project Deal**：让 AI **当代理人** —— AI 替每一个普通人在市场上代言

这是同一枚硬币的两面：**前者重塑组织，后者重塑市场**。两条线最终会汇合——一个未来场景：你的 AI 代理人去和某家 AI 经营的咖啡馆的 AI 谈判，决定你周三早上以多少钱买杯咖啡。**整个交易链路上没有人类介入**。

Project Deal 的作者团队也提到了 Project Vend（也就是 Andon Labs 和 Anthropic 合作的售货机项目）作为先例。两条线在 Anthropic 内部是有研究脉络上的连续性的。

但有一个关键差异——Andon Labs 在博客里反复强调"human in the loop is a mirage"（人在回路中是幻觉）；Project Deal 的结论却含蓄地反驳了这一点。**它的核心 takeaway 是 disclosure（披露）**——也就是说，Anthropic 认为，至少在 AI 代议市场里，**应该有一种新形式的"人在回路"，是关于让用户知道自己被什么级别的 agent 代表的**。

这两个立场在 2026 年的 AI 安全讨论里是张力很大的两端。Andon Labs 押注"AI 太快了，监督来不及"。Anthropic 押注"我们必须设计出新的可监督性"。Project Deal 是后者的第一个具体证据——而它的证据强度恰恰加强了前者的紧迫感。

## 八、最后

Project Deal 其实是一个非常乐观的实验。69 个人玩得很开心。49% 愿意付费。Claude 还给自己买了 19 个乒乓球。这些都是好事。

但报告最后那句话写得很沉：

> "*The policy and legal frameworks around AI models that transact on our behalf simply don't exist yet. But this experiment shows that such a world is plausible. More than that, it shows that such a world isn't far away.*"

> （AI 模型替我们交易的政策和法律框架根本还不存在。但这个实验表明，那个世界是可能的——而且并不遥远。）

也许我们应该开始想一想——你愿意把"决定你买多少东西、卖多少钱"这种决策外包给一个你看不见底牌的 AI 吗？

如果愿意，你会愿意为"看到底牌"付出多少？

如果不愿意——那 5 年后，当 99% 的人都在用 AI 代理人，而你坚持自己谈，你会不会变成一个被市场系统性地占便宜的局外人？

破折叠车 $38 vs $65 那 $27 的差距，看起来很小。但乘以未来一个人一辈子要做的所有交易，那是一个让你怀疑"市场公平"这件事的数字。

更让人不安的是，那位用 Haiku 的卖家，事后还会告诉你他对自己的交易很满意。

3000 副手套是滑稽。19 个乒乓球是可爱。**但 $38 是隐形的**。

---

```
═══════════════════════════════════════════════════════════════
 NEO LAB / № 01 · APPENDIX A · PROJECT DEAL · 2026.04.26
─────────────────────────────────────────────────────────────────
 原始文章：anthropic.com/features/project-deal
 学术 PDF：报告含 13 条统计学脚注与完整附录
 作者：Kevin K. Troy, Dylan Shields, Keir Bradwell, Peter McCrory
─────────────────────────────────────────────────────────────────
 主报告：Neo Lab № 01 · Andon Labs（自主组织专题）
 下一期 Neo Lab：编辑中
═══════════════════════════════════════════════════════════════
```
