# -*- coding: utf-8 -*-
"""Phần dùng chung cho mọi máy đăng Facebook của Nam Ban Villas.

Hai việc:
  1. kiem_token()  — in ngay đầu log token thuộc loại gì, còn hạn bao lâu.
  2. gan_link()    — thả link web vào COMMENT đầu tiên, không bao giờ nhét vào bài.

Vì sao tách ra: cả fb-auto-post.py (tin rao) và fb-bai-viet.py (bài viết) đều
cần đúng hai việc này. Viết hai lần là hai lần lệch nhau.
"""
import datetime
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"
UA = {"User-Agent": "NamBanVillas-AutoPost/1.0"}
CTX = ssl.create_default_context()


def _get(path, params):
    url = GRAPH + path + ("&" if "?" in path else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def _post(path, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(GRAPH + path, data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


# ── 1. Kiểm token, in ngay đầu log mỗi lần chạy ──────────────────────────────
# ĐÃ TỪNG DÍNH: cầm nhầm token NGƯỜI DÙNG tưởng là token Trang. Token người dùng
# dài hạn sống đúng 60 ngày — hai tháng sau hệ thống chết lặng lẽ, mà Action vẫn
# xanh vì ngày nào không có tin mới thì nó thoát sạch. Nên phải in ra MỖI LẦN,
# không giấu sau biến debug.
def kiem_token(token):
    """In loại token + hạn dùng. Trả về True nếu token dùng đăng Trang được.

    Kiểm hỏng (mạng, quyền) KHÔNG chặn việc đăng — chỉ in ra rồi chạy tiếp.
    """
    try:
        d = _get("/debug_token", {"input_token": token, "access_token": token}).get("data", {})
    except Exception as e:
        print("Token: không kiểm được (%s) — vẫn thử đăng." % str(e)[:80])
        return True

    loai = (d.get("type") or "?").upper()
    exp = d.get("expires_at")
    if exp == 0 or exp is None:
        han = "KHÔNG HẾT HẠN"
    else:
        ngay = datetime.datetime.utcfromtimestamp(exp)
        con = (ngay - datetime.datetime.utcnow()).days
        han = "HẾT HẠN sau %d ngày (%s UTC)" % (con, ngay.strftime("%d/%m/%Y %H:%M"))
    print("Token: loại %s · %s" % (loai, han))

    if loai != "PAGE":
        print("  CẢNH BÁO: đây KHÔNG phải token Trang. Token người dùng chỉ sống 60 ngày.")
        print("  Cách lấy token Trang không hết hạn: xem docs/fb-auto-setup.md")
    if exp not in (0, None):
        print("  CẢNH BÁO: token có hạn — tới ngày trên là máy đăng chết lặng lẽ.")

    quyen = set(d.get("scopes") or [])
    if quyen and "pages_manage_engagement" not in quyen:
        print("  THIẾU QUYỀN pages_manage_engagement — sẽ KHÔNG comment link được.")
    return loai == "PAGE" or not d.get("type")


# ── 2. Link về web CHỈ nằm ở comment ────────────────────────────────────────
# LUẬT: không bao giờ chèn link vào thân bài. Facebook bóp tầm với bài có link
# ra ngoài, và chủ web không thích nhìn link nằm trên bài.
# Comment hỏng thì GHI LẠI, lần chạy sau thử lại — không "chữa cháy" bằng cách
# nhét link lên bài.
def gan_link(token, post_id, url, loi_moi="Chi tiết và hình ảnh đầy đủ: "):
    try:
        _post("/%s/comments" % post_id, {"message": loi_moi + url, "access_token": token})
        print("  · đã comment link: %s" % url)
        return True
    except urllib.error.HTTPError as e:
        than = e.read().decode("utf-8", "ignore")[:200]
        print("  · CHƯA comment được link (HTTP %s %s) — để lần sau thử lại." % (e.code, than))
    except Exception as e:
        print("  · CHƯA comment được link (%s) — để lần sau thử lại." % str(e)[:120])
    return False


def thu_lai_comment(token, cho_comment):
    """Đầu mỗi lần chạy: thử lại những bài lần trước chưa gắn được link.

    cho_comment: dict {post_id: url}. Trả về danh sách post_id đã gắn xong.
    """
    if not cho_comment:
        return []
    print("Còn %d bài chưa gắn được link — thử lại:" % len(cho_comment))
    xong = []
    for pid, u in list(cho_comment.items()):
        if gan_link(token, pid, u):
            xong.append(pid)
    return xong


# ── 3. Chốt chặn: caption tuyệt đối không được chứa link ────────────────────
def khong_duoc_co_link(caption):
    thap = caption.lower()
    for dau in ("http://", "https://", "nambanvillas.vn", "www."):
        if dau in thap:
            raise RuntimeError(
                "Caption chứa link (%s) — link chỉ được nằm ở comment. Dừng, không đăng." % dau)
