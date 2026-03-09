import { capturePresentationScreens, outputPdf, savePdfDeck } from "./export-presentation.mjs";

async function main() {
  const screenshots = await capturePresentationScreens();
  const pdfPath = await savePdfDeck(screenshots);

  console.log(`\nSaved PDF → ${pdfPath || outputPdf}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});