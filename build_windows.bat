@echo off
chcp 65001 >nul
echo ====================================
echo   文件批量重命名工具 - Windows打包
echo ====================================
echo.

echo 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6或更高版本
    pause
    exit /b 1
)

echo 开始打包过程...
python build_windows.py

if errorlevel 1 (
    echo.
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo ====================================
echo          打包完成！
echo ====================================
echo.
echo 可执行文件位置: dist\文件批量重命名工具.exe
echo.
echo 下一步：创建安装包
echo 1. 下载并安装 Inno Setup: https://jrsoftware.org/isdl.php
echo 2. 用 Inno Setup 打开 installer_script.iss 文件
echo 3. 点击 "Compile" 生成安装包
echo.
echo 安装包将生成在 setup 文件夹中
echo.
pause 