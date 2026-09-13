# PHIẾU ĐĂNG TIN CHO THUÊ NAM BAN
## Dành cho ô đăng tin — đăng tin THUÊ khác tin BÁN ở đâu, và làm thế nào để lên top nhanh nhất

> Đọc file này **trước khi đăng tin cho thuê đầu tiên**. Quy trình ảnh, checker, chống mồ côi vẫn y như `MO-O-DANG-TIN.md` — file này chỉ nói **những chỗ tin thuê KHÁC tin bán**. Chỗ nào không nhắc tới thì làm y hệt tin bán.

---

## 0 · ĐIỀU PHẢI BIẾT TRƯỚC: WEB ĐÃ CÓ HUB CHO THUÊ

**`/cho-thue/` đã tồn tại và đã lên production.** Đây là trang cha của toàn bộ mảng thuê. Mọi tin cho thuê phải nối về đây.

Hub đang có 7 mục, mỗi mục là một ý định tìm kiếm khác nhau — nhớ đúng cái neo này vì tin mới phải cắm vào đúng mục:

| Neo | Ý định khách | Tin thuê loại nào cắm vào đây |
|---|---|---|
| `#o-dai-han` | thuê để ở dài hạn | nhà ở, nhà vườn |
| `#nguyen-can` | thuê nhà nguyên căn | nhà riêng một căn, nhà mới xây |
| `#phong-tro` | thuê phòng | phòng trọ, nhà trọ |
| `#nghi-ngan` | nghỉ vài ngày | homestay, farmstay, villa theo đêm |
| `#kinh-doanh` | mở quán, kho | mặt bằng, kho, cơ sở lưu trú |
| `#o-thu` | ở thử trước khi mua đất | nhà thuê ngắn hạn ở khu đang có đất bán |
| `#gui-tai-san` | chủ nhà muốn cho thuê | (ô nhận nguồn hàng, có form chọn chip) |

Hub cũng đang có **3 thẻ tài sản thật làm mốc giá** (5 · 12 · 13 triệu/tháng), cả ba **đang có khách thuê**. Đừng xoá, đừng đổi trạng thái, đừng biến thành hàng đang trống.

**Bản đồ keyword + luật tách URL:** `docs/package/CHO-THUE-BAN-DO-KEYWORD.md`. Đọc kèm.

---

## 1 · LUẬT SỐ MỘT: KHÔNG MỞ URL NHÁNH TRƯỚC KHI CÓ 3 TIN THẬT

Đây là luật cứng, đã viết trong bản đồ keyword, nhắc lại vì đây là lỗi dễ mắc nhất:

> **Một nhánh chỉ được cắt URL riêng khi có TỪ 3 TIN THẬT TRỞ LÊN.**

- Có 1 villa cho thuê → **không** mở `/cho-thue/villa-nam-ban/`. Đăng trang tin riêng cho villa đó, rồi chèn card vào mục `#nghi-ngan` của hub. Hết.
- Có 3 villa cho thuê → **lúc này** mới mở `/cho-thue/villa-nam-ban/`, gom 3 card vào đó, mục `#nghi-ngan` trong hub rút thành đoạn tóm tắt + link sang.

Vì sao: trang nhánh rỗng bị Google xếp là thin content, và khách vào thấy trống thì không gọi. Web đã dính đúng lỗi này một lần với chip "Nam Hà" hiện 0 sản phẩm.

Cấu trúc URL khi tách (đã khoá, đừng đặt kiểu khác):

```
/cho-thue/                          hub — đã có
/cho-thue/nha-nam-ban/              khi đủ 3 nhà nguyên căn
/cho-thue/phong-tro-nam-ban/        khi đủ 3 phòng trọ
/cho-thue/homestay-nam-ban/         khi đủ 3 homestay
/cho-thue/biet-thu-nam-ban/         khi đủ 3 villa
/cho-thue/mat-bang-nam-ban/         khi đủ 3 mặt bằng
/cho-thue/<slug-tai-san>/           trang từng tài sản — làm NGAY từ tin đầu tiên
```

**Trang từng tài sản thì làm ngay từ tin thứ nhất**, không chờ đủ 3. Chính trang tài sản mới bắt được long-tail kiểu "biệt thự mới xây Nam Ban cho thuê" — không cần bài blog 2.000 chữ nào cả.

---

## 2 · BỐN TRẠNG THÁI — KHÔNG BAO GIỜ XOÁ TRANG, KHÔNG BAO GIỜ 404

Tin thuê quay vòng nhanh hơn tin bán rất nhiều. Đây là khác biệt lớn nhất so với đăng tin bán.

| Trạng thái | Nhãn trên trang | CTA | Schema `availability` |
|---|---|---|---|
| **CÒN TRỐNG** | "Còn trống" | Gọi/Zalo nổi bật | `InStock` |
| **ĐANG GIỮ CHỖ** | "Đang giữ chỗ" | "vào danh sách chờ" | `LimitedAvailability` |
| **ĐÃ THUÊ** | "Đang có khách thuê" | "tìm căn tương tự" + 3 link cùng nhánh | `SoldOut` |
| **NGỪNG CHO THUÊ** | "Ngừng cho thuê" | đẩy sang nhánh cùng loại | `Discontinued` |

**Luật:** không xoá trang, không 404, không redirect hàng loạt. Trang đã thuê vẫn là tài sản SEO — nó giữ điểm, giữ lịch sử giá, và chuyển khách sang căn tương tự. Xoá đi là đốt sạch.

Mỗi lần đổi trạng thái: sửa nhãn + `availability` + **`dateModified`** + `lastmod` trong sitemap. Ba chỗ, đủ cả ba.

---

## 3 · SCHEMA TIN THUÊ — KHÁC TIN BÁN Ở CHỖ NÀO

Tin bán dùng `Product` + `Offer` giá một cục. Tin thuê **không** được làm vậy: giá thuê là giá **theo tháng hoặc theo đêm**, khai sai thì Google hiểu thành giá bán.

Khối bắt buộc cho một trang tài sản cho thuê, gộp trong một `@graph`:

```json
{"@type":"SingleFamilyResidence",
 "@id":"https://nambanvillas.vn/cho-thue/<slug>/#tai-san",
 "name":"...", "url":"...", "image":["... đủ TẤT CẢ ảnh, trỏ .webp ..."],
 "numberOfRooms":3, "numberOfBathroomsTotal":2,
 "floorSize":{"@type":"QuantitativeValue","value":169,"unitCode":"MTK"},
 "address":{"@type":"PostalAddress","addressLocality":"Nam Ban",
            "addressRegion":"Lâm Hà, Lâm Đồng","addressCountry":"VN"},
 "amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Sân vườn","value":true}]}
```

Và khối giá thuê:

```json
{"@type":"Offer",
 "@id":"https://nambanvillas.vn/cho-thue/<slug>/#offer",
 "itemOffered":{"@id":"...#tai-san"},
 "businessFunction":"https://purl.org/goodrelations/v1#LeaseOut",
 "availability":"https://schema.org/InStock",
 "priceSpecification":{"@type":"UnitPriceSpecification",
   "price":5000000, "priceCurrency":"VND",
   "unitCode":"MON", "referenceQuantity":{"@type":"QuantitativeValue","value":1,"unitCode":"MON"}},
 "seller":{"@id":"https://nambanvillas.vn/#organization"}}
```

- `businessFunction: LeaseOut` — **đây là thứ phân biệt cho thuê với bán.** Thiếu nó là tin thuê bị đọc thành tin bán.
- `unitCode` — `MON` cho giá theo tháng, `DAY` cho giá theo đêm.
- Homestay/farmstay có bán phòng theo đêm thì dùng `@type: LodgingBusiness` thay cho `SingleFamilyResidence`, và thêm `checkinTime`/`checkoutTime` nếu biết thật.
- Mặt bằng kinh doanh: dùng `@type: Place` + `Offer` như trên.
- **Vẫn phải có:** `BreadcrumbList` · `WebPage` (có `geo`) · `FAQPage` ≥3 câu. Y như tin bán.
- Tất cả gộp một `@graph`, nối `@id` về `https://nambanvillas.vn/#organization`. Chạy `scripts/gop-schema-graph.py` nếu lỡ viết rời.

---

## 4 · ẢNH TIN THUÊ — MỘT LUẬT RIÊNG RẤT QUAN TRỌNG

Quy trình ảnh y hệt tin bán: `prep-anh.py` → `tao-webp.py` → `sitemap-anh.py` → `kiem-tra-truoc-khi-dang.py`. Nhưng tin thuê có thêm ba luật riêng:

1. **Nhà đang có người ở — tuyệt đối không lộ vị trí chính xác.** Tin bán lộ vị trí thì chỉ là chuyện đất. Tin thuê lộ vị trí là lộ **chỗ ở của một gia đình đang sống trong đó**. Không đăng số nhà, không đăng toạ độ GPS thật, không đăng ảnh thấy rõ biển số xe hay bảng tên đường trước cửa. Mô tả vị trí ở mức "gần hồ Bãi Công", "bám trục ĐT.725", "cách chợ Nam Ban 5 phút".
2. **Không đăng ảnh có người trong đó** — người thuê cũ, trẻ con, đồ đạc cá nhân. Chụp lúc trống hoặc cắt bỏ.
3. **Ảnh phòng ốc thường là ảnh dọc** → chạy `prep-anh.py <slug> ... --ratio keep`, đừng để bị cắt mất trần nhà.

`alt` vẫn phải neo mốc thật kiểm được được (hồ Bãi Công · chùa Linh Ẩn · Thác Voi · ĐT.725) — đó là thứ AI trích khi khách hỏi "thuê nhà gần hồ Bãi Công".

---

## 5 · AEO — TRẢ LỜI TRƯỚC, RỒI MỚI ĐẾN TÀI SẢN

Người tìm thuê hỏi câu rất cụ thể. Mỗi trang tài sản mở đầu bằng **một đoạn trả lời thẳng**, không bắt đọc hết mới biết.

Mẫu mở đầu một trang tài sản:

> **Nhà 2PN full nội thất 169m² gần hồ Bãi Công — 5 triệu/tháng, còn trống từ tháng 10.**
> Nhà trệt có sân trước sân sau, đường bê tông vào tận cửa, nước máy. Chủ cho thuê tối thiểu 6 tháng. Xem nhà gọi 0978 758 788.

Ba thứ trong một đoạn: **giá · trạng thái · điều kiện thuê**. Đó là ba thứ người thuê hỏi đầu tiên, và cũng là ba thứ AI trích.

FAQ mỗi trang tài sản ≥3 câu, **hỏi đúng cái người thuê hỏi**, không phải câu SEO chung chung:
- "Căn này còn trống không?" → trả lời kèm ngày cập nhật.
- "Thuê tối thiểu bao lâu, cọc mấy tháng?"
- "Điện nước tính thế nào?"
- "Có cho nuôi thú cưng / ở ghép không?" (nếu biết thật)

**Luật vàng về số:** phân biệt rõ hai loại số, không được trộn.
- **Số xác minh thật** — của tài sản Villas nắm được, đi xem được. Dùng làm mốc.
- **Số ghi nhận trên tin rao** — thấy trên sàn/nhóm, chưa xác minh. **Phải ghi rõ là chưa xác minh.**

Hub đang ghi: nguyên căn 4–8 triệu/tháng và phòng trọ ~800 nghìn/tháng là loại thứ hai; 5/12/13 triệu là loại thứ nhất. Giữ đúng cách phân biệt đó ở mọi trang mới.

---

## 6 · IA — NỐI TIN MỚI VÀO HỆ THỐNG (5 CHỖ, THIẾU 1 LÀ MỒ CÔI)

Mỗi tin cho thuê mới, làm đủ 5 việc:

1. **Trang tài sản** `/cho-thue/<slug>/` — dựng xong, chạy checker.
2. **Card vào hub** `/cho-thue/` — chèn vào đúng mục theo bảng ở phần 0. Dùng lại đúng class `.ct-ds` / `.ct-item` đang có, đừng đẻ CSS mới.
3. **ItemList của hub** — hiện `@id` là `https://nambanvillas.vn/cho-thue/#itemlist`, `numberOfItems` **phải khớp đúng số card thật**. Checker có bẫy bắt lệch số này.
4. **Sitemap** — thêm URL (có `/` cuối) + chạy `sitemap-anh.py`, và **đổi `lastmod` của `/cho-thue/`** vì hub vừa có hàng mới.
5. **`dateModified` của hub** — mảng thuê ăn nhau ở độ tươi. Hub đứng im 3 tháng là tụt.

Thêm: nếu tài sản nằm ở khu đang có đất bán, đặt **một link hai chiều** giữa trang tài sản và trang khu đất đó — đây là cầu nối sang mục `#o-thu` (thuê ở thử trước khi mua), nhóm giá trị nhất của cả mảng.

---

## 7 · GEO — ENTITY, KHÔNG PHẢI KEYWORD

Mỗi tài sản phải gắn được vào cùng một mạng thực thể của site: **Nam Ban → loại tài sản → khu → giá → diện tích → tiện nghi → trạng thái → ngày cập nhật → Nam Ban Villas.**

Cụ thể trong trang:
- `address.addressLocality` luôn đúng xã/thôn thật (Nam Ban · Đông Thanh · Mê Linh · Gia Lâm · Nam Hà), không ghi chung "Lâm Đồng".
- `WebPage.geo` đặt ở **toạ độ trung tâm xã**, không phải toạ độ căn nhà (xem luật riêng tư ở phần 4).
- Mọi khối schema nối `@id` về `https://nambanvillas.vn/#organization` — để Google hiểu 200 trang này là **một** doanh nghiệp, không phải 200 mẩu rời.
- Mô tả neo mốc có thật, kiểm được: hồ Bãi Công, chùa Linh Ẩn, Thác Voi, chợ Nam Ban, ĐT.725, 35–40 phút xuống Đà Lạt, Liên Khương 22km, mùa mưa tháng 5–11. **Dùng đúng các số này, đừng tự đổi** — cả site đang thống nhất.

---

## 8 · RANH GIỚI — ĐỪNG LẤN

- **Villas làm:** môi giới cho thuê — tìm khách, dẫn xem, chốt hợp đồng, nhận ký gửi.
- **GreenSpacers làm:** trông coi & quản lý tài sản thu phí hàng tháng. Chủ ở xa thì trỏ sang `greenspacers.vn`.
- **Panorama:** Villas **TUYỆT ĐỐI không đặt thẻ `<a>` trỏ sang** (canonical thì được). Xem `docs/HIEN-PHAP-3-WEB.md`.
- **Không bịa bất cứ gì:** không bịa tin thuê, không bịa giá, không bịa đánh giá, không copy chữ của sàn khác, không hotlink ảnh web khác. Chưa có hàng thì ghi là chưa có — đó chính là thứ làm khách tin và gọi.

---

## 9 · CHECKLIST 10 DÒNG CHO MỘT TIN THUÊ

1. Ảnh: `prep-anh.py` (ảnh dọc thêm `--ratio keep`) → `tao-webp.py` → `sitemap-anh.py`
2. Ảnh không lộ số nhà, GPS, biển số, người ở trong
3. Thẻ `<img>` trỏ `.webp`, đủ `alt`/`width`/`height`; hero `fetchpriority="high"` và **không** lazy; còn lại lazy
4. Đoạn mở đầu trả lời thẳng: **giá · trạng thái · điều kiện thuê**
5. Schema: `SingleFamilyResidence`/`LodgingBusiness` + `Offer` có **`businessFunction: LeaseOut`** + `UnitPriceSpecification` đúng `unitCode` (`MON`/`DAY`) + `BreadcrumbList` + `WebPage(geo)` + `FAQPage` ≥3 câu, gộp `@graph`
6. Nhãn trạng thái đúng 1 trong 4, khớp với `availability`
7. Chèn card vào đúng mục của `/cho-thue/`; cập nhật `ItemList.numberOfItems`
8. Sitemap: thêm URL + đổi `lastmod` của `/cho-thue/`; đổi `dateModified` của hub
9. Chưa đủ 3 tin cùng nhánh thì **không** mở URL nhánh
10. `python3 scripts/kiem-tra-truoc-khi-dang.py` = 0 lỗi rồi mới push
