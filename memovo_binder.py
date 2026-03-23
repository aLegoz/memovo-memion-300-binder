import sys
import os
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

import tkinter as tk
from tkinter import ttk, messagebox
import hid
import json
import os
import time
import threading
from pynput import keyboard, mouse

VENDOR_ID = 0x17ef
PRODUCT_ID = 0x60e4
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memovo_config.json")

MOUSE_BUTTONS = [
    (0x00, "Button 1 (Left)"),
    (0x01, "Button 2 (Right)"),
    (0x02, "Button 3 (Middle)"),
    (0x09, "Button 4 (DPI)"),
    (0x05, "Button 5"),
    (0x06, "Button 6"),
    (0x07, "Button 7"),
    (0x08, "Button 8"),
]

ACTIONS = [
    ("--- Mouse ---",     None,       None),
    ("Left Click",        "special",  0xb0),
    ("Right Click",       "special",  0xb1),
    ("Middle Click",      "special",  0xb2),
    ("Forward",           "special",  0xb3),
    ("Backward",          "special",  0xb4),
    ("DPI Switch",        "special",  0xc1),
    ("--- Media ---",     None,       None),
    ("Volume Up",         "special",  0x90),
    ("Volume Down",       "special",  0x91),
    ("Mute",              "special",  0x92),
    ("Play / Pause",      "special",  0x93),
    ("Previous Track",    "special",  0x95),
    ("Next Track",        "special",  0x96),
    ("--- Other ---",     None,       None),
    ("Disable",           "disable",  0x01),
    ("Keyboard Key...",   "keyboard", None),
    ("Macro...",          "macro",    None),
]

TK_TO_HID = {
    "a":0x04,"b":0x05,"c":0x06,"d":0x07,"e":0x08,"f":0x09,"g":0x0a,"h":0x0b,
    "i":0x0c,"j":0x0d,"k":0x0e,"l":0x0f,"m":0x10,"n":0x11,"o":0x12,"p":0x13,
    "q":0x14,"r":0x15,"s":0x16,"t":0x17,"u":0x18,"v":0x19,"w":0x1a,"x":0x1b,
    "y":0x1c,"z":0x1d,"1":0x1e,"2":0x1f,"3":0x20,"4":0x21,"5":0x22,"6":0x23,
    "7":0x24,"8":0x25,"9":0x26,"0":0x27,"return":0x28,"escape":0x29,
    "backspace":0x2a,"tab":0x2b,"space":0x2c,"minus":0x2d,"equal":0x2e,
    "bracketleft":0x2f,"bracketright":0x30,"backslash":0x31,"semicolon":0x33,
    "apostrophe":0x34,"grave":0x35,"comma":0x36,"period":0x37,"slash":0x38,
    "caps_lock":0x39,"f1":0x3a,"f2":0x3b,"f3":0x3c,"f4":0x3d,"f5":0x3e,
    "f6":0x3f,"f7":0x40,"f8":0x41,"f9":0x42,"f10":0x43,"f11":0x44,"f12":0x45,
    "print":0x46,"scroll_lock":0x47,"pause":0x48,"insert":0x49,"home":0x4a,
    "prior":0x4b,"delete":0x4c,"end":0x4d,"next":0x4e,"right":0x4f,"left":0x50,
    "down":0x51,"up":0x52,"num_lock":0x53,"kp_divide":0x54,"kp_multiply":0x55,
    "kp_subtract":0x56,"kp_add":0x57,"kp_enter":0x58,"kp_end":0x59,
    "kp_down":0x5a,"kp_next":0x5b,"kp_left":0x5c,"kp_begin":0x5d,
    "kp_right":0x5e,"kp_home":0x5f,"kp_up":0x60,"kp_prior":0x61,
    "kp_insert":0x62,"kp_delete":0x63,"control_l":0xe0,"shift_l":0xe1,
    "alt_l":0xe2,"super_l":0xe3,"control_r":0xe4,"shift_r":0xe5,
    "alt_r":0xe6,"super_r":0xe7,
}

PYNPUT_TO_HID = {
    keyboard.Key.enter: 0x28, keyboard.Key.esc: 0x29, keyboard.Key.backspace: 0x2a,
    keyboard.Key.tab: 0x2b, keyboard.Key.space: 0x2c, keyboard.Key.caps_lock: 0x39,
    keyboard.Key.f1: 0x3a, keyboard.Key.f2: 0x3b, keyboard.Key.f3: 0x3c,
    keyboard.Key.f4: 0x3d, keyboard.Key.f5: 0x3e, keyboard.Key.f6: 0x3f,
    keyboard.Key.f7: 0x40, keyboard.Key.f8: 0x41, keyboard.Key.f9: 0x42,
    keyboard.Key.f10: 0x43, keyboard.Key.f11: 0x44, keyboard.Key.f12: 0x45,
    keyboard.Key.print_screen: 0x46, keyboard.Key.scroll_lock: 0x47,
    keyboard.Key.pause: 0x48, keyboard.Key.insert: 0x49, keyboard.Key.home: 0x4a,
    keyboard.Key.page_up: 0x4b, keyboard.Key.delete: 0x4c, keyboard.Key.end: 0x4d,
    keyboard.Key.page_down: 0x4e, keyboard.Key.right: 0x4f, keyboard.Key.left: 0x50,
    keyboard.Key.down: 0x51, keyboard.Key.up: 0x52, keyboard.Key.num_lock: 0x53,
    keyboard.Key.ctrl_l: 0xe0, keyboard.Key.shift_l: 0xe1, keyboard.Key.alt_l: 0xe2,
    keyboard.Key.cmd_l: 0xe3, keyboard.Key.ctrl_r: 0xe4, keyboard.Key.shift_r: 0xe5,
    keyboard.Key.alt_r: 0xe6, keyboard.Key.cmd_r: 0xe7,
    keyboard.Key.ctrl: 0xe0, keyboard.Key.shift: 0xe1, keyboard.Key.alt: 0xe2,
}

HID_TO_NAME = {v: k.upper().replace("_"," ") for k,v in TK_TO_HID.items()}
HID_TO_NAME.update({
    0x28:"ENTER",0x29:"ESC",0x2a:"BACKSPACE",0x2b:"TAB",0x2c:"SPACE",
    0x4a:"HOME",0x4b:"PAGE UP",0x4d:"END",0x4e:"PAGE DOWN",
    0x4f:"→",0x50:"←",0x51:"↓",0x52:"↑",0x53:"NUM LOCK",
    0xe0:"LEFT CTRL",0xe1:"LEFT SHIFT",0xe2:"LEFT ALT",
    0xe4:"RIGHT CTRL",0xe5:"RIGHT SHIFT",0xe6:"RIGHT ALT",
})

BG="#0f0f0f"; BG2="#1a1a1a"; BG3="#242424"; BG4="#2e2e2e"
ACCENT="#e8333a"; ACCENT2="#ff6b6b"
FG="#e0e0e0"; FG2="#888888"; GREEN="#00e676"; YELLOW="#ffd740"; BLUE="#4fc3f7"
FONT=("Segoe UI",9); FONT_B=("Segoe UI",9,"bold"); FONT_SM=("Segoe UI",8)
FONT_MONO=("Consolas",9)


def get_hid_path():
    for d in hid.enumerate(VENDOR_ID, PRODUCT_ID):
        if d['usage_page'] == 0xFF01:
            return d['path']
    return None


def send_packet(pkt):
    path = get_hid_path()
    if not path:
        return False, "Mouse not found"
    try:
        h = hid.device()
        h.open_path(path)
        h.set_nonblocking(1)
        h.write([0x00] + pkt + [0x00]*(64-len(pkt)))
        h.close()
        return True, "OK"
    except Exception as e:
        return False, str(e)


def commit():
    return send_packet([0x05] + [0x00]*63)


def send_bind(btn_code, action_type, action_code, key_code=None):
    if action_type == "keyboard":
        kc = key_code or 0x04
        cs = (0xfe + kc + btn_code + 0x02) & 0xFF
        pkt = [0x02,0x00,btn_code,0xfe,kc]+[0x00]*58+[cs]
    elif action_type == "disable":
        cs = (0x01 + btn_code + 0x02) & 0xFF
        pkt = [0x02,0x00,btn_code,0x01,0x00]+[0x00]*58+[cs]
    else:
        cs = (action_code + btn_code + 0x02) & 0xFF
        pkt = [0x02,0x00,btn_code,action_code,0x00]+[0x00]*58+[cs]
    return send_packet(pkt)


def send_macro(btn_code, slot, events):
    CHUNK_PAYLOAD = 0x32
    evt_bytes = []
    for (etype, ecode, delay_ms) in events:
        dl = delay_ms & 0xFF
        dh = (delay_ms >> 8) & 0xFF
        evt_bytes += [etype, ecode, 0x01, dl, dh]
    total_bytes = len(evt_bytes)
    ok, msg = send_packet([0xfb, slot] + [0x00]*62)
    if not ok: return False, msg
    ok, msg = send_packet([0xfe, slot, 0x00, total_bytes & 0xFF, (total_bytes >> 8) & 0xFF] + [0x00]*59)
    if not ok: return False, msg
    chunks = []
    i = 0
    while i < len(evt_bytes):
        chunks.append(evt_bytes[i:i+CHUNK_PAYLOAD])
        i += CHUNK_PAYLOAD
    total_chunks = len(chunks)
    for chunk_num, chunk in enumerate(chunks, start=1):
        chunk_size = len(chunk)
        pkt = [0xfd, slot, 0x00, chunk_num, 0x00, total_chunks, chunk_size, 0x00]
        pkt += [0x00] * 14
        pkt += chunk
        ok, msg = send_packet(pkt)
        if not ok: return False, msg
    cs = (0xf2 + slot + btn_code + 0x02) & 0xFF
    ok, msg = send_packet([0x02, 0x00, btn_code, 0xf2, slot] + [0x00]*58 + [cs])
    if not ok: return False, msg
    return commit()


EVENT_TYPE_NAMES = {
    0x02: "Key Press", 0x03: "Key Release",
    0x04: "Mouse Press", 0x05: "Mouse Release",
    0x09: "Wheel Down", 0x08: "Wheel Up",
}
MOUSE_BTN_NAMES = {0x01: "Left", 0x02: "Right", 0x03: "Middle"}


class MacroEditor(tk.Toplevel):
    def __init__(self, parent, macro_name="", events=None, on_save=None):
        super().__init__(parent)
        self.title("Macro Editor")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.geometry("600x520")
        self.on_save = on_save
        self.events = list(events or [])
        self.recording = False
        self._rec_listener_kb = None
        self._rec_listener_ms = None
        self._rec_last_time = None
        self._record_clicks = tk.BooleanVar(value=True)
        self._macro_name = tk.StringVar(value=macro_name or "Macro")
        self._build()
        self._refresh_list()
        self.grab_set()

    def _build(self):
        top = tk.Frame(self, bg=BG, pady=10)
        top.pack(fill="x", padx=16)
        tk.Label(top, text="Name:", font=FONT, fg=FG2, bg=BG).pack(side="left")
        tk.Entry(top, textvariable=self._macro_name, font=FONT_B, bg=BG3, fg=FG,
                 insertbackground=FG, relief="flat", width=20).pack(side="left", padx=(4,16))
        tk.Checkbutton(top, text="Record clicks", variable=self._record_clicks,
                       font=FONT_SM, bg=BG, fg=FG2, selectcolor=BG3,
                       activebackground=BG, activeforeground=FG).pack(side="left")
        tk.Frame(self, bg="#2a2a2a", height=1).pack(fill="x")
        list_frame = tk.Frame(self, bg=BG)
        list_frame.pack(fill="both", expand=True, padx=16, pady=8)
        cols = ("#", "Action", "Delay (ms)")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=14)
        self.tree.heading("#", text="#")
        self.tree.heading("Action", text="Action")
        self.tree.heading("Delay (ms)", text="Delay (ms)")
        self.tree.column("#", width=40, anchor="center")
        self.tree.column("Action", width=300)
        self.tree.column("Delay (ms)", width=120, anchor="center")
        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        btn_frame = tk.Frame(self, bg=BG, pady=8)
        btn_frame.pack(fill="x", padx=16)
        self.rec_btn = tk.Button(btn_frame, text="● RECORD", font=FONT_B,
                                  bg=ACCENT, fg="white", relief="flat", cursor="hand2",
                                  padx=12, pady=6, command=self._toggle_record)
        self.rec_btn.pack(side="left", padx=(0,8))
        tk.Button(btn_frame, text="Delete", font=FONT, bg=BG3, fg=FG,
                  relief="flat", cursor="hand2", padx=10, pady=6,
                  command=self._delete_selected).pack(side="left", padx=(0,8))
        tk.Button(btn_frame, text="Clear", font=FONT, bg=BG3, fg=FG,
                  relief="flat", cursor="hand2", padx=10, pady=6,
                  command=self._clear).pack(side="left")
        tk.Button(btn_frame, text="Save", font=FONT_B, bg=GREEN, fg="#000",
                  relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._save).pack(side="right")
        self.status = tk.Label(self, text="", font=FONT_SM, bg=BG, fg=FG2)
        self.status.pack(pady=(0,8))

    def _refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for i, (etype, ecode, delay_ms) in enumerate(self.events):
            self.tree.insert("", "end", values=(i+1, self._event_name(etype, ecode), delay_ms))

    def _event_name(self, etype, ecode):
        if etype in (0x02, 0x03):
            return f"{'Press' if etype==0x02 else 'Release'} {HID_TO_NAME.get(ecode, f'Key 0x{ecode:02x}')}"
        elif etype in (0x04, 0x05):
            return f"Mouse {'Press' if etype==0x04 else 'Release'} {MOUSE_BTN_NAMES.get(ecode, f'Btn{ecode}')}"
        elif etype == 0x09: return "Wheel Down"
        elif etype == 0x08: return "Wheel Up"
        return f"Unknown 0x{etype:02x} 0x{ecode:02x}"

    def _toggle_record(self):
        if not self.recording: self._start_record()
        else: self._stop_record()

    def _start_record(self):
        self.recording = True
        self.rec_btn.config(text="■ STOP", bg="#555")
        self.status.config(text="Recording... press STOP when done", fg=ACCENT2)
        self._rec_last_time = time.time()

        def on_press(key):
            if not self.recording: return
            hid_code = PYNPUT_TO_HID.get(key)
            if hid_code is None and hasattr(key, 'char') and key.char:
                hid_code = TK_TO_HID.get(key.char.lower())
            if hid_code:
                now = time.time()
                delay = int((now - self._rec_last_time) * 1000)
                self._rec_last_time = now
                self.events.append([0x02, hid_code, delay])
                self.after(0, self._refresh_list)

        def on_release(key):
            if not self.recording: return
            hid_code = PYNPUT_TO_HID.get(key)
            if hid_code is None and hasattr(key, 'char') and key.char:
                hid_code = TK_TO_HID.get(key.char.lower())
            if hid_code:
                now = time.time()
                delay = int((now - self._rec_last_time) * 1000)
                self._rec_last_time = now
                self.events.append([0x03, hid_code, delay])
                self.after(0, self._refresh_list)

        def on_click(x, y, button, pressed):
            if not self.recording or not self._record_clicks.get(): return
            btn_map = {mouse.Button.left:0x01, mouse.Button.right:0x02, mouse.Button.middle:0x03}
            code = btn_map.get(button)
            if code:
                now = time.time()
                delay = int((now - self._rec_last_time) * 1000)
                self._rec_last_time = now
                self.events.append([0x04 if pressed else 0x05, code, delay])
                self.after(0, self._refresh_list)

        def on_scroll(x, y, dx, dy):
            if not self.recording: return
            now = time.time()
            delay = int((now - self._rec_last_time) * 1000)
            self._rec_last_time = now
            self.events.append([0x09 if dy < 0 else 0x08, 0x01, delay])
            self.after(0, self._refresh_list)

        self._rec_listener_kb = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._rec_listener_ms = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
        self._rec_listener_kb.start()
        self._rec_listener_ms.start()

    def _stop_record(self):
        self.recording = False
        if self._rec_listener_kb: self._rec_listener_kb.stop()
        if self._rec_listener_ms: self._rec_listener_ms.stop()
        self.rec_btn.config(text="● RECORD", bg=ACCENT)
        self.status.config(text=f"Recorded {len(self.events)} events", fg=GREEN)

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel: return
        for i in sorted([self.tree.index(s) for s in sel], reverse=True):
            self.events.pop(i)
        self._refresh_list()

    def _clear(self):
        self.events.clear()
        self._refresh_list()

    def _save(self):
        if self.recording: self._stop_record()
        if self.on_save: self.on_save(self._macro_name.get(), self.events)
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Memovo Memion 300 Binder")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.macros = {}
        self.btn_state = {}
        for btn_code, _ in MOUSE_BUTTONS:
            self.btn_state[btn_code] = {"key_code": None, "key_name": None, "macro_name": None}
        self._listening_btn = None
        self._first_launch = not os.path.exists(CONFIG_FILE)
        self._load_config()
        self._build()
        if self._first_launch:
            self._reset_defaults()
        self._refresh_status()

    def _build(self):
        hdr = tk.Frame(self, bg=BG, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="MEMOVO MEMION 300", font=("Segoe UI",16,"bold"), fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text=" BINDER", font=("Segoe UI",16), fg=FG2, bg=BG).pack(side="left")
        self.status_lbl = tk.Label(hdr, text="", font=FONT_SM, bg=BG)
        self.status_lbl.pack(side="right")
        tk.Frame(self, bg="#2a2a2a", height=1).pack(fill="x")
        hrow = tk.Frame(self, bg=BG2, pady=4)
        hrow.pack(fill="x")
        tk.Label(hrow, text="Button", font=FONT_SM, fg=FG2, bg=BG2, width=20, anchor="w").pack(side="left", padx=(20,8))
        tk.Label(hrow, text="Action", font=FONT_SM, fg=FG2, bg=BG2, width=20, anchor="w").pack(side="left", padx=(0,8))
        tk.Label(hrow, text="Parameter", font=FONT_SM, fg=FG2, bg=BG2, width=18, anchor="w").pack(side="left")
        tk.Frame(self, bg="#2a2a2a", height=1).pack(fill="x")
        for i, (btn_code, btn_name) in enumerate(MOUSE_BUTTONS):
            bg = BG if i % 2 == 0 else BG2
            frame = tk.Frame(self, bg=bg, pady=6)
            frame.pack(fill="x")
            tk.Label(frame, text=btn_name, font=FONT_B, fg=FG, bg=bg, width=20, anchor="w").pack(side="left", padx=(20,8))
            var = tk.StringVar(value="Left Click")
            self.btn_state[btn_code]["var"] = var
            cb = ttk.Combobox(frame, textvariable=var, values=[a[0] for a in ACTIONS], state="readonly", width=18, font=FONT)
            cb.pack(side="left", padx=(0,8))
            cb.bind("<<ComboboxSelected>>", lambda e, b=btn_code: self._on_action_change(b))
            param_lbl = tk.Label(frame, text="", font=FONT_SM, bg=BG3, fg=FG2,
                                 relief="flat", padx=10, pady=5, width=18, cursor="hand2")
            param_lbl.pack(side="left", padx=(0,16))
            param_lbl.bind("<Button-1>", lambda e, b=btn_code: self._param_click(b))
            self.btn_state[btn_code]["param_lbl"] = param_lbl
        tk.Frame(self, bg="#2a2a2a", height=1).pack(fill="x")
        footer = tk.Frame(self, bg=BG, pady=12)
        footer.pack(fill="x", padx=24)
        tk.Button(footer, text="APPLY ALL", font=("Segoe UI",10,"bold"),
                  bg=ACCENT, fg="white", activebackground="#c0272d", activeforeground="white",
                  relief="flat", cursor="hand2", padx=18, pady=7,
                  command=self._apply_all).pack(side="right")
        tk.Button(footer, text="Reset to Default", font=FONT, bg=BG3, fg=FG2,
                  relief="flat", cursor="hand2", padx=10, pady=7,
                  command=self._reset_defaults).pack(side="right", padx=(0,8))
        tk.Label(footer, text="Configure buttons and click Apply", font=FONT_SM, fg=FG2, bg=BG).pack(side="left")
        self._restore_ui()

    def _current_action(self, btn_code):
        name = self.btn_state[btn_code]["var"].get()
        for a in ACTIONS:
            if a[0] == name: return a
        return ACTIONS[1]

    def _on_action_change(self, btn_code):
        if self._listening_btn == btn_code: self._stop_listen()
        self._update_param_label(btn_code)

    def _update_param_label(self, btn_code):
        lbl = self.btn_state[btn_code]["param_lbl"]
        atype = self._current_action(btn_code)[1]
        if atype == "keyboard":
            kname = self.btn_state[btn_code]["key_name"]
            lbl.config(text=kname if kname else "[ press a key ]", fg=GREEN if kname else FG2, cursor="hand2")
        elif atype == "macro":
            mname = self.btn_state[btn_code]["macro_name"]
            lbl.config(text=mname if mname else "[ select macro ]", fg=BLUE if mname else FG2, cursor="hand2")
        else:
            lbl.config(text="", cursor="")

    def _param_click(self, btn_code):
        atype = self._current_action(btn_code)[1]
        if atype == "keyboard": self._start_listen(btn_code)
        elif atype == "macro": self._open_macro_picker(btn_code)

    def _start_listen(self, btn_code):
        if self._listening_btn is not None: self._stop_listen()
        self._listening_btn = btn_code
        self.btn_state[btn_code]["param_lbl"].config(text="● listening...", fg=ACCENT2)
        self.bind("<KeyPress>", self._on_key)
        self.focus_set()

    def _stop_listen(self):
        self.unbind("<KeyPress>")
        if self._listening_btn is not None: self._update_param_label(self._listening_btn)
        self._listening_btn = None

    def _on_key(self, event):
        btn_code = self._listening_btn
        if btn_code is None: return
        key = event.keysym.lower()
        hid_code = TK_TO_HID.get(key)
        if hid_code is not None:
            self.btn_state[btn_code]["key_code"] = hid_code
            self.btn_state[btn_code]["key_name"] = HID_TO_NAME.get(hid_code, key.upper())
        else:
            self.btn_state[btn_code]["key_code"] = None
            self.btn_state[btn_code]["key_name"] = f"? {key}"
        self._stop_listen()

    def _open_macro_picker(self, btn_code):
        win = tk.Toplevel(self)
        win.title("Select Macro")
        win.configure(bg=BG)
        win.geometry("320x400")
        win.grab_set()
        tk.Label(win, text="Macros", font=FONT_B, fg=FG, bg=BG).pack(pady=(12,4))
        tk.Frame(win, bg="#2a2a2a", height=1).pack(fill="x")
        lbox_frame = tk.Frame(win, bg=BG)
        lbox_frame.pack(fill="both", expand=True, padx=16, pady=8)
        lbox = tk.Listbox(lbox_frame, bg=BG3, fg=FG, font=FONT_MONO,
                          selectbackground=ACCENT, selectforeground="white", relief="flat", borderwidth=0)
        lbox.pack(fill="both", expand=True)
        for name in self.macros: lbox.insert("end", name)
        btn_row = tk.Frame(win, bg=BG, pady=10)
        btn_row.pack(fill="x", padx=16)
        def new_macro():
            def on_save(name, events):
                self.macros[name] = events
                lbox.insert("end", name)
                self._save_config()
            MacroEditor(win, on_save=on_save)
        def select_macro():
            sel = lbox.curselection()
            if not sel: return
            name = lbox.get(sel[0])
            self.btn_state[btn_code]["macro_name"] = name
            self._update_param_label(btn_code)
            win.destroy()
        def edit_macro():
            sel = lbox.curselection()
            if not sel: return
            name = lbox.get(sel[0])
            def on_save(new_name, new_events):
                if new_name != name:
                    del self.macros[name]
                    lbox.delete(sel[0])
                    lbox.insert(sel[0], new_name)
                self.macros[new_name] = new_events
                self._save_config()
            MacroEditor(win, macro_name=name, events=self.macros.get(name,[]), on_save=on_save)
        def delete_macro():
            sel = lbox.curselection()
            if not sel: return
            name = lbox.get(sel[0])
            del self.macros[name]
            lbox.delete(sel[0])
            self._save_config()
        tk.Button(btn_row, text="New", font=FONT, bg=BG3, fg=FG, relief="flat", cursor="hand2", padx=8, pady=5, command=new_macro).pack(side="left", padx=(0,4))
        tk.Button(btn_row, text="Edit", font=FONT, bg=BG3, fg=FG, relief="flat", cursor="hand2", padx=8, pady=5, command=edit_macro).pack(side="left", padx=(0,4))
        tk.Button(btn_row, text="Delete", font=FONT, bg=BG3, fg=FG, relief="flat", cursor="hand2", padx=8, pady=5, command=delete_macro).pack(side="left")
        tk.Button(btn_row, text="Select", font=FONT_B, bg=GREEN, fg="#000", relief="flat", cursor="hand2", padx=10, pady=5, command=select_macro).pack(side="right")

    def _apply_all(self):
        applied = 0; errors = []
        for btn_code, btn_name in MOUSE_BUTTONS:
            action = self._current_action(btn_code)
            aname, atype, acode = action
            if atype is None: continue
            if atype == "keyboard":
                kc = self.btn_state[btn_code]["key_code"]
                if not kc:
                    errors.append(f"{btn_name}: key not selected")
                    continue
                ok, msg = send_bind(btn_code, "keyboard", None, kc)
            elif atype == "macro":
                mname = self.btn_state[btn_code]["macro_name"]
                if not mname or mname not in self.macros:
                    errors.append(f"{btn_name}: macro not selected")
                    continue
                ok, msg = send_macro(btn_code, 0x07, self.macros[mname])
            else:
                ok, msg = send_bind(btn_code, atype, acode)
            if ok: applied += 1
            else: errors.append(f"{btn_name}: {msg}")
        self._save_config()
        commit()
        if errors: messagebox.showerror("Error", "\n".join(errors))
        if applied: messagebox.showinfo("Done", f"✓ Applied {applied} binds!")

    def _reset_defaults(self):
        defaults = {
            0x00:"Left Click", 0x01:"Right Click", 0x02:"Middle Click",
            0x09:"DPI Switch", 0x05:"Forward", 0x06:"Backward",
            0x07:"Disable", 0x08:"Disable",
        }
        for btn_code, action_name in defaults.items():
            self.btn_state[btn_code]["var"].set(action_name)
            self.btn_state[btn_code]["key_code"] = None
            self.btn_state[btn_code]["key_name"] = None
            self.btn_state[btn_code]["macro_name"] = None
            self._update_param_label(btn_code)

    def _refresh_status(self):
        path = get_hid_path()
        self.status_lbl.config(text="● connected" if path else "● not found",
                               fg=GREEN if path else ACCENT)
        self.after(3000, self._refresh_status)

    def _save_config(self):
        data = {"macros": self.macros, "buttons": {}}
        for btn_code, _ in MOUSE_BUTTONS:
            st = self.btn_state[btn_code]
            action = self._current_action(btn_code)
            data["buttons"][str(btn_code)] = {
                "action": action[0],
                "key_code": st.get("key_code"),
                "key_name": st.get("key_name"),
                "macro_name": st.get("macro_name"),
            }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Config save error: {e}")

    def _load_config(self):
        if not os.path.exists(CONFIG_FILE): return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.macros = data.get("macros", {})
            for btn_code, _ in MOUSE_BUTTONS:
                bdata = data.get("buttons", {}).get(str(btn_code))
                if bdata:
                    self.btn_state[btn_code]["key_code"] = bdata.get("key_code")
                    self.btn_state[btn_code]["key_name"] = bdata.get("key_name")
                    self.btn_state[btn_code]["macro_name"] = bdata.get("macro_name")
                    self.btn_state[btn_code]["_saved_action"] = bdata.get("action")
        except Exception as e:
            print(f"Config load error: {e}")

    def _restore_ui(self):
        for btn_code, _ in MOUSE_BUTTONS:
            saved = self.btn_state[btn_code].get("_saved_action")
            if saved: self.btn_state[btn_code]["var"].set(saved)
            self._update_param_label(btn_code)


def style_widgets(root):
    s = ttk.Style(root)
    s.theme_use("default")
    s.configure("TCombobox", fieldbackground=BG3, background=BG3, foreground=FG,
                selectbackground=BG3, selectforeground=FG, arrowcolor=FG2, borderwidth=0)
    s.map("TCombobox", fieldbackground=[("readonly",BG3)], foreground=[("readonly",FG)],
          selectbackground=[("readonly",BG3)])
    s.configure("Treeview", background=BG3, foreground=FG, fieldbackground=BG3, borderwidth=0, rowheight=24)
    s.configure("Treeview.Heading", background=BG2, foreground=FG2, borderwidth=0, relief="flat")
    s.map("Treeview", background=[("selected",ACCENT)], foreground=[("selected","white")])


if __name__ == "__main__":
    app = App()
    style_widgets(app)
    app.mainloop()
