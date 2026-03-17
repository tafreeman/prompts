import { layoutRegistry } from "../registry.ts";
import { AdvdOverviewLayout } from "./AdvdOverviewLayout.tsx";
import { AdvdStatsLayout } from "./AdvdStatsLayout.tsx";
import { AdvdHurdlesLayout } from "./AdvdHurdlesLayout.tsx";
import { AdvdFutureLayout } from "./AdvdFutureLayout.tsx";
import { AdvdPlatformLayout } from "./AdvdPlatformLayout.tsx";

/** Advocacy-dense: transcription target — effects only. */
const ADVD_FEATURES = { effects: true };

layoutRegistry.register("advd-overview", AdvdOverviewLayout, ADVD_FEATURES);
layoutRegistry.register("advd-stats", AdvdStatsLayout, ADVD_FEATURES);
layoutRegistry.register("advd-hurdles", AdvdHurdlesLayout, ADVD_FEATURES);
layoutRegistry.register("advd-future", AdvdFutureLayout, ADVD_FEATURES);
layoutRegistry.register("advd-platform", AdvdPlatformLayout, ADVD_FEATURES);
