# IMPLEMENTATION_KNOWLEDGE_REPOSITORY — NAM BAN VILLAS
*Prompt 1C. Thu hồi ĐẦY ĐỦ tri thức triển khai. Giữ nguyên số/tên/config/thuật ngữ. Không merge/diễn giải.*

## A. TECHNICAL ARCHITECTURE
- **Static HTML + CSS + Vanilla JS** — không framework, không bundler, không build step. Zero-build → GitHub → Vercel.
- Repo `doanquocduyet/nambanvillas`. Branch dev `claude/dreamy-ritchie-xBezi` → squash merge `main` = deploy production. Site `nambanvillas.vn`.
- **Vercel**: auto-deploy từ main; quota free **100 build/ngày**; 1 project DUY NHẤT (`nambanvillas`, slug `duyet-s-projects`); preview link ở PR comment do Vercel bot đăng.
- **Routing**: mỗi trang = folder `<slug>/index.html`. `vercel.json`: `cleanUrls:true`, `trailingSlash:false`, ~30 redirect 301 (/tin-tuc→/thi-truong, /tin-tuc/:path*→/thi-truong/:path*, 4 slug tin-tuc cũ, /dat-nen→/dat-nen-nam-ban, /nha-ban→/nha-ban-nam-ban, /dat-nen/lo-*, /gia-dat-nam-ban→/thi-truong/bang-gia-dat-lam-dong-2026, /nam-ban-o-dau→/ve-nam-ban, /khi-hau-nam-ban→/thi-truong/khi-hau-cuoc-song-nam-ban, /contact→/lien-he...).
- Section: dat-nen-nam-ban, nha-ban-nam-ban, thi-truong, ve-nam-ban, namban-notes, dich-vu, lien-he, hoi-dap; lô `dat-nen/<lô>`, nhà `nha-ban/<căn>`.

## B. DEVELOPMENT KNOWLEDGE
- 51 index.html. Template bài có 3 dạng: (1) `.article-header`+`.article-body`+`<div>` (pillar mới), (2) `<article class="article-body">`+`.article-hero` (bài cũ), (3) inline-styled trần (bài quy hoạch có SVG chart). Chèn nội dung phải khớp đúng anchor từng dạng.
- Marker tự động: `<!-- DAILY-DIGEST:START/END -->` (tin-rao), `<!-- DAY:YYYY-MM-DD -->` (mỗi ngày), `<!-- WEEKLY-PRICE:START/END -->` + `<!-- WEEK:... -->` (giá tuần).
- Reusable: header/nav/footer/mobile-sheet lặp mọi trang; box CTA Zalo `background:#EBF4EE`; box lô đang bán `border:1px solid #E2E0DB`.

## C. DESIGN SYSTEM IMPLEMENTATION
- Token: `--green:#1A3D2B` · `--gold:#C9A84C` · `--bg:#F7F3EE` · `--bg2:#FFFFFF` · `--muted`. Radius, border `#E2DBD0/#ECEAE4`.
- Font Plus Jakarta Sans Variable (jsDelivr, preconnect). CSS: `css/style.css` (553 dòng) + `css/article.css` (142). Trùng chéo 12 selector (override, để yên). ~43 class nghi không dùng (để yên).
- `.article-img` width:100% bo góc 12px; `.notes-editorial` grid 3 cột ≥769px.

## D. FRONTEND IMPLEMENTATION
- Popup sell-widget: localStorage `nbv_popup_seen`, trigger scroll ≥60% + exit-intent (mouseleave). Mobile bottom nav + mobile sheet menu. QH map zoom/pan (wheel + drag). Quiz mục đích (4 lựa chọn → gợi ý trang). loading="lazy" + fetchpriority="high" ảnh hero.

## E. BACKEND / INFRASTRUCTURE
- Không backend/CMS/DB — thuần static. Form liên hệ dùng Zalo/tel. Secrets: `ANTHROPIC_API_KEY` (GitHub Actions). Domain nambanvillas.vn nối Vercel (từng disconnect khi xóa project thừa → phải reconnect ở vercel.com/.../settings/domains).

## F. AI IMPLEMENTATION
- Claude Code + GitHub MCP (mọi thao tác GitHub). CLAUDE.md nạp context mỗi phiên; docs/ chứa Hiến pháp/Form/Hồ sơ/Tư duy + **docs/package/** (Project OS). Context engineering: phiên mới đọc `docs/package/ALL-IN-ONE.md` để bootstrap.
- Automation AI: `daily-listings.mjs` gọi Claude API `claude-sonnet-5` + tool `web_search_20250305`.

## G. SEO / GEO TECHNICAL IMPLEMENTATION
- **Schema JSON-LD:** RealEstateAgent (telephone +84978758788, address PostalAddress, areaServed, geo GeoCoordinates, openingHours Mo-Su 07:00-21:00, priceRange $$, sameAs[https://zalo.me/0978758788], knowsAbout[]) + WebSite (SearchAction + speakable cssSelector[.hero-title,.hero-sub]) + FAQPage (76 chỗ; hoi-dap +speakable cssSelector[summary]) + Product+Offer từng lô + Service (dich-vu: provider+areaServed Place+serviceType[]+offers price 0) + BreadcrumbList + Article/NewsArticle + **spatialCoverage** (Place Nam Ban/Lâm Hà/Lâm Đồng, 26 bài).
- **Toạ độ 11.7586, 108.2432** (đúng tâm Nam Ban; KHÔNG lệch — Greenspace từng lệch 108.383).
- **Địa danh "Xã Nam Ban"** (sửa "TT. Nam Ban" 30 chỗ); giữ "thị trấn" trong bài kể sáp nhập.
- **llms.txt** entity-focused (chỉ trang Villas sở hữu, số 2-7tr, Q&A nhanh). **robots.txt**: 8+ AI bot (GPTBot, OAI-SearchBot, ChatGPT-User, Google-Extended, PerplexityBot, Perplexity-User, ClaudeBot, Claude-Web, anthropic-ai, CCBot, Applebot-Extended, Bingbot); Disallow /admin/ /subscribe/.
- **sitemap.xml**: chỉ self-canonical (loại noindex/redirect/canonical-off-domain); dựng lại từ canonical khi conflict; tin-rao daily, khác weekly/monthly.
- **IDs:** GA4 `G-LHGW9K1BDP` (51 file) · GSC `YGizLbsXiK5UhFc-1FL2YP_f0IsXxdljfiiibFIkQ68` · Bing `4EC1CA93863C0CE0E9822A68994C9222` · IndexNow key `abdd063f81d049182d79e17f4239ad8f`.
- OG `images/og-namban.jpg` 1200×630 130KB (khôi phục từ git history sau khi bị truncate). RSS feed.xml + link alternate.

## H. DEVELOPMENT WORKFLOW
- Đổi = PR + squash merge. Conflict (sitemap/file vừa sửa): fetch+merge main, `--ours` giữ bản mới hoặc dựng lại sitemap, push, merge lại. Xóa để vào main: merge main trước → git rm → xác minh ls-tree.
- CẤM DOTALL `.*?`; sửa schema hàng loạt qua json.loads/dumps. Verify (JSON/XML valid, 0 placeholder, link/ảnh tồn tại) trước push. Commit message không lộ model ID/token.

## I. QA / TESTING
- Sau mỗi thay đổi: `python3 json.loads` mọi ld+json; `minidom.parse` sitemap/feed; grep placeholder = 0; kiểm link nội bộ gãy; `file` kiểm ảnh binary thật (từng phát hiện ảnh .jpg là base64 text). Hard refresh Ctrl+Shift+R kiểm cache. Kiểm 1 H1/trang, không slug trùng.

## J. ASSETS
- **scripts/**: `daily-listings.mjs` (cron 7 0 * * *; chọn 1–2 tin FORM-DANG-TIN, bỏ SĐT, chèn tin-rao giữ 20 ngày, market-note ≥3 ngày, state data/tin-rao-state.json, fail-safe exit 0), `build-feed.mjs` (rebuild feed.xml từ HTML self-canonical, skip canonical off-domain).
- **workflows/**: daily-listings.yml (cần secret ANTHROPIC_API_KEY), weekly-update.yml (build-feed thứ 2), indexnow.yml (push→sleep 90s→submit Bing/IndexNow).
- **docs/**: CLAUDE.md, HIEN-PHAP-3-WEB, FORM-DANG-TIN, HO-SO-TONG-NAMBAN-MAX, TU-DUY-TINH-TUE, package/ (00/02/04/06/08 + repo/ 4 file _REPOSITORY + ALL-IN-ONE + PROJECT-INSTRUCTION).
- **Ảnh:** PIL (ImageOps.fit 1200×600 q82 progressive; hero max 1600). Đã xóa: shared-images/ 47MB, .htaccess, HUONG-DAN-DEPLOY.html, p1-p6.jpg, update-news.mjs+news.json.
- **CÒN LẠI ngoài code (cần Chú):** bật automation (Anthropic key → secret), Google Business Profile, Facebook Page cho sameAs, ảnh listing thật (tự chụp/xin phép).
