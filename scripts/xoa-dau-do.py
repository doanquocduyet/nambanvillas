#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xoa-dau-do.py — Xoá dấu bút ĐỎ + chữ đỏ khỏi ảnh bản vẽ / sơ đồ phân lô.
Luật CLAUDE.md: "Bỏ hết dấu đỏ và chữ trong bản đồ" trước khi đăng.

Kỹ thuật (thuần PIL, không cần cv2/numpy):
  1. Mask pixel đỏ: R nổi trội hơn hẳn G và B (R - max(G,B) >= thresh) và đủ đậm.
  2. Nới mask (dilate) để phủ viền nét.
  3. Trám (inpaint) từng pixel đỏ bằng trung bình 4 hướng pixel KHÔNG-đỏ gần nhất
     → hoà vào nền, không để lại vệt hồng hay đốm trắng.

Dùng:
  python3 scripts/xoa-dau-do.py input.jpg output.jpg
  python3 scripts/xoa-dau-do.py input.jpg output.jpg --thresh 40 --dilate 3
"""
import argparse
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Cần Pillow: pip install Pillow")


def build_mask(px, w, h, thresh):
    mask = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if r - max(g, b) >= thresh and r >= 70:
                mask[y][x] = True
    return mask


def dilate(mask, w, h, d):
    if d <= 0:
        return mask
    out = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if mask[y][x]:
                for dy in range(-d, d + 1):
                    yy = y + dy
                    if 0 <= yy < h:
                        row = out[yy]
                        for dx in range(-d, d + 1):
                            xx = x + dx
                            if 0 <= xx < w:
                                row[xx] = True
    return out


def inpaint(img, mask, w, h):
    px = img.load()
    for y in range(h):
        for x in range(w):
            if not mask[y][x]:
                continue
            samples = []
            # trái, phải, trên, dưới — pixel không-đỏ gần nhất
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                xx, yy = x + dx, y + dy
                steps = 0
                while 0 <= xx < w and 0 <= yy < h and mask[yy][xx] and steps < max(w, h):
                    xx += dx
                    yy += dy
                    steps += 1
                if 0 <= xx < w and 0 <= yy < h and not mask[yy][xx]:
                    samples.append(px[xx, yy][:3])
            if samples:
                r = sum(s[0] for s in samples) // len(samples)
                g = sum(s[1] for s in samples) // len(samples)
                b = sum(s[2] for s in samples) // len(samples)
                px[x, y] = (r, g, b)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--thresh", type=int, default=40, help="ngưỡng đỏ trội (mặc định 40)")
    ap.add_argument("--dilate", type=int, default=3, help="nới mask (mặc định 3)")
    args = ap.parse_args()

    img = Image.open(args.src)
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size
    mask = build_mask(img.load(), w, h, args.thresh)
    n = sum(sum(1 for v in row if v) for row in mask)
    mask = dilate(mask, w, h, args.dilate)
    img = inpaint(img, mask, w, h)
    img.save(args.dst, "JPEG", quality=92)
    print(f"Xoá {n} pixel đỏ (dilate {args.dilate}) -> {args.dst}  {w}x{h}")


if __name__ == "__main__":
    main()
