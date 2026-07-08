# HƯỚNG DẪN ĐĂNG "CỤM MỚI" — cho box Claude Code đăng tin

> Mục tiêu: mỗi khi có 1 CỤM đất mới (nhiều nền phân lô cùng khu), đăng ĐÚNG 3 nơi
> để nó tự hiện lên trang Cụm Mới và dẫn khách về Gọi/Zalo 0978 758 788.
> KHÔNG bịa số liệu. Chỉ đăng cụm THẬT (tên khu, số nền, diện tích, giá thật).

Phân biệt: **CỤM** = nhiều nền cùng 1 khu vừa phân lô (đăng theo hướng dẫn này).
**LÔ LẺ** = 1 lô đơn → đăng vào `/dat-nen/` như bình thường, KHÔNG đụng trang Cụm Mới.

---

## 3 VIỆC PHẢI LÀM KHI CÓ CỤM MỚI

### 1) Tạo trang chi tiết cụm
Đường dẫn: `dat-nen/cum-<slug>/index.html`
(ví dụ đã có: `dat-nen/cum-tu-liem-13-nen/`)
Làm theo đúng mẫu trang cụm đã có (bảng các nền, giá từng nền, ảnh, CTA Gọi/Zalo,
breadcrumb, canonical, schema). Copy 1 trang cụm cũ rồi sửa số liệu.

### 2) Nén ảnh cụm TRƯỚC khi commit
```
python3 scripts/nen-anh.py images/listings/cum-<slug>/
```
Ảnh điện thoại 3–5MB không được đưa thẳng lên.

### 3) Gắn card vào trang Cụm Mới — `cum-moi-nam-ban/index.html`
Đây là NƠI ĐĂNG chính để khách thấy cụm. Tìm dòng:

```html
    <p style="...">Cụm đang mở</p>
```

Chèn card mới NGAY DƯỚI dòng đó (cụm mới nhất nằm trên cùng).
Dùng đúng mẫu này, chỉ thay phần in HOA:

```html
    <a href="/dat-nen/cum-SLUG/" style="display:flex;gap:20px;background:#fff;border:1px solid #E3E0D8;border-radius:18px;overflow:hidden;text-decoration:none;box-shadow:0 8px 26px -14px rgba(26,61,43,.25);transition:.18s;margin-bottom:14px" class="cm-cluster">
      <img src="/images/listings/cum-SLUG/1.jpg" alt="ALT-TẢ-CỤM" width="300" height="220" loading="lazy" style="width:44%;max-width:300px;object-fit:cover;display:block;flex:0 0 auto">
      <div style="padding:20px 22px 20px 0;min-width:0">
        <span style="display:inline-block;background:#EEF3EC;color:#1A3D2B;font-size:.72rem;font-weight:700;padding:3px 11px;border-radius:20px;margin-bottom:9px">SỐ nền · vừa mở</span>
        <h3 style="font-size:1.14rem;font-weight:800;color:#1A3D2B;line-height:1.35;margin:0 0 8px">TÊN CỤM NGẮN GỌN</h3>
        <p style="font-size:.9rem;color:#5a6660;line-height:1.55;margin:0 0 12px">DIỆN-TÍCH/nền · thổ cư · đường · vị trí</p>
        <span style="font-weight:800;color:#1A3D2B;font-size:1.1rem">Từ GIÁ/nền</span>
        <span style="display:block;margin-top:10px;color:#C9A84C;font-weight:800;font-size:.9rem">Xem cả cụm →</span>
      </div>
    </a>
```

### 4) Thêm URL cụm vào `sitemap.xml`
Chèn 1 dòng (đặt cạnh các URL /dat-nen/):
```xml
  <url><loc>https://nambanvillas.vn/dat-nen/cum-SLUG/</loc><lastmod>NGÀY</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
```

---

## LUẬT GIỮ TRANG SẠCH

- **Tối đa 4 card** trong "Cụm đang mở". Có cụm thứ 5 → xoá card cụm CŨ NHẤT (hoặc cụm đã bán hết).
- **Cụm bán hết → gỡ card** khỏi trang Cụm Mới (trang chi tiết có thể giữ hoặc ghi "đã bán").
- **KHÔNG** đưa lô lẻ vào trang Cụm Mới — chỉ card cụm.
- Số liệu (số nền, m², giá) phải THẬT, khớp với trang chi tiết cụm.
- Kỹ thuật: dùng `str_replace` khớp chính xác, KHÔNG regex DOTALL (luật CLAUDE.md).
- Sau khi sửa: verify HTML cân thẻ, push → tạo PR → merge main (deploy).

---

## TÓM TẮT 1 DÒNG
Có cụm mới → (1) trang `/dat-nen/cum-<slug>/` + (2) nén ảnh + (3) chèn card vào
`cum-moi-nam-ban/index.html` dưới chữ "Cụm đang mở" + (4) thêm vào sitemap. Tối đa 4 card.
