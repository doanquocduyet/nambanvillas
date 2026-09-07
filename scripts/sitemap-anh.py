#!/usr/bin/env python3
"""Bơm ảnh vào sitemap.xml (Google Image Sitemap).

Google chỉ còn đọc <image:loc> — image:title/caption/license đã bỏ từ 2022,
nên script chỉ ghi image:loc cho gọn và đúng chuẩn hiện hành.

Chạy: python3 scripts/sitemap-anh.py
Chạy lại nhiều lần vô hại — ảnh cũ bị xoá và ghi lại theo HTML hiện tại.
"""
import os, re, sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://nambanvillas.vn"
# Ảnh giao diện, không phải ảnh nội dung — không đưa vào sitemap
BO_QUA = ("/images/logo", "/images/icon", "favicon", ".svg", "/images/og-")


def duong_dan_file(url):
    p = url[len(SITE):].strip("/")
    return os.path.join(GOC, p, "index.html") if p else os.path.join(GOC, "index.html")


def anh_trong_trang(html_path):
    if not os.path.exists(html_path):
        return []
    s = open(html_path, encoding="utf-8").read()
    ra, thay = [], set()
    for src in re.findall(r'<img[^>]+src="([^"]+)"', s):
        if not src or src.startswith("data:"):
            continue
        if src.startswith("http"):
            u = src
        else:
            # ../images/x.jpg và /images/x.jpg đều quy về gốc site
            u = SITE + "/" + src.lstrip("./").lstrip("/")
        if not u.startswith(SITE):
            continue
        if any(b in u for b in BO_QUA):
            continue
        # Chỉ nhận ảnh có thật trên đĩa — loại chuỗi ghép trong JS, link hỏng
        if not os.path.exists(os.path.join(GOC, u[len(SITE):].lstrip("/"))):
            continue
        if u not in thay:
            thay.add(u)
            ra.append(u)
    return ra


def main():
    sm = os.path.join(GOC, "sitemap.xml")
    s = open(sm, encoding="utf-8").read()

    if "xmlns:image" not in s:
        s = s.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
        )

    khoi = re.findall(r"<url>.*?</url>", s, re.S)
    tong_anh = 0
    trang_co_anh = 0
    for k in khoi:
        loc = re.search(r"<loc>([^<]+)</loc>", k).group(1)
        anh = anh_trong_trang(duong_dan_file(loc))
        # bỏ phần image cũ, dựng lại
        sach = re.sub(r"<image:image>.*?</image:image>", "", k, flags=re.S)
        sach = sach.replace("</url>", "").rstrip()
        if anh:
            trang_co_anh += 1
            tong_anh += len(anh)
            them = "".join(
                "\n    <image:image><image:loc>%s</image:loc></image:image>" % u.replace("&", "&amp;")
                for u in anh
            )
            moi = sach + them + "\n  </url>"
        else:
            moi = sach + "</url>"
        s = s.replace(k, moi, 1)

    open(sm, "w", encoding="utf-8").write(s)
    print("Đã ghi sitemap: %d trang có ảnh, %d ảnh." % (trang_co_anh, tong_anh))


if __name__ == "__main__":
    sys.exit(main())
