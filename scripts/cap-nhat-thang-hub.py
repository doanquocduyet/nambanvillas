#!/usr/bin/env python3
"""Tự cập nhật tháng trong <title> các trang hub mỗi đầu tháng.

Với mỗi file trong HUBS: đổi token 'T<tháng>/<năm>' trong <title> sang
tháng hiện tại (giờ Việt Nam) và cập nhật mọi "dateModified" trong schema
sang ngày hôm nay — tín hiệu 'tươi' cho Google/AI.
An toàn, khớp chính xác, idempotent — không đổi gì khác trên trang.
Chạy tay: python3 scripts/cap-nhat-thang-hub.py
"""
import re
import sys
from datetime import datetime, timezone, timedelta

HUBS = [
    "cum-moi-nam-ban/index.html",
    "nha-ban-nam-ban/index.html",
]
VN = timezone(timedelta(hours=7))  # Asia/Ho_Chi_Minh (không DST)

def update_file(path: str, want: str, today: str) -> int:
    try:
        html = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"Không thấy {path} — bỏ qua.", file=sys.stderr)
        return 0
    orig = html

    # 1) Đổi token tháng T<n>/<năm> trong <title>
    m = re.search(r"<title>.*?</title>", html, re.S)
    if m:
        new_title, n = re.subn(r"T\d{1,2}/\d{4}", want, m.group(0), count=1)
        if n:
            html = html[: m.start()] + new_title + html[m.end() :]

    # 2) Cập nhật dateModified trong schema
    html = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"',
                  f'"dateModified":"{today}"', html)

    if html == orig:
        print(f"{path}: đã đúng ({want} · {today}) — không đổi.")
        return 0
    open(path, "w", encoding="utf-8").write(html)
    print(f"{path}: cập nhật → {want} · {today}.")
    return 1

def main() -> int:
    now = datetime.now(VN)
    want = f"T{now.month}/{now.year}"
    today = now.strftime("%Y-%m-%d")
    for f in HUBS:
        update_file(f, want, today)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
