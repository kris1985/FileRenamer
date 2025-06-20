@echo off
chcp 65001 >nul
echo 文件批量重命名工具
echo ==================
echo.
echo 正在启动应用...
python main.py
if errorlevel 1 (
    echo.
    echo 启动失败，请检查Python是否已正确安装
    pause
) 