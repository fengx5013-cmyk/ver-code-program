# 获取验证码：前端 + Python 后端（Flask + Playwright）

## 目录
- static/index.html  前端页面（黑金粒子风格）
- server.py          Flask 服务：提供 / 和 /proxy/code
- Verif_code_acquire.py  Playwright 抓取验证码逻辑（可被 server.py 调用）

## 安装
```bash
pip install -r requirements.txt
playwright install chromium
```

## 运行
```bash
python server.py
```

浏览器打开：
- http://127.0.0.1:8000/
- 或带参数自动填入 token：http://127.0.0.1:8000/?token=123abcTE

## 配置目标页面
Verif_code_acquire.py 默认打开：
  http://43.161.219.197:5566/index.html?

你可以用环境变量覆盖：
```bash
# Windows PowerShell
$env:VERIF_PAGE_URL="http://example.com/whatever"
python server.py

# macOS/Linux
export VERIF_PAGE_URL="http://example.com/whatever"
python server.py
```
