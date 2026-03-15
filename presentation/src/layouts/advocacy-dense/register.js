import { layoutRegistry } from "../registry.ts";
import { AdvdOverviewLayout } from "./AdvdOverviewLayout.jsx";
import { AdvdStatsLayout } from "./AdvdStatsLayout.jsx";
import { AdvdHurdlesLayout } from "./AdvdHurdlesLayout.jsx";
import { AdvdFutureLayout } from "./AdvdFutureLayout.jsx";
import { AdvdPlatformLayout } from "./AdvdPlatformLayout.jsx";

layoutRegistry.register("advd-overview", AdvdOverviewLayout);
layoutRegistry.register("advd-stats", AdvdStatsLayout);
layoutRegistry.register("advd-hurdles", AdvdHurdlesLayout);
layoutRegistry.register("advd-future", AdvdFutureLayout);
layoutRegistry.register("advd-platform", AdvdPlatformLayout);
