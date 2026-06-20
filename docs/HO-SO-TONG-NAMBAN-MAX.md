# HỒ SƠ TỔNG — DỰ ÁN NAM BAN (PANORAMA METHOD + NAM BAN VILLAS)
## BẢN MAX v3 — Dùng để dời sang project mới với 100% ngữ cảnh
*Cập nhật: 19/6/2026 · Tác giả: Claude Code · Dự án: nambanvillas.vn + nambanpanorama.com*

---

> **CÁCH ĐỌC TÀI LIỆU NÀY**
> Đây là hồ sơ "nguồn sự thật" (source of truth) để bất kỳ AI hoặc người nào mở
> project mới đều tái lập được TOÀN BỘ tư duy, chiến lược, kỹ thuật, tâm lý và
> code của dự án — không cần đọc lại ~1 triệu từ trao đổi gốc.
>
> Tài liệu gồm **3 lớp**:
> 1. **Lớp chiến lược** — PANORAMA METHOD (triết lý, định vị, phễu, tâm lý).
> 2. **Lớp sản phẩm** — Nam Ban Villas (site thực tế đang chạy, code đầy đủ).
> 3. **Lớp lịch sử** — mọi quyết định, đối thoại, lỗi đã gặp & cách sửa.
>
> Phần cuối (PHỤ LỤC CODE) chứa **nguyên văn 3 file lõi** (index.html,
> style.css, main.js) để khôi phục 100% kể cả khi mất GitHub.

---

# PHẦN 0 — BẢN ĐỒ TỔNG THỂ: HAI THƯƠNG HIỆU, MỘT HỆ SINH THÁI

Dự án không phải một website đơn lẻ. Nó là một **hệ sinh thái hai tầng** theo
đúng kiến trúc **Parent / Product** (Apple → iPhone) mà chính Playbook mô tả ở
mục 2.5:

| | **NAMBAN PANORAMA** (Parent) | **NAM BAN VILLAS** (Product) |
|---|---|---|
| Vai trò | Thương hiệu mẹ — trí tuệ, trust, độ rộng | Site sản phẩm — tin đăng, chuyển đổi |
| Domain | nambanpanorama.com | nambanvillas.vn (đang chạy live) |
| Tinh thần | "Im lặng mà sang", đọc rủi ro | Redfin-style, rõ ràng, thực dụng |
| Font | Fraunces + Be Vietnam Pro | Plus Jakarta Sans Variable |
| Màu | Kem + đất nung (--clay #9d5d38) | Kem + xanh rừng (--green #1A3D2B) + vàng (--gold) |
| Mục tiêu | Mental Availability, phễu nguội | Lọc + đẩy khách tới cuộc gặp/Zalo |
| Tài sản | PANORAMA METHOD (15 tài liệu) | 46 trang HTML, 14 tin đăng thật |

**Điểm nối quan trọng nhất:** mục **Namban Notes** trên site Nam Ban Villas
chính là hiện thân của triết lý Panorama (phễu 4 tầng "đọc rủi ro"). Đây là cây
cầu giữa hai brand — phần "sang" của Panorama sống ngay trong site thực dụng.

> **Lưu ý lịch sử/định danh:** Trong các tài liệu Playbook, dự án được gọi là
> "Namban Panorama" (nambanpanorama.com). Site đang vận hành thực tế lại mang
> tên "Nam Ban Villas" (nambanvillas.vn). Hai tên này là **hai lớp của cùng một
> dự án** — Panorama là phương pháp/định vị, Villas là sản phẩm bán hàng. Khi
> sang project mới, giữ rõ sự phân tầng này.

---

# PHẦN 1 — PANORAMA METHOD (LỚP CHIẾN LƯỢC)

> Đây là phần GIÁ TRỊ NHẤT. Toàn bộ phương pháp được chắt từ ~1 triệu từ trao
> đổi, 10+ phiên, hàng trăm quyết định. Bộ kit gốc gồm **15 tài liệu** (file
> 00–14, hiện nằm trong repo dưới dạng .docx). Phần dưới tóm lược ĐẦY ĐỦ tinh
> thần để dùng ngay; bản nguyên văn chi tiết nằm trong các .docx tương ứng.

## 1.1. Triết lý một dòng
**Website không phải để đẹp — nó là CÔNG CỤ đạt mục tiêu kinh doanh. Thắng bằng
CHẤT LƯỢNG NIỀM TIN, không bằng số lượng click. Một người tin thật > 1000 người
lướt qua.**

## 1.2. Mười nguyên tắc của System Prompt (dán đầu mỗi project mới)

**0. Vai trò:** Chuyên gia dựng web chiến lược, không phải thợ code thuần. Biến
mục tiêu kinh doanh thành website-công-cụ. Lo hết kỹ thuật cho chủ web (người
KHÔNG rành kỹ thuật).

**1. Nguyên tắc tối thượng (bộ lọc mọi quyết định):** Trước khi làm bất cứ gì,
hỏi "Điều này có đưa người dùng tiến gần hơn tới HÀNH ĐỘNG MỤC TIÊU không?" Nếu
không → không làm. Chuyển đổi thật thường KHÔNG xảy ra trên web — web là cỗ máy
**LỌC + NUÔI + ĐẨY** người dùng tới điểm chuyển đổi thật (cuộc gặp, cuộc gọi).

**2. Giai đoạn khám phá (TRƯỚC khi code):** Chốt 6 điều — (1) mục tiêu kinh
doanh thật; (2) Moat (1-2 lợi thế đối thủ không sao chép được); (3) nơi chuyển
đổi thật xảy ra; (4) chân dung khách + các trạng thái tâm lý (phễu); (5) khách
cảnh giác điều gì; (6) giọng/tông + "tics" ngôn ngữ chủ web ghét.

**3. Đặt tên & định vị:** Luật **90/10** — Tên = 10%, định vị = 90%. Chọn tên
"đủ tốt" rồi DỪNG. Tên phải mang **MOAT** (lợi thế địa phương → tên mang địa
danh). **Trust trước Authority** (năm đầu chưa có vị thế → "tôi cho bạn thấy sự
thật, kể cả mặt xấu" mạnh hơn "tôi biết nhiều hơn bạn"). Định vị "người nói
thật, kể cả bất lợi cho mình — dám nói đừng mua".

**4. Kiến trúc nội dung & phễu:** Chiếm CẢ HAI đầu phễu — đầu nóng (đã có nhu
cầu, ít người) + đầu nguội (chưa nghĩ tới sản phẩm nhưng có "nỗi đau" dẫn tới —
RỘNG nhất). Phễu 4 tầng: **Tò mò → Thích → Tự soi → Người thật.** Bậc thang cam
kết: đọc → quiz → nhận tài liệu (để lại liên lạc) → cập nhật định kỳ → gặp.
KHÔNG nhảy thẳng từ "đọc" sang "gọi điện". "Không bán" ở đúng chỗ người ta mong
bị bán.

**5. SEO/AEO:** Mục tiêu thật = **Mental Availability** (khi ai nghĩ tới chủ đề
X, đầu họ bật lên brand này). **Entry Point Compression** — một câu mở "ngã tư"
chạm nhiều kiểu người cùng lúc ("1 câu tốt = 20 keyword"). Nghĩ theo **TRẠNG
THÁI TÂM LÝ** người tìm kiếm, không theo keyword (người ta search "40 tuổi muốn
bỏ phố", "kiệt sức vì Sài Gòn" — không search "Nam Ban"). **Hub Page + FAQPage
schema.** "Tên đẹp cho người, từ khóa cho máy".

**6. UX/UI "im lặng mà sang":** Chuẩn tham khảo Aesop, The Row, Stratechery,
Monocle, Kinfolk, Bloomberg. Sang nằm ở **khoảng trắng và tiết chế**. Nguyên
tắc vàng: **"Không lộ sự cố gắng."** Một bảng màu hạn chế (tông trầm/đất) + một
màu nhấn duy nhất. Tối đa 2 font (serif cá tính + sans dễ đọc). KHÔNG emoji. Số
thứ tự kiểu tạp chí (01, 02). Menu mobile = side-panel mờ kính che KÍN.

**7. Tâm lý & Trust:** Định vị **"đọc rủi ro", không bán giấc mơ.** Phán đoán
hiện tại (kiểm chứng ngay) khác dự đoán tương lai (dễ sai). Lead magnet. **Drip
ngụy trang tận tâm** (cập nhật định kỳ = cớ chạm lại danh sách). **Phân phối
1-1 mạnh hơn 1-nhiều.** "Danh thiếp trí tuệ" (một bài sắc nhất để gửi).

**8. Quy trình kỹ thuật & deploy:** Local → GitHub (Contents API) → Vercel
(auto-build) → domain (1 A record). **[CẤM] KHÔNG dùng regex DOTALL `.*?`** để
xóa/sửa khối HTML/CSS (ăn lan, xóa nhầm hàng nghìn ký tự). Dùng str_replace
khớp CHÍNH XÁC, DUY NHẤT. **VERIFY sau MỖI thay đổi** (cân bằng thẻ, node
--check, json.loads, grep nội dung). Git là lưới an toàn.

**9. Phong cách làm việc với chủ web:** Chủ web thao tác ÍT NHẤT. ĐỀ XUẤT → DUYỆT
→ rồi mới LÀM. KHÔNG bịa chi tiết/nhân vật (bịa = mất moat). Nói THẲNG, dám phản
biện, số thật.

**10. Dữ liệu & độ chính xác:** Định vị trung thực → MỌI con số/ngày/dữ kiện đúng
tuyệt đối. Bản đồ/sơ đồ "nhìn là biết đúng/sai" — sai vị trí = mất uy tín tức
thì; không chắc 100% thì vẽ trừu tượng hơn.

## 1.3. Các mô-típ ngôn ngữ BỊ CẤM (chủ web cực ghét)
- "Người ta thường nói X... nhưng thực ra Y" (thông thái rởm).
- "Không phải X mà là Y" lặp lại.
- Tỏ vẻ khẳng định bản thân, "cố giới thiệu nhiều".
- Tính từ rỗng: "tuyệt đẹp", "lý tưởng", "đáng mơ ước".
→ Viết THẲNG, số thật, dám mất khách.

## 1.4. Saga đặt tên (6 vòng — minh họa luật 90/10)
"Namban Society" (bỏ — game 10 năm) → "Namban Intelligence" (bỏ — "tình báo"
lạnh, đòi authority chưa có) → "Namban Notes/Compass" (khiêm tốn) → **"Namban
Panorama"** (rộng, hợp DNA nhìn-toàn-cảnh). Chốt Panorama làm thương hiệu mẹ,
đóng đinh định vị "toàn cảnh = cả cơ hội LẪN rủi ro". "Intelligence" tụt xuống
thành lớp Advisory trả phí (cửa sau). **Bài học: tốn 6 vòng cho 10% (cái tên),
trong khi 90% (nội dung đầu tiên) chưa nhúc nhích.**

## 1.5. Các nhánh ĐÃ THỬ rồi BỎ (vàng cho project khác)
- Diễn đàn/cộng đồng mở ngay từ đầu → bỏ (sân khấu trống/spam). Cộng đồng phải
  mọc TRÊN thứ đã có người đọc.
- Tự code profile + feed + reputation → bỏ (một người không kham nổi).
- Netlify → chọn GitHub+Vercel (token trong context = tự động hoàn toàn).
- Tạo 200-500 URL/landing cho từng từ khóa → DỨT KHOÁT từ chối (doorway pages,
  Google phạt cả site). Thay bằng Entry Point Compression + Hub.
- Quiz dài 16 kết quả 80-120 chữ → rút còn 4-6 câu (quiz là cánh cửa, không phải
  đích).

## 1.6. Bốn insight phân phối sâu (Thư viện nguyên văn)
- **Shadow Distribution:** Người trung gian (môi giới, banker) là kênh phân phối
  mạnh nhất. Thiết kế web để họ DÁM gửi cho khách (gỡ rủi ro mất mặt).
- **Người đọc rủi ro hiện tại** (không phải nhà tiên tri tương lai): xây uy tín
  bằng giúp TRÁNH sai lầm (kiểm chứng ngay), không hứa TRÚNG cơ hội. Slogan mẫu:
  *"Đôi khi quyết định đúng là không mua gì cả."*
- **"Viên gạch thật"** (chống phân tích-để-trì-hoãn): có người ngoài chấm điểm +
  có rủi ro mất mặt thật + kết thúc trong 7 ngày.
- **Thumbnail/OG như "hộp quà":** tiêu chuẩn nghiệm thu — *"Một banker có dám gửi
  thẻ này cho khách VIP không?"*

## 1.7. Bốn bài phễu cốt lõi + giọng văn mẫu
- **Tầng 1 (Tò mò):** "Một ngày ở X" / "X có gì" — mở bằng quan sát cụ thể, kết
  lọc đúng người.
- **Tầng 2 (Thích):** "X có đáng sống/mua không".
- **Tầng 3 (Tự soi):** "Không phải ai cũng hợp với X" — đặt người đọc tự đánh giá.
- **Tầng 4 (Người thật):** chân dung một người thật (PHẢI thật, chủ web cấp).
- **Bài "danh thiếp":** "[N] sai lầm khiến người [nhóm] mất tiền ở [lĩnh vực]".

Giọng văn Panorama: mở bằng quan sát cụ thể không bằng quảng cáo; thẳng thắn
tiết kiệm thời gian; dám nói nơi này KHÔNG hợp với ai; kết mở không chốt sale;
câu ngắn xen câu dài.

---

# PHẦN 2 — NAM BAN VILLAS (LỚP SẢN PHẨM — SITE ĐANG CHẠY)

## 2.1. Hồ sơ kỹ thuật
- **Stack:** Static HTML + CSS + Vanilla JS. Không framework, không bundler, không build step.
- **Hosting:** Vercel (auto-deploy từ GitHub `main`).
- **Repo:** github.com/doanquocduyet/nambanvillas
- **Domain:** nambanvillas.vn (đăng ký Pa Vietnam) — A record 76.76.21.21 + CNAME www → cname.vercel-dns.com. SSL auto.
- **Font:** Plus Jakarta Sans Variable qua jsDelivr CDN (`@fontsource-variable/plus-jakarta-sans@5`).
- **News:** rss2json.com API (bypass CORS) — VnExpress BĐS + Google News "Nam Ban Lâm Đồng".
- **Branch dev hiện tại:** `claude/dreamy-ritchie-xBezi` (merge vào main = deploy production).

**Tại sao static thuần:** zero build, Vercel serve CDN cực nhanh, SEO hoàn hảo
(HTML render sẵn), không dependency hell, dễ sửa cho người không phải dev, page
speed tốt hơn React (không hydration).

## 2.2. Design tokens (CSS variables) — bản THỰC TẾ đang chạy
```css
:root{
 --green:#1A3D2B; --green2:#2E5C40; --green-light:#EBF4EE;
 --gold:#C9A84C; --gold-light:#FBF6E9;
 --bg:#F7F3EE; --bg2:#FFFFFF;
 --text:#1C1C1C; --muted:#6B6B6B; --border:#E2DBD0;
 --radius:10px; --radius-lg:16px;
 --shadow:0 2px 16px rgba(26,61,43,.07);
 --shadow-lg:0 8px 40px rgba(26,61,43,.13);
 --trans:.22s ease;
 --font:'Plus Jakarta Sans Variable',...;
}
```
> Khác biệt với token Panorama gốc (--clay đất nung): Villas dùng xanh rừng +
> vàng đồng cho hợp ngành BĐS/nghỉ dưỡng, nhưng GIỮ nguyên tắc "1 tông trầm + 1
> nhấn dùng tiết chế".

## 2.3. Thứ tự sections trang chủ (sau redesign "Level B")
**Hero → Listings → Why → Quy hoạch (bản đồ zoom/pan) → 3 Nỗi Lo (Pain) →
Testimonials → Quiz (mục đích) → Namban Notes (editorial) → Footer → Mobile
bottom nav → Mobile sheet → Sell widget (popup).**

Nhịp màu (không 2 section sáng liền kề trừ cặp đã đủ tương phản):
1. Hero — gradient xanh đậm + ảnh aerial
2. Listings — trắng (--bg2)
3. Why — kem (--bg)
4. Quy hoạch — #F0EDE8 (kem xám)
5. Pain — **xanh rừng đậm #1A3D2B** (điểm tương phản tối, "nghỉ mắt")
6. Testimonials — trắng (--bg2) *(đổi từ kem để phá chuỗi đơn điệu)*
7. Quiz — **xanh rừng** (nền tối, vàng nhấn)
8. Namban Notes — xanh nhạt (--green-light), viền vàng trái
9. Footer — #0D2B1C (đậm nhất)

## 2.4. Hero — phân tích từng chữ
- Eyebrow: "Nam Ban · Lâm Hà · Lâm Đồng" (vàng, uppercase, Entity).
- H1: `<span>Giúp Bạn</span> Ra Quyết Định <em>Đúng</em> <span>Về Đất Nam Ban</span>`
  - "Giúp Bạn" (phụ, nhỏ): đặt user làm trung tâm, không phải seller.
  - "Ra Quyết Định Đúng" (chính, vàng "Đúng"): chạm pain "sợ mua sai".
  - "Về Đất Nam Ban" (phụ): specificity, Entity.
- Sub: "Chúng tôi sẽ giúp bạn hiểu rõ những giao dịch đang diễn ra ở Nam Ban."
  *(đổi từ "những gì đang thực sự diễn ra" → "những giao dịch" cụ thể hơn, "sẽ"
  = cam kết hành động.)*
- Search box: 2 tab (Đất Nền / Nhà Bán) + 3 select (Khu vực / Mức giá / Diện tích).
- 3 hero-stats: **25'** Từ trung tâm Đà Lạt · **100%** Sổ đỏ lâu dài · **0đ**
  Check quy hoạch miễn phí. *(Lưu ý tinh tế: `.hstat strong` dùng `font-weight:400`
  + màu vàng — cố ý thanh, không "to đậm market-style".)*

## 2.5. Pain section — "3 Nỗi Lo Phổ Biến" (bản THỰC TẾ)
Nền xanh rừng đậm, 3 cột chỉ ngăn bằng border-left (không hộp card). Số 01/02/03
vàng opacity .35 (trang trí). Nội dung thực tế:
1. **"Không biết tin ai"** → "Chúng tôi không bán tất cả những gì chúng tôi có.
   Mỗi lô đã qua bộ lọc: pháp lý thực, giá thực, hiện trạng thực..." → CTA "Hỏi
   thẳng về lô bạn quan tâm".
2. **"Không có thời gian đi khảo sát — ở tận TP.HCM"** → "Chúng tôi có thể khảo
   sát thay bạn: ảnh, video, check quy hoạch, đo đạc, phỏng vấn hàng xóm..." →
   CTA Zalo "Nhờ khảo sát thay".
3. **"Sợ mua sai — mua xong mới phát hiện vấn đề pháp lý"** → "100% có sổ đỏ
   riêng, đã kiểm tra tranh chấp, quy hoạch... có thể yêu cầu bản sao sổ và tra
   cứu độc lập trước khi cọc." → CTA "Xem các lô đã qua kiểm tra".

> Đây là hiện thân trực tiếp của định vị Panorama "người nói thật, kể cả bất lợi
> cho mình" — "không bán tất cả những gì chúng tôi có".

## 2.6. Quiz "mục đích" (interactive — 4 nhánh)
Câu hỏi: **"Bạn đang nghĩ đến Nam Ban với mục đích gì?"** → 4 lựa chọn, mỗi cái
trả ra 1 đoạn tư vấn + 2 CTA:
- **nghi-duong** (xây nhà nghỉ dưỡng) → "Xem đất phù hợp" + "Hỏi thêm qua Zalo".
- **dau-tu** (chờ tăng giá) → "Xem phân tích thị trường" + "Hỏi thẳng qua Zalo".
- **dinh-cu** (chuyển lên sống) → "Khám phá cuộc sống Nam Ban" + "Cafe ở Nam Ban nhé?".
- **tim-hieu** (chưa rõ) → "Đọc Namban Notes" + "Hay là cafe đi?".

Thiết kế đúng nguyên tắc Panorama 7.5: quiz NGẮN (cánh cửa, không phải đích),
"không cần đăng ký" hạ rào cản, kết gợi tò mò dẫn sang bước sau. Lưu ý: từng bị
bỏ sót khi redesign → user hỏi "Quiz đâu rồi" → thêm lại.

## 2.7. Namban Notes — cây cầu sang Panorama (phễu 4 tầng THẬT)
4 bài editorial đang có, ánh xạ 1-1 với phễu Panorama:
| Bài | URL | Tầng phễu |
|---|---|---|
| Nam Ban Có Gì? Một Buổi Chiều Đủ Để Hiểu | /namban-notes/nam-ban-co-gi/ | **Tầng 1 — Tò mò** |
| Nam Ban Có Đáng Sống Không? Câu Trả Lời Thật | /namban-notes/co-dang-song-o-nam-ban/ | **Tầng 2 — Thích** |
| Không Phải Ai Cũng Hợp Với Nam Ban — Và Đó Là Điều Tốt | /namban-notes/khong-phai-ai-cung-hop/ | **Tầng 3 — Tự soi** |
| Buổi Sáng Trên Đồi Cà Phê — Người Đàn Ông Quyết Định Không Mua | /namban-notes/buoi-sang-tren-doi-ca-phe/ | **Tầng 4 — Người thật** |

Trang chủ chỉ nổi bài Tầng 4 (editorial, viền vàng trái, nền xanh nhạt) — cố ý
khác hẳn card testimonial để không bị nhầm là "ô nhỏ".

## 2.8. Bản đồ quy hoạch (zoom/pan thuần JS)
Ảnh `quy-hoach-nam-ban-2030.svg` trong khung có nút +/−/reset, hỗ trợ wheel zoom
+ kéo (mouse & touch), scale 1–6. CTA "Check Quy Hoạch Miễn Phí" → Zalo (màu
xanh rừng, KHÔNG phải xanh dương off-brand như bản lỗi cũ).

---

# PHẦN 3 — INVENTORY ĐẦY ĐỦ (14 TIN ĐĂNG THẬT)

> Tất cả là tin thật, ảnh thực tế (`/images/listings/<slug>/`), **đã bỏ hết số
> điện thoại chủ đất** — mọi liên hệ funnel qua 0978 758 788 / Zalo.

## 3.1. Đất nền (11 lô) — `/dat-nen/<slug>/`
| Slug | Tiêu đề | Giá | Diện tích | Ảnh |
|---|---|---|---|---|
| dong-thanh-320m2 | Đất Nền Đông Thanh 320–330m², sát khu dân cư, gần Chùa Linh Ẩn | — | 320–330m² | 3 |
| dong-thanh-845m2 | Lô 845m² Đông Thanh "Góc săn mây", view sương mây, MT 12m, tặng thiết kế 50tr | Chưa tới 2 tỷ | 845m² (239 thổ cư) | 3 |
| giap-suoi-2700m2 | Đất 2.700m² 2 mặt giáp suối, bán gấp | 2,95 tỷ | 2.700m² | 4 |
| hai-mat-tien-345m2 | Lô 2 mặt tiền 345m² | 1,15 tỷ | 345m² | 3 |
| ho-bai-cong-lot1 | Đất >700m² giáp Hồ Bãi Công (Lô 1) | 1,95 tỷ | >700m² | 3 |
| ho-bai-cong-lot2 | Đất 950m² giáp Hồ Bãi Công, MT 15m, view đồi thông (Lô 2) | — | 950m² | 3 |
| ho-tu-liem-700m2 | Đất >700m² view Hồ Từ Liêm | 1,2 tỷ | >700m² | 2 |
| me-linh-suoi-thong-650m2 | Đất 650m² view suối thông Mê Linh ven Đà Lạt | 1,25 tỷ | 650m² | 3 |
| pho-thong-villas-130m2 | 2 lô 130m² sát Phố Thông Villas | 568 triệu/lô | 130m²/lô | 1 |
| sieu-pham-3700m2 | Siêu phẩm 3.700m² MT 61m, phù hợp phân lô/homestay | — | 3.700m² | 1 |
| thung-lung-530m2 | Đất 530m² view thung lũng sương mờ, gần Thác Voi | 899 triệu | 530m² | 2 |

## 3.2. Nhà bán (3) — `/nha-ban/<slug>/`
| Slug | Tiêu đề | Giá | Diện tích |
|---|---|---|---|
| hill-house-village | Hill House Village — nhà nghỉ dưỡng 2PN, quản gia 2 năm, gần Chùa Linh Ẩn | 2,6 tỷ | 203m² |
| nha-vuon-1018m2 | Nhà vườn 1.018m², 3PN, hồ cá Koi, view đẹp | 3,8 tỷ | 1.018m² |
| villa-mini-me-linh | Villa Mini Mê Linh 239m², 3PN, sân BBQ | 2,38 tỷ | 239m² |

## 3.3. Thị trường (13 bài — copy nội dung đầy đủ, KHÔNG dẫn link)
bang-gia-dat-lam-dong-2026 · bds-quy-1-2026 · dat-nam-ban-tang-gia-2025 ·
kham-pha-vuon-thao-moc-nam-ban-villas · khi-hau-cuoc-song-nam-ban ·
lam-dong-quy-hoach-dieu-chinh-2026 · mua-dat-nam-ban-kinh-nghiem-2025 ·
nghi-duong-retreat-cao-nguyen-lam-dong ·
nhung-thay-doi-quan-trong-quy-hoach-lam-dong-2025 ·
quy-hoach-tinh-lam-dong-dieu-chinh-2025 ·
san-bay-lien-khuong-mo-rong-anh-huong-nam-ban · thi-truong-gia-tri-thuc-2026 ·
tuyen-tranh-nam-ban-khi-nao-hoan-thanh.

## 3.4. Về Nam Ban (5 bài)
dau-gia-dat-nam-ban-2026 · du-lich-canh-nong-lam-dong ·
nhung-thay-doi-quan-trong-nam-ban-2026 · tiem-nang-dau-tu-nam-ban ·
xa-nam-ban-sap-nhap.

## 3.5. Trang tĩnh
/lien-he/ · /hoi-dap/ (FAQPage schema) · /ve-nam-ban/ (hub) · /thi-truong/ (hub)
· /dat-nen/ · /nha-ban/ · /namban-notes/.

## 3.6. Dữ liệu địa lý THẬT (phải đúng tuyệt đối — nền của trust)
- Nam Ban – Đà Lạt: ~27km qua đèo Tà Nung (hero ghi "25 phút").
- Nam Ban – sân bay Liên Khương: ~22km / "25 phút".
- Đặc sản: cà phê Yellow Bourbon, dâu tằm tơ lụa.
- Khí hậu: 19–22°C quanh năm.
- Schema geo: lat 11.7586, long 108.2432; openingHours Mo-Su 07:00-21:00.
- Hotline: 0978 758 788 (+84978758788). Zalo: zalo.me/0978758788.

---

# PHẦN 4 — LỚP SEO/AEO ĐÃ TRIỂN KHAI

- **Schema.org JSON-LD:** RealEstateAgent (trang chủ), Product+Offer (mỗi
  listing), FAQPage (/hoi-dap/), BreadcrumbList, ItemList.
- **llms.txt** — điều hướng cho AI crawler (ChatGPT/Perplexity/Claude). AEO.
- **IndexNow** — ping search engine khi có nội dung mới (key file + GitHub Action `.github/workflows/indexnow.yml`).
- **RSS feed** `/feed.xml` — tự generate bởi `scripts/build-feed.mjs`.
- **Cập nhật tin tức tự động** — `scripts/update-news.mjs` + GitHub Action
  `.github/workflows/weekly-update.yml` (cập nhật 1 tuần/lần).
- **Meta đầy đủ:** title/description/keywords/canonical/OG/Twitter/geo trên mọi trang.
- **preconnect** jsDelivr CDN. **font-display: swap.**
- **vercel.json** — routing sạch cho các trang con (sửa lỗi 404 listing).
- robots.txt allow all (gồm AI crawlers). sitemap.xml.

---

# PHẦN 5 — LỊCH SỬ DỰ ÁN (SESSION BY SESSION)

## GĐ1 — Build ban đầu (nhiều phiên song song)
Upload 2 docx chiến lược + yêu cầu site BĐS Redfin-style. Dựng skeleton HTML,
CSS từ đầu, hero + search, listings, footer, mobile responsive.
**Trục trặc hạ tầng:** lỡ revoke quyền Claude Code (phải re-authorize GitHub);
Google Drive MCP "Server Turned Down" (lặp nhiều phiên); cấp quyền repo; DNS Pa
Vietnam; Vercel hiện 3 domains (bình thường).

## GĐ2 — Nội dung & tin đăng
"tự tìm ảnh đẹp ở nam ban tự up"; "tự tìm tất cả tin đăng... bỏ hết số điện
thoại"; "tất cả bài viết thị trường... phải copy về... ko phải dẫn link... cập
nhật 1 tuần 1 lần". → Copy toàn bộ content về (giữ user onsite, dwell time,
content ownership), bỏ phone chủ đất, weekly automation.

## GĐ3 — SEO/AEO layer
Schema khắp nơi, IndexNow, llms.txt, RSS, internal linking, preconnect.

## GĐ4 — Lỗi 404 listing + KMZ + favicon + ảnh thật
"phần tin đăng bị lỗi 404" → vercel.json. Upload KMZ quy hoạch → bản đồ
zoom/pan. "load hình thực tế lô đất, ko up hình tự vẽ", "bỏ định vị google map",
"thay logo + favicon".

## GĐ5 — Redesign lớn ("Làm B trước")
"trang chủ quá dày chữ, nhiều khoảng trống ko cần thiết" → đề xuất A (chỉnh
nhẹ) / B (restructure). User chọn **B**. Xác nhận GIỮ NGUYÊN toàn bộ SEO/AEO,
phễu, popup — chỉ đổi visual layout. Pain → dark, no card. Testimonials tách
riêng. Notes → editorial. Mobile → bottom nav. Quiz thêm lại.

## GĐ6 — Tinh chỉnh (phiên gần nhất)
Hero stats 1 hàng (grid fix), bỏ câu thừa, CTA về xanh rừng, popup psychology,
audit số điện thoại, audit màu, dọn code.

---

# PHẦN 6 — TẤT CẢ LỖI ĐÃ GẶP & ROOT CAUSE

1. **Hero stats 2 hàng (gặp 2 lần):** root cause = `.hstat-div` separators +
   flex-wrap. Fix: xóa hết hstat-div khỏi HTML + `display:grid;
   grid-template-columns:repeat(3,auto)` (grid không bao giờ wrap).
2. **404 listing pages:** path không có file → vercel.json rewrite/trailingSlash.
3. **Cards kẹt opacity:0:** IntersectionObserver set opacity:0 inline, không fire
   nếu off-screen. Fix: `setTimeout 2500ms` ép opacity:1 cho card còn ẩn.
4. **Hero mobile dead space:** min-height:100vh tạo khoảng trắng. Fix:
   `min-height:auto` ở 480px.
5. **Why-grid 1 cột ở 480px** → 4 màn hình. Fix: giữ 2-col mọi mobile size.
6. **CTA off-brand blue (#0068FF):** Fix → var(--green).
7. **Pain ≡ Testimonials:** cùng white+card. Fix: Pain → dark green, no box.
8. **Notes ≡ Testimonials:** "ô nhỏ giống khách nói gì". Fix: editorial, viền vàng.
9. **Pain đánh số sai:** "5 Nỗi Lo" nhưng 3 card 01/03/04 → "3 Nỗi Lo" 01/02/03.
10. **Dead CSS:** .float-btns, .pain-card--cta, .hstat-div... đã xóa.
11. **Dead JS:** #backTop (không có DOM). Đã xóa.
12. **Inline `<style>` trong body** (KMZ) → chuyển vào style.css.
13. **[CẤM kinh điển] regex DOTALL `.*?`:** 2 lần mất CSS/nội dung trong dự án
    gốc (mất slogan+quiz; mất ~5000 chars CSS). Khôi phục từ commit sha mốc
    (7c4df129, 0911bb8f). → Sinh ra quy tắc str_replace chính xác + verify.
14. **Form FormSubmit bị antivirus chặn** → Google Form no-cors.
15. **Ảnh aerial 404 do chưa sync** → đẩy lại. Preview tool ≠ web thật.

## TODO còn lại
- **GA4 thật:** thay `G-XXXXXXXXXX` (placeholder ở index.html dòng 62-63).
- **`/images/nam-ban-aerial.jpg`** thiếu (hero vẫn ổn nhờ gradient) → upload ảnh thật.
- **Google Search Console:** verify + submit sitemap.
- **Form → Google Form thật** (hiện contact form chỉ confirm UI giả).
- **Testimonials thật** (hiện là mẫu — đúng tinh thần "không bịa": cần quote thật từ khách).
- **GBP** (Google Business Profile) cho "Nam Ban Villas".

---

# PHẦN 7 — TÂM LÝ POPUP & MOBILE UX

## 7.1. Popup (sell widget) — nghiên cứu & quyết định
Research: exit-intent (mouse rời mép trên) converts > scroll-depth > time-based;
với BĐS thời gian đọc dài nên dùng hành vi (scroll) thay vì thời gian.
**Quyết định cuối (user: "kết hợp cả 2, popup chỉ nhảy 1 lần, ko làm như page
rác"):** trigger = scroll ≥ 60% **HOẶC** exit-intent (cái nào tới trước);
`localStorage 'nbv_popup_seen'` = hiện đúng **1 lần duy nhất trong đời** (không
sessionStorage). Nội dung popup = CTA Zalo "Bạn có câu hỏi về mua/bán đất Nam
Ban? Hỏi thẳng · Trả lời thật".

## 7.2. Mobile UX — bottom nav (thumb zone)
User: "menu trên điện thoại để ở giữa phía trên 2 ngón đều khó thao tác". →
Research thumb zone (Hoober): vùng dễ chạm = 1/3 dưới màn hình; hamburger
top-corner = tệ nhất. **Giải pháp:** bottom nav 5 mục [Trang chủ][Tìm
đất][**GỌI NGAY** (vàng, nhô lên giữa)][Zalo][Menu]. `env(safe-area-inset-bottom)`
cho iPhone notch. Menu = sheet trượt lên từ đáy. Icon Zalo = chữ "Z" trong ô bo
góc. Ẩn hết hotline/hamburger/nav cũ trên mobile; body padding-bottom:64px chừa chỗ.

## 7.3. Tinh gọn điểm liên hệ
Trước: floating buttons + header + mỗi section đều có CTA → rối. Sau: 1 kênh
chính (header desktop / bottom-nav mobile) + 1 kênh ngữ cảnh (Zalo/form). Bỏ
floating buttons, bỏ phone trong listing. Audit xác nhận không chồng chéo.

---

# PHẦN 8 — HƯỚNG DẪN DỜI SANG PROJECT MỚI (QUAN TRỌNG)

Khi mở Claude Project mới cho dự án này:
1. **Dán System Prompt** (PHẦN 1.2 ở trên, hoặc nguyên văn file `01 — SYSTEM
   PROMPT`) vào Custom Instructions.
2. **Đính kèm tài liệu này** + repo `doanquocduyet/nambanvillas` (đã chứa toàn
   bộ code + 18 docx playbook).
3. Nhấn mạnh: GIỮ phân tầng Panorama (parent) / Villas (product); GIỮ định vị
   "đọc rủi ro, không bán giấc mơ"; GIỮ kỷ luật SEO (không doorway pages).
4. **Quy tắc kỹ thuật bắt buộc:** không regex DOTALL; str_replace chính xác;
   verify trước push; static HTML thuần (không đổi sang framework trừ khi cực kỳ
   cần thiết); gold dùng tiết chế; popup chỉ 1 lần (localStorage).
5. Việc cần làm ngay: GA4 ID thật, ảnh aerial, Search Console, Google Form.

**North Star:** khi ai search "đất Nam Ban" trên Google / ChatGPT / Perplexity →
nambanvillas.vn xuất hiện top 3. "Một người tin thật > 1000 người lướt qua."

---

*(Phụ lục CODE — nguyên văn index.html / style.css / main.js — nối ngay sau đây.)*

---

# PHỤ LỤC A — NGUYÊN VĂN index.html (trang chủ, 606 dòng)

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Đất Nền & Nhà Đất Nam Ban – Mua Bán BĐS Nam Ban Villas | Lâm Đồng</title>
  <meta name="description" content="Mua bán đất Nam Ban, nhà đất Nam Ban Lâm Đồng. Đất nền phân lô sổ đỏ lâu dài, biệt thự nghỉ dưỡng view đồi cà phê. Tư vấn miễn phí – Nam Ban Villas.">
  <meta name="keywords" content="nhà đất nam ban, đất nam ban, mua bán đất nam ban, phân lô nam ban, nam ban, đất lâm đồng, biệt thự nam ban, đất nghỉ dưỡng nam ban, đất nền nam ban, bất động sản nam ban, lâm hà lâm đồng">
  <meta name="geo.region" content="VN-LB">
  <meta name="geo.placename" content="Nam Ban, Lâm Hà, Lâm Đồng">
  <link rel="canonical" href="https://nambanvillas.vn/">
  <!-- ===== XÁC MINH GOOGLE SEARCH CONSOLE =====
       Vào search.google.com/search-console → thêm tài sản "nambanvillas.vn"
       → chọn phương thức "Thẻ HTML" → copy đoạn mã → dán meta bên dưới (bỏ chú thích):
       <meta name="google-site-verification" content="DÁN_MÃ_TẠI_ĐÂY">
  -->
  <!-- ===== XÁC MINH BING WEBMASTER (cho ChatGPT/Copilot) =====
       Vào bing.com/webmasters → thêm site → có thể "Import từ Google Search Console".
  -->
  <meta property="og:title" content="Đất Nền & Nhà Đất Nam Ban – Mua Bán BĐS Nam Ban Villas | Lâm Đồng">
  <meta property="og:description" content="Mua bán đất Nam Ban, nhà đất Nam Ban Lâm Đồng. Đất nền phân lô sổ đỏ lâu dài, biệt thự nghỉ dưỡng view đồi cà phê. Tư vấn miễn phí – Nam Ban Villas.">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://nambanvillas.vn/images/listings/dong-thanh-845m2/1.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Đất Nền & Nhà Đất Nam Ban – Mua Bán BĐS Nam Ban Villas | Lâm Đồng">
  <meta name="twitter:description" content="Mua bán đất Nam Ban, nhà đất Nam Ban Lâm Đồng. Đất nền phân lô sổ đỏ lâu dài, biệt thự nghỉ dưỡng view đồi cà phê. Tư vấn miễn phí – Nam Ban Villas.">
  <meta name="twitter:image" content="https://nambanvillas.vn/images/listings/dong-thanh-845m2/1.jpg">
  <meta property="og:url" content="https://nambanvillas.vn/">
  <meta property="og:site_name" content="Nam Ban Villas">
  <link rel="icon" href="images/favicon.png" type="image/png">
  <link rel="alternate" type="application/rss+xml" title="Nam Ban Villas — Tin mới" href="https://nambanvillas.vn/feed.xml">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/plus-jakarta-sans@5/wght.css">
  <link rel="stylesheet" href="css/style.css">
  <script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Nam Ban Villas",
  "description": "Mua bán đất nền Nam Ban, nhà đất Nam Ban Lâm Đồng. Phân lô sổ đỏ, biệt thự nghỉ dưỡng cao nguyên.",
  "url": "https://nambanvillas.vn",
  "telephone": "+84978758788",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Nam Ban",
    "addressRegion": "Lâm Hà, Lâm Đồng",
    "addressCountry": "VN"
  },
  "areaServed": "Nam Ban, Lâm Hà, Lâm Đồng",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "11.7586",
    "longitude": "108.2432"
  },
  "openingHours": "Mo-Su 07:00-21:00",
  "priceRange": "$$"
}
</script>
  <!-- Google Analytics 4 — thay G-XXXXXXXXXX bằng Measurement ID thật của chú -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-XXXXXXXXXX');</script>
</head>
<body>

<!-- HEADER -->
<header class="header" id="header">
  <div class="container header-inner">
    <a href="/" class="logo">
      <img src="/images/logo.png" alt="Nam Ban Villas" width="41" height="52">
      <span class="logo-text">NamBan<strong>Villas</strong></span>
    </a>
    <nav class="nav" id="nav">
      <a href="/dat-nen/" class="nav-link">Đất Nền</a>
      <a href="/nha-ban/" class="nav-link">Nhà Bán</a>
      <a href="/ve-nam-ban/" class="nav-link">Về Nam Ban</a>
      <a href="/thi-truong/" class="nav-link">Thị Trường</a>
      <a href="/lien-he/" class="nav-link">Liên Hệ</a>
    </nav>
    <div class="header-right">
      <a href="tel:0978758788" class="hotline-btn">
        0978 758 788
      </a>
      <button class="menu-btn" id="menuBtn" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<!-- HERO -->
<section class="hero">
  <div class="hero-bg" style="background:linear-gradient(165deg,rgba(10,35,15,0.88) 0%,rgba(18,60,25,0.75) 40%,rgba(12,40,18,0.85) 100%),url('/images/nam-ban-aerial.jpg') center/cover no-repeat;filter:none"></div>
  <div class="container hero-content">
    <p class="hero-eyebrow">Nam Ban · Lâm Hà · Lâm Đồng</p>
    <h1 class="hero-title"><span class="hero-title-secondary">Giúp Bạn</span> Ra Quyết Định <em>Đúng</em> <span class="hero-title-secondary">Về Đất Nam Ban</span></h1>
    <p class="hero-sub">Chúng tôi sẽ giúp bạn hiểu rõ những giao dịch đang diễn ra ở Nam Ban.</p>

    <div class="search-box">
      <div class="search-tabs">
        <button class="stab active" data-tab="dat-nen">Đất Nền</button>
        <button class="stab" data-tab="nha-ban">Nhà Bán</button>
      </div>
      <form class="search-form" action="/dat-nen/" method="get">
        <div class="sf-field">
          <label>Khu vực</label>
          <select name="kv">
            <option value="">Toàn Nam Ban</option>
            <option>TT. Nam Ban</option>
            <option>Nam Hà</option>
          </select>
        </div>
        <div class="sf-field">
          <label>Mức giá</label>
          <select name="gia">
            <option value="">Tất cả</option>
            <option>500tr – 1 tỷ</option>
            <option>1 tỷ – 2 tỷ</option>
            <option>Đất diện tích lớn</option>
          </select>
        </div>
        <div class="sf-field">
          <label>Diện tích</label>
          <select name="dt">
            <option value="">Tất cả</option>
            <option>&lt; 200 m²</option>
            <option>&gt; 200 m²</option>
            <option>&gt; 1000 m²</option>
          </select>
        </div>
        <button type="submit" class="search-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="white" stroke-width="2.5"/><path d="m21 21-4.35-4.35" stroke="white" stroke-width="2.5" stroke-linecap="round"/></svg>
          Tìm kiếm
        </button>
      </form>
    </div>

    <div class="hero-stats">
      <div class="hstat"><strong>25'</strong><span>Từ trung tâm Đà Lạt</span></div>
      <div class="hstat"><strong>100%</strong><span>Sổ đỏ lâu dài</span></div>
      <div class="hstat"><strong>0đ</strong><span>Check quy hoạch miễn phí</span></div>
    </div>
  </div>
</section>

<!-- LISTINGS -->
<section class="section listings" id="listings">
  <div class="container">
    <div class="sec-header">
      <div>
        <p class="sec-label">Đang mở bán</p>
        <h2 class="sec-title">Sản Phẩm Nổi Bật</h2>
      </div>
      <div class="listing-tabs">
        <button class="ltab active" data-type="all">Tất cả</button>
        <button class="ltab" data-type="dat-nen">Đất Nền</button>
        <button class="ltab" data-type="nha-ban">Nhà Bán</button>
      </div>
    </div>

    <div class="prop-grid" id="propGrid">

      <article class="prop-card" data-type="dat-nen">
        <a href="/dat-nen/dong-thanh-845m2/" class="prop-img-wrap">
          <img src="images/listings/dong-thanh-845m2/1.jpg" alt="Lô đất 845m² Đông Thanh Nam Ban view sương mây" width="400" height="260" fetchpriority="high">
          <span class="prop-badge hot">Nổi Bật</span>
        </a>
        <div class="prop-body">
          <div class="prop-top">
            <span class="prop-price">Chưa tới 2 tỷ</span>
            <span class="prop-area">845 m²</span>
          </div>
          <h3 class="prop-title"><a href="/dat-nen/dong-thanh-845m2/">Góc săn mây – Lô 845m² mặt tiền 12m, tặng thiết kế 50 triệu</a></h3>
          <p class="prop-loc"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="2"/></svg>Đông Thanh · Nam Ban · Lâm Hà</p>
          <div class="prop-specs">
            <span>239m² thổ cư</span>
            <span>Cách Đà Lạt 28km</span>
            <span>Sổ hồng riêng</span>
          </div>
          <a href="/dat-nen/dong-thanh-845m2/" class="prop-cta">Hỏi về lô này →</a>
        </div>
      </article>

      <article class="prop-card" data-type="nha-ban">
        <a href="/nha-ban/hill-house-village/" class="prop-img-wrap">
          <img src="images/listings/hill-house-village/1.jpg" alt="Hill House Village nhà nghỉ dưỡng Nam Ban 203m²" width="400" height="260" loading="lazy">
          <span class="prop-badge">Nhà Bán</span>
        </a>
        <div class="prop-body">
          <div class="prop-top">
            <span class="prop-price">2,6 tỷ</span>
            <span class="prop-area">203 m²</span>
          </div>
          <h3 class="prop-title"><a href="/nha-ban/hill-house-village/">Hill House Village – Nhà nghỉ dưỡng 2PN, quản gia 2 năm</a></h3>
          <p class="prop-loc"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="2"/></svg>Nam Ban · Lâm Hà · Lâm Đồng</p>
          <div class="prop-specs">
            <span>2 phòng ngủ</span>
            <span>Gần Chùa Linh Ẩn</span>
            <span>Sổ hồng riêng</span>
          </div>
          <a href="/nha-ban/hill-house-village/" class="prop-cta">Hỏi về căn này →</a>
        </div>
      </article>

      <article class="prop-card" data-type="dat-nen">
        <a href="/dat-nen/thung-lung-530m2/" class="prop-img-wrap">
          <img src="images/listings/thung-lung-530m2/1.jpg" alt="Đất 530m² view thung lũng sương mờ Nam Ban 899 triệu" width="400" height="260" loading="lazy">
          <span class="prop-badge">Đất Nền</span>
        </a>
        <div class="prop-body">
          <div class="prop-top">
            <span class="prop-price">899 triệu</span>
            <span class="prop-area">530 m²</span>
          </div>
          <h3 class="prop-title"><a href="/dat-nen/thung-lung-530m2/">Đất 530m² view thung lũng sương mờ – Gần rừng thông, hồ bãi công</a></h3>
          <p class="prop-loc"><svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="2"/></svg>Gần Thác Voi · Nam Ban · Lâm Hà</p>
          <div class="prop-specs">
            <span>Sổ hồng riêng</span>
            <span>Cách Thác Voi 4km</span>
            <span>Cần bán gấp</span>
          </div>
          <a href="/dat-nen/thung-lung-530m2/" class="prop-cta">Hỏi về lô này →</a>
        </div>
      </article>

    </div>

    <div class="view-all-wrap">
      <a href="/dat-nen/" class="view-all-btn">Xem tất cả sản phẩm</a>
    </div>
  </div>
</section>

<!-- WHY NAM BAN -->
<section class="section why">
  <div class="container">
    <div class="sec-header center">
      <p class="sec-label">Tại sao chọn Nam Ban</p>
      <h2 class="sec-title">Vùng Đất Vàng Ngay Cạnh Đà Lạt</h2>
    </div>
    <div class="why-grid">
      <div class="why-card">
        <div class="why-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="9" r="2.5" stroke="currentColor" stroke-width="2"/></svg>
        </div>
        <h3>Vị trí chiến lược</h3>
        <p>25 phút từ Đà Lạt, 25 phút từ sân bay Liên Khương. Kết nối 3 trục du lịch lớn của vùng Cao Nguyên.</p>
      </div>
      <div class="why-card">
        <div class="why-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><polyline points="22,12 18,12 15,21 9,3 6,12 2,12" stroke="currentColor" stroke-width="2"/></svg>
        </div>
        <h3>Tiềm năng tăng giá</h3>
        <p>Tuyến tránh Nam Ban đang thi công, kỳ vọng giá tăng 30–50% giai đoạn 2025–2027. Đất từ 2022 đã lãi 40–50%.</p>
      </div>
      <div class="why-card">
        <div class="why-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" stroke="currentColor" stroke-width="2"/></svg>
        </div>
        <h3>Pháp lý rõ ràng</h3>
        <p>100% sổ hồng, công chứng ngay. Mỗi lô được kiểm tra tranh chấp, quy hoạch trước khi giới thiệu.</p>
      </div>
      <div class="why-card">
        <div class="why-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="currentColor" stroke-width="2"/><polyline points="9,22 9,12 15,12 15,22" stroke="currentColor" stroke-width="2"/></svg>
        </div>
        <h3>Khí hậu lý tưởng</h3>
        <p>Mát mẻ quanh năm, vẻ đẹp nguyên bản của núi rừng Cao Nguyên – nơi lý tưởng để an cư & nghỉ dưỡng.</p>
      </div>
    </div>
  </div>
</section>

<!-- QUY HOACH MAP -->
<section class="section qh-section" style="background:#F0EDE8">
  <div class="container">
    <div class="sec-header center" style="margin-bottom:24px">
      <h2 class="sec-title">Quy Hoạch Quyền Sử Dụng Đất</h2>
      <p style="font-size:.82rem;color:var(--muted);font-weight:400;margin-top:4px">Xã Nam Ban – Huyện Lâm Hà</p>
    </div>
    <div class="qh-map-wrap" id="qhMapWrap">
      <div class="qh-map-inner" id="qhMapInner">
        <div id="qhMapImgWrap" style="position:relative">
          <img id="qhMapImg" src="/images/quy-hoach-nam-ban-2030.svg" alt="Bản đồ quy hoạch sử dụng đất Nam Ban 2030" style="width:100%;height:auto;display:block;transform-origin:0 0;cursor:grab" draggable="false">
          <div class="qh-zoom-controls">
            <button class="qh-zoom-btn" id="qhZoomIn" title="Phóng to">+</button>
            <button class="qh-zoom-btn" id="qhZoomOut" title="Thu nhỏ">−</button>
            <button class="qh-zoom-btn" id="qhZoomReset" title="Đặt lại" style="font-size:12px">⟳</button>
          </div>
        </div>
      </div>
      <p style="text-align:center;font-size:.78rem;color:#9B9B9B;margin-top:10px">Sử dụng nút +/− hoặc cuộn chuột để zoom · Kéo để di chuyển bản đồ</p>
    </div>
    <div style="text-align:center;margin-top:24px">
      <a href="https://zalo.me/0978758788" target="_blank" class="qh-cta-btn">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="vertical-align:middle;margin-right:6px"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="currentColor" stroke-width="2"/></svg>
        Check Quy Hoạch Miễn Phí
      </a>
      <p style="font-size:.8rem;color:#6B6B6B;margin-top:10px">Nhắn Zalo để được tra cứu quy hoạch lô đất cụ thể · Miễn phí · Trả lời ngay trong ngày</p>
    </div>
  </div>
</section>


<script>
(function(){
  var img=document.getElementById('qhMapImg');
  var wrap=document.getElementById('qhMapImgWrap');
  if(!img||!wrap)return;
  var scale=1,tx=0,ty=0,dragging=false,startX,startY;
  function applyTransform(){img.style.transform='translate('+tx+'px,'+ty+'px) scale('+scale+')';img.style.transformOrigin='0 0';}
  document.getElementById('qhZoomIn').onclick=function(){scale=Math.min(scale*1.3,6);applyTransform();};
  document.getElementById('qhZoomOut').onclick=function(){scale=Math.max(scale/1.3,1);if(scale<=1){tx=0;ty=0;}applyTransform();};
  document.getElementById('qhZoomReset').onclick=function(){scale=1;tx=0;ty=0;applyTransform();};
  wrap.addEventListener('wheel',function(e){e.preventDefault();var delta=e.deltaY>0?0.85:1.18;scale=Math.max(1,Math.min(6,scale*delta));if(scale<=1){tx=0;ty=0;}applyTransform();},{passive:false});
  wrap.addEventListener('mousedown',function(e){if(scale>1){dragging=true;startX=e.clientX-tx;startY=e.clientY-ty;img.style.cursor='grabbing';}});
  window.addEventListener('mousemove',function(e){if(!dragging)return;tx=e.clientX-startX;ty=e.clientY-startY;applyTransform();});
  window.addEventListener('mouseup',function(){dragging=false;img.style.cursor='grab';});
  wrap.addEventListener('touchstart',function(e){if(scale>1&&e.touches.length===1){dragging=true;startX=e.touches[0].clientX-tx;startY=e.touches[0].clientY-ty;}});
  wrap.addEventListener('touchmove',function(e){if(!dragging||e.touches.length!==1)return;e.preventDefault();tx=e.touches[0].clientX-startX;ty=e.touches[0].clientY-startY;applyTransform();},{passive:false});
  wrap.addEventListener('touchend',function(){dragging=false;});
})();
</script>

<!-- NOI LO -->
<section class="section pain-section">
  <div class="container">
    <div class="sec-header center" style="margin-bottom:36px">
      <p class="sec-label">Người mua từ xa thường gặp</p>
      <h2 class="sec-title">3 Nỗi Lo Phổ Biến Trước Khi Mua Đất Nam Ban</h2>
    </div>
      <div class="pain-grid">

      <div class="pain-card">
        <div class="pain-num">01</div>
        <h3 class="pain-q">Không biết tin ai</h3>
        <p class="pain-a">Chúng tôi không bán tất cả những gì chúng tôi có. Mỗi lô được đăng trên site này đã qua bộ lọc: pháp lý thực, giá thực, hiện trạng thực. Nếu lô nào không đạt, chúng tôi không đăng.</p>
        <a href="/lien-he/" class="pain-cta">Hỏi thẳng về lô bạn quan tâm →</a>
      </div>

      <div class="pain-card">
        <div class="pain-num">02</div>
        <h3 class="pain-q">Không có thời gian đi khảo sát — ở tận TP.HCM</h3>
        <p class="pain-a">Chúng tôi có thể khảo sát thay bạn: ảnh thực tế, video, check quy hoạch, đo đạc, phỏng vấn hàng xóm, kiểm tra lũ lụt, mất điện nước. Bạn ra quyết định dựa trên dữ liệu đầy đủ mà không cần phải đi.</p>
        <a href="https://zalo.me/0978758788" target="_blank" class="pain-cta">Nhờ khảo sát thay qua Zalo →</a>
      </div>

      <div class="pain-card">
        <div class="pain-num">03</div>
        <h3 class="pain-q">Sợ mua sai — mua xong mới phát hiện vấn đề pháp lý</h3>
        <p class="pain-a">100% sản phẩm chúng tôi giới thiệu có sổ đỏ riêng, đã qua kiểm tra tranh chấp, quy hoạch và hàng xóm. Bạn có thể yêu cầu bản sao sổ và tra cứu độc lập trước khi đặt cọc bất kỳ lô nào.</p>
        <a href="/dat-nen/" class="pain-cta">Xem các lô đã qua kiểm tra →</a>
      </div>

    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section class="section testimonials">
  <div class="container">
    <div class="sec-header center">
      <p class="sec-label">Khách hàng nói gì</p>
      <h2 class="sec-title">Tin Tưởng Được Xây Dựng Từ Thực Tế</h2>
    </div>
    <div class="testi-grid">

      <div class="testi-card">
        <span class="testi-quote">"</span>
        <p class="testi-text">Tôi mua lô đất ở đây đầu năm 2024. Điều hài lòng nhất là pháp lý rõ ràng — sổ hồng riêng, công chứng xong trong 3 ngày. Anh tư vấn không hề thúc ép, giải thích tường tận từng chi tiết hợp đồng.</p>
        <div class="testi-author">
          <div class="testi-avatar">MT</div>
          <div>
            <div class="testi-stars">★★★★★</div>
            <div class="testi-name">Anh Minh Tuấn</div>
            <div class="testi-role">Kỹ sư – Đà Lạt · Đất nền 336m²</div>
          </div>
        </div>
      </div>

      <div class="testi-card">
        <span class="testi-quote">"</span>
        <p class="testi-text">Gia đình tôi ở TP.HCM, mua đất Nam Ban để nghỉ dưỡng cuối tuần. Được dẫn đi xem thực địa rất chu đáo. Giờ mỗi cuối tuần lên đây tinh thần khỏe hẳn, không khí mát mẻ tuyệt vời.</p>
        <div class="testi-author">
          <div class="testi-avatar">TH</div>
          <div>
            <div class="testi-stars">★★★★★</div>
            <div class="testi-name">Chị Thu Hằng</div>
            <div class="testi-role">Doanh nhân – TP.HCM · Villa nghỉ dưỡng</div>
          </div>
        </div>
      </div>

      <div class="testi-card">
        <span class="testi-quote">"</span>
        <p class="testi-text">Đầu tư lô đất từ giữa 2023, đến nay giá tăng khoảng 35%. Quan trọng hơn là không rủi ro pháp lý — đúng như cam kết ban đầu. Sẽ tiếp tục tìm hiểu thêm sản phẩm tại đây.</p>
        <div class="testi-author">
          <div class="testi-avatar">VA</div>
          <div>
            <div class="testi-stars">★★★★★</div>
            <div class="testi-name">Anh Việt Anh</div>
            <div class="testi-role">Nhà đầu tư – Bình Dương · Đất nền 259m²</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- QUIZ / MỤC ĐÍCH -->
<section class="section quiz-section">
  <div class="container">
    <div class="hero-survey" id="heroSurvey">
      <p class="hero-survey-label">Bắt đầu từ đây</p>
      <h3>Bạn đang nghĩ đến Nam Ban với mục đích gì?</h3>
      <div class="survey-choices" id="surveyChoices">
        <button class="survey-choice" data-ans="nghi-duong"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M9 22V12h6v10" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>Xây nhà nghỉ dưỡng cuối tuần</button>
        <button class="survey-choice" data-ans="dau-tu"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0"><polyline points="23,6 13.5,15.5 8.5,10.5 1,18" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><polyline points="17,6 23,6 23,12" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>Đầu tư — chờ tăng giá</button>
        <button class="survey-choice" data-ans="dinh-cu"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0"><path d="M12 22V12" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="M12 12 C12 12 7 9 7 5a5 5 0 0110 0c0 4-5 7-5 7z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M5 22c0-3 3-5 7-5s7 2 7 5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>Định cư — chuyển lên sống hẳn</button>
        <button class="survey-choice" data-ans="tim-hieu"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" style="flex-shrink:0"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="1.7"/><path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>Đang tìm hiểu — chưa rõ</button>
      </div>
      <div class="survey-result" id="surveyResult"></div>
    </div>
  </div>
</section>

<script>
(function(){
  var answers={
    'nghi-duong':{
      text:'Nam Ban cách Đà Lạt 25 phút, khí hậu mát quanh năm, thị trường đất nền và đất vườn đa dạng diện tích từ 200m² trở lên. Nhiều gia đình từ TP.HCM, Hà Nội và nhiều tỉnh thành đang thực sự về Nam Ban để xây ngôi nhà second home mơ ước cho gia đình.',
      cta1:{label:'Xem đất phù hợp',href:'/dat-nen/'},
      cta2:{label:'Hỏi thêm qua Zalo',href:'https://zalo.me/0978758788',ext:true}
    },
    'dau-tu':{
      text:'Từ 2022 đến nay, đất Nam Ban có những nơi tăng 30–50% do nhiều nguyên nhân khách quan và nội tại. Chúng tôi sẽ phân tích thẳng khu vực nào, lô nào còn tiềm năng thật sự — không chỉ nói theo cảm tính.',
      cta1:{label:'Xem phân tích thị trường',href:'/thi-truong/'},
      cta2:{label:'Hỏi thẳng qua Zalo',href:'https://zalo.me/0978758788',ext:true}
    },
    'dinh-cu':{
      text:'Nam Ban đang đổi thay nhanh: trường học, chợ mới, café, dịch vụ đang mọc lên. Khí hậu 19–22°C quanh năm. Chúng tôi sẽ giới thiệu những khu phù hợp để ở lâu dài — không chỉ để đầu tư.',
      cta1:{label:'Khám phá cuộc sống Nam Ban',href:'/ve-nam-ban/'},
      cta2:{label:'Hay là cafe ở Nam Ban nhé?',href:'/lien-he/'}
    },
    'tim-hieu':{
      text:'Hoàn toàn bình thường — phần lớn người hỏi chúng tôi cũng bắt đầu như vậy. Không cần phải quyết định gì. Chỉ cần nói chuyện 15 phút, chúng tôi sẽ giúp bạn hiểu rõ hơn về Nam Ban.',
      cta1:{label:'Đọc Namban Notes',href:'/namban-notes/'},
      cta2:{label:'Hay là cafe đi?',href:'/lien-he/'}
    }
  };
  var sc=document.getElementById('surveyChoices');
  if(!sc)return;
  sc.addEventListener('click',function(e){
    var btn=e.target.closest('.survey-choice');
    if(!btn)return;
    var key=btn.dataset.ans;
    var a=answers[key];
    if(!a)return;
    document.querySelectorAll('.survey-choice').forEach(function(b){b.classList.remove('selected')});
    btn.classList.add('selected');
    var r=document.getElementById('surveyResult');
    r.innerHTML='<p>'+a.text+'</p><div class="survey-result-actions"><a href="'+a.cta1.href+'" class="survey-result-btn survey-result-btn-primary">'+a.cta1.label+'</a><a href="'+a.cta2.href+'"'+(a.cta2.ext?' target="_blank"':'')+' class="survey-result-btn survey-result-btn-sec">'+a.cta2.label+'</a></div>';
    r.style.display='block';
  });
})();
</script>

<!-- NAMBAN NOTES -->
<section class="notes-section">
  <div class="container">
    <div class="notes-editorial-wrap">
      <p class="notes-editorial-eyebrow">✦ Namban Notes</p>
      <a href="/namban-notes/buoi-sang-tren-doi-ca-phe/" class="notes-editorial">
        <div class="notes-editorial-meta">Tháng 5 · 2026 &nbsp;·&nbsp; Góc nhìn thực địa</div>
        <h3 class="notes-editorial-title">Buổi Sáng Trên Đồi Cà Phê — Và Người Đàn Ông Quyết Định Không Mua</h3>
        <p class="notes-editorial-desc">Anh đứng ở mép đồi nhìn ra thung lũng rất lâu. Rồi quay lại nói: "Đất đẹp thật. Nhưng tôi không mua." Một cuộc trò chuyện trung thực về bất động sản.</p>
        <span class="notes-read-btn">Đọc câu chuyện →</span>
      </a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <div class="container footer-inner">
    <div class="footer-brand">
      <a href="/" class="logo" style="margin-bottom:12px; display:inline-flex;">
        <img src="/images/logo.png" alt="Nam Ban Villas" width="41" height="52">
        <span class="logo-text" style="color:white;">NamBan<strong>Villas</strong></span>
      </a>
      <p><strong>Địa chỉ:</strong> TT. Nam Ban, Lâm Hà, Lâm Đồng</p>
      <div style="margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,.1)">
        <p style="color:white;font-size:.85rem;font-weight:700;margin-bottom:8px">Kết nối</p>
        <p><a href="tel:0978758788" style="color:#C9A84C;font-size:.88rem;">📞 0978 758 788</a> · <a href="https://zalo.me/0978758788" target="_blank" style="color:#C9A84C;font-size:.88rem;">Zalo</a></p>
      </div>
    </div>
    <div class="footer-links">
      <h4>Bất động sản</h4>
      <a href="/dat-nen/">Đất Nền Nam Ban</a>
      <a href="/nha-ban/">Nhà Bán Nam Ban</a>
    </div>
    <div class="footer-links">
      <h4>Thông tin</h4>
      <a href="/thi-truong/">Thị Trường BĐS</a>
      <a href="/ve-nam-ban/">Về Nam Ban</a>
      <a href="/lien-he/">Liên Hệ</a>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      <span>Giúp bạn ra quyết định đúng về đất Nam Ban</span>
    </div>
  </div>
</footer>

<!-- MOBILE BOTTOM NAV (chỉ hiện trên điện thoại) -->
<nav class="mobile-nav" aria-label="Điều hướng nhanh">
  <a href="/" class="mnav-item">
    <svg viewBox="0 0 24 24" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 22V12h6v10" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>
    <span>Trang chủ</span>
  </a>
  <a href="/dat-nen/" class="mnav-item">
    <svg viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="m20 20-3.5-3.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    <span>Tìm đất</span>
  </a>
  <a href="tel:0978758788" class="mnav-item mnav-call" aria-label="Gọi điện">
    <span class="mnav-call-circle">
      <svg viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.8 19.79 19.79 0 01.4 1.13 2 2 0 012.38.93h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 8.77a16 16 0 006.29 6.29l1.16-1.16a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="white" stroke-width="2"/></svg>
    </span>
    <span>Gọi ngay</span>
  </a>
  <a href="https://zalo.me/0978758788" target="_blank" class="mnav-item">
    <svg viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="6" stroke="currentColor" stroke-width="1.8"/><text x="12" y="16.5" text-anchor="middle" font-size="11" font-weight="800" font-family="Arial,sans-serif" fill="currentColor">Z</text></svg>
    <span>Zalo</span>
  </a>
  <button class="mnav-item" id="mnavMenuBtn" aria-label="Mở menu">
    <svg viewBox="0 0 24 24" fill="none"><path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    <span>Menu</span>
  </button>
</nav>

<!-- MOBILE MENU SHEET -->
<div class="mobile-sheet-overlay" id="mobileSheetOverlay"></div>
<div class="mobile-sheet" id="mobileSheet" role="dialog" aria-label="Menu">
  <div class="mobile-sheet-handle"></div>
  <a href="/dat-nen/">Đất Nền</a>
  <a href="/nha-ban/">Nhà Bán</a>
  <a href="/ve-nam-ban/">Về Nam Ban</a>
  <a href="/thi-truong/">Thị Trường</a>
  <a href="/lien-he/">Liên Hệ</a>
</div>
<script>
(function(){
  var btn=document.getElementById('mnavMenuBtn');
  var sheet=document.getElementById('mobileSheet');
  var ov=document.getElementById('mobileSheetOverlay');
  if(!btn||!sheet||!ov)return;
  function open(){sheet.classList.add('open');ov.classList.add('open');}
  function close(){sheet.classList.remove('open');ov.classList.remove('open');}
  btn.addEventListener('click',open);
  ov.addEventListener('click',close);
})();
</script>

<!-- FLOAT BUTTONS (desktop) -->
<script src="js/main.js" defer></script>

<!-- SELL WIDGET -->
<div class="sell-widget" id="sellWidget" style="display:none">
  <button class="sell-widget-close" id="sellWidgetClose" aria-label="Đóng">×</button>
  <h3 class="sell-widget-title">Bạn có câu hỏi về<br>mua/bán đất Nam Ban?</h3>
  <p class="sell-widget-desc">Hỏi thẳng · Trả lời thật</p>
  <div class="sell-widget-actions">
    <a href="https://zalo.me/0978758788" target="_blank" class="sell-widget-btn sell-widget-btn-primary">Nhắn Zalo</a>
  </div>
</div>
<script>
(function(){
  var w=document.getElementById('sellWidget');
  var c=document.getElementById('sellWidgetClose');
  if(!w||!c)return;
  // Chỉ hiện 1 lần duy nhất — dùng localStorage thay sessionStorage
  if(localStorage.getItem('nbv_popup_seen'))return;
  var shown=false;
  function show(){
    if(shown)return;
    shown=true;
    w.style.display='block';
    localStorage.setItem('nbv_popup_seen','1');
  }
  c.addEventListener('click',function(){w.style.display='none';});
  // Trigger 1: scroll qua 60% trang
  window.addEventListener('scroll',function(){
    var pct=window.scrollY/(document.body.scrollHeight-window.innerHeight);
    if(pct>=0.6)show();
  },{passive:true});
  // Trigger 2: exit intent (chuẩn bị thoát — chỉ desktop)
  document.addEventListener('mouseleave',function(e){
    if(e.clientY<10)show();
  });
})();
</script>
</body>
</html>
```

# PHỤ LỤC B — NGUYÊN VĂN css/style.css (411 dòng)

```css
/* ============================================================
 NAM BAN VILLAS – Redfin-style system fonts, no external deps
 Primary: #1A3D2B Gold: #C9A84C BG: #F7F3EE
 ============================================================ */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
 --green:#1A3D2B;--green2:#2E5C40;--green-light:#EBF4EE;
 --gold:#C9A84C;--gold-light:#FBF6E9;
 --bg:#F7F3EE;--bg2:#FFFFFF;
 --text:#1C1C1C;--muted:#6B6B6B;--border:#E2DBD0;
 --radius:10px;--radius-lg:16px;
 --shadow:0 2px 16px rgba(26,61,43,.07);
 --shadow-lg:0 8px 40px rgba(26,61,43,.13);
 --trans:.22s ease;
 /* Plus Jakarta Sans — geometric, close to Redfin's Maison Neue */
 --font: 'Plus Jakarta Sans Variable','Plus Jakarta Sans',
         -apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;
}
html{scroll-behavior:smooth;font-size:16px}
body{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.6;font-weight:400;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
h1,h2,h3,h4{font-weight:700;letter-spacing:-0.025em}
img{max-width:100%;height:auto;display:block}
a{color:inherit;text-decoration:none}
ul{list-style:none}
button{cursor:pointer;border:none;background:none;font-family:inherit}
.container{max-width:1180px;margin:0 auto;padding:0 24px}
.section{padding:64px 0}

/* ===== HEADER ===== */
.header{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(247,243,238,.97);backdrop-filter:blur(10px);border-bottom:1px solid transparent;transition:all var(--trans)}
.header.scrolled{border-bottom-color:var(--border);box-shadow:var(--shadow)}
.header-inner{display:flex;align-items:center;height:68px;gap:24px}
.logo{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-text{font-size:1.1rem;font-weight:500;color:var(--text);letter-spacing:-.01em}
.logo-text strong{color:var(--green);font-weight:800}
.nav{display:flex;align-items:center;gap:4px;margin-left:auto}
.nav-link{padding:7px 14px;border-radius:8px;font-size:.9rem;font-weight:500;color:var(--muted);transition:all var(--trans)}
.nav-link:hover,.nav-link.active{color:var(--green);background:var(--green-light)}
.header-right{display:flex;align-items:center;gap:12px;flex-shrink:0}
.hotline-btn{display:flex;align-items:center;gap:7px;background:var(--green);color:white;padding:9px 18px;border-radius:8px;font-weight:400;font-size:.88rem;transition:all var(--trans)}
.hotline-btn:hover{background:var(--green2);transform:translateY(-1px)}
.menu-btn{display:none;flex-direction:column;gap:5px;padding:6px}
.menu-btn span{display:block;width:20px;height:2px;background:var(--text);border-radius:2px;transition:all var(--trans)}

/* ===== HERO ===== */
.hero{position:relative;min-height:100vh;display:flex;align-items:center;padding-top:68px;overflow:hidden}
.hero-bg{position:absolute;inset:0;background:linear-gradient(150deg,#0D2B1C 0%,#1A3D2B 45%,#2E5C40 100%)}
.hero-bg::after{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")}
.hero-content{position:relative;z-index:1;color:white;padding:60px 0 80px}
.hero-eyebrow{font-size:.82rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:16px;opacity:.9}
.hero-title{font-size:clamp(2.2rem,5vw,3.8rem);font-weight:800;line-height:1.08;margin-bottom:18px;letter-spacing:-.04em}
.hero-title-sm{font-size:.52em;font-weight:400;opacity:.75;letter-spacing:-.01em;display:block}
.hero-title em{color:var(--gold);font-style:normal}
.hero-title-secondary{font-size:.72em;font-weight:400;opacity:.7;letter-spacing:0}
.hero-sub{font-size:1.05rem;color:rgba(255,255,255,.78);margin-bottom:36px;max-width:520px}

/* Search box */
.search-box{background:white;border-radius:var(--radius-lg);overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.25);max-width:780px;margin-bottom:48px}
.search-tabs{display:flex;border-bottom:2px solid var(--border);padding:0 8px}
.stab{padding:14px 20px;font-weight:600;font-size:.88rem;color:var(--muted);border-bottom:3px solid transparent;margin-bottom:-2px;transition:all var(--trans)}
.stab.active,.stab:hover{color:var(--green);border-bottom-color:var(--green)}
.search-form{display:flex;align-items:stretch}
.sf-field{flex:1;display:flex;flex-direction:column;padding:12px 16px;border-right:1px solid var(--border)}
.sf-field label{font-size:.72rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-bottom:3px}
.sf-field select{border:none;outline:none;font-size:.9rem;font-weight:500;font-family:inherit;color:var(--text);background:transparent;cursor:pointer}
.search-btn{display:flex;align-items:center;gap:8px;background:var(--green);color:white;padding:0 24px;font-weight:700;font-size:.9rem;transition:background var(--trans);flex-shrink:0}
.search-btn:hover{background:var(--green2)}

/* Hero stats */
.hero-stats{display:grid;grid-template-columns:repeat(3,auto);align-items:center;gap:28px}
.hstat strong{display:block;font-size:1.5rem;font-weight:400;color:var(--gold);line-height:1;letter-spacing:-.01em}
.hstat span{font-size:.76rem;color:rgba(255,255,255,.55);margin-top:3px;font-weight:400}

/* ===== LISTINGS ===== */
.listings{background:var(--bg2)}
.sec-header{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:36px;gap:16px;flex-wrap:wrap}
.sec-label{font-size:.74rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:6px;opacity:.85}
.sec-title{font-size:clamp(1.5rem,2.6vw,2rem);font-weight:700;line-height:1.18;color:var(--green);letter-spacing:-.02em}
/* Primary section (Listings) — anchor of the page, slightly larger */
.listings .sec-title{font-size:clamp(1.7rem,3vw,2.3rem);font-weight:800}
.sec-header.center{flex-direction:column;align-items:center;text-align:center}
.listing-tabs{display:flex;gap:6px}
.ltab{padding:8px 18px;border-radius:100px;border:2px solid var(--border);font-size:.85rem;font-weight:600;color:var(--muted);transition:all var(--trans)}
.ltab.active,.ltab:hover{border-color:var(--green);color:var(--green);background:var(--green-light)}

/* Property cards */
.prop-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:24px}
.prop-card{background:white;border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border);transition:all var(--trans)}
.prop-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg);border-color:transparent}
.prop-card.hidden{display:none}
.prop-img-wrap{position:relative;display:block;aspect-ratio:3/2;overflow:hidden;background:#EBF4EE}
.prop-img-wrap img{width:100%;height:100%;object-fit:cover;transition:transform .4s ease}
.prop-card:hover .prop-img-wrap img{transform:scale(1.04)}
.prop-badge{position:absolute;top:12px;left:12px;padding:4px 10px;border-radius:6px;font-size:.73rem;font-weight:700;background:var(--green);color:white}
.prop-badge.hot{background:var(--gold)}
.prop-body{padding:18px}
.prop-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.prop-price{font-size:1.1rem;font-weight:800;color:var(--green)}
.prop-area{font-size:.82rem;font-weight:600;color:var(--muted);background:var(--green-light);padding:3px 10px;border-radius:100px}
.prop-title{font-size:.97rem;font-weight:700;line-height:1.35;margin-bottom:7px}
.prop-title a:hover{color:var(--green)}
.prop-loc{display:flex;align-items:center;gap:4px;font-size:.8rem;color:var(--muted);margin-bottom:10px}
.prop-specs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.prop-specs span{font-size:.75rem;background:var(--bg);border:1px solid var(--border);padding:3px 9px;border-radius:100px;color:var(--muted)}
.prop-cta{display:block;text-align:center;padding:10px;background:var(--green);color:white;border-radius:8px;font-weight:700;font-size:.85rem;transition:background var(--trans)}
.prop-cta:hover{background:var(--green2)}
.view-all-wrap{text-align:center;margin-top:40px}
.view-all-btn{display:inline-flex;align-items:center;gap:8px;border:2px solid var(--green);color:var(--green);padding:12px 32px;border-radius:8px;font-weight:700;font-size:.95rem;transition:all var(--trans)}
.view-all-btn:hover{background:var(--green);color:white}

/* ===== WHY ===== */
.why{background:var(--bg)}
.why-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:20px;margin-top:8px}
.why-card{background:white;border-radius:var(--radius-lg);padding:22px 20px;border:1px solid var(--border);transition:all var(--trans)}
.why-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);border-color:var(--green-light)}
.why-icon{width:40px;height:40px;background:var(--green-light);border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--green);margin-bottom:10px}
.why-card h3{font-size:1rem;font-weight:700;margin-bottom:8px;color:var(--green)}
.why-card p{font-size:.88rem;color:var(--muted);line-height:1.6}

/* ===== PAIN SECTION ===== */
.pain-section{background:#1A3D2B}
.pain-section .sec-label{color:rgba(201,168,76,.7)}
.pain-section .sec-title{color:white}
.pain-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0}
@media(max-width:900px){.pain-grid{grid-template-columns:1fr}}
@media(max-width:580px){.pain-grid{grid-template-columns:1fr}}
.pain-card{padding:32px 28px;border-left:1px solid rgba(255,255,255,.1);display:flex;flex-direction:column;gap:10px}
.pain-card:first-child{border-left:none}
@media(max-width:900px){.pain-card{border-left:none;border-top:1px solid rgba(255,255,255,.1)}.pain-card:first-child{border-top:none}}
.pain-num{font-size:2.4rem;font-weight:900;color:var(--gold);opacity:.35;line-height:1;letter-spacing:-.04em}
.pain-q{font-size:.97rem;font-weight:700;color:white;line-height:1.4;margin:0}
.pain-a{font-size:.85rem;color:rgba(255,255,255,.55);line-height:1.75;flex:1;margin:0}
a.pain-cta{font-size:.8rem;font-weight:700;color:var(--gold);text-decoration:none;margin-top:4px;display:inline-block;opacity:.9}
a.pain-cta:hover{opacity:1;text-decoration:underline}
.btn{display:inline-block;padding:12px 24px;border-radius:50px;font-size:.88rem;font-weight:700;text-decoration:none;text-align:center;transition:all .2s;cursor:pointer}
.btn-gold{background:var(--gold);color:white}
.btn-gold:hover{background:#b8943e;transform:translateY(-1px)}
.btn-outline-light{border:1.5px solid rgba(255,255,255,.35);color:rgba(255,255,255,.85);background:transparent}
.btn-outline-light:hover{background:rgba(255,255,255,.1)}


/* ===== CTA STRIP ===== */
.cta-strip{background:linear-gradient(135deg,#0D2B1C,#1A3D2B);padding:64px 0;color:white}
.cta-inner{display:flex;justify-content:space-between;align-items:center;gap:32px;flex-wrap:wrap}
.cta-text h2{font-size:1.8rem;font-weight:800;margin-bottom:6px}
.cta-text p{opacity:.8;font-size:.97rem}
.cta-actions{display:flex;gap:12px;flex-wrap:wrap}
.btn-cta-primary{display:flex;align-items:center;gap:8px;background:var(--gold);color:white;padding:13px 24px;border-radius:8px;font-weight:700;font-size:.95rem;transition:all var(--trans)}
.btn-cta-primary:hover{background:#b8943b;transform:translateY(-1px)}
.btn-cta-zalo{display:flex;align-items:center;gap:8px;background:transparent;border:2px solid rgba(255,255,255,.4);color:white;padding:13px 24px;border-radius:8px;font-weight:700;font-size:.95rem;transition:all var(--trans)}
.btn-cta-zalo:hover{border-color:white;background:rgba(255,255,255,.08)}

/* ===== FOOTER ===== */
.footer{background:#0D2B1C;color:rgba(255,255,255,.7);padding:56px 0 0}
.footer-inner{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;margin-bottom:40px}
.footer-brand p{font-size:.88rem;line-height:1.7;margin-bottom:4px}
.footer-links{display:flex;flex-direction:column;gap:4px}
.footer-links h4{color:white;font-size:.9rem;font-weight:700;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.1)}
.footer-links a{font-size:.88rem;padding:4px 0;transition:color var(--trans)}
.footer-links a:hover{color:var(--gold)}
.footer-qr h4{color:white;font-size:.9rem;font-weight:700;margin-bottom:12px}
.footer-qr p{font-size:.78rem;margin-top:8px;opacity:.6}
#qrcode canvas,#qrcode img{border-radius:8px;border:3px solid white}
.footer-bottom{border-top:1px solid rgba(255,255,255,.08);padding:20px 0}
.footer-bottom .container{display:flex;justify-content:space-between;align-items:center;font-size:.8rem;flex-wrap:wrap;gap:8px}
.footer-bottom a:hover{color:var(--gold)}

/* ===== SELL WIDGET (fixed bottom-right) ===== */
.sell-widget{position:fixed;bottom:210px;right:24px;width:244px;background:var(--green);color:white;border-radius:16px;padding:20px;box-shadow:0 8px 32px rgba(0,0,0,.28);z-index:997;animation:slideInRight .4s ease}
@keyframes slideInRight{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:translateX(0)}}
.sell-widget-close{position:absolute;top:10px;right:12px;background:rgba(255,255,255,.15);border:none;color:white;width:22px;height:22px;border-radius:50%;font-size:14px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0;transition:background var(--trans)}
.sell-widget-close:hover{background:rgba(255,255,255,.3)}
.sell-widget-title{font-size:.95rem;font-weight:800;line-height:1.35;margin-bottom:8px;letter-spacing:-.01em}
.sell-widget-desc{font-size:.75rem;opacity:.78;line-height:1.5;margin-bottom:14px}
.sell-widget-actions{display:flex;flex-direction:column;gap:8px}
.sell-widget-btn{display:block;text-align:center;padding:9px 14px;border-radius:8px;font-weight:700;font-size:.82rem;transition:all var(--trans)}
.sell-widget-btn-primary{background:var(--gold);color:white}
.sell-widget-btn-primary:hover{background:#b8943b}
.sell-widget-btn-zalo{background:rgba(255,255,255,.15);color:white;border:1px solid rgba(255,255,255,.3)}
.sell-widget-btn-zalo:hover{background:rgba(255,255,255,.25)}
@media(max-width:768px){.sell-widget{width:220px;right:16px;bottom:190px}}
@media(max-width:480px){.sell-widget{width:200px;right:12px;bottom:170px}.sell-widget-desc{display:none}}


/* ===== MINI CONTACT FORM (listing sidebar) ===== */
.mini-contact-form h4{color:var(--green);font-size:.95rem;font-weight:700;margin-bottom:12px}
.quick-form{display:flex;flex-direction:column;gap:9px}
.quick-form input{width:100%;padding:10px 12px;border:1.5px solid var(--border);border-radius:8px;font-family:inherit;font-size:.88rem;outline:none;transition:border-color var(--trans);background:white}
.quick-form input:focus{border-color:var(--green)}
.quick-form-btn{width:100%;padding:11px;background:var(--green);color:white;border-radius:8px;font-weight:700;font-size:.88rem;cursor:pointer;border:none;font-family:inherit;transition:background var(--trans)}
.quick-form-btn:hover{background:var(--green2)}
.form-note{font-size:.75rem;color:var(--muted);margin-top:8px;text-align:center}
.form-note a{color:var(--gold);font-weight:600}
.form-success{display:none;text-align:center;padding:12px;background:var(--green-light);border-radius:8px;color:var(--green);font-weight:600;font-size:.88rem}

/* ===== TESTIMONIALS ===== */
.testimonials{background:var(--bg2)}
.testi-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px}
@media(max-width:900px){.testi-grid{grid-template-columns:1fr 1fr}}
@media(max-width:580px){.testi-grid{grid-template-columns:1fr}}
.testi-card{background:white;border-radius:10px;padding:20px;border:1px solid var(--border);position:relative}
.testi-quote{display:none}
.testi-text{font-size:.85rem;line-height:1.7;color:var(--muted);margin-bottom:14px;padding-top:0;font-style:normal;border-left:2px solid var(--border);padding-left:12px}
.testi-author{display:flex;align-items:center;gap:9px}
.testi-avatar{width:32px;height:32px;border-radius:50%;background:var(--green-light);color:var(--green);display:flex;align-items:center;justify-content:center;font-weight:600;font-size:.75rem;flex-shrink:0}
.testi-name{font-weight:600;font-size:.83rem;color:var(--text)}
.testi-role{font-size:.73rem;color:var(--muted);margin-top:1px}
.testi-stars{color:var(--gold);font-size:.72rem;margin-bottom:2px;letter-spacing:.05em}
@media(max-width:768px){.testi-grid{grid-template-columns:1fr}}
.news-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}
.news-card{background:white;border-radius:var(--radius-lg);overflow:hidden;border:1px solid var(--border);transition:all var(--trans)}
.news-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg)}
.news-card-img{aspect-ratio:16/9;overflow:hidden;background:var(--green-light)}
.news-card-img img{width:100%;height:100%;object-fit:cover;transition:transform .4s}
.news-card:hover .news-card-img img{transform:scale(1.04)}
.news-card-body{padding:18px}
.news-source{font-size:.72rem;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px}
.news-card-title{font-size:.95rem;font-weight:700;line-height:1.4;margin-bottom:8px}
.news-card-title a:hover{color:var(--green)}
.news-date{font-size:.78rem;color:var(--muted)}
.news-loading{text-align:center;padding:48px;color:var(--muted);grid-column:1/-1}
.news-loading .spinner{width:32px;height:32px;border:3px solid var(--border);border-top-color:var(--green);border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px}
@keyframes spin{to{transform:rotate(360deg)}}
.page-hero{background:linear-gradient(135deg,#0D2B1C,#1A3D2B);color:white;padding:120px 0 60px}
.page-hero h1{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;margin-bottom:10px}
.page-hero p{opacity:.8;font-size:1rem;max-width:540px}
.breadcrumb{display:flex;gap:8px;align-items:center;font-size:.82rem;margin-bottom:16px;opacity:.65}
.breadcrumb a:hover{color:var(--gold)}

/* ===== CONTACT PAGE ===== */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start}
.contact-info h3{font-size:1.1rem;font-weight:700;margin-bottom:16px;color:var(--green)}
.contact-item{display:flex;gap:14px;align-items:flex-start;margin-bottom:20px}
.contact-icon{width:40px;height:40px;background:var(--green-light);border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--green);flex-shrink:0}
.contact-item strong{display:block;font-weight:700;margin-bottom:2px}
.contact-item a:hover{color:var(--green)}
.form-card{background:white;border-radius:var(--radius-lg);padding:32px;border:1px solid var(--border)}
.form-card h3{font-size:1.1rem;font-weight:700;margin-bottom:20px;color:var(--green)}
.form-field{margin-bottom:16px}
.form-field label{display:block;font-size:.82rem;font-weight:700;margin-bottom:6px;color:var(--text)}
.form-field input,.form-field select,.form-field textarea{width:100%;padding:11px 14px;border:2px solid var(--border);border-radius:8px;font-family:inherit;font-size:.9rem;outline:none;transition:border-color var(--trans);background:white}
.form-field input:focus,.form-field select:focus,.form-field textarea:focus{border-color:var(--green)}
.form-field textarea{resize:vertical;min-height:100px}
.form-submit{width:100%;padding:13px;background:var(--green);color:white;border-radius:8px;font-weight:700;font-size:.95rem;cursor:pointer;transition:background var(--trans)}
.form-submit:hover{background:var(--green2)}
.qr-box{background:white;border-radius:var(--radius-lg);padding:24px;border:1px solid var(--border);text-align:center;margin-top:20px}
.qr-box h4{font-weight:700;margin-bottom:12px;color:var(--green)}
#qrcodeLarge canvas,#qrcodeLarge img{margin:0 auto;border-radius:8px}

/* ===== RESPONSIVE ===== */
@media(max-width:1024px){
 .footer-inner{grid-template-columns:2fr 1fr 1fr}
 .contact-grid{grid-template-columns:1fr}
}
@media(max-width:768px){
 .section{padding:44px 0}
 .nav{position:fixed;top:68px;left:0;right:0;background:var(--bg2);border-top:1px solid var(--border);flex-direction:column;align-items:stretch;padding:12px;transform:translateY(-100%);opacity:0;pointer-events:none;transition:all var(--trans);box-shadow:var(--shadow-lg)}
 .nav.open{transform:translateY(0);opacity:1;pointer-events:all}
 .nav-link{padding:12px 14px;border-radius:8px}
 .menu-btn{display:flex}
 .hotline-btn{display:none}
 .menu-btn.open span:nth-child(1){transform:rotate(45deg) translate(5px,5px)}
 .menu-btn.open span:nth-child(2){opacity:0}
 .menu-btn.open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px)}
 .search-form{flex-direction:column}
 .sf-field{border-right:none;border-bottom:1px solid var(--border)}
 .search-btn{border-radius:0 0 var(--radius-lg) var(--radius-lg);padding:16px;justify-content:center}
 .hero-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;text-align:center}
 .hstat{display:flex;flex-direction:column;align-items:center}
 .hstat strong{font-size:1.35rem}
 .hstat span{font-size:.7rem;line-height:1.3}
 .hstat-div{display:none}
 .prop-grid{grid-template-columns:1fr}
 .why-grid{grid-template-columns:1fr 1fr}
 .cta-inner{flex-direction:column;text-align:center}
 .footer-inner{grid-template-columns:1fr;gap:24px}
 .footer-bottom .container{flex-direction:column;text-align:center}
 .sec-header{flex-direction:column;align-items:flex-start}
}
@media(max-width:480px){
 .hero{min-height:auto;padding-bottom:40px}
 .hero-content{padding:44px 0 52px}
 .why-grid{grid-template-columns:1fr 1fr}
 .hero-stats{grid-template-columns:repeat(3,1fr)}
}
:focus-visible{outline:2px solid var(--green);outline-offset:2px}

/* ===== QUIZ / MỤC ĐÍCH (light section) ===== */
.quiz-section{background:var(--green);color:white}
.quiz-section .hero-survey{max-width:720px;margin:0 auto;text-align:center}
.hero-survey-label{font-size:.74rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-bottom:10px;opacity:.9}
.hero-survey h3{font-size:1.35rem;font-weight:700;color:white;margin-bottom:24px;line-height:1.35;letter-spacing:-.02em}
.survey-choices{display:grid;grid-template-columns:1fr 1fr;gap:12px;text-align:left}
.survey-choice{background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.18);border-radius:12px;padding:14px 18px;color:rgba(255,255,255,.9);font-size:.88rem;font-weight:600;cursor:pointer;text-align:left;transition:all .2s;font-family:inherit;line-height:1.4;display:flex;align-items:center;gap:12px}
.survey-choice svg{color:var(--gold)}
.survey-choice:hover{background:rgba(201,168,76,.15);border-color:var(--gold);color:white}
.survey-choice.selected{background:rgba(201,168,76,.2);border-color:var(--gold);color:white}
.survey-result{display:none;margin-top:18px;padding:20px;background:rgba(255,255,255,.07);border:1px solid rgba(201,168,76,.35);border-radius:12px;animation:fadeIn .3s ease;text-align:left}
.survey-result p{font-size:.92rem;color:rgba(255,255,255,.9);line-height:1.7;margin-bottom:16px}
.survey-result-actions{display:flex;gap:10px;flex-wrap:wrap}
.survey-result-btn{padding:10px 22px;border-radius:8px;font-size:.85rem;font-weight:700;text-decoration:none;transition:all .2s}
.survey-result-btn-primary{background:var(--gold);color:white}
.survey-result-btn-primary:hover{background:#b8943b}
.survey-result-btn-sec{background:transparent;border:1.5px solid rgba(255,255,255,.35);color:rgba(255,255,255,.85)}
.survey-result-btn-sec:hover{border-color:white}
@media(max-width:600px){.survey-choices{grid-template-columns:1fr}}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

/* ===== CAFE CTA STRIP ===== */
.cafe-strip{background:linear-gradient(135deg,#0D2B1C,#1A3D2B);padding:80px 0;color:white;text-align:center}
.cafe-strip-inner{max-width:640px;margin:0 auto;padding:0 24px}
.cafe-strip-eyebrow{font-size:.75rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:16px;opacity:.9}
.cafe-strip h2{font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;line-height:1.15;margin-bottom:14px;letter-spacing:-.03em}
.cafe-strip h2 em{color:var(--gold);font-style:normal}
.cafe-strip p{font-size:1rem;color:rgba(255,255,255,.72);line-height:1.7;margin-bottom:32px;max-width:500px;margin-left:auto;margin-right:auto}
.cafe-strip-btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.cafe-btn-primary{display:inline-flex;align-items:center;gap:9px;background:var(--gold);color:white;padding:15px 32px;border-radius:50px;font-weight:800;font-size:1rem;transition:all .2s;letter-spacing:-.01em}
.cafe-btn-primary:hover{background:#b8943b;transform:translateY(-2px);box-shadow:0 8px 24px rgba(201,168,76,.35)}
.cafe-btn-sec{display:inline-flex;align-items:center;gap:9px;background:transparent;border:2px solid rgba(255,255,255,.3);color:rgba(255,255,255,.85);padding:15px 32px;border-radius:50px;font-weight:700;font-size:1rem;transition:all .2s}
.cafe-btn-sec:hover{border-color:white;background:rgba(255,255,255,.07)}
.cafe-strip-note{font-size:.78rem;color:rgba(255,255,255,.4);margin-top:20px}

/* ===== NAMBAN NOTES SECTION ===== */
.notes-section{background:var(--green-light);padding:40px 0}
.notes-editorial-wrap{max-width:680px;margin:0 auto}
.notes-editorial-eyebrow{font-size:.72rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--green);opacity:.7;margin-bottom:12px}
.notes-editorial{display:block;border-left:3px solid var(--gold);padding-left:20px;text-decoration:none}
.notes-editorial-meta{font-size:.75rem;color:var(--muted);margin-bottom:8px;font-weight:500}
.notes-editorial-title{font-size:1.15rem;font-weight:700;color:var(--green);line-height:1.4;margin-bottom:8px;letter-spacing:-.02em}
.notes-editorial-desc{font-size:.88rem;color:var(--muted);line-height:1.65;margin-bottom:12px}
.notes-read-btn{display:inline-block;color:var(--green);font-weight:600;font-size:.82rem;border-bottom:1px solid var(--gold);padding-bottom:1px;transition:opacity .15s}
.notes-read-btn:hover{opacity:.7}

/* ===== CONTACT PAGE UPGRADE ===== */
.contact-page-intro{max-width:580px;margin-bottom:4px}
.contact-page-intro p{font-size:1rem;color:rgba(255,255,255,.75);line-height:1.7}
.form-context-row{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.form-honest-note{font-size:.82rem;color:var(--muted);text-align:center;margin-top:12px;line-height:1.6}
.form-honest-note strong{color:var(--green)}
@media(max-width:600px){.form-context-row{grid-template-columns:1fr}}

/* ===== MOBILE BOTTOM NAV ===== */
.mobile-nav{display:none}
.mobile-sheet,.mobile-sheet-overlay{display:none}
@media(max-width:768px){
  /* Thanh điều hướng cố định dưới đáy — vùng ngón cái dễ thao tác nhất */
  .mobile-nav{
    display:flex;position:fixed;bottom:0;left:0;right:0;z-index:1000;
    background:rgba(255,255,255,.97);backdrop-filter:blur(12px);
    border-top:1px solid var(--border);
    padding:6px 4px calc(6px + env(safe-area-inset-bottom));
    box-shadow:0 -2px 16px rgba(26,61,43,.08);
  }
  .mnav-item{
    flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
    gap:3px;padding:6px 2px;color:var(--muted);font-size:.66rem;font-weight:600;
    background:none;border:none;font-family:inherit;line-height:1;text-align:center;
    -webkit-tap-highlight-color:transparent;transition:color .15s;
  }
  .mnav-item svg{width:22px;height:22px}
  .mnav-item:active{color:var(--green)}
  .mnav-item span{white-space:nowrap}
  /* Nút Gọi nổi bật ở giữa, nhô lên */
  .mnav-call{color:var(--green)}
  .mnav-call-circle{
    display:flex;align-items:center;justify-content:center;
    width:52px;height:52px;border-radius:50%;background:var(--gold);
    box-shadow:0 4px 14px rgba(201,168,76,.45);margin-top:-22px;margin-bottom:1px;
    border:3px solid var(--bg);
  }
  .mnav-call-circle svg{width:24px;height:24px}

  /* Menu sheet trượt lên từ dưới */
  .mobile-sheet-overlay{
    display:block;position:fixed;inset:0;z-index:1001;background:rgba(13,43,28,.5);
    opacity:0;pointer-events:none;transition:opacity .25s;
  }
  .mobile-sheet-overlay.open{opacity:1;pointer-events:auto}
  .mobile-sheet{
    display:block;position:fixed;left:0;right:0;bottom:0;z-index:1002;
    background:var(--bg2);border-radius:20px 20px 0 0;
    padding:10px 20px calc(20px + env(safe-area-inset-bottom));
    transform:translateY(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);
    box-shadow:0 -8px 40px rgba(0,0,0,.2);
  }
  .mobile-sheet.open{transform:translateY(0)}
  .mobile-sheet-handle{width:40px;height:4px;background:var(--border);border-radius:99px;margin:6px auto 14px}
  .mobile-sheet a{
    display:block;padding:15px 8px;font-size:1rem;font-weight:600;color:var(--text);
    border-bottom:1px solid var(--bg);
  }
  .mobile-sheet a:last-child{border-bottom:none}
  .mobile-sheet a:active{color:var(--green)}

  /* Ẩn các điều khiển cũ trên mobile — bottom nav thay thế hết */
  .menu-btn{display:none}
  .hotline-btn{display:none}
  .nav{display:none}
  /* Chừa chỗ cho bottom nav, tránh che nội dung cuối trang */
  body{padding-bottom:64px}
  .footer{padding-bottom:24px}
}

/* ===== QUY HOẠCH MAP ===== */
.qh-map-wrap{background:white;border-radius:16px;border:2px solid #E2DBD0;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.08)}
.qh-map-inner{position:relative;overflow:hidden;user-select:none}
.qh-zoom-controls{position:absolute;top:60px;right:12px;display:flex;flex-direction:column;gap:4px}
.qh-zoom-btn{width:32px;height:32px;background:white;border:1px solid #ccc;border-radius:6px;font-size:18px;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.15);color:#1A3D2B;line-height:1}
.qh-zoom-btn:hover{background:#f0f0f0}
.qh-cta-btn{display:inline-flex;align-items:center;padding:14px 32px;background:var(--green);color:white;border-radius:50px;font-size:1rem;font-weight:700;text-decoration:none;transition:background .2s,transform .2s}
.qh-cta-btn:hover{background:var(--green2);transform:translateY(-2px)}
```

# PHỤ LỤC C — NGUYÊN VĂN js/main.js (124 dòng)

```javascript
/* Nam Ban Villas – Main JS */
(function(){
'use strict';

// Header scroll
const header=document.getElementById('header');
window.addEventListener('scroll',()=>header.classList.toggle('scrolled',window.scrollY>10),{passive:true});

// Mobile menu
const menuBtn=document.getElementById('menuBtn');
const nav=document.getElementById('nav');
menuBtn?.addEventListener('click',()=>{
  const o=menuBtn.classList.toggle('open');
  nav.classList.toggle('open',o);
});
document.addEventListener('click',e=>{
  if(nav?.classList.contains('open')&&!nav.contains(e.target)&&!menuBtn.contains(e.target)){
    nav.classList.remove('open');menuBtn.classList.remove('open');
  }
});

// Search tabs
document.querySelectorAll('.stab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.stab').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  const form=document.querySelector('.search-form');
  if(form) form.action='/'+t.dataset.tab+'/';
}));

// Listing filter
const ltabs=document.querySelectorAll('.ltab');
const cards=document.querySelectorAll('.prop-card');
ltabs.forEach(t=>t.addEventListener('click',()=>{
  ltabs.forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  const f=t.dataset.type;
  cards.forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.type!==f));
}));

// QR Code – Zalo
function makeQR(id,url,size){
  const el=document.getElementById(id);
  if(!el||typeof QRCode==='undefined') return;
  new QRCode(el,{text:url,width:size||120,height:size||120,colorDark:'#1A3D2B',colorLight:'#ffffff',correctLevel:QRCode.CorrectLevel.H});
}
window.addEventListener('load',()=>{
  makeQR('qrcode','https://zalo.me/0978758788',110);
  makeQR('qrcodeLarge','https://zalo.me/0978758788',180);
});

// Animate on scroll
if('IntersectionObserver' in window){
  const obs=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting){e.target.style.animation='fadeUp .5s ease forwards';obs.unobserve(e.target);}
    });
  },{threshold:.1,rootMargin:'0px 0px -30px 0px'});
  const animEls=document.querySelectorAll('.prop-card,.why-card,.news-card');
  animEls.forEach((el,i)=>{
    el.style.opacity='0';
    el.style.animationDelay=`${(i%4)*.07}s`;
    obs.observe(el);
  });
  // Fallback: nếu element không vào viewport sau 2.5s thì show hết
  setTimeout(()=>animEls.forEach(el=>{if(el.style.opacity==='0')el.style.opacity='1';}),2500);
}
const s=document.createElement('style');
s.textContent='@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}';
document.head.appendChild(s);

// ===== RSS NEWS LOADER =====
// Dùng rss2json API để bypass CORS
const RSS2JSON='https://api.rss2json.com/v1/api.json?rss_url=';

async function loadRSS(containerId,rssUrl,limit=9){
  const el=document.getElementById(containerId);
  if(!el) return;
  try{
    const res=await fetch(RSS2JSON+encodeURIComponent(rssUrl)+'&count='+limit);
    const data=await res.json();
    if(data.status!=='ok'||!data.items?.length) throw new Error('no items');
    el.innerHTML=data.items.map(item=>{
      const date=new Date(item.pubDate).toLocaleDateString('vi-VN');
      const img=item.thumbnail||item.enclosure?.link||'images/news-placeholder.svg';
      const source=data.feed?.title||rssUrl.replace('https://','').split('/')[0];
      return `<article class="news-card">
        <a href="${item.link}" target="_blank" rel="noopener" class="news-card-img">
          <img src="${img}" alt="${item.title}" width="400" height="225" loading="lazy" onerror="this.src='images/news-placeholder.svg'">
        </a>
        <div class="news-card-body">
          <p class="news-source">${source}</p>
          <h3 class="news-card-title"><a href="${item.link}" target="_blank" rel="noopener">${item.title}</a></h3>
          <p class="news-date">${date}</p>
        </div>
      </article>`;
    }).join('');
  }catch(e){
    el.innerHTML='<p class="news-loading">Đang cập nhật tin tức...</p>';
  }
}

// Thi truong – BDS news
const thiTruongEl=document.getElementById('news-thi-truong');
if(thiTruongEl){
  // VnExpress BĐS + CafeF BĐS
  loadRSS('news-thi-truong','https://vnexpress.net/rss/bat-dong-san.rss');
}

// Ve Nam Ban – local news
const veNamBanEl=document.getElementById('news-ve-nam-ban');
if(veNamBanEl){
  loadRSS('news-ve-nam-ban','https://news.google.com/rss/search?q=Nam+Ban+L%C3%A2m+%C4%90%E1%BB%93ng&hl=vi&gl=VN&ceid=VN:vi');
}

// Contact form
document.getElementById('contactForm')?.addEventListener('submit',function(e){
  e.preventDefault();
  const btn=this.querySelector('.form-submit');
  btn.textContent='✓ Đã gửi! Chúng tôi sẽ liên hệ sớm.';
  btn.style.background='#16a34a';
  setTimeout(()=>{this.reset();btn.textContent='Gửi yêu cầu';btn.style.background='';},4000);
});

})();
```

# PHỤ LỤC D — NGUYÊN VĂN vercel.json + llms.txt

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [
    {"source": "/mua-dat-nam-ban", "destination": "/dat-nen/", "permanent": true},
    {"source": "/dat-nam-ban", "destination": "/dat-nen/", "permanent": true},
    {"source": "/dat-nen-nam-ban-lam-dong", "destination": "/dat-nen/", "permanent": true},
    {"source": "/gia-dat-nam-ban", "destination": "/thi-truong/bang-gia-dat-lam-dong-2026/", "permanent": true},
    {"source": "/bang-gia-dat-nam-ban", "destination": "/thi-truong/bang-gia-dat-lam-dong-2026/", "permanent": true},
    {"source": "/second-home-da-lat", "destination": "/ve-nam-ban/tiem-nang-dau-tu-nam-ban/", "permanent": true},
    {"source": "/nha-nghi-duong-nam-ban", "destination": "/nha-ban/", "permanent": true},
    {"source": "/nam-ban-o-dau", "destination": "/ve-nam-ban/", "permanent": true},
    {"source": "/khi-hau-nam-ban", "destination": "/thi-truong/khi-hau-cuoc-song-nam-ban/", "permanent": true},
    {"source": "/song-cham-lam-dong", "destination": "/thi-truong/khi-hau-cuoc-song-nam-ban/", "permanent": true},
    {"source": "/co-nen-mua-dat-nam-ban", "destination": "/ve-nam-ban/tiem-nang-dau-tu-nam-ban/", "permanent": true},
    {"source": "/dat-nam-ban-co-tang-gia-khong", "destination": "/thi-truong/dat-nam-ban-tang-gia-2025/", "permanent": true},
    {"source": "/quy-hoach-nam-ban", "destination": "/thi-truong/lam-dong-quy-hoach-dieu-chinh-2026/", "permanent": true},
    {"source": "/lien-he", "destination": "/lien-he/", "permanent": true},
    {"source": "/contact", "destination": "/lien-he/", "permanent": true}
  ]
}
```

```
# Nam Ban Villas

> Nam Ban Villas là đơn vị môi giới bất động sản chuyên sâu về vùng Nam Ban, huyện Lâm Hà, tỉnh Lâm Đồng — khu vực cao nguyên gần Đà Lạt. Website cung cấp thông tin đất nền, nhà bán, phân tích thị trường, quy hoạch và đời sống tại Nam Ban. Mọi bất động sản giới thiệu đều đã kiểm tra pháp lý. Hotline/Zalo: 0978 758 788.

## Thông tin nền tảng về Nam Ban (dữ kiện chính xác)

- Vị trí: Thị trấn Nam Ban, huyện Lâm Hà, tỉnh Lâm Đồng, Việt Nam.
- Cách trung tâm Đà Lạt khoảng 27km theo đèo Tà Nung (đi xe 35–40 phút).
- Cách sân bay Liên Khương khoảng 22km — gần hơn cả Đà Lạt trung tâm.
- Độ cao khoảng 850–1.000m so với mực nước biển; nhiệt độ trung bình 18–22°C quanh năm.
- Đặc sản: cà phê Yellow Bourbon (arabica), dâu tằm tơ lụa, rau củ ôn đới.
- Điểm tham quan: Thác Voi, Hồ Bãi Công, Chùa Linh Ẩn, đồi thông, vườn cà phê.
- Giá đất thổ cư 2025–2026: khoảng 3–8 triệu đồng/m² tùy vị trí; đất view hồ/mặt tiền lớn 10–15 triệu/m². Giá tăng 30–50% so với 2023.
- Định hướng quy hoạch: phát triển du lịch sinh thái và nghỉ dưỡng (theo điều chỉnh quy hoạch tỉnh Lâm Đồng 2025).

## Trang chính

- [Trang chủ Nam Ban Villas](https://nambanvillas.vn/): Tổng quan mua bán đất nền và nhà tại Nam Ban.
- [Hỏi Đáp Mua Đất Nam Ban](https://nambanvillas.vn/hoi-dap/): 29 câu hỏi thường gặp về pháp lý, giá cả, quy hoạch, thủ tục, cuộc sống tại Nam Ban — nguồn trả lời nhanh và chính xác nhất.
- [Liên hệ](https://nambanvillas.vn/lien-he/): Hotline và Zalo 0978 758 788.

## Đất nền đang bán

- [Danh sách đất nền Nam Ban](https://nambanvillas.vn/dat-nen/): 11 lô đất nền phân lô sổ đỏ đang mở bán.
- [Đất 530m² view thung lũng — 899 triệu](https://nambanvillas.vn/dat-nen/thung-lung-530m2/)
- [Đất Đông Thanh 845m² view sương mây — 1,9 tỷ](https://nambanvillas.vn/dat-nen/dong-thanh-845m2/)
- [Đất Đông Thanh 320m² — 850 triệu](https://nambanvillas.vn/dat-nen/dong-thanh-320m2/)
- [Đất 2.700m² 2 mặt giáp suối — 2,95 tỷ](https://nambanvillas.vn/dat-nen/giap-suoi-2700m2/)
- [Đất 2 mặt tiền 345m² — 1,15 tỷ](https://nambanvillas.vn/dat-nen/hai-mat-tien-345m2/)
- [Đất Hồ Bãi Công lô 1 — 700m²](https://nambanvillas.vn/dat-nen/ho-bai-cong-lot1/)
- [Đất Hồ Bãi Công lô 2 — 950m²](https://nambanvillas.vn/dat-nen/ho-bai-cong-lot2/)
- [Đất Hồ Từ Liêm 700m²](https://nambanvillas.vn/dat-nen/ho-tu-liem-700m2/)
- [Đất Mê Linh suối thông 650m² — 1,25 tỷ](https://nambanvillas.vn/dat-nen/me-linh-suoi-thong-650m2/)
- [Đất 130m² sát Phố Thông Villas — 568 triệu](https://nambanvillas.vn/dat-nen/pho-thong-villas-130m2/)
- [Siêu phẩm đất 3.700m² mặt tiền 61m](https://nambanvillas.vn/dat-nen/sieu-pham-3700m2/)

## Nhà bán

- [Danh sách nhà bán Nam Ban](https://nambanvillas.vn/nha-ban/): Nhà nghỉ dưỡng và biệt thự vườn.
- [Hill House Village 203m² ven Đà Lạt — 2,6 tỷ](https://nambanvillas.vn/nha-ban/hill-house-village/)
- [Villa Mini Mê Linh 239m² 3PN — 2,38 tỷ](https://nambanvillas.vn/nha-ban/villa-mini-me-linh/)
- [Nhà vườn 1.018m² 3PN hồ cá Koi — 3,8 tỷ](https://nambanvillas.vn/nha-ban/nha-vuon-1018m2/)

## Thị trường & quy hoạch

- [Thị trường BĐS Nam Ban](https://nambanvillas.vn/thi-truong/): Tổng hợp phân tích thị trường.
- [Bảng giá đất Lâm Đồng 2026](https://nambanvillas.vn/thi-truong/bang-gia-dat-lam-dong-2026/)
- [Quy hoạch Lâm Đồng điều chỉnh 2026](https://nambanvillas.vn/thi-truong/lam-dong-quy-hoach-dieu-chinh-2026/)
- [Sân bay Liên Khương mở rộng — ảnh hưởng Nam Ban](https://nambanvillas.vn/thi-truong/san-bay-lien-khuong-mo-rong-anh-huong-nam-ban/)
- [Tuyến tránh Nam Ban — tiến độ và tác động giá đất](https://nambanvillas.vn/thi-truong/tuyen-tranh-nam-ban-khi-nao-hoan-thanh/)
- [Khí hậu và cuộc sống ở Nam Ban](https://nambanvillas.vn/thi-truong/khi-hau-cuoc-song-nam-ban/)
- [5 điều cần biết khi mua đất nền Nam Ban](https://nambanvillas.vn/thi-truong/mua-dat-nam-ban-kinh-nghiem-2025/)

## Về Nam Ban

- [Giới thiệu Về Nam Ban](https://nambanvillas.vn/ve-nam-ban/): Tổng quan vùng đất.
- [Tiềm năng đầu tư Nam Ban](https://nambanvillas.vn/ve-nam-ban/tiem-nang-dau-tu-nam-ban/)
- [Xã Nam Ban sau sáp nhập 2025](https://nambanvillas.vn/ve-nam-ban/xa-nam-ban-sap-nhap/)

## Namban Notes (chuỗi câu chuyện thật — phễu trải nghiệm)

- [Nam Ban có gì? Một buổi chiều đủ để hiểu](https://nambanvillas.vn/namban-notes/nam-ban-co-gi/)
- [Nam Ban có đáng sống không? Câu trả lời thật](https://nambanvillas.vn/namban-notes/co-dang-song-o-nam-ban/)
- [Không phải ai cũng hợp với Nam Ban](https://nambanvillas.vn/namban-notes/khong-phai-ai-cung-hop/)
- [Buổi sáng trên đồi cà phê — và người đàn ông quyết định không mua](https://nambanvillas.vn/namban-notes/buoi-sang-tren-doi-ca-phe/)
```

# PHỤ LỤC E — scripts/update-news.mjs + build-feed.mjs

```javascript
// ===== scripts/update-news.mjs =====
/**
 * Weekly news updater – fetches RSS feeds, writes data/news.json
 * Run via GitHub Actions every Monday 07:00 UTC (14:00 VN time)
 */
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const RSS_SOURCES = {
  thiTruong: [
    'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fvnexpress.net%2Frss%2Fbat-dong-san.rss&count=8',
    'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fcafef.vn%2Fthi-truong-bat-dong-san.rss&count=8',
  ],
  veNamBan: [
    'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fnews.google.com%2Frss%2Fsearch%3Fq%3DNam%2BBan%2BL%C3%A2m%2B%C4%90%E1%BB%93ng%26hl%3Dvi%26gl%3DVN%26ceid%3DVN%3Avi&count=8',
  ],
};

async function fetchRSS(url) {
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(15000) });
    const json = await res.json();
    if (json.status === 'ok') return json.items || [];
  } catch (e) {
    console.error('RSS fetch failed:', url, e.message);
  }
  return [];
}

function cleanHtml(str) {
  return (str || '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").trim();
}

function stripPhone(text) {
  return text.replace(/0\d{9}/g, '').replace(/\(\d{3,4}\)\s*\d{3,4}[\s-]\d{3,4}/g, '').trim();
}

async function main() {
  console.log('Fetching RSS feeds...');

  const [vnexpress, cafef] = await Promise.all([
    fetchRSS(RSS_SOURCES.thiTruong[0]),
    fetchRSS(RSS_SOURCES.thiTruong[1]),
  ]);
  const namBanItems = await fetchRSS(RSS_SOURCES.veNamBan[0]);

  // Merge + deduplicate by title
  const thiTruongRaw = [...vnexpress, ...cafef];
  const seen = new Set();
  const thiTruong = [];
  for (const item of thiTruongRaw) {
    const key = (item.title || '').slice(0, 60);
    if (!seen.has(key)) { seen.add(key); thiTruong.push(item); }
    if (thiTruong.length >= 10) break;
  }

  const data = {
    updatedAt: new Date().toISOString(),
    thiTruong: thiTruong.slice(0, 8).map(item => ({
      title: stripPhone(cleanHtml(item.title)),
      link: item.link || '#',
      pubDate: item.pubDate || '',
      description: stripPhone(cleanHtml(item.description || item.content || '')).slice(0, 300),
      thumbnail: item.thumbnail || item.enclosure?.link || '',
      source: new URL(item.link || 'https://vnexpress.net').hostname.replace('www.', ''),
    })),
    veNamBan: namBanItems.slice(0, 8).map(item => ({
      title: stripPhone(cleanHtml(item.title)),
      link: item.link || '#',
      pubDate: item.pubDate || '',
      description: stripPhone(cleanHtml(item.description || item.content || '')).slice(0, 300),
      thumbnail: item.thumbnail || item.enclosure?.link || '',
      source: new URL(item.link || 'https://news.google.com').hostname.replace('www.', ''),
    })),
  };

  mkdirSync(path.join(ROOT, 'data'), { recursive: true });
  writeFileSync(path.join(ROOT, 'data', 'news.json'), JSON.stringify(data, null, 2), 'utf8');
  console.log(`✓ Wrote data/news.json — thiTruong: ${data.thiTruong.length}, veNamBan: ${data.veNamBan.length}`);
}

main().catch(err => { console.error(err); process.exit(1); });

// ===== scripts/build-feed.mjs =====
// build-feed.mjs — Tạo RSS feed (feed.xml) từ các bài viết & tin đăng
// Chạy: node scripts/build-feed.mjs
// Dùng để: web có feed chuẩn -> tự động đồng bộ sang Facebook/Zalo/Telegram
// qua công cụ như Make/Zapier (không phải đăng tay), và để người đọc theo dõi.

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';

const SITE = 'https://nambanvillas.vn';
const ROOT = process.cwd();

// Các thư mục chứa bài viết / tin đăng cần đưa vào feed
const SECTIONS = ['thi-truong', 've-nam-ban', 'namban-notes', 'dat-nen', 'nha-ban'];

function extract(html, re) {
  const m = html.match(re);
  return m ? m[1].trim() : '';
}

function getDate(html) {
  // Ưu tiên datePublished trong JSON-LD
  let d = extract(html, /"datePublished"\s*:\s*"([^"]+)"/);
  if (d) return new Date(d);
  // Hoặc thẻ article:published_time
  d = extract(html, /property="article:published_time"\s+content="([^"]+)"/);
  if (d) return new Date(d);
  return null;
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

const items = [];

for (const section of SECTIONS) {
  const dir = join(ROOT, section);
  if (!existsSync(dir)) continue;
  for (const slug of readdirSync(dir)) {
    const file = join(dir, slug, 'index.html');
    if (!existsSync(file)) continue;
    const html = readFileSync(file, 'utf8');

    let title = extract(html, /<title>([^<]+)<\/title>/);
    title = title.replace(/\s*[|–-]\s*(Nam Ban Villas|Namban Notes)\s*$/i, '').trim();
    const desc = extract(html, /<meta name="description" content="([^"]+)"/);
    const canonical = extract(html, /<link rel="canonical" href="([^"]+)"/) || `${SITE}/${section}/${slug}/`;
    let date = getDate(html);
    if (!date || isNaN(date)) date = statSync(file).mtime;

    items.push({ title, desc, url: canonical, date, section });
  }
}

// Sắp xếp mới nhất trước, giới hạn 40 mục
items.sort((a, b) => b.date - a.date);
const top = items.slice(0, 40);

const now = new Date().toUTCString();
const xmlItems = top.map(it => `    <item>
      <title>${esc(it.title)}</title>
      <link>${esc(it.url)}</link>
      <guid isPermaLink="true">${esc(it.url)}</guid>
      <category>${esc(it.section)}</category>
      <description>${esc(it.desc)}</description>
      <pubDate>${it.date.toUTCString()}</pubDate>
    </item>`).join('\n');

const feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Nam Ban Villas — Đất nền, nhà bán &amp; thị trường Nam Ban</title>
    <link>${SITE}/</link>
    <atom:link href="${SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Tin mới nhất về đất nền, nhà bán, thị trường và đời sống tại Nam Ban, Lâm Đồng.</description>
    <language>vi-VN</language>
    <lastBuildDate>${now}</lastBuildDate>
${xmlItems}
  </channel>
</rss>
`;

writeFileSync(join(ROOT, 'feed.xml'), feed, 'utf8');
console.log(`feed.xml tạo xong với ${top.length} mục.`);
```

---
*Hết hồ sơ. Nguồn: repo doanquocduyet/nambanvillas + 18 docx PANORAMA METHOD (file 00–14). Bản nguyên văn playbook chi tiết nằm trong các .docx tương ứng ở gốc repo.*
