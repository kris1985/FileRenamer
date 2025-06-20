#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS打包脚本
使用PyInstaller将Python应用打包为macOS应用程序
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
    [],
    exclude_binaries=True,
    name='文件批量重命名工具',
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='文件批量重命名工具',
)

app = BUNDLE(
    coll,
    name='文件批量重命名工具.app',
    icon='app_icon.icns',
    bundle_identifier='com.filerenamer.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'Folder',
                'CFBundleTypeRole': 'Editor',
                'LSItemContentTypes': ['public.folder'],
            }
        ],
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13',
    },
)
'''
    
    with open("FileRenamer_macOS.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("已创建PyInstaller规格文件: FileRenamer_macOS.spec")

def build_executable():
    """构建可执行文件"""
    print("开始构建macOS应用程序...")
    try:
        # 使用spec文件构建
        subprocess.check_call([
            "pyinstaller", 
            "--clean",
            "FileRenamer_macOS.spec"
        ])
        print("macOS应用程序构建成功！")
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
        "requirements.txt"
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_dir)
            print(f"已复制: {file_name}")

def create_icon():
    """创建应用图标"""
    print("正在创建应用图标...")
    try:
        import create_mac_icon
        if create_mac_icon.create_mac_icon():
            return True
        else:
            print("图标创建失败，将使用默认图标")
            return False
    except Exception as e:
        print(f"图标创建失败: {e}")
        return False

def update_spec_file_with_icon():
    """更新spec文件以包含图标"""
    if os.path.exists("app_icon.icns"):
        # 读取现有的spec文件
        with open("FileRenamer_macOS.spec", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 图标路径已经在spec文件中设置了
        print("已设置应用图标")

def set_permissions():
    """设置应用程序权限"""
    app_path = "dist/文件批量重命名工具.app"
    if os.path.exists(app_path):
        try:
            # 设置执行权限
            subprocess.check_call([
                "chmod", "-R", "755", app_path
            ])
            print("已设置应用程序权限")
        except subprocess.CalledProcessError as e:
            print(f"设置权限失败: {e}")

def main():
    """主函数"""
    print("=== macOS打包脚本 ===")
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
        # 设置权限
        set_permissions()
        
        # 复制额外文件
        copy_additional_files()
        
        print()
        print("=== 构建完成 ===")
        print("应用程序位置: dist/文件批量重命名工具.app")
        print("可以将整个dist文件夹分发给用户")
        print()
        print("如需创建DMG安装包，请运行: python create_dmg.py")
    else:
        print("构建失败")

if __name__ == "__main__":
    main() 