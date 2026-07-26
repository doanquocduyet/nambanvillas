# PHIẾU BÀN GIAO → Ô CODE ĐĂNG
## Content vừa xong: bài trụ + 4 bài cẩm nang khu (đợt 26/7/2026)

> Ô content đã VIẾT xong, verify xong. Ô code đăng chỉ cần ĐĂNG (merge + deploy) theo phiếu này.

---

### 1. BÀI TRỤ — đã live trên main (chỉ cần thêm back-link)
- URL: `https://nambanvillas.vn/thi-truong/dat-phan-lo-nam-ban/` (đã index, đã trong sitemap).
- **Việc:** thêm 1 link TỪ hub `/cum-moi-nam-ban/index.html` TRỎ LÊN bài trụ, đặt trong khối liên quan/thị trường, anchor có keyword:
  `<a href="/thi-truong/dat-phan-lo-nam-ban/">Cẩm nang mua đất phân lô Nam Ban 2026 — bảng giá theo khu</a>`
  → bơm lực 2 chiều hub ↔ bài trụ.

### 2. 4 BÀI CẨM NANG KHU — nằm trên branch, CẦN MERGE VÀO MAIN
Branch: **`claude/noi-dung-cam-nang-khu`** (đã push, off `main`).
Gồm 4 file + sitemap đã cập nhật (đã thêm 4 URL, priority 0.8):
- `thi-truong/dat-nen-dong-thanh-nam-ban/` → link xuống cụm `dat-nen/cum-dong-thanh-15-nen/`
- `thi-truong/dat-nen-me-linh-nam-ban/` → link xuống cụm `dat-nen/cum-me-linh-14-nen/`
- `thi-truong/dat-nen-tu-liem-nam-ban/` → link xuống cụm `dat-nen/cum-tu-liem-13-nen/`
- `thi-truong/dat-nen-tam-xa-nam-ban/` → link xuống cụm `dat-nen/cum-tam-xa-5-nen/`

**Việc:** squash merge branch `claude/noi-dung-cam-nang-khu` vào `main` (Vercel auto-deploy).
- Nếu conflict ở `sitemap.xml`: giữ CẢ 4 dòng URL mới (dat-nen-dong-thanh / me-linh / tu-liem / tam-xa) + các dòng của main.
- 4 bài đều index (không noindex), đã có Article + FAQPage + BreadcrumbList + geo VN-LB.

**Tùy chọn (nên làm):** trong mỗi trang cụm `dat-nen/cum-*/`, ở sidebar "Thị Trường Liên Quan" thêm link NGƯỢC lên bài cẩm nang khu tương ứng (vd trang `cum-dong-thanh-15-nen` → link `/thi-truong/dat-nen-dong-thanh-nam-ban/`) để mạng nội bộ 2 chiều.

### 3. ĐÃ VERIFY (ô content làm rồi, ô code khỏi lo)
- 3 JSON-LD/bài hợp lệ · sitemap XML hợp lệ · 0 placeholder · 1 H1/bài · nút Gọi + Zalo đủ · 0 link Panorama · mọi link cụm tồn tại.
- Ranh giới: 4 bài chỉ góc GIAO DỊCH (giá/pháp lý/đang bán), không đụng cụm đời sống/du lịch (Panorama) hay trông coi (Greenspace).

### 4. RANH GIỚI 2 Ô (nhắc lại)
- Ô content KHÔNG tự merge main từ đây; bàn giao qua phiếu này.
- Ô code đăng lo: merge/deploy, sửa hub, sửa trang cụm, ảnh, kỹ thuật.
