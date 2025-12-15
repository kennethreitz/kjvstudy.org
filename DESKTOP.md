# KJV Study Desktop App

A fully offline desktop application for studying the King James Bible, built with [Tauri](https://tauri.app/).

## Features

Everything from kjvstudy.org, completely offline:

- **Complete KJV Bible** - All 31,102 verses from the 1769 Cambridge edition
- **Verse Commentary** - In-depth theological analysis for 12,321+ verses
- **Interlinear Bible** - Hebrew (OT) and Greek (NT) word-by-word analysis
- **Strong's Concordance** - 14,298 Hebrew and Greek word definitions
- **Cross-References** - Treasury of Scripture Knowledge
- **Study Resources** - 36 study guides, 38 topics, 12 reading plans
- **Family Trees** - 429+ biblical figures with genealogies
- **Full-Text Search** - Fast SQLite FTS5 search across all verses
- **Dark Mode** - System-aware theme switching
- **Accessibility** - Full keyboard navigation, screen reader support

**Note:** PDF export is not available in the desktop version (WeasyPrint system dependencies are not bundled).

## Requirements

### For Development
- macOS 10.15+ (Catalina or later)
- Rust (install via [rustup](https://rustup.rs/))
- Python 3.11+ with uv package manager
- Xcode Command Line Tools

### For Users
- macOS 10.15+ (Catalina or later)
- ~200MB disk space

## First-Time Setup

```bash
# 1. Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# 2. Install Tauri CLI
cargo install tauri-cli

# 3. Verify installations
cargo --version      # Should show cargo 1.x.x
cargo tauri --version # Should show tauri-cli 2.x.x
```

## Quick Start (Development)

```bash
# 1. Start the Python server (in one terminal)
make -f Makefile.desktop dev

# 2. Run Tauri in dev mode (in another terminal)
make -f Makefile.desktop dev-tauri
```

## Building for Distribution

```bash
# Full build (bundle Python + build Tauri app)
make -f Makefile.desktop build

# Or step by step:
make -f Makefile.desktop bundle-python  # Create Python executable
make -f Makefile.desktop build-tauri    # Build macOS app
```

The app bundle will be in `src-tauri/target/release/bundle/`.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Tauri Shell                     │
│  ┌───────────────────────────────────────────┐  │
│  │           Native WebKit WebView            │  │
│  │                                            │  │
│  │    ┌──────────────────────────────────┐   │  │
│  │    │     http://127.0.0.1:31102       │   │  │
│  │    │                                  │   │  │
│  │    │   KJV Study Web Interface        │   │  │
│  │    │   (Jinja2 templates + Tufte CSS) │   │  │
│  │    │                                  │   │  │
│  │    └──────────────────────────────────┘   │  │
│  │                    │                       │  │
│  └────────────────────│───────────────────────┘  │
│                       │                          │
│  ┌────────────────────▼───────────────────────┐  │
│  │         FastAPI Server (Sidecar)           │  │
│  │                                            │  │
│  │  • Bible data (JSON)      • Search (SQLite)│  │
│  │  • Commentary             • Cross-refs     │  │
│  │  • Interlinear            • Strong's       │  │
│  │  • Study guides           • Reading plans  │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**How it works:**

1. Tauri app launches and spawns the Python/FastAPI server as a sidecar process
2. Server runs on `127.0.0.1:31102` (port = number of KJV verses)
3. WebView navigates to the local server
4. All data is served from bundled JSON/SQLite files
5. On quit, Tauri terminates the sidecar process

## Port Selection

The app uses port **31102** - the exact number of verses in the King James Bible. This avoids conflicts with common development ports (3000, 5000, 8000, 8080).

## Directory Structure

```
kjvstudy.org/
├── src-tauri/           # Tauri application
│   ├── Cargo.toml       # Rust dependencies
│   ├── tauri.conf.json  # Tauri configuration
│   ├── src/
│   │   └── main.rs      # Sidecar launcher
│   └── icons/           # App icons
├── sidecar/             # Bundled Python executable (after build)
├── kjvstudy_org/        # Python application
│   ├── server.py        # FastAPI app
│   ├── desktop.py       # Desktop entry point
│   ├── templates/       # Jinja2 templates
│   └── static/          # CSS, JS, fonts
├── data/                # Bible data (JSON)
├── Makefile.desktop     # Build commands
├── pyproject-desktop.toml  # Desktop dependencies (no WeasyPrint)
└── DESKTOP.md           # This file
```

## Troubleshooting

### Server won't start
Check if port 31102 is already in use:
```bash
lsof -i :31102
```

### App shows blank screen
The server may not be ready. Check Console.app for logs, or run in dev mode to see output.

### Icons not showing
Regenerate icons:
```bash
make -f Makefile.desktop icons
```

## License

MIT License - See LICENSE file for details.
