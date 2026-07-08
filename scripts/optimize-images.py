#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optimize-images.py — Nén TOÀN BỘ ảnh JPEG trong images/ cho web tải nhanh.

Làm gì:
  - Duyệt images/**.jpg|jpeg. Với ảnh NẶNG (> ngưỡng KB) hoặc QUÁ LỚN (> cạnh tối đa):
      auto-xoay EXIF → xoá EXIF → resize cạnh dài về tối đa → nén JPEG dò chất lượng ~mục tiêu KB.
  - Ảnh đã nhẹ + đúng kích thước: BỎ QUA (không nén lại để khỏi giảm chất lượng thừa).
  - Không đụng PNG/SVG (logo, favicon).

Dùng:  python3 scripts/optimize-images.py [--kb 150] [--max 1600] [--skip-under 165] [--dir images]
"""
import argparse, os, sys
from io import BytesIO
try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Thiếu Pillow. Chạy: pip3 install Pillow")


def encode(img, target_kb, qmin=45, qmax=88):
    target = target_kb * 1024
    best = None
    lo, hi = qmin, qmax
    while lo <= hi:
        q = (lo + hi) // 2
        buf = BytesIO(); img.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= target:
            best = buf.getvalue(); lo = q + 1
        else:
            hi = q - 1
    if best is None:
        buf = BytesIO(); img.save(buf, "JPEG", quality=qmin, optimize=True, progressive=True); best = buf.getvalue()
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", type=int, default=150, help="mục tiêu KB/ảnh khi nén")
    ap.add_argument("--max", type=int, default=1600, help="cạnh dài tối đa px")
    ap.add_argument("--skip-under", type=int, default=165, help="ảnh ≤ KB này và đúng kích thước → bỏ qua")
    ap.add_argument("--dir", default="images")
    args = ap.parse_args()

    tot_before = tot_after = 0
    done = skipped = 0
    for root, _, files in os.walk(args.dir):
        for name in files:
            if not name.lower().endswith((".jpg", ".jpeg")):
                continue
            p = os.path.join(root, name)
            sz = os.path.getsize(p)
            tot_before += sz
            try:
                im = Image.open(p)
                oversized = max(im.size) > args.max
                if sz <= args.skip_under * 1024 and not oversized:
                    tot_after += sz; skipped += 1; continue
                im = ImageOps.exif_transpose(im).convert("RGB")
                if max(im.size) > args.max:
                    s = args.max / max(im.size)
                    im = im.resize((round(im.size[0]*s), round(im.size[1]*s)), Image.LANCZOS)
                data = encode(im, args.kb)
                # chỉ ghi nếu thật sự nhẹ hơn
                if len(data) < sz:
                    open(p, "wb").write(data); tot_after += len(data)
                    print(f"  {p}  {sz//1024}KB -> {len(data)//1024}KB")
                else:
                    tot_after += sz; skipped += 1
                done += 1
            except Exception as e:
                tot_after += sz; print(f"  ⚠️ {p}: {e}")
    print(f"\nNén {done} ảnh, bỏ qua {skipped}. Tổng {tot_before//1024}KB -> {tot_after//1024}KB "
          f"(giảm {(tot_before-tot_after)//1024}KB, {100*(tot_before-tot_after)//max(tot_before,1)}%)")


if __name__ == "__main__":
    main()
