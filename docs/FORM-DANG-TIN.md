# FORM ĐĂNG TIN RAO — NAM BAN VILLAS
## Chuẩn để bot (và người) viết mỗi tin rao giống hệt nhau, tối ưu AEO/SEO/GEO/UX

> Áp dụng cho trang `/thi-truong/tin-rao-dat-nam-ban-moi/` (tin thị trường, chưa kiểm chứng).
> KHÁC với lô Villas đã kiểm tra ở `/dat-nen-nam-ban/`. Đọc kèm `HIEN-PHAP-3-WEB.md` (Villas = giao dịch, lô thật, số thật).

---

## BƯỚC 1 — LỌC: tin nào ĐÁNG đăng, tin nào BỎ

Chỉ đăng tin đạt **cả 4** tiêu chí (thiếu 1 → bỏ, thà ít mà chất):
1. **Có giá rõ** (số cụ thể, không "liên hệ", không "giá tốt").
2. **Có diện tích rõ** (m², tốt nhất có kích thước cạnh).
3. **Vị trí cụ thể** (khu/thôn/gần mốc: Đông Thanh, Mê Linh, gần Thác Voi, gần Hồ Bãi Công…), thuộc **xã Nam Ban, Lâm Hà, Lâm Đồng**.
4. **Có tín hiệu pháp lý** (sổ hồng/sổ đỏ/thổ cư bao nhiêu m²). Ưu tiên tin có sổ.

**Ưu tiên** (nếu nhiều tin đạt): có thổ cư cao · mặt tiền đường nhựa · gần tiện ích/mốc du lịch · giá hợp mặt bằng 2–9 triệu/m².

Mỗi ngày chọn **1–2 tin** tốt nhất. Không đủ chất → **không đăng** (thà trống hơn rác).

### 1a. LOẠI THẲNG nếu tin chứa từ ngữ "rác" (blocklist)
Bỏ ngay nếu tiêu đề/mô tả có kiểu:
- **Hứa hão / thổi phồng lợi nhuận:** "chắc chắn lời", "lời ngay", "mua là thắng", "x2/x3 tài khoản", "sinh lời khủng", "một vốn bốn lời", "10 năm có 1", "kèo thơm".
- **Tạo sốt giả:** "sốt đất", "siêu hiếm", "cực phẩm", "độc nhất", "duy nhất còn lại", "giá sốc", "rẻ nhất thị trường".
- **Bom tấn / câu view rỗng:** "siêu phẩm", "vị trí vàng", "đất vàng", "không mua là tiếc", quá nhiều dấu "!!!", emoji.
- **Tiêu cực câu kéo quá mức:** "ngộp bank", "cắt lỗ sâu", "bán tháo gấp trong đêm", "vỡ nợ bán rẻ" (dùng để dụ, không có số thật).
→ Những từ này = tín hiệu tin kém chất lượng. Google/AI cũng hạ tin dạng này.

### 1b. CHECKLIST SỐ LIỆU (tin tốt phải đủ dữ kiện — chấm điểm)
Đếm số dữ kiện tin có; **bắt buộc ≥ 4/7**, ưu tiên tin nhiều điểm hơn:
1. ☐ Diện tích (m²)
2. ☐ Kích thước cạnh / chiều ngang mặt tiền (VD 10×63m, ngang 12m)
3. ☐ Đất thổ cư bao nhiêu m² (hoặc "full thổ")
4. ☐ Giá cụ thể (số, không "liên hệ")
5. ☐ Vị trí cụ thể — gần mốc nào (Đông Thanh, Mê Linh, gần Thác Voi, Hồ Bãi Công, chợ, trường…)
6. ☐ Loại đường / mặt tiền (đường nhựa/bê tông rộng mấy mét, mấy mặt tiền)
7. ☐ Pháp lý (sổ hồng/đỏ riêng, công chứng ngay)
→ Tin đủ 6–7 mục = tin tốt nhất, ưu tiên đăng. Tin < 4 mục = bỏ.

---

## BƯỚC 2 — THÔNG SỐ CẦN BẮT (từ tin gốc)

Rút cho được, theo thứ tự ưu tiên: **loại đất → diện tích (+kích thước) → thổ cư (m²) → giá (+ giá/m² nếu tính được) → vị trí/khu → mặt tiền/đường → view/đặc điểm → pháp lý (sổ) → nguồn (URL)**.
- Không có số nào thì bỏ trống, **không bịa**.
- **KHÔNG lấy: số điện thoại, tên người bán, ảnh của tin gốc** (bản quyền).

---

## BƯỚC 3 — VIẾT (viết lại bằng lời mình, KHÔNG copy)

Mỗi tin = 1 dòng `<li>`, gồm 3 phần theo đúng thứ tự:

**(A) Tiêu đề in đậm** — công thức: `Loại đất + diện tích + đặc điểm mạnh nhất + khu — thổ cư/giá`
> VD: *Đất vườn 622m² trung tâm Nam Ban — vườn bơ xen cà phê, sẵn 100m² thổ cư*

**(B) Mô tả 2–3 câu** — nêu: đặc điểm nổi bật + hợp ai + **1 rủi ro CẦN KIỂM** (bắt buộc, đúng chất "đọc rủi ro").
> VD: *…hợp người vừa giữ vườn vừa dựng nhà nhỏ. Cần kiểm tra: phần nông nghiệp còn lại có chuyển thổ thêm được không, ranh có khớp sổ.*

**(C) Ghi chú + nguồn** — luôn có: *"Giá là mức rao / tin thị trường, chưa kiểm chứng"* + link `<a ... rel="nofollow noopener">Nguồn</a>`.

**Mỗi ≥3 ngày** thêm 1 đoạn `Quan sát thị trường:` 2–3 câu (xu hướng thật + link nguồn).

---

## BƯỚC 4 — GIỌNG VĂN (bất biến)

- Trầm, thật, thẳng. Đọc rủi ro, KHÔNG hô hào.
- **CẤM tính từ rỗng:** tuyệt đẹp, lý tưởng, hoàn hảo, siêu phẩm, cực hiếm, số 1, giá sốc.
- KHÔNG đụng chạm ai (không "cò", "lừa đảo").
- Số thật, không làm tròn tô hồng. Không chắc thì ghi "mức rao, cần đối chiếu".

---

## BƯỚC 5 — HTML MẪU (bot xuất đúng khối này, chèn dưới `<!-- DAILY-DIGEST:START -->`)

```html
<!-- DAY:YYYY-MM-DD -->
<h2>Ngày D/M/YYYY</h2>
<ul style="line-height:1.9;color:#3D3D3D;font-size:.95rem">
  <li><strong>TIÊU ĐỀ</strong> — MÔ TẢ 2–3 câu kèm 1 rủi ro cần kiểm. Tin thị trường, chưa kiểm chứng. <a href="URL" target="_blank" rel="nofollow noopener">Nguồn</a></li>
  <!-- tối đa 2 li/ngày -->
</ul>
<!-- (mỗi ≥3 ngày) -->
<p style="background:#F0F4F1;border-radius:8px;padding:12px 16px;font-size:.92rem;color:#3D3D3D"><strong style="color:#1A3D2B">Quan sát thị trường:</strong> … <a href="URL" target="_blank" rel="nofollow noopener">Nguồn</a></p>
```

Sau khi chèn: cập nhật `"dateModified"` và dòng `article-cat` sang ngày mới; giữ tối đa 20 mục ngày gần nhất.

---

## VÌ SAO FORM NÀY TỐI ƯU

- **AEO:** mỗi tin là 1 đơn vị dữ kiện gọn (loại/diện tích/giá/vị trí) → AI trích thẳng khi ai hỏi "đất Nam Ban đang bán loại nào giá bao nhiêu".
- **SEO:** freshness mỗi ngày (dateModified) + key "tin rao đất nam ban", "giá đất nam ban hôm nay"; `rel="nofollow"` ở link ngoài để không rò link-juice.
- **GEO:** luôn gắn địa danh xã Nam Ban/Lâm Hà/Lâm Đồng + trang đã có `spatialCoverage`.
- **UX/UI:** khối ngắn, in đậm số quan trọng, mới nhất lên đầu, 1 nút Zalo duy nhất; rủi ro nêu rõ → tạo niềm tin, không gây lo.
- **Thương hiệu:** tách bạch "tin chưa kiểm chứng" vs "lô Villas đã kiểm tra" → giữ lời hứa, và mọi tin đều dẫn về Zalo để Villas kiểm giúp (biến tin người khác thành lead của mình).
