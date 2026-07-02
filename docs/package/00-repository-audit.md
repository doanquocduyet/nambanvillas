# 00 · REPOSITORY AUDIT — NAM BAN VILLAS
*Prompt 0: kiểm kê + trùng/khác. Chỉ mô tả, không phân tích. Cập nhật 2/7/2026.*

## 1. INVENTORY (loại .git/.claude)
- **51 trang HTML** (index.html) — trang chủ + section: dat-nen-nam-ban, nha-ban-nam-ban, dich-vu, lien-he, hoi-dap, thi-truong/*, ve-nam-ban/*, namban-notes/*, dat-nen/<lô>, nha-ban/<căn>.
- **76 ảnh jpg** (22 ảnh bài `images/articles/` + hero + listing `images/listings/`), 28 svg (icon + infographic `images/news/`, bản đồ quy hoạch), 2 png (logo, favicon).
- **docs/**: 4 md — HIEN-PHAP-3-WEB, FORM-DANG-TIN, HO-SO-TONG-NAMBAN-MAX, TU-DUY-TINH-TUE. (+ bộ package này.)
- **scripts/**: build-feed.mjs, daily-listings.mjs.
- **.github/workflows/**: weekly-update (feed), indexnow, daily-listings.
- **Gốc**: index.html, CLAUDE.md, sitemap.xml, feed.xml, llms.txt, robots.txt, vercel.json, IndexNow key txt.

## 2. DUPLICATE GROUPS (đã dọn trong quá trình xây)
- `/tin-tuc/*` từng trùng `/thi-truong/*` (4 bài) → **đã xóa + 301**.
- `/dat-nen/` và `/nha-ban/` (hub cũ) trùng `-nam-ban` → **đã xóa + 301**.
- 4 bài quy hoạch từng có 2 bản → đã gộp về `/thi-truong/`.
→ Hiện **không còn slug trùng**.

## 3. DIFFERENCE / TRẠNG THÁI
- **22 trang** canonical sang Panorama (đã nhường theo Hiến pháp — nhóm editorial/quy hoạch/đời sống).
- **1 trang noindex**: `thi-truong/song-o-nam-ban` (nhường Panorama).
- Cụm giao dịch Villas (mua-dat-bao-nhieu, nam-ban-so-voi-noi-khac, dau-tu-dat-nam-ban) — self-canonical, đã viết nội dung thật, index.
- Cụm thị trường sống: tin-rao (ngày), gia-dat-hom-nay (tuần), mua-dat (nền tảng).
