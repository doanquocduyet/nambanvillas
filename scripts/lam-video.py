#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tự dựng video dọc 9:16 (TikTok / Reels / YouTube Shorts) từ ảnh + thông số của 1 lô.
Không nhạc (an toàn bản quyền). Chữ tiếng Việt có dấu. Xuất file .mp4.

Dùng:  python3 scripts/lam-video.py <đường-dẫn-thư-mục-tin> [file-ra.mp4]
Ví dụ: python3 scripts/lam-video.py nha-ban/moc-home-nam-ban video-moc-home.mp4
"""
import os, re, sys, subprocess, tempfile, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import listing_common as lc

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1080, 1920
SEC_PER = 3.0            # giây mỗi ảnh
FPS = 30
GREEN = (26, 61, 43)
GOLD = (201, 168, 76)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
HOTLINE = "0938 227 988"
WEB = "nambanvillas.vn"


def ff():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def font(sz, bold=True):
    return ImageFont.truetype(FONTB if bold else FONT, sz)


def read_listing(folder):
    f = ROOT / folder / "index.html"
    html = f.read_text(encoding="utf-8", errors="ignore")
    slug = folder.rstrip("/").split("/")[-1]
    imgs = [ROOT / rel for rel in lc.gallery_rels(html, slug) if (ROOT / rel).exists()]
    return {"title": lc.og(html, "og:title"), "images": imgs, "specs": lc.extract_specs(html)}


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def cover(img_path):
    """Cắt ảnh phủ kín khung 9:16."""
    im = Image.open(img_path).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def grad_bottom(im, h=760):
    """Phủ tối dần từ dưới lên để chữ nổi."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(h):
        a = int(210 * (i / h) ** 1.3)
        d.line([(0, H - i), (W, H - i)], fill=(10, 20, 14, a))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")


def badge(d, x, y, text, fnt, pad=22, bg=GREEN, fg=(255, 255, 255)):
    w = d.textlength(text, font=fnt)
    asc, desc = fnt.getmetrics()
    h = asc + desc
    d.rounded_rectangle([x, y, x + w + pad * 2, y + h + pad * 1.2], radius=18, fill=bg)
    d.text((x + pad, y + pad * 0.55), text, font=fnt, fill=fg)
    return h + pad * 1.2


def frame_intro(listing):
    im = grad_bottom(cover(listing["images"][0]))
    d = ImageDraw.Draw(im)
    # nhãn thương hiệu trên cùng
    badge(d, 60, 70, "NAM BAN VILLAS", font(40), bg=(255, 255, 255), fg=GREEN)
    # tiêu đề dưới
    title = listing["title"].split("–")[0].split("-")[0].strip() or listing["title"]
    lines = wrap(d, title, font(70), W - 130)[:3]
    y = H - 520
    for ln in lines:
        d.text((60, y), ln, font=font(70), fill=(255, 255, 255))
        y += 92
    # giá nếu có
    price = next((v for k, v in listing["specs"] if k.lower().startswith("giá")), "")
    if price:
        y += 20
        badge(d, 60, y, "Giá  " + price, font(58), bg=GOLD, fg=GREEN)
    return im


def frame_spec(img_path, pairs):
    im = grad_bottom(cover(img_path))
    d = ImageDraw.Draw(im)
    y = H - 130 - len(pairs) * 108
    for k, v in pairs:
        d.text((60, y), k.upper(), font=font(38, False), fill=(210, 225, 214))
        d.text((60, y + 44), v, font=font(60), fill=(255, 255, 255))
        y += 108
    return im


def frame_cta(listing):
    base = cover(listing["images"][0]).filter(ImageFilter.GaussianBlur(14))
    ov = Image.new("RGBA", (W, H), (10, 20, 14, 170))
    im = Image.alpha_composite(base.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)

    def center(text, fnt, y, fill):
        w = d.textlength(text, font=fnt)
        d.text(((W - w) / 2, y), text, font=fnt, fill=fill)

    center("Xem đất tận nơi – nói thẳng nên hay không", font(46), 620, (255, 255, 255))
    center("Gọi / Zalo", font(52), 780, (210, 225, 214))
    center(HOTLINE, font(120), 850, GOLD)
    # nút giả
    bw, bh = 620, 130
    bx = (W - bw) / 2
    d.rounded_rectangle([bx, 1050, bx + bw, 1050 + bh], radius=28, fill=(255, 255, 255))
    tw = d.textlength(WEB, font=font(56))
    d.text(((W - tw) / 2, 1082), WEB, font=font(56), fill=GREEN)
    return im


def build_frames(listing, tmp):
    frames = [frame_intro(listing)]
    specs = [p for p in listing["specs"] if not p[0].lower().startswith("giá")]
    imgs = listing["images"][1:] or listing["images"]
    # chia thông số cho các ảnh, mỗi ảnh 2 dòng
    chunks = [specs[i:i + 2] for i in range(0, len(specs), 2)] or [[]]
    for i, img in enumerate(imgs):
        frames.append(frame_spec(img, chunks[i % len(chunks)]))
    frames.append(frame_cta(listing))
    paths = []
    for i, fr in enumerate(frames):
        p = tmp / f"f{i:02d}.png"
        fr.save(p)
        paths.append(p)
    return paths


def encode(paths, out):
    # mỗi ảnh SEC_PER giây, nối bằng fade. (Không zoompan — tránh lỗi nhân khung.)
    n = len(paths)
    inputs = []
    for p in paths:
        inputs += ["-loop", "1", "-t", str(SEC_PER), "-i", str(p)]
    parts = [f"[{i}:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[v{i}]" for i in range(n)]
    fade = 0.4
    cur = "v0"
    xf = []
    off = SEC_PER - fade
    for i in range(1, n):
        o = f"m{i}"
        xf.append(f"[{cur}][v{i}]xfade=transition=fade:duration={fade}:offset={off:.2f}[{o}]")
        cur = o
        off += SEC_PER - fade
    filt = ";".join(parts + (xf if n > 1 else []))
    last = cur if n > 1 else "v0"
    cmd = [ff(), "-y", *inputs, "-filter_complex", filt, "-map", f"[{last}]",
           "-c:v", "libx264", "-profile:v", "high", "-level", "4.0",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-crf", "23",
           "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main():
    if len(sys.argv) < 2:
        print("Cần: python3 scripts/lam-video.py <thư-mục-tin> [ra.mp4]")
        return 1
    folder = sys.argv[1].strip("/")
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / f"video-{folder.split('/')[-1]}.mp4"
    listing = read_listing(folder)
    if not listing["images"]:
        print("Không tìm thấy ảnh cho tin này.")
        return 1
    with tempfile.TemporaryDirectory() as td:
        paths = build_frames(listing, pathlib.Path(td))
        encode(paths, out)
    print("XONG:", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
