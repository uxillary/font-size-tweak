# Font Size Tweak — Project Context

## Project overview

**Font Size Tweak** is a lightweight, open-source Windows utility for changing supported Windows UI font sizes **without increasing overall display scaling**.

The project started because some Windows text — especially File Explorer/sidebar text and other system UI text — was difficult to read, while increasing Windows scaling made everything else too large.

The goal is to keep the app:

- free
- lightweight
- accessible
- portable
- open source
- easy to download from GitHub
- simple enough to understand and maintain
- useful as an alternative to tools such as Advanced System Font Changer

Repository:

`https://github.com/uxillary/font-size-tweak`

GitHub Pages:

`https://uxillary.github.io/font-size-tweak/`

Latest release:

`https://github.com/uxillary/font-size-tweak/releases/latest`

Support:

`https://coff.ee/admjski`

---

# Why the app exists

Windows provides:

- Display scaling
- Accessibility → Text size
- App-specific zoom

But increasing Windows scaling can also enlarge:

- icons
- toolbars
- buttons
- panels
- entire application interfaces

Font Size Tweak instead focuses on supported Windows system font metrics, allowing text to be enlarged without deliberately scaling the rest of the desktop UI.

---

# Core Windows registry approach

The app modifies font metrics stored under:

`HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics`

The supported registry values are:

- `CaptionFont`
- `MenuFont`
- `MessageFont`
- `IconFont`
- `StatusFont`

Approximate mapping:

| App label | Registry value | Typical use |
| --- | --- | --- |
| Title Bar | `CaptionFont` | Window title text |
| Menus | `MenuFont` | Classic menus/context menus |
| Message Boxes | `MessageFont` | Some classic dialog/message UI |
| Icons | `IconFont` | Desktop/File Explorer labels and related shell text |
| Status Bar | `StatusFont` | Status text in compatible legacy UI |

Windows contains a mixture of classic Win32 and newer UI/rendering systems, so not every visible piece of Windows text responds to these settings.

Do not make guarantees about unsupported Windows components.

---

# Important technical discovery

The project originally attempted to manually build the Windows `LOGFONT` binary structure using `struct.pack()`.

This caused repeated packing/structure errors.

The more reliable solution was to preserve the existing registry data and change only the font-height field.

The current approach is:

1. Read the existing `REG_BINARY` value.
2. Convert it to a `bytearray`.
3. Preserve all existing font/style information.
4. Replace only the first four bytes representing `lfHeight`.
5. Write the modified binary back.

Example:

```python
value, regtype = winreg.QueryValueEx(key, font_key_name)

font_bytes = bytearray(value)

font_bytes[0:4] = struct.pack("<l", height)

winreg.SetValueEx(
    key,
    font_key_name,
    0,
    winreg.REG_BINARY,
    bytes(font_bytes)
)
