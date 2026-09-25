# BÀN GIAO ĐỢT 2 — NAM BAN VILLAS (23→25/9/2026) — ĐỂ ÁP SANG WEB KHÁC (GreenSpace…)

> Dán nguyên file này vào phiên Claude của web kia, kèm câu: **"Đọc hết, rà web này theo từng mục, cái nào hợp thì làm, cái nào khác ngữ cảnh thì bỏ và nói lý do."**
> Đi kèm file đợt 1: `docs/LOI-DA-GAP-VA-CACH-KIEM.md` (lỗi #1–#28 + 3 lỗi tự gây). File này là đợt 2: **19 PR (#515→#533)**, lỗi #29→#45.
> Mỗi mục có: **đã làm · vì sao · cách kiểm · sai đã gặp (nếu có)**. Số liệu Nam Ban chỉ để minh hoạ — web khác phải tự đo lại.

---

## PHẦN 0 — ĐỌC TRƯỚC: CÁI GÌ KHÔNG ĐƯỢC CHÉP NGUYÊN

| Luật bên Villas | Áp cho GreenSpace? |
|---|---|
| Không xưng ngôi thứ nhất, viết "Nam Ban Villas" | **KHÔNG.** GreenSpace là dịch vụ quan hệ, xưng **"chúng tôi"** là đúng giọng (đã chốt riêng bên đó). Chỉ chép phần *cấm chữ máy móc* (mục 7). |
| "Lâm Hà" luôn kèm "Nam Ban" | Chỉ chép **ý tưởng** (mục 8): tên vùng rộng phải neo vào địa bàn chính của web đó. Không chép nguyên câu. |
| Villas KHÔNG link sang Panorama | GreenSpace cũng **KHÔNG nhắc/link Panorama** (hiến pháp 3 web). Villas ↔ GreenSpace link 2 chiều được. |
| Trang giá đất / lô / ngộp / vườn | Villas là web **giao dịch**. GreenSpace là **dịch vụ trông coi đất** — không đăng lô, không làm trang giá. Chép **cách làm** (số sống, script, bẫy), không chép **trang**. |

---

## PHẦN 1 — NGUYÊN LÝ RÚT RA (áp cho mọi web)

1. **Số trên web phải do dữ liệu sinh ra, không gõ tay.** Mọi con số (số lô, giá "từ", khoảng giá, số dịch vụ…) ở title, mô tả, H1, schema, llms.txt đều từng bị cũ vì gõ tay. Villas: title hub ghi "94 lô, từ 480 triệu" trong khi thật là 116 lô, từ 368 triệu.
2. **Mỗi lời hứa phải có máy chạy đứng sau.** Trang ghi "cập nhật hàng tuần" mà không có việc nào chạy → đứng im 83 ngày. Hứa gì → cài lịch chạy + kiểm lần chạy đầu tiên thật sự thành công.
3. **Đặt nút liên hệ theo khoảnh khắc khách tin nhất**, không chỉ đầu/cuối trang: sau khối rủi ro, giữa bài phân tích, trên từng thẻ sản phẩm, đầu trang dịch vụ.
4. **Không nói quá, kể cả trong tiêu đề.** Đã phải sửa: "100% sổ hồng", "vườn đang thu hoạch" (không đúng mọi lô), "hạ giá thật" (có lô chưa hạ), "tuyến tránh đang thi công" (chưa duyệt).
5. **Trang đang top: không đụng URL / title / H1.** Chỉ sửa số sai, thêm nội dung bên dưới, chỉnh mô tả. Title do script sinh chỉ đổi theo **tháng**, không theo ngày/tuần.
6. **Không bao giờ tự xoá nội dung có ngày tháng.** Lịch sử có ngày là bằng chứng thật cho Google/AI. Cũ thì tụt xuống, không gỡ.
7. **Một ý định tìm kiếm = một URL.** Trùng ≥ ~50% nội dung thì gộp (301); khác câu hỏi thì giữ riêng và nối cụm.
8. **Mỗi lỗi sửa xong phải thành một bẫy** trong script kiểm tra, và **thử phá** để chắc bẫy nổ.
9. **Tạo trang/nhãn/luật mới liên quan tới việc đăng nội dung → ghi ngay vào phiếu của ô đăng** trong cùng PR (ô kia chỉ đọc phiếu).

---

## PHẦN 2 — CHI TIẾT TỪNG VIỆC (theo PR)

### 2.1 Nút Gọi/Zalo đúng chỗ (#515) — ÁP ĐƯỢC NGAY
- **Đã làm:** script `them-nut-goi.py` chạy lại được (idempotent), chèn:
  - nút Gọi trên **từng thẻ** sản phẩm (điện thoại: nút tròn chỉ icon góc thẻ, có `aria-label`);
  - dải "Chưa thấy cái hợp? Gọi…" sau mỗi 12 thẻ trong danh sách dài;
  - khối Gọi/Zalo **ngay sau khối rủi ro** trên trang chi tiết;
  - khối giữa bài (bài > 1.800 chữ, chưa có nút ở nửa đầu) + khối cuối bài (thay nút `/lien-he/` bằng `tel:` + Zalo);
  - cặp nút ngay dưới đoạn mở của 8 trang dịch vụ; trang hỏi đáp thêm khối sau mỗi 2 nhóm câu;
  - **mục cuối menu điện thoại** (được CSS tô thành nút to nhất) = `tel:` thay vì `/lien-he/`.
- **Vì sao:** đo thấy hub cuộn 122 thẻ = 90% trang không có nút gọi; bài viết phải đọc hết mới gặp nút; nút to nhất menu lại dẫn sang trang khác.
- **Cách kiểm:** đếm vị trí `tel:` đầu tiên theo % chữ của thân trang; bẫy 14 (thiếu nút trên thẻ, mục cuối menu không phải `tel:`, trang chi tiết thiếu khối sau rủi ro, thiếu speculationrules).
- **Sai đã gặp:** trang chủ đã có cặp Gọi/Zalo riêng trên thẻ → gắn thêm thành 2 nút → thêm điều kiện "thẻ có sẵn cặp nút thì bỏ qua".

### 2.2 Sự thật trên trang (#515, #518, #519)
- Gỡ: "đang thi công / kỳ vọng +20%", "100% sổ hồng", "40–60%", ROI 8–12%/năm, lấp đầy 60–70%, 20–40 triệu/tháng (không nguồn) → gỡ hoặc thay **số thật trong danh mục** (vd "villa 385m² đang cho thuê 12 triệu/tháng").
- Gỡ 9 tính từ rỗng ("lý tưởng nhất", "hàng đầu Đông Nam Á") → thay bằng dữ kiện.
- **Sai tự gây:** viết FAQ "đất Đà Lạt chênh 5–10 lần" không nguồn, mâu thuẫn chính bài so sánh trên site (50–150 triệu/m²) → **luật: số mới phải đối chiếu với bài gốc trên site trước khi viết.**

### 2.3 Trùng URL (#515)
- 1 lô đăng 2 URL (trùng từng thông số) → giữ 1, 301 cái kia, gỡ khỏi hub/trang khu/sitemap, đổi mọi link nội bộ, sửa số đếm. Script đổ thẻ sang trang con phải **bỏ thẻ không còn trên nguồn**.
- **GreenSpace áp:** quét bài/trang dịch vụ trùng ý (≥ 50% nội dung) → gộp + 301.

### 2.4 WCAG / UX (#515) — ÁP ĐƯỢC NGAY
- Chữ trắng trên nền vàng (2.3:1) → chữ tối (7:1). Xám `#8a978f` (3:1, 527 chỗ) → `#5F6E66` (5.8:1). `.sec-label` bỏ `opacity:.85`. Dấu breadcrumb, tiêu đề menu, dòng nguồn: đổi màu đạt 4.5:1. **Tính tỷ lệ bằng công thức WCAG, không đoán.**
- Nút đóng/xoá < 24px → ≥ 24px (WCAG 2.2 SC 2.5.8).
- Menu điện thoại/thanh so sánh ẩn bằng `transform/opacity` → Tab vẫn dừng vào link vô hình → thêm `visibility:hidden` + `transition-delay`; `aria-expanded` trên nút; Esc đóng + trả focus.

### 2.5 Tốc độ / bảo mật (#515) — ÁP ĐƯỢC NGAY
- Ảnh hero là **nền CSS** (không có srcset) → `@media` đổi `background-image` theo bề rộng (480/800/1200/gốc) + `<link rel=preload media=…>` cho trang chủ.
- CSS/JS đã có `?v=<hash>` nhưng cache chỉ 1 ngày → `max-age=31536000, immutable`.
- Thêm Content-Security-Policy (liệt kê đúng tên miền đang dùng).
- `404.html` không có `?v=` vì script đóng dấu chỉ quét `**/index.html` → quét `**/*.html`.
- 18 trang mới thiếu `speculationrules` → thêm + bẫy.

### 2.6 Title / mô tả (#516, #533)
- 140 mô tả > 160 ký tự → rút, **giá lấy từ schema** (không bắt chữ: suýt ghi giá thuê thành giá bán), kết bằng hotline. 69 title dài bỏ đuôi thương hiệu.
- **Sai tự gây (nặng):** rút mô tả **theo số ký tự** → 4 mô tả **cụt giữa câu** ("lô 577m² (ngang. Từ 699 triệu…"). Phiên sau sửa + bẫy 9c chặn mô tả cắt dở (ngoặc mở chưa đóng, cụt ý).
- **Luật:** rút mô tả phải cắt ở **ranh câu**, rồi đọc lại từng câu; không cắt máy móc.

### 2.7 Trang số liệu tự cập nhật (#516 → #527, #531) — CHÉP CÁCH LÀM
- `cap-nhat-gia-hom-nay.py`: đọc dữ liệu thẻ trên hub (`data-price`, `data-area`, `data-loc`, `data-nhan`) → tính khoảng giá phổ biến + **giá trung bình** → sinh bảng tuần, bảng theo khu, khung "Trả lời nhanh" (AEO), FAQ có số, title/mô tả/schema (Dataset, WebPage speakable). Lịch sử lưu `data/gia-tuan.json`.
- **Chạy bằng GitHub Actions** (`gia-tuan.yml`): ngay khi dữ liệu nguồn đổi + mỗi thứ Hai; kiểm tra sạch mới đẩy. Đã tắt Routine trùng việc.
- **Mỗi tuần 1 ô:** trong tuần làm mới ô của tuần đó; sang tuần thêm ô mới; không xoá ô cũ.
- **Tính bù lịch sử:** git còn giữ hub ở từng thời điểm → tính lại các thứ Hai đã lỡ (31/8→21/9) từ đúng dữ liệu hôm đó.
- **Sai đã gặp:**
  - Trang hứa "cập nhật hàng tuần" nhưng từ đầu **chưa từng nối script** (tài liệu ghi "chưa nối") → đứng im 83 ngày. Chủ web đã dặn "cập nhật liên tục" từ trước.
  - Tự xoá bảng tuần 2/7 khi làm lại trang → phải khôi phục từ git.
  - Script có lệnh "giữ tối đa 8 tuần / 20 ngày / 8 mục" → gỡ hết.
  - Máy chạy theo giờ UTC → ghi "cập nhật 24/9" khi web đã là 25/9 → **script tự tính ngày theo `Asia/Ho_Chi_Minh`** + `TZ` trong workflow.
  - Chạy script qua `| head` → BrokenPipe cắt ngang giữa chừng, 1 trang ghi dở → không bao giờ pipe output script ghi file.
  - Đọc thẻ kiểu cũ (`class="prop-card"` không có `sp-row`) ra 0 lô → regex nhận cả 2 kiểu.
  - Dấu `%` trong chuỗi format Python → phải viết `%%`.
- **Chữ cho người đọc:** "trung vị", "10%–90%", "giá giữa" → khách không hiểu. Đổi **cách tính** sang trung bình cộng sau khi bỏ 10% đầu + 10% cuối, gọi **"giá trung bình"** (đúng nghĩa), "khoảng giá phổ biến". Tính lại toàn bộ lịch sử cùng cách.
- **GreenSpace áp:** chỗ nào có số (số khách đang trông, giá gói, số lần kiểm trong tháng…) → sinh từ dữ liệu, không gõ tay; nếu hứa "cập nhật" → có workflow chạy thật.

### 2.8 Trang theo từ khoá (#517→#530) — CHÉP CÁCH CHỌN CHỖ
Quy trình mỗi từ khoá chủ web đưa (dán kết quả Google):
1. Tìm trang đang có: nếu đã có trang cùng ý định → **nâng trang đó**, không mở trang mới (tránh tự cắn).
2. Nếu trang đó đang top → chỉ thêm mục/FAQ bên dưới + chỉnh mô tả (vd mục "Có 300 triệu mua được đất không?" thêm vào trang giá rẻ top 4).
3. Chỉ mở trang mới khi ý định khác hẳn **và** có đủ nội dung thật (≥ 3 sản phẩm thật).
4. Kiểm hiến pháp 3 web (ai sở hữu từ khoá).
5. Mỗi trang: khung "Trả lời nhanh" 40–60 chữ có số, H1 + H2 dạng **câu người ta gõ**, FAQ có số sống, nối link 2 chiều với trang anh em, llms.txt, sitemap.
- **Sai đã gặp:**
  - Mở 2 trang "vườn cà phê" + "vườn bơ" → trùng 3/4 lô, chủ web thấy lủng củng → gộp 1 trang "Bán đất vườn Nam Ban" với H2 cho từng loại, 301 2 trang cũ.
  - Gắn nhãn theo từ khoá trong mô tả → bắt nhầm "xung quanh là vườn cà phê", "view đồi cà phê", "phía dưới giáp suối" (thành "dưới giá") → **luật: đọc câu gốc từng mục trước khi gắn nhãn**.
  - "Đất trồng cây lâu năm" là loại đất trên sổ, không phải cây có trên đất → không gắn nhãn, viết hẳn mục giải thích (câu AI thích trích).
  - Chủ web đưa tin "Nam Hà sắp sáp nhập Nam Ban" → tra nguồn chính thức không thấy → **không đưa lên web**, chờ văn bản.

### 2.9 Trang chủ đang top 1 (#521) — ÁP ĐƯỢC NGAY
- Mô tả chung chung → Google tự nhặt câu lẻ để hiện. Viết lại mô tả có số thật + đúng ý định ("đưa đi xem tận nơi") + hotline; thêm 1 câu đúng ý định trong thân; schema `makesOffer` cho dịch vụ có thật. **Không đụng title/H1.**
- **GreenSpace áp:** xem Google đang hiện câu nào dưới trang chủ cho từ khoá chính; nếu là câu lẻ → viết mô tả + 1 câu đúng ý định.

### 2.10 Luật neo địa danh (#519, #525)
- Chủ web chốt: "Lâm Hà" luôn có "Nam Ban" ngay cạnh, Nam Ban đứng trước. Script `lam-ha-kem-nam-ban.py` viết lại **tất định** (thân trang và JSON-LD đổi y hệt → FAQ hiển thị và schema không lệch): 1.025 chỗ / 216 trang. Xã khác ghi "Nam Hà (giáp Nam Ban)" — không ghi sai địa giới. Bẫy 18.
- **Sai đã gặp:** cửa sổ regex `finditer` nuốt nhau khi 2 cặp đứng sát → kiểm **từng chỗ** riêng; ký tự ngoặc kép chen giữa làm bẫy báo nhầm.

### 2.11 Giữ thứ hạng (#520)
- Rà mọi title/H1/canonical đổi trong ngày so với bản đầu ngày. Phát hiện script đưa **ngày + số lô** vào title/H1 → đổi mỗi tuần → Google đánh giá lại liên tục → title/H1 chỉ đổi theo tháng. Bẫy 19.

### 2.12 Không bao giờ tự xoá (#526)
- Gỡ mọi "giữ tối đa N" trong script, Routine, tài liệu (tin rao theo ngày, bảng tuần, mục cập nhật thị trường, card cụm bán hết → giữ + nhãn "Đã bán"). Bẫy 21: số khối có ngày trên nhánh không được ít hơn main.
- **GreenSpace áp:** ô "Cập nhật" đang có lệnh "giữ tối đa 6 mục, xoá mục cũ nhất" → **gỡ** (theo luật này).

### 2.13 Giọng đội ngũ (#524) — ÁP ĐƯỢC NGAY
- Chủ web: khách không bao giờ được đọc thấy "script, tự động, auto, bot, AI, nhập tay, thuật toán". Viết "đội ngũ … tổng hợp mỗi thứ Hai". Thành ngữ "không tự động nghĩa là" → "không mặc nhiên". Ngoại lệ: tên tiện ích thật ("béc tưới tự động"). Bẫy 20 soi thân trang + title + meta + alt + JSON-LD + llms.txt.
- **Sai đã gặp:** quét chữ "ai" không phân biệt hoa thường → bắt nhầm chữ tiếng Việt "ai" (người nào) 269 lần → chỉ bắt "AI" viết hoa, đứng riêng.

### 2.14 Dữ liệu ẩn lệch chữ hiện (#530)
- Thẻ ghi "990 tr/lô" nhưng `data-price="0.9"`; cụm ghi "Từ 1,108 tỷ" nhưng 1.167 → sai lan sang bộ lọc + mọi trang số liệu. Bẫy 13c: giá hiển thị (1 giá, không phải khoảng) phải khớp thuộc tính dữ liệu ±2%.
- **GreenSpace áp:** nếu có bảng giá gói ở nhiều nơi (trang chủ, trang giá, FAQ, schema) → 1 nguồn, các nơi khác sinh ra; bẫy so khớp.

### 2.15 Phiếu cho ô đăng nội dung (#531, #532, #533)
- Viết mục "🆕 CẬP NHẬT" đầu phiếu ô đăng tin: chạm đúng chỗ nào, thuộc tính bắt buộc, bảng nhãn, luật chữ, title/mô tả/H1, chống trùng, không xoá, thứ tự lệnh, trang tự cập nhật, checklist 12 dòng. Luật CLAUDE.md: tạo gì mới → ghi phiếu trong cùng PR.
- Phiên đăng tin đọc phiếu → tự sửa 5 tin cũ lệch phiếu (title 110 → 54 ký tự, mô tả cụt câu).

---

## PHẦN 3 — BẪY KIỂM TRA ĐÃ THÊM (chép ý tưởng, viết lại cho web kia)

| Bẫy | Kiểm gì | Lỗi thật đã bắt |
|---|---|---|
| 13b | Số trong `<head>` (title, mô tả, og) của trang danh sách = số thẻ thật | "94 lô" khi thật 116 |
| 13c | Giá hiển thị trên thẻ = thuộc tính dữ liệu | 990 tr vs 0.9 |
| 14 | Nút gọi trên mọi thẻ; mục cuối menu điện thoại là `tel:`; trang chi tiết có khối sau rủi ro; có speculationrules | hub 122 thẻ không nút |
| 18 | Tên vùng rộng luôn neo địa bàn chính | 1.025 chỗ |
| 19 | Title/H1 trang do script sinh không chứa ngày/số tuần | title đổi mỗi tuần |
| 20 | Không chữ máy móc trong mọi chữ khách đọc | "script của Nam Ban Villas" |
| 21 | Số khối có ngày không được ít hơn main | mất bảng tuần 2/7 |
| 9c | Mô tả không cụt giữa câu | 4 mô tả cụt |

Cách viết bẫy: đọc file → regex/đếm → `L("[mô tả lỗi] file")` → chạy trong CI mỗi push. **Mỗi bẫy phải thử phá** (cố ý tạo lỗi, thấy bẫy nổ, trả lại).

---

## PHẦN 4 — CHECKLIST RÀ CHO GREENSPACE (làm theo thứ tự)

1. [ ] Mọi con số ở title/mô tả/H1/schema/llms.txt: gõ tay hay sinh từ dữ liệu? Số nào sai hiện tại?
2. [ ] Lời hứa tần suất ("cập nhật hàng tuần", "báo cáo mỗi tháng") có workflow chạy thật không? Lần chạy gần nhất khi nào?
3. [ ] Ô "Cập nhật" có lệnh xoá mục cũ không → gỡ, giữ toàn bộ kèm ngày.
4. [ ] Vị trí nút Zalo/Gọi đầu tiên ở bao nhiêu % trang (trang chủ, trang dịch vụ, bài viết)? Có khối liên hệ ngay sau đoạn thuyết phục nhất không? Mục cuối menu điện thoại có gọi thẳng không?
5. [ ] Chữ máy móc (script, tự động, bot, AI…) có lọt ra trang không.
6. [ ] Tương phản màu chữ phụ (tính WCAG), nút < 24px, menu ẩn còn nhận Tab không, `aria-expanded`.
7. [ ] Ảnh hero nền CSS có bản nhỏ cho điện thoại không; cache CSS/JS có vân tay + `immutable` không; có CSP không; 404 có đóng dấu phiên bản không.
8. [ ] Mô tả > 160 ký tự hoặc cụt câu; title > 60 ký tự.
9. [ ] Trang đang top (xem Search Console) → khoá title/H1/URL, chỉ thêm nội dung.
10. [ ] Nội dung trùng ý (≥ 50%) → gộp + 301; khác câu hỏi → giữ riêng, nối cụm bằng câu hỏi.
11. [ ] Nói quá / số không nguồn (ROI, % tăng, "100%") → gỡ hoặc gắn nguồn.
12. [ ] Không link/nhắc Panorama.
13. [ ] Mỗi lỗi sửa → thêm bẫy vào script kiểm tra + thử phá.
14. [ ] Ghi lại tất cả vào tài liệu lỗi của web đó (như file này).

---

## PHẦN 5 — DANH SÁCH LỖI TỰ GÂY TRONG ĐỢT NÀY (để phiên kia khỏi lặp)

1. Cắt mô tả theo số ký tự → cụt câu (4 trang).
2. Xoá bảng tuần cũ khi làm lại trang.
3. FAQ số không nguồn, mâu thuẫn bài có sẵn.
4. Title/H1 đưa ngày + số lô → đổi mỗi tuần.
5. Tiêu đề nói quá ("đang thu hoạch", "hạ giá thật").
6. Mở 2 trang trùng 3/4 nội dung.
7. Đặt tên thống kê bằng thuật ngữ khách không hiểu ("trung vị", "giá giữa").
8. Máy giờ UTC ghi sai ngày.
9. Pipe output script ghi file qua `head` → ghi dở.
10. Regex bắt nhầm ("dưới giá" trong "dưới giáp suối"; "ai" thường).
11. Tưởng trang được cập nhật hàng tuần mà chưa từng nối script — không kiểm lần chạy thật.
