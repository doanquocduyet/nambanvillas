# Kinh nghiệm quét tin rao (rút từ bộ đo Namban Index của Panorama, 26/9/2026)

> Tài liệu nội bộ cho ô Villas — ô DUY NHẤT quét tin (CLAUDE.md, chốt 26/9/2026). Panorama chỉ đọc trang tin rao của Villas.

## 0. Vì sao Panorama từng "ra nhiều tin hơn"
Panorama đếm MỌI tin còn trên mạng (634 tin, 25/9); Villas chỉ giữ tin ĐÃ KIỂM được ngày đăng (318 tin). Học cách mở rộng độ phủ, KHÔNG bỏ bước kiểm.

## 1. Vào từ 5 cửa mỗi sàn
Sàn vẫn xếp theo tên cũ: xã Nam Ban Lâm Hà (mới) + thị trấn Nam Ban, xã Đông Thanh, xã Mê Linh, xã Gia Lâm. Cửa nào biết khu thì gắn sẵn khu cho tin lấy từ cửa đó.
Sàn: guland, datnenlamdong, batdongsanonline, thuviennhadat, muaban, mogi (+ Chợ Tốt API, YouTube).

## 2. Tự dò phân trang
Thử lần lượt `/trang/2/` · `/page-2/` · `/trang--2.html` · `?page=2` · `?p=2` · `?cp=2`; kiểu nào ra link mới thì dùng tiếp, dừng khi trang không ra link mới (tối đa 30). Lọc link tin bằng mẫu URL riêng (guland: `/post/`), bỏ `?…` `#…` trước khi so trùng.

## 3. Đọc trang chi tiết theo tầng
1) JSON-LD (datePosted/datePublished, price, address, floorSize) → 2) meta `article:published_time` / `<time datetime>` → 3) chữ "Ngày đăng / Diện tích / Mức giá" → 4) chỗ riêng từng sàn (guland `.dtl-prc__ttl`, `.dtl-prc__dtc`) → địa chỉ: breadcrumb, rồi tiêu đề.

## 4. Đọc tiền / diện tích / ngày
- Tiền: `1 tỷ 350 triệu`, `1 tỷ 3`, `1,65 tỷ`, `1.599 tỷ` (dấu sau "tỷ" là thập phân), `850tr`. Phân biệt giá cả lô / m² / sào / lô-nền. "Thỏa thuận" → bỏ.
- Sào = 1.000 m². Giá "/sào" chia 1.000 ra giá/m²; KHÔNG chia cho diện tích cả lô.
- Diện tích: m², m2, ha (×10.000), sào (×1.000); chỉ nhận 10–500.000 m².
- Ngày: dd/mm/yyyy, yyyy-mm-dd; "3 ngày trước" = ước lượng (gắn cờ, không trộn ngày thật). Guland "ngày cập nhật" ≠ ngày đăng.
- Chặn số vô lý: giá/m² ngoài 0,1–100 triệu, giá lô ngoài 50 triệu–200 tỷ → bỏ.

## 5. Phân khu
Địa chỉ trước, tiêu đề sau. Loại: Phi Tô, Tà Nung, Đinh Văn, Đạ Đờn, Tân Hà, Tân Văn, Phú Sơn, Liên Hà, Hoài Đức, Phúc Thọ, Đan Phượng, Tân Thanh, Bảo Lộc, Di Linh, Đức Trọng, Lạc Dương, Đơn Dương, Cam Ly. **Nam Hà: Villas GIỮ, ghi "Nam Hà (giáp Nam Ban), Lâm Hà"** (luật Villas). Nhận: Đông Thanh, Mê Linh (cả Buôn Chuối), Gia Lâm, mốc Thăng Long, Chi Lăng, Bãi Công, Từ Liêm, Thanh Trì, Linh Ẩn, thác Voi, Tổng Đội, Ba Đình, ĐT725. Vừa nhận vừa loại → "mơ hồ", không đoán, không đăng.

## 6. Gộp trùng giữa sàn
Cùng khu + diện tích lệch ≤ 2% + giá lệch ≤ 3% = một lô. Giữ bản có URL gốc và ngày chắc nhất.

## 7. Chạy lịch sự
Đọc robots.txt; nghỉ ≥1,5 s/lần cùng sàn; tối đa ~450 tin/nguồn/lượt; bị 403 thì đổi chỗ chạy (máy GitHub Actions), không vượt Cloudflare/captcha.

## 8. Luật dừng — thà không đăng còn hơn số sai
Dừng, không sửa trang khi: nguồn tuần trước có tin mà nay về 0 (nghi bị chặn/đổi giao diện); số vô lý hàng loạt; giá trung bình nhóm (≥30 tin) nhảy >25%.

## 9. Lưu ngay
Sàn gỡ tin sau 2–3 tháng → quét mỗi sáng, đăng ngay. Không bao giờ xoá/tính lại tháng cũ bằng mẫu nhỏ hơn.

## 10. Chỉ giữ số, không giữ người
Không lưu SĐT, tên người, ảnh của tin gốc. Viết lại mô tả bằng lời Nam Ban Villas.

## 11. Mạng xã hội
YouTube: được (yt-dlp `player_client=android`, `process=False`, nghỉ ~3 s, cache). Facebook nhóm / Zalo / TikTok sau đăng nhập: KHÔNG cào. Cách hợp lệ: "hộp nhận tin" — người gửi tự nguyện link tin công khai, bộ đọc mở đúng link đó và kiểm như mọi tin.

## Khuôn trang tin rao (Panorama đọc máy — không đổi khi chưa báo)
`<!-- DAY:YYYY-MM-DD -->` → `li.tin-item` → `.tin-specs`: span ĐẦU = diện tích, có 1 span tổng giá, span CUỐI = vị trí; tin số lệch ghi "lệch nhau" trong `.tin-desc`.
