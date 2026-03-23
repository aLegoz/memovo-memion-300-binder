# Memovo Memion 300 Binder — Project Architecture

## Overview
A Windows desktop GUI application that replaces the official Lenovo Legion Software for the Legion M300 RGB Gaming Mouse. It communicates directly with the mouse via HID protocol, bypassing the limited official app.

---

## Tech Stack
- **Language**: Python 3.8+
- **GUI**: tkinter + ttk (standard library, no extra UI deps)
- **HID communication**: `hidapi` (pip)
- **Macro recording**: `pynput` (pip) — keyboard and mouse listener
- **Config**: JSON file (`memovo_config.json`) saved next to the executable
- **Distribution**: Single `.exe` via PyInstaller (`--onefile --windowed`)

---

## Project Structure
```
memovo-memion-300-binder/
├── memovo_binder.py       # Single-file app — all logic and UI
├── requirements.txt       # hidapi, pynput
├── README.md
├── .gitignore
└── memovo_config.json     # Auto-generated on first run (gitignored)
```

---

## Hardware Target
- **Device**: Lenovo Legion M300 RGB Gaming Mouse
- **Vendor ID**: `0x17ef` (Lenovo)
- **Product ID**: `0x60e4`
- **HID Interface**: `usage_page = 0xFF01` (vendor-specific)
- **Endpoint**: `0x04`, URB_INTERRUPT out

---

## HID Protocol (Reverse Engineered)

All commands are 64-byte HID packets sent to the vendor-specific interface.
Always prepend `0x00` (report ID) when writing via hidapi.

### Button Bind Command
```
02 00 [btn] [action_code] [key_code] 00 ... [checksum]
```
- `btn` — mouse button number (see table below)
- `action_code` — type of action (see table below)  
- `key_code` — HID keycode (only for keyboard binds, `0xfe` action)
- `checksum` = `(action_code + key_code + btn + 0x02) & 0xFF`

### Commit Command
Must be sent after all bind commands to apply changes:
```
05 00 00 00 ... (64 bytes)
```

### Mouse Button Numbers
```
0x00 = Button 1 (Left)
0x01 = Button 2 (Right)
0x02 = Button 3 (Middle)
0x09 = Button 4 (DPI)
0x05 = Button 5
0x06 = Button 6
0x07 = Button 7
0x08 = Button 8
```

### Action Codes
```
# Mouse
0xb0 = Left Click
0xb1 = Right Click
0xb2 = Middle Click
0xb3 = Forward
0xb4 = Backward
0xc1 = DPI Switch

# Media
0x90 = Volume Up
0x91 = Volume Down
0x92 = Mute
0x93 = Play/Pause
0x95 = Previous Track
0x96 = Next Track

# Other
0x01 = Disable
0xfe = Keyboard Key (next byte = HID keycode)
```

### Keyboard Key Bind (hold behavior)
When action_code = `0xfe`, the mouse holds the key as long as the button is pressed — identical to a real keyboard key. Checksum formula: `(0xfe + keycode + btn + 0x02) & 0xFF`

---

## Application Architecture (`memovo_binder.py`)

### Constants
- `VENDOR_ID`, `PRODUCT_ID` — mouse identification
- `CONFIG_FILE` — path to config JSON (next to exe)
- `MOUSE_BUTTONS` — list of `(btn_code, display_name)` tuples
- `ACTIONS` — list of `(display_name, type, code)` — used to populate dropdowns
- `TK_TO_HID` — maps tkinter keysym strings to HID keycodes (for key capture)
- `PYNPUT_TO_HID` — maps pynput Key objects to HID keycodes (for macro recording)
- `HID_TO_NAME` — reverse map HID keycode → human readable name

### HID Layer (module-level functions)
```
get_hid_path()         → find mouse HID path by vendor/product/usage_page
send_packet(pkt)       → write 64-byte packet to mouse
commit()               → send 05 00... commit packet
send_bind(btn, type, code, keycode) → send single button bind
send_macro(btn, slot, events)       → send macro (CURRENTLY HIDDEN/DISABLED)
```

### MacroEditor (tk.Toplevel) — CURRENTLY HIDDEN
Modal window for recording and editing macros. Uses `pynput` listeners to capture keyboard/mouse events in real time. Events stored as `[type, code, delay_ms]`.
> **Note**: Macro functionality is implemented but hidden from UI pending stability fixes. The `send_macro()` function works but has known issues with slot conflicts causing unintended repeat behavior. Do not expose in UI until fixed.

### App (tk.Tk) — Main Window
Main application class. Builds UI, manages state, handles config.

**State per button** (`btn_state[btn_code]`):
```python
{
    "var": tk.StringVar,      # selected action name
    "key_code": int | None,   # HID keycode for keyboard binds
    "key_name": str | None,   # display name for keyboard binds
    "macro_name": str | None, # macro name for macro binds (hidden)
    "param_lbl": tk.Label,    # the clickable parameter label widget
}
```

**Key methods**:
```
_build()              → construct all UI widgets
_current_action()     → get (name, type, code) for a button's current selection
_on_action_change()   → callback when dropdown changes
_update_param_label() → refresh the parameter label (key name / macro name / empty)
_param_click()        → handle click on param label (start key listen or open macro picker)
_start_listen()       → bind <KeyPress> to capture next key for a button
_stop_listen()        → unbind <KeyPress>
_on_key()             → handle captured keypress, store HID code
_apply_all()          → send all binds to mouse + commit + save config
_reset_defaults()     → restore factory button layout
_refresh_status()     → poll mouse connection every 3s
_save_config()        → write state to memovo_config.json
_load_config()        → read state from memovo_config.json
_restore_ui()         → apply loaded config to UI widgets
```

### style_widgets()
Applies dark theme to ttk.Combobox and ttk.Treeview widgets.

---

## Config Format (`memovo_config.json`)
```json
{
  "macros": {},
  "buttons": {
    "0": { "action": "Left Click", "key_code": null, "key_name": null, "macro_name": null },
    "1": { "action": "Right Click", "key_code": null, "key_name": null, "macro_name": null },
    "2": { "action": "Middle Click", "key_code": null, "key_name": null, "macro_name": null },
    "9": { "action": "DPI Switch", "key_code": null, "key_name": null, "macro_name": null },
    "5": { "action": "Forward", "key_code": null, "key_name": null, "macro_name": null },
    "6": { "action": "Backward", "key_code": null, "key_name": null, "macro_name": null },
    "7": { "action": "Disable", "key_code": null, "key_name": null, "macro_name": null },
    "8": { "action": "Disable", "key_code": null, "key_name": null, "macro_name": null }
  }
}
```

---

## Default Preset (first launch)
```
Button 1 → Left Click
Button 2 → Right Click
Button 3 → Middle Click
Button 4 → DPI Switch
Button 5 → Forward
Button 6 → Backward
Button 7 → Disable
Button 8 → Disable
```

---

## UI Layout
```
┌─────────────────────────────────────────────┐
│ MEMOVO MEMION 300 BINDER        ● connected │
├─────────────────────────────────────────────┤
│ Button          Action      Parameter       │
├─────────────────────────────────────────────┤
│ Button 1 (Left) [Left Click ▼] [          ] │
│ Button 2 (Right)[Right Click▼] [          ] │
│ ...                                         │
│ Button 8        [Disable    ▼] [          ] │
├─────────────────────────────────────────────┤
│ Configure buttons...  [Reset to Default]    │
│                              [APPLY ALL]    │
└─────────────────────────────────────────────┘
```

When "Keyboard Key..." is selected, the Parameter label shows `[ press a key ]`. Clicking it activates key capture mode — next keypress is stored as the bind target.

---

## Building & Distribution
```bash
pip install hidapi pynput pyinstaller
pyinstaller --onefile --windowed --name "MemovoMemion300Binder" memovo_binder.py
# Output: dist/MemovoMemion300Binder.exe
```

The `--windowed` flag hides the console window. The app also hides it at runtime via `ctypes.windll.user32.ShowWindow`.

---

## Known Issues / Future Work
- **Macros**: Protocol partially reverse engineered. Single slot (0x07) works but multiple macro slots need investigation. Hidden from UI until stable.
- **Checksum**: Formula `(action_code + btn + 0x02) & 0xFF` confirmed for all tested binds. Edge cases not fully explored.
- **Read-back**: Mouse does not return current config — all ACK responses are empty. Config is managed entirely by the app.
