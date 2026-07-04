// daily-listings.mjs — Mỗi ngày: dùng Claude API (có web search) tìm 1–2 tin rao đất Nam Ban
// chất lượng, viết lại theo giọng Nam Ban Villas (bỏ SĐT người bán), chèn vào trang tin-rao.
// Mỗi >=3 ngày thêm 1 khối "quan sát thị trường".
// Fail-safe: nếu API lỗi hoặc không có tin mới → thoát sạch, KHÔNG sửa file (không commit rác).

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import path from 'path';

const ROOT = process.cwd();
const PAGE = path.join(ROOT, 'thi-truong', 'tin-rao-dat-nam-ban-moi', 'index.html');
const STATE = path.join(ROOT, 'data', 'tin-rao-state.json');
const KEY = process.env.ANTHROPIC_API_KEY;
const YT_KEY = process.env.YOUTUBE_API_KEY;   // tùy chọn — có thì quét thêm YouTube
const MODEL = process.env.CLAUDE_MODEL || 'claude-sonnet-5';
const MAX_DAYS = 20; // giữ tối đa 20 mục ngày gần nhất

if (!KEY) { console.error('Thiếu ANTHROPIC_API_KEY — bỏ qua.'); process.exit(0); }

const today = new Date();
const iso = today.toISOString().slice(0, 10);            // 2026-07-02
const dmy = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;

// ---- State: lần cuối ra "quan sát thị trường" ----
let state = { lastMarketNote: null };
try { if (existsSync(STATE)) state = JSON.parse(readFileSync(STATE, 'utf8')); } catch {}
const daysSinceNote = state.lastMarketNote
  ? Math.round((today - new Date(state.lastMarketNote)) / 86400000)
  : 99;
const wantMarketNote = daysSinceNote >= 3;

// ---- Quét YouTube (tùy chọn, fail-safe) ----
// Lấy video môi giới/chủ đất đăng gần đây; mô tả video thường có giá/diện tích/vị trí.
async function fetchYouTube() {
  if (!YT_KEY) return '';
  const since = new Date(today.getTime() - 3 * 86400000).toISOString(); // 3 ngày gần nhất
  const queries = ['bán đất Nam Ban', 'đất Nam Ban Lâm Hà', 'đất vườn Nam Ban', 'bán đất Lâm Hà Lâm Đồng',
                   'đất Đông Thanh Lâm Hà', 'đất Mê Linh Nam Ban', 'đất Nam Ban view Đà Lạt', 'đất nền Nam Ban sổ đỏ'];
  const seen = new Set(); const ids = [];
  try {
    for (const q of queries) {
      const u = `https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&order=date&maxResults=8&publishedAfter=${encodeURIComponent(since)}&q=${encodeURIComponent(q)}&key=${YT_KEY}`;
      const r = await fetch(u); if (!r.ok) continue;
      const j = await r.json();
      for (const it of (j.items || [])) { const id = it.id?.videoId; if (id && !seen.has(id)) { seen.add(id); ids.push(id); } }
    }
    if (!ids.length) return '';
    // Lấy mô tả đầy đủ
    const vu = `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${ids.slice(0, 25).join(',')}&key=${YT_KEY}`;
    const vr = await fetch(vu); if (!vr.ok) return '';
    const vj = await vr.json();
    const lines = (vj.items || []).map(v => {
      const s = v.snippet || {};
      const desc = (s.description || '').replace(/\s+/g, ' ').slice(0, 400);
      return `- [${s.channelTitle}] ${s.title} | ${desc} | https://www.youtube.com/watch?v=${v.id}`;
    });
    return lines.length ? `\n\nNGUỒN VIDEO YOUTUBE (mới, môi giới/chủ đất đăng — bóc giá/diện tích/vị trí từ mô tả; source phải là link video, ghi kênh):\n${lines.join('\n')}` : '';
  } catch (e) { console.error('YouTube lỗi (bỏ qua):', e.message); return ''; }
}
const ytBlock = await fetchYouTube();

// ---- Prompt cho Claude (có web search) ----
const sys = `Bạn là biên tập viên Nam Ban Villas (môi giới đất xã Nam Ban, Lâm Hà, Lâm Đồng). Viết theo đúng FORM-DANG-TIN.md.

LỌC — tin tốt phải đủ ≥4/7 dữ kiện: diện tích · kích thước/mặt tiền · thổ cư(m²) · giá bằng số · vị trí cụ thể (gần mốc nào) · loại đường · pháp lý(sổ). Ưu tiên tin đủ 6–7.
LOẠI THẲNG tin chứa từ rác: "chắc chắn lời/lời ngay/mua là thắng/x2 tài khoản/sinh lời khủng", "sốt đất/siêu hiếm/cực phẩm/độc nhất/giá sốc/rẻ nhất", "siêu phẩm/đất vàng/vị trí vàng", "ngộp bank/cắt lỗ sâu/bán tháo gấp" — hoặc không giá, mơ hồ vị trí. Chọn 1–2 tin tốt nhất. Không đủ chất → listings rỗng (thà trống hơn rác).

NGUỒN: dùng cả (a) web search tin rao chữ, (b) VIDEO YouTube/TikTok. Với web search, thử thêm truy vấn "đất Nam Ban site:youtube.com" và "đất Nam Ban site:tiktok.com". Nếu có khối NGUỒN VIDEO YOUTUBE bên dưới, ưu tiên bóc từ mô tả video. Với tin từ video: source = LINK VIDEO, và desc ghi rõ "Nguồn: video kênh [tên kênh]".

VIẾT (viết lại bằng lời mình, KHÔNG copy nguyên văn):
- title: "Loại đất + diện tích + đặc điểm mạnh nhất + khu — thổ cư/giá".
- desc: 2–3 câu — đặc điểm nổi bật + hợp ai + BẮT BUỘC 1 rủi ro cần kiểm; kết bằng "Tin thị trường, chưa kiểm chứng."
- Số thật từ kết quả tìm kiếm/mô tả video, KHÔNG bịa. TUYỆT ĐỐI KHÔNG lấy số điện thoại/tên người bán/ảnh/video.

GIỌNG: trầm, thật, đọc rủi ro, KHÔNG hô hào. CẤM tính từ rỗng (tuyệt đẹp, lý tưởng, hoàn hảo, siêu phẩm, cực hiếm, số 1, giá sốc). Không đụng chạm ai.

${wantMarketNote ? 'Thêm 1 đoạn "quan sát thị trường" 2–3 câu về xu hướng đất Nam Ban tuần này (dựa trên tin/tín hiệu thật).' : 'Hôm nay KHÔNG cần quan sát thị trường.'}

TRẢ VỀ DUY NHẤT một JSON (không markdown, không lời dẫn):
{"listings":[{"title":"...","desc":"...","source":"URL"}],"marketNote":${wantMarketNote ? '"..."' : 'null'}}`;

const body = {
  model: MODEL,
  max_tokens: 1500,
  tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: 5 }],
  system: sys,
  messages: [{ role: 'user', content: `Hôm nay ${dmy}. Tìm tin rao đất Nam Ban mới (web + video YouTube/TikTok) và trả JSON theo yêu cầu.${ytBlock}` }],
};

let data;
try {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) { console.error('API lỗi', res.status, await res.text()); process.exit(0); }
  const json = await res.json();
  const text = (json.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) { console.error('Không parse được JSON:', text.slice(0, 300)); process.exit(0); }
  data = JSON.parse(m[0]);
} catch (e) { console.error('Lỗi gọi API:', e.message); process.exit(0); }

const listings = Array.isArray(data.listings) ? data.listings.filter(l => l && l.title && l.desc) : [];
if (!listings.length && !data.marketNote) { console.log('Không có tin đạt chất lượng hôm nay — không cập nhật.'); process.exit(0); }

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// ---- Dựng khối HTML ngày mới ----
let block = `        <!-- DAY:${iso} -->\n        <h2>Ngày ${dmy}</h2>\n`;
if (listings.length) {
  block += `        <ul style="line-height:1.9;color:#3D3D3D;font-size:.95rem">\n`;
  for (const l of listings) {
    const src = l.source ? ` <a href="${esc(l.source)}" target="_blank" rel="nofollow noopener">Nguồn</a>` : '';
    block += `          <li><strong>${esc(l.title)}</strong> — ${esc(l.desc)}${src}</li>\n`;
  }
  block += `        </ul>\n`;
}
if (data.marketNote) {
  block += `        <p style="background:#F0F4F1;border-radius:8px;padding:12px 16px;font-size:.92rem;color:#3D3D3D"><strong style="color:#1A3D2B">Quan sát thị trường:</strong> ${esc(data.marketNote)}</p>\n`;
}

// ---- Chèn vào trang giữa 2 marker, giữ tối đa MAX_DAYS mục ----
let html = readFileSync(PAGE, 'utf8');
const START = '<!-- DAILY-DIGEST:START';
const END = '<!-- DAILY-DIGEST:END -->';
const si = html.indexOf(START), ei = html.indexOf(END);
if (si === -1 || ei === -1) { console.error('Không thấy marker DAILY-DIGEST'); process.exit(0); }
const startLineEnd = html.indexOf('\n', si) + 1;
const head = html.slice(0, startLineEnd);
let mid = html.slice(startLineEnd, ei);
const tail = html.slice(ei);

// Nếu đã có mục hôm nay → thay thế, tránh trùng
mid = mid.replace(new RegExp(`\\s*<!-- DAY:${iso} -->[\\s\\S]*?(?=<!-- DAY:|$)`), '\n');

// Trim: giữ MAX_DAYS block gần nhất
const days = mid.split(/(?=<!-- DAY:)/).filter(s => s.includes('<!-- DAY:'));
const kept = days.slice(0, MAX_DAYS - 1).join('');
mid = '\n' + block + '\n' + kept;

// Cập nhật dateModified + article-cat
let out = head + mid + tail;
out = out.replace(/"dateModified":"[^"]*"/, `"dateModified":"${iso}"`);
out = out.replace(/(<p class="article-cat">Quan sát thị trường · Cập nhật )[^<]*/, `$1${dmy}`);
writeFileSync(PAGE, out, 'utf8');

// Lưu state
mkdirSync(path.dirname(STATE), { recursive: true });
if (data.marketNote) state.lastMarketNote = iso;
state.lastRun = iso;
writeFileSync(STATE, JSON.stringify(state, null, 2), 'utf8');

console.log(`Cập nhật ${dmy}: ${listings.length} tin${data.marketNote ? ' + quan sát thị trường' : ''}.`);
