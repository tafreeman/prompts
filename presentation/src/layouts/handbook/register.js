import { layoutRegistry } from "../registry.ts";
import { HbChapterLayout } from "./HbChapterLayout.jsx";
import { HbPracticesLayout } from "./HbPracticesLayout.jsx";
import { HbProcessLayout } from "./HbProcessLayout.jsx";
import { HbManifestoLayout } from "./HbManifestoLayout.jsx";
import { HbIndexLayout } from "./HbIndexLayout.jsx";

layoutRegistry.registerBatch({
  "hb-chapter": HbChapterLayout,
  "hb-practices": HbPracticesLayout,
  "hb-process": HbProcessLayout,
  "hb-manifesto": HbManifestoLayout,
  "hb-index": HbIndexLayout,
});
