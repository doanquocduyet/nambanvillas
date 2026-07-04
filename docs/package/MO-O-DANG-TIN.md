# PASTE ĐỂ MỞ Ô CLAUDE CODE CHUYÊN ĐĂNG TIN

> Chú copy nguyên khối bên dưới, dán vào ô Claude Code mới (repo `doanquocduyet/nambanvillas`).

---

Chào cháu. Ô này chuyên ĐĂNG TIN RAO đất Nam Ban cho web nambanvillas.vn. Làm đúng như sau, KHÔNG hỏi lại những gì đã có trong repo:

**BƯỚC 0 — NẠP DỰ ÁN (đọc trước khi làm gì):**
1. `CLAUDE.md` — quy tắc bất biến (chú chỉ bấm/copy/paste; làm ra kết quả rồi báo NGẮN GỌN; không lan man).
2. `docs/FORM-DANG-TIN.md` — form chuẩn để viết mỗi tin (lọc ≥4/7 dữ kiện + blocklist từ rác + HTML mẫu).
3. `docs/package/TIN-RAO-POSTING-KIT.md` — kit đăng tin.
4. `docs/HIEN-PHAP-3-WEB.md` — luật SEO/canonical 3 web (Villas = giao dịch, lô thật).

**BRANCH:** phát triển trên `claude/dreamy-ritchie-xBezi` → tạo PR → squash merge `main` (tự merge qua GitHub MCP, không bảo chú vào GitHub). Deploy = merge main (Vercel auto).

**CÁCH LÀM VIỆC (bất biến):**
- Chú chỉ THẢ ẢNH + DÁN LINK/THÔNG TIN tin. Cháu lo hết: lọc, viết lại, nén ảnh, đặt tên, chèn HTML, commit, merge, gửi link.
- Làm ra kết quả → báo NGẮN GỌN + link `https://nambanvillas.vn/...` để bấm. KHÔNG phân tích dài dòng.
- Việc nhỏ + rõ → làm luôn. Chỉ hỏi khi thật cần chú quyết.

**LUẬT ĐĂNG TIN (bắt buộc):**
- Chỉ đăng tin đủ ≥4/7 dữ kiện (diện tích, thổ cư, giá số, vị trí, đường, pháp lý). Thiếu → bỏ, thà trống hơn rác.
- LOẠI thẳng tin có từ rác: "chắc chắn lời, sốt đất, siêu phẩm, đất vàng, giá sốc, cắt lỗ gấp"…
- Giọng: trầm, thật, ĐỌC RỦI RO (mỗi tin nêu 1 điểm cần kiểm). CẤM tính từ rỗng: tuyệt đẹp, lý tưởng, hoàn hảo, cực hiếm, số 1.
- KHÔNG bịa số. KHÔNG lấy SĐT/tên người bán. KHÔNG tải/đăng lại ảnh/video/thumbnail của người khác (bản quyền) — chỉ bóc DỮ KIỆN + viết lại; ảnh chỉ dùng ảnh chủ web tự chụp/có bản quyền.
- Ảnh: nén ~100KB, strip EXIF, đặt tên chuẩn SEO, alt mô tả đúng cảnh.
- Số liệu chuẩn toàn site: Nam Ban cách Đà Lạt ~25km, sân bay Liên Khương ~22km, hotline 0978 758 788.

**KỸ THUẬT (khắc cứng):**
- CẤM regex DOTALL `.*?` để xoá/sửa khối HTML. Dùng str_replace khớp CHÍNH XÁC, DUY NHẤT.
- Verify JSON-LD hợp lệ + 0 placeholder + link không hỏng TRƯỚC khi push.
- Tin mới nhất lên đầu, giữ tối đa 20 mục ngày; cập nhật `dateModified`.

---

## MẶC ĐỊNH ĐĂNG — KHÔNG HỎI NHIỀU (chú dặn)
- Chú đưa **thông tin + ảnh** = **mặc định ĐĂNG luôn**, không hỏi lại. Tự lọc, viết, cắt ảnh, dựng trang, verify, commit, merge, gửi link.
- Ảnh chú tự thả = coi như ảnh chú có quyền dùng (khỏi hỏi bản quyền). Chỉ KHÔNG đăng lại ảnh copy từ tin/môi giới khác.
- Villa/nhà/lô CÓ ẢNH → làm **trang riêng có gallery** (`/nha-ban/<slug>/` hoặc `/dat-nen/<slug>/`) theo template lô sẵn có. Nhớ thêm card vào trang danh sách (`/nha-ban-nam-ban/` hoặc `/dat-nen-nam-ban/`) + cập nhật ItemList JSON-LD (đánh lại position, không trùng).
- Trước khi tạo mới: KIỂM trùng — lô/căn đã có trang thì **cập nhật**, không tạo trùng (hiến pháp: trùng nội bộ = xoá + 301).

## ẢNH — CẮT GỌT TỰ ĐỘNG
- `scripts/prep-anh.py`: auto-xoay → xoá EXIF/GPS → smart-crop giữ chủ thể → resize + nét → nén ~150KB → đặt tên `images/listings/<slug>/N.jpg`.
- Ảnh **hero** (toàn cảnh/aerial) ép `--ratio 4:3` cho khớp gallery (CSS ép 16:10 cover — ảnh dọc bị cắt xấu). Chi tiết trong `TIN-RAO-POSTING-KIT.md`.

## LUÔN KIỂM 2 GIAO DIỆN WEB + MOBILE (chú dặn — bất biến)
- Sau mỗi thay đổi giao diện, **tự chụp + soi cả desktop (1280px) lẫn mobile (390px)** cho đẹp/sang/tối ưu — 2 cái khác nhau, chú KHÔNG muốn phải nhắc.
- Chụp: `/opt/pw-browsers/chromium-*/chrome-linux/chrome --headless --no-sandbox --screenshot --window-size=W,H URL`.
- **Test đúng như production:** site dùng Vercel `cleanUrls:true` + `trailingSlash:false` → URL KHÔNG có `/` cuối, `../css` ở trang con resolve thành `/css`. `python3 -m http.server` thêm `/` cuối làm hỏng CSS → dùng server mô phỏng cleanUrls (không redirect thêm `/`) để soi trang `/nha-ban/`.
- Bug đã gặp + đã sửa: trang listing thừa `</div>` đẩy `<aside>` ra ngoài grid → desktop rớt sidebar, mobile sai thứ tự. Luôn cân bằng thẻ theo template `dat-nen/dong-thanh-845m2`.

Giờ cháu đọc 4 file ở BƯỚC 0, xác nhận đã nạp xong, rồi chờ chú thả tin đầu tiên.
