import { z } from 'zod';
import { ActionTitleSchema, BulletListSchema, SourceSchema } from './guards.js';

// -- Reusable content schemas --------------------------------------------------

const BarSchema = z.object({
  label: z.string(),
  value: z.number(),
  highlight: z.boolean().optional(),   // Highlighted bar (background band)
  accent: z.boolean().optional(),      // Darker accent treatment
});

const BarGroupSchema = z.object({
  id: z.string(),
  label: z.string().optional(),
  bars: z.array(BarSchema).min(1).max(20),
});

const AnnotationItemSchema = z.object({
  label: z.string(),
  value: z.string(),
});

const AnnotationSchema = z.object({
  label: z.string(),
  items: z.array(AnnotationItemSchema).optional(),
});

const SpokeSchema = z.object({
  position: z.enum(["top", "bottom", "left", "right"]),
  label: z.string(),
  eyebrow: z.string().optional(),
});

const HubCenterSchema = z.object({
  label: z.string(),
  sublabel: z.string().optional(),
});

const WorkflowStageSchema = z.object({
  label: z.string(),
  description: z.string().optional(),
  meta: z.string().optional(),
  highlight: z.boolean().optional(),
});

const CycleNodeSchema = z.object({
  label: z.string(),
  body: z.string().optional(),
});

const CardSchema = z.object({
  title: z.string(),
  body: z.string().optional(),
  stat: z.union([z.string(), z.number()]).optional(),
  label: z.string().optional(),
  icon: z.string().optional(),
});

const KpiSchema = z.object({
  value: z.union([z.string(), z.number()]),
  label: z.string(),
  trend: z.enum(["up", "down", "flat"]).optional(),
  detail: z.string().optional(),
});

const StepSchema = z.object({
  label: z.string(),
  description: z.string().optional(),
  icon: z.string().optional(),
});

const EventSchema = z.object({
  date: z.string(),
  title: z.string(),
  description: z.string().optional(),
  icon: z.string().optional(),
});

const ColumnSchema = z.object({
  title: z.string().optional(),
  body: z.string().optional(),
  bullets: BulletListSchema.optional(),
  items: z.array(z.string()).max(7).optional(),
});

const CellSchema = z.object({
  title: z.string(),
  body: z.string().optional(),
  stat: z.union([z.string(), z.number()]).optional(),
  icon: z.string().optional(),
  size: z.enum(["sm", "md", "lg"]).default("md"),
});

// -- Base fields shared by all slides ------------------------------------------

const SlideBase = z.object({
  id: z.string().min(1),
  title: ActionTitleSchema,
  subtitle: z.string().max(200).optional(),
  eyebrow: z.string().max(50).optional(),
  notes: z.string().optional(),           // Speaker notes
  bgOverride: z.string().optional(),      // Per-slide background color override
});

// -- 12 Layout Schemas ---------------------------------------------------------

export const CoverSlide = SlideBase.extend({
  layout: z.literal("cover"),
  tagline: z.string().optional(),
  kpis: z.array(KpiSchema).max(4).optional(),
});

export const SectionSlide = SlideBase.extend({
  layout: z.literal("section"),
  sectionNumber: z.union([z.string(), z.number()]).optional(),
});

export const TextSlide = SlideBase.extend({
  layout: z.literal("text"),
  body: z.string().optional(),
  bullets: BulletListSchema.optional(),
  image: z.string().optional(),           // Image URL or path
  imageAlt: z.string().optional(),
  columns: z.enum(["1", "2"]).default("1"),
  leftColumn: ColumnSchema.optional(),    // Used when columns = "2"
  rightColumn: ColumnSchema.optional(),
  callout: z.string().optional(),
  source: SourceSchema.optional(),
});

export const CardsSlide = SlideBase.extend({
  layout: z.literal("cards"),
  cards: z.array(CardSchema).min(1).max(6),
  callout: z.string().optional(),
  source: SourceSchema.optional(),
});

export const NumberSlide = SlideBase.extend({
  layout: z.literal("number"),
  stat: z.union([z.string(), z.number()]),
  statLabel: z.string(),
  context: z.string().optional(),
  source: SourceSchema.optional(),
});

export const CompareSlide = SlideBase.extend({
  layout: z.literal("compare"),
  left: ColumnSchema,
  right: ColumnSchema,
  callout: z.string().optional(),
  source: SourceSchema.optional(),
});

export const StepsSlide = SlideBase.extend({
  layout: z.literal("steps"),
  steps: z.array(StepSchema).min(2).max(7),
  callout: z.string().optional(),
});

export const TableSlide = SlideBase.extend({
  layout: z.literal("table"),
  columns: z.array(z.string()).min(1).max(8),
  rows: z.array(z.record(z.string(), z.union([z.string(), z.number()]))).min(1),
  highlight: z.string().optional(),       // Row ID or column to highlight
  source: SourceSchema.optional(),
});

export const ScorecardSlide = SlideBase.extend({
  layout: z.literal("scorecard"),
  kpis: z.array(KpiSchema).min(1).max(8),
  callout: z.string().optional(),
  source: SourceSchema.optional(),
});

export const TimelineSlide = SlideBase.extend({
  layout: z.literal("timeline"),
  events: z.array(EventSchema).min(2).max(10),
  callout: z.string().optional(),
});

export const GridSlide = SlideBase.extend({
  layout: z.literal("grid"),
  cells: z.array(CellSchema).min(2).max(9),
  columns: z.union([z.literal(2), z.literal(3), z.literal(4)]).default(3),
  callout: z.string().optional(),
});

export const ClosingSlide = SlideBase.extend({
  layout: z.literal("closing"),
  nextSteps: BulletListSchema.optional(),
  contact: z.string().optional(),
});

// -- 5 New Layout Schemas ------------------------------------------------------

/** Horizontal (or vertical) bar chart with grouped data series. */
export const ChartSlide = SlideBase.extend({
  layout: z.literal("chart"),
  chartType: z.enum(["bar-h", "bar-v"]).default("bar-h"),
  unit: z.string().optional(),          // e.g. "%" or "$M"
  groups: z.array(BarGroupSchema).min(1).max(4),
  annotations: z.array(AnnotationSchema).optional(),
  source: SourceSchema.optional(),
});

/** Hub-and-spoke diagram — center concept with labeled spoke endpoints. */
export const HubSlide = SlideBase.extend({
  layout: z.literal("hub"),
  center: HubCenterSchema,
  spokes: z.array(SpokeSchema).min(2).max(8),
  body: z.string().optional(),
});

/** Three-column process/workflow table — stage | description | meta. */
export const WorkflowSlide = SlideBase.extend({
  layout: z.literal("workflow"),
  columnLabels: z.tuple([z.string(), z.string(), z.string()]).optional(),
  stages: z.array(WorkflowStageSchema).min(2).max(12),
});

/** Circle/arc diagram — input node feeds center, outputs branch right. */
export const CycleSlide = SlideBase.extend({
  layout: z.literal("cycle"),
  centerLabel: z.string().optional(),
  input: CycleNodeSchema.optional(),
  outputs: z.array(CycleNodeSchema).min(1).max(6),
  source: SourceSchema.optional(),
});

/** Large pull-quote with attribution — editorial emphasis. */
export const QuoteSlide = SlideBase.extend({
  layout: z.literal("quote"),
  quote: z.string().max(500),
  attribution: z.string().optional(),
  role: z.string().optional(),
  logo: z.string().optional(),          // company logo URL
});

// -- Discriminated Union -------------------------------------------------------

export const SlideSchema = z.discriminatedUnion("layout", [
  CoverSlide,
  SectionSlide,
  TextSlide,
  CardsSlide,
  NumberSlide,
  CompareSlide,
  StepsSlide,
  TableSlide,
  ScorecardSlide,
  TimelineSlide,
  GridSlide,
  ClosingSlide,
  ChartSlide,
  HubSlide,
  WorkflowSlide,
  CycleSlide,
  QuoteSlide,
]);

export type Slide = z.infer<typeof SlideSchema>;

// -- Layout ID list (for CLI help, validation messages) ------------------------

export const LAYOUT_IDS = [
  "cover", "section", "text", "cards", "number", "compare",
  "steps", "table", "scorecard", "timeline", "grid", "closing",
  "chart", "hub", "workflow", "cycle", "quote",
] as const;

export type LayoutId = typeof LAYOUT_IDS[number];
