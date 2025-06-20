#!/bin/bash
# macOS打包启动脚本

echo "=== macOS 应用程序打包脚本 ==="
echo

# 检查是否在macOS上
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  警告: 不在macOS系统上，某些功能可能无法正常工作"
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python 3.6+"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装"
    exit 1
fi

# 安装依赖
echo "📦 安装Python依赖..."
pip3 install pyinstaller pillow

# 检查并安装create-dmg
if ! command -v create-dmg &> /dev/null; then
    echo "📦 安装create-dmg工具..."
    if command -v brew &> /dev/null; then
        brew install create-dmg
    else
        echo "⚠️  Homebrew未安装，create-dmg可能无法自动安装"
        echo "请手动安装: brew install create-dmg"
    fi
fi

# 构建应用
echo "🔨 开始构建macOS应用程序..."
python3 build_macos.py

# 检查构建是否成功
if [ -d "dist/文件批量重命名工具.app" ]; then
    echo "✅ 应用程序构建成功！"
    
    # 询问是否创建DMG
    read -p "是否创建DMG安装包？ (y/n): " create_dmg_choice
    if [[ $create_dmg_choice =~ ^[Yy]$ ]]; then
        echo "📦 创建DMG安装包..."
        python3 create_dmg.py
        
        if [ -f "setup/文件批量重命名工具-macOS.dmg" ]; then
            echo "✅ DMG安装包创建成功！"
            echo "📍 位置: setup/文件批量重命名工具-macOS.dmg"
        else
            echo "⚠️  DMG创建可能失败，但应用程序可用"
        fi
    fi
    
    echo
    echo "=== 构建完成 ==="
    echo "应用程序: dist/文件批量重命名工具.app"
    if [ -f "setup/文件批量重命名工具-macOS.dmg" ]; then
        echo "安装包: setup/文件批量重命名工具-macOS.dmg"
    fi
    echo
    echo "💡 提示："
    echo "- 双击.app文件直接运行应用"
    echo "- 拖拽.app到Applications文件夹安装"
    echo "- 分发DMG文件给其他用户"
    
else
    echo "❌ 应用程序构建失败"
    exit 1
fi 