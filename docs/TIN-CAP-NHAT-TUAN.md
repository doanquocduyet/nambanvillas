# TIN CẬP NHẬT HÀNG TUẦN — cho box Claude Code đăng tin

> Mỗi TUẦN đăng 1 bài mới cho mục "Tin Liên Quan" ở trang Thị Trường.
> Nguyên tắc VÀNG: **KHÔNG trỏ link sang web khác. KHÔNG dùng ảnh web khác. KHÔNG copy.**
> Lấy Ý từ báo ngoài → VIẾT LẠI theo hướng Nam Ban Villas → chèn ẢNH của mình.

---

## MỖI TUẦN LÀM 1 LẦN

### 1) Chọn 1 tin nguồn hợp hướng
Tìm 1 bài mới (tuần đó) từ báo/nguồn BĐS: CafeF, VnEconomy, Báo Đầu Tư, Batdongsan,
Guland, báo Lâm Đồng… có nội dung liên quan: **thị trường đất/BĐS Lâm Đồng – Nam Ban,
giá đất, quy hoạch, hạ tầng (cao tốc, sân bay, tuyến tránh), chính sách đất đai, đầu tư
farmstay/nghỉ dưỡng cao nguyên.** Ưu tiên tin ăn nhập trực tiếp với Nam Ban.

### 2) VIẾT LẠI (không copy)
- Diễn đạt lại bằng giọng Villas: **thẳng, số thật, "đọc rủi ro không bán giấc mơ".**
- **Kéo về Nam Ban:** thêm 1–2 đoạn "điều này nghĩa gì với đất Nam Ban / người mua ở Nam Ban".
- Giữ đúng số liệu nguồn (không bịa). Không chắc thì bỏ, đừng đoán.
- Có thể ghi chung "Tổng hợp từ báo chí" — **TUYỆT ĐỐI không dán URL/link nguồn ngoài.**

### 3) Ảnh của Nam Ban Villas
- Dùng ảnh trong `images/` (ảnh thật Nam Ban) hoặc ảnh chú cung cấp. **KHÔNG hotlink ảnh web khác.**
- Ảnh mới → nén: `python3 scripts/nen-anh.py images/articles/<slug>.jpg`

### 4) Tạo trang bài nội bộ
`thi-truong/<slug>/index.html` — theo mẫu bài thị trường đã có (copy 1 bài cũ rồi sửa):
- Schema `NewsArticle` (headline, datePublished, publisher Nam Ban Villas, image nội bộ).
- Breadcrumb, ảnh hero (ảnh của mình), thân bài, khối CTA Gọi/Zalo cuối bài.
- **Không có link ra ngoài trong toàn bài.**

### 5) Gắn lên trang Thị Trường
- Thêm 1 card vào lưới "Phân Tích & Quy Hoạch" (đầu lưới).
- Cập nhật mục **"Tin Liên Quan"** (`thi-truong/index.html`): đưa bài mới lên **số 01**,
  giữ tối đa 3 bài, bài cũ nhất tụt xuống/gỡ. Tất cả link là **nội bộ `/thi-truong/...`**.

### 6) Sitemap + feed
- Thêm URL bài vào `sitemap.xml` (changefreq weekly).
- Nếu có `feed.xml` → thêm item.

---

## LUẬT CẤM (nhắc lại)
- ❌ Không đặt bất kỳ link `http(s)://` ra web ngoài trong bài hay mục Tin Liên Quan.
- ❌ Không dùng ảnh của web khác (kể cả nhúng link ảnh).
- ❌ Không copy nguyên văn — phải viết lại.
- ❌ Không bịa số liệu, tên người, testimonial.
- ✅ Dùng `str_replace` khớp chính xác, không regex DOTALL. Verify rồi push → PR → merge.

## TÓM TẮT 1 DÒNG
Mỗi tuần: đọc 1 tin báo hợp Nam Ban → viết lại giọng Villas + ảnh của mình → tạo bài
`/thi-truong/<slug>/` → đưa lên số 01 mục Tin Liên Quan (link nội bộ) → sitemap. Không trỏ web khác.
