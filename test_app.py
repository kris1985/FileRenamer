#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量重命名工具测试脚本
用于创建测试文件和文件夹结构
"""

import os
import shutil
from pathlib import Path


def create_test_structure():
    """创建测试文件夹结构"""
    # 创建测试根目录
    test_dir = Path("test_files")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    
    # 创建主文件夹
    main_folder = test_dir / "产品图片"
    main_folder.mkdir()
    
    # 在主文件夹中创建一些文件
    for i in range(3):
        (main_folder / f"主图_{i+1}.jpg").touch()
        (main_folder / f"详情图副图_1_{i+1}.png").touch()
    
    # 创建子文件夹
    sub_folders = ["颜色1", "颜色2", "尺寸图"]
    
    for folder_name in sub_folders:
        sub_folder = main_folder / folder_name
        sub_folder.mkdir()
        
        # 在每个子文件夹中创建文件
        for i in range(4):
            (sub_folder / f"{folder_name}_图片_{i+1}.jpg").touch()
            (sub_folder / f"{folder_name}_副图_1_{i+1}.png").touch()
    
    # 创建更深层的嵌套文件夹
    deep_folder = main_folder / "颜色1" / "深层文件夹"
    deep_folder.mkdir()
    for i in range(2):
        (deep_folder / f"深层图片_{i+1}.jpg").touch()
        (deep_folder / f"深层副图_1_{i+1}.gif").touch()
    
    print(f"测试文件结构已创建在: {test_dir.absolute()}")
    print("\n文件夹结构:")
    print_directory_tree(test_dir)


def print_directory_tree(path, prefix=""):
    """打印目录树结构"""
    path = Path(path)
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        print(f"{prefix}{current_prefix}{item.name}")
        
        if item.is_dir():
            next_prefix = prefix + ("    " if is_last else "│   ")
            print_directory_tree(item, next_prefix)


def create_copy_target():
    """创建复制目标文件夹"""
    target_dir = Path("copy_target")
    if not target_dir.exists():
        target_dir.mkdir()
    print(f"复制目标文件夹已创建: {target_dir.absolute()}")


def cleanup_test_files():
    """清理测试文件"""
    test_dir = Path("test_files")
    target_dir = Path("copy_target")
    
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("已删除测试文件夹")
    
    if target_dir.exists():
        shutil.rmtree(target_dir)
        print("已删除目标文件夹")


def main():
    """主函数"""
    print("文件批量重命名工具 - 测试脚本")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建测试文件结构")
        print("2. 创建复制目标文件夹")
        print("3. 显示当前文件结构")
        print("4. 清理所有测试文件")
        print("5. 启动主应用程序")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == "1":
            create_test_structure()
        elif choice == "2":
            create_copy_target()
        elif choice == "3":
            test_dir = Path("test_files")
            if test_dir.exists():
                print(f"\n当前测试文件结构 ({test_dir.absolute()}):")
                print_directory_tree(test_dir)
            else:
                print("测试文件夹不存在，请先创建测试文件结构")
        elif choice == "4":
            cleanup_test_files()
        elif choice == "5":
            print("启动主应用程序...")
            import main
            main.main()
            break
        elif choice == "0":
            print("退出测试脚本")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    main() 