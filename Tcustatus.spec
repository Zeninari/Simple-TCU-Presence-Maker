# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

# ---------------- Collect Tesseract-OCR files (exclude tessdata) ----------------
tess_exe_folder = 'Tesseract-OCR'
datas_to_include = []

for root, dirs, files in os.walk(tess_exe_folder):
    if 'tessdata' in dirs:
        dirs.remove('tessdata')  # skip tessdata folder
    for f in files:
        full_path = os.path.join(root, f)
        # Relative path in the bundle
        relative_path = os.path.relpath(root, tess_exe_folder)
        target_path = os.path.join('Tesseract-OCR', relative_path)
        datas_to_include.append((full_path, target_path))

# ---------------- Hidden imports ----------------
hidden_imports = [
    '_overlapped',
    'asyncio.windows_events',
    '_asyncio',
    '_tkinter',
]

# ---------------- Analysis ----------------
a = Analysis(
    ['TcuStatus.py'],
    pathex=[],
    binaries=[],
    datas=datas_to_include,
    hiddenimports=hidden_imports,
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
    icon='TheCrewUnlimited.ico'
)
