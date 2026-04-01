# -*- mode: python ; coding: utf-8 -*-

import sys
import platform
from PyInstaller.utils.hooks import collect_all

# 确定路径分隔符
if platform.system() == "Windows":
    sep = ";"
else:
    sep = ":"

# 收集所有需要的包数据
rapidocr_data = collect_all('rapidocr_onnxruntime')
onnxruntime_data = collect_all('onnxruntime')

# 合并所有数据文件
all_datas = []
all_binaries = []
all_hiddenimports = []

# 收集 rapidocr_onnxruntime
if rapidocr_data:
    all_datas.extend(rapidocr_data[0])  # datas
    all_binaries.extend(rapidocr_data[1])  # binaries
    all_hiddenimports.extend(rapidocr_data[2])  # hiddenimports

# 收集 onnxruntime
if onnxruntime_data:
    all_datas.extend(onnxruntime_data[0])
    all_binaries.extend(onnxruntime_data[1])
    all_hiddenimports.extend(onnxruntime_data[2])

a = Analysis(
    ['Start.py'],
    pathex=[],  # 可以添加额外的搜索路径
    binaries=all_binaries,
    datas=[
        ('resources', 'resources'),
    ] + all_datas,
    hiddenimports=list(set([
        'cv2',
        'numpy',
        'pynput',
        'ttkbootstrap',
        'mss',
        'yaml',
        'winsound',
        'ctypes',
        'PIL',
        'tkinter',
        'json',
        'os',
        'sys',
        'time',
        'threading',
        'datetime',
        're',
        'queue',
        'random',
        'webbrowser',
        'warnings',
    ] + all_hiddenimports)),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoFish',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 如果安装了 UPX 会启用压缩
    upx_dir='G:/PyChamProject/AutoFish/upx-5.1.1-win64',
    console=False,  # False = --windowed, True = 显示控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='resources/logo.ico',
)