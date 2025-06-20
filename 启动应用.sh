#!/bin/bash

echo "文件批量重命名工具"
echo "=================="
echo ""
echo "正在启动应用..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python 3.6或更高版本"
    read -p "按回车键退出..."
    exit 1
fi

# 启动应用
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败，请检查Python是否已正确安装"
    read -p "按回车键退出..."
fi 