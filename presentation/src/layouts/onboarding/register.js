/**
 * Register onboarding layouts with the global layout registry.
 *
 * Import this module once (side-effect only) to make all onboarding
 * layouts available via layoutRegistry.get("info-cards"), etc.
 */

import { layoutRegistry } from "../registry.ts";
import InfoCardsLayout from "./InfoCardsLayout.tsx";
import ChecklistLayout from "./ChecklistLayout.tsx";
import WorkflowLayout from "./WorkflowLayout.tsx";
import PillarsLayout from "./PillarsLayout.tsx";
import CatalogLayout from "./CatalogLayout.tsx";
import OpBriefLayout from "./OpBriefLayout.tsx";
import OpFlowLayout from "./OpFlowLayout.tsx";

layoutRegistry.register("info-cards", InfoCardsLayout);
layoutRegistry.register("checklist", ChecklistLayout);
layoutRegistry.register("workflow", WorkflowLayout);
layoutRegistry.register("pillars", PillarsLayout);
layoutRegistry.register("catalog", CatalogLayout);
layoutRegistry.register("op-brief", OpBriefLayout);
layoutRegistry.register("op-flow", OpFlowLayout);
