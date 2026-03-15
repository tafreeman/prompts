import { layoutRegistry } from "../registry.ts";
import { HbChapterLayout } from "./HbChapterLayout.tsx";
import { HbPracticesLayout } from "./HbPracticesLayout.tsx";
import { HbProcessLayout } from "./HbProcessLayout.tsx";
import { HbManifestoLayout } from "./HbManifestoLayout.tsx";
import { HbIndexLayout } from "./HbIndexLayout.tsx";

layoutRegistry.registerBatch({
  "hb-chapter": HbChapterLayout,
  "hb-practices": HbPracticesLayout,
  "hb-process": HbProcessLayout,
  "hb-manifesto": HbManifestoLayout,
  "hb-index": HbIndexLayout,
});
