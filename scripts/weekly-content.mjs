// weekly-content.mjs — Mỗi tuần: dùng Claude API (web search) research 1 keyword giao dịch Villas
// còn trống → viết 1 bài SEO/AEO đầy đủ → LƯU DẠNG NHÁP (noindex, KHÔNG vào sitemap) chờ chú duyệt.
// 4 chốt cứng không đụng key Panorama/Greenspace: (1) allowlist keyword, (2) blocklist chủ đề,
// (3) chống trùng slug đã có, (4) prompt khắc luật + lọc internal link (cấm Panorama).
// Fail-safe: API lỗi / không đạt chất lượng → thoát sạch, KHÔNG commit rác.

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import path from 'path';

const ROOT = process.cwd();
const TT = path.join(ROOT, 'thi-truong');
const VE = path.join(ROOT, 've-nam-ban');
const QUEUE = path.join(ROOT, 'data', 'content-queue.json');
const KEY = process.env.ANTHROPIC_API_KEY;
const MODEL = process.env.CLAUDE_MODEL || 'claude-sonnet-5';
if (!KEY) { console.error('Thiếu ANTHROPIC_API_KEY — bỏ qua.'); process.exit(0); }

// ─────────────────────────────────────────────────────────────
// (1) ALLOWLIST — CHỈ key giao dịch trực tiếp + rao bán của Villas.
//     Máy chỉ được chọn chủ đề từ đây, không tự nghĩ chủ đề tự do.
// ─────────────────────────────────────────────────────────────
const ALLOW = [
  { slug: 'dat-nam-ban',                kw: 'đất Nam Ban',                    title: 'Đất Nam Ban 2026: Giá, Khu Đang Bán, Pháp Lý & Cách Mua Không Dính Bẫy' },
  { slug: 'dat-nen-nam-ban-gia',        kw: 'đất nền Nam Ban',                title: 'Đất Nền Nam Ban 2026: Bảng Giá Theo Khu, Sổ Riêng Thổ Cư & Điều Cần Kiểm' },
  { slug: 'dat-nam-ban-gia-re',         kw: 'đất Nam Ban giá rẻ',             title: 'Đất Nam Ban Giá Rẻ Là Đất Gì? Rẻ Thật Hay Có Bẫy, 4 Điều Phải Kiểm' },
  { slug: 'dat-ngop-nam-ban',           kw: 'đất ngộp Nam Ban',               title: 'Đất Ngộp Nam Ban Là Gì? Mua Có Thật Sự Hời Không & Cách Không Dính Bẫy' },
  { slug: 'mua-ban-dat-nam-ban',        kw: 'mua bán đất Nam Ban',            title: 'Mua Bán Đất Nam Ban 2026: Quy Trình, Giấy Tờ, Chi Phí Sang Tên' },
  { slug: 'ban-dat-nam-ban-nhanh',      kw: 'bán đất Nam Ban',                title: 'Bán Đất Nam Ban Nhanh: Định Giá Đúng, Giấy Tờ Cần Có, Sang Tên Gọn' },
  { slug: 'dat-nam-ban-so-rieng',       kw: 'đất Nam Ban sổ riêng',           title: 'Đất Nam Ban Sổ Riêng vs Chưa Tách Thửa: Khác Gì, Mua Loại Nào An Toàn' },
  { slug: 'dat-nam-ban-tho-cu',         kw: 'đất thổ cư Nam Ban',             title: 'Đất Thổ Cư Nam Ban: Bao Nhiêu m² Đất Ở, Xây Được Không, Kiểm Trên Sổ Sao' },
  { slug: 'dat-nen-f0-nam-ban',         kw: 'đất nền F0 Nam Ban',             title: 'Đất Nền F0 Nam Ban Là Gì? Mua Sao Cho Đúng, Rủi Ro & Checklist' },
  { slug: 'giay-to-mua-dat-nam-ban',    kw: 'giấy tờ mua đất Nam Ban',        title: 'Mua Đất Nam Ban Cần Giấy Tờ Gì? Checklist Pháp Lý Trước Khi Cọc' },
];

// ─────────────────────────────────────────────────────────────
// (2) BLOCKLIST — nếu chủ đề/nội dung lỡ chạm cụm ĐỘC QUYỀN của web khác → loại.
//     Panorama: đời sống/du lịch/quy hoạch-bàn-luận/"có nên-có đáng". Greenspace: trông coi/quản lý đất.
// ─────────────────────────────────────────────────────────────
const BLOCK_TOPIC = /trông coi|trông giữ|giữ đất|quản lý đất|kiểm tra ranh|cắm mốc|giữ ranh|báo cáo gps|du lịch|quán cà phê|săn mây|thác voi|có gì chơi|ăn gì|có đáng sống|có nên sống|homestay có nên|review/i;

// ─────────────────────────────────────────────────────────────
// (3) CHỐNG TRÙNG — đọc slug đã có trong /thi-truong/ + /ve-nam-ban/ + queue.
// ─────────────────────────────────────────────────────────────
const dirSlugs = d => (existsSync(d) ? readdirSync(d, { withFileTypes: true }).filter(e => e.isDirectory()).map(e => e.name) : []);
const existing = new Set([...dirSlugs(TT), ...dirSlugs(VE)]);

let queue = { done: [], drafts: [] };
try { if (existsSync(QUEUE)) queue = { done: [], drafts: [], ...JSON.parse(readFileSync(QUEUE, 'utf8')) }; } catch {}
const doneSlugs = new Set([...(queue.done || []), ...(queue.drafts || []).map(d => d.slug)]);

// Chọn keyword đầu tiên trong allowlist chưa có bài + chưa nháp
const pick = ALLOW.find(a => !existing.has(a.slug) && !doneSlugs.has(a.slug));
if (!pick) { console.log('Hết keyword trống trong allowlist — không viết mới.'); process.exit(0); }

// ─────────────────────────────────────────────────────────────
// (4) PROMPT khắc luật thương hiệu + intent Villas.
// ─────────────────────────────────────────────────────────────
const today = new Date();
const iso = today.toISOString().slice(0, 10);
const dmy = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;

// Số thật bất biến để máy bám, KHÔNG bịa ngoài khung này:
const FACTS = `SỐ THẬT BẤT BIẾN (chỉ dùng trong khung này, KHÔNG bịa số ngoài):
- Giá đất Nam Ban ~2–7 triệu/m² (nền thổ cư 3–7; vườn nông nghiệp 0,2–3; view cao hơn nền cùng khu ~10–30%). Giá chốt thấp hơn giá rao 5–15%.
- Cụm đang mở: Đông Thanh quanh 500–600tr/nền; Mê Linh dưới 600tr/nền; Từ Liêm từ 650tr/nền; Tầm Xá F0 sổ sẵn từ 1,15 tỷ/lô. Tất cả sổ riêng, sẵn thổ cư.
- Vị trí: xã Nam Ban, Lâm Hà, Lâm Đồng; cách Đà Lạt ~25–28km (35–40 phút đèo Tà Nung); sân bay Liên Khương ~22km; cao 850–1.000m; 18–22°C.
- Hành chính: từ 1/7/2025 là "xã Nam Ban" (sáp nhập TT Nam Ban + Đông Thanh + Mê Linh + Gia Lâm).
- Thị trường: 2023–2025 tăng nóng (~40–60% năm 2025) → 2026 điều chỉnh, chọn lọc. Thanh khoản vùng ven chậm hơn đô thị.`;

const sys = `Bạn là biên tập viên Nam Ban Villas — môi giới đất THẬT tại xã Nam Ban, Lâm Hà, Lâm Đồng. Viết 1 bài SEO/AEO cho web nambanvillas.vn (web GIAO DỊCH: mua/bán/giá/lô/pháp lý giao dịch).

CHỦ ĐỀ BÀI: "${pick.kw}". Tiêu đề: "${pick.title}".

LUẬT INTENT (bất biến — web khác giữ cụm này, TUYỆT ĐỐI KHÔNG lấn):
- CHỈ viết góc GIAO DỊCH: giá, khu đang bán, sổ/thổ cư, pháp lý mua bán, quy trình, checklist, rủi ro khi mua.
- CẤM góc đời sống/du lịch/"có gì chơi/ăn gì/săn mây", CẤM bàn luận quy hoạch, CẤM "trông coi/quản lý/giữ đất từ xa". Đó là cụm của web khác.
- KHÔNG chèn link sang website khác. Chỉ nói nội dung, KHÔNG tự bịa URL.

GIỌNG (thương hiệu "đọc rủi ro, không bán giấc mơ"): trầm, thật, số cụ thể. BẮT BUỘC có phần rủi ro / "điều cần kiểm" / "ai KHÔNG nên mua". CẤM tính từ rỗng: tuyệt đẹp, lý tưởng, hoàn hảo, siêu phẩm, cơ hội vàng, số 1, giá sốc, đất vàng, chắc chắn lời, x2 tài khoản. Với chủ đề "giá rẻ/ngộp": viết kiểu GIẢI THÍCH + cảnh báo bẫy, KHÔNG hô hào "cắt lỗ/ôm ngay".
KHÔNG bịa: số/tên người/testimonial. Chỉ dùng số trong khung FACTS + số THẬT lấy từ web search (ghi chung chung, không cần trích nguồn trong văn).

${FACTS}

CẤU TRÚC: 4–6 mục H2, mỗi mục 2–3 đoạn ngắn. Ít nhất 1 mục có bảng hoặc list dữ kiện (để AI bóc). FAQ 5–6 câu, CÂU ĐẦU TRẢ LỜI THẲNG (giá? khu nào? pháp lý? rủi ro?).

TRẢ VỀ DUY NHẤT 1 JSON (không markdown, không lời dẫn):
{
 "metaDesc": "140–160 ký tự, có keyword + số + Nam Ban",
 "cat": "vd: Cẩm nang giao dịch",
 "lead": "1–2 câu mở, nêu giá trị + đọc rủi ro",
 "sections": [ {"h2":"...", "html":"<p>...</p><p>...</p>"} ],
 "faqs": [ {"q":"...", "a":"..."} ]
}
Trong "html" chỉ dùng thẻ <p>, <strong>, <em>, <ul><li>, <ol><li>, <table>...</table> (bảng inline-style tối giản). KHÔNG dùng <script>, <a href>, <img>, <h1>, <h2>. Số quan trọng bọc <strong>.`;

const body = {
  model: MODEL,
  max_tokens: 4000,
  tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: 5 }],
  system: sys,
  messages: [{ role: 'user', content: `Hôm nay ${dmy}. Research keyword "${pick.kw}" (web search giá/tin/pháp lý đất Nam Ban mới nhất) rồi viết bài, trả JSON đúng yêu cầu.` }],
};

let data;
try {
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) { console.error('API lỗi', res.status, (await res.text()).slice(0, 300)); process.exit(0); }
  const json = await res.json();
  const text = (json.content || []).filter(b => b.type === 'text').map(b => b.text).join('\n');
  const m = text.match(/\{[\s\S]*\}/);
  if (!m) { console.error('Không parse được JSON:', text.slice(0, 300)); process.exit(0); }
  data = JSON.parse(m[0]);
} catch (e) { console.error('Lỗi gọi API:', e.message); process.exit(0); }

// ── Kiểm chất lượng tối thiểu + blocklist nội dung ──
const sections = Array.isArray(data.sections) ? data.sections.filter(s => s && s.h2 && s.html) : [];
const faqs = Array.isArray(data.faqs) ? data.faqs.filter(f => f && f.q && f.a) : [];
if (sections.length < 3 || faqs.length < 4) { console.log('Bài chưa đủ chất (thiếu mục/FAQ) — không lưu.'); process.exit(0); }

const allText = (data.lead || '') + sections.map(s => s.h2 + s.html).join(' ') + faqs.map(f => f.q + f.a).join(' ');
if (BLOCK_TOPIC.test(allText)) { console.error('Nội dung chạm cụm web khác (blocklist) — HỦY, không lưu.'); process.exit(0); }
if (/panorama|greenspace|<script|<a\s+href/i.test(allText)) { console.error('Nội dung có thẻ cấm/tên web khác — HỦY.'); process.exit(0); }

// ── Dựng HTML bài theo template Villas chuẩn (noindex, chưa vào sitemap) ──
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const url = `https://nambanvillas.vn/thi-truong/${pick.slug}/`;
const bodyHtml = sections.map(s => `        <h2>${esc(s.h2)}</h2>\n        ${s.html}\n`).join('\n');
const faqVisible = faqs.map(f => `        <div class="faq-item">\n          <h3>${esc(f.q)}</h3>\n          <p>${esc(f.a)}</p>\n        </div>\n`).join('\n');
const faqSchema = JSON.stringify({ '@context': 'https://schema.org', '@type': 'FAQPage', mainEntity: faqs.map(f => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: f.a } })) });
const articleSchema = JSON.stringify({ '@context': 'https://schema.org', '@type': 'Article', headline: pick.title, url, image: 'https://nambanvillas.vn/images/og-namban.jpg', publisher: { '@type': 'Organization', name: 'Nam Ban Villas', url: 'https://nambanvillas.vn' }, author: { '@type': 'Organization', name: 'Nam Ban Villas' }, datePublished: iso, dateModified: iso, inLanguage: 'vi', spatialCoverage: { '@type': 'Place', name: 'Nam Ban, Lâm Hà, Lâm Đồng', geo: { '@type': 'GeoCoordinates', latitude: 11.7586, longitude: 108.2432 }, address: { '@type': 'PostalAddress', addressLocality: 'Nam Ban', addressRegion: 'Lâm Đồng', addressCountry: 'VN' } } });
const bcSchema = JSON.stringify({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Trang chủ', item: 'https://nambanvillas.vn/' }, { '@type': 'ListItem', position: 2, name: 'Thị Trường', item: 'https://nambanvillas.vn/thi-truong/' }, { '@type': 'ListItem', position: 3, name: pick.title, item: url }] });

const page = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex,follow"><!-- NHÁP: chờ chú duyệt. Duyệt xong đổi thành index + thêm sitemap. -->
  <title>${esc(pick.title)}</title>
  <meta name="description" content="${esc(data.metaDesc)}">
  <link rel="canonical" href="${url}">
  <meta name="geo.region" content="VN-LB">
  <meta name="geo.placename" content="Nam Ban, Lâm Hà, Lâm Đồng">
  <meta name="geo.position" content="11.7586;108.2432">
  <meta name="ICBM" content="11.7586, 108.2432">
  <meta property="og:title" content="${esc(pick.title)}">
  <meta property="og:description" content="${esc(data.metaDesc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${url}">
  <meta property="og:image" content="https://nambanvillas.vn/images/og-namban.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${esc(pick.title)}">
  <meta name="twitter:image" content="https://nambanvillas.vn/images/og-namban.jpg">
  <link rel="icon" href="/images/favicon.png" type="image/png">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/plus-jakarta-sans@5/wght.css">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" href="../../css/article.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-LHGW9K1BDP"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-LHGW9K1BDP');</script>
  <script type="application/ld+json">${articleSchema}</script>
  <script type="application/ld+json">${faqSchema}</script>
  <script type="application/ld+json">${bcSchema}</script>
</head>
<body>
<header class="header scrolled" id="header">
  <div class="container header-inner">
    <a href="/" class="logo"><img src="/images/logo.png" alt="Nam Ban Villas" width="41" height="52" style="display:block"><span class="logo-text">NamBan<strong>Villas</strong></span></a>
    <nav class="nav" id="nav">
      <a href="/dat-nen-nam-ban/" class="nav-link">Đất Nền</a>
      <a href="/nha-ban-nam-ban/" class="nav-link">Nhà Bán</a>
      <a href="/dich-vu/" class="nav-link">Dịch Vụ</a>
      <a href="/ve-nam-ban/" class="nav-link">Về Nam Ban</a>
      <a href="/thi-truong/" class="nav-link active">Thị Trường</a>
      <a href="/lien-he/" class="nav-link">Liên Hệ</a>
    </nav>
    <div class="header-right">
      <a href="tel:0978758788" class="hotline-btn">0978 758 788</a>
      <button class="menu-btn" id="menuBtn"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>

<main>
  <div class="breadcrumb-bar">
    <div class="container">
      <nav class="breadcrumb">
        <a href="/">Trang chủ</a><span class="bc-sep">›</span>
        <a href="/thi-truong/">Thị Trường</a><span class="bc-sep">›</span>
        <span>${esc(pick.title)}</span>
      </nav>
    </div>
  </div>

  <div class="article-wrap">
    <div class="container">
      <div class="article-header">
        <p class="article-cat">${esc(data.cat || 'Cẩm nang giao dịch')} · Cập nhật ${dmy}</p>
        <h1 class="article-title">${esc(pick.title)}</h1>
        <p class="article-lead">${esc(data.lead)}</p>
      </div>

      <div class="article-body">
${bodyHtml}
        <h2>Câu Hỏi Thường Gặp</h2>

${faqVisible}
        <div style="border:1px solid #E2E0DB;border-radius:12px;padding:22px 24px;margin-top:36px">
          <p style="font-weight:700;color:#1A3D2B;margin-bottom:2px">Xem thêm để ra quyết định</p>
          <p style="color:#6b6b6b;font-size:.84rem;margin-bottom:10px">Các trang giúp so giá và chọn lô trước khi mua:</p>
          <a href="/thi-truong/dat-phan-lo-nam-ban/" style="display:block;padding:10px 0;border-top:1px solid #ECEAE4;color:#1A3D2B;font-weight:600;font-size:.9rem;text-decoration:none">Mua đất phân lô Nam Ban — bảng giá theo khu <span style="color:#9a8a4c">→</span></a>
          <a href="/cum-moi-nam-ban/" style="display:block;padding:10px 0;border-top:1px solid #ECEAE4;color:#1A3D2B;font-weight:600;font-size:.9rem;text-decoration:none">Tất cả cụm phân lô Nam Ban đang mở <span style="color:#9a8a4c">→</span></a>
          <a href="/thi-truong/mua-dat-nam-ban-bao-nhieu/" style="display:block;padding:10px 0;border-top:1px solid #ECEAE4;color:#1A3D2B;font-weight:600;font-size:.9rem;text-decoration:none">Mua đất Nam Ban bao nhiêu tiền — dải giá theo diện tích <span style="color:#9a8a4c">→</span></a>
        </div>

        <div style="background:#EBF4EE;border-radius:12px;padding:24px;margin-top:40px">
          <p style="font-weight:700;color:#1A3D2B;margin-bottom:8px">Gửi lô bạn đang xem, cháu rà pháp lý giúp trước khi cọc</p>
          <p style="color:#4a4a4a;font-size:.92rem;margin-bottom:16px">Kiểm sổ, thổ cư, quy hoạch, đường vào — nói thẳng lô nào nên mua, lô nào nên tránh. Miễn phí.</p>
          <a href="tel:0978758788" style="display:inline-block;background:#1A3D2B;color:white;padding:10px 24px;border-radius:8px;font-weight:600;font-size:.9rem;margin-right:8px">Gọi 0978 758 788</a>
          <a href="https://zalo.me/0978758788" target="_blank" style="display:inline-block;background:#C9A84C;color:#1A3D2B;padding:10px 24px;border-radius:8px;font-weight:700;font-size:.9rem">Nhắn Zalo →</a>
        </div>

      </div>
    </div>
  </div>
</main>

<footer class="footer">
  <div class="container footer-inner">
    <div class="footer-brand">
      <a href="/" class="logo" style="margin-bottom:12px;display:inline-flex;">
        <img src="/images/logo.png" alt="Nam Ban Villas" width="41" height="52">
        <span class="logo-text" style="color:white;">NamBan<strong>Villas</strong></span>
      </a>
      <p><strong>Địa chỉ:</strong> Xã Nam Ban, Lâm Hà, Lâm Đồng</p>
      <div style="margin-top:14px;padding-top:14px;border-top:1px solid rgba(255,255,255,.1)">
        <p><a href="tel:0978758788" style="color:#C9A84C;font-size:.88rem;">0978 758 788</a> · <a href="https://zalo.me/0978758788" target="_blank" style="color:#C9A84C;font-size:.88rem;">Zalo</a></p>
      </div>
    </div>
    <div class="footer-links">
      <h4>Bất động sản</h4>
      <a href="/dat-nen-nam-ban/">Đất Nền Nam Ban</a>
      <a href="/cum-moi-nam-ban/">Cụm Phân Lô Đang Mở</a>
      <a href="/nha-ban-nam-ban/">Nhà Bán Nam Ban</a>
    </div>
    <div class="footer-links">
      <h4>Thông tin</h4>
      <a href="/thi-truong/">Thị Trường BĐS</a>
      <a href="/ve-nam-ban/">Về Nam Ban</a>
      <a href="/lien-he/">Liên Hệ</a>
    </div>
  </div>
  <div class="footer-bottom"><div class="container"><span>Giúp bạn ra quyết định đúng về đất Nam Ban</span></div></div>
</footer>
<script src="../../js/main.js" defer></script>
</body>
</html>
`;

// ── Verify JSON-LD trước khi ghi ──
for (const b of [articleSchema, faqSchema, bcSchema]) { try { JSON.parse(b); } catch { console.error('JSON-LD hỏng — HỦY.'); process.exit(0); } }

const outDir = path.join(TT, pick.slug);
mkdirSync(outDir, { recursive: true });
writeFileSync(path.join(outDir, 'index.html'), page, 'utf8');

// ── Cập nhật queue (nháp chờ duyệt) ──
queue.drafts = queue.drafts || [];
queue.drafts.push({ slug: pick.slug, title: pick.title, kw: pick.kw, url, created: iso, status: 'draft' });
mkdirSync(path.dirname(QUEUE), { recursive: true });
writeFileSync(QUEUE, JSON.stringify(queue, null, 2), 'utf8');

console.log(`NHÁP MỚI: ${pick.title}\n  ${url}  (noindex — chờ chú duyệt)`);
