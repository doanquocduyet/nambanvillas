# 08 · IMPLEMENTATION — KỸ THUẬT / SEO-GEO / AUTOMATION
*Prompt 1C: thu hồi ĐẦY ĐỦ tri thức triển khai. Giữ nguyên số/tên/config.*

## 1. TECHNICAL ARCHITECTURE
- **Static HTML + CSS + Vanilla JS** — không framework, không bundler, không build step.
- Repo `doanquocduyet/nambanvillas` · branch dev `claude/dreamy-ritchie-xBezi` → squash merge `main` = deploy.
- Host **Vercel** (auto-deploy từ main). Quota free **100 build/ngày** — không push thừa. **1 project Vercel DUY NHẤT** nối repo (`nambanvillas`, slug `duyet-s-projects`); phát hiện 2–3 project cùng nối = báo ngay (từng gây stale + duplicate + domain disconnect).
- Mỗi trang = folder `<slug>/index.html`. Section: `dat-nen-nam-ban`, `nha-ban-nam-ban`, `thi-truong`, `ve-nam-ban`, `namban-notes`, `dich-vu`, `lien-he`, `hoi-dap`; lô ở `dat-nen/<lô>`, nhà ở `nha-ban/<căn>`.
- `vercel.json`: `cleanUrls:true`, `trailingSlash:false`, **~30 redirect 301**: `/tin-tuc→/thi-truong`, `/tin-tuc/:path*→/thi-truong/:path*`, 4 slug /tin-tuc/* cũ, `/dat-nen→/dat-nen-nam-ban`, `/nha-ban→/nha-ban-nam-ban`, `/dat-nen/lo-*`, `/gia-dat-nam-ban→bang-gia`, `/nam-ban-o-dau→ve-nam-ban`, `/contact→lien-he`, v.v.

## 2. DESIGN SYSTEM (token)
- Màu: `--green:#1A3D2B` · `--gold:#C9A84C` · `--bg:#F7F3EE` · `--bg2:#FFFFFF` · `--muted`. Font **Plus Jakarta Sans Variable** (jsDelivr CDN, preconnect).
- CSS: `css/style.css` (toàn site, 553 dòng) + `css/article.css` (bài, 142 dòng; class `.article-img/.article-body/.article-hero/.article-header/.faq-item`). **Trùng chéo 12 selector** (.breadcrumb-bar, .quick-form-btn, .sidebar-specs...) — override, để yên (rủi ro sửa cao). ~43 class có thể không dùng — để yên (dò tự động dễ nhầm class JS chèn).
- JS: `js/main.js`. Popup sell-widget: **localStorage** `nbv_popup_seen` (1 lần/đời user), trigger scroll ≥60% + exit-intent (mouseleave desktop).
- Ảnh: xử bằng **PIL** (KHÔNG có ImageMagick/cv2). `ImageOps.exif_transpose` + `ImageOps.fit` cover-crop **1200×600 q82 progressive**; hero resize max 1600 wide. `.article-img` bo góc 12px. `Date.now/Math.random` KHÔNG dùng trong script sandbox (workflow node thì dùng bình thường).

## 3. SEO / GEO TECHNICAL (kịch trần on-page)
- **Schema (JSON-LD):** RealEstateAgent (trang chủ: telephone +84978758788, address, areaServed, geo, openingHours Mo-Su 07:00-21:00, priceRange $$, **sameAs**[zalo], **knowsAbout**) + WebSite (SearchAction + **speakable** [.hero-title/.hero-sub]) + **FAQPage** (76 chỗ, +speakable ở hoi-dap) + **Product/Offer từng lô** + **Service** (dich-vu: provider RealEstateAgent + areaServed Place + serviceType[] + offers) + BreadcrumbList + Article/NewsArticle + **spatialCoverage** (Place Nam Ban/Lâm Hà/Lâm Đồng, 26 bài).
- **Toạ độ 11.7586, 108.2432** (ĐÚNG tâm Nam Ban — KHÔNG lệch; Greenspace từng lệch 108.383 ~10km, Villas không dính).
- Địa danh **"Xã Nam Ban"** (sửa "TT. Nam Ban" 30 chỗ); giữ "thị trấn" chỉ trong bài kể sáp nhập (đúng lịch sử).
- **`llms.txt`** entity-focused (chỉ trang Villas sở hữu: lô/giá/pháp lý/FAQ; bỏ trang nhường Panorama; số thật 2-7tr; Q&A trả lời nhanh).
- **`robots.txt`** cho 8+ AI bot: GPTBot, OAI-SearchBot, ChatGPT-User, Google-Extended, PerplexityBot, Perplexity-User, ClaudeBot, Claude-Web, anthropic-ai, CCBot, Applebot-Extended, Bingbot. Disallow /admin/ /subscribe/. Sitemap ref.
- **`sitemap.xml`**: chỉ trang self-canonical (loại noindex + redirect + canonical→Panorama). Dựng lại tự động từ canonical khi conflict. tin-rao changefreq daily, gia-dat/nhà/đất weekly.
- **IDs thật**: GA4 `G-LHGW9K1BDP` (thay G-XXXXXXXXXX ở 51 file) · GSC `YGizLbsXiK5UhFc-1FL2YP_f0IsXxdljfiiibFIkQ68` · Bing `msvalidate.01=4EC1CA93863C0CE0E9822A68994C9222` · IndexNow key file `abdd063f81d049182d79e17f4239ad8f.txt`.
- OG image `images/og-namban.jpg` 1200×630 130KB (từng bị truncate→2KB text, khôi phục từ git history). RSS `feed.xml` + `<link rel=alternate>`.
- **Đã dọn duplicate content**: /tin-tuc/* (4 bài) + hub /tin-tuc/ + /dat-nen/ + /nha-ban/ (hub cũ) — xóa + 301. Xóa `.htaccess` (Apache vô dụng Vercel), `HUONG-DAN-DEPLOY.html` (nội bộ lộ), `shared-images/` (47MB kho trung chuyển trùng ảnh Panorama), 6 ảnh rác p1-p6.jpg.

## 4. AUTOMATION (3 GitHub Actions)
- **`daily-listings.yml`** cron `7 0 * * *` (=7h07 VN): `scripts/daily-listings.mjs` gọi Claude API (`claude-sonnet-5`, tool `web_search_20250305` max 5) → chọn 1–2 tin theo `FORM-DANG-TIN.md` (lọc ≥4/7 dữ kiện + blocklist từ rác) → viết lại bỏ SĐT/ảnh → chèn `thi-truong/tin-rao-dat-nam-ban-moi/index.html` giữa marker `<!-- DAILY-DIGEST:START/END -->`, giữ 20 mục (`<!-- DAY:YYYY-MM-DD -->`), cập nhật dateModified + article-cat; market-note mỗi ≥3 ngày (state `data/tin-rao-state.json`). **Cần secret `ANTHROPIC_API_KEY`** để bật. **Fail-safe**: thiếu key/API lỗi/không tin chất lượng → `process.exit(0)`, KHÔNG commit rác. Commit `git add ...index.html state feed.xml`, `[skip ci]`.
- **`weekly-update.yml`** cron thứ 2: `scripts/build-feed.mjs` rebuild `feed.xml` từ HTML self-canonical (bỏ trang canonical off-domain, dùng URL nội bộ). Trước từng chạy `update-news.mjs` ghi news.json rỗng → đã gỡ (automation chết).
- **`indexnow.yml`** on push HTML/sitemap lên main: sleep 90s chờ Vercel rồi submit URL đổi cho Bing/IndexNow (env INDEXNOW_KEY + HOST).
- Trang `gia-dat-nam-ban-hom-nay` có marker `<!-- WEEKLY-PRICE:START/END -->` (chưa nối script — có thể thêm cron Chủ nhật tổng hợp tin tuần).

## 5. WORKFLOW GIT (bài học kỹ thuật)
- CẤM DOTALL `.*?` sửa HTML/CSS → str_replace/JSON parser/sed chuỗi cố định.
- Conflict hay ở sitemap/file vừa sửa → `git fetch+merge origin/main`, `git checkout --ours <file>` giữ bản mới, hoặc dựng lại sitemap từ self-canonical, push, merge PR lại.
- Xóa file để vào main: **merge main vào branch TRƯỚC rồi git rm** (merge-base phải chứa file) → xác minh `git ls-tree -r origin/main | grep`.
- Verify TRƯỚC push: `json.loads` mọi JSON-LD, `minidom.parse` XML, 0 placeholder, ảnh/link tồn tại.
- Commit message: KHÔNG lộ model ID / token / thông tin nội bộ.

## 6. CÒN LẠI (ngoài code — cần Chú)
- Bật automation: tạo Anthropic API key (console.anthropic.com) → GitHub Secrets `ANTHROPIC_API_KEY`. Có thể chạy tay `workflow_dispatch`.
- **Google Business Profile** (business.google.com) → lên Google Maps + local pack (schema giúp Google HIỂU, GBP mới cho XUẤT HIỆN trên bản đồ).
- Facebook Page chính thức → thêm vào `sameAs`.
- Ảnh listing thật: chỉ khi lô thành lô Villas (tự chụp/xin phép), không lấy ảnh tin người khác.
