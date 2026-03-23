# 🖱️ Lenovo Legion M300 RGB — Button Remapper

> 100% vibe coded. No cap.

Tired of the official Lenovo software doing basically nothing? Now you can program **any keyboard key** directly onto your mouse — on any of the 8 buttons. Open the app, pick your keys, hit Apply. Done.

---

## ✨ Features

- 🎹 Any keyboard key on any mouse button
- 🖱️ Mouse button remapping (left, right, middle, forward, backward)
- 🎵 Media keys: volume up/down, mute, play/pause, next/previous track
- ⚡ DPI Switch
- 🚫 Disable any button
- 💾 Config saved on Apply — persists across restarts
- 🚀 No Legion Software, no drivers, no background services

---

## 📥 Download

**[Download MemovoMemion300Binder.exe](../../releases/latest)** — no Python needed, just run it.

---

## 🚀 How to use

1. Plug in your mouse via USB
2. Run `MemovoMemion300Binder.exe`
3. Pick an action for each button from the dropdown
4. For keyboard keys — select "Keyboard Key...", click the field next to it, then press the key you want
5. Hit **APPLY ALL**

---

## 🔧 Compatibility

| Device | Status |
|---|---|
| Lenovo Legion M300 RGB (USB) | ✅ Tested |
| Lenovo Legion M300s | ❓ Untested (likely works) |

**Vendor ID:** `0x17ef` · **Product ID:** `0x60e4`

---

## 🛠️ Building from source

```bash
git clone https://github.com/aLegoz/memovo-memion-300-binder
cd memovo-memion-300-binder
pip install hidapi pynput pyinstaller
pyinstaller --onefile --windowed --name "MemovoMemion300Binder" memovo_binder.py
```

Output: `dist/MemovoMemion300Binder.exe`

---

## 🔬 How it works

The HID protocol was reverse engineered by capturing USB traffic with **Wireshark + USBPcap** while the official Legion Software was running. All commands are sent directly to the mouse as 64-byte HID packets.

Full protocol docs in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## ⚙️ Requirements (running from source)

- Windows 10/11
- Python 3.8+
- `pip install hidapi pynput`

---

## 📄 License

MIT — free to use, modify and distribute.

---

## ⚠️ Disclaimer

This software sends raw HID commands directly to your mouse. Use at your own risk. The author is not responsible for any damage to your device.

---

## 🤖 Vibe coded

Entirely built with AI assistance. Zero manual protocol documentation — HID packets were reverse engineered from Wireshark captures and the rest was vibes.

---

## 🔍 Related searches

Lenovo Legion M300 RGB remap · Lenovo Legion M300 bind keyboard · Legion M300 RGB button binding · Legion M300 RGB keyboard bind · Legion M300 bind key · M300 RGB keybind · Legion M300 RGB alternative software · Legion M300 RGB custom software · Legion mouse HID · Legion Zone alternative · lenovo gaming mouse remap keys
