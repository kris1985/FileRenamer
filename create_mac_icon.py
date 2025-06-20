#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macOS应用图标生成脚本
创建ICNS格式的应用图标，支持高分辨率Retina显示器
"""

import os
import sys
import subprocess
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("PIL/Pillow未安装，正在尝试安装...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        from PIL import Image, ImageDraw, ImageFont
        print("PIL/Pillow安装成功")
    except Exception as e:
        print(f"安装失败: {e}")
        sys.exit(1)

def create_folder_icon():
    """创建文件夹样式的图标"""
    # macOS应用图标需要的所有尺寸
    icon_sizes = [
        16, 32, 48, 64, 128, 256, 512, 1024
    ]
    
    icons = []
    
    for size in icon_sizes:
        # 创建图像
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 计算尺寸比例
        scale = size / 128.0
        
        # 绘制文件夹形状
        folder_width = int(90 * scale)
        folder_height = int(70 * scale)
        folder_x = (size - folder_width) // 2
        folder_y = int((size - folder_height) // 2 + 10 * scale)
        
        # 文件夹主体
        folder_rect = [
            folder_x,
            folder_y,
            folder_x + folder_width,
            folder_y + folder_height
        ]
        
        # 渐变色填充（蓝色主题）
        for i in range(folder_height):
            y = folder_y + i
            progress = i / folder_height
            r = int(70 + (130 - 70) * progress)  # 70 -> 130
            g = int(130 + (170 - 130) * progress)  # 130 -> 170
            b = int(220 + (250 - 220) * progress)  # 220 -> 250
            
            draw.line(
                [(folder_x, y), (folder_x + folder_width, y)],
                fill=(r, g, b, 255),
                width=1
            )
        
        # 文件夹标签页
        tab_width = int(30 * scale)
        tab_height = int(12 * scale)
        tab_rect = [
            folder_x,
            folder_y - tab_height,
            folder_x + tab_width,
            folder_y + int(3 * scale)
        ]
        
        draw.rounded_rectangle(
            tab_rect,
            radius=int(3 * scale),
            fill=(90, 140, 200, 255)
        )
        
        # 文件夹边框
        draw.rounded_rectangle(
            folder_rect,
            radius=int(5 * scale),
            outline=(50, 100, 180, 255),
            width=max(1, int(2 * scale))
        )
        
        # 添加文件图标（小的文档图标）
        if size >= 64:
            file_size = int(16 * scale)
            file_x = folder_x + int(20 * scale)
            file_y = folder_y + int(15 * scale)
            
            # 第一个文件
            file_rect1 = [
                file_x,
                file_y,
                file_x + file_size,
                file_y + int(20 * scale)
            ]
            draw.rounded_rectangle(
                file_rect1,
                radius=int(2 * scale),
                fill=(255, 255, 255, 200)
            )
            draw.rounded_rectangle(
                file_rect1,
                radius=int(2 * scale),
                outline=(150, 150, 150, 255),
                width=1
            )
            
            # 第二个文件
            file_x2 = file_x + int(25 * scale)
            file_rect2 = [
                file_x2,
                file_y + int(8 * scale),
                file_x2 + file_size,
                file_y + int(28 * scale)
            ]
            draw.rounded_rectangle(
                file_rect2,
                radius=int(2 * scale),
                fill=(255, 255, 255, 180)
            )
            draw.rounded_rectangle(
                file_rect2,
                radius=int(2 * scale),
                outline=(150, 150, 150, 255),
                width=1
            )
        
        # 添加重命名箭头（如果尺寸足够大）
        if size >= 128:
            arrow_size = int(12 * scale)
            arrow_x = folder_x + folder_width - int(25 * scale)
            arrow_y = folder_y + folder_height - int(25 * scale)
            
            # 绘制箭头
            arrow_points = [
                (arrow_x, arrow_y + arrow_size // 2),
                (arrow_x + arrow_size, arrow_y + arrow_size // 2),
                (arrow_x + arrow_size - int(4 * scale), arrow_y + int(2 * scale)),
                (arrow_x + arrow_size - int(4 * scale), arrow_y + arrow_size - int(2 * scale))
            ]
            
            draw.polygon(arrow_points, fill=(255, 200, 0, 255))
            draw.polygon(arrow_points, outline=(200, 150, 0, 255), width=1)
        
        icons.append(img)
    
    return icons, icon_sizes

def create_icns_file(icons, sizes, output_path="app_icon.icns"):
    """创建ICNS文件（macOS图标格式）"""
    try:
        # 创建临时PNG文件
        temp_dir = Path("temp_icons")
        temp_dir.mkdir(exist_ok=True)
        
        png_files = []
        for icon, size in zip(icons, sizes):
            png_path = temp_dir / f"icon_{size}x{size}.png"
            icon.save(png_path, "PNG")
            png_files.append(png_path)
        
        # 使用iconutil创建ICNS（macOS专用）
        if sys.platform == "darwin":
            # 创建iconset目录结构
            iconset_dir = temp_dir / "AppIcon.iconset"
            iconset_dir.mkdir(exist_ok=True)
            
            # 映射尺寸到iconset文件名
            iconset_mapping = {
                16: "icon_16x16.png",
                32: "icon_16x16@2x.png",
                48: "icon_24x24@2x.png",  # 不是标准的，但有些工具支持
                64: "icon_32x32@2x.png",
                128: "icon_128x128.png",
                256: "icon_128x128@2x.png",
                512: "icon_256x256@2x.png",
                1024: "icon_512x512@2x.png"
            }
            
            # 标准macOS图标尺寸
            standard_mapping = {
                16: "icon_16x16.png",
                32: ["icon_16x16@2x.png", "icon_32x32.png"],
                64: "icon_32x32@2x.png",
                128: "icon_128x128.png",
                256: ["icon_128x128@2x.png", "icon_256x256.png"],
                512: ["icon_256x256@2x.png", "icon_512x512.png"],
                1024: "icon_512x512@2x.png"
            }
            
            # 复制图标到iconset目录
            for icon, size in zip(icons, sizes):
                if size in standard_mapping:
                    target_names = standard_mapping[size]
                    if isinstance(target_names, str):
                        target_names = [target_names]
                    
                    for target_name in target_names:
                        target_path = iconset_dir / target_name
                        icon.save(target_path, "PNG")
            
            # 使用iconutil生成icns
            try:
                subprocess.check_call([
                    "iconutil", "-c", "icns", str(iconset_dir), "-o", output_path
                ])
                print(f"成功创建ICNS文件: {output_path}")
                return True
            except subprocess.CalledProcessError:
                print("iconutil执行失败，尝试替代方法...")
                return False
        else:
            # 非macOS系统，创建一个大尺寸的PNG作为替代
            largest_icon = icons[-1]  # 最大尺寸的图标
            largest_icon.save(output_path.replace(".icns", ".png"), "PNG")
            print(f"非macOS系统，已创建PNG图标: {output_path.replace('.icns', '.png')}")
            return True
            
    except Exception as e:
        print(f"创建ICNS失败: {e}")
        return False
    finally:
        # 清理临时文件
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)

def create_mac_icon():
    """主函数：创建macOS应用图标"""
    print("正在创建macOS应用图标...")
    
    try:
        # 创建图标
        icons, sizes = create_folder_icon()
        
        # 创建ICNS文件
        if create_icns_file(icons, sizes):
            print("macOS应用图标创建成功！")
            print("文件位置: app_icon.icns")
            return True
        else:
            print("图标创建失败")
            return False
            
    except Exception as e:
        print(f"创建图标时发生错误: {e}")
        return False

if __name__ == "__main__":
    create_mac_icon() 