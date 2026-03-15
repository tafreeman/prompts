/**
 * register.js — self-registration of base layouts into the global registry.
 *
 * Import this module once at app startup (e.g. in main.jsx) to make all
 * base-family layouts available via layoutRegistry.get("two-col"), etc.
 */

import { layoutRegistry } from "../registry.ts";

import TwoColLayout from "./TwoColLayout.tsx";
import StatCardsLayout, {
  ManifestStatCardsLayout,
} from "./StatCardsLayout.tsx";
import BeforeAfterLayout from "./BeforeAfterLayout.tsx";
import HStripLayout from "./HStripLayout.tsx";
import ProcessLanesLayout from "./ProcessLanesLayout.tsx";

layoutRegistry.register("two-col", TwoColLayout);
layoutRegistry.register("stat-cards", StatCardsLayout);
layoutRegistry.register("stat-cards-manifest", ManifestStatCardsLayout);
layoutRegistry.register("before-after", BeforeAfterLayout);
layoutRegistry.register("h-strip", HStripLayout);
layoutRegistry.register("process-lanes", ProcessLanesLayout);
