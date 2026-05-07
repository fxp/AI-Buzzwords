# X / Twitter Thread — DeepDive 协议深潜

> 文案目标：把 9000 字深潜文章卖给"协议设计 / 嵌入式 / agent 工具链"读者。比 № 01 / № 02 thread 硬核 3 倍。
> 双语：中文版投微博 / 即刻 / 中文圈 X，英文版投 HN / Hacker News / r/embedded / r/anthropic。
> 配图：第 1 条 banner，第 4 条心跳 JSON 截图，第 6 条协议栈表，第 9 条提案卡。

---

# 中文版（18 条）

## 1/18 — 钩子（配 banner 图）

```
我把 Anthropic 的六份对外协议拆了一遍，
发现一件事：

claude-desktop-buddy 不是个玩具
是 Anthropic 在"agent 物理近场"这个无人区
插下的一面旗。

这一面旗值得仔细看 👇

（一篇 9000 字深潜文章的 thread 摘要）
```

## 2/18 — 立场

```
2026 年，Anthropic 已经有 6 份对外开发者协议：

1. MCP（agent ↔ 外部工具）
2. Skills（agent ↔ 用户脚本）
3. Hooks（agent ↔ 用户钩子）
4. Permissions（agent ↔ 安全策略）
5. Remote Control（agent ↔ 远程人类）
6. Buddy BLE（agent ↔ 物理近场）  ← 唯一物理协议

每份协议占一格 surface area。
```

## 3/18 — 协议栈

```
Buddy 协议有 4 层：

应用语义    JSON 消息（heartbeat / permission / turn / status / char_*）
帧层         UTF-8、\n 分隔的行
传输层       Nordic UART Service over BLE GATT
物理层       BLE 4.2+ / 5.0

每一层都有故事。
```

## 4/18 — NUS UUIDs（配代码截图）

```
传输层用 Nordic UART Service：

Service:  6e400001-b5a3-f393-e0a9-e50e24dcca9e
RX:       6e400002-...
TX:       6e400003-...

为什么不发明新 GATT？因为 NUS 在 ESP32/nRF/macOS/Linux 都是 first-class，
nRF Connect 直接嗅探。

姿态信号：选事实标准而不是发明 = "应用层规范"，
基础设施留给生态。
```

## 5/18 — 一个聪明设计

```
帧层用 \n 分隔的 JSON。代价是 payload 不能含 \n、二进制要 base64。
收益是：

- bluetoothctl 直接读到 JSON
- 任何语言 readline() 就够用
- 一行解析失败不影响下一行
- 协议层【不感知 MTU】——下层 BLE 4 还是 BLE 6 协议都不变

调试性优先于带宽。值钱的设计冗余。
```

## 6/18 — 完整时序（配时序图）

```
一次典型审批流的完整消息序列：

BLE pair ──────────────────────→
         ←── Connected · Encrypted
heartbeat (idle)  t=0s ────────→ 👀
heartbeat (busy)  t+10s ───────→ 💦
heartbeat (attention+prompt) ──→ ❗ LED 闪
         ←── {decision:"once"}
heartbeat (heart) <5s later ───→ 💖
heartbeat (busy)  t+10s ───────→ 💦
─ ─ ─ ─ ─ 30s 无心跳 ─ ─ ─ ─ → 😴

[配时序图 FIG/SEQ]
```

## 7/18 — 心跳合约

```
心跳每 10s 一次，30s 没收到当断线。三个合约：

频率：必须做"30s 没数据"超时，不依赖 BLE 链路状态
幂等：完整快照不是增量——设备覆盖即可，不用 reconcile
预聚合：entries 是字符串、tokens 是累加值——
       设备拿到的是【最终展示形态】，零计算

主机预聚合 + 设备哑显示。
让设备做最少的事才是正解。
```

## 8/18 — 协议刻意不暴露能力

```
权限审批只有两种 decision：
- once（批准这一次）
- deny

没有 always / forever / whitelist。

为什么？协议层主动不暴露持久授权，
是【为了保护审批的物理摩擦】——
一旦允许 always，设备就从"审批员"退化成"麻木盖章机"。

把产品决策固化在协议里。少见但聪明。
```

## 9/18 — 5 个明显缺口

```
公平起见列出来：

❌ 无版本协商——schema 改名会静默挂掉
❌ 无规则引擎接口——无法做"读自动批/写要人工"
❌ 无工具调用 progress 事件——长任务看不到细节
❌ 不能区分多会话——团队场景废
❌ 单向——设备不能 push prompt 给 agent

每个都有合理修复路径。
```

## 10/18 — 在 Anthropic 协议栈里的位置

```
横向对比：

vs MCP        都是 JSON，但 RPC vs event stream，软件 vs 硬件
vs Remote Control  云中转 vs 本地直连——两条相反方向，互补
vs Computer Use     方向相反：agent 看屏幕 vs 桌面看 agent
vs Hooks           in-process vs over-BLE，开发者 vs maker

Anthropic 同时投相反方向的协议，
是有意的覆盖：不同问题用不同物理拓扑解。
```

## 11/18 — Buddy 占的 niche

```
前 5 份协议都是软件接口或网络协议。

Buddy 是这家公司第一份【物理近场协议】。

为什么这层值得独立协议？
软件接口能注入工具和钩子，
但没法解决"agent 在后台跑你怎么知道"。

物理近场有三个软件没有的属性：
余光可见、无需锁定焦点、物理摩擦不可绕过。
```

## 12/18 — 5 个未来方向

```
agent ↔ hardware 协议会朝这 5 个方向走：

1. 双向意图（设备能 push prompt）
2. 本地优先 / 无中介（BLE Mesh / Matter）
3. 多设备 fan-out（1:N 订阅过滤）
4. 能力协商（设备 caps 握手）
5. 分级信任传输（不同操作走不同物理通道）

每个都是 v2 协议必须解的问题。
```

## 13/18 — 提案 1（配卡片图）

```
我提 3 个【应该存在但还没人做】的协议。

提案 1：Agent Wake
  一个 BLE 设备 + 麦克风 + 按键
  按住说话 → push 音频给 agent
  Echo 的 agent 形态，但音频本地处理
  ESP32 ~$30 实现门槛
```

## 14/18 — 提案 2

```
提案 2：Distributed Approval
  高风险操作（删数据库、prod 部署）
  广播到 N 个绑定设备，M/N 投票才执行
  在 prompt 加 quorum:{n:3, m:2}
  Yubikey 的 agent 形态
  适用：金融、医疗、生产部署
```

## 15/18 — 提案 3

```
提案 3：Agent-to-Agent BLE
  两台 Mac 上的 Claude 互相广播 ClaudePeer_*
  配对后建立反向 NUS 桥
  query 对方 session、push prompt 到对方会话

  为什么 BLE 不 WiFi/IP？
  物理半径就是信任半径。
  pair programming / code review / 家庭多用户共享
```

## 16/18 — Anthropic 的协议风格

```
回看那六份协议——
没有一份是"产品级 SDK"，都是 5-15% 完成度的草图：

MCP 实现简陋
Skills 没标准目录
Hooks 是最朴素的 stdin/HTTP
Permissions DSL 简单到不能再简单
Remote Control "research preview"
Buddy BLE 只有 2 个 commit

规律很明显：先定接口、不做工具链、让社区填实现。
```

## 17/18 — 给开发者的启示

```
对开发者意味着两件事：

1. 每份协议早期生态都缺优秀实现——
   这个缺口现在还在

2. 别期待 Anthropic 帮你做完工具链——
   协议是合约，不是 platform
```

## 18/18 — 链接 + CODA

```
完整 9000 字深潜在这里 👇
[文章链接]

涵盖：
✓ BLE 物理层到 JSON 应用语义逐层拆解
✓ 6 个关键决策 / 4 处聪明 / 5 个缺口
✓ Anthropic 6 份协议横向对比
✓ 5 个演化方向 + 3 个应该存在的协议提案
✓ broad-and-shallow 策略论

CODA：这些都是真正早期的协议。
读它的理由不是里面写了什么，
而是这个位置现在是空的。
```

---

# 英文版（投 HN / r/embedded / r/anthropic / X 国际线）

## 1/12 — Hook

```
I disassembled all six of Anthropic's developer-facing protocols.

Found something:
claude-desktop-buddy isn't a toy.
It's Anthropic planting a flag in
"ambient agent UX over physical proximity"—
a surface no one else has claimed.

Worth a careful look 👇

(thread summary of a 9k-word deep dive)
```

## 2/12 — The Stack

```
By 2026, Anthropic ships 6 open developer protocols:

1. MCP — agent ↔ external tools
2. Skills — agent ↔ user playbooks
3. Hooks — agent ↔ user code
4. Permissions — agent ↔ policy
5. Remote Control — agent ↔ remote human
6. Buddy BLE — agent ↔ physical-proximity hw

Buddy is the first physical-proximity protocol.
```

## 3/12 — Protocol layers

```
4 layers, bottom-up:

physical    BLE 4.2+ / 5.0
transport   Nordic UART Service (NUS) over GATT
framing     UTF-8, \n-delimited lines
semantics   JSON messages (heartbeat, permission, turn, ...)

Picking NUS over a custom GATT profile = "we want this debuggable
with nRF Connect from day one." Stance signal.
```

## 4/12 — A smart trick

```
Framing is line-delimited JSON. Cost: payload can't contain \n,
binary must be base64. Wins:

- bluetoothctl reads JSON directly
- readline() in any language
- one bad line doesn't poison the next
- protocol DOES NOT KNOW about MTU—works on BLE 4 (20-byte) AND BLE 6 (4096-byte)

Debuggability over bandwidth. Cheap insurance against transport
upgrade churn.
```

## 5/12 — The clever omission

```
Permission decisions: only "once" or "deny".

No "always", no whitelist, no rule engine hook.

Why? Because Buddy's product value IS the physical friction
of glancing + pressing a button. Allow "always" and the
device degrades from approver to rubber stamp.

The protocol enforces a product invariant. Rare. Smart.
```

## 6/12 — Heartbeat semantics

```
Three contracts in heartbeat design:

- frequency: 10s heartbeat, 30s = disconnected (don't trust BLE link state)
- idempotent: full snapshot not delta (device can drop old, no reconcile)
- pre-aggregated: entries are strings, tokens cumulative
  (device displays, host computes)

Result: device firmware stays tiny. Evolution path lives on host side.
```

## 7/12 — Five real gaps

```
Where it falls short:

❌ no protocol versioning—schema rename will silently break
❌ no rule engine surface—can't auto-approve reads
❌ no per-tool progress events—3-min Bash invisible
❌ can't distinguish sessions—team scenarios broken
❌ unidirectional—device can't push prompts to agent

Each fixable in a v2.
```

## 8/12 — In context

```
Buddy vs sibling protocols:

vs MCP            both JSON, but RPC vs event stream;
                  software-engineer vs hardware-hacker audience
vs Remote Control cloud relay vs local direct (opposite topologies, complementary)
vs Computer Use   reverse direction: agent sees screen vs desktop sees agent
vs Hooks          in-process vs over-BLE; developer vs maker

Anthropic shipped opposing topologies on purpose.
```

## 9/12 — The niche claim

```
First 5 protocols are software/network.
Buddy is the FIRST physical-proximity protocol from Anthropic.

Why does this layer deserve its own protocol?
Software interfaces can inject tools and hooks,
but can't solve "how do you know your agent is running."

Physical proximity has three properties software doesn't:
peripheral-vision visible, no focus lock required,
physical friction that can't be bypassed in code.
```

## 10/12 — Five evolution directions

```
agent ↔ hardware protocols will evolve along:

1. Bidirectional intent (devices push prompts)
2. Local-first / unmediated (BLE Mesh / Matter)
3. Multi-device fan-out (subscription/filter)
4. Capability negotiation (versioning + caps)
5. Tiered-trust transports (different ops, different physical channels)
```

## 11/12 — Three protocols that should exist

```
1. Agent Wake — voice/gesture button → push prompt
   ESP32 + I2S mic + button. ~$30 BOM.
   Echo's agent-native shape, audio local-processed.

2. Distributed Approval — N-of-M devices vote on high-stakes ops
   add quorum:{n:3,m:2} to prompt. Yubikey's agent shape.

3. Agent-to-Agent BLE — two nearby Claudes federate
   ClaudePeer_*, query/push across desktop. BLE = trust radius.
```

## 12/12 — Protocol style + Link

```
None of the 6 protocols are production SDKs—each is a 5-15% sketch.
Pattern: define the interface, skip the toolchain,
let the community fill implementations.

Two things this means for builders:
- every protocol's early ecosystem is missing good implementations right now
- don't expect a polished SDK; the protocol is the contract, not the platform

Full 9k-word breakdown 👇
[link]

Sister piece: Buddy product perspective (also linked).
github.com/anthropics/claude-desktop-buddy
```
