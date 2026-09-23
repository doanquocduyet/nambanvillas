#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DỰNG TRANG KHU NAM HÀ — /dat-nam-ha-nam-ban/

Nam Hà đã có 4 lô đất + 1 nhà nhưng chưa có trang khu riêng, trong khi Đông
Thanh / Mê Linh / Gia Lâm / Từ Liêm / Hồ Bãi Công đều có. Chip "Nam Hà" trên hub
vì thế không có data-trang để bấm sang.

Dựng từ khuôn trang Từ Liêm (cùng loại, cùng bố cục), thay toàn bộ phần chữ.
Mọi số trong bài lấy từ CHÍNH các trang lô Nam Hà, không bịa:
  - 2 lô 498m² (80m² thổ) 699tr · 577m² (90m² thổ) 769tr
  - 2 lô gần chùa Linh Ẩn: 321m² và lô góc 770m², 420–770tr
  - lô 240m²/lô, 100m² thổ cư, 550tr/lô
  - nhà 3PN 2WC view đồi núi, 3,5 tỷ
  - Thiên Vân Village: xã Đinh Văn, giáp xã Nam Hà — 72 nền, từ 2,1 tỷ
Thẻ lô do scripts/do-lo-vao-trang-khu.py đổ vào sau.
"""
import json
import os
import re

os.chdir("/home/user/nambanvillas")

SRC = "dat-tu-liem-nam-ban/index.html"
DST = "dat-nam-ha-nam-ban"
ANH = "/images/listings/dat-nam-ha-240m2-550tr/1.jpg"

TIEU_DE = "Đất Nam Hà Nam Ban — Lô Thật Có Sổ, Sẵn Thổ Cư Ven Đà Lạt"
MO_TA = ("Đất Nam Hà (Lâm Hà, ven Đà Lạt): lô 240m² sẵn 100m² thổ cư từ 550 triệu, "
         "lô 498–577m² từ 699 triệu, nhà 3PN view đồi núi. Sổ riêng, công chứng ngay. "
         "Gọi 0978 758 788.")

FAQ = [
    ("Đất Nam Hà giá bao nhiêu?",
     "Lô 240m² sẵn 100m² thổ cư khoảng 550 triệu/lô; lô 498m² (80m² thổ cư) 699 triệu và "
     "lô 577m² (90m² thổ cư) 769 triệu; lô gần chùa Linh Ẩn 420–770 triệu tùy diện tích. "
     "Nhà xây sẵn 3PN view đồi núi khoảng 3,5 tỷ. Gọi 0978 758 788 để lấy giá từng lô."),
    ("Nam Hà ở đâu, cách Đà Lạt bao xa?",
     "Nam Hà thuộc Lâm Hà, Lâm Đồng — vùng ven Đà Lạt, cách trung tâm Đà Lạt khoảng 30km. "
     "Khu vực đã có dân cư, homestay và nhà nghỉ dưỡng hiện hữu, xung quanh có chợ, "
     "trường học và các khu du lịch; một số lô nằm gần chùa Linh Ẩn."),
    ("Đất Nam Hà có sổ riêng và thổ cư sẵn không?",
     "Các lô Nam Ban Villas đăng tại Nam Hà đều có sổ riêng và sẵn phần thổ cư — phổ biến "
     "80–100m² đất ở mỗi lô, công chứng sang tên ngay. Vẫn nên kiểm sổ đúng thửa và số m² "
     "thổ cư thực tế trước khi đặt cọc."),
    ("Mua đất Nam Hà hợp làm gì?",
     "Phần lớn lô có chiều sâu tốt (có lô dài tới ~63m) nên làm nhà trước – vườn sau thoải "
     "mái. Khu vực đã có homestay và nhà nghỉ dưỡng hoạt động, hợp nhà vườn, second home "
     "hoặc homestay cuối tuần."),
]


def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    s = open(SRC, encoding="utf-8").read()

    # ── HEAD ──────────────────────────────────────────────────────────────
    s = re.sub(r"<title>.*?</title>",
               "<title>%s | Nam Ban Villas</title>" % esc(TIEU_DE), s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*"',
               '<meta name="description" content="%s"' % esc(MO_TA), s, count=1)
    s = re.sub(r'<meta name="keywords" content="[^"]*"',
               '<meta name="keywords" content="đất Nam Hà, đất Nam Hà Lâm Hà, '
               'đất Nam Hà ven Đà Lạt, nhà đất Nam Hà, đất thổ cư Nam Hà"', s, count=1)
    s = s.replace('content="Từ Liêm, Nam Ban, Lâm Hà, Lâm Đồng"',
                  'content="Nam Hà, Lâm Hà, Lâm Đồng"')
    s = s.replace("https://nambanvillas.vn/dat-tu-liem-nam-ban/",
                  "https://nambanvillas.vn/dat-nam-ha-nam-ban/")
    s = re.sub(r'<meta property="og:title" content="[^"]*"',
               '<meta property="og:title" content="%s"' % esc(TIEU_DE), s, count=1)
    s = re.sub(r'<meta name="twitter:title" content="[^"]*"',
               '<meta name="twitter:title" content="%s"' % esc(TIEU_DE), s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*"',
               '<meta property="og:description" content="%s"' % esc(MO_TA), s, count=1)
    # ảnh đại diện + preload LCP
    s = s.replace("/images/listings/cum-tu-liem-13-nen/1-480.jpg",
                  ANH.replace("1.jpg", "1-480.jpg"))
    s = s.replace("/images/listings/cum-tu-liem-13-nen/1-800.jpg",
                  ANH.replace("1.jpg", "1-800.jpg"))
    s = s.replace("/images/listings/cum-tu-liem-13-nen/1.jpg", ANH)

    # ── SCHEMA: parse ra object rồi sửa, không đụng regex vào JSON ─────────
    def sua(m):
        g = json.loads(m.group(2))

        def di(n):
            if isinstance(n, dict):
                t = n.get("@type")
                if t == "CollectionPage":
                    n["name"] = TIEU_DE
                    n["description"] = MO_TA
                    n["@id"] = "https://nambanvillas.vn/dat-nam-ha-nam-ban/#webpage"
                if t == "ItemList":
                    n["name"] = "Đất & nhà Nam Hà, Lâm Hà"
                    n["numberOfItems"] = 0
                    n["itemListElement"] = []
                if t == "BreadcrumbList":
                    for it in n.get("itemListElement", []):
                        if it.get("name") == "Từ Liêm":
                            it["name"] = "Nam Hà"
                if t == "FAQPage":
                    n["mainEntity"] = [
                        {"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in FAQ]
                if t == "Place":
                    n["name"] = "Nam Hà, Lâm Hà, Lâm Đồng"
                for v in n.values():
                    di(v)
            elif isinstance(n, list):
                for v in n:
                    di(v)
        di(g)
        return m.group(1) + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + m.group(3)

    s = re.sub(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', sua, s)

    # ── THÂN TRANG ────────────────────────────────────────────────────────
    s = s.replace("<span>Từ Liêm</span>", "<span>Nam Hà</span>")
    s = re.sub(r"<h1>.*?</h1>", "<h1>%s</h1>" % esc(TIEU_DE), s, count=1)
    s = s.replace(
        "Từ Liêm là khu dân cư hiện hữu của Nam Ban (Lâm Hà, Lâm Đồng), có hồ Từ Liêm "
        "và nhiều nền ngang 5m sẵn thổ cư. Dưới đây là các lô thật đang bán tại Từ Liêm, "
        "đã kiểm pháp lý trước khi đăng.",
        "Nam Hà là vùng ven Đà Lạt thuộc Lâm Hà, cách trung tâm Đà Lạt khoảng 30km — khí "
        "hậu mát, yên tĩnh, đã có dân cư, homestay và nhà nghỉ dưỡng hiện hữu. Lô ở đây "
        "phổ biến sẵn 80–100m² thổ cư và sổ riêng, tầm tiền vừa phải. Dưới đây là các lô "
        "và nhà thật đang bán tại Nam Hà, đã kiểm pháp lý trước khi đăng.")
    s = s.replace(">Nhắn Zalo nhận bảng giá<", ">Nhắn Zalo hỏi lô Nam Hà<")
    s = re.sub(r"(<h2[^>]*>)Đất Từ Liêm Nam Ban — [^<]*(</h2>)",
               lambda m: m.group(1) + "Đất Nam Hà — lô đang bán" + m.group(2), s, count=1)
    s = re.sub(r'<div class="lt-note">[\s\S]*?</div>',
               '<div class="lt-note"><strong>Vì sao nhiều người chọn Nam Hà:</strong> giá '
               'còn mềm so với trung tâm Nam Ban, lô thường sẵn 80–100m² thổ cư và có '
               'chiều sâu tốt nên làm nhà trước – vườn sau thoải mái. Đổi lại, Nam Hà xa '
               'trung tâm Nam Ban hơn các khu khác — nếu cần chợ, trường, bệnh viện trong '
               'vài phút thì cân nhắc kỹ. Gửi lô bạn nhắm, Nam Ban Villas '
               '<a href="/phap-ly-mua-dat-nam-ban/" style="color:#1A3D2B;font-weight:700">'
               'kiểm sổ, thổ cư, ranh mốc giúp miễn phí</a> trước khi bạn đặt cọc.</div>',
               s, count=1)

    # chip khu: trang nào thì bỏ chính nó, thêm khu còn thiếu
    chip = ('<a href="/dat-tu-liem-nam-ban/" style="background:#EBF4EE;color:#1A3D2B;'
            'font-weight:700;font-size:.88rem;padding:8px 16px;border-radius:20px;'
            'text-decoration:none;border:1px solid #DCE6D8">Khu Từ Liêm</a>\n        ')
    s = s.replace('<a href="/dat-dong-thanh-nam-ban/"', chip + '<a href="/dat-dong-thanh-nam-ban/"', 1)

    # FAQ hiện trên trang
    kh = ['<section class="faq-hien" aria-label="Câu hỏi thường gặp">',
          "  <h2>Câu hỏi thường gặp</h2>"]
    for q, a in FAQ:
        kh.append("  <details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)))
    kh.append("</section>")
    s = re.sub(r'<section class="faq-hien"[\s\S]*?</section>', "\n".join(kh), s, count=1)

    # Lưới thẻ phải XOÁ SẠCH thẻ của khu cũ rồi mới để script đổ lô điền.
    # ĐÃ DÍNH: dùng regex [\s\S]*? để xoá lưới -> dừng ở </div> ĐẦU TIÊN nằm
    # TRONG một thẻ, nên 3 lô Từ Liêm lọt sang trang Nam Hà. Cắt bằng chỉ số:
    # mở lưới -> </div> ngay sau </article> CUỐI CÙNG.
    i = s.index('<div class="prop-grid sp-sang">')
    i = s.index(">", i) + 1
    j = s.index("</div>", s.rindex("</article>"))
    s = s[:i] + "\n    " + s[j:]
    assert "tu-liem" not in s.split('<div class="prop-grid sp-sang">')[1].split("</div>")[0]

    os.makedirs(DST, exist_ok=True)
    open(DST + "/index.html", "w", encoding="utf-8").write(s)
    print("đã dựng /%s/" % DST)
    con = [x for x in ("Từ Liêm", "tu-liem") if x in s.replace("Khu Từ Liêm", "").replace("/dat-tu-liem-nam-ban/", "")]
    print("còn sót chữ Từ Liêm ngoài chip liên kết:", con or "không")


if __name__ == "__main__":
    main()
