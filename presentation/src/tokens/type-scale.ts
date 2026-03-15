// ─── TYPE SCALE ───
// Source of truth extracted from genai_advocacy_hub_10.jsx.
// All font-size values are in px; use directly in React inline styles.

export interface TypeScaleEntry {
  readonly fontSize: number;
  readonly fontWeight: number;
  readonly letterSpacing: number;
  readonly lineHeight: number;
  readonly textTransform?: "uppercase" | "lowercase" | "capitalize" | "none";
}

export type TypeScaleKey = "STAT" | "HERO" | "TITLE" | "SECTION" | "CARD" | "BODY" | "CAPTION" | "EYEBROW";

export const TYPE_SCALE: Record<TypeScaleKey, TypeScaleEntry> = {
  STAT:    { fontSize: 48, fontWeight: 800, letterSpacing: -1.5, lineHeight: 1 },
  HERO:    { fontSize: 44, fontWeight: 800, letterSpacing: -1,   lineHeight: 0.96 },
  TITLE:   { fontSize: 32, fontWeight: 700, letterSpacing: -0.5, lineHeight: 1.05 },
  SECTION: { fontSize: 24, fontWeight: 700, letterSpacing: 0,    lineHeight: 1.12 },
  CARD:    { fontSize: 18, fontWeight: 600, letterSpacing: 0,    lineHeight: 1.2  },
  BODY:    { fontSize: 16, fontWeight: 400, letterSpacing: 0,    lineHeight: 1.6  },
  CAPTION: { fontSize: 13, fontWeight: 500, letterSpacing: 0.5,  lineHeight: 1.4  },
  EYEBROW: { fontSize: 11, fontWeight: 700, letterSpacing: 2.5,  lineHeight: 1, textTransform: "uppercase" },
};
