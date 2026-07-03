# PRODUCT_TASTE_REPOSITORY — NAM BAN VILLAS
*Prompt 1A+. Thu hồi ĐẦY ĐỦ gu thẩm mỹ/gu sản phẩm. Không thu hồi cách làm việc (→1A) hay token (→1C). Chỉ thu hồi GU.*

═══════════════════════════════════════════════
## 1. DESIGN TASTE
═══════════════════════════════════════════════
- **Định vị thẩm mỹ cốt lõi: "Im lặng mà sang"** — không emoji, không banner, không gấp gáp, không hô hào. (CLAUDE.md Nguyên tắc 5.)
- **Bố cục/nhịp:** sạch, nhiều khoảng trắng, khối ngắn, mới nhất lên đầu; số quan trọng **tô đậm `<strong>`** để quét mắt. Bảng so sánh phải nhìn 1 mắt thấy hết.
- **Màu:** Gold `#C9A84C` chỉ **4 chỗ** — nút call mobile nav · số Pain section · border-left Notes editorial · hover nền tối. Lạm dụng gold = sai gu (khắc CLAUDE.md).
- **Trình bày trên PC (gu cụ thể Chú yêu cầu):** ô phụ Namban Notes **dàn 3 cột ngang** ≥769px (không chiếm chỗ như ô chính); listing sản phẩm **hiển thị hàng ngang** (flex row) trên desktop. Bối cảnh: Chú bảo "namban notes chiếm chỗ quá, dàn gọn lại, đó ko phải ô chính".
- **Hình ảnh:** cắt khung 2:1 (1200×600), bo góc 12px; hero phủ **lớp gradient xanh đậm** cho chữ đọc được (đây là "tráng lớp mờ đen/xanh" Chú gợi ý). Bài đã có infographic SVG → không chèn ảnh trùng. Ảnh "minh hoạ chung" chấp nhận được; ảnh giả-làm-lô-cụ-thể thì không.
- **Popup:** hiện đúng 1 lần/đời user (localStorage, không sessionStorage).

═══════════════════════════════════════════════
## 2. PRODUCT TASTE — NGƯỠNG "ĐÚNG Ý / CHƯA TỚI"
═══════════════════════════════════════════════
- **Đúng gu:** số thật cụ thể — "2–7 triệu/m²", "568 triệu/lô", "cách Đà Lạt 35–40 phút", "400–1.000m²".
- **Sai gu (quá AI / phô / rỗng):** "giá cực tốt", "view đỉnh", "vị trí đắc địa", tính từ không kèm số.
- **CẤM tính từ rỗng** — đã quét & xóa toàn site (số lần từng xuất hiện): tuyệt đẹp ×6 · cơ hội vàng ×7 · lý tưởng ×9 · tốt nhất ×3 · hoàn hảo ×2 · số 1/số một · siêu phẩm · cực hiếm · rẻ nhất · giá sốc · đất vàng · vị trí vàng. **Ngoại lệ:** "giá rẻ nhất bao nhiêu?" trong CÂU HỎI FAQ là search-intent thật → giữ.
- **CẤM từ spam trong tin rao** (blocklist): chắc chắn lời · lời ngay · mua là thắng · x2/x3 tài khoản · sinh lời khủng · sốt đất · độc nhất · ngộp bank · cắt lỗ sâu · bán tháo gấp · kèo thơm · 10 năm có 1.
- **"Chưa tới":** bài/tin thiếu phần **"1 rủi ro cần kiểm"** = chưa đạt. Dám nói "đừng mua" / "ai KHÔNG nên mua" = đủ chiều sâu, tạo tin.
- **Lỗi không chấp nhận:** lộ `[NỘI DUNG CẦN VIẾT]` ra live.
- **"Quá nhiều / quá ít":** thà 1–2 tin CHẤT hơn nhiều tin rác; không đủ chất → không đăng. Khi Chú thấy bản OS "cô đặc quá ít" → đó là tín hiệu gu: tài liệu nội bộ thì muốn ĐẦY ĐỦ, không cắt.
- **AEO:** FAQ trả lời thẳng ở câu ĐẦU (để AI trích).

═══════════════════════════════════════════════
## 3. CRITIQUE TASTE (cách Chú nêu vấn đề)
═══════════════════════════════════════════════
- Câu ngắn, thẳng, đôi khi 1 chữ/cụm: "trùng thế nào", "số sai 2-7tr", "xem kỹ", "vẫn quá ít", "cô đặc nhất", "làm đi ko hỏi lại".
- Tín hiệu chưa chấp nhận: Chú lặp lại yêu cầu ở góc khác ("chuẩn geo chưa" → "áp dụng mọi kỹ thuật" → "còn gì hay bổ sung") = muốn đào sâu thêm, chưa đủ.
- Cách Chú dẫn về đúng hướng: đưa **số thật** hoặc **case/tài liệu** làm chuẩn đối chiếu.
- Chú ít giải thích dài; kỳ vọng Claude tự hiểu và tự sửa toàn bộ hệ quả (sửa 1 số → sửa cả FAQ schema + mọi trang liên quan).

═══════════════════════════════════════════════
## 4. COMPARISON TASTE (tiêu chí phân biệt / loại phương án)
═══════════════════════════════════════════════
- **Cụ thể-chạm > trừu tượng-đẹp:** lô thật/giá thật/bảng số > concept/triết lý/hệ sinh thái. (Trùng bài học Zames: bán giải-đau cụ thể, không bán vision.)
- Loại phương án "flex/phô": trang so sánh phải có **bảng số 4 cột**, không "so chung chung"; trang giá phải có **con số/m²**, không "giá tốt"; trang đầu tư phải có **số ROI/chi phí thật**, không "tiềm năng lớn".
- Ưu tiên khi cân: **freshness + dữ liệu sống** (cụm tin ngày → giá tuần) hơn 1 con số tĩnh.
- Đánh đổi: chấp nhận noindex trang chưa đủ chất (mất tạm SEO) để **giữ thương hiệu** — không index rác để có thêm URL.

═══════════════════════════════════════════════
## 5. PERFECTION TASTE (mức cầu toàn / luôn kiểm)
═══════════════════════════════════════════════
- **3 điều luôn tự kiểm mỗi lần:** (1) số có THẬT không · (2) có đụng **bản quyền** không (KHÔNG lấy ảnh/chữ nguyên văn tin người khác — viết lại bằng lời mình + ghi Nguồn rel=nofollow) · (3) có **đụng chạm** ai không (KHÔNG "cò/lừa đảo/thổi giá"; chỉ nói nỗi lo khách).
- **Chi tiết Chú luôn soi:** giá/số nhất quán toàn site; địa danh đúng ("Xã Nam Ban" từ 1/7/2025, giữ "thị trấn" chỉ khi kể lịch sử); trang không lộ placeholder; link bấm được (có https://).
- **Tiêu chuẩn hình thành qua nhiều vòng:** tách bạch tuyệt đối "lô Villas đã kiểm tra" vs "tin thị trường chưa kiểm chứng"; mọi tin dẫn về Zalo để biến thành lead.
- **Quy luật khi hoàn thiện:** thương hiệu "đọc rủi ro, không bán giấc mơ" đặt TRÊN mọi cám dỗ marketing — bất biến, không thương lượng.
