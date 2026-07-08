#!/usr/bin/env python3
"""
Nén ảnh trước khi đưa lên site — dùng cho MỌI ảnh mới.
Luật (CLAUDE.md NGUYÊN TẮC SỐ 4): ảnh mới phải nén trước khi commit.

Cách dùng:
  python3 scripts/nen-anh.py <file-hoặc-thư-mục> [file2 ...]
  python3 scripts/nen-anh.py images/listings/lo-moi/     # nén cả thư mục

Quy tắc an toàn:
  - Giảm kích thước tối đa 1600px chiều rộng (đủ cho mọi vị trí hiển thị).
  - JPEG quality 82, progressive, xoá metadata.
  - CHỈ ghi đè nếu file mới NHỎ HƠN thật (không làm ảnh gốc đã tối ưu bị phình/xấu).
  - Xoay ảnh theo EXIF để không bị nằm ngang.
"""
import os, sys
try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Cần Pillow: pip install Pillow")

MAXW = 1600
QUALITY = 82

def collect(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for dp, _, fns in os.walk(p):
                for fn in fns:
                    if fn.lower().endswith(('.jpg', '.jpeg', '.png')):
                        out.append(os.path.join(dp, fn))
        elif p.lower().endswith(('.jpg', '.jpeg', '.png')):
            out.append(p)
    return out

def compress(p):
    b = os.path.getsize(p)
    tmp = p + '.tmp'
    im = ImageOps.exif_transpose(Image.open(p))
    w, h = im.size
    resized = w > MAXW
    if resized:
        im = im.resize((MAXW, round(h * MAXW / w)), Image.LANCZOS)
    if p.lower().endswith('.png'):
        im.convert('RGB').save(tmp, 'PNG', optimize=True)
    else:
        im.convert('RGB').save(tmp, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
    nb = os.path.getsize(tmp)
    if resized or nb < b * 0.98:
        os.replace(tmp, p)
        return b, nb, True
    os.remove(tmp)
    return b, b, False

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    files = collect(sys.argv[1:])
    if not files:
        sys.exit("Không tìm thấy ảnh .jpg/.png nào.")
    tb = ta = 0; n = 0
    for p in files:
        try:
            b, a, changed = compress(p)
            tb += b; ta += a
            if changed:
                n += 1
                print(f"  {b//1024:4d}KB -> {a//1024:4d}KB  {p}")
        except Exception as e:
            print(f"  LỖI {p}: {e}")
    print(f"\nNén {n}/{len(files)} ảnh · {tb/1024/1024:.2f}MB -> {ta/1024/1024:.2f}MB "
          f"(giảm {100*(tb-ta)/tb:.0f}%)" if tb else "Không có gì để nén")

if __name__ == '__main__':
    main()
