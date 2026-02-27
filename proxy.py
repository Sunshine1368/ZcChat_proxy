from flask import Flask, request, jsonify
import requests
import os
import sys

app = Flask(__name__)

def get_api_key():
    """从同目录下的 api.txt 文件中读取 API Key"""
    # 获取可执行文件所在目录（兼容打包后的路径）
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    api_file = os.path.join(base_path, 'api.txt')
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            key = f.read().strip()
            if not key:
                raise ValueError("api.txt 文件为空")
            return key
    except FileNotFoundError:
        print(f"错误：找不到 {api_file} 文件，请在程序同目录下创建 api.txt 并写入你的 DeepSeek API Key")
        sys.exit(1)
    except Exception as e:
        print(f"读取 API Key 失败：{e}")
        sys.exit(1)

DEEPSEEK_API_KEY = get_api_key()

@app.route('/v1/chat/completions', methods=['POST'])
def proxy_chat():
    try:
        openai_req = request.get_json()
        deepseek_payload = openai_req.copy()
        deepseek_payload['model'] = 'deepseek-chat'  # 强制使用 DeepSeek 模型
        
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        # 关键修改：禁用系统代理（解决代理错误）
        deepseek_resp = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            json=deepseek_payload,
            headers=headers,
            timeout=30,
            proxies={'http': None, 'https': None}  # 禁用代理
        )
        deepseek_resp.raise_for_status()
        return jsonify(deepseek_resp.json())
    
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if e.response:
            try:
                error_msg = e.response.json()
            except:
                error_msg = e.response.text
        print('DeepSeek 请求失败:', error_msg)
        return jsonify({'error': 'DeepSeek API 请求失败'}), 500
    except Exception as e:
        print('代理内部错误:', str(e))
        return jsonify({'error': '代理服务器内部错误'}), 500

if __name__ == '__main__':
    print("DeepSeek 代理启动成功，监听地址：http://127.0.0.1:8080")
    print("请确保同目录下的 api.txt 文件包含你的 DeepSeek API Key")
    app.run(host='0.0.0.0', port=8080, debug=False)