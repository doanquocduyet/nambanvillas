#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LUẬT CHỦ WEB (24/9/2026): chữ "Lâm Hà" LUÔN có "Nam Ban" ngay bên cạnh.

Lý do: web bán đất Nam Ban; "Lâm Hà" đứng một mình kéo Google/AI hiểu sang cả vùng
Lâm Hà rộng, loãng thực thể Nam Ban. Đứng cạnh nhau thì mỗi lần nhắc Lâm Hà là một
lần củng cố cặp "Nam Ban – Lâm Hà".

Quy tắc viết lại (tất định — cùng một cụm trong thân trang và trong JSON-LD đổi y
hệt nhau, nên FAQ hiển thị và FAQPage schema không bao giờ lệch):
  - Khu THUỘC xã Nam Ban (NQ 202/2025/QH15: thị trấn Nam Ban cũ + Đông Thanh + Mê
    Linh + Gia Lâm; cùng các khu Tầm Xá, Từ Liêm, Bãi Công nằm trong đó):
        "Mê Linh, Lâm Hà"  -> "Mê Linh, Nam Ban, Lâm Hà"
        "Mê Linh · Lâm Hà" -> "Mê Linh · Nam Ban · Lâm Hà"
        "Mê Linh Lâm Hà"   -> "Mê Linh Nam Ban Lâm Hà"
  - Xã KHÁC giáp Nam Ban (Nam Hà, Đinh Văn…): KHÔNG được ghi là thuộc Nam Ban ->
        "Nam Hà, Lâm Hà"   -> "Nam Hà (giáp Nam Ban), Lâm Hà"
  - "đất Lâm Hà" / "Giá đất Lâm Hà" -> "đất Nam Ban Lâm Hà" (thứ tự chủ web chốt)
  - "huyện Lâm Hà" -> "huyện Lâm Hà (vùng Nam Ban)"
  - còn lại: "Lâm Hà" -> "Nam Ban, Lâm Hà"
Bỏ qua chỗ đã có "Nam Ban" sát bên (chỉ cách nhau dấu phẩy, chấm giữa, gạch, ngoặc,
khoảng trắng hoặc chữ "huyện").

    python3 scripts/lam-ha-kem-nam-ban.py          # sửa
    python3 scripts/lam-ha-kem-nam-ban.py --kiem   # chỉ đếm, không sửa (bẫy dùng)
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SEP = r"[\s,·–\-\(\)]{0,4}(?:[Hh]uyện\s)?"
KE_BEN = re.compile(r"Nam Ban%sLâm Hà|Lâm Hà%sNam Ban" % (SEP, r"[\s,·–\-\(\)]{0,4}(?:\(vùng |\(giáp |vùng )?"))
TRONG_NAM_BAN = r"(Mê Linh|Đông Thanh|Gia Lâm|Tầm Xá|Từ Liêm|Hồ Bãi Công|Bãi Công)"
GIAP = r"(Nam Hà|Đinh Văn)"


def viet_lai(s):
    # 1) khu trong xã Nam Ban
    s = re.sub(TRONG_NAM_BAN + r",\s*(?:[Hh]uyện\s)?Lâm Hà", r"\1, Nam Ban, Lâm Hà", s)
    s = re.sub(TRONG_NAM_BAN + r"\s·\sLâm Hà", r"\1 · Nam Ban · Lâm Hà", s)
    s = re.sub(TRONG_NAM_BAN + r"\s–\sLâm Hà", r"\1 – Nam Ban – Lâm Hà", s)
    s = re.sub(TRONG_NAM_BAN + r" Lâm Hà", r"\1 Nam Ban Lâm Hà", s)
    # 2) xã giáp Nam Ban
    s = re.sub(GIAP + r",\s*(?:[Hh]uyện\s)?Lâm Hà", r"\1 (giáp Nam Ban), Lâm Hà", s)
    s = re.sub(GIAP + r"\s·\sLâm Hà", r"\1 · Lâm Hà (giáp Nam Ban)", s)
    s = re.sub(GIAP + r"\s–\sLâm Hà", r"\1 – Lâm Hà (giáp Nam Ban)", s)
    s = re.sub(GIAP + r" Lâm Hà", r"\1 Lâm Hà (giáp Nam Ban)", s)

    # 3) phần còn lại: xử lý từng chỗ, bỏ qua chỗ đã có Nam Ban sát bên
    out, pos = [], 0
    for m in re.finditer(r"Lâm Hà", s):
        a, b = m.start(), m.end()
        if ke_ben(s, a, b):
            continue
        truoc = s[max(0, a - 7):a]
        if re.search(r"[Hh]uyện\s$", truoc):
            moi = "Lâm Hà (vùng Nam Ban)"
        elif re.search(r"[Đđ]ất\s$", truoc):
            moi = "Nam Ban Lâm Hà"          # chủ web chốt thứ tự "giá đất Nam Ban Lâm Hà" (24/9/2026)
        else:
            moi = "Nam Ban, Lâm Hà"
        out.append(s[pos:a])
        out.append(moi)
        pos = b
    out.append(s[pos:])
    return "".join(out)


TRUOC = re.compile(r"Nam Ban[\s,·–\-\(\)\"“”]{0,4}(?:[Hh]uyện\s)?[\"“]?$")
SAU = re.compile(r"^[\"”]?[\s,·–\-\(\)]{0,4}(?:\(vùng |\(giáp |vùng |giáp )?Nam Ban")


def ke_ben(s, a, b):
    """Kiểm TỪNG chỗ riêng (không dùng finditer trên cửa sổ — 2 cặp sát nhau từng bị nuốt nhau)."""
    return bool(TRUOC.search(s[max(0, a - 20):a]) or SAU.search(s[b:b + 24]))


def con_le(s):
    """Đếm 'Lâm Hà' chưa có Nam Ban sát bên."""
    return sum(1 for m in re.finditer(r"Lâm Hà", s) if not ke_ben(s, m.start(), m.end()))


def main():
    kiem = "--kiem" in sys.argv
    tong_truoc = tong_sau = trang = 0
    for f in sorted(glob.glob("**/*.html", recursive=True) + ["llms.txt"]):
        if f.startswith(("node_modules", "docs")) or not os.path.exists(f):
            continue
        s = open(f, encoding="utf-8").read()
        n = con_le(s)
        if not n:
            continue
        tong_truoc += n
        if kiem:
            print("  %3d  %s" % (n, f))
            continue
        s2 = viet_lai(s)
        tong_sau += con_le(s2)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            trang += 1
    if kiem:
        print("Còn %d chỗ 'Lâm Hà' thiếu 'Nam Ban' bên cạnh." % tong_truoc)
        return 1 if tong_truoc else 0
    print("Sửa %d trang: %d chỗ -> còn %d" % (trang, tong_truoc, tong_sau))
    return 0


if __name__ == "__main__":
    sys.exit(main())
