#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gộp mọi khối JSON-LD của một trang thành MỘT khối @graph có liên kết thực thể.

Vì sao: mỗi trang đang có 3–5 khối schema rời rạc (Product, FAQPage, Breadcrumb,
RealEstateAgent…). Google đọc được nhưng KHÔNG biết chúng nói về cùng một doanh
nghiệp, cùng một trang. Gộp vào @graph và nối bằng @id thì cả site trở thành một
thực thể duy nhất — đây là thứ quyết định việc Google và AI hiểu "Nam Ban Villas
là ai" thay vì thấy 193 mẩu rời.

Chạy: python3 scripts/gop-schema-graph.py           (gộp, có kiểm tra)
      python3 scripts/gop-schema-graph.py --thu     (chỉ in ra, không ghi)

An toàn: chỉ ghi khi số node sau khi gộp BẰNG số node trước khi gộp.
"""
import glob, json, os, re, sys

SITE = "https://nambanvillas.vn"
ID_ORG = SITE + "/#organization"
ID_WEB = SITE + "/#website"
THU = "--thu" in sys.argv

# Loại schema -> đuôi @id gắn theo URL trang
DUOI = {
    "WebPage": "webpage", "CollectionPage": "webpage", "AboutPage": "webpage",
    "ItemPage": "webpage", "Article": "article", "NewsArticle": "article",
    "BlogPosting": "article", "Product": "product", "FAQPage": "faq",
    "BreadcrumbList": "breadcrumb", "ItemList": "itemlist", "Service": "service",
    "HowTo": "howto", "Dataset": "dataset",
}
LOAI_TRANG = ("WebPage", "CollectionPage", "AboutPage", "ItemPage")
LOAI_BAI = ("Article", "NewsArticle", "BlogPosting")
LOAI_TO_CHUC = ("Organization", "RealEstateAgent", "LocalBusiness")


def url_trang(f):
    d = os.path.dirname(f)
    return SITE + "/" + (d + "/" if d else "")


def lam_phang(obj):
    ra = []
    for x in (obj if isinstance(obj, list) else [obj]):
        if not isinstance(x, dict):
            continue
        if isinstance(x.get("@graph"), list):
            ra.extend(n for n in x["@graph"] if isinstance(n, dict))
        else:
            ra.append(x)
    return ra


def gop_mot_trang(f):
    s = open(f, encoding="utf-8").read()
    khoi = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if len(khoi) < 2:
        return None, 0, 0           # 1 khối thì gộp cũng chẳng lợi gì

    nodes, tho = [], []
    for b in khoi:
        try:
            d = json.loads(b)
        except Exception:
            return None, 0, 0       # có khối hỏng -> không đụng vào trang này
        tho.append(b)
        nodes.extend(lam_phang(d))
    if any("@graph" in b for b in tho):
        return None, 0, 0           # đã gộp rồi

    truoc = len(nodes)
    url = url_trang(f)

    # 1) gắn @id cho từng node
    co_trang, co_bai = None, None
    for n in nodes:
        n.pop("@context", None)
        t = n.get("@type")
        t0 = t[0] if isinstance(t, list) and t else t
        if t0 in LOAI_TO_CHUC:
            n["@id"] = ID_ORG
        elif t0 in DUOI:
            n.setdefault("@id", url + "#" + DUOI[t0])
            if t0 in LOAI_TRANG:
                co_trang = n["@id"]
            if t0 in LOAI_BAI:
                co_bai = n["@id"]

    # 2) nối các thực thể với nhau
    for n in nodes:
        t = n.get("@type")
        t0 = t[0] if isinstance(t, list) and t else t
        if t0 in LOAI_TO_CHUC:
            continue
        if t0 in LOAI_TRANG or t0 in LOAI_BAI:
            n["isPartOf"] = {"@id": ID_WEB}
            n["publisher"] = {"@id": ID_ORG}
        if t0 == "Product":
            n.setdefault("seller", {"@id": ID_ORG})
            if co_trang:
                n["mainEntityOfPage"] = {"@id": co_trang}
        if t0 in ("FAQPage", "BreadcrumbList", "ItemList"):
            neo = co_bai or co_trang
            if neo:
                n["isPartOf"] = {"@id": neo}

    graph = {"@context": "https://schema.org", "@graph": nodes}
    khoi_moi = ('<script type="application/ld+json">%s</script>'
                % json.dumps(graph, ensure_ascii=False, separators=(",", ":")))

    # 3) thay khối đầu bằng @graph, xoá các khối còn lại
    dau = '<script type="application/ld+json">%s</script>' % tho[0]
    s2 = s.replace(dau, khoi_moi, 1)
    for b in tho[1:]:
        cu = '<script type="application/ld+json">%s</script>' % b
        s2 = s2.replace(cu + "\n", "", 1) if (cu + "\n") in s2 else s2.replace(cu, "", 1)

    # 4) kiểm: đọc lại phải ra ĐÚNG số node cũ
    lai = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s2, re.S)
    sau = 0
    for b in lai:
        try:
            sau += len(lam_phang(json.loads(b)))
        except Exception:
            return None, truoc, -1
    if sau != truoc:
        return None, truoc, sau
    return s2, truoc, sau


def main():
    ok = bo = loi = 0
    tong_node = 0
    for f in sorted(glob.glob("**/*.html", recursive=True)):
        if f.startswith(("node_modules", "docs")):
            continue
        s2, truoc, sau = gop_mot_trang(f)
        if s2 is None:
            if truoc and sau != truoc:
                print("  BỎ (lệch node) %s: %d -> %d" % (f, truoc, sau))
                loi += 1
            else:
                bo += 1
            continue
        tong_node += truoc
        if not THU:
            open(f, "w", encoding="utf-8").write(s2)
        ok += 1
    print("Gộp %d trang (%d node schema) | bỏ qua %d | lệch %d%s"
          % (ok, tong_node, bo, loi, "  [chỉ thử, chưa ghi]" if THU else ""))
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
