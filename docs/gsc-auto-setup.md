# Bật báo cáo index Google Search Console tự động — Nam Ban Villas

> Làm **1 lần, ~5 phút**. Xong là mỗi thứ Hai hằng tuần web tự đọc Google Search
> Console và ghi báo cáo vào `docs/gsc-status.md` (trang nào đã index, trang nào chưa).
>
> **Vì sao chú phải làm tay phần này:** Google BẮT BUỘC chủ web tự cấp 1 "chìa khoá"
> để cho phép đọc dữ liệu Search Console. Đây là bảo mật của Google — không app/AI nào
> vượt được. Cháu đã dựng sẵn toàn bộ máy (script + lịch chạy), chỉ chờ chìa khoá này.

---

## A. Tạo "chìa khoá" trên Google Cloud (miễn phí)

1. Mở https://console.cloud.google.com/ → góc trên chọn hoặc tạo **1 project bất kỳ**.
2. Bật API: mở https://console.cloud.google.com/apis/library/searchconsole.googleapis.com → bấm **Enable**.
3. Mở https://console.cloud.google.com/iam-admin/serviceaccounts → **Create service account**
   → tên `gsc-reader` → **Create** → **Done** (bỏ qua phần role).
4. Bấm vào `gsc-reader` vừa tạo → tab **Keys** → **Add key** → **Create new key** → chọn **JSON**
   → **Create**. Máy tự tải 1 file `.json` — **giữ file này**.
5. **Copy email** của service account (dạng `gsc-reader@...iam.gserviceaccount.com`).

## B. Cho chìa khoá đó đọc Search Console

6. Mở https://search.google.com/search-console → chọn **nambanvillas.vn** → **Cài đặt (Settings)**
   → **Người dùng và quyền** → **Thêm người dùng** → dán email ở bước 5 → quyền **Toàn quyền (Full)** → **Thêm**.

## C. Dán chìa khoá vào GitHub

7. Mở https://github.com/doanquocduyet/nambanvillas/settings/secrets/actions
   → **New repository secret** → **Name** gõ đúng `GSC_SA_JSON`
   → **Value**: mở file `.json` ở bước 4, **copy toàn bộ**, dán vào → **Add secret**.

---

## Chạy thử lần đầu

Mở https://github.com/doanquocduyet/nambanvillas/actions → chọn workflow
**"Báo cáo index Google Search Console"** → **Run workflow**. Chờ ~1 phút, mở
`docs/gsc-status.md` xem kết quả. Từ đó nó tự chạy mỗi thứ Hai.

## Nếu property là kiểu "Miền" (Domain), không phải "URL-prefix"

Mặc định script dùng property dạng URL `https://nambanvillas.vn/`. Nếu trong GSC
property của chú là kiểu **Miền** (biểu tượng địa cầu, tên chỉ `nambanvillas.vn`),
thì thêm 1 biến:

- Mở https://github.com/doanquocduyet/nambanvillas/settings/variables/actions
  → **New repository variable** → Name `GSC_SITE_URL` → Value `sc-domain:nambanvillas.vn` → Add.

## Nói thẳng (đừng kỳ vọng sai)

- 7 bước trên là **mức tối thiểu Google bắt buộc** — đã rút gọn hết cỡ.
- Cháu **chưa test được đầu–cuối** (môi trường của cháu chặn Google + cháu không giữ
  chìa khoá của chú). Lần chạy thật đầu tiên nếu báo lỗi, chú **copy dòng lỗi trong tab
  Actions gửi cháu**, cháu sửa ngay.
