/**
 * collect_app_tokens.mjs
 *
 * Captures design tokens, layout structure, component inventory, and
 * visual patterns from ANY public website — v0/Vercel apps, SaaS landing
 * pages, documentation sites, portfolios, etc.
 *
 * Writes to presentation/src/tokens/raw-themes/<app-name>/
 *   metadata.json   — full structured capture
 *   snapshot.html   — self-contained visual report
 *   screenshot.png  — 1280x800 viewport capture (skipped with --no-screenshot)
 *
 * Usage
 * -----
 *   # Single URL  (name inferred from hostname)
 *   node presentation/scripts/collect_app_tokens.mjs <url> [name]
 *
 *   # Batch from JSON file
 *   node presentation/scripts/collect_app_tokens.mjs --batch <targets.json>
 *
 *   # Skip screenshot (faster)
 *   node presentation/scripts/collect_app_tokens.mjs <url> [name] --no-screenshot
 *
 * Batch JSON format
 * -----------------
 *   [{ "url": "https://example.com/", "name": "example" }]
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = path.dirname(__filename);
const RAW_THEMES = path.join(__dirname, '..', 'src', 'tokens', 'raw-themes');

// ---------------------------------------------------------------------------
// CLI parsing
// ---------------------------------------------------------------------------

const args = process.argv.slice(2);

if (args.length === 0 || args[0] === '--help') {
  console.log(
    'Usage:\n' +
    '  node collect_app_tokens.mjs <url> [name] [--no-screenshot]\n' +
    '  node collect_app_tokens.mjs --batch <targets.json> [--no-screenshot]'
  );
  process.exit(args[0] === '--help' ? 0 : 1);
}

const noScreenshot = args.includes('--no-screenshot');
const cleanArgs    = args.filter(a => a !== '--no-screenshot');

/** @type {{ url: string; name: string }[]} */
let targets = [];

if (cleanArgs[0] === '--batch') {
  const batchFile = cleanArgs[1];
  if (!batchFile || !fs.existsSync(batchFile)) {
    console.error(`Batch file not found: ${batchFile}`);
    process.exit(1);
  }
  targets = JSON.parse(fs.readFileSync(batchFile, 'utf-8')).filter(t => t.url);
} else {
  targets = [{ url: cleanArgs[0], name: cleanArgs[1] ?? '' }];
}

// ---------------------------------------------------------------------------
// Slug derivation  (works for any URL)
// ---------------------------------------------------------------------------

function slugFromUrl(rawUrl, override) {
  if (override) {
    return override.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '');
  }
  let { hostname, pathname } = new URL(rawUrl);

  // Strip known PaaS suffixes
  hostname = hostname
    .replace(/\.(vercel|netlify|render|railway|fly)\.app$/, '')
    .replace(/\.pages\.dev$/, '')
    .replace(/\.(com|io|app|dev|co|net|org|ai)$/, '')
    .replace(/^v0-/, '')
    .replace(/^www\./, '');

  // If hostname is very short, prepend first pathname segment for clarity
  const parts = pathname.split('/').filter(Boolean);
  if (hostname.length < 5 && parts.length > 0) hostname += '-' + parts[0];

  return hostname.toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/^-+|-+$/g, '') || 'site';
}

// ---------------------------------------------------------------------------
// Extractors
// ---------------------------------------------------------------------------

/** All CSS custom properties from :root computed styles */
async function extractCSSVars(page) {
  return page.evaluate(() => {
    const cs  = window.getComputedStyle(document.documentElement);
    const out = {};
    for (let i = 0; i < cs.length; i++) {
      const p = cs[i];
      if (p.startsWith('--')) {
        const v = cs.getPropertyValue(p).trim();
        if (v) out[p] = v;
      }
    }
    return out;
  });
}

/** Title, description, og meta, canonical, font families */
async function extractPageMeta(page) {
  return page.evaluate(() => {
    function meta(sel) { return document.querySelector(sel)?.content ?? ''; }

    const title       = document.title ?? '';
    const description = meta('meta[name="description"]') || meta('meta[property="og:description"]');
    const generator   = meta('meta[name="generator"]');
    const keywords    = meta('meta[name="keywords"]');
    const ogImage     = meta('meta[property="og:image"]');
    const canonical   = document.querySelector('link[rel="canonical"]')?.href ?? '';

    const fonts = new Set();
    for (const sh of document.styleSheets) {
      try {
        for (const rule of sh.cssRules ?? []) {
          if (rule.style?.fontFamily) fonts.add(rule.style.fontFamily);
        }
      } catch { /* cross-origin */ }
    }
    for (const el of [document.body, ...document.querySelectorAll('h1,h2,h3,p,pre,code,button,a,input')]) {
      if (el) fonts.add(window.getComputedStyle(el).fontFamily);
    }

    return { title, description, generator, keywords, ogImage, canonical, fontFamilies: [...fonts] };
  });
}

/** Tech stack detection — fully serialisable, no DOM node refs */
async function detectStack(page) {
  return page.evaluate(() => {
    const scripts = [...document.querySelectorAll('script[src]')].map(s => s.src);
    const links   = [...document.querySelectorAll('link[href]')].map(l => l.href);
    const all     = [...scripts, ...links];

    const isNextJs  = !!document.querySelector('#__NEXT_DATA__') || all.some(s => s.includes('/_next/'));
    const isNuxt    = !!document.querySelector('#__NUXT_DATA__') || all.some(s => s.includes('/_nuxt/'));
    const isRemix   = all.some(s => s.includes('/__remix_'));
    const isAstro   = !!document.querySelector('astro-island') || all.some(s => s.includes('/astro/'));
    const isVite    = all.some(s => s.includes('/@vite/') || s.includes('/vite/client'));
    const isSvelte  = all.some(s => s.includes('/svelte/'));
    const isReact   = typeof window.__REACT_DEVTOOLS_GLOBAL_HOOK__ !== 'undefined' ||
                      !!document.querySelector('[data-reactroot],[data-react-helmet]');
    const isVue     = typeof window.__VUE__ !== 'undefined' || !!document.querySelector('[data-v-]');
    const isAngular = typeof window.getAllAngularRootElements === 'function' ||
                      !!document.querySelector('[ng-version]');

    const isTailwind  = all.some(s => s.includes('tailwind')) ||
                        [...document.querySelectorAll('[class]')]
                          .some(el => /\b(flex|grid|p-\d|m-\d|text-\w+|bg-\w+|rounded|border)\b/.test(el.className));
    const hasShadcn   = !!document.querySelector('[data-radix-popper-content-wrapper],[data-state]') ||
                        all.some(s => s.includes('radix'));
    const hasBootstrap = all.some(s => s.includes('bootstrap'));
    const hasChakra    = all.some(s => s.includes('chakra'));
    const hasMui       = all.some(s => s.includes('material-ui') || s.includes('@mui'));

    const hasFramer  = all.some(s => s.includes('framer-motion'));
    const hasGSAP    = typeof window.gsap !== 'undefined';
    const hasThreeJs = typeof window.THREE !== 'undefined' || all.some(s => s.includes('three.js') || s.includes('/three/'));
    const hasLucide  = all.some(s => s.includes('lucide'));

    const framework = isNextJs  ? 'Next.js'
                    : isNuxt    ? 'Nuxt'
                    : isRemix   ? 'Remix'
                    : isAstro   ? 'Astro'
                    : isSvelte  ? 'SvelteKit'
                    : isVite    ? 'Vite'
                    : isReact   ? 'React'
                    : isVue     ? 'Vue'
                    : isAngular ? 'Angular'
                    : 'Unknown';

    const cssLibs = [
      isTailwind   && 'Tailwind CSS',
      hasShadcn    && 'shadcn/ui',
      hasBootstrap && 'Bootstrap',
      hasChakra    && 'Chakra UI',
      hasMui       && 'Material UI',
    ].filter(Boolean);

    const extras = [
      hasFramer  && 'Framer Motion',
      hasGSAP    && 'GSAP',
      hasThreeJs && 'Three.js',
      hasLucide  && 'Lucide',
    ].filter(Boolean);

    return { framework, cssLibs, extras };
  });
}

/**
 * Full layout analysis:
 *   - sections[]     : semantic/landmark elements with layout info
 *   - components{}   : counts of UI primitives
 *   - spacingScale   : unique spacing values sampled from containers
 *   - shadows        : unique box-shadow values
 *   - borderRadii    : unique border-radius values from interactive elements
 *   - typeScale      : computed typography per HTML element type
 */
async function extractLayout(page) {
  return page.evaluate(() => {
    // -- shared helpers -------------------------------------------------------

    function cs(el)   { return window.getComputedStyle(el); }
    function px(v)    { return parseFloat(v) || 0; }
    function hex(rgb) {
      const m = rgb?.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      return m ? '#' + [m[1], m[2], m[3]].map(n => parseInt(n).toString(16).padStart(2, '0')).join('') : null;
    }
    function visible(el) {
      if (!el) return false;
      const r = el.getBoundingClientRect();
      const s = cs(el);
      return r.width > 0 && r.height > 0 &&
             s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
    }

    // -- section map ----------------------------------------------------------

    const LANDMARKS = [
      'header','nav','main','footer','aside','section','article',
      '[role="banner"]','[role="navigation"]','[role="main"]',
      '[role="contentinfo"]','[role="complementary"]',
      '.hero','#hero','#header','#footer','#main','#content',
    ];
    const seenEls = new WeakSet();
    const sections = [];

    for (const sel of LANDMARKS) {
      for (const el of document.querySelectorAll(sel)) {
        if (seenEls.has(el) || !visible(el)) continue;
        seenEls.add(el);

        const style   = cs(el);
        const rect    = el.getBoundingClientRect();
        const display = style.display;

        let layout  = 'block';
        if      (display === 'flex')             layout = 'flex';
        else if (display === 'grid')             layout = 'grid';
        else if (display.includes('inline'))     layout = 'inline';

        // column count
        let columns = 1;
        if (display === 'grid') {
          const gtc = style.gridTemplateColumns;
          columns = gtc && gtc !== 'none'
            ? gtc.trim().split(/\s+(?=[^(]*(?:\(|$))/).length
            : 1;
        } else if (display === 'flex' && style.flexDirection !== 'column') {
          const kids = [...el.children].filter(visible);
          if (kids.length > 1) {
            const baseY = kids[0].getBoundingClientRect().top;
            columns = kids.filter(c => Math.abs(c.getBoundingClientRect().top - baseY) < 10).length;
            if (columns < 1) columns = 1;
          }
        }

        sections.push({
          tag:     el.tagName.toLowerCase(),
          role:    el.getAttribute('role') ?? null,
          id:      el.id || null,
          classes: [...el.classList].slice(0, 6).join(' ') || null,
          heading: el.querySelector('h1,h2,h3,h4')?.textContent?.trim().slice(0, 80) ?? null,
          layout,
          columns,
          flexDirection: display === 'flex' ? style.flexDirection : null,
          gap:     style.gap !== 'normal' ? style.gap : null,
          width:   Math.round(rect.width),
          height:  Math.round(rect.height),
          top:     Math.round(rect.top + window.scrollY),
          bgColor: hex(style.backgroundColor),
          padding: [style.paddingTop, style.paddingRight, style.paddingBottom, style.paddingLeft]
                     .map(v => Math.round(px(v))).join(' '),
        });
      }
    }

    // -- component inventory --------------------------------------------------

    const allLinks   = [...document.querySelectorAll('a[href]')];
    const navLinks   = allLinks.filter(a => a.closest('nav,header,[role="navigation"]'));
    const extLinks   = allLinks.filter(a => {
      try { return new URL(a.href).hostname !== window.location.hostname; } catch { return false; }
    });
    const allButtons = document.querySelectorAll('button,[role="button"],input[type="submit"],input[type="button"]');
    const allInputs  = document.querySelectorAll('input:not([type="hidden"]),textarea,select');
    const allForms   = document.querySelectorAll('form');
    const allImages  = document.querySelectorAll('img,picture source');
    const allVideos  = document.querySelectorAll('video,iframe[src*="youtube"],iframe[src*="vimeo"]');
    const allTables  = document.querySelectorAll('table');

    // Card-like containers (bordered/shadowed boxes with meaningful size)
    let cardLike = 0;
    for (const el of document.querySelectorAll('div,article,li,aside')) {
      const s    = cs(el);
      const rect = el.getBoundingClientRect();
      if (rect.width < 60 || rect.height < 40) continue;
      if (s.display === 'none' || s.visibility === 'hidden') continue;
      const hasBorder = px(s.borderWidth) > 0;
      const hasShadow = s.boxShadow !== 'none';
      const hasBg     = s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent';
      if (hasBg && (hasBorder || hasShadow)) cardLike++;
    }

    // Small SVGs treated as icons
    const icons = [...document.querySelectorAll('svg')].filter(el => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.width < 48 && r.height < 48;
    }).length;

    const components = {
      buttons:      allButtons.length,
      inputs:       allInputs.length,
      forms:        allForms.length,
      images:       allImages.length,
      videos:       allVideos.length,
      tables:       allTables.length,
      icons,
      cardLike,
      links:        allLinks.length,
      navLinks:     navLinks.length,
      externalLinks: extLinks.length,
    };

    // -- spacing scale (sampled px values) ------------------------------------

    const spacingSet = new Set();
    const SP_PROPS   = ['paddingTop','paddingBottom','paddingLeft','paddingRight',
                        'marginTop','marginBottom','gap','rowGap','columnGap'];
    for (const el of document.querySelectorAll('section,main,header,footer,nav,div,article')) {
      if (!visible(el)) continue;
      const s = cs(el);
      for (const prop of SP_PROPS) {
        const v = px(s[prop]);
        if (v >= 2 && v <= 320) spacingSet.add(Math.round(v));
      }
      if (spacingSet.size > 80) break;
    }

    // -- shadow patterns -------------------------------------------------------

    const shadowSet = new Set();
    for (const el of document.querySelectorAll('*')) {
      const s = cs(el).boxShadow;
      if (s && s !== 'none') shadowSet.add(s);
      if (shadowSet.size >= 24) break;
    }

    // -- border radii (interactive + card elements) ---------------------------

    const radiusSet = new Set();
    for (const el of document.querySelectorAll('button,input,img,[class*="card"],[class*="btn"],[class*="rounded"]')) {
      const v = cs(el).borderRadius;
      if (v && v !== '0px') radiusSet.add(v);
    }

    // -- type scale ------------------------------------------------------------

    const typeScale = {};
    for (const tag of ['h1','h2','h3','h4','p','small','button','a','code','label']) {
      const el = document.querySelector(tag);
      if (!el || !visible(el)) continue;
      const s = cs(el);
      typeScale[tag] = {
        fontFamily:    s.fontFamily.split(',')[0].trim().replace(/['"]/g, ''),
        fontSize:      s.fontSize,
        fontWeight:    s.fontWeight,
        lineHeight:    s.lineHeight,
        letterSpacing: s.letterSpacing !== 'normal' ? s.letterSpacing : null,
        color:         s.color,
      };
    }

    return {
      pageHeight:   Math.round(document.documentElement.scrollHeight),
      pageWidth:    Math.round(document.documentElement.scrollWidth),
      sections,
      components,
      spacingScale: [...spacingSet].sort((a, b) => a - b),
      shadows:      [...shadowSet].slice(0, 20),
      borderRadii:  [...radiusSet].slice(0, 16),
      typeScale,
    };
  });
}

/** All accent colors from rendered elements (rgb -> hex, deduped) */
async function extractAccentColors(page) {
  return page.evaluate(() => {
    function hex(rgb) {
      const m = rgb?.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      return m ? '#' + [m[1], m[2], m[3]].map(n => parseInt(n).toString(16).padStart(2, '0')).join('') : null;
    }
    const seen = new Set();
    for (const el of document.querySelectorAll('*')) {
      const cs = window.getComputedStyle(el);
      for (const prop of ['backgroundColor','color','borderTopColor','outlineColor','fill','stroke']) {
        const v = cs[prop];
        if (v && v !== 'rgba(0, 0, 0, 0)' && v !== 'transparent') {
          const h = hex(v);
          if (h) seen.add(h);
        }
      }
    }
    return [...seen];
  });
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const SYSTEM_FONTS = new Set([
  'serif','sans-serif','monospace','system-ui','inherit','initial','unset',
  'ui-sans-serif','ui-monospace','ui-serif','cursive','fantasy','math',
  'Geneva','Tahoma','Verdana','Arial','Helvetica','Times New Roman',
  'Segoe UI','Roboto','Georgia','Courier New','Courier','-apple-system',
]);

const KEY_CSS_VARS = [
  '--background','--foreground',
  '--card','--card-foreground',
  '--popover','--popover-foreground',
  '--primary','--primary-foreground',
  '--secondary','--secondary-foreground',
  '--muted','--muted-foreground',
  '--accent','--accent-foreground',
  '--destructive','--destructive-foreground',
  '--border','--input','--ring','--radius',
  '--sidebar','--sidebar-foreground','--sidebar-border',
  '--chart-1','--chart-2','--chart-3','--chart-4','--chart-5',
];

function cssValueToStyle(val) {
  if (!val) return null;
  if (val.startsWith('#') || val.startsWith('rgb') || val.startsWith('hsl')) return val;
  // Shorthand HSL "220 14% 96%" -> hsl(220, 14%, 96%)
  if (/^\d+(\.\d+)?\s+\d/.test(val)) {
    const p = val.trim().split(/\s+/);
    if (p.length === 3) return `hsl(${p[0]}, ${p[1]}, ${p[2]})`;
  }
  return null;
}

// ---------------------------------------------------------------------------
// HTML report generator
// ---------------------------------------------------------------------------

function generateSnapshotHtml({ meta, lightVars, darkVars, accentColors, layout, appName, sourceUrl }) {
  const capturedAt = new Date().toISOString().split('T')[0];

  const cleanFonts = [...new Set(
    (meta.fontFamilies ?? [])
      .flatMap(f => f.split(',').map(s => s.trim().replace(/['"]/g, '')))
      .filter(f => f && !SYSTEM_FONTS.has(f))
  )].slice(0, 12);

  // All var keys (standard shadcn set + any discovered ones, skip Tailwind internals)
  const allVarKeys = [...new Set([
    ...KEY_CSS_VARS,
    ...Object.keys(lightVars).filter(k => !k.startsWith('--tw-') && !k.startsWith('--vp-')),
  ])];

  function varRows(vars, base) {
    return allVarKeys
      .filter(k => vars[k] && (!base || vars[k] !== base[k]))
      .map(k => {
        const val      = vars[k];
        const cssColor = cssValueToStyle(val);
        const sw = cssColor
          ? `<span class="swatch" style="background:${cssColor}"></span>`
          : `<span class="swatch swatch-empty"></span>`;
        return `<div class="token-row">${sw}<code>${k}</code><span class="val">${val}</span></div>`;
      }).join('');
  }

  // Accent palette — filter to "interesting" (not pure black/white)
  const filteredAccents = [...new Set(accentColors)].filter(h6 => {
    const h = h6.replace('#', '');
    if (h.length !== 6) return false;
    const r = parseInt(h.slice(0, 2), 16);
    const g = parseInt(h.slice(2, 4), 16);
    const b = parseInt(h.slice(4, 6), 16);
    const luma = 0.299 * r + 0.587 * g + 0.114 * b;
    return luma > 15 && luma < 240;
  }).slice(0, 60);

  // Section diagram (proportional to scroll height)
  const totalH = Math.max(layout.pageHeight || 1, ...layout.sections.map(s => s.top + s.height), 1);
  const COLORS  = ['#dbeafe','#dcfce7','#fef9c3','#fce7f3','#ede9fe','#ffedd5','#f1f5f9','#fae8ff','#ecfdf5','#fff7ed'];
  const sectionBlocks = layout.sections.map((s, i) => {
    const topPct = ((s.top  / totalH) * 100).toFixed(1);
    const hPct   = Math.max(((s.height / totalH) * 100), 1.5).toFixed(1);
    const label  = [
      `<strong>${s.tag}${s.id ? '#' + s.id : ''}</strong>`,
      s.heading ? `"${s.heading.slice(0, 40)}"` : '',
      `${s.layout}${s.columns > 1 ? ' x' + s.columns : ''}`,
      `${s.width}x${s.height}`,
    ].filter(Boolean).join('<br>');
    return `<div class="sec-block" style="top:${topPct}%;height:${hPct}%;background:${COLORS[i % COLORS.length]}">${label}</div>`;
  }).join('');

  // Type scale rows
  const tsRows = Object.entries(layout.typeScale ?? {}).map(([tag, ts]) =>
    `<tr>
      <td><code>&lt;${tag}&gt;</code></td>
      <td style="font-family:${ts.fontFamily},system-ui">${ts.fontFamily}</td>
      <td>${ts.fontSize}</td>
      <td>${ts.fontWeight}</td>
      <td>${ts.lineHeight}</td>
    </tr>`
  ).join('');

  // Component counts
  const compRows = Object.entries(layout.components ?? {}).map(([k, v]) =>
    `<tr><td>${k}</td><td><strong>${v}</strong></td></tr>`
  ).join('');

  const spacingPills = (layout.spacingScale ?? [])
    .map(v => `<span class="sp-pill">${v}px</span>`).join('');

  const shadowSamples = (layout.shadows ?? []).map(s =>
    `<div class="shadow-sample" style="box-shadow:${s}" title="${s}"></div>`
  ).join('');

  const lightRows = varRows(lightVars);
  const darkRows  = varRows(darkVars, lightVars);
  const varCount  = Object.keys(lightVars).length;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>${meta.title || appName} - Token Snapshot</title>
  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    body{font-family:system-ui,-apple-system,sans-serif;background:#f4f4f5;color:#18181b;font-size:14px;padding:28px;line-height:1.5}
    h1{font-size:22px;font-weight:700}
    h2{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:#71717a;margin-bottom:14px}
    .subtitle{font-size:13px;color:#71717a;margin-top:3px;margin-bottom:24px}
    .subtitle a{color:#3b82f6;text-decoration:none}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
    .grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px}
    @media(max-width:900px){.grid,.grid-3{grid-template-columns:1fr}}
    .card{background:#fff;border:1px solid #e4e4e7;border-radius:12px;padding:20px 24px;margin-bottom:18px}
    .card-dark{background:#18181b;border-color:#27272a;color:#fafafa}
    .token-row{display:flex;align-items:center;gap:10px;padding:5px 0;border-bottom:1px solid #f4f4f5}
    .card-dark .token-row{border-bottom-color:#27272a}
    .token-row:last-child{border-bottom:none}
    .swatch{flex-shrink:0;width:20px;height:20px;border-radius:4px;border:1px solid rgba(0,0,0,.12)}
    .swatch-empty{background:#f4f4f5;border-style:dashed}
    .card-dark .swatch-empty{background:#27272a}
    code{font-family:ui-monospace,'Cascadia Code',monospace;font-size:11px;color:#7c3aed;flex:1;min-width:0}
    .card-dark code{color:#c4b5fd}
    .val{font-size:11px;color:#52525b;white-space:nowrap}
    .card-dark .val{color:#a1a1aa}
    .pill-group{display:flex;flex-wrap:wrap;gap:8px}
    .pill{background:#ede9fe;color:#5b21b6;border-radius:99px;padding:3px 12px;font-size:12px;font-weight:500}
    .badge{display:inline-block;background:#dbeafe;color:#1e40af;border-radius:6px;padding:2px 10px;font-size:11px;margin:2px}
    .accent-grid{display:flex;flex-wrap:wrap;gap:8px}
    .accent-dot{display:inline-block;width:30px;height:30px;border-radius:6px;border:1px solid rgba(0,0,0,.1);transition:transform .1s;cursor:default}
    .accent-dot:hover{transform:scale(1.2)}
    .section-diagram{position:relative;width:100%;height:440px;border:1px solid #e4e4e7;border-radius:8px;overflow:hidden;background:#fafafa}
    .sec-block{position:absolute;left:0;right:0;border-bottom:1px solid rgba(0,0,0,.06);padding:5px 10px;font-size:11px;line-height:1.4;overflow:hidden}
    table{width:100%;border-collapse:collapse;font-size:12px}
    th{text-align:left;padding:5px 8px;background:#f4f4f5;border-bottom:1px solid #e4e4e7;font-size:11px}
    td{padding:5px 8px;border-bottom:1px solid #f4f4f5;vertical-align:top}
    tr:last-child td{border-bottom:none}
    .sp-pill{display:inline-block;background:#f0fdf4;color:#166534;border:1px solid #86efac;border-radius:4px;padding:2px 8px;font-size:11px;margin:3px}
    .shadow-row{display:flex;flex-wrap:wrap;gap:16px;align-items:center;margin-bottom:12px}
    .shadow-sample{width:44px;height:44px;background:#fff;border-radius:8px;border:1px solid #e4e4e7}
    .shadow-list{font-size:11px;color:#71717a;font-family:ui-monospace,monospace}
    .shadow-list div{padding:2px 0}
    dl.meta{display:grid;grid-template-columns:140px 1fr;gap:4px 12px}
    dl.meta dt{font-size:12px;color:#71717a}
    dl.meta dd{font-size:13px;font-weight:500;word-break:break-all}
  </style>
</head>
<body>
  <h1>${meta.title || appName}</h1>
  <p class="subtitle">
    <a href="${sourceUrl}" target="_blank" rel="noopener">${sourceUrl}</a>
    &nbsp;·&nbsp; captured ${capturedAt}
  </p>

  <div class="card">
    <h2>App Metadata</h2>
    <dl class="meta">
      ${meta.description ? `<dt>Description</dt><dd>${meta.description}</dd>` : ''}
      ${meta.generator   ? `<dt>Generator</dt><dd>${meta.generator}</dd>` : ''}
      ${meta.canonical && meta.canonical !== sourceUrl ? `<dt>Canonical</dt><dd>${meta.canonical}</dd>` : ''}
      <dt>Page size</dt><dd>${layout.pageWidth}x${layout.pageHeight}px</dd>
    </dl>
  </div>

  ${cleanFonts.length ? `
  <div class="card">
    <h2>Font Families</h2>
    <div class="pill-group">${cleanFonts.map(f => `<span class="pill">${f}</span>`).join('')}</div>
  </div>` : ''}

  <div class="grid">
    <div class="card">
      <h2>CSS Tokens - Light Mode (${varCount} vars total)</h2>
      ${lightRows || '<em style="color:#71717a;font-size:13px">No CSS custom properties on :root. Colors captured from rendered elements below.</em>'}
    </div>
    ${darkRows ? `
    <div class="card card-dark">
      <h2>CSS Tokens - Dark Mode (changed values)</h2>
      ${darkRows}
    </div>` : '<div></div>'}
  </div>

  ${filteredAccents.length ? `
  <div class="card">
    <h2>Color Palette (${filteredAccents.length} colors extracted from rendered elements)</h2>
    <div class="accent-grid">
      ${filteredAccents.map(c => `<span class="accent-dot" title="${c}" style="background:${c}"></span>`).join('')}
    </div>
  </div>` : ''}

  ${layout.sections.length ? `
  <div class="card">
    <h2>Page Layout - Section Map (${layout.sections.length} sections detected)</h2>
    <div class="section-diagram">${sectionBlocks}</div>
    <div style="margin-top:14px">
      <table>
        <thead><tr><th>Element</th><th>Heading / Label</th><th>Layout</th><th>Cols</th><th>Size</th><th>Gap</th><th>Padding</th></tr></thead>
        <tbody>
          ${layout.sections.map(s => `<tr>
            <td><code>${s.tag}${s.id ? '#'+s.id : ''}${s.role ? ' ['+s.role+']' : ''}</code></td>
            <td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${s.heading ?? ''}</td>
            <td>${s.layout}${s.flexDirection ? ' ' + s.flexDirection.replace('row','').replace('column','col') : ''}</td>
            <td style="text-align:center">${s.columns}</td>
            <td style="white-space:nowrap">${s.width}x${s.height}</td>
            <td>${s.gap ?? ''}</td>
            <td>${s.padding}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>
  </div>` : ''}

  <div class="grid">
    <div class="card">
      <h2>Component Inventory</h2>
      <table><thead><tr><th>Type</th><th>Count</th></tr></thead>
      <tbody>${compRows}</tbody></table>
    </div>
    <div class="card">
      <h2>Type Scale</h2>
      ${tsRows ? `
      <table>
        <thead><tr><th>Tag</th><th>Family</th><th>Size</th><th>Weight</th><th>Line-H</th></tr></thead>
        <tbody>${tsRows}</tbody>
      </table>` : '<em style="color:#71717a;font-size:13px">None detected</em>'}
    </div>
  </div>

  ${spacingPills ? `
  <div class="card">
    <h2>Spacing Scale (sampled from containers)</h2>
    <div>${spacingPills}</div>
  </div>` : ''}

  ${layout.shadows?.length ? `
  <div class="card">
    <h2>Box Shadow Patterns (${layout.shadows.length} unique)</h2>
    <div class="shadow-row">${shadowSamples}</div>
    <div class="shadow-list">${layout.shadows.map(s => `<div>${s}</div>`).join('')}</div>
  </div>` : ''}

  ${layout.borderRadii?.length ? `
  <div class="card">
    <h2>Border Radii</h2>
    <div class="pill-group">
      ${layout.borderRadii.map(r => `<span class="pill" style="border-radius:${r}">${r}</span>`).join('')}
    </div>
  </div>` : ''}

</body>
</html>`;
}

// ---------------------------------------------------------------------------
// Core collection
// ---------------------------------------------------------------------------

async function collectApp(browser, { url, name }) {
  const appName = slugFromUrl(url, name);
  const outDir  = path.join(RAW_THEMES, appName);

  console.log(`\n+-- ${appName}`);
  console.log(`|   url: ${url}`);
  console.log(`|   out: ${outDir}`);

  fs.mkdirSync(outDir, { recursive: true });

  // -- Light mode pass -------------------------------------------------------
  const lightPage = await browser.newPage();
  await lightPage.setViewportSize({ width: 1280, height: 800 });
  await lightPage.emulateMedia({ colorScheme: 'light' });

  try {
    await lightPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 40000 });
    await lightPage.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => null);
  } catch {
    await lightPage.waitForTimeout(5000);
  }
  await lightPage.waitForTimeout(2500); // SPA settle time

  console.log('|   extracting CSS vars (light)...');
  const lightVars = await extractCSSVars(lightPage);

  console.log('|   extracting page metadata...');
  const meta = await extractPageMeta(lightPage);

  console.log('|   detecting stack...');
  const stack = await detectStack(lightPage);

  console.log('|   analysing layout...');
  const layout = await extractLayout(lightPage);

  console.log('|   sampling colors...');
  const accentColors = await extractAccentColors(lightPage);

  if (!noScreenshot) {
    console.log('|   capturing screenshot...');
    await lightPage.screenshot({ path: path.join(outDir, 'screenshot.png'), fullPage: false });
    console.log('|   screenshot.png saved');
  }
  await lightPage.close();

  // -- Dark mode pass --------------------------------------------------------
  const darkPage = await browser.newPage();
  await darkPage.setViewportSize({ width: 1280, height: 800 });
  await darkPage.emulateMedia({ colorScheme: 'dark' });

  try {
    await darkPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 40000 });
    await darkPage.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => null);
  } catch {
    await darkPage.waitForTimeout(5000);
  }
  await darkPage.waitForTimeout(2500);

  console.log('|   extracting CSS vars (dark)...');
  const darkVars = await extractCSSVars(darkPage);
  await darkPage.close();

  // -- Assemble & write metadata.json ----------------------------------------
  const cleanFonts = [...new Set(
    (meta.fontFamilies ?? [])
      .flatMap(f => f.split(',').map(s => s.trim().replace(/['"]/g, '')))
      .filter(f => f && !SYSTEM_FONTS.has(f))
  )];

  const metadata = {
    app: {
      name:        meta.title    || appName,
      description: meta.description || '',
      url,
      canonical:   meta.canonical  || url,
      ogImage:     meta.ogImage    || null,
      generator:   meta.generator  || null,
      capturedAt:  new Date().toISOString().split('T')[0],
    },
    stack: {
      framework: stack.framework,
      cssLibs:   stack.cssLibs,
      extras:    stack.extras,
      fonts:     cleanFonts,
    },
    designTokens: {
      light: lightVars,
      dark:  darkVars,
    },
    layout,
    accentColors: [...new Set(accentColors)].slice(0, 80),
  };

  const metaPath = path.join(outDir, 'metadata.json');
  fs.writeFileSync(metaPath, JSON.stringify(metadata, null, 2), 'utf-8');
  console.log(`|   metadata.json  (${(fs.statSync(metaPath).size / 1024).toFixed(1)} KB)`);

  const html     = generateSnapshotHtml({ meta, lightVars, darkVars, accentColors, layout, appName, sourceUrl: url });
  const snapPath = path.join(outDir, 'snapshot.html');
  fs.writeFileSync(snapPath, html, 'utf-8');
  console.log(`+-- snapshot.html  (${(fs.statSync(snapPath).size / 1024).toFixed(1)} KB)`);
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main() {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const target of targets) {
      await collectApp(browser, target);
    }
  } finally {
    await browser.close();
  }
  console.log(`\nDone -- ${targets.length} site(s) collected.\n`);
}

main().catch(err => { console.error('\nFatal:', err.message); process.exit(1); });
