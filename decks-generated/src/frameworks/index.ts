export { executiveBrief, sampleManifest as executiveBriefManifest } from './executive-brief.js';
export { pitchDeck, sampleManifest as pitchDeckManifest } from './pitch-deck.js';
export { strategySCR, sampleManifest as strategySCRManifest } from './strategy-scr.js';
export { techArchitecture, sampleManifest as techArchitectureManifest } from './tech-architecture.js';
export { statusReport, sampleManifest as statusReportManifest } from './status-report.js';

import type { Framework } from '../schemas/framework.js';
import { executiveBrief } from './executive-brief.js';
import { pitchDeck } from './pitch-deck.js';
import { strategySCR } from './strategy-scr.js';
import { techArchitecture } from './tech-architecture.js';
import { statusReport } from './status-report.js';

/** All available framework templates. */
export const FRAMEWORKS: readonly Framework[] = [
  executiveBrief,
  pitchDeck,
  strategySCR,
  techArchitecture,
  statusReport,
] as const;

/** Lookup a framework by its ID. */
export const FRAMEWORKS_BY_ID: Record<string, Framework> = {
  'executive-brief': executiveBrief,
  'pitch-deck': pitchDeck,
  'strategy-scr': strategySCR,
  'tech-architecture': techArchitecture,
  'status-report': statusReport,
} as const;
