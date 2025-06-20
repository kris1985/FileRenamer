# GitHub Actions 自动构建文档

本文档说明如何使用GitHub Actions自动构建Windows和macOS版本的文件批量重命名工具。

## 功能特性

- ✅ 跨平台自动构建（Windows + macOS）
- ✅ 自动创建应用图标
- ✅ 生成安装包（Windows EXE + macOS DMG）
- ✅ 自动发布到GitHub Releases
- ✅ 构建产物上传为Artifacts

## 工作流触发条件

工作流会在以下情况自动运行：

1. **推送到主分支**: 当代码推送到 `main` 或 `master` 分支
2. **创建标签**: 当推送标签（格式：`v*`，如 `v1.0.0`）
3. **Pull Request**: 当创建或更新Pull Request时

## 构建矩阵

| 平台 | 运行环境 | 输出文件 | 安装包 |
|------|----------|----------|--------|
| Windows | `windows-latest` | `文件批量重命名工具.exe` | Windows安装程序 |
| macOS | `macos-latest` | `文件批量重命名工具.app` | DMG安装包 |

## 使用方法

### 1. 设置仓库

确保你的代码已推送到GitHub仓库，并包含以下文件：

```
FileRenamer/
├── .github/workflows/build-release.yml  # GitHub Actions工作流
├── main.py                              # 主程序
├── build_windows.py                     # Windows构建脚本
├── build_macos.py                       # macOS构建脚本
├── create_icon.py                       # Windows图标生成
├── create_mac_icon.py                   # macOS图标生成
├── create_dmg.py                        # DMG安装包生成
└── requirements.txt                     # Python依赖
```

### 2. 推送代码触发构建

```bash
# 推送代码到主分支（触发构建但不发布）
git add .
git commit -m "更新应用程序"
git push origin main

# 创建版本标签（触发构建并发布）
git tag v1.0.0
git push origin v1.0.0
```

### 3. 查看构建状态

1. 访问GitHub仓库页面
2. 点击 "Actions" 标签
3. 查看工作流运行状态

### 4. 下载构建产物

#### 方法一：从Artifacts下载

1. 进入成功运行的工作流
2. 在 "Artifacts" 部分下载：
   - `windows-app`: Windows应用程序和安装包
   - `macos-app`: macOS应用程序和DMG安装包

#### 方法二：从Releases下载（仅限标签构建）

1. 访问仓库的 "Releases" 页面
2. 下载最新发布的文件：
   - Windows: `.exe` 安装程序
   - macOS: `.dmg` 安装包

## 工作流详细说明

### 构建阶段

每个平台的构建过程包括：

1. **环境准备**
   - 检出代码
   - 设置Python 3.11环境
   - 安装依赖（PyInstaller, Pillow）

2. **图标生成**
   - Windows: 生成ICO格式图标
   - macOS: 生成ICNS格式图标

3. **应用构建**
   - 使用PyInstaller打包为可执行文件
   - Windows: 生成EXE文件
   - macOS: 生成APP包

4. **安装包创建**
   - Windows: 创建Windows安装程序
   - macOS: 创建DMG安装包

5. **产物上传**
   - 上传构建结果为GitHub Artifacts
   - 保留30天

### 发布阶段

当推送版本标签时，会自动：

1. 下载所有平台的构建产物
2. 创建GitHub Release
3. 上传安装包到Release
4. 生成发布说明

## 本地测试

在推送到GitHub之前，可以本地测试构建脚本：

### Windows本地构建

```bash
# 安装依赖
pip install pyinstaller pillow

# 生成图标
python create_icon.py

# 构建应用
python build_windows.py
```

### macOS本地构建

```bash
# 安装依赖
pip install pyinstaller pillow
brew install create-dmg

# 生成图标
python create_mac_icon.py

# 构建应用
python build_macos.py

# 创建DMG
python create_dmg.py
```

## 自定义配置

### 修改应用信息

编辑以下文件中的应用信息：

- `build_windows.py`: Windows应用配置
- `build_macos.py`: macOS应用配置
- `.github/workflows/build-release.yml`: 工作流配置

### 修改构建参数

在工作流文件中可以修改：

- Python版本（默认3.11）
- 构建平台
- 产物保留时间
- 发布条件

### 添加代码签名

#### Windows代码签名

在工作流中添加证书配置：

```yaml
- name: Import certificate
  uses: actions/import-certificate@v1
  with:
    certificate-data: ${{ secrets.WINDOWS_CERTIFICATE }}
    certificate-password: ${{ secrets.CERT_PASSWORD }}

- name: Sign executable
  run: |
    signtool sign /tr http://timestamp.digicert.com /fd sha256 dist/*.exe
```

#### macOS代码签名

```yaml
- name: Import certificate
  uses: apple-actions/import-codesign-certs@v1
  with:
    p12-file-base64: ${{ secrets.MACOS_CERTIFICATE }}
    p12-password: ${{ secrets.CERT_PASSWORD }}

- name: Sign app
  run: |
    codesign --force --sign "Developer ID Application: Your Name" dist/*.app
```

## 故障排除

### 常见问题

1. **构建失败**
   - 检查Python代码语法
   - 确认所有依赖文件存在
   - 查看工作流日志详细信息

2. **图标生成失败**
   - 确认Pillow库正确安装
   - 检查图标生成脚本权限

3. **安装包创建失败**
   - Windows: 检查Inno Setup配置
   - macOS: 确认create-dmg工具可用

4. **发布失败**
   - 确认标签格式正确（`v*`）
   - 检查仓库权限设置

### 调试技巧

1. **启用详细日志**
   在工作流中添加：
   ```yaml
   env:
     ACTIONS_RUNNER_DEBUG: true
   ```

2. **本地复现问题**
   使用相同的命令在本地运行构建脚本

3. **查看构建产物**
   下载Artifacts查看详细的构建结果

## 许可证和分发

- 构建的应用程序继承源代码的许可证
- 确保第三方依赖的许可证兼容性
- 考虑添加许可证文件到安装包中

## 进阶配置

### 矩阵构建扩展

可以扩展构建矩阵以支持更多平台：

```yaml
strategy:
  matrix:
    include:
      - os: windows-latest
        platform: windows
      - os: macos-latest
        platform: macos
      - os: ubuntu-latest
        platform: linux
```

### 条件构建

根据变更的文件决定是否构建：

```yaml
- name: Check changes
  uses: dorny/paths-filter@v2
  id: changes
  with:
    filters: |
      app:
        - '*.py'
        - 'requirements.txt'
```

### 缓存优化

缓存Python依赖以加速构建：

```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
``` 