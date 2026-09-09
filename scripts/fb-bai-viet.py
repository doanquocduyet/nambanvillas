#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Đăng BÀI VIẾT của web lên Facebook Page — vài ngày 1 bài, không dồn.

Khác gì fb-auto-post.py:
  - fb-auto-post.py đăng TIN RAO (lô/nhà đang bán).
  - File này đăng BÀI VIẾT (thị trường, về Nam Ban, notes, cẩm nang) — thứ khiến
    người ta bấm Theo dõi. Page toàn tin rao thì không ai follow.

Ba điều cố ý làm khác để không bị Facebook bóp phân phối:
  1. LINK ĐẶT Ở COMMENT ĐẦU TIÊN, không nằm trong bài. Facebook giảm hiển thị
     bài đẩy người dùng rời nền tảng — đây là cách chuẩn để tránh.
  2. Bài đăng đủ ý đọc được ngay trên Facebook, không phải mẩu teaser cụt.
  3. Giãn cách NGAY_GIAN ngày mới đăng 1 bài, chạy lại nhiều lần trong ngày
     cũng chỉ đăng đúng 1 bài.

Bảo mật: chỉ đăng lên Page của FB_PAGE_TOKEN. Không đụng nick cá nhân, không đụng group.

Chạy:
  python3 scripts/fb-bai-viet.py            # đăng nếu đã đủ ngày giãn cách
  python3 scripts/fb-bai-viet.py --ep       # ép đăng ngay, bỏ qua giãn cách
  python3 scripts/fb-bai-viet.py --thu      # in thử bài sắp đăng, KHÔNG đăng
"""
import os, re, sys, json, ssl, html, pathlib, datetime
import urllib.request, urllib.parse, urllib.error
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "fb-baiviet-posted.json"
SITE = "https://nambanvillas.vn"
GRAPH = "https://graph.facebook.com/v21.0"
NGAY_GIAN = 3                      # vài ngày 1 bài
CTX = ssl.create_default_context()
UA = {"User-Agent": "NamBanVillas-BaiViet/1.0"}

# Thư mục chứa bài viết + vài trang cẩm nang đáng đăng.
# KHÔNG lấy trang danh sách lô (đã có fb-auto-post lo) và trang liên hệ.
THU_MUC = ["thi-truong", "ve-nam-ban", "namban-notes"]
TRANG_LE = [
    "phap-ly-mua-dat-nam-ban",
    "hoi-dap",
    "cham-diem-lo-dat",
    "di-mot-vong-nam-ban",
]


# Khối chỉ có nghĩa khi nhìn thấy trên web (bảng số liệu, hộp điều hướng, chân trang)
# — đọc trên Facebook sẽ cụt lủn nên bỏ hẳn.
BO_KHOI = ("so-lieu-that", "truoc", "footer", "tour-jump", "nav", "breadcrumb",
           "mobile-sheet", "prop-card", "sp-row", "cm-cluster", "tq")


class BocDoan(HTMLParser):
    """Lấy các đoạn <p> thuộc phần thân bài, bỏ các khối chỉ có nghĩa trên web."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.doan, self.buf = [], None
        self.bo_sau = None      # độ sâu thẻ nơi bắt đầu bỏ qua
        self.sau = 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in ("div", "section", "footer", "nav", "aside", "details"):
            self.sau += 1
            if self.bo_sau is None:
                lop = (d.get("class") or "") + " " + (d.get("id") or "")
                if any(k in lop.split() or k in lop for k in BO_KHOI):
                    self.bo_sau = self.sau
        elif tag == "p" and self.bo_sau is None:
            self.buf = []

    def handle_endtag(self, tag):
        if tag in ("div", "section", "footer", "nav", "aside", "details"):
            if self.bo_sau is not None and self.sau == self.bo_sau:
                self.bo_sau = None
            self.sau = max(0, self.sau - 1)
        elif tag == "p" and self.buf is not None:
            t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            self.buf = None
            if len(t) >= 70 and not t.startswith(("Nguồn:", "Ảnh:", "Cập nhật")) and t not in self.doan:
                self.doan.append(t)

    def handle_data(self, data):
        if self.buf is not None:
            self.buf.append(data)


def doan_van(s):
    p = BocDoan()
    try:
        p.feed(s)
    except Exception:
        pass
    return p.doan[:4]


def sach(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def bai_viet():
    """Trả về danh sách đường dẫn bài viết, thứ tự ổn định."""
    ra = []
    for d in THU_MUC:
        thu_muc = ROOT / d
        if not thu_muc.is_dir():
            continue
        for p in sorted(thu_muc.iterdir()):
            if (p / "index.html").exists():
                ra.append(f"/{d}/{p.name}/")
    for t in TRANG_LE:
        if (ROOT / t / "index.html").exists():
            ra.append(f"/{t}/")
    return ra


def doc_bai(duong_dan):
    f = ROOT / duong_dan.strip("/") / "index.html"
    if not f.exists():
        return None
    s = f.read_text(encoding="utf-8", errors="ignore")

    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    tieu_de = sach(m.group(1)) if m else ""
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    mo_ta = html.unescape(m.group(1)) if m else ""
    m = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    anh = m.group(1) if m else ""

    doan = doan_van(s)

    if not (tieu_de and anh and doan):
        return None
    return dict(url=SITE + duong_dan, tieu_de=tieu_de, mo_ta=mo_ta, anh=anh, doan=doan)


def viet_caption(b):
    """Bài đọc trọn vẹn trên Facebook. Link nằm ở comment, không ở đây."""
    than = "\n\n".join(b["doan"][:3])
    if len(than) > 1500:
        than = than[:1500].rsplit(" ", 1)[0] + "…"
    # Bài viết KHÔNG kèm số điện thoại — đây là bài đọc, không phải bài rao.
    # Ai muốn liên hệ đã có nút trên Page và link web ở comment.
    return (
        f"{b['tieu_de']}\n\n"
        f"{than}\n\n"
        f"Bài đầy đủ ở link dưới phần bình luận."
    )


def doc_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"da_dang": {}, "lan_cuoi": None}


def ghi_state(st):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def gan_link(token, post_id, url):
    """Gắn link về web. Thử comment trước; token thiếu quyền bình luận (403) thì
    chèn thẳng link vào cuối bài. Không bao giờ để bài trôi mà không có đường về web."""
    try:
        api("/%s/comments" % post_id, {"message": "Đọc bài đầy đủ: " + url,
                                       "access_token": token})
        return "comment"
    except Exception as e:
        print("Không comment được (%s) — chèn link vào bài." % e)
    try:
        cur = get("/%s" % post_id, {"fields": "message", "access_token": token})
        msg = (cur.get("message") or "").replace(
            "Bài đầy đủ ở link dưới phần bình luận.", "").rstrip()
        api("/%s" % post_id, {"message": msg + "\n\nĐọc bài đầy đủ: " + url,
                              "access_token": token})
        return "trong-bai"
    except Exception as e:
        print("Cũng không sửa được bài:", e)
    return None


def get(path, params):
    url = GRAPH + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def api(path, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(GRAPH + path, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def du_ngay(lan_cuoi):
    if not lan_cuoi:
        return True
    try:
        truoc = datetime.date.fromisoformat(lan_cuoi[:10])
    except Exception:
        return True
    return (datetime.date.today() - truoc).days >= NGAY_GIAN


def main():
    ep = "--ep" in sys.argv
    thu = "--thu" in sys.argv
    st = doc_state()
    da = st.setdefault("da_dang", {})

    # Vá bài cũ đăng rồi mà chưa gắn được link (ví dụ hôm token còn thiếu quyền)
    token_va = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if token_va and not thu:
        for dd, info in da.items():
            if info.get("post_id") and not info.get("link"):
                cach = gan_link(token_va, info["post_id"], SITE + dd)
                if cach:
                    info["link"] = cach
                    ghi_state(st)
                    print("Đã vá link cho bài cũ:", dd, "->", cach)

    con_lai = [u for u in bai_viet() if u not in da]
    if not con_lai:
        print("Đã đăng hết bài viết. Có bài mới trên web thì tự vào hàng đợi.")
        return 0

    if not (ep or thu) and not du_ngay(st.get("lan_cuoi")):
        print("Chưa đủ %d ngày kể từ bài trước (%s) — bỏ qua lần này."
              % (NGAY_GIAN, st.get("lan_cuoi")))
        return 0

    duong_dan = con_lai[0]
    b = doc_bai(duong_dan)
    if not b:
        print("Bỏ qua (thiếu tiêu đề/ảnh/nội dung):", duong_dan)
        da[duong_dan] = {"bo_qua": True}
        ghi_state(st)
        return 0

    caption = viet_caption(b)
    if thu:
        print("=== SẼ ĐĂNG:", b["url"])
        print("--- ảnh:", b["anh"])
        print("--- caption:\n" + caption)
        print("--- comment đầu:\n" + f"Đọc bài đầy đủ: {b['url']}")
        print("\nCòn lại trong hàng đợi:", len(con_lai) - 1, "bài")
        return 0

    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if not token:
        print("Thiếu FB_PAGE_TOKEN — thoát êm, không đăng gì.")
        return 0

    res = api("/me/photos", {"url": b["anh"], "caption": caption, "access_token": token})
    post_id = res.get("post_id") or res.get("id")
    if not post_id:
        print("Đăng hỏng:", res)
        return 1

    cach = gan_link(token, post_id, b["url"])
    da[duong_dan] = {"post_id": post_id, "ngay": datetime.date.today().isoformat(),
                     "link": cach}
    st["lan_cuoi"] = datetime.date.today().isoformat()
    ghi_state(st)
    print("Đã đăng:", b["url"], "->", post_id)
    print("Còn lại trong hàng đợi:", len(con_lai) - 1, "bài")
    return 0


if __name__ == "__main__":
    sys.exit(main())
