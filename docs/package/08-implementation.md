# 08 · IMPLEMENTATION — KỸ THUẬT / SEO-GEO / AUTOMATION
*Prompt 1C: kiến trúc, code, design token, SEO/GEO technical, automation, workflow.*

## 1. TECHNICAL ARCHITECTURE
- **Static HTML + CSS + Vanilla JS** — không framework, không bundler, không build step.
- Repo `doanquocduyet/nambanvillas` → branch dev `claude/dreamy-ritchie-xBezi` → merge `main` = deploy.
- Host **Vercel** (auto-deploy từ main). Quota free 100 build/ngày — không push thừa. Deploy = merge PR (dùng GitHub MCP, squash).
- Cấu trúc: mỗi trang là 1 folder `<slug>/index.html`. Section: dat-nen, nha-ban, thi-truong, ve-nam-ban, namban-notes.

## 2. DESIGN SYSTEM (token)
- Màu: `--green:#1A3D2B` · `--gold:#C9A84C` · `--bg:#F7F3EE` · `--bg2:#FFFFFF`.
- Font: Plus Jakarta Sans Variable (jsDelivr CDN). CSS: `css/style.css` + `css/article.css` (bài).
- Popup: localStorage (không sessionStorage) — 1 lần/đời user.
- Ảnh bài: `.article-img` 1200×600, bo góc; xử bằng PIL (không có ImageMagick).

## 3. SEO / GEO TECHNICAL (đã triển khai)
- Schema: RealEstateAgent + WebSite + FAQPage + Product/Offer (từng lô) + Service (dich-vu) + Breadcrumb + Article + **spatialCoverage** (bài) + **sameAs/knowsAbout** + **speakable**.
- Toạ độ homepage **11.7586, 108.2432** (đúng tâm Nam Ban — không lệch).
- Địa danh chuẩn: **Xã Nam Ban** (từ 1/7/2025, không còn "thị trấn"). Giữ "thị trấn" chỉ trong bài kể lịch sử sáp nhập.
- **llms.txt** entity-focused; robots cho 8 AI bot (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Google-Extended, CCBot, Applebot-Extended, Bingbot).
- **IndexNow** auto-submit (workflow indexnow.yml) + RSS feed.xml (build-feed.mjs) + sitemap.xml (chỉ trang self-canonical, không noindex/redirect).
- GA4: `G-LHGW9K1BDP`. GSC + Bing verify tag ở index.html.

## 4. AUTOMATION
- `scripts/daily-listings.mjs` + workflow `daily-listings.yml` (7h sáng VN): Claude API (web search) → chọn 1–2 tin theo `FORM-DANG-TIN.md` → viết lại (bỏ SĐT) → chèn trang tin-rao. **Cần secret `ANTHROPIC_API_KEY`** để bật.
- `scripts/build-feed.mjs` + `weekly-update.yml` (thứ 2): rebuild feed.xml.
- Fail-safe: API lỗi/không tin chất lượng → thoát sạch, không commit rác.

## 5. WORKFLOW GIT (bài học)
- Conflict hay gặp ở sitemap/file vừa sửa → `git fetch+merge main`, `--ours` giữ bản mới, push, merge lại.
- Cuối commit message KHÔNG để lộ model ID / thông tin nội bộ.
- Verify sau mỗi thay đổi (JSON-LD valid, XML valid, không placeholder) TRƯỚC khi push.
