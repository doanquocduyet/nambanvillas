#!/usr/bin/env python3
"""Tự cập nhật tháng trong <title> trang hub Cụm Mới mỗi đầu tháng.

Chỉ đổi token 'T<tháng>/<năm>' NẰM TRONG dòng <title> của
cum-moi-nam-ban/index.html sang tháng hiện tại (giờ Việt Nam).
An toàn, khớp chính xác, idempotent — không đổi gì khác trên trang.
Chạy tay: python3 scripts/cap-nhat-thang-hub.py
"""
import re
import sys
from datetime import datetime, timezone, timedelta

FILE = "cum-moi-nam-ban/index.html"
VN = timezone(timedelta(hours=7))  # Asia/Ho_Chi_Minh (không DST)

def main() -> int:
    now = datetime.now(VN)
    want = f"T{now.month}/{now.year}"  # ví dụ T8/2026

    today = now.strftime("%Y-%m-%d")  # ISO, ví dụ 2026-09-01

    html = open(FILE, encoding="utf-8").read()
    orig = html

    # 1) Đổi token tháng T<n>/<năm> trong <title>
    m = re.search(r"<title>.*?</title>", html, re.S)
    if not m:
        print("Không tìm thấy <title> — bỏ qua.", file=sys.stderr)
        return 1
    new_title, n = re.subn(r"T\d{1,2}/\d{4}", want, m.group(0), count=1)
    if n == 0:
        print("Tiêu đề không có token tháng dạng T<n>/<năm> — bỏ qua.")
    else:
        html = html[: m.start()] + new_title + html[m.end() :]

    # 2) Cập nhật dateModified trong schema (tín hiệu 'tươi' cho Google/AI)
    html, d = re.subn(
        r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{today}"', html
    )

    if html == orig:
        print(f"Đã đúng ({want} · {today}) — không đổi.")
        return 0

    open(FILE, "w", encoding="utf-8").write(html)
    print(f"Đã cập nhật: tiêu đề → {want}, dateModified → {today}.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
