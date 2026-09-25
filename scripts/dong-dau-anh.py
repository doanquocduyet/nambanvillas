#!/usr/bin/env python3
"""
Đóng dấu bản quyền vào bên trong file ảnh (EXIF + XMP) — không đổi điểm ảnh, không nén lại.

Vì sao: ảnh bị lấy đăng lại nơi khác vẫn mang "© Nam Ban Villas — nambanvillas.vn" trong file;
Google/AI đọc được chủ ảnh (IPTC/XMP là tín hiệu nguồn gốc ảnh Google dùng cho Hình ảnh & Licensable).

Cách dùng:
  python3 scripts/dong-dau-anh.py                # đóng dấu toàn bộ images/ (bỏ qua ảnh đã có dấu)
  python3 scripts/dong-dau-anh.py <file/thư-mục> # chỉ ảnh đó
  python3 scripts/dong-dau-anh.py --kiem         # chỉ kiểm, liệt kê ảnh chưa có dấu (checker dùng)

nen-anh.py và prep-anh.py gọi lại hàm dong_dau() sau khi nén, nên ảnh mới đi qua 2 script đó tự có dấu.
JPEG: chèn 2 đoạn APP1 (EXIF, XMP) sau APP0 — dữ liệu ảnh giữ nguyên byte.
WebP: chuyển hộp VP8X + chunk EXIF/XMP — dữ liệu VP8 giữ nguyên byte.
PNG: ghi lại (không mất chất lượng) kèm tEXt Copyright/Author + iTXt XMP.
"""
import datetime, os, struct, sys

CHU = "Nam Ban Villas"
WEB = "https://nambanvillas.vn/"
DAU = "Nam Ban Villas — nambanvillas.vn"      # dùng trong XMP (UTF-8)
DAU_ASCII = "Nam Ban Villas - nambanvillas.vn"  # EXIF chỉ nhận ASCII — cũng là chuỗi nhận diện khi kiểm
DUOI = (".jpg", ".jpeg", ".png", ".webp")
NAM = datetime.date.today().year


def _ban_quyen(nam=None):
    return "© %d %s" % (nam or NAM, DAU)


def _ban_quyen_ascii(nam=None):
    return "(c) %d %s" % (nam or NAM, DAU_ASCII)


def _xmp(nam=None):
    bq = _ban_quyen(nam)
    return ('<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>'
            '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
            '<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" '
            'xmlns:plus="http://ns.useplus.org/ldf/xmp/1.0/" xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">'
            '<dc:creator><rdf:Seq><rdf:li>%s</rdf:li></rdf:Seq></dc:creator>'
            '<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">%s</rdf:li></rdf:Alt></dc:rights>'
            '<xmpRights:Marked>True</xmpRights:Marked>'
            '<xmpRights:WebStatement>%s</xmpRights:WebStatement>'
            '<xmpRights:UsageTerms><rdf:Alt><rdf:li xml:lang="x-default">Ảnh thuộc %s. Không dùng lại khi chưa có đồng ý — liên hệ 0978 758 788.</rdf:li></rdf:Alt></xmpRights:UsageTerms>'
            '<photoshop:Credit>%s</photoshop:Credit><photoshop:Source>%s</photoshop:Source>'
            '<plus:Licensor><rdf:Seq><rdf:li rdf:parseType="Resource"><plus:LicensorName>%s</plus:LicensorName><plus:LicensorURL>%s</plus:LicensorURL></rdf:li></rdf:Seq></plus:Licensor>'
            '<Iptc4xmpCore:CreatorContactInfo rdf:parseType="Resource"><Iptc4xmpCore:CiUrlWork>%s</Iptc4xmpCore:CiUrlWork><Iptc4xmpCore:CiTelWork>0978 758 788</Iptc4xmpCore:CiTelWork></Iptc4xmpCore:CreatorContactInfo>'
            '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>'
            % (CHU, bq, WEB, CHU, CHU, WEB, CHU, WEB, WEB)).encode("utf-8")


def _exif_tiff(nam=None):
    """TIFF (không có tiền tố 'Exif\\0\\0') chứa Artist + Copyright. Không bao giờ có GPS."""
    from PIL import Image
    ex = Image.Exif()
    ex[0x013B] = CHU                      # Artist
    ex[0x8298] = _ban_quyen_ascii(nam)    # Copyright (EXIF = ASCII)
    return ex.tobytes()[6:]


# ---------- JPEG ----------
def _jpeg_segments(d):
    """Danh sách (marker, start, end) tới hết các APPn/COM đầu file — dừng trước SOS/DQT/SOF."""
    i, out = 2, []
    while i + 4 <= len(d) and d[i] == 0xFF:
        m = d[i + 1]
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        n = struct.unpack(">H", d[i + 2:i + 4])[0]
        if not (0xE0 <= m <= 0xEF or m == 0xFE):
            break
        out.append((m, i, i + 2 + n))
        i += 2 + n
    return out


def _jpeg_co_dau(d):
    for m, a, b in _jpeg_segments(d):
        if m == 0xE1 and DAU_ASCII.encode() in d[a:b]:
            return True
    return False


def _jpeg(p, d, nam):
    segs = _jpeg_segments(d)
    giu = [s for s in segs if not (s[0] == 0xE1 and (d[s[1] + 4:s[1] + 10] == b"Exif\x00\x00" or d[s[1] + 4:s[1] + 33] == b"http://ns.adobe.com/xap/1.0/\x00"))]
    dau_anh = segs[-1][2] if segs else 2
    exif = b"Exif\x00\x00" + _exif_tiff(nam)
    xmp = b"http://ns.adobe.com/xap/1.0/\x00" + _xmp(nam)
    app1 = b"".join(b"\xFF\xE1" + struct.pack(">H", len(x) + 2) + x for x in (exif, xmp))
    app0 = [d[a:b] for m, a, b in giu if m == 0xE0]
    khac = [d[a:b] for m, a, b in giu if m != 0xE0]
    return d[:2] + b"".join(app0) + app1 + b"".join(khac) + d[dau_anh:]


# ---------- WebP ----------
def _webp_chunks(d):
    i, out = 12, []
    while i + 8 <= len(d):
        tag, n = d[i:i + 4], struct.unpack("<I", d[i + 4:i + 8])[0]
        out.append((tag, d[i + 8:i + 8 + n]))
        i += 8 + n + (n & 1)
    return out


def _webp_co_dau(d):
    return d[:4] == b"RIFF" and any(t == b"EXIF" and DAU_ASCII.encode() in c for t, c in _webp_chunks(d))


def _webp(p, d, nam):
    from PIL import Image
    im = Image.open(p)
    w, h = im.size
    co_alpha = "A" in im.getbands()
    chunks = [(t, c) for t, c in _webp_chunks(d) if t not in (b"VP8X", b"EXIF", b"XMP ")]
    flags = 0x08 | 0x04 | (0x10 if co_alpha else 0)
    for t, c in chunks:
        if t == b"ICCP":
            flags |= 0x20
        if t == b"ANIM":
            flags |= 0x02
    vp8x = struct.pack("<B", flags) + b"\x00\x00\x00" + struct.pack("<I", w - 1)[:3] + struct.pack("<I", h - 1)[:3]
    chunks = [(b"VP8X", vp8x)] + chunks + [(b"EXIF", _exif_tiff(nam)), (b"XMP ", _xmp(nam))]
    body = b"".join(t + struct.pack("<I", len(c)) + c + (b"\x00" if len(c) & 1 else b"") for t, c in chunks)
    return b"RIFF" + struct.pack("<I", 4 + len(body)) + b"WEBP" + body


# ---------- PNG ----------
def _png_co_dau(p):
    from PIL import Image
    info = Image.open(p).info
    return DAU_ASCII in str(info.get("Copyright", "")) or DAU in str(info.get("XML:com.adobe.xmp", ""))


def _png(p, nam):
    from PIL import Image
    from PIL.PngImagePlugin import PngInfo
    im = Image.open(p)
    im.load()
    meta = PngInfo()
    meta.add_text("Author", CHU)
    meta.add_text("Copyright", _ban_quyen_ascii(nam))
    meta.add_itxt("XML:com.adobe.xmp", _xmp(nam).decode("utf-8"))
    tmp = p + ".tmp"
    im.save(tmp, "PNG", optimize=True, pnginfo=meta)
    os.replace(tmp, p)


def co_dau(p):
    lp = p.lower()
    try:
        if lp.endswith((".jpg", ".jpeg")):
            return _jpeg_co_dau(open(p, "rb").read())
        if lp.endswith(".webp"):
            return _webp_co_dau(open(p, "rb").read())
        if lp.endswith(".png"):
            return _png_co_dau(p)
    except Exception:
        return False
    return True                                    # định dạng khác: không kiểm


def dong_dau(p, nam=None, ep=False):
    """Đóng dấu 1 ảnh. Trả True nếu đã ghi. Ảnh đã có dấu thì bỏ qua (trừ ep=True)."""
    if not ep and co_dau(p):
        return False
    lp = p.lower()
    if lp.endswith((".jpg", ".jpeg")):
        d = open(p, "rb").read()
        if d[:2] != b"\xFF\xD8":
            return False
        moi = _jpeg(p, d, nam)
    elif lp.endswith(".webp"):
        d = open(p, "rb").read()
        if d[:4] != b"RIFF" or d[8:12] != b"WEBP":
            return False
        moi = _webp(p, d, nam)
    elif lp.endswith(".png"):
        _png(p, nam)
        return True
    else:
        return False
    tmp = p + ".tmp"
    open(tmp, "wb").write(moi)
    os.replace(tmp, p)
    return True


def gom(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            for dp, _, fns in os.walk(p):
                out += [os.path.join(dp, f) for f in fns if f.lower().endswith(DUOI)]
        elif p.lower().endswith(DUOI):
            out.append(p)
    return sorted(out)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = gom(args or ["images"])
    if "--kiem" in sys.argv:
        thieu = [f for f in files if not co_dau(f)]
        for f in thieu:
            print(f)
        print("%d/%d ảnh chưa có dấu" % (len(thieu), len(files)))
        sys.exit(1 if thieu else 0)
    n = 0
    for f in files:
        try:
            if dong_dau(f, ep="--ep" in sys.argv):
                n += 1
        except Exception as e:
            print("LỖI %s: %s" % (f, e))
    print("Đã đóng dấu %d/%d ảnh" % (n, len(files)))


if __name__ == "__main__":
    main()
