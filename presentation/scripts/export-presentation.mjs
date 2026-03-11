import { chromium } from "playwright";
import { PDFDocument } from "pdf-lib";
import { createServer } from "vite";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");

export const outputDir = path.join(rootDir, "single-file");
export const slideImagesDir = path.join(outputDir, "slide-images");
export const outputPdf = path.join(outputDir, "GenAI-Advocacy-Deck.pdf");

export const viewport = { width: 1920, height: 1080 };

const TIMEOUTS = {
  themeButton: 10_000,
  selector: 15_000,
  backButton: 10_000,
};

export const SLIDES = [
  { id: "intro", label: "Intro Splash" },
  { id: "landing", label: "Navigation Hub" },
  { id: "overview", label: "Case Study Overview" },
  { id: "human", label: "Human in the Loop" },
  { id: "hurdles", label: "Hurdles We Overcame" },
  { id: "sprint", label: "AI Sprint Cycle" },
  { id: "future", label: "Looking Ahead" },
  { id: "platform", label: "Service Platform" },
];

const TILE_TITLES = {
  overview: "Case Study Overview",
  human: "Human in the Loop",
  hurdles: "Hurdles We Overcame",
  sprint: "AI Sprint Cycle",
  future: "Looking Ahead",
  platform: "Service Platform",
};

const CAPTURE_ORDER = ["overview", "human", "hurdles", "sprint", "future", "platform"];

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

async function waitForLanding(page) {
  await page.waitForSelector("h2", { timeout: TIMEOUTS.selector });
  await waitForStableRender(page);
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

async function selectTheme(page) {
  const themeButton = page.locator("button").filter({ hasText: "Midnight Teal" }).first();
  await themeButton.waitFor({ state: "visible", timeout: TIMEOUTS.themeButton });
  await themeButton.click();
}

async function dismissIntroToLanding(page) {
  await page.mouse.click(viewport.width / 2, viewport.height / 2);
  await waitForLanding(page);
}

async function restoreLanding(page, url) {
  await page.goto(url, { waitUntil: "networkidle" });
  await selectTheme(page);
  await dismissIntroToLanding(page);
}

async function clickTile(page, title) {
  const h2 = page.locator("h2").filter({ hasText: title });
  const altTile = page.locator("div[style*='cursor: pointer']").filter({ hasText: title });
  const tile = (await h2.first().isVisible().catch(() => false)) ? h2.first() : altTile.first();

  await tile.waitFor({ state: "visible", timeout: TIMEOUTS.selector });
  await tile.click();
}

async function goBack(page) {
  const backButton = page.locator("button").filter({ hasText: "Back" }).first();
  await backButton.waitFor({ state: "visible", timeout: TIMEOUTS.backButton });
  await backButton.click();
  await waitForLanding(page);
}

async function capture(page, label) {
  await waitForStableRender(page);
  const png = await page.screenshot({ type: "png" });
  console.log(`  ✓ ${label}`);
  return png;
}

function assertAllSlidesCaptured(screenshots) {
  const missing = SLIDES.filter(({ id }) => !screenshots.has(id)).map(({ label }) => label);

  if (missing.length > 0) {
    throw new Error(`Export did not capture all slides. Missing: ${missing.join(", ")}`);
  }
}

export async function capturePresentationScreens() {
  await mkdir(outputDir, { recursive: true });

  console.log("Starting Vite dev server...");
  const { server, url } = await startDevServer();
  console.log(`  → ${url}\n`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport });
  const screenshots = new Map();
  const failures = [];

  try {
    await page.goto(url, { waitUntil: "networkidle" });

    console.log("Selecting theme...");
    await selectTheme(page);

    console.log("Capturing slides...");
    screenshots.set("intro", await capture(page, "Intro Splash"));

    await dismissIntroToLanding(page);
    screenshots.set("landing", await capture(page, "Navigation Hub"));

    for (const id of CAPTURE_ORDER) {
      try {
        await clickTile(page, TILE_TITLES[id]);
        screenshots.set(id, await capture(page, TILE_TITLES[id]));
        await goBack(page);
      } catch (error) {
        const reason = error instanceof Error ? error.message : String(error);
        failures.push(`${TILE_TITLES[id]} (${reason})`);
        console.warn(`  ⚠ Failed to capture ${TILE_TITLES[id]}: ${reason}`);
        await restoreLanding(page, url);
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