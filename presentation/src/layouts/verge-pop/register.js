/**
 * Verge Pop layout registration — registers all Verge-style layouts with the
 * central layout registry.
 *
 * Import this module once at app bootstrap to make these layouts available.
 */

import { layoutRegistry } from "../registry.ts";
import StatHeroLayout from "./StatHeroLayout.tsx";
import QuoteCollageLayout from "./QuoteCollageLayout.tsx";
import BadgeGridLayout from "./BadgeGridLayout.tsx";
import DataTableLayout from "./DataTableLayout.tsx";
import BarChartLayout from "./BarChartLayout.tsx";
import ColorBlocksLayout from "./ColorBlocksLayout.tsx";

/** Verge-pop: transcription target — effects only, no render-as or background. */
const VERGE_FEATURES = { effects: true };

layoutRegistry.register("stat-hero", StatHeroLayout, VERGE_FEATURES);
layoutRegistry.register("quote-collage", QuoteCollageLayout, VERGE_FEATURES);
layoutRegistry.register("badge-grid", BadgeGridLayout, VERGE_FEATURES);
layoutRegistry.register("data-table", DataTableLayout, VERGE_FEATURES);
layoutRegistry.register("bar-chart", BarChartLayout, VERGE_FEATURES);
layoutRegistry.register("color-blocks", ColorBlocksLayout, VERGE_FEATURES);
