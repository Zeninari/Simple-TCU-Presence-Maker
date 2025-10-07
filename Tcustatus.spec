# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['TcuStatus.py'],
    pathex=[],
    binaries=[],
    datas=[('Tesseract-OCR', 'Tesseract-OCR')],
    hiddenimports=['_overlapped', 'asyncio.windows_events','_asyncio', '_tkinter'],
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
    a.datas,
    [],
    name='TcuStatus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['TheCrewUnlimited.ico'],
)
