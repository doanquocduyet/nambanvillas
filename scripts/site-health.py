#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự kiểm sức khỏe web nambanvillas.vn — KHÔNG cần chìa khoá Google.
Với mỗi URL trong sitemap: kiểm HTTP 200, có bị chuyển hướng không, canonical
có khớp URL không. Bắt đúng các lỗi khiến Google không index (redirect/404/canonical lệch).
Ghi kết quả vào docs/site-health.md. Chạy được ngay, không cần cấu hình gì.
"""
import re, ssl, sys, json, datetime, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "site-health.md"
UA = {"User-Agent": "NamBanVillas-HealthCheck/1.0"}
CTX = ssl.create_default_context()


def now_vn():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")


def norm(u):
    return u.rstrip("/")


def load_urls():
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", sm)


def fetch(u):
    """Trả (status, final_url, html_or_'')."""
    req = urllib.request.Request(u, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
            final = r.geturl()
            body = r.read(200000).decode("utf-8", "ignore")
            return r.status, final, body
    except urllib.error.HTTPError as e:
        return e.code, u, ""
    except Exception as e:
        return 0, u, str(e)[:100]


def main():
    urls = load_urls()
    redirects, errors, canon_bad, ok = [], [], [], 0
    for u in urls:
        st, final, body = fetch(u)
        if st == 0:
            errors.append((u, "không kết nối: " + body)); continue
        if st >= 400:
            errors.append((u, f"HTTP {st}")); continue
        if norm(final) != norm(u):
            redirects.append((u, final)); continue
        m = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', body)
        if m and norm(m.group(1)) != norm(final):
            canon_bad.append((u, m.group(1))); continue
        ok += 1

    lines = [
        "# Tự kiểm sức khỏe web — Nam Ban Villas",
        "",
        f"> Cập nhật tự động: **{now_vn()}** · (không cần Google Search Console)",
        "",
        f"- Tổng URL: **{len(urls)}**",
        f"- ✅ Khỏe (200, không redirect, canonical khớp): **{ok}**",
        f"- ↪️ Bị chuyển hướng: **{len(redirects)}**",
        f"- 🔀 Canonical lệch: **{len(canon_bad)}**",
        f"- ❌ Lỗi (404/không tải được): **{len(errors)}**",
        "",
    ]
    if errors:
        lines += ["## ❌ Lỗi — SỬA NGAY (Google không index được)", ""]
        lines += [f"- `{u}` — {m}" for u, m in errors] + [""]
    if redirects:
        lines += ["## ↪️ Bị chuyển hướng (URL sitemap nên trỏ thẳng đích)", ""]
        lines += [f"- `{u}` → `{f}`" for u, f in redirects] + [""]
    if canon_bad:
        lines += ["## 🔀 Canonical lệch (dễ làm Google bối rối)", ""]
        lines += [f"- `{u}` — canonical trỏ `{c}`" for u, c in canon_bad] + [""]
    if not (errors or redirects or canon_bad):
        lines += ["## 🎉 Không phát hiện lỗi kỹ thuật nào. Web sạch.", ""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK {ok} · redirect {len(redirects)} · canonical lệch {len(canon_bad)} · lỗi {len(errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
