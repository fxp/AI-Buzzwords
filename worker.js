/**
 * Cloudflare Worker for xiaopingfeng.com/blog/ai-buzzwords*
 *
 * Routes:
 *   /blog/ai-buzzwords/<path>            → fxp.github.io/AI-Buzzwords/<path>  (default)
 *   /blog/ai-buzzwords/<path>?v=N        → historical: fetches the file at the
 *                                          commit recorded in <slug>.meta.json
 *                                          version_log[v=N].git_sha
 *
 * For ?v=N requests:
 *   1. Strip the path to identify the article (slug = filename without .html and lang suffix)
 *   2. Fetch <slug>.meta.json from current main to look up git_sha for version N
 *   3. Fetch the file content from raw.githubusercontent.com at that sha
 *   4. Inject a small banner at the top of <body> indicating this is a historical version
 *
 * If meta.json lookup fails or version not found → fall back to current version with a
 * tiny banner saying "请求的历史版本不可用"
 */
const PREFIX = '/blog/ai-buzzwords';
const ORIGIN_HOST = 'fxp.github.io';
const ORIGIN_BASE = `https://${ORIGIN_HOST}/AI-Buzzwords`;
const RAW_BASE = 'https://raw.githubusercontent.com/fxp/AI-Buzzwords';

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const subpath = url.pathname.slice(PREFIX.length) || '/';
    const versionParam = url.searchParams.get('v');

    // No ?v=N: simple proxy
    if (!versionParam) {
      return fetchOrigin(subpath, url.search, request.headers);
    }

    // ?v=N: try historical version
    const v = parseInt(versionParam, 10);
    if (!Number.isInteger(v) || v < 1) {
      return fetchOrigin(subpath, '', request.headers);
    }

    const historical = await fetchHistorical(subpath, v);
    if (historical) {
      return historical;
    }
    // Fall back to current with a small note
    return fetchOriginWithBanner(
      subpath,
      `<div style="background:#c4850a;color:#fff;padding:8px 12px;font:12px JetBrains Mono,monospace;text-align:center;border-bottom:1px solid rgba(0,0,0,0.2);">
         ⚠️ 请求的历史版本 v${v} 不可用，已显示当前版本。
       </div>`,
      request.headers
    );
  },
};

function fetchOrigin(subpath, search, headers) {
  return fetch(`${ORIGIN_BASE}${subpath}${search}`, { headers });
}

async function fetchHistorical(subpath, v) {
  // subpath looks like: /deepdive/labor-day-2026/white-collar.html
  // Need to determine slug to find <slug>.meta.json
  const m = subpath.match(/^(.+)\/([^\/]+?)(?:\.[a-z]{2}(?:-[a-z]{2,4})?)?\.html$/i);
  if (!m) return null;
  const dir = m[1]; // /deepdive/labor-day-2026
  const slug = m[2]; // white-collar

  // Fetch meta.json from current main
  const metaUrl = `${ORIGIN_BASE}${dir}/${slug}.meta.json`;
  let meta;
  try {
    const r = await fetch(metaUrl, { cf: { cacheTtl: 60 } });
    if (!r.ok) return null;
    meta = await r.json();
  } catch (e) {
    return null;
  }

  const entry = (meta.version_log || []).find((x) => x.v === v);
  if (!entry || !entry.git) return null;

  // Fetch from raw.githubusercontent.com at that sha
  // subpath: /deepdive/labor-day-2026/white-collar.html
  // raw URL needs path under repo root: deepdive/labor-day-2026/white-collar.html
  const rawPath = subpath.startsWith('/') ? subpath.slice(1) : subpath;
  const rawUrl = `${RAW_BASE}/${entry.git}/${rawPath}`;

  let r;
  try {
    r = await fetch(rawUrl, { cf: { cacheTtl: 3600 } });
  } catch (e) {
    return null;
  }
  if (!r.ok) return null;

  const html = await r.text();
  const banner = renderBanner(v, entry, meta);
  const injected = injectBanner(html, banner);
  return new Response(injected, {
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'X-Content-Source': `git@${entry.git}`,
      'X-Content-Version': String(v),
    },
  });
}

async function fetchOriginWithBanner(subpath, bannerHtml, headers) {
  const r = await fetch(`${ORIGIN_BASE}${subpath}`, { headers });
  const ct = r.headers.get('Content-Type') || '';
  if (!ct.includes('text/html')) return r;
  const text = await r.text();
  return new Response(injectBanner(text, bannerHtml), {
    status: r.status,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
    },
  });
}

function renderBanner(v, entry, meta) {
  const isLatest = v === meta.current_version;
  if (isLatest) return '';
  const latestUrl = '?v=' + meta.current_version;
  const summary = (entry.summary || '').replace(/"/g, '&quot;').slice(0, 200);
  return `
<div style="background:#1e1a15;color:#f0ebe0;padding:10px 16px;font:12px JetBrains Mono,monospace;text-align:center;border-bottom:1px solid rgba(232,64,64,0.4);">
  📜 您正在查看历史版本 <strong style="color:#e84040">v${v}</strong> · ${entry.date}
  · <span style="opacity:0.7">${summary}</span>
  · <a href="?" style="color:#7fb88b;text-decoration:underline;">返回当前 v${meta.current_version}</a>
</div>`;
}

function injectBanner(html, banner) {
  if (!banner) return html;
  // Insert right after <body...>
  return html.replace(/(<body[^>]*>)/i, (m) => m + banner);
}
