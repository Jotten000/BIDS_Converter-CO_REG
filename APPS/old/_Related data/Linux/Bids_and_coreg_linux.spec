# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all

datas = [('/home/jotten/miniconda3/envs/BIDS_and_coreg_linux/lib/python3.11/site-packages/ci_info/vendors.json', 'ci_info')]
binaries = [('/home/jotten/miniconda3/envs/BIDS_and_coreg_linux/bin/dcm2niix', '.'), ('/home/jotten/miniconda3/envs/BIDS_and_coreg_linux/lib/libexpat.so.1', '.')]
hiddenimports = []
datas += collect_data_files('bidsschematools')
datas += collect_data_files('etelemetry')
tmp_ret = collect_all('openpyxl')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['./pyi_fix_stdio.py'],
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
    name='Bids_and_coreg_linux',
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
    name='Bids_and_coreg_linux',
)
