#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows打包脚本
使用PyInstaller将Python应用打包为Windows可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("PyInstaller not installed, installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("PyInstaller installation failed, please install manually: pip install pyinstaller")
            return False

def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned directory: {dir_name}")
    
    # 清理.spec文件
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"Deleted: {spec_file}")

def create_spec_file():
    """创建PyInstaller规格文件"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    a.zipfiles,
    a.datas,
    [],
    name='FileRenamer',
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
    icon=None,
)
'''
    
    with open("FileRenamer.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("Created PyInstaller spec file: FileRenamer.spec")

def build_executable():
    """构建可执行文件"""
    print("Starting executable build...")
    try:
        # 使用spec文件构建
        subprocess.check_call([
            "pyinstaller", 
            "--clean",
            "FileRenamer.spec"
        ])
        print("Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def copy_additional_files():
    """复制额外的文件到dist目录"""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("dist directory does not exist")
        return
    
    # 要复制的文件
    files_to_copy = [
        "README.md",
        "requirements.txt",
        "启动应用.bat"
    ]
    
    files_copied = 0
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            try:
                shutil.copy2(file_name, dist_dir)
                files_copied += 1
                # 避免打印中文文件名，改为打印数量
                if file_name.endswith('.bat'):
                    print("Copied: startup script")
                else:
                    print(f"Copied: {file_name}")
            except Exception as e:
                print(f"Failed to copy file: {e}")
    
    print(f"Total files copied: {files_copied}")

def create_icon():
    """创建应用图标"""
    print("Creating application icon...")
    try:
        import create_icon
        if create_icon.create_simple_icon():
            return True
        else:
            print("Icon creation failed, will use default icon")
            return False
    except Exception as e:
        print(f"Icon creation failed: {e}")
        return False

def update_spec_file_with_icon():
    """更新spec文件以包含图标"""
    if os.path.exists("app_icon.ico"):
        # 读取现有的spec文件
        with open("FileRenamer.spec", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 更新图标路径
        content = content.replace("icon=None,", "icon='app_icon.ico',")
        
        # 写回文件
        with open("FileRenamer.spec", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("Updated spec file to include icon")

def main():
    """主函数"""
    print("=== Windows Build Script ===")
    print()
    
    # 检查PyInstaller
    if not check_pyinstaller():
        return
    
    # 清理构建目录
    clean_build_dirs()
    
    # 创建图标
    create_icon()
    
    # 创建规格文件
    create_spec_file()
    
    # 更新规格文件以包含图标
    update_spec_file_with_icon()
    
    # 构建可执行文件
    if build_executable():
        # 复制额外文件
        copy_additional_files()
        
        print()
        print("=== Build Complete ===")
        print("Executable location: dist/FileRenamer.exe")
        print("You can distribute the entire dist folder to users")
        print()
        print("To create installer, run Inno Setup with installer_script.iss file")
    else:
        print("Build failed")

if __name__ == "__main__":
    main() 