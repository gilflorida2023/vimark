[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet "Markdown Cheatsheet")

# README for vimark (Vim + Mark Integrator)

[![Python](https://img.shields.io/badge/Python-3.11.2-brightgreen?logo=python)](https://www.python.org/)
[![Watchdog](https://img.shields.io/badge/Watchdog-6.0.0-orange)](https://python-watchdog.readthedocs.io/)

`vimark` is a Python utility that launches Vim for editing a GFM Markdown file while simultaneously opening `mark` (the viewer) in the background. It uses `watchdog` for instant file watching—on save in Vim, it sends SIGHUP to refresh the viewer without polling. When Vim exits, it kills the viewer and cleans up.

## Features

- **Integrated Workflow**: Edit in **Vim** (foreground), preview live in mark GUI (background).
- **Instant Reload**: Inotify-based watching—no delay on saves.
- **Graceful Cleanup**: Vim exit → SIGKILL to mark + exit.
- **Simple CLI**: One command for the full loop.

## Installation

1. **Dependencies**: Add to `requirements.txt` (besides mark's):

   watchdog==6.0.0

Run `pip install -r requirements.txt`.
2. **Ensure `mark` & Vim**: Have `mark.py` in PATH or same dir; Vim installed.
3. **Executable**: `chmod +x vimark.py`.

## Usage

./vimark.py example.md

- Vim opens foreground for editing.
- Mark GUI launches background, rendering the file.
- Edit/save in Vim (:w) → Mark refreshes instantly.
- Exit Vim (:q or :wq) → Mark closes, vimark exits.
- Ctrl+C → Cleanup and exit.

### Example Session
1. `./vimark.py notes.md` → Vim + mark window.
2. Add `# New Header` in Vim, save → Mark updates.
3. `:wq` in Vim → Everything shuts down cleanly.

## Architecture

- **Processes**: Vim (foreground, `os.system`), mark (detached `Popen`).
- **Watching**: Watchdog on file dir—`on_modified` sends SIGHUP to mark PID.
- **Cleanup**: `os.killpg` for process group kill on exit/interrupt.
- **~50 LOC**: Lightweight, no threads needed.

## Limitations & Roadmap

- **Single File**: Watches only the passed .md; extend to dir.
- **Error Handling**: Assumes vim/mark succeed; add retries.
- **Cross-Platform**: Inotify on Linux; fallback to polling on Windows.

MIT License. PRs welcome for multi-file or VSCode integration!

Github's own document describing **Github Flavored Markdown (GFM)** 


# README for mark (Markdown Viewer)
![Python](https://img.shields.io/badge/Python-3.11.2-brightgreen?logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-6.9.0-blue)
### **mark** is a lightweight Python GUI viewer for GitHub Flavored Markdown (GFM) files, using the markdown library with pymdown-extensions for rich rendering (tables, syntax-highlighted code, task lists, etc.) and PyQt6's QWebEngineView for browser-like display. 

- It supports live reloading on SIGHUP and graceful exit on SIGINT (Ctrl+C).FeaturesRich GFM Rendering: Full support for tables, fenced code blocks with highlighting, blockquotes, lists, math (via arithmatex), and more.
- Live Reload: Edit the file externally and send SIGHUP to refresh instantly.
- Light Theme: Clean white background with black text for readability.
- Cross-Platform: Works on Linux (X11/Wayland), Windows, macOS via PyQt6.
- Minimal: No external browser needed—embedded WebEngine.

- InstallationPython 3.11.2+: Ensure it's installed.
- Dependencies: Create requirements.txt and run:

	pip install -r requirements.txt
### requirements.txt:
```
PyQt6==6.9.1
PyQt6-WebEngine==6.9.0
markdown==3.7
pymdown-extensions==10.7
```

System Libs (Linux): For Qt XCB plugin:

sudo apt install libxcb-cursor0 libxkbcommon-x11-0 qt6-base-dev libqt6webenginecore6

UsageRun with a Markdown file:

python mark.py example.md

Window opens with rendered content (headers, code blocks highlighted, tables gridded).
Resize/scroll—content reflows.
Reload: Edit file, then kill -HUP $(pgrep -f mark.py) → Instant refresh.
Exit: Ctrl+C in terminal → Closes window.

Example Input (example.md)markdown
```
# H1 Header
## H2 Subheader

This is **bold** and *italic* text with `inline code`.

| Col1 | Col2 |
|------|------|
| Row1 | Data |
```

