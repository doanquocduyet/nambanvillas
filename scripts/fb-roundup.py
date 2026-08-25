#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Đăng 1 BÀI TỔNG HỢP "hàng mới tuần qua" lên Facebook Page (1 post, không spam từng tin).
Gom các tin MỚI thêm trong N ngày (mặc định 7) theo git, nhóm theo loại, đăng 1 bài.

Cần FB_PAGE_TOKEN (như fb-auto-post). Thiếu token -> thoát êm.
Chạy: python3 scripts/fb-roundup.py [số_ngày]
"""
import os, re, sys, json, ssl, subprocess, pathlib
import urllib.request, urllib.parse, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import listing_common as lc

ROOT = pathlib.Path(__file__).resolve().parent.parent
GRAPH = "https://graph.facebook.com/v21.0"
HOTLINE = "0978 758 788"
CTX = ssl.create_default_context()
UA = {"User-Agent": "NamBanVillas-Roundup/1.0"}
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 7


def new_listings(days):
    """Trang lô tạo mới trong `days` ngày (theo git)."""
    try:
        out = subprocess.check_output(
            ["git", "log", f"--since={days} days ago", "--diff-filter=A",
             "--name-only", "--pretty=format:", "--",
             "dat-nen/*/index.html", "nha-ban/*/index.html"], text=True)
    except Exception as e:
        print("git log lỗi:", e); return []
    seen, files = set(), []
    for l in out.splitlines():
        l = l.strip()
        if l.endswith("index.html") and l not in seen and (ROOT / l).exists():
            seen.add(l); files.append(l)
    return files


def info(f):
    html = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
    ogt = lc.og(html, "og:title") or ""
    tt = re.search(r"<title>([^<]+)</title>", html)
    full = (tt.group(1) if tt else ogt).split("|")[0].strip()
    # giá: cụm "<số> triệu/tỷ[/nền|/lô]" trong title đầy đủ
    m = re.search(r"([\d.,]+\s*(?:[Tt]riệu|[Tt]ỷ)(?:\s*/\s*(?:[Nn]ền|[Ll]ô))?)(?!\s*/\s*[Tt]háng)", full)
    price = m.group(1) if m else ""
    short = re.split(r"\s*[–-]\s*", ogt or full)[0].strip()
    kind = "nha" if f.startswith("nha-ban/") else ("cum" if "/cum-" in f else "dat")
    return {"title": short, "price": price, "kind": kind}


def build_caption(items):
    grp = {"cum": [], "dat": [], "nha": []}
    for it in items:
        grp[it["kind"]].append(it)
    parts = [f"NAM BAN VILLAS — HÀNG MỚI TUẦN QUA ({len(items)} sản phẩm)",
             "", "Đất nền, nhà và cụm phân lô mới về tại Nam Ban – Lâm Hà. Tất cả đều có sổ, đã xem tận nơi.", ""]
    def sec(title, arr):
        if not arr: return
        parts.append(title)
        for it in arr:
            line = "• " + it["title"]
            if it["price"]: line += " – " + it["price"]
            parts.append(line)
        parts.append("")
    sec("CỤM PHÂN LÔ (F0, sổ sẵn):", grp["cum"])
    sec("ĐẤT NỀN:", grp["dat"])
    sec("NHÀ & VILLA:", grp["nha"])
    parts.append("Xem lô nào gửi Zalo em đối chiếu sổ + đưa đi xem tận nơi, nói thẳng nên hay không.")
    parts.append(f"Gọi / Zalo: {HOTLINE} · nambanvillas.vn")
    return "\n".join(parts)


def post_feed(token, message):
    data = urllib.parse.urlencode({"message": message, "access_token": token}).encode()
    req = urllib.request.Request(GRAPH + "/me/feed", data=data, headers=UA)
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def main():
    files = new_listings(DAYS)
    if not files:
        print(f"Không có tin mới trong {DAYS} ngày — không đăng roundup."); return 0
    items = [info(f) for f in files]
    items = [it for it in items if it["title"]]
    cap = build_caption(items)
    token = os.environ.get("FB_PAGE_TOKEN", "").strip()
    if not token:
        print("THIẾU FB_PAGE_TOKEN — in thử caption:\n"); print(cap); return 0
    try:
        res = post_feed(token, cap)
        print("ĐĂNG ROUNDUP OK:", res.get("id", ""))
    except urllib.error.HTTPError as e:
        print("LỖI:", e.code, e.read().decode("utf-8", "ignore")[:300]); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
