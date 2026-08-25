# TIN RAO POSTING KIT — dán vào ô Claude khác để đăng tin
*Dán toàn bộ file này. Ô nào có GitHub (MCP hoặc quyền commit repo nambanvillas) là đăng được ngay.*

## ĐÍCH ĐĂNG
- Repo: **doanquocduyet/nambanvillas**, branch dev **claude/dreamy-ritchie-xBezi** → PR + squash merge `main` (Vercel auto-deploy).
- File: **`thi-truong/tin-rao-dat-nam-ban-moi/index.html`**
- Chèn khối ngày MỚI ngay **dưới dòng** `<!-- DAILY-DIGEST:START ...`, mới nhất lên đầu. Giữ tối đa 20 mục (`<!-- DAY:YYYY-MM-DD -->`). Nếu đã có mục cùng ngày → thay, không thêm trùng.
- Sau khi chèn: sửa `"dateModified":"YYYY-MM-DD"` và dòng `<p class="article-cat">Quan sát thị trường · Cập nhật D/M/YYYY` sang ngày mới.

## LỌC (chỉ đăng tin CHẤT)
- Đủ **≥4/7 dữ kiện**: diện tích · kích thước/mặt tiền · thổ cư(m²) · giá bằng số · vị trí cụ thể (gần mốc nào, thuộc xã Nam Ban/Lâm Hà/Lâm Đồng) · loại đường · pháp lý(sổ). Ưu tiên đủ 6–7.
- **LOẠI THẲNG** nếu có từ rác: chắc chắn lời/lời ngay/mua là thắng/x2 tài khoản/sinh lời khủng · sốt đất/siêu hiếm/cực phẩm/độc nhất/giá sốc/rẻ nhất · siêu phẩm/đất vàng/vị trí vàng · ngộp bank/cắt lỗ sâu/bán tháo gấp. Hoặc không giá, mơ hồ vị trí → bỏ.
- Mỗi ngày **1–2 tin** tốt nhất. Không đủ chất → **không đăng** (thà trống hơn rác).

## VIẾT (viết lại bằng lời mình, KHÔNG copy nguyên văn)
- **Tiêu đề:** `Loại đất + diện tích + đặc điểm mạnh nhất + khu — thổ cư/giá`.
- **Mô tả 2–3 câu:** đặc điểm + hợp ai + **BẮT BUỘC 1 rủi ro cần kiểm** + kết "Tin thị trường, chưa kiểm chứng."
- Số thật, KHÔNG bịa. **TUYỆT ĐỐI KHÔNG lấy số điện thoại/tên người bán/ảnh/video** (bản quyền).
- `source` = link gốc (tin/video); nếu từ video ghi "Nguồn: video kênh [tên]".
- Giọng: trầm, thật, đọc rủi ro, KHÔNG hô hào, KHÔNG tính từ rỗng.
- Mỗi ≥3 ngày thêm 1 đoạn "Quan sát thị trường".

## HTML MẪU (xuất đúng khối này, chèn dưới DAILY-DIGEST:START)
```html
<!-- DAY:2026-07-03 -->
<h2>Ngày 3/7/2026</h2>
<ul style="line-height:1.9;color:#3D3D3D;font-size:.95rem">
  <li><strong>TIÊU ĐỀ</strong> — MÔ TẢ 2–3 câu kèm 1 rủi ro cần kiểm. Tin thị trường, chưa kiểm chứng. <a href="URL" target="_blank" rel="nofollow noopener">Nguồn</a></li>
  <!-- tối đa 2 li/ngày -->
</ul>
<!-- (mỗi ≥3 ngày) thêm: -->
<p style="background:#F0F4F1;border-radius:8px;padding:12px 16px;font-size:.92rem;color:#3D3D3D"><strong style="color:#1A3D2B">Quan sát thị trường:</strong> … <a href="URL" target="_blank" rel="nofollow noopener">Nguồn</a></p>
```

## CÁCH ĐĂNG (2 tình huống)
- **Ô có GitHub (MCP/commit):** đọc file `thi-truong/tin-rao-dat-nam-ban-moi/index.html` trên branch `claude/dreamy-ritchie-xBezi`, chèn khối mới sau marker, commit + tạo PR + squash merge main. Verify HTML hợp lệ trước khi push. KHÔNG dùng regex DOTALL để sửa — chèn bằng str_replace tại marker.
- **Ô KHÔNG có GitHub:** chỉ **xuất khối HTML** theo mẫu trên rồi đưa cho người có quyền (hoặc phiên Villas có GitHub) dán vào file + đăng.

## ẢNH — CẮT GỌT TỰ ĐỘNG (chỉ ảnh chủ web tự chụp / có bản quyền)
> **CẤM** tải/đăng lại ảnh của tin gốc / môi giới khác (bản quyền). Chỉ xử ảnh chú tự chụp hoặc chú xác nhận có quyền đăng.

Script: **`scripts/prep-anh.py`** — tự động cho ra ảnh web đẹp, chuẩn SEO:
1. Auto-xoay theo EXIF → **xoá sạch EXIF** (bay cả GPS toạ độ, không lộ vị trí thật).
2. **Smart-crop** theo tỉ lệ đích — giữ vùng nhiều chi tiết nhất (gradient-energy), không cắt cụt chủ thể như center-crop.
3. Resize cạnh dài (mặc định 1280px) + sharpen nhẹ cho nét.
4. Nén JPEG dò chất lượng chạm ~mục tiêu KB (mặc định 150; ảnh nhiều lá cây có thể ~200KB — chấp nhận, bằng ảnh hero site đang có).
5. Đặt tên chuẩn: `images/listings/<slug>/1.jpg 2.jpg 3.jpg …` (mới nhất/đẹp nhất để `1.jpg` làm hero + og:image).

Cách chạy (ảnh **hero** ép 16:9 như listing site; ảnh **phòng/dọc** để `keep` khỏi mất trần-sàn):
```
python3 scripts/prep-anh.py <slug> --ratio 16:9 --start 1 hero.jpg
python3 scripts/prep-anh.py <slug> --ratio keep --start 2 phong1.jpg phong2.jpg …
```
Tham số: `--ratio 16:9|4:3|3:2|1:1|keep` · `--kb 150` · `--long 1280` · `--out images/listings` · `--start N`.
Alt ảnh: mô tả đúng cảnh + địa danh (vd `Villa mini Mê Linh Nam Ban — mặt tiền sân vườn`). KHÔNG nhồi key.

## LƯU Ý HỆ 3 WEB
- Đây là **tin thị trường CHƯA kiểm chứng** — khác lô Villas đã kiểm tra ở `/dat-nen-nam-ban/`. Không lẫn.
- Villas KHÔNG link sang Panorama. Mọi tin dẫn về Zalo 0978 758 788.
