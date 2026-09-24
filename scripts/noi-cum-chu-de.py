#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NỐI CÁC BÀI CÙNG CHỦ ĐỀ THÀNH MỘT CỤM.

LUẬT CHỦ ĐÃ CHỐT (23/9/2026): các bài cùng chủ đề GIỮ RIÊNG, không gộp, không
301 — mỗi bài nhắm một câu người ta search khác nhau, gộp là mất cửa vào.

Nhưng giữ riêng chỉ THẮNG khi các bài NỐI VỚI NHAU. Đo được: 6 bài cùng cụm mà
0 bài nào trỏ sang bài nào; bài quy hoạch chỉ có 1 link vào cả site. Google gặp
6 trang yếu lẻ loi thay vì 1 cụm mạnh — đó đúng là lý do người ta khuyên gộp.
Nối lại thì giữ riêng vừa đủ cửa vào, vừa đủ sức.

Cách nối: cuối mỗi bài thêm khối "Cùng chủ đề", trỏ sang các bài anh em bằng
CHỮ NEO LÀ CÂU HỎI mà bài đích trả lời (không dùng "xem thêm", "tại đây").
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Mỗi bài: đường dẫn -> (chữ neo khi bài KHÁC trỏ tới nó, mô tả ngắn)
CUM = {
    "thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh": (
        "Tuyến tránh Nam Ban khi nào hoàn thành?",
        "Hiện trạng tháng 9/2026: chưa duyệt, chưa khởi công"),
    "thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban": (
        "Sân bay Liên Khương mở rộng ảnh hưởng gì tới Nam Ban?",
        "Nâng lên 5 triệu khách/năm — được gì, chưa nên kỳ vọng gì"),
    "thi-truong/khi-hau-cuoc-song-nam-ban": (
        "Sống ở Nam Ban thì có gì và chưa có gì?",
        "Khí hậu 18–23°C, tiện ích tại chỗ và thứ phải đi xa"),
    "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025": (
        "Quy hoạch Lâm Đồng 2025 đổi những gì?",
        "5 thay đổi lớn và phần nào thật sự chạm tới Nam Ban"),
    "thi-truong/dat-nam-ban-tang-gia-2025": (
        "Giá đất Nam Ban bao nhiêu một mét?",
        "Các mốc giá có văn bản: bảng giá 2026, giá đấu giá, giá đang giao dịch"),
    "ve-nam-ban/xa-nam-ban-sap-nhap": (
        "Xã Nam Ban sau sáp nhập gồm những xã nào?",
        "Từ 01/7/2025 theo Nghị quyết 202/2025/QH15"),
    "thi-truong/gia-dat-nam-ban-hom-nay": (
        "Giá đất Nam Ban hôm nay bao nhiêu một m²?",
        "Tính từ lô thật đang rao, theo loại và theo 7 khu, cập nhật mỗi thứ Hai"),
    "thi-truong/bang-gia-dat-2026-nam-ban": (
        "Bảng giá đất 2026 ảnh hưởng gì tới người mua đất Nam Ban?",
        "Giá nhà nước khác giá thị trường ra sao, phải tính thêm khoản gì"),
    "thi-truong/lam-dong-quy-hoach-dieu-chinh-2026": (
        "Quy hoạch Lâm Đồng điều chỉnh 2026 đổi những gì?",
        "7 thay đổi lớn, Nam Ban lên đô thị loại III"),
    "thi-truong/quy-hoach-tinh-lam-dong-dieu-chinh-2025": (
        "Điều chỉnh quy hoạch tỉnh Lâm Đồng 2025 có gì đáng chú ý?",
        "Mục tiêu 2030, mô hình 1–6–7–18–5, ý nghĩa với Lâm Hà"),
    "ve-nam-ban/nhung-thay-doi-quan-trong-nam-ban-2026": (
        "Nam Ban 2026–2030 sẽ thay đổi ra sao?",
        "5 thay đổi định hình lại giá trị bất động sản"),
    "thi-truong/dau-tu-dat-nam-ban": (
        "Đầu tư đất Nam Ban có dòng tiền không?",
        "Homestay, second home — con số thật, không hứa hẹn"),
    "ve-nam-ban/tiem-nang-dau-tu-nam-ban": (
        "Vì sao Nam Ban được gọi là viên ngọc ẩn?",
        "So với Đà Lạt, Bảo Lộc: giá, quỹ đất, ai đang mua"),
    "thi-truong/nghi-duong-retreat-cao-nguyen-lam-dong": (
        "Retreat cao nguyên có phải xu hướng thật?",
        "3 phân khúc hưởng lợi, giá thuê 3–8 triệu/đêm"),
    "thi-truong/nam-ban-so-voi-noi-khac": (
        "Nam Ban, Bảo Lộc, Di Linh hay Đà Lạt — mua ở đâu?",
        "Cùng 1–2 tỷ mua được gì ở mỗi nơi, nói cả mặt yếu"),
    "thi-truong/song-o-nam-ban": (
        "Sống ở Nam Ban thực tế tốn bao nhiêu?",
        "Chi phí, trường học, internet, điện nước 2026"),
    "thi-truong/nam-ban-lam-ha-50-nam-vung-kinh-te-moi": (
        "Nam Ban có gốc gác gì với người Hà Nội?",
        "50 năm vùng kinh tế mới — vì sao nhiều người Hà Nội tìm về"),
}

# Bài nào nên trỏ sang bài nào — chọn theo LIÊN QUAN THẬT, không nối bừa cả 6.
NOI = {
    "thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh": [
        "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025",
        "thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban",
        "thi-truong/dat-nam-ban-tang-gia-2025"],
    "thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban": [
        "thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh",
        "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025",
        "thi-truong/khi-hau-cuoc-song-nam-ban"],
    "thi-truong/khi-hau-cuoc-song-nam-ban": [
        "ve-nam-ban/xa-nam-ban-sap-nhap",
        "thi-truong/dat-nam-ban-tang-gia-2025",
        "thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban"],
    "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025": [
        "thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh",
        "ve-nam-ban/xa-nam-ban-sap-nhap",
        "thi-truong/dat-nam-ban-tang-gia-2025"],
    "thi-truong/dat-nam-ban-tang-gia-2025": [
        "thi-truong/gia-dat-nam-ban-hom-nay",
        "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025",
        "thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh"],
    "thi-truong/gia-dat-nam-ban-hom-nay": [
        "thi-truong/dat-nam-ban-tang-gia-2025",
        "thi-truong/bang-gia-dat-2026-nam-ban",
        "thi-truong/nam-ban-so-voi-noi-khac"],
    "ve-nam-ban/xa-nam-ban-sap-nhap": [
        "thi-truong/dat-nam-ban-tang-gia-2025",
        "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025",
        "thi-truong/khi-hau-cuoc-song-nam-ban"],
    # cụm QUY HOẠCH & GIÁ
    "thi-truong/bang-gia-dat-2026-nam-ban": [
        "thi-truong/gia-dat-nam-ban-hom-nay",
        "thi-truong/dat-nam-ban-tang-gia-2025",
        "thi-truong/lam-dong-quy-hoach-dieu-chinh-2026"],
    "thi-truong/lam-dong-quy-hoach-dieu-chinh-2026": [
        "ve-nam-ban/nhung-thay-doi-quan-trong-nam-ban-2026",
        "thi-truong/quy-hoach-tinh-lam-dong-dieu-chinh-2025",
        "thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh"],
    "thi-truong/quy-hoach-tinh-lam-dong-dieu-chinh-2025": [
        "thi-truong/lam-dong-quy-hoach-dieu-chinh-2026",
        "thi-truong/nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025",
        "ve-nam-ban/xa-nam-ban-sap-nhap"],
    "ve-nam-ban/nhung-thay-doi-quan-trong-nam-ban-2026": [
        "thi-truong/lam-dong-quy-hoach-dieu-chinh-2026",
        "thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban",
        "thi-truong/bang-gia-dat-2026-nam-ban"],
    # cụm ĐẦU TƯ & SỐNG
    "thi-truong/dau-tu-dat-nam-ban": [
        "ve-nam-ban/tiem-nang-dau-tu-nam-ban",
        "thi-truong/nghi-duong-retreat-cao-nguyen-lam-dong",
        "thi-truong/dat-nam-ban-tang-gia-2025"],
    "ve-nam-ban/tiem-nang-dau-tu-nam-ban": [
        "thi-truong/nam-ban-so-voi-noi-khac",
        "thi-truong/dau-tu-dat-nam-ban",
        "ve-nam-ban/nhung-thay-doi-quan-trong-nam-ban-2026"],
    "thi-truong/nghi-duong-retreat-cao-nguyen-lam-dong": [
        "thi-truong/dau-tu-dat-nam-ban",
        "thi-truong/khi-hau-cuoc-song-nam-ban",
        "thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban"],
    "thi-truong/nam-ban-so-voi-noi-khac": [
        "thi-truong/gia-dat-nam-ban-hom-nay",
        "ve-nam-ban/tiem-nang-dau-tu-nam-ban",
        "thi-truong/song-o-nam-ban"],
    "thi-truong/song-o-nam-ban": [
        "thi-truong/khi-hau-cuoc-song-nam-ban",
        "thi-truong/nam-ban-lam-ha-50-nam-vung-kinh-te-moi",
        "thi-truong/nam-ban-so-voi-noi-khac"],
    "thi-truong/nam-ban-lam-ha-50-nam-vung-kinh-te-moi": [
        "thi-truong/song-o-nam-ban",
        "ve-nam-ban/xa-nam-ban-sap-nhap",
        "thi-truong/khi-hau-cuoc-song-nam-ban"],
}


def khoi(nguon):
    muc = []
    for d in NOI[nguon]:
        neo, mo = CUM[d]
        muc.append(
            '    <li><a href="/%s/">%s</a><span>%s</span></li>' % (d, neo, mo))
    return ('<nav class="cum-chu-de" aria-label="Bài cùng chủ đề">\n'
            "  <h2>Cùng chủ đề</h2>\n  <ul>\n" + "\n".join(muc) + "\n  </ul>\n</nav>\n")


CSS = """
/* Khối "Cùng chủ đề" — nối các bài cùng cụm lại với nhau. Chữ neo là CÂU HỎI
   bài đích trả lời, để Google và bộ máy trả lời AI hiểu bài kia nói về gì. */
.cum-chu-de{max-width:780px;margin:32px auto 0;padding:20px 22px;background:#F7F3EE;border-radius:14px}
.cum-chu-de h2{font-size:.78rem;font-weight:800;letter-spacing:.11em;text-transform:uppercase;color:#8a978f;margin:0 0 12px}
.cum-chu-de ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.cum-chu-de li{display:flex;flex-direction:column;gap:2px}
.cum-chu-de a{color:var(--green,#1A3D2B);font-weight:700;font-size:.97rem;text-decoration:none;line-height:1.4}
.cum-chu-de a:hover{text-decoration:underline;text-underline-offset:3px}
.cum-chu-de span{color:#6B6B6B;font-size:.85rem;line-height:1.5}
@media(max-width:560px){.cum-chu-de{margin-inline:0;padding:16px 18px}}
"""


def main():
    css = open("css/style.css", encoding="utf-8").read()
    if ".cum-chu-de{" not in css:
        open("css/style.css", "w", encoding="utf-8").write(css.rstrip() + "\n" + CSS)
        print("style.css: thêm CSS khối Cùng chủ đề")

    for nguon in NOI:
        f = nguon + "/index.html"
        s = open(f, encoding="utf-8").read()
        if 'class="cum-chu-de"' in s:
            print("  đã có, bỏ qua:", nguon)
            continue
        # đặt ngay TRƯỚC khối kêu gọi liên hệ, sau phần thân bài
        m = re.search(r'\s*<div class="article-cta-box"', s)
        if not m:
            m = re.search(r'\s*<section class="faq-hien"', s)
        if not m:   # bài không có khối CTA/FAQ chuẩn -> đặt cuối <main>
            m = re.search(r'\s*</main>', s)
        if not m:
            m = re.search(r'\s*<footer', s)
        if not m:
            print("  KHÔNG tìm được chỗ chèn:", nguon)
            continue
        s = s[:m.start()] + "\n  " + khoi(nguon) + s[m.start():]
        open(f, "w", encoding="utf-8").write(s)
        print("  + Cùng chủ đề (%d link): %s" % (len(NOI[nguon]), nguon))


if __name__ == "__main__":
    main()
