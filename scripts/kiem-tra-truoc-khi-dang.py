#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KIỂM TRA TRƯỚC KHI ĐĂNG — cổng chặn lỗi cho Nam Ban Villas.

Chạy:  python3 scripts/kiem-tra-truoc-khi-dang.py
Thoát 0 = sạch, được push.   Thoát 1 = CÓ LỖI, sửa rồi chạy lại.

Script này bắt lại ĐÚNG những lỗi đã từng xảy ra thật trên site (mỗi mục ghi rõ
"đã từng dính" để hiểu vì sao phải kiểm). Máy kiểm thay vì trông vào trí nhớ.
Không cần mạng — chỉ đọc file trong repo.
"""
import glob, json, os, re, sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
HOST = "https://nambanvillas.vn"

loi, canh_bao = [], []
def L(msg):  loi.append(msg)
def W(msg):  canh_bao.append(msg)

# ── nạp dữ liệu ────────────────────────────────────────────────────────────
pages = [f for f in glob.glob("**/index.html", recursive=True)
         if not f.startswith(("node_modules", "docs"))]
data = {f: open(f, encoding="utf-8").read() for f in pages}
def cac_node(obj):
    """Trả mọi node schema, kể cả khi gói trong @graph.
    ĐÃ TỪNG SUÝT DÍNH: gộp schema vào @graph thì mọi luật đọc @type ở tầng ngoài
    lặng lẽ ngừng chạy — script vẫn báo SẠCH trong khi không còn kiểm gì."""
    ra = []
    for x in (obj if isinstance(obj, list) else [obj]):
        if not isinstance(x, dict):
            continue
        if isinstance(x.get("@graph"), list):
            ra.extend(n for n in x["@graph"] if isinstance(n, dict))
        else:
            ra.append(x)
    return ra


def duong_dan(f):
    d = os.path.dirname(f)
    return f"/{d}/" if d else "/"
tap_trang = {duong_dan(f) for f in pages}

sitemap = open("sitemap.xml", encoding="utf-8").read()
sm_urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
sm_paths = {u.replace(HOST, "") for u in sm_urls}
vercel = json.load(open("vercel.json", encoding="utf-8"))
redirects = vercel.get("redirects", [])
nguon_redirect = {r["source"].rstrip("/") + "/" for r in redirects}

# trang thông tin ĐƯỢC PHÉP canonical sang web khác (Hiến pháp 3 web)
CANONICAL_NGOAI_OK = ("thi-truong/", "ve-nam-ban/", "namban-notes/")
# tuỳ bút cố ý viết ngôi thứ nhất
TUY_BUT = ("buoi-sang-tren-doi-ca-phe", "co-dang-song-o-nam-ban",
           "khong-phai-ai-cung-hop", "nam-ban-co-gi")
# Ngôi thứ nhất CỐ Ý, đã duyệt — không báo nữa:
#   cham-diem-lo-dat : nút "Tôi sắp MUA/BÁN" (lời của khách) + thành ngữ "biết mình đang đứng ở đâu"
#   namban-notes/    : trích lời người thật trong câu chuyện
MIEN_TRU_NGOI_1 = ("cham-diem-lo-dat/index.html", "namban-notes/index.html")

print("KIỂM TRA %d TRANG\n%s" % (len(pages), "=" * 62))

# ── 1. JSON-LD hợp lệ + không sót dấu xung đột git ────────────────────────
# ĐÃ TỪNG DÍNH: schema hỏng do nối chuỗi tay; marker <<<<<<< lọt vào file đã commit.
for f, s in data.items():
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(b)
        except Exception as e:
            L(f"[JSON-LD hỏng] {f}: {str(e)[:60]}")
    for ln in s.split("\n"):
        if ln.startswith("<<<<<<< ") or ln.startswith(">>>>>>> ") or ln == "=======":
            L(f"[Dấu xung đột git còn trong file] {f}")
            break

# ── 2. Thẻ cơ bản: title/description duy nhất, 1 H1, canonical ────────────
titles, descs = defaultdict(list), defaultdict(list)
for f, s in data.items():
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not t: L(f"[Thiếu <title>] {f}")
    else:
        tt = t.group(1).strip()
        titles[tt].append(f)
        # Google cắt title ở khoảng 60–65 ký tự tiếng Việt. Cắt mất đuôi thương
        # hiệu thì không sao, nhưng title >100 ký tự là cắt mất cả GIÁ và THỔ CƯ
        # — đúng hai thứ khiến người ta bấm vào. Dồn số quan trọng lên đầu.
        if len(tt) > 100:
            W(f"[Title {len(tt)} ký tự — Google cắt mất giá/thổ cư, dồn số lên đầu] {f}")
    if not d: L(f"[Thiếu meta description] {f}")
    else: descs[d.group(1).strip()].append(f)

    n_h1 = len(re.findall(r"<h1[^>]*>", s))
    if n_h1 != 1: L(f"[Phải có đúng 1 thẻ H1, đang có {n_h1}] {f}")

    c = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not c:
        L(f"[Thiếu canonical] {f}")
    else:
        can = c.group(1)
        if HOST in can and not can.endswith("/"):
            # ĐÃ TỪNG DÍNH: canonical thiếu dấu / cuối → Google báo "chuyển hướng/chưa index"
            L(f"[Canonical thiếu dấu / cuối] {f}: {can}")
        if HOST not in can and not f.startswith(CANONICAL_NGOAI_OK):
            L(f"[Trang giao dịch KHÔNG được canonical sang web khác] {f}: {can}")
        if HOST not in can and f.startswith(CANONICAL_NGOAI_OK):
            # ĐÃ TỪNG DÍNH (nặng): 2 HUB (thi-truong/, ve-nam-ban/ — 217 link vào mỗi hub)
            # và 6 bài giao dịch canonical sang TRANG CHỦ Panorama / trang khác chủ đề.
            # Hiến pháp §6.3: canonical ngoài CHỈ khi hai trang cùng intent trùng thật.
            # Hub không bao giờ là bản trùng của một trang khác; đích là index/trang chủ
            # thì chắc chắn không cùng intent với một bài cụ thể.
            la_hub = f.count("/") == 1
            dich_index = can.rstrip("/").endswith(("namban-index", "nambanpanorama.com", "/index"))
            if la_hub:
                L(f"[HUB không được canonical sang web khác — hub không phải bản trùng] {f}: {can}")
            elif dich_index:
                L(f"[Canonical ngoài trỏ trang chủ/index — không cùng intent] {f}: {can}")
for k, v in titles.items():
    if len(v) > 1: L(f"[Trùng <title>] {k[:55]}… → {[x for x in v]}")
for k, v in descs.items():
    if len(v) > 1: L(f"[Trùng description] {k[:55]}… → {[x for x in v]}")

# ── 3. Ảnh: alt, ưu tiên tải đúng (Core Web Vitals) ───────────────────────
# ĐÃ TỪNG DÍNH: gán fetchpriority cho LOGO và loading=lazy cho ẢNH HERO → chậm LCP.
for f, s in data.items():
    tags = re.findall(r"<img\b[^>]*>", s)
    for tg in tags:
        if "alt=" not in tg:
            L(f"[Ảnh thiếu alt] {f}: {tg[:70]}")
        if ("logo.png" in tg or "favicon" in tg) and "fetchpriority" in tg:
            L(f"[Logo không được fetchpriority=high] {f}")
    noi_dung = [t for t in tags if "logo.png" not in t and "favicon" not in t]
    if noi_dung and 'loading="lazy"' in noi_dung[0]:
        # Chỉ là ẢNH HERO khi nó nằm trên màn hình đầu. Trang chữ nhiều (ví dụ
        # /cho-thue/) có ảnh đầu tiên nằm sau cả nghìn chữ — ảnh đó KHÔNG phải LCP,
        # ép nó tải sớm mới là hại. Đo bằng lượng chữ thật đứng trước ảnh.
        than = s.split("<body", 1)[-1]
        truoc = than.split(noi_dung[0], 1)[0]
        chu = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", truoc)).strip())
        if chu < 900:
            L(f"[Ảnh hero KHÔNG được loading=lazy — hại LCP] {f}")

# ── 3b. srcset: file phải có thật, preload phải khớp, gallery phải xoá srcset ──
# ĐÃ SUÝT DÍNH 3 lần khi làm srcset:
#  1) sinh bản nhỏ đúng bằng width khai báo (700px) → điện thoại cần 780px nên
#     trình duyệt vẫn chọn bản GỐC, làm xong mà không giảm được byte nào.
#  2) gán chung sizes 1130px cho mọi hero → 14 ảnh CARD rộng 400px sẽ tải bản to.
#  3) swapMain gán .src mà không xoá srcset → bấm thumbnail hiện SAI ảnh.
for f, s in data.items():
    for ss in re.findall(r'srcset="([^"]+)"', s):
        for phan in ss.split(","):
            p = phan.strip().split()[0]
            if p.startswith("/images") and not os.path.exists(p.lstrip("/")):
                L(f"[srcset trỏ file không tồn tại] {f} → {p}")
    hero = re.search(r'<img\b[^>]*fetchpriority="high"[^>]*>', s)
    if hero and "srcset=" in hero.group(0):
        pl = re.search(r'<link rel="preload" as="image"[^>]*>', s)
        if pl:
            a = re.search(r'imagesrcset="([^"]+)"', pl.group(0))
            b = re.search(r'srcset="([^"]+)"', hero.group(0))
            if not a or a.group(1) != b.group(1):
                L(f"[preload không khớp srcset — trình duyệt tải 2 ảnh] {f}")
    if "function swapMain" in s and 'removeAttribute("srcset")' not in s:
        L(f"[swapMain không xoá srcset — bấm thumbnail sẽ hiện sai ảnh] {f}")

# ── 4. Liên kết nội bộ không được gãy ─────────────────────────────────────
# ĐÃ TỪNG DÍNH: 2 trang trỏ tới /dat-nam-ban-tren-2-ty/ khi trang chưa tồn tại.
BO_QUA = ("/images/", "/css/", "/js/")
DUOI_FILE = (".xml", ".txt", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp", ".pdf",
             ".webmanifest", ".json")
for f, s in data.items():
    for h in set(re.findall(r'href="(/[^"#?]*)"', s)):
        if h.startswith(BO_QUA):
            continue
        if h.endswith(DUOI_FILE):
            # Trỏ tới một FILE thật (favicon, manifest, sitemap…) — kiểm luôn
            # file đó có trên đĩa không, thay vì bỏ qua. Gõ sai tên file thì
            # trình duyệt im lặng bỏ icon, không ai biết.
            if not os.path.exists(h.lstrip("/")):
                L(f"[File không tồn tại] {f} → {h}")
            continue
        h2 = h if h.endswith("/") else h + "/"
        if h2 not in tap_trang and h2 not in nguon_redirect:
            L(f"[Link nội bộ gãy] {f} → {h}")

# ── 4b. Link TƯƠNG ĐỐI phải resolve đúng file trên đĩa ────────────────────
# ĐÃ TỪNG DÍNH: 3 trang nhà dùng src="../images/..." ở trang chi tiết (sâu 2 cấp)
# → thực tế trỏ /nha-ban/images/... KHÔNG tồn tại, ảnh/CSS/JS chết. Check 4 chỉ
# soi link tuyệt đối (bắt đầu bằng /) nên mù với link tương đối → thêm lớp này.
# (../../images/ ở related-card sang tin khác vẫn ĐÚNG vì về đúng gốc — không báo.)
BO_QUA_REL = ("http://", "https://", "//", "mailto:", "tel:", "sms:", "#", "data:", "javascript:")
for f, s in data.items():
    thu_muc = os.path.dirname(f)
    s_hien = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S)  # bỏ JS dựng chuỗi
    for val in set(re.findall(r'(?:src|href)="([^"]+)"', s_hien)):
        if val.startswith("/") or val.lower().startswith(BO_QUA_REL) or "zalo.me" in val.lower():
            continue
        clean = val.split("#")[0].split("?")[0]
        if not clean:
            continue
        dich = os.path.normpath(os.path.join(thu_muc, clean))
        if os.path.isfile(dich):
            continue
        if "." not in clean.split("/")[-1] and os.path.isfile(os.path.join(dich, "index.html")):
            continue
        L(f"[Link tương đối gãy — trỏ file không tồn tại] {f} → {val}")

# ── 5. Không trang nào được mồ côi ────────────────────────────────────────
# ĐÃ TỪNG DÍNH: /hoi-dap/ (tài sản AEO tốt nhất) 0 inbound; sau đó 2 trang thi-truong.
inbound = Counter()
for f, s in data.items():
    me = duong_dan(f)
    for h in set(re.findall(r'href="(/[^"#?]*)"', s)):
        h2 = h if h.endswith("/") else h + "/"
        if h2 != me: inbound[h2] += 1
for p in sorted(tap_trang):
    if inbound[p] == 0:
        L(f"[Trang mồ côi — 0 link trỏ tới] {p}")

# ── 6. Sitemap khớp đúng tập trang ────────────────────────────────────────
for p in sorted(tap_trang - sm_paths): L(f"[Thiếu trong sitemap.xml] {p}")
for p in sorted(sm_paths - tap_trang): L(f"[Sitemap trỏ trang không tồn tại] {p}")
for u in sm_urls:
    if not u.endswith("/"): L(f"[URL sitemap thiếu dấu / cuối] {u}")

# ── 6b. Ảnh: phải có trong sitemap ảnh + khai báo đủ trong schema ─────────
# ĐÃ TỪNG DÍNH: sitemap.xml không hề có <image:image> → Google Images không
# biết 1.000+ ảnh của site; và 77 tin chỉ khai 1 ảnh trong Product schema.
sm_imgs = set(re.findall(r"<image:loc>([^<]+)</image:loc>", sitemap))
for f in pages:
    s_ = open(f, encoding="utf-8").read()
    slug = os.path.basename(os.path.dirname(f))
    thu_muc = os.path.join("images/listings", slug)
    if not os.path.isdir(thu_muc):
        continue
    trong_trang = []
    for src in re.findall(r'<img[^>]+src="([^"]+)"', s_):
        ten = src.split("/")[-1]
        if f"/images/listings/{slug}/" in src and os.path.exists(os.path.join(thu_muc, ten)):
            u = f"{HOST}/images/listings/{slug}/{ten}"
            if u not in trong_trang:
                trong_trang.append(u)
    for u in trong_trang:
        if u not in sm_imgs:
            L(f"[Ảnh thiếu trong sitemap] {u} — chạy python3 scripts/sitemap-anh.py")
            break
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s_, re.S):
        try:
            obj = json.loads(b)
        except Exception:
            continue
        for x in cac_node(obj):
            if x.get("@type") == "Product":
                im = x.get("image")
                im = [im] if isinstance(im, str) else (im or [])
                if len(im) < len(trong_trang):
                    L(f"[Product schema thiếu ảnh] {duong_dan(f)} — có {len(trong_trang)} ảnh, khai {len(im)}")

# ── 6c. Ảnh mới phải có bản .webp nếu webp nhẹ hơn ────────────────────────
# Chạy: python3 scripts/tao-webp.py  (giữ nguyên .jpg cũ, chỉ thêm .webp)
for f in pages:
    for src in re.findall(r'<img[^>]+src="([^"]+\.jpg)"', open(f, encoding="utf-8").read()):
        rel = src.lstrip("./").lstrip("/")
        if os.path.exists(rel) and os.path.exists(rel[:-4] + ".webp"):
            W(f"[Còn dùng .jpg dù đã có .webp nhẹ hơn] {src} — {duong_dan(f)}")

# ── 6d. Số đếm hiển thị & ItemList phải khớp số thẻ thật ──────────────────
# ĐÃ TỪNG DÍNH: hub ghi "96 tin" khi có 96 thẻ nhưng ItemList khai 99 — 3 lô có
# trang sống mà không có thẻ nào trên hub, khách duyệt không bao giờ thấy.
# Trang Nhà Bán thì ghi 25 trong khi có 26 thẻ.
for hub in ("dat-nen-nam-ban/index.html", "nha-ban-nam-ban/index.html"):
    if not os.path.exists(hub):
        continue
    s_ = open(hub, encoding="utf-8").read()
    the = re.findall(r'<h3 class="sp-title"><a href="([^"]+)"', s_)
    # Dòng "Hiển thị N" nói về lô ĐANG BÁN — đúng bằng số thẻ trừ thẻ data-ban="1".
    # ĐÃ TỪNG DÍNH: dòng này ghi tổng số thẻ (gồm cả lô đã bán) trong khi nút lọc
    # ghi số đang bán, nên bấm nút là số nhảy, người dùng tưởng lọc không chạy.
    da_ban = len(re.findall(r'<article class="prop-card sp-row"[^>]*data-ban="1"', s_))
    dang = len(the) - da_ban
    m = re.search(r"Hiển thị <strong[^>]*>(\d+)</strong>", s_)
    if m and int(m.group(1)) != dang:
        L(f"[Số đếm sai] {hub} ghi {m.group(1)} nhưng có {dang} lô đang bán "
          f"({len(the)} thẻ - {da_ban} đã bán)")
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s_, re.S):
        try:
            d = json.loads(b)
        except Exception:
            continue
        il = [x for x in cac_node(d) if x.get("@type") == "ItemList"]
        if not il:
            continue
        d = il[0]
        u = [x["url"].replace(HOST, "") for x in d.get("itemListElement", [])]
        for x in u:
            if x not in the:
                L(f"[ItemList thừa] {hub} khai {x} nhưng hub không có thẻ nào")
        for x in the:
            if x not in u:
                L(f"[ItemList thiếu] {hub} có thẻ {x} nhưng ItemList không khai")
        if d.get("numberOfItems") != len(u):
            L(f"[numberOfItems sai] {hub}: khai {d.get('numberOfItems')}, thật {len(u)}")

# ── 6e. Trọng lượng trang lúc mở: chỉ 1 ảnh ưu tiên, phần còn lại phải lazy ──
# ĐÃ TỪNG DÍNH NẶNG: hub Nhà Bán gắn fetchpriority="high" cho 17 ảnh -> trình duyệt
# kéo 3MB TRƯỚC khi hiện chữ. Đo mới ra, nhìn code không thấy.
for f in pages:
    s_ = open(f, encoding="utf-8").read()
    the = re.findall(r"<img\b[^>]*>", s_)
    uu_tien = [t for t in the if "fetchpriority" in t and "logo" not in t]
    if len(uu_tien) > 1:
        L(f"[{len(uu_tien)} ảnh cùng fetchpriority — chỉ được 1] {duong_dan(f)}")
    nang = 0
    for t in the:
        if 'loading="lazy"' in t or "logo" in t:
            continue
        m = re.search(r'src="([^"]+)"', t)
        if not m:
            continue
        rel = m.group(1).lstrip("./").lstrip("/")
        if os.path.exists(rel):
            nang += os.path.getsize(rel)
    if nang > 900 * 1024:
        L(f"[Trang nặng {nang//1024}KB ảnh lúc mở — thêm loading=lazy] {duong_dan(f)}")
    elif nang > 500 * 1024:
        W(f"[Trang tải ngay {nang//1024}KB ảnh — nên bớt] {duong_dan(f)}")

# ── 6f. Hiến pháp 3 web: Villas KHÔNG được link sang Panorama ───────────────
# docs/HIEN-PHAP-3-WEB.md điều 1: Panorama đứng độc lập, Villas/Greenspace không
# link sang. Canonical thì ĐƯỢC (điều 3, khi cùng intent) — chỉ cấm thẻ <a>.
for f in pages:
    s_ = open(f, encoding="utf-8").read()
    if re.search(r'<a [^>]*href="https?://[^"]*nambanpanorama', s_):
        L(f"[Link sang Panorama — hiến pháp 3 web cấm] {duong_dan(f)}")

# ── 6g. Giao diện điện thoại: những thứ đã từng sai ────────────────────────
for f in pages:
    s_ = open(f, encoding="utf-8").read()
    if 'name="viewport"' not in s_:
        L(f"[Thiếu thẻ viewport — vỡ hoàn toàn trên điện thoại] {duong_dan(f)}")
    if "user-scalable=no" in s_ or "maximum-scale=1" in s_:
        L(f"[Chặn phóng to — hại người mắt kém, Google trừ điểm] {duong_dan(f)}")
    if 'class="mobile-nav"' not in s_:
        L(f"[Thiếu nút Gọi/Zalo nổi trên điện thoại] {duong_dan(f)}")
    # Ảnh thiếu width/height gây nhảy layout (CLS) — trừ ảnh lightbox do JS đổ vào
    for t in re.findall(r"<img\b[^>]*>", s_):
        if "lbImg" in t or "width=" in t:
            continue
        L(f"[Ảnh thiếu width/height — gây nhảy layout] {duong_dan(f)}")
        break

# ── 6h. Nhãn nhanh ở hub: số trên nút phải khớp số lô thật ─────────────────
hub_nhan = "dat-nen-nam-ban/index.html"
if os.path.exists(hub_nhan):
    s_ = open(hub_nhan, encoding="utf-8").read()
    # ĐÃ BÁN = thẻ có data-ban="1" (badge nền đỏ + chữ đúng "Đã bán", hoặc
    # dòng giá ghi "Đã bán"). ĐÃ TỪNG SAI: bắt chuỗi "Đã bán" ở bất cứ đâu trong
    # thẻ, nên loại nhầm cụm ghi "Đã bán 8 · còn 10 nền" — cụm đó VẪN ĐANG BÁN.
    dem = Counter()
    for at, bd in re.findall(r'<article class="prop-card sp-row"([^>]*)>([\s\S]*?)</article>', s_):
        if 'data-ban="1"' in at:
            continue
        m = re.search(r'data-nhan="([^"]*)"', at)
        for x in (m.group(1).split() if m else []):
            dem[x] += 1
    dem_loc = Counter()
    dang_ban = 0
    for blk in re.findall(r'<article class="prop-card sp-row"([^>]*)>([\s\S]*?)</article>', s_):
        if 'data-ban="1"' in blk[0]:
            continue
        dang_ban += 1
        m = re.search(r'data-loc="([^"]*)"', blk[0])
        for x in (m.group(1).split() if m else []):
            dem_loc[x] += 1
    for val, so in re.findall(r'class="lc-chip[^"]*" data-nhan="([^"]*)"[^>]*>[^<]*<b>(\d+)</b>', s_):
        that = dang_ban if val == "" else dem[val]
        if int(so) != that:
            L(f"[Nút nhu cầu '{val or 'tất cả'}' ghi {so} lô nhưng thật {that}] /dat-nen-nam-ban/")
    for val, so in re.findall(r'class="lc-chip[^"]*" data-loc="([^"]*)"[^>]*>[^<]*<b>(\d+)</b>', s_):
        that = dang_ban if val == "" else dem_loc[val]
        if int(so) != that:
            L(f"[Nút khu '{val or 'tất cả'}' ghi {so} lô nhưng thật {that}] /dat-nen-nam-ban/")
    # lô đã bán không được mang nhãn — khách bấm vào thấy hàng chết
    for blk in re.findall(r'<article class="prop-card sp-row" data-nhan[^>]*>[\s\S]*?</article>', s_):
        if "Đã bán" in blk:
            L("[Lô đã bán vẫn mang nhãn nhanh] /dat-nen-nam-ban/")
            break

# ── 7. vercel.json: redirect PHẢI có biến thể dấu / cuối ──────────────────
# ĐÃ TỪNG DÍNH NẶNG: trailingSlash:true chuẩn hoá thêm '/' TRƯỚC khi khớp redirect,
# mà mọi source đều thiếu '/' → toàn bộ 36 redirect trả 404, mất sạch link cũ.
if vercel.get("trailingSlash") is True:
    co_slash = {r["source"] for r in redirects if r["source"].endswith("/")}
    for r in redirects:
        src = r["source"]
        if ":" in src:  # wildcard
            continue
        if not src.endswith("/") and (src + "/") not in co_slash:
            L(f"[Redirect sẽ trả 404 — thiếu biến thể có dấu / cuối] {src}")
for r in redirects:
    d = r["destination"]
    if d.startswith("http") or ":" in d:
        continue
    dd = d if d.endswith("/") else d + "/"
    if dd not in tap_trang and dd not in nguon_redirect:
        L(f"[Redirect trỏ tới trang không tồn tại] {r['source']} → {d}")

# ── 8. Giọng thương hiệu: không emoji, không ngôi thứ nhất ────────────────
NGOI_1 = re.compile(r"\b(mình|tôi|chúng tôi|chúng mình|chúng em)\b|(?<!trẻ )\bem\b")
EMOJI = re.compile(r"[\U0001F000-\U0001FAFF\U00002B00-\U00002BFF]")

# ĐÃ TỪNG DÍNH (nặng): "Nếu chú là người Hà Nội đang tìm về", "cháu gửi ngay",
# "Cháu đang sống tại đây" — 11 chỗ lọt ra trang công khai.
# "chú/cháu" là cách xưng hô RIÊNG giữa chủ web và trợ lý trong lúc trao đổi.
# Web nói với KHÁCH LẠ: chủ thể là "Nam Ban Villas", khách là "bạn" hoặc "anh/chị".
# Loại trừ: ghi chú · chú ý · chú trọng · chú thích · con cháu · chú rể.
XUNG_HO_RIENG = re.compile(
    r"(?<!ghi )(?<!Ghi )(?<!con )(?<!Con )\b[CcHh]?(chú|cháu|Chú|Cháu)\b"
    r"(?!\s*(ý|Ý|trọng|thích|rể))")

# ĐÃ TỪNG DÍNH: "Bé phân tích 5 thay đổi lớn nhất", "Bé hỗ trợ kiểm tra quy
# hoạch" — cùng loại lỗi với chú/cháu: trợ lý tự xưng trên trang công khai.
# Chỉ bắt "Bé" đứng đầu mệnh đề + theo sau là ĐỘNG TỪ, để không đụng tên riêng
# kiểu "Nhà hàng Minh Bé".
XUNG_HO_BE = re.compile(r"(?:^|[.!?;]\s|\A)\s*Bé\s+(?=[a-zàâăđêôơư])")

for f, s in data.items():
    if EMOJI.search(s):
        L(f"[Có emoji — luật thương hiệu cấm] {f}")
    # Bẫy này chạy trên MỌI trang, kể cả tuỳ bút — không có ngoại lệ.
    than_ch = s[s.find("<body"):]
    than_ch = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", than_ch, flags=re.S)
    than_ch = re.sub(r"<!--.*?-->", "", than_ch, flags=re.S)
    chu_ch = re.sub(r"<[^>]+>", " ", than_ch)
    for m in XUNG_HO_RIENG.finditer(chu_ch):
        doan = re.sub(r"\s+", " ", chu_ch[max(0, m.start()-45):m.end()+45]).strip()
        L(f"[Xưng hô chú/cháu — web phải viết \"Nam Ban Villas\"] {f}: …{doan}…")
    for m in XUNG_HO_BE.finditer(chu_ch):
        doan = re.sub(r"\s+", " ", chu_ch[m.start():m.end()+60]).strip()
        L(f"[Trợ lý tự xưng \"Bé\" — web phải viết \"Nam Ban Villas\"] {f}: …{doan}…")
    if any(k in f for k in TUY_BUT) or f in MIEN_TRU_NGOI_1:
        continue  # cố ý ngôi thứ nhất, đã duyệt
    than = s[s.find("<body"):]
    than = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", than, flags=re.S)
    chu = re.sub(r"<[^>]+>", " ", than)
    for m in NGOI_1.finditer(chu):
        doan = re.sub(r"\s+", " ", chu[max(0, m.start()-45):m.end()+45]).strip()
        W(f"[Ngôi thứ nhất — đổi sang \"Nam Ban Villas\"] {f}: …{doan}…")

# ── 9. Trang tin rao (lô/nhà): schema + có mặt trong hub ──────────────────
# ĐÃ TỪNG DÍNH: hub thiếu 13 lô trong ItemList; breadcrumb trỏ /dat-nen/ (404).
HUB = {"dat-nen": "dat-nen-nam-ban/index.html", "nha-ban": "nha-ban-nam-ban/index.html"}
hub_urls = {}
for kind, hf in HUB.items():
    s = data.get(hf, "")
    hub_urls[kind] = set(re.findall(r'"url":"' + HOST + r'(/[^"]+/)"', s))
for f, s in data.items():
    kind = f.split("/")[0]
    if kind not in HUB:
        continue
    url = duong_dan(f)
    co_product = False
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            if any(x.get("@type") == "Product" for x in cac_node(json.loads(b))):
                co_product = True
                break
        except Exception:
            pass
    if not co_product:
        L(f"[Tin rao thiếu schema Product] {f}")
    # Lô "giá đang cập nhật" không có Offer là ĐÚNG; chỉ bắt khi có Offer mà thiếu đơn vị tiền
    if '"offers"' in s and '"priceCurrency":"VND"' not in s:
        L(f"[Có Offer nhưng thiếu priceCurrency VND] {f}")
    if "FAQPage" not in s:
        W(f"[Tin rao nên có FAQPage (AEO)] {f}")

    if url not in hub_urls[kind]:
        L(f"[Chưa thêm vào ItemList của hub {HUB[kind]}] {url}")
    if f'"item":"{HOST}/{kind}/"' in s:
        L(f"[Breadcrumb trỏ /{kind}/ (404) — phải trỏ hub thật] {f}")
    og = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    if og and "og-namban.jpg" in og.group(1):
        W(f"[og:image dùng ảnh chung — nên dùng ảnh của chính lô] {f}")


# ── FAQ schema PHẢI hiện trên trang ─────────────────────────────────────────
# ĐÃ TỪNG DÍNH (nặng): 174/194 trang có FAQPage trong schema nhưng KHÔNG có câu
# hỏi nào hiện ra cho khách đọc. Google yêu cầu nội dung structured data phải
# nhìn thấy được — vi phạm là mất rich result, nặng thì bị phạt thủ công.
for f, s in data.items():
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            j = json.loads(b)
        except Exception:
            continue
        for n in cac_node(j):
            if n.get("@type") != "FAQPage":
                continue
            than = re.sub(r"<script.*?</script>", "", s, flags=re.S)
            chu = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", than))
            an = [q.get("name", "") for q in n.get("mainEntity", [])
                  if q.get("name", "")[:40] not in chu]
            if an:
                L(f"[FAQ schema có {len(an)} câu KHÔNG hiện trên trang — Google phạt] {f}: {an[0][:50]}")
# ── 10. GEO ───────────────────────────────────────────────────────────────
for f, s in data.items():
    g = re.search(r'<meta name="geo.region" content="([^"]+)"', s)
    if g and g.group(1) != "VN-35":
        L(f"[geo.region phải là VN-35] {f}: {g.group(1)}")

# ── 11. Lô ĐÃ BÁN phải còn nguyên trên trang khu ──────────────────────────
# LUẬT CHỦ ĐẶT: lô/cụm/nhà đã bán KHÔNG BAO GIỜ GỠ — luôn để lại, chỉ mang nhãn
# "Đã bán". Đó là bằng chứng giao dịch thật và là mốc giá để khách tự định giá
# lô đang xem. ĐÃ TỪNG DÍNH: 4 lô đã bán bị gỡ khỏi 3 trang khu khi đổ đủ lô.
KHU_TRANG = {
    "dong-thanh": "dat-dong-thanh-nam-ban", "me-linh": "dat-me-linh-nam-ban",
    "gia-lam": "dat-gia-lam-nam-ban", "tu-liem": "dat-tu-liem-nam-ban",
    "ho-bai-cong": "dat-ho-bai-cong-nam-ban", "nam-ban": "dat-trung-tam-thi-tran-nam-ban",
}
# Chủ đã xác nhận khu cho mọi lô (23/9/2026). Giữ tập rỗng để sau này có lô
# treo thì bỏ vào đây thay vì tắt cả bẫy.
CHUA_XAC_NHAN_KHU = set()
_ban = {}
for _f in ("dat-nen-nam-ban/index.html", "nha-ban-nam-ban/index.html"):
    _s = data.get(_f, "")
    for _m in re.finditer(r'<article class="prop-card sp-row[^"]*"([^>]*)>(.*?)</article>',
                          _s, flags=re.S):
        if 'data-ban="1"' not in _m.group(1):
            continue
        _u = re.search(r'href="(/(?:dat-nen|nha-ban)/[a-z0-9-]+/)"', _m.group(2))
        _l = re.search(r'data-loc="([^"]*)"', _m.group(1))
        if _u and _l:
            _ban[_u.group(1)] = _l.group(1).split()
# Phải tìm trong LƯỚI THẺ, không tìm cả trang: URL còn nằm trong ItemList thì
# vẫn "có" trong file dù thẻ đã bị gỡ khỏi mắt khách.
_the_khu = {}
for _t in set(KHU_TRANG.values()):
    _s = data.get(_t + "/index.html", "")
    _the_khu[_t] = set(re.findall(
        r'<article class="prop-card[^>]*>.*?href="(/(?:dat-nen|nha-ban)/[a-z0-9-]+/)"',
        _s, flags=re.S))
for _u, _locs in _ban.items():
    if _u in CHUA_XAC_NHAN_KHU:
        continue
    for _k in _locs:
        _t = KHU_TRANG.get(_k)
        if _t and (_t + "/index.html") in data and _u not in _the_khu[_t]:
            L(f"[Lô ĐÃ BÁN bị gỡ khỏi trang khu — luật: luôn để lại, chỉ ghi Đã bán] "
              f"/{_t}/ thiếu {_u}")

# ── 12. CSS thẻ lô phải nằm ở style.css, không inline ─────────────────────
# ĐÃ TỪNG DÍNH (nặng, khách chụp màn hình báo "sao xấu dữ"): toàn bộ layout
# .sp-sang chỉ nằm INLINE trong 3 trang; 12 trang khác dùng đúng loại thẻ đó mà
# không có CSS -> ~250 thẻ vỡ hẳn trên điện thoại. Nay CSS ở css/style.css.
_css = open("css/style.css", encoding="utf-8").read()
for _k in (".sp-sang .sp-row{", ".sp-sang .sp-thumb{", ".sp-sang .sp-chips span{",
           ".sp-sang .sp-right{", ".sp-sang .sp-price{", ".sp-sang .sp-mid{"):
    if _k not in _css:
        L(f"[CSS thẻ lô biến mất khỏi style.css — mọi trang khu sẽ vỡ] thiếu {_k}")
for _f, _s in data.items():
    if "prop-grid sp-sang" not in _s:
        continue
    if "css/style.css" not in _s:
        L(f"[Trang dùng thẻ .sp-sang nhưng KHÔNG nạp style.css] {_f}")
    if ".sp-sang .sp-thumb{" in _s:
        L(f"[CSS thẻ lô lại bị chép inline — sẽ lệch với style.css] {_f}")

# ── 13. CSS/JS phải đóng dấu phiên bản đúng ───────────────────────────────
# ĐÃ TỪNG DÍNH (chủ chụp màn hình 2 lần, lần 2 y hệt lần 1): vercel.json cache
# /css/* 24 tiếng + stale 7 ngày, tên file không đổi -> sửa CSS xong đẩy lên mà
# khách cũ vẫn thấy bản CŨ, kéo-xuống-refresh cũng không ăn thua.
# Chữa bằng ?v=<vân tay nội dung>. Bẫy này bắt khi quên chạy lại script.
import hashlib as _hl
_ts = {}
for _p in ("css/style.css", "css/article.css", "js/main.js"):
    if os.path.exists(_p):
        _ts[_p] = _hl.sha1(open(_p, "rb").read()).hexdigest()[:8]
_re_ts = re.compile(r'(?:href|src)="((?:\.\./)*/?(?:css/(?:style|article)\.css|js/main\.js))(\?v=([0-9a-f]+))?"')
for _f, _s in data.items():
    for _m in _re_ts.finditer(_s):
        _ten = re.sub(r"^(?:\.\./)*/?", "", _m.group(1))
        if _ten not in _ts:
            continue
        if not _m.group(2):
            L(f"[CSS/JS thiếu ?v= — khách cũ sẽ thấy bản cũ tới 24h] {_f}: {_m.group(1)}"
              " — chạy python3 scripts/dat-phien-ban-css.py")
        elif _m.group(3) != _ts[_ten]:
            L(f"[?v= cũ, không khớp nội dung file] {_f}: {_ten} ?v={_m.group(3)}"
              f" nhưng file đang là {_ts[_ten]} — chạy python3 scripts/dat-phien-ban-css.py")

# ── 14. Bậc tiêu đề không được nhảy cóc ───────────────────────────────────
# ĐÃ TỪNG DÍNH: 208/219 trang nhảy h2 -> h4 vì tiêu đề chân trang và thanh bên
# để h4. Trình đọc màn hình và bộ trích dẫn của AI đọc trang theo cây tiêu đề,
# nhảy bậc là cây gãy.
for _f, _s in data.items():
    _b = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", _s, flags=re.S)
    _t = 0
    for _m in re.finditer(r"<h([1-6])\b", _b):
        _h = int(_m.group(1))
        if _t and _h > _t + 1:
            L(f"[Bậc tiêu đề nhảy cóc h{_t}->h{_h} — hại AEO & trình đọc màn hình] {_f}")
            break
        _t = _h

# ── 15. Gọi luôn máy kiểm nút bấm & bộ lọc ────────────────────────────────
# Một lệnh kiểm hết, để không bao giờ "quên chạy cái kia".
import subprocess as _sp
_kq = _sp.run([sys.executable, "scripts/kiem-bo-loc.py"], capture_output=True, text=True)
if _kq.returncode != 0:
    for _d in _kq.stdout.splitlines():
        if _d.startswith("  X "):
            L("[Bộ lọc] " + _d[4:])

# ── 16. preload ảnh phải trỏ ĐÚNG ảnh LCP (fetchpriority=high) ─────────────
# ĐÃ TỪNG DÍNH (cwv-7): hub thêm tin mới lên đầu nhưng preload vẫn trỏ ảnh của
# thẻ đầu CŨ -> tải ưu tiên cao một ảnh không phải LCP, làm chậm chính ảnh LCP.
for _f, _s in data.items():
    _b = _s[_s.find("<body"):]
    _hi = re.search(r'<img\b[^>]*fetchpriority="high"[^>]*>', _b)
    _pl = re.search(r'<link rel="preload" as="image"[^>]*href="([^"]+)"', _s)
    if not _hi or not _pl:
        continue
    _src = re.search(r'src="([^"]+)"', _hi.group(0))
    if _src and _src.group(1) != _pl.group(1):
        L(f"[preload trỏ {_pl.group(1)[-40:]} nhưng ảnh LCP là {_src.group(1)[-40:]}] {_f}")

# ── 18. LUẬT CHỦ WEB: "Lâm Hà" luôn có "Nam Ban" ngay bên cạnh ─────────────
# (24/9/2026) Lâm Hà đứng một mình kéo Google/AI hiểu sang cả vùng rộng, loãng thực
# thể Nam Ban. Sửa: python3 scripts/lam-ha-kem-nam-ban.py (tất định, chạy lại được).
_kq = _sp.run([sys.executable, "scripts/lam-ha-kem-nam-ban.py", "--kiem"], capture_output=True, text=True)
if _kq.returncode != 0:
    for _d in _kq.stdout.splitlines():
        if _d.startswith("  "):
            L("[Lâm Hà thiếu Nam Ban bên cạnh — chạy python3 scripts/lam-ha-kem-nam-ban.py]" + _d)

# ── 19. Trang đang có thứ hạng: title + H1 do script sinh chỉ được đổi theo THÁNG ──
# (24/9/2026) Chủ web: "đang top search, làm lung tung là tụt". Script tuần từng đưa ngày
# (24/9/2026) và số lô vào title/H1 -> đổi mỗi tuần. Số tuần chỉ được nằm ở mô tả/thân trang.
for _f in ("thi-truong/gia-dat-nam-ban-hom-nay/index.html", "gia-dat-lam-ha/index.html", "dat-nam-ban-gia-re/index.html"):
    if not os.path.exists(_f):
        continue
    _s = open(_f, encoding="utf-8").read()
    for _tag, _p in (("title", r"<title>(.*?)</title>"), ("H1", r"<h1[^>]*>(.*?)</h1>")):
        _m = re.search(_p, _s, re.S)
        if _m and (re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", _m.group(1)) or re.search(r"\d+\s+Lô", _m.group(1))):
            L("[%s đổi theo tuần (có ngày hoặc số lô) — chỉ được đổi theo tháng] %s" % (_tag, _f))

# ── 20. GIỌNG ĐỘI NGŨ: khách không bao giờ đọc thấy "script / tự động / bot / AI / nhập tay" ──
# (24/9/2026) Chủ web: web do ĐỘI NGŨ Nam Ban Villas làm. Từng lọt "Mỗi thứ Hai, script của Nam Ban
# Villas…", "(tự động mỗi thứ Hai)", "Không có số nhập tay". Viết: "đội ngũ Nam Ban Villas tổng hợp…".
# Ngoại lệ duy nhất: "béc tưới tự động" (tiện ích thật của lô). Soi thân trang + title + meta + alt + JSON-LD.
import html as _html
_CAM = re.compile(r"(?<![A-Za-zÀ-ỹ])(AI|A\.I\.|[Ss]cripts?|[Bb]ots?|[Aa]uto|chatbot|Routine)(?![A-Za-zÀ-ỹ])|[Tt]ự [Đđ]ộng|nhập tay|thuật toán")
def _thay_duoc(_s):
    _s = re.sub(r"<!--[\s\S]*?-->", "", _s)
    _ld = " ".join(re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', _s))
    _mt = " ".join(re.findall(r"<title>([^<]*)", _s) + re.findall(r'<meta [^>]*content="([^"]*)"', _s)
                   + re.findall(r'(?:alt|title|aria-label)="([^"]*)"', _s))
    _b = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[\s\S]*?</\1>", "", _s))
    return _html.unescape(_b + " " + _mt + " " + _ld)
for _f, _s in list(data.items()) + [("llms.txt", open("llms.txt", encoding="utf-8").read())]:
    _t = _thay_duoc(_s) if _f.endswith(".html") else _s
    for _m in _CAM.finditer(_t):
        _c = _t[max(0, _m.start() - 40):_m.end() + 30]
        if "béc tưới" in _c:
            continue
        L("[Lộ chữ máy móc '%s' — viết 'đội ngũ Nam Ban Villas'] %s: …%s…" % (_m.group(0), _f, re.sub(r"\s+", " ", _c)))
        break

# ── 21. KHÔNG BAO GIỜ TỰ XOÁ TIN (chủ web chốt 24/9/2026) ────────────────────
# Tin rao theo ngày, bảng giá theo tuần, mục Cập Nhật Thị Trường: số khối trên nhánh này
# KHÔNG được ít hơn trên main. Từng mất bảng giá tuần 2/7/2026 khi làm lại trang.
for _f, _p in (("thi-truong/tin-rao-dat-nam-ban-moi/index.html", r"<!-- DAY:\d{4}-\d{2}-\d{2} -->"),
               ("thi-truong/gia-dat-nam-ban-hom-nay/index.html", r"<!-- WEEK:\d{4}-\d{2}-\d{2} -->"),
               ("thi-truong/index.html", r'<h3 class="mkt-h">')):
    _cu = _sp.run(["git", "show", "origin/main:" + _f], capture_output=True, text=True)
    if _cu.returncode != 0 or not os.path.exists(_f):
        continue          # CI clone nông / chưa có main: bỏ qua, không báo nhầm
    _n_cu = len(re.findall(_p, _cu.stdout))
    _n_moi = len(re.findall(_p, open(_f, encoding="utf-8").read()))
    if _n_moi < _n_cu:
        L("[Mất tin cũ: %d -> %d khối — KHÔNG BAO GIỜ xoá tin có ngày tháng] %s" % (_n_cu, _n_moi, _f))

# ── 17. dateModified trong trang phải == lastmod trong sitemap ─────────────
# ĐÃ TỪNG DÍNH (aeo-8/schema-7): 65 trang lệch hai chiều, 12 bài lệch tới 97
# ngày — hai tín hiệu "mới" tự chọi nhau, Google không tin cái nào.
_lm = {m.group(1): m.group(2) for m in re.finditer(r"<loc>([^<]+)</loc>\s*<lastmod>([\d-]+)</lastmod>", sitemap)}
for _f, _s in data.items():
    _u = HOST + duong_dan(_f)
    _dms = set(re.findall(r'"dateModified":\s*"([\d-]{10})', _s))
    if not _dms or _u not in _lm:
        continue
    if len(_dms) > 1:
        L(f"[Trang có {len(_dms)} dateModified khác nhau] {_f}: {sorted(_dms)}")
    elif _lm[_u] not in _dms:
        L(f"[dateModified {list(_dms)[0]} != sitemap lastmod {_lm[_u]}] {_f}")

# ── kết luận ──────────────────────────────────────────────────────────────
print()
if canh_bao:
    print("CẢNH BÁO (%d) — nên xem, không chặn push:" % len(canh_bao))
    for m in canh_bao[:25]: print("  ! " + m)
    if len(canh_bao) > 25: print("  … còn %d cảnh báo" % (len(canh_bao) - 25))
    print()
if loi:
    print("LỖI (%d) — PHẢI sửa trước khi push:" % len(loi))
    for m in loi[:60]: print("  X " + m)
    if len(loi) > 60: print("  … còn %d lỗi" % (len(loi) - 60))
    print("\nKẾT QUẢ: CHƯA ĐẠT — sửa hết lỗi rồi chạy lại.")
    sys.exit(1)
print("KẾT QUẢ: SẠCH — %d trang, 0 lỗi. Được push." % len(pages))
sys.exit(0)
