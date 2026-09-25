# CLAUDE.md — Dự án Nam Ban Villas
## Quy tắc làm việc bắt buộc cho mọi phiên

---

## 🎯 MỤC TIÊU TỐI THƯỢNG (ĐỨNG TRÊN MỌI THỨ)

**Đích cuối cùng của web = làm cho khách LIÊN HỆ: nhắn Zalo hoặc GỌI ĐIỆN 0978 758 788.**

- SEO/AEO/GEO/thiết kế/nội dung — tất cả chỉ là phương tiện dẫn tới hành động này.
- Mọi trang, mọi lô, mọi bài: luôn có đường dẫn rõ ràng, dễ bấm tới **Gọi / Zalo**.
- Khi phân vân "làm cái gì": chọn cái làm khách bấm gọi/Zalo nhiều hơn.
- Không hy sinh nút liên hệ để lấy thẩm mỹ. Đẹp mà không ai gọi = thất bại.

---

## NGUYÊN TẮC SỐ 1 — CHỦ WEB CHỈ BẤM, COPY, PASTE

**Chú (chủ web) không rành kỹ thuật. Mọi việc khó cháu tự làm hết.**

- Không bao giờ bảo chú "vào GitHub rồi làm X" — cháu dùng GitHub MCP tự làm.
- Không bao giờ bảo chú "mở terminal rồi chạy lệnh Y" — cháu chạy hết.
- Không bao giờ bảo chú "copy đoạn code này rồi paste vào file Z" — cháu edit file trực tiếp.
- Khi cần chú làm GÌ ĐÓ (ví dụ: share file ảnh, cung cấp thông tin thật), nói rõ đúng 1 việc duy nhất + kèm link trực tiếp nếu cần bấm vào đâu.
- Khi share hướng dẫn hoặc link, luôn kèm URL đầy đủ để chú chỉ cần bấm — không viết "vào trang X rồi tìm Y".

**Tiêu chuẩn: Chú chỉ cần bấm 1 cái, copy 1 đoạn, hoặc share 1 file — cháu lo phần còn lại.**

### CÁCH LÀM VIỆC (bất biến)
- **Tập trung làm ra kết quả** rồi báo cáo NGẮN GỌN. KHÔNG phân tích lan man, KHÔNG nói nhiều.
- Báo cáo = việc đã xong + link bấm. Bỏ đoạn giải thích dài, bỏ liệt kê phương án không làm.
- **Việc hiển nhiên/auto KHÔNG báo cáo** (đổi sđt môi giới → hotline site, làm mờ PII trên sổ/ảnh, nén ảnh, che tên/CCCD…) — đó là mặc định, làm ngầm. Chỉ báo việc cần chú biết hoặc cần chú quyết.
- Việc nhỏ + rõ → làm luôn, không hỏi. Chỉ hỏi khi thật sự cần chú quyết.

### CHUẨN CAO NHẤT — AEO/SEO/GEO/UX/UI + CÔNG NGHỆ MỚI NHẤT
- Mọi thứ làm ra phải đạt **chuẩn AEO/SEO/GEO/UX/UI tốt nhất hiện có** — không làm cho xong, làm là phải đỉnh.
- Luôn **cập nhật công nghệ, thuật toán, best-practice mới nhất & xịn nhất** (schema.org mới, Core Web Vitals, cách AI/Google index & trích dẫn hiện hành…) rồi áp dụng.
- Khi có cách mới tốt hơn → chủ động đề xuất/nâng cấp, không bám cái cũ chỉ vì quen.

### GIAO DIỆN — LUÔN CHECK CẢ 2 (DESKTOP + MOBILE)
- Mỗi lần làm/sửa giao diện: **tự kiểm KỸ cả bản máy tính VÀ bản điện thoại** — đẹp, sang, gọn, tối ưu nhất ở CẢ HAI. 2 màn hình khác nhau, không được chỉ ngắm 1 cái.
- Chú KHÔNG muốn phải xem chi tiết rồi nhắc từng chút — cháu tự lo mobile lẫn desktop trước khi push.
- Bắt buộc: responsive @media, ảnh không tràn ngang, chữ không bể, nút Gọi/Zalo luôn dễ bấm trên điện thoại.

### [CẤM] KHÔNG TỰ CHỤP ẢNH / RENDER PREVIEW ĐỂ KIỂM — TỐN TIME + TOKEN
- **KHÔNG** dùng Playwright/screenshot để "vẽ" xem thử. Kiểm giao diện bằng **đọc code + logic responsive** (breakpoint, flex/grid, đơn vị relative) — cháu đủ giỏi để tự tin không cần ảnh.
- "Check cả 2 màn hình" = rà @media + cấu trúc trong đầu, KHÔNG phải chụp hình.
- Muốn xem thật → dùng **link preview Vercel** trong PR comment (miễn phí, không tốn token của cháu).
- Chỉ chụp ảnh khi CHÚ YÊU CẦU rõ, hoặc khi nghi có bug hiển thị không thể suy ra từ code.

---

## NGUYÊN TẮC SỐ 2 — WORKFLOW BẮT BUỘC

```
ĐỀ XUẤT (cháu) → DUYỆT (chú gật/lắc) → LÀM (cháu tự làm hết)
```

- Với việc nhỏ (sửa chữ, đổi màu, fix bug): làm luôn không cần hỏi.
- Với việc lớn (restructure, thêm section mới, đổi logic): đề xuất trước, chờ chú gật.
- Sau khi làm xong: **luôn kèm link đầy đủ có https:// để chú bấm vào thẳng trang vừa thay đổi**.
- Nếu thay đổi nhiều trang: liệt kê từng link, 1 link / 1 dòng.
- Format bắt buộc: `👉 https://nambanvillas.vn/ten-trang/` (phải có https:// để bấm được ngay)

---

## NGUYÊN TẮC SỐ 3 — THÔNG TIN DỰ ÁN

- **Repo:** `doanquocduyet/nambanvillas` (GitHub)
- **Branch dev:** `claude/dreamy-ritchie-xBezi` → merge vào `main` = deploy production
- **Site live:** nambanvillas.vn (Vercel, auto-deploy từ main)
- **Hotline:** 0978 758 788
- **Stack:** Static HTML + CSS + Vanilla JS (không framework, không bundler)
- **Font:** Plus Jakarta Sans Variable (jsDelivr CDN)
- **Design tokens:** --green:#1A3D2B · --gold:#C9A84C · --bg:#F7F3EE · --bg2:#FFFFFF

---

## NGUYÊN TẮC SỐ 4 — QUY TẮC KỸ THUẬT BẮT BUỘC

- **[CẤM TUYỆT ĐỐI]** Không dùng regex DOTALL `.*?` để xóa/sửa khối HTML/CSS — đã gây mất dữ liệu 2 lần.
- Luôn dùng `str_replace` khớp CHÍNH XÁC, DUY NHẤT.
- Verify kết quả sau mỗi thay đổi trước khi push.
- Gold (#C9A84C) chỉ dùng ở: mobile nav call button, Pain section numbers, Notes editorial border-left, hover on dark bg.
- Popup: localStorage (không phải sessionStorage) — hiện đúng 1 lần trong đời user.
- **[KHÔNG GỘP BÀI — CHỐT 23/9/2026]** Bài cùng chủ đề **GIỮ RIÊNG**, không gộp, không 301 sang nhau. Mỗi bài nhắm **một câu người ta search khác nhau** — "tuyến tránh khi nào xong" ≠ "sân bay ảnh hưởng gì" ≠ "giá bao nhiêu một mét". Gộp là mất một cửa vào Google. Đã đo: 28 bài, **0 cặp trùng từ khoá trên 30%** → không có chuyện tự cắn nhau.
  - Đổi lại, giữ riêng **bắt buộc phải NỐI THÀNH CỤM**: cuối mỗi bài có khối `.cum-chu-de` trỏ sang 3 bài anh em, **chữ neo là CÂU HỎI bài đích trả lời** (cấm "xem thêm", "tại đây"). Bài lẻ loi mới là bài yếu — không phải bài ngắn.
  - Thêm bài mới cùng cụm → chạy `python3 scripts/noi-cum-chu-de.py`. Checker mục 11 chặn nếu bài trong cụm không nối nhau.
- **[LÂM HÀ LUÔN KÈM NAM BAN — CHỐT 24/9/2026]** Chữ "Lâm Hà" ở bất kỳ đâu (thân bài, title, mô tả, schema, llms.txt) PHẢI có "Nam Ban" ngay bên cạnh: "Nam Ban, Lâm Hà" · "Nam Ban Lâm Hà" · "giá đất Nam Ban Lâm Hà" (thứ tự Nam Ban đứng TRƯỚC Lâm Hà). Khu trong xã Nam Ban (Mê Linh, Đông Thanh, Gia Lâm…) viết "Mê Linh, Nam Ban, Lâm Hà". Xã khác (Nam Hà, Đinh Văn) viết "Nam Hà (giáp Nam Ban), Lâm Hà" — KHÔNG ghi là thuộc Nam Ban. Sửa hàng loạt: `python3 scripts/lam-ha-kem-nam-ban.py`; checker mục 18 chặn.
- **[TRANG ĐANG TOP — KHÔNG ĐỤNG TITLE/H1/URL — CHỐT 24/9/2026]** Trang đang có thứ hạng (vd `/dat-nam-ban-gia-re/` top 4 "giá đất nam ban", trang chủ, hub Đất Nền): KHÔNG đổi URL, KHÔNG viết lại title/H1. Chỉ được: sửa số sai, thêm nội dung/FAQ bên dưới, chỉnh mô tả. Title/H1 do script sinh chỉ đổi theo THÁNG, không đưa ngày hay số lô tuần vào (checker mục 19 chặn).
- **[KHÔNG BAO GIỜ TỰ XOÁ TIN — CHỐT 24/9/2026]** Tin rao theo ngày, bảng giá theo tuần, mục Cập Nhật Thị Trường, bài Tin Liên Quan, card cụm, lô/nhà đã bán: **GIỮ TOÀN BỘ, kèm ngày tháng**. Đây là dữ liệu index quý nhất (lịch sử có ngày = bằng chứng thật cho Google/AI). Tin cũ chỉ được TỤT XUỐNG, không được gỡ. Script và Routine KHÔNG được có lệnh cắt "giữ tối đa N".
- **[TẠO GÌ MỚI LIÊN QUAN ĐĂNG TIN → GHI VÀO PHIẾU ĐĂNG TIN NGAY — CHỐT 25/9/2026]** Mỗi khi tạo trang mới nhận lô (vd trang ngộp, trang vườn), nhãn `data-nhan` mới, hay luật chữ/giá mới: cập nhật mục "🆕 CẬP NHẬT" đầu `docs/package/MO-O-DANG-TIN.md` (bảng nhãn, danh sách trang tự cập nhật, checklist) **trong cùng PR**. Ô đăng tin chỉ đọc phiếu đó — không ghi là ô đó không biết.
- **[GIÁ ĐẤT HÔM NAY — TIN TRƯỚC, TỔNG HỢP SAU — CHỐT 25/9/2026]** Mỗi tuần trên `/thi-truong/gia-dat-nam-ban-hom-nay/`: tin rao trong tuần → lô mới lên Nam Ban Villas → **Tổng hợp tuần là mục CUỐI**. Script `cap-nhat-gia-hom-nay.py` tự dựng theo thứ tự này.
- **[NÉN ẢNH BẮT BUỘC]** Mọi ảnh MỚI trước khi commit phải chạy `python3 scripts/nen-anh.py <file/thư-mục>` (max 1600px, JPEG q82, chỉ ghi đè nếu nhỏ hơn thật). Ảnh từ điện thoại thường 3–5MB — không được đưa thẳng lên site. Ảnh cũ đã tối ưu sẵn, nén lại không lợi → chỉ nén ảnh mới.

---

## NGUYÊN TẮC SỐ 5 — TINH THẦN THƯƠNG HIỆU (FRIENDLY LUXURY)

**Định hướng tối cao: FRIENDLY LUXURY — sang trọng nhưng dễ gần. Ưu tiên số 1 là TRẢI NGHIỆM NGƯỜI DÙNG và việc khách BẤM LIÊN HỆ. Đẹp mà dễ chịu, dễ gần, đơn giản — không xa cách, không phô trương.**

- Định vị: "Đọc rủi ro, không bán giấc mơ" — dám nói đừng mua.
- **Giọng văn:** thẳng, số thật, không tính từ rỗng ("tuyệt đẹp", "lý tưởng"). Thân thiện qua sự RÕ RÀNG & CHÂN THÀNH, KHÔNG qua chữ sến/trẻ con ("chào bạn", "nhắn mình", "xem thử" → CẤM).
  - **[CẤM] Hạn chế tối đa xưng hô ngôi thứ nhất** (mình / tôi / em / chúng tôi / chúng mình). Cần nhắc chủ thể → viết **"Nam Ban Villas"** (ngôi thứ ba).
  - **[CẤM TUYỆT ĐỐI] KHÔNG BAO GIỜ viết "chú" / "cháu" lên web.** Đây là cách xưng hô RIÊNG giữa chủ web và trợ lý trong lúc trao đổi — **không phải** cách web nói với khách lạ.
    - Sai: *"Nếu chú là người Hà Nội…"* · *"Sơ đồ cháu gửi ngay"* · *"Cháu đang sống tại đây"*
    - Đúng: chủ thể là **"Nam Ban Villas"**, khách là **"bạn"** hoặc **"anh/chị"**. Hoặc viết thẳng không cần đại từ.
    - Lỗi này ĐÃ XẢY RA THẬT: 11 chỗ lọt ra trang công khai. Checker nay có bẫy `[Xưng hô chú/cháu]` chặn cứng, **chạy trên mọi trang, không có ngoại lệ** (kể cả tuỳ bút).
    - Chỉ hợp lệ khi là danh từ: *ghi chú · chú ý · chú trọng · chú thích · con cháu*.
  - **[CẤM — CHỐT 24/9/2026] KHÔNG BAO GIỜ để khách đọc thấy chữ máy móc:** script, tự động, auto, bot, AI, nhập tay, thuật toán, "hệ thống tự…". Nam Ban Villas là **một đội ngũ**: viết "đội ngũ Nam Ban Villas tổng hợp mỗi thứ Hai…", hoặc "chúng tôi" khi thật cần. Kể cả thành ngữ "không tự động nghĩa là" → "không mặc nhiên". Ngoại lệ: "béc tưới tự động" (tiện ích của lô). Checker mục 20 chặn (thân trang, title, meta, alt, JSON-LD, llms.txt).
  - Vẫn giữ chất đẳng cấp, người lớn, đáng tin — thân thiện chứ không xuề xòa.
- **Thẩm mỹ FRIENDLY LUXURY:** giữ xanh (#1A3D2B) + gold (#C9A84C) làm nhận diện, nhưng LÀM MỀM: bo góc tròn hơn (radius lớn), nền ấm, bóng đổ mềm, nhiều khoảng thở. Dễ chịu, dễ nhìn, không cứng/lạnh.
  - **Icon:** dùng ICON TUYẾN MẢNH (line SVG, stroke ~1.7) cho ấm & thân thiện. **VẪN KHÔNG DÙNG EMOJI** (emoji màu = kém sang). Icon mảnh THAY cho emoji.
  - **Liên hệ là chính:** nút Gọi/Zalo to, bo tròn, dễ bấm, hiện ở mọi nơi; mobile có thanh Gọi/Zalo dán đáy. Mọi thiết kế ưu tiên đưa khách tới hành động gọi/Zalo.
- Không bịa bất cứ điều gì — số liệu, testimonial, tên người đều phải thật.

---

## NGUYÊN TẮC SỐ 6 — VERCEL & DEPLOY

- **Dự án Vercel chính (DUY NHẤT được giữ):** `nambanvillas` — slug: `duyet-s-projects`
- **Chỉ 1 project Vercel nối repo** — nếu phát hiện có 2–3 project cùng nối: báo ngay, đây là vấn đề nghiêm trọng (quota build + SEO duplicate content).
- **Quota build Vercel free:** 100 lượt/ngày — mỗi push tốn 1 lượt. Không push thừa.
- **Deploy production = merge PR vào `main`** — cháu dùng GitHub MCP tự merge, không cần chú vào GitHub.
- **Xem bản demo (preview):** link preview có sẵn trong PR comment do Vercel bot đăng tự động sau mỗi push.
- **Khi cần chú Delete project Vercel thừa:** link trực tiếp dạng `https://vercel.com/duyet-s-projects/[tên-project]/settings` → kéo xuống cuối → Delete Project → gõ tên project xác nhận.

---

## FILE QUAN TRỌNG

- `docs/package/NGUON-TIN-VIDEO.md` — **HỆ THỐNG NGUỒN TIN** (web + YouTube API + TikTok) cho bot cập nhật liên tục trang tin-rao.
- `docs/FORM-DANG-TIN.md` — **FORM ĐĂNG TIN RAO** chuẩn cho trang tin-rao-dat-nam-ban-moi (bot + người bám theo: lọc → thông số → viết → HTML mẫu). Chuẩn AEO/SEO/GEO.
- `docs/TIN-CAP-NHAT-TUAN.md` — **TIN CẬP NHẬT HÀNG TUẦN** (mục Tin Liên Quan / Thị Trường): mỗi tuần lấy Ý 1 tin báo hợp Nam Ban → VIẾT LẠI giọng Villas + ẢNH của mình → tạo bài nội bộ `/thi-truong/<slug>/` → đưa lên số 01. **CẤM trỏ link/ảnh web khác, cấm copy, cấm bịa số.**
- `docs/DANG-CUM-MOI.md` — **HƯỚNG DẪN ĐĂNG CỤM MỚI**: khi có 1 CỤM (nhiều nền cùng khu) → tạo trang `/dat-nen/cum-<slug>/` + nén ảnh + chèn card vào `cum-moi-nam-ban/index.html` (mục "Cụm đang mở") + thêm sitemap. Cụm mới trên cùng, KHÔNG xoá card cũ; bán hết thì giữ card, gắn nhãn "Đã bán". Lô lẻ KHÔNG đưa vào trang Cụm Mới. **Cuối file: chuẩn KEYWORD + AEO/SEO/GEO cho cụm — mỗi cụm mới cập nhật ItemList + dải giá của hub, link ngược hub.**
- `scripts/them-nut-goi.py` — **NÚT GỌI ĐÚNG CHỖ** (thẻ lô, sau khối rủi ro, giữa bài, đầu trang dịch vụ, mục cuối menu điện thoại). Chạy lại được; bẫy 14 trong `kiem-bo-loc.py` chặn trang thiếu. Thêm trang/thẻ mới → chạy lại.
- **Trang theo cây trồng** `/ban-vuon-nam-ban/` (gộp mọi loại vườn, chủ web chốt 25/9/2026): lô vào trang theo nhãn `ca-phe` / `bo` / `cay-an-trai` / `vuon-hoa` trong `data-nhan` thẻ hub — CHỈ gắn khi vườn/cây nằm TRÊN chính lô (xem `docs/package/MO-O-DANG-TIN.md`).
- `scripts/cap-nhat-gia-hom-nay.py` — **GIÁ ĐẤT HÔM NAY tự tính từ lô thật** (khoảng giá phổ biến + giá trung bình cắt 10% hai đầu — trên web ghi "giá trung bình", KHÔNG ghi "trung vị"; lịch sử `data/gia-tuan.json`). Chạy bằng GitHub Actions `gia-tuan.yml`: NGAY khi hub đổi + mỗi thứ Hai. Mỗi tuần 1 ô (trong tuần làm mới, sang tuần thêm ô), KHÔNG xoá ô cũ. Không bao giờ điền số tay vào bảng tuần.
- `docs/package/DANG-TIN-KHONG-LOI.md` — **QUY TRÌNH ĐĂNG TIN KHÔNG LỖI**: mỗi mục là 1 lỗi ĐÃ XẢY RA THẬT (redirect 404 toàn tập, ảnh hero hại LCP, hub thiếu ItemList, trang mồ côi, link gãy…). Kèm `scripts/kiem-tra-truoc-khi-dang.py` — chạy trước mỗi lần push; CI cũng chạy tự động.
- `docs/fb-lam-lai-token.md` — **LÀM LẠI TOKEN FACEBOOK** khi thiếu quyền comment: 5 bước copy–dán, kèm bảng đọc log để tự kiểm (`Token: loại PAGE · KHÔNG HẾT HẠN`). Luật: link web CHỈ nằm ở comment đầu, không bao giờ ở thân bài.
- `docs/package/DANG-TIN-CHO-THUE.md` — **PHIẾU ĐĂNG TIN CHO THUÊ**: web đã có hub `/cho-thue/`; tin thuê khác tin bán ở giá theo tháng/đêm (`businessFunction: LeaseOut`), 4 trạng thái không bao giờ xoá trang, ảnh không lộ vị trí vì có người đang ở, và luật **đủ 3 tin cùng nhánh mới mở URL nhánh**.
- `docs/package/CHO-THUE-BAN-DO-KEYWORD.md` — **BẢN ĐỒ KEYWORD CHO THUÊ**: 7 vùng key, luật 1 ý định = 1 URL, cặp key dễ tự cắn nhau (`homestay nam ban` khách du lịch vs `cho thuê homestay nam ban` chủ cơ sở), số tham chiếu thị trường (phân biệt số xác minh thật với số ghi nhận trên tin rao).
- `docs/package/MO-O-DANG-TIN.md` — **PHIẾU MỞ Ô ĐĂNG TIN** (ô chuyên code/đăng lô-cụm): quy trình lọc → viết → cắt/nén ảnh → dựng trang → chèn card → merge. Chuẩn AEO/SEO/GEO/UX/UI + luật sổ/bản vẽ.
- `docs/package/FB-KHO-HOOK.md` — **KHO 30 CÂU MỞ ĐẦU FACEBOOK** theo 5 cơ chế tâm lý, kèm bảng số thật để điền vào hook. Luật: số trong hook phải là số thật, không có số thì đổi hook.
- `docs/package/FB-LICH-30-NGAY.md` — **LỊCH CONTENT FACEBOOK 30 NGÀY**: mỗi tuần 2 giáo dục · 2 viral · 1 cá nhân · 1 seeding · 1 tương tác, kèm chủ đề + góc tiếp cận + số hook. Đăng tối 19–21h, tách với tin rao (10h) và bài viết (8h) đã tự động.
- `docs/package/MO-O-VIET-CONTENT.md` — **PHIẾU MỞ Ô VIẾT CONTENT** (ô chuyên viết bài SEO, tách khỏi ô code): keyword mục tiêu, chuẩn mỗi bài (SEO/AEO/GEO/Article schema), danh sách bài trụ + cẩm nang khu, ranh giới với ô đăng tin, branch content riêng.
- `docs/package/` — **PROJECT OS PACKAGE** (00 audit · 02 working-os · 04 product-taste · 06 project-knowledge · 08 implementation). Phiên mới đọc trước để nạp toàn bộ dự án.
- `docs/HIEN-PHAP-3-WEB.md` — **HIẾN PHÁP HỆ 3 WEB** (Panorama·Villas·Greenspace). Đọc TRƯỚC khi làm bất cứ việc gì về keyword/SEO/AEO/link/canonical. Luật vàng: cùng keyword KHÁC INTENT → không cắn nhau; Villas ôm key GIAO DỊCH (lô thật, giá thật); Panorama đứng ĐỘC LẬP — Villas/Greenspace KHÔNG link sang Panorama; Villas↔Greenspace link 2 chiều thoải mái.
- `docs/HO-SO-TONG-NAMBAN-MAX.md` — Hồ sơ tổng toàn diện (1903 dòng)
- `docs/TU-DUY-TINH-TUE.md` — Tư duy & tinh tuý dự án (23 nguyên tắc)
- `index.html` — Trang chủ (606 dòng)
- `css/style.css` — Toàn bộ CSS
- `js/main.js` — Toàn bộ JS
