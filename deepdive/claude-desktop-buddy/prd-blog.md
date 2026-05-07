# 不止是桌面宠物：Claude Desktop Buddy 对开发者意味着什么

## 它解决的真问题

Claude Code 跑长任务时，最烦的不是等——是弹窗。

你刚进状态，`approve: Bash` 跳出来，切窗口、点按钮、切回编辑器，刚才脑子里那条线断了。单次不痛，叠起来很痛。越敢放权给 agent，弹窗越多；不放权 agent 又跑不动。

Buddy 做的事很简单：把「切回 Claude 窗口点按钮」变成「余光看设备、伸手按一下」。

听起来省了两秒，实际省的是注意力上下文的切换。

---

## 设备有 7 种状态

| 状态 | 触发条件 | 表现 |
|---|---|---|
| `sleep` | 桌面端没连上 | 闭眼，慢呼吸 |
| `idle` | 连上了但没事干 | 眨眼，东张西望 |
| `busy` | session 在跑 | 出汗、忙工作脸 |
| `attention` | **有审批弹窗** | 警觉表情 + **LED 闪** |
| `celebrate` | 累计用满 50K tokens | 撒彩花、跳跃 |
| `dizzy` | 晃了它（IMU 触发） | 转圈眼 |
| `heart` | 5 秒内秒批一个审批 | 飘心 |

按键语义随状态变——同一个按钮在不同页面意思不一样：

| | 平时 | 看宠物 | 看信息 | 有审批时 |
|---|---|---|---|---|
| **A**（正面） | 切下一屏 | 切下一屏 | 切下一屏 | **批准** |
| **B**（右侧） | 滚动对话 | 切下一只宠物 | 翻页 | **拒绝** |
| **长按 A** | 进菜单 | 进菜单 | 进菜单 | 进菜单 |
| 左侧电源短按 | 关屏 | | | |
| 左侧电源长按 6s | 硬关机 | | | |
| 晃一下 | 转晕 | | | |
| 倒扣放桌上 | 睡觉回血 | | | |

30 秒无操作自动息屏，有审批时除外。

---

实际用一天大概是这样：

- 早上开 Claude 桌面端 → 设备从 `sleep` 睁眼进 `idle`，开始眨眼东张西望
- 让 Code 跑重构 → 进 `busy`，开始出汗
- 跑到一半要 `git push` 需要审批 → 切 `attention`，LED 闪。余光扫到，伸手按 A，5 秒内批完 → `heart` 飘心
- 中间跑了个长 agent 烧了 50K tokens → `celebrate` 撒彩花
- 出门吃饭把它倒扣桌上 → 进 `sleep` 回能量
- 回来摇一下 → `dizzy` 转圈眼

---

## 实际有用的地方

**审批不破坏工作流。** 你在另一个终端调试，Claude 在后台跑批量任务。不用来回切窗口，手不离键盘，余光扫一眼，按一下。特别适合双屏或者 Claude 跑在另一台机器上的场景。

**token 消耗变得可感知。** 每 50K tokens 升一级放彩花。原来 token 数字埋在网页里，没什么感知。现在桌上会发生一个物理事件，你会实际注意到自己烧了多少——对控制成本和感知 agent 调用密度都有用。

**倒扣和摇晃。** 倒扣 = 去睡别烦我，摇 = 闲着玩。听起来有点蠢，但这两个手势传达意图的成本比打字低很多，而且是真实的物理操作，不是软件按钮。

---

## 怎么改

Buddy 另一个值得一提的地方是很好改。

### 换宠物

固件内置 18 个 ASCII 物种，长按 A → 菜单 → next pet 循环切换，掉电不丢。如果只是想换个皮，这一步就够了。

### 推 GIF 角色包

不想要 ASCII？做一套 GIF 拖到 Claude Desktop 的 Hardware Buddy 窗口 drop target，走 BLE 推到设备实时切换。仓库里 `characters/bufo/` 是完整的青蛙例子。

文件夹结构：

```
my-character/
  manifest.json     # 元信息 + 颜色 + 状态到文件的映射
  sleep.gif
  idle_0.gif
  idle_1.gif        # idle 可以是数组，循环轮播
  busy.gif
  attention.gif
  celebrate.gif
  dizzy.gif
  heart.gif
```

约束：GIF 96px 宽，< 1.8MB。`tools/prep_character.py` 帮你统一缩放，`gifsicle --lossy=80 -O3 --colors 64` 一般能压掉 40-60%。

想还原 ASCII：设备上菜单 → delete char。

### USB 直刷（迭代角色时更快）

迭代角色包时不想每次走蓝牙：

```bash
tools/flash_character.py characters/bufo
```

把角色放到 `data/` 然后 `pio run -t uploadfs` 直接写文件系统。

### 改固件

`src/` 结构清晰：

- `main.cpp` — 主循环 + 状态机 + UI 屏幕
- `buddies/` — 一个文件一个物种，7 个动画函数
- `ble_bridge.cpp` — Nordic UART 桥
- `character.cpp` — GIF 解码渲染
- `data.h` / `xfer.h` — 协议和文件传输
- `stats.h` — NVS 持久化（统计、设置、宠物选择）

加新状态、加新触发（比如双击）、改动画——基本上改一个文件的事。

---

## 协议是开放的

Nordic UART over BLE，JSON over line buffer，schema 都在仓库 `REFERENCE.md`。文档明确写了："Building your own device? You don't need any of the code here."

这意味着：

- **不用 M5Stick** 也能接——任何能跑 BLE 的 ESP32、nRF52、树莓派 + dongle
- **不显示宠物** 也行——机械翻页时钟、办公室门口的雾化灯、旧诺基亚屏
- **反向用** 也可以——把 Claude 状态接 Home Assistant，agent 跑起来时家里灯调暗

M5StickC Plus 整机约 25 美元，固件开源，PlatformIO 刷机。门槛基本是零。

---

## 你现在就能做什么

以下视频演示了步骤 1 的完整上手流程（约 80 秒）：PlatformIO 环境搭建、固件烧录、Claude 桌面端开启开发者模式、BLE 配对，以及实机上的审批交互——设备进入 attention 状态后，手按正面键完成 Write 操作审批。

<video controls width="720" style="max-width:100%"><source src="tutorial.mp4" type="video/mp4"></video>

按投入从低到高：

1. **拿来用**：M5StickC Plus 烧官方固件，先体验一周再说。
2. **换宠物**：长按 A → 菜单 → next pet，18 种 ASCII 物种都试一遍。
3. **换皮**：拖 GIF 角色包过去，或自己做一个（96px 宽，< 1.8MB）。
4. **改固件**：加个双击触发、改动画、加新状态。
5. **接其他硬件**：基于公开 BLE 协议，让你现有的设备接 Claude 状态。
6. **反向应用**：Claude 状态接 Home Assistant / Stream Deck / 自定义键盘宏。

哪怕完全不碰硬件，单纯把 Buddy 当「agent 审批 UI 该长什么样」的一个参考案例研究一下，也值这 25 美元和一个下午。
