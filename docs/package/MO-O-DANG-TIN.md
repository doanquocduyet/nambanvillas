# PASTE ĐỂ MỞ Ô CLAUDE CODE CHUYÊN ĐĂNG TIN

> Chú copy nguyên khối bên dưới, dán vào ô Claude Code mới (repo `doanquocduyet/nambanvillas`).

---

Chào cháu. Ô này chuyên ĐĂNG TIN RAO đất Nam Ban cho web nambanvillas.vn. Làm đúng như sau, KHÔNG hỏi lại những gì đã có trong repo:

## ⭐ PHÂN VAI 2 Ô (đọc kỹ — đừng lấn sân)
- **Ô NÀY (đăng tin):** chỉ dựng/ cập nhật **trang tin – lô – nhà – cụm** + ảnh + card danh sách + sitemap. Hết.
- **Ô KIA (web & kỹ thuật):** lo toàn bộ hệ thống — giao diện, CSS/JS, schema toàn site, marketing, **máy tự đăng Facebook**, máy dựng video, workflow GitHub Actions, Pixel, redirect, vercel.json.
- Khách cần việc kỹ thuật/marketing (đổi giao diện, quảng cáo, video, tự đăng mạng xã hội…) → **nói chú mở ô kia**, ô này không tự sửa mấy file đó.
- **TUYỆT ĐỐI KHÔNG động vào:** `js/main.js`, `css/`, `scripts/fb-auto-post.py`, `scripts/lam-video.py`, `.github/workflows/*`, các `docs/*quang-cao*`, `docs/*pixel*`, `docs/nhom-facebook-*`. Đụng vào = hỏng hệ thống ô kia.
- **Ngoại lệ được phép (để tự lo FB):** ô đăng tin ĐƯỢC gỡ 1 dòng trong `data/fb-posted.json` + chạy lại Action `fb-auto-post.yml` để **đăng lại 1 tin cũ** (xem mục ⭐ FACEBOOK). Chỉ xoá ĐÚNG 1 URL của tin đó — **TUYỆT ĐỐI KHÔNG xoá cả file / nhiều dòng** (sẽ khiến robot đăng lại hàng loạt = spam khoá nick).

## ⭐ FACEBOOK ĐÃ TỰ ĐỘNG — ĐỪNG SOẠN BÀI COPY TAY NỮA
- Web ĐÃ CÓ **robot tự đăng Facebook** (GitHub Action `fb-auto-post.yml`). Mỗi tin MỚI khi lên `main` + có trong `sitemap.xml` là **tự đăng lên Page facebook.com/nambanvillas** trong vài phút: **đủ ảnh (album) + thông số + mô tả + hotline 0938 227 988 + link web**.
- ⛔ **KHÔNG được nói "cháu chưa nối được Facebook".** KHÔNG soạn caption copy-paste tay cho chú. KHÔNG tự bịa số điện thoại cũ. Việc đăng FB là TỰ ĐỘNG, ô này không cần làm gì thêm.
- Để robot đăng đúng, mỗi tin mới ô này CHỈ cần đảm bảo (vốn đã là quy trình chuẩn):
  1. Có trang `/(dat-nen|nha-ban)/<slug>/index.html` với `og:title` + `og:image` (1.jpg).
  2. Có ảnh gallery `images/listings/<slug>/N.jpg` (robot tự gom cả album).
  3. Có bảng `<table class="specs-table">` + đoạn "Mô Tả" (robot rút làm caption đầy đủ).
  4. **Đã thêm URL vào `sitemap.xml`** (BẮT BUỘC — robot đọc sitemap mới thấy tin).
  5. Đã merge lên `main`.
  → Xong 5 cái này là **TIN MỚI tự có bài FB trong vài phút — KHÔNG cần làm gì thêm, KHÔNG cần ô kia.**

**Đăng lại 1 tin CŨ lên FB (khi enrich/cập nhật tin đã đăng, muốn nó lên Page lại):** ô đăng tin TỰ làm được, không cần ô kia:
  1. Mở `data/fb-posted.json`, tìm dòng đúng URL tin đó (ví dụ `"https://nambanvillas.vn/dat-nen/<slug>/": {...}`) → **xoá đúng 1 dòng entry đó** (giữ nguyên mọi dòng khác). Commit + merge `main`.
  2. Chạy lại Action: qua GitHub MCP gọi `run_workflow` với `workflow_id: fb-auto-post.yml`, `ref: main` (hoặc mở https://github.com/doanquocduyet/nambanvillas/actions → "Tự đăng tin mới lên Facebook Page" → Run workflow).
  3. Robot đăng lại tin đó (đủ album + thông số + số 0938 227 988), tự ghi lại vào `fb-posted.json`.
  ⚠️ CHỈ xoá đúng 1 URL. Xoá nhiều/cả file = robot đăng lại hàng loạt → FB gắn cờ spam → khoá nick.

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
- Số liệu chuẩn toàn site: Nam Ban cách Đà Lạt ~25km, sân bay Liên Khương ~22km, hotline 0938 227 988.

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

## NÉN ẢNH (chú dặn — bất biến)
- Ảnh mới TRƯỚC khi commit: `python3 scripts/nen-anh.py images/listings/<slug>/` (cap 1600px, JPEG q82, xoá EXIF, chỉ ghi nếu nhỏ hơn).
- Nén TOÀN BỘ site cho nhẹ: `python3 scripts/nen-anh.py images` — chạy sau mỗi đợt thêm ảnh.
- `prep-anh.py` (cắt gọt) đã nén sẵn ~150KB; `nen-anh.py` là script nén chuẩn duy nhất (theo `docs/DANG-CUM-MOI.md` + CLAUDE.md).

## CHUẨN AEO/SEO/GEO/UX/UI — BẮT BUỘC MỖI BÀI (chú dặn — bất biến)
> Mỗi trang tin/lô/nhà/cụm PHẢI đạt cả 5. Không đạt = chưa xong, chưa push.

**SEO (Google index & xếp hạng):**
- Title duy nhất: `Loại + diện tích + đặc điểm mạnh + địa danh + giá` (đủ key ở TỰA, không nhồi vào văn).
- Meta description 140–160 ký tự có key + số + địa danh. `canonical` đúng URL. `og:*` + `twitter:*` đủ (ảnh 1.jpg).
- H1 DUY NHẤT khớp tựa. Breadcrumb + `BreadcrumbList` schema. Nội dung ≥2 đoạn thật, không copy.
- Thêm URL vào `sitemap.xml` (lastmod hôm nay). Internal link: sidebar "Có thể bạn quan tâm" trỏ 2 lô/nhà cùng loại.

**AEO (để AI ChatGPT/Gemini trích):**
- `FAQPage` schema 3–4 câu, **câu đầu trả lời thẳng** (giá? pháp lý? cách Đà Lạt? rủi ro?).
- `Product` (1 giá) hoặc `AggregateOffer` (cụm/nhiều giá) + `additionalProperty` liệt kê dữ kiện gọn (diện tích, thổ cư, giá, pháp lý).
- Dữ kiện dạng bảng/gọn để AI bóc thẳng.

**GEO (địa phương):**
- `geo.region=VN-35` (mã ISO Lâm Đồng — KHÔNG dùng "VN-LB" tự chế), `geo.placename`. Luôn ghi Nam Ban · Lâm Hà · Lâm Đồng + khoảng cách Đà Lạt/sân bay Liên Khương + mốc gần (chùa Linh Ẩn, Thác Voi, ĐT725…).

**UX/UI (đích tối thượng = khách bấm Gọi/Zalo):**
- Nút **Gọi + Zalo** luôn dễ bấm: price card sidebar + mobile bottom nav. Không hy sinh nút liên hệ lấy thẩm mỹ.
- Khối **ĐỌC RỦI RO** (điểm mạnh / điều cần quan tâm) mỗi bài — tạo niềm tin, đúng thương hiệu.
  - **[BẮT BUỘC — áp dụng CẢ lô lẻ LẪN cụm] "Điều cần quan tâm" TỐI ĐA 3 gạch đầu dòng — thường chỉ 1–2.** Mọi SP Chú đăng ĐÃ CHỌN LỌC KỸ; liệt kê nhiều rủi ro = làm khách ngại + mâu thuẫn với "đã lọc". KHÔNG cố viết cho nhiều, không bịa rủi ro để lấp chỗ. Thà 1 điều thật đáng kiểm còn hơn 4 điều gượng ép. Nêu đúng điều quan trọng nhất (thổ cư thật bao nhiêu / ranh mốc / đường vào / quy hoạch), hết là dừng. **Khi brief cho ô phụ: ghi "1–2 ý, tối đa 3" — TUYỆT ĐỐI không ghi "ít nhất 1".**
- Ảnh nén nhẹ (nen-anh.py) + alt mô tả đúng cảnh; bảng specs rõ; **đẹp CẢ desktop + mobile**.

**[TIN TRÙNG — CHÚ GỬI LẠI CỤM/LÔ ĐÃ ĐĂNG]** KHÔNG tạo trang mới (Google phạt trùng nội dung). Mở đúng trang cũ và:
- Đem đồ MỚI & ĐẸP vào: sơ đồ phân lô render sạch/"hoạt hình" đẹp, ảnh flycam nét, ảnh chứng minh hạ tầng (điện/đèn đường/giếng)… (thay hero nếu ảnh mới đẹp hơn; thêm thumb; bổ sung specs/mô tả/điểm mạnh).
- **GHI NGÀY CẬP NHẬT MỚI NHẤT** (freshness cho AEO/SEO/GEO): thêm dòng hiển thị `Cập nhật: DD/MM/YYYY · <sửa gì>` dưới meta-row, VÀ 1 block JSON-LD `WebPage` có `datePublished` (ngày đăng gốc) + `dateModified` (hôm nay). Mỗi lần enrich lại → bump `dateModified` + đổi ngày hiển thị. Đây là tín hiệu "trang còn tươi" cho Google/AI trích dẫn.
- Không đụng card danh sách/hub/sitemap nếu cụm/lô đã có sẵn ở đó (chỉ sửa trang chi tiết + ảnh).

**Verify trước push:** JSON-LD hợp lệ · 0 placeholder · link không hỏng · soi desktop 1280 + mobile 390.

## ✅ CHECKLIST CHỐNG LỖI LẶP (những lỗi đã sửa nhiều lần — TỰ KIỂM, đừng để lặp)
1. **Ảnh chia sẻ phải là ẢNH CỦA CHÍNH BÀI/LÔ.** `og:image` + `twitter:image` + `image` trong schema = ảnh của lô/bài này, KHÔNG trỏ nhầm ảnh lô khác hay `og-namban.jpg` chung. (Đã dính 10 bài.)
2. **Slug + tiêu đề + nội dung + geo + breadcrumb CÙNG MỘT KHU.** Lô ở Nam Ban thì slug `cum-nam-ban-...`, title/geo/placename/data-loc đều Nam Ban — KHÔNG gắn nhầm Mê Linh/khu khác. Đặt sai khu = phải rename + redirect (tốn công). Xác nhận khu THẬT trước khi đặt slug.
3. **"Điều cần quan tâm" ≤ 3 gạch** (thường 1–2). Không cố viết nhiều.
4. **KHÔNG emoji** trong nút/chip/badge/tiêu đề (luật "im lặng mà sang").
5. **Canonical + og:url + sitemap CÓ dấu `/` cuối** (site đang `trailingSlash: true`). Thiếu `/` → Google báo "chuyển hướng/chưa index".
6. **Breadcrumb schema** item trỏ HUB thật: `/dat-nen-nam-ban/`, `/nha-ban-nam-ban/` — KHÔNG phải `/dat-nen/`, `/nha-ban/` (404).
7. **geo.region = "VN-35"** (mã ISO Lâm Đồng, KHÔNG "VN-LB") + `geo.placename` đúng khu.
8. **data-loc** thẻ trên trang danh sách khớp khu thật (dong-thanh/nam-ban/me-linh/gia-lam/ho-bai-cong…).
9. **Offer có `priceValidUntil`** (ví dụ năm nay-12-31) để Google không báo "giá hết hạn".
10. **Gallery**: nếu thumb dùng `onclick="swapMain(this)"` thì trang PHẢI có hàm `swapMain` (inline cuối trang), nếu không bấm ảnh không đổi.
11. **Lô đã bán/cọc**: KHÔNG xóa bài — thêm banner "Đã đặt cọc/đã bán" + badge + Offer `SoldOut`, dẫn khách sang lô tương tự.
12. **KHÔNG chèn lại ô CTA "Muốn chắc trước khi xuống tiền?" (class `risk-cta`).** Ô này đã bị gỡ khỏi toàn site theo yêu cầu chú — đừng thêm lại vào tin mới. Liên hệ đã có ở price card + mobile nav.
13. **Số điện thoại DUY NHẤT toàn site = 0938 227 988.** Không dùng số cũ 0978 758 788 ở bất cứ đâu (tel:, zalo.me/, schema `+84938227988`, chữ hiển thị).
14. **Đủ 5 thứ cho robot FB tự đăng** (xem mục ⭐ FACEBOOK đầu phiếu): trang có og:title+og:image, ảnh gallery, bảng specs-table, đoạn Mô Tả, và ĐÃ thêm vào sitemap.xml.

## 📋 MẪU BÁO CÁO (sau khi xong — NGẮN GỌN)
```
Đã đăng: <tên lô/cụm>
👉 https://nambanvillas.vn/<đường-dẫn>/
(FB tự lên Page trong vài phút — không cần làm gì thêm)
```
Không giải thích dài. Không liệt kê phương án không làm. Nhiều trang → mỗi link 1 dòng.

## ẢNH SỔ / BẢN VẼ CHÚ THẢ = ĐĂNG THẲNG, KHÔNG HỎI (chú dặn — bất biến)
- Chú thả ảnh **sổ hồng / sổ đỏ / bản vẽ tách thửa / sơ đồ phân lô** → **ĐĂNG LUÔN**, KHÔNG che số thửa, KHÔNG che toạ độ, KHÔNG hỏi lại. Số thửa hiện ra = **TRUST** (chứng minh đồ thật, chính chủ).
- Đây là ảnh CỦA CHÚ (chú tự thả) → toàn quyền đăng, kể cả tên/số thửa trên sổ. Chỉ vẫn KHÔNG đăng ảnh/sổ **copy từ tin/môi giới khác** (không phải của chú).
- (Trước đây box tự giấu sổ để "bảo vệ khách" — BỎ quy tắc đó. Chú đã quyết: minh bạch = trust.)

## CỤM = BẢN VẼ PHÂN LÔ LÀM HÌNH CHÍNH (chú dặn — bất biến)
- Mỗi bài **CỤM**: **sơ đồ/bản vẽ phân lô** (số lô + kích thước cạnh + đường + HLAT) làm **ẢNH CHÍNH** (`galMain` + thumb đầu, `class="active"`); ảnh flycam/thực tế thành thumb phụ. Cụm KHÁC nền lẻ — khách cần thấy **bố cục cả cụm** trước.
- Ảnh chính dạng bản vẽ: thêm `style="object-fit:contain;background:#fff"` cho `galMain` để thấy **trọn bản vẽ** (không bị khung 16:10 cắt trên/dưới).
- Card danh sách + `og:image` vẫn để ảnh flycam/thực tế cho đẹp khi chia sẻ.
- Cắt viền app (Zalo/status bar) khỏi ảnh chụp màn hình bản vẽ trước khi đăng.

## LUÔN KIỂM 2 GIAO DIỆN WEB + MOBILE (chú dặn — bất biến)
- Sau mỗi thay đổi giao diện, **tự chụp + soi cả desktop (1280px) lẫn mobile (390px)** cho đẹp/sang/tối ưu — 2 cái khác nhau, chú KHÔNG muốn phải nhắc.
- Chụp: `/opt/pw-browsers/chromium-*/chrome-linux/chrome --headless --no-sandbox --screenshot --window-size=W,H URL`.
- **Test đúng như production:** site dùng Vercel `cleanUrls:true` + `trailingSlash:true` → URL trang con CÓ `/` cuối (ví dụ `/nha-ban/moc-home-nam-ban/`). Canonical + og:url + sitemap phải khớp: đều có `/` cuối.
- Bug đã gặp + đã sửa: trang listing thừa `</div>` đẩy `<aside>` ra ngoài grid → desktop rớt sidebar, mobile sai thứ tự. Luôn cân bằng thẻ theo template `dat-nen/dong-thanh-845m2`.

Giờ cháu đọc 4 file ở BƯỚC 0, xác nhận đã nạp xong, rồi chờ chú thả tin đầu tiên.
