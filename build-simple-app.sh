#!/bin/bash

# Ultra-simple build script for MarkLex.app - focus on working, not fancy

set -e

echo "🔨 Building Simple MarkLex.app"
echo "============================="

# Clean everything
echo "🧹 Cleaning..."
rm -rf build/ dist/ venv/ *.spec

# Create fresh virtual environment
echo "📦 Setting up clean environment..."
python3 -m venv venv
source venv/bin/activate

# Install only what we need
echo "📥 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Create minimal spec file
echo "📝 Creating minimal spec..."
cat > MarkLex-Simple.spec << 'EOF'
# Minimal working spec for MarkLex
import sys
import os

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('src', 'src'), ('assets', 'assets')],
    hiddenimports=['src.main_window', 'src.widgets.welcome_widget', 'src.widgets.setup_widget', 'src.widgets.lexicon_widget', 'src.widgets.analysis_widget', 'src.models.embedding_manager', 'src.models.text_processor', 'src.models.lexicon_manager', 'src.utils.app_dirs', 'src.styles.modern_style'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

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
    icon='assets/MarkLex-icon.icns'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='MarkLex'
)

app = BUNDLE(
    coll,
    name='MarkLex.app',
    icon='assets/MarkLex-icon.icns',
    bundle_identifier='com.marklex.desktop',
)
EOF

# Build
echo "🏗️  Building app..."
pyinstaller MarkLex-Simple.spec --clean

# Check build
if [ ! -d "dist/MarkLex.app" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Remove all quarantine and security attributes
echo "🔓 Removing quarantine attributes..."
sudo xattr -rd com.apple.quarantine dist/MarkLex.app 2>/dev/null || true
xattr -cr dist/MarkLex.app
find dist/MarkLex.app -type f -exec chmod +x {} \; 2>/dev/null || true
chmod -R 755 dist/MarkLex.app

# Test launch
echo "🧪 Testing app..."
dist/MarkLex.app/Contents/MacOS/MarkLex &
APP_PID=$!
sleep 2

if ps -p $APP_PID > /dev/null; then
    echo "✅ App launched successfully!"
    kill $APP_PID
else
    echo "❌ App failed to launch"
fi

echo ""
echo "🎉 MarkLex.app created at: dist/MarkLex.app"
echo "📏 Size: $(du -sh dist/MarkLex.app | cut -f1)"
echo ""
echo "🚀 To run: open dist/MarkLex.app"
echo "   Or double-click dist/MarkLex.app in Finder"