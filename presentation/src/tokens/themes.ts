// ─── THEMES ───
// Shared theme token source for all presentation variants and reference decks.
// Includes the original set plus image-derived themes extracted from deck.gallery references.

// ── Theme interface ──────────────────────────────────────────────────────────

export interface Theme {
  readonly id: string;
  readonly name: string;
  readonly vibe: string;
  readonly fontDisplay: string;
  readonly fontBody: string;
  readonly bg: string;
  readonly bgCard: string;
  readonly bgDeep: string;
  readonly text: string;
  readonly textMuted: string;
  readonly textDim: string;
  readonly accent: string;
  readonly accentGlow: string;
  readonly gradient: readonly [string, string];
  readonly success: string;
  readonly danger: string;
  readonly warning: string;
  readonly surfaceElevated: string;
  readonly fontsUrl?: string;
}

export type ThemeId =
  | "midnight-teal" | "obsidian-ember" | "arctic-steel" | "midnight-verdant"
  | "neon-noir" | "paper-ink" | "atelier-sage" | "signal-cobalt"
  | "verge-orange" | "verge-blue" | "verge-pink" | "verge-yellow"
  | "gamma-dark" | "studio-craft" | "linear";

// Per-theme Google Fonts URLs — used by runtime loaders and export scripts.
export const THEME_FONT_URLS: Record<ThemeId, string> = {
  "midnight-teal":    "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap",
  "obsidian-ember":   "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap",
  "arctic-steel":     "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap",
  "midnight-verdant": "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Karla:wght@400;500;600;700&display=swap",
  "neon-noir":        "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap",
  "paper-ink":        "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
  "atelier-sage":     "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap",
  "signal-cobalt":    "https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Libre+Franklin:wght@400;500;600;700&display=swap",
  "verge-orange":     "https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Work+Sans:wght@400;500;600;700;800;900&display=swap",
  "verge-blue":       "https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Work+Sans:wght@400;500;600;700;800;900&display=swap",
  "verge-pink":       "https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Work+Sans:wght@400;500;600;700;800;900&display=swap",
  "verge-yellow":     "https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Work+Sans:wght@400;500;600;700;800;900&display=swap",
  "gamma-dark":       "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;600;700&display=swap",
  "studio-craft":     "https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap",
  "linear":           "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
};

// Combined URL for the theme-switcher preview panel (display fonts only).
export const THEME_SELECTOR_FONTS_URL =
  "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Playfair+Display:wght@700&family=JetBrains+Mono:wght@700&family=Outfit:wght@700&family=Chakra+Petch:wght@700&family=DM+Serif+Display&family=Cormorant+Garamond:wght@600;700&family=Sora:wght@600;700;800&family=Space+Mono:wght@700&family=Syne:wght@700;800&family=Inter:wght@600;700&display=swap";

const BASE_THEMES: readonly Omit<Theme, "fontsUrl">[] = [
  {
    id: "midnight-teal", name: "Midnight Teal", vibe: "Current Default",
    fontDisplay: "'Space Grotesk',sans-serif", fontBody: "'DM Sans',sans-serif",
    bg: "#0B1426", bgCard: "#162240", bgDeep: "#111827",
    text: "#F0F4F8", textMuted: "#CBD5E1", textDim: "#64748B",
    accent: "#22D3EE", accentGlow: "rgba(8,145,178,0.3)", gradient: ["#22D3EE", "#10B981"],
    success: "#10B981", danger: "#EF4444", warning: "#F59E0B", surfaceElevated: "#0A1628",
  },
  {
    id: "obsidian-ember", name: "Obsidian & Ember", vibe: "Editorial / Luxury",
    fontDisplay: "'Playfair Display',serif", fontBody: "'Source Sans 3',sans-serif",
    bg: "#1A1A1E", bgCard: "#242428", bgDeep: "#2C2C32",
    text: "#E8E4DF", textMuted: "#9B9590", textDim: "#6B6560",
    accent: "#D4A853", accentGlow: "rgba(212,168,83,0.25)", gradient: ["#D4A853", "#C75B39"],
    success: "#5B8A72", danger: "#C75B39", warning: "#D4A853", surfaceElevated: "#141416",
  },
  {
    id: "arctic-steel", name: "Arctic Steel", vibe: "Industrial Nordic",
    fontDisplay: "'JetBrains Mono',monospace", fontBody: "'Nunito Sans',sans-serif",
    bg: "#0F1318", bgCard: "#171D24", bgDeep: "#1E2630",
    text: "#D6DDE6", textMuted: "#7B8EA3", textDim: "#4E6178",
    accent: "#4FC3F7", accentGlow: "rgba(79,195,247,0.2)", gradient: ["#4FC3F7", "#B2EBF2"],
    success: "#69F0AE", danger: "#FF6B6B", warning: "#FFD54F", surfaceElevated: "#0B1018",
  },
  {
    id: "midnight-verdant", name: "Midnight Verdant", vibe: "Organic Tech",
    fontDisplay: "'Outfit',sans-serif", fontBody: "'Karla',sans-serif",
    bg: "#0A1628", bgCard: "#112240", bgDeep: "#152A4E",
    text: "#CCD6F6", textMuted: "#8892B0", textDim: "#5A6480",
    accent: "#64FFDA", accentGlow: "rgba(100,255,218,0.18)", gradient: ["#64FFDA", "#48BB78"],
    success: "#64FFDA", danger: "#F78166", warning: "#F1FA8C", surfaceElevated: "#071420",
  },
  {
    id: "neon-noir", name: "Neon Noir", vibe: "Cyberpunk / Bold",
    fontDisplay: "'Chakra Petch',sans-serif", fontBody: "'Barlow',sans-serif",
    bg: "#050508", bgCard: "#0D0D12", bgDeep: "#14141C",
    text: "#EAEAF0", textMuted: "#8585A0", textDim: "#55556E",
    accent: "#00E5FF", accentGlow: "rgba(0,229,255,0.2)", gradient: ["#00E5FF", "#FF2D95"],
    success: "#AAFF00", danger: "#FF2D95", warning: "#FFD600", surfaceElevated: "#030305",
  },
  {
    id: "paper-ink", name: "Paper & Ink", vibe: "Light Editorial",
    fontDisplay: "'DM Serif Display',serif", fontBody: "'Atkinson Hyperlegible',sans-serif",
    bg: "#FAF8F5", bgCard: "#FFFFFF", bgDeep: "#F0EDE8",
    text: "#1A1A2E", textMuted: "#5C5C6F", textDim: "#8E8E9F",
    accent: "#1E40AF", accentGlow: "rgba(30,64,175,0.12)", gradient: ["#1E40AF", "#7C3AED"],
    success: "#047857", danger: "#DC2626", warning: "#B45309", surfaceElevated: "#E8E5E0",
  },
  {
    id: "atelier-sage", name: "Atelier Sage", vibe: "Airy Editorial / Process",
    fontDisplay: "'Cormorant Garamond',serif", fontBody: "'Source Sans 3',sans-serif",
    bg: "#F6F2EA", bgCard: "#FFFDF8", bgDeep: "#ECE5D8",
    text: "#23312C", textMuted: "#556A61", textDim: "#8B9388",
    accent: "#557868", accentGlow: "rgba(85,120,104,0.18)", gradient: ["#557868", "#D7AA58"],
    success: "#6E8D79", danger: "#C87052", warning: "#D7AA58", surfaceElevated: "#E8E0D1",
  },
  {
    id: "signal-cobalt", name: "Signal Cobalt", vibe: "Swiss / Brutalist Systems",
    fontDisplay: "'Sora',sans-serif", fontBody: "'Libre Franklin',sans-serif",
    bg: "#F7F6F1", bgCard: "#FFFFFF", bgDeep: "#ECE9E1",
    text: "#121212", textMuted: "#404040", textDim: "#818181",
    accent: "#1328FF", accentGlow: "rgba(19,40,255,0.16)", gradient: ["#1328FF", "#FF6A13"],
    success: "#1F8A53", danger: "#E94F1D", warning: "#FFB000", surfaceElevated: "#E6E2D8",
  },
  {
    id: "verge-orange", name: "Verge Orange", vibe: "Pop Art / Citrus",
    fontDisplay: "'Space Mono',monospace", fontBody: "'Work Sans',sans-serif",
    bg: "#FF6B00", bgCard: "#FFF3E0", bgDeep: "#E85D00",
    text: "#000000", textMuted: "#3D1F00", textDim: "#7A4000",
    accent: "#000000", accentGlow: "rgba(0,0,0,0.12)", gradient: ["#FF3366", "#00CC99"],
    success: "#00CC66", danger: "#FF3366", warning: "#FFD600", surfaceElevated: "#CC5500",
  },
  {
    id: "verge-blue", name: "Verge Blue", vibe: "Pop Art / Electric",
    fontDisplay: "'Space Mono',monospace", fontBody: "'Work Sans',sans-serif",
    bg: "#1A75FF", bgCard: "#E6F0FF", bgDeep: "#0052CC",
    text: "#FFFFFF", textMuted: "#CCE0FF", textDim: "#80B3FF",
    accent: "#FFD600", accentGlow: "rgba(255,214,0,0.2)", gradient: ["#FFD600", "#FF6633"],
    success: "#00CC66", danger: "#FF3366", warning: "#FFD600", surfaceElevated: "#0047B3",
  },
  {
    id: "verge-pink", name: "Verge Pink", vibe: "Pop Art / Magenta",
    fontDisplay: "'Space Mono',monospace", fontBody: "'Work Sans',sans-serif",
    bg: "#FF0099", bgCard: "#FFE6F5", bgDeep: "#CC007A",
    text: "#000000", textMuted: "#33001F", textDim: "#660040",
    accent: "#000000", accentGlow: "rgba(0,0,0,0.12)", gradient: ["#FFD600", "#00CC99"],
    success: "#00CC66", danger: "#FF3333", warning: "#FFD600", surfaceElevated: "#B30070",
  },
  {
    id: "verge-yellow", name: "Verge Yellow", vibe: "Pop Art / Sunshine",
    fontDisplay: "'Space Mono',monospace", fontBody: "'Work Sans',sans-serif",
    bg: "#FFD600", bgCard: "#FFFDE6", bgDeep: "#CCB000",
    text: "#000000", textMuted: "#332B00", textDim: "#665500",
    accent: "#FF3366", accentGlow: "rgba(255,51,102,0.15)", gradient: ["#FF3366", "#0066FF"],
    success: "#00CC66", danger: "#FF3366", warning: "#FF9900", surfaceElevated: "#B39700",
  },
  {
    id: "gamma-dark", name: "Gamma Dark", vibe: "Cinematic / Ember",
    fontDisplay: "'Space Grotesk',sans-serif", fontBody: "'DM Sans',sans-serif",
    bg: "#060608", bgCard: "#111113", bgDeep: "#0C0C0E",
    text: "#F5F0EB", textMuted: "#A8A099", textDim: "#6B6560",
    accent: "#F97316", accentGlow: "rgba(249,115,22,0.25)", gradient: ["#F97316", "#FBBF24"],
    success: "#22C55E", danger: "#EF4444", warning: "#FBBF24", surfaceElevated: "#050506",
  },
  {
    id: "studio-craft", name: "Studio Craft", vibe: "Agency Handbook / Editorial Yellow",
    fontDisplay: "'Syne',sans-serif", fontBody: "'IBM Plex Sans',sans-serif",
    bg: "#F8F6F0", bgCard: "#FFFFFF", bgDeep: "#EDEAE0",
    text: "#0E0E0B", textMuted: "#4B4843", textDim: "#8C8885",
    accent: "#F4E04D", accentGlow: "rgba(244,224,77,0.35)", gradient: ["#F4E04D", "#F2A614"],
    success: "#2E6E3E", danger: "#C53B2F", warning: "#F2A614", surfaceElevated: "#EAE6DC",
  },
  {
    id: "linear", name: "Linear", vibe: "Product / Clean Dark",
    fontDisplay: "'Inter',sans-serif", fontBody: "'Inter',sans-serif",
    bg: "#0F1117", bgCard: "#161B27", bgDeep: "#0C0E18",
    text: "#E2E4F0", textMuted: "#8F93A9", textDim: "#545870",
    accent: "#5E6AD2", accentGlow: "rgba(94,106,210,0.22)", gradient: ["#5E6AD2", "#8B7CE8"],
    success: "#4CC38A", danger: "#E5484D", warning: "#FFB224", surfaceElevated: "#080A12",
  },
];

export const THEMES: readonly Theme[] = BASE_THEMES.map((theme) => ({
  ...theme,
  fontsUrl: THEME_FONT_URLS[theme.id as ThemeId],
}));

export const THEMES_BY_ID: Record<string, Theme> = Object.fromEntries(
  THEMES.map((theme) => [theme.id, theme]),
);

export default THEMES;
