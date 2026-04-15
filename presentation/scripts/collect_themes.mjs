import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const THEMES = [
  "base", "mono", "cosmic-night", "neo-brutalism", 
  "vintage-paper", "modern-minimal", "bubblegum", 
  "violet-bloom", "doom-64"
];

async function collectThemes() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const results = [];

  for (const theme of THEMES) {
    const url = `https://v0.app/chat/design-systems/v0example--${theme}`;
    console.log(`Navigating to ${url}...`);
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      // Wait a bit for CSS to apply
      await page.waitForTimeout(3000);
      
      console.log(`Extracting variables for ${theme}...`);
      const variables = await page.evaluate(() => {
        const styles = window.getComputedStyle(document.documentElement);
        const vars = {};
        for (let i = 0; i < styles.length; i++) {
          const prop = styles[i];
          if (prop.startsWith('--')) {
            const val = styles.getPropertyValue(prop);
            if (val && val.trim() !== '') {
              vars[prop] = val.trim();
            }
          }
        }
        return vars;
      });
      
      results.push({
        themeName: theme,
        url: url,
        timestamp: new Date().toISOString(),
        variables: variables
      });
      console.log(`Successfully collected ${Object.keys(variables).length} vars for ${theme}`);
      
    } catch (e) {
      console.error(`Failed to collect ${theme}:`, e.message);
    }
  }

  await browser.close();
  
  const outPath = path.join(__dirname, '..', 'src', 'tokens', 'raw-themes', 'all_themes.json');
  fs.writeFileSync(outPath, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`Saved all themes to ${outPath}`);
}

collectThemes().catch(console.error);
