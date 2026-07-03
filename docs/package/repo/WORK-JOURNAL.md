# WORK JOURNAL — NAM BAN VILLAS (biên niên toàn bộ quá trình)
*Ghi lại chi tiết từng việc/vấn đề/quyết định theo trình tự, từ đầu đến 2/7/2026. Không bỏ sót. Đây là "quá trình dài" mà các tài liệu _REPOSITORY tóm lại thành nguyên tắc.*

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 0 — NỀN TẢNG (phiên trước, tóm từ context)
═══════════════════════════════════════════════════════════════
- **Namban Notes gọn lại:** Chú phản ánh "bản PC: namban notes chiếm chỗ quá, dàn gọn lại, đó ko phải ô chính". → Làm 3 editorial item thành **grid 3 cột ngang ≥769px** (`.notes-editorial-wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:0 28px}`), giảm chiều cao. Conflict `.notes-section` padding (giữ 20px 0 thay 28px cũ).
- **Listing ngang:** Chú "bản pc chưa thấy list sp ngang" → xác nhận CSS đã có trên main (`.prop-grid{display:flex;flex-direction:column}` + `.prop-card{grid-template-columns:272px 1fr}`), bảo hard refresh cache.
- **Google Search Console:** thêm `<meta name="google-site-verification" content="YGizLbsXiK5UhFc-1FL2YP_f0IsXxdljfiiibFIkQ68">`. Chú dán nhầm tag nhiều lần, verify fail nhiều lần.
- **Chẩn đoán GSC fail = gốc rễ Vercel:** site live serve bản CŨ vì `nambanvillas.vn` **bị disconnect khỏi Vercel** sau khi Chú xóa 2 project thừa (`nambanvillas-2afy`, `nambanvillas-nr8v`). Hướng dẫn Chú reconnect domain ở vercel.com/duyet-s-projects/nambanvillas/settings/domains. Đây là bài học "1 project Vercel duy nhất".
- **GA4:** thay placeholder `G-XXXXXXXXXX` → `G-LHGW9K1BDP` trên **51 file HTML** (find + sed).
- **Bing Webmaster:** thêm `<meta name="msvalidate.01" content="4EC1CA93863C0CE0E9822A68994C9222">`.
- **4 trang pillar SEO/AEO (khung):** Chú duyệt chiến lược "4 pillar thay 17 bài lẻ, mỗi trang ôm nhiều cụm key, Q&A cho AEO". Tạo 3/4: mua-dat-nam-ban-bao-nhieu, dau-tu-dat-nam-ban, nam-ban-so-voi-noi-khac (đều có FAQ+Article+Breadcrumb schema, placeholder `[NỘI DUNG CẦN VIẾT]`). Chú chốt "xong".

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 1 — HOÀN TẤT 4 PILLAR (PR#7)
═══════════════════════════════════════════════════════════════
- Tạo trang thứ 4 **`thi-truong/song-o-nam-ban/`** (chi phí/trường học/internet/điện nước/y tế; FAQ có sẵn số thật: 10-18tr/tháng, THPT Nam Ban, internet 100-300Mbps, TT y tế Lâm Hà).
- Commit 4 trang → PR#7 → merge main. Gửi Chú 4 link.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 2 — PHÂN TÍCH TRÙNG KEYWORD 3 SITE
═══════════════════════════════════════════════════════════════
- Chú gửi keyword doc của **Greenspace** + **Panorama**, hỏi trùng không.
- Kết luận: **Greenspace KHÔNG trùng** (thuần dịch vụ trông coi/kiểm tra đất — lane sạch). **Panorama TRÙNG NẶNG** (gần như cả bộ key thương mại: giá rẻ, view, vườn, phân lô, đầu tư, sống, so sánh).
- Giải thích: khác domain không bị "phạt" nhưng **pha loãng** (Google chọn 1 site/truy vấn) + **AEO tệ hơn** (AI chọn 1 nguồn). Đề xuất phân vai theo intent.
- "trùng thế nay thi sao" → giải thích hệ quả, khuyên cross-link + đừng đẩy 5 bài Greenspace.
- Chú báo **đã đẩy 5 bài Greenspace** (dat-vuon-ai-trong, view-dep, gia-re, dat-nen-phan-lo, ban-dat-o-xa). → Đề xuất **canonical 5 trang Greenspace về Villas** (gắn 1 dòng vào file Greenspace, không cần share repo). Map cụ thể từng trang.
- "Panorama cung lam vay dc ko" → map Panorama→Villas canonical (mua-dat, namban-index, tiem-nang-dau-tu, dat-vuon, view-dep, gia-re, phan-lo, so-sanh); giữ nguyên trang key riêng của Panorama (dat-gan-da-lat, quy-hoach, du lịch...).

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 3 — DỌN TRÙNG NỘI BỘ /tin-tuc/ (PR#8)
═══════════════════════════════════════════════════════════════
- Chú chỉ ra 4 bài nghi trùng (lam-dong-quy-hoach-dieu-chinh-2026, quy-hoach-tinh-2025, nhung-thay-doi-2025, nghi-duong-retreat).
- Phát hiện: đây là **trùng NỘI BỘ** — mỗi bài có 2 bản ở `/thi-truong/` (đầy đủ ~16-21KB) VÀ `/tin-tuc/` (gọn ~12-18KB), **cả 2 đều self-canonical** = duplicate content thật. Khác hẳn chuyện canonical 3 site.
- "trùng trong 1 trang thì nên xóa 1 bản" → kiểm vercel.json (đã có redirects sẵn), link nội bộ. Phát hiện thêm: `/tin-tuc/index.html` link tới 10 bài `/tin-tuc/...` nhưng chỉ 4 folder tồn tại → **6 link 404 ngầm**.
- Xử: `git rm` 4 folder /tin-tuc trùng; sửa link /tin-tuc/index.html trỏ hết sang /thi-truong (vá luôn 6 link gãy); thêm 4 redirect 301 `/tin-tuc/*→/thi-truong/*`.
- Conflict merge (main vừa sửa 4 file cháu xóa) → `git rm -f` giữ quyết định xóa. PR#8 merge.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 4 — AUDIT SÂU SITE (PR#9)
═══════════════════════════════════════════════════════════════
- "kiểm tra kỹ lại xem còn trùng gì, link mở đc ko, nội dung ok ko".
- Không còn slug trùng. 52 trang.
- **Link gãy `/bat-dong-san/`** ở tin-tuc + thi-truong (nav cũ) → sửa → `/dat-nen-nam-ban/`. (thi-truong còn "bat-dong-san" là link BÁO ngoài vneconomy/baodautu — hợp lệ, giữ.)
- **Ảnh hỏng nghiêm trọng:**
  - `og-namban.jpg` = **text base64 2KB** (không phải ảnh) → ảnh share Facebook/Zalo hỏng trên 5 trang. Git log cho thấy từng là JPEG 130KB (commit 36bf948) rồi bị deploy ghi đè thành text. → Khôi phục `git show 36bf948:images/og-namban.jpg` = 129979 bytes 1200×630.
  - `p1-p6.jpg` = 21 byte rác, không trang nào dùng → xóa.
  - `nam-ban-aerial.jpg` (nền hero trang chủ) = **CHƯA TỪNG được commit** → hero chỉ hiện gradient. Báo Chú cần ảnh flycam thật.
  - Xác nhận ảnh listing (200-260KB) thật, mở được.
- PR#9 merge.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 5 — HIẾN PHÁP 3 WEB + ÁP DỤNG (PR constitution, PR#10)
═══════════════════════════════════════════════════════════════
- Chú gửi **HIEN-PHAP-3-WEB** (8 phần: tư tưởng từng web, 3 tệp khách, "cùng keyword khác intent", bản đồ keyword, keys độc quyền, luật link/canonical, AEO, nguyên tắc bất biến).
- Lưu `docs/HIEN-PHAP-3-WEB.md` + trỏ CLAUDE.md. Điểm sửa đề xuất trước: **Panorama đứng độc lập → CẤM Villas link sang Panorama** (thay cross-link cũ bằng link Greenspace).
- **BRIEF VILLAS từ hub** — thực thi:
  - **LOẠI 2 (22 trang) canonical→Panorama**: 6 đời sống + 8 giá/thị trường/đầu tư/sân bay + 8 quy hoạch/về-nam-ban. Đổi self-canonical → URL Panorama qua python.
  - **LOẠI 1 (3 trang giao dịch) GIỮ + tái định vị**: thêm khối "lô đang bán" link xuống 2-3 lô thật (giá thật 568tr/899tr/1,25tỷ...), KHÔNG canonical.
  - **Xóa hub /tin-tuc/** rỗng + 301.
  - **Link Villas→Greenspace** ở /dich-vu ("mua xong ở xa? trông coi đất từ xa →").
  - Conflict sitemap + vercel.json → resolve. PR#10 merge. Verify origin/main.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 6 — TOKEN MỚI + VIỆC TỪ HUB (PR#17)
═══════════════════════════════════════════════════════════════
- Chú dán token villas-only (fine-grained, Contents R/W, chỉ repo nambanvillas). Cháu test đọc index.html qua github MCP → OK. **KHÔNG lưu token vào file**. Báo "token mới chạy OK".
- Việc từ hub (Panorama vừa audit): (1) sửa canonical `nam-ban-co-hop-voi-ban-khong` → `nam-ban-co-hop-voi-ban` (Panorama đổi slug) — grep toàn repo chỉ 1 file dùng. (2) Gỡ dứt `shared-images/` 47MB còn kẹt main.
- **Bài học squash net-xóa:** lần trước gỡ shared-images không vào main vì merge-base chưa chứa. Lần này **merge main vào branch TRƯỚC** (đưa 152 file vào base) rồi `git rm` → deletion vào thật. Xác minh `git ls-tree -r origin/main | grep shared-images` = 0. PR#17.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 7 — AUDIT KỸ THUẬT SÂU (PR#11)
═══════════════════════════════════════════════════════════════
- "kiểm tra kỹ thuật, rà chậm chi tiết".
- Loại file: 57→52 html; scripts .mjs được workflow gọi (không chết); .github có 2 workflow (weekly-update, indexnow).
- **File chết/trùng phát hiện + xóa:**
  - `/dat-nen/index.html` + `/nha-ban/index.html` = hub CŨ, trùng `-nam-ban`, **bị 301 che → không serve được = chết**. Xóa index (giữ lô con).
  - `.htaccess` = Apache config, Vercel bỏ qua = chết. Xóa.
  - `HUONG-DAN-DEPLOY.html` = tài liệu deploy nội bộ lộ public. Xóa.
- **Sitemap mâu thuẫn:** 45 URL, trong đó **21 trang vừa canonical→Panorama vẫn nằm trong sitemap** (sitemap bảo index, canonical bảo Panorama) + **thiếu 3 trang giao dịch**. → Dựng lại từ trang self-canonical = 27 URL.
- **build-feed.mjs** dùng canonical làm URL → feed.xml link sang Panorama (nghịch Hiến pháp). Sửa: skip trang canonical off-domain, dùng URL nội bộ. Regenerate feed.
- Sửa comment GA4 gây hiểu nhầm. PR#11.
- **Báo Chú (không tự sửa):** CSS trùng chéo 12 selector + ~43 class nghi không dùng (rủi ro cao, để yên); update-news.mjs ghi news.json rỗng vô ích.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 8 — CEO XỬ 3 VIỆC + GỠ AUTOMATION CHẾT (PR#13)
═══════════════════════════════════════════════════════════════
- "nếu cháu là ceo/chuyên gia thì xử sao".
- **Nguyên tắc chốt:** code tĩnh dư vô hại → để yên (CSS #1,#2 — ROI âm, rủi ro vỡ layout). Máy chạy vô ích → tắt (#3).
- Gỡ `update-news.mjs` + `data/news.json`; đơn giản hóa `weekly-update.yml` còn rebuild feed. PR#13.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 9 — AUDIT NỘI DUNG (PR#14, PR#15)
═══════════════════════════════════════════════════════════════
- "kiểm tra content, câu từ đụng chạm, chuẩn aeo/seo/ux/ui, dàn trang, cỡ chữ, tô đậm".
- **TỐT:** không từ đụng chạm (không cò/lừa đảo/thổi giá); mọi trang đúng 1 H1; FAQ trả lời thẳng câu đầu; typography nhất quán (design token).
- **Placeholder LỘ ra live:** 4 trang (mua-dat 7 khối, dau-tu 8, nam-ban-so 7, song-o 5). lien-he "placeholder" là form input hợp lệ (bỏ qua).
- **Từ hô hào/rỗng:** tuyệt đẹp×6 (kham-pha H1), cơ hội vàng×7 (san-bay title/H1), hoàn hảo×2, lý tưởng×9, số một×1, tốt nhất×3. → Sửa ở title/H1/meta: "vườn thảo mộc tuyệt đẹp"→"vườn thảo mộc"; "cơ hội vàng cho BĐS"→"tác động tới"; bang-gia title bỏ "Cơ Hội Vàng"; thung-lung FAQ "thiên nhiên tuyệt đẹp"→"khung cảnh thiên nhiên". "rẻ nhất" trong FAQ giữ (search intent). PR#14.
- **4 trang placeholder:** theo luật "không bịa — anh Duyệt điền" → **noindex,follow + chuyển `[NỘI DUNG CẦN VIẾT]` thành HTML comment** (ẩn khỏi khách, giữ brief) + rút 3 trang giao dịch khỏi sitemap. PR#15.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 10 — VIẾT NỘI DUNG THẬT (bỏ luật cấm) (PR#16, #26, #28)
═══════════════════════════════════════════════════════════════
- Chú "tạm bỏ qua luật cấm, nếu cháu là CEO/SEO/AEO/UX thì ưu tiên cái nào hiệu quả nhất".
- **Nguyên tắc CEO:** dồn vào trang gần tiền nhất, không dàn đều. Ưu tiên #1 = hoàn thiện 3 trang giao dịch (đang noindex = tài sản bỏ không, nhắm key người-sắp-mua).
- **mua-dat-nam-ban-bao-nhieu (PR#16):** viết 4 H2 + 3 FAQ bằng số thật (lô 568tr→5,7 tỷ, dải 2-9tr/m², rủi ro từng loại). Gỡ noindex, thêm sitemap. (Sau Chú sửa 2-9→2-7.)
- **nam-ban-so-voi-noi-khac (PR#26):** "cái nào lợi nhất thì làm" → chọn trang so sánh (AEO cao nhất — câu so sánh AI hay hỏi). Bảng 4 vùng (giá/m², cách SG, khí hậu, hợp ai, rủi ro), 3 mục + 3 FAQ số thật. Gỡ noindex.
- **dau-tu-dat-nam-ban (PR#28):** "tự research rồi viết" → web search homestay/second-home. Viết dòng tiền (đất trống không tự sinh), homestay (thuê 500k-1,5tr/đêm, rủi ro công suất), second home (đất 400tr-2 tỷ + xây 100-200tr/100m² + vận hành 30-80tr/năm, yield 5-6%), tăng giá 2023-25, "ai KHÔNG nên mua". Gỡ noindex.
- **Sửa số thật (PR#27):** Chú "Nam ban 2-7tr, Bảo lộc 5-15tr, 2 tỷ 400-1000m2" → cập nhật toàn site + FAQ schema; **giữ ngữ cảnh** (không đụng "20-40 triệu/tháng" homestay, "20-40%" tăng giá).
- song-o-nam-ban giữ noindex (nhường Panorama).

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 11 — GEO (PR#18, PR#19)
═══════════════════════════════════════════════════════════════
- "chuẩn geo nhất chưa, áp dụng mọi kỹ thuật".
- Đã có: schema RealEstateAgent/FAQPage×76/Product+Offer×56/Breadcrumb; llms.txt; robots 8 AI bot; IndexNow.
- **Thêm (PR#18):** refresh `llms.txt` entity-focused (bỏ trang nhường Panorama, số 2-7tr, khối Q&A nhanh); `sameAs`[zalo] + `knowsAbout` vào RealEstateAgent; `speakable` vào WebSite + hoi-dap FAQPage.
- **Từ Panorama session (PR#19):** thêm `spatialCoverage` (Place Nam Ban/Lâm Hà/Lâm Đồng) vào **26 bài**; sửa "TT. Nam Ban"→"Xã Nam Ban" **30 chỗ** (giữ "thị trấn" trong bài kể sáp nhập). Xác nhận **toạ độ Villas 11.7586,108.2432 ĐÚNG** (Greenspace lệch 108.383, Villas không dính). dich-vu đã có Service schema sẵn.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 12 — TỰ ĐỘNG TIN RAO (PR#12, #21, #22, #23, #24, #25)
═══════════════════════════════════════════════════════════════
- "mỗi ngày cháu tự tìm tin bds nam ban, chắt lọc tự đăng, ko để số điện thoại".
- **Quyết định thiết kế:** KHÔNG tạo bài lẻ mỗi ngày (thin content) → **1 trang sống** cập nhật (mới nhất lên đầu), ghi rõ "chưa kiểm chứng" tách khỏi lô Villas.
- Tạo **`tin-rao-dat-nam-ban-moi`** + marker DAILY-DIGEST; wired sitemap/llms/link (PR#21).
- **2 tin mẫu (PR#23):** web search → đất vườn 622m² (bơ+cà phê, 100 thổ, MT4m), lô góc 450m² (252 thổ, 2MT) + quan sát thị trường (đấu giá 3/7). Viết lại lời mình, bỏ SĐT, ghi Nguồn, nút Zalo.
- Chú làm rõ: 1-2 tin CHẤT/ngày, viết lại kiểu mình, bỏ SĐT.
- **Automation (PR#12/#22):** `daily-listings.mjs` gọi Claude API (claude-sonnet-5 + web_search_20250305) → chọn 1-2 tin theo FORM → viết lại bỏ SĐT → chèn trang, giữ 20 ngày, market-note ≥3 ngày, state file, **fail-safe exit 0**. Workflow `daily-listings.yml` cron 7h07 VN, **cần secret ANTHROPIC_API_KEY**.
- **Chi phí:** giải thích 2 cách — A (cháu làm tay, miễn phí, khi phiên mở) vs B (tự động, ~vài nghìn/ngày API).
- **Ảnh listing người khác:** khuyên KHÔNG lấy (bản quyền + proxy chặn); dùng ảnh chung.
- **FORM-DANG-TIN.md (PR#24):** 5 bước (lọc→thông số→viết→giọng→HTML mẫu) + vì sao tối ưu. Trỏ CLAUDE.md.
- **Trang giá tuần + nâng lọc (PR#25):** `gia-dat-nam-ban-hom-nay` (bảng giá/m² theo loại, so tuần trước, marker WEEKLY-PRICE); FORM thêm **blocklist từ rác** (chắc chắn lời/sốt đất/ngộp bank...) + **checklist 7 dữ kiện (≥4)**.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 13 — ẢNH BÀI (PR#12 images)
═══════════════════════════════════════════════════════════════
- Chú up `shared-images/` (152 ảnh) lên GitHub, "cháu tự chọn ảnh phù hợp, up cho các bài".
- Xử bằng **PIL** (không có ImageMagick): cover-crop 1200×600 q82. Hero `nam-ban-aerial.jpg` (fix hero thiếu). **22 ảnh lead** khớp chủ đề chèn vào bài (4 template khác nhau). Bỏ qua bài đã có infographic SVG. Xóa ảnh mồ côi.
- **Gỡ `shared-images/` 47MB** khỏi repo (kho trung chuyển trùng ảnh Panorama). PR#12.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 14 — LOCAL / MODEL
═══════════════════════════════════════════════════════════════
- "đưa con qua local" → hướng dẫn Claude Code desktop (claude.ai/download) + clone repo; nói thẳng local không lợi hơn cho workflow auto-deploy của Chú.
- Chú tự đổi model fable-5 ↔ opus-4-8 giữa phiên.

═══════════════════════════════════════════════════════════════
# GIAI ĐOẠN 15 — PROJECT OS PACKAGE (PR#29→#33)
═══════════════════════════════════════════════════════════════
- Chú gửi Drive Panorama (5 prompt Project OS Migration Protocol) — cháu KHÔNG mở được Drive (MCP ngắt + proxy chặn). Chú upload 5 docx + case Zames.
- Đọc 5 prompt: 0 Repository Audit · 1A Working OS · 1A+ Product Taste · 1B Project Knowledge · 1C Implementation (mỗi cái "thu hồi ĐẦY ĐỦ, không diễn giải").
- Phân tích case Zames Chew: bán "certainty/giảm rủi ro" không bán đất; giải nỗi đau cụ thể trước, không xây hệ sinh thái trước → **Villas đang đúng hướng**.
- Tạo `docs/package/` 00/02/04/06/08 + README (PR#29) → cô đặc + ALL-IN-ONE (PR#30) → PROJECT-INSTRUCTION description+instructions (PR#31) → mở rộng đầy đủ (PR#32) → **4 tài liệu _REPOSITORY sâu** repo/ (PR#33).
- Chú: "vẫn quá ít, quá trình rất lâu và dài" → viết **WORK-JOURNAL này** (biên niên đầy đủ).

═══════════════════════════════════════════════════════════════
# TỔNG KẾT TRẠNG THÁI (2/7/2026)
═══════════════════════════════════════════════════════════════
- **Cụm giao dịch (index, số thật):** mua-dat-bao-nhieu · nam-ban-so-voi-noi-khac · dau-tu-dat-nam-ban.
- **Cụm thị trường sống:** tin-rao (ngày, chờ bật API key) · gia-dat-hom-nay (tuần) · mua-dat (nền tảng).
- **22 trang** canonical→Panorama; **1 noindex** (song-o).
- **GEO kịch trần on-page**; toạ độ đúng; địa danh Xã Nam Ban.
- **~30 PR** đã merge trong hành trình.
- **Còn ngoài code (cần Chú):** bật automation (Anthropic key→secret ANTHROPIC_API_KEY), Google Business Profile, Facebook Page cho sameAs, ảnh hero/listing thật, viết số thật enrich thêm.
- **Bộ Project OS:** docs/package/ (5 bản tóm + 4 _REPOSITORY sâu + WORK-JOURNAL + PROJECT-INSTRUCTION + ALL-IN-ONE).
