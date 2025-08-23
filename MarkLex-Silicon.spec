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
