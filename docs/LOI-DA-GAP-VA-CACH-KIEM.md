# SỔ LỖI — TẤT CẢ LỖI TÌM ĐƯỢC SAU ĐỢT TỔNG RÀ, VÀ CÁCH TỰ KIỂM

> **Tờ này để làm gì:** đưa nguyên văn cho người/trợ lý đang lo một web khác, bảo họ
> **rà đúng từng mục** xem web đó có dính lỗi tương tự không. Mỗi mục có: triệu chứng thật ·
> vì sao nguy · **lệnh tự kiểm** · cách sửa · cách chặn tái phát.
>
> **Phạm vi:** mọi lỗi phát hiện từ sau đợt tổng rà toàn site tới 23/9/2026
> (PR #494 → #509 của nambanvillas.vn, web tĩnh HTML/CSS/JS thuần, 219 trang).
>
> **Đọc theo thứ tự nào:** phần A là bảng tra nhanh. Phần B chi tiết từng lỗi.
> Phần C là những thứ **đã đúng sẵn** — vẫn nên kiểm vì web khác có thể sai.
> Phần D là 6 bài học gốc — **quan trọng nhất**, vì lỗi cụ thể thì mỗi web mỗi khác,
> còn nguyên nhân gốc thì giống nhau.

---

## A. BẢNG TRA NHANH — 28 LỖI THẬT

Cột "Nặng" theo mức hại: 🔴 mất tiền/mất niềm tin · 🟠 mất thứ hạng/traffic · 🟡 khó dùng.

| # | Lỗi | Nặng | Quy mô khi phát hiện |
|---|---|---|---|
| 1 | Trang tự nhường index cho web khác (canonical sai) | 🔴 | 8 trang, 838 link vào |
| 2 | Schema FAQ có nhưng chữ **không hiện trên trang** | 🔴 | 174 trang |
| 3 | Bịa số liệu ("Khảo sát của chúng tôi cho thấy 45%…") | 🔴 | 1 bài |
| 4 | Bài nói sai sự thật đã kiểm chứng được | 🔴 | 4 bài |
| 5 | Web tự chọi web (cùng 1 số, 3 kiểu khác nhau) | 🔴 | 13 trang |
| 6 | Thẻ lọc trỏ sai bài (tiêu đề một đằng, link một nẻo) | 🔴 | 1 thẻ |
| 7 | Lô **đã bán** nằm dưới tiêu đề "đang bán" | 🔴 | 4 lô / 3 trang |
| 8 | Trang khu hứa "tất cả lô" nhưng chỉ hiện 1 phần | 🔴 | 6 trang, 39/159 lô |
| 9 | Ảnh gãy trên tin đang bán (.webp vs .jpg) | 🔴 | 1 tin |
| 10 | Giá trên thẻ ≠ giá trên trang chi tiết | 🟠 | 1 tin |
| 11 | Lô có giá thật nhưng `data-price="0"` → lọc không bao giờ ra | 🟠 | 1 tin |
| 12 | **CSS chỉ nằm nhúng trong 3 trang** → 12 trang khác vỡ hẳn | 🔴 | ~250 thẻ |
| 13 | **Cache CSS 24h + tên file không đổi** → sửa xong khách không thấy | 🔴 | toàn site |
| 14 | Nút hiện ra nhưng JS chặn theo đường dẫn → bấm không ăn gì | 🔴 | 142 nút / 6 trang |
| 15 | Nút Menu thanh đáy `display:none` + id chết | 🟠 | 8 trang |
| 16 | Từ hành chính hết hiệu lực (huyện/thị trấn đã bỏ) | 🟠 | 280 chỗ |
| 17 | Câu hỏi để thì tương lai cho việc đã xảy ra 14 tháng | 🟠 | 1 trang (trang Hỏi Đáp) |
| 18 | Bậc tiêu đề nhảy cóc h2→h4 | 🟠 | 208/219 trang |
| 19 | Bài trong hub **không được chính hub liệt kê** | 🟠 | 5 bài |
| 20 | Hub thiếu hẳn CollectionPage + ItemList | 🟠 | 3 hub |
| 21 | Tin đăng thiếu node WebSite/SearchAction | 🟡 | 16 tin |
| 22 | ItemList khai nhiều hơn số thẻ thật trên trang | 🟠 | 1 trang |
| 23 | Lọc xong **không ghi vào URL** → không chia sẻ được | 🟡 | 1 hub |
| 24 | Chip bật/tắt thiếu `aria-pressed` | 🟡 | 23 chip |
| 25 | Ô chọn/ô tìm thiếu nhãn | 🟡 | 2 ô |
| 26 | Thẻ nhà thiếu `data-area`/`data-price` → không lọc được | 🟠 | 33 thẻ |
| 27 | Trang khu là **ngõ cụt** — không có đường sang khu khác | 🟡 | 3 trang |
| 28 | 6 bài cùng chủ đề **không bài nào trỏ sang bài nào** | 🟠 | 6 bài |

**Thêm 3 lỗi tự gây trong lúc sửa** (ghi lại vì rất dễ lặp):

| # | Lỗi tự gây | Hậu quả |
|---|---|---|
| T1 | Sửa JSON bằng regex `\](?=\})` | Cắt cụt JSON-LD của 6 trang |
| T2 | Xoá khối HTML bằng `[\s\S]*?` | 3 lô khu khác lọt sang trang mới |
| T3 | Chèn chú thích không xét ngoặc đang mở | `)` lồng nhau ở 6 trang, lặp từ 37 chỗ |

---

## B. CHI TIẾT TỪNG LỖI

### 🔴 1. Trang tự nhường index cho web khác

**Triệu chứng.** 8 trang khai `<link rel="canonical">` trỏ sang một web khác của cùng chủ.
Trong đó có **2 trang hub**, mỗi hub có 217 link nội bộ trỏ vào. Tổng 838 link nội bộ
đổ vào những trang đang tự nói "đừng index tôi, index trang kia đi".

**Vì sao nguy.** Canonical ngoài chỉ đúng khi **hai trang cùng ý định và trùng nội dung thật**.
Một hub không bao giờ là bản sao của trang khác. Trỏ canonical sang **trang chủ** của web kia
thì chắc chắn sai — trang chủ không cùng ý định với một bài cụ thể.

**Tự kiểm.**
```bash
grep -rho '<link rel="canonical" href="[^"]*"' --include=index.html . \
  | sort | uniq -c | sort -rn | head -20
```
Nhìn: có URL nào **không thuộc tên miền của chính web** không? Có URL nào **lặp nhiều lần**
(nhiều trang cùng trỏ 1 đích) không?

**Sửa.** Trả về tự trỏ chính nó. Chỉ giữ canonical ngoài khi thật sự là bản trùng cùng ý định.

**Chặn tái phát.** Luật: trang hub **không bao giờ** được canonical ra ngoài; canonical ngoài
trỏ vào `/` hay `/index` là sai tự động.

---

### 🔴 2. Schema FAQ có nhưng chữ không hiện trên trang

**Triệu chứng.** **174/194 trang** có `FAQPage` trong JSON-LD với đầy đủ câu hỏi/đáp án,
nhưng trên trang **không có một chữ nào** của những câu đó.

**Vì sao nguy.** Google yêu cầu nội dung trong structured data **phải có mặt cho người dùng thấy**.
Khai thứ không hiện = rủi ro bị phạt thủ công, mất toàn bộ kết quả nổi bật.

**Tự kiểm.** Với mỗi trang: lấy mọi `Question.name` trong JSON-LD, kiểm xem chuỗi đó có
xuất hiện trong phần chữ hiển thị không.
```bash
python3 - <<'EOF'
import re,glob,json
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    chu=re.sub(r'<[^>]+>',' ',re.sub(r'<script[\s\S]*?</script>','',s))
    for b in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',s):
        def di(n):
            if isinstance(n,dict):
                if n.get('@type')=='FAQPage':
                    an=[q['name'] for q in n.get('mainEntity',[]) if q['name'][:40] not in chu]
                    if an: print(f,'-> %d câu KHÔNG hiện'%len(an), an[0][:50])
                [di(v) for v in n.values()]
            elif isinstance(n,list): [di(v) for v in n]
        try: di(json.loads(b))
        except: pass
EOF
```

**Sửa.** In câu hỏi/đáp án ra trang bằng `<details><summary>`. **Và mở sẵn** (xem lỗi #29 dưới).

---

### 🔴 3. Bịa số liệu

**Triệu chứng.** Một bài viết: *"**Khảo sát của [tên công ty]** cho thấy: 45% nhà đầu tư dài hạn ·
30% second home · 15% nông nghiệp · 10% định cư"*. **Không hề có khảo sát nào.**

**Vì sao nguy.** Số bịa sẽ chui vào FAQ, vào schema, rồi được AI trích dẫn như số chính thức.
Một lần bị bắt là mất niềm tin cả web. Đây là loại lỗi **không có đường lùi**.

**Tự kiểm.** Quét mọi cụm phần trăm / "X lần" đi kèm cách dẫn nguồn mơ hồ:
```bash
grep -rn "Khảo sát của\|Theo số liệu\|Theo thống kê\|Các chuyên gia cho rằng\|Nhiều người cho rằng" \
  --include=*.html . | head -30
grep -rno "[0-9]\{1,3\}\s*[–-]\s*[0-9]\{1,3\}\s*%" --include=*.html . | head -40
```
Với **mỗi** kết quả, hỏi: *số này lấy ở đâu, có tên văn bản/cơ quan/ngày không?*
Không trả lời được → **gỡ**, đừng làm mềm câu chữ.

**Sửa.** Thay bằng quan sát thực tế **và nói rõ đó là quan sát**, hoặc bỏ hẳn con số.
Ví dụ đã dùng: bỏ phần trăm, đánh số thứ tự 01–04, thêm câu
*"đây là quan sát thực tế, không phải số liệu thống kê"*.

---

### 🔴 4. Bài nói sai sự thật kiểm chứng được

**4 bài** cùng loại lỗi. Nặng nhất:

- Bài *"Tuyến tránh khi nào hoàn thành"* viết **"dự kiến thông xe 2026"**, trong khi **một bài khác
  của chính web** ghi dự án đó *"mới đang ở bước đề xuất"*. Web tự chọi web, ở đúng câu hỏi
  khách hỏi nhiều nhất khi đi xem đất.
- Bài giá đất dẫn *"theo số liệu từ các sàn giao dịch"* với mức **40–60%**, trong khi bài bảng giá
  của chính web ghi **30–50%** kèm số hiệu nghị quyết.
- Bài sân bay dẫn *"Phú Quốc tăng 5–10 lần"* không nguồn, lại so một đảo du lịch quốc tế với
  một xã cao nguyên.
- Bài khí hậu ghi **18–22°C** trong khi bài khác ghi **18–23°C**; *"bệnh viện huyện cách 10 phút"*
  trong khi thực tế bệnh viện huyện cách ~15km.

**Tự kiểm.** Lấy mọi **con số đặc trưng** (nhiệt độ, khoảng cách, công suất, mốc thời gian)
gom theo loại, xem cùng một thứ có bị nói nhiều kiểu không:
```bash
python3 - <<'EOF'
import re,glob
from collections import defaultdict
pat={'Nhiệt độ':r'\d\d\s*[–-]\s*\d\d\s*°C',
     'Công suất':r'\d[\d,.]*\s*triệu (?:lượt )?(?:hành )?khách',
     'Độ cao':r'\d{3,4}\s*m so với mực nước biển'}
for ten,p in pat.items():
    d=defaultdict(list)
    for f in glob.glob('**/*.html',recursive=True):
        t=re.sub(r'<[^>]+>',' ',open(f,encoding='utf-8').read())
        for m in re.finditer(p,t): d[m.group(0).strip()].append(f)
    if len(d)>1:
        print(ten,'— %d cách nói khác nhau:'%len(d))
        for k,v in d.items(): print('   %-16s %d trang'%(k,len(v)))
EOF
```

> **Lưu ý quan trọng — đừng sửa nhầm.** Khoảng cách tới một địa điểm khai **khác nhau giữa các
> tin** là **đúng** (mỗi lô một vị trí), không phải mâu thuẫn. Máy quét báo "86 cách nói khác nhau"
> nhưng soi lại thì hợp lệ. Chỉ thống nhất những thứ là **thuộc tính của cả vùng** (nhiệt độ,
> độ cao, công suất sân bay), không đụng thuộc tính của **từng tin**.

---

### 🔴 6. Thẻ trỏ sai bài

**Triệu chứng.** Một thẻ trên trang hub: tiêu đề, mô tả, nguồn, `alt` ảnh **đều là tin đấu giá
ngày 12/6**, nhưng `href` lại trỏ vào **bài du lịch nông nghiệp**.

**Vì sao nguy.** Khách bấm ra sai bài (mất niềm tin ngay lập tức). Google đọc chữ neo
"đấu giá quyền sử dụng đất" trỏ vào trang nông nghiệp → **hại cả hai trang**.

**Tự kiểm.** So chữ neo / tiêu đề thẻ với `<title>` của trang đích:
```bash
python3 - <<'EOF'
import re,glob,os
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    for m in re.finditer(r'<a href="(/[a-z0-9\-/]+/)"[^>]*>([^<]{15,90})</a>',s):
        p=m.group(1).strip('/')+'/index.html'
        if not os.path.exists(p): continue
        t=re.search(r'<title>(.*?)</title>',open(p,encoding='utf-8').read())
        if not t: continue
        neo=set(m.group(2).lower().split()); tit=set(t.group(1).lower().split())
        if neo and len(neo&tit)/len(neo)<0.15:
            print('%-40s neo="%s" -> %s'%(f[:40],m.group(2)[:44],t.group(1)[:44]))
EOF
```
Kết quả ra nhiều dòng là bình thường (chữ neo ngắn gọn ≠ title). Đọc lướt tìm cặp **lệch hẳn chủ đề**.

---

### 🔴 7. Lô đã bán nằm dưới tiêu đề "đang bán"

**Triệu chứng.** 3 trang khu có tiêu đề *"— lô đang bán"* nhưng trong lưới có **4 tin đã bán**,
trong đó **thẻ nổi bật đầu trang** là một cụm đã bán sỉ cả cụm.

**Vì sao nguy.** Thứ đầu tiên khách nhìn thấy là hàng không còn.

**Luật đã chốt sau đó.** Tin đã bán **không bao giờ gỡ** — để lại, mang nhãn "Đã bán", xếp cuối,
và **tiêu đề tách bạch hai con số**: *"25 lô đất đang bán · 2 đã bán"*. Tin đã bán là bằng chứng
giao dịch thật và là mốc giá để khách tự định giá.

**Tự kiểm.** Đếm tin có cờ "đã bán" nằm trong khối tiêu đề "đang bán"; đối chiếu con số ghi
trên tiêu đề với số thẻ thật.

---

### 🔴 8. Trang khu hứa một đằng, hiện một nẻo

**Triệu chứng.** Trang `/dat-dong-thanh.../` tiêu đề *"lô đang bán"*, chỉ có **6 thẻ**,
trong khi bộ lọc trên hub đếm **26 lô** cùng khu. Khách bấm chip "Đông Thanh 26" rồi bấm
"Xem trang riêng" → **ra trang ít lô hơn cái vừa xem**. Nặng nhất: trung tâm **11 thẻ / 69 lô**.

**Cách sửa an toàn (quan trọng).** Đổ đủ lô vào bằng cách **copy nguyên khối thẻ HTML** từ hub,
**không viết lại chữ** → không có cơ hội chế nhầm diện tích/giá/pháp lý. Sau đó **đối chiếu lại
từng thẻ với bản gốc**: lệch 0 ký tự.

**Và phải kiểm phân loại.** Đối chiếu nhãn khu của hub với **nội dung từng trang chi tiết**
(H1 + hàng "Vị trí" + mô tả). Kết quả thật: 155 tin, lệch 15, soi tay từng cái —
**11 là báo động giả** (trang nhắc tên khu khác vì đó là **tên đường** hoặc **địa danh gần**:
*"đường nhựa X, tuyến A–B"*, *"gần hồ Y"*), **1 sai thật**, **3 không đủ chắc → không xếp,
chờ chủ xác nhận**.

> Bài học: **máy quét chỉ để khoanh vùng, không để quyết định.** Tỉ lệ báo động giả 73%.

---

### 🔴 12. CSS chỉ nằm nhúng trong 3 trang

**Triệu chứng.** Toàn bộ layout của thẻ sản phẩm (lưới 3 cột, ảnh, chip, cột giá, media query
điện thoại) **chỉ nằm trong `<style>` nhúng của 3 trang**. **12 trang khác** dùng **đúng loại thẻ đó**
mà không có một dòng CSS → **~250 thẻ vỡ hẳn**: chữ tràn, các chip dính liền nhau
(*"Đông Thanh · Nam Ban · Lâm **Hà**Thổ cư ~95m²/lô**Khu** dân cư hiện hữu"*), cột giá bị bóp
thành dòng dọc (*"Từ / 8xx / triệu"*).

**Vì sao lâu không ai thấy.** Các trang đó ít thẻ nên trông "hơi xấu" chứ không "vỡ".
Chỉ khi một trang lên 96 thẻ mới lộ.

**Tự kiểm — đây là phép kiểm đáng giá nhất trong tờ này.**
```bash
# Trang nào dùng một lớp CSS mà lớp đó không có trong file CSS dùng chung?
python3 - <<'EOF'
import re,glob
css=''.join(open(f,encoding='utf-8').read() for f in glob.glob('css/*.css'))
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    noi=' '.join(re.findall(r'<style>([\s\S]*?)</style>',s))
    for lop in set(re.findall(r'class="([a-z][a-z0-9 _-]*)"',s)):
        for l in lop.split():
            if '.'+l not in css and '.'+l not in noi:
                print('%-46s .%s  KHÔNG có CSS ở đâu cả'%(f[:46],l))
EOF
```

**Sửa.** Đưa **một bản duy nhất** vào file CSS dùng chung, **gỡ hết bản nhúng** để không lệch nhau.

---

### 🔴 13. Cache CSS 24h + tên file không đổi

**Triệu chứng.** Sửa CSS, đẩy lên, chủ web mở lại: **y nguyên như cũ**. Sửa lần nữa: vẫn vậy.

**Nguyên nhân.** Header đặt `/css/*` là `max-age=86400, stale-while-revalidate=604800`.
Tên file **không bao giờ đổi** → máy đã vào web dùng bản cũ **tới 24 tiếng**,
**kéo-xuống-refresh trên iPhone không tải lại file css**, `stale-while-revalidate` kéo thêm 7 ngày.

> **Đây là lỗi nền nguy hiểm nhất trong tờ này** vì nó làm **mọi lần sửa giao diện trước đó**
> đều tới tay khách chậm cả ngày, mà không ai biết.

**Tự kiểm.**
```bash
# 1. Header cache cho css/js đặt bao lâu?
grep -A3 "css\|js" vercel.json   # hoặc .htaccess / nginx.conf / netlify.toml
# 2. Đường dẫn CSS có mã phiên bản không?
grep -rho 'href="[^"]*\.css[^"]*"' --include=*.html . | sort -u
```
Nếu cache dài **và** đường dẫn không có `?v=` hay mã băm trong tên file → **đang dính**.

**Sửa (cách mọi web lớn dùng).** Gắn `?v=<vân tay nội dung>` vào đường dẫn:
```bash
python3 - <<'EOF'
import hashlib,glob,re
v={p:hashlib.sha1(open(p,'rb').read()).hexdigest()[:8] for p in ['css/style.css','js/main.js']}
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read(); g=s
    for p,h in v.items():
        s=re.sub(r'((?:href|src)="(?:\.\./)*/?%s)(\?v=[0-9a-f]+)?"'%re.escape(p),
                 r'\1?v='+h+'"',s)
    if s!=g: open(f,'w',encoding='utf-8').write(s)
EOF
```
**Không cần sửa header** — giữ cache dài vẫn tốt, chỉ cần địa chỉ đổi khi nội dung đổi.

**Chặn tái phát.** Cổng chặn push: nếu `?v=` **không khớp vân tay file hiện tại** → báo lỗi.

---

### 🔴 14. Nút hiện ra nhưng JS chặn theo đường dẫn

**Triệu chứng.** File JS dùng chung có dòng:
```js
var p=location.pathname;
if(p.indexOf('/trang-a')<0 && p.indexOf('/trang-b')<0) return;
```
Nhưng nút mà đoạn JS đó điều khiển lại được **in ra trên 6 trang khác** → **142 nút bấm không ăn gì.**

**Vì sao nguy.** Khách bấm, không có gì xảy ra, bỏ đi. Không có lỗi nào hiện ra để ai biết.

**Tự kiểm — phép kiểm quan trọng nhất cho nút bấm.**
```bash
python3 - <<'EOF'
import re,glob,os
chung=open('js/main.js',encoding='utf-8').read()
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    d='/'+os.path.dirname(f)+'/'
    js=' '.join(re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>',s))
    if 'js/main.js' in s: js+=chung
    for m in re.finditer(r'var\s+p\s*=\s*location\.pathname;\s*if\s*\(([\s\S]{0,240}?)\)\s*return;',js):
        cho=re.findall(r"p\.indexOf\('([^']+)'\)<0",m.group(1))
        if cho and all(x not in d for x in cho):
            print('%-44s JS bị chặn, chỉ chạy ở %s'%(f[:44],', '.join(cho)))
EOF
```
Rộng hơn: **liệt kê mọi lớp/id nút trong HTML, kiểm xem chuỗi đó có trong JS chạy trên trang đó không.**

**Sửa.** Bỏ chặn theo đường dẫn. Dùng điều kiện **"trang có nút đó không"** thay vì
**"trang tên gì"** — vì tên trang sẽ thay đổi, còn nút thì tự nó biết mình có mặt.

---

### 🟠 16. Từ hành chính hết hiệu lực

**Triệu chứng.** Đơn vị hành chính đổi từ 1/7/2025 (bỏ cấp huyện, thị trấn nhập thành xã),
nhưng web còn **47 chỗ "huyện X"** và **198 chỗ "thị trấn Y"** nói như hiện tại.

**Xử lý có cân nhắc — đừng thay máy móc.**
- `huyện X` → `X`: **an toàn tuyệt đối**, chỉ bỏ một đơn vị đã bỏ, câu không đổi nghĩa.
- `thị trấn Y` → khó hơn: **người ta VẪN search "đất thị trấn Y"**. Bỏ sạch là mất từ khoá.
  - **Cách đã chốt:** giữ nguyên `<title>`, `<h1>`, URL (giữ từ khoá + không mất link đang index);
    trong thân bài đổi thành *"trung tâm Y"*, **lần đầu mỗi trang ghi thêm "(thị trấn Y cũ)"**
    để người search từ cũ vẫn thấy chữ đó trên trang.
  - **Không đụng** câu FAQ giải thích *"Thị trấn Y còn tồn tại không?"* — đó chính là chỗ giải thích.

**Tự kiểm.**
```bash
grep -rno "huyện [A-ZĐ][a-zà-ỹ]*\|thị trấn [A-ZĐ][a-zà-ỹ]*" --include=*.html . \
  | sed 's/:[0-9]*:/ | /' | sort | uniq -c | sort -rn | head
```
Rồi tra lại quyết định sáp nhập của địa phương xem tên nào đã hết hiệu lực.

**Bẫy tự gây khi làm (T3).** Thay `thị trấn Y` → `trung tâm Y` làm câu
*"trung tâm **thị trấn** Y"* thành *"trung tâm **trung tâm** Y"* ở **37 chỗ / 9 trang**;
và chú thích chèn vào giữa một ngoặc đơn có sẵn tạo `)` lồng nhau ở 6 trang.
**Luôn quét lặp từ sau khi thay hàng loạt:**
```bash
grep -rno "\b\(\w\+\) \1\b" --include=*.html . | head -20
grep -rn "))" --include=*.html . | head
```

---

### 🟠 17. Thì tương lai cho việc đã xảy ra

**Triệu chứng.** Trang Hỏi Đáp — **trang AI và Google đọc trước tiên** — còn hỏi
*"Xã X **sắp** sáp nhập vào đâu?"* với câu trả lời ở thì tương lai, trong khi việc đã xảy ra
**14 tháng trước**.

**Tự kiểm.** Quét từ chỉ tương lai đi kèm mốc đã qua:
```bash
grep -rn "sắp \|dự kiến \|sẽ sớm \|trong thời gian tới\|đang triển khai" --include=*.html . | head -30
```
Với mỗi kết quả: **việc đó đã xảy ra chưa?**

**Chú ý.** Phải sửa **cả bản hiện trên trang lẫn bản trong JSON-LD** — hai chỗ, dễ sót một.

---

### 🟠 18. Bậc tiêu đề nhảy cóc

**Triệu chứng.** **208/219 trang** nhảy `h2 → h4`, do tiêu đề chân trang và thanh bên để `h4`
trong khi thân bài dùng `h2`.

**Vì sao nguy.** Trình đọc màn hình và bộ trích dẫn của AI đọc trang **theo cây tiêu đề**.
Nhảy bậc là cây gãy — máy không biết mục nào thuộc mục nào.

**Tự kiểm.**
```bash
python3 - <<'EOF'
import re,glob
for f in glob.glob('**/*.html',recursive=True):
    s=re.sub(r'<(script|style)[\s\S]*?</\1>','',open(f,encoding='utf-8').read())
    t=0
    for m in re.finditer(r'<h([1-6])\b',s):
        h=int(m.group(1))
        if t and h>t+1: print(f,'nhảy h%d->h%d'%(t,h)); break
        t=h
EOF
```

**Sửa — cẩn thận chỗ này.** Đổi `h4`→`h2` thì **cỡ chữ đổi hẳn** nếu CSS đang nhắm `h4`
(mặc định `h2` to gấp rưỡi). Phải: đổi tag **và** cập nhật mọi selector `... h4` thành `... h2`,
**và** ghi rõ `font-size` cho các lớp không có luật riêng làm lưới an toàn.

---

### 🟠 19–22. Nhóm lỗi "hub không làm đúng việc của hub"

- **#19** — **5 bài không được chính hub của nó liệt kê**, trong đó có bài 5.672 chữ.
  Không mồ côi (trang khác có link), nhưng hub là mục lục chính, Google tính rất nặng.
  ```bash
  # so danh sách thư mục con với danh sách link trên trang hub
  ls -d chuyen-muc/*/ | sed 's|/$||;s|.*/||' | sort > /tmp/co.txt
  grep -o 'href="/chuyen-muc/[a-z0-9-]*/"' chuyen-muc/index.html \
    | sed 's|.*/\([^/]*\)/"|\1|' | sort -u > /tmp/lk.txt
  comm -23 /tmp/co.txt /tmp/lk.txt     # bài có mà hub không liệt kê
  ```
- **#20** — 3 hub **thiếu hẳn** `CollectionPage` + `ItemList` → Google không hiểu đó là bộ sưu tập.
- **#21** — 16 trang chi tiết thiếu node `WebSite`/`SearchAction`, `WebPage` không nối vào website.
- **#22** — `ItemList` khai **9 mục** trong khi trang chỉ hiện **7 thẻ**: 2 tin thật **bị thiếu khỏi trang**
  mà schema vẫn khai. Luôn kiểm **số mục ItemList == số thẻ hiện trên trang**, và **đúng thứ tự**.

---

### 🟠 26. Thẻ thiếu dữ liệu mà bộ lọc đọc tới

**Triệu chứng.** 33 thẻ nhà không có `data-area`/`data-price` → hub đó **không lọc theo giá
hay diện tích được**, và khi đưa sang trang khác có bộ lọc thì chúng **bị ẩn nhầm**.

**Luật đã chốt khi sửa — rất quan trọng.**
> Giá trị **0 nghĩa là CHƯA BIẾT**, và **chưa biết thì KHÔNG ẩn**. Ẩn đi là **giấu mất hàng thật**
> của chủ web. Thà hiện thừa còn hơn giấu nhầm.

**Tự kiểm.** Với mỗi trang có bộ lọc: đọc JS xem nó dùng những `data-*` nào, rồi đếm thẻ thiếu.
```bash
python3 - <<'EOF'
import re,glob
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    js=' '.join(re.findall(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)</script>',s))
    the=re.findall(r'<article class="[^"]*card[^"]*"[^>]*>',s)
    for k in re.findall(r"getAttribute\(['\"]data-([a-z]+)['\"]\)",js):
        thieu=[t for t in the if 'data-%s='%k not in t]
        if thieu: print('%-44s %d/%d thẻ thiếu data-%s'%(f[:44],len(thieu),len(the),k))
EOF
```

---

### 🟠 28. Bài cùng chủ đề không nối nhau

**Triệu chứng.** 6 bài cùng cụm chủ đề, **0 bài nào trỏ sang bài nào**. Một bài chỉ có
**đúng 1 link vào** cả site.

**Vì sao nguy.** Đây là **lý do chính khiến người ta khuyên gộp bài**. Google gặp 6 trang yếu
lẻ loi thay vì 1 cụm mạnh. **Giữ riêng chỉ thắng khi các bài nối nhau.**

**Trước khi quyết gộp hay giữ — đo tự cắn từ khoá:**
```bash
python3 - <<'EOF'
import re,glob,os
def tu(s):
    s=re.sub(r'[^a-zà-ỹ0-9\s]',' ',s.lower())
    return set(w for w in s.split() if len(w)>2)
B=[]
for f in glob.glob('chuyen-muc/*/index.html'):
    s=open(f,encoding='utf-8').read()
    t=re.search(r'<title>(.*?)</title>',s).group(1)
    d=re.search(r'<meta name="description" content="([^"]*)"',s)
    h=' '.join(re.sub(r'<[^>]+>','',x) for x in re.findall(r'<h2[^>]*>([\s\S]{0,90}?)</h2>',s)[:6])
    B.append((os.path.dirname(f),tu(t+' '+(d.group(1) if d else '')+' '+h)))
for i in range(len(B)):
    for j in range(i+1,len(B)):
        a,b=B[i][1],B[j][1]
        if a and b and len(a&b)/len(a|b)>0.30:
            print('%.0f%%  %s  <->  %s'%(len(a&b)/len(a|b)*100,B[i][0],B[j][0]))
EOF
```
- Có cặp **>30%** → hai bài đang giành nhau một câu search → **cân nhắc gộp**.
- **Không cặp nào** → giữ riêng là đúng, nhưng **bắt buộc nối thành cụm**.

**Cách nối đúng.** Cuối mỗi bài, khối "Cùng chủ đề" trỏ sang 3 bài anh em, **chữ neo là CÂU HỎI
bài đích trả lời**. **Cấm "xem thêm", "tại đây", "click vào đây"** — chữ neo vô nghĩa thì
Google và AI không biết bài kia nói gì.

Kết quả thật sau khi nối: bài yếu nhất từ **1 → 5 link vào**.

---

### 🟡 23–25, 27. Nhóm lỗi trải nghiệm & khả năng tiếp cận

- **#23** Lọc xong **không ghi vào URL** → khách lọc ra "Đông Thanh + dưới 1 tỷ" rồi **không gửi
  được cho ai**, bấm back cũng mất. Sửa bằng `history.replaceState`. *(Một hub có, một hub không —
  đúng kiểu lỗi "chép tay nên lệch".)*
- **#24** Chip bật/tắt thiếu `aria-pressed` → trình đọc màn hình không biết chip nào đang bật.
- **#25** Ô chọn / ô tìm thiếu `aria-label` hoặc `<label for>`.
- **#27** **3/7 trang khu là ngõ cụt** — không có đường sang khu khác, khách vào rồi chỉ có
  đường quay ra hub.

---

### 🟠 29. Câu hỏi để đóng (bổ sung, chốt sau cùng)

**Luật đã chốt:** **724 câu hỏi trên 204 trang** đều để `<details>` **đóng**. Đổi thành
**mở sẵn hết** — đáp án hiện thẳng trên trang cho Google và các bộ máy trả lời AI đọc,
khách cũng khỏi phải bấm. Dấu `+`/`–` vẫn chạy, ai muốn gập vẫn gập được.

```bash
grep -c "<details\b" index.html ; grep -c "<details open" index.html   # hai số phải bằng nhau
```

---

### 🟠 15. Nút Menu thanh đáy chết

**Triệu chứng.** 8 trang có nút Menu ở thanh đáy điện thoại mang **id lạ** lại còn `display:none`,
trong khi JS mở menu tìm một id khác → **không mở được menu từ thanh đáy**, khách phải cuộn
ngược lên đầu trang.

**Tự kiểm.** Với mọi trang: thanh đáy có đủ **Gọi · Zalo · Menu bấm được** không?
```bash
python3 - <<'EOF'
import re,glob
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    i=s.find('class="mobile-nav"')
    if i<0: print(f,'KHÔNG có thanh đáy'); continue
    bar=s[i:s.find('</nav>',i)]
    if 'tel:' not in bar: print(f,'thiếu nút GỌI')
    nut=[m.group(0) for m in re.finditer(r'<(?:button|a)[^>]*>',bar)
         if 'menu' in m.group(0).lower()
         and 'display:none' not in m.group(0) and not re.search(r'\shidden(?=[\s>])',m.group(0))]
    if not nut: print(f,'nút Menu KHÔNG bấm được')
EOF
```

---

## C. NHỮNG THỨ ĐÃ ĐÚNG SẴN — VẪN NÊN KIỂM Ở WEB KHÁC

Đo được, không phải đoán. Web khác rất có thể **sai ở đúng những chỗ này**.

| Hạng mục | Kết quả đo | Lệnh kiểm |
|---|---|---|
| Trang mồ côi | **0** | dựng đồ thị link, BFS từ trang chủ |
| Độ sâu bấm từ trang chủ | xa nhất **3 lần bấm** | BFS, đếm tầng |
| Link nội bộ gãy | **0** | `href` nội bộ → `os.path.exists` |
| Ảnh gãy | **0** (sau khi sửa 1) | `src` → `os.path.exists` |
| JSON-LD hỏng | **0/219 trang** | `json.loads` từng khối |
| Viewport chặn phóng to | **0 trang** | tìm `user-scalable=no`, `maximum-scale` |
| Bảng rộng tràn màn | **0** — đều bọc `overflow-x:auto` | tìm `<table ... min-width` không có bọc |
| Cỡ chữ quá nhỏ | **0 luật** dưới 11px | quét `font-size:<0.7rem` |
| Ảnh thiếu `width`/`height` | chỉ thẻ lightbox rỗng — đúng thiết kế | đếm `<img>` thiếu 2 thuộc tính |
| Ảnh thiếu `alt` | **0** | đếm `<img>` không có `alt=` |
| Chữ bị giấu ăn SEO | **0** — 16 khối ẩn đều là trạng thái giao diện thật | quét `display:none`, `hidden`, `visibility:hidden`, `opacity:0`, `text-indent` âm, `font-size:0` |
| Số trên chip lọc | **khớp 100%** số thẻ lọc ra | mô phỏng từng chip |
| Thanh Gọi/Zalo dán đáy | **219/219 trang** | như lệnh mục #15 |
| Tự cắn từ khoá | **0 cặp >30%** trên 28 bài | như lệnh mục #28 |
| Tin đăng có bảng thông số | **155/155** | đếm `<table>` trong trang chi tiết |
| Trùng `<title>` / `description` | **0** | gom vào dict, đếm trùng |
| Redirect thiếu biến thể `/` cuối | **0** | so `source` với/không dấu `/` |

**Hai thứ nữa đã đúng nhưng suýt "sửa nhầm" — ghi lại để đừng phá cái đang đúng:**

1. **Khoảng cách khai khác nhau giữa các tin là ĐÚNG** (mỗi tin một vị trí).
   Máy báo "86 cách nói khác nhau" — đọc kỹ thì hợp lệ.
2. **Tin để giá "Liên hệ" mà không có `Offer` trong schema là ĐÚNG.**
   `Offer` không có giá là sai chuẩn; thêm vào mới là làm hỏng. 3 tin thuộc diện này.

---

## D. SÁU BÀI HỌC GỐC — PHẦN QUAN TRỌNG NHẤT

Lỗi cụ thể thì mỗi web mỗi khác. **Nguyên nhân gốc thì giống nhau.**

### 1. Thứ gì chép tay ra nhiều trang thì sẽ có trang sai

Ba lỗi **nặng nhất** trong tờ này đều cùng gốc này:
- CSS thẻ sản phẩm nhúng trong 3 trang → 12 trang khác vỡ
- JS mở menu chép tay từng trang → 8 trang có id lạ
- Ghi URL khi lọc → một hub có, một hub không

> **Luật:** thứ gì dùng ở **hơn một trang** thì phải nằm ở **một chỗ duy nhất** dùng chung.
> Kiểm bằng cách: **liệt kê mọi lớp CSS / mọi id JS trong HTML, đối chiếu với file dùng chung.**

### 2. Chỉ kiểm cái vừa sửa là kiểu gì cũng sót

Chủ web nói đúng: *"sửa và rà nhiều lần vẫn ra lỗi"*. Vì mỗi lần chỉ kiểm đúng chỗ vừa đụng.

> **Luật:** sửa một cái thì **kiểm cả loại đó trên mọi trang**.
> Ví dụ: thêm `aria-pressed` cho chip ở hub A → phải quét **mọi chip trên mọi hub**.
> Thực tế: làm đúng vậy mới lòi ra 6 chip ở hub khác và 2 ô chọn còn thiếu.

### 3. Mỗi lỗi sửa xong phải thành một cái bẫy tự động

Sửa tay thì lần sau lặp lại. Cách duy nhất để **không nói hoài** là biến mỗi lỗi thành
một phép kiểm chạy trước mỗi lần đăng, **và thử phá để chắc bẫy kêu thật**.

Thực tế: có **3 lần** bẫy viết xong **không kêu** vì viết sai (sai khoá dictionary, quét cả trang
thay vì quét đúng khối, regex bắt hụt). **Không thử phá thì đã tưởng là an toàn.**

> **Luật:** viết bẫy xong, **cố tình phá một chỗ**, chạy lại, thấy nó kêu **rồi mới khôi phục**.

### 4. Máy quét để khoanh vùng, không để quyết định

- Đối chiếu phân loại khu: 15 chỗ lệch → **11 là báo động giả** (73%).
- Khoảng cách: báo "86 cách nói khác nhau" → thực ra đúng hết.
- Lặp từ: báo "Nam Ban Nam Ban" → là hai phần tử cạnh nhau, không phải lỗi.

> **Luật:** máy chỉ ra danh sách nghi ngờ; **người đọc từng cái rồi mới sửa**.
> Cái nào **không đủ chắc thì để nguyên và hỏi chủ**, đừng đoán. (3 lô đã để lại chờ chủ xác nhận —
> và hoá ra 1 trong 3 chủ xếp khác hẳn suy đoán của máy.)

### 5. Đừng sửa HTML/JSON bằng biểu thức tìm kiếm mù

Ba lỗi **tự gây** trong đợt này đều do đó:
- `\](?=\})` khớp nhầm dấu `]` đầu tiên → **cắt cụt JSON-LD của 6 trang**
- `[\s\S]*?` dừng ở `</div>` đầu tiên **nằm trong** một thẻ → **3 mục lạ lọt sang trang mới**
- Chèn chú thích không xét ngoặc đang mở → **`)` lồng nhau** + **lặp từ 37 chỗ**

> **Luật:**
> - JSON → **`json.loads` ra object, sửa trong cây, `json.dumps` lại.** Không regex.
> - HTML khối → cắt bằng **chỉ số** (tìm thẻ mở, tìm thẻ đóng cuối cùng), không dùng `.*?`.
> - Thay chuỗi hàng loạt → **quét lặp từ và ngoặc lệch ngay sau đó**.

### 6. Lỗi tệ nhất là lỗi không báo lỗi

Xếp theo mức khó phát hiện:

| Loại | Vì sao khó thấy |
|---|---|
| **Cache CSS** | Code đúng, deploy đúng, chỉ máy khách là cũ. Không log, không lỗi. |
| **Nút bấm chết** | Nút hiện đẹp, bấm không có gì, không lỗi console. |
| **Schema không khớp chữ hiện** | Trang trông bình thường. Chỉ Google thấy. |
| **Trang khu thiếu tin** | Trang trông đầy đủ. Phải đếm mới biết thiếu. |
| **Số liệu tự chọi nhau** | Mỗi trang đọc riêng đều hợp lý. Phải gom cả site mới thấy. |

> **Luật:** những thứ này **không bao giờ tự lộ ra**. Phải **chủ động đo định kỳ**, không đợi ai báo.

---

## E. BỘ LỆNH KIỂM NHANH — COPY CHẠY MỘT LƯỢT

```bash
# 1. JSON-LD có hỏng không
python3 -c "
import re,glob,json,sys
b=0
for f in glob.glob('**/*.html',recursive=True):
    for m in re.finditer(r'<script type=\"application/ld\+json\">([\s\S]*?)</script>',open(f,encoding='utf-8').read()):
        try: json.loads(m.group(1))
        except Exception as e: b+=1; print('JSON hỏng:',f)
print('JSON-LD lỗi:',b)"

# 2. Canonical trỏ ra ngoài
grep -rho '<link rel="canonical" href="[^"]*"' --include=*.html . | sort | uniq -c | sort -rn | head

# 3. Cache CSS/JS + có mã phiên bản chưa
grep -rho 'href="[^"]*\.css[^"]*"' --include=*.html . | sort -u

# 4. Lớp CSS dùng mà không có định nghĩa
# (xem lệnh đầy đủ ở mục #12)

# 5. Bậc tiêu đề nhảy cóc
# (xem lệnh ở mục #18)

# 6. Câu hỏi còn đóng
python3 -c "
import re,glob
t=o=0
for f in glob.glob('**/*.html',recursive=True):
    s=open(f,encoding='utf-8').read()
    for m in re.finditer(r'<details([^>]*)>',s):
        t+=1
        if re.search(r'\bopen\b',m.group(1)): o+=1
print('details: %d | mở sẵn: %d | còn đóng: %d'%(t,o,t-o))"

# 7. Link & ảnh gãy
python3 -c "
import re,glob,os
g=0
for f in glob.glob('**/*.html',recursive=True):
    b=re.sub(r'<script[\s\S]*?</script>','',open(f,encoding='utf-8').read())
    for i in re.findall(r'src=\"(/[^\"]+\.(?:jpg|png|webp|svg))\"',b):
        if not os.path.exists(i.lstrip('/')): g+=1; print('ảnh gãy:',f,i)
print('ảnh gãy:',g)"

# 8. Số liệu tự chọi nhau + số không nguồn
grep -rn "Khảo sát của\|Theo số liệu\|Theo thống kê" --include=*.html . | head -20

# 9. Từ chỉ tương lai cho việc đã xảy ra
grep -rn "sắp \|dự kiến \|sẽ sớm \|đang triển khai" --include=*.html . | head -20

# 10. Thanh liên hệ dán đáy trên điện thoại
# (xem lệnh ở mục #15)
```

---

## F. KẾT LẠI THÀNH DANH SÁCH KIỂM

Đưa danh sách này cho người lo web khác, bảo họ trả lời **có/không** từng dòng:

**Nền tảng (hỏng cái này thì mọi thứ khác vô nghĩa)**
- [ ] File CSS/JS có mã phiên bản đổi theo nội dung chưa? Cache đặt bao lâu?
- [ ] Có lớp CSS nào dùng mà không có định nghĩa ở file dùng chung không?
- [ ] Có nút bấm nào hiện ra mà JS không chạy trên trang đó không?
- [ ] JSON-LD có trang nào hỏng không?

**Sự thật & niềm tin**
- [ ] Có số liệu nào không nói được nguồn không?
- [ ] Cùng một thứ có bị nói nhiều kiểu số khác nhau giữa các trang không?
- [ ] Có mốc thời gian/tình trạng nào đã lỗi thời không?
- [ ] Hàng đã bán/hết còn nằm dưới tiêu đề "đang bán" không?
- [ ] Số ghi trên nhãn/nút có khớp số thật hiện ra không?
- [ ] Có thẻ nào tiêu đề một đằng, link một nẻo không?

**SEO / AEO / GEO**
- [ ] Canonical có trang nào nhường index cho web khác không?
- [ ] Nội dung trong schema có hiện trên trang không?
- [ ] Câu hỏi có mở sẵn không?
- [ ] Bậc tiêu đề có nhảy cóc không?
- [ ] Hub có liệt kê đủ bài con không? Có CollectionPage + ItemList không?
- [ ] ItemList có khớp đúng số và thứ tự thẻ hiện trên trang không?
- [ ] Bài cùng chủ đề có nối nhau không? Chữ neo có nghĩa không?
- [ ] Có cặp bài nào giành nhau một câu search không?

**Trải nghiệm**
- [ ] Trang nào là ngõ cụt (không có đường đi tiếp) không?
- [ ] Độ sâu bấm từ trang chủ tối đa bao nhiêu? Có trang mồ côi không?
- [ ] Lọc xong có ghi vào URL để chia sẻ được không?
- [ ] Trạng thái rỗng (lọc ra 0 kết quả) có chỉ đường đi tiếp không?
- [ ] Trên điện thoại: thanh liên hệ dán đáy có đủ nút không, Menu bấm được không?
- [ ] Nút bật/tắt có `aria-pressed` không? Ô chọn/ô tìm có nhãn không?
- [ ] Trên điện thoại có tràn ngang không? Có chặn phóng to không?

**Kỷ luật lâu dài**
- [ ] Mỗi lỗi đã sửa có thành một phép kiểm tự động chưa?
- [ ] Đã **thử phá** để chắc phép kiểm đó kêu thật chưa?
- [ ] Phép kiểm có chạy tự động trước mỗi lần đăng không?

---

## Bổ sung 24/9/2026 — đợt kiểm tay 42 mục còn lại

| # | Lỗi | Cách kiểm | Cách sửa |
|---|-----|-----------|----------|
| 29 | Hub cuộn 122 thẻ lô không có một nút Gọi; trang lô đọc xong khối rủi ro hết nút; mục to nhất menu điện thoại trỏ /lien-he/ | `python3 scripts/kiem-bo-loc.py` (bẫy 14) | `python3 scripts/them-nut-goi.py` — nút Gọi từng thẻ (icon tròn trên điện thoại), khối Gọi sau rủi ro, giữa bài, đầu 8 trang dịch vụ, mục cuối sheet = `tel:` |
| 30 | Trang chủ nói "tuyến tránh đang thi công", "100% sổ hồng" trong khi bài/lô nói ngược lại; ROI 8–12%, lấp đầy 60–70%, 40–60% không nguồn | grep số % + "100%" + "đang thi công" toàn site, đối chiếu bài gốc | Gỡ số hoặc gắn số thật từ danh mục (villa 385m² cho thuê 12 triệu/tháng) |
| 31 | Một lô đăng 2 URL (trùng từng thông số) — tự tranh hạng, khách nghi khan hiếm giả | quét trang lô khớp (giá, diện tích, mặt tiền) | 301 URL cũ → URL mới trong vercel.json, gỡ khỏi hub/khu/sitemap, đổi mọi link nội bộ, chỉnh số đếm; `do-lo-vao-trang-khu.py` nay bỏ thẻ không còn trên hub |
| 32 | Trang "giá hôm nay, cập nhật hàng tuần" đứng im 83 ngày | so `dateModified` với lời hứa tần suất trong title | `scripts/cap-nhat-gia-hom-nay.py` + Routine thứ Hai; số lấy từ data-area/data-price hub, không điền tay |
| 33 | Chữ trắng trên vàng 2.29:1, #8a978f 3.04:1 (527 chỗ), `.sec-label` opacity .85 kéo xuống 3.5:1 | tính WCAG (không đoán) | Chữ tối #1A2420 trên vàng; #8a978f→#5F6E66; bỏ opacity, đổi màu thật |
| 34 | Sheet menu / thanh so sánh ẩn bằng transform/opacity → Tab vẫn dừng vào link vô hình; không aria-expanded; Esc không đóng bảng | grep `aria-expanded`, đọc CSS lúc đóng | `visibility:hidden` + transition delay; aria-expanded 2 nút; Esc + trả focus |
| 35 | Hero nền CSS không có srcset → điện thoại tải bản 152KB cho khung 390px | ls kích thước ảnh + grep `url(` | @media đổi background-image theo bề rộng; preload có `media=` cho trang chủ |
| 36 | Mô tả meta 176 trang >160 ký tự, giá + hotline nằm sau chỗ Google cắt; nút "Gọi tư vấn" yếu; thiếu "trả lời trong ngày, không ràng buộc" | script đo độ dài | Cắt ở ranh câu 80–130 ký tự + giá lấy từ **schema** (không bắt chữ — đã suýt ghi giá thuê thành giá bán) + "Gọi 0978 758 788." |
| 37 | 404.html không có `?v=` vì script chỉ quét `**/index.html`; cache css/js 1 ngày dù đã có vân tay; thiếu CSP | grep href style.css toàn HTML | glob `**/*.html`; `max-age=31536000, immutable`; CSP liệt kê đúng tên miền đang dùng |

**Bài học thêm:** (1) số trong mô tả/tiêu đề phải lấy từ dữ liệu có cấu trúc, không regex chữ; (2) mỗi lời hứa tần suất ("hàng tuần", "hôm nay") phải có script + Routine đứng sau, không thì đừng hứa; (3) nút liên hệ đặt theo **khoảnh khắc khách tin nhất** (sau rủi ro, sau phân tích), không chỉ đầu/cuối trang.

| 38 | Hub Đất Nền ghi "94 lô, từ 480 triệu" ở `<title>`, mô tả, og, twitter, schema — thật là 116 lô, từ 368 triệu | bẫy 13b trong `kiem-bo-loc.py` (soi `<head>`, bẫy 13 cũ chỉ soi thân trang) | `cap-nhat-gia-hom-nay.py` đặt lại title/mô tả 2 hub mỗi thứ Hai |
| 39 | FAQ tự viết "Đà Lạt chênh 5–10 lần" — không nguồn, mâu thuẫn bài so sánh (50–150 triệu/m²) | đối chiếu mọi số mới với bài gốc trên site trước khi viết | Dẫn đúng số bài so sánh, không tự suy tỷ lệ |
| 40 | `/ban-dat-thi-tran-nam-ban` 301 về hub chung thay vì trang thị trấn | đọc `vercel.json` theo từ khoá | 301 về `/dat-trung-tam-thi-tran-nam-ban/` |

**Bài học:** số trong `<head>` (title, mô tả, og) là thứ Google hiện ra — phải do script sinh từ dữ liệu, không gõ tay.

