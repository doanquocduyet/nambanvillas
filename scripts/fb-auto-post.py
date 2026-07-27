#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự đăng tin MỚI lên Facebook Page Nam Ban Villas — hợp lệ 100% (Graph API chính thức).

Cách chạy:
  - Quét sitemap tìm mọi trang tin (/dat-nen/<slug>/ và /nha-ban/<slug>/).
  - Trang nào CHƯA có trong data/fb-posted.json => đăng ảnh + caption lên Page,
    rồi ghi lại vào data/fb-posted.json để không đăng trùng.
  - Mỗi lần chạy đăng tối đa MAX_PER_RUN tin (chống dồn spam).

Bảo mật: KHÔNG đụng nick cá nhân / group. Chỉ đăng đúng Page của token.
Token đọc từ biến môi trường FB_PAGE_TOKEN (lưu trong GitHub Secrets, KHÔNG nằm trong code).

Chế độ seed (chạy 1 lần khi cài đặt):  python scripts/fb-auto-post.py --seed
  -> đánh dấu TẤT CẢ tin hiện có là "đã đăng" mà KHÔNG đăng gì cả,
     để từ nay chỉ tin THÊM MỚI mới tự lên Page.
"""
import os, re, sys, json, time, ssl, pathlib
import urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "fb-posted.json"
SITEMAP = ROOT / "sitemap.xml"
HOTLINE = "0938 227 988"   # Số dùng RIÊNG cho bài đăng Facebook (khác hotline web)
GRAPH = "https://graph.facebook.com/v21.0"
MAX_PER_RUN = 3            # tối đa 3 tin/lần chạy — đăng đều, không dồn
CTX = ssl.create_default_context()
UA = {"User-Agent": "NamBanVillas-FBposter/1.0"}


def listing_urls():
    sm = SITEMAP.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    out = []
    for u in locs:
        if re.search(r"/(dat-nen|nha-ban)/[^/]+/$", u):
            out.append(u.rstrip("/") + "/")
    # giữ thứ tự, bỏ trùng
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u); uniq.append(u)
    return uniq


def url_to_path(u):
    """https://nambanvillas.vn/dat-nen/x/  ->  ROOT/dat-nen/x/index.html"""
    p = urllib.parse.urlparse(u).path.strip("/")
    return ROOT / p / "index.html"


SITE = "https://nambanvillas.vn"


def _clean(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#8211;", "–")
    return re.sub(r"\s+", " ", t).strip()


def extract_specs(html):
    """Rút bảng thông số <table class="specs-table"> -> [(nhãn, giá trị), ...]."""
    m = re.search(r'<table class="specs-table">(.*?)</table>', html, re.S)
    if not m:
        return []
    pairs = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S):
        cells = [_clean(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        cells = [c for c in cells if c != ""]
        # ghép cặp nhãn:giá trị (hàng 4 ô = 2 cặp, hàng 2 ô = 1 cặp)
        for i in range(0, len(cells) - 1, 2):
            pairs.append((cells[i], cells[i + 1]))
    return pairs


def extract_desc(html):
    """Rút đoạn Mô Tả (các <p> giữa 'Mô Tả' và mục kế)."""
    i = html.find("Mô Tả")
    if i == -1:
        return ""
    j = re.search(r"<h[23]", html[i + 5:])
    seg = html[i:i + 5 + (j.start() if j else 4000)]
    ps = [_clean(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", seg, re.S)]
    ps = [p for p in ps if len(p) > 20]
    return "\n\n".join(ps)


def meta_of(u):
    """Bóc tiêu đề, mô tả, thông số, và TẤT CẢ ảnh gallery từ file HTML local."""
    f = url_to_path(u)
    if not f.exists():
        return None
    html = f.read_text(encoding="utf-8", errors="ignore")

    def grab(prop):
        m = re.search(
            r'<meta[^>]+property=["\']' + re.escape(prop) + r'["\'][^>]+content=["\']([^"\']+)["\']',
            html)
        return (m.group(1).strip() if m else "")

    title = grab("og:title")
    og_image = grab("og:image")
    slug = urllib.parse.urlparse(u).path.strip("/").split("/")[-1]
    # tất cả ảnh gallery của tin này (theo đúng thứ tự xuất hiện, bỏ trùng)
    imgs, seen = [], set()
    for rel in re.findall(r'images/listings/' + re.escape(slug) + r'/[^"\')\s]+\.(?:jpg|jpeg|png|webp)', html, re.I):
        full = SITE + "/" + rel
        if full not in seen:
            seen.add(full); imgs.append(full)
    if not imgs and og_image:
        imgs = [og_image]
    if not (title and imgs):
        return None
    return {
        "title": title,
        "desc": grab("og:description"),
        "specs": extract_specs(html),
        "longdesc": extract_desc(html),
        "images": imgs[:10],   # FB album tối đa 10 ảnh
    }


def caption_for(m, url):
    # Giọng Villas: không emoji, thẳng, đăng ĐỦ thông số + mô tả + đường liên hệ.
    parts = [m["title"]]
    if m["specs"]:
        parts.append("\n".join(f"• {k}: {v}" for k, v in m["specs"]))
    body = m["longdesc"] or m["desc"]
    if body:
        parts.append(body)
    parts.append(f"Liên hệ xem đất / gửi ảnh sổ qua Zalo: {HOTLINE}")
    parts.append(f"Chi tiết + hình ảnh đầy đủ: {url}")
    return "\n\n".join(parts)


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"posted": {}}


def save_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def _api(path, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(GRAPH + path, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def post_listing(token, images, caption):
    """1 ảnh -> đăng ảnh kèm caption. Nhiều ảnh -> đăng ALBUM (1 bài, nhiều ảnh)."""
    if len(images) <= 1:
        return _api("/me/photos", {"url": images[0], "caption": caption, "access_token": token})
    # Album: tải từng ảnh ở chế độ chưa đăng, rồi gộp vào 1 bài feed.
    media_ids = []
    for img in images:
        res = _api("/me/photos", {"url": img, "published": "false", "access_token": token})
        if res.get("id"):
            media_ids.append(res["id"])
    if not media_ids:
        raise RuntimeError("không tải được ảnh nào")
    params = {"message": caption, "access_token": token}
    for i, mid in enumerate(media_ids):
        params[f"attached_media[{i}]"] = json.dumps({"media_fbid": mid})
    return _api("/me/feed", params)


def main():
    seed = "--seed" in sys.argv
    st = load_state()
    posted = st.setdefault("posted", {})
    urls = listing_urls()

    todo = [u for u in urls if u not in posted]

    if seed:
        for u in todo:
            posted[u] = {"seeded": True}
        save_state(st)
        print(f"SEED xong: đánh dấu {len(todo)} tin hiện có là đã đăng (không đăng gì).")
        return 0

    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if not token:
        print("THIẾU FB_PAGE_TOKEN — chưa cài chìa khoá Page. Xem docs/fb-auto-setup.md")
        # Không phải lỗi cứng: thoát êm để Action không báo đỏ trước khi chú cài token.
        return 0

    # Đèn chẩn đoán — CHỈ chạy khi cần debug (đặt biến FB_DIAG=1). Ngày thường im lặng,
    # không gọi API thừa. Nếu đăng lỗi thì post_listing đã in rõ nguyên nhân.
    if os.environ.get("FB_DIAG"):
        def _get(path):
            req = urllib.request.Request(
                GRAPH + path + ("&" if "?" in path else "?") +
                urllib.parse.urlencode({"access_token": token}), headers=UA)
            with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
                return json.loads(r.read().decode("utf-8", "ignore"))
        try:
            me = _get("/me?fields=id,name")
            print(f"CHẨN ĐOÁN /me: id={me.get('id')} name={me.get('name')}")
        except Exception as e:
            print("CHẨN ĐOÁN /me lỗi:", str(getattr(e, 'read', lambda: b'')() or e)[:200])
        try:
            dbg = _get(f"/debug_token?input_token={urllib.parse.quote(token)}")
            exp = dbg.get("data", {}).get("expires_at", None)
            if exp == 0:
                print("CHẨN ĐOÁN HẠN TOKEN: VĨNH VIỄN (không hết hạn).")
            elif exp:
                import datetime as _dt
                print("CHẨN ĐOÁN HẠN TOKEN: HẾT HẠN lúc",
                      _dt.datetime.utcfromtimestamp(exp).strftime("%d/%m/%Y %H:%M UTC"))
            else:
                print("CHẨN ĐOÁN HẠN TOKEN: không đọc được ngày hết hạn.")
        except Exception as e:
            print("CHẨN ĐOÁN HẠN TOKEN lỗi:", str(getattr(e, 'read', lambda: b'')() or e)[:150])

    if not todo:
        print("Không có tin mới. Bỏ qua.")
        return 0

    done = 0
    for u in todo[:MAX_PER_RUN]:
        m = meta_of(u)
        if not m:
            print(f"BỎ QUA (thiếu meta): {u}")
            posted[u] = {"skipped": "no-meta"}
            continue
        cap = caption_for(m, u)
        try:
            res = post_listing(token, m["images"], cap)
            posted[u] = {"post_id": res.get("post_id") or res.get("id", "")}
            done += 1
            print(f"ĐĂNG OK ({len(m['images'])} ảnh): {u} -> {posted[u]['post_id']}")
            time.sleep(3)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")
            print(f"LỖI ĐĂNG {u}: HTTP {e.code} {body[:300]}")
            # Token hỏng/hết hạn -> dừng, KHÔNG đánh dấu, để lần sau thử lại.
            break
        except Exception as e:
            print(f"LỖI ĐĂNG {u}: {str(e)[:200]}")
            break

    save_state(st)
    print(f"Hoàn tất: đăng {done} tin mới.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
