/**
 * Verge Pop layout registration — registers all Verge-style layouts with the
 * central layout registry.
 *
 * Import this module once at app bootstrap to make these layouts available.
 */

import { layoutRegistry } from "../registry.ts";
import StatHeroLayout from "./StatHeroLayout.jsx";
import QuoteCollageLayout from "./QuoteCollageLayout.jsx";
import BadgeGridLayout from "./BadgeGridLayout.jsx";
import DataTableLayout from "./DataTableLayout.jsx";
import BarChartLayout from "./BarChartLayout.jsx";
import ColorBlocksLayout from "./ColorBlocksLayout.jsx";

layoutRegistry.register("stat-hero", StatHeroLayout);
layoutRegistry.register("quote-collage", QuoteCollageLayout);
layoutRegistry.register("badge-grid", BadgeGridLayout);
layoutRegistry.register("data-table", DataTableLayout);
layoutRegistry.register("bar-chart", BarChartLayout);
layoutRegistry.register("color-blocks", ColorBlocksLayout);
