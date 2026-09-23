#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIỂM MỌI NÚT BẤM & BỘ LỌC TRÊN TOÀN SITE.

Vì sao có script này: sửa tay từng chỗ rồi vẫn lòi lỗi chỗ khác, vì mỗi lần chỉ
kiểm đúng cái vừa đụng. Script này kiểm CẢ MỘT LOẠI trên MỌI TRANG, mỗi lần chạy.

Bắt 8 loại lỗi — đều là lỗi ĐÃ XẢY RA THẬT:
 1. Nút hiện ra nhưng JS bị chặn theo đường dẫn -> bấm không ăn gì
    (142 nút "So sánh" chết trên 6 trang khu vì main.js chặn ngoài 2 hub)
 2. Số ghi trên chip không khớp số thẻ lọc ra
 3. Thẻ thiếu data-* mà bộ lọc đọc -> lọc ẩn nhầm hàng thật
 4. Nút bật/tắt thiếu aria-pressed -> trình đọc màn hình mù
 5. Ô select/tìm thiếu nhãn
 6. Lọc xong không ghi vào URL -> không chia sẻ/lưu/back được
 7. Không có trạng thái rỗng -> khách nhìn màn hình trắng
 8. Lớp CSS bộ lọc dùng mà style.css không có -> giao diện vỡ

Chạy: python3 scripts/kiem-bo-loc.py
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

loi, canh = [], []
def L(m): loi.append(m)
def W(m): canh.append(m)

CSS = open("css/style.css", encoding="utf-8").read()
JS_CHUNG = open("js/main.js", encoding="utf-8").read()

pages = [f for f in glob.glob("**/index.html", recursive=True)
         if not f.startswith(("node_modules", "docs"))]


def duong(f):
    d = os.path.dirname(f)
    return "/%s/" % d if d else "/"


def js_cua(f, s):
    """Toàn bộ JS chạy trên trang: inline + main.js nếu có nạp."""
    j = " ".join(re.findall(r"<script(?![^>]*\ssrc=)[^>]*>([\s\S]*?)</script>", s))
    if re.search(r'src="[^"]*js/main\.js', s):
        j += "\n" + JS_CHUNG
    return j


def chan_theo_duong(js, d):
    """main.js có đoạn chặn 'không phải trang X thì thôi' — nút trên trang khác
    sẽ hiện mà không chạy. Trả True nếu trang này BỊ CHẶN."""
    for m in re.finditer(
            r"var\s+p\s*=\s*location\.pathname;\s*if\s*\((.{0,240}?)\)\s*return;", js, re.S):
        dk = m.group(1)
        cho = re.findall(r"p\.indexOf\('([^']+)'\)<0", dk)
        if cho and all(x not in d for x in cho):
            return cho
    return None


# ── quét từng trang ────────────────────────────────────────────────────────
for f in sorted(pages):
    s = open(f, encoding="utf-8").read()
    d = duong(f)
    js = js_cua(f, s)

    # (1) nút So sánh hiện ra mà JS bị chặn theo đường dẫn
    n_cmp = s.count('class="cmp-btn"')
    if n_cmp:
        bi = chan_theo_duong(js, d)
        if bi:
            L("[%d nút 'So sánh' hiện ra nhưng JS chặn ngoài %s — bấm không ăn gì] %s"
              % (n_cmp, "/".join(bi), d))

    # thẻ lô trên trang
    the = re.findall(r'<article class="prop-card[^>]*>', s)
    dang_ban = [t for t in the if 'data-ban="1"' not in t]

    # (2) số trên chip vs số thẻ lọc ra
    for kind in ("loc", "nhan"):
        for m in re.finditer(
                r'<button[^>]*class="(?:lc-chip|nb-khu)[^"]*"([^>]*)>([\s\S]{0,120}?)</button>', s):
            at, nhan = m.group(1), m.group(2)
            mv = re.search(r'data-%s="([^"]*)"' % kind, at)
            if not mv:
                continue
            v = mv.group(1)
            txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", nhan)).strip()
            mn = re.search(r"(\d+)\s*$", txt)
            if not mn:
                continue
            ghi = int(mn.group(1))
            if v == "":
                that = len(dang_ban)
            else:
                that = sum(1 for t in dang_ban
                           if re.search(r'data-%s="[^"]*\b%s\b' % (kind, re.escape(v)), t))
            if ghi != that:
                L("[Chip ghi %d nhưng lọc ra %d] %s — chip \"%s\"" % (ghi, that, d, txt))

            # (4) nút bật/tắt phải có aria-pressed
            if "aria-pressed" not in at:
                L("[Chip thiếu aria-pressed — trình đọc màn hình không biết chip nào đang bật] %s — \"%s\""
                  % (d, txt))

    # (3) thẻ thiếu data-* mà bộ lọc trên trang đọc tới
    doc = set()
    for k in ("area", "price", "loc", "ban", "nhan"):
        if re.search(r"getAttribute\(['\"]data-%s['\"]\)|dataset\.%s\b" % (k, k), js):
            doc.add(k)
    if the and doc:
        for k in sorted(doc - {"ban", "nhan"}):   # ban/nhan vắng = hợp lệ
            thieu = [t for t in the if "data-%s=" % k not in t]
            if thieu:
                L("[%d/%d thẻ thiếu data-%s — bộ lọc sẽ ẩn nhầm hàng thật] %s"
                  % (len(thieu), len(the), k, d))

    # (5) ô select / ô tìm phải có nhãn
    for m in re.finditer(r"<select[^>]*>", s):
        t = m.group(0)
        mid = re.search(r'id="([^"]*)"', t)
        co_label = mid and re.search(r'<label[^>]*for="%s"' % re.escape(mid.group(1)), s)
        if "aria-label" not in t and not co_label:
            L("[Ô chọn thiếu nhãn (aria-label hoặc <label for>)] %s: %s" % (d, t[:70]))
    for m in re.finditer(r'<input[^>]*type="search"[^>]*>', s):
        t = m.group(0)
        mid = re.search(r'id="([^"]*)"', t)
        co_label = mid and re.search(r'<label[^>]*for="%s"' % re.escape(mid.group(1)), s)
        if "aria-label" not in t and not co_label:
            L("[Ô tìm thiếu nhãn] %s" % d)

    # (6)(7) trang CÓ bộ lọc thì phải ghi URL và phải có trạng thái rỗng
    co_loc = bool(re.search(r'id="(?:f-area|kl-area)"', s)) or 'class="lc-chip' in s or 'class="nb-khu' in s
    if co_loc:
        if "replaceState" not in js and "pushState" not in js:
            L("[Lọc xong không ghi vào URL — không chia sẻ/lưu/back được] %s" % d)
        if not re.search(r"loc-empty|kl-trong|nb-trong|trong\.hidden|trống", js + s):
            W("[Không thấy trạng thái rỗng khi lọc ra 0 kết quả] %s" % d)

    # (8) lớp CSS của bộ lọc phải có thật
    for lop in ("kl-box", "kl-tim", "kl-dem", "kl-trong", "lc-chip", "nb-khu", "an-di", "nb-an"):
        if ('class="%s' % lop) in s or ("'%s'" % lop) in js:
            if ("." + lop) not in CSS and ("." + lop) not in s:
                L("[Lớp .%s dùng mà không có CSS ở đâu cả] %s" % (lop, d))


# ── 9/10. Thanh đáy điện thoại + câu hỏi phải mở sẵn ──────────────────────
for f in sorted(pages):
    s = open(f, encoding="utf-8").read()
    d = duong(f)

    # (9) thanh đáy phải có Gọi, Zalo và nút Menu BẤM ĐƯỢC
    # ĐÃ TỪNG DÍNH: 8 trang khu có nút Menu mang id lạ (menuBtn2) + display:none
    # -> trên điện thoại không mở được menu từ thanh đáy.
    i = s.find('class="mobile-nav"')
    if i < 0:
        L("[Không có thanh Gọi/Zalo dán đáy trên điện thoại] %s" % d)
    else:
        bar = s[i:s.find("</nav>", i)]
        if "tel:0978758788" not in bar:
            L("[Thanh đáy thiếu nút GỌI] %s" % d)
        if "zalo.me" not in bar:
            L("[Thanh đáy thiếu nút ZALO] %s" % d)
        nut = [m.group(0) for m in re.finditer(r"<(?:button|a)[^>]*>", bar)
               if ("mnavMenuBtn" in m.group(0) or "mnav-menu" in m.group(0))
               and "display:none" not in m.group(0)
               and not re.search(r"\shidden(?=[\s>])", m.group(0))]
        if not nut:
            L("[Thanh đáy không có nút Menu bấm được — khách phải cuộn ngược lên đầu] %s" % d)
        elif 'id="mobileSheet"' not in s:
            L("[Có nút Menu nhưng không có bảng menu để mở] %s" % d)

    # (10) câu hỏi phải MỞ SẴN — luật chủ đặt: đáp án hiện thẳng trên trang cho
    # Google và các bộ máy trả lời AI đọc, khách khỏi phải bấm.
    dong = len(re.findall(r"<details(?![^>]*\bopen\b)", s))
    if dong:
        L("[%d câu hỏi còn đóng — phải mở sẵn để ăn SEO/AEO/GEO] %s" % (dong, d))

# ── kết luận ───────────────────────────────────────────────────────────────
print("KIỂM NÚT BẤM & BỘ LỌC — %d trang\n%s" % (len(pages), "=" * 62))
if canh:
    print("CẢNH BÁO (%d):" % len(canh))
    for m in canh[:20]:
        print("  ! " + m)
    print()
if loi:
    print("LỖI (%d):" % len(loi))
    for m in loi[:60]:
        print("  X " + m)
    if len(loi) > 60:
        print("  … còn %d lỗi" % (len(loi) - 60))
    sys.exit(1)
print("SẠCH — mọi nút bấm và bộ lọc đều chạy đúng.")
sys.exit(0)
