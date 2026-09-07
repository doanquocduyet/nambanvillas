# ĐĂNG TIN KHÔNG LỖI — quy trình bất biến cho ô đăng tin

> **Ảnh cũng là bài đăng.** Toàn bộ luật ảnh (alt, width/height, LCP, WebP,
> `Product.image`, sitemap ảnh, og:image, GEO, che PII trên sổ) nằm ở
> `docs/package/MO-O-DANG-TIN.md` — mục "ẢNH CŨNG PHẢI CHUẨN AEO/SEO/GEO".
> Bài chuẩn mà ảnh bỏ trống = mất nguyên kênh Google Images + Google Lens + AI.

> Đọc file này TRƯỚC khi đăng bất kỳ tin nào. Mọi mục dưới đây đều xuất phát từ
> **lỗi đã xảy ra thật** trên nambanvillas.vn và đã phải mất công truy + sửa.
> Mục tiêu: mỗi lần đăng đều suôn, không lặp lại lỗi cũ, chuẩn AEO/SEO/GEO.
>
> 👉 Kèm theo: **`docs/package/MO-O-DANG-TIN.md`** — đầu file có **✅ CHECKLIST KHÔNG BỎ SÓT (8 dòng)**. Đọc checklist đó trước, rồi mới xuống các lỗi chi tiết dưới đây.

---

## 0. LUẬT VÀNG — 1 câu

> **Dựng chuỗi → KIỂM TRONG BỘ NHỚ → mới GHI ra file → chạy script kiểm → mới push.**

Không bao giờ ghi file rồi mới kiểm. Đã dính: ghi ra file rồi mới phát hiện JSON-LD
hỏng / marker git lọt vào, phải khôi phục từ git và làm lại.

---

## 1. CHẠY SCRIPT KIỂM — BẮT BUỘC, KHÔNG NGOẠI LỆ

```bash
python3 scripts/kiem-tra-truoc-khi-dang.py
```

- Thoát **0 = SẠCH**, được push.
- Thoát **1 = CÓ LỖI**, in rõ từng lỗi + tên file. Sửa hết rồi chạy lại.

Script kiểm 10 nhóm (mục 3–12 dưới đây). **CI cũng chạy nó** mỗi lần push/PR vào
`main` (`.github/workflows/kiem-tra.yml`) — nên có bỏ qua ở máy thì CI vẫn bắt.

> Lần chạy đầu tiên script đã bắt ngay 1 lỗi thật mà rà tay bỏ sót:
> một tin nhà chưa được thêm vào ItemList của hub. **Máy đáng tin hơn trí nhớ.**

---

## 2. THỨ TỰ LÀM 1 TIN MỚI (không đảo)

1. **Xác nhận khu THẬT** trước khi đặt slug (Nam Ban / Đông Thanh / Mê Linh / Gia Lâm /
   Từ Liêm / Bãi Công / Chi Lăng…). Đặt sai khu = phải đổi tên + thêm redirect, rất tốn công.
2. **Nén ảnh**: `python3 scripts/nen-anh.py images/listings/<slug>/`
   (ảnh điện thoại 3–5MB không được đưa thẳng lên site).
3. **Dựng trang chi tiết** theo `docs/FORM-DANG-TIN.md` + mục 3–12 dưới.
4. **Nối dây** (mục 6) — bước hay quên nhất.
5. **Chạy script kiểm** (mục 1).
6. Commit → PR → merge vào `main` (Vercel tự deploy).
7. **Yêu cầu lập chỉ mục** URL mới trong Google Search Console (mục 13).

---

## 3. JSON-LD & DẤU XUNG ĐỘT GIT

**Đã dính:** schema hỏng do nối chuỗi bằng tay; `<<<<<<< HEAD` lọt vào file đã commit **2 lần**.

- Sửa schema thì **parse JSON → sửa object → dump lại**. KHÔNG cắt/nối chuỗi JSON bằng regex.
- Trước khi ghi file: `json.loads()` mọi khối `application/ld+json`.
- Sau khi gộp nhánh: `grep -rn '^<<<<<<< ' --include=index.html .` phải ra rỗng.
- **[CẤM]** regex DOTALL `.*?` để xoá/sửa khối HTML — đã gây mất dữ liệu.

---

## 4. THẺ CƠ BẢN

- `<title>` **duy nhất toàn site**, mô tả **duy nhất**. Trùng = tự cắn nhau.
- Đúng **1 thẻ `<h1>`** mỗi trang.
- `canonical` **có dấu `/` cuối** và **tự trỏ chính nó** với mọi trang giao dịch
  (lô, nhà, hub, trang khu, trang giá). Chỉ bài thông tin trong `thi-truong/`,
  `ve-nam-ban/`, `namban-notes/` mới được canonical sang Panorama (Hiến pháp 3 web).
- `og:image` + `twitter:image` = **ảnh của chính lô này**, không phải `og-namban.jpg` chung.

---

## 5. ẢNH — CORE WEB VITALS (yếu tố xếp hạng thật)

**Đã dính:** gán `fetchpriority="high"` cho **logo** và `loading="lazy"` cho **ảnh hero**
→ làm **chậm LCP**, tức hại đúng thứ đang muốn cải thiện.

Luật:
| Ảnh | Thuộc tính |
|---|---|
| Logo / favicon | **KHÔNG** `fetchpriority`, **KHÔNG** `lazy` |
| Ảnh hero (ảnh nội dung đầu tiên) | `fetchpriority="high"`, **KHÔNG** `lazy` |
| Mọi ảnh còn lại | `loading="lazy"` |
| Tất cả | `alt` mô tả đúng cảnh + `width`/`height` (chống nhảy layout) |

Ngoại lệ hợp lệ: khung lightbox rỗng `<img id="lbImg" src="">` do JS đổ vào — không cần kích thước.

---

## 6. NỐI DÂY — BƯỚC HAY QUÊN NHẤT

**Đã dính:** hub thiếu **13 lô** trong ItemList; `/hoi-dap/` mồ côi 0 inbound;
2 trang trỏ tới `/dat-nam-ban-tren-2-ty/` khi trang **chưa tồn tại**.

Mỗi tin mới phải có **đủ 4** thứ:
1. **`sitemap.xml`** — thêm URL (có dấu `/` cuối) + `lastmod` hôm nay.
2. **ItemList của hub** — `dat-nen/*` → `dat-nen-nam-ban`; `nha-ban/*` → `nha-ban-nam-ban`.
3. **Ít nhất 1 link trỏ tới** (không được mồ côi) — thường là card ở hub + trang khu hợp.
4. **Trang khu / facet hợp** nếu có (`dat-ho-bai-cong-nam-ban`, `dat-gia-lam-nam-ban`,
   `dat-nam-ban-duoi-1-ty`, `dat-nam-ban-1-2-ty`, `dat-nam-ban-tren-2-ty`, `dat-vuon-nam-ban`…).

**Ngược lại:** đã đặt link tới trang nào thì **trang đó phải tồn tại**. Không link tới trang "sẽ làm sau".

---

## 7. REDIRECT — LỖI NẶNG NHẤT ĐÃ TỪNG DÍNH

Site đặt `trailingSlash: true`. Vercel **thêm dấu `/` TRƯỚC** rồi mới so khớp `redirects`.
Vì mọi `source` trong `vercel.json` đều thiếu `/`, **toàn bộ 36 redirect trả 404** —
mọi URL cũ chết, mất sạch link equity. Phải curl thật mới phát hiện.

**Luật:** mỗi redirect phải có **biến thể `source` kết thúc bằng `/`**.
```json
{ "source": "/duong-dan-cu",  "destination": "/dich/", "permanent": true },
{ "source": "/duong-dan-cu/", "destination": "/dich/", "permanent": true }
```
Kiểm thật (curl trên mạng mở, không đoán):
Actions → **"Kiểm chuỗi chuyển hướng & 404 (live)"** → Run workflow.
`hop=2` với URL thiếu `/` là **bình thường** (`/x` → `/x/` → đích).

---

## 8. GIỌNG VĂN

- **Không emoji** ở bất kỳ đâu (nút, chip, badge, tiêu đề, nội dung).
- **Không ngôi thứ nhất** (mình / tôi / em / chúng tôi). Cần nhắc chủ thể → **"Nam Ban Villas"**.
  Ngôi thứ 2 (`bạn`, `anh/chị`) **được phép**.
  *Lưu ý bộ dò báo nhầm:* "trẻ **em**", "**xem**", "th**êm**" — không phải lỗi.
  Miễn trừ có chủ đích: tuỳ bút `namban-notes/`, nút "Tôi sắp MUA" (lời khách), trích dẫn.
- Thẳng, số thật, không tính từ rỗng ("tuyệt đẹp", "lý tưởng"). Không sến, không trẻ con.
- **Không bịa** số liệu / testimonial / tên người.

---

## 9. SCHEMA CHO TIN RAO

- `Product` bắt buộc. Có giá → `offers` đủ `price` + `priceCurrency: "VND"` + `availability`
  (+ `priceValidUntil` để Google không báo giá hết hạn).
  Lô **"giá đang cập nhật"** → **không cần** `offers`, đó là đúng.
- `FAQPage` 3–4 câu, **câu đầu trả lời thẳng** (giá / pháp lý / cách Đà Lạt / rủi ro) — đây là
  thứ AI trích dẫn.
- `BreadcrumbList` trỏ **hub thật**: `/dat-nen-nam-ban/`, `/nha-ban-nam-ban/`.
  **KHÔNG** trỏ `/dat-nen/` hay `/nha-ban/` — đó là 404.
- Cụm nhiều giá → `AggregateOffer` (`lowPrice`/`highPrice`/`offerCount`).

---

## 10. GEO

- `geo.region = "VN-35"` (mã ISO Lâm Đồng — **không** tự chế "VN-LB").
- Toạ độ Nam Ban: `11.8347, 108.2622`. **Đã dính:** trang chủ để `11.7586, 108.2432` — lệch ~8km.
- Luôn ghi: Nam Ban · Lâm Hà · Lâm Đồng + khoảng cách Đà Lạt / sân bay Liên Khương + mốc gần
  (chợ Thăng Long, chùa Linh Ẩn, Thác Voi, hồ Bãi Công, ĐT725).
- Hành chính: **"thị trấn Nam Ban" cũ, nay là xã Nam Ban** (sau 1/7/2025). Nêu cả 2 cách gọi
  trong mô tả/FAQ để bắt cả 2 kiểu người ta tìm; schema dùng đơn vị hiện hành.

---

## 11. UX — ĐÍCH TỐI THƯỢNG LÀ KHÁCH BẤM GỌI/ZALO

- Nút **Gọi + Zalo** dễ bấm: price card sidebar + thanh dán đáy mobile. Không hy sinh nút liên hệ lấy thẩm mỹ.
- Khối **đọc rủi ro**: điểm mạnh / **"điều cần quan tâm" tối đa 3 gạch, thường 1–2**.
  Không bịa rủi ro để lấp chỗ.
- SĐT duy nhất toàn site: **0978 758 788**.
- Kiểm cả **desktop lẫn mobile** bằng đọc code + breakpoint (không chụp ảnh — tốn thời gian).

---

## 12. TIN TRÙNG (chú gửi lại lô/cụm đã đăng)

**KHÔNG tạo trang mới** (Google phạt trùng nội dung). Mở đúng trang cũ:
- Thêm ảnh/sơ đồ mới đẹp hơn, bổ sung specs/mô tả.
- Bump `dateModified` + dòng hiển thị `Cập nhật: DD/MM/YYYY`.
- Không đụng card hub/sitemap nếu đã có sẵn.

---

## 13. SAU KHI ĐĂNG — ĐỪNG BỎ QUÊN

1. **Yêu cầu lập chỉ mục** URL mới: Search Console → ô "Kiểm tra URL" → dán URL →
   **Yêu cầu lập chỉ mục** (~10–12 URL/ngày).
2. Facebook tự đăng (robot) — không cần soạn tay.

**Bối cảnh quan trọng:** hiện có **82 trang Google "đã phát hiện, chưa lập chỉ mục"** —
đây là **hạn mức thu thập** của site còn mới, không phải lỗi kỹ thuật. Nghĩa là:
> **Đẻ thêm trang khi chưa có hàng thật là phản tác dụng** — càng chia mỏng hạn mức.
> Chỉ tạo trang mới khi có **lô thật** để đưa lên. Ưu tiên ép Google đọc trang đã có.

---

## 14. MẪU BÁO CÁO (ngắn, không giải thích dài)

```
Đã đăng: <tên lô/cụm>
👉 https://nambanvillas.vn/<đường-dẫn>/
Kiểm tra: SẠCH (178 trang, 0 lỗi)
```
Nhiều trang → mỗi link 1 dòng.
