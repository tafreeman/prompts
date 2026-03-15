import { layoutRegistry } from "../registry.ts";
import { AdvdOverviewLayout } from "./AdvdOverviewLayout.tsx";
import { AdvdStatsLayout } from "./AdvdStatsLayout.tsx";
import { AdvdHurdlesLayout } from "./AdvdHurdlesLayout.tsx";
import { AdvdFutureLayout } from "./AdvdFutureLayout.tsx";
import { AdvdPlatformLayout } from "./AdvdPlatformLayout.tsx";

layoutRegistry.register("advd-overview", AdvdOverviewLayout);
layoutRegistry.register("advd-stats", AdvdStatsLayout);
layoutRegistry.register("advd-hurdles", AdvdHurdlesLayout);
layoutRegistry.register("advd-future", AdvdFutureLayout);
layoutRegistry.register("advd-platform", AdvdPlatformLayout);
