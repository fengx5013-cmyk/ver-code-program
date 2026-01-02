# 获取ver-code：前端 + Python 后端（Flask + Playwright）

## 目录
- static/index.html  前端页面（黑金粒子风格）
- server.py          Flask 服务：提供 / 和 /proxy/code
- Verif_code_acquire.py  Playwright 抓取code逻辑（可被 server.py 调用）

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
