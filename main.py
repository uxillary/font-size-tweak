import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import winreg
import struct

# Font keys and descriptions
font_key_map = {
    "Title Bar (CaptionFont)": "CaptionFont",
    "Menus (MenuFont)": "MenuFont",
    "Message Boxes (MessageFont)": "MessageFont",
    "Icons (IconFont)": "IconFont",
    "Status Bar (StatusFont)": "StatusFont"
}

font_key_desc = {
    "CaptionFont": "Affects: Window title bars (e.g. Notepad, Explorer)",
    "MenuFont": "Affects: Menu bars and right-click menus",
    "MessageFont": "Affects: Message dialogs (OK/Cancel popups)",
    "IconFont": "Affects: Desktop and Explorer icon labels",
    "StatusFont": "Affects: Status bars in legacy apps"
}

registry_path = r'Control Panel\\Desktop\\WindowMetrics'
default_size = 9

# ========== Font Reading Helper ==========
def get_current_font_size(font_key_name):
    try:
        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, registry_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, font_key_name)
        winreg.CloseKey(key)

        font_bytes = bytearray(value)
        height = struct.unpack("<l", font_bytes[0:4])[0]
        pt_size = round(abs(height) / 1.33)
        return f"{pt_size}pt (height: {height})"
    except:
        return "Unknown"

# ========== Registry Write ==========
def set_font_size(size):
    try:
        height = -round(size * 1.33)
        font_key_name = font_key_map[selected_font.get()]

        registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(registry, registry_path, 0, winreg.KEY_ALL_ACCESS)

        value, regtype = winreg.QueryValueEx(key, font_key_name)
        font_bytes = bytearray(value)
        font_bytes[0:4] = struct.pack("<l", height)

        winreg.SetValueEx(key, font_key_name, 0, winreg.REG_BINARY, bytes(font_bytes))
        winreg.CloseKey(key)
        return True
    except Exception as e:
        ttk.dialogs.Messagebox.show_error("Registry Error", str(e))
        return False

def reset_all():
    for font_key_name in font_key_map.values():
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, registry_path, 0, winreg.KEY_ALL_ACCESS)
            value, regtype = winreg.QueryValueEx(key, font_key_name)
            font_bytes = bytearray(value)
            font_bytes[0:4] = struct.pack("<l", -round(default_size * 1.33))
            winreg.SetValueEx(key, font_key_name, 0, winreg.REG_BINARY, bytes(font_bytes))
            winreg.CloseKey(key)
        except:
            pass
    quick_feedback.config(text="✅ All fonts reset to default size.")

# ========== App Window ==========
app = ttk.Window(title="Font Size Tweak", themename="darkly", resizable=(False, False))
app.geometry("540x860")
app.option_add("*Font", ("Segoe UI", 12))

# ========== HEADER ==========
ttk.Label(app, text="Font Size Tweak", font=("Segoe UI", 16, "bold"), bootstyle="inverse-dark")\
    .pack(pady=(15, 10))

# ========== QUICK APPLY ==========
quick_frame = ttk.LabelFrame(app, text="Quick Apply (All Fonts)", padding=(15, 10))
quick_frame.pack(fill="x", padx=20, pady=(0, 20))

ttk.Label(quick_frame, text="Choose Font Size:", bootstyle="secondary", font=("Segoe UI", 13, "bold")).pack()
quick_slider = ttk.Scale(quick_frame, from_=8, to=16, orient="horizontal", length=300)
quick_slider.set(11)
quick_slider.pack(pady=5)

quick_val_label = ttk.Label(quick_frame, text=f"{int(quick_slider.get())} pt")
quick_val_label.pack()

def update_quick_val(*args):
    quick_val_label.config(text=f"{int(quick_slider.get())} pt")

quick_slider.configure(command=lambda v: update_quick_val())

def quick_apply():
    size = int(quick_slider.get())
    for font_key_name in font_key_map.values():
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, registry_path, 0, winreg.KEY_ALL_ACCESS)
            value, regtype = winreg.QueryValueEx(key, font_key_name)
            font_bytes = bytearray(value)
            font_bytes[0:4] = struct.pack("<l", -round(size * 1.33))
            winreg.SetValueEx(key, font_key_name, 0, winreg.REG_BINARY, bytes(font_bytes))
            winreg.CloseKey(key)
        except:
            pass
    quick_feedback.config(text=f"✅ Applied {size}pt to all fonts. Log out to apply.")

# Buttons
ttk.Button(quick_frame, text="Apply to All", command=quick_apply, bootstyle="success-outline")\
    .pack(pady=(10, 5))
quick_feedback = ttk.Label(quick_frame, text="", bootstyle="success")
quick_feedback.pack()

# ========== INDIVIDUAL CONTROL ==========
indiv_frame = ttk.LabelFrame(app, text="Advanced Control (Individual Fonts)", padding=(15, 10))
indiv_frame.pack(fill="x", padx=20, pady=(0, 20))

selected_font = ttk.StringVar(value="Icons (IconFont)")
slider_val = ttk.IntVar(value=11)

# Dropdown & current size
ttk.Label(indiv_frame, text="🗂️ Choose Font Type:", font=("Segoe UI", 13, "bold")).pack()
ttk.OptionMenu(indiv_frame, selected_font, selected_font.get(), *font_key_map.keys()).pack()

info_label = ttk.Label(indiv_frame, text="", wraplength=300, bootstyle="info")
info_label.pack(pady=2)
current_val_label = ttk.Label(indiv_frame, text="", bootstyle="secondary")
current_val_label.pack(pady=(2, 5))

# Size slider
slider = ttk.Scale(indiv_frame, from_=8, to=16, orient="horizontal", variable=slider_val, length=300)
slider.pack(pady=5)
indiv_val_label = ttk.Label(indiv_frame, text=f"{slider_val.get()} pt")
indiv_val_label.pack()

preview_label = ttk.Label(indiv_frame, text="The quick brown fox", font=("Segoe UI", 13), bootstyle="info")
preview_label.pack(pady=8)

# Presets
preset_frame = ttk.Frame(indiv_frame)
preset_frame.pack(pady=5)
ttk.Button(preset_frame, text="Small", command=lambda: slider_val.set(9), bootstyle="outline-secondary").pack(side="left", padx=2)
ttk.Button(preset_frame, text="Medium", command=lambda: slider_val.set(11), bootstyle="outline-secondary").pack(side="left", padx=2)
ttk.Button(preset_frame, text="Large", command=lambda: slider_val.set(13), bootstyle="outline-secondary").pack(side="left", padx=2)

feedback_label = ttk.Label(indiv_frame, text="", bootstyle="success")
feedback_label.pack()

def update_info(*args):
    key = font_key_map[selected_font.get()]
    info_label.config(text=font_key_desc.get(key, ""))
    current_val_label.config(text=f"🕵️ Current size: {get_current_font_size(key)}")
    feedback_label.config(text="")

def update_preview(*args):
    preview_label.config(font=("Segoe UI", slider_val.get()))

def update_indiv_val(*args):
    indiv_val_label.config(text=f"{slider_val.get()} pt")

selected_font.trace("w", update_info)
slider_val.trace("w", update_preview)
slider_val.trace("w", update_indiv_val)

def apply_size():
    size = slider_val.get()
    if set_font_size(size):
        feedback_label.config(
            text=f"✅ Applied {size}pt to {selected_font.get().split()[0]}. Log out to apply."
        )
        current_val_label.config(
            text=f"🕵️ Current size: {get_current_font_size(font_key_map[selected_font.get()])}"
        )

# Buttons
button_frame = ttk.Frame(indiv_frame)
button_frame.pack(pady=(10, 5))
ttk.Button(button_frame, text="Apply Size", command=apply_size, bootstyle="success").pack(side="left", padx=5)
ttk.Button(button_frame, text="Reset Font", command=lambda: slider_val.set(default_size), bootstyle="secondary").pack(side="left", padx=5)

# Global Reset
ttk.Button(app, text="Reset All Fonts to Default", command=reset_all, bootstyle="danger-outline")\
    .pack(pady=(0, 15))

# Footer note
ttk.Label(
    app,
    text="Note: Properties windows and some system dialogs may only scale via Accessibility settings.",
    wraplength=500,
    bootstyle="warning"
).pack(pady=(0, 10))

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev & for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app.iconbitmap(resource_path("icon.ico"))
app.mainloop()
