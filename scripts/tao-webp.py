#!/usr/bin/env python3
"""Tạo bản .webp cho mọi ảnh .jpg trong images/.

Vì sao: WebP nhẹ hơn JPEG ~30% ở cùng chất lượng → trang tải nhanh hơn →
Core Web Vitals tốt hơn → Google xếp hạng cao hơn. Mọi trình duyệt còn dùng
hiện nay đều đọc được WebP nên không cần thẻ <picture> dự phòng.

Bản .jpg cũ ĐƯỢC GIỮ LẠI để các link ảnh Google đã lập chỉ mục không chết.

Chạy: python3 scripts/tao-webp.py            (chỉ tạo ảnh còn thiếu)
      python3 scripts/tao-webp.py --lam-lai  (tạo lại toàn bộ)
"""
import os, sys, glob
from PIL import Image

CHAT_LUONG = 82
lam_lai = "--lam-lai" in sys.argv

tao = bo_qua = to_hon = 0
truoc = sau = 0
for f in sorted(glob.glob("images/**/*.jpg", recursive=True)):
    w = f[:-4] + ".webp"
    if os.path.exists(w) and not lam_lai:
        bo_qua += 1
        continue
    im = Image.open(f)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    im.save(w, "WEBP", quality=CHAT_LUONG, method=5)
    a, b = os.path.getsize(f), os.path.getsize(w)
    # WebP to hơn JPEG thì giữ JPEG, xoá webp đi cho khỏi rác
    if b >= a:
        os.remove(w)
        to_hon += 1
        continue
    truoc += a
    sau += b
    tao += 1

print("Tạo %d ảnh webp | bỏ qua %d (đã có) | %d ảnh webp to hơn nên giữ jpg" % (tao, bo_qua, to_hon))
if tao:
    print("Dung lượng: %.1fMB → %.1fMB (giảm %.0f%%)" % (
        truoc / 1e6, sau / 1e6, 100 * (1 - sau / truoc)))
