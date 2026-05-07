# Buddy 协议深潜
## 从 BLE 比特流看 Agent 硬件通信协议的未来

> 一份关于 claude-desktop-buddy 协议的逐层拆解 + 设计分析 + 在 Anthropic 协议栈里的定位 + 对未来 agent-hardware 通信协议的预测。先解构现实，再推演未来。

> 姊妹篇：[№ 01 价值篇 — Buddy 对开发者意味着什么](../[PRD]%20Claude%20Desktop%20Buddy/Claude%20Desktop%20Buddy%20对开发者的价值.html)

---

## 这篇文章想做什么

Buddy 协议表面是一个 maker 玩具的接口规范。往下挖会发现三件值得讨论的事：

1. **它是 Anthropic 的第六份对外协议**——前五份是 MCP、Skills、Hooks、Permissions、Remote Control。每份对应 agent 工作流的一层。
2. **它是其中唯一的物理近场协议**。其他五份都是软件接口或网络协议；Buddy 是这家公司第一次划定 agent 与"实体硬件"之间的合约。
3. **它的设计选择反映了一个尚未公开声明的判断**：agent 的"物理在场感"是一个产品维度，值得用一份独立协议去支持。

文章结构：

- **§ 01–02 — 概述** Buddy 是什么、它能做什么
- **PART I — 协议形态** 从 BLE 物理层到 JSON 应用语义的逐层拆解 + 硬件参考实现
- **PART II — 设计分析** 6 个关键决策、4 处聪明、5 个缺口、威胁模型
- **PART III — 在 Anthropic 协议栈中** 6 份协议横向对比、Buddy 占哪一格
- **PART IV — 未来** 5 个演化方向 + 3 个应该存在的协议提案 + 策略分析

写给：协议设计者、做 agent 工具链的工程师、想做硬件接 AI 的 maker、对 protocol-as-product 感兴趣的产品人。

---

## § 01 / 这是什么

[claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy) 是 Anthropic 开源的一个参考实现，包括两件东西：

- **协议文档**：Claude 桌面版（macOS / Windows）通过蓝牙 LE 对外暴露的 BLE 接口规范
- **示例固件**：运行在 M5StickCPlus（ESP32）上的桌面宠物，可视化 Claude 会话状态并支持物理按键审批

你不需要这个仓库里的<em>任何代码</em>就能接入这个 API——只要一块能广播 Nordic UART Service 的开发板和这份协议文档。仓库的存在是给 Maker 社区一个可以直接 fork 和刷机的起点。

### 仓库考古

仓库元数据有点意思：

- **1.6k Stars / 218 Forks**
- **Contributors 只有一位**：Felix Rieseberg（Electron 核心维护者，前 Slack 桌面客户端主作者）
- **全仓库只有 2 个 commit**

这不是有机生长的开源项目——是某个内部项目**清理后开源**的清白版本。Anthropic 想把这个能力推给 Maker 社区。这个细节会在 § 17 谈策略时再回来。

---

## § 02 / 它能做什么

连接后，硬件实时获取 Claude 的工作状态——会话数、运行/等待数、token 累计、当前权限请求。状态映射到设备上的 7 种动画（详见 [价值篇 № 01 状态表](../[PRD]%20Claude%20Desktop%20Buddy/Claude%20Desktop%20Buddy%20对开发者的价值.html)）。

关键交互是**审批流程**：Claude 执行 Bash 命令、文件操作等需要用户确认的工具调用时，设备屏幕显示 `approve: Bash` 附具体命令预览。**按 A 批准、按 B 拒绝**。整个过程不需要看电脑屏幕。

这解决一个真实痛点：Claude Code 跑长任务时偶尔会停下等审批，你需要切回电脑窗口点击。有了这块设备，你可以继续做别的事，等宠物不耐烦了再瞥一眼按键。

这件小事的产品意义在 № 01 价值篇讲过。这篇文章关心的是：**这件小事用什么协议实现，为什么这么实现**。

---

# PART I — 协议形态

## § 03 / 协议栈结构

Buddy 协议有四层：

```
应用语义层    JSON 消息（heartbeat / permission / turn / status / char_*）
                              ↓ ↑
帧层          UTF-8、\n 分隔的行（line-buffered）
                              ↓ ↑
传输层        Nordic UART Service (NUS) over BLE GATT
                              ↓ ↑
物理层        Bluetooth Low Energy 4.2+ / 5.0
```

每一层都有故事。从下往上看。

## § 04 / 物理 + 传输层

### 4.1 / 为什么是 BLE 而不是 WiFi / USB / UWB

候选方案对比：

| 候选 | 距离 | 配对成本 | 功耗 | 调试性 | 成本 |
|---|---|---|---|---|---|
| **BLE** | 桌面级 (~10m) | 一次配对 | 极低 | 高（嗅探器随处可得） | 几美元 |
| WiFi | 房间级 (~30m) | 路由器密码 | 中 | 中（需在同网络） | 同 |
| USB | 接触 | 即插即用 | 取自总线 | 高 | 同 |
| UWB | 桌面级 | 复杂 | 中 | 低 | 较高 |
| 5G/Cellular | 全球 | SIM | 高 | 低 | 高 |

Buddy 选 BLE 的理由可以反推：

- **桌面级范围正好**——既不限制在物理接触（USB），也不会无意中被楼下办公室嗅到（WiFi/全球网络）
- **配对一次，重连自动**——符合"放工位上不管它"的交互模式
- **极低功耗**——纽扣电池 / USB-C 待机几天没问题
- **现成生态**——任何 ESP32、nRF52、树莓派 + dongle 都能广播；macOS/Windows/Linux 都有原生客户端
- **物理半径即信任半径**——这点很关键，§ 11 再讲

USB 也是合理候选，但要求设备必须线连主机；BLE 让设备可以放在桌上任何位置（甚至显示器后面、抽屉里），这个自由度对 ambient device 很重要。

### 4.2 / Nordic UART Service —— 为什么不发明新 GATT

NUS 是事实标准：

```
Service:  6e400001-b5a3-f393-e0a9-e50e24dcca9e
RX (W):   6e400002-b5a3-f393-e0a9-e50e24dcca9e   主机→设备 Write
TX (N):   6e400003-b5a3-f393-e0a9-e50e24dcca9e   设备→主机 Notify
```

为什么用 NUS 而不是设计一份 Buddy-specific 的 GATT profile？

- **生态一致性**：NUS 在 Nordic SoftDevice、ESP32 NimBLE、Apple CoreBluetooth、Linux BlueZ、Python `bleak` 都是 first-class，第三方实现门槛接近零
- **调试可观测性**：nRF Connect、`bluetoothctl`、`hcitool` 都能直接订阅 NUS 流量。协议设计者**主动让自己的协议变得容易嗅探和复现**——这是开放性信号
- **范式天然匹配**：NUS 本质就是双向"串口"，正好对应 agent ↔ 硬件这种"主机推状态、设备回决策"的对称结构。如果你的协议形态本身就是文本流，没必要发明二进制 GATT
- **姿态信号**：选事实标准而不是发明新的——表明 Anthropic 把这份协议定位成"应用层规范"而非"基础设施"。基础设施留给生态，他们只做应用层

这种选择和 MCP 的 JSON-RPC 2.0 over stdio/SSE 是一致的——都是**复用现有标准当传输底座，把新意全部投入应用语义层**。

### 4.3 / 广播命名前缀：Claude*

设备广播名字必须以 `Claude` 开头。这是个简单的过滤约定，但它代替了几种更复杂的方案：

- ❌ Manufacturer-specific data（要去 Bluetooth SIG 注册 16-bit Company ID）
- ❌ 自定义 Service UUID 用于 advertise（占 advertising payload，128-bit UUID 占 16 字节）
- ✅ **名字前缀**——零注册成本，扫描时一行代码过滤

副作用：任何人都可以广播 `Claude_xxx` 假冒设备。但这在 BLE 范围内本来就要靠加密层防护（§ 11），不是命名约定该解决的。**用对工具**。

### 4.4 / MTU 限制和"协议层不关心 MTU"

BLE 4.0 的 ATT_MTU 默认 23 字节，扣掉头之后 Notify 一次只能发 20 字节负载。BLE 5.0 协商后可以到 247 字节。但你不能假设每个客户端都协商了大 MTU。

Buddy 的处理方式很聪明：**协议层不感知 MTU**。

```
发送方：把 JSON 序列化成 UTF-8，逐字节写入 NUS RX/TX，自然分包
接收方：缓冲所有收到的字节，遇到 \n 就解析一行
```

这意味着：

- 协议在 BLE 4.0（20-byte 包）和 BLE 6.0（如果 MTU 推到 4096）下行为一致
- 任何能模拟 NUS 的传输（USB CDC、TCP socket）都能跑同样的协议
- 调试时用 `cat` 重定向到 NUS 设备文件就能模拟客户端

**抗 MTU 漂移 + 抗传输替换**。下层任何变化都不需要改协议。这是值钱的设计冗余。

## § 05 / 帧层 —— 为什么 \n 分隔的 JSON

候选方案：

| 框架方式 | 优点 | 缺点 |
|---|---|---|
| **\n 分隔行** | 易调试（文本可读）、零开销、telnet 都能验 | 需要保证 payload 不含 \n |
| 长度前缀（4-byte LE + payload） | 严格、二进制安全 | 需要解析器，调试要工具 |
| Length-Type-Value | 多类型分发清晰 | 复杂度高 |
| WebSocket-style frame | 已成熟 | 头部开销 |

Buddy 选 \n。这要求协议层保证 JSON 序列化时不产生原始换行符——即所有 JSON 都是单行的（minified）。这不是 JSON 标准默认行为，但任何序列化库设个 `indent=None` / `pretty=false` 就行。

副作用：
- 调试无敌——`bluetoothctl` 直接读到的就是 JSON 字符串
- 流处理简单——任何语言里 `readline()` 就够用
- 错误恢复天然——一行解析失败不影响下一行

代价：
- 二进制数据必须 base64（见 Folder Push 的 `chunk.d` 字段，每 chunk 多 33% 体积）
- 没有原生的"消息边界即帧边界"保证，必须依赖 \n 约定

总的来说这是个**调试性优先于带宽**的选择。Buddy 的吞吐需求很低（心跳 10s 一次、状态推送几秒一次），调试性的收益远超带宽损失。

## § 06 / 应用语义层 —— 五种消息

Buddy 协议在应用层只有 5 种消息族。一一拆解。

### 6.1 / 心跳快照（设备 ← 桌面）

```json
{
  "total": 3,
  "running": 1,
  "waiting": 1,
  "msg": "approve: Bash",
  "entries": ["10:42 git push", "10:41 yarn test", "10:39 reading file..."],
  "tokens": 184502,
  "tokens_today": 31200,
  "prompt": {
    "id": "req_abc123",
    "tool": "Bash",
    "hint": "rm -rf /tmp/foo"
  }
}
```

字段语义和合约：

- `total`：当前会话总数。`= 0` 表示完全没有活跃 Claude——设备该进 sleep
- `running > 0`：有任意会话在生成——设备该进 busy
- `waiting > 0`：有任意会话被审批阻塞——设备该进 attention
- `msg`：人类可读字符串，可选；用于在小屏幕展示"正在做什么"
- `entries`：最近的活动摘要，已经是格式化好的字符串数组，前 ~3 条
- `tokens` / `tokens_today`：累积 token 使用量
- `prompt` 子对象：**只在需要权限决策时出现**。`id` 是后续回复要用的 nonce，`tool` 是工具名，`hint` 是工具具体参数的简短预览

这个设计有几个值得注意的合约：

**频率合约**：状态变化时发，最长 10 秒一次保活。30 秒收不到当连接断。设备必须做"30s 没数据"超时逻辑，**不能依赖 BLE 链路状态**。

**幂等合约**：每次心跳是完整快照，不是增量。设备可以丢弃任何旧的心跳，只看最新一条。这极大简化了设备状态机——不需要 reconcile，直接覆盖。

**预聚合合约**：`entries` 已经是字符串、不是结构化日志；`tokens` 已经累加；`prompt.hint` 已经截断。**所有聚合在桌面端做**，设备只负责显示。这把复杂度推给主机端（资源充足），设备只做"哑终端"。

这种"主机预聚合 + 设备哑显示"的范式 Buddy 用得很彻底。换成我设计，可能会想"让设备自己计算 stats"——这是错的。设备的 NVS 存储有限、CPU 慢、调试难，**让它做最少的事**才是正解。

### 6.2 / 权限审批（设备 → 桌面）

```json
{"cmd":"permission","id":"req_abc123","decision":"once"}
{"cmd":"permission","id":"req_abc123","decision":"deny"}
```

合约：

- `id` 必须 byte-for-byte 等于上一条心跳里的 `prompt.id`。桌面用这个 id 路由到对应的 session
- `decision` 只有两个值：`once`（批准这一次）或 `deny`
- 没有 `always` / `forever` / `whitelist`——**协议层主动不暴露持久授权**

最后这点是关键。Claude Code 桌面端本身有"始终允许"模式（permissions.json 里的 `allow` 规则）。Buddy 故意不让设备触发这个。为什么？

**物理摩擦是 feature，不是 bug**。如果允许"在 Buddy 上点一次就永久允许 git push"，那设备就从"审批员"退化成"麻木盖章机"。Buddy 的产品定位是给每次审批一个"瞥一眼 + 按一次"的轻摩擦，这个摩擦本身就在阻止一类错误。一旦允许 always，整个产品价值就垮了。

这种"协议刻意不暴露能力"的克制设计很少见。多数协议设计者会想"提供给客户端，让客户端选要不要用"——Buddy 反过来：**禁止客户端拥有这个选择**。这是产品决策固化在协议里的例子。

### 6.3 / Turn 事件（设备 ← 桌面，异步）

```json
{
  "evt": "turn",
  "role": "assistant",
  "content": [{"type": "text", "text": "..."}]
}
```

每个 Claude 回复完成后触发一次。`content` 数组是 SDK 的原生格式（text / tool_use / tool_result 等）。**超过 4 KB 的事件被丢弃**。

为什么 4 KB？我推测是工程约束驱动的：

- BLE Notify 实测吞吐 ~10-20 KB/s（取决于连接参数）
- 4 KB 一帧约 200-400 ms 传输完
- 超过 4 KB 的回复一般是大段代码或长解释——反正小屏幕也展示不下
- 4 KB 也够 ESP32 RAM 缓冲一帧（这块 SoC 默认 RAM 320 KB）

设计意图：**Turn 不是为了让设备完整复制对话，而是为了触发"Claude 说话了"动画**。如果设备想要完整记录，应该用别的传输（USB 直连、WiFi）。Buddy 在 BLE 上的角色是"状态指示器"，不是"日志同步器"。

这条约束防止协议被滥用。如果没有 4 KB cap，会有人尝试通过 Turn 事件在 BLE 上做长文本同步——结果是带宽打满、心跳延迟、用户体验崩。**用约束保护协议的产品定位**。

### 6.4 / 状态上报 ack（桌面 ← 设备）

```json
{
  "ack": "status",
  "ok": true,
  "data": {
    "name": "Clawd",
    "sec": true,
    "bat": {"pct": 87, "mV": 4012, "mA": -120, "usb": true},
    "sys": {"up": 8412, "heap": 84200},
    "stats": {"appr": 42, "deny": 3, "vel": 8, "nap": 12, "lvl": 5}
  }
}
```

桌面 poll、设备答。填充 Hardware Buddy 窗口的统计面板。每个字段都是可选——设备不支持就不填。

这是协议里**最弱合约的部分**。设计意图很明确：让设备自由暴露它的健康指标，但不强制——这样不同硬件平台可以选择性实现。M5StickC Plus 有电池、IMU、屏幕，所以全填；某个 e-ink 显示器可能只有 `name` 和 `sys.up`，那也是合法的。

`stats.lvl` 是设备自己跟踪的"等级"（每 5 万 token 升一级），上报给桌面。这个状态**桌面不维护**——设备的 NVS 是单一真相源。这又是一个克制的设计：**让设备拥有它显示的状态**，桌面只是消费方。

### 6.5 / Folder Push —— 流式角色包传输

这是协议里最复杂的部分。Hardware Buddy 窗口的 drop target 收到一个文件夹后会触发：

```
桌面: {"cmd":"char_begin","name":"bufo","total":184320}
设备: {"ack":"char_begin","ok":true}

桌面: {"cmd":"file","path":"manifest.json","size":412}
设备: {"ack":"file","ok":true}
桌面: {"cmd":"chunk","d":"<base64>"}
设备: {"ack":"chunk","ok":true,"n":4096}
... 重复 chunk 直到 size 字节传完 ...
桌面: {"cmd":"file_end"}
设备: {"ack":"file_end","ok":true,"n":412}

... 重复 file/chunk/file_end 处理每个文件 ...

桌面: {"cmd":"char_end"}
设备: {"ack":"char_end","ok":true}
```

设计要点：

**Chunk 级 ACK 给了天然流控**。桌面不发下一个 chunk 直到拿到上一个的 ack——这等于在应用层实现了 stop-and-wait 协议。BLE 本身有链路层 ACK，但应用层加这一层让协议在更高抽象上能感知"设备 flash 写慢了"——设备只要拖延 ack，桌面自然降速。

**`n` 字段返回累积字节数**。给 progress bar 一个直接的数据源。

**path 校验责任在设备**。protocol 里不规定具体校验逻辑，但文档明确要求接收方拒绝包含 `..` 或绝对路径的路径。这是**防御纵深**：即使桌面端代码被攻破往设备发恶意 path，设备自身仍要拒绝。这是写给"参考实现外的第三方设备"看的——任何接 Buddy 协议的人都必须实现这层校验。

**整包 1.8 MB 上限**来自 ESP32 4 MB Flash 的现实约束。这不是协议层的强约束，是参考实现的提示。

**这个传输协议与内容无关**。GIF、配置、固件镜像都行，只要满足 path 约束 + 大小约束。这意味着 Buddy 协议未来可以在不修改 wire format 的情况下扩展支持新内容类型——OTA 固件更新、设备 wallpaper、自定义 sound pack。**协议 = 抽象**，不是具体功能。

### 6.6 / 角色包 manifest 格式

Folder Push 传输的内容里，`manifest.json` 的 schema：

```json
{
  "name": "bufo",
  "colors": {
    "body": "#6B8E23",
    "bg": "#000000",
    "text": "#FFFFFF",
    "textDim": "#808080",
    "ink": "#000000"
  },
  "states": {
    "sleep": "sleep.gif",
    "idle": ["idle_0.gif", "idle_1.gif", "idle_2.gif"],
    "busy": "busy.gif",
    "attention": "attention.gif",
    "celebrate": "celebrate.gif",
    "dizzy": "dizzy.gif",
    "heart": "heart.gif"
  }
}
```

约束：
- GIF 宽度固定 96px、高度上限 ~140px（M5StickCPlus 屏幕 135×240 竖屏）
- 整包 < 1.8 MB；`gifsicle --lossy=80 -O3 --colors 64` 一般能压缩 40-60%
- `idle` 可以是数组——每次循环结束切换到下一个 GIF（待机轮播）
- 仓库里 `tools/prep_character.py` 批量调整尺寸；`tools/flash_character.py` 跳过 BLE 直接 USB 烧录

这个 manifest 是 Buddy 协议里唯一一处具体内容格式的强约束。其他所有 wire format 都是结构（消息族），manifest 是数据（资产）。把内容格式独立成一份小 schema 的好处：**协议不变，资产可以独立演化**——比如 v2 加 `sound` 字段挂音效文件，老设备读到忽略，新设备启用。

## § 07 / 硬件参考实现

协议规范是抽象的。Anthropic 提供了一份具体硬件参考实现：M5StickC Plus。

### 7.1 / M5StickC Plus 按键映射

| 按键 | 普通状态 | 宠物页 | 审批页 |
|---|---|---|---|
| **A**（正面） | 切换屏幕 | 切换屏幕 | **批准** ✓ |
| **B**（侧面） | 滚动对话 | 翻页 | **拒绝** ✗ |
| **长按 A** | 进入菜单 | 进入菜单 | 进入菜单 |
| **左侧电源**短按 | 关屏 | — | — |
| **左侧电源**长按 6s | 硬关机 | — | — |
| **晃动** | 触发眩晕动画 | — | — |
| **倒扣放置** | 进入休眠（能量回充） | — | — |

屏幕 30 秒无操作自动关闭，**有审批待处理时保持常亮**。

注意"按键含义随状态变化"这一点——同一个按钮在不同 page 下意思完全不同。这是协议设计上**让设备自己决定按键语义**的体现：协议只规定"设备发 once/deny"，不规定"哪个按键发哪个"。设备开发者完全自由。

### 7.2 / 刷机方法

```bash
# 安装 PlatformIO Core，然后：
pio run -t upload

# 从全新设备开始先清除：
pio run -t erase && pio run -t upload
```

> 完整安装演示（约 80 秒）见[价值篇](../[PRD]%20Claude%20Desktop%20Buddy/Claude%20Desktop%20Buddy%20对开发者的价值.md)内嵌视频：PlatformIO 环境搭建 → 固件烧录 → Claude 开发者模式开启 → BLE 配对（`Connected · Encrypted`）→ 实机审批交互特写。

仓库 `platformio.ini` 已经把 board、partitions、文件系统都配好。`uploadfs` target 单独写文件系统（用于角色包热更新）。

### 7.3 / 适配其他硬件

固件核心 `ble_bridge.cpp` 只依赖 Nordic UART Service，**与硬件无关**。M5StickCPlus 特定的代码集中在 `buddy.cpp` 和显示驱动层。

| 需要换 | 不用动 | 备选硬件 |
|---|---|---|
| 显示驱动 | BLE 层 | nRF52 系列 |
| 按键 GPIO 映射 | JSON 协议解析 | ESP32-S3 |
| IMU 接口（可选） | 状态机 | 树莓派 + BLE dongle |
|  |  | PC + USB BLE dongle |

任何能广播 Nordic UART Service 的设备都能接入。**协议的硬件无关性**是设计的核心承诺——这也是为什么 NUS 选择如此重要（§ 4.2）。

---

# PART II — 设计分析

## § 08 / 六个关键决策

把上面拆出来的设计选择整理成一张决策表：

| # | 决策 | 替代方案 | 选这个的理由 | 代价 |
|---|---|---|---|---|
| 1 | NUS over BLE | 自定义 GATT profile | 生态、调试、姿态 | 没有 |
| 2 | JSON over CBOR/MsgPack | 二进制紧凑格式 | 调试、可读、任意语言可解 | 带宽、需 base64 包二进制 |
| 3 | 行分隔（\n） over 长度前缀 | LTV / WebSocket frame | 文本可读、无需解析器 | payload 不能含 \n |
| 4 | 单次决策 over 持久授权 | once / always / whitelist | 保护审批的物理摩擦 | 设备无法做规则 cache |
| 5 | 无版本字段 | header 里塞 `v: 1` | 现在简单 | 未来 schema 演化时痛苦 |
| 6 | 4 KB Turn 上限 | 大帧分片传输 | 防止滥用、保护 BLE 带宽 | 长回复无法完整传输 |

每个决策单独看都合理。串起来读会发现一个模式：**Buddy 的协议设计在"现在简单"和"未来灵活"之间，反复倒向"现在简单"**。这是一个早期阶段产品的合理选择——但它意味着 v2 协议必然要做一次破坏性升级。设计者对此显然心知肚明（仓库只有 2 个 commit、文档明确说"还没有版本协商"）。

## § 09 / 四个值得注意的设计

### 9.1 / 协议层不感知 MTU

通过 \n 分隔 + 字节流写入，把所有 BLE MTU、分包、重组的事推给两端的应用层缓冲。这让协议**在传输层升级时零修改**。

### 9.2 / Path 校验责任放在接收端

不是简单的"客户端 + 服务器都校验"——是明确把校验**责任**写进协议规范。任何接 Buddy 协议的设备都必须实现，否则"协议合规"就不成立。这是防御纵深做成协议合规的例子。

### 9.3 / Chunk-by-Chunk ACK 给了天然流控

应用层 ack/n 既是确认，又是 progress 数据源，又是流控信号。一个字段三种用途。比拆成 ack + progress + flow_control 三个 message 干净得多。

### 9.4 / 主机预聚合 + 设备哑显示

`entries` 是字符串而非结构化对象，`tokens` 是累加值而非事件流。设备拿到的就是"最终展示形态"，零计算开销。这把复杂度严格地分割开——主机管复杂、设备管显示。结果是设备固件可以**很小**（Buddy 固件只有几百 KB），而协议的 evolution 路径主要在主机侧。

## § 10 / 五个明显缺口

公平起见，把缺口也列清楚。

### 10.1 / 没有版本协商

协议没有 `version` / `protocol_v` 字段。schema 加新字段还能容忍（JSON 容忍未知 key），但语义变化（如 `decision: "once"` 改名 `decision: "approve"`）会直接挂掉，且没有告警机制。

修复路径：在 4.6 的 status ack 里加 `proto: "1.0.0"`，桌面据此判断是否需要降级。

### 10.2 / 单决策权限模型缺规则引擎接口

协议层禁止 `always` 是合理设计（§ 6.2），但意味着无法在协议层做"规则引擎"——比如"读操作自动批 / 写操作要人工"。要做这个，必须在桌面客户端外加一个中间代理。

这其实是有意的——Buddy 强调的是"人在回路"。但对于只想做规则引擎、不想做物理设备的人来说，应该有另一份协议（比如本地 HTTP API）来覆盖这个用例。Buddy 自己不应该做这个。

### 10.3 / 无工具调用进度事件

设备只看到"有 N 个 running"，看不到具体某个工具调用执行到哪一步。如果一个 Bash 命令跑了 3 分钟，设备没法显示"已执行 1m20s"。这对长任务的可视化不够。

修复路径：加一个 `evt: "tool_progress"` 事件流，每 5 秒推一次，含 `session_id` / `tool` / `elapsed_ms`。

### 10.4 / 不能区分多会话

一个设备看到的是聚合后的 `total / running / waiting`——知道有 3 个会话、1 个在跑、1 个等审批，但不知道是哪个。如果用户开了 5 个 Claude Code 会话同时跑、3 个同时要审批，Buddy 无法让用户精确点到具体某个。

这对单设备 + 单用户场景没问题，但对"团队场景"（一个 device 给整个 office 看）就完全废了。

修复路径：心跳里加 `sessions: [{id, status, prompt?}, ...]` 数组，设备 UI 能切换查看。

### 10.5 / 单向（设备不能 push 内容回去）

设备只能：① 回审批决策、② 上报状态。它不能：① push 一个 prompt 给 Claude、② 对 Claude 的回复发评论或修改、③ 触发 Claude 进入特定模式。

这是 Buddy 当前的产品定位决定的——它是"指示器+开关"，不是"输入设备"。但这同时也限制了 Buddy 协议的延展性：基于 Buddy 协议你做不出"按 B 让 Claude 总结当前会话"这种交互，因为协议没有 prompt push 通道。

修复路径：加一个 `cmd: "user_input"` 反向消息，桌面收到后注入到当前会话。但这个一旦开了就难关——会有人滥用、会有安全考虑。Anthropic 现在不放是合理的克制。这条会在 § 15.1 展开讨论。

## § 11 / 威胁模型 + LE Secure Connections 的取舍

### 攻击面

Buddy 协议传输：
- 工具调用预览（`prompt.hint`）—— 含路径、命令、URL
- 对话片段（Turn 事件 4KB）
- token 累计、会话计数

**未加密的 BLE 链路**在 ~10m 范围内可被廉价 nRF 嗅探器（< $30）实时记录。文档明确建议实现 LE Secure Connections bonding，但**没有强制**。

### 为什么不强制加密？

我推测三个原因：

1. **Maker 友好**：很多 maker 用的开发板默认不开 BLE 加密（NimBLE / Arduino BLE 库的 default config）。强制加密会大幅提高接入门槛
2. **配对 UX 痛**：BLE bonding 需要用户输入 6 位 passkey 或确认 yes/no——这在没屏幕的设备上很麻烦
3. **威胁模型现实主义**：能物理接近你工位的人，多半已经能看到你的屏幕——加密 BLE 不能阻止 over-the-shoulder

这个取舍可以争论。我的判断：**对个人 dev 桌面 OK，对企业环境完全不 OK**。如果 Anthropic 想推 Buddy 进 SOC2/HIPAA 合规环境，bonding 必须强制。这就需要协议层加 `sec: required` 字段或在握手时拒绝未加密连接。

### 防御层级

如果你要实现 production-grade 的 Buddy 设备，应该：

1. **必须**：实现 path traversal 校验（§ 6.5）
2. **必须**：实现 prompt.id 严格匹配（§ 6.2）——拒绝 echo 旧 id
3. **建议**：LE Secure Connections + DisplayOnly IO + 6-digit passkey
4. **建议**：把 NUS Characteristic 和 TX CCCD 标记 `encrypt-only`
5. **建议**：广播只在用户主动按按钮后开启 60 秒（reduces attack surface）
6. **可选**：在 device 上加 deny 黑名单——某些 tool name（比如 `Bash` 含 `rm -rf /`）即使用户按 A 也拒绝执行

最后一条尤其有意思——**让设备拥有否决权**而不只是批准权。这超出了当前协议的明文规定，但合规：协议允许设备 deny，没规定 deny 的依据必须是用户按键。设备可以基于内置规则自动 deny。

---

# PART III — 在 Anthropic 协议栈里的位置

## § 12 / 六份协议的全图

到 2026 年，Anthropic 已经有六份对外的、面向开发者的协议规范。它们一起构成了围绕 Claude agent 的开放接口表面。

| 协议 | 范围 | 传输 | 序列化 | 主导实现方 | 推出 |
|---|---|---|---|---|---|
| **MCP** (Model Context Protocol) | agent ↔ 外部数据/工具 | stdio · SSE · HTTP | JSON-RPC 2.0 | 第三方工具方 | 2024-11 |
| **Skills** | agent ↔ 用户脚本/playbook | 文件系统约定 | Markdown + YAML frontmatter | 用户/插件作者 | 2025 |
| **Hooks** | agent ↔ 用户钩子 | stdin / HTTP / MCP / Prompt | JSON | 用户 | 2025 |
| **Permissions** | agent ↔ 安全策略 | 配置文件 | JSON DSL | 用户/组织管理员 | 2024–25 |
| **Remote Control** | agent ↔ 远程人类 | HTTPS over Anthropic 云 | （未公开） | Anthropic | 2026-02 |
| **Buddy BLE** | agent ↔ 物理近场硬件 | NUS / BLE | JSON · line-buffered | 任意 maker | 2026 |

每一份协议覆盖 agent 工作流的不同切面：

```
                    ┌─ 工具发现/调用       MCP
                    ├─ 用户编排/playbook   Skills
agent 工作流  ←────── ┼─ 事件/钩子           Hooks
                    ├─ 边界/策略           Permissions
                    ├─ 远程控制           Remote Control
                    └─ 物理近场指示       Buddy BLE  ←─ 这是 Buddy 占的格
```

## § 13 / Buddy 唯一覆盖的层：物理近场

前五份协议都是软件接口或网络协议——你用代码、配置、HTTPS 跟 agent 交互。Buddy 是**第一份明确把"物理近场设备"作为协议合作方**的规范。

为什么这层值得独立协议？

软件接口（MCP、Hooks）可以在 agent 运行时注入工具或钩子，但不能解决"agent 在后台跑你怎么知道"的问题——你得切窗口去看。物理近场设备恰好解决这个问题：

1. **永远在视线内**，不需要打开任何窗口
2. **状态变化吸引余光**，不需要主动关注
3. **物理按键有摩擦感**，按一下硬件 ≠ 点击 OK

Buddy 协议就是为这三件事定的接口规范。它不替代屏幕，只做屏幕做不好的那件事——让 agent 的后台状态可以不打扰地被感知到。

Anthropic 用这份小协议定住了这个接口位置，让 maker 社区填实现。官方固件只是一个参考起点。

## § 14 / 横向对比深度

### vs MCP — 都是 JSON 但目标受众相反

| | MCP | Buddy |
|---|---|---|
| 调用模式 | RPC（请求-响应） | event stream + 单点回应 |
| 谁主动 | agent 主动调工具 | 桌面主动推状态 |
| 实现方 | 工具开发者（数据库、API、SaaS） | 硬件 maker（M5Stick、ESP32） |
| 接入门槛 | 写一个 npm/pip 包 | 烧一段固件 |
| 编程范式 | 服务端 | 嵌入式 |

虽然都用 JSON、都被 Anthropic 设计、甚至传输层都可能是 stdio/socket——**面向的人和场景天差地别**。MCP 是给软件工程师用的，Buddy 是给硬件 hacker 用的。把它们合并成"统一协议"是个错误——协议设计要适配读者，不是追求统一。

### vs Remote Control — 同样的问题，相反的解

Remote Control（2026-02 推出）和 Buddy 都解决"如何不在主机前操作 agent"的问题。但解法相反：

| | Remote Control | Buddy |
|---|---|---|
| 网络拓扑 | 客户端 → Anthropic 云 ← 主机 | 设备 ↔ 主机（直连） |
| 传输 | HTTPS over TLS | BLE NUS |
| 范围 | 全球 | ~10m |
| 认证 | claude.ai 账号 | BLE 配对 |
| 数据流 | 经过云 | 完全本地 |
| 适用场景 | 出差、移动、跨机器 | 桌面、ambient、低延迟 |

这两个协议**互补**，不是竞争。Remote Control 解决"我不在电脑前但需要继续 agent 工作"——拿手机当客户端。Buddy 解决"我在电脑前但不想被弹窗打断"——拿桌上的物件当 ambient 信号。

Anthropic 同时有这两条协议——一条云中转、一条本地直连。不同问题用不同物理拓扑解，两者互补，不竞争。

### vs Computer Use — 方向相反的可见性

Computer Use 让 agent **看到屏幕、操作鼠标**——agent 看见桌面。Buddy 让桌面**看到 agent 的内部状态**——桌面看见 agent。

```
Computer Use:   agent ──观察 / 操作──→ desktop  (agent 是主动方)
Buddy:          desktop ──状态 / 决策──→ agent   (人/物理设备是主动方)
```

两者都是 agent 与物理世界的接口，但方向相反。Computer Use 让 agent 进入人的世界，Buddy 让人通过设备影响 agent。把它们组合起来——agent 看屏幕调试代码、人在 ambient 设备上批准 git push——是 2026 年 agent 工作流的完整形态。

### vs Hooks — 协议形态对比

Hooks 是 in-process 的事件钩子——`PreToolUse` / `PostToolUse` / `PermissionRequest` 等事件在 agent 执行流里同步触发，钩子可以读 stdin、回 JSON 决定。

Buddy 在概念上类似 Hooks 的子集——`PermissionRequest` 钩子的"硬件实现版"。区别：

| | Hooks | Buddy |
|---|---|---|
| 部署 | 用户配置文件 | 物理设备 |
| 延迟 | < 100ms | 100ms-2s（BLE 链路） |
| 信任 | 同主机进程 | BLE 链路（需加密） |
| 写在哪 | shell / Python / HTTP endpoint | C++ 固件 |

理论上你可以把 Buddy 看作"通过 BLE 桥实现的 PermissionRequest hook"。Anthropic 没把它合并进 Hooks 协议是对的——Hooks 是**给开发者写代码 hook**，Buddy 是**给 maker 接硬件**。两类受众的协议形态需要不同。

---

# PART IV — Agent-Hardware 通信协议的未来

到这里我已经把 Buddy 协议拆完了。最后一节做预测：未来 5 年，agent ↔ hardware 通信协议会朝哪几个方向演化？

## § 15 / 五个演化方向

### 15.1 / 双向意图（设备不只接收，还能发起）

当前 Buddy 是"主机推 + 设备回审批"的单向偏向。下一步是**让设备能主动 push 给 agent**——比如：

- 桌上一个语音按钮，按住说话 → 转 prompt → push 到当前 Claude 会话
- 一个温湿度传感器，每小时把环境数据 push 给 agent 当上下文
- 一个 NFC 卡贴在文件夹上，刷一下就让 agent 读取那个文件夹的内容

这需要在协议里加一个 **`cmd: "user_input"` 或 `evt: "device_push"` 通道**。安全模型变得复杂——设备能 push 任意 prompt 等于给了它越权能力。需要加：① push 频率限制、② 内容长度限制、③ 主机端的 user-confirm 弹窗。

### 15.2 / 本地优先 / 无中介

Buddy 已经是本地直连。但 Remote Control 是云中转。未来会有**第三种**：本地多台设备之间组网，不需要任何一台去访问云。

具体形态：
- 一台 Mac + 一个 iPad + 一个桌面 ambient device + 一个手腕震动器，全部 BLE 互联
- agent 状态在四个 surface 上同步显示
- 任何一个 surface 上的决策都会被另外三个看到

技术底座：Matter / Thread / BLE Mesh / UWB。这些标准已经成熟，缺的是**"agent 状态"这个语义层的标准化**——也就是给 agent state 定一份能在 mesh 网络里跑的 schema。

Buddy 协议是这个 schema 的雏形。如果未来某个开放联盟（不一定是 Anthropic）把 Buddy 的心跳/permission/turn 抽象成 mesh-friendly 格式，就有了"分布式 agent ambient"这件事。

### 15.3 / 多设备 fan-out

一个 agent 状态推给多个 ambient peripheral。当前 Buddy 是 1:1 配对。下一步是 1:N：

- 一台 Mac 跑 Claude → 同时驱动桌上的 buddy + 显示器旁的 LED 灯条 + 客厅的 e-ink 仪表盘 + 手腕的震动器
- 不同 surface 显示不同抽象层级（buddy 显示 emoji 状态、LED 灯条只显示 idle/busy/attention 三色、e-ink 显示数字摘要、震动器只在 attention 时响）

这需要协议层加**订阅/过滤机制**——设备告诉主机"我只关心 attention 事件"，主机就只对它推这类事件。当前 Buddy 是"全推"，每个设备自己丢弃不关心的字段。这在 1:1 OK，1:N 时浪费带宽。

### 15.4 / 能力协商

当前 Buddy 没有版本字段、没有 capability negotiation。新设备和老桌面、老设备和新桌面互连时只能"祈祷字段兼容"。

未来必须加**握手阶段**：

```
device → host: {"hello": {"proto": "1.2", "caps": ["nus", "char_push", "voice_in"]}}
host → device: {"hello_ack": {"proto": "1.2", "negotiated": ["nus", "char_push"]}}
```

这是协议老问题，HTTP/SMTP/TLS 都解决过。Buddy 现在简单是因为只有一个参考实现；一旦 maker 社区做出 100 种设备，capability negotiation 就是必需。

### 15.5 / 分级信任传输

不同决策权重应该走不同物理通道：

| 决策类型 | 推荐传输 | 信任根 |
|---|---|---|
| 看状态（只读） | BLE / WiFi / 云 | 任意 |
| 批准只读工具调用 | BLE 配对设备 | 一次配对 |
| 批准写文件 | BLE + 设备 PIN | 配对 + 设备本地认证 |
| 批准 prod 部署 | USB 直连 + 物理按键 + 第二人确认 | 接触 + 多方 |
| 批准转账/删数据 | NFC 刷卡 + 生物识别 | 物理 token + 生物 |

不同操作的 blast radius 不同，认证强度应该成比例。当前 Buddy 协议把所有 permission 当一类，这是早期合理简化——未来必然要拆分。

提示：不需要发明新协议——可以把"高风险操作必须走 USB"作为**约定**写进协议规范，让设备自己判断。比如设备只批准 `tool != "Bash" || hint.matches(/^(ls|cat|grep)/)` 的操作，其他的强制 deny → 让用户走桌面端。

## § 16 / 三个应该存在的协议

这一节是个人意见。基于上面的分析，我觉得有三个 agent-hardware 协议**值得存在但还没人做**。

### 提案 1 / Agent Wake — 给 agent 一个物理唤醒入口

**问题**：现在调起 Claude 必须开电脑、打开窗口、敲字符。如果你只是想说一句"帮我查下今天天气"，全套流程过重。

**协议设计**：一个 BLE 设备广播 `Wake_*` 名字，主机连上后接收 PCM 音频流（`{cmd:"audio", d:"<base64>"}`）。设备有一个按键、一个麦克风、可能一个小屏。按住说话，松开就把整段音频 push 给 agent。

**对比现有方案**：Echo 是云路由——你说"Alexa 怎么样"，全程在 AWS。Wake 协议要求**音频本地处理**，只在 BLE 范围内传输；可以选 push 给本地 Claude 也可以走 Anthropic API，但路径开发者完全控制。

**为什么是 BLE 而不是 USB**：你不会想把麦克风用线插在电脑上。

**实现门槛**：~30 美元（ESP32 + I2S 麦 + 按键 + 3D 打印外壳）。

### 提案 2 / Distributed Approval — 多设备投票

**问题**：高风险操作（删数据库、prod 部署、大额转账）只让一个人在一个设备上批不够。但要求"两个人到一个房间双人确认"又太重。

**协议设计**：一个高风险操作发出后，主机把审批请求广播到一组绑定的设备（teammate 1 的 buddy + teammate 2 的 buddy + ops 的 e-ink 屏）。N 中 M 个设备批准（比如 3 中 2）才执行。每个设备独立运行 Buddy 协议，主机做投票聚合。

**协议增量**：在 prompt 字段加 `quorum: {n: 3, m: 2}`，主机收到任一设备 `decision: "once"` 时计数，达到 `m` 就执行、超时未达就 deny。

**对比现有方案**：现在 Slack 有 OpsGenie 多人审批，但全在云上。Distributed Approval 让审批走物理设备——确认你在场而不只是登录了。

**适用场景**：金融机构、医疗系统、生产部署。Yubikey 的 agent 形态。

### 提案 3 / Agent-to-Agent BLE — 邻近 agent 协作

**问题**：你的 Mac 跑 Claude Code、你同事的 Mac 也跑——两个 agent 之间没有任何协作通道（除了让人在 Slack 转贴）。

**协议设计**：两台 Mac 上的 Claude 互相广播 `ClaudePeer_*`，配对后建立反向 NUS 桥。每个 agent 可以 query 对方的 session list、push prompt 到对方会话、订阅对方的 turn 事件。形成一个**桌面级 agent 局域网**。

**为什么是 BLE 而不是 WiFi/IP**：物理半径就是信任半径。BLE 范围内的是同一个房间的人，这本身就是粗粒度的访问控制。WiFi/IP 可以让任何同 LAN 的攻击者扫描到你的 agent。

**协议增量**：需要 capability negotiation（§ 15.4）—两个 Claude 会版本不同步。需要双向意图（§ 15.1）—peer 能 push prompt。需要分级信任（§ 15.5）—默认只读，写操作需要配对方主动同意。

**适用场景**：pair programming（双方 Claude 共享上下文）、code review（让对方的 agent 检查你的 PR）、家庭多用户共享同一个 agent。

## § 17 / Anthropic 的协议风格

回看那张协议表（§ 12），这六份协议没有一份是完整的产品级 SDK。都是最小化规范：

- **MCP**：核心规范开放，参考实现简陋，社区做了真正的工具
- **Skills**：连个标准目录都没，全靠约定 + frontmatter
- **Hooks**：JSON over stdin/HTTP，最朴素的形态
- **Permissions**：DSL 简单到不能再简单
- **Remote Control**：research preview，没承诺 SLA
- **Buddy BLE**：只有 2 个 commit、1 个 contributor

规律很明显：先定接口、不做工具链、让社区填实现。Buddy 是这个模式的最新一例——接口位置定住了，官方固件只是个参考起点。

对开发者来说，这意味着两件实际的事：

1. **别等 Anthropic 出完整工具链**——他们的协议是接口规范，不是平台，生态建设要自己来
2. **早做早有优势**——每份协议的早期生态都缺好的实现，这个窗口不会一直开着

---

# CODA

把 Buddy 协议当前的边界列清楚：

- ESP32 能批准 Claude 的 git push — **能**
- 能持久授权（always allow）— **不能**，故意的
- 能 push 内容回给 Claude — **不能**，目前
- 要不要加密 — **建议但不强制**
- 能跟另一只 ESP32 直接通话 — **不能**，没这条 wire

这些限制不是疏漏，是设计决策——审批有摩擦、协议足够简单能 fork、设备不能绕过人。

值得读这份协议的原因不是它现在能做什么，是它**定住了一个此前没有协议的位置**：agent 与物理近场硬件之间的接口。这个位置现在是空的，官方实现也只是个起点。

---

*姊妹篇：[价值篇 № 01 — Buddy 对开发者意味着什么](../[PRD]%20Claude%20Desktop%20Buddy/Claude%20Desktop%20Buddy%20对开发者的价值.html)*

*仓库：[github.com/anthropics/claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy)*

*Filed 2026-05-07*

---

*姊妹篇：[价值篇 № 01 — Buddy 对开发者意味着什么](../[PRD]%20Claude%20Desktop%20Buddy/Claude%20Desktop%20Buddy%20对开发者的价值.html)*

*仓库：[github.com/anthropics/claude-desktop-buddy](https://github.com/anthropics/claude-desktop-buddy)*

*Filed 2026-05-07*
