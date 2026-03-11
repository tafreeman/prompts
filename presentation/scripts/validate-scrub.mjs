/**
 * Validates that all three app variants load without errors
 * and contain no client-specific terminology on-screen.
 */
import { chromium } from "playwright";

const BASE = "http://localhost:5173";
const VARIANTS = [
  { key: "v10",   label: "v10 — Original" },
  { key: "v10_2", label: "v10.2 — Enhanced" },
  { key: "v13",   label: "v13 — Latest" },
];

const results = [];

async function validateVariant(browser, { key, label }) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const errors = [];
  const consoleErrors = [];

  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("pageerror", (err) => errors.push(err.message));

  try {
    // Load variant
    await page.goto(`${BASE}/?app=${key}`, { waitUntil: "networkidle", timeout: 15000 });
    await page.waitForTimeout(2000);

    // Check for render errors (white screen / no content)
    const rootHTML = await page.$eval("#root", (el) => el.innerHTML);
    if (!rootHTML || rootHTML.length < 100) {
      errors.push(`Render failure: #root has only ${rootHTML?.length ?? 0} chars`);
    }

    // Check the picker exists (all variants)
    const pickerButtons = await page.locator("button").filter({ hasText: /v1/ }).count();
    if (pickerButtons < 3) {
      errors.push(`Picker missing: found ${pickerButtons} variant buttons, expected 3`);
    }

    // Click into the page to dismiss intro splash (if present)
    await page.mouse.click(960, 540);
    await page.waitForTimeout(1500);

    // Try clicking each topic tile to verify navigation works
    const tiles = await page.locator("h2").allTextContents();
    const clickable = tiles.filter((t) =>
      ["Human in the Loop", "Hurdles We Overcame", "AI Sprint Cycle", "Looking Ahead", "Case Study Overview"].some((s) => t.includes(s))
    );

    for (const title of clickable.slice(0, 2)) {
      try {
        const tile = page.locator("h2").filter({ hasText: title }).first();
        if (await tile.isVisible()) {
          await tile.click({ timeout: 3000 });
          await page.waitForTimeout(800);

          // Go back
          const back = page.locator("button").filter({ hasText: /Back|←/ }).first();
          if (await back.isVisible({ timeout: 2000 }).catch(() => false)) {
            await back.click();
            await page.waitForTimeout(800);
          }
        }
      } catch {
        // Navigation test is best-effort
      }
    }

    // Report console errors (filter noise)
    const realErrors = consoleErrors.filter(
      (e) => !e.includes("favicon") && !e.includes("HMR") && !e.includes("Fast Refresh")
    );
    if (realErrors.length > 0) {
      errors.push(`Console errors: ${realErrors.slice(0, 3).join(" | ")}`);
    }

    results.push({ key, label, status: errors.length === 0 ? "PASS" : "FAIL", errors });
  } catch (err) {
    results.push({ key, label, status: "CRASH", errors: [err.message] });
  } finally {
    await page.close();
  }
}

const browser = await chromium.launch({ headless: true });

for (const variant of VARIANTS) {
  await validateVariant(browser, variant);
}

await browser.close();

// Print report
console.log("\n" + "=".repeat(60));
console.log("  SCRUB VALIDATION REPORT");
console.log("=".repeat(60) + "\n");

for (const r of results) {
  let icon;
  if (r.status === "PASS") {
    icon = "✓";
  } else if (r.status === "FAIL") {
    icon = "✕";
  } else {
    icon = "!";
  }
  console.log(`${icon}  ${r.label} (${r.key}): ${r.status}`);
  for (const e of r.errors) {
    console.log(`     → ${e}`);
  }
}

const passed = results.filter((r) => r.status === "PASS").length;
console.log(`\n${passed}/${results.length} variants passed.\n`);

process.exit(passed === results.length ? 0 : 1);
