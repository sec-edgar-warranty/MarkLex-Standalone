# -*- mode: python ; coding: utf-8 -*-


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
    [],
    exclude_binaries=True,
    name='MarkLex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MarkLex',
)
app = BUNDLE(
    coll,
    name='MarkLex.app',
    icon='assets/MarkLex-icon.icns',
    bundle_identifier='com.marklex.desktop',
)
