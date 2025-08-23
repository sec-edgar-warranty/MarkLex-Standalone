#!/bin/bash

# Local build script for MarkLex Desktop with proper dependency inclusion
# This builds only for macOS but ensures all dependencies are properly bundled

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔨 MarkLex Local Builder (macOS)${NC}"
echo "================================"

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1-2)
echo -e "${YELLOW}Python: $python_version${NC}"

if [[ "$python_version" < "3.8" ]]; then
    echo -e "${RED}❌ Error: Python 3.8 or higher is required${NC}"
    exit 1
fi

# Create and activate virtual environment
echo -e "${YELLOW}📦 Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    rm -rf venv
fi
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install requirements
echo -e "${YELLOW}⬆️  Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Verify all packages are installed
echo -e "${YELLOW}🔍 Verifying installed packages...${NC}"
pip list | grep -E "(pandas|numpy|gensim|nltk|scikit-learn|PyQt6)"

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build/ dist/

# Create enhanced spec file for better dependency inclusion
echo -e "${YELLOW}📝 Creating enhanced build specification...${NC}"
cat > MarkLex-Enhanced.spec << 'EOF'
# -*- mode: python ; coding: utf-8 -*-
# Enhanced MarkLex build configuration with complete dependency inclusion

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all data files and submodules for problematic packages
datas = []
hiddenimports = []

# Add our own modules
hiddenimports.extend([
    'src.main_window',
    'src.widgets.welcome_widget', 
    'src.widgets.setup_widget',
    'src.widgets.lexicon_widget',
    'src.widgets.analysis_widget',
    'src.models.embedding_manager',
    'src.models.text_processor',
    'src.models.lexicon_manager',
    'src.utils.app_dirs',
    'src.styles.modern_style',
])

# Pandas and numpy dependencies
hiddenimports.extend([
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.np_datetime',
    'pandas._libs.tslibs.nattype',
    'pandas._libs.skiplist',
    'pandas.io.formats.format',
    'numpy.core._methods',
    'numpy.lib.format',
])

# Scikit-learn dependencies
try:
    sklearn_modules = collect_submodules('sklearn')
    hiddenimports.extend(sklearn_modules)
except:
    hiddenimports.extend(['sklearn.utils._cython_blas', 'sklearn.neighbors._typedefs'])

# NLTK data
try:
    nltk_data = collect_data_files('nltk')
    datas.extend(nltk_data)
except:
    pass

# Gensim dependencies
hiddenimports.extend([
    'gensim.models.word2vec',
    'gensim.models.keyedvectors',
    'gensim.similarities.docsim',
])

# PyQt6 dependencies
hiddenimports.extend([
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.sip'
])

# Add source files
datas.append(('src', 'src'))

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MarkLex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
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
    upx=True,
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
        'LSBackgroundOnly': False,
    }
)
EOF

# Build the application
echo -e "${YELLOW}🏗️  Building MarkLex with enhanced dependency inclusion...${NC}"
pyinstaller MarkLex-Enhanced.spec --clean

# Check build results
if [ -d "dist/MarkLex.app" ]; then
    echo -e "${GREEN}✅ Build completed successfully!${NC}"
    
    # Show build size
    build_size=$(du -sh dist/MarkLex.app | cut -f1)
    echo -e "${BLUE}📏 Build size: $build_size${NC}"
    
    echo -e "${BLUE}📦 Build contents:${NC}"
    ls -la dist/
    
    echo
    echo -e "${GREEN}🎉 MarkLex Desktop build complete!${NC}"
    echo -e "${YELLOW}📋 Next steps:${NC}"
    echo "1. Test the application: open dist/MarkLex.app"
    echo "2. Check dependencies: otool -L dist/MarkLex.app/Contents/MacOS/MarkLex"
    echo "3. For cross-platform builds, install Docker and use ./build-cross-platform.sh"
    echo "4. To upload to GitHub: ./upload-releases.sh"
    
else
    echo -e "${RED}❌ Build failed! Check the output above for errors.${NC}"
    exit 1
fi