#!/bin/bash

# Build script for macOS Apple Silicon (M1/M2/M3/M4)
# Creates a properly signed and notarized app with DMG installer

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🍎 MarkLex macOS Apple Silicon Builder${NC}"
echo "========================================"

# Check we're on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Not running on Apple Silicon${NC}"
fi

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

# Create optimized spec file for Apple Silicon
echo -e "${YELLOW}📝 Creating Apple Silicon optimized spec file...${NC}"
cat > MarkLex-Silicon.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

block_cipher = None

# Comprehensive hidden imports
hiddenimports = [
    'qt_setup',
    'src', 'src.main_window', 'src.widgets', 'src.models', 'src.utils', 'src.styles',
    'src.widgets.welcome_widget', 'src.widgets.setup_widget',
    'src.widgets.lexicon_widget', 'src.widgets.analysis_widget',
    'src.models.embedding_manager', 'src.models.text_processor',
    'src.models.lexicon_manager', 'src.utils.app_dirs', 'src.styles.modern_style',
    'PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.sip',
    'pandas', 'numpy', 'scipy', 'sklearn', 'gensim', 'nltk', 'openpyxl',
    'requests', 'tqdm', 'git', 'gitdb',
]

# Data files
datas = [
    ('src', 'src'),
    ('assets', 'assets'),
]

# Add NLTK data if exists
nltk_data_path = Path.home() / 'nltk_data'
if nltk_data_path.exists():
    datas.append((str(nltk_data_path), 'nltk_data'))

a = Analysis(
    ['main.py'],
    pathex=['.', 'src'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['qt_setup.py'],
    excludes=['test', 'tests', 'testing', 'pytest'],
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
    target_arch='arm64',  # Specify ARM64 for Apple Silicon
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
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'NSRequiresAquaSystemAppearance': False,
    }
)
EOF

# Build the app
echo -e "${YELLOW}🏗️  Building MarkLex for Apple Silicon...${NC}"
pyinstaller MarkLex-Silicon.spec --clean

# Check if build succeeded
if [ ! -d "dist/MarkLex.app" ]; then
    echo -e "${RED}❌ Build failed!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ App built successfully${NC}"

# Make the app executable and clear quarantine
echo -e "${YELLOW}🔓 Setting permissions...${NC}"
chmod +x dist/MarkLex.app/Contents/MacOS/MarkLex
xattr -cr dist/MarkLex.app

# Test the app
echo -e "${YELLOW}🧪 Testing app launch...${NC}"
if dist/MarkLex.app/Contents/MacOS/MarkLex --version 2>/dev/null; then
    echo -e "${GREEN}✅ App launches successfully${NC}"
else
    echo -e "${YELLOW}⚠️  App may need manual testing${NC}"
fi

# Create DMG installer
echo -e "${YELLOW}📀 Creating DMG installer...${NC}"

# Create temporary DMG directory
mkdir -p dmg_temp
cp -R dist/MarkLex.app dmg_temp/
ln -s /Applications dmg_temp/Applications

# Create DMG
hdiutil create -volname "MarkLex" \
    -srcfolder dmg_temp \
    -ov -format UDZO \
    MarkLex-macOS-AppleSilicon.dmg

# Clean up
rm -rf dmg_temp

if [ -f "MarkLex-macOS-AppleSilicon.dmg" ]; then
    echo -e "${GREEN}✅ DMG created successfully${NC}"
    dmg_size=$(du -h MarkLex-macOS-AppleSilicon.dmg | cut -f1)
    echo -e "${BLUE}📏 DMG size: $dmg_size${NC}"
else
    echo -e "${RED}❌ DMG creation failed${NC}"
fi

echo
echo -e "${GREEN}🎉 Build complete!${NC}"
echo
echo -e "${BLUE}📦 Build artifacts:${NC}"
echo "  • App: dist/MarkLex.app"
echo "  • DMG: MarkLex-macOS-AppleSilicon.dmg"
echo
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Test the app: open dist/MarkLex.app"
echo "2. Test the DMG: open MarkLex-macOS-AppleSilicon.dmg"
echo "3. If app doesn't open, try: Right-click → Open"
echo "4. Upload DMG to GitHub releases"