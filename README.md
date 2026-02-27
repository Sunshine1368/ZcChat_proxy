# DeepSeek 代理 for ZcChat 使用说明

## 📌 简介
这是一个本地代理程序，用于将 ZcChat 软件对 OpenAI API 的调用**无缝转发**到 DeepSeek API。通过此代理，你可以在 ZcChat 中使用 DeepSeek 模型，无需 OpenAI 账户。

## 📁 文件说明
下载后你会得到两个文件，请放在**同一个文件夹**中：
- `DeepSeekProxy.exe` – 代理程序
- `api.txt` – 用于存放你的 DeepSeek API Key 的文本文件

## 🚀 快速开始

### 1️⃣ 获取 DeepSeek API Key
- 访问 [DeepSeek 开放平台](https://platform.deepseek.com/) 并登录/注册。
- 进入控制台，创建一个 API Key，复制（以 `sk-` 开头的一串字符）。

### 2️⃣ 创建 `api.txt`
- 在 `DeepSeekProxy.exe` 所在的文件夹中，新建一个名为 `api.txt` 的文本文件。
- 用记事本打开，将你复制的 API Key **完整粘贴进去**，保存。
  - **注意**：文件中只有这一行 Key，不要有多余的空格或换行。

### 3️⃣ 运行代理
- 双击 `DeepSeekProxy.exe`，会弹出一个命令行窗口，显示：