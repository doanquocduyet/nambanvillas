#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐƯA NÚT GỌI/ZALO TỚI ĐÚNG CHỖ KHÁCH ĐANG NÓNG NHẤT — chạy lại được nhiều lần.

Mục tiêu tối thượng của web là khách bấm Gọi/Zalo. Đợt rà 23–24/9/2026 đo được
5 chỗ khách đang ở đúng lúc muốn hỏi mà không có nút:
  cta-3  hub Đất Nền: cuộn qua 122 thẻ lô = 90% trang, không một nút Gọi;
         thẻ lô chỉ có nút "So sánh".
  cta-4  27/35 bài viết: đọc gần hết bài mới gặp nút; 11 bài có khối CTA cuối
         nhưng nút lại trỏ /lien-he/ (thêm 1 lần tải trang) chứ không gọi.
  cta-5  8 trang dịch vụ/chuyển đổi: nút đầu tiên nằm ở 62–99% chiều dài trang.
  cta-6  trang lô trên điện thoại: đọc xong mô tả + khối rủi ro (2.600 chữ) thì
         không còn nút nào tới footer — đúng lúc khách tin nhất.
  cta-8  nút to nhất trong menu điện thoại là "Liên Hệ" -> /lien-he/, không gọi.
  cta-9/10  dòng tin cậy dưới nút thiếu lời hứa trả lời/không ràng buộc; 5 trang
         dùng chữ nút yếu "Gọi tư vấn" và không có dòng tin cậy.

Cách làm: mỗi việc là 1 hàm, nhận HTML trả HTML, KHÔNG dùng regex nuốt khối
([\s\S]*?) — chèn theo chỉ số, đếm độ sâu thẻ khi cần. Chạy xong nhớ:
    python3 scripts/do-lo-vao-trang-khu.py   (thẻ trên trang khu chép từ hub)
    python3 scripts/dat-phien-ban-css.py      (CSS đổi -> đóng lại ?v=)
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TEL = 'tel:0978758788'
ZALO = 'https://zalo.me/0978758788'
SVG_GOI = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
           '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z" '
           'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def khoi_goi(cau, lop=""):
    """Khối liên hệ dùng chung: 1 câu + 2 nút Gọi/Zalo. Chữ nút nói rõ bấm xong được gì."""
    return ('<div class="goi-nhanh%s">' % ((" " + lop) if lop else "")
            + '<p>%s</p>' % cau
            + '<div class="goi-nhanh-nut">'
            + '<a href="%s" class="goi-nhanh-goi">%s Gọi 0978 758 788</a>' % (TEL, SVG_GOI)
            + '<a href="%s" target="_blank" rel="noopener" class="goi-nhanh-zalo">Nhắn Zalo</a>' % ZALO
            + '</div></div>')


def cuoi_the(s, i, mo="div"):
    """Trả chỉ số ngay SAU thẻ đóng khớp với thẻ mở tại i (đếm độ sâu)."""
    pat = re.compile(r'<%s\b|</%s>' % (mo, mo))
    depth = 0
    for m in pat.finditer(s, i):
        depth += 1 if not m.group(0).startswith("</") else -1
        if depth == 0:
            return m.end()
    raise ValueError("không thấy thẻ đóng")


def sau_khoang_trang(s, j):
    while j < len(s) and s[j] in " \n\t":
        j += 1
    return j


# ── cta-3: nút Gọi trên TỪNG thẻ lô (.sp-right) ─────────────────────────────
def nut_goi_the_lo(s):
    n = 0
    pos = 0
    while True:
        i = s.find('<div class="sp-right">', pos)
        if i < 0:
            break
        j = cuoi_the(s, i)
        the = s[i:j]
        # thẻ đã có cặp Gọi/Zalo riêng (.sp-cta2, trang chủ) thì không gắn thêm
        _a = s.rfind("<article", 0, i); _b = s.find("</article>", i)
        da_co_cta2 = _a >= 0 and _b > 0 and "sp-cta2" in s[_a:_b]
        if 'class="sp-goi"' not in the and not da_co_cta2:
            # tên lô lấy từ tiêu đề thẻ để aria-label nói rõ gọi hỏi lô nào
            k = s.rfind('<h3 class="sp-title">', 0, i)
            ten = ""
            if k > 0:
                m = re.search(r'<h3 class="sp-title"><a[^>]*>([\s\S]*?)</a>', s[k:i])
                if m:
                    ten = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
            nut = ('<a href="%s" class="sp-goi" aria-label="Gọi hỏi lô %s">%s Gọi hỏi lô này</a>'
                   % (TEL, ten.replace('"', "&quot;")[:80] if ten else "này", SVG_GOI))
            # chèn ngay trước </div> đóng .sp-right
            dong = the.rfind("</div>")
            the2 = the[:dong].rstrip() + "\n          " + nut + "\n        " + the[dong:]
            s = s[:i] + the2 + s[j:]
            j = i + len(the2)
            n += 1
        pos = j
    return s, n


# ── cta-3b: dải liên hệ xen giữa danh sách dài (sau mỗi 12 thẻ) ─────────────
DAI = khoi_goi('Chưa thấy lô hợp? <strong>Gọi 0978 758 788</strong> nói ngân sách và mục đích, '
               'Nam Ban Villas lọc giúp 2–3 lô đúng ý rồi đưa đi xem.', "sp-goi-dai")


def dai_giua_danh_sach(s):
    """Chỉ chèn vào lưới .prop-grid.sp-sang có >= 20 thẻ. Chạy lại: gỡ dải cũ rồi chèn lại."""
    s = s.replace("\n      " + DAI, "").replace(DAI, "")
    i = s.find('<div class="prop-grid sp-sang')     # hub: sp-sang sp-datnen / sp-nhaban
    if i < 0:
        return s, 0
    j = cuoi_the(s, i)
    luoi = s[i:j]
    if luoi.count("</article>") < 20:
        return s, 0
    ra, dem, n = [], 0, 0
    pos = 0
    for m in re.finditer(r"</article>", luoi):
        dem += 1
        ra.append(luoi[pos:m.end()])
        pos = m.end()
        if dem % 12 == 0 and dem < luoi.count("</article>"):
            ra.append("\n      " + DAI)
            n += 1
    ra.append(luoi[pos:])
    return s[:i] + "".join(ra) + s[j:], n


# ── cta-8: mục cuối menu điện thoại = GỌI ───────────────────────────────────
def menu_cuoi_la_goi(s):
    if 'class="mobile-sheet"' not in s:
        return s, 0
    # chỉ nhìn TRONG sheet (thanh trên cũng có "Liên Hệ" + "Gọi…" nên không dò toàn trang)
    m = re.search(r'class="mobile-sheet"[\s\S]*?\n\s*</div>', s)
    if not m:
        return s, 0
    sheet = m.group(0)
    links = re.findall(r'<a href="([^"]+)"', sheet)
    if links and links[-1].startswith("tel:"):
        return s, 0
    m2 = re.search(r'(<a href="/lien-he/">Liên Hệ</a>)(\s*)(</div>)$', sheet)
    if not m2:
        return s, 0
    # "Liên Hệ" giữ làm mục thường; mục CUỐI (được CSS tô thành nút to nhất) = gọi thẳng
    sheet2 = sheet[:m2.start()] + m2.group(1) + "\n  " + '<a href="%s">Gọi 0978 758 788</a>' % TEL + m2.group(2) + m2.group(3)
    return s[:m.start()] + sheet2 + s[m.end():], 1


# ── cta-9/10: trang lô — chữ nút rõ phần thưởng + dòng tin cậy đủ 3 ý ──────
TIN_CAY_CU = '<p style="text-align:center;font-size:.76rem;color:#7a8a7e;margin-top:10px">Đưa đi xem tận nơi miễn phí · Đối chiếu sổ thật</p>'
TIN_CAY = '<p style="text-align:center;font-size:.76rem;color:#7a8a7e;margin-top:10px">Đưa đi xem tận nơi miễn phí · Đối chiếu sổ thật · Trả lời trong ngày, không ràng buộc</p>'


def trang_lo_nut_va_tin_cay(s):
    n = 0
    if 'class="btn-listing-cta">Gọi tư vấn</a>' in s:
        s = s.replace('class="btn-listing-cta">Gọi tư vấn</a>', 'class="btn-listing-cta">Gọi xem sổ + giá</a>')
        n += 1
    if TIN_CAY_CU in s:
        s = s.replace(TIN_CAY_CU, TIN_CAY)
        n += 1
    i = s.find('<div class="listing-cta-row">')
    if i > 0:
        j = cuoi_the(s, i)
        k = sau_khoang_trang(s, j)
        if not s.startswith('<p style="text-align:center;font-size:.76rem', k):
            s = s[:j] + "\n          " + TIN_CAY + s[j:]
            n += 1
    return s, n


# ── cta-6: trang lô — khối liên hệ ngay SAU khối rủi ro ─────────────────────
SAU_RUI_RO = khoi_goi('Đọc hết rủi ro rồi vẫn thấy hợp? Gọi để Nam Ban Villas đưa đi xem tận nơi, '
                      'đối chiếu sổ thật và nói thẳng nên hay không nên.', "goi-sau-rui-ro")


def sau_khoi_rui_ro(s):
    if 'class="goi-nhanh goi-sau-rui-ro"' in s:
        return s, 0
    i = s.find('<div class="risk-block">')
    if i < 0 or 'class="listing-cta-row"' not in s:
        return s, 0
    j = cuoi_the(s, i)
    return s[:j] + "\n\n        " + SAU_RUI_RO + s[j:], 1


# ── cta-4: bài viết — khối CTA cuối phải GỌI được + 1 khối giữa bài ─────────
NUT_LIEN_HE_CU = '<a href="/lien-he/" class="btn-cta">Liên hệ tư vấn miễn phí →</a>'
NUT_GOI_MOI = ('<a href="%s" class="btn-cta">Gọi 0978 758 788</a> '
               '<a href="%s" target="_blank" rel="noopener" class="btn-cta btn-cta-zalo">Nhắn Zalo</a>' % (TEL, ZALO))
GIUA_BAI = khoi_goi('Đang nhắm một lô cụ thể ở Nam Ban? Gọi hỏi thẳng giá thật, sổ và quy hoạch của lô đó '
                    '— trả lời trong ngày, không ràng buộc.', "goi-giua-bai")


def bai_viet(s):
    n = 0
    # khối CTA cuối bài: mọi kiểu nút trỏ /lien-he/ (thêm 1 lần tải trang) -> Gọi + Zalo
    pos = 0
    while True:
        i = s.find('class="article-cta-box"', pos)
        if i < 0:
            break
        i = s.rfind("<div", 0, i)
        j = cuoi_the(s, i)
        khoi = s[i:j]
        khoi2 = re.sub(r'<a href="/lien-he/"(?: class="btn-cta")?>[^<]*</a>', NUT_GOI_MOI, khoi)
        if khoi2 != khoi:
            s = s[:i] + khoi2 + s[j:]
            n += 1
        pos = i + len(khoi2)
    a = s.find("<main")
    b = s.find("<footer", a)
    if a < 0 or b < 0:
        return s, n
    if TEL not in s[a:b] and 'class="goi-nhanh goi-cuoi-bai"' not in s:
        # khối cuối bài đặt SAU .article-cta-box (nếu có), không thì trước FAQ/cụm/</article>
        k = s.find('class="article-cta-box"', a, b)
        if k > 0:
            j = cuoi_the(s, s.rfind("<div", 0, k))
        else:
            moc = [s.find(x, a, b) for x in ('<section class="faq-hien"', '<nav class="cum-chu-de"', '</article>')]
            moc = [x for x in moc if x > 0]
            j = min(moc) if moc else b
        s = s[:j] + "\n\n    " + khoi_goi('Đọc xong còn muốn hỏi gì về Nam Ban? Gọi hỏi thẳng — '
                                          '<strong>trả lời trong ngày, không ràng buộc</strong>.', "goi-cuoi-bai") + s[j:]
        n += 1
        b = s.find("<footer", a)
    if 'class="goi-nhanh goi-giua-bai"' in s:
        return s, n
    # điểm kết thúc thân bài: mốc sớm nhất trong các khối đuôi
    duoi = [s.find(x, a, b) for x in ('<nav class="cum-chu-de"', 'class="article-cta-box"',
                                       'class="faq-hien"', '<h2>Câu hỏi thường gặp', '</article>')]
    duoi = [x for x in duoi if x > 0]
    end = min(duoi) if duoi else b
    than = s[a:end]
    chu = re.sub(r"<[^>]+>", "", re.sub(r"<(script|style)[\s\S]*?</\1>", "", than))
    if len(chu) < 1800:               # bài rất ngắn: 1 khối cuối là đủ
        return s, n
    # đã có nút trong nửa đầu thân bài thì thôi
    nua = than[: len(than) // 2]
    if TEL in nua or "zalo.me" in nua:
        return s, n
    h2 = [m.start() for m in re.finditer(r"<h2\b", than)]
    if len(h2) < 2:
        return s, n
    muc = len(than) * 0.45
    tot = min(h2[1:], key=lambda x: abs(x - muc))
    s = s[: a + tot] + GIUA_BAI + "\n\n" + s[a + tot:]
    return s, n + 1


# ── cta-5: 8 trang dịch vụ/chuyển đổi — nút ngay sau đoạn mở ────────────────
DAU_TRANG = {
    "dich-vu/index.html": ('<div class="dv-filter">', "truoc", '<div class="container">%s</div>\n'),
    "hoi-dap/index.html": ('<div class="faq-section">', "truoc", '<div class="container">%s</div>\n  '),
    "phap-ly-mua-dat-nam-ban/index.html": ('<div class="pl-toc">', "sau-khoi", "\n  %s"),
    "dat-nam-ban-gia-re/index.html": ('<div class="gr-nhanh">', "sau-khoi", "\n  %s"),
    "ky-gui-ban-dat-nam-ban/index.html": ('<div class="ct-nhanh">', "sau-khoi", "\n  %s"),
    "nho-xem-dat-ho-nam-ban/index.html": ('<div class="ct-nhanh">', "sau-khoi", "\n  %s"),
    "hop-tac/index.html": ('<div class="ct-nhanh">', "sau-khoi", "\n  %s"),
    "cho-thue/index.html": ('<div class="ct-nhanh">', "sau-khoi", "\n  %s"),
}
CAU_DAU = {
    "dich-vu/index.html": 'Cần kiểm một lô ngay? <strong>Gọi trước khi đặt cọc</strong> — kiểm sổ, quy hoạch miễn phí, trả lời trong ngày.',
    "hoi-dap/index.html": 'Không thấy câu hỏi của bạn? Gọi hỏi thẳng — <strong>trả lời trong ngày, không ràng buộc</strong>.',
    "phap-ly-mua-dat-nam-ban/index.html": 'Đang nhắm một lô? Gửi sổ, Nam Ban Villas <strong>kiểm pháp lý miễn phí</strong> trước khi bạn xuống tiền.',
    "dat-nam-ban-gia-re/index.html": 'Nói ngân sách và mục đích, Nam Ban Villas <strong>lọc giúp 2–3 lô trong tầm tiền</strong> rồi đưa đi xem.',
    "ky-gui-ban-dat-nam-ban/index.html": 'Có đất muốn bán? Gọi gửi thông tin lô — <strong>chưa bán được thì không mất gì</strong>.',
    "nho-xem-dat-ho-nam-ban/index.html": 'Ở xa, cần người xem đất hộ? Gọi nói lô cần xem — <strong>gửi ảnh, video thực tế trong ngày</strong>.',
    "hop-tac/index.html": 'Muốn trao đổi hợp tác? Gọi thẳng — <strong>trả lời trong ngày, không ràng buộc</strong>.',
    "cho-thue/index.html": 'Cần thuê hoặc có nhà cho thuê ở Nam Ban? Gọi nói nhu cầu — <strong>trả lời trong ngày</strong>.',
}
DAU_HOI_DAP_MOI_2_MUC = khoi_goi('Còn băn khoăn? Gọi hỏi thẳng — <strong>trả lời trong ngày, không ràng buộc</strong>.', "goi-giua-bai")


def dau_trang_dich_vu(f, s):
    if f not in DAU_TRANG:
        return s, 0
    if 'class="goi-nhanh goi-dau-trang"' in s:
        return s, 0
    moc, kieu, khuon = DAU_TRANG[f]
    khoi = khoi_goi(CAU_DAU[f], "goi-dau-trang")
    i = s.find(moc)
    if i < 0:
        return s, 0
    if kieu == "truoc":
        s = s[:i] + (khuon % khoi) + s[i:]
    else:
        j = cuoi_the(s, i)
        s = s[:j] + (khuon % khoi) + s[j:]
    n = 1
    if f == "hoi-dap/index.html" and DAU_HOI_DAP_MOI_2_MUC not in s:
        # thêm 1 khối sau mỗi 2 nhóm câu hỏi (khách chỉ đọc đúng nhóm mình quan tâm)
        pos, dem = 0, 0
        while True:
            k = s.find('<div class="faq-category">', pos)
            if k < 0:
                break
            j = cuoi_the(s, k)
            dem += 1
            if dem % 2 == 0 and s.find('<div class="faq-category">', j) > 0:
                s = s[:j] + "\n\n    " + DAU_HOI_DAP_MOI_2_MUC + s[j:]
                j += len(DAU_HOI_DAP_MOI_2_MUC) + 6
                n += 1
            pos = j
    return s, n


# ── hub bài viết (thi-truong/, ve-nam-ban/, namban-notes/): 1 dải giữa trang ─
HUB_BAI = {
    "thi-truong/index.html": '<section class="section">',
    "ve-nam-ban/index.html": '<section class="section">',
    "namban-notes/index.html": '<section class="section">',
}
CAU_HUB = 'Đọc phân tích rồi muốn hỏi về một lô cụ thể? Gọi hỏi thẳng giá thật, sổ và quy hoạch — <strong>trả lời trong ngày</strong>.'


def hub_bai_viet(f, s):
    if f not in HUB_BAI or 'class="goi-nhanh goi-hub-bai"' in s:
        return s, 0
    i = s.find(HUB_BAI[f])
    if i < 0:
        return s, 0
    khoi = '<div class="container">' + khoi_goi(CAU_HUB, "goi-hub-bai") + '</div>\n'
    return s[:i] + khoi + s[i:], 1


def main():
    tong = {}
    for f in sorted(glob.glob("**/index.html", recursive=True)):
        if f.startswith(("node_modules", "docs")):
            continue
        s0 = open(f, encoding="utf-8").read()
        s = s0
        dem = {}
        s, dem["the-lo"] = nut_goi_the_lo(s)
        s, dem["dai"] = dai_giua_danh_sach(s)
        s, dem["menu"] = menu_cuoi_la_goi(s)
        la_lo = f.startswith(("dat-nen/", "nha-ban/", "cho-thue/")) and 'class="listing-cta-row"' in s
        if la_lo:
            s, dem["lo"] = trang_lo_nut_va_tin_cay(s)
            s, dem["rui-ro"] = sau_khoi_rui_ro(s)
        if f.startswith(("thi-truong/", "ve-nam-ban/", "namban-notes/")) and f.count("/") == 2:
            s, dem["bai"] = bai_viet(s)
        s, dem["dau"] = dau_trang_dich_vu(f, s)
        s, dem["hub"] = hub_bai_viet(f, s)
        if s != s0:
            open(f, "w", encoding="utf-8").write(s)
            for k, v in dem.items():
                if v:
                    tong[k] = tong.get(k, 0) + v
    for k, v in sorted(tong.items()):
        print("  %-8s %d" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
