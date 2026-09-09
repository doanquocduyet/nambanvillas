#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm FB_PAGE_TOKEN đang dùng là loại gì và làm được những gì.

Vì sao cần: Graph API Explorer cho ra HAI loại mã trông y hệt nhau —
mã Người dùng (User token) và mã Trang (Page token). Dán nhầm mã Người dùng
thì đăng bài trả 403 mà không nói rõ lý do. File này chỉ ra ngay nhầm ở đâu.

TUYỆT ĐỐI KHÔNG in mã token ra log.
Chạy: python3 scripts/fb-kiem-token.py
"""
import os, sys, json, ssl
import urllib.request, urllib.parse, urllib.error

GRAPH = "https://graph.facebook.com/v21.0"
CTX = ssl.create_default_context()
UA = {"User-Agent": "NamBanVillas-KiemToken/1.0"}


def get(path, params):
    url = GRAPH + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def loi(e):
    try:
        d = json.loads(e.read().decode("utf-8", "ignore"))
        return d.get("error", {}).get("message", "")[:200]
    except Exception:
        return str(e)


def main():
    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if not token:
        print("Chưa có FB_PAGE_TOKEN trong secrets.")
        return 0

    print("=" * 60)
    print("KIỂM MÃ TOKEN ĐANG DÙNG")
    print("=" * 60)

    # 1. Mã này là của ai?
    try:
        me = get("/me", {"fields": "id,name", "access_token": token})
        print("Tên chủ mã   :", me.get("name"))
        print("ID           :", me.get("id"))
    except urllib.error.HTTPError as e:
        print("Mã không dùng được:", loi(e))
        return 0

    # 2. Là mã Trang hay mã Người dùng?
    la_trang = None
    try:
        # Chỉ mã Người dùng mới liệt kê được danh sách Trang
        acc = get("/me/accounts", {"fields": "name,id", "access_token": token})
        ds = acc.get("data", [])
        la_trang = False
        print("\nLOẠI MÃ      : MÃ NGƯỜI DÙNG  <-- SAI, cần mã Trang")
        if ds:
            print("Mã này quản lý các Trang sau:")
            for p in ds:
                print("   -", p.get("name"), "(id", p.get("id") + ")")
    except urllib.error.HTTPError:
        la_trang = True
        print("\nLOẠI MÃ      : MÃ TRANG  <-- ĐÚNG")

    # 3. Thử từng việc thật (không đăng gì, chỉ đọc)
    print("\nLÀM ĐƯỢC GÌ:")
    viec = [
        ("Đọc danh sách bài đã đăng", "/me/posts", {"limit": 1}),
        ("Đọc bình luận",             "/me/feed",  {"limit": 1, "fields": "comments.limit(1)"}),
    ]
    for ten, path, extra in viec:
        p = dict(extra); p["access_token"] = token
        try:
            get(path, p)
            print("   OK   ", ten)
        except urllib.error.HTTPError as e:
            print("   HỎNG ", ten, "->", loi(e))

    print("\n" + "=" * 60)
    if la_trang is False:
        print("CÁCH SỬA: vào Graph API Explorer, gõ vào ô địa chỉ:")
        print("    me/accounts?fields=name,access_token")
        print("bấm Gửi, rồi copy chuỗi access_token của Trang Namban Villas")
        print("(KHÔNG phải mã đang dán hiện tại) và cập nhật lại secret FB_PAGE_TOKEN.")
    else:
        print("Mã đúng loại. Nếu vẫn có việc HỎNG ở trên thì là thiếu quyền, không phải sai mã.")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
