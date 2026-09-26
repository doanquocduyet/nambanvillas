#!/usr/bin/env python3
"""
LÔ TƯƠNG TỰ — mục "Có Thể Bạn Quan Tâm" trên mỗi trang lô: 4 lô cùng khu, giá gần nhất,
ưu tiên lô đang ít được trỏ tới (để không trang lô nào mồ côi). Chạy lại được, không nhân đôi.

  python3 scripts/lo-tuong-tu.py          # ghi
  python3 scripts/lo-tuong-tu.py --thu    # chỉ in

Nguồn lô: thẻ hub dat-nen-nam-ban/index.html (data-price, data-loc, data-ban). Lô đã bán không được gợi ý.
Chỉ thay NỘI DUNG khối <div class="sidebar-related-list"> đầu tiên của trang (cắt theo chỉ số, đếm thẻ div).
"""
import html as H, os, re, sys, collections

HUB = "dat-nen-nam-ban/index.html"
SO_LO = 4
THU = "--thu" in sys.argv


def doc_hub():
    s = open(HUB, encoding="utf-8").read()
    ds = []
    for m in re.finditer(r'<article class="prop-card(?: [^"]*)?"([^>]*)>', s):
        at = m.group(1)
        sau = s[m.end():m.end() + 2500]
        u = re.search(r'href="(/dat-nen/[^"]+/)"', sau)
        t = re.search(r'<h3 class="sp-title"><a[^>]*>([^<]*)', sau)
        p = re.search(r'data-price="([\d.]+)"', at)
        if not u or not t:
            continue
        ds.append(dict(url=u.group(1), ten=H.unescape(t.group(1)).strip(), gia=float(p.group(1)) if p else 0.0,
                       loc=(re.search(r'data-loc="([^"]*)"', at) or [None, ""])[1].split(),
                       ban='data-ban="1"' in at))
    return ds


def anh(url):
    slug = url.strip("/").split("/")[-1]
    for ext in ("webp", "jpg", "jpeg", "png"):
        p = "images/listings/%s/1.%s" % (slug, ext)
        if os.path.exists(p):
            return "/" + p
    return None


def khoi_list(s):
    """(start, end) phần NỘI DUNG bên trong <div class="sidebar-related-list">…</div> đầu tiên."""
    mo = '<div class="sidebar-related-list">'
    i = s.find(mo)
    if i == -1:
        return None
    a = i + len(mo); k = a; sau = 1
    while sau:
        n_mo = s.find("<div", k); n_dong = s.find("</div>", k)
        if n_dong == -1:
            return None
        if n_mo != -1 and n_mo < n_dong:
            sau += 1; k = n_mo + 4
        else:
            sau -= 1; k = n_dong + 6
    return a, k - 6


def main():
    lo = [x for x in doc_hub() if os.path.exists(x["url"].strip("/") + "/index.html")]
    con = [x for x in lo if not x["ban"] and anh(x["url"])]
    # số trang đang trỏ vào mỗi lô (không tính hub + trang khu: mọi lô đều có)
    vao = collections.Counter()
    trang = {x["url"]: open(x["url"].strip("/") + "/index.html", encoding="utf-8").read() for x in lo}
    for u, s in trang.items():
        for h in set(re.findall(r'href="(/dat-nen/[^"]+/)"', s)):
            if h != u:
                vao[h] += 1
    doi = 0
    for x in lo:
        s = trang[x["url"]]
        kh = khoi_list(s)
        if not kh:
            continue
        ung = [y for y in con if y["url"] != x["url"]]
        cung_khu = [y for y in ung if set(y["loc"]) & set(x["loc"])] or ung
        cung_khu.sort(key=lambda y: (abs(y["gia"] - x["gia"]) if x["gia"] and y["gia"] else 9, vao[y["url"]]))
        # 3 lô gần giá nhất + 1 lô ít được trỏ tới nhất cùng khu
        chon = cung_khu[:3]
        it = sorted([y for y in cung_khu if y not in chon], key=lambda y: vao[y["url"]])
        chon += it[:SO_LO - len(chon)]
        the = "".join(
            '<a href="%s" class="related-card"><img src="%s" alt="%s" loading="lazy" width="400" height="275">'
            '<div class="related-card-body"><p class="related-card-title">%s</p><p class="related-card-cta">Xem chi tiết →</p></div></a>'
            % (y["url"], anh(y["url"]), H.escape(y["ten"]), H.escape(y["ten"], quote=False)) for y in chon)
        moi = s[:kh[0]] + the + s[kh[1]:]
        if moi != s:
            doi += 1
            if not THU:
                open(x["url"].strip("/") + "/index.html", "w", encoding="utf-8").write(moi)
    print("Cập nhật lô tương tự: %d/%d trang lô" % (doi, len(lo)))


if __name__ == "__main__":
    main()
