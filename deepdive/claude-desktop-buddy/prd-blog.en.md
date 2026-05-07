# More Than a Desktop Pet: What Claude Desktop Buddy Means for Developers

## The Real Problem It Solves

When Claude Code runs long tasks, the most annoying part isn't the waiting—it's the pop-ups.

Just as you get into the zone, an `approve: Bash` pops up. You switch windows, click a button, switch back to the editor, and the thread in your head is broken. A single time isn't painful, but they add up. The more authority you give the AI agent, the more pop-ups you get; but without that authority, the AI agent can't run.

What Buddy does is simple: it turns "switching back to the Claude window to click a button" into "glancing at the device in your peripheral vision and reaching out to press a button."

It might sound like it saves two seconds, but what it actually saves is the context switch of your attention.

---

## The Device Has 7 States

| State | Trigger | Behavior |
|---|---|---|
| `sleep` | Desktop not connected | Eyes closed, slow breathing |
| `idle` | Connected but idle | Blinking, looking around |
| `busy` | Session running | Sweating, busy working face |
| `attention` | **Approval pop-up pending** | Alert expression + **LED flashing** |
| `celebrate` | Cumulative usage hits 50K tokens | Throwing confetti, jumping |
| `dizzy` | Shaken (IMU triggered) | Spinning eyes |
| `heart` | Approving a request within 5 seconds | Floating hearts |

Button semantics change with the state—the same button means different things on different screens:

| | Normal | Viewing Pet | Viewing Info | During Approval |
|---|---|---|---|---|
| **A** (Front) | Next screen | Next screen | Next screen | **Approve** |
| **B** (Right) | Scroll conversation | Next pet | Page down | **Reject** |
| **Long press A** | Enter menu | Enter menu | Enter menu | Enter menu |
| Left power short press | Screen off | | | |
| Left power long press 6s | Hard power off | | | |
| Shake | Get dizzy | | | |
| Place face down on desk | Sleep to recover energy | | | |

Screen turns off automatically after 30 seconds of inactivity, except when an approval is pending.

---

A typical day of use looks something like this:

- Turn on Claude Desktop in the morning → Device wakes from `sleep` to `idle`, starts blinking and looking around
- Have Code run a refactoring task → Enters `busy`, starts sweating
- Halfway through, it needs approval for a `git push` → Switches to `attention`, LED flashes. Catch it in your peripheral vision, reach out and press A, approved within 5 seconds → `heart` floating hearts
- A long AI agent run burns 50K tokens → `celebrate` throws confetti
- Go out for lunch and place it face down on the desk → Enters `sleep` to recover energy
- Come back and give it a shake → `dizzy` spinning eyes

---

## Where It's Actually Useful

**Approvals don't break your workflow.** You're debugging in one terminal while Claude runs batch tasks in the background. No need to switch windows back and forth; your hands stay on the keyboard, you just glance and press. This is especially great for dual-monitor setups or when Claude is running on a separate machine.

**Token consumption becomes tangible.** Every 50K tokens triggers a confetti celebration. Previously, token counts were buried in a web page and easy to ignore. Now, a physical event happens on your desk, making you actually notice how much you're burning—useful for controlling costs and sensing the density of AI agent calls.

**Face-down and shaking.** Face-down = go to sleep, don't bother me; shake = just playing around. It sounds a bit silly, but the cost of conveying intent with these two gestures is much lower than typing, and they are real physical actions, not software buttons.

---

## How to Modify It

Another noteworthy thing about Buddy is how easy it is to modify.

### Changing Pets

The firmware includes 18 built-in ASCII species. Long press A → Menu → next pet to cycle through them; settings persist after power loss. If you just want a new skin, this is all you need.

### Pushing GIF Character Packs

Don't want ASCII? Create a set of GIFs, drag them to the Hardware Buddy drop target in Claude Desktop, and push them to the device via BLE for real-time switching. The `characters/bufo/` directory in the repo is a complete frog example.

Folder structure:

```
my-character/
  manifest.json     # Meta info + colors + state-to-file mapping
  sleep.gif
  idle_0.gif
  idle_1.gif        # idle can be an array, cycles through
  busy.gif
  attention.gif
  celebrate.gif
  dizzy.gif
  heart.gif
```

Constraints: GIFs must be 96px wide and < 1.8MB. `tools/prep_character.py` helps standardize the scaling, and `gifsicle --lossy=80 -O3 --colors 64` can typically compress them by 40-60%.

To revert to ASCII: Menu on device → delete char.

### Direct USB Flashing (Faster for Iterating on Characters)

When iterating on character packs, if you don't want to go through Bluetooth every time:

```bash
tools/flash_character.py characters/bufo
```

Place the character in `data/` and then run `pio run -t uploadfs` to write directly to the filesystem.

### Modifying the Firmware

The `src/` structure is clean:

- `main.cpp` — Main loop + state machine + UI screen
- `buddies/` — One file per species, 7 animation functions
- `ble_bridge.cpp` — Nordic UART bridge
- `character.cpp` — GIF decoding and rendering
- `data.h` / `xfer.h` — Protocol and file transfer
- `stats.h` — NVS persistence (stats, settings, pet selection)

Adding new states, adding new triggers (like double-clicks), or changing animations—basically just a matter of modifying one file.

---

## The Protocol is Open

Nordic UART over BLE, JSON over line buffer, and the schema is all in the repo's `REFERENCE.md`. The documentation explicitly states: "Building your own device? You don't need any of the code here."

This means:

- **You don't need an M5Stick** to connect—any ESP32, nRF52, or Raspberry Pi + dongle that can run BLE works.
- **You don't have to display a pet**—a mechanical flip clock, an atomized light by the office door, or an old Nokia screen works too.
- **You can use it in reverse**—hook Claude's status up to Home Assistant, and have your living room lights dim when an AI agent is running.

An M5StickC Plus unit costs about $25, the firmware is open-source, and you flash it via PlatformIO. The barrier to entry is essentially zero.

---

## What You Can Do Right Now

The video below demonstrates the complete onboarding process for Step 1 (approx. 80 seconds): PlatformIO environment setup, firmware flashing, enabling developer mode in Claude Desktop, BLE pairing, and a live approval interaction—pressing the front button to approve a Write operation after the device enters the attention state.

<video controls width="720" style="max-width:100%"><source src="tutorial.mp4" type="video/mp4"></video>

Ordered from lowest to highest effort:

1. **Just use it**: Flash the official firmware onto an M5StickC Plus and experience it for a week first.
2. **Change pets**: Long press A → Menu → next pet, and try all 18 ASCII species.
3. **Reskin**: Drag and drop a GIF character pack, or make your own (96px wide, < 1.8MB).
4. **Modify the firmware**: Add a double-click trigger, change animations, or add new states.
5. **Connect other hardware**: Use the open BLE protocol to hook your existing devices up to Claude's status.
6. **Reverse applications**: Connect Claude's status to Home Assistant / Stream Deck / custom keyboard macros.

Even if you never touch hardware, simply studying Buddy as a reference case for "what an AI agent approval UI should look like" is worth the $25 and an afternoon.