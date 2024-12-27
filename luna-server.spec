# -*- mode: python ; coding: utf-8 -*-


import os
import numpy as np

def find_shared_libs():
    # Dynamically find necessary shared libraries
    base_dir = os.path.dirname(np.__file__)
    paths = [
        os.path.join(base_dir, 'random', f) for f in os.listdir(os.path.join(base_dir, 'random')) if f.endswith('.so')
    ]
    # Add any other required shared libraries
    return [(path, '.') for path in paths]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=find_shared_libs(),  # Use the dynamic loader
    datas=[],
    hiddenimports=[],
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
    name='luna-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='luna-server',
)
