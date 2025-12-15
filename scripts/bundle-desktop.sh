#!/bin/bash
# Bundle the KJV Study Python application for desktop distribution
# This script creates a standalone executable using PyInstaller

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/sidecar"

echo "=== KJV Study Desktop Bundler ==="
echo "Project directory: $PROJECT_DIR"
echo "Output directory: $OUTPUT_DIR"

cd "$PROJECT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Install desktop dependencies (without weasyprint)
echo ""
echo "=== Installing desktop dependencies ==="
pip install pyinstaller
pip install "fastapi[standard]>=0.115.12" "ged4py>=0.5.2" "mistune>=3.0.2" "parse>=1.20.2" "python-gedcom>=1.0.0"

# Create PyInstaller spec file
echo ""
echo "=== Creating PyInstaller spec ==="
cat > "$PROJECT_DIR/kjvstudy-server.spec" << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all kjvstudy_org submodules
hiddenimports = collect_submodules('kjvstudy_org')
hiddenimports += collect_submodules('fastapi')
hiddenimports += collect_submodules('starlette')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += ['kjvstudy_org.server', 'kjvstudy_org.desktop']

# Collect data files
datas = [
    ('kjvstudy_org/templates', 'kjvstudy_org/templates'),
    ('kjvstudy_org/static', 'kjvstudy_org/static'),
    ('data', 'data'),
]

a = Analysis(
    ['kjvstudy_org/desktop.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['weasyprint', 'cairo', 'gi'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='kjvstudy-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOF

# Run PyInstaller
echo ""
echo "=== Running PyInstaller ==="
pyinstaller --clean --noconfirm kjvstudy-server.spec

# Move output to sidecar directory
echo ""
echo "=== Moving output to sidecar directory ==="
cp -f "dist/kjvstudy-server" "$OUTPUT_DIR/"

echo ""
echo "=== Bundle complete! ==="
echo "Executable: $OUTPUT_DIR/kjvstudy-server"
echo ""
echo "Next steps:"
echo "  1. cd src-tauri"
echo "  2. cargo tauri build"
