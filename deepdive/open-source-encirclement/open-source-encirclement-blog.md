# 这一周，开源 AI 第一次真正赢了

> 一句话版：DeepSeek V4 让开源首次在 Agentic Coding 上超越 GPT-5 和 Claude Opus 4.7，**同一天** Google 砸 400 亿给 Anthropic——这两件事不矛盾，是 AI 产业护城河从"能力"转移到"算力"的同一道分水岭。

```
日期：2026-04-30 · 类型：博客版（传播性）
对应深度报告：开源包围战：能力护城河消失，算力护城河加高
```

---

## 30 秒读完

| # | 这周发生了什么 | 这意味着什么 |
|---|--------------|------------|
| 1 | DeepSeek V4 开源（1.6T/49B），Agentic Coding 首次开源 SOTA，1M Context 默认 | 闭源最值钱的差异化卖点被穿透 |
| 2 | Kimi K2.6 / Qwen3.6 / Gemma 4 同周齐发，"小模型星座"成型 | 不是 DeepSeek 一家，是一场协调好的包围战 |
| 3 | Sam Altman 承认 Pro 订阅亏钱 | 闭源"补贴→锁定→提价"剧本被压缩 |
| 4 | Google 给 Anthropic 投 400 亿，估值 1 万亿超越 OpenAI | 表面是 AI 投资，本质是算力绑定（Anthropic 用 Google TPU） |
| 5 | NVIDIA 重回 5 万亿市值 + Blackwell Ultra 跑 V4 拿 150+ TPS | 谁赢都得买 NVIDIA，闭源开源都是卡奴 |

---

## 这周最好的那个比喻

> "**算力循环回流**"——Google 的 400 亿最终回到 Google Cloud，是隐性的长期采购协议。
>
> Anthropic 表面上在抗 OpenAI，本质上在执行 Google 的经典剧本——**商品化补充产品（杀 SaaS）以保护核心城堡（API + 算力）**。每杀掉一个 SaaS 品类（Figma → Claude Design / Cursor → Claude Code / RPA → Workspace Agents），剩下的预算就流向 Claude API。
>
> ——改写自 Tom Tunguz《Competitive Strategy in the Age of AI》

---

## 三种人的下一步

**模型选型者**：你的产品差异化如果还停留在"我们用了 GPT-5"，能力平价后这个差异化即将清零。要么转向数据飞轮，要么转向工作流深度集成。

**SaaS 创始人**：Tunguz 框架不是预测，是现实描述。如果你的 SaaS 价值是"信息整合"或"流程自动化"——这部分价值正在被三大模型厂直接内化到 API 里。能不能活到明年取决于你能不能把价值从"流程"重定义到"数据"或"信任"。

**企业 IT 决策者**：自部署门槛真的降了——DeepSeek V4 是第一个生产级开源 Agentic Coding。但**开源不是免费**，是成本中心从 API 计费转到 GPU+MLOps 团队。算清楚这笔账再决定，别只看权重。

---

## 一个非共识观察

当前 scaling 的主流不是堆单一超大模型，而是协调大量小模型的星座。

证据：Qwen3.6-35B-A3B（MoE 激活 3B）成为 HuggingFace 下载量第一；Kimi K2.6 支持 300 子 Agent 连续运行 12 小时；Sakana Fugu 直接把 Agent 协调作为模型能力训练。

如果这个观察对，下一代 AI 基础设施的核心指标不是"参数规模"而是"集群协同效率"——评估标准要重写。

---

## 一段话结论

赢家可能既不是开源也不是闭源，而是**底层硬件和云**。开源赢能力但每次推理仍烧 GPU；闭源失去能力差异化但靠算力绑定续命；NVIDIA 双向通吃；云厂商通过投资把 AI 厂商绑死。**能力平价不是结束，是真正商业模式比拼的开始。**

---

*想看完整论证、数据、来源链接？读对应深度报告：《开源包围战：能力护城河消失，算力护城河加高》*
