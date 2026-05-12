# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('C:\\Users\\ellio\\anaconda3\\Lib\\site-packages\\ci_info\\vendors.json', 'ci_info')]
datas += collect_data_files('bidsschematools')
datas += collect_data_files('etelemetry')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('C:\\Users\\ellio\\anaconda3\\envs\\BIDS_and_coreg\\Library\\bin\\dcm2niix.exe', '.')],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['.\\pyi_fix_stdio.py'],
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
    name='Bids_and_coreg',
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
    icon=['Prel_BIDS_icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Bids_and_coreg',
)
