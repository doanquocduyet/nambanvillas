#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐỔ ĐỦ LÔ VÀO TRANG KHU (bản 2).

Bản 1 sửa schema bằng regex `\\](?=\\})` -> khớp nhầm dấu ] đầu tiên, cắt cụt
ItemList, hỏng JSON cả 6 trang. Bản này PARSE JSON ra object rồi sửa trong cây,
serialize lại — không đụng regex vào JSON nữa.

NGUỒN SỰ THẬT: data-loc trên thẻ ở 2 hub. Copy NGUYÊN thẻ, không viết lại nội
dung -> không có cơ hội chế nhầm thông tin lô.
"""
import json
import os
import re

os.chdir("/home/user/nambanvillas")

# Hub đã gán đủ khu cho mọi lô (nam-ban-3223m2-view-ho đã thêm gia-lam thẳng
# vào data-loc trên hub), không cần vá trong script nữa.
THEM_KHU = {}
# Chủ đã xác nhận khu cho cả 3 lô từng treo (23/9/2026):
#   cum-ts-retreat        -> Gia Lâm      (hub đã gán đúng)
#   cum-tam-xa-5-nen      -> Đông Thanh   (hub đã gán đúng)
#   cum-thien-van-village -> Nam Hà       (hub gán nam-ban, đã sửa thành nam-ha)
# Không còn lô nào treo.
CHO_XAC_NHAN = {}
TRANG_KHU = {
    "dong-thanh":  "dat-dong-thanh-nam-ban",
    "me-linh":     "dat-me-linh-nam-ban",
    "gia-lam":     "dat-gia-lam-nam-ban",
    "tu-liem":     "dat-tu-liem-nam-ban",
    "ho-bai-cong": "dat-ho-bai-cong-nam-ban",
    "nam-ban":     "dat-trung-tam-thi-tran-nam-ban",
}
THE = re.compile(r'<article class="prop-card sp-row[^"]*"([^>]*)>([\s\S]*?)</article>')
URL = re.compile(r'href="(/(?:dat-nen|nha-ban)/[a-z0-9-]+/)"')


def doc_the(f):
    ra = []
    for m in THE.finditer(open(f, encoding="utf-8").read()):
        at, body = m.group(1), m.group(2)
        u = URL.search(body)
        if not u:
            continue
        loc = re.search(r'data-loc="([^"]*)"', at)
        ra.append(dict(url=u.group(1), loc=set(loc.group(1).split()) if loc else set(),
                       ban='data-ban="1"' in at, html=m.group(0)))
    return ra


def ten_lo(html):
    m = re.search(r'<h3 class="sp-title"><a[^>]*>([\s\S]*?)</a>', html)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
    return t.replace("&amp;", "&").replace("&nbsp;", " ")


def sua_itemlist(s, urls, ten):
    """Parse từng khối ld+json, sửa ItemList trong cây object, ghi lại."""
    ra = []
    vi = 0
    sua = 0
    for m in re.finditer(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', s):
        g = json.loads(m.group(2))

        def di(n):
            nonlocal sua
            if isinstance(n, dict):
                if n.get("@type") == "ItemList":
                    n["numberOfItems"] = len(urls)
                    n["itemListElement"] = [
                        {"@type": "ListItem", "position": i + 1,
                         "url": "https://nambanvillas.vn" + u, "name": ten[u]}
                        for i, u in enumerate(urls)]
                    sua += 1
                for v in n.values():
                    di(v)
            elif isinstance(n, list):
                for v in n:
                    di(v)
        di(g)
        ra.append(s[vi:m.start()])
        ra.append(m.group(1) + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + m.group(3))
        vi = m.end()
    ra.append(s[vi:])
    return "".join(ra), sua


def main():
    the = doc_the("dat-nen-nam-ban/index.html") + doc_the("nha-ban-nam-ban/index.html")
    for c in the:
        if c["url"] in THEM_KHU:
            c["loc"].add(THEM_KHU[c["url"]])
    theo_url = {c["url"]: c for c in the}
    da_ban = {c["url"] for c in the if c["ban"]}

    for khu, thu_muc in TRANG_KHU.items():
        f = thu_muc + "/index.html"
        s = open(f, encoding="utf-8").read()

        i = s.index('<div class="prop-grid sp-sang">')
        i = s.index(">", i) + 1
        j = s.index("</div>", s.rindex("</article>"))

        # 1) thẻ đang có trên trang: giữ nguyên thứ tự
        cu = []
        for m in THE.finditer(s[i:j]):
            u = URL.search(m.group(2))
            if u:
                cu.append(u.group(1))
        cu = [u for u in dict.fromkeys(cu) if u not in da_ban]

        # 2) bổ sung mọi lô CÒN BÁN của khu
        them = [c for c in the
                if khu in c["loc"] and not c["ban"]
                and c["url"] not in CHO_XAC_NHAN and c["url"] not in cu]

        # 3) lô ĐÃ BÁN: KHÔNG gỡ bao giờ — để nguyên, chỉ mang nhãn "Đã bán".
        #    Bằng chứng giao dịch thật; khách xem giá lô đã bán để tự định giá lô
        #    đang xem. Xếp cuối để hàng mua được lên trước.
        ban = [c for c in the
               if khu in c["loc"] and c["ban"] and c["url"] not in CHO_XAC_NHAN]

        thu_tu = cu + [c["url"] for c in them] + [c["url"] for c in ban]
        so_ban = len(ban)
        html = []
        for k, u in enumerate(thu_tu):
            h = theo_url[u]["html"]
            h = h.replace('<article class="prop-card sp-row sp-feat"',
                          '<article class="prop-card sp-row"')
            if k == 0:                       # ảnh LCP của trang khu
                h = h.replace(' loading="lazy"', ' fetchpriority="high"', 1)
            else:
                h = h.replace(' fetchpriority="high"', ' loading="lazy"')
            html.append(h)
        s = s[:i] + "\n" + "\n".join(html) + "\n    " + s[j:]

        n = len(thu_tu)
        con = n - so_ban
        n_dat = sum(1 for u in thu_tu[:con] if u.startswith("/dat-nen/"))
        n_nha = con - n_dat
        cau = "%d lô đất" % n_dat + (" & %d nhà" % n_nha if n_nha else "") + " đang bán"
        if so_ban:
            cau += " · %d đã bán" % so_ban

        s = re.sub(r"Dưới đây là \d+ lô", "Dưới đây là %d lô" % con, s)
        s = re.sub(r"(<h2[^>]*>[^<]*?) — (?:\d+ lô đất(?: & \d+ nhà)?|lô) đang bán(?: · \d+ đã bán)?</h2>",
                   lambda m: "%s — %s</h2>" % (m.group(1), cau), s, count=1)

        ten = {u: ten_lo(theo_url[u]["html"]) for u in thu_tu}
        s, n_sua = sua_itemlist(s, thu_tu, ten)

        open(f, "w", encoding="utf-8").write(s)
        print("  /%s/  %d thẻ = %d đang bán (%d đất + %d nhà) + %d đã bán | thêm mới %d"
              % (thu_muc, n, con, n_dat, n_nha, so_ban, len(them)))

    print("\nGiữ lại chờ chủ xác nhận (%d lô, vẫn nằm trên hub chính):" % len(CHO_XAC_NHAN))
    for u, ly in CHO_XAC_NHAN.items():
        print("   %s\n      %s" % (u, ly))


if __name__ == "__main__":
    main()
