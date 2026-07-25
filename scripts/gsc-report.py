#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Báo cáo index Google Search Console cho nambanvillas.vn.
Chạy tự động trong GitHub Action (mỗi tuần) — đọc trạng thái index từng URL trong
sitemap.xml qua URL Inspection API, ghi kết quả vào docs/gsc-status.md.

Cần:
  - Secret GSC_SA_JSON  : nội dung file JSON của service account (Google Cloud).
  - Biến GSC_SITE_URL   : property trong GSC. Mặc định "https://nambanvillas.vn/".
                          Nếu property kiểu "Miền" thì đặt "sc-domain:nambanvillas.vn".

Không có secret -> KHÔNG fail, chỉ ghi trạng thái "chưa cấu hình" rồi thoát 0.
"""
import os, sys, re, json, time, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "gsc-status.md"
SITE = os.environ.get("GSC_SITE_URL", "https://nambanvillas.vn/").strip()
SA_RAW = os.environ.get("GSC_SA_JSON", "").strip()


def now_vn():
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M")


def write(md):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(md, encoding="utf-8")
    print("Đã ghi", OUT)


def load_urls():
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>([^<]+)</loc>", sm)


def main():
    if not SA_RAW:
        write(
            f"# Báo cáo index Google Search Console — Nam Ban Villas\n\n"
            f"> Cập nhật: {now_vn()}\n\n"
            f"⚠️ **Chưa cấu hình.** Cần thêm secret `GSC_SA_JSON` và cấp quyền service "
            f"account đọc Search Console. Xem hướng dẫn: `docs/gsc-auto-setup.md`.\n"
        )
        print("Chưa có GSC_SA_JSON — bỏ qua (không lỗi).")
        return 0

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except Exception as e:
        write(f"# Báo cáo index GSC\n\n> {now_vn()}\n\n❌ Thiếu thư viện: {e}\n")
        print("Thiếu thư viện google-auth/api-client:", e)
        return 1

    info = json.loads(SA_RAW)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)

    urls = load_urls()
    indexed, notidx, errors = [], [], []
    for u in urls:
        try:
            r = svc.urlInspection().index().inspect(
                body={"inspectionUrl": u, "siteUrl": SITE}).execute()
            res = r.get("inspectionResult", {}).get("indexStatusResult", {})
            verdict = res.get("verdict", "?")
            state = res.get("coverageState", "?")
            last = res.get("lastCrawlTime", "")
            if verdict == "PASS":
                indexed.append((u, state))
            else:
                notidx.append((u, state, last))
        except Exception as e:
            msg = str(e)
            errors.append((u, msg[:160]))
            # lỗi quyền/property sai -> dừng sớm, báo rõ
            if "403" in msg or "does not have" in msg or "permission" in msg.lower():
                break
        time.sleep(0.5)  # nhẹ nhàng với quota

    total = len(urls)
    lines = [
        "# Báo cáo index Google Search Console — Nam Ban Villas",
        "",
        f"> Cập nhật tự động: **{now_vn()}** · Property: `{SITE}`",
        "",
        f"- Tổng URL trong sitemap: **{total}**",
        f"- ✅ Đã lập chỉ mục: **{len(indexed)}**",
        f"- ⏳ Chưa lập chỉ mục: **{len(notidx)}**",
        f"- ⚠️ Lỗi khi kiểm: **{len(errors)}**",
        "",
    ]
    if notidx:
        lines += ["## ⏳ Trang CHƯA index (cần chú ý)", ""]
        for u, state, last in notidx:
            lines.append(f"- `{u}` — {state}" + (f" · lần crawl cuối {last[:10]}" if last else ""))
        lines.append("")
    if errors:
        lines += ["## ⚠️ Lỗi khi kiểm", ""]
        for u, msg in errors[:20]:
            lines.append(f"- `{u}` — {msg}")
        lines.append("")
        lines += ["> Nếu lỗi 403/permission: kiểm lại đã cấp quyền service account trong "
                  "GSC chưa, và `GSC_SITE_URL` có đúng loại property (URL-prefix vs Miền) không.", ""]
    lines += ["## ✅ Trang đã index", ""]
    for u, state in indexed:
        lines.append(f"- `{u}` — {state}")
    lines.append("")

    write("\n".join(lines))
    print(f"Xong: index {len(indexed)} · chưa {len(notidx)} · lỗi {len(errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
