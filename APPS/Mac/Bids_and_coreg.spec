# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('/opt/anaconda3/envs/BIDS_and_coreg/lib/python3.14/site-packages/ci_info/vendors.json', 'ci_info')]
datas += collect_data_files('bidsschematools')
datas += collect_data_files('etelemetry')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('/opt/anaconda3/envs/BIDS_and_coreg/bin/dcm2niix', '.'), ('/opt/anaconda3/envs/BIDS_and_coreg/bin/deno', '.')],
    datas=datas,
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
app = BUNDLE(
    coll,
    name='Bids_and_coreg.app',
    icon='Prel_BIDS_icon.ico',
    bundle_identifier='se.ki.kex26.bidsandcoreg',
)
