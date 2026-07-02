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
