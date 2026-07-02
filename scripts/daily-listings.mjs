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

// ---- Prompt cho Claude (có web search) ----
const sys = `Bạn là biên tập viên của Nam Ban Villas — môi giới đất tại xã Nam Ban, Lâm Hà, Lâm Đồng.
Giọng: trầm, thật, đọc rủi ro, KHÔNG hô hào, KHÔNG tính từ rỗng ("tuyệt đẹp","lý tưởng").
Nhiệm vụ: tìm trên web các TIN RAO BÁN ĐẤT/NHÀ tại Nam Ban (Lâm Hà) mới nhất, chọn 1–2 tin CHẤT LƯỢNG
(có giá rõ, diện tích rõ, vị trí cụ thể, ưu tiên có sổ). Với mỗi tin, VIẾT LẠI bằng lời của mình (không copy nguyên văn),
2–4 câu, nêu: loại đất, diện tích, giá, vị trí, điểm đáng lưu ý + 1 rủi ro cần kiểm tra. TUYỆT ĐỐI KHÔNG ghi số điện thoại người bán.
${wantMarketNote ? 'Ngoài ra viết thêm 1 đoạn "quan sát thị trường" 2–3 câu về xu hướng đất Nam Ban tuần này (dựa trên tin thật).' : 'Hôm nay KHÔNG cần quan sát thị trường.'}
Chỉ dùng dữ kiện có thật từ kết quả tìm kiếm. Nếu không tìm được tin nào đạt chất lượng, trả listings rỗng.
TRẢ VỀ DUY NHẤT một JSON (không markdown, không giải thích) dạng:
{"listings":[{"title":"...","desc":"...","source":"URL"}],"marketNote":${wantMarketNote ? '"..."' : 'null'}}`;

const body = {
  model: MODEL,
  max_tokens: 1500,
  tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: 5 }],
  system: sys,
  messages: [{ role: 'user', content: `Hôm nay ${dmy}. Tìm tin rao đất Nam Ban mới và trả JSON theo yêu cầu.` }],
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
