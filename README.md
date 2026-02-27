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
- DeepSeek 代理启动成功，监听地址：http://127.0.0.1:8080
请确保同目录下的 api.txt 文件包含你的 DeepSeek API Key

Running on all addresses (0.0.0.0)

Running on http://127.0.0.1:8080
- **保持此窗口一直开着**（最小化即可），关闭窗口代理即停止。

### 4️⃣ 配置 ZcChat
打开 ZcChat，进入 **AI模型配置**，按以下填写：
- **BaseUrl / openai URL**：`http://127.0.0.1:8080/v1/chat/completions`
- **APIKey**：任意填写，例如 `sk-dummy`（代理不检查此项）
- **Model**：任意填写，例如 `gpt-3.5-turbo`（代理会自动替换为 `deepseek-chat`）

其他选项保持默认即可。保存配置后，重启 ZcChat（重要！）。

### 5️⃣ 开始聊天
在对话框中输入消息，如果一切正常，你将收到来自 DeepSeek 的回复。代理命令行窗口也会显示请求日志。

## ❓ 常见问题

### Q: 运行时提示“找不到 api.txt”怎么办？
A: 请确认 `api.txt` 和 `DeepSeekProxy.exe` 在**同一个文件夹**中，且文件名完全一致（注意大小写和扩展名 `.txt`）。

### Q: 提示“API Key 无效”或返回错误？
A: 
- 检查 `api.txt` 中的 Key 是否正确（建议重新复制，注意不要有空格）。
- 确认 DeepSeek 账户余额充足（免费用户有一定额度）。
- 可以用 curl 命令单独测试 Key 是否有效（见下方“测试 Key”）。

### Q: 代理启动后，ZcChat 仍然报错？
A:
- 检查 ZcChat 中的 **openai URL** 是否填写为 `http://127.0.0.1:8080/v1/chat/completions`（注意是完整路径）。
- 确保 ZcChat 已重启。
- 查看代理命令行窗口是否有红色错误信息，如果有，请根据错误提示排查（如网络代理问题）。

### Q: 我的电脑需要代理才能访问外网，怎么办？
A: 目前脚本默认**禁用系统代理**（避免常见的代理错误）。如果你必须使用代理才能访问 DeepSeek，请手动修改脚本（需懂一点 Python）或联系我们获取定制版。

### Q: 如何测试代理本身是否工作正常？
A: 在命令行中执行（Windows 的 cmd 或 PowerShell）：
```bash
curl -X POST http://127.0.0.1:8080/v1/chat/completions ^
-H "Content-Type: application/json" ^
-d "{\"model\":\"gpt-3.5-turbo\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}"

如果返回包含 choices 字段的 JSON，说明代理正常。

⚠️ 注意事项
安全：api.txt 中包含你的 API Key，请勿将该文件分享给他人。

防火墙：首次运行可能弹出 Windows 防火墙警告，请允许 DeepSeekProxy.exe 访问网络。

资源占用：代理占用内存极小，可长期运行。

停止代理：直接关闭命令行窗口即可。

🔧 高级：自定义代理端口
如果你需要修改端口（例如 8080 被占用），可联系我们获取修改版，或自行用 Python 脚本修改（需安装 Python 环境）。

如果还有任何问题，欢迎随时反馈！祝你使用愉快 🎉
