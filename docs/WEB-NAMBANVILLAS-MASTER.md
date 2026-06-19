# WEB NAMBANVILLAS — BẢN GHI TỔNG (MASTER RECORD)

> Tài liệu cô đặc, đậm đặc nhất về toàn bộ quá trình thiết kế lại, tối ưu, và các
> quyết định — kỹ thuật, thiết kế, tâm lý, nội dung — của website **nambanvillas.vn**.
> Ghi lại không chỉ "đã làm gì" mà cả "tại sao", "đã tranh luận gì", và "nguyên tắc rút ra".
>
> Cập nhật: 2026-06-19 · Repo: `doanquocduyet/nambanvillas` · Deploy: Vercel auto từ `main`
> Chủ sở hữu: doanquocduyet@gmail.com

---

## MỤC LỤC

1. [Định danh & bối cảnh dự án](#1-định-danh--bối-cảnh-dự-án)
2. [Vấn đề gốc & ý định của chủ](#2-vấn-đề-gốc--ý-định-của-chủ)
3. [Triết lý thiết kế hình thành](#3-triết-lý-thiết-kế-hình-thành)
4. [Hệ thống thiết kế (Design System)](#4-hệ-thống-thiết-kế-design-system)
5. [Kiến trúc kỹ thuật](#5-kiến-trúc-kỹ-thuật)
6. [Nhật ký quyết định theo dòng thời gian](#6-nhật-ký-quyết-định-theo-dòng-thời-gian)
7. [Phân tích từng section trang chủ](#7-phân-tích-từng-section-trang-chủ)
8. [Chiến lược Mobile UX](#8-chiến-lược-mobile-ux)
9. [Tâm lý học ứng dụng](#9-tâm-lý-học-ứng-dụng)
10. [Quy trình kiểm thử (QA)](#10-quy-trình-kiểm-thử-qa)
11. [Dọn dẹp code & nợ kỹ thuật](#11-dọn-dẹp-code--nợ-kỹ-thuật)
12. [Hệ thống SEO/AEO (được bảo toàn)](#12-hệ-thống-seoaeo-được-bảo-toàn)
13. [Lịch sử commit có chú giải](#13-lịch-sử-commit-có-chú-giải)
14. [Bug đã gặp & nguyên nhân gốc](#14-bug-đã-gặp--nguyên-nhân-gốc)
15. [Còn lại / TODO](#15-còn-lại--todo)
16. [Nguyên tắc & bài học rút ra](#16-nguyên-tắc--bài-học-rút-ra)
17. [Phụ lục: đối thoại nguyên văn](#17-phụ-lục-đối-thoại-nguyên-văn)

---

## 1. ĐỊNH DANH & BỐI CẢNH DỰ ÁN

- **Tên:** Nam Ban Villas (nambanvillas.vn)
- **Lĩnh vực:** Bất động sản — đất nền & nhà bán tại **Nam Ban, Lâm Hà, Lâm Đồng** (cao nguyên, sát Đà Lạt ~25 phút).
- **Loại site:** Website tĩnh thuần — **HTML + CSS + JavaScript vanilla**, không framework, không build step nặng. Deploy tự động qua **Vercel** mỗi khi push lên nhánh `main` GitHub.
- **Quy mô:** **46 file HTML** — 1 trang chủ + ~45 trang con:
  - `dat-nen/` — 11 trang chi tiết lô đất + 1 trang index
  - `nha-ban/` — 3 trang nhà (hill-house-village, nha-vuon-1018m2, villa-mini-me-linh)
  - `thi-truong/` — 11 bài phân tích thị trường/quy hoạch
  - `namban-notes/` — 4 bài editorial (góc nhìn thực địa)
  - `ve-nam-ban/`, `lien-he/`, `hoi-dap/` (hub FAQ 29 câu)
- **Tài sản phụ trợ:** `feed.xml` (RSS), `llms.txt` (cho AI crawler), `robots.txt`, `sitemap.xml`, `vercel.json`, IndexNow key file, `scripts/` (build-feed.mjs, update-news.mjs), `data/news.json`.
- **Kích thước core hiện tại:** `index.html` 606 dòng · `css/style.css` 411 dòng · `js/main.js` 124 dòng.

### Định vị thương hiệu (brand positioning)
Câu lõi xuyên suốt — slogan và là copyright của TẤT CẢ các trang:

> **"Giúp bạn ra quyết định đúng về đất Nam Ban"**

Đây không phải site "bán đất bằng mọi giá". Định vị là **người dẫn đường trung thực** — giúp khách *hiểu* thị trường để *tự* ra quyết định, kể cả quyết định KHÔNG mua. (Xem mục 9 — Tâm lý học.)

---

## 2. VẤN ĐỀ GỐC & Ý ĐỊNH CỦA CHỦ

Câu khởi động toàn bộ phiên làm việc (nguyên văn):

> *"chú phát hiện trang chủ đang quá dày chữ, và nhiều khoảng trống ko cần thiết, cháu nghiên cứu thiết kế lại cho phù hợp, vừa đủ sang, vừa đủ ko quá trống."*

**Phân rã yêu cầu:**
- "Quá dày chữ" → giảm mật độ text, tăng khoảng thở có chủ đích.
- "Nhiều khoảng trống ko cần thiết" → khác với khoảng thở — đây là *dead space* vô nghĩa cần xóa.
- "Vừa đủ sang" → sang trọng nhưng không phô trương (luxury kiềm chế).
- "Vừa đủ ko quá trống" → cân bằng — không dày, không loãng.

**Ràng buộc cứng (chủ xác nhận):**
> *"Có giữ nguyên nội dung ko... các kỹ thuật content, seo, aeo, các kỹ thuật khác để tạo phễu và hút khách, tự động hút khách như từng làm ở trên ko"*

→ **TUYỆT ĐỐI giữ nguyên:** toàn bộ nội dung, Schema.org JSON-LD, hệ thống SEO/AEO, phễu khách, RSS/IndexNow/llms.txt. Chỉ thay đổi **trình bày (presentation)**, không động vào **dữ liệu/nội dung/máy móc tự động hóa**.

**Lựa chọn hướng đi:** Cháu đề xuất 2 mức — (A) chỉnh nhẹ CSS, (B) tái cấu trúc toàn bộ thứ tự section. Chủ chọn:
> *"Làm B trước"* → tái cấu trúc sâu.

---

## 3. TRIẾT LÝ THIẾT KẾ HÌNH THÀNH

Đây là phần "tâm lý/nguyên tắc" mà nhiều khi không gọi tên được, nhưng chi phối mọi quyết định nhỏ.

### 3.1. Kỷ luật màu sắc (color discipline)
**Vấn đề ban đầu:** Vàng gold (`#C9A84C`) bị dùng tràn lan — section label, tiêu đề, nút, số liệu — làm loãng giá trị của chính nó. Khi mọi thứ đều "nổi" thì không gì nổi.

**Nguyên tắc thiết lập:**
- **Gold = tài nguyên hiếm.** Chỉ dùng cho: số liệu hero, sao đánh giá, CTA quan trọng, điểm nhấn nhỏ. KHÔNG dùng cho section label.
- **Section label → xám muted** (`--muted`), weight 600 thay vì gold 700. Nhãn là thứ phụ, không tranh chỗ với tiêu đề.
- **Chỉ section "neo" (Listings) được "đối xử nặng"** — tiêu đề lớn hơn (clamp 1.7–2.3rem, weight 800). Các section khác tiêu đề nhẹ hơn (1.5–2rem, weight 700). Vì Listings là *lý do tồn tại* của trang.

### 3.2. Nhịp điệu section (section rhythm)
Mắt cần điểm nghỉ. Không để 4 section sáng liên tiếp.
- Xen kẽ **sáng ↔ tối**: Hero (tối) → Listings (trắng) → Why (kem) → Quy hoạch (kem) → **Pain (xanh đậm — neo tối)** → Testimonials (trắng) → **Quiz (xanh đậm)** → Notes (xanh nhạt) → Footer (tối).
- Mỗi section phải **khác biệt thị giác rõ ràng** — không 2 section nào "trông giống nhau". (Đây là nguồn gốc nhiều lần sửa: Pain vs Testimonials vs Notes.)

### 3.3. Mô hình tiếp xúc "1 cố định + 1 theo ngữ cảnh"
**Vấn đề:** Nút Gọi/Zalo/SĐT nổi (floating) + lặp trong mọi bài + mọi sản phẩm = rối mắt, mất sang.

**Nguyên tắc:**
- **1 điểm cố định:** header (desktop) / bottom-nav (mobile).
- **1 điểm theo ngữ cảnh:** CTA box trong nội dung / card sidebar của trang sản phẩm.
- **Bỏ hết floating buttons** site-wide.

### 3.4. Thumb zone (vùng ngón cái) trên mobile
> *"Thanh menu trên điện thoại để ở giữa phía trên 2 ngón đều khó thao tác / Nên thiết kế tối ưu mọi thứ trải nghiệm trên điện thoại"*

→ Hamburger ở góc trên = phản ergonomics. Thay bằng **bottom navigation bar** — vùng ngón cái với tới dễ nhất khi cầm điện thoại 1 tay.

### 3.5. "Vừa đủ" — chống cả hai thái cực
- Chống **dày:** bỏ rotating quote, mini-survey trong hero, manifesto, 1 stat thừa.
- Chống **loãng:** bỏ `min-height:100vh` của hero (tạo khoảng trắng chết), nén padding card.

---

## 4. HỆ THỐNG THIẾT KẾ (DESIGN SYSTEM)

### 4.1. Biến CSS (`:root`)
```css
--green:#1A3D2B;      /* xanh thương hiệu chính */
--green2:#2E5C40;     /* xanh hover/nhạt hơn */
--green-light:#EBF4EE;/* nền xanh rất nhạt (Notes, icon why) */
--gold:#C9A84C;       /* vàng điểm nhấn — DÙNG HIẾM */
--gold-light:#FBF6E9;
--bg:#F7F3EE;         /* nền kem chủ đạo */
--bg2:#FFFFFF;        /* nền trắng (Listings, Testimonials) */
--text:#1C1C1C;
--muted:#6B6B6B;      /* xám phụ — section label, mô tả */
--border:#E2DBD0;
--radius:10px; --radius-lg:16px;
--shadow:0 2px 16px rgba(26,61,43,.07);
--shadow-lg:0 8px 40px rgba(26,61,43,.13);
--trans:.22s ease;
```

### 4.2. Bảng màu nền theo section (sau tất cả tinh chỉnh)
| Section | Nền | Vai trò |
|---|---|---|
| Hero | gradient xanh đậm `#0D2B1C→#1A3D2B→#2E5C40` | mở màn mạnh, brand |
| Listings | trắng `#FFF` (`--bg2`) | sạch, neo sản phẩm |
| Why | kem `#F7F3EE` (`--bg`) | nhẹ |
| Quy hoạch | kem | bản đồ |
| **Pain** | **xanh `#1A3D2B`** (đổi từ `#0D2B1C`) | neo tối, vừa tầm |
| Testimonials | trắng (`--bg2`, đổi từ `--bg`) | phá chuỗi đơn điệu |
| Quiz | gradient xanh đậm | tương tác |
| Notes | xanh nhạt `#EBF4EE` | editorial |
| Footer | xanh đậm | đóng trang |

### 4.3. Typography
- **Font:** `Plus Jakarta Sans Variable` (geometric, gần Maison Neue của Redfin) từ **jsDelivr CDN**, có `preconnect` hint trên 44 trang. Fallback: system fonts (`-apple-system`, `Segoe UI`...).
- **Heading:** weight 700, `letter-spacing:-0.025em`.
- **Hero title:** `clamp(2.2rem,5vw,3.8rem)`, weight 800, line-height 1.08.
- **`hero-title-secondary`** ("Giúp Bạn", "Về Đất Nam Ban"): font-size `.72em`, weight 400, opacity .7 — chữ phụ nhẹ, để "Ra Quyết Định **Đúng**" (gold) nổi lên.

### 4.4. Spacing
- `.section{padding:64px 0}` (giảm từ 80px) → 44px trên mobile.
- `.container{max-width:1180px; padding:0 24px}`.

---

## 5. KIẾN TRÚC KỸ THUẬT

### 5.1. Stack
- HTML tĩnh, CSS thường, JS vanilla IIFE (`js/main.js`).
- Không bundler. Vercel serve tĩnh. `vercel.json` cấu hình.

### 5.2. `js/main.js` — các module
1. **Header scroll** — thêm class `.scrolled` khi `scrollY>10`.
2. **Mobile menu** (cũ — hamburger toggle, vẫn còn cho tương thích).
3. **Search tabs** — đổi `form.action` theo tab đất-nền/nhà-bán.
4. **Listing filter** — `.ltab` lọc `.prop-card` theo `data-type`.
5. **QR Code Zalo** — `makeQR()` dùng thư viện QRCode (chỉ chạy ở trang có `#qrcode`, vd lien-he).
6. **Animate on scroll** — `IntersectionObserver` thêm `fadeUp` cho `.prop-card,.why-card,.news-card`. **CÓ FALLBACK 2.5s** (xem 14.3).
7. **RSS loader** — `rss2json` API bypass CORS, nạp tin VnExpress BĐS + Google News "Nam Ban Lâm Đồng".
8. **Contact form** — submit giả lập (hiện "Đã gửi").

### 5.3. JS riêng trong `index.html`
- **Quy hoạch map** — pan/zoom bản đồ SVG (`#qhMapImg`): zoom in/out/reset, wheel zoom, drag chuột + touch. Giữ trong `<script>` cuối trang.
- **Popup (sell-widget)** — trigger hành vi (xem mục 9.1).

---

## 6. NHẬT KÝ QUYẾT ĐỊNH THEO DÒNG THỜI GIAN

### Giai đoạn 0 — Trước phiên này (nền tảng SEO/AEO đã có)
Các commit 2026-06-17 → 06-18 sáng đã dựng: Schema Product+Offer (14 trang), BreadcrumbList (37 trang), FAQPage hub /hoi-dap/ (29 câu), ItemList, og:image + Twitter Card (22 trang), preconnect CDN (44 trang), internal "Đọc thêm" links (14 trang), IndexNow + llms.txt + RSS feed + AI crawler access, đơn giản hóa UX + bỏ social proof giả + tối ưu hiệu năng.

### Giai đoạn 1 — Tái cấu trúc lớn (Level B) — 06-18 chiều
Commit `70e422a` → `14f2854`:
- **Đổi copyright footer TẤT CẢ trang** → "Giúp bạn ra quyết định đúng về đất Nam Ban" (dùng `sed`).
- **Tái sắp xếp section** trang chủ: Hero → Listings → Why → Quy hoạch → Pain → Testimonials → Quiz → Notes → Footer.
- **Polish:** typographic rhythm + color discipline (gold→muted label).
- **Khôi phục Quiz** — ban đầu bị gỡ khỏi hero, chủ hỏi *"Quiz đâu rồi"* → đưa lại thành section độc lập sau Testimonials.
- **Mobile bottom nav** — thay hamburger, 5 mục: Trang chủ · Tìm đất · **Gọi (nút tròn gold nổi giữa)** · Zalo · Menu. + bottom sheet (panel trượt lên). Hỗ trợ `env(safe-area-inset-bottom)` cho iPhone tai thỏ.
- **Bỏ floating Gọi/Zalo** site-wide (Python script qua 45 trang).
- **Hero stats** 4→3 (bỏ "100+ lô"). Fix layout 3 cột (lần 1).

### Giai đoạn 2 — Phiên hiện tại (06-18 tối → 06-19)

**(a) 3 fix cùng lúc** — commit `277c86b`:
- Bug hero stats "vẫn thấy 2 hàng" → **gỡ hẳn `hstat-div`** khỏi HTML, đổi base `.hero-stats` từ `flex+flex-wrap` sang `grid(3,auto)`. (Nguyên nhân gốc: flex-wrap cho phép xuống hàng.)
- **Cắt hero-sub:** bỏ " — để ra quyết định tốt hơn, nhanh hơn, chính xác hơn."
- **Notes redesign:** từ "card giống testimonial" → **editorial** (nền `--green-light`, viền vàng trái 3px, eyebrow nhỏ, tiêu đề lớn).

**(b) Pain ≠ Testimonials** — commit `bf5e0ae`:
> *"3 nỗi lo và khách nói gì giống nhau quá"*
→ Pain section đổi sang **nền xanh đậm `#0D2B1C`, bỏ card box**, các cột ngăn bằng đường kẻ mỏng, số gold mờ to, chữ trắng. Xóa CSS chết `.pain-card--cta`, `.pain-cta-inner`.

**(c) Kiểm thử toàn diện lần 1** — commit `e3db856`:
> *"Check lại tất cả xem trải nghiệm web tốt nhất chưa"*
Dùng **Playwright** screenshot desktop (1280) + mobile (iPhone 390). Phát hiện & sửa:
- Hero mobile có **dead space** (do `min-height:100vh`) → `min-height:auto` + padding gọn.
- Why cards xuống 1 cột ở 480px (4 card = 4 màn) → giữ **2 cột**.
- Why card padding 28→22px, icon 48→40px.
- Kết quả: chiều cao trang mobile **8110px → 7852px**.

**(d) Audit code** — commit `c0fb33c`:
> *"Check kỹ lại tất cả, kiểm tra code có chồng chéo nhau ko, web mượt nhất chưa, ảnh và cách cái dư thừa bỏ chưa"*
Dùng sub-agent Explore quét. Sửa:
- Xóa **`.float-btns` CSS** (9 rule chết, element đã gỡ).
- Xóa **`#backTop` JS** (5 dòng, không có element khớp).
- **Chuyển `<style>` block** (quy hoạch map) từ trong `<body>` → `style.css`.
- Xóa `style="display:block"` thừa trên 2 logo img (rule `img{}` global đã lo).
- *Lưu ý còn lại:* `/images/nam-ban-aerial.jpg` không tồn tại (hero dùng gradient thay, nhưng vẫn có 1 request 404).

**(e) Sửa copy hero** — commit `e5f0605`:
> "Chúng tôi giúp bạn hiểu rõ những gì đang thực sự diễn ra ở Nam Ban." → **"Chúng tôi sẽ giúp bạn hiểu rõ những giao dịch đang diễn ra ở Nam Ban."**

**(f) Popup tâm lý học** — commit `aac9fb4`:
Thảo luận nghiên cứu UX timing (xem mục 9.1). Chủ chốt:
> *"kết hợp cả 2, popup chỉ nhảy ra 1 lần, ko làm nhiều lần như page rác"*
→ Trigger **scroll 60% HOẶC exit-intent** (cái nào trước), **hiện 1 lần** qua `localStorage`. Thay `setTimeout 30s` cũ.

**(g) SĐT + màu Pain + icon Zalo** — commit `22f5876`:
> *"check lại phần số điện thoại, có hiện ra nhiều và chồng chéo... 3 nỗi lo... có nên đổi màu khác, thấy hơi nặng ko? ... menu ở cuối trên phone... icon zalo nên đổi cái khác cho đúng hơn ko"*
- SĐT: xác nhận **không chồng chéo** (mô hình 1+1).
- Pain `#0D2B1C` → **`#1A3D2B`** (nhẹ hơn, bớt nặng).
- Zalo icon: chat-bubble generic → **chữ "Z" trong ô bo góc** (nhận diện đúng Zalo).

**(h) Tone màu & độ trong** — commit `e105fb3`:
> *"Xem cách tone màu ok hết chưa / Độ trong của web ok chưa"*
Screenshot lại 16 ảnh (8 desktop + 8 mobile). Sửa:
- Nút "Check Quy Hoạch" `#0068FF` (xanh dương lạc tông) → **`var(--green)`**.
- Thêm **fallback opacity 2.5s** cho card animation (chống card vô hình nếu observer chậm).
- Testimonials nền `--bg` → **`--bg2`** (trắng) phá chuỗi 4 section đơn điệu.

---

## 7. PHÂN TÍCH TỪNG SECTION TRANG CHỦ

### 7.1. Hero
- Cấu trúc: eyebrow ("Nam Ban · Lâm Hà · Lâm Đồng") → H1 → sub → search box → 3 stats.
- H1: `<span secondary>Giúp Bạn</span> Ra Quyết Định <em>Đúng</em> <span secondary>Về Đất Nam Ban</span>` — "Đúng" gold, phần phụ nhẹ.
- 3 stats: **25'** (từ Đà Lạt) · **100%** (sổ đỏ) · **0đ** (check quy hoạch). Grid 3 cột cứng — không bao giờ xuống 2 hàng.
- Đã bỏ: rotating quote (`recoLine`), mini survey, `min-height:100vh` trên mobile.

### 7.2. Listings (neo)
- Tabs lọc: Tất cả / Đất Nền / Nhà Bán.
- Card: ảnh 3:2, badge (Nổi Bật/Đất Nền/Nhà Bán), giá đậm, diện tích pill, tags, nút "Hỏi về lô này".
- Tiêu đề được "đối xử nặng" nhất (weight 800).

### 7.3. Why (Tại sao chọn Nam Ban)
- "Vùng Đất Vàng Ngay Cạnh Đà Lạt" — 4 card: Vị trí chiến lược · Tiềm năng tăng giá · Pháp lý rõ ràng · Khí hậu lý tưởng.
- Icon trong ô bo góc nền `--green-light`. Mobile 2 cột.

### 7.4. Quy hoạch
- Bản đồ SVG pan/zoom tương tác. CTA "Check Quy Hoạch Miễn Phí" (đã đổi xanh lá).
- Bỏ label gold, subtitle gọn ("Xã Nam Ban – Huyện Lâm Hà").

### 7.5. Pain (3 Nỗi Lo)
- "3 Nỗi Lo Phổ Biến Trước Khi Mua Đất Nam Ban" (eyebrow: "Người mua từ xa thường gặp").
- 3 nỗi lo nhắm khách TP.HCM ở xa:
  1. **Không biết tin ai** → "Chúng tôi không bán tất cả những gì có. Mỗi lô qua bộ lọc..."
  2. **Không có thời gian khảo sát** → "Chúng tôi khảo sát thay: ảnh, video, check quy hoạch, đo đạc, phỏng vấn hàng xóm, kiểm tra lũ lụt/điện nước..."
  3. **Sợ mua sai pháp lý** → "100% sổ đỏ riêng, kiểm tra tranh chấp/quy hoạch, có thể yêu cầu bản sao sổ tra cứu độc lập trước cọc."
- Mỗi nỗi lo có CTA riêng (Liên hệ / Zalo / Xem lô).
- Nền xanh `#1A3D2B`, số gold mờ, không box.
- *Sửa lỗi:* trước là "5 Nỗi Lo" nhưng chỉ 3 card đánh số 01/03/04 → sửa thành 3 + 01/02/03.

### 7.6. Testimonials (Khách nói gì)
- "Tin Tưởng Được Xây Dựng Từ Thực Tế" — 3 review: Anh Minh Tuấn (KS Đà Lạt, đất 336m²) · Chị Thu Hằng (DN TP.HCM, villa) · Anh Việt Anh (NĐT Bình Dương, đất 259m²).
- Style nhẹ: nền trắng, viền trái 2px, avatar chữ cái, sao gold nhỏ. **Bỏ dấu nháy lớn** (`.testi-quote{display:none}`).

### 7.7. Quiz (Mục đích)
- "Bạn đang nghĩ đến Nam Ban với mục đích gì?" — 4 lựa chọn: Xây nhà nghỉ dưỡng · Đầu tư chờ tăng giá · Định cư · Đang tìm hiểu.
- Nền xanh đậm, phân luồng khách theo intent.

### 7.8. Notes (Namban Notes)
- 1 bài editorial nổi bật: "Buổi Sáng Trên Đồi Cà Phê — Và Người Đàn Ông Quyết Định Không Mua".
- Style editorial: nền xanh nhạt, viền vàng trái, eyebrow "✦ Namban Notes", meta "Tháng 5 · 2026 · Góc nhìn thực địa", nút "Đọc câu chuyện →".

### 7.9. Footer
- Logo + địa chỉ + Kết nối (SĐT gold + Zalo) + cột links (BĐS / Thông tin) + copyright slogan.

---

## 8. CHIẾN LƯỢC MOBILE UX

### 8.1. Bottom Navigation (thanh điều hướng đáy)
- `position:fixed; bottom:0`, z-index 1000, 5 mục đều nhau.
- Mục giữa **"Gọi ngay"** = nút **tròn gold nổi lên** (`margin-top:-22px`, 52px) — điểm nhấn hành động chính, đúng tâm thumb zone.
- Icon: Trang chủ (nhà) · Tìm đất (kính lúp) · Gọi (điện thoại, nền gold) · Zalo (**chữ Z bo góc**) · Menu (3 gạch).
- `body{padding-bottom:64px}` chừa chỗ, không che nội dung cuối.
- Trên mobile ẩn: `.nav`, `.menu-btn`, `.hotline-btn` (header) — tránh trùng lặp.

### 8.2. Bottom Sheet (panel menu trượt)
- `transform:translateY(100%)` → trượt lên khi mở. Overlay mờ. Handle bar trên cùng.
- Mở từ nút "Menu", chứa full menu điều hướng.

### 8.3. Responsive breakpoints
- `768px` — chuyển mobile: bottom nav hiện, header nav ẩn, search form dọc, prop-grid 1 cột, why-grid 2 cột.
- `480px` — hero `min-height:auto`, why-grid vẫn 2 cột, hero-stats vẫn 3 cột.

---

## 9. TÂM LÝ HỌC ỨNG DỤNG

### 9.1. Popup timing — nghiên cứu & quyết định
**Tổng hợp nghiên cứu UX (Sumo, HubSpot, OptinMonster, Nielsen Norman Group):**
| Thời điểm | Hiệu quả |
|---|---|
| < 5s | Tệ nhất — chưa đọc gì, bounce tăng |
| 15–30s | Phổ biến nhưng vẫn cắt ngang flow |
| 60s | Tốt cho nội dung dài |
| **Exit intent** | Conversion cao nhất (~3–5x time-based) |
| **Scroll 50–70%** | Cao — người đã quan tâm thật |

**Lý do chọn hành vi thay vì thời gian cho BĐS:** Khách BĐS đọc kỹ, cân nhắc lâu, không mua impulsive. Đếm giây bỏ qua mức engagement thật (người đọc nhanh 20s xong vs người đọc 2 phút). Trigger hành vi đo đúng "đang quan tâm".

**Quyết định cuối:** `scroll ≥60% HOẶC exit-intent (mouseleave top, chỉ desktop)`, cái nào trước thắng. **`localStorage` (không phải `sessionStorage`)** → đóng trình duyệt mở lại tuần sau vẫn không hiện. Đóng popup = hết vĩnh viễn. → Không phải "page rác".

### 9.2. Định vị trung thực (honesty positioning)
- Bài Notes flagship kể chuyện người đàn ông **quyết định KHÔNG mua** — phản trực giác với site bán đất, nhưng xây niềm tin.
- Pain copy: "Chúng tôi không bán tất cả những gì chúng tôi có" — thừa nhận lọc hàng.
- Bỏ social proof giả (commit `107a6ba` giai đoạn trước) — chỉ giữ review thật.

### 9.3. Giảm ma sát quyết định
- Stats hero là 3 nỗi lo lớn nhất được trả lời sẵn: khoảng cách (25'), pháp lý (100% sổ), chi phí kiểm tra (0đ).
- Quiz phân luồng theo intent → dẫn khách đến đúng nội dung họ cần.
- "Khảo sát thay" — gỡ rào cản lớn nhất của khách ở xa.

### 9.4. Ergonomics = tâm lý
Thumb zone không chỉ tiện tay mà giảm "tải nhận thức" — hành động chính (gọi) ở nơi dễ với nhất, không bắt người dùng nghĩ.

---

## 10. QUY TRÌNH KIỂM THỬ (QA)

**Công cụ:** Playwright (chromium headless, `--no-sandbox`) qua Node, phục vụ site bằng `python3 -m http.server`.

**Phương pháp:**
1. Render desktop 1280×900 (deviceScaleFactor 2) + mobile iPhone 390×844 (DSF 3, UA iPhone).
2. Screenshot từng mốc scroll (0, 900, 1800... px) → quan sát từng section thật.
3. Full-page screenshot đo chiều cao trang (phát hiện dead space).
4. Clip vùng cụ thể (vd bottom nav y=760–844) soi chi tiết.
5. So sánh trước/sau mỗi fix.

**Phát hiện nhờ QA (không thấy nếu chỉ đọc code):**
- Dead space hero mobile.
- Why card mờ (opacity animation chưa fire).
- Tone xanh dương lạc của nút Quy hoạch.
- 4 section sáng liên tiếp đơn điệu.

---

## 11. DỌN DẸP CODE & NỢ KỸ THUẬT

| Mục | Trạng thái | Chi tiết |
|---|---|---|
| `.float-btns` CSS (9 rule) | ✅ Xóa | Element đã gỡ, CSS thành chết |
| `.float-btns{display:none}` mobile | ✅ Xóa | |
| `#backTop` JS (5 dòng) | ✅ Xóa | Không có element `#backTop` nào |
| `<style>` block trong `<body>` | ✅ Chuyển vào style.css | Quy hoạch map styles |
| `style="display:block"` ×2 logo | ✅ Xóa | Rule `img{}` global đã có |
| `.pain-card--cta`, `.pain-cta-inner` | ✅ Xóa | Card CTA đã gỡ khỏi HTML |
| `hstat-div` separators | ✅ Xóa khỏi HTML | Gây bug 2 hàng |
| `.manifesto-wrap`, `.hero-survey`, `.footer-tagline` | ✅ Đã xóa (gđ trước) | |
| `/images/nam-ban-aerial.jpg` 404 | ⚠️ Còn | Hero dùng gradient; nếu có ảnh aerial thì đặt vào hết 404 |
| `sessionStorage 'sellWidgetClosed'` cũ | ✅ Thay bằng localStorage | |

**Kết quả:** giảm ~30+ dòng code chết, gộp inline → stylesheet, không còn selector trỏ vào element không tồn tại.

---

## 12. HỆ THỐNG SEO/AEO (ĐƯỢC BẢO TOÀN — KHÔNG ĐỘNG VÀO)

> Đây là "máy hút khách tự động" chủ dặn giữ nguyên. Liệt kê để biết KHÔNG được phá.

- **Schema.org JSON-LD:** RealEstateAgent (+ PostalAddress, GeoCoordinates), Product+Offer (14 trang lô), FAQPage (hub /hoi-dap/ 29 câu + Question/Answer), BreadcrumbList (37 trang), ItemList/ListItem (trang index dat-nen).
- **Meta:** og:image + dimensions, Twitter Card (22 trang); title ≤70 ký tự.
- **Phân phối tự động cho AI/crawler:**
  - `llms.txt` (5.3KB) — bản đồ nội dung cho LLM.
  - `feed.xml` (RSS, 22KB) — build bằng `scripts/build-feed.mjs`.
  - `robots.txt` — mở cho AI crawler.
  - IndexNow key (`abdd063f...txt`) — ping search engine khi cập nhật.
  - `sitemap.xml` (7.6KB).
- **Internal linking:** block "Đọc thêm" liên kết 14 trang lô.
- **Performance:** preconnect jsDelivr CDN (44 trang).
- **RSS tin tức động:** main.js nạp VnExpress BĐS + Google News Nam Ban (rss2json bypass CORS).

⚠️ **Quy tắc vàng:** mọi thay đổi presentation KHÔNG được chạm JSON-LD, meta, sitemap, feed, robots, llms.txt.

---

## 13. LỊCH SỬ COMMIT CÓ CHÚ GIẢI

```
e105fb3  2026-06-19 04:12  Color/clarity: CTA xanh lá, fallback animation, nhịp section
22f5876  2026-06-19 03:50  Pain nhẹ màu (#1A3D2B), Zalo icon → chữ Z
aac9fb4  2026-06-19 03:42  Popup: scroll 60% + exit intent, 1 lần (localStorage)
e5f0605  2026-06-19 03:37  Sửa copy hero ("những giao dịch đang diễn ra")
c0fb33c  2026-06-19 00:03  Dọn code chết, gộp inline style vào stylesheet
e3db856  2026-06-18 23:36  Mobile: bỏ dead space hero, why 2 cột, padding gọn
bf5e0ae  2026-06-18 22:54  Pain section nền tối, bỏ box (khác testimonials)
277c86b  2026-06-18 22:38  Fix hero stats 3 cột, cắt hero-sub, Notes editorial
14f2854  2026-06-18 15:13  Hero stats 3-up grid mobile (lần 1)
36a196a  2026-06-18 15:11  Bỏ floating call/zalo site-wide
21450d3  2026-06-18 15:08  Mobile bottom nav (thumb-zone) mọi trang
da2ef82  2026-06-18 15:04  Khôi phục quiz thành section riêng
bd4c91d  2026-06-18 15:02  Nhịp typography + kỷ luật màu
ca5fef9  2026-06-18 14:55  Tái sắp xếp section, bỏ rối thị giác
70e422a  2026-06-18 14:34  Làm nhẹ trang chủ, đổi tagline footer mọi trang
─── nền tảng SEO/AEO (trước phiên redesign) ───
a9283b3  2026-06-18 07:04  IndexNow, llms.txt, RSS, AI crawler access
107a6ba  2026-06-18 05:56  Đơn giản UX, bỏ social proof giả, tối ưu perf
9f8c466  ...              Internal "Đọc thêm" 14 trang lô
2dafb82  ...              Preconnect jsDelivr 44 trang
d16efd4  ...              ItemList schema dat-nen
211933c  ...              og:image dims + Twitter Card 22 trang
0fd5fa9  ...              Fix title >70 ký tự + sitemap /hoi-dap/
bf7dad8  ...              Hub /hoi-dap/ FAQPage 29 câu
ffb0043  ...              BreadcrumbList 37 trang
2a600ca  ...              Product+Offer schema 14 trang lô
```

---

## 14. BUG ĐÃ GẶP & NGUYÊN NHÂN GỐC

### 14.1. Hero stats "vẫn thấy 2 hàng" (dai dẳng, sửa 2 lần)
- **Triệu chứng:** 3 số liệu hero hiển thị 2 hàng trên điện thoại dù đã set grid 3 cột ở media query.
- **Nguyên nhân gốc:** base `.hero-stats` dùng `display:flex; flex-wrap:wrap` + có 2 element `.hstat-div` (vạch ngăn) trong HTML. Override grid ở mobile không thắng được vì các `hstat-div` vẫn chiếm chỗ và flex-wrap cho phép xuống hàng.
- **Fix đúng:** GỠ HẲN `.hstat-div` khỏi HTML + đổi base sang `display:grid; grid-template-columns:repeat(3,auto)`. Grid không wrap → luôn 1 hàng.
- **Bài học:** sửa ở media query là chữa ngọn; phải sửa base layout (gốc).

### 14.2. Pain đánh số sai (5 Nỗi Lo / 01,03,04)
- Tiêu đề "5 Nỗi Lo" nhưng chỉ 3 card, đánh số 01/03/04 (lệch).
- Fix: "3 Nỗi Lo Phổ Biến" + 01/02/03.

### 14.3. Card vô hình (opacity stuck)
- **Triệu chứng:** why-card/prop-card đôi khi mờ/trong suốt.
- **Nguyên nhân:** JS set `el.style.opacity='0'` inline rồi chờ IntersectionObserver fire mới animate. Nếu observer chậm/không fire (scroll nhanh, JS lag), card kẹt opacity 0.
- **Fix:** thêm `setTimeout 2500ms` — sau 2.5s element nào còn opacity 0 thì ép về 1. Animation chỉ là enhancement, không phải điều kiện hiển thị.

### 14.4. Section trùng diện mạo
- Pain ↔ Testimonials ↔ Notes đều từng dùng "nền trắng + border + radius" → nhìn giống nhau.
- Fix: mỗi cái 1 ngôn ngữ riêng (Pain tối/không-box, Testimonials trắng/card, Notes xanh-nhạt/viền-trái).

### 14.5. Footer tagline trùng
- `footer-bottom` và `footer-tagline` cùng text → xóa `footer-tagline`.

---

## 15. CÒN LẠI / TODO

- [ ] **GA4 ID thật** — đang placeholder `G-XXXXXXXXXX`, chờ chủ cấp.
- [ ] **`/images/nam-ban-aerial.jpg`** — chưa tồn tại, gây 404 nhẹ. Nếu có ảnh aerial Nam Ban đặt vào → hero có ảnh nền thật thay vì chỉ gradient.
- [ ] **Upload tài liệu này lên Google Drive** folder "Web Nambanvillas" — chờ MCP Google Drive kết nối lại (hiện đang ngắt).
- [ ] Cân nhắc lazy-load thư viện QRCode (chỉ cần ở trang liên hệ).

---

## 16. NGUYÊN TẮC & BÀI HỌC RÚT RA

1. **Sửa gốc, không sửa ngọn.** Bug hero stats: phải đổi base layout, không vá ở media query.
2. **Tài nguyên hiếm mới có giá trị.** Gold dùng tràn lan = vô nghĩa. Hạn chế → nổi bật.
3. **Mỗi section một danh tính.** Trùng diện mạo = người dùng lẫn lộn, mất phân tầng thông tin.
4. **Nhịp sáng-tối cho mắt nghỉ.** Không xếp nhiều section cùng tông liên tiếp.
5. **Hành vi > thời gian** trong việc đo "khách đang quan tâm" (popup).
6. **Hiển thị không được phụ thuộc JS animation.** Luôn có fallback — animation là enhancement.
7. **1 cố định + 1 ngữ cảnh** cho điểm tiếp xúc — không spam liên hệ.
8. **Thumb zone** quyết định vị trí hành động chính trên mobile.
9. **Kiểm thử bằng mắt (screenshot thật)** bắt lỗi mà đọc code không thấy.
10. **Presentation tách khỏi data.** Đổi giao diện không bao giờ chạm SEO/Schema/feed.
11. **Trung thực bán được hàng.** Câu chuyện "không mua" xây niềm tin mạnh hơn lời chào mời.
12. **Code chết phải xóa.** CSS/JS trỏ vào element không tồn tại = nợ kỹ thuật, gây nhầm lẫn về sau.

---

## 17. PHỤ LỤC: ĐỐI THOẠI NGUYÊN VĂN (các câu chỉ đạo của chủ)

Sắp theo thứ tự, giữ nguyên văn — đây là "ý chí thiết kế" gốc:

1. *"chú phát hiện trang chủ đang quá dày chữ, và nhiều khoảng trống ko cần thiết, cháu nghiên cứu thiết kế lại cho phù hợp, vừa đủ sang, vừa đủ ko quá trống."*
2. *"Có giữ nguyên nội dung ko, có ảnh những tới các kỹ thuật content, seo, aeo, các kỹ thuật khác để tạo phễu và hút khách, tự động huý khách như từng làm ở trên ko"*
3. *"Làm B trước"*
4. *"Quiz đâu rồi"*
5. *"Thanh menu trên điện thoại để ở giữa phía trên 2 ngón đều khó thao tác / Nên thiết kế tối ưu mọi thứ trải nghiệm trên điện thoại"*
6. *"Mấy cái liên quan tới liên hệ, đặt lịch, nút gọi, zalo, số điện thoại khi vào trong các bài và nhất là sản phẩm quá nhiều / Cháu xem có nên hoặc tinh gọn thế nào cho gọn nhẹ, đỡ rối mắt nhất ko"*
7. *"25' / Từ trung tâm Đà Lạt / 100% / Sổ đỏ lâu dài / 0đ / Check quy hoạch miễn phí / Dàn trên phone chưa gọn"*
8. *"Vẫn thấy 2 hàng / Bỏ câu '— để ra quyết định tốt hơn, nhanh hơn, chính xác hơn.' / Phần nban note giống 1 ô nhỏ trong khach hàng nói gì quá"*
9. *"3 nỗi lo và khach noi gi giong nhau qua"*
10. *"Check lại tất cả xem trải nghiệm web tốt nhất chưa"*
11. *"Check kỹ lại tất cả, kiểm tra code có chồng chéo nhau ko, web mượt nhất chưa, ảnh và cách cái dư thừa bỏ chưa"*
12. *"TRANG CHỦ ... đổi thành 'Chúng tôi sẽ giúp bạn hiểu rõ những giao dịch đang diễn ra ở Nam Ban'"*
13. *"popup dựa trên tất các những dữ liệu nghiên cứu về tâm lý dùng web, bao nhiêu lâu thì hiện lên là tối ưu nhất"*
14. *"kết hợp cả 2, popup chỉ nhảy ra 1 lần, ko làm nhiều lần như page rác"*
15. *"check lại phần số điện thoại... 3 nỗi lo... đổi màu khác, thấy hơi nặng ko? ... menu ở cuối trên phone... icon zalo nên đổi cái khác cho đúng hơn ko"*
16. *"Xem cách tone màu ok hết chưa / Độ trong của web ok chưa"*

---

*Hết bản ghi tổng. Tài liệu này phản ánh trạng thái repo tại commit `e105fb3` (2026-06-19).*
