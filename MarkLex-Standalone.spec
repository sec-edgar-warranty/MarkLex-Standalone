# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

# Comprehensive build configuration for standalone executables
block_cipher = None

# Collect all hidden imports
hiddenimports = [
    # Our modules
    'src', 'src.main_window', 'src.widgets', 'src.models', 'src.utils', 'src.styles',
    'src.widgets.welcome_widget', 'src.widgets.setup_widget',
    'src.widgets.lexicon_widget', 'src.widgets.analysis_widget',
    'src.models.embedding_manager', 'src.models.text_processor', 
    'src.models.lexicon_manager', 'src.utils.app_dirs', 'src.styles.modern_style',
    
    # PyQt6
    'PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'PyQt6.sip',
    
    # Data science packages
    'pandas', 'pandas._libs', 'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.nattype',
    'pandas._libs.skiplist', 'pandas.io.formats.format',
    
    'numpy', 'numpy.core._methods', 'numpy.lib.format',
    'numpy.core._multiarray_umath', 'numpy.random',
    
    'scipy', 'scipy.special', 'scipy.sparse', 'scipy.linalg',
    
    'sklearn', 'sklearn.utils._cython_blas', 'sklearn.neighbors._typedefs',
    'sklearn.metrics', 'sklearn.preprocessing', 'sklearn.feature_extraction',
    
    'gensim', 'gensim.models', 'gensim.models.word2vec', 
    'gensim.models.keyedvectors', 'gensim.similarities.docsim',
    
    'nltk', 'nltk.tokenize', 'nltk.corpus', 'nltk.stem',
    
    # Other dependencies
    'openpyxl', 'requests', 'tqdm', 'git', 'gitdb'
]

# Collect data files
datas = [
    ('src', 'src'),
    ('assets', 'assets'),
]

# Add NLTK data if it exists
import nltk
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
    runtime_hooks=[],
    excludes=['test', 'tests', 'testing', 'pytest', 'pyinstaller'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Platform-specific configuration
import platform
system = platform.system()

if system == 'Darwin':  # macOS
    exe = EXE(
        pyz, a.scripts, [],
        exclude_binaries=True,
        name='MarkLex',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,  # Don't use UPX on macOS
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='assets/MarkLex-icon.icns'
    )
    
    coll = COLLECT(
        exe, a.binaries, a.zipfiles, a.datas,
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
        }
    )
    
elif system == 'Windows':
    exe = EXE(
        pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
        name='MarkLex',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='assets/MarkLex-icon.png'
    )
    
else:  # Linux
    exe = EXE(
        pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
        name='MarkLex',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
