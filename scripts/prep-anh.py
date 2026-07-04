#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prep-anh.py — Cắt gọt + nén ảnh tin/lô đất Nam Ban Villas cho web.

Làm tự động:
  1. Auto-xoay theo EXIF rồi XÓA SẠCH EXIF (bỏ cả GPS toạ độ — bảo mật vị trí).
  2. Smart-crop theo tỉ lệ đích: giữ vùng nhiều "chi tiết" nhất (gradient-energy),
     KHÔNG cắt cụt chủ thể như center-crop mù.
  3. Resize cạnh dài về mức web + sharpen nhẹ cho nét.
  4. Nén JPEG dò chất lượng để chạm ~mục tiêu KB (mặc định ~110KB).
  5. Đặt tên chuẩn: images/listings/<slug>/1.jpg 2.jpg 3.jpg ...

Dùng:
  python3 scripts/prep-anh.py <slug> anh1.jpg anh2.jpg ...
  python3 scripts/prep-anh.py <slug> --ratio 16:9 hero.jpg     # ép 1 tỉ lệ
  python3 scripts/prep-anh.py <slug> --ratio keep phong.jpg    # giữ nguyên khung, chỉ nén
  python3 scripts/prep-anh.py <slug> --kb 100 --long 1280 ...

Mặc định: ratio 3:2 (khung landscape hợp gallery BĐS), cạnh dài 1280px, ~110KB.
Ảnh dọc (phòng ốc) nên để --ratio keep để không mất trần/sàn.
"""
import argparse
import os
import sys

try:
    from PIL import Image, ImageOps, ImageFilter
except ImportError:
    sys.exit("Thiếu Pillow. Chạy: pip3 install Pillow")


def parse_ratio(s):
    if s.lower() == "keep":
        return None
    if ":" in s:
        w, h = s.split(":")
        return float(w) / float(h)
    return float(s)


def energy_profile(img):
    """Trả về (colsum, rowsum) năng lượng cạnh — vùng nhiều chi tiết = giá trị cao."""
    g = img.convert("L").filter(ImageFilter.FIND_EDGES)
    px = g.load()
    w, h = g.size
    cols = [0] * w
    rows = [0] * h
    # bước nhảy để nhanh với ảnh lớn, vẫn đủ chính xác chọn cửa sổ
    step = max(1, min(w, h) // 400)
    for y in range(0, h, step):
        for x in range(0, w, step):
            v = px[x, y]
            cols[x] += v
            rows[y] += v
    return cols, rows


def best_window(profile, length, total):
    """Chọn offset [o, o+length] trong 'total' sao cho tổng energy lớn nhất."""
    if length >= total:
        return 0
    # cumulative sum
    cum = [0] * (total + 1)
    for i in range(total):
        cum[i + 1] = cum[i] + profile[i]
    best_o, best_v = 0, -1
    for o in range(0, total - length + 1):
        v = cum[o + length] - cum[o]
        if v > best_v:
            best_v, best_o = v, o
    return best_o


def smart_crop(img, ratio):
    if ratio is None:
        return img
    w, h = img.size
    cur = w / h
    if abs(cur - ratio) < 0.01:
        return img
    cols, rows = energy_profile(img)
    if cur > ratio:  # quá rộng → cắt bớt chiều ngang
        cw = max(1, round(h * ratio))
        x = best_window(cols, cw, w)
        return img.crop((x, 0, x + cw, h))
    else:  # quá cao → cắt bớt chiều dọc
        ch = max(1, round(w / ratio))
        y = best_window(rows, ch, h)
        return img.crop((0, y, w, y + ch))


def fit_long(img, long_side):
    w, h = img.size
    m = max(w, h)
    if m <= long_side:
        return img
    s = long_side / m
    return img.resize((round(w * s), round(h * s)), Image.LANCZOS)


def encode_to_target(img, path, target_kb, qmin=46, qmax=88):
    """Dò nhị phân chất lượng JPEG để chạm ~target_kb (không vượt), progressive, strip EXIF."""
    target = target_kb * 1024
    best = None
    lo, hi = qmin, qmax
    while lo <= hi:
        q = (lo + hi) // 2
        from io import BytesIO
        buf = BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        size = buf.tell()
        if size <= target:
            best = (q, buf.getvalue())
            lo = q + 1  # thử chất lượng cao hơn
        else:
            hi = q - 1
    if best is None:  # ngay cả qmin vẫn quá nặng → lấy qmin
        from io import BytesIO
        buf = BytesIO()
        img.save(buf, "JPEG", quality=qmin, optimize=True, progressive=True)
        best = (qmin, buf.getvalue())
    with open(path, "wb") as f:
        f.write(best[1])
    return best[0], len(best[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="slug thư mục, vd: me-linh-villa-238")
    ap.add_argument("images", nargs="+", help="đường dẫn ảnh gốc")
    ap.add_argument("--ratio", default="3:2", help="16:9 | 4:3 | 3:2 | 1:1 | keep (mặc định 3:2)")
    ap.add_argument("--kb", type=int, default=150, help="mục tiêu KB/ảnh (mặc định 150; ảnh nhiều lá cây có thể nhỉnh hơn)")
    ap.add_argument("--long", type=int, default=1280, help="cạnh dài tối đa px (mặc định 1280)")
    ap.add_argument("--out", default="images/listings", help="thư mục gốc output")
    ap.add_argument("--start", type=int, default=1, help="số bắt đầu đánh tên (mặc định 1)")
    args = ap.parse_args()

    ratio = parse_ratio(args.ratio)
    outdir = os.path.join(args.out, args.slug)
    os.makedirs(outdir, exist_ok=True)

    n = args.start
    for src in args.images:
        img = Image.open(src)
        img = ImageOps.exif_transpose(img)  # auto-xoay
        img = img.convert("RGB")
        img = smart_crop(img, ratio)
        img = fit_long(img, args.long)
        img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=60, threshold=2))  # nét nhẹ
        dst = os.path.join(outdir, f"{n}.jpg")
        q, size = encode_to_target(img, dst, args.kb)
        w, h = img.size
        print(f"  {os.path.basename(src)} -> {dst}  {w}x{h}  q{q}  {size//1024}KB")
        n += 1
    print(f"Xong {n - args.start} ảnh → {outdir}/")


if __name__ == "__main__":
    main()
