/**
 * Palette utilities — resolve per-slide accent colors from the active theme.
 * Enables any content deck × any theme combination.
 */

import type { Theme } from "./themes";

/* ── hex helpers ─────────────────────────────────────────── */

export function lightenHex(hex: string, amount: number): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  const l = (c: number) => Math.round(c + (255 - c) * amount);
  return `#${[l(r), l(g), l(b)].map((c) => c.toString(16).padStart(2, "0")).join("")}`;
}

export function hexToGlow(hex: string, alpha = 0.25): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

/* ── palette from theme ─────────────────────────────────── */

/** Build a rotation palette from a theme's semantic tokens. */
export function buildPalette(theme: Theme): string[] {
  return [
    theme.accent,
    theme.gradient[0],
    theme.gradient[1],
    theme.success,
    theme.warning,
    theme.danger,
  ].filter(Boolean);
}

export interface SlideColor {
  readonly color: string;
  readonly colorLight: string;
  readonly colorGlow: string;
}

/** Resolve color / colorLight / colorGlow for one slide by index. */
export function resolveSlideColor(theme: Theme, slideIndex: number): SlideColor {
  const palette = buildPalette(theme);
  const base = palette[slideIndex % palette.length];
  return {
    color: base,
    colorLight: lightenHex(base, 0.3),
    colorGlow: hexToGlow(base, 0.25),
  };
}

/** Re-color an entire topics array from the active theme. */
export function resolveTopicColors<T extends Record<string, unknown>>(
  topics: readonly T[],
  theme: Theme,
): (T & SlideColor)[] {
  return topics.map((topic, idx) => ({
    ...topic,
    ...resolveSlideColor(theme, idx),
  }));
}

export interface IntroStat {
  readonly val: string;
  readonly lbl: string;
  readonly color: string;
}

/** Re-color intro-stat items from the active theme. */
export function resolveIntroStatColors(
  stats: readonly IntroStat[],
  theme: Theme,
): IntroStat[] {
  const palette = buildPalette(theme);
  return stats.map((stat, idx) => ({
    ...stat,
    color: palette[idx % palette.length],
  }));
}
