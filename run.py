#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件批量重命名工具启动脚本
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 6):
        print("错误: 此应用需要Python 3.6或更高版本")
        print(f"当前Python版本: {sys.version}")
        return False
    return True

def check_tkinter():
    """检查tkinter是否可用"""
    try:
        import tkinter
        return True
    except ImportError:
        print("错误: tkinter未安装或不可用")
        print("请确保Python安装时包含了tkinter模块")
        return False

def main():
    """主函数"""
    print("文件批量重命名工具")
    print("=" * 30)
    
    # 检查系统要求
    if not check_python_version():
        input("按回车键退出...")
        return
    
    if not check_tkinter():
        input("按回车键退出...")
        return
    
    # 启动应用
    try:
        print("正在启动应用...")
        import main
        main.main()
    except KeyboardInterrupt:
        print("\n应用已被用户中断")
    except Exception as e:
        print(f"启动应用时发生错误: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main() 