// build-feed.mjs — Tạo RSS feed (feed.xml) từ các bài viết & tin đăng
// Chạy: node scripts/build-feed.mjs
// Dùng để: web có feed chuẩn -> tự động đồng bộ sang Facebook/Zalo/Telegram
// qua công cụ như Make/Zapier (không phải đăng tay), và để người đọc theo dõi.

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';

const SITE = 'https://nambanvillas.vn';
const ROOT = process.cwd();

// Các thư mục chứa bài viết / tin đăng cần đưa vào feed
const SECTIONS = ['thi-truong', 've-nam-ban', 'namban-notes', 'dat-nen', 'nha-ban'];

function extract(html, re) {
  const m = html.match(re);
  return m ? m[1].trim() : '';
}

function getDate(html) {
  // Ưu tiên datePublished trong JSON-LD
  let d = extract(html, /"datePublished"\s*:\s*"([^"]+)"/);
  if (d) return new Date(d);
  // Hoặc thẻ article:published_time
  d = extract(html, /property="article:published_time"\s+content="([^"]+)"/);
  if (d) return new Date(d);
  return null;
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

const items = [];

for (const section of SECTIONS) {
  const dir = join(ROOT, section);
  if (!existsSync(dir)) continue;
  for (const slug of readdirSync(dir)) {
    const file = join(dir, slug, 'index.html');
    if (!existsSync(file)) continue;
    const html = readFileSync(file, 'utf8');

    let title = extract(html, /<title>([^<]+)<\/title>/);
    title = title.replace(/\s*[|–-]\s*(Nam Ban Villas|Namban Notes)\s*$/i, '').trim();
    const desc = extract(html, /<meta name="description" content="([^"]+)"/);
    const canonical = extract(html, /<link rel="canonical" href="([^"]+)"/) || `${SITE}/${section}/${slug}/`;
    let date = getDate(html);
    if (!date || isNaN(date)) date = statSync(file).mtime;

    items.push({ title, desc, url: canonical, date, section });
  }
}

// Sắp xếp mới nhất trước, giới hạn 40 mục
items.sort((a, b) => b.date - a.date);
const top = items.slice(0, 40);

const now = new Date().toUTCString();
const xmlItems = top.map(it => `    <item>
      <title>${esc(it.title)}</title>
      <link>${esc(it.url)}</link>
      <guid isPermaLink="true">${esc(it.url)}</guid>
      <category>${esc(it.section)}</category>
      <description>${esc(it.desc)}</description>
      <pubDate>${it.date.toUTCString()}</pubDate>
    </item>`).join('\n');

const feed = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Nam Ban Villas — Đất nền, nhà bán &amp; thị trường Nam Ban</title>
    <link>${SITE}/</link>
    <atom:link href="${SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Tin mới nhất về đất nền, nhà bán, thị trường và đời sống tại Nam Ban, Lâm Đồng.</description>
    <language>vi-VN</language>
    <lastBuildDate>${now}</lastBuildDate>
${xmlItems}
  </channel>
</rss>
`;

writeFileSync(join(ROOT, 'feed.xml'), feed, 'utf8');
console.log(`feed.xml tạo xong với ${top.length} mục.`);
