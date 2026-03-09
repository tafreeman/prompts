import { capturePresentationScreens, saveSlideImages, slideImagesDir } from "./export-presentation.mjs";

async function main() {
  const screenshots = await capturePresentationScreens();
  const files = await saveSlideImages(screenshots);

  console.log(`\nSaved ${files.length} slide image(s) → ${slideImagesDir}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});