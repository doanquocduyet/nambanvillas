# HỆ THỐNG NGUỒN TIN — CẬP NHẬT LIÊN TỤC (web + YouTube + TikTok)
*Sơ đồ nguồn cho trang tin-rao. Mục tiêu: cập nhật liên tục, luôn tìm cách kéo TikTok/YouTube về tự động.*

## ENGINE LIÊN TỤC — bot hàng ngày
`scripts/daily-listings.mjs` (workflow `daily-listings.yml`, cron 7h07 VN, MỖI NGÀY) →
1. **Web search** (Claude API) — tin chữ (batdongsan, nhatot, alonhadat...) + hint `site:youtube.com`, `site:tiktok.com`.
2. **YouTube Data API** — nếu có secret `YOUTUBE_API_KEY`: quét video mới 3 ngày (8 truy vấn: bán đất Nam Ban, đất vườn, Đông Thanh, Mê Linh, view Đà Lạt...), đọc **full mô tả** (giá/diện tích/vị trí).
3. Lọc theo FORM (≥4/7 dữ kiện + blocklist) → 1–2 tin CHẤT → viết lại bỏ SĐT → chèn trang tin-rao, giữ 20 ngày.
→ Đây là phần **tự động, chạy liên tục không cần đụng tay**.

## TRẠNG THÁI TỪNG NGUỒN
| Nguồn | Mức tự động | Cần gì |
|---|---|---|
| Web (tin chữ) | ✅ Tự động | ANTHROPIC_API_KEY |
| **YouTube** | ✅ Tự động (đọc full mô tả) | + YOUTUBE_API_KEY (miễn phí) |
| **TikTok** | 🟡 Bán tự động | web search site:tiktok.com (yếu) + **gửi link** |

## TIKTOK — luôn tìm cách kéo về tự động
- **Hiện tại (miễn phí):** (a) web search `site:tiktok.com` trong bot — Google index yếu, ra ít; (b) **gửi link** → `node scripts/extract-video.mjs <link>` bóc caption+kênh qua **oEmbed chính thức** → viết tin theo FORM. Đây là cách chất lượng cao nhất hiện có.
- **Nâng cấp khi TikTok ra nhiều deal (tốn tiền):** thuê API/scraper bên thứ 3 (Apify TikTok Scraper, TikAPI, ScrapTik) → theo dõi 5–10 kênh môi giới Nam Ban, kéo video mới tự động vào bot. Chỉ làm khi TikTok là nguồn chính đáng đầu tư.
- **Rà lại định kỳ:** mỗi vài tháng kiểm xem TikTok đã mở API search miễn phí/ổn định chưa để tự động hoá thêm.

## LUẬT (mọi nguồn)
- Chỉ bóc **DỮ KIỆN** (giá/diện tích/thổ cư/vị trí/sổ) + viết lại bằng lời mình. **KHÔNG tải/đăng lại video/ảnh/thumbnail** (bản quyền). `source` = link gốc, ghi "Nguồn: video kênh [tên]".
- Tin thị trường **CHƯA kiểm chứng** — khác lô Villas đã kiểm tra. Dẫn về Zalo 0978 758 788.

## BẬT / VẬN HÀNH
- **Tự động YouTube:** tạo YouTube Data API key → GitHub Secrets `YOUTUBE_API_KEY`. (Web đã chạy nếu có ANTHROPIC_API_KEY.)
- **TikTok gửi link:** người thấy video hay → gửi link → phiên có GitHub bóc + đăng (hoặc `extract-video.mjs` rồi viết theo FORM).
