from __future__ import annotations

import os
import re
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError


# 你原脚本里是直接打开这个页面：page.goto("http://43.161.219.197:5566/index.html?")。
# 这里保留为默认值，但你可以通过环境变量 VERIF_PAGE_URL 覆盖它。
DEFAULT_PAGE_URL = "http://43.161.219.197:5566/index.html?"
PAGE_URL = os.getenv("VERIF_PAGE_URL", DEFAULT_PAGE_URL)


def acquire_verification_code(
    token: str,
    *,
    page_url: str = PAGE_URL,
    headless: bool = True,
    timeout_ms: int = 15000,
    post_click_wait_ms: int = 3000,
) -> str:
    """用 Playwright 自动化获取 6 位验证码并返回。

    逻辑来源于你上传的脚本：填 token -> 点击“获取验证码” -> 从页面中提取 6 位数字。
    """
    token = (token or "").strip()
    if not token:
        raise ValueError("missing token")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        try:
            page = browser.new_page()
            page.goto(page_url, wait_until="load", timeout=timeout_ms)

            # 等待按钮出现（你原脚本也做了这个等待）
            page.wait_for_selector("text=获取验证码", timeout=timeout_ms)

            # 输入 token（你原脚本写死了 token，这里改成参数传入）
            page.locator("input").first.fill(token)

            # 点击“获取验证码”
            page.get_by_text("获取验证码", exact=False).first.click(timeout=timeout_ms)

            # 优先等“验证码结果”出现（如果目标页面就是你那套前端，会出现 .code-glow）
            try:
                page.wait_for_selector(".code-glow", timeout=timeout_ms)
                code_text = page.locator(".code-glow").first.inner_text().strip()
                if re.fullmatch(r"\d{6}", code_text):
                    return code_text
            except PWTimeoutError:
                # 退回到正则扫描 body
                pass

            # 给一点时间让页面渲染/跳转（保持你原脚本的思路）
            if post_click_wait_ms > 0:
                page.wait_for_timeout(post_click_wait_ms)

            text = page.locator("body").inner_text()
            numbers = re.findall(r"\b\d{6}\b", text)
            if not numbers:
                raise RuntimeError("未找到验证码（页面无 6 位数字）")
            return numbers[0]
        finally:
            browser.close()


if __name__ == "__main__":
    # 方便你单独测试：python Verif_code_acquire.py 123abcTE
    import sys

    t = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        code = acquire_verification_code(t, headless=False)
        print(code)
    except Exception as e:
        print(f"ERROR: {e}")
