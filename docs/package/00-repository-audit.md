# 00 · REPOSITORY AUDIT — NAM BAN VILLAS
*Prompt 0: kiểm kê + trùng/khác. Chỉ mô tả. Cập nhật 2/7/2026.*

## INVENTORY
- **51 index.html.** Gốc: `index.html`(trang chủ 606 dòng). Section hub: `dat-nen-nam-ban/`, `nha-ban-nam-ban/`, `thi-truong/`, `ve-nam-ban/`, `namban-notes/`, `dich-vu/`, `lien-he/`, `hoi-dap/`.
- **Lô đất** `dat-nen/`: dong-thanh-320m2, dong-thanh-845m2, thung-lung-530m2, sieu-pham-3700m2, giap-suoi-2700m2, ho-tu-liem-700m2, ho-bai-cong-lot1, ho-bai-cong-lot2, pho-thong-villas-130m2, me-linh-suoi-thong-650m2, hai-mat-tien-345m2 (11 lô).
- **Nhà** `nha-ban/`: hill-house-village, villa-mini-me-linh, nha-vuon-1018m2 (3 căn).
- **thi-truong/**: 3 trang giao dịch (mua-dat-nam-ban-bao-nhieu, nam-ban-so-voi-noi-khac, dau-tu-dat-nam-ban) + song-o-nam-ban(noindex) + tin-rao-dat-nam-ban-moi + gia-dat-nam-ban-hom-nay + hub + ~10 bài quy hoạch/thị trường (nhường Panorama).
- **Assets**: 76 jpg (22 `images/articles/` + hero `nam-ban-aerial.jpg` + `images/listings/`), 28 svg (icon + `images/news/*.svg` infographic + bản đồ QH), logo.png, favicon.png.
- **Config gốc**: CLAUDE.md, sitemap.xml, feed.xml, llms.txt, robots.txt, vercel.json, `abdd063f81d049182d79e17f4239ad8f.txt`(IndexNow key).
- **docs/**: HIEN-PHAP-3-WEB, FORM-DANG-TIN, HO-SO-TONG-NAMBAN-MAX, TU-DUY-TINH-TUE + `package/` (bộ này).
- **scripts/**: build-feed.mjs, daily-listings.mjs. **workflows/**: weekly-update.yml, indexnow.yml, daily-listings.yml.

## ĐÃ DỌN TRÙNG (không còn slug trùng)
- `/tin-tuc/*` (4 bài) trùng `/thi-truong/*` → xóa + 301, xóa cả hub /tin-tuc/.
- `/dat-nen/` + `/nha-ban/` (hub cũ) trùng `-nam-ban` → xóa index + 301 (giữ lô con).
- 4 bài quy hoạch từng 2 bản → gộp về `/thi-truong/`.
- Xóa: `.htaccess`(Apache vô dụng trên Vercel), `HUONG-DAN-DEPLOY.html`(nội bộ lộ), `shared-images/`(47MB kho trung chuyển), `update-news.mjs`+news.json(automation chết), 6 ảnh rác p1-p6.jpg.

## TRẠNG THÁI SEO
- **27–29 URL trong sitemap** (chỉ trang self-canonical, không noindex/redirect).
- **22 trang canonical→Panorama** (editorial/quy hoạch/đời sống — đã nhường).
- **1 noindex**: `thi-truong/song-o-nam-ban` (nhường Panorama).
- 3 trang giao dịch: self-canonical, nội dung thật, index.
