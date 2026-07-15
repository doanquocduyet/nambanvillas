# PASTE ĐỂ MỞ Ô CLAUDE CODE CHUYÊN VIẾT CONTENT

> Chú copy nguyên khối bên dưới, dán vào ô Claude Code mới (repo `doanquocduyet/nambanvillas`).
> Ô này **chỉ viết bài/content SEO** — KHÔNG đụng trang đăng tin lô/cụm (ô đăng tin lo).

---

Chào cháu. Ô này chuyên **VIẾT CONTENT / BÀI SEO** cho web nambanvillas.vn. Đích tối thượng vẫn là làm khách **bấm Gọi / Zalo 0978 758 788** — bài viết là để kéo khách vào rồi dẫn xuống trang cụm/lô.

## BƯỚC 0 — NẠP DỰ ÁN (đọc trước khi viết)
1. `CLAUDE.md` — quy tắc bất biến (chú chỉ bấm/copy/paste; làm ra kết quả rồi báo NGẮN GỌN; giọng "đọc rủi ro", số thật, không hype).
2. `docs/HIEN-PHAP-3-WEB.md` — **luật canonical/keyword 3 web**. ĐỌC KỸ: Villas ôm key GIAO DỊCH; cùng key khác intent thì không cắn nhau; không tự tạo trang trùng canonical.
3. `docs/DANG-CUM-MOI.md` — mục **"KEYWORD + AEO/SEO/GEO CHUẨN CHO CỤM"** (bộ keyword + luật hub).
4. `docs/package/MO-O-DANG-TIN.md` — mục **"CHUẨN AEO/SEO/GEO/UX/UI"** (áp dụng chung cho mọi trang).

**BRANCH:** làm trên branch content RIÊNG (vd `claude/noi-dung-nam-ban-*`) → PR → squash merge `main`. **KHÔNG dùng chung branch với ô đăng tin** (tránh đụng nhau).

## RANH GIỚI 2 Ô (không giẫm chân)
- **Ô ĐĂNG TIN (code):** trang lô/cụm `/dat-nen/…`, `/nha-ban/…`, ảnh, sơ đồ, kỹ thuật, deploy.
- **Ô CONTENT (ô này):** bài viết trong `/thi-truong/`, `/ve-nam-ban/`, hoặc trang cẩm nang mới; SEO copy; internal link trỏ về hub `/cum-moi-nam-ban/` + các trang cụm/lô.
- Nếu cần sửa trang đăng tin → GHI CHÚ lại cho ô đăng tin, đừng tự sửa.

## KEYWORD MỤC TIÊU (Villas ôm — giao dịch + thông tin)
- Head/mid: `đất phân lô Nam Ban` · `cụm đất nền Nam Ban` · `đất nền phân lô Nam Ban` · `giá đất Nam Ban` · `mua đất Nam Ban` · `đất nền Nam Ban Lâm Hà`
- Long-tail: `đất nền Nam Ban sổ riêng` · `đất nền Nam Ban thổ cư` · `đất nền F0 Nam Ban` · `đất phân lô Nam Ban giá rẻ` · `kinh nghiệm mua đất Nam Ban`
- Theo khu: Đông Thanh · Từ Liêm · Mê Linh · Tầm Xá · Nam Ban trung tâm.

## CHUẨN MỖI BÀI (bắt buộc đủ 4)
**SEO:** title duy nhất (key ở đầu) · meta desc 140–160 có key+số+địa danh · `canonical` đúng URL (không trùng bài cũ) · H1 duy nhất · breadcrumb + `BreadcrumbList` · og/twitter · **thêm URL vào `sitemap.xml`** · **internal link**: mỗi bài trỏ về hub `/cum-moi-nam-ban/` + 2–3 trang cụm/lô liên quan (anchor có keyword).
**AEO:** `FAQPage` 4–6 câu, **câu đầu trả lời thẳng** (giá? khu nào? pháp lý? rủi ro?). `Article` schema (`headline`, `datePublished`, `dateModified`, `author`/`publisher` = Nam Ban Villas, `image`). Có bảng dữ liệu (giá theo khu…) để AI bóc.
**GEO:** `geo.region=VN-LB` + `geo.placename` + Nam Ban · Lâm Hà · Lâm Đồng + khoảng cách Đà Lạt (~22–25km) / sân bay Liên Khương (~22km) + mốc (chùa Linh Ẩn/Thiền Viện, núi Voi, Thác Voi, ĐT725).
**UX/UI + thương hiệu:** nút **Gọi + Zalo** rõ (như các bài `/thi-truong/` sẵn có) · giọng "**đọc rủi ro**", số thật, KHÔNG "lời to/sốt/siêu phẩm" · **KHÔNG bịa số, testimonial, tên người** · đẹp **desktop + mobile** (rà @media, không chụp ảnh tốn token — soi bằng đọc code responsive).

## KỸ THUẬT (khắc cứng)
- Template: copy khung 1 bài `/thi-truong/…` sẵn có (vd `thi-truong/dau-tu-dat-nam-ban/index.html` — đã có Article + FAQ + breadcrumb), thay nội dung. Dùng `/css/style.css` + `/css/article.css`, path gốc `/css/…`, `/js/…`.
- **CẤM regex DOTALL** `.*?` để xoá/sửa khối HTML — dùng str_replace khớp CHÍNH XÁC.
- **CẤM trỏ link/nhúng ảnh của web khác**; ảnh chỉ dùng ảnh của web (nén `python3 scripts/nen-anh.py` nếu thêm ảnh mới).
- Verify trước push: JSON-LD hợp lệ · 0 placeholder · link nội bộ không hỏng · canonical không đụng bài cũ.
- **KHÔNG tạo bài trùng chủ đề đã có** trong `/thi-truong/` (đã có ~20 bài: bảng giá, đầu tư, kinh nghiệm mua, quy hoạch Lâm Đồng, sân bay Liên Khương, khí hậu/sống ở Nam Ban…). Trùng thì NÂNG CẤP bài cũ thay vì tạo mới.

## DANH SÁCH BÀI ƯU TIÊN (làm từ trên xuống)
1. **[BÀI TRỤ]** *"Mua đất phân lô Nam Ban 2026: bảng giá theo khu, khu nào đang mở, pháp lý & 5 điều cần kiểm"* → slug gợi ý `/thi-truong/dat-phan-lo-nam-ban/`. ~900–1200 chữ, có **bảng giá theo khu** (Mê Linh/Đông Thanh <600tr, Từ Liêm từ 650tr, Tầm Xá từ 1,15 tỷ), FAQ 5–6 câu, **link xuống hub + cả 4 cụm đang mở**. Đây là bài kéo top mạnh nhất cho nhóm key "đất phân lô Nam Ban".
   → Sau khi đăng: thêm 1 link từ hub `/cum-moi-nam-ban/` trỏ LÊN bài trụ (ghi chú cho ô đăng tin nếu cần sửa hub).
2. Cẩm nang từng khu (mỗi khu 1 bài): *"Đất nền Đông Thanh / Mê Linh / Từ Liêm / Tầm Xá Nam Ban: vị trí, giá, pháp lý, có gì"* — link tới trang cụm tương ứng.
3. *"Đất nền F0 Nam Ban là gì, mua sao cho đúng?"* — giải nghĩa F0 + rủi ro + checklist.
4. *"Sổ riêng vs chưa tách thửa khi mua đất phân lô Nam Ban"* — pháp lý, đúng brand "đọc rủi ro".
5. Cập nhật định kỳ *"Giá đất Nam Ban tháng …"* (nếu bài bảng giá cũ chưa phủ) — hoặc nâng cấp bài bảng giá sẵn có.

## WORKFLOW MỖI BÀI
Viết HTML bài → verify (JSON-LD/link/canonical/desktop+mobile) → thêm sitemap → internal link về hub + cụm → PR → squash merge main (Vercel auto deploy) → báo NGẮN GỌN + link `https://nambanvillas.vn/…`.

Giờ cháu đọc BƯỚC 0, xác nhận đã nạp, rồi bắt đầu từ **BÀI TRỤ số 1**.
