// extract-video.mjs — Bóc metadata từ 1 link video (YouTube/TikTok) qua oEmbed chính thức (miễn phí, không cần key).
// Dùng cho luồng "gửi link → bóc": node scripts/extract-video.mjs <url>
// Trả về: tiêu đề (caption) + tác giả/kênh. KHÔNG tải video/ảnh. Từ đó người/bot viết tin theo FORM-DANG-TIN.md.

const url = process.argv[2];
if (!url) { console.error('Cách dùng: node scripts/extract-video.mjs <link YouTube/TikTok>'); process.exit(1); }

function endpoint(u) {
  if (/tiktok\.com/.test(u)) return `https://www.tiktok.com/oembed?url=${encodeURIComponent(u)}`;
  if (/youtube\.com|youtu\.be/.test(u)) return `https://www.youtube.com/oembed?url=${encodeURIComponent(u)}&format=json`;
  return null;
}

const ep = endpoint(url);
if (!ep) { console.error('Chỉ hỗ trợ link YouTube/TikTok.'); process.exit(1); }

try {
  const r = await fetch(ep, { headers: { 'user-agent': 'Mozilla/5.0' } });
  if (!r.ok) { console.error('oEmbed lỗi', r.status); process.exit(1); }
  const j = await r.json();
  console.log(JSON.stringify({
    nguon: url,
    tieu_de_caption: j.title || '',
    kenh_tac_gia: j.author_name || '',
    // caption TikTok/YouTube của tin đất thường có giá/diện tích/vị trí — bóc từ đây, viết lại theo FORM.
  }, null, 2));
} catch (e) { console.error('Lỗi:', e.message); process.exit(1); }
