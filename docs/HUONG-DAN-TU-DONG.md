# Hướng dẫn: Cỗ máy tự động đưa web đến người có nhu cầu

Tài liệu này giải thích những gì đã được dựng sẵn (chạy tự động, không cần làm gì)
và những công tắc **chỉ chú bật được một lần** rồi để máy chạy mãi.

---

## PHẦN A — Đã tự động (không cần chú làm gì)

| Cơ chế | Tác dụng | File |
|--------|----------|------|
| **IndexNow** | Mỗi lần web đổi/thêm bài, tự báo Bing, Yandex, Naver... (qua đó tới ChatGPT Search & Copilot) | `.github/workflows/indexnow.yml` + `abdd063f81d049182d79e17f4239ad8f.txt` |
| **llms.txt** | "Bản đồ sạch" để ChatGPT, Claude, Perplexity, Gemini đọc và trích web đúng | `/llms.txt` |
| **robots.txt mở cửa AI** | Cho phép rõ ràng GPTBot, ClaudeBot, PerplexityBot, Google-Extended... dùng nội dung làm câu trả lời | `/robots.txt` |
| **RSS feed** | Bài mới tự gom vào `feed.xml` để nối sang mạng xã hội | `/feed.xml` + `scripts/build-feed.mjs` |
| **Cập nhật tin tức + feed hàng tuần** | Thứ Hai hàng tuần tự chạy, tự commit | `.github/workflows/weekly-update.yml` |

> Các cơ chế trên chạy ngầm. Mỗi khi có bài mới được đẩy lên, search engine và AI
> được báo trong vài phút.

---

## PHẦN B — Công tắc CHỈ chú bật được (mỗi việc làm 1 lần, ~10 phút)

Đây là phần quan trọng nhất. Không có nó, cỗ máy chạy ở mức "âm thầm";
có nó, chú nói thẳng với Google/Bing "web tôi đây, đọc hết đi".

### B1. Google Search Console (QUAN TRỌNG NHẤT)
1. Vào https://search.google.com/search-console
2. Thêm tài sản (Add property) → chọn "URL prefix" → nhập `https://nambanvillas.vn`
3. Chọn phương thức xác minh **"Thẻ HTML" (HTML tag)** → copy đoạn mã
4. Mở file `index.html`, tìm dòng có chữ `XÁC MINH GOOGLE SEARCH CONSOLE`,
   dán mã vào (hoặc gửi mã cho cháu, cháu dán giúp)
5. Quay lại Search Console bấm "Verify"
6. Vào mục **Sitemaps** → nhập `sitemap.xml` → Submit

→ Từ giờ Google index web nhanh hơn nhiều và chú thấy được người ta tìm từ khóa gì.

### B2. Bing Webmaster Tools (nuôi ChatGPT/Copilot)
1. Vào https://www.bing.com/webmasters
2. Chọn **"Import from Google Search Console"** (nhanh nhất) hoặc thêm thủ công
3. Submit sitemap `https://nambanvillas.vn/sitemap.xml`

→ Bing cấp dữ liệu cho ChatGPT Search và Microsoft Copilot.

### B3. Google Business Profile (hiện trên Google Maps)
1. Vào https://www.google.com/business
2. Tạo hồ sơ "Nam Ban Villas" — loại hình: Bất động sản / môi giới
3. Địa chỉ khu vực Nam Ban, Lâm Hà; thêm SĐT 0978 758 788, website, giờ mở cửa, ảnh

→ Khi ai tìm "bất động sản Nam Ban" gần khu vực, hồ sơ hiện kèm bản đồ.

### B4. Google Analytics 4 (xem khách từ đâu tới)
1. Vào https://analytics.google.com → tạo property cho nambanvillas.vn
2. Lấy Measurement ID dạng `G-XXXXXXXXXX`
3. Gửi ID cho cháu — cháu thay vào toàn bộ trang (hiện đang để placeholder `G-XXXXXXXXXX`)

---

## PHẦN C — Tự động đăng mạng xã hội (nối 1 lần, sau đó tự chạy)

Web đã có RSS feed tại `https://nambanvillas.vn/feed.xml`. Dùng nó để bài mới
**tự đăng** lên Facebook/Zalo/Telegram mà không phải copy tay:

**Cách làm với Make.com (miễn phí gói cơ bản):**
1. Tạo tài khoản tại https://make.com
2. Tạo "Scenario" mới → module **RSS: Watch RSS feed items**
   → dán `https://nambanvillas.vn/feed.xml`
3. Nối tiếp module **Facebook Pages: Create a Post** (hoặc Telegram, X/Twitter...)
4. Map: tiêu đề bài → nội dung post, link bài → link
5. Bật scenario, đặt chạy mỗi 1–24 giờ

→ Từ giờ mỗi bài/tin mới tự lên trang Facebook, không cần đăng tay.

> Zalo Official Account chưa có API mở cho việc này; với Zalo nên đăng tay
> hoặc dùng nhóm/cộng đồng.

---

## Ghi chú kỹ thuật

- **Khóa IndexNow**: `abdd063f81d049182d79e17f4239ad8f` (file cùng tên ở thư mục gốc — đừng xóa).
- **Đổi tên miền?** Nếu sau này đổi domain, báo cháu cập nhật URL trong:
  `llms.txt`, `robots.txt`, `sitemap.xml`, `feed.xml`, `indexnow.yml`.
- **Thêm bài mới** → đẩy lên main → IndexNow tự báo search engine; chạy
  `node scripts/build-feed.mjs` (hoặc đợi cập nhật tự động thứ Hai) để feed có bài mới.
