# Ô CẬP NHẬT THỊ TRƯỜNG — quy trình cho phiên tự động (mỗi ~4 ngày)

> Vị trí: đầu trang `thi-truong/index.html`, giữa 2 marker
> `<!-- MARKET-DIGEST:START ... -->` và `<!-- MARKET-DIGEST:END -->`.
> Mục tiêu: mỗi vài ngày đăng 1–3 mục cập nhật MỚI về Nam Ban + thị trường BĐS
> Lâm Đồng/cao nguyên, viết lại theo góc nhìn Nam Ban Villas.

## LUẬT VÀNG (bất biến)
- **KHÔNG trỏ link sang web khác. KHÔNG hotlink ảnh web khác. KHÔNG copy nguyên văn.**
  Lấy Ý từ báo → VIẾT LẠI. Ghi chung "Tổng hợp từ báo chí công khai", không dán URL.
- **KHÔNG bịa số.** Giữ đúng số liệu nguồn; không chắc thì bỏ, đừng đoán.
- **KHÔNG xưng ngôi thứ nhất** (mình/tôi/em/chúng tôi). Cần nhắc chủ thể → "Nam Ban Villas".
- Giọng: thẳng, số thật, đẳng cấp-thân thiện — "đọc rủi ro, không bán giấc mơ". Không sến, không emoji.
- Chủ đề hợp: thị trường/giá đất Lâm Đồng – Nam Ban, quy hoạch, hạ tầng (cao tốc Dầu Giây–Liên Khương, sân bay Liên Khương, tuyến tránh), chính sách đất đai, đầu tư farmstay/nghỉ dưỡng cao nguyên. Ưu tiên tin ăn nhập trực tiếp Nam Ban.

## CÁC BƯỚC
1. **Tìm tin mới** (WebSearch) trong ~7 ngày gần nhất về các chủ đề trên. Chọn 1–3 tin đáng.
   Đối chiếu để không trùng mục đã có trong ô (đọc các `<h3 class="mkt-h">` hiện có).
2. **Viết mỗi mục** theo mẫu HTML dưới — 2–3 câu tóm ý + 1 dòng "Với đất Nam Ban:" (nghĩa là gì với người mua Nam Ban).
3. **Chèn** các mục mới NGAY DƯỚI dòng `<!-- MARKET-DIGEST:START ... -->` (mục mới lên đầu). Cập nhật ngày trong `.mkt-date`. **Giữ tối đa 8 mục** — xoá bớt mục cũ nhất phía dưới nếu quá.
4. Cập nhật dòng `.mkt-src` cuối ô: đổi ngày "(đến D/M/2026)".
5. Cập nhật `lastmod` của `thi-truong/` trong `sitemap.xml` sang ngày hôm nay.
6. Verify JSON-LD còn hợp lệ, không có ngôi thứ nhất trong ô. Commit + PR + merge vào main (deploy).

## MẪU 1 MỤC (dán ngay dưới MARKET-DIGEST:START)
```html
  <article class="mkt-item">
    <div class="mkt-date">D/M/2026</div>
    <div>
      <h3 class="mkt-h">Tiêu đề ngắn, có từ khoá</h3>
      <p class="mkt-p">2–3 câu tóm ý tin, số thật, không link ngoài.</p>
      <p class="mkt-nb"><strong>Với đất Nam Ban:</strong> 1 câu nghĩa là gì với người mua Nam Ban.</p>
    </div>
  </article>
```

## CADENCE
- Routine (scheduled trigger) chạy **mỗi ~4 ngày**, tạo phiên mới thực hiện đúng quy trình này.
- Nếu tuần đó không có tin gì đáng → KHÔNG đăng cho có; ghi nhận và chờ kỳ sau (thà ít mà thật).
