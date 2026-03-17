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

/** Onboarding: transcription target — effects only. */
const ONBOARD_FEATURES = { effects: true };

layoutRegistry.register("info-cards", InfoCardsLayout, ONBOARD_FEATURES);
layoutRegistry.register("checklist", ChecklistLayout, ONBOARD_FEATURES);
layoutRegistry.register("workflow", WorkflowLayout, ONBOARD_FEATURES);
layoutRegistry.register("pillars", PillarsLayout, ONBOARD_FEATURES);
layoutRegistry.register("catalog", CatalogLayout, ONBOARD_FEATURES);
layoutRegistry.register("op-brief", OpBriefLayout, ONBOARD_FEATURES);
layoutRegistry.register("op-flow", OpFlowLayout, ONBOARD_FEATURES);
