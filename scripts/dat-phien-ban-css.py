#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐÓNG DẤU PHIÊN BẢN VÀO CSS/JS — để sửa giao diện là khách thấy NGAY.

ĐÃ TỪNG DÍNH (chủ chụp màn hình 2 lần, lần sau vẫn y nguyên lần trước):
vercel.json đặt /css/* và /js/* là `max-age=86400, stale-while-revalidate=604800`.
Tên file không bao giờ đổi, nên sau khi sửa CSS:
  - máy khách đã vào web rồi sẽ dùng bản CŨ tới 24 tiếng
  - kéo-xuống-refresh trên iPhone KHÔNG tải lại file css
  - còn stale-while-revalidate kéo dài thêm tới 7 ngày
=> Sửa xong, đẩy lên, mà chủ nhìn vẫn "vẫn vậy".

CÁCH CHỮA (cách mọi web lớn dùng): gắn ?v=<vân tay nội dung> vào đường dẫn.
Nội dung đổi -> vân tay đổi -> địa chỉ file đổi -> trình duyệt buộc tải bản mới,
mà vẫn giữ được cache dài cho lần sau. Không phải sửa vercel.json.

Chạy sau MỖI lần sửa css/ hoặc js/:
    python3 scripts/dat-phien-ban-css.py
"""
import glob
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TAI_SAN = ["css/style.css", "css/article.css", "js/main.js"]


def van_tay(p):
    return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]


def main():
    v = {p: van_tay(p) for p in TAI_SAN if os.path.exists(p)}
    for p, h in v.items():
        print("  %-18s v=%s" % (p, h))

    # khớp mọi kiểu đường dẫn đang dùng: /css/style.css, ../css/…, ../../css/…, css/…
    pat = re.compile(
        r'((?:href|src)=")((?:\.\./)*/?(?:css/(?:style|article)\.css|js/main\.js))(\?v=[0-9a-f]+)?(")')

    n_trang = n_sua = 0
    # ĐÃ TỪNG DÍNH (css404-1): chỉ quét **/index.html nên 404.html ở gốc mãi không có ?v=
    for f in sorted(glob.glob("**/*.html", recursive=True)):
        if f.startswith(("node_modules", "docs")):
            continue
        s = open(f, encoding="utf-8").read()
        dem = [0]

        def thay(m):
            duong = m.group(2)
            ten = re.sub(r"^(?:\.\./)*/?", "", duong)   # -> css/style.css
            if ten not in v:
                return m.group(0)
            moi = "%s%s?v=%s%s" % (m.group(1), duong, v[ten], m.group(4))
            if moi != m.group(0):
                dem[0] += 1
            return moi

        s2 = pat.sub(thay, s)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            n_trang += 1
            n_sua += dem[0]
    print("\nĐóng dấu %d đường dẫn / %d trang." % (n_sua, n_trang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
