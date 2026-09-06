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
    "dat-nen-nam-ban/index.html",
    "cum-moi-nam-ban/index.html",
    "nha-ban-nam-ban/index.html",
    "thi-truong/index.html",
]
VN = timezone(timedelta(hours=7))  # Asia/Ho_Chi_Minh (không DST)

def update_file(path: str, want: str, today: str) -> int:
    try:
        html = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"Không thấy {path} — bỏ qua.", file=sys.stderr)
        return 0
    orig = html
    # 1) Đổi mốc tháng ('Tháng 9/2026' hoặc kiểu cũ 'T9/2026') trong <title>, og:title, twitter:title, <h1>
    pat = r"(?i)(?:tháng\s*|T)\d{1,2}/\d{4}"
    def rep(m):
        s = m.group(0)
        return want.replace("Tháng", "tháng", 1) if s[:1] == "t" else want  # giữ hoa/thường như cũ
    for tag in (r"<title>.*?</title>", r'<meta property="og:title"[^>]*>', r'<meta name="twitter:title"[^>]*>', r"<h1[^>]*>.*?</h1>"):
        html = re.sub(tag, lambda m: re.sub(pat, rep, m.group(0)), html, count=1, flags=re.S)
    # 1b) Nhãn tươi mới "Cập nhật tháng N/YYYY" ở bất kỳ đâu
    html = re.sub(r"(?i)(Cập nhật )tháng\s*\d{1,2}/\d{4}", lambda m: m.group(1) + want.replace("Tháng", "tháng", 1), html)
    # 2) Cập nhật dateModified trong schema
    html = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', f'"dateModified":"{today}"', html)
    if html == orig:
        print(f"{path}: đã đúng ({want} · {today}) — không đổi.")
        return 0
    open(path, "w", encoding="utf-8").write(html)
    print(f"{path}: cập nhật → {want} · {today}.")
    return 1

def main() -> int:
    now = datetime.now(VN)
    want = f"Tháng {now.month}/{now.year}"
    today = now.strftime("%Y-%m-%d")
    for f in HUBS:
        update_file(f, want, today)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
