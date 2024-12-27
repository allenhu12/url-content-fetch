# -*- mode: python ; coding: utf-8 -*-
import sys

a = Analysis(
    ['standalone_link_extractor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['bs4', 'requests'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data)

if sys.platform == 'darwin':  # macOS specific
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='LinkExtractor',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=True,  # Important for macOS
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    )
    
    # Create app bundle
    app = BUNDLE(
        exe,
        name='LinkExtractor.app',
        icon=None,
        bundle_identifier=None,
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False',
            'CFBundleName': 'LinkExtractor',
            'CFBundleDisplayName': 'Link Extractor',
            'CFBundleGetInfoString': "Link Extractor",
            'CFBundleIdentifier': "com.linkextractor.app",
            'CFBundleVersion': "1.0.0",
            'CFBundleShortVersionString': "1.0.0",
        }
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name='LinkExtractor',
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
    ) 