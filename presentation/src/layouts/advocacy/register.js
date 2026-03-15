/**
 * Register advocacy layouts with the global layout registry.
 *
 * Import this module once (side-effect only) to make all advocacy
 * layouts available via layoutRegistry.get("adv-overview"), etc.
 */

import { layoutRegistry } from "../registry.ts";
import { AdvOverviewLayout } from "./AdvOverviewLayout.jsx";
import { AdvStatsLayout } from "./AdvStatsLayout.jsx";
import { AdvHurdlesLayout } from "./AdvHurdlesLayout.jsx";
import { AdvFutureLayout } from "./AdvFutureLayout.jsx";
import { AdvPlatformLayout } from "./AdvPlatformLayout.jsx";

layoutRegistry.register("adv-overview", AdvOverviewLayout);
layoutRegistry.register("adv-stats", AdvStatsLayout);
layoutRegistry.register("adv-hurdles", AdvHurdlesLayout);
layoutRegistry.register("adv-future", AdvFutureLayout);
layoutRegistry.register("adv-platform", AdvPlatformLayout);
