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


# ── TRANG /gia-dat-lam-ha/ — từ khoá "giá đất Lâm Hà" (Google gợi ý dưới "giá đất nam ban") ──
# Sinh TRỌN trang mỗi tuần từ cùng dữ liệu lô. Phạm vi nói thật: chỉ xã Nam Ban (gồm thị trấn
# Nam Ban cũ, Đông Thanh, Mê Linh, Gia Lâm — NQ 202/2025/QH15) và xã Nam Hà, nơi có lô thật.
LAM_HA = "gia-dat-lam-ha/index.html"
URL_LH = "https://nambanvillas.vn/gia-dat-lam-ha/"
XA_NAM_BAN = {"nam-ban", "dong-thanh", "me-linh", "gia-lam", "ho-bai-cong", "tu-liem"}

THAN_LAM_HA = """<main id="main">
  <div class="breadcrumb-bar">
    <div class="container">
      <nav class="breadcrumb" aria-label="Đường dẫn">
        <a href="/">Trang chủ</a><span class="bc-sep">›</span>
        <a href="/thi-truong/">Thị Trường</a><span class="bc-sep">›</span>
        <span>Giá Đất Nam Ban Lâm Hà</span>
      </nav>
    </div>
  </div>

  <div class="article-wrap">
    <div class="container">
      <div class="article-header">
        <p class="article-cat">Giá thị trường · Cập nhật: %(ngay)s</p>
        <h1 class="article-title">Giá Đất Nam Ban Lâm Hà Tháng %(thang)s — Theo Xã, Theo Khu, Tính Từ Lô Thật Đang Rao</h1>
        <p class="article-lead">Giá đất Nam Ban Lâm Hà không có một con số chung: cùng vùng nhưng khu này có thể gấp đôi khu kia. Trang này tính thẳng từ các lô đang rao ở xã Nam Ban và xã Nam Hà, cập nhật mỗi thứ Hai.</p>
      </div>

      <div class="article-body">
        <div id="tra-loi-nhanh" class="tra-loi-nhanh">
          <p class="tra-loi-nhanh-nhan">Trả lời nhanh</p>
          <p class="tra-loi-nhanh-cau">%(cau)s</p>
          <div class="goi-nhanh-nut"><a href="tel:0978758788" class="goi-nhanh-goi">Gọi 0978 758 788 hỏi lô cụ thể</a><a href="https://zalo.me/0978758788" target="_blank" rel="noopener" class="goi-nhanh-zalo">Nhắn Zalo</a></div>
        </div>

        <h2>Lâm Hà, Nam Ban bây giờ gồm những xã nào?</h2>
        <p>Từ 01/7/2025 cả nước bỏ cấp huyện, nên "huyện Lâm Hà" (vùng Nam Ban) không còn trên giấy tờ mới. Theo Nghị quyết 202/2025/QH15, <strong>xã Nam Ban</strong> mới gồm thị trấn Nam Ban cũ, xã Đông Thanh, xã Mê Linh và xã Gia Lâm. <strong>Xã Nam Hà</strong> nằm liền kề. Người mua vẫn gọi cả vùng là Nam Ban, Lâm Hà, nên trang này dùng tên đó. Chi tiết ở bài <a href="/ve-nam-ban/xa-nam-ban-sap-nhap/">xã Nam Ban sau sáp nhập gồm những xã nào</a>.</p>

        <h2>Giá đất Nam Ban Lâm Hà theo xã</h2>
        <div style="overflow-x:auto">
        <table style="width:100%%;border-collapse:collapse;font-size:.92rem;margin:14px 0 8px">
          <caption style="text-align:left;font-size:.82rem;color:#5F6E66;padding:0 0 8px">Giá rao đất Nam Ban Lâm Hà theo xã, ngày %(ngay)s — triệu đồng/m² (khoảng 10%%–90%%)</caption>
          <thead><tr style="background:#F2F6F3;text-align:left"><th scope="col" style="%(th)s">Xã</th><th scope="col" style="%(th)s">Giá rao (triệu/m²)</th><th scope="col" style="%(th)s">Lô dưới 1 tỷ</th><th scope="col" style="%(th)s">Lô rẻ nhất</th></tr></thead>
          <tbody>
%(hang_xa)s
          </tbody>
        </table>
        </div>

        <h2>Khu nào ở Nam Ban, Lâm Hà rẻ nhất, khu nào đắt nhất?</h2>
        <p>Xếp từ khu có đơn giá trung vị thấp nhất lên cao nhất. Bấm tên khu để xem toàn bộ lô, bấm giá để mở lô rẻ nhất khu đó.</p>
        <div style="overflow-x:auto">
        <table style="width:100%%;border-collapse:collapse;font-size:.92rem;margin:14px 0 8px">
          <caption style="text-align:left;font-size:.82rem;color:#5F6E66;padding:0 0 8px">Đơn giá trung vị theo khu, ngày %(ngay)s</caption>
          <thead><tr style="background:#F2F6F3;text-align:left"><th scope="col" style="%(th)s">Khu</th><th scope="col" style="%(th)s">Trung vị</th><th scope="col" style="%(th)s">Lô dưới 1 tỷ</th><th scope="col" style="%(th)s">Lô rẻ nhất</th></tr></thead>
          <tbody>
%(hang_khu)s
          </tbody>
        </table>
        </div>

        <h2>Giá đất Nam Ban Lâm Hà theo loại đất</h2>
        <p><strong>Đất nền có thổ cư</strong> (dưới 3.000m²): %(tho)s triệu/m², trung vị %(tho_tv)s. <strong>Đất vườn và lô lớn</strong> từ 3.000m²: %(vuon)s triệu/m². <strong>Đất view hồ, view đẹp</strong>: %(ho)s triệu/m². Tính từ %(tong)d lô, bỏ 10%% lô rẻ nhất và 10%% lô đắt nhất để lô ngoại lệ không kéo lệch.</p>
        <p>Muốn xem so sánh theo từng tuần thì mở <a href="/thi-truong/gia-dat-nam-ban-hom-nay/">giá đất Nam Ban hôm nay</a>. Ngân sách nhẹ thì đọc <a href="/dat-nam-ban-gia-re/">đất Nam Ban giá rẻ có gì trong tầm 450 triệu–1 tỷ</a>. Lô lớn tính theo sào ở <a href="/dat-vuon-nam-ban/">đất vườn, đất sào Nam Ban giá rẻ</a>.</p>

        <div class="goi-nhanh goi-giua-bai"><p>Đang nhắm một lô ở Nam Ban, Lâm Hà? Gọi hỏi thẳng giá chốt, sổ và quy hoạch của lô đó — <strong>trả lời trong ngày, không ràng buộc</strong>.</p><div class="goi-nhanh-nut"><a href="tel:0978758788" class="goi-nhanh-goi">Gọi 0978 758 788</a><a href="https://zalo.me/0978758788" target="_blank" rel="noopener" class="goi-nhanh-zalo">Nhắn Zalo</a></div></div>

        <h2>Giá này lấy từ đâu?</h2>
        <p>Mỗi thứ Hai, đội ngũ Nam Ban Villas tổng hợp diện tích và giá rao của mọi lô còn bán trên trang <a href="/dat-nen-nam-ban/">Đất Nền Nam Ban</a>, quy ra triệu đồng/m² rồi tính khoảng 10%%–90%% và trung vị. Số nào cũng đối chiếu được với lô thật đang rao. Dữ liệu các tuần lưu công khai ở <a href="/data/gia-tuan.json">gia-tuan.json</a>. Giá nhà nước dùng tính thuế là chuyện khác, xem <a href="/thi-truong/bang-gia-dat-2026-nam-ban/">bảng giá đất 2026 ảnh hưởng gì tới người mua</a>.</p>
      </div>
    </div>
  </div>

<section class="faq-hien" aria-label="Câu hỏi thường gặp">
  <h2>Câu hỏi thường gặp về giá đất Nam Ban Lâm Hà</h2>
%(faq)s
</section>
"""


def _td(x):
    return '<td style="%s">%s</td>' % (TD, x)


def lam_trang_lam_ha(ngay, lo, kq, khu):
    nguon = open(TRANG, encoding="utf-8").read()
    t = kq["tho"]
    d = datetime.date.fromisoformat(ngay)
    xa = []
    for ten, link, dk in (("Xã Nam Ban", "/dat-nen-nam-ban/", lambda x: XA_NAM_BAN & set(x["loc"])),
                          ("Xã Nam Hà", "/dat-nam-ha-nam-ban/", lambda x: "nam-ha" in x["loc"])):
        v = [x for x in lo if dk(x)]
        if len(v) >= 3:
            st = thong_ke([x["m2"] for x in v])
            st.update(ten=ten, link=link, re=min(v, key=lambda x: x["ty"]), duoi1=sum(1 for x in v if x["ty"] < 1))
            xa.append(st)
    tong = len(lo)
    duoi1 = sum(1 for x in lo if x["ty"] < 1)
    re_nhat = min(lo, key=lambda x: x["ty"])
    khu_re, khu_dat = min(khu, key=lambda x: x["tv"]), max(khu, key=lambda x: x["tv"])
    vuon = "%s–%s" % (so(kq["vuon"]["lo"]), so(kq["vuon"]["hi"])) if "vuon" in kq else "–"

    tieu_de = "Giá Đất Nam Ban Lâm Hà T%d/%d: Theo Xã, Theo Khu, Tính Từ Lô Thật" % (d.month, d.year)
    mo_ta = ("Giá đất Nam Ban Lâm Hà T%d/%d: đất nền thổ cư %s–%s triệu/m², xã Nam Ban và Nam Hà, %d lô dưới 1 tỷ, rẻ nhất %s. Gọi 0978 758 788."
             % (d.month, d.year, so(t["lo"]), so(t["hi"]), duoi1, tien(re_nhat["ty"])))
    cau = ("Giá đất Nam Ban Lâm Hà tháng %d/%d, tính từ %d lô đang rao ở xã Nam Ban và xã Nam Hà: đất nền có thổ cư <strong>%s–%s triệu/m²</strong>, "
           "trung vị %s triệu/m²; đất vườn, lô lớn %s triệu/m². Có %d lô dưới 1 tỷ, rẻ nhất từ %s."
           % (d.month, d.year, tong, so(t["lo"]), so(t["hi"]), so(t["tv"]), vuon, duoi1, tien(re_nhat["ty"])))

    hang_xa = "\n".join("            <tr>%s%s%s%s</tr>" % (
        _td('<a href="%s" style="color:#1A3D2B;font-weight:600">%s</a> <span style="color:#6B6B6B;font-size:.8rem">(%d lô)</span>' % (x["link"], x["ten"], x["n"])),
        _td("<strong>%s – %s</strong> · trung vị %s" % (so(x["lo"]), so(x["hi"]), so(x["tv"]))),
        _td("%d lô" % x["duoi1"]),
        _td('<a href="%s">từ %s</a>' % (x["re"]["url"], tien(x["re"]["ty"])))) for x in xa)
    hang = []
    for k in sorted(khu, key=lambda x: x["tv"]):
        key = [a[0] for a in KHU if a[2] == k["link"]][0]
        v = [x for x in lo if key in x["loc"]]
        r = min(v, key=lambda x: x["ty"])
        hang.append("            <tr>%s%s%s%s</tr>" % (
            _td('<a href="%s" style="color:#1A3D2B;font-weight:600">%s</a>' % (k["link"], k["ten"])),
            _td("%s triệu/m²" % so(k["tv"])),
            _td("%d lô" % sum(1 for x in v if x["ty"] < 1)),
            _td('<a href="%s" title="%s">từ %s</a>' % (r["url"], H.escape(r["ten"], quote=True), tien(r["ty"])))))

    faq = [
        ("Giá đất Nam Ban Lâm Hà bao nhiêu một m²?",
         "Tính tháng %d/%d từ %d lô đang rao ở xã Nam Ban và xã Nam Hà: đất nền có thổ cư %s–%s triệu/m², trung vị %s triệu/m²; đất vườn và lô lớn %s triệu/m². "
         "Đây là giá rao; giá chốt thường thấp hơn sau thương lượng." % (d.month, d.year, tong, so(t["lo"]), so(t["hi"]), so(t["tv"]), vuon)),
        ("Huyện Lâm Hà (Nam Ban) còn không sau sáp nhập?",
         "Từ 01/7/2025 cả nước bỏ cấp huyện. Theo Nghị quyết 202/2025/QH15, xã Nam Ban mới gồm thị trấn Nam Ban cũ, xã Đông Thanh, xã Mê Linh và xã Gia Lâm. "
         "Người mua vẫn quen gọi cả vùng là Nam Ban, Lâm Hà; trên giấy tờ mới ghi tên xã và tỉnh Lâm Đồng."),
        ("Mua đất Nam Ban, Lâm Hà dưới 1 tỷ ở khu nào?",
         "Tháng %d/%d có %d lô dưới 1 tỷ. Đơn giá trung vị mềm nhất ở %s (%s triệu/m²), cao nhất ở %s (%s triệu/m²). Lô rẻ nhất hiện từ %s."
         % (d.month, d.year, duoi1, khu_re["ten"], so(khu_re["tv"]), khu_dat["ten"], so(khu_dat["tv"]), tien(re_nhat["ty"]))),
    ]
    if len(xa) == 2:
        faq.append(("Giá đất Nam Hà so với Nam Ban thế nào?",
                    "Theo lô đang rao tháng %d/%d, trung vị xã Nam Ban %s triệu/m² (%d lô), xã Nam Hà %s triệu/m² (%d lô). Lô rẻ nhất xã Nam Ban từ %s, xã Nam Hà từ %s."
                    % (d.month, d.year, so(xa[0]["tv"]), xa[0]["n"], so(xa[1]["tv"]), xa[1]["n"], tien(xa[0]["re"]["ty"]), tien(xa[1]["re"]["ty"]))))
    faq.append(("Giá trên trang này có phải bảng giá nhà nước không?",
                "Không. Bảng giá đất tỉnh Lâm Đồng là giá nhà nước dùng tính thuế, phí sang tên và bồi thường, thường thấp hơn giá rao nhiều lần. "
                "Trang này là giá rao của lô thật đang bán, dùng để biết mua được với giá nào."))

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": URL_LH + "#webpage", "url": URL_LH, "name": tieu_de, "description": mo_ta, "inLanguage": "vi",
         "isPartOf": {"@id": "https://nambanvillas.vn/#website"}, "publisher": {"@id": "https://nambanvillas.vn/#organization"},
         "datePublished": "2026-09-24", "dateModified": ngay,
         "about": {"@type": "Place", "name": "Nam Ban, Lâm Hà, Lâm Đồng",
                   "containsPlace": [{"@type": "Place", "name": "Xã Nam Ban"}, {"@type": "Place", "name": "Xã Nam Hà"}]},
         "primaryImageOfPage": {"@type": "ImageObject", "url": "https://nambanvillas.vn/images/og-namban.jpg"},
         "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["#tra-loi-nhanh", ".article-title"]},
         "isBasedOn": {"@id": URL + "#dataset"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": "https://nambanvillas.vn/"},
            {"@type": "ListItem", "position": 2, "name": "Thị Trường", "item": "https://nambanvillas.vn/thi-truong/"},
            {"@type": "ListItem", "position": 3, "name": "Giá Đất Nam Ban Lâm Hà", "item": URL_LH}]},
        {"@type": "FAQPage", "@id": URL_LH + "#faq", "isPartOf": {"@id": URL_LH + "#webpage"},
         "mainEntity": [{"@type": "Question", "name": q_, "acceptedAnswer": {"@type": "Answer", "text": a_}} for q_, a_ in faq]}]}

    head = nguon[:nguon.index("<body")]
    head = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', "", head, flags=re.S)
    head = head.replace("../../css/", "/css/")
    head = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % H.escape(tieu_de, quote=False), head)
    for k, v in (('<meta name="description" content="', mo_ta), ('<meta property="og:description" content="', mo_ta),
                 ('<meta property="og:title" content="', tieu_de), ('<meta name="twitter:title" content="', tieu_de),
                 ('<meta name="keywords" content="', "giá đất nam ban lâm hà, giá đất nam ban lâm hà 2026, giá đất nam ban lâm hà lâm đồng, đất nam ban lâm hà dưới 1 tỷ, giá đất nam hà nam ban lâm hà")):
        if k in head:
            i = head.index(k) + len(k)
            head = head[:i] + H.escape(v, quote=True) + head[head.index('"', i):]
    head = head.replace(URL, URL_LH).replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
    head = head.replace("</head>", '  <script type="application/ld+json">%s</script>\n</head>' % json.dumps(ld, ensure_ascii=False, separators=(",", ":")))

    chrome_tren = nguon[nguon.index("<body"):nguon.index("<main")]
    chrome_duoi = nguon[nguon.index("</main>"):].replace("../../js/", "/js/")
    than = THAN_LAM_HA % dict(
        ngay=ngay_vn(ngay), thang="%d/%d" % (d.month, d.year), tong=tong, cau=cau, th=TH, hang_xa=hang_xa, hang_khu="\n".join(hang),
        tho="%s–%s" % (so(t["lo"]), so(t["hi"])), tho_tv=so(t["tv"]), vuon=vuon,
        ho="%s–%s" % (so(kq["ho"]["lo"]), so(kq["ho"]["hi"])) if "ho" in kq else "–",
        faq="\n".join("  <details open><summary>%s</summary><p>%s</p></details>" % (q_, a_) for q_, a_ in faq))
    os.makedirs("gia-dat-lam-ha", exist_ok=True)
    open(LAM_HA, "w", encoding="utf-8").write(head + chrome_tren + than + chrome_duoi)

    sm = open("sitemap.xml", encoding="utf-8").read()
    if URL_LH not in sm:
        sm = sm.replace("</urlset>", "  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.85</priority></url>\n</urlset>" % (URL_LH, ngay))
    sm = re.sub(r"(<loc>%s</loc><lastmod>)\d{4}-\d{2}-\d{2}" % re.escape(URL_LH), r"\g<1>" + ngay, sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("  Lâm Hà: %s" % ", ".join("%s %s" % (x["ten"], so(x["tv"])) for x in xa))



def cap_nhat_meta_hub(ngay):
    """ĐÃ TỪNG DÍNH: hub Đất Nền ghi '94 lô, từ 480 triệu' ở title + mô tả + og + schema suốt nhiều tuần
    trong khi thật là 116 lô, từ 368 triệu (bẫy cũ chỉ soi thân trang). Nay script tuần đặt lại."""
    d = datetime.date.fromisoformat(ngay)
    for f, loai in (("dat-nen-nam-ban/index.html", "dat"), ("nha-ban-nam-ban/index.html", "nha")):
        s = open(f, encoding="utf-8").read()
        g = s[s.index("prop-grid sp-sang"):]
        the = [x for x in re.findall(r'<article class="prop-card[^>]*>', g) if 'data-ban="1"' not in x]
        gia = [float(x) for t_ in the for x in re.findall(r'data-price="([\d.]+)"', t_) if float(x) > 0]
        n, re_ = len(the), tien(min(gia))
        if loai == "dat":
            td = "Mua Bán Đất Nền Nam Ban Tháng %d/%d – %d Lô Sổ Đỏ Chính Chủ, Từ %s" % (d.month, d.year, n, re_.title())
            mt = ("Mua bán đất Nam Ban Lâm Hà (thị trấn Nam Ban cũ), Lâm Đồng: %d lô thật chính chủ, từ %s, sẵn thổ cư, "
                  "đã kiểm pháp lý, quy hoạch trước khi đăng. Gọi 0978 758 788." % (n, re_))
        else:
            td = "Nhà Bán Nam Ban Tháng %d/%d – %d Căn Nhà Vườn, Biệt Thự, Từ %s" % (d.month, d.year, n, re_.title())
            mt = ("Mua nhà vườn, biệt thự nghỉ dưỡng Nam Ban Lâm Hà (thị trấn Nam Ban cũ): %d căn thật đang bán, từ %s, "
                  "sổ riêng hay sổ chung ghi rõ từng căn. Gọi 0978 758 788." % (n, re_))
        s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % H.escape(td, quote=False), s, count=1)
        for k, v in (('<meta name="description" content="', mt), ('<meta property="og:description" content="', mt),
                     ('<meta name="twitter:description" content="', mt), ('<meta property="og:title" content="', td),
                     ('<meta name="twitter:title" content="', td)):
            if k in s:
                i = s.index(k) + len(k)
                s = s[:i] + H.escape(v, quote=True) + s[s.index('"', i):]

        def fix(m):
            gj = json.loads(m.group(1))
            for nd in gj.get("@graph", [gj]):
                if nd.get("@type") in ("CollectionPage", "WebPage") and "description" in nd:
                    nd["description"] = mt
                    nd["name"] = td
            return '<script type="application/ld+json">' + json.dumps(gj, ensure_ascii=False, separators=(",", ":")) + "</script>"
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)
        open(f, "w", encoding="utf-8").write(s)
        print("  hub %s: %d, từ %s" % (loai, n, re_))


def cap_nhat_trang_chu(ngay):
    """Trang chủ đang TOP 1 "xem đất nam ban" (24/9/2026). LUẬT: KHÔNG đụng title/H1/URL.
    Chỉ đặt: meta/og description + câu "Xem đất Nam Ban" dưới Sản Phẩm Nổi Bật, số lấy từ 2 hub."""
    dem = {}
    for f, k in (("dat-nen-nam-ban/index.html", "dat"), ("nha-ban-nam-ban/index.html", "nha")):
        s = open(f, encoding="utf-8").read()
        g = s[s.index("prop-grid sp-sang"):]
        the = [x for x in re.findall(r'<article class="prop-card[^>]*>', g) if 'data-ban="1"' not in x]
        gia = [float(x) for t_ in the for x in re.findall(r'data-price="([\d.]+)"', t_) if float(x) > 0]
        dem[k] = (len(the), min(gia))
    re_ = tien(min(dem["dat"][1], dem["nha"][1]))
    mt = ("Mua bán đất Nam Ban, nhà đất Nam Ban Lâm Hà: %d lô đất và %d nhà thật đang bán, từ %s. "
          "Đưa đi xem đất tận nơi miễn phí. Gọi 0978 758 788." % (dem["dat"][0], dem["nha"][0], re_))
    cau = ('<!-- XEM-DAT:START -->\n    <p class="xem-dat"><strong>Xem đất Nam Ban tận nơi:</strong> %d lô đất và %d nhà đang bán, từ %s. '
           'Nam Ban Villas đưa đi xem miễn phí, đối chiếu sổ thật tại chỗ. Ở xa thì <a href="/nho-xem-dat-ho-nam-ban/">nhờ xem đất hộ</a>, '
           'nhận ảnh và video trong ngày.</p>\n    <!-- XEM-DAT:END -->' % (dem["dat"][0], dem["nha"][0], re_))
    f = "index.html"
    s = open(f, encoding="utf-8").read()
    s = thay_khoi(s, "<!-- XEM-DAT:START -->", "<!-- XEM-DAT:END -->", cau)
    for k in ('<meta name="description" content="', '<meta property="og:description" content="', '<meta name="twitter:description" content="'):
        if k in s:
            i = s.index(k) + len(k)
            s = s[:i] + H.escape(mt, quote=True) + s[s.index('"', i):]

    def fix(m):
        g = json.loads(m.group(1))
        for nd in g.get("@graph", []):
            if nd.get("@type") == "WebPage" and nd.get("@id", "").endswith("/#webpage"):
                nd["description"] = mt
        return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>"
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, count=1, flags=re.S)
    open(f, "w", encoding="utf-8").write(s)
    print("  trang chủ: %d lô, %d nhà, từ %s" % (dem["dat"][0], dem["nha"][0], re_))


# ── TRANG /dat-vuon-nam-ban/ — từ khoá "đất vườn nam ban giá rẻ" + "đất sào nam ban giá rẻ" ──
# 1 URL cho cả 2 ý định (cùng người mua: lô lớn, vườn cây, tính giá theo sào) — không mở trang mới
# để khỏi cắn trang /dat-nam-ban-gia-re/ đang top. Thẻ lô chép NGUYÊN từ hub (nguồn sự thật).
DAT_VUON = "dat-vuon-nam-ban/index.html"
URL_VUON = "https://nambanvillas.vn/dat-vuon-nam-ban/"


def _the_hub(f, chon):
    s = open(f, encoding="utf-8").read()
    ra = []
    for m in re.finditer(r'<article class="prop-card sp-row[^"]*"([^>]*)>([\s\S]*?)</article>', s):
        at, body = m.group(1), m.group(2)
        if 'data-ban="1"' in at:
            continue
        u = re.search(r'href="(/(?:dat-nen|nha-ban)/[^"]+/)"', body)
        t = re.search(r'<h3 class="sp-title"><a[^>]*>([^<]*)', body)
        a = float((re.search(r'data-area="([\d.]+)"', at) or [0, 0])[1])
        p = float((re.search(r'data-price="([\d.]+)"', at) or [0, 0])[1])
        nhan = (re.search(r'data-nhan="([^"]*)"', at) or [0, ""])[1]
        x = dict(html=m.group(0), url=u.group(1) if u else "", ten=H.unescape(t.group(1)) if t else "", area=a, ty=p, nhan=nhan)
        if x["url"] and chon(x):
            ra.append(x)
    return ra


def cap_nhat_dat_vuon(ngay):
    d = datetime.date.fromisoformat(ngay)
    lo = _the_hub(HUB, lambda x: "vuon" in x["nhan"] or x["area"] >= 1000) + \
        _the_hub("nha-ban-nam-ban/index.html", lambda x: re.search(r"[Nn]hà [Vv]ườn", x["ten"]))
    seen, uniq = set(), []
    for x in lo:
        if x["url"] not in seen:
            seen.add(x["url"]); uniq.append(x)
    lo = sorted(uniq, key=lambda x: (x["ty"] <= 0, x["ty"]))
    co_gia = [x for x in lo if x["ty"] > 0]
    # giá/sào chỉ tính trên thẻ MỘT lô (thẻ cụm/"2 lô": giá lô rẻ nhất + diện tích lô lớn nhất -> méo)
    nhieu_lo = lambda t: bool(re.match(r"\s*(Cụm|\d+\s*(lô|nền))", t, re.I) or re.search(r"\b\d+\s*(lô|nền)\b", t, re.I))
    sao = [x for x in co_gia if x["area"] >= 1000 and not nhieu_lo(x["ten"])]
    re_nhat = co_gia[0]
    duoi1 = [x for x in co_gia if x["ty"] < 1]
    tu1den2 = [x for x in co_gia if 1 <= x["ty"] < 2]
    tren2 = [x for x in co_gia if x["ty"] >= 2]
    tr_sao = [x["ty"] * 1e6 / x["area"] for x in sao]          # triệu đồng / 1.000m² (1 sào)
    sao_lo, sao_tv, sao_hi = (q(tr_sao, .1), statistics.median(tr_sao), q(tr_sao, .9)) if len(tr_sao) >= 3 else (0, 0, 0)
    ts = lambda tr: tien(tr / 1000)          # triệu/sào -> "553 triệu" / "1,53 tỷ"
    sao_re = min(sao, key=lambda x: x["ty"] * 1e6 / x["area"]) if sao else None

    def lk(x):
        return '<a href="%s">%s</a>' % (x["url"], H.escape(x["ten"], quote=False))

    cau = ("Đất vườn, đất sào Nam Ban giá rẻ tháng %d/%d: rẻ nhất từ <strong>%s</strong>, có %d lô dưới 1 tỷ trong %d lô vườn và lô từ 1.000m² đang bán"
           % (d.month, d.year, tien(re_nhat["ty"]), len(duoi1), len(lo)))
    if sao_tv:
        cau += "; lô từ 1.000m² trở lên giá phổ biến <strong>%s–%s/sào</strong> (1 sào = 1.000m²), trung vị %s/sào." % (ts(sao_lo), ts(sao_hi), ts(sao_tv))
    else:
        cau += "."
    bang = ""
    for ten, v in (("Dưới 1 tỷ", duoi1), ("1–2 tỷ", tu1den2), ("Trên 2 tỷ", tren2)):
        if v:
            bang += '<tr><td style="%s"><strong>%s</strong></td><td style="%s">%d lô</td><td style="%s">%s — %s</td></tr>' % (
                TD, ten, TD, len(v), TD, tien(v[0]["ty"]), lk(v[0]))
    khoi = '''<!-- VUON-SO:START -->
    <div id="tra-loi-nhanh" class="tra-loi-nhanh">
      <p class="tra-loi-nhanh-nhan">Trả lời nhanh</p>
      <p class="tra-loi-nhanh-cau">%s</p>
      <div class="goi-nhanh-nut"><a href="tel:0978758788" class="goi-nhanh-goi">Gọi 0978 758 788 hỏi lô vườn</a><a href="https://zalo.me/0978758788" target="_blank" rel="noopener" class="goi-nhanh-zalo">Nhắn Zalo</a></div>
    </div>
    <h2 style="font-size:clamp(1.15rem,2.6vw,1.5rem);color:#1A3D2B;letter-spacing:-.015em;margin:0 0 12px">Đất vườn Nam Ban giá rẻ theo tầm tiền</h2>
    <div style="overflow-x:auto">
    <table style="width:100%%;border-collapse:collapse;font-size:.92rem;margin:0 0 26px">
      <caption style="text-align:left;font-size:.82rem;color:#5F6E66;padding:0 0 8px">Lô vườn, lô sào đang bán ngày %s — lô rẻ nhất từng tầm</caption>
      <thead><tr style="background:#F2F6F3;text-align:left"><th scope="col" style="%s">Tầm tiền</th><th scope="col" style="%s">Số lô</th><th scope="col" style="%s">Rẻ nhất</th></tr></thead>
      <tbody>%s</tbody>
    </table>
    </div>
    <!-- VUON-SO:END -->''' % (cau, ngay_vn(ngay), TH, TH, TH, bang)

    s = open(DAT_VUON, encoding="utf-8").read()
    s = thay_khoi(s, "<!-- VUON-SO:START -->", "<!-- VUON-SO:END -->", khoi)
    # thẻ: chép nguyên từ hub, ảnh đầu = LCP
    the = []
    for k, x in enumerate(lo):
        h = x["html"].replace('<article class="prop-card sp-row sp-feat"', '<article class="prop-card sp-row"')
        if k == 0:
            h = h.replace(' loading="lazy"', ' fetchpriority="high"', 1)
        else:
            h = h.replace(' fetchpriority="high"', ' loading="lazy"')
        the.append("      " + h)
    s = thay_khoi(s, "<!-- VUON-THE:START -->", "<!-- VUON-THE:END -->",
                  "<!-- VUON-THE:START -->\n" + "\n\n".join(the) + "\n<!-- VUON-THE:END -->")
    # preload = ảnh thẻ đầu
    img = re.search(r'<img [^>]*>', the[0]).group(0)
    src = re.search(r'src="([^"]+)"', img).group(1)
    ss = re.search(r'srcset="([^"]+)"', img)
    sz = re.search(r'sizes="([^"]+)"', img)
    pl = '<link rel="preload" as="image" href="%s" fetchpriority="high"%s%s>' % (
        src, (' imagesrcset="%s"' % ss.group(1)) if ss else "", (' imagesizes="%s"' % sz.group(1)) if sz and ss else "")
    s = re.sub(r'<link rel="preload" as="image"[^>]*>', lambda m: pl, s, count=1)

    # FAQ số sống
    s = faq_html(s, "vuon-gia", "Tháng %d/%d có %d lô vườn và lô từ 1.000m² đang bán: %d lô dưới 1 tỷ, %d lô 1–2 tỷ, %d lô trên 2 tỷ. Rẻ nhất từ %s; "
                 "lô từ 1.000m² trở lên phổ biến %s–%s/sào. Giá từng lô còn tuỳ phần thổ cư, đường vào và tuổi vườn."
                 % (d.month, d.year, len(lo), len(duoi1), len(tu1den2), len(tren2), tien(re_nhat["ty"]), ts(sao_lo), ts(sao_hi)))
    s = faq_html(s, "vuon-re", "Tính tháng %d/%d, lô vườn rẻ nhất Nam Ban Villas đang có là %s (%s). Có %d lô vườn dưới 1 tỷ; "
                 "danh sách xếp từ rẻ nhất ở trên trang." % (d.month, d.year, tien(re_nhat["ty"]), H.escape(re_nhat["ten"], quote=False), len(duoi1)))
    if sao_tv and sao_re:
        s = faq_html(s, "sao", "Ở Lâm Đồng, 1 sào tính 1.000m². Theo %d lô từ 1.000m² trở lên đang bán tháng %d/%d, giá phổ biến %s–%s/sào, "
                     "trung vị %s/sào. Lô rẻ nhất theo sào hiện khoảng %s/sào (%s). Lô có sẵn thổ cư, mặt đường nhựa thì cao hơn."
                     % (len(sao), d.month, d.year, ts(sao_lo), ts(sao_hi), ts(sao_tv), ts(sao_re["ty"] * 1e6 / sao_re["area"]), H.escape(sao_re["ten"], quote=False)))

    td = "Đất Vườn, Đất Sào Nam Ban Giá Rẻ T%d/%d — Lô Vườn Cây, Lô Lớn Từ 1.000m²" % (d.month, d.year)
    mt = ("Đất vườn, đất sào Nam Ban giá rẻ T%d/%d: %d lô vườn và lô lớn đang bán, từ %s%s. Gọi 0978 758 788."
          % (d.month, d.year, len(lo), tien(re_nhat["ty"]), (", phổ biến %s–%s/sào" % (ts(sao_lo), ts(sao_hi))) if sao_tv else ""))
    s = re.sub(r"<title>[^<]*</title>", "<title>%s</title>" % H.escape(td, quote=False), s, count=1)
    for k, v in (('<meta name="description" content="', mt), ('<meta property="og:description" content="', mt),
                 ('<meta name="twitter:description" content="', mt), ('<meta property="og:title" content="', td),
                 ('<meta name="twitter:title" content="', td)):
        if k in s:
            i = s.index(k) + len(k)
            s = s[:i] + H.escape(v, quote=True) + s[s.index('"', i):]

    def fix(m):
        g = json.loads(m.group(1))
        for nd in g.get("@graph", []):
            t_ = nd.get("@type")
            if t_ == "CollectionPage":
                nd.update(name=td, description=mt, dateModified=ngay)
            elif t_ == "ItemList":
                nd["numberOfItems"] = len(lo)
                nd["itemListOrder"] = "https://schema.org/ItemListOrderAscending"
                nd["itemListElement"] = [{"@type": "ListItem", "position": i + 1, "url": "https://nambanvillas.vn" + x["url"], "name": x["ten"]}
                                         for i, x in enumerate(lo)]
            elif t_ == "FAQPage":
                sec = s[s.index('<section class="faq-hien"'):]
                sec = sec[:sec.index("</section>")]
                nd["mainEntity"] = [{"@type": "Question", "name": H.unescape(re.sub(r"<[^>]+>", "", a_)).strip(),
                                     "acceptedAnswer": {"@type": "Answer", "text": H.unescape(re.sub(r"<[^>]+>", "", b_)).strip()}}
                                    for a_, b_ in re.findall(r"<summary>(.*?)</summary>\s*<p>(.*?)</p>", sec, re.S)]
            if "dateModified" in nd:
                nd["dateModified"] = ngay
        return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>"
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, flags=re.S)
    open(DAT_VUON, "w", encoding="utf-8").write(s)
    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"(<loc>%s</loc><lastmod>)\d{4}-\d{2}-\d{2}" % re.escape(URL_VUON), r"\g<1>" + ngay, sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print("  đất vườn: %d lô, từ %s, %d dưới 1 tỷ, sào %s–%s (tv %s)" % (len(lo), tien(re_nhat["ty"]), len(duoi1), ts(sao_lo), ts(sao_hi), ts(sao_tv)))


def cap_nhat_300tr(ngay):
    """Từ khoá "đất nam ban 300tr" (24/9/2026). Nói THẬT: Nam Ban Villas có lô 300 triệu hay không,
    lô gần nhất bao nhiêu, và tin rao 300 triệu thường thiếu gì. Không dựng trang riêng — mục nằm
    trong /dat-nam-ban-gia-re/ (đang top 4, title KHÔNG đổi)."""
    lo = sorted([x for x in doc_lo() if x["ty"] > 0], key=lambda x: x["ty"])
    d = datetime.date.fromisoformat(ngay)
    duoi300 = [x for x in lo if x["ty"] <= 0.3]
    duoi400 = [x for x in lo if x["ty"] < 0.4]
    duoi500 = [x for x in lo if x["ty"] < 0.5]
    gan = lo[:3]
    # CHỈ ghi giá: thẻ nhiều lô (cụm, "2 lô") có data-price = lô rẻ nhất nhưng data-area = lô lớn nhất -> ghép 2 số là sai
    ds = "; ".join('<a href="%s">%s</a> (từ %s)' % (x["url"], H.escape(x["ten"], quote=False), tien(x["ty"])) for x in gan)
    if duoi300:
        mo = "Có. Tháng %d/%d Nam Ban Villas có %d lô từ 300 triệu trở xuống." % (d.month, d.year, len(duoi300))
    else:
        mo = ("Tháng %d/%d, Nam Ban Villas chưa có lô nào 300 triệu. Lô rẻ nhất đang bán là %s; có %d lô dưới 400 triệu và %d lô dưới 500 triệu."
              % (d.month, d.year, tien(lo[0]["ty"]), len(duoi400), len(duoi500)))
    khoi = ('<!-- GIA-300:START -->\n'
            '  <h2>Có 300 triệu mua được đất Nam Ban không?</h2>\n'
            '  <p>%s Ba lô gần mức 300 triệu nhất: %s.</p>\n'
            '  <p>Tin rao "đất Nam Ban 300 triệu" trên mạng thường rơi vào một trong mấy trường hợp: lô nhỏ trong hẻm sâu, đường đất; '
            'lô chưa có thổ cư nên không xây được nhà; sổ chung hoặc chưa tách thửa; hoặc giá 300 triệu là giá một mét ngang, không phải cả lô. '
            'Trước khi cọc lô 300 triệu, hỏi đủ bốn thứ: sổ riêng hay chung, bao nhiêu m² thổ cư, đường vào rộng bao nhiêu, và thửa có dính quy hoạch không.</p>\n'
            '  <p>Có sẵn 300–400 triệu thì gọi <a href="tel:0978758788">0978 758 788</a> báo ngân sách: Nam Ban Villas báo ngay khi có lô đúng tầm, '
            'và nói thẳng nếu tầm tiền đó chưa có lô sổ riêng, có thổ cư.</p>\n'
            '  <!-- GIA-300:END -->' % (mo, ds))
    f = GIA_RE
    s = open(f, encoding="utf-8").read()
    s = thay_khoi(s, "<!-- GIA-300:START -->", "<!-- GIA-300:END -->", khoi)
    s = faq_html(s, "300tr", "%s Tin rao 300 triệu thường là lô hẻm sâu, chưa có thổ cư, sổ chung, hoặc giá tính theo mét ngang; "
                 "hỏi rõ sổ, thổ cư, đường vào và quy hoạch trước khi cọc." % mo)
    open(f, "w", encoding="utf-8").write(s)
    print("  300tr: %d lô ≤300tr, %d lô <400tr, rẻ nhất %s" % (len(duoi300), len(duoi400), tien(lo[0]["ty"])))

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
    # TIÊU ĐỀ + H1 ỔN ĐỊNH (chỉ đổi theo THÁNG): trang đang có thứ hạng mà title đổi mỗi tuần thì
    # Google phải đánh giá lại liên tục. Số tuần nằm ở mô tả + khối Trả lời nhanh + bảng.
    tieu_de = "Giá Đất Nam Ban Hôm Nay T%d/%d — Tính Từ Lô Thật, Cập Nhật Mỗi Thứ Hai" % (datetime.date.fromisoformat(ngay).month, datetime.date.fromisoformat(ngay).year)
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
               '<h1 class="article-title">Giá Đất Nam Ban Hôm Nay — Tính Từ Lô Thật Đang Rao, Cập Nhật Mỗi Thứ Hai</h1>', s, count=1)
    s = re.sub(r"Cập nhật tuần: \d+/\d+/\d+", "Cập nhật tuần: %s" % ngay_vn(ngay), s)
    s = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', '"dateModified":"%s"' % ngay, s)
    s = sua_schema(s, ngay, tieu_de, mo_ta, cau, kq, tong)
    open(TRANG, "w", encoding="utf-8").write(s)

    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"(<loc>%s</loc><lastmod>)\d{4}-\d{2}-\d{2}" % re.escape(URL), r"\g<1>" + ngay, sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    cap_nhat_300tr(ngay)
    cap_nhat_gia_re(ngay, [x for x in lo if x["ty"] > 0], kq, khu)
    lam_trang_lam_ha(ngay, [x for x in lo if x["ty"] > 0], kq, khu)
    cap_nhat_meta_hub(ngay)
    cap_nhat_trang_chu(ngay)
    cap_nhat_dat_vuon(ngay)
    # mô tả trang thị trấn: "từ X triệu" = lô rẻ nhất khu trung tâm (đã từng ghi 480 khi thật là 397)
    tt = [x for x in lo if x["ty"] > 0 and "nam-ban" in x["loc"]]
    if tt:
        f = "dat-trung-tam-thi-tran-nam-ban/index.html"
        s2 = open(f, encoding="utf-8").read()
        s2 = re.sub(r'(<meta (?:name="description"|property="og:description") content="[^"]*?)từ [\d.,]+ (?:triệu|tỷ)', lambda m: m.group(1) + "từ " + tien(min(x["ty"] for x in tt)), s2)
        open(f, "w", encoding="utf-8").write(s2)
    for k, v in kq.items():
        print("  %-5s %3d lô  %s – %s  trung vị %s" % (k, v["n"], so(v["lo"]), so(v["hi"]), so(v["tv"])))
    print("  khu:", ", ".join("%s %s" % (t["ten"], so(t["tv"])) for t in khu))
    print("Đã cập nhật %s (%s)" % (TRANG, ngay))
    return 0


if __name__ == "__main__":
    sys.exit(main())
