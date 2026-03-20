/**
 * Theme interface -- the visual identity of a deck.
 *
 * Color roles follow the 60-30-10 rule:
 *   bg (60%)      -- slide background, dominant visual area
 *   surface (30%) -- cards, panels, content containers
 *   accent (10%)  -- highlights, CTAs, emphasis elements
 *
 * pptxgenjs mapping:
 *   bg        -> slide background color
 *   surface   -> shape fill for card rectangles
 *   accent    -> accent bars, stat numbers, icon fills
 *   text      -> title + body text color
 *   textMuted -> subtitle, caption, secondary text
 */
export interface Theme {
  readonly id: ThemeId;
  readonly name: string;
  readonly vibe: string;
  // Typography
  readonly fontDisplay: string;   // Headings, titles (pptxgenjs fontFace)
  readonly fontBody: string;      // Body text, bullets (pptxgenjs fontFace)
  readonly fontsUrl: string;      // Google Fonts URL for web preview
  // 60-30-10 color system
  readonly bg: string;            // 60% -- slide background
  readonly surface: string;       // 30% -- card/panel fills
  readonly surfaceDeep: string;   // Recessed/sunken surfaces
  readonly accent: string;        // 10% -- emphasis, CTAs
  readonly accentGlow: string;    // Soft glow for web preview effects
  readonly gradient: readonly [string, string];
  // Text hierarchy
  readonly text: string;          // Primary text
  readonly textMuted: string;     // Secondary/supporting text
  readonly textDim: string;       // Tertiary/decorative text
  // Semantic colors
  readonly success: string;
  readonly danger: string;
  readonly warning: string;
}

export type ThemeId =
  | "midnight-teal"
  | "neon-noir"
  | "linear"
  | "paper-ink"
  | "signal-cobalt"
  | "studio-craft"
  | "electric-cyan"
  | "hot-neon"
  | "sunset-fire"
  | "glass-dark";

// ---------------------------------------------------------------------------
// Theme definitions
// ---------------------------------------------------------------------------

const midnightTeal: Theme = {
  id: "midnight-teal",
  name: "Midnight Teal",
  vibe: "Professional tech",
  fontDisplay: "Space Grotesk",
  fontBody: "DM Sans",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap",
  bg: "#0B1426",
  surface: "#162240",
  surfaceDeep: "#111827",
  accent: "#22D3EE",
  accentGlow: "rgba(8,145,178,0.3)",
  gradient: ["#22D3EE", "#10B981"] as const,
  text: "#F0F4F8",
  textMuted: "#CBD5E1",
  textDim: "#64748B",
  success: "#10B981",
  danger: "#EF4444",
  warning: "#F59E0B",
} as const;

const neonNoir: Theme = {
  id: "neon-noir",
  name: "Neon Noir",
  vibe: "Cyberpunk bold",
  fontDisplay: "Chakra Petch",
  fontBody: "Barlow",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap",
  bg: "#050508",
  surface: "#0D0D12",
  surfaceDeep: "#14141C",
  accent: "#00E5FF",
  accentGlow: "rgba(0,229,255,0.2)",
  gradient: ["#00E5FF", "#FF2D95"] as const,
  text: "#EAEAF0",
  textMuted: "#8585A0",
  textDim: "#55556E",
  success: "#AAFF00",
  danger: "#FF2D95",
  warning: "#FFD600",
} as const;

const linear: Theme = {
  id: "linear",
  name: "Linear",
  vibe: "Clean product",
  fontDisplay: "Inter",
  fontBody: "Inter",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
  bg: "#0F1117",
  surface: "#161B27",
  surfaceDeep: "#0C0E18",
  accent: "#5E6AD2",
  accentGlow: "rgba(94,106,210,0.22)",
  gradient: ["#5E6AD2", "#8B7CE8"] as const,
  text: "#E2E4F0",
  textMuted: "#8F93A9",
  textDim: "#545870",
  success: "#4CC38A",
  danger: "#E5484D",
  warning: "#FFB224",
} as const;

const paperInk: Theme = {
  id: "paper-ink",
  name: "Paper & Ink",
  vibe: "Classic editorial",
  fontDisplay: "DM Serif Display",
  fontBody: "Atkinson Hyperlegible",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
  bg: "#FAF8F5",
  surface: "#FFFFFF",
  surfaceDeep: "#F0EDE8",
  accent: "#1E40AF",
  accentGlow: "rgba(30,64,175,0.12)",
  gradient: ["#1E40AF", "#7C3AED"] as const,
  text: "#1A1A2E",
  textMuted: "#5C5C6F",
  textDim: "#8E8E9F",
  success: "#047857",
  danger: "#DC2626",
  warning: "#B45309",
} as const;

const signalCobalt: Theme = {
  id: "signal-cobalt",
  name: "Signal Cobalt",
  vibe: "Corporate systems",
  fontDisplay: "Sora",
  fontBody: "Libre Franklin",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Libre+Franklin:wght@400;500;600;700&display=swap",
  bg: "#F7F6F1",
  surface: "#FFFFFF",
  surfaceDeep: "#ECE9E1",
  accent: "#1328FF",
  accentGlow: "rgba(19,40,255,0.16)",
  gradient: ["#1328FF", "#FF6A13"] as const,
  text: "#121212",
  textMuted: "#404040",
  textDim: "#818181",
  success: "#1F8A53",
  danger: "#E94F1D",
  warning: "#FFB000",
} as const;

const studioCraft: Theme = {
  id: "studio-craft",
  name: "Studio Craft",
  vibe: "Warm handbook",
  fontDisplay: "Syne",
  fontBody: "IBM Plex Sans",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap",
  bg: "#F8F6F0",
  surface: "#FFFFFF",
  surfaceDeep: "#EDEAE0",
  accent: "#F4E04D",
  accentGlow: "rgba(244,224,77,0.35)",
  gradient: ["#F4E04D", "#F2A614"] as const,
  text: "#0E0E0B",
  textMuted: "#4B4843",
  textDim: "#8C8885",
  success: "#2E6E3E",
  danger: "#C53B2F",
  warning: "#F2A614",
} as const;

const electricCyan: Theme = {
  id: "electric-cyan",
  name: "Electric Cyan",
  vibe: "Bold data journalism",
  fontDisplay: "Outfit",
  fontBody: "Outfit",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap",
  bg: "#00C8E0",
  surface: "#FFFFFF",
  surfaceDeep: "#00B0C8",
  accent: "#FFE600",
  accentGlow: "rgba(255,230,0,0.35)",
  gradient: ["#FFE600", "#FF6B00"] as const,
  text: "#000000",
  textMuted: "#1A3A40",
  textDim: "#3D6068",
  success: "#00C853",
  danger: "#FF1744",
  warning: "#FF6D00",
} as const;

const hotNeon: Theme = {
  id: "hot-neon",
  name: "Hot Neon",
  vibe: "Maximalist pop",
  fontDisplay: "Unbounded",
  fontBody: "Work Sans",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800&family=Work+Sans:wght@400;500;600&display=swap",
  bg: "#000000",
  surface: "#1A1A1A",
  surfaceDeep: "#0D0D0D",
  accent: "#FF1493",
  accentGlow: "rgba(255,20,147,0.3)",
  gradient: ["#FF1493", "#AAFF00"] as const,
  text: "#FFFFFF",
  textMuted: "#B0B0B0",
  textDim: "#666666",
  success: "#AAFF00",
  danger: "#FF4444",
  warning: "#FFE600",
} as const;

const sunsetFire: Theme = {
  id: "sunset-fire",
  name: "Sunset Fire",
  vibe: "Warm maximalist",
  fontDisplay: "Archivo Black",
  fontBody: "Source Sans 3",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Archivo+Black&family=Source+Sans+3:wght@400;500;600;700&display=swap",
  bg: "#FF6A13",
  surface: "#FFF0E0",
  surfaceDeep: "#E85D10",
  accent: "#FFE600",
  accentGlow: "rgba(255,230,0,0.4)",
  gradient: ["#FFE600", "#FF1493"] as const,
  text: "#000000",
  textMuted: "#3D1800",
  textDim: "#6B3A15",
  success: "#00C853",
  danger: "#D50000",
  warning: "#FFB300",
} as const;

const glassDark: Theme = {
  id: "glass-dark",
  name: "Glass Dark",
  vibe: "Premium SaaS",
  fontDisplay: "Plus Jakarta Sans",
  fontBody: "Plus Jakarta Sans",
  fontsUrl:
    "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
  bg: "#0C0F1A",
  surface: "#151929",
  surfaceDeep: "#0A0D15",
  accent: "#8B7CF6",
  accentGlow: "rgba(139,124,246,0.2)",
  gradient: ["#8B7CF6", "#6366F1"] as const,
  text: "#E8EAF6",
  textMuted: "#9CA3BF",
  textDim: "#5A6178",
  success: "#34D399",
  danger: "#F87171",
  warning: "#FBBF24",
} as const;

// ---------------------------------------------------------------------------
// Exports
// ---------------------------------------------------------------------------

/** All 10 curated themes. */
export const THEMES: readonly Theme[] = [
  midnightTeal,
  neonNoir,
  linear,
  paperInk,
  signalCobalt,
  studioCraft,
  electricCyan,
  hotNeon,
  sunsetFire,
  glassDark,
] as const;

/** Lookup a theme by its ID. */
export const THEMES_BY_ID: Record<ThemeId, Theme> = {
  "midnight-teal": midnightTeal,
  "neon-noir": neonNoir,
  "linear": linear,
  "paper-ink": paperInk,
  "signal-cobalt": signalCobalt,
  "studio-craft": studioCraft,
  "electric-cyan": electricCyan,
  "hot-neon": hotNeon,
  "sunset-fire": sunsetFire,
  "glass-dark": glassDark,
} as const;

/** Google Fonts CSS URLs keyed by theme ID. */
export const THEME_FONT_URLS: Record<ThemeId, string> = {
  "midnight-teal":
    "https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,700&family=Space+Grotesk:wght@500;700&display=swap",
  "neon-noir":
    "https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap",
  "linear":
    "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
  "paper-ink":
    "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Atkinson+Hyperlegible:wght@400;700&display=swap",
  "signal-cobalt":
    "https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Libre+Franklin:wght@400;500;600;700&display=swap",
  "studio-craft":
    "https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap",
  "electric-cyan":
    "https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap",
  "hot-neon":
    "https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800&family=Work+Sans:wght@400;500;600&display=swap",
  "sunset-fire":
    "https://fonts.googleapis.com/css2?family=Archivo+Black&family=Source+Sans+3:wght@400;500;600;700&display=swap",
  "glass-dark":
    "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap",
} as const;
