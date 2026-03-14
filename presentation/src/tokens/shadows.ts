/**
 * Elevation shadow tokens — consistent box-shadow scale.
 * Use for card depth, modals, dropdowns, and floating elements.
 */

export const SHADOWS = {
  none: 'none',
  sm:   '0 1px 2px rgba(0,0,0,0.08)',
  md:   '0 4px 12px rgba(0,0,0,0.12)',
  lg:   '0 8px 24px rgba(0,0,0,0.16)',
  xl:   '0 16px 48px rgba(0,0,0,0.24)',
} as const;

export type ShadowKey = keyof typeof SHADOWS;
