# Deepseek API Client

一个极简的 Deepseek 官方 API 调用客户端，支持 macOS、Windows 和 Linux (Ubuntu) 三大平台，提供 GUI 和 CLI 两种使用方式。

## 项目结构

```
Deepseek-API-Client/
├── for-macos/          # macOS 版本
├── for-windows/        # Windows 版本
├── for-linux/          # Linux (Ubuntu) 版本
├── LICENSE             # 许可证文件
└── README.md           # 本说明文档
```

## 项目定位

- **极简设计**：专注于核心功能，避免不必要的复杂性
- **跨平台支持**：完美适配 macOS、Windows 和 Linux (Ubuntu)
- **双模式支持**：同时提供 GUI（图形界面）和 CLI（命令行）两种使用方式
- **会话管理**：支持创建、切换、删除会话
- **历史记录编辑**：支持查看、编辑、删除历史对话记录
- **API 参数配置**：支持调整 API 调用参数（如温度、最大 tokens 等）

## 各平台使用说明

### macOS 版本

进入 `for-macos` 目录使用。

#### 安装依赖
```bash
pip3 install requests
```

#### 运行方式

**GUI 模式：**
```bash
python3 src/gui_main.py
```

**CLI 模式：**
```bash
python3 src/cli_main.py
```

---

### Windows 版本

进入 `for-windows` 目录使用。

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 运行方式

**GUI 模式（推荐）：**
直接双击 `启动GUI.bat` 文件，或在命令行运行：
```bash
python src\gui_main.py
```

**CLI 模式：**
直接双击 `启动CLI.bat` 文件，或在命令行运行：
```bash
python src\cli_main.py
```

---

### Linux (Ubuntu) 版本

Linux 版本基于与 macOS/Windows 相同的 Python 源码实现，主要通过 Tkinter 提供 GUI 界面，无需额外原生编译。

#### 安装依赖
```bash
# 在项目根目录（包含 src/ 的目录）下执行
pip3 install -r requirements.txt
```

#### 运行方式

**GUI 模式：**
```bash
python3 src/gui_main.py
```

**CLI 模式：**
```bash
python3 src/cli_main.py
```

如需仅查看平台说明，可进入 `for-linux` 目录阅读 `README.md`。

---

## 功能特性

### 1. 会话管理
- 创建新会话
- 切换会话
- 删除会话（默认会话不可删除）
- 查看所有会话

### 2. 聊天功能
- 发送消息
- 查看聊天历史
- 编辑历史消息
- 删除历史消息
- 支持多行输入

### 3. 配置管理
- 修改 API 密钥
- 调整模型参数（温度、最大 tokens、top_p 等）
- 查看当前配置

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 注意

本项目仅供学习和研究使用，请遵守 Deepseek API 的使用条款和相关法律法规。

本项目仅供学习和研究使用，请遵守 Deepseek API 的使用条款和相关法律法规和相关法律法规。
