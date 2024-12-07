import os
from glob import glob
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.api import PYZ, EXE, COLLECT

# Manually collect data files from your project directory
datas = []

# Add settings.prc manually
config_file = os.path.join(os.getcwd(), 'settings.prc')
datas.append((config_file, 'settings.prc'))  # Add settings.prc to the root of the build

# Optionally, add more files from your project directory
datas.extend([(file, os.path.basename(file)) for file in glob(os.path.join('E:\\soul-symphony', '*.prc'))])  # All .prc files
datas.extend([(file, os.path.basename(file)) for file in glob(os.path.join('E:\\soul-symphony', '*.png'))])  # All .png files

# Collect DLLs if needed
lib_dir = os.path.abspath("lib")
dll_files = [(file, os.path.join('_include', os.path.basename(file))) for file in glob(os.path.join(lib_dir, "*.dll"))]

# Include other binary files if needed
binaries = [
    ('C:\\Users\\User\\miniconda3\\python310.dll', '_internal/python310.dll'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt5-sip'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='灵魂交响乐',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='灵魂交响乐',
)
