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
    else: titles[t.group(1).strip()].append(f)
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
        L(f"[Ảnh hero KHÔNG được loading=lazy — hại LCP] {f}")

# ── 4. Liên kết nội bộ không được gãy ─────────────────────────────────────
# ĐÃ TỪNG DÍNH: 2 trang trỏ tới /dat-nam-ban-tren-2-ty/ khi trang chưa tồn tại.
BO_QUA = ("/images/", "/css/", "/js/")
DUOI_FILE = (".xml", ".txt", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp", ".pdf")
for f, s in data.items():
    for h in set(re.findall(r'href="(/[^"#?]*)"', s)):
        if h.startswith(BO_QUA) or h.endswith(DUOI_FILE):
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
    m = re.search(r"Hiển thị <strong[^>]*>(\d+)</strong>", s_)
    if m and int(m.group(1)) != len(the):
        L(f"[Số đếm sai] {hub} ghi {m.group(1)} tin nhưng có {len(the)} thẻ")
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
for f, s in data.items():
    if EMOJI.search(s):
        L(f"[Có emoji — luật thương hiệu cấm] {f}")
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

# ── 10. GEO ───────────────────────────────────────────────────────────────
for f, s in data.items():
    g = re.search(r'<meta name="geo.region" content="([^"]+)"', s)
    if g and g.group(1) != "VN-35":
        L(f"[geo.region phải là VN-35] {f}: {g.group(1)}")

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
