from flask import Flask, request, jsonify
import requests
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import win32event, win32api, winerror
from win32event import CreateMutex

# ------------------ 全局配置 ------------------
app = Flask(__name__)
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proxy.log')
API_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api.txt')

# ------------------ 日志设置 ------------------
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=2)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

# 禁用 Flask 默认的控制台输出
logging.getLogger('werkzeug').disabled = True

# ------------------ 单实例检测 ------------------
mutex_name = "Global\\DeepSeekProxy_Instance_Mutex"
mutex = CreateMutex(None, False, mutex_name)
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    logging.error("程序已经在运行中，请勿重复启动。")
    sys.exit(1)

# ------------------ API Key 获取/输入窗口 ------------------
def get_api_key_interactive():
    """弹出输入窗口让用户输入 API Key，保存到 api.txt，返回 Key"""
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("DeepSeek 代理", "未找到 api.txt 文件，请在弹出的窗口中输入你的 DeepSeek API Key。")

    while True:
        key = simpledialog.askstring(
            "输入 API Key",
            "请输入你的 DeepSeek API Key（以 sk- 开头）：\n(输入后会自动保存到 api.txt，取消则退出程序)",
            parent=root
        )
        if key is None:
            logging.info("用户取消了输入，程序退出。")
            sys.exit(0)
        key = key.strip()
        if key.startswith('sk-') and len(key) > 10:
            break
        else:
            messagebox.showerror("错误", "API Key 格式似乎不正确，请重新输入（应以 sk- 开头）。")

    try:
        with open(API_FILE, 'w', encoding='utf-8') as f:
            f.write(key)
        messagebox.showinfo("成功", f"API Key 已保存到 {API_FILE}\n代理将在后台继续运行。")
    except Exception as e:
        messagebox.showerror("错误", f"保存文件失败：{e}")
        logging.error(f"保存 API Key 失败：{e}")
        sys.exit(1)

    root.destroy()
    return key

def get_api_key():
    """如果 api.txt 存在则读取，否则弹出窗口获取"""
    if os.path.exists(API_FILE):
        try:
            with open(API_FILE, 'r', encoding='utf-8') as f:
                key = f.read().strip()
                if key:
                    return key
                else:
                    logging.warning("api.txt 文件为空，将弹出输入窗口")
                    return get_api_key_interactive()
        except Exception as e:
            logging.error(f"读取 api.txt 失败：{e}，将弹出输入窗口")
            return get_api_key_interactive()
    else:
        return get_api_key_interactive()

DEEPSEEK_API_KEY = get_api_key()
logging.info("API Key 加载成功")

# ------------------ Flask 代理路由 ------------------
@app.route('/v1/chat/completions', methods=['POST'])
def proxy_chat():
    try:
        openai_req = request.get_json()
        deepseek_payload = openai_req.copy()
        deepseek_payload['model'] = 'deepseek-chat'

        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }

        # 不再强制禁用代理，让 requests 自动使用系统环境变量 HTTP_PROXY/HTTPS_PROXY
        deepseek_resp = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            json=deepseek_payload,
            headers=headers,
            timeout=30
        )
        deepseek_resp.raise_for_status()
        return jsonify(deepseek_resp.json())

    except requests.exceptions.ProxyError as e:
        error_msg = f"代理错误: {str(e)}。请检查系统代理设置或暂时关闭代理软件。"
        logging.error(error_msg)
        return jsonify({'error': error_msg}), 500
    except requests.exceptions.ConnectionError as e:
        error_msg = f"连接错误: {str(e)}。请检查网络连接。"
        logging.error(error_msg)
        return jsonify({'error': error_msg}), 500
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if e.response:
            try:
                error_msg = e.response.json()
            except:
                error_msg = e.response.text
        logging.error(f'DeepSeek 请求失败: {error_msg}')
        return jsonify({'error': f'DeepSeek API 请求失败: {error_msg}'}), 500
    except Exception as e:
        logging.error(f'代理内部错误: {str(e)}')
        return jsonify({'error': '代理服务器内部错误'}), 500

# ------------------ 启动 Flask（后台运行） ------------------
def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)

if __name__ == '__main__':
    logging.info("DeepSeek 代理启动成功，监听地址：http://127.0.0.1:8080")
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    flask_thread.join()