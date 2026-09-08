# Font Size Tweak — Project Context

## Product

Font Size Tweak is a lightweight, open-source Windows 10/11 utility for changing supported Windows UI font sizes without increasing overall display scaling. It exists for cases where particular interface text is uncomfortable to read but broader Windows scaling makes controls, spacing and whole applications too large.

The project should remain free, accessible, portable, understandable and focused. It uses Python, tkinter, ttkbootstrap and Windows registry APIs; it should not gain telemetry, accounts, a background service or a heavyweight application framework.

## Current release

Version **1.1.0** is the current documented release. It provides:

- a shared Quick Adjustment for all supported metrics;
- individual 8–16 pt controls with current/proposed values and sample previews;
- persistent capture and restore of the user's original raw settings;
- one-level, session-only undo;
- validation, operation status and partial-failure reporting; and
- a compact dark interface.

The current application screenshot is [`docs/assets/screenshot1.png`](../docs/assets/screenshot1.png). Documentation should link that file rather than the older `assets/screenshot.png` or `docs/v1screenshot.png` images.

## Registry implementation

The app works with `HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics`:

| App label | Registry value | Typical use |
| --- | --- | --- |
| Title Bar | `CaptionFont` | Classic window title text |
| Menus | `MenuFont` | Classic menus and context menus |
| Message Boxes | `MessageFont` | Some classic dialogs and prompts |
| Icons | `IconFont` | Desktop and supported Explorer labels |
| Status Bar | `StatusFont` | Status text in compatible legacy UI |

The reliable implementation is to read and validate each existing `REG_BINARY` value, preserve its font/style data and replace only the first four bytes containing `lfHeight`. Do not reconstruct a complete `LOGFONT` structure merely to change its size.

Original values are captured before the first write and stored at `%APPDATA%\FontSizeTweak\original-settings.json`. The backup must contain all five complete values, must not be overwritten on subsequent launches and must remain the source for restore operations. Undo is intentionally one level and in memory, so documentation must not imply that it persists between launches.

## Accuracy rules

- Describe the utility as portable, but clarify that its persistent backup lives in the user's Windows profile.
- Do not describe the sample label as a full Windows UI preview.
- Do not promise that every Explorer view, dialog or application will respond.
- Explain that newer/custom-rendered interfaces may ignore classic metrics and that a sign-out may be needed.
- Do not advertise font-family, bold, italic, preset or profile support until those features exist.
- State that administrator rights are unnecessary because settings are per user.

## Links

- Repository: <https://github.com/uxillary/font-size-tweak>
- Project website: <https://uxillary.github.io/font-size-tweak/>
- Latest release: <https://github.com/uxillary/font-size-tweak/releases/latest>
- Issues: <https://github.com/uxillary/font-size-tweak/issues>
- Support: <https://coff.ee/admjski>
