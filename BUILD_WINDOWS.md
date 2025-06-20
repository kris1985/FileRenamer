# Windows 打包说明

本文档说明如何将Python应用打包为Windows可执行文件和安装包。

## 🔧 准备工作

### 1. 安装Python
确保已安装Python 3.6或更高版本，并将Python添加到系统PATH中。

### 2. 安装依赖
```bash
pip install pyinstaller
pip install pillow  # 可选，用于生成应用图标
```

## 📦 打包步骤

### 方法1：使用批处理文件（推荐）
1. 双击运行 `build_windows.bat`
2. 等待打包完成
3. 可执行文件将生成在 `dist` 文件夹中

### 方法2：使用Python脚本
```bash
python build_windows.py
```

### 方法3：手动打包
```bash
# 1. 安装PyInstaller
pip install pyinstaller

# 2. 创建图标（可选）
python create_icon.py

# 3. 打包应用
pyinstaller --name="文件批量重命名工具" --windowed --onefile --icon=app_icon.ico main.py
```

## 🎁 创建安装包

### 1. 下载Inno Setup
- 访问: https://jrsoftware.org/isdl.php
- 下载并安装最新版本的Inno Setup

### 2. 编译安装脚本
1. 打开Inno Setup
2. 选择 "打开现有脚本文件"
3. 选择项目中的 `installer_script.iss` 文件
4. 点击 "编译" 按钮（或按F9）
5. 安装包将生成在 `setup` 文件夹中

## 📁 文件结构

打包完成后，项目目录结构如下：

```
FileRenamer/
├── main.py                          # 主应用程序
├── build_windows.py                 # 打包脚本
├── build_windows.bat               # Windows批处理脚本
├── create_icon.py                  # 图标生成脚本
├── installer_script.iss            # Inno Setup安装脚本
├── FileRenamer.spec               # PyInstaller规格文件（自动生成）
├── app_icon.ico                   # 应用图标（自动生成）
├── dist/                          # 打包输出目录
│   └── 文件批量重命名工具.exe      # 可执行文件
├── setup/                         # 安装包输出目录
│   └── 文件批量重命名工具_安装程序_v1.0.0.exe
└── build/                         # 临时构建文件（可删除）
```

## ⚙️ 配置选项

### PyInstaller 选项
在 `build_windows.py` 中可以修改以下选项：

- `--name`: 可执行文件名称
- `--windowed`: 无控制台窗口
- `--onefile`: 打包为单个文件
- `--icon`: 应用图标

### Inno Setup 选项
在 `installer_script.iss` 中可以修改：

- 应用名称和版本
- 安装目录
- 桌面快捷方式
- 开始菜单项
- 卸载程序

## 🚨 常见问题

### 1. PyInstaller 未找到
**问题**: 'pyinstaller' 不是内部或外部命令
**解决**: 
```bash
pip install pyinstaller
# 或者使用
python -m pip install pyinstaller
```

### 2. 图标创建失败
**问题**: PIL (Pillow) 未安装
**解决**: 
```bash
pip install pillow
```
或者手动创建一个名为 `app_icon.ico` 的图标文件。

### 3. 打包后运行错误
**问题**: 缺少依赖库
**解决**: 
- 检查 `FileRenamer.spec` 文件
- 在 `hiddenimports` 中添加缺少的模块

### 4. 中文显示问题
**问题**: 安装包中文显示乱码
**解决**: 
- 确保系统支持UTF-8编码
- 使用Inno Setup的中文语言包

## 📋 发布检查清单

打包完成后，请检查以下项目：

- [ ] 可执行文件能正常启动
- [ ] 所有功能正常工作
- [ ] 界面显示正确
- [ ] 文件操作权限正常
- [ ] 安装包能正确安装和卸载
- [ ] 桌面快捷方式正常工作
- [ ] 开始菜单项正常

## 📈 优化建议

### 减小文件大小
1. 使用 `--exclude-module` 排除不需要的模块
2. 压缩可执行文件（UPX）
3. 删除不需要的库文件

### 提高启动速度
1. 使用 `--onedir` 而不是 `--onefile`
2. 优化导入语句
3. 延迟加载重型库

### 安全性
1. 数字签名可执行文件
2. 病毒扫描
3. 测试在不同Windows版本上的兼容性

## 🎯 自动化构建

可以创建GitHub Actions工作流或其他CI/CD流程来自动化打包过程：

```yaml
# .github/workflows/build-windows.yml
name: Build Windows App
on: [push, pull_request]
jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install pyinstaller pillow
    - name: Build application
      run: python build_windows.py
    - name: Upload artifacts
      uses: actions/upload-artifact@v2
      with:
        name: windows-app
        path: dist/
``` 