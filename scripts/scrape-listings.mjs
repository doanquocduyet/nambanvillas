// scrape-listings.mjs — Bản MIỄN PHÍ (không cần API key).
// Chạy trên GitHub Actions (internet mở) mỗi sáng: đọc các sàn BĐS, bóc tin đất Nam Ban thô,
// ghi vào data/tin-thu-thap/<ngày>.json + log. KHÔNG publish lên web (chờ phiên duyệt + viết chuẩn).
// Fail-safe: nguồn nào lỗi thì bỏ qua, luôn ghi log để biết nguồn nào chạy được.

import { writeFileSync, mkdirSync, existsSync, appendFileSync } from 'fs';
import path from 'path';

const ROOT = process.cwd();
const OUTDIR = path.join(ROOT, 'data', 'tin-thu-thap');
if (!existsSync(OUTDIR)) mkdirSync(OUTDIR, { recursive: true });

const today = new Date();
const iso = today.toISOString().slice(0, 10);
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const HDRS = { 'User-Agent': UA, 'Accept': 'text/html,application/json', 'Accept-Language': 'vi,en;q=0.9' };

function relevant(txt) {
  const t = (txt || '').toLowerCase();
  if (t.includes('hà nội') || t.includes('bình thuận') || t.includes('huyện gia lâm')) return false; // loại trùng tên khác tỉnh
  if (t.includes('nam ban') || t.includes('nam bàn')) return true;
  const near = ['đông thanh', 'mê linh', 'nam hà', 'gia lâm'].some(k => t.includes(k));
  return near && (t.includes('lâm hà') || t.includes('lâm đồng'));
}
function num(s){ const m=(s||'').replace(/[.,]/g,'').match(/\d+/); return m?+m[0]:null; }

const results = [];
const log = [`\n## ${iso}`];

// ---- Nguồn 1: Chotot public API (JSON, không cần key) ----
async function chotot() {
  const urls = [
    'https://gateway.chotot.com/v1/public/ad-listing?q=%C4%91%E1%BA%A5t%20Nam%20Ban%20L%C3%A2m%20H%C3%A0&limit=30&cg=1000&st=s,k',
    'https://gateway.chotot.com/v1/public/ad-listing?q=%C4%91%E1%BA%A5t%20Nam%20Ban&limit=30&cg=1000',
  ];
  for (const u of urls) {
    try {
      const r = await fetch(u, { headers: HDRS });
      if (!r.ok) { log.push(`- Chotot ${r.status} ${u.slice(0,60)}`); continue; }
      const j = await r.json();
      const ads = j.ads || j.data?.ads || [];
      let n = 0;
      for (const a of ads) {
        const blob = `${a.subject||''} ${a.body||''} ${a.area_name||''} ${a.region_name||''}`;
        if (!relevant(blob)) continue;
        results.push({
          source: 'chotot',
          title: a.subject || '',
          area_m2: a.size || a.land_area || null,
          price: a.price_string || (a.price ? a.price : null),
          location: [a.ward_name, a.area_name, a.region_name].filter(Boolean).join(', '),
          date: a.list_time ? new Date(a.list_time).toISOString().slice(0,10) : null,
          url: a.list_id ? `https://www.nhatot.com/${a.list_id}.htm` : (a.ad_id?`https://www.nhatot.com/mua-ban-${a.ad_id}.htm`:''),
        });
        n++;
      }
      log.push(`- Chotot OK: ${ads.length} tin, ${n} khớp Nam Ban`);
      if (n) return;
    } catch (e) { log.push(`- Chotot lỗi: ${e.message.slice(0,80)}`); }
  }
}

// ---- Nguồn 2-4: HTML sàn — bóc thô bằng regex ----
async function scrapeHtml(name, url) {
  try {
    const r = await fetch(url, { headers: HDRS });
    log.push(`- ${name}: HTTP ${r.status}`);
    if (!r.ok) return;
    const html = await r.text();
    // tách theo thẻ tin (thô): tìm các đoạn có m² + giá gần nhau
    const chunks = html.split(/<\/(?:article|li|div)>/i);
    let n = 0;
    for (const c of chunks) {
      const text = c.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      if (!relevant(text)) continue;
      const area = text.match(/(\d{2,4})\s*m²|(\d{2,4})\s*m2/i);
      const price = text.match(/(\d+([.,]\d+)?)\s*(tỷ|triệu)/i);
      if (!area || !price) continue;
      const href = (c.match(/href="([^"]+)"/) || [])[1] || '';
      results.push({
        source: name,
        title: text.slice(0, 120),
        area_m2: num(area[0]),
        price: price[0],
        location: 'Nam Ban / Lâm Hà (thô)',
        date: null,
        url: href.startsWith('http') ? href : (href ? new URL(href, url).href : ''),
      });
      n++;
      if (n >= 15) break;
    }
    log.push(`  → ${n} tin khớp`);
  } catch (e) { log.push(`- ${name} lỗi: ${e.message.slice(0,80)}`); }
}

await chotot();
await scrapeHtml('batdongsan', 'https://batdongsan.com.vn/ban-dat-thi-tran-nam-ban');
await scrapeHtml('guland', 'https://guland.vn/mua-ban-bat-dong-san-thi-tran-nam-ban-huyen-lam-ha-lam-dong');
await scrapeHtml('homedy', 'https://homedy.com/ban-dat-thi-tran-nam-ban-huyen-lam-ha-lam-dong');

// ---- Dedupe thô theo (area+price) ----
const seen = new Set();
const uniq = results.filter(r => {
  const k = `${r.area_m2}|${r.price}`;
  if (seen.has(k)) return false; seen.add(k); return true;
});

writeFileSync(path.join(OUTDIR, `${iso}.json`), JSON.stringify(uniq, null, 2));
log.push(`### TỔNG: ${uniq.length} tin thô (đã gộp trùng)`);
appendFileSync(path.join(OUTDIR, 'log.md'), log.join('\n') + '\n');
console.log(`Thu thập ${uniq.length} tin thô → data/tin-thu-thap/${iso}.json`);
console.log(log.join('\n'));
