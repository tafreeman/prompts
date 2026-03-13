// ─── THEMES ───
// Source of truth for all theme tokens, extracted from genai_advocacy_hub_10.jsx.
// v10 extended set includes success/danger/warning/surfaceElevated tokens missing from v13.

export const THEMES = [
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
];

// Per-theme Google Fonts URLs — used by FontLoader and build-single-file.mjs
export const THEME_FONT_URLS = {
  "midnight-teal":    "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap",
  "obsidian-ember":   "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap",
  "arctic-steel":     "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700;800&family=Nunito+Sans:wght@400;500;600;700&display=swap",
  "midnight-verdant": "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Karla:wght@400;500;600;700&display=swap",
  "neon-noir":        "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap",
  "paper-ink":        "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
};

// Combined URL for the theme-switcher preview panel (all display fonts in one request)
export const THEME_SELECTOR_FONTS_URL =
  "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&family=Playfair+Display:wght@700&family=JetBrains+Mono:wght@700&family=Outfit:wght@700&family=Chakra+Petch:wght@700&family=DM+Serif+Display&display=swap";

export default THEMES;
