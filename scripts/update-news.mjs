/**
 * Weekly news updater – fetches RSS feeds, writes data/news.json
 * Run via GitHub Actions every Monday 07:00 UTC (14:00 VN time)
 */
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const RSS_SOURCES = {
  thiTruong: [
    'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fvnexpress.net%2Frss%2Fbat-dong-san.rss&count=8',
    'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fcafef.vn%2Fthi-truong-bat-dong-san.rss&count=8',
  ],
  veNamBan: [
    'https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fnews.google.com%2Frss%2Fsearch%3Fq%3DNam%2BBan%2BL%C3%A2m%2B%C4%90%E1%BB%93ng%26hl%3Dvi%26gl%3DVN%26ceid%3DVN%3Avi&count=8',
  ],
};

async function fetchRSS(url) {
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(15000) });
    const json = await res.json();
    if (json.status === 'ok') return json.items || [];
  } catch (e) {
    console.error('RSS fetch failed:', url, e.message);
  }
  return [];
}

function cleanHtml(str) {
  return (str || '').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").trim();
}

function stripPhone(text) {
  return text.replace(/0\d{9}/g, '').replace(/\(\d{3,4}\)\s*\d{3,4}[\s-]\d{3,4}/g, '').trim();
}

async function main() {
  console.log('Fetching RSS feeds...');

  const [vnexpress, cafef] = await Promise.all([
    fetchRSS(RSS_SOURCES.thiTruong[0]),
    fetchRSS(RSS_SOURCES.thiTruong[1]),
  ]);
  const namBanItems = await fetchRSS(RSS_SOURCES.veNamBan[0]);

  // Merge + deduplicate by title
  const thiTruongRaw = [...vnexpress, ...cafef];
  const seen = new Set();
  const thiTruong = [];
  for (const item of thiTruongRaw) {
    const key = (item.title || '').slice(0, 60);
    if (!seen.has(key)) { seen.add(key); thiTruong.push(item); }
    if (thiTruong.length >= 10) break;
  }

  const data = {
    updatedAt: new Date().toISOString(),
    thiTruong: thiTruong.slice(0, 8).map(item => ({
      title: stripPhone(cleanHtml(item.title)),
      link: item.link || '#',
      pubDate: item.pubDate || '',
      description: stripPhone(cleanHtml(item.description || item.content || '')).slice(0, 300),
      thumbnail: item.thumbnail || item.enclosure?.link || '',
      source: new URL(item.link || 'https://vnexpress.net').hostname.replace('www.', ''),
    })),
    veNamBan: namBanItems.slice(0, 8).map(item => ({
      title: stripPhone(cleanHtml(item.title)),
      link: item.link || '#',
      pubDate: item.pubDate || '',
      description: stripPhone(cleanHtml(item.description || item.content || '')).slice(0, 300),
      thumbnail: item.thumbnail || item.enclosure?.link || '',
      source: new URL(item.link || 'https://news.google.com').hostname.replace('www.', ''),
    })),
  };

  mkdirSync(path.join(ROOT, 'data'), { recursive: true });
  writeFileSync(path.join(ROOT, 'data', 'news.json'), JSON.stringify(data, null, 2), 'utf8');
  console.log(`✓ Wrote data/news.json — thiTruong: ${data.thiTruong.length}, veNamBan: ${data.veNamBan.length}`);
}

main().catch(err => { console.error(err); process.exit(1); });
