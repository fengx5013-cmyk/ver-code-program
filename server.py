from __future__ import annotations

import threading
from flask import Flask, jsonify, request, send_from_directory

from Verif_code_acquire import acquire_verification_code

app = Flask(__name__, static_folder="static", static_url_path="")
_lock = threading.Lock()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index02.html")


@app.get("/proxy/code")
def proxy_code():
    token = (request.args.get("token") or "").strip()
    if not token:
        return jsonify({"error": "请输入 Token"}), 400

    # Playwright 启动浏览器很重，先加个锁，避免并发把机器打满
    with _lock:
        try:
            code = acquire_verification_code(token, headless=True)
            return jsonify({"code": code})
        except Exception as e:
            # 前端会把 error 展示在状态栏
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # 默认跑在 8000，避免跟你脚本里访问的 5566 端口撞车
    app.run(host="0.0.0.0", port=8000, debug=False)
    #app.run(host="127.0.0.1", port=5050, debug=False)


