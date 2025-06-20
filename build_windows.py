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
        print(f"PyInstaller版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller安装成功")
            return True
        except subprocess.CalledProcessError:
            print("PyInstaller安装失败，请手动安装: pip install pyinstaller")
            return False

def clean_build_dirs():
    """清理之前的构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理目录: {dir_name}")
    
    # 清理.spec文件
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"已删除: {spec_file}")

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
    name='文件批量重命名工具',
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
    print("已创建PyInstaller规格文件: FileRenamer.spec")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    try:
        # 使用spec文件构建
        subprocess.check_call([
            "pyinstaller", 
            "--clean",
            "FileRenamer.spec"
        ])
        print("可执行文件构建成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False

def copy_additional_files():
    """复制额外的文件到dist目录"""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("dist目录不存在")
        return
    
    # 要复制的文件
    files_to_copy = [
        "README.md",
        "requirements.txt",
        "启动应用.bat"
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"已复制: {file_name}")

def create_icon():
    """创建应用图标"""
    print("正在创建应用图标...")
    try:
        import create_icon
        if create_icon.create_simple_icon():
            return True
        else:
            print("图标创建失败，将使用默认图标")
            return False
    except Exception as e:
        print(f"图标创建失败: {e}")
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
        
        print("已更新spec文件以包含图标")

def main():
    """主函数"""
    print("=== Windows打包脚本 ===")
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
        print("=== 构建完成 ===")
        print("可执行文件位置: dist/文件批量重命名工具.exe")
        print("可以将整个dist文件夹分发给用户")
        print()
        print("如需创建安装包，请运行 Inno Setup 并使用 installer_script.iss 文件")
    else:
        print("构建失败")

if __name__ == "__main__":
    main() 