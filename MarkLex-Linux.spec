# -*- mode: python ; coding: utf-8 -*-
# Linux build configuration for MarkLex Desktop

a = Analysis(
    ['main.py'],
    pathex=['src'],
    binaries=[],
    datas=[('src', 'src')],
    hiddenimports=[
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
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
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