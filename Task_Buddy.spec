# -*- mode: python ; coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import mpxj
mpxj_path = os.path.dirname(mpxj.__file__)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icons', 'icons'),
    (mpxj_path, 'mpxj')],
    hiddenimports=[
        'mpxj',
        'jpype',
        'jpype._jvm',
        'jpype._core',
        'jpype.types',
        'utils.common',
        'menus.datetime_menu',
        'menus.file_operations_menu',
        'menus.case_menu',
        'menus.string_replace_menu',
        'menus.line_operation_menu',
        'menus.sql_menu',
        'menus.browser_menu'
    ],
    hookspath=['.'],
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
    name='Task Buddy',
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
    icon=['icons\\task_buddy_blue.ico'],
)
