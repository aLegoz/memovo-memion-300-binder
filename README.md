# Lenovo Legion M300 RGB — Button Remapper & Binder

> 100% vibe coded. No cap.

> Tired of the limited official Legion Software? This tool lets you bind **any key, mouse button, or media key** to any of the 8 buttons on the **Lenovo Legion M300 RGB Gaming Mouse** — no Legion Zone required.

---

## Why this exists

The official Lenovo Legion Software only allows basic remapping for the M300 RGB. This app communicates directly with the mouse over HID, giving you full control over all 8 buttons.

---

## Features

- Remap all 8 mouse buttons freely
- Bind keyboard keys (key is held as long as the button is pressed)
- Mouse button remapping (left, right, middle, forward, backward)
- Media keys: volume up/down, mute, play/pause, next/previous track
- DPI switch binding
- Disable any button
- Config saved on Apply — persists across restarts
- Default preset applied on first launch
- No Legion Software, no drivers, no background services

---

## Download

**[Download MemovoMemion300Binder.exe](../../releases/latest)** — no Python required, just run it.

---

## Usage

1. Plug in your Lenovo Legion M300 RGB via USB
2. Run `MemovoMemion300Binder.exe`
3. Select an action for each button from the dropdown
4. For keyboard keys — choose "Keyboard Key..." and click the parameter field, then press the desired key
5. Click **APPLY ALL**

---

## Compatibility

| Device | Status |
|---|---|
| Lenovo Legion M300 RGB (USB) | ✅ Tested |
| Lenovo Legion M300s | ❓ Untested (same VID/PID likely) |

**Vendor ID:** `0x17ef` · **Product ID:** `0x60e4`

---

## Building from source

```bash
git clone https://github.com/aLegoz/memovo-memion-300-binder
cd memovo-memion-300-binder
pip install hidapi pynput pyinstaller
pyinstaller --onefile --windowed --name "MemovoMemion300Binder" memovo_binder.py
```

Output: `dist/MemovoMemion300Binder.exe`

---

## How it works

The HID protocol was reverse engineered by capturing USB traffic with **Wireshark + USBPcap** while the official Legion Software was running. All button binds are sent as 64-byte HID packets directly to the mouse's vendor-specific interface (`usage_page = 0xFF01`).

See [ARCHITECTURE.md](ARCHITECTURE.md) for full protocol documentation.

---

## Requirements (running from source)

- Windows 10/11
- Python 3.8+
- `pip install hidapi pynput`

---

## Disclaimer

This software sends raw HID commands directly to your mouse. Use at your own risk. The author is not responsible for any damage to your device.

---

## Vibe coded

This project was entirely vibe coded with AI assistance. Zero manual protocol documentation — HID packets were reverse engineered from Wireshark captures and the rest was vibes.

---

## Related searches

Lenovo Legion M300 RGB remap · Legion M300 RGB button binding · Legion M300 RGB alternative software · Legion mouse HID · M300 RGB keybind · Legion Zone alternative
