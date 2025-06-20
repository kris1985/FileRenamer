#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS DMG安装包创建脚本
将应用程序打包为DMG格式的安装包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """检查必要的工具是否可用"""
    required_tools = []
    
    # 检查是否在macOS上
    if sys.platform != "darwin":
        print("警告: 不在macOS系统上，DMG创建可能无法正常工作")
        return False
    
    # 检查create-dmg工具
    try:
        subprocess.check_output(["which", "create-dmg"], stderr=subprocess.DEVNULL)
        print("create-dmg工具已安装")
    except subprocess.CalledProcessError:
        print("create-dmg工具未安装，尝试使用Homebrew安装...")
        try:
            subprocess.check_call(["brew", "install", "create-dmg"])
            print("create-dmg安装成功")
        except subprocess.CalledProcessError:
            print("create-dmg安装失败，请手动安装:")
            print("brew install create-dmg")
            return False
    
    return True

def create_dmg_structure():
    """创建DMG所需的目录结构"""
    dmg_temp_dir = Path("dmg_temp")
    
    # 清理旧的临时目录
    if dmg_temp_dir.exists():
        shutil.rmtree(dmg_temp_dir)
    
    dmg_temp_dir.mkdir()
    print(f"已创建临时目录: {dmg_temp_dir}")
    
    # 检查应用程序是否存在
    app_path = Path("dist/文件批量重命名工具.app")
    if not app_path.exists():
        print(f"错误: 应用程序不存在: {app_path}")
        print("请先运行 python build_macos.py 构建应用程序")
        return None, None
    
    # 复制应用程序到临时目录
    target_app = dmg_temp_dir / "文件批量重命名工具.app"
    shutil.copytree(app_path, target_app)
    print(f"已复制应用程序到: {target_app}")
    
    # 创建应用程序文件夹的快捷方式
    applications_link = dmg_temp_dir / "Applications"
    try:
        applications_link.symlink_to("/Applications")
        print("已创建Applications快捷方式")
    except Exception as e:
        print(f"创建Applications快捷方式失败: {e}")
    
    # 复制README文件（如果存在）
    readme_path = Path("README.md")
    if readme_path.exists():
        shutil.copy2(readme_path, dmg_temp_dir)
        print("已复制README.md")
    
    return dmg_temp_dir, target_app

def create_dmg_background():
    """创建DMG背景图像"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建背景图像
        width, height = 600, 400
        img = Image.new('RGB', (width, height), (245, 245, 245))
        draw = ImageDraw.Draw(img)
        
        # 绘制渐变背景
        for y in range(height):
            progress = y / height
            r = int(245 - progress * 20)
            g = int(245 - progress * 20)
            b = int(245 - progress * 20)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # 添加标题文字
        try:
            # 尝试使用系统字体
            font_large = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
            font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
        except:
            # 使用默认字体
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 绘制安装说明
        title = "文件批量重命名工具"
        instruction = "将应用程序拖拽到 Applications 文件夹"
        
        # 计算文字位置
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        
        instruction_bbox = draw.textbbox((0, 0), instruction, font=font_small)
        instruction_width = instruction_bbox[2] - instruction_bbox[0]
        instruction_x = (width - instruction_width) // 2
        
        # 绘制文字
        draw.text((title_x, 50), title, fill=(50, 50, 50), font=font_large)
        draw.text((instruction_x, 350), instruction, fill=(100, 100, 100), font=font_small)
        
        # 绘制箭头
        arrow_y = 200
        arrow_start_x = 150
        arrow_end_x = 450
        
        # 箭头线
        draw.line([(arrow_start_x, arrow_y), (arrow_end_x, arrow_y)], 
                 fill=(100, 100, 100), width=3)
        
        # 箭头头部
        arrow_head = [
            (arrow_end_x, arrow_y),
            (arrow_end_x - 15, arrow_y - 8),
            (arrow_end_x - 15, arrow_y + 8)
        ]
        draw.polygon(arrow_head, fill=(100, 100, 100))
        
        # 保存背景图像
        bg_path = Path("dmg_temp/background.png")
        img.save(bg_path)
        print(f"已创建DMG背景图像: {bg_path}")
        return bg_path
        
    except Exception as e:
        print(f"创建背景图像失败: {e}")
        return None

def create_dmg_with_create_dmg(dmg_temp_dir):
    """使用create-dmg工具创建DMG"""
    # 确保setup目录存在
    setup_dir = Path("setup")
    setup_dir.mkdir(exist_ok=True)
    
    dmg_name = "文件批量重命名工具-macOS"
    dmg_path = setup_dir / f"{dmg_name}.dmg"
    
    # 删除已存在的DMG文件
    if dmg_path.exists():
        dmg_path.unlink()
    
    # create-dmg命令参数
    cmd = [
        "create-dmg",
        "--volname", "文件批量重命名工具",
        "--volicon", "app_icon.icns" if Path("app_icon.icns").exists() else "",
        "--window-pos", "200", "120",
        "--window-size", "600", "400",
        "--icon-size", "100",
        "--icon", "文件批量重命名工具.app", "150", "200",
        "--hide-extension", "文件批量重命名工具.app",
        "--app-drop-link", "450", "200",
        str(dmg_path),
        str(dmg_temp_dir)
    ]
    
    # 过滤空参数
    cmd = [arg for arg in cmd if arg]
    
    try:
        print("正在创建DMG安装包...")
        print(f"命令: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print(f"DMG创建成功: {dmg_path}")
        return dmg_path
    except subprocess.CalledProcessError as e:
        print(f"create-dmg执行失败: {e}")
        return None

def create_dmg_with_hdiutil(dmg_temp_dir):
    """使用hdiutil创建基本DMG（备用方法）"""
    setup_dir = Path("setup")
    setup_dir.mkdir(exist_ok=True)
    
    dmg_name = "文件批量重命名工具-macOS-simple"
    dmg_path = setup_dir / f"{dmg_name}.dmg"
    
    # 删除已存在的DMG文件
    if dmg_path.exists():
        dmg_path.unlink()
    
    try:
        print("正在使用hdiutil创建DMG...")
        subprocess.check_call([
            "hdiutil", "create",
            "-volname", "文件批量重命名工具",
            "-srcfolder", str(dmg_temp_dir),
            "-ov",
            "-format", "UDZO",
            str(dmg_path)
        ])
        print(f"简单DMG创建成功: {dmg_path}")
        return dmg_path
    except subprocess.CalledProcessError as e:
        print(f"hdiutil执行失败: {e}")
        return None

def cleanup_temp_files():
    """清理临时文件"""
    dmg_temp_dir = Path("dmg_temp")
    if dmg_temp_dir.exists():
        shutil.rmtree(dmg_temp_dir)
        print("已清理临时文件")

def main():
    """主函数"""
    print("=== macOS DMG安装包创建脚本 ===")
    print()
    
    # 检查必要工具
    if not check_requirements():
        print("必要工具检查失败，退出")
        return
    
    try:
        # 创建DMG结构
        dmg_temp_dir, app_path = create_dmg_structure()
        if not dmg_temp_dir:
            return
        
        # 创建背景图像
        create_dmg_background()
        
        # 尝试使用create-dmg创建DMG
        dmg_path = create_dmg_with_create_dmg(dmg_temp_dir)
        
        # 如果失败，使用hdiutil作为备用
        if not dmg_path:
            print("尝试使用备用方法创建DMG...")
            dmg_path = create_dmg_with_hdiutil(dmg_temp_dir)
        
        if dmg_path:
            print()
            print("=== DMG创建完成 ===")
            print(f"安装包位置: {dmg_path}")
            print(f"文件大小: {dmg_path.stat().st_size / 1024 / 1024:.1f} MB")
            print()
            print("用户可以:")
            print("1. 双击DMG文件挂载")
            print("2. 将应用程序拖拽到Applications文件夹")
            print("3. 在启动台中找到并运行应用程序")
        else:
            print("DMG创建失败")
    
    finally:
        # 清理临时文件
        cleanup_temp_files()

if __name__ == "__main__":
    main() 