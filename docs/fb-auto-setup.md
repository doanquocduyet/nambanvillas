# Bật TỰ ĐỘNG đăng tin lên Facebook Page — Nam Ban Villas

> Làm **1 lần**. Xong là mỗi khi có lô/cụm mới lên web, hệ thống **tự đăng lên Page
> facebook.com/nambanvillas** — chú không phải đụng tay. Hợp lệ 100% (API chính thức
> của Facebook), **không đụng nick cá nhân, không đụng group**, không sợ khoá nick.
>
> **Vì sao chú phải làm phần này:** Facebook BẮT BUỘC chủ Page tự tạo 1 "chìa khoá"
> (token) mới cho phép đăng. Đây là bảo mật của Facebook — không app/AI nào vượt được.
> Cháu đã dựng sẵn toàn bộ máy, chỉ chờ chìa khoá này. Mất ~15 phút, chỉ **copy–paste**.
>
> Toàn bộ bên dưới chỉ cần: **dán link vào trình duyệt → copy đoạn chữ kết quả**.
> Không cần mở terminal, không cần gõ lệnh.

---

## PHẦN A — Tạo "ứng dụng" để lấy chìa khoá (5 phút)

1. Mở https://developers.facebook.com/apps → bấm **Create App** (Tạo ứng dụng).
   - Nếu lần đầu, Facebook bắt xác nhận tài khoản nhà phát triển → bấm đồng ý, xong.
2. Ở "Use cases" chọn **Other** → **Next** → loại app chọn **Business** → **Next**.
3. Đặt tên app bất kỳ (ví dụ `namban-poster`) → **Create app** (nhập lại mật khẩu FB nếu hỏi).
4. Vào app vừa tạo → menu trái **App settings → Basic**. Chú sẽ thấy:
   - **App ID** (dãy số) — lát dùng.
   - **App Secret** — bấm **Show**, nhập mật khẩu FB → hiện ra một dãy — lát dùng.
   Giữ tab này mở.

## PHẦN B — Lấy chìa khoá tạm (short-lived) trong Graph Explorer (3 phút)

5. Mở https://developers.facebook.com/tools/explorer
6. Góc phải trên, ô **Meta App**: chọn đúng app `namban-poster` vừa tạo.
7. Bấm nút **Add a Permission / Permissions** (Quyền), tick 2 quyền này:
   - `pages_manage_posts`
   - `pages_read_engagement`
8. Bấm **Generate Access Token** (Tạo token) → cửa sổ FB hiện lên → chọn **đúng Page
   Nam Ban Villas** khi được hỏi → **Continue / Đồng ý** hết.
9. Ô **Access Token** giờ có một đoạn chữ dài → **copy toàn bộ đoạn này** (gọi là **TOKEN-TẠM**).

## PHẦN C — Đổi sang chìa khoá dài hạn (dán 1 link, 1 phút)

10. Ghép link dưới đây, thay 3 chỗ IN HOA bằng của chú, rồi **dán vào thanh địa chỉ trình duyệt** và Enter:

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=TOKEN_TAM
```

- `APP_ID` = App ID ở bước 4
- `APP_SECRET` = App Secret ở bước 4
- `TOKEN_TAM` = đoạn copy ở bước 9

11. Trình duyệt hiện ra một đoạn JSON dạng `{"access_token":"XXXXX","token_type":...}`.
    **Copy đoạn `XXXXX`** (phần trong ngoặc kép sau `access_token`) — gọi là **TOKEN-DÀI**.

## PHẦN D — Lấy đúng chìa khoá của PAGE (vĩnh viễn) (1 phút)

12. Ghép link dưới, thay `TOKEN_DAI` bằng đoạn vừa copy, dán vào trình duyệt, Enter:

```
https://graph.facebook.com/v21.0/me/accounts?access_token=TOKEN_DAI
```

13. Trình duyệt hiện danh sách Page của chú. Tìm khối có `"name":"Nam Ban Villas"`,
    trong đó có `"access_token":"YYYYY"`. **Copy đoạn `YYYYY`** — đây là
    **CHÌA KHOÁ PAGE** (không hết hạn). Xong phần khó nhất.

## PHẦN E — Dán chìa khoá vào GitHub (1 phút)

14. Mở https://github.com/doanquocduyet/nambanvillas/settings/secrets/actions
    → **New repository secret**
    - **Name**: gõ đúng `FB_PAGE_TOKEN`
    - **Value**: dán **CHÌA KHOÁ PAGE** (đoạn `YYYYY` ở bước 13)
    - **Add secret**

---

## Chạy thử

Mở https://github.com/doanquocduyet/nambanvillas/actions → chọn
**"Tự đăng tin mới lên Facebook Page"** → **Run workflow**.

- Lần này sẽ **không đăng gì** nếu chưa có tin mới (mọi tin cũ đã được "seed").
- Từ giờ, **mỗi lô/cụm mới cháu đưa lên web là tự động đăng lên Page** trong vài phút.
- Mỗi lần chạy đăng tối đa 3 tin (đăng đều, không dồn spam).

## Nói thẳng

- Phần này **dài hơn Google** vì Facebook bắt tạo app riêng — nhưng làm 1 lần là xong mãi.
- Chìa khoá Page lấy theo cách trên **không hết hạn** (vì đổi qua token dài hạn ở phần C).
  Nếu lỡ đổi mật khẩu FB hoặc gỡ quyền app, token có thể hỏng → chỉ cần làm lại phần B–E.
- Nếu lần chạy đầu báo lỗi, chú **copy dòng lỗi trong tab Actions gửi cháu**, cháu sửa ngay.
- **Group**: Facebook cấm bot đăng group (đăng là khoá nick) → phần group cháu KHÔNG auto.
  Chỉ **Page** mới được tự đăng hợp lệ.
