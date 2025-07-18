# 🪄 FontSize Tweak

FontSize Tweak is a tiny, open-source Windows app that lets you change system font sizes (like title bars, menus, icons, etc.) without messing with global scaling or blurry text.

> ✨ Built with Python + ttkbootstrap  
> 🎯 Target: Windows 10/11

---

## 🖼️ Features

- 🔘 Quick Apply: Change all system fonts in one click  
- ⚙️ Advanced Control: Customize each font individually (Title bar, Menu, Icon, Message box, Status bar)  
- 👀 Live preview of text before applying  
- ✅ One-click reset to default  
- 🧠 Detects current size per font  
- 🌙 Dark mode UI with accessible layout  
- 🧊 Portable `.exe` — no install needed!

---

## 📥 Download

➡ [**Download the latest release**](https://github.com/uxillary/font-size-tweak/releases/latest/download/FontSizeTweak-v1.0.zip)

Extract and run `FontSizeTweak.exe`. That’s it.

> ⚠️ Changes require you to **log out and log back in** to take full effect.

---

## 📦 How to Build (Dev)

Install the required library:

```
pip install ttkbootstrap
```

To run the app:

```
python main.py
```

To build a standalone `.exe`:

```
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

---

## 📁 Folder Contents

- `FontSizeTweak.exe` – The app (built with PyInstaller)  
- `main.py` – The source code  
- `icon.ico` – App icon  
- `LICENSE` – MIT License  
- `version.txt` – Current version info  

---

## ❓ FAQ

**💬 Does this work on Windows 11?**  
Yes, it tweaks classic system font metrics that still apply in many places.

**🧩 Why doesn’t it change Properties windows?**  
Modern dialog windows (like file Properties) use a different rendering engine. You'll need to adjust those using Windows accessibility options:  
**Settings → Accessibility → Text size**

---

## 🛠️ License

MIT – do whatever you want, just give credit.

---

## 🧠 Author

Made by [@admjski](https://github.com/uxillary)
Because squinting at 9pt fonts is not a personality trait.
