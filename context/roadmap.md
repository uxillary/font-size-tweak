# Font Size Tweak — Development Roadmap

## Project direction

Font Size Tweak should grow from a simple Windows font-size utility into a polished, free and open-source alternative to tools such as:

- System Font Size Changer
- Advanced System Font Changer

The goal is **not** to copy those applications directly.

The goal is to provide the same important capabilities, then improve on them through:

- better UX
- safer restore/backup behaviour
- clearer explanations
- modern styling
- open-source transparency
- accessibility
- useful presets
- profiles
- simpler operation
- no artificial feature/paywall restrictions

The app should remain lightweight and focused.

---

# Core product promise

**Make supported Windows UI fonts easier to read without making the entire Windows interface huge.**

The app should remain useful for people searching for problems such as:

- File Explorer text too small
- Windows 11 text too small
- Windows scaling makes everything too large
- make Windows text larger without changing display scaling
- increase Windows menu font size
- change Windows icon font size
- change Windows system font
- Advanced System Font Changer alternative

---

# Current supported font metrics

Font Size Tweak currently works with:

- CaptionFont
- MenuFont
- MessageFont
- IconFont
- StatusFont

These are stored under:

`HKEY_CURRENT_USER\Control Panel\Desktop\WindowMetrics`

The application preserves the existing raw `REG_BINARY` font structure and only modifies the relevant height field when changing font size.

This safe approach should remain the basis of future development.

---

# Current strengths

Font Size Tweak already has several advantages worth preserving.

## Free and open source

The application is:

- free
- MIT licensed
- available on GitHub
- inspectable by users
- modifiable/forkable

There should be no artificial premium tier for basic functionality.

---

## Lightweight

The app currently uses:

- Python
- tkinter
- ttkbootstrap
- Windows registry APIs

Avoid unnecessary frameworks or background components.

Do not introduce:

- Electron
- background services
- telemetry
- user accounts
- subscription systems

---

## Safe registry editing

Instead of reconstructing Windows font structures from scratch, the application preserves the existing binary value and modifies only the font height.

Keep this behaviour.

---

## Original-settings backup

The v1.1 direction includes persistent backup of the original raw font registry values.

This allows the application to restore the user's actual settings rather than pretending a hard-coded 9pt size is always the Windows default.

This should remain a key trust/safety feature.

---

## Current vs proposed values

The application can show something such as:

`Current: 9 pt`

`New: 11 pt`

This is clearer than blindly applying changes.

Future features should follow the same principle:

**Show users what exists now and what will change before writing it.**

---

## Undo

The application includes one-level undo for recent operations.

Future versions may expand this into a proper history system.

---

# Version roadmap

---

# v1.1 — Safety, reliability and UX foundation

## Status

Current development focus.

## Goal

Turn the existing utility into a polished, safe and trustworthy application before expanding its feature set.

## Features

### Persistent original-settings backup

Store the original raw registry values before the first modification.

Suggested location:

`%APPDATA%\FontSizeTweak\original-settings.json`

Backup should include:

- CaptionFont
- MenuFont
- MessageFont
- IconFont
- StatusFont

Use the complete binary values.

Do not overwrite the original backup on every launch.

---

### Restore selected font

Allow users to restore only the currently selected font metric.

Examples:

- Restore Icons
- Restore Menus
- Restore Title Bar

Restore the actual backed-up original binary value.

---

### Restore all original settings

Restore all supported registry values to the original backed-up values.

Require confirmation before performing the operation.

---

### Undo last change

Maintain a one-level undo snapshot.

Examples:

- Apply Icons → Undo restores the previous IconFont value.
- Apply to All → Undo restores all five pre-operation values.
- Restore operation → Undo can restore the state immediately before the restore.

---

### Exact numeric input

Keep sliders but add synchronized numeric controls.

Supported size range should remain sensible, approximately:

`8–16 pt`

Users should be able to select exact values without fighting a slider.

---

### Current / proposed values

Display:

`Current: X pt`

`New: Y pt`

Indicate when the new value has not yet been applied.

Disable or de-emphasize Apply when there is no actual change.

---

### Status panel

Use a persistent status area instead of confusing transient messages.

Example states:

- Ready
- Changes saved
- Restore completed
- Undo completed
- Partial failure
- Registry read/write error

---

### Better registry reliability

Remove broad:

`except:`

blocks.

Use:

- specific exception handling
- context managers
- registry-value validation
- clear partial-failure reporting

Never show full success if only some font values were updated.

---

### Compact UI

Keep the newer compact layout.

Avoid excessive empty vertical space.

Maintain readable text because this is itself an accessibility utility.

---

### Better contrast

Ensure:

- descriptions
- subtitle
- status text
- current/new values
- footer notes

remain readable on the dark theme.

Nothing active should look disabled unintentionally.

---

### Footer limitation wording

Use factual wording such as:

`Some Windows interfaces use different rendering systems and may not respond to these font metrics.`

Do not claim every unsupported dialog can be fixed through Accessibility settings.

---

# v1.2 — Font appearance controls

## Goal

Close the biggest functional gap between Font Size Tweak and established Windows font-changing utilities.

Add more than just font-size control.

---

## Font family selection

Allow users to choose the actual Windows font family used for supported UI elements.

Examples:

- Segoe UI
- Arial
- Tahoma
- Verdana
- other installed fonts

Use installed Windows fonts rather than shipping font files.

The selected font family should be applied individually to supported font metrics.

---

## Bold control

Add a toggle for font weight.

Example:

`Bold: On / Off`

Support individual UI categories where Windows respects the setting.

---

## Italic control

Add an optional italic toggle where supported.

Keep this secondary because most users will not need it.

---

## Preserve existing LOGFONT data safely

When changing font family/style:

- modify only relevant fields
- preserve unrelated binary structure
- validate before writing

Do not blindly reconstruct unknown font structures if a safer patching method is available.

---

## Expand supported font categories

Investigate adding:

- Tooltip font
- Palette title font

Only include metrics that still behave meaningfully on supported Windows versions.

Do not add registry values purely because older utilities expose them.

Verify actual Windows behaviour first.

---

## Better individual preview

Expand the preview to reflect:

- selected font family
- size
- bold
- italic

Preview should update before applying.

---

# v1.3 — Profiles and presets

## Goal

Make the utility much more convenient than older alternatives.

---

## User profiles

Allow users to save complete font configurations.

A profile may include:

- font sizes
- font families
- bold state
- italic state
- relevant supported metrics

Examples:

`My Default`

`Laptop`

`Large Monitor`

`TV`

`Accessibility`

---

## Profile actions

Support:

- Save profile
- Load profile
- Rename profile
- Delete profile
- Duplicate profile

---

## Built-in presets

Provide useful built-in configurations.

Potential presets:

### Default / Original

Restore original backed-up settings.

### Comfortable

Slightly larger fonts without aggressive changes.

### Large

Useful for high-resolution displays.

### High Readability

Larger fonts with a readable font family/weight.

### Compact

Smaller supported fonts for users who prefer more screen space.

Built-in presets should be optional and reversible.

---

## Profile preview

Before applying a profile, show a summary of what will change.

Example:

```text
Icons
9 pt → 12 pt
Segoe UI → Segoe UI
Regular → Bold

Menus
9 pt → 11 pt
