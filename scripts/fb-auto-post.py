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
HOTLINE = "0978 758 788"
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


def meta_of(u):
    """Bóc og:title, og:description, og:image từ file HTML local."""
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
    desc = grab("og:description")
    image = grab("og:image")
    if not (title and image):
        return None
    return {"title": title, "desc": desc, "image": image}


def caption_for(m, url):
    # Giọng Villas: không emoji, thẳng, có số + đường liên hệ rõ.
    parts = [m["title"]]
    if m["desc"]:
        parts.append(m["desc"])
    parts.append(f"Gọi / Zalo: {HOTLINE}")
    parts.append(f"Xem chi tiết + hình ảnh: {url}")
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


def post_photo(token, image_url, caption):
    data = urllib.parse.urlencode({
        "url": image_url,
        "caption": caption,
        "access_token": token,
    }).encode()
    req = urllib.request.Request(GRAPH + "/me/photos", data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


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

    # Đèn chẩn đoán: token là của Page hay Người dùng? (KHÔNG lộ token)
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
        perms = _get("/me/permissions")
        granted = [p["permission"] for p in perms.get("data", []) if p.get("status") == "granted"]
        print("CHẨN ĐOÁN: đây là TOKEN NGƯỜI DÙNG. Quyền đã cấp:", ", ".join(granted) or "(không có)")
        print("  -> Cần dùng TOKEN CỦA PAGE (lấy từ /me/accounts), không phải token này.")
    except urllib.error.HTTPError as e:
        # /me/permissions chỉ chạy với token người dùng; lỗi = có thể là token Page.
        print("CHẨN ĐOÁN: /me/permissions không đọc được -> nhiều khả năng token của PAGE. HTTP", e.code)

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
            res = post_photo(token, m["image"], cap)
            posted[u] = {"post_id": res.get("post_id") or res.get("id", "")}
            done += 1
            print(f"ĐĂNG OK: {u} -> {posted[u]['post_id']}")
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
