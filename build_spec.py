# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller build specification for MarkLex Desktop
Handles cross-platform standalone executable creation
"""

import os
import sys
import platform
from pathlib import Path

# Application info
APP_NAME = "MarkLex"
APP_VERSION = "1.0.0"
APP_AUTHOR = "MarkLex"

# Determine platform-specific settings
SYSTEM = platform.system().lower()
if SYSTEM == "darwin":
    ICON_FILE = "assets/icon.icns" if Path("assets/icon.icns").exists() else None
    BUNDLE_IDENTIFIER = "com.marklex.desktop"
elif SYSTEM == "windows":
    ICON_FILE = "assets/icon.ico" if Path("assets/icon.ico").exists() else None
else:  # Linux
    ICON_FILE = "assets/icon.png" if Path("assets/icon.png").exists() else None

# PyInstaller configuration
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        # Include any data files if needed
        # ('src/data', 'data'),
    ],
    hiddenimports=[
        # Core PyQt6 modules
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        
        # Scientific computing
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        
        # ML and NLP
        'gensim',
        'gensim.models',
        'nltk',
        'nltk.corpus',
        'nltk.tokenize',
        
        # Network and utilities
        'requests',
        'urllib3',
        'tqdm',
        'openpyxl',
        'git',
        
        # Platform specific
        'platform',
        'pathlib',
        'tempfile',
        'shutil',
        'zipfile',
        
        # Threading
        'threading',
        'queue',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'IPython',
        'jupyter',
        'notebook',
        'pytest',
        'test',
        'tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable configuration
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_FILE,
)

# Collect all files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)

# macOS App Bundle
if SYSTEM == "darwin":
    app = BUNDLE(
        coll,
        name=f'{APP_NAME}.app',
        icon=ICON_FILE,
        bundle_identifier=BUNDLE_IDENTIFIER,
        info_plist={
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': 'MarkLex - Marketing Lexicon Creation',
            'CFBundleGetInfoString': f'{APP_NAME} {APP_VERSION}',
            'CFBundleVersion': APP_VERSION,
            'CFBundleShortVersionString': APP_VERSION,
            'NSHighResolutionCapable': True,
            'NSRequiresAquaSystemAppearance': False,
            'LSMinimumSystemVersion': '10.13.0',
            'NSHumanReadableCopyright': f'Copyright © 2024 {APP_AUTHOR}. All rights reserved.',
            'NSAppTransportSecurity': {
                'NSAllowsArbitraryLoads': True,  # Required for GitHub downloads
            },
            'NSNetworkVolumesUsageDescription': 'MarkLex needs network access to download embedding models.',
            'NSDesktopFolderUsageDescription': 'MarkLex may save exported data to your desktop.',
            'NSDocumentsFolderUsageDescription': 'MarkLex may save exported data to your documents folder.',
            'NSDownloadsFolderUsageDescription': 'MarkLex may save exported data to your downloads folder.',
        },
    )