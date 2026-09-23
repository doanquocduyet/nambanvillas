#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINH ẢNH BẢN NHỎ + GẮN srcset CHO ẢNH HERO.

Vì sao: ảnh hero (LCP) trung vị 163KB, nhiều trang >200KB, rộng 1280px — trong
khi điện thoại chỉ hiển thị ~390–420px. Máy tính tải đúng bản to là hợp lý;
điện thoại tải bản to là phí. srcset để trình duyệt tự chọn bản vừa.

Chạy: python3 scripts/tao-srcset.py
      python3 scripts/tao-srcset.py --thu    (chỉ in, không ghi)

An toàn:
- Chỉ đụng thẻ <img> có fetchpriority="high" (đúng 1 ảnh/trang).
- Bản nhỏ cùng ĐỊNH DẠNG với src (trộn jpg/webp trong 1 srcset là sai).
- Chỉ ghi file khi thật sự nhỏ hơn; không tạo bản rộng hơn ảnh gốc.
- Chạy lại nhiều lần không nhân đôi thuộc tính (idempotent).
- Cập nhật <link rel=preload as=image> kèm imagesrcset/imagesizes — preload
  không khớp srcset thì trình duyệt tải 2 ảnh, hại chứ không lợi.
"""
import glob
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
THU = "--thu" in sys.argv

# Bề rộng hiển thị lấy từ chính thuộc tính width của thẻ — đó là con số tác giả
# đã khai cho trình duyệt, chính xác hơn mọi suy đoán từ CSS.
# ĐÃ SUÝT DÍNH: gán chung sizes 1130px cho mọi hero thì 14 ảnh CARD rộng 400px
# sẽ khiến trình duyệt tải bản 1280 — nặng hơn cả trước khi làm srcset.
RONG_TOI_THIEU = 300       # nhỏ hơn mức này thì srcset không đáng, bỏ qua

# Thang bề rộng cố định, phủ đúng các máy thật:
#   480  — điện thoại DPR1
#   800  — điện thoại DPR2 (390–430px viewport × 2) ← mức ăn nhiều byte nhất
#   1200 — máy tính
# ĐÃ SUÝT DÍNH: sinh bản theo đúng width khai báo (700px cho gallery) thì ở điện
# thoại trình duyệt cần 780px, thấy 700 < 780 nên vẫn chọn bản GỐC 1280 — làm
# xong mà không giảm được gì. Thang phải có mức NẰM TRÊN nhu cầu điện thoại.
THANG = [480, 800, 1200]


def sizes_theo_rong(w):
    return "(max-width: %dpx) 100vw, %dpx" % (w + 120, w)


def sinh_ban_nho(p, rong_hien_thi):
    """Sinh bản đúng bề rộng cần: 1x và 2x của kích thước hiển thị.

    Trả [(w, path), ...] tăng dần, mục cuối luôn là ảnh gốc.
    """
    base, ext = os.path.splitext(p)
    if not os.path.exists(p):
        return []
    try:
        im = Image.open(p)
    except Exception:
        return []
    goc_w = im.width
    can = [w for w in THANG if w < goc_w and w <= rong_hien_thi * 2]
    ra = []
    for w in can:
        if w >= goc_w:
            continue
        out = "%s-%d%s" % (base, w, ext)
        if not os.path.exists(out) and not THU:
            nho = im.convert("RGB").resize((w, round(im.height * w / goc_w)), Image.LANCZOS)
            if ext.lower() == ".webp":
                nho.save(out, "WEBP", quality=80, method=6)
            else:
                nho.save(out, "JPEG", quality=78, optimize=True, progressive=True)
            if os.path.getsize(out) >= os.path.getsize(p):
                os.remove(out)      # bản nhỏ không nhẹ hơn thì giữ làm gì
                continue
        if os.path.exists(out):
            ra.append((w, out))
    ra.append((goc_w, p))
    return ra


def gan(tg, srcset, sizes):
    """Gắn/ghi đè srcset + sizes vào một thẻ img, giữ nguyên mọi thuộc tính khác."""
    tg = re.sub(r'\s+srcset="[^"]*"', "", tg)
    tg = re.sub(r'\s+sizes="[^"]*"', "", tg)
    return tg[:-1].rstrip() + ' srcset="%s" sizes="%s">' % (srcset, sizes)


def main():
    n_trang = n_anh = 0
    truoc = sau = 0
    mau = []
    for f in sorted(glob.glob("**/index.html", recursive=True)):
        if f.startswith(("node_modules", "docs")):
            continue
        s = open(f, encoding="utf-8").read()
        m = re.search(r'<img\b[^>]*fetchpriority="high"[^>]*>', s)
        if not m:
            continue
        tg = m.group(0)
        # ĐÃ TỪNG DÍNH (cwv-6): chỉ bắt src="/images/..." nên 12 trang dùng đường dẫn
        # TƯƠNG ĐỐI (../images/, ../../images/) bị bỏ qua dù bản -480 đã có sẵn.
        src = re.search(r'src="((?:\.\./)*/?images/[^"]+)"', tg)
        if not src:
            continue
        tien_to = re.match(r'(?:\.\./)*/?', src.group(1)).group(0)   # giữ nguyên kiểu đường dẫn
        p = src.group(1)[len(tien_to):]
        mw = re.search(r'width="(\d+)"', tg)
        rong = int(mw.group(1)) if mw else 1130
        if rong < RONG_TOI_THIEU:
            continue
        ban = sinh_ban_nho(p, rong)
        if len(ban) < 2:          # không có bản nhỏ nào → để nguyên
            continue
        srcset = ", ".join("%s%s %dw" % (tien_to, x, w) for w, x in ban)
        sizes = sizes_theo_rong(rong)
        tg_moi = gan(tg, srcset, sizes)
        s2 = s.replace(tg, tg_moi, 1)

        # preload phải khớp srcset, nếu không trình duyệt tải 2 ảnh
        pl = re.search(r'<link rel="preload" as="image"[^>]*>', s2)
        if pl:
            t = pl.group(0)
            t2 = re.sub(r'\s+imagesrcset="[^"]*"', "", t)
            t2 = re.sub(r'\s+imagesizes="[^"]*"', "", t2)
            t2 = t2[:-1].rstrip() + ' imagesrcset="%s" imagesizes="%s">' % (srcset, sizes)
            s2 = s2.replace(t, t2, 1)

        if s2 != s:
            if not THU:
                open(f, "w", encoding="utf-8").write(s2)
            n_trang += 1
            n_anh += len(ban) - 1
            # byte điện thoại 390px DPR2 ⇒ cần ~780px ⇒ chọn bản ≥780 nhỏ nhất
            muc = 780 if rong >= 600 else rong * 2
            chon = min([w for w, _ in ban if w >= muc] or [ban[-1][0]])
            fp = dict((w, x) for w, x in ban)[chon]
            truoc += os.path.getsize(p) / 1024
            sau += os.path.getsize(fp) / 1024 if os.path.exists(fp) else 0
            if len(mau) < 3:
                mau.append(tg_moi[:150])

    print("Trang sửa: %d | bản nhỏ sinh: %d" % (n_trang, n_anh))
    if truoc:
        print("Ảnh hero ở điện thoại (390px DPR2): %.0fKB -> %.0fKB (giảm %.0f%%)"
              % (truoc, sau, 100 * (1 - sau / truoc)))
    for x in mau:
        print("  ", x)
    if THU:
        print("[chỉ thử, chưa ghi]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
