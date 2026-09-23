#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐỔI "thị trấn Nam Ban" -> "trung tâm Nam Ban" TRONG THÂN BÀI.

Từ 01/7/2025 không còn thị trấn Nam Ban (NQ 202/2025/QH15), nhưng người mua VẪN
search "đất thị trấn Nam Ban". Chủ chốt:
  - TIÊU ĐỀ trang /dat-trung-tam-thi-tran-nam-ban/ GIỮ NGUYÊN (giữ URL + từ khoá)
  - TRONG BÀI đổi thành "trung tâm Nam Ban", lần đầu mỗi trang ghi thêm
    "(thị trấn Nam Ban cũ)" để vừa đúng vừa còn từ khoá.

VÙNG CẤM ĐỤNG:
  1. <title> và <h1>            -> giữ từ khoá + không đổi tiêu đề đang index
  2. "Thị Trấn Nam Ban" hoa cả  -> đó là tên riêng trong tiêu đề/schema name
  3. chỗ đã có chữ "cũ" ngay sau -> đang nói đúng rồi
  4. câu FAQ "Thị trấn Nam Ban còn tồn tại không?" và câu trả lời của nó
     -> đây CHÍNH LÀ chỗ giải thích, đổi đi là mất nghĩa
"""
import os
import re

os.chdir("/home/user/nambanvillas")

# Câu FAQ giải thích — không đụng
GIU = [
    "Thị trấn Nam Ban còn tồn tại không?",
    "Sau sắp xếp đơn vị hành chính (1/7/2025), thị trấn Nam Ban cũ nay thuộc xã Nam Ban",
    "người dân vẫn quen gọi 'thị trấn Nam Ban'",
    "người dân vẫn quen gọi &#39;thị trấn Nam Ban&#39;",
]

# Bắt "thị trấn Nam Ban" KHÔNG viết hoa cả cụm, KHÔNG theo sau bởi "cũ"
PAT = re.compile(r"([Tt])hị trấn Nam Ban(?!\s*cũ)")


def vung_cam(s):
    """Trả danh sách (đầu, cuối) các đoạn không được đụng."""
    ra = []
    for m in re.finditer(r"<title>[\s\S]*?</title>", s):
        ra.append((m.start(), m.end()))
    for m in re.finditer(r"<h1[^>]*>[\s\S]*?</h1>", s):
        ra.append((m.start(), m.end()))
    for g in GIU:
        i = 0
        while True:
            i = s.find(g, i)
            if i < 0:
                break
            ra.append((i, i + len(g)))
            i += len(g)
    return ra


def trong_vung(i, vung):
    return any(a <= i < b for a, b in vung)


def main():
    tong = 0
    trang = 0
    for f in sorted(__import__("glob").glob("**/index.html", recursive=True)):
        if f.startswith(("docs", "node_modules")):
            continue
        s = open(f, encoding="utf-8").read()
        if "hị trấn Nam Ban" not in s:
            continue
        vung = vung_cam(s)

        ra = []
        vi = 0
        n = 0
        for m in PAT.finditer(s):
            if trong_vung(m.start(), vung):
                continue
            hoa = m.group(1) == "T"
            ra.append(s[vi:m.start()])
            ra.append(("T" if hoa else "t") + "rung tâm Nam Ban")
            vi = m.end()
            n += 1
        ra.append(s[vi:])
        s2 = "".join(ra)

        if n:
            # Lần đầu xuất hiện TRONG MỘT ĐOẠN VĂN <p> thì chú thích tên cũ,
            # để khách tìm "thị trấn Nam Ban" vẫn thấy chữ đó trên trang.
            m = re.search(r"<p[^>]*>(?:(?!</p>)[\s\S])*?trung tâm Nam Ban", s2)
            if m:
                j = m.end()
                s2 = s2[:j] + " (thị trấn Nam Ban cũ)" + s2[j:]
            open(f, "w", encoding="utf-8").write(s2)
            tong += n
            trang += 1
            print("  %-52s %3d chỗ%s" % (f, n, "  + chú thích tên cũ" if m else ""))
    print("\nĐổi %d chỗ / %d trang." % (tong, trang))


if __name__ == "__main__":
    main()
