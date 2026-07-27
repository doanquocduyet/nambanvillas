# -*- coding: utf-8 -*-
"""
Bóc dữ liệu chung từ trang tin (HTML) — DÙNG CHUNG cho fb-auto-post.py và lam-video.py.
Gộp về 1 chỗ để không lặp code 2 nơi.
"""
import re

SITE = "https://nambanvillas.vn"


def clean(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#8211;", "–")
    return re.sub(r"\s+", " ", t).strip()


def og(html, prop):
    """Lấy nội dung meta property (og:title, og:image, og:description...)."""
    m = re.search(
        r'<meta[^>]+property=["\']' + re.escape(prop) + r'["\'][^>]+content=["\']([^"\']+)["\']',
        html)
    return m.group(1).strip() if m else ""


def extract_specs(html):
    """Bảng <table class="specs-table"> -> [(nhãn, giá trị), ...]."""
    m = re.search(r'<table class="specs-table">(.*?)</table>', html, re.S)
    if not m:
        return []
    pairs = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S):
        cells = [clean(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        cells = [c for c in cells if c != ""]
        for i in range(0, len(cells) - 1, 2):
            pairs.append((cells[i], cells[i + 1]))
    return pairs


def extract_desc(html):
    """Đoạn 'Mô Tả' (các <p> giữa 'Mô Tả' và mục kế)."""
    i = html.find("Mô Tả")
    if i == -1:
        return ""
    j = re.search(r"<h[23]", html[i + 5:])
    seg = html[i:i + 5 + (j.start() if j else 4000)]
    ps = [clean(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", seg, re.S)]
    ps = [p for p in ps if len(p) > 20]
    return "\n\n".join(ps)


def gallery_rels(html, slug):
    """Đường dẫn tương đối các ảnh gallery của tin (theo thứ tự, bỏ trùng)."""
    rels, seen = [], set()
    for rel in re.findall(
            r'images/listings/' + re.escape(slug) + r'/[^"\')\s]+\.(?:jpg|jpeg|png|webp)', html, re.I):
        if rel not in seen:
            seen.add(rel); rels.append(rel)
    return rels
