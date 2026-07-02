# CLAUDE.md — Dự án Nam Ban Villas
## Quy tắc làm việc bắt buộc cho mọi phiên

---

## NGUYÊN TẮC SỐ 1 — CHỦ WEB CHỈ BẤM, COPY, PASTE

**Chú (chủ web) không rành kỹ thuật. Mọi việc khó cháu tự làm hết.**

- Không bao giờ bảo chú "vào GitHub rồi làm X" — cháu dùng GitHub MCP tự làm.
- Không bao giờ bảo chú "mở terminal rồi chạy lệnh Y" — cháu chạy hết.
- Không bao giờ bảo chú "copy đoạn code này rồi paste vào file Z" — cháu edit file trực tiếp.
- Khi cần chú làm GÌ ĐÓ (ví dụ: share file ảnh, cung cấp thông tin thật), nói rõ đúng 1 việc duy nhất + kèm link trực tiếp nếu cần bấm vào đâu.
- Khi share hướng dẫn hoặc link, luôn kèm URL đầy đủ để chú chỉ cần bấm — không viết "vào trang X rồi tìm Y".

**Tiêu chuẩn: Chú chỉ cần bấm 1 cái, copy 1 đoạn, hoặc share 1 file — cháu lo phần còn lại.**

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

---

## NGUYÊN TẮC SỐ 5 — TINH THẦN THƯƠNG HIỆU

- Định vị: "Đọc rủi ro, không bán giấc mơ" — dám nói đừng mua.
- Giọng văn: thẳng, số thật, không tính từ rỗng ("tuyệt đẹp", "lý tưởng").
- Thẩm mỹ: "Im lặng mà sang" — không emoji, không banner, không gấp gáp.
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

- `docs/FORM-DANG-TIN.md` — **FORM ĐĂNG TIN RAO** chuẩn cho trang tin-rao-dat-nam-ban-moi (bot + người bám theo: lọc → thông số → viết → HTML mẫu). Chuẩn AEO/SEO/GEO.
- `docs/package/` — **PROJECT OS PACKAGE** (00 audit · 02 working-os · 04 product-taste · 06 project-knowledge · 08 implementation). Phiên mới đọc trước để nạp toàn bộ dự án.
- `docs/HIEN-PHAP-3-WEB.md` — **HIẾN PHÁP HỆ 3 WEB** (Panorama·Villas·Greenspace). Đọc TRƯỚC khi làm bất cứ việc gì về keyword/SEO/AEO/link/canonical. Luật vàng: cùng keyword KHÁC INTENT → không cắn nhau; Villas ôm key GIAO DỊCH (lô thật, giá thật); Panorama đứng ĐỘC LẬP — Villas/Greenspace KHÔNG link sang Panorama; Villas↔Greenspace link 2 chiều thoải mái.
- `docs/HO-SO-TONG-NAMBAN-MAX.md` — Hồ sơ tổng toàn diện (1903 dòng)
- `docs/TU-DUY-TINH-TUE.md` — Tư duy & tinh tuý dự án (23 nguyên tắc)
- `index.html` — Trang chủ (606 dòng)
- `css/style.css` — Toàn bộ CSS
- `js/main.js` — Toàn bộ JS
