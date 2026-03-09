import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..");
const distDir = path.join(projectRoot, "dist");
const outputDir = path.join(projectRoot, "single-file");
const outputFile = path.join(outputDir, "genai-advocacy-hub.html");

const FONT_CSS_URL =
  "https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Barlow:wght@400;500;600&family=Chakra+Petch:wght@500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,700&family=DM+Serif+Display&family=JetBrains+Mono:wght@500;700;800&family=Karla:wght@400;500;600;700&family=Nunito+Sans:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap";

const REQUEST_HEADERS = {
  "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
};

function escapeInlineTagContent(source) {
  return source.replace(/<\/(script|style)/gi, "<\\/$1");
}

function isLocalAsset(href) {
  return !/^(?:[a-z]+:)?\/\//i.test(href) && !href.startsWith("data:");
}

function resolveDistAsset(assetPath) {
  const normalized = assetPath.replace(/^\.\//, "");
  return path.resolve(distDir, normalized);
}

function selectLatinFontFaces(css) {
  const blocks = css.match(/(?:\/\*[\s\S]*?\*\/\s*)?@font-face\s*{[\s\S]*?}/g) ?? [];
  const latinBlocks = blocks.filter(
    (block) =>
      /\/\*\s*latin\s*\*\//i.test(block) ||
      /unicode-range:\s*[^;]*U\+0000-00FF/i.test(block) ||
      /unicode-range:\s*[^;]*U\+0131/i.test(block)
  );

  return (latinBlocks.length ? latinBlocks : blocks).join("\n\n");
}

function fontMimeType(fontUrl) {
  const pathname = new URL(fontUrl).pathname.toLowerCase();
  if (pathname.endsWith(".woff2")) return "font/woff2";
  if (pathname.endsWith(".woff")) return "font/woff";
  if (pathname.endsWith(".ttf")) return "font/ttf";
  if (pathname.endsWith(".otf")) return "font/otf";
  return "application/octet-stream";
}

async function fetchText(url) {
  const response = await fetch(url, { headers: REQUEST_HEADERS });
  if (!response.ok) {
    throw new Error(`Failed to fetch text asset: ${url} (${response.status})`);
  }
  return response.text();
}

async function fetchBuffer(url) {
  const response = await fetch(url, { headers: REQUEST_HEADERS });
  if (!response.ok) {
    throw new Error(`Failed to fetch binary asset: ${url} (${response.status})`);
  }
  return Buffer.from(await response.arrayBuffer());
}

async function buildEmbeddedFontCss() {
  const rawCss = await fetchText(FONT_CSS_URL);
  const latinCss = selectLatinFontFaces(rawCss);
  const fontUrls = [
    ...new Set(
      Array.from(
        latinCss.matchAll(/url\((['"]?)(https:[^)'"]+)\1\)/g),
        (match) => match[2]
      )
    ),
  ];

  const urlMap = new Map();
  for (const fontUrl of fontUrls) {
    const fontData = await fetchBuffer(fontUrl);
    urlMap.set(fontUrl, `data:${fontMimeType(fontUrl)};base64,${fontData.toString("base64")}`);
  }

  return latinCss.replace(/url\((['"]?)(https:[^)'"]+)\1\)/g, (_match, _quote, fontUrl) => {
    return `url("${urlMap.get(fontUrl)}")`;
  });
}

async function inlineLocalStylesheets(html) {
  const matches = [...html.matchAll(/<link\b[^>]*rel=["']stylesheet["'][^>]*href=["']([^"']+)["'][^>]*>/gi)];
  let nextHtml = html;

  for (const match of matches) {
    const [fullTag, href] = match;
    if (!isLocalAsset(href)) continue;
    const cssPath = resolveDistAsset(href);
    const css = await fs.readFile(cssPath, "utf8");
    nextHtml = nextHtml.replace(fullTag, () => `<style>\n${escapeInlineTagContent(css)}\n</style>`);
  }

  return nextHtml;
}

async function inlineLocalScripts(html) {
  const matches = [...html.matchAll(/<script\b([^>]*)\bsrc=["']([^"']+)["']([^>]*)><\/script>/gi)];
  let nextHtml = html;

  for (const match of matches) {
    const [fullTag, beforeAttrs, src, afterAttrs] = match;
    if (!isLocalAsset(src)) continue;
    const scriptPath = resolveDistAsset(src);
    const script = await fs.readFile(scriptPath, "utf8");
    const attrs = `${beforeAttrs} ${afterAttrs}`.replace(/\bcrossorigin\b/gi, "").trim();
    const attrText = attrs ? ` ${attrs}` : "";
    nextHtml = nextHtml.replace(
      fullTag,
      () => `<script${attrText}>\n${escapeInlineTagContent(script)}\n</script>`
    );
  }

  return nextHtml;
}

async function copyImages() {
  const srcDir = path.join(distDir, "images");
  const dstDir = path.join(outputDir, "images");
  let entries;
  try {
    entries = await fs.readdir(srcDir);
  } catch {
    return; // no images directory — nothing to copy
  }
  await fs.mkdir(dstDir, { recursive: true });
  for (const filename of entries) {
    await fs.copyFile(path.join(srcDir, filename), path.join(dstDir, filename));
  }
  console.log(`Copied ${entries.length} image(s) to ${dstDir}`);
}

async function main() {
  const htmlPath = path.join(distDir, "index.html");
  let html = await fs.readFile(htmlPath, "utf8");

  html = await inlineLocalStylesheets(html);
  html = await inlineLocalScripts(html);

  const embeddedFontCss = await buildEmbeddedFontCss();
  html = html.replace(
    "</head>",
    `  <style id="embedded-fonts">\n${escapeInlineTagContent(embeddedFontCss)}\n  </style>\n</head>`
  );

  await fs.mkdir(outputDir, { recursive: true });
  await fs.writeFile(outputFile, html, "utf8");
  await copyImages();

  console.log(`Wrote standalone HTML to ${outputFile}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
