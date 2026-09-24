#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CẬP NHẬT TRANG "GIÁ ĐẤT NAM BAN HÔM NAY" TỪ LÔ THẬT ĐANG RAO — chạy mỗi thứ Hai.

ĐÃ TỪNG DÍNH (tin-4): tiêu đề hứa "cập nhật hàng tuần" nhưng bảng đứng im 83 ngày,
cột "So tuần trước" mãi ghi "(tuần đầu)". Khách gõ "giá đất Nam Ban hôm nay" — truy
vấn thương mại nóng nhất — vào thấy số cũ 3 tháng là mất tin ngay.

Số ở đây KHÔNG bịa: lấy data-area / data-price / data-loc của các thẻ lô CÒN BÁN
trên hub dat-nen-nam-ban/ (cùng nguồn với bộ lọc), quy ra triệu/m², lấy P10–P90
(bỏ 10% hai đầu để lô ngoại lệ không kéo lệch) + trung vị. Lịch sử tuần lưu
data/gia-tuan.json để điền cột "So tuần trước". Giữ tối đa 8 tuần trên trang.

Script SỞ HỮU các khối sau trên trang (đừng sửa tay, chạy lại là mất):
  <!-- TRA-LOI-NHANH -->  câu trả lời 40–60 chữ ngay đầu bài (AEO/GEO: AI trích thẳng)
  <!-- WEEKLY-PRICE -->   bảng tuần (P10–P90 · trung vị · so tuần trước)
  <!-- GIA-KHU -->        bảng theo khu (7 khu, link sang trang khu)
  <details data-faq="m2"> / data-faq="re">  2 câu FAQ có số (schema FAQPage sinh lại từ HTML)
  <title>, meta description, og/twitter title, H1, .article-cat, JSON-LD (Article/Dataset/WebPage)

    python3 scripts/cap-nhat-gia-hom-nay.py            # cập nhật theo hôm nay
"""
import datetime
import html as H
import json
import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TRANG = "thi-truong/gia-dat-nam-ban-hom-nay/index.html"
URL = "https://nambanvillas.vn/thi-truong/gia-dat-nam-ban-hom-nay/"
LICH_SU = "data/gia-tuan.json"
HUB = "dat-nen-nam-ban/index.html"
TD = "padding:10px 12px;border-bottom:1px solid #ECEAE4"
TH = "padding:10px 12px;border-bottom:2px solid #1A3D2B"
TEL = "tel:0978758788"
ZALO = "https://zalo.me/0978758788"

KHU = [  # (data-loc, tên, trang khu)
    ("nam-ban", "Trung tâm Nam Ban (thị trấn cũ)", "/dat-trung-tam-thi-tran-nam-ban/"),
    ("dong-thanh", "Đông Thanh", "/dat-dong-thanh-nam-ban/"),
    ("me-linh", "Mê Linh", "/dat-me-linh-nam-ban/"),
    ("gia-lam", "Gia Lâm", "/dat-gia-lam-nam-ban/"),
    ("ho-bai-cong", "Hồ Bãi Công", "/dat-ho-bai-cong-nam-ban/"),
    ("tu-liem", "Từ Liêm", "/dat-tu-liem-nam-ban/"),
    ("nam-ha", "Nam Hà (giáp Nam Ban)", "/dat-nam-ha-nam-ban/"),
]
TEN = {"tho": "Đất nền có thổ cư (dưới 3.000m²)", "vuon": "Đất vườn / lô lớn từ 3.000m²", "ho": "Đất view hồ / view đẹp"}


def q(v, p):
    v = sorted(v)
    k = (len(v) - 1) * p
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def so(x):
    """1.42 -> '1,4' · 0.52 -> '0,5'"""
    return ("%.1f" % x).replace(".", ",")


def tien(ty):
    """0.599 -> '599 triệu' · 1.5 -> '1,5 tỷ'"""
    if ty >= 1:
        return ("%.2f" % ty).rstrip("0").rstrip(".").replace(".", ",") + " tỷ"
    return "%d triệu" % round(ty * 1000)


def ngay_vn(iso):
    d = datetime.date.fromisoformat(iso)
    return "%d/%d/%d" % (d.day, d.month, d.year)


def doc_lo():
    s = open(HUB, encoding="utf-8").read()
    ra = []
    for m in re.finditer(r'<article class="prop-card sp-row[^"]*"([^>]*)>', s):
        at = m.group(1)
        if 'data-ban="1"' in at:
            continue
        a = re.search(r'data-area="([\d.]+)"', at)
        p = re.search(r'data-price="([\d.]+)"', at)
        if not a or not p:
            continue
        area, price = float(a.group(1)), float(p.group(1))   # m², tỷ
        if area <= 0 or price <= 0:
            continue
        nhan = (re.search(r'data-nhan="([^"]*)"', at) or [None, ""])[1]
        loc = (re.search(r'data-loc="([^"]*)"', at) or [None, ""])[1]
        u = re.search(r'href="(/dat-nen/[^"]+/)"', s[m.end():m.end() + 600])
        t = re.search(r'<h3 class="sp-title"><a[^>]*>([^<]*)', s[m.end():m.end() + 1500])
        ra.append(dict(area=area, ty=price, m2=price * 1000 / area, nhan=nhan, loc=loc.split(),
                       url=u.group(1) if u else "", ten=H.unescape(t.group(1)) if t else ""))
    return ra


def thong_ke(v):
    return dict(n=len(v), lo=round(q(v, .1), 2), tv=round(statistics.median(v), 2), hi=round(q(v, .9), 2))


def tinh(lo):
    nhom = {
        "tho": [x["m2"] for x in lo if "vuon" not in x["nhan"] and x["area"] < 3000],
        "vuon": [x["m2"] for x in lo if "vuon" in x["nhan"] or x["area"] >= 3000],
        "ho": [x["m2"] for x in lo if "ho-bai-cong" in x["loc"] or "view-dep" in x["nhan"]],
    }
    return {k: thong_ke(v) for k, v in nhom.items() if len(v) >= 3}


def tinh_khu(lo):
    ra = []
    for key, ten, link in KHU:
        v = [x for x in lo if key in x["loc"]]
        if len(v) < 3:
            continue
        t = thong_ke([x["m2"] for x in v])
        t.update(ten=ten, link=link, re_nhat=min(x["ty"] for x in v))
        ra.append(t)
    return ra


def so_sanh(moi, cu):
    if not cu:
        return "— (tuần đầu tính từ lô thật)"
    d = moi["tv"] - cu["tv"]
    if abs(d) < 0.05:
        return "Đi ngang (trung vị %s)" % so(cu["tv"])
    return "%s %s triệu/m² so với trung vị tuần trước (%s)" % ("Tăng" if d > 0 else "Giảm", so(abs(d)), so(cu["tv"]))


def bang_tuan(ngay, kq, cu, tong):
    tr = []
    for k in ("tho", "vuon", "ho"):
        if k not in kq:
            continue
        v = kq[k]
        tr.append('            <tr><td style="%s">%s <span style="color:#6B6B6B;font-size:.8rem">(%d lô)</span></td>'
                  '<td style="%s"><strong>%s – %s</strong> · trung vị %s</td><td style="%s">%s</td></tr>'
                  % (TD, TEN[k], v["n"], TD, so(v["lo"]), so(v["hi"]), so(v["tv"]), TD, so_sanh(v, (cu or {}).get(k))))
    return '''        <!-- WEEK:%s -->
        <h2>Tuần %s</h2>
        <div style="overflow-x:auto">
        <table style="width:100%%;border-collapse:collapse;font-size:.92rem;margin-bottom:8px">
          <caption style="text-align:left;font-size:.82rem;color:#5F6E66;padding:0 0 8px">Giá rao đất Nam Ban theo loại, tuần %s — triệu đồng/m²</caption>
          <thead>
            <tr style="background:#F2F6F3;text-align:left">
              <th scope="col" style="%s">Loại đất</th>
              <th scope="col" style="%s">Giá rao (triệu/m², khoảng 10%%–90%%)</th>
              <th scope="col" style="%s">So tuần trước</th>
            </tr>
          </thead>
          <tbody>
%s
          </tbody>
        </table>
        </div>
        <p style="font-size:.9rem;color:#3D3D3D"><strong>Cách tính:</strong> từ %d lô đang rao trên Nam Ban Villas ngày %s (cùng dữ liệu với bộ lọc trang Đất Nền), quy ra triệu/m² theo giá rao cả lô; bỏ 10%% lô rẻ nhất và 10%% lô đắt nhất để lô ngoại lệ không kéo lệch. Giá chốt thật thường thấp hơn giá rao.</p>

''' % (ngay, ngay_vn(ngay), ngay_vn(ngay), TH, TH, TH, "\n".join(tr), tong, ngay_vn(ngay))


def bang_khu(ngay, khu):
    tr = []
    for t in khu:
        tr.append('            <tr><td style="%s"><a href="%s" style="color:#1A3D2B;font-weight:600">%s</a> <span style="color:#6B6B6B;font-size:.8rem">(%d lô)</span></td>'
                  '<td style="%s"><strong>%s – %s</strong></td><td style="%s">%s</td><td style="%s">từ %s/lô</td></tr>'
                  % (TD, t["link"], t["ten"], t["n"], TD, so(t["lo"]), so(t["hi"]), TD, so(t["tv"]), TD, tien(t["re_nhat"])))
    return '''<!-- GIA-KHU:START -->
        <h2>Giá đất Nam Ban theo khu — khu nào rẻ, khu nào đắt?</h2>
        <p>Cùng một xã Nam Ban nhưng đơn giá giữa các khu chênh nhau 2–3 lần. Bảng dưới tính từ chính các lô đang rao ngày %s: bấm tên khu để xem từng lô, sổ và giá.</p>
        <div style="overflow-x:auto">
        <table style="width:100%%;border-collapse:collapse;font-size:.92rem;margin:14px 0 8px">
          <caption style="text-align:left;font-size:.82rem;color:#5F6E66;padding:0 0 8px">Giá rao đất Nam Ban theo khu, ngày %s — triệu đồng/m² (khoảng 10%%–90%%)</caption>
          <thead>
            <tr style="background:#F2F6F3;text-align:left">
              <th scope="col" style="%s">Khu</th>
              <th scope="col" style="%s">Giá rao (triệu/m²)</th>
              <th scope="col" style="%s">Trung vị</th>
              <th scope="col" style="%s">Lô rẻ nhất</th>
            </tr>
          </thead>
          <tbody>
%s
          </tbody>
        </table>
        </div>
        <!-- GIA-KHU:END -->''' % (ngay_vn(ngay), ngay_vn(ngay), TH, TH, TH, TH, "\n".join(tr))


def cau_tra_loi(ngay, kq, khu, tong):
    """40–60 chữ, số thật, đọc xong là có câu trả lời."""
    t = kq["tho"]
    re_nhat = min(khu, key=lambda x: x["tv"]) if khu else None
    dat_nhat = max(khu, key=lambda x: x["tv"]) if khu else None
    cau = ('Giá đất Nam Ban hôm nay (%s): đất nền có thổ cư <strong>%s–%s triệu/m²</strong>, trung vị %s triệu/m², '
           'tính từ %d lô đang rao trên Nam Ban Villas.' % (ngay_vn(ngay), so(t["lo"]), so(t["hi"]), so(t["tv"]), tong))
    if "vuon" in kq:
        cau += ' Đất vườn, lô lớn %s–%s triệu/m².' % (so(kq["vuon"]["lo"]), so(kq["vuon"]["hi"]))
    if re_nhat and dat_nhat and re_nhat is not dat_nhat:
        cau += ' Rẻ nhất: %s (trung vị %s); cao nhất: %s (%s).' % (re_nhat["ten"], so(re_nhat["tv"]), dat_nhat["ten"], so(dat_nhat["tv"]))
    cau += ' Giá chốt thường thấp hơn giá rao.'
    return cau


def khoi_tra_loi(cau):
    return '''<!-- TRA-LOI-NHANH:START -->
        <div id="tra-loi-nhanh" class="tra-loi-nhanh">
          <p class="tra-loi-nhanh-nhan">Trả lời nhanh</p>
          <p class="tra-loi-nhanh-cau">%s</p>
          <div class="goi-nhanh-nut"><a href="%s" class="goi-nhanh-goi">Gọi 0978 758 788 hỏi giá lô cụ thể</a><a href="%s" target="_blank" rel="noopener" class="goi-nhanh-zalo">Nhắn Zalo</a></div>
        </div>
        <!-- TRA-LOI-NHANH:END -->''' % (cau, TEL, ZALO)


def thay_khoi(s, mo, dong, moi):
    i = s.index(mo)
    j = s.index(dong) + len(dong)
    return s[:i] + moi + s[j:]


def faq_html(s, key, tra_loi):
    """Thay phần <p>…</p> của <details data-faq=key> — chỉ trong 1 thẻ, không nuốt khối."""
    i = s.index('data-faq="%s">' % key)          # mọi kiểu <details … data-faq="key">
    a = s.index("<p>", i) + 3
    b = s.index("</p>", a)
    return s[:a] + tra_loi + s[b:]


def faq_schema_tu_html(s):
    """FAQPage sinh lại từ HTML để 2 bên KHÔNG BAO GIỜ lệch (Google phạt lệch)."""
    ra = []
    sec = s[s.index('<section class="faq-hien"'):]
    sec = sec[:sec.index("</section>")]
    for m in re.finditer(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", sec, re.S):
        hoi = H.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        dap = H.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        ra.append({"@type": "Question", "name": hoi, "acceptedAnswer": {"@type": "Answer", "text": dap}})
    return ra


def sua_schema(s, ngay, tieu_de, mo_ta, cau, kq, tong):
    def fix(m):
        g = json.loads(m.group(1))
        nodes = g["@graph"]
        co_webpage = co_dataset = False
        for n in nodes:
            t = n.get("@type")
            if t == "Article":
                n["headline"] = tieu_de
                n["description"] = mo_ta
                n["dateModified"] = ngay
                n["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": ["#tra-loi-nhanh", ".article-title"]}
                n["about"] = {"@type": "Place", "name": "Nam Ban, Lâm Hà, Lâm Đồng"}
                n["mainEntityOfPage"] = {"@id": URL + "#webpage"}
            elif t == "FAQPage":
                n["mainEntity"] = faq_schema_tu_html(s)
                n["isPartOf"] = {"@id": URL + "#webpage"}
            elif t == "WebPage":
                co_webpage = True
                n.update({"url": URL, "name": tieu_de, "description": mo_ta, "dateModified": ngay,
                          "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#tra-loi-nhanh", ".article-title"]}})
            elif t == "Dataset":
                co_dataset = True
                n.update(dataset(ngay, mo_ta, kq, tong))
        if not co_webpage:
            nodes.append({"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": tieu_de, "description": mo_ta,
                          "inLanguage": "vi", "isPartOf": {"@id": "https://nambanvillas.vn/#website"},
                          "publisher": {"@id": "https://nambanvillas.vn/#organization"}, "dateModified": ngay,
                          "primaryImageOfPage": {"@type": "ImageObject", "url": "https://nambanvillas.vn/images/og-namban.jpg"},
                          "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#tra-loi-nhanh", ".article-title"]}})
        if not co_dataset:
            nodes.append(dataset(ngay, mo_ta, kq, tong))
        return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>"
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, count=1, flags=re.S)


def dataset(ngay, mo_ta, kq, tong):
    bien = []
    for k in ("tho", "vuon", "ho"):
        if k in kq:
            bien.append({"@type": "PropertyValue", "name": TEN[k], "unitText": "triệu đồng/m²",
                         "minValue": kq[k]["lo"], "maxValue": kq[k]["hi"], "value": kq[k]["tv"],
                         "description": "Khoảng 10%%–90%% và trung vị từ %d lô đang rao" % kq[k]["n"]})
    return {"@type": "Dataset", "@id": URL + "#dataset", "name": "Giá rao đất Nam Ban theo tuần (triệu đồng/m²)",
            "description": mo_ta, "url": URL, "inLanguage": "vi", "license": "https://creativecommons.org/licenses/by/4.0/",
            "creator": {"@id": "https://nambanvillas.vn/#organization"}, "dateModified": ngay,
            "temporalCoverage": "2026-07-02/" + ngay, "isAccessibleForFree": True,
            "spatialCoverage": {"@type": "Place", "name": "Nam Ban, Lâm Hà, Lâm Đồng",
                                "geo": {"@type": "GeoCoordinates", "latitude": 11.8347, "longitude": 108.2622}},
            "measurementTechnique": "Quy giá rao cả lô ra triệu đồng/m² từ %d lô đang rao trên Nam Ban Villas; lấy khoảng 10%%–90%% và trung vị" % tong,
            "variableMeasured": bien,
            "distribution": {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "https://nambanvillas.vn/data/gia-tuan.json"}}


GIA_RE = "dat-nam-ban-gia-re/index.html"
URL_GIA_RE = "https://nambanvillas.vn/dat-nam-ban-gia-re/"


def cap_nhat_gia_re(ngay, lo, kq, khu):
    """Trang /dat-nam-ban-gia-re/ đang top 4 "giá đất nam ban": giữ số sống, tháng trong title,
    khối 'Giá đất Nam Ban hiện tại' + 2 FAQ số thật, FAQPage sinh lại từ HTML."""
    if not os.path.exists(GIA_RE):
        return
    s = open(GIA_RE, encoding="utf-8").read()
    t = kq["tho"]
    d = datetime.date.fromisoformat(ngay)
    co_gia = [x for x in lo if x["ty"] > 0]
    re_nhat = min(co_gia, key=lambda x: x["ty"])
    duoi_1ty = sum(1 for x in co_gia if x["ty"] < 1)
    duoi_700 = sum(1 for x in co_gia if x["ty"] < 0.7)
    khu_re = min(khu, key=lambda x: x["tv"])
    khu_dat = max(khu, key=lambda x: x["tv"])
    khoi = ('<!-- GIA-RE-SO:START -->\n'
            '  <h2>Giá đất Nam Ban hiện tại bao nhiêu một m²?</h2>\n'
            '  <p>Tính ngày %s từ %d lô đang rao trên Nam Ban Villas: đất nền có thổ cư <strong>%s–%s triệu/m²</strong>, trung vị %s triệu/m². '
            'Khu rẻ nhất là %s (trung vị %s), đắt nhất là %s (%s). Với 500 triệu, ở mức trung vị mua được khoảng %d m².</p>\n'
            '  <p>Bên Nam Ban Villas đang có <strong>%d lô dưới 1 tỷ</strong> (trong đó %d lô dưới 700 triệu); rẻ nhất từ <strong>%s</strong>: '
            '<a href="%s">%s</a>. Số này đổi theo tuần — bảng đầy đủ theo loại và theo 7 khu ở <a href="/thi-truong/gia-dat-nam-ban-hom-nay/">giá đất Nam Ban hôm nay</a>.</p>\n'
            '  <!-- GIA-RE-SO:END -->'
            % (ngay_vn(ngay), len(lo), so(t["lo"]), so(t["hi"]), so(t["tv"]), khu_re["ten"], so(khu_re["tv"]), khu_dat["ten"], so(khu_dat["tv"]),
               round(500 / t["tv"]), duoi_1ty, duoi_700, tien(re_nhat["ty"]), re_nhat["url"], H.escape(re_nhat["ten"], quote=False)))
    s = thay_khoi(s, "<!-- GIA-RE-SO:START -->", "<!-- GIA-RE-SO:END -->", khoi)
    s = faq_html(s, "re-nhat", "Trong các tin đang rao trên thị trường có lô quanh mức 390–450 triệu, ví dụ 450 triệu cho 163m². "
                 "Bên Nam Ban Villas ngày %s có lô từ %s (%s), và %d lô dưới 700 triệu. Giá và cấu hình đổi theo thời điểm; giá trên tin rao không phải giá giao dịch."
                 % (ngay_vn(ngay), tien(re_nhat["ty"]), H.escape(re_nhat["ten"], quote=False), duoi_700))
    s = faq_html(s, "m2", "Tính ngày %s từ %d lô đang rao: đất nền có thổ cư %s–%s triệu/m² (trung vị %s); đất vườn, lô lớn %s–%s triệu/m². "
                 "Khu rẻ nhất %s trung vị %s, khu đắt nhất %s trung vị %s. Cập nhật mỗi thứ Hai ở trang giá đất Nam Ban hôm nay."
                 % (ngay_vn(ngay), len(lo), so(t["lo"]), so(t["hi"]), so(t["tv"]),
                    so(kq["vuon"]["lo"]) if "vuon" in kq else "", so(kq["vuon"]["hi"]) if "vuon" in kq else "",
                    khu_re["ten"], so(khu_re["tv"]), khu_dat["ten"], so(khu_dat["tv"])))
    s = re.sub(r"T\d{1,2}/\d{4}", "T%d/%d" % (d.month, d.year), s)     # tháng trong title/og
    # mô tả hiện trên Google: chứa đúng cụm "Giá đất Nam Ban" + số m² + lô rẻ nhất + hotline (≤160 ký tự)
    mo_ta = ("Giá đất Nam Ban T%d/%d: đất nền thổ cư %s–%s triệu/m². Đất giá rẻ từ %s, %d lô dưới 1 tỷ, sổ riêng. Gọi 0978 758 788."
             % (d.month, d.year, so(t["lo"]), so(t["hi"]), tien(re_nhat["ty"]), duoi_1ty))
    for k in ('<meta name="description" content="', '<meta property="og:description" content="', '<meta name="twitter:description" content="'):
        if k in s:
            i = s.index(k) + len(k)
            s = s[:i] + H.escape(mo_ta, quote=True) + s[s.index('"', i):]
    s = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', '"dateModified":"%s"' % ngay, s)

    def fix(m):
        g = json.loads(m.group(1))
        for n in g["@graph"]:
            if n.get("@type") == "FAQPage":
                ra = []
                for mm in re.finditer(r'<details open class="gr-faq"[^>]*><summary>(.*?)</summary><p>(.*?)</p>', s, re.S):
                    ra.append({"@type": "Question", "name": H.unescape(re.sub(r"<[^>]+>", "", mm.group(1))).strip(),
                               "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub(r"<[^>]+>", "", mm.group(2))).strip()}})
                n["mainEntity"] = ra
            if n.get("@type") == "WebPage":
                n["speakable"] = {"@type": "SpeakableSpecification", "cssSelector": [".gr-h1", ".gr-nhanh"]}
        return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>"
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, count=1, flags=re.S)
    open(GIA_RE, "w", encoding="utf-8").write(s)
    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"(<loc>%s</loc><lastmod>)\d{4}-\d{2}-\d{2}" % re.escape(URL_GIA_RE), r"\g<1>" + ngay, sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("  giá rẻ: %d lô dưới 1 tỷ, rẻ nhất %s" % (duoi_1ty, tien(re_nhat["ty"])))


def main():
    ngay = datetime.date.today().isoformat()
    lo = doc_lo()
    kq = tinh(lo)
    khu = tinh_khu(lo)
    tong = len(lo)
    ls = json.load(open(LICH_SU, encoding="utf-8")) if os.path.exists(LICH_SU) else {}
    truoc = [k for k in sorted(ls) if k < ngay]
    cu = ls[truoc[-1]] if truoc else None
    ls[ngay] = dict(kq, khu={t["link"]: {k: t[k] for k in ("n", "lo", "tv", "hi")} for t in khu}, tong=tong)
    os.makedirs("data", exist_ok=True)
    json.dump(ls, open(LICH_SU, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    s = open(TRANG, encoding="utf-8").read()
    t = kq["tho"]
    cau = cau_tra_loi(ngay, kq, khu, tong)
    tieu_de = "Giá Đất Nam Ban Hôm Nay %s: %s–%s Triệu/m² (Từ %d Lô Thật)" % (ngay_vn(ngay), so(t["lo"]), so(t["hi"]), tong)
    mo_ta = ("Giá đất Nam Ban hôm nay %s: đất nền thổ cư %s–%s triệu/m² (trung vị %s), theo 7 khu, tính từ %d lô đang rao. "
             "Cập nhật mỗi thứ Hai. Gọi 0978 758 788." % (ngay_vn(ngay), so(t["lo"]), so(t["hi"]), so(t["tv"]), tong))

    # 1) khối trả lời nhanh · 2) bảng tuần · 3) bảng khu
    s = thay_khoi(s, "<!-- TRA-LOI-NHANH:START -->", "<!-- TRA-LOI-NHANH:END -->", khoi_tra_loi(cau))
    i = s.index("<!-- WEEKLY-PRICE:START")
    i = s.index("\n", i) + 1
    j = s.index("        <!-- WEEKLY-PRICE:END -->")
    tuan = re.split(r"(?=        <!-- WEEK:)", s[i:j])
    tuan = [x for x in tuan if x.strip() and ("<!-- WEEK:%s -->" % ngay) not in x][:7]
    s = s[:i] + "\n" + bang_tuan(ngay, kq, cu, tong) + "".join(tuan) + s[j:]
    s = thay_khoi(s, "<!-- GIA-KHU:START -->", "<!-- GIA-KHU:END -->", bang_khu(ngay, khu))

    # 4) FAQ có số sống
    khu_re = sorted(khu, key=lambda x: x["tv"])[:3]
    s = faq_html(s, "m2", "Tính ngày %s từ %d lô đang rao trên Nam Ban Villas: đất nền có thổ cư %s–%s triệu/m² (trung vị %s)%s%s. "
                 "Đây là giá rao, giá chốt thực tế thường thấp hơn 5–15%%."
                 % (ngay_vn(ngay), tong, so(t["lo"]), so(t["hi"]), so(t["tv"]),
                    ", đất vườn và lô lớn %s–%s triệu/m²" % (so(kq["vuon"]["lo"]), so(kq["vuon"]["hi"])) if "vuon" in kq else "",
                    ", đất view hồ và view đẹp %s–%s triệu/m²" % (so(kq["ho"]["lo"]), so(kq["ho"]["hi"])) if "ho" in kq else ""))
    if khu_re:
        s = faq_html(s, "re", "Theo lô đang rao ngày %s, đơn giá trung vị thấp nhất ở %s. Lô rẻ nhất toàn xã hiện từ %s. "
                     "Lô trung tâm, view hồ và đất vườn diện tích lớn cao hơn mặt bằng chung."
                     % (ngay_vn(ngay), "; ".join("%s (%s triệu/m², từ %s/lô)" % (k["ten"], so(k["tv"]), tien(k["re_nhat"])) for k in khu_re),
                        tien(min(x["ty"] for x in lo))))

    if '<details open data-faq="500tr">' in s:
        s = faq_html(s, "500tr", "Ở đơn giá trung vị %s triệu/m² (ngày %s), 500 triệu tương đương khoảng %d m² đất nền có thổ cư; "
                     "chọn khu rẻ như %s thì được khoảng %d m², chọn khu đắt như %s thì chỉ khoảng %d m². "
                     "Thực tế còn tuỳ phần thổ cư và đường vào của từng lô — xem danh sách <a href=\"/dat-nam-ban-duoi-1-ty/\">đất Nam Ban dưới 1 tỷ</a>."
                     % (so(t["tv"]), ngay_vn(ngay), round(500 / t["tv"]),
                        min(khu, key=lambda x: x["tv"])["ten"], round(500 / min(khu, key=lambda x: x["tv"])["tv"]),
                        max(khu, key=lambda x: x["tv"])["ten"], round(500 / max(khu, key=lambda x: x["tv"])["tv"])))

    # 5) tiêu đề, mô tả, H1, nhãn ngày
    s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % H.escape(tieu_de, quote=False), s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="%s"' % H.escape(mo_ta, quote=True), s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="%s"' % H.escape(tieu_de, quote=True), s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*"', '<meta property="og:description" content="%s"' % H.escape(mo_ta, quote=True), s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*"', '<meta name="twitter:title" content="%s"' % H.escape(tieu_de, quote=True), s, count=1)
    s = re.sub(r'<h1 class="article-title">[^<]*</h1>',
               '<h1 class="article-title">Giá Đất Nam Ban Hôm Nay (%s) — Tính Từ %d Lô Thật Đang Rao, Cập Nhật Mỗi Thứ Hai</h1>' % (ngay_vn(ngay), tong), s, count=1)
    s = re.sub(r"Cập nhật tuần: \d+/\d+/\d+", "Cập nhật tuần: %s" % ngay_vn(ngay), s)
    s = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', '"dateModified":"%s"' % ngay, s)
    s = sua_schema(s, ngay, tieu_de, mo_ta, cau, kq, tong)
    open(TRANG, "w", encoding="utf-8").write(s)

    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"(<loc>%s</loc><lastmod>)\d{4}-\d{2}-\d{2}" % re.escape(URL), r"\g<1>" + ngay, sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    cap_nhat_gia_re(ngay, [x for x in lo if x["ty"] > 0], kq, khu)
    for k, v in kq.items():
        print("  %-5s %3d lô  %s – %s  trung vị %s" % (k, v["n"], so(v["lo"]), so(v["hi"]), so(v["tv"])))
    print("  khu:", ", ".join("%s %s" % (t["ten"], so(t["tv"])) for t in khu))
    print("Đã cập nhật %s (%s)" % (TRANG, ngay))
    return 0


if __name__ == "__main__":
    sys.exit(main())
