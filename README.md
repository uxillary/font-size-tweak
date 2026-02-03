# Font Size Tweak

[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE) [![GitHub release](https://img.shields.io/github/v/release/uxillary/font-size-tweak?sort=semver)](https://github.com/uxillary/font-size-tweak/releases/latest) [![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen)](https://uxillary.github.io/font-size-tweak/)


Font Size Tweak is a free, portable Windows 11/10 utility that lets you change Windows system font size without scaling. Adjust title bar, menus, icons, message boxes, and status bar text independently while keeping everything crisp.

## Features

- Change Windows system font size per element or all at once
- Live preview before committing registry values
- Dark mode interface with manual override
- Portable executable (no installation or admin rights required)
- One-click reset to Microsoft defaults
- Open-source MIT licence and free forever

## How it works

Font Size Tweak updates the registry keys under `HKCU\Control Panel\Desktop\WindowMetrics`, matching the same locations Windows uses internally. The app is transparent about every value and does not ship with telemetry or background services.

## Download

Get the latest release from GitHub and verify the checksum provided in the notes:

- 👉 [Download Font Size Tweak (latest)](https://github.com/uxillary/font-size-tweak/releases/latest)

No installer is required; simply run the executable.

## Privacy &amp; safety

- 100% offline, no network calls, and no cookies.
- Source code is open for review.
- Reset option restores Windows defaults instantly.

## Troubleshooting

- Some apps cache metrics, so sign out and back in after big adjustments.
- If fonts look wrong, use the reset control or restore a registry backup.

## Support

- Report issues or request features via [GitHub Issues](https://github.com/uxillary/font-size-tweak/issues).
- Sponsor development on [Buy Me a Coffee](https://www.buymeacoffee.com/uxillary).
