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

layoutRegistry.register("stat-hero", StatHeroLayout);
layoutRegistry.register("quote-collage", QuoteCollageLayout);
layoutRegistry.register("badge-grid", BadgeGridLayout);
layoutRegistry.register("data-table", DataTableLayout);
layoutRegistry.register("bar-chart", BarChartLayout);
layoutRegistry.register("color-blocks", ColorBlocksLayout);
