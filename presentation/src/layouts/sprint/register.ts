import { layoutRegistry } from "../registry.ts";
import { SprintLayout } from "./SprintLayout.tsx";

/** Sprint: specialized process view — effects only. */
layoutRegistry.register("process-cycle", SprintLayout, { effects: true });
