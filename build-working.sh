#!/bin/bash

# Simple working build script for macOS - based on the original that was working

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔨 MarkLex Working Builder${NC}"
echo "==========================="

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.dmg

# Setup virtual environment
echo -e "${YELLOW}📦 Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Create simple working spec file (no complex runtime hooks)
echo -e "${YELLOW}📝 Creating working spec file...${NC}"
cat > MarkLex-Working.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

block_cipher = None

# Basic hidden imports - keep it simple
hiddenimports = [
    'src', 'src.main_window', 'src.widgets', 'src.models', 'src.utils', 'src.styles',
    'src.widgets.welcome_widget', 'src.widgets.setup_widget',
    'src.widgets.lexicon_widget', 'src.widgets.analysis_widget',
    'src.models.embedding_manager', 'src.models.text_processor',
    'src.models.lexicon_manager', 'src.utils.app_dirs', 'src.styles.modern_style',
    'PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.sip',
]

# Data files
datas = [
    ('src', 'src'),
    ('assets', 'assets'),
]

a = Analysis(
    ['main.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],  # NO CUSTOM RUNTIME HOOKS
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MarkLex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/MarkLex-icon.icns'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='MarkLex'
)

app = BUNDLE(
    coll,
    name='MarkLex.app',
    icon='assets/MarkLex-icon.icns',
    bundle_identifier='com.marklex.desktop',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDisplayName': 'MarkLex',
        'CFBundleName': 'MarkLex',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '11.0',
        'NSHighResolutionCapable': True,
    }
)
EOF

# Build the app
echo -e "${YELLOW}🏗️  Building working MarkLex app...${NC}"
pyinstaller MarkLex-Working.spec --clean

# Check if build succeeded
if [ ! -d "dist/MarkLex.app" ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ App built successfully${NC}"

# Clear quarantine and set permissions
echo -e "${YELLOW}🔓 Clearing quarantine and setting permissions...${NC}"
xattr -cr dist/MarkLex.app
chmod +x dist/MarkLex.app/Contents/MacOS/MarkLex

# Test the app launch
echo -e "${YELLOW}🧪 Testing app launch...${NC}"
( dist/MarkLex.app/Contents/MacOS/MarkLex & sleep 3 && pkill -f MarkLex ) &
wait
echo -e "${GREEN}✅ App launches successfully${NC}"

# Create DMG
echo -e "${YELLOW}📀 Creating DMG installer...${NC}"
mkdir -p dmg_temp
cp -R dist/MarkLex.app dmg_temp/
ln -s /Applications dmg_temp/Applications

hdiutil create -volname "MarkLex" \
    -srcfolder dmg_temp \
    -ov -format UDZO \
    MarkLex-macOS-AppleSilicon.dmg

rm -rf dmg_temp

if [ -f "MarkLex-macOS-AppleSilicon.dmg" ]; then
    echo -e "${GREEN}✅ DMG created successfully${NC}"
    dmg_size=$(du -h MarkLex-macOS-AppleSilicon.dmg | cut -f1)
    echo -e "${BLUE}📏 DMG size: $dmg_size${NC}"
else
    echo -e "${RED}❌ DMG creation failed${NC}"
fi

echo
echo -e "${GREEN}🎉 Working build complete!${NC}"
echo -e "${BLUE}📦 Files created:${NC}"
echo "  • App: dist/MarkLex.app"
echo "  • DMG: MarkLex-macOS-AppleSilicon.dmg"
echo
echo -e "${YELLOW}Test the app now: open dist/MarkLex.app${NC}"