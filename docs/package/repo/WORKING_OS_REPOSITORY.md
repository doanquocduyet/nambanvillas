# WORKING_OS_REPOSITORY — NAM BAN VILLAS
*Prompt 1A. Thu hồi ĐẦY ĐỦ hệ LÀM VIỆC Chú↔Claude. Mỗi mục kèm bối cảnh/lý do/quyết định cuối. Không diễn giải lại, không chuẩn hóa.*

═══════════════════════════════════════════════
## 1. WORKING WORKFLOW
═══════════════════════════════════════════════

### 1.1 Cách bắt đầu / tiếp cận việc
- **Vòng chuẩn: ĐỀ XUẤT (Claude) → DUYỆT (Chú gật/lắc) → LÀM (Claude tự làm hết).** Bối cảnh: định nghĩa ngay trong CLAUDE.md Nguyên tắc 2, lặp lại đúng suốt phiên.
- Việc nhỏ (sửa chữ, đổi màu, fix bug, đổi số) → **làm luôn không hỏi**. Việc lớn (thêm section, đổi logic, restructure, canonical hàng loạt, tạo bộ tài liệu) → **đề xuất trước, chờ gật**. Quyết định cuối: ranh giới này Chú không bao giờ phàn nàn khi Claude tự làm việc nhỏ, nhưng khi Claude tự làm việc lớn (không hỏi) thì vẫn OK MIỄN LÀ đúng ý — vd "làm đi ko hỏi lại" = cho phép bỏ bước duyệt khi Chú đã tin.

### 1.2 Cách chia nhỏ / đào sâu / xử lý nhiều phương án
- Khi việc lớn (vd áp Hiến pháp 3 web: 22 canonical + 3 trang giao dịch + xóa /tin-tuc + link Greenspace) → Claude **gộp thành 1 commit/PR** theo yêu cầu brief, không chẻ nhỏ gây tốn build.
- Nhiều phương án → Claude **đưa 1 khuyến nghị + lý do**, không dàn options. Bối cảnh: Chú nhiều lần chọn ngay "hướng A/1" → xác nhận gu quyết đoán.

### 1.3 Review / iterate / phát hiện sai / đổi hướng
- Chú review bằng **đưa số thật** ("Nam ban 2-7tr") hoặc **chỉ hướng** ("gần tiền nhất", "cái nào lợi nhất") → Claude sửa toàn site + đối chiếu ngữ cảnh.
- Chú phát hiện mâu thuẫn bằng **case thực tế** (gửi case Zames Chew hỏi "áp dụng được gì") → Claude phải đối chiếu chiến lược, không gật theo.
- Đổi hướng giữa chừng: Chú đổi từ "digest thị trường" sang "1-2 tin cụ thể viết lại" → Claude pivot ngay, không bảo thủ bản cũ.

### 1.4 Chốt / ra quyết định / deploy
- Deploy = tạo PR + **squash merge vào `main`** qua GitHub MCP (branch dev `claude/dreamy-ritchie-xBezi`). Vercel auto-deploy. Chú KHÔNG vào GitHub.
- Xong việc → **kèm link `👉 https://nambanvillas.vn/...`** (bắt buộc https://). Nhiều trang → mỗi link 1 dòng.
- Chú chốt bằng "xong"/"ok"/chuyển việc; **thường không khen**, im lặng đi tiếp = đạt.

═══════════════════════════════════════════════
## 2. WORKING TASTE (gu trong lúc làm — chi tiết ở PRODUCT_TASTE)
═══════════════════════════════════════════════
- Số thật > tính từ; khối ngắn, tô đậm số; "im lặng mà sang". (Xem PRODUCT_TASTE_REPOSITORY để đầy đủ.)
- Trong lúc làm: Claude luôn **verify trước push** (JSON/XML valid, 0 placeholder) — thành phản xạ sau nhiều lần Chú bắt lỗi lộ placeholder.

═══════════════════════════════════════════════
## 3. WORKING PRINCIPLES (bất thành văn, rút qua nhiều vòng)
═══════════════════════════════════════════════
- **P1 — Chú chỉ bấm/copy/paste.** Không bao giờ bảo Chú "vào GitHub/mở terminal/dán code". Cần Chú → đúng 1 việc + link https:// bấm thẳng; hướng dẫn từng bước 1-2-3 (GBP, API key, GSC), không "vào trang X tìm Y".
- **P2 — Nói thẳng giới hạn, không hứa suông.** Bối cảnh: Drive mất kết nối + proxy chặn ảnh ngoài → Claude nói thẳng "không đọc/ghi Drive được" + đưa cách thay thế (lưu repo). Quyết định cuối: thà mất mặt hơn giả vờ làm được.
- **P3 — KHÔNG bịa.** Số/tên/testimonial phải thật; không có → để trống hoặc hỏi Chú. Hệ quả: trang chưa có nội dung → **noindex + ẩn `[NỘI DUNG CẦN VIẾT]` thành comment**, không lộ live. Sau khi Chú "tạm bỏ qua luật cấm" → Claude vẫn chỉ viết từ số đã công bố/research thật, không bịa bừa.
- **P4 — CEO-mindset: ROI + rủi ro, không "cho sạch".** Vd: CSS trùng chéo 12 selector + ~43 class nghi không dùng → **để yên** (sửa rủi ro cao, lợi ≈0). update-news.mjs ghi news.json rỗng mỗi tuần → **tắt** (máy chạy vô ích). 3 trang giao dịch noindex → **ưu tiên viết** (gần tiền nhất).
- **P5 — Bảo mật.** Token/API key KHÔNG ghi vào file/commit/PR (khi Chú dán token mới, Claude chỉ test đọc, không lưu). Model ID không lộ trong commit/PR/artifact. Token fine-grained villas-only chạm repo khác → 403 = đúng thiết kế.
- **P6 — Frugal.** Quota Vercel 100 build/ngày → không push thừa; chỉ comment GitHub khi cần.
- **P7 — Verify sau mỗi thay đổi** trước push (thành luật ở CLAUDE.md).

═══════════════════════════════════════════════
## 4. COLLABORATION
═══════════════════════════════════════════════
### 4.1 Cách Claude học Chú
- Qua **sửa số** (2-7 không phải 2-9; Bảo Lộc 5-15 không phải 20-40) → Claude cập nhật + nhớ dùng nhất quán.
- Qua **chỉ hướng ngắn** → Claude tự suy ưu tiên.
- Qua **phản biện/case** → Claude đối chiếu, điều chỉnh chiến lược (không xây hệ sinh thái trước — theo Zames).

### 4.2 Cách Chú giúp Claude hiểu mình
- Chú cung cấp tài liệu nền: CLAUDE.md, HIEN-PHAP-3-WEB, FORM-DANG-TIN, HO-SO-TONG, TU-DUY-TINH-TUE; gửi brief từ hub; gửi keyword 3 site; gửi case study.
- Chú đổi model khi muốn (fable-5/opus-4-8) — Claude không bàn.

### 4.3 Phối hợp hệ 3 web (đa phiên)
- Phiên hub/Panorama/Greenspace gửi việc cho phiên Villas → Claude làm đúng phần Villas, **báo lại hub để đối chiếu** ("đã sạch shared-images trên main + đã sửa canonical"), **xác minh trên origin/main thật** trước khi báo xong.
- Nhận keyword 3 site → phân tích trùng/intent, đề xuất canonical/redirect, KHÔNG tự sửa repo khác (không có quyền).

═══════════════════════════════════════════════
## 5. TRIAL & ERROR (đã thử/thay đổi/loại bỏ + vì sao)
═══════════════════════════════════════════════
- **CẤM regex DOTALL `.*?`** sửa HTML/CSS — đã mất dữ liệu 2 lần (ghi rõ CLAUDE.md) → dùng str_replace khớp duy nhất / JSON parser / sed chuỗi cố định. Khi phải sửa schema hàng loạt → **json.loads → sửa dict → json.dumps** (an toàn tuyệt đối).
- **Merge conflict** tái diễn ở `sitemap.xml` + file vừa sửa (2 nhánh cùng đụng) → quy trình chốt: `git fetch origin main && git merge origin/main --no-edit`, resolve **`git checkout --ours <file>`** giữ bản mới, HOẶC dựng lại sitemap từ trang self-canonical bằng script, push, rồi merge PR lại. Lặp lại ~10 lần trong phiên → thành phản xạ.
- **Squash "net xóa" TRƯỢT** (shared-images 47MB không vào main dù git rm): merge-base chưa chứa file. → Bài học chốt: **merge main vào branch TRƯỚC (đưa file vào merge-base) rồi mới `git rm`**; xác minh `git ls-tree -r origin/main | grep <file>` = rỗng.
- **Vercel 2-3 project** cùng nối repo → stale deploy + duplicate SEO; xóa project thừa làm **domain nambanvillas.vn disconnect** → serve bản cũ → GSC không verify. Bài học: 1 project duy nhất; xóa project xong phải kiểm domain.
- **GSC/Bing verify**: chọn HTML tag (không DNS — không có quyền DNS). Fail thường do chưa deploy/domain disconnect, không phải sai tag.
- **OG image** bị commit deploy ghi đè thành text 2KB → khôi phục 130KB từ git history.
- **CronCreate session-only** (không bền qua phiên) → automation "hàng ngày" phải là **GitHub Action + API key**, không phải cron trong phiên. Nói thẳng cho Chú thay vì hứa cron chạy mãi.
- **update-news.mjs** gọi API cafef ghi news.json rỗng, không ai dùng → gỡ; giữ build-feed (hữu ích).
- Ảnh: môi trường KHÔNG có ImageMagick nhưng CÓ PIL → xử ảnh bằng PIL. KHÔNG lấy ảnh listing người khác (bản quyền) → dùng ảnh chung hoặc không ảnh.
