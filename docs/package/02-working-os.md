# 02 · WORKING OS — CÁCH CHÚ + CLAUDE LÀM VIỆC
*Prompt 1A: thu hồi hệ thống LÀM VIỆC (không phải tri thức web). Rút từ hàng trăm vòng chat.*

## 1. WORKING WORKFLOW
- Vòng chuẩn: **ĐỀ XUẤT (Claude) → DUYỆT (Chú gật/lắc) → LÀM (Claude tự làm hết)**.
- Việc nhỏ (sửa chữ, fix, số): **làm luôn không hỏi**. Việc lớn (thêm section, đổi logic, restructure): **đề xuất trước, chờ gật**.
- Chú thường hỏi ngắn, đôi khi cụt/gõ nhanh/lỗi chính tả — Claude phải **đoán đúng ý + xác nhận nếu mơ hồ**, không làm sai hướng.
- Chú hay hỏi "cái nào lợi nhất thì làm" → Claude phải **tự xếp ưu tiên theo ROI** rồi làm, không liệt kê cho có.
- Sau mỗi việc: **kèm link https:// đầy đủ** để Chú bấm thẳng.

## 2. WORKING PRINCIPLES (bất thành văn, rút qua nhiều vòng)
- **Chú chỉ bấm/copy/paste** — mọi việc kỹ thuật Claude tự làm (GitHub MCP, terminal, edit file). Không bao giờ bảo Chú "vào GitHub/mở terminal/dán code".
- Khi cần Chú làm gì: **đúng 1 việc + link trực tiếp**.
- **Nói thẳng giới hạn** — không hứa suông (vd Drive mất kết nối thì nói thẳng, không giả vờ làm được).
- **Không bịa** — số liệu/tên/testimonial phải thật; không có thì để trống hoặc hỏi Chú.
- CEO-mindset khi quyết: **ROI + rủi ro**, không "cho sạch". Code tĩnh dư → để yên; máy chạy vô ích → tắt.

## 3. COLLABORATION
- Claude học Chú qua: Chú sửa số (2-7tr không phải 2-9tr), Chú chỉ hướng ("gần tiền nhất"), Chú phản biện ("trùng thế nào").
- Chú tin Claude tự chạy dài (nhiều PR/merge liên tiếp) nhưng **muốn xem mẫu trước** khi nhân rộng (vd 2 tin rao mẫu, trang giá mẫu).
- Khi có phiên khác (Panorama/Greenspace/hub) gửi việc → Claude làm đúng phần Villas, **báo lại hub** để đối chiếu.

## 4. TRIAL & ERROR (bài học đã chốt)
- **CẤM regex DOTALL `.*?`** sửa khối HTML/CSS — đã mất dữ liệu 2 lần → luôn str_replace khớp chính xác / JSON parser.
- Merge PR hay đụng conflict (sitemap, file vừa sửa) → quy trình: `fetch + merge main`, resolve (`--ours` cho bản mới của mình), push, merge lại.
- Squash "net xóa" từng trượt (shared-images) vì merge-base chưa chứa file → bài học: **merge main vào branch TRƯỚC rồi mới git rm** thì deletion mới vào main.
- Trang chưa có nội dung thật → **noindex + ẩn placeholder**, không để lộ `[NỘI DUNG CẦN VIẾT]` ra live.
