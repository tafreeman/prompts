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

/** Base layouts: full ControlPanel — transcribable, effects, background. */
const BASE_FEATURES = { renderAs: true, effects: true, background: true };

layoutRegistry.register("two-col", TwoColLayout, BASE_FEATURES);
layoutRegistry.register("stat-cards", StatCardsLayout, BASE_FEATURES);
layoutRegistry.register("stat-cards-manifest", ManifestStatCardsLayout, BASE_FEATURES);
layoutRegistry.register("before-after", BeforeAfterLayout, BASE_FEATURES);
layoutRegistry.register("h-strip", HStripLayout, BASE_FEATURES);
layoutRegistry.register("process-lanes", ProcessLanesLayout, BASE_FEATURES);
