#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Đọc số liệu thật của Facebook Page rồi rút ra công thức bài nào ăn.

Vì sao cần: mọi lời khuyên "hook thế này mới viral" đều là đoán nếu không nhìn
số của chính Page mình. File này lấy reach/like/comment/share của từng bài đã
đăng, xếp hạng, rồi tự tìm điểm chung của nhóm bài mạnh nhất.

Ghi ra:
  data/fb-insights.json   — số liệu thô từng bài (để lần sau so sánh)
  data/fb-insights.md     — bản đọc được: top bài, công thức rút ra

Cần FB_PAGE_TOKEN có quyền pages_read_engagement. Thiếu quyền -> báo rõ, không làm hỏng gì.
Chạy: python3 scripts/fb-insights.py [số_bài]      (mặc định 100 bài gần nhất)
"""
import os, re, sys, json, ssl, pathlib, datetime, statistics
import urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "data" / "fb-insights.json"
OUT_MD = ROOT / "data" / "fb-insights.md"
GRAPH = "https://graph.facebook.com/v21.0"
CTX = ssl.create_default_context()
UA = {"User-Agent": "NamBanVillas-Insights/1.0"}
SO_BAI = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 100


def get(path, params):
    url = GRAPH + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


# Bộ trường đầy đủ cần pages_read_engagement; bộ rút gọn thì không.
FIELDS_DU = ("id,created_time,message,permalink_url,shares,"
             "likes.summary(true).limit(0),comments.summary(true).limit(0)")
FIELDS_GON = "id,created_time,message,permalink_url,shares"


def lay_bai(token, gioi_han, fields=FIELDS_DU):
    """Lấy bài đã đăng kèm số tương tác. Phân trang tới khi đủ."""
    bai, sau = [], None
    while len(bai) < gioi_han:
        p = {"fields": fields, "limit": 25, "access_token": token}
        if sau:
            p["after"] = sau
        d = get("/me/posts", p)
        for x in d.get("data", []):
            bai.append(x)
        sau = (d.get("paging", {}).get("cursors", {}) or {}).get("after")
        if not sau or not d.get("data"):
            break
    return bai[:gioi_han]


def lay_reach(token, post_id):
    """Số người thấy bài. Cần pages_read_engagement — thiếu quyền thì trả None."""
    try:
        d = get("/%s/insights" % post_id,
                {"metric": "post_impressions_unique", "access_token": token})
        for m in d.get("data", []):
            vals = m.get("values") or []
            if vals:
                return vals[0].get("value")
    except urllib.error.HTTPError:
        return None
    except Exception:
        return None
    return None


def do_dai(msg):
    return len((msg or "").split())


def cau_dau(msg):
    t = (msg or "").strip().split("\n")[0].strip()
    return t[:120]


def kieu_bai(msg):
    """Đoán loại bài từ nội dung — chỉ để nhóm lại, không phải phán xét."""
    t = (msg or "").lower()
    if re.search(r"\d+\s*(triệu|tỷ)/", t) or "thổ cư" in t and "sổ" in t and "•" in (msg or ""):
        return "tin rao"
    if "bài đầy đủ ở link" in t:
        return "bài viết"
    return "khác"


def main():
    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if not token:
        print("Thiếu FB_PAGE_TOKEN — thoát êm.")
        return 0

    day_du = True
    try:
        bai = lay_bai(token, SO_BAI)
    except urllib.error.HTTPError as e:
        loi = e.read().decode("utf-8", "ignore")
        thieu = "pages_read_engagement" in loi
        # Thiếu quyền đọc tương tác thì vẫn lấy được danh sách bài + lượt chia sẻ.
        # Có ít số liệu còn hơn không có gì.
        if thieu:
            try:
                bai = lay_bai(token, SO_BAI, FIELDS_GON)
                day_du = False
                print("Thiếu pages_read_engagement — chỉ đọc được bài và lượt chia sẻ.")
            except urllib.error.HTTPError as e2:
                loi = e2.read().decode("utf-8", "ignore")
                bai = None
        else:
            bai = None
        if bai is None:
            print("Không đọc được danh sách bài:", loi[:400])
            # Thiếu quyền là chuyện của token, không phải lỗi code — ghi lại rõ ràng
            # rồi thoát êm, để lịch chạy hàng tuần không báo đỏ vô nghĩa.
            OUT_MD.parent.mkdir(parents=True, exist_ok=True)
            OUT_MD.write_text(
                "# Số liệu Facebook Page — chưa đọc được\n\n"
                "Thử đọc ngày %s nhưng token thiếu quyền `pages_read_engagement`.\n\n"
                "Cách mở: vào https://developers.facebook.com/tools/explorer/ → chọn Page "
                "Nam Ban Villas → Permissions → tick `pages_read_engagement` và "
                "`pages_manage_engagement` → Generate Access Token → dán token mới vào "
                "secret `FB_PAGE_TOKEN`.\n\n"
                "Cùng một token đó cũng mở luôn việc tự động comment link dưới bài.\n"
                % datetime.date.today().isoformat(), encoding="utf-8")
            return 0
        return 1
    if not bai:
        print("Page chưa có bài nào.")
        return 0

    thieu_quyen = 0
    rows = []
    for x in bai:
        pid = x.get("id")
        like = ((x.get("likes") or {}).get("summary") or {}).get("total_count", 0)
        cmt = ((x.get("comments") or {}).get("summary") or {}).get("total_count", 0)
        shr = ((x.get("shares") or {}).get("count", 0)) if x.get("shares") else 0
        reach = lay_reach(token, pid) if day_du else None
        if reach is None:
            thieu_quyen += 1
        rows.append(dict(
            id=pid, ngay=(x.get("created_time") or "")[:10],
            link=x.get("permalink_url", ""),
            cau_dau=cau_dau(x.get("message")),
            tu=do_dai(x.get("message")),
            kieu=kieu_bai(x.get("message")),
            like=like, cmt=cmt, share=shr, reach=reach,
            diem=like + cmt * 3 + shr * 5,   # comment và share đáng giá hơn like
        ))

    rows.sort(key=lambda r: -r["diem"])
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(
        {"ngay_doc": datetime.date.today().isoformat(), "so_bai": len(rows), "bai": rows},
        ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- rút công thức ----
    co_tuong_tac = [r for r in rows if r["diem"] > 0]
    top = rows[:10]
    duoi = rows[-10:]
    md = ["# Số liệu Facebook Page — đọc ngày %s" % datetime.date.today().isoformat(), ""]
    md.append("Đọc %d bài. %d bài có tương tác, %d bài im lặng hoàn toàn."
              % (len(rows), len(co_tuong_tac), len(rows) - len(co_tuong_tac)))
    if not day_du:
        md.append("")
        md.append("> Token thiếu quyền `pages_read_engagement` nên **chưa đọc được "
                  "like, bình luận và lượt tiếp cận**. Bảng dưới chỉ có lượt chia sẻ. "
                  "Mở quyền đó ở Graph API Explorer là có đủ số.")
    elif thieu_quyen == len(rows):
        md.append("")
        md.append("> Chưa đọc được số người tiếp cận (reach): token thiếu quyền "
                  "`pages_read_engagement`. Các số like/comment/share bên dưới vẫn đúng.")
    md.append("")

    if co_tuong_tac:
        md.append("## 10 bài mạnh nhất")
        md.append("")
        md.append("| # | Ngày | Kiểu | Chữ | Like | Cmt | Share | Câu mở đầu |")
        md.append("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(top, 1):
            md.append("| %d | %s | %s | %d | %d | %d | %d | %s |"
                      % (i, r["ngay"], r["kieu"], r["tu"], r["like"], r["cmt"],
                         r["share"], r["cau_dau"].replace("|", "/")[:70]))
        md.append("")

        # Độ dài nào ăn
        dai_top = [r["tu"] for r in top if r["tu"]]
        dai_all = [r["tu"] for r in rows if r["tu"]]
        if dai_top and dai_all:
            md.append("## Độ dài")
            md.append("")
            md.append("- Bài mạnh nhất: trung vị **%d chữ**" % statistics.median(dai_top))
            md.append("- Toàn bộ Page: trung vị %d chữ" % statistics.median(dai_all))
            md.append("")

        # Kiểu bài nào ăn
        md.append("## Kiểu bài")
        md.append("")
        for k in ("tin rao", "bài viết", "khác"):
            nhom = [r for r in rows if r["kieu"] == k]
            if not nhom:
                continue
            tb = sum(r["diem"] for r in nhom) / len(nhom)
            md.append("- **%s**: %d bài, điểm tương tác trung bình **%.1f**" % (k, len(nhom), tb))
        md.append("")
        md.append("> Điểm tương tác = like + comment×3 + share×5. "
                  "Comment và share đáng giá hơn like vì Facebook dùng chúng để quyết định phân phối.")
        md.append("")

        md.append("## 10 bài yếu nhất — xem để tránh lặp")
        md.append("")
        for r in duoi:
            md.append("- (%d điểm) %s — %s" % (r["diem"], r["ngay"], r["cau_dau"][:80]))
        md.append("")
    else:
        md.append("Chưa đo được tương tác nào. %s"
                  % ("Do token thiếu quyền đọc like/bình luận."
                     if not day_du else
                     "Page có bài nhưng chưa ai like/bình luận/chia sẻ."))
        md.append("")
        md.append("## 10 bài gần nhất")
        md.append("")
        for r in sorted(rows, key=lambda x: x["ngay"], reverse=True)[:10]:
            md.append("- %s (%s, %d chữ) — %s" % (r["ngay"], r["kieu"], r["tu"], r["cau_dau"][:80]))
        md.append("")

    md.append("Số liệu thô từng bài: `data/fb-insights.json`.")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("Đã đọc %d bài. Ghi: %s và %s" % (len(rows), OUT_JSON.name, OUT_MD.name))
    if thieu_quyen:
        print("Không lấy được reach của %d bài (token có thể thiếu pages_read_engagement)." % thieu_quyen)
    if co_tuong_tac:
        print("Bài mạnh nhất: %d điểm — %s" % (rows[0]["diem"], rows[0]["cau_dau"][:70]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
