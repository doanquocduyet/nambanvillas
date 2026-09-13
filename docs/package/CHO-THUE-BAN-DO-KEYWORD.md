# BẢN ĐỒ KEYWORD CHO THUÊ NAM BAN
## Lộ trình chiếm top search mảng cho thuê — mở URL theo hàng thật, không mở trước

**Mục tiêu cuối:** khách search bất cứ kiểu gì về thuê ở Nam Ban đều ra Nam Ban Villas, rồi bấm gọi **0978 758 788**.

---

## LUẬT NỀN — 1 Ý ĐỊNH = 1 URL

Cắn key (cannibalization) là cách chắc chắn nhất để tự thua: hai trang cùng nhắm một ý định thì Google chia điểm cho cả hai, không trang nào lên. Mỗi ô dưới đây chỉ được có **đúng một** URL đại diện.

| Ý định khách | URL đại diện | Trạng thái |
|---|---|---|
| Tổng quát "cho thuê Nam Ban" | `/cho-thue/` | **ĐÃ MỞ** |
| Thuê ở dài hạn | `/cho-thue/` mục `#o-dai-han` | neo trong hub |
| Thuê nhà nguyên căn | `/cho-thue/` mục `#nguyen-can` | neo trong hub |
| Thuê phòng trọ, nhà trọ | `/cho-thue/` mục `#phong-tro` | neo trong hub |
| Thuê để ở thử trước khi mua đất | `/cho-thue/` mục `#o-thu` | neo trong hub |
| Thuê nghỉ ngắn ngày (homestay, villa theo đêm) | `/cho-thue/` mục `#nghi-ngan` | neo trong hub |
| Thuê mặt bằng kinh doanh | `/cho-thue/` mục `#kinh-doanh` | neo trong hub |
| Chủ nhà muốn cho thuê (ký gửi) | `/cho-thue/` mục `#gui-tai-san` | neo trong hub |
| Bảng giá thuê Nam Ban | `/cho-thue/` mục giá | neo trong hub |

**Vì sao neo (`#`) chứ chưa tách URL:** Villas hiện có **0 tin cho thuê** trong kho. Mở `/cho-thue-villa-nam-ban/` khi chưa có villa nào cho thuê = trang rỗng — Google xếp là thin content, và khách vào thấy trống thì không gọi. Đúng lỗi đã mắc với chip "Nam Hà" hiện 0 sản phẩm.

**Điều kiện tách URL riêng:** một nhánh có **từ 3 tin thật trở lên** trong `data/tin-thue/` thì mới cắt mục đó ra thành URL riêng, và mục trong hub đổi thành đoạn tóm tắt + link sang.

---

## HAI CẶP KEY DỄ TƯỞNG GIỐNG MÀ KHÁC HẲN Ý ĐỊNH

Đây là chỗ dễ tự đánh nhau nhất khi tách URL sau này.

| Keyword | Người gõ là ai | URL tương lai |
|---|---|---|
| `homestay nam ban` | **khách du lịch** tìm chỗ nghỉ — muốn ảnh, giá/đêm, vị trí | `/homestay-nam-ban/` |
| `cho thuê homestay nam ban` | **chủ cơ sở** muốn cho thuê, hoặc người muốn thuê lại cả homestay để kinh doanh | `/cho-thue-homestay-nam-ban/` |
| `villa nam ban` | người tìm **chỗ nghỉ** hoặc tìm hiểu villa ở Nam Ban | `/villa-nam-ban/` |
| `villa nam ban cho thuê` | người muốn **thuê villa** | `/cho-thue/biet-thu-nam-ban/` |

Gộp hai vế vào một trang là cách chắc chắn để cả hai đều không lên.

## VÙNG 7 · Ở THỬ TRƯỚC KHI MUA — vùng nối thẳng vào phễu đất

`thuê nhà ở thử nam ban` · `ở thử nam ban trước khi mua đất` · `thuê nhà nam ban vài tháng` · `sống thử ở nam ban`

Đây là nhóm giá trị nhất: người đã tính mua đất Nam Ban, chỉ chưa chắc có hợp không. Thuê vài tháng rồi mua là quyết định tốt hơn cho khách, và vẫn dẫn về đúng nghiệp vụ chính của Villas. Hiện ở `#o-thu`.

## SỐ THAM CHIẾU THỊ TRƯỜNG (ghi nhận trên tin rao, chưa xác minh từng căn)

| Loại | Mức ghi nhận | Ghi chú |
|---|---|---|
| Nhà nguyên căn | 4 – 8 triệu/tháng | đầu thấp: nhà nhỏ vài chục m²; đầu cao: mới xây đủ nội thất |
| Phòng trọ | ~800 nghìn – hơn 1 triệu/tháng | điện nước tính riêng theo số |
| Nhà đủ nội thất (xác minh thật) | 5 · 12 · 13 triệu/tháng | ba căn của chính Villas, đang có khách thuê |

**Luật:** số "ghi nhận trên tin rao" phải luôn ghi rõ là chưa xác minh. Số "xác minh thật" mới được dùng làm mốc.

---

## 6 VÙNG KEY (ocean) — thứ tự ưu tiên theo hàng có trước

### 1 · Ở DÀI HẠN — mở trước nhất khi có hàng
`cho thuê nhà nam ban` · `nhà cho thuê nam ban` · `thuê nhà nam ban lâm hà` · `cho thuê nhà nguyên căn nam ban` · `thuê phòng nam ban` · `phòng trọ nam ban` · `nhà trọ nam ban giá rẻ` · `cho thuê nhà đông thanh lâm hà` · `cho thuê nhà mê linh lâm hà`
→ URL tương lai: `/cho-thue/nha-nam-ban/`

### 2 · NGHỈ NGẮN NGÀY
`homestay nam ban` · `homestay nam ban giá rẻ` · `thuê homestay nam ban` · `farmstay nam ban` · `villa nam ban` · `thuê villa nam ban theo đêm` · `homestay gần thác voi` · `chỗ ở nam ban lâm hà`
→ URL tương lai: `/cho-thue/homestay-nam-ban/`

### 3 · BIỆT THỰ / VILLA THUÊ
`biệt thự nam ban cho thuê` · `cho thuê biệt thự nam ban` · `biệt thự mới xây nam ban cho thuê` · `thuê biệt thự nghỉ dưỡng lâm hà` · `villa nguyên căn nam ban`
→ URL tương lai: `/cho-thue/biet-thu-nam-ban/`

### 4 · MẶT BẰNG KINH DOANH
`cho thuê mặt bằng nam ban` · `thuê kho nam ban` · `mặt bằng kinh doanh nam ban` · `cho thuê quán cà phê nam ban` · `thuê xưởng lâm hà`
→ URL tương lai: `/cho-thue/mat-bang-nam-ban/`

### 5 · ĐẤT / VƯỜN THUÊ
`thuê đất nam ban` · `cho thuê đất trồng nam ban` · `thuê vườn cà phê lâm hà` · `thuê đất làm homestay nam ban`
→ URL tương lai: `/cho-thue/dat-nam-ban/`

### 6 · PHÍA CHỦ NHÀ (nguồn hàng — vùng ít cạnh tranh nhất, giá trị cao nhất)
`ký gửi cho thuê nam ban` · `môi giới cho thuê nam ban` · `cho thuê nhà hộ nam ban` · `quản lý nhà cho thuê lâm hà`
→ hiện nằm ở `#gui-tai-san`. **Đây là vùng nên đánh mạnh ngay** vì không cần kho hàng — chính nó tạo ra kho hàng.

---

## BỐN TRẠNG THÁI CỦA MỘT TIN THUÊ — KHÔNG BAO GIỜ 404

Tin thuê quay vòng nhanh hơn tin bán rất nhiều. Xoá trang khi hết hàng = đốt hết điểm SEO đã tích, và khách bấm từ Google vào gặp 404 thì mất luôn.

| Trạng thái | Trang làm gì |
|---|---|
| **CÒN TRỐNG** | hiện đầy đủ, nút Gọi/Zalo nổi bật |
| **ĐANG GIỮ CHỖ** | giữ nguyên, gắn nhãn "đang giữ chỗ", vẫn mời liên hệ để vào danh sách chờ |
| **ĐÃ THUÊ** | giữ trang, gắn nhãn "đã có khách", đổi CTA thành "tìm căn tương tự" + 3 link căn cùng nhánh |
| **NGỪNG CHO THUÊ** | giữ trang, nêu rõ, đẩy link sang nhánh cùng loại |

Luật: **không xoá, không 404, không redirect hàng loạt.** Đúng bài học đã ghi ở `docs/package/DANG-TIN-KHONG-LOI.md`.

---

## LÀM MỚI (freshness) — thứ quyết định thắng thua ở mảng thuê

Search thuê là search "còn trống không". Trang đứng im 3 tháng sẽ tụt.

- Bot `scripts/thu-thap-thue.mjs` chạy 07:20 mỗi ngày, gom vào `data/tin-thue/`.
- Khi có hàng: mục giá trong hub cập nhật dải giá thật theo tháng, `lastmod` sitemap đổi theo.
- Mỗi lần thêm/đổi trạng thái một tin → cập nhật `dateModified` của hub.

---

## RANH GIỚI VỚI GREENSPACE

- **Villas:** môi giới cho thuê — tìm khách, dẫn xem, chốt hợp đồng, ký gửi.
- **Greenspace:** quản lý tài sản/đất thu phí hàng tháng.
- Hai bên link 2 chiều thoải mái. Không trang nào của Villas đặt `<a>` sang Panorama (`docs/HIEN-PHAP-3-WEB.md`).

---

## VIỆC TIẾP THEO, THEO THỨ TỰ

1. Để bot chạy, tích `data/tin-thue/` — xem nhánh nào có hàng thật trước.
2. Đánh mạnh vùng 6 (phía chủ nhà) ngay: nội dung ký gửi, vì không cần kho hàng.
3. Nhánh nào đủ 3 tin thật → cắt URL riêng theo bảng trên, không mở trước.
