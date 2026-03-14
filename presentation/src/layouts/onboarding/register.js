/**
 * Register onboarding layouts with the global layout registry.
 *
 * Import this module once (side-effect only) to make all onboarding
 * layouts available via layoutRegistry.get("info-cards"), etc.
 */

import { layoutRegistry } from "../registry.ts";
import InfoCardsLayout from "./InfoCardsLayout.jsx";
import ChecklistLayout from "./ChecklistLayout.jsx";
import WorkflowLayout from "./WorkflowLayout.jsx";
import PillarsLayout from "./PillarsLayout.jsx";
import CatalogLayout from "./CatalogLayout.jsx";
import OpBriefLayout from "./OpBriefLayout.jsx";
import OpFlowLayout from "./OpFlowLayout.jsx";

layoutRegistry.register("info-cards", InfoCardsLayout);
layoutRegistry.register("checklist", ChecklistLayout);
layoutRegistry.register("workflow", WorkflowLayout);
layoutRegistry.register("pillars", PillarsLayout);
layoutRegistry.register("catalog", CatalogLayout);
layoutRegistry.register("op-brief", OpBriefLayout);
layoutRegistry.register("op-flow", OpFlowLayout);
