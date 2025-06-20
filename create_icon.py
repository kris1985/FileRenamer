#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建应用图标
使用PIL创建一个简单的图标文件
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL (Pillow) not installed, cannot create icon")
    print("Install with: pip install Pillow")

def create_simple_icon():
    """创建一个简单的应用图标"""
    if not PIL_AVAILABLE:
        return False
    
    # 创建256x256的图像
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制背景圆形
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=(70, 130, 180, 255), outline=(30, 90, 140, 255), width=4)
    
    # 绘制文件夹图标
    folder_color = (255, 215, 0, 255)  # 金色
    folder_width = size // 3
    folder_height = size // 4
    folder_x = (size - folder_width) // 2
    folder_y = (size - folder_height) // 2 - 10
    
    # 文件夹主体
    draw.rectangle([folder_x, folder_y, folder_x + folder_width, folder_y + folder_height],
                  fill=folder_color, outline=(200, 165, 0, 255), width=2)
    
    # 文件夹标签
    tab_width = folder_width // 3
    tab_height = 8
    draw.rectangle([folder_x, folder_y - tab_height, folder_x + tab_width, folder_y],
                  fill=folder_color, outline=(200, 165, 0, 255), width=2)
    
    # 绘制箭头表示重命名
    arrow_color = (255, 255, 255, 255)
    arrow_y = folder_y + folder_height + 20
    arrow_size = 15
    
    # 向右箭头
    points = [
        (folder_x + folder_width//4, arrow_y),
        (folder_x + folder_width//4 + arrow_size, arrow_y + arrow_size//2),
        (folder_x + folder_width//4, arrow_y + arrow_size)
    ]
    draw.polygon(points, fill=arrow_color)
    
    # 第二个文件夹（表示重命名后）
    folder2_x = folder_x + folder_width//2
    draw.rectangle([folder2_x, folder_y, folder2_x + folder_width, folder_y + folder_height],
                  fill=(144, 238, 144, 255), outline=(34, 139, 34, 255), width=2)
    
    # 保存为ICO文件
    try:
        # 创建多个尺寸的图标
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        
        for icon_size in sizes:
            resized = image.resize(icon_size, Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # 保存ICO文件
        icons[0].save('app_icon.ico', format='ICO', sizes=[(img.width, img.height) for img in icons])
        print("Icon file created: app_icon.ico")
        return True
        
    except Exception as e:
        print(f"Failed to save icon: {e}")
        return False

def main():
    """Main function"""
    print("=== Creating Application Icon ===")
    if create_simple_icon():
        print("Icon created successfully!")
    else:
        print("Icon creation failed")
        print("You can manually create an app_icon.ico file")

if __name__ == "__main__":
    main() 