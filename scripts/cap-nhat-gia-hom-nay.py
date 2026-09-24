#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CẬP NHẬT TRANG "GIÁ ĐẤT NAM BAN HÔM NAY" TỪ LÔ THẬT ĐANG RAO — chạy mỗi thứ Hai.

ĐÃ TỪNG DÍNH (tin-4): tiêu đề hứa "cập nhật hàng tuần" nhưng bảng đứng im 83 ngày,
cột "So tuần trước" mãi ghi "(tuần đầu)". Khách gõ "giá đất Nam Ban hôm nay" — truy
vấn thương mại nóng nhất — vào thấy số cũ 3 tháng là mất tin ngay.

Số ở đây KHÔNG bịa: lấy data-area / data-price của các thẻ lô CÒN BÁN trên hub
dat-nen-nam-ban/ (cùng nguồn với bộ lọc), quy ra triệu/m², lấy P10–P90 (bỏ 10% hai
đầu để lô ngoại lệ không kéo lệch) + trung vị. Lịch sử tuần lưu data/gia-tuan.json
để điền cột "So tuần trước". Giữ tối đa 8 tuần trên trang.

    python3 scripts/cap-nhat-gia-hom-nay.py            # cập nhật theo hôm nay
"""
import datetime
import json
import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
TRANG = "thi-truong/gia-dat-nam-ban-hom-nay/index.html"
LICH_SU = "data/gia-tuan.json"
HUB = "dat-nen-nam-ban/index.html"
TD = "padding:10px 12px;border-bottom:1px solid #ECEAE4"


def q(v, p):
    v = sorted(v)
    k = (len(v) - 1) * p
    f = int(k)
    c = min(f + 1, len(v) - 1)
    return v[f] + (v[c] - v[f]) * (k - f)


def so(x):
    """1.42 -> '1,4' · 4.56 -> '4,6' · 0.52 -> '0,5'"""
    return ("%.1f" % x).replace(".", ",")


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
        ra.append(dict(area=area, m2=price * 1000 / area, nhan=nhan, loc=loc))
    return ra


def tinh(lo):
    nhom = {
        "tho": [x["m2"] for x in lo if "vuon" not in x["nhan"] and x["area"] < 3000],
        "vuon": [x["m2"] for x in lo if "vuon" in x["nhan"] or x["area"] >= 3000],
        "ho": [x["m2"] for x in lo if "ho-bai-cong" in x["loc"] or "view-dep" in x["nhan"]],
    }
    kq = {}
    for k, v in nhom.items():
        if len(v) < 3:
            continue
        kq[k] = dict(n=len(v), lo=round(q(v, .1), 2), tv=round(statistics.median(v), 2), hi=round(q(v, .9), 2))
    return kq


def so_sanh(moi, cu):
    if not cu:
        return "— (tuần đầu tính từ lô thật)"
    d = moi["tv"] - cu["tv"]
    if abs(d) < 0.05:
        return "Đi ngang (trung vị %s)" % so(cu["tv"])
    return "%s %s triệu/m² so với trung vị tuần trước (%s)" % ("Tăng" if d > 0 else "Giảm", so(abs(d)), so(cu["tv"]))


TEN = {"tho": "Đất nền có thổ cư (dưới 3.000m²)", "vuon": "Đất vườn / lô lớn từ 3.000m²", "ho": "Đất view hồ / view đẹp"}


def bang(ngay, kq, cu, tong):
    d = datetime.date.fromisoformat(ngay)
    tr = []
    for k in ("tho", "vuon", "ho"):
        if k not in kq:
            continue
        v = kq[k]
        tr.append('            <tr><td style="%s">%s <span style="color:#6B6B6B;font-size:.8rem">(%d lô)</span></td>'
                  '<td style="%s"><strong>%s – %s</strong> · trung vị %s</td><td style="%s">%s</td></tr>'
                  % (TD, TEN[k], v["n"], TD, so(v["lo"]), so(v["hi"]), so(v["tv"]), TD, so_sanh(v, (cu or {}).get(k))))
    return '''        <!-- WEEK:%s -->
        <h2>Tuần %d/%d/%d</h2>
        <div style="overflow-x:auto">
        <table style="width:100%%;border-collapse:collapse;font-size:.92rem;margin-bottom:8px">
          <thead>
            <tr style="background:#F2F6F3;text-align:left">
              <th style="padding:10px 12px;border-bottom:2px solid #1A3D2B">Loại đất</th>
              <th style="padding:10px 12px;border-bottom:2px solid #1A3D2B">Giá rao (triệu/m², khoảng 10%%–90%%)</th>
              <th style="padding:10px 12px;border-bottom:2px solid #1A3D2B">So tuần trước</th>
            </tr>
          </thead>
          <tbody>
%s
          </tbody>
        </table>
        </div>
        <p style="font-size:.9rem;color:#3D3D3D"><strong>Cách tính:</strong> từ %d lô đang rao trên Nam Ban Villas ngày %d/%d/%d (cùng dữ liệu với bộ lọc trang Đất Nền), quy ra triệu/m² theo giá rao cả lô; bỏ 10%% lô rẻ nhất và 10%% lô đắt nhất để lô ngoại lệ không kéo lệch. Giá chốt thật thường thấp hơn giá rao.</p>

''' % (ngay, d.day, d.month, d.year, "\n".join(tr), tong, d.day, d.month, d.year)


def main():
    ngay = datetime.date.today().isoformat()
    lo = doc_lo()
    kq = tinh(lo)
    ls = json.load(open(LICH_SU, encoding="utf-8")) if os.path.exists(LICH_SU) else {}
    truoc = [k for k in sorted(ls) if k < ngay]
    cu = ls[truoc[-1]] if truoc else None
    ls[ngay] = kq
    os.makedirs("data", exist_ok=True)
    json.dump(ls, open(LICH_SU, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    s = open(TRANG, encoding="utf-8").read()
    i = s.index("<!-- WEEKLY-PRICE:START")
    i = s.index("\n", i) + 1
    j = s.index("        <!-- WEEKLY-PRICE:END -->")
    # bỏ tuần cùng ngày (chạy lại trong ngày), rồi giữ tối đa 7 tuần cũ
    khoi = s[i:j]
    tuan = re.split(r"(?=        <!-- WEEK:)", khoi)
    tuan = [t for t in tuan if t.strip() and ("<!-- WEEK:%s -->" % ngay) not in t]
    tuan = tuan[:7]
    s = s[:i] + "\n" + bang(ngay, kq, cu, len(lo)) + "".join(tuan) + s[j:]

    d = datetime.date.fromisoformat(ngay)
    s = re.sub(r"Cập nhật tuần: \d+/\d+/\d+", "Cập nhật tuần: %d/%d/%d" % (d.day, d.month, d.year), s)
    s = re.sub(r'"dateModified":"\d{4}-\d{2}-\d{2}"', '"dateModified":"%s"' % ngay, s)
    open(TRANG, "w", encoding="utf-8").write(s)

    sm = open("sitemap.xml", encoding="utf-8").read()
    sm2 = re.sub(r"(<loc>https://nambanvillas.vn/thi-truong/gia-dat-nam-ban-hom-nay/</loc><lastmod>)\d{4}-\d{2}-\d{2}", r"\g<1>" + ngay, sm)
    open("sitemap.xml", "w", encoding="utf-8").write(sm2)
    for k, v in kq.items():
        print("  %-5s %3d lô  %s – %s  trung vị %s" % (k, v["n"], so(v["lo"]), so(v["hi"]), so(v["tv"])))
    print("Đã cập nhật %s (%s)" % (TRANG, ngay))
    return 0


if __name__ == "__main__":
    sys.exit(main())
