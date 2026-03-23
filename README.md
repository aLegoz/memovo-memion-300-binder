# Memovo Memion 300 Binder

A replacement for the limited Legion Software — bind any keyboard key, mouse button, media key, or macro to any of the 8 mouse buttons on the Memovo Memion 300 (Lenovo Legion M300 RGB).

## Features
- Bind keyboard keys (held = key stays pressed)
- Mouse button remapping
- Media keys (volume, play/pause, etc.)
- DPI switch
- Macro recorder (keyboard + mouse clicks + scroll)
- Config saved automatically
- Default preset on first launch

## Requirements
- Windows
- Python 3.8+
- `pip install hidapi pynput`

## Usage
```
python memovo_binder.py
```

Or download the `.exe` from [Releases](../../releases).

## Building exe
```
pip install pyinstaller
pyinstaller --onefile --windowed --name "MemovoMemion300Binder" memovo_binder.py
```

## How it works
Reverse engineered HID protocol by capturing USB traffic with Wireshark + USBPcap while Legion Software was running. All commands are sent directly via hidapi.
