import React, { useState, useEffect, useRef } from "react";
import type { Theme } from "../../tokens/themes.ts";
import type { StyleMode } from "../../tokens/style-modes.ts";
import type { LayoutFeatures } from "../../layouts/registry.ts";
import { DEFAULT_FEATURES } from "../../layouts/registry.ts";

const STYLE_SIGNATURES: Record<string, { borderRadius: string; borderWidth: string; label: string; symbol: string }> = {
  default:   { borderRadius: "10px", borderWidth: "1px", label: "Default",   symbol: "◎" },
  brutalist: { borderRadius: "0px",  borderWidth: "3px", label: "Brutalist", symbol: "■" },
  editorial: { borderRadius: "4px",  borderWidth: "1px", label: "Editorial", symbol: "—" },
  pop:       { borderRadius: "14px", borderWidth: "2px", label: "Pop Art",   symbol: "◉" },
};

const RENDER_FAMILIES: [string, string][] = [
  ["native", "Native"],
  ["base", "Base"],
  ["verge", "Verge"],
  ["handbook", "Handbook"],
  ["advocacy", "Advocacy"],
  ["advocacy-dense", "Dense"],
];

interface DeckMeta {
  title: string;
  titleAccent?: string;
}

interface AnimOptions {
  intro: boolean;
  comet: boolean;
  [key: string]: boolean;
}

interface TogglePillProps {
  on: boolean;
  accentColor: string;
}

function TogglePill({ on, accentColor }: TogglePillProps) {
  return (
    <div style={{
      width: 28, height: 16, borderRadius: 8, flexShrink: 0,
      background: on ? accentColor : "rgba(255,255,255,0.15)",
      position: "relative", transition: "background 0.2s",
    }}>
      <div style={{
        position: "absolute", top: 2, width: 12, height: 12,
        borderRadius: "50%", background: "white",
        left: on ? 14 : 2, transition: "left 0.2s ease",
      }} />
    </div>
  );
}

interface SectionLabelProps {
  label: string;
  extra?: React.ReactNode;
}

function SectionLabel({ label, extra }: SectionLabelProps) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
      <span style={{
        fontSize: 9, letterSpacing: 2, textTransform: "uppercase",
        color: "rgba(255,255,255,0.3)", fontFamily: "'Space Grotesk',sans-serif",
      }}>{label}</span>
      {extra}
    </div>
  );
}

interface PanelSectionProps {
  label: string;
  extra?: React.ReactNode;
  children: React.ReactNode;
}

function PanelSection({ label, extra, children }: PanelSectionProps) {
  return (
    <div style={{ marginBottom: 18 }}>
      <SectionLabel label={label} extra={extra} />
      {children}
    </div>
  );
}

export interface ControlPanelProps {
  decks: Record<string, DeckMeta>;
  deckKey: string;
  onDeckChange: (key: string) => void;
  themes: Theme[];
  theme: Theme | null;
  onThemeChange: (theme: Theme) => void;
  onThemeReset: () => void;
  themeManual: boolean;
  deckThemeId: string;
  styleModes: StyleMode[];
  styleModeId: string;
  onStyleModeChange: (id: string) => void;
  renderFamily: string;
  onRenderFamilyChange: (family: string) => void;
  /** Feature manifest for the active layout — drives conditional sections. */
  layoutFeatures?: LayoutFeatures;
  animOptions?: AnimOptions | null;
  onAnimOptionsChange?: ((opts: AnimOptions) => void) | null;
  heroImage?: string | null;
  heroImageEnabled?: boolean;
  onHeroImageToggle?: ((enabled: boolean) => void) | null;
  onHeroImageChange?: ((url: string) => void) | null;
  /** Content swapping — only shown for migrated decks */
  contentSwappable?: boolean;
  availableContent?: readonly { id: string; label: string; matchCount: number; totalSlides: number }[];
  contentKey?: string | null;
  onContentChange?: ((key: string) => void) | null;
}

export function ControlPanel({
  decks, deckKey, onDeckChange,
  themes, theme, onThemeChange, onThemeReset, themeManual, deckThemeId,
  styleModes, styleModeId, onStyleModeChange,
  renderFamily, onRenderFamilyChange, layoutFeatures,
  animOptions, onAnimOptionsChange,
  heroImage, heroImageEnabled, onHeroImageToggle, onHeroImageChange,
  contentSwappable, availableContent, contentKey, onContentChange,
}: ControlPanelProps) {
  const features = layoutFeatures ?? DEFAULT_FEATURES;
  const [open, setOpen] = useState(false);
  const wrapperRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    if (!open) return;
    function handleMouseDown(e: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleMouseDown);
    return () => document.removeEventListener("mousedown", handleMouseDown);
  }, [open]);

  // Close on ESC
  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.key === "Escape") setOpen(false);
    }
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, []);

  const contentIsSwapped = contentSwappable && contentKey && availableContent?.some((p) => p.id === contentKey && p.matchCount < p.totalSlides);
  const hasCustomSettings = themeManual || styleModeId !== "default" || renderFamily !== "native" || (animOptions && (animOptions.intro || animOptions.comet)) || heroImageEnabled === false || !!contentIsSwapped;
  const accentColor = theme?.accent ?? "#22D3EE";

  return (
    <div
      ref={wrapperRef}
      style={{
        position: "fixed", right: 0, top: "50%", transform: "translateY(-50%)",
        zIndex: 1000, display: "flex", flexDirection: "row", alignItems: "stretch",
        pointerEvents: "auto",
      }}
    >
      {/* Toggle tab — always visible */}
      <button
        onClick={() => setOpen((o) => !o)}
        aria-label={open ? "Close design panel" : "Open design panel"}
        style={{
          width: 32,
          background: open ? `${accentColor}18` : "rgba(8,10,20,0.7)",
          border: `1px solid ${open ? `${accentColor}50` : "rgba(255,255,255,0.1)"}`,
          borderRight: "none",
          borderRadius: "8px 0 0 8px",
          cursor: "pointer",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 10,
          padding: "14px 0",
          backdropFilter: "blur(10px)",
          transition: "background 0.2s ease, border-color 0.2s ease",
        }}
      >
        <div style={{
          width: 6, height: 6, borderRadius: "50%",
          background: hasCustomSettings ? accentColor : "rgba(255,255,255,0.25)",
          transition: "background 0.3s ease",
          flexShrink: 0,
        }} />
        <span style={{
          fontSize: 9, letterSpacing: 2.5, textTransform: "uppercase",
          color: open ? accentColor : "rgba(255,255,255,0.4)",
          fontFamily: "'Space Grotesk',sans-serif",
          writingMode: "vertical-rl",
          transform: "rotate(180deg)",
          transition: "color 0.2s ease",
          userSelect: "none",
        }}>Design</span>
      </button>

      {/* Sliding panel content */}
      <div style={{
        width: open ? 300 : 0,
        overflow: "hidden",
        transition: "width 0.3s cubic-bezier(0.22,1,0.36,1)",
        background: "rgba(8,10,24,0.94)",
        backdropFilter: "blur(20px)",
        borderLeft: "1px solid rgba(255,255,255,0.07)",
        borderTop: "1px solid rgba(255,255,255,0.07)",
        borderBottom: "1px solid rgba(255,255,255,0.07)",
        borderRadius: "0 0 0 8px",
      }}>
        <div style={{ width: 300, padding: "18px 14px", overflowY: "auto", maxHeight: "80vh" }}>

          {/* ── DECK ── */}
          <PanelSection label="Deck">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 5 }}>
              {Object.entries(decks).map(([key, d]) => {
                const isActive = key === deckKey;
                return (
                  <button
                    key={key}
                    onClick={() => { onDeckChange(key); setOpen(false); }}
                    style={{
                      background: isActive ? `${accentColor}18` : "rgba(255,255,255,0.04)",
                      border: `1px solid ${isActive ? `${accentColor}55` : "rgba(255,255,255,0.08)"}`,
                      borderRadius: 7,
                      padding: "7px 4px",
                      cursor: "pointer",
                      textAlign: "center",
                      transition: "background 0.15s ease, border-color 0.15s ease",
                    }}
                  >
                    <div style={{
                      fontSize: 9, color: isActive ? accentColor : "rgba(255,255,255,0.55)",
                      letterSpacing: 0.3, fontFamily: "'Space Grotesk',sans-serif",
                      lineHeight: 1.3, fontWeight: isActive ? 600 : 400,
                    }}>{d.title}</div>
                    <div style={{ fontSize: 8, color: "rgba(255,255,255,0.25)", marginTop: 2, lineHeight: 1.2 }}>{d.titleAccent}</div>
                  </button>
                );
              })}
            </div>
          </PanelSection>

          {/* ── CONTENT (only for migrated decks) ── */}
          {contentSwappable && availableContent && availableContent.length > 1 && onContentChange && (
            <PanelSection label="Content">
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                {availableContent.map((pack) => {
                  const isActive = pack.id === contentKey;
                  const isPartial = pack.matchCount < pack.totalSlides;
                  return (
                    <button
                      key={pack.id}
                      onClick={() => onContentChange(pack.id)}
                      style={{
                        background: isActive ? `${accentColor}12` : "rgba(255,255,255,0.02)",
                        border: `1px solid ${isActive ? `${accentColor}45` : "rgba(255,255,255,0.07)"}`,
                        borderRadius: 8,
                        padding: "7px 10px",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: 9,
                        textAlign: "left",
                        transition: "background 0.15s ease",
                      }}
                    >
                      <div style={{
                        width: 8, height: 8, borderRadius: "50%",
                        background: isActive ? accentColor : "rgba(255,255,255,0.2)",
                        flexShrink: 0,
                        boxShadow: isActive ? `0 0 6px ${accentColor}80` : "none",
                      }} />
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{
                          fontSize: 11, fontFamily: "'Space Grotesk',sans-serif",
                          color: isActive ? accentColor : "rgba(255,255,255,0.65)",
                          fontWeight: isActive ? 600 : 400,
                          lineHeight: 1,
                        }}>{pack.label}</div>
                        <div style={{ fontSize: 9, color: "rgba(255,255,255,0.28)", marginTop: 2 }}>
                          {isPartial
                            ? `${pack.matchCount}/${pack.totalSlides} slides matched`
                            : `${pack.totalSlides} slides`}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </PanelSection>
          )}

          {/* ── THEME ── */}
          <PanelSection
            label="Theme"
            extra={themeManual && (
              <button
                onClick={onThemeReset}
                title="Reset to deck default theme"
                style={{
                  background: "transparent", border: "none", fontSize: 10,
                  color: "rgba(255,255,255,0.4)", cursor: "pointer", padding: "0 2px",
                  fontFamily: "'Space Grotesk',sans-serif",
                }}
              >↺ Reset</button>
            )}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
              {themes.map((t) => {
                const isActive = theme?.id === t.id;
                const isDeckDefault = t.id === deckThemeId;
                return (
                  <button
                    key={t.id}
                    onClick={() => onThemeChange(t)}
                    style={{
                      background: isActive ? `${t.accent}12` : "rgba(255,255,255,0.02)",
                      border: `1px solid ${isActive ? `${t.accent}45` : "rgba(255,255,255,0.07)"}`,
                      borderRadius: 8,
                      padding: "7px 10px",
                      cursor: "pointer",
                      display: "flex",
                      alignItems: "center",
                      gap: 9,
                      textAlign: "left",
                      transition: "background 0.15s ease",
                    }}
                  >
                    <div style={{
                      width: 8, height: 8, borderRadius: "50%",
                      background: t.accent, flexShrink: 0,
                      boxShadow: isActive ? `0 0 6px ${t.accent}80` : "none",
                    }} />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{
                        fontSize: 11, fontFamily: "'Space Grotesk',sans-serif",
                        color: isActive ? t.accent : "rgba(255,255,255,0.65)",
                        fontWeight: isActive ? 600 : 400,
                        lineHeight: 1,
                      }}>{t.name}</div>
                      <div style={{ fontSize: 9, color: "rgba(255,255,255,0.28)", marginTop: 2 }}>{t.vibe}</div>
                    </div>
                    {isDeckDefault && !themeManual && (
                      <div style={{ fontSize: 8, color: "rgba(255,255,255,0.25)", flexShrink: 0 }}>deck</div>
                    )}
                  </button>
                );
              })}
            </div>
          </PanelSection>

          {/* ── STYLE ── */}
          <PanelSection label="Style">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
              {styleModes.map((m) => {
                const sig = STYLE_SIGNATURES[m.id] ?? STYLE_SIGNATURES["default"];
                const isActive = m.id === styleModeId;
                return (
                  <button
                    key={m.id}
                    onClick={() => onStyleModeChange(m.id)}
                    style={{
                      background: isActive ? `${accentColor}12` : "rgba(255,255,255,0.03)",
                      border: `${sig.borderWidth} solid ${isActive ? `${accentColor}60` : "rgba(255,255,255,0.12)"}`,
                      borderRadius: sig.borderRadius,
                      padding: "9px 10px",
                      cursor: "pointer",
                      textAlign: "left",
                      transition: "background 0.15s ease",
                    }}
                  >
                    <div style={{ fontSize: 16, marginBottom: 4, color: isActive ? accentColor : "rgba(255,255,255,0.5)" }}>{sig.symbol}</div>
                    <div style={{
                      fontSize: 10, fontFamily: "'Space Grotesk',sans-serif", letterSpacing: 0.4,
                      color: isActive ? accentColor : "rgba(255,255,255,0.6)", fontWeight: isActive ? 600 : 400,
                    }}>{sig.label}</div>
                    <div style={{ fontSize: 9, color: "rgba(255,255,255,0.28)", marginTop: 2 }}>{m.vibe}</div>
                  </button>
                );
              })}
            </div>
          </PanelSection>

          {/* ── RENDER AS (conditional on layout feature) ── */}
          {features.renderAs && (
            <PanelSection label="Render As">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 5 }}>
                {RENDER_FAMILIES.map(([fam, label]) => {
                  const isActive = fam === renderFamily;
                  return (
                    <button
                      key={fam}
                      onClick={() => onRenderFamilyChange(fam)}
                      style={{
                        background: isActive ? `${accentColor}15` : "rgba(255,255,255,0.03)",
                        border: `1px solid ${isActive ? `${accentColor}50` : "rgba(255,255,255,0.09)"}`,
                        borderRadius: 7,
                        padding: "7px 10px",
                        cursor: "pointer",
                        fontSize: 10,
                        color: isActive ? accentColor : "rgba(255,255,255,0.45)",
                        fontFamily: "'Space Grotesk',sans-serif",
                        letterSpacing: 0.5,
                        textTransform: "uppercase",
                        textAlign: "center",
                        fontWeight: isActive ? 600 : 400,
                        transition: "background 0.15s ease",
                      }}
                    >{label}</button>
                  );
                })}
              </div>
            </PanelSection>
          )}

          {/* ── EFFECTS (conditional on layout feature) ── */}
          {features.effects && animOptions && onAnimOptionsChange && (
            <PanelSection label="Effects">
              {[
                { key: "intro", label: "Intro Sequence", sub: "Cinematic deck opener" },
                { key: "comet", label: "Comet Transitions", sub: "Animated navigation" },
              ].map(({ key, label, sub }) => {
                const on = animOptions[key];
                return (
                  <button
                    key={key}
                    onClick={() => onAnimOptionsChange({ ...animOptions, [key]: !on })}
                    style={{
                      display: "flex", alignItems: "center", gap: 10, width: "100%",
                      marginBottom: 5, textAlign: "left", cursor: "pointer",
                      background: on ? `${accentColor}12` : "rgba(255,255,255,0.02)",
                      border: `1px solid ${on ? `${accentColor}40` : "rgba(255,255,255,0.07)"}`,
                      borderRadius: 8, padding: "7px 10px",
                      transition: "background 0.15s ease",
                    }}
                  >
                    <TogglePill on={on} accentColor={accentColor} />
                    <div>
                      <div style={{
                        fontSize: 11, fontFamily: "'Space Grotesk',sans-serif",
                        color: on ? accentColor : "rgba(255,255,255,0.6)",
                        fontWeight: on ? 600 : 400,
                      }}>{label}</div>
                      <div style={{ fontSize: 9, color: "rgba(255,255,255,0.28)", marginTop: 1 }}>{sub}</div>
                    </div>
                  </button>
                );
              })}
            </PanelSection>
          )}

          {/* ── BACKGROUND (conditional on layout feature) ── */}
          {features.background && onHeroImageToggle && (
            <PanelSection label="Background">
              <button
                onClick={() => onHeroImageToggle(!heroImageEnabled)}
                style={{
                  display: "flex", alignItems: "center", gap: 10, width: "100%",
                  marginBottom: 8, textAlign: "left", cursor: "pointer",
                  background: heroImageEnabled ? `${accentColor}12` : "rgba(255,255,255,0.02)",
                  border: `1px solid ${heroImageEnabled ? `${accentColor}40` : "rgba(255,255,255,0.07)"}`,
                  borderRadius: 8, padding: "7px 10px",
                  transition: "background 0.15s ease",
                }}
              >
                <TogglePill on={!!heroImageEnabled} accentColor={accentColor} />
                <div>
                  <div style={{
                    fontSize: 11, fontFamily: "'Space Grotesk',sans-serif",
                    color: heroImageEnabled ? accentColor : "rgba(255,255,255,0.6)",
                    fontWeight: heroImageEnabled ? 600 : 400,
                  }}>Hero Image</div>
                  <div style={{ fontSize: 9, color: "rgba(255,255,255,0.28)", marginTop: 1 }}>Landing background</div>
                </div>
              </button>
              {heroImageEnabled && onHeroImageChange && (
                <input
                  value={heroImage || ""}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => onHeroImageChange(e.target.value)}
                  placeholder="URL or relative path"
                  style={{
                    width: "100%", marginTop: 2, boxSizing: "border-box",
                    background: "rgba(255,255,255,0.05)",
                    border: "1px solid rgba(255,255,255,0.1)", borderRadius: 6,
                    padding: "5px 8px", fontSize: 10, color: "rgba(255,255,255,0.5)",
                    fontFamily: "monospace",
                  }}
                />
              )}
            </PanelSection>
          )}

        </div>
      </div>
    </div>
  );
}
