# Deepseek API Client for Linux (Ubuntu)

适用于 Linux (Ubuntu) 的 Deepseek 官方 API 调用客户端，本版本采用纯 Python 实现，**与 macOS/Windows 共用一套 GUI 和 CLI 源码**，通过 Tkinter 提供图形界面，开箱即用。

## 项目定位

- **极简设计**：只关注 Deepseek API 调用与会话管理
- **跨平台统一代码**：Linux 与 macOS/Windows 共享 `src/` 下的核心实现
- **双模式支持**：同时提供 GUI（图形界面）和 CLI（命令行）两种使用方式
- **会话/历史管理**：支持创建会话、查看/编辑/删除历史对话

> 提示：`for-linux` 目录仅用于存放本平台说明文档，实际运行请在上一级目录（包含 `src/` 的目录）中完成。

## 环境要求

- Python 3.7+
- pip（Python 包管理器）
- Tkinter（大部分桌面版 Ubuntu 已内置，如缺失可通过发行版包管理器安装）

示例（Ubuntu/Debian 系）：

```bash
sudo apt update
sudo apt install python3-tk -y
```

## 安装依赖

在包含 `src/` 的项目根目录下（`for-linux` 的上一级目录）执行：

```bash
pip3 install -r requirements.txt
```

依赖非常精简，仅包含：

```text
requests
```

## 运行方式

在项目根目录（包含 `src/` 的目录）下执行以下命令：

### GUI 模式（推荐）

```bash
python3 src/gui_main.py
```

### CLI 模式

```bash
python3 src/cli_main.py
```

## GUI 说明（Linux 兼容重点）

Linux GUI 版本基于 Tkinter，界面布局与 macOS/Windows 保持一致，并针对字体做了跨平台兼容性处理：

- 优先尝试常见开源中文字体（如 `Noto Sans CJK SC`）
- 回退到常见中文黑体（如 `SimHei`、`Microsoft YaHei`）
- 最终回退到通用英文字体（如 `Arial`），确保界面可正常显示

因此在大多数桌面 Linux 发行版上，不需要额外为本程序单独配置字体即可正常使用。

## 功能特性概览

- **会话管理**：创建/删除/切换会话，默认会话不可删除
- **聊天功能**：发送消息、查看历史、编辑/删除历史消息（部分编辑功能在 GUI 中为弹窗形式）
- **配置管理**：设置 API Key，调整 `temperature`、`max_tokens`、`top_p` 等参数
- **错误处理**：API/网络错误会以系统消息形式写入当前会话，便于排查

## 维护与扩展

Linux 版本与其他平台共享核心 Python 代码，后续如有新功能（如代理设置、导出聊天记录、多语言界面等），会统一在 `src/` 目录中演进，Linux 端可自动获得更新。

如果你在特定 Linux 发行版上遇到兼容性问题（尤其是 GUI/字体相关），建议：

- 先确认已安装 Tkinter 与基础中文字体
- 在 Issue 中补充发行版名称、桌面环境、Python 版本及错误信息

## 许可证

本项目采用 MIT 许可证，详见上一级目录中的 `LICENSE` 文件。
