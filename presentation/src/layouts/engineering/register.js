/**
 * register.js — self-registration of engineering layouts into the global registry.
 */

import { layoutRegistry } from "../registry.ts";

import ArchitectureSlide from "./ArchitectureSlide.jsx";
import CodeFlowDiagram from "./CodeFlowDiagram.jsx";
import TechStackTimeline from "./TechStackTimeline.jsx";
import RoadmapMilestones from "./RoadmapMilestones.jsx";

layoutRegistry.register("eng-architecture", ArchitectureSlide);
layoutRegistry.register("eng-code-flow", CodeFlowDiagram);
layoutRegistry.register("eng-tech-stack", TechStackTimeline);
layoutRegistry.register("eng-roadmap", RoadmapMilestones);
