/**
 * Animation timing constants and easing functions.
 * Centralises all magic timing values from the monolith.
 *
 * CSS durations are in seconds (for inline style `transition`).
 * Phase delays are in milliseconds (for `setTimeout` sequences).
 */

export const TIMING = {
  /** CSS transition durations (seconds) */
  fast:     0.2,   // hover feedback, micro-interactions
  normal:   0.4,   // standard transition
  slow:     0.8,   // entrance animations
  verySlow: 1.2,   // major page transitions

  /** setTimeout delays for sequenced animations (ms) */
  phaseDelays: {
    immediate: 0,
    short:    100,   // perceived as simultaneous
    medium:   600,   // previous animation settles
    long:    1200,   // clear visual separation
    veryLong: 2000,  // definite pause
  },
} as const;

/**
 * Named easing curves for CSS transitions.
 * Use with template literals: `transition: all ${TIMING.normal}s ${EASING.smooth}`
 */
export const EASING = {
  linear:    'linear',
  easeIn:    'cubic-bezier(0.4, 0, 1, 1)',
  easeOut:   'cubic-bezier(0, 0, 0.2, 1)',
  easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
  bounce:    'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  smooth:    'cubic-bezier(0.7, 0, 0.3, 1)',
} as const;

export type EasingKey = keyof typeof EASING;

/**
 * Generate an array of cumulative phase durations for sequenced animations.
 * Used by ThematicIntro and other multi-phase animation components.
 *
 * @param baseDelay - middle phase delay (default: medium = 600ms)
 * @returns Array of 5 phase start times in ms
 */
export function getPhaseDurations(
  baseDelay: number = TIMING.phaseDelays.medium,
): number[] {
  return [
    TIMING.phaseDelays.immediate,
    TIMING.phaseDelays.short,
    baseDelay,
    baseDelay + TIMING.phaseDelays.long,
    baseDelay + TIMING.phaseDelays.veryLong,
  ];
}
