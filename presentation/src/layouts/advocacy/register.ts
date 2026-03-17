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

/** Advocacy: transcription target — effects only. */
const ADV_FEATURES = { effects: true };

layoutRegistry.register("adv-overview", AdvOverviewLayout, ADV_FEATURES);
layoutRegistry.register("adv-stats", AdvStatsLayout, ADV_FEATURES);
layoutRegistry.register("adv-hurdles", AdvHurdlesLayout, ADV_FEATURES);
layoutRegistry.register("adv-future", AdvFutureLayout, ADV_FEATURES);
layoutRegistry.register("adv-platform", AdvPlatformLayout, ADV_FEATURES);
