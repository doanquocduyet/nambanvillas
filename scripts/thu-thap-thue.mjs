// Thu thập tin CHO THUÊ ở Nam Ban từ nguồn công khai.
//
// Vì sao tách riêng khỏi scrape-listings.mjs (thu tin BÁN): giá thuê tính theo
// tháng/đêm, lọc khác hẳn, và trộn chung một lần là hỏng cả hai. File này chỉ
// ghi ra data/tin-thue/, không đụng vào dữ liệu tin bán.
//
// Chạy: node scripts/thu-thap-thue.mjs
// Ghi:  data/tin-thue/<ngày>.json  +  data/tin-thue/log.md

import fs from 'node:fs';
import path from 'node:path';

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const HDRS = { 'User-Agent': UA, 'Accept': 'text/html,application/json', 'Accept-Language': 'vi,en;q=0.9' };
const iso = new Date().toISOString().slice(0, 10);
const OUT = 'data/tin-thue';

// Đúng vùng Nam Ban, loại trùng tên nơi khác (Gia Lâm Hà Nội, Mê Linh Hà Nội…)
function dungVung(t) {
  t = (t || '').toLowerCase();
  // Trùng tên nơi khác: Gia Lâm/Mê Linh ở Hà Nội, và ĐƯỜNG Mê Linh ở Đà Lạt
  if (t.includes('hà nội') || t.includes('bình thuận') || t.includes('huyện gia lâm')) return false;
  if (/(đường|phố|hẻm)\s*(mê linh|gia lâm|nam hà|đông thanh)/.test(t)) return false;
  // Huyện/thành khác trong Lâm Đồng — chỉ bỏ khi không hề nhắc Lâm Hà / Nam Ban
  const noiKhac = ['đà lạt', 'bảo lộc', 'đức trọng', 'di linh', 'đơn dương', 'lạc dương', 'đam rông', 'bảo lâm', 'cát tiên', 'đạ huoai', 'đạ tẻh'];
  if (noiKhac.some(k => t.includes(k)) && !t.includes('lâm hà') && !t.includes('nam ban')) return false;
  if (t.includes('nam ban') || t.includes('nam bàn')) return true;
  // "Lâm Đồng" một mình quá rộng — phải đúng huyện Lâm Hà
  const gan = ['đông thanh', 'mê linh', 'nam hà', 'gia lâm'].some(k => t.includes(k));
  return gan && t.includes('lâm hà');
}

// Phải thật sự là tin CHO THUÊ, không phải tin bán có nhắc chữ thuê
function laChoThue(t) {
  t = (t || '').toLowerCase();
  if (/\bbán\b/.test(t) && !/cho thuê|cần thuê|thuê nhà|thuê phòng/.test(t)) return false;
  return /cho thuê|thuê nhà|thuê phòng|thuê villa|thuê homestay|thuê mặt bằng|\/tháng|\/ tháng|một tháng|mỗi tháng/.test(t);
}

// Loại tài sản — quyết định nó thuộc nhánh nào của hub
function loaiTaiSan(t) {
  t = (t || '').toLowerCase();
  if (/homestay|farmstay|bungalow|cabin|lưu trú|theo đêm|\/đêm/.test(t)) return 'luu-tru';
  if (/mặt bằng|kinh doanh|văn phòng|kho|xưởng|quán|nhà hàng|showroom/.test(t)) return 'kinh-doanh';
  if (/villa|biệt thự/.test(t)) return 'villa';
  if (/phòng trọ|nhà trọ|thuê phòng|ký túc/.test(t)) return 'phong';
  if (/nhà vườn|vườn/.test(t)) return 'nha-vuon';
  if (/nhà|căn hộ|studio|nguyên căn/.test(t)) return 'nha';
  return 'khac';
}

// Giá thuê: trả về {so, donvi} — triệu/tháng hoặc nghìn/đêm
function bocGia(t) {
  t = (t || '').replace(/\s+/g, ' ');
  let m = t.match(/([\d.,]+)\s*(triệu|tr)\s*\/?\s*(tháng|th)\b/i);
  if (m) return { so: soThuc(m[1]), donvi: 'triệu/tháng' };
  m = t.match(/([\d.,]+)\s*(nghìn|k|đ|vnd)\s*\/?\s*(đêm|ngày)\b/i);
  if (m) {
    let v = soThuc(m[1]);
    // "600.000đ/đêm" ra 600000 đồng -> quy về nghìn cho cùng một thang đo
    if (v != null && v >= 1000) v = v / 1000;
    return { so: v, donvi: 'nghìn/đêm' };
  }
  m = t.match(/([\d.,]+)\s*(triệu|tr)\b/i);
  if (m) return { so: soThuc(m[1]), donvi: 'triệu/tháng' };
  return null;
}
function soThuc(v) {
  v = String(v).replace(/\.(?=\d{3}\b)/g, '').replace(/,(?=\d{3}\b)/g, '').replace(',', '.');
  const n = parseFloat(v);
  return Number.isFinite(n) ? n : null;
}
function dienTich(t) {
  const m = (t || '').match(/(\d{2,5})\s*m2|(\d{2,5})\s*m²/i);
  return m ? +(m[1] || m[2]) : null;
}
function soPhong(t) {
  const m = (t || '').match(/(\d{1,2})\s*(phòng ngủ|pn)\b/i);
  return m ? +m[1] : null;
}

const ra = [];
const log = [`\n## ${iso}`];

// ---- Chotot: dùng chính API công khai, đổi truy vấn sang "cho thuê" ----
async function chotot() {
  const truyVan = [
    'cho thuê nhà Nam Ban Lâm Hà',
    'cho thuê Nam Ban Lâm Đồng',
    'thuê phòng Nam Ban',
    'cho thuê nhà Mê Linh Lâm Hà',
  ];
  for (const q of truyVan) {
    const u = `https://gateway.chotot.com/v1/public/ad-listing?q=${encodeURIComponent(q)}&limit=30`;
    try {
      const r = await fetch(u, { headers: HDRS });
      if (!r.ok) { log.push(`- Chotot ${r.status} — "${q}"`); continue; }
      const j = await r.json();
      const ads = j.ads || j.data?.ads || [];
      let n = 0;
      for (const a of ads) {
        const blob = `${a.subject || ''} ${a.body || ''} ${a.area_name || ''} ${a.region_name || ''}`;
        if (!dungVung(blob) || !laChoThue(blob)) continue;
        const g = bocGia(`${a.price_string || ''} ${a.subject || ''} ${a.body || ''}`);
        ra.push({
          nguon: 'chotot',
          tieu_de: a.subject || '',
          loai: loaiTaiSan(blob),
          gia_so: g?.so ?? null,
          gia_donvi: g?.donvi ?? null,
          gia_goc: a.price_string || null,
          dien_tich_m2: a.size || dienTich(blob) || null,
          phong_ngu: a.rooms || soPhong(blob) || null,
          vi_tri: [a.ward_name, a.area_name, a.region_name].filter(Boolean).join(', '),
          ngay: a.list_time ? new Date(a.list_time).toISOString().slice(0, 10) : null,
          url: a.list_id ? `https://www.nhatot.com/${a.list_id}.htm` : '',
        });
        n++;
      }
      log.push(`- Chotot "${q}": ${ads.length} tin, ${n} khớp thuê Nam Ban`);
    } catch (e) {
      log.push(`- Chotot lỗi "${q}": ${e.message.slice(0, 70)}`);
    }
  }
}

// ---- Sàn HTML: bóc thô, chỉ lấy đoạn vừa đúng vùng vừa đúng là cho thuê ----
async function sanHtml(ten, url) {
  try {
    const r = await fetch(url, { headers: HDRS });
    log.push(`- ${ten}: HTTP ${r.status}`);
    if (!r.ok) return;
    const html = await r.text();
    const khoi = html.split(/<\/(?:article|li|div)>/i);
    let n = 0;
    for (const c of khoi) {
      const t = c.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      if (t.length < 40 || t.length > 600) continue;
      if (!dungVung(t) || !laChoThue(t)) continue;
      const g = bocGia(t);
      if (!g) continue;
      const href = (c.match(/href="(\/[^"]+)"/) || [])[1];
      ra.push({
        nguon: ten,
        tieu_de: t.slice(0, 120),
        loai: loaiTaiSan(t),
        gia_so: g.so, gia_donvi: g.donvi, gia_goc: null,
        dien_tich_m2: dienTich(t), phong_ngu: soPhong(t),
        vi_tri: 'Nam Ban, Lâm Hà, Lâm Đồng', ngay: iso,
        url: href ? new URL(href, url).href : url,
      });
      n++;
    }
    log.push(`  → ${n} tin khớp`);
  } catch (e) {
    log.push(`- ${ten} lỗi: ${e.message.slice(0, 70)}`);
  }
}

const main = async () => {
  await chotot();
  await sanHtml('batdongsan', 'https://batdongsan.com.vn/cho-thue-nha-rieng-xa-nam-ban-lam-ha');
  await sanHtml('guland', 'https://guland.vn/cho-thue-bat-dong-san-xa-nam-ban-lam-ha-lam-dong');

  // bỏ trùng theo url
  const thay = new Set();
  const sach = ra.filter(x => {
    const k = x.url || x.tieu_de;
    if (thay.has(k)) return false;
    thay.add(k); return true;
  });

  fs.mkdirSync(OUT, { recursive: true });
  fs.writeFileSync(path.join(OUT, `${iso}.json`), JSON.stringify(sach, null, 2), 'utf8');

  const dem = {};
  for (const x of sach) dem[x.loai] = (dem[x.loai] || 0) + 1;
  log.push(`### TỔNG: ${sach.length} tin cho thuê — ${JSON.stringify(dem)}`);
  fs.appendFileSync(path.join(OUT, 'log.md'), log.join('\n') + '\n', 'utf8');
  console.log(log.join('\n'));
};
main();
