import { chromium } from "playwright";
import { PDFDocument } from "pdf-lib";
import { createServer } from "vite";
import { mkdir, writeFile, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");

export const outputDir = path.join(rootDir, "single-file");
export const slideImagesDir = path.join(outputDir, "slide-images");

export const viewport = { width: 1920, height: 1080 };

const TIMEOUTS = {
  selector: 15_000,
  backButton: 10_000,
};

// ── Deck manifest ────────────────────────────────────────────────────
// Resolve deck from CLI arg or default to onboarding.
const deckArg = process.argv[2] || "onboarding";
const contentDir = path.join(rootDir, "src", "content", deckArg);

// Read content.json directly (no TypeScript dependency chain)
const contentJson = JSON.parse(
  await readFile(path.join(contentDir, "content.json"), "utf-8")
);

const slideIds = Object.keys(contentJson.slides);
const TILE_TITLES = Object.fromEntries(
  slideIds.map((id) => [id, contentJson.slides[id].title])
);

export const outputPdf = path.join(
  outputDir,
  `${contentJson.deck?.title || deckArg}-Deck.pdf`
);

// SLIDES list: landing + each content slide
export const SLIDES = [
  { id: "landing", label: "Navigation Hub" },
  ...slideIds.map((id) => ({ id, label: TILE_TITLES[id] })),
];

// ── Helpers ──────────────────────────────────────────────────────────

async function startDevServer() {
  const server = await createServer({
    root: rootDir,
    server: { host: "127.0.0.1", port: 0, strictPort: false },
  });

  await server.listen();
  await new Promise((resolve) => setTimeout(resolve, 250));

  const localUrl = server.resolvedUrls?.local?.[0];
  const address = server.httpServer?.address();
  const port = typeof address === "object" && address ? address.port : null;

  if (!localUrl && !port) {
    await server.close();
    throw new Error("Unable to determine the Vite dev server port.");
  }

  return { server, url: localUrl ?? `http://127.0.0.1:${port}` };
}

async function waitForStableRender(page) {
  await page.waitForLoadState("networkidle").catch(() => {});
  await page.evaluate(async () => {
    if ("fonts" in document) {
      await document.fonts.ready;
    }

    await new Promise((resolve) => {
      requestAnimationFrame(() => requestAnimationFrame(resolve));
    });
  });
}

async function waitForLanding(page) {
  // Wait for any visible text content to appear on the landing page
  await page.locator("h2, h3, [class*='title']").first().waitFor({
    state: "visible",
    timeout: TIMEOUTS.selector,
  });
  await waitForStableRender(page);
}

async function clickTile(page, title) {
  // Nav hub tiles have visible title text — click it directly
  const byText = page.getByText(title, { exact: true }).first();
  const byPartial = page.getByText(title, { exact: false }).first();

  const target = (await byText.isVisible().catch(() => false))
    ? byText
    : byPartial;

  await target.waitFor({ state: "visible", timeout: TIMEOUTS.selector });
  await target.click({ force: true });
}

async function goBack(page) {
  const backButton = page.locator("button").filter({ hasText: "Back" }).first();
  await backButton.waitFor({ state: "visible", timeout: TIMEOUTS.backButton });
  await backButton.click({ force: true });
  await waitForLanding(page);
}

// CSS injected to hide all UI chrome so slides fill the full viewport
const HIDE_CHROME_CSS = `
  [style*="position: fixed"][style*="z-index: 1000"],
  [style*="position: fixed"][style*="z-index: 200"],
  [style*="position: fixed"][style*="zIndex: 1000"],
  [style*="position: fixed"][style*="zIndex: 200"],
  button:has(> span) { }
`;

async function hideChrome(page) {
  await page.evaluate(() => {
    // Hide ControlPanel (fixed, right:0, z-index:1000)
    // Hide layout cycle toolbar (fixed, bottom:20, z-index:200)
    // Hide one-pager toggle (fixed, top:16, right:60, z-index:200)
    document.querySelectorAll('[style]').forEach(el => {
      const s = el.getAttribute('style') || '';
      if (
        (s.includes('position: fixed') || s.includes('position:fixed')) &&
        (s.includes('z-index: 1000') || s.includes('z-index:1000') ||
         s.includes('z-index: 200') || s.includes('z-index:200') ||
         s.includes('zIndex') )
      ) {
        el.dataset.exportHidden = el.style.display;
        el.style.display = 'none';
      }
    });
  });
}

async function showChrome(page) {
  await page.evaluate(() => {
    document.querySelectorAll('[data-export-hidden]').forEach(el => {
      el.style.display = el.dataset.exportHidden || '';
      delete el.dataset.exportHidden;
    });
  });
}

async function capture(page, label) {
  await waitForStableRender(page);
  await hideChrome(page);
  const png = await page.screenshot({ type: "png" });
  await showChrome(page);
  console.log(`  ✓ ${label}`);
  return png;
}

function assertAllSlidesCaptured(screenshots) {
  const missing = SLIDES.filter(({ id }) => !screenshots.has(id)).map(({ label }) => label);

  if (missing.length > 0) {
    throw new Error(`Export did not capture all slides. Missing: ${missing.join(", ")}`);
  }
}

// ── Main capture flow ────────────────────────────────────────────────

export async function capturePresentationScreens() {
  await mkdir(outputDir, { recursive: true });

  console.log(`Exporting deck: ${deckArg}`);
  console.log("Starting Vite dev server...");
  const { server, url } = await startDevServer();
  const deckUrl = `${url}?deck=${deckArg}`;
  console.log(`  → ${deckUrl}\n`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport });
  const screenshots = new Map();
  const failures = [];

  try {
    await page.goto(deckUrl, { waitUntil: "networkidle" });

    // Dismiss any intro splash by clicking center of viewport
    await page.mouse.click(viewport.width / 2, viewport.height / 2);
    await waitForLanding(page);

    console.log("Capturing slides...");
    screenshots.set("landing", await capture(page, "Navigation Hub"));

    for (const id of slideIds) {
      try {
        await clickTile(page, TILE_TITLES[id]);

        // Wait for slide content to render
        await waitForStableRender(page);
        await new Promise((resolve) => setTimeout(resolve, 500));

        screenshots.set(id, await capture(page, TILE_TITLES[id]));
        await goBack(page);
      } catch (error) {
        const reason = error instanceof Error ? error.message : String(error);
        failures.push(`${TILE_TITLES[id]} (${reason})`);
        console.warn(`  ⚠ Failed to capture ${TILE_TITLES[id]}: ${reason}`);
        // Recover by navigating back to landing
        await page.goto(deckUrl, { waitUntil: "networkidle" });
        await page.mouse.click(viewport.width / 2, viewport.height / 2);
        await waitForLanding(page);
      }
    }

    if (failures.length > 0) {
      console.warn(`\nCapture completed with ${failures.length} warning(s):`);
      for (const failure of failures) {
        console.warn(`  • ${failure}`);
      }
    }

    return screenshots;
  } finally {
    await browser.close();
    await server.close();
  }
}

// ── Image export ─────────────────────────────────────────────────────

export async function saveSlideImages(screenshots) {
  assertAllSlidesCaptured(screenshots);
  await mkdir(slideImagesDir, { recursive: true });

  const files = [];
  console.log("\nSaving slide images...");

  for (let index = 0; index < SLIDES.length; index += 1) {
    const { id, label } = SLIDES[index];
    const png = screenshots.get(id);
    if (!png) {
      console.warn(`  ⚠ Missing screenshot for ${label}`);
      continue;
    }

    const filename = `${String(index + 1).padStart(2, "0")}-${id}.png`;
    const filePath = path.join(slideImagesDir, filename);
    await writeFile(filePath, png);
    files.push(filePath);
    console.log(`  ✓ ${filename}`);
  }

  return files;
}

// ── PDF export ───────────────────────────────────────────────────────

export async function savePdfDeck(screenshots) {
  assertAllSlidesCaptured(screenshots);
  const pdf = await PDFDocument.create();

  console.log("\nBuilding PDF deck...");

  for (const { id, label } of SLIDES) {
    const png = screenshots.get(id);
    if (!png) {
      console.warn(`  ⚠ Skipping ${label}; screenshot was not captured.`);
      continue;
    }

    const embeddedImage = await pdf.embedPng(png);
    const page = pdf.addPage([viewport.width, viewport.height]);
    page.drawImage(embeddedImage, {
      x: 0,
      y: 0,
      width: viewport.width,
      height: viewport.height,
    });
    console.log(`  ✓ ${label}`);
  }

  await writeFile(outputPdf, await pdf.save());
  return outputPdf;
}
