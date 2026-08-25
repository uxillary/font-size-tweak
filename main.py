import os
import struct
import sys
import tkinter as tk
from tkinter import messagebox
import winreg

import ttkbootstrap as ttk


FONT_KEY_MAP = {
    "Title Bar": "CaptionFont",
    "Menus": "MenuFont",
    "Message Boxes": "MessageFont",
    "Icons": "IconFont",
    "Status Bar": "StatusFont",
}
FONT_KEY_DESC = {
    "CaptionFont": "Window title bars (for example, Notepad and Explorer)",
    "MenuFont": "Menu bars and right-click menus",
    "MessageFont": "Message dialogs and prompts",
    "IconFont": "Desktop and Explorer icon labels",
    "StatusFont": "Status bars in legacy applications",
}
REGISTRY_PATH = r"Control Panel\Desktop\WindowMetrics"
MIN_SIZE, MAX_SIZE, START_SIZE = 8, 16, 11

original_values = None
undo_values = None
operation_in_progress = False


# Preserve every byte except the first four-byte lfHeight when changing a size.
def read_font_value(font_key_name):
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_READ
    ) as key:
        value, value_type = winreg.QueryValueEx(key, font_key_name)
    if value_type != winreg.REG_BINARY:
        raise ValueError(f"{font_key_name} is not a REG_BINARY value")
    if not isinstance(value, bytes) or len(value) < 4:
        raise ValueError(f"{font_key_name} contains invalid font data")
    return value


def write_font_value(font_key_name, value):
    if not isinstance(value, bytes) or len(value) < 4:
        raise ValueError(f"Refusing to write invalid data to {font_key_name}")
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, REGISTRY_PATH, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, font_key_name, 0, winreg.REG_BINARY, value)


def value_with_size(value, size):
    if not isinstance(value, bytes) or len(value) < 4:
        raise ValueError("Font data is too short to contain lfHeight")
    font_bytes = bytearray(value)
    font_bytes[:4] = struct.pack("<l", -round(size * 1.33))
    return bytes(font_bytes)


def point_size_from_value(value):
    height = struct.unpack("<l", value[:4])[0]
    return round(abs(height) / 1.33)


def read_values(font_key_names):
    return {name: read_font_value(name) for name in font_key_names}


def ensure_original_backup():
    global original_values
    if original_values is None:
        # Refuse all writes unless all five originals can first be captured.
        original_values = read_values(FONT_KEY_MAP.values())
    return original_values


def resource_path(relative_path):
    """Return an asset path for development and PyInstaller onefile builds."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def valid_size(value):
    try:
        size = int(value)
    except (TypeError, ValueError):
        return None
    return size if MIN_SIZE <= size <= MAX_SIZE else None


app = ttk.Window(title="Font Size Tweak", themename="darkly", resizable=(False, False))
app.geometry("570x650")
app.option_add("*Font", ("Segoe UI", 10))

quick_size = tk.StringVar(value=str(START_SIZE))
individual_size = tk.StringVar(value=str(START_SIZE))
selected_font = tk.StringVar(value="Icons")
current_size = None
size_sync_in_progress = False


def set_status(text, style="secondary"):
    status_label.configure(text=text, bootstyle=style)


def update_undo_button():
    state = "disabled" if operation_in_progress or undo_values is None else "normal"
    undo_button.configure(state=state)


def set_operation_controls_enabled(enabled):
    state = "normal" if enabled else "disabled"
    for control in operation_controls:
        control.configure(state=state)
    update_undo_button()


def run_operation(callback):
    global operation_in_progress
    if operation_in_progress:
        return
    operation_in_progress = True
    set_operation_controls_enabled(False)
    app.update_idletasks()
    try:
        callback()
    finally:
        operation_in_progress = False
        set_operation_controls_enabled(True)


def format_errors(errors):
    return "; ".join(f"{name}: {error}" for name, error in errors)


def refresh_current_value(clear_status=False):
    global current_size
    display_name = selected_font.get()
    font_key_name = FONT_KEY_MAP[display_name]
    description_label.configure(text=FONT_KEY_DESC[font_key_name])
    apply_individual_button.configure(text=f"Apply to {display_name}")
    restore_selected_button.configure(text=f"Restore {display_name}")
    try:
        current_size = point_size_from_value(read_font_value(font_key_name))
        current_label.configure(text=f"Current: {current_size} pt")
    except (OSError, ValueError, struct.error) as error:
        current_size = None
        current_label.configure(text="Current: unavailable")
        set_status(f"Could not read {font_key_name}: {error}", "danger")
    update_proposed_value()
    if clear_status and current_size is not None:
        set_status("Ready. Changes affect supported Windows font metrics only.")


def update_proposed_value(*_args):
    size = valid_size(individual_size.get())
    if size is None:
        proposed_label.configure(
            text=f"New: enter {MIN_SIZE}\u2013{MAX_SIZE} pt", bootstyle="warning"
        )
    elif current_size is not None and size != current_size:
        proposed_label.configure(text=f"New: {size} pt", bootstyle="info")
    else:
        proposed_label.configure(text=f"New: {size} pt", bootstyle="light")


def sync_from_slider(variable, slider_value, preview_label):
    global size_sync_in_progress
    if size_sync_in_progress:
        return
    size_sync_in_progress = True
    try:
        size = max(MIN_SIZE, min(MAX_SIZE, round(float(slider_value))))
        variable.set(str(size))
        preview_label.configure(font=("Segoe UI", size))
    finally:
        size_sync_in_progress = False
    update_proposed_value()


def sync_from_spinbox(variable, slider, preview_label):
    global size_sync_in_progress
    if size_sync_in_progress:
        return
    size = valid_size(variable.get())
    if size is None:
        if variable is individual_size:
            update_proposed_value()
        return
    size_sync_in_progress = True
    try:
        slider.set(size)
        preview_label.configure(font=("Segoe UI", size))
    finally:
        size_sync_in_progress = False
    if variable is individual_size:
        update_proposed_value()


def validate_spinbox(proposed):
    return proposed == "" or (proposed.isdigit() and len(proposed) <= 2)


def apply_sizes(font_key_names, size, success_text):
    global undo_values
    try:
        ensure_original_backup()
    except (OSError, ValueError) as error:
        set_status(f"Could not back up original settings: {error}", "danger")
        return

    previous, errors = {}, []
    for font_key_name in font_key_names:
        try:
            value = read_font_value(font_key_name)
            updated_value = value_with_size(value, size)
            if updated_value != value:
                write_font_value(font_key_name, updated_value)
                previous[font_key_name] = value
        except (OSError, ValueError, struct.error) as error:
            errors.append((font_key_name, error))

    if previous:
        undo_values = previous
        update_undo_button()
        refresh_current_value()
    if errors:
        prefix = f"Updated {len(previous)} setting(s). " if previous else ""
        set_status(prefix + "Could not update " + format_errors(errors), "danger")
    elif previous:
        set_status(success_text, "success")
    else:
        set_status("No changes were needed.")


def quick_apply():
    size = valid_size(quick_size.get())
    if size is None:
        set_status(f"Enter a quick font size from {MIN_SIZE} to {MAX_SIZE} pt.", "warning")
        return
    run_operation(
        lambda: apply_sizes(
            list(FONT_KEY_MAP.values()), size,
            "Changes saved. Sign out of Windows to see them everywhere.",
        )
    )


def apply_individual():
    size = valid_size(individual_size.get())
    if size is None:
        set_status(
            f"Enter an individual font size from {MIN_SIZE} to {MAX_SIZE} pt.",
            "warning",
        )
        return
    display_name = selected_font.get()
    run_operation(
        lambda: apply_sizes(
            [FONT_KEY_MAP[display_name]], size,
            f"{display_name} saved. Sign out of Windows to see the change everywhere.",
        )
    )


def restore_values(target_values, success_text):
    global undo_values
    previous, errors = {}, []
    for font_key_name, original_value in target_values.items():
        try:
            current_value = read_font_value(font_key_name)
            if current_value != original_value:
                write_font_value(font_key_name, original_value)
                previous[font_key_name] = current_value
        except (OSError, ValueError) as error:
            errors.append((font_key_name, error))

    if previous:
        undo_values = previous
        update_undo_button()
        refresh_current_value()
    if errors:
        prefix = f"Restored {len(previous)} setting(s). " if previous else ""
        set_status(prefix + "Could not restore " + format_errors(errors), "danger")
    elif previous:
        set_status(success_text, "success")
    else:
        set_status("The selected settings already match the original values.")


def restore_selected():
    display_name = selected_font.get()
    font_key_name = FONT_KEY_MAP[display_name]

    def restore():
        try:
            backup = ensure_original_backup()
        except (OSError, ValueError) as error:
            set_status(f"Could not back up original settings: {error}", "danger")
            return
        restore_values(
            {font_key_name: backup[font_key_name]},
            f"{display_name} restored to its original setting.",
        )

    run_operation(restore)


def restore_all():
    if not messagebox.askyesno(
        "Restore Original Settings",
        "Restore all five font settings to the values captured before this app's first change?",
        parent=app,
    ):
        return

    def restore():
        try:
            backup = ensure_original_backup()
        except (OSError, ValueError) as error:
            set_status(f"Could not back up original settings: {error}", "danger")
            return
        restore_values(backup, "All font settings restored to their original values.")

    run_operation(restore)


def undo_last_change():
    global undo_values
    if undo_values is None:
        return

    def undo():
        global undo_values
        values_to_restore = undo_values
        undo_values = None  # One level only; consume the snapshot before writing.
        errors = []
        failed_values = {}
        restored = 0
        for font_key_name, value in values_to_restore.items():
            try:
                write_font_value(font_key_name, value)
                restored += 1
            except (OSError, ValueError) as error:
                errors.append((font_key_name, error))
                failed_values[font_key_name] = value
        # Retain only failed entries so a transient registry error can be retried.
        undo_values = failed_values or None
        refresh_current_value()
        if errors:
            prefix = f"Restored {restored} setting(s). " if restored else ""
            set_status(prefix + "Could not undo " + format_errors(errors), "danger")
        else:
            set_status("Last change undone.", "success")

    run_operation(undo)


# Compact dark interface.
ttk.Label(
    app, text="Font Size Tweak", font=("Segoe UI", 17, "bold"), bootstyle="light"
).pack(pady=(14, 1))
ttk.Label(
    app,
    text="Adjust supported Windows text without changing display scaling",
    bootstyle="secondary",
).pack(pady=(0, 10))

content = ttk.Frame(app, padding=(18, 0))
content.pack(fill="both", expand=True)
content.columnconfigure(0, weight=1)
spin_validation = (app.register(validate_spinbox), "%P")

quick_frame = ttk.LabelFrame(content, text="QUICK ADJUSTMENT", padding=(12, 9))
quick_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
quick_frame.columnconfigure(1, weight=1)
ttk.Label(quick_frame, text="Font size:", bootstyle="light").grid(
    row=0, column=0, padx=(0, 10)
)
quick_slider = ttk.Scale(quick_frame, from_=MIN_SIZE, to=MAX_SIZE, length=300)
quick_slider.set(START_SIZE)
quick_slider.grid(row=0, column=1, sticky="ew", padx=(0, 10))
quick_spinbox = ttk.Spinbox(
    quick_frame, from_=MIN_SIZE, to=MAX_SIZE, increment=1, width=5,
    textvariable=quick_size, validate="key", validatecommand=spin_validation,
)
quick_spinbox.grid(row=0, column=2)
ttk.Label(quick_frame, text="pt", bootstyle="light").grid(row=0, column=3, padx=(4, 0))
quick_preview = ttk.Label(
    quick_frame, text="Preview:  The quick brown fox",
    font=("Segoe UI", START_SIZE), bootstyle="info",
)
quick_preview.grid(row=1, column=0, columnspan=4, pady=(8, 7))
apply_all_button = ttk.Button(
    quick_frame, text="Apply to all font types", command=quick_apply, bootstyle="success"
)
apply_all_button.grid(row=2, column=0, columnspan=4)

individual_frame = ttk.LabelFrame(content, text="INDIVIDUAL ADJUSTMENT", padding=(12, 9))
individual_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
individual_frame.columnconfigure(1, weight=1)
ttk.Label(individual_frame, text="Font type:", bootstyle="light").grid(
    row=0, column=0, sticky="w", padx=(0, 10)
)
font_menu = ttk.OptionMenu(
    individual_frame, selected_font, selected_font.get(), *FONT_KEY_MAP.keys(),
    bootstyle="secondary",
)
font_menu.grid(row=0, column=1, columnspan=3, sticky="w")
description_label = ttk.Label(individual_frame, text="", bootstyle="secondary")
description_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 7))

value_frame = ttk.Frame(individual_frame)
value_frame.grid(row=2, column=0, columnspan=4, sticky="w", pady=(0, 6))
current_label = ttk.Label(value_frame, text="Current: --", bootstyle="light")
current_label.pack(side="left", padx=(0, 24))
proposed_label = ttk.Label(value_frame, text=f"New: {START_SIZE} pt", bootstyle="info")
proposed_label.pack(side="left")

individual_slider = ttk.Scale(individual_frame, from_=MIN_SIZE, to=MAX_SIZE, length=300)
individual_slider.set(START_SIZE)
individual_slider.grid(row=3, column=0, columnspan=2, sticky="ew", padx=(0, 10))
individual_spinbox = ttk.Spinbox(
    individual_frame, from_=MIN_SIZE, to=MAX_SIZE, increment=1, width=5,
    textvariable=individual_size, validate="key", validatecommand=spin_validation,
)
individual_spinbox.grid(row=3, column=2)
ttk.Label(individual_frame, text="pt", bootstyle="light").grid(
    row=3, column=3, padx=(4, 0)
)
individual_preview = ttk.Label(
    individual_frame, text="Preview:  The quick brown fox",
    font=("Segoe UI", START_SIZE), bootstyle="info",
)
individual_preview.grid(row=4, column=0, columnspan=4, pady=(8, 7))

individual_buttons = ttk.Frame(individual_frame)
individual_buttons.grid(row=5, column=0, columnspan=4)
apply_individual_button = ttk.Button(
    individual_buttons, text="Apply to Icons", command=apply_individual, bootstyle="success"
)
apply_individual_button.pack(side="left", padx=(0, 6))
restore_selected_button = ttk.Button(
    individual_buttons, text="Restore Icons", command=restore_selected, bootstyle="secondary"
)
restore_selected_button.pack(side="left")

status_frame = ttk.LabelFrame(content, text="STATUS", padding=(12, 8))
status_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
status_label = ttk.Label(
    status_frame, text="Ready. Changes affect supported Windows font metrics only.",
    wraplength=500, justify="left", bootstyle="secondary",
)
status_label.pack(anchor="w")

recovery_buttons = ttk.Frame(content)
recovery_buttons.grid(row=3, column=0, pady=(0, 7))
undo_button = ttk.Button(
    recovery_buttons, text="Undo Last Change", command=undo_last_change,
    bootstyle="secondary", state="disabled",
)
undo_button.pack(side="left", padx=(0, 7))
restore_all_button = ttk.Button(
    recovery_buttons, text="Restore Original Settings", command=restore_all,
    bootstyle="outline-light",
)
restore_all_button.pack(side="left")

ttk.Label(
    content,
    text="Some Windows properties and system dialogs only respond to Accessibility or display scaling.",
    wraplength=520, justify="center", bootstyle="secondary",
).grid(row=4, column=0, pady=(0, 8))

operation_controls = [
    apply_all_button, apply_individual_button, restore_selected_button, restore_all_button
]
quick_slider.configure(
    command=lambda value: sync_from_slider(quick_size, value, quick_preview)
)
individual_slider.configure(
    command=lambda value: sync_from_slider(individual_size, value, individual_preview)
)
quick_size.trace_add(
    "write", lambda *_: sync_from_spinbox(quick_size, quick_slider, quick_preview)
)
individual_size.trace_add(
    "write", lambda *_: sync_from_spinbox(
        individual_size, individual_slider, individual_preview
    )
)
selected_font.trace_add("write", lambda *_: refresh_current_value(clear_status=True))

refresh_current_value()
try:
    app.iconbitmap(resource_path("icon.ico"))
except (OSError, tk.TclError):
    pass  # A missing development icon must not prevent the app from opening.

app.mainloop()
