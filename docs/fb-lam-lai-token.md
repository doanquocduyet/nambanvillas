# LÀM LẠI TOKEN FACEBOOK CHO VILLAS — thêm quyền comment

> **Vì sao phải làm:** token hiện tại thiếu quyền `pages_manage_engagement`, nên máy đăng
> **không thả được link xuống comment**. Bài vẫn lên Page bình thường, chỉ là không có
> đường về web — mất hết khách bấm vào.
>
> **Không phải làm lại app.** App cũ giữ nguyên. Chỉ cấp thêm 1 quyền rồi lấy token mới.
>
> Toàn bộ chỉ là **copy — dán**. Khoảng 6 phút.

---

## BƯỚC 0 — Lấy App ID và App Secret (giữ tab này mở)

Mở: **https://developers.facebook.com/apps**

Bấm vào app đã tạo trước đây (tên kiểu `namban-poster`) → menu trái **App settings → Basic**.

Trên màn hình có:
- **App ID** — một dãy số. Copy để riêng ra giấy nháp / ghi chú.
- **App Secret** — bấm **Show**, nhập mật khẩu Facebook → hiện một dãy chữ số. Copy để riêng.

Giữ tab này mở, lát cần.

---

## BƯỚC 1 — Cấp thêm quyền comment

Mở: **https://developers.facebook.com/tools/explorer**

1. Góc phải trên, ô **Meta App** → chọn đúng app vừa mở ở bước 0.
2. Ô **User or Page** → chọn **User Token**.
3. Bấm **Add a Permission** (ô quyền bên dưới), tick cho đủ **4 quyền** sau:

| Quyền | Để làm gì |
|---|---|
| `pages_show_list` | thấy danh sách Trang |
| `pages_manage_posts` | đăng bài |
| **`pages_manage_engagement`** | **comment — đây là cái đang thiếu** |
| `pages_read_engagement` | đọc số liệu bài |

4. Bấm nút xanh **Generate Access Token**.
5. Facebook hiện cửa sổ hỏi → chọn đúng **Trang Nam Ban Villas** → **Continue / Tiếp tục**.
   - Màn hỏi "áp dụng cho Doanh nghiệp nào" → chọn ô **"riêng Doanh nghiệp hiện tại"**, đừng chọn "tất cả hiện tại và tương lai" (rộng hơn mức cần).
   - Màn liệt kê quyền → phải thấy đủ 4 dòng trên, **để nguyên bật hết**, bấm **Xong**.
6. Ô **Access Token** hiện một chuỗi dài. **Copy cả chuỗi.**

Chuỗi này gọi là **TOKEN-TẠM**. Nó chết sau ~1 tiếng — chưa dùng được, phải đổi ở bước 2.

---

## BƯỚC 2 — Đổi sang chuỗi dài hạn

Chép nguyên dòng dưới ra ghi chú, thay **3 chỗ IN HOA** bằng của chú, rồi **dán vào thanh địa chỉ trình duyệt** và Enter:

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=TOKEN_TAM
```

- `APP_ID` → dãy số ở bước 0
- `APP_SECRET` → dãy chữ số ở bước 0
- `TOKEN_TAM` → chuỗi copy ở bước 1

Trình duyệt hiện ra dạng:

```
{"access_token":"XXXXXXXXXX","token_type":"bearer","expires_in":5183944}
```

**Copy đoạn `XXXXXXXXXX`** — chỉ phần trong ngoặc kép, **không lấy hai dấu nháy**. Gọi là **TOKEN-DÀI**.

> Đây vẫn là token **người dùng**, sống 60 ngày. Chưa phải cái cuối. Bước 3 mới ra cái vĩnh viễn.

---

## BƯỚC 3 — Lấy token của TRANG (vĩnh viễn)

Thay `TOKEN_DAI` bằng chuỗi vừa copy, dán vào thanh địa chỉ, Enter:

```
https://graph.facebook.com/v21.0/me/accounts?fields=name,access_token&access_token=TOKEN_DAI
```

Kết quả là danh sách Trang. Tìm khối có `"name":"Nam Ban Villas"`, trong khối đó có:

```
"access_token":"YYYYYYYYYY"
```

**Copy đoạn `YYYYYYYYYY`** — không lấy hai dấu nháy.

**Đây là chuỗi cuối cùng.** Token Trang, không hết hạn.

---

## BƯỚC 4 — Dán vào GitHub

Mở: **https://github.com/doanquocduyet/nambanvillas/settings/secrets/actions**

Tìm dòng **`FB_PAGE_TOKEN`** đã có sẵn → bấm biểu tượng **bút chì** bên phải (Update).

- **Value**: xoá hết, dán chuỗi ở bước 3
- Bấm **Update secret**

> Nếu không thấy dòng `FB_PAGE_TOKEN`: bấm **New repository secret**, Name gõ đúng `FB_PAGE_TOKEN`, Value dán chuỗi, **Add secret**.

---

## BƯỚC 5 — Chạy thử và tự kiểm

Mở: **https://github.com/doanquocduyet/nambanvillas/actions/workflows/fb-auto-post.yml**

Bấm **Run workflow** → **Run workflow** (nút xanh). Chờ ~1 phút, bấm vào lần chạy vừa hiện → mở mục log.

**Nhìn đúng dòng đầu tiên.** Đúng thì nó ghi:

```
Token: loại PAGE · KHÔNG HẾT HẠN
```

| Log ghi gì | Nghĩa là |
|---|---|
| `loại PAGE · KHÔNG HẾT HẠN` | **Xong. Đúng hết.** |
| `loại USER` | lấy nhầm ở bước 2, chưa làm bước 3 → quay lại bước 3 |
| `HẾT HẠN sau N ngày` | cũng là lấy nhầm bậc → quay lại bước 3 |
| `THIẾU QUYỀN pages_manage_engagement` | bước 1 chưa tick đủ 4 quyền → làm lại từ bước 1 |

Không cần tự vào Debugger kiểm nữa — script tự in ra mỗi lần chạy.

---

## SAU KHI XONG

Lần chạy kế tiếp, những bài **đã đăng trước đây mà chưa gắn được link** sẽ được máy
**tự thử lại comment** — không mất bài nào. Log in ra:

```
Còn N bài chưa gắn được link — thử lại:
  · đã comment link: https://nambanvillas.vn/...
```

---

## AN TOÀN

- **Đừng chụp màn hình lúc thấy trọn chuỗi token gửi cho ai.** Ai có chuỗi đó là đăng được lên Trang Nam Ban Villas.
- Lỡ lộ: Facebook → **Cài đặt → Ứng dụng và trang web** → gỡ app đó ra → làm lại từ bước 1. Token cũ chết ngay lập tức.
- Cháu (Claude) **không nhận và không cần** chuỗi token. Chú dán thẳng vào GitHub ở bước 4, cháu không đọc được nó.
