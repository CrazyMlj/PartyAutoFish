# build.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# 收集 rapidocr_onnxruntime 的所有资源
ocr_datas, ocr_binaries, ocr_hidden = collect_all('rapidocr_onnxruntime')

# 收集 onnxruntime 的所有资源
ort_datas, ort_binaries, ort_hidden = collect_all('onnxruntime')

# 合并所有资源
datas = ocr_datas + ort_datas
binaries = ocr_binaries + ort_binaries
hiddenimports = ocr_hidden + ort_hidden

# 确保关键模块被包含
key_modules = [
    'rapidocr_onnxruntime.ch_ppocr_v2_cls',
    'rapidocr_onnxruntime.ch_ppocr_v3_det',
    'rapidocr_onnxruntime.ch_ppocr_v3_rec',
    'onnxruntime.capi',
]
for module in key_modules:
    if module not in hiddenimports:
        hiddenimports.append(module)

added_files = [
    # 包含整个 resources 文件夹
    ('resources', 'resources'),
    # 如果需要单独添加 dll
    # ('dxgi4py.dll', '.'),
    # 添加配置文件
    ('parameters.json', '.'),
]

a = Analysis(
    ['Start.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoFish',                  # 输出文件名
    debug=True,                      # 调试模式
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                         # 启用 UPX 压缩（需要安装 upx）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                    # False=隐藏控制台，True=显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/logo.ico'         # 程序图标
)

