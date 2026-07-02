# ================ NAM BAN VILLAS — PROJECT OS (ALL-IN-ONE) ================
*Copy toàn bộ file này dán vào Knowledge của project. Gộp từ docs/package/. Cập nhật 2/7/2026.*



======================================================================
# NAM BAN VILLAS — PROJECT OS PACKAGE
*Gói đóng để mọi phiên AI mới nạp là hiểu ngay dự án. Theo protocol Panorama (Prompt 0→1A→1A+→1B→1C).*

Đọc theo thứ tự:
1. `00-repository-audit.md` — repo có gì, trạng thái.
2. `02-working-os.md` — cách Chú + Claude làm việc.
3. `04-product-taste.md` — gu thẩm mỹ/chất lượng của Chú.
4. `06-project-knowledge.md` — business, số thật, hệ 3 web, IA.
5. `08-implementation.md` — stack, schema, SEO/GEO, automation.

Đọc kèm (chi tiết sâu hơn): `../HIEN-PHAP-3-WEB.md`, `../FORM-DANG-TIN.md`, `../HO-SO-TONG-NAMBAN-MAX.md`, `../TU-DUY-TINH-TUE.md`, `../../CLAUDE.md`.

*Gói này là bản tinh gọn (extraction, không phình). Cập nhật khi có tri thức mới đáng lưu.*



======================================================================
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



======================================================================
# 02 · WORKING OS — CÁCH CHÚ + CLAUDE LÀM VIỆC
*Prompt 1A: hệ LÀM VIỆC. Rút từ hàng trăm vòng chat.*

## WORKFLOW
- Vòng: **ĐỀ XUẤT → DUYỆT (chú gật/lắc) → LÀM (Claude tự làm hết)**. Việc nhỏ làm luôn; việc lớn đề xuất trước.
- Mỗi việc xong: **kèm link `👉 https://nambanvillas.vn/...`** để chú bấm thẳng. Nhiều trang → mỗi link 1 dòng.
- Deploy = tạo PR + **squash merge vào main** qua GitHub MCP. Không cần chú vào GitHub.

## CÁCH CHÚ RA LỆNH (đọc đúng ý)
- Câu ngắn, đôi khi gõ nhanh/lỗi chính tả/cụt ("Tự researxh rồi viết đi", "cái nào lợi nhất thì lầm"). Claude phải **đoán đúng + xác nhận nếu mơ hồ**, không chạy sai hướng.
- "Cái nào lợi nhất cho aeo seo geo ux ui thì làm" = Claude **tự xếp ưu tiên theo ROI rồi làm**, không liệt kê options cho có.
- "Có gì hay bổ sung không" = chú muốn Claude **chủ động đề xuất cái tốt hơn**.
- Chú **sửa số trực tiếp** ("Nam ban 2-7tr, Bảo lộc 5-15tr") → Claude cập nhật toàn site + FAQ schema, giữ đúng ngữ cảnh (không đụng "20-40%/tháng").
- Chú **muốn xem mẫu trước khi nhân rộng** (2 tin rao mẫu, trang giá mẫu) rồi mới chốt tự động.
- Chú tự đổi model giữa chừng (fable-5 ↔ opus-4-8) — model là quyền của chú.

## NGUYÊN TẮC BẤT THÀNH VĂN
- **Chú chỉ bấm/copy/paste.** Không bao giờ bảo chú "vào GitHub/mở terminal/dán code". Cần chú làm gì → đúng 1 việc + link trực tiếp.
- **Nói thẳng giới hạn** — Drive mất kết nối/proxy chặn ảnh ngoài thì nói thẳng, không hứa suông, không giả vờ làm được.
- **Không bịa** — số/tên/testimonial phải thật; không có thì để trống hoặc hỏi chú. Trang chưa có nội dung → **noindex + ẩn `[NỘI DUNG CẦN VIẾT]`**, không lộ ra live.
- **CEO-mindset khi quyết**: ROI + rủi ro, không "cho sạch". Code tĩnh dư vô hại → để yên (CSS trùng, class không dùng); máy chạy vô ích → tắt (update-news).
- **Bảo mật**: token/API key KHÔNG bao giờ ghi vào file/commit; model ID không để lộ trong commit/PR.
- Phiên khác (Panorama/Greenspace/hub) gửi việc → làm đúng phần Villas, **báo lại hub đối chiếu**. Token fine-grained chỉ mở repo nambanvillas (chạm repo khác → 403 là đúng thiết kế).

## GIT — BÀI HỌC ĐÃ TRẢ GIÁ
- **CẤM regex DOTALL `.*?`** sửa HTML/CSS (mất dữ liệu 2 lần) → str_replace khớp duy nhất / JSON parser.
- Merge hay conflict ở **sitemap / file vừa sửa** → `git fetch origin main && git merge origin/main`, resolve bằng **`git checkout --ours <file>`** (giữ bản mới của mình), hoặc dựng lại sitemap từ trang self-canonical, push, merge lại.
- **Squash "net xóa" từng trượt** (shared-images không vào main): vì merge-base chưa chứa file. Cách đúng: **merge main vào branch TRƯỚC** (đưa file vào base) **rồi mới `git rm`** → deletion mới vào main.
- **Verify TRƯỚC khi push**: JSON-LD valid, XML valid, 0 placeholder, link không gãy.



======================================================================
# 04 · PRODUCT TASTE — GU CỦA CHÚ
*Prompt 1A+: gu thẩm mỹ/chất lượng. Không phải cách làm việc, không phải token.*

## DESIGN TASTE
- **"Im lặng mà sang"** — không emoji, không banner, không gấp gáp, không hô hào.
- Sạch, nhiều khoảng trắng, khối ngắn, **mới nhất lên đầu**, số quan trọng **tô đậm** để quét mắt.
- **Gold `#C9A84C` chỉ 4 chỗ**: nút call mobile nav · số Pain section · border-left Notes editorial · hover trên nền tối. Lạm dụng gold = sai gu.
- Ảnh: cắt khung **2:1 (1200×600)**, bo góc 12px; hero phủ lớp gradient xanh đậm cho chữ đọc được. Không ảnh thô/lòe loẹt.
- Bản PC: ô phụ (Namban Notes) dàn gọn 3 cột ngang, không chiếm chỗ ô chính; listing hiển thị ngang.

## PRODUCT TASTE (ngưỡng "đúng ý")
- **Số thật > tính từ đẹp.** "2–7 triệu/m²", "568 triệu/lô" đúng gu; "giá cực tốt", "view đỉnh" sai gu.
- **CẤM tính từ rỗng** (đã quét & xóa toàn site): tuyệt đẹp · lý tưởng · hoàn hảo · siêu phẩm · cực hiếm · số 1 · rẻ nhất · giá sốc · cơ hội vàng · đất vàng · vị trí vàng.
- Dám nói **rủi ro / "đừng mua"** = tín hiệu chất lượng, tạo tin. Bài/tin thiếu phần "rủi ro cần kiểm" = **chưa tới**.
- Trang lộ `[NỘI DUNG CẦN VIẾT]` ra live = **lỗi nặng, không chấp nhận**.
- **Thà ít mà chất**: 1–2 tin tốt/ngày hơn nhiều tin rác. Không đủ chất → không đăng.

## CRITIQUE TASTE (cách chú review)
- Câu ngắn, thẳng: "trùng thế nào", "số sai 2-7tr", "cái nào lợi nhất thì làm", "xem kỹ".
- Ghét dài dòng/liệt kê lựa chọn → muốn **1 khuyến nghị + làm luôn**.
- Chú duyệt bằng cách **đưa số thật** hoặc **chỉ hướng**, ít khi khen; im lặng qua = ổn.

## COMPARISON / PERFECTION TASTE
- Ưu tiên **cụ thể-chạm** (lô thật, giá thật, link lô) hơn **trừu tượng-đẹp** (concept, triết lý, hệ sinh thái).
- Luôn tự kiểm 3 điều: số có thật không · có đụng bản quyền không (KHÔNG lấy ảnh/chữ nguyên văn của tin người khác) · có đụng chạm ai không (KHÔNG "cò/lừa đảo/thổi giá").
- Đánh đổi đã chốt: **thương hiệu "đọc rủi ro, không bán giấc mơ" đặt trên mọi cám dỗ marketing.** Không tối ưu chuyển đổi bằng cách nói quá.



======================================================================
# 06 · PROJECT KNOWLEDGE — BUSINESS / SỐ THẬT / IA
*Prompt 1B: business, research, content, information architecture.*

## BUSINESS
- **Villas = phần "ra tiền" của hệ 3 web.** Vai: môi giới + pháp lý giao dịch. Vũ khí độc quyền: ~14 lô THẬT, giá thật, sổ thật (Panorama không có).
- Doanh thu: người sắp mua → xem lô → chốt; ăn phí giao dịch (sang tên/công chứng/hợp đồng/tách thửa/chuyển thổ).
- **Bài học Zames Chew (case chú gửi):** thị trường trả tiền cho **giải nỗi đau cụ thể**, KHÔNG cho ý tưởng/hệ sinh thái đẹp. Villas bán **"giảm rủi ro / chắc chắn hơn khi ra quyết định"**, không bán đất. Có khách trước → mới có hệ sinh thái, không ngược lại.
- **5 nỗi đau khách (TP.HCM, 10–15 tỷ)**: (1) không biết tin ai · (2) không biết khu nào đáng nghiên cứu · (3) không có thời gian khảo sát · (4) sợ mua sai · (5) sợ mua đỉnh. Mọi nội dung Villas nhắm 5 cái này. Khách sợ **mất 3 năm/mua sai**, không sợ mất 100 triệu.

## SỐ THẬT (chú xác nhận — dùng nhất quán)
- Giá đất Nam Ban **2–7 triệu/m²** (nền thổ cư 3–7 · vườn nông nghiệp 0,2–3 · view cao hơn nền cùng khu ~10–30%). Giá chốt thấp hơn giá rao 5–15%.
- Bảo Lộc **5–15tr/m²** · Đà Lạt nội đô **50–150tr/m²** · Di Linh thấp (nông nghiệp).
- **2 tỷ ở Nam Ban = 400–1.000m²** có thổ cư; ở Đà Lạt chỉ ~15–40m².
- Cách Đà Lạt **35–40 phút (~27–28km)** đèo Tà Nung · sân bay Liên Khương ~22km. Khí hậu 18–22°C, cao 850–1.000m.
- Homestay thuê **500k–1,5tr/đêm**; yield cho thuê tham chiếu **~5–6%/năm**. Chi phí sống gia đình 3–4 người **10–18tr/tháng** (thấp hơn Đà Lạt 30–40%).
- Second home tổng: đất 400tr–2 tỷ + xây **100–200tr/100m²** + vận hành 30–80tr/năm.
- 2023–25 tăng mạnh (**+40–60% năm 2025**) → 2026 điều chỉnh/chọn lọc, ưu tiên sản phẩm khai thác được.
- Hành chính: từ **1/7/2025 "Xã Nam Ban"** (sáp nhập thị trấn NB + Đông Thanh + Mê Linh + Gia Lâm). 30 câu hỏi ở /hoi-dap/.

## LÔ ĐANG BÁN (giá thật để dẫn chứng)
Phố Thông Villas 2×130m²(80m² thổ) **568tr/lô** · Thung Lũng 530m² view **899tr** · Đông Thanh 320m² · Đông Thanh 845m²(239 thổ) chưa tới 2 tỷ · Hai mặt tiền 345m² **1,15 tỷ** · Hồ Từ Liêm 700m² **1,2 tỷ** · Mê Linh suối 650m² **1,25 tỷ** · Hồ Bãi Công lô1 700m²(200 thổ) **1,95 tỷ** · Hồ Bãi Công lô2 950m² · Giáp Suối 2.700m²(400 thổ) **2,95 tỷ** · Siêu phẩm 3.700m² MT61m full thổ **5,7 tỷ**. Nhà: Hill House 203m² **2,6 tỷ** · Villa Mini Mê Linh 239m² **2,38 tỷ** · Nhà vườn 1.018m² hồ koi **3,8 tỷ**.

## CONTENT PHILOSOPHY
- "Đọc rủi ro, không bán giấc mơ". Tách bạch **lô Villas đã kiểm tra** vs **tin thị trường chưa kiểm chứng** (trang tin-rao).
- Mọi tin/bài dẫn về **Zalo 0978 758 788** để Villas kiểm giúp = biến traffic thành lead.

## INFORMATION ARCHITECTURE
- **Hệ 3 web — cùng keyword KHÁC INTENT → không cắn nhau**: Panorama=nghiên cứu/cộng đồng (đầu phễu, ĐỘC LẬP) · Villas=giao dịch (lô/giá/pháp lý) · Greenspace=trông coi đất (hậu mua). Chi tiết `HIEN-PHAP-3-WEB.md`.
- **Luật link**: Villas KHÔNG link Panorama; Villas↔Greenspace 2 chiều (link Greenspace ở /dich-vu/).
- **Cụm thị trường sống**: tin-rao (ngày) → gia-dat-hom-nay (tuần) → mua-dat-bao-nhieu (nền tảng) — link chéo, freshness.
- **Cụm giao dịch** (self-canonical, đã viết số thật): mua-dat-nam-ban-bao-nhieu · nam-ban-so-voi-noi-khac · dau-tu-dat-nam-ban.
- Nav: Đất Nền · Nhà Bán · Về Nam Ban · Thị Trường · Dịch Vụ · Liên Hệ.



======================================================================
# 08 · IMPLEMENTATION — KỸ THUẬT / SEO-GEO / AUTOMATION
*Prompt 1C: kiến trúc, code, token, technical SEO/GEO, automation, workflow.*

## ARCHITECTURE
- **Static HTML + CSS + Vanilla JS** — không framework/bundler/build step.
- Repo `doanquocduyet/nambanvillas` · branch dev `claude/dreamy-ritchie-xBezi` → merge `main` = deploy.
- Host **Vercel** (auto-deploy main). Quota free 100 build/ngày — không push thừa. **1 project Vercel duy nhất** nối repo (`nambanvillas`, slug duyet-s-projects); phát hiện 2–3 project cùng nối = báo ngay (từng gây stale + duplicate).
- Mỗi trang = folder `<slug>/index.html`. `vercel.json`: `cleanUrls:true`, `trailingSlash:false`, ~30 redirect 301 (gồm /tin-tuc/*→/thi-truong/*, /dat-nen→/dat-nen-nam-ban, /nha-ban→/nha-ban-nam-ban, các slug cũ).

## DESIGN TOKEN
- `--green:#1A3D2B` · `--gold:#C9A84C` · `--bg:#F7F3EE` · `--bg2:#FFFFFF` · `--muted`. Font Plus Jakarta Sans Variable (jsDelivr).
- CSS: `css/style.css` (toàn site) + `css/article.css` (bài, class `.article-img/.article-body/.article-hero`). Có trùng chéo 12 selector (override, để yên — rủi ro sửa cao).
- JS: `js/main.js`. Popup sell-widget: **localStorage** `nbv_popup_seen` (1 lần/đời user), trigger scroll 60% + exit-intent.
- Ảnh xử bằng **PIL** (không có ImageMagick): `ImageOps.fit` cover-crop 1200×600, quality 82, progressive.

## SEO/GEO (đã triển khai — kịch trần on-page)
- Schema: RealEstateAgent + WebSite (+SearchAction+**speakable**) + FAQPage(+speakable) + **Product/Offer từng lô** + Service (dich-vu: provider+areaServed+serviceType) + Breadcrumb + Article + **spatialCoverage**(26 bài) + **sameAs**[zalo] + **knowsAbout**.
- **Toạ độ 11.7586, 108.2432** (đúng tâm Nam Ban — KHÔNG lệch; Greenspace từng lệch 108.383).
- Địa danh **"Xã Nam Ban"** (giữ "thị trấn" chỉ trong bài kể sáp nhập).
- `llms.txt` entity-focused (chỉ trang Villas sở hữu). `robots.txt` cho 8 AI bot: GPTBot, OAI-SearchBot, ChatGPT-User, Google-Extended, PerplexityBot, ClaudeBot, CCBot, Applebot-Extended, Bingbot.
- `sitemap.xml`: chỉ trang self-canonical (loại noindex + redirect); dựng lại tự động từ canonical khi conflict.
- IDs: GA4 `G-LHGW9K1BDP` (51 file) · GSC `YGizLbsXiK5UhFc-1FL2YP_f0IsXxdljfiiibFIkQ68` · Bing `4EC1CA93863C0CE0E9822A68994C9222` · IndexNow key `abdd063f81d049182d79e17f4239ad8f`.
- OG image `images/og-namban.jpg` (130KB thật; từng bị truncate thành 2KB text — khôi phục từ git history).

## AUTOMATION (3 GitHub Actions)
- **daily-listings.yml** (cron `7 0 * * *` = 7h07 VN): `scripts/daily-listings.mjs` → Claude API (model `claude-sonnet-5`, tool `web_search_20250305`) chọn 1–2 tin theo `FORM-DANG-TIN.md`, viết lại bỏ SĐT, chèn `tin-rao-dat-nam-ban-moi` giữa marker `DAILY-DIGEST:START/END`, giữ 20 ngày; market-note mỗi ≥3 ngày (state `data/tin-rao-state.json`). **Cần secret `ANTHROPIC_API_KEY`** để bật. Fail-safe: API lỗi/không tin → exit 0, không commit.
- **weekly-update.yml** (thứ 2): `build-feed.mjs` rebuild `feed.xml` từ HTML self-canonical.
- **indexnow.yml** (push HTML/sitemap lên main): submit URL đổi cho Bing/IndexNow (sleep 90s chờ Vercel).
- Trang giá tuần `gia-dat-nam-ban-hom-nay` có marker `WEEKLY-PRICE:START/END` (chưa nối script — có thể thêm cron Chủ nhật).

## CÒN LẠI (ngoài code — cần chú)
- Bật automation: tạo Anthropic API key → GitHub Secrets tên `ANTHROPIC_API_KEY`.
- **Google Business Profile** (business.google.com) — để lên Google Maps/local pack.
- 3 trang giao dịch đã xong nội dung; song-o-nam-ban giữ noindex (nhường Panorama).
