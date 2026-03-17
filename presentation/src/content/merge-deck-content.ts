/**
 * Merge utility — combines a deck structure skeleton with swappable text content.
 *
 * Usage:
 *   import { mergeDeckContent } from "./merge-deck-content";
 *   import { structure } from "./genai-advocacy/structure";
 *   import content from "./genai-advocacy/content.json";
 *   // — or swap in different text: —
 *   // import content from "./some-other-deck/content.json";
 *
 *   const { themeId, slides, contentSlides, sprintNodes, deckMeta } =
 *     mergeDeckContent(structure, content);
 *
 * Match priority (for cross-deck content swapping):
 *   1. Exact slide ID match
 *   2. Semantic role match (structure.role === content.role)
 *   3. Layout-type match (structure.layout compatible with content.sourceLayout)
 *   4. Positional fallback (slide at same index)
 *   5. Structure-only (label as title)
 */

import type { DeckContent } from "./content-types";

// ── Semantic role vocabulary ────────────────────────────────────────────
//
// Roles describe the *narrative purpose* of a slide, independent of layout.
// Used for cross-deck content matching when slide IDs don't align.

export type SlideRole =
  | "overview"     // intro/orientation slide
  | "evidence"     // proof points, stats, case study data
  | "challenges"   // hurdles, before/after, problems solved
  | "process"      // workflow, sprint cycle, step-by-step
  | "vision"       // future, roadmap, looking ahead
  | "tools"        // approved tools, guardrails, governance
  | "data"         // tables, charts, quantitative stories
  | "principles"   // beliefs, manifesto, pillars, disciplines
  | "people"       // team, clients, community, belonging
  | "compliance";  // data classification, security, rules

// ── Layout compatibility groups ─────────────────────────────────────────
//
// Layouts that consume similar data shapes. Used for sourceLayout matching.

const LAYOUT_COMPAT: Record<string, readonly string[]> = {
  "two-col":        ["two-col", "adv-overview", "advd-overview", "eng-code-flow"],
  "stat-cards":     ["stat-cards", "info-cards", "adv-stats", "advd-stats", "eng-architecture", "eng-tech-stack", "op-brief"],
  "before-after":   ["before-after", "adv-hurdles", "advd-hurdles"],
  "process-cycle":  ["process-cycle", "hb-process"],
  "h-strip":        ["h-strip", "adv-future", "advd-future", "eng-roadmap", "hb-manifesto"],
  "process-lanes":  ["process-lanes", "adv-platform", "advd-platform"],
  "stat-hero":      ["stat-hero"],
  "quote-collage":  ["quote-collage"],
  "badge-grid":     ["badge-grid"],
  "data-table":     ["data-table"],
  "bar-chart":      ["bar-chart"],
  "color-blocks":   ["color-blocks"],
  "hb-chapter":     ["hb-chapter"],
  "hb-practices":   ["hb-practices"],
  "hb-index":       ["hb-index", "catalog"],
  "workflow":       ["workflow", "op-flow"],
  "checklist":      ["checklist"],
  "pillars":        ["pillars"],
};

function getCompatGroup(layout: string): string | undefined {
  for (const [group, members] of Object.entries(LAYOUT_COMPAT)) {
    if (members.includes(layout)) return group;
  }
  return undefined;
}

// ── Structure types (matches the shape exported by structure.js files) ──

export interface SlideStructure {
  readonly id: string;
  readonly order: number;
  readonly layout: string;
  readonly role?: SlideRole;
  readonly label?: string;
  readonly num?: string;
  readonly optional?: boolean;
  readonly color?: string;
  readonly colorLight?: string;
  readonly colorGlow?: string;
  readonly icon?: string;
}

interface SprintNode {
  readonly abbr: string;
  readonly label: string;
  readonly type: string;
  readonly t?: number;
}

export interface DeckStructure {
  readonly themeId: string;
  readonly introStatColors?: readonly string[];
  readonly sprintNodes: readonly SprintNode[];
  readonly shellSlides: readonly SlideStructure[];
  readonly contentSlides: readonly SlideStructure[];
}

// ── Merge result ────────────────────────────────────────────────────────

export type MatchMethod = "id" | "role" | "layout" | "positional" | "none";

export interface MergedSlide extends SlideStructure {
  readonly matchMethod?: MatchMethod;
  readonly [key: string]: unknown;
}

export interface MergedDeck {
  readonly themeId: string;
  readonly sprintNodes: readonly SprintNode[];
  /** All slides (shell + content), sorted by order */
  readonly slides: readonly MergedSlide[];
  /** Content slides only (shell slides excluded), sorted by order */
  readonly contentSlides: readonly MergedSlide[];
  /** Deck-level text metadata (brandLine, title, tagline, intro, stats) */
  readonly deckMeta: DeckContent["deck"];
  /** Match statistics for UI display */
  readonly matchStats: Readonly<Record<MatchMethod, number>>;
}

// ── Core merge function ─────────────────────────────────────────────────

/**
 * Merge a deck structure with text content.
 *
 * For each content slide in the structure, resolves text content using
 * a cascading match strategy:
 *   1. Exact slide ID match
 *   2. Fallback content by ID (if provided)
 *   3. Semantic role match — finds a content slide with the same `role`
 *   4. Layout compatibility match — finds a content slide whose
 *      `sourceLayout` belongs to the same layout compat group
 *   5. Positional fallback — uses content slide at the same index
 *   6. Structure-only — shows label as title (no content matched)
 */
export function mergeDeckContent(
  structure: DeckStructure,
  content: DeckContent,
  fallback?: DeckContent,
): MergedDeck {
  // Build indexes for role and layout matching
  const contentEntries = Object.entries(content.slides);
  const usedContentIds = new Set<string>();
  const matchCounts: Record<MatchMethod, number> = {
    id: 0, role: 0, layout: 0, positional: 0, none: 0,
  };

  const mergedContentSlides: MergedSlide[] = structure.contentSlides.map(
    (skeleton, index) => {
      // 1. Exact ID match
      const idMatch = content.slides[skeleton.id]
        ?? fallback?.slides[skeleton.id]
        ?? null;
      if (idMatch) {
        usedContentIds.add(skeleton.id);
        matchCounts.id++;
        return { ...idMatch, ...skeleton, matchMethod: "id" as const } as MergedSlide;
      }

      // 2. Role match — find unused content slide with same role
      if (skeleton.role) {
        const roleMatch = contentEntries.find(
          ([id, slide]) =>
            !usedContentIds.has(id) &&
            (slide as Record<string, unknown>).role === skeleton.role,
        );
        if (roleMatch) {
          usedContentIds.add(roleMatch[0]);
          matchCounts.role++;
          return { ...roleMatch[1], ...skeleton, matchMethod: "role" as const } as MergedSlide;
        }
      }

      // 3. Layout compatibility match — find unused content slide with compatible sourceLayout
      const structGroup = getCompatGroup(skeleton.layout);
      if (structGroup) {
        const layoutMatch = contentEntries.find(
          ([id, slide]) => {
            if (usedContentIds.has(id)) return false;
            const srcLayout = (slide as Record<string, unknown>).sourceLayout as string | undefined;
            if (!srcLayout) return false;
            return getCompatGroup(srcLayout) === structGroup;
          },
        );
        if (layoutMatch) {
          usedContentIds.add(layoutMatch[0]);
          matchCounts.layout++;
          return { ...layoutMatch[1], ...skeleton, matchMethod: "layout" as const } as MergedSlide;
        }
      }

      // 4. Positional fallback — use unused content slide at same index
      const unusedEntries = contentEntries.filter(([id]) => !usedContentIds.has(id));
      if (unusedEntries.length > 0) {
        // Pick the first unused entry (preserves original content order)
        const [posId, posContent] = unusedEntries[0];
        usedContentIds.add(posId);
        matchCounts.positional++;
        return { ...posContent, ...skeleton, matchMethod: "positional" as const } as MergedSlide;
      }

      // 5. Structure-only fallback
      matchCounts.none++;
      return { ...skeleton, title: skeleton.label ?? skeleton.id, matchMethod: "none" as const } as MergedSlide;
    },
  );

  const shellSlides: MergedSlide[] = structure.shellSlides.map(
    (s) => ({ ...s }) as MergedSlide,
  );

  const allSlides = [...shellSlides, ...mergedContentSlides].sort(
    (a, b) => a.order - b.order,
  );

  // Attach intro stat colors to deck meta if structure provides them
  const deckMeta = structure.introStatColors
    ? {
        ...content.deck,
        introStats: content.deck.introStats.map((stat, i) => ({
          ...stat,
          color: structure.introStatColors![i] ?? undefined,
        })),
      }
    : content.deck;

  return {
    themeId: structure.themeId,
    sprintNodes: structure.sprintNodes,
    slides: allSlides,
    contentSlides: mergedContentSlides.sort((a, b) => a.order - b.order),
    deckMeta,
    matchStats: matchCounts,
  };
}
