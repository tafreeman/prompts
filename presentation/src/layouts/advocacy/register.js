/**
 * Register advocacy layouts with the global layout registry.
 *
 * Import this module once (side-effect only) to make all advocacy
 * layouts available via layoutRegistry.get("adv-overview"), etc.
 */

import { layoutRegistry } from "../registry.ts";
import { AdvOverviewLayout } from "./AdvOverviewLayout.tsx";
import { AdvStatsLayout } from "./AdvStatsLayout.tsx";
import { AdvHurdlesLayout } from "./AdvHurdlesLayout.tsx";
import { AdvFutureLayout } from "./AdvFutureLayout.tsx";
import { AdvPlatformLayout } from "./AdvPlatformLayout.tsx";

layoutRegistry.register("adv-overview", AdvOverviewLayout);
layoutRegistry.register("adv-stats", AdvStatsLayout);
layoutRegistry.register("adv-hurdles", AdvHurdlesLayout);
layoutRegistry.register("adv-future", AdvFutureLayout);
layoutRegistry.register("adv-platform", AdvPlatformLayout);
