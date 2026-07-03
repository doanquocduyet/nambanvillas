# 02 · WORKING OS — CÁCH CHÚ + CLAUDE LÀM VIỆC
*Prompt 1A: thu hồi ĐẦY ĐỦ hệ LÀM VIỆC (không phải tri thức web). Không bỏ sót dù chỉ xuất hiện 1 lần.*

## 1. WORKING WORKFLOW
- Vòng chuẩn: **ĐỀ XUẤT (Claude) → DUYỆT (Chú gật/lắc) → LÀM (Claude tự làm hết)**.
- Việc nhỏ (sửa chữ, đổi màu, fix bug, sửa số): **làm luôn, không hỏi**. Việc lớn (thêm section, đổi logic, restructure, canonical hàng loạt): **đề xuất trước, chờ gật**.
- Mỗi việc xong: **kèm link `👉 https://nambanvillas.vn/...`** (phải có https:// để bấm được). Nhiều trang → mỗi link 1 dòng.
- Deploy = tạo PR + **squash merge vào `main`** qua GitHub MCP. Branch dev `claude/dreamy-ritchie-xBezi`. Vercel auto-deploy. Chú KHÔNG cần vào GitHub.
- Chú xem preview qua link Vercel bot đăng trong PR comment.
- Sau merge, luôn **hard refresh (Ctrl+Shift+R)** vì cache trình duyệt (đã nhiều lần Chú tưởng chưa deploy vì cache).

## 2. CÁCH CHÚ RA LỆNH — ĐỌC ĐÚNG Ý (quan trọng nhất)
- Chú viết **câu ngắn, gõ nhanh, hay lỗi chính tả/không dấu/cụt**: "Tự researxh rồi viết đi", "cái nào lợi nhất thì lầm", "viet intruction và mô tả", "1b". Claude phải **đoán đúng + xác nhận nếu thật sự mơ hồ**, KHÔNG chạy sai hướng, KHÔNG bắt Chú gõ lại.
- "Cái nào lợi nhất cho aeo/seo/geo/ux/ui thì làm" = Claude **tự xếp ưu tiên theo ROI rồi làm ngay**, không liệt kê options cho có.
- "Có gì hay bổ sung không / cháu có đề xuất gì hay hơn" = Chú muốn Claude **chủ động đề xuất cái tốt hơn**, được phép làm luôn.
- "Nếu cháu là founder/CEO/chuyên gia SEO thì xử sao" = Chú muốn **góc nhìn quyết đoán + hành động**, không phân tích lửng lơ.
- Chú **sửa số trực tiếp giữa chừng** ("Nam ban 2-7tr, Bảo lộc 5-15tr", "2 tỷ nam ban 400-1000m2") → Claude cập nhật **toàn site + FAQ schema**, giữ đúng ngữ cảnh (KHÔNG đụng "20-40 triệu/tháng" homestay hay "20-40%" tăng giá).
- Chú **muốn xem MẪU trước khi nhân rộng**: 2 tin rao mẫu, trang giá mẫu, bài đầu tiên. Duyệt mẫu rồi mới bật tự động.
- Chú tự **đổi model giữa phiên** (fable-5 ↔ opus-4-8) — là quyền của Chú, Claude không bàn.
- Chú hỏi cùng 1 việc nhiều góc ("chuẩn geo chưa", "áp dụng mọi kỹ thuật", "xem kỹ chi tiết cô đặc nhất") = muốn **đào sâu thêm**, không phải làm lại.

## 3. NGUYÊN TẮC BẤT THÀNH VĂN (rút qua nhiều vòng)
- **Chú chỉ bấm/copy/paste.** Không bao giờ bảo Chú "vào GitHub rồi làm X", "mở terminal chạy Y", "copy code dán vào file Z". Cần Chú làm gì → **đúng 1 việc + link trực tiếp có https://**. Khi hướng dẫn (GBP, API key, GSC) → từng bước 1-2-3 + link bấm thẳng, không "vào trang X tìm Y".
- **Nói thẳng giới hạn** — không hứa suông: Drive mất kết nối/proxy chặn ảnh ngoài/không tạo được folder Drive → **nói thẳng + đưa cách thay thế** (lưu vào repo), không giả vờ làm được.
- **KHÔNG bịa** — số/tên/testimonial/tên quán phải thật; không có thì để trống hoặc hỏi Chú. Trang chưa có nội dung thật → **noindex + ẩn `[NỘI DUNG CẦN VIẾT]` thành comment**, KHÔNG lộ ra live (lỗi nặng).
- **CEO-mindset khi quyết**: xét ROI + rủi ro, không "làm cho sạch". Code tĩnh dư vô hại (CSS trùng chéo 12 selector, ~43 class không dùng) → **để yên** (sửa rủi ro cao, lợi 0). Máy chạy vô ích (update-news ghi news.json rỗng) → **tắt**. Việc gần tiền nhất (3 trang giao dịch) → **ưu tiên làm trước**.
- **Bảo mật**: token / API key KHÔNG bao giờ ghi vào file / commit / PR. Model ID KHÔNG để lộ trong commit/PR/artifact (chỉ nói trong chat). Token fine-grained "villas-only" chỉ mở repo nambanvillas → chạm repo khác trả 403 = **đúng thiết kế, không phải lỗi**.
- **Phối hợp hệ 3 web**: phiên khác (hub/Panorama/Greenspace) gửi việc → Claude làm đúng phần Villas, **báo lại hub để đối chiếu** ("đã sạch X + đã sửa Y"). Xác minh trên `origin/main` thật trước khi báo xong.
- **Frugal GitHub**: chỉ comment/PR khi thật cần (quota Vercel 100 build/ngày, không push thừa).

## 4. COLLABORATION — CÁCH CLAUDE HỌC CHÚ
- Chú dạy qua: **sửa số** (2-7 không phải 2-9), **chỉ hướng** ("gần tiền nhất", "cái nào lợi nhất"), **phản biện** ("trùng thế nào", "thực tế phải như bài viết không").
- Chú tin Claude **tự chạy dài** (nhiều PR/merge liên tiếp trong 1 lượt) nhưng vẫn muốn **báo cáo gọn + link** sau mỗi cụm.
- Chú thường **không khen**; im lặng đi tiếp = ổn. Chốt bằng "xong", "ok", hoặc chuyển việc.
- Khi Chú lo (SEO delay, Vercel stale, GSC không verify) → Claude phải **giải thích nguyên nhân gốc** (domain disconnect, cache, canonical), không trấn an suông.

## 5. TRIAL & ERROR — BÀI HỌC ĐÃ TRẢ GIÁ
- **CẤM regex DOTALL `.*?`** sửa khối HTML/CSS — đã mất dữ liệu 2 lần → luôn `str_replace` khớp CHÍNH XÁC DUY NHẤT / JSON parser / sed chuỗi cố định.
- **Merge conflict** hay ở `sitemap.xml` và file vừa sửa (2 nhánh cùng đụng) → quy trình: `git fetch origin main && git merge origin/main --no-edit`, resolve bằng **`git checkout --ours <file>`** (giữ bản mới của mình) HOẶC dựng lại sitemap từ trang self-canonical, push, rồi merge PR lại.
- **Squash "net xóa" từng TRƯỢT** (shared-images 47MB không vào main dù đã git rm): vì merge-base chưa chứa file. → Bài học: **merge main vào branch TRƯỚC** (đưa file vào merge-base) **rồi mới `git rm`** → deletion mới thật sự vào main. Xác minh `git ls-tree -r origin/main | grep <file>` = rỗng.
- **Vercel**: từng có 2-3 project cùng nối repo → stale deploy + duplicate SEO. Xóa project thừa làm **domain nambanvillas.vn bị disconnect** → site serve bản cũ → GSC không verify được. Bài học: chỉ 1 project (`nambanvillas`), phát hiện >1 = báo ngay; sau khi xóa project phải kiểm domain còn nối không.
- **GSC/Bing verify**: chọn phương thức **HTML tag** (không DNS — mình không có quyền DNS). Verify fail thường do **Vercel chưa deploy bản mới / domain disconnect**, không phải sai tag.
- **OG image** `og-namban.jpg` từng bị commit deploy ghi đè thành **text 2KB** (hỏng ảnh share) → khôi phục bản 130KB thật từ git history (`git show <sha>:path`).
- **Verify TRƯỚC khi push**: JSON-LD valid (json.loads), XML valid (minidom), 0 placeholder, link nội bộ không gãy, ảnh tồn tại.
