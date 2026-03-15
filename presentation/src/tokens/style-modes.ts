/**
 * Style modes — visual chrome variants that control layout treatment.
 * Independent of color themes: any theme × any style mode.
 *
 *  default   — current rounded-glow tech feel
 *  brutalist — sharp edges, thick borders, no glow, uppercase labels
 *  editorial — thin rules, generous whitespace, serif-leaning
 *  pop       — bold flat zine feel
 */

export interface StyleMode {
  readonly id: StyleModeId;
  readonly name: string;
  readonly vibe: string;
  readonly cardRadius: number;
  readonly innerRadius: number;
  readonly cardBorderWidth: number;
  readonly accentBarHeight: number;
  readonly sectionGap: number;
  readonly tileRadius: number;
  readonly pillRadius: number;
  readonly tagRadius: number;
  readonly useGlow: boolean;
  readonly useSoftShadow: boolean;
  readonly headingWeight: number;
  readonly headingTransform: "none" | "uppercase";
  readonly labelTracking: number;
}

export type StyleModeId = "default" | "brutalist" | "editorial" | "pop";

export const STYLE_MODES: readonly StyleMode[] = [
  {
    id: "default",
    name: "Default",
    vibe: "Modern Tech",
    cardRadius: 16,
    innerRadius: 12,
    cardBorderWidth: 1,
    accentBarHeight: 3,
    sectionGap: 28,
    tileRadius: 16,
    pillRadius: 999,
    tagRadius: 999,
    useGlow: true,
    useSoftShadow: true,
    headingWeight: 700,
    headingTransform: "none",
    labelTracking: 3,
  },
  {
    id: "brutalist",
    name: "Brutalist",
    vibe: "Swiss Systems",
    cardRadius: 0,
    innerRadius: 0,
    cardBorderWidth: 3,
    accentBarHeight: 6,
    sectionGap: 20,
    tileRadius: 0,
    pillRadius: 2,
    tagRadius: 0,
    useGlow: false,
    useSoftShadow: false,
    headingWeight: 900,
    headingTransform: "uppercase",
    labelTracking: 4,
  },
  {
    id: "editorial",
    name: "Editorial",
    vibe: "Magazine Pacing",
    cardRadius: 4,
    innerRadius: 4,
    cardBorderWidth: 1,
    accentBarHeight: 1,
    sectionGap: 36,
    tileRadius: 8,
    pillRadius: 999,
    tagRadius: 4,
    useGlow: false,
    useSoftShadow: true,
    headingWeight: 600,
    headingTransform: "none",
    labelTracking: 5,
  },
  {
    id: "pop",
    name: "Pop Art",
    vibe: "Bold Flat Zine",
    cardRadius: 16,
    innerRadius: 12,
    cardBorderWidth: 3,
    accentBarHeight: 6,
    sectionGap: 20,
    tileRadius: 16,
    pillRadius: 999,
    tagRadius: 12,
    useGlow: false,
    useSoftShadow: false,
    headingWeight: 700,
    headingTransform: "none",
    labelTracking: 2,
  },
];

export const STYLE_MODES_BY_ID: Record<StyleModeId, StyleMode> = Object.fromEntries(
  STYLE_MODES.map((m) => [m.id, m]),
) as Record<StyleModeId, StyleMode>;

export default STYLE_MODES;
