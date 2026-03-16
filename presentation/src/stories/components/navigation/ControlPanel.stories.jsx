import React, { useState } from "react";
import { ControlPanel } from "../../../components/navigation/ControlPanel.tsx";
import { THEMES, THEMES_BY_ID } from "../../../tokens/themes.ts";
import { STYLE_MODES, STYLE_MODES_BY_ID } from "../../../tokens/style-modes.ts";

export default {
  title: "Navigation/ControlPanel",
  component: ControlPanel,
  parameters: {
    layout: "fullscreen",
  },
};

// Minimal deck stubs matching the shape used in App.v14
const MOCK_DECKS = {
  current: {
    id: "current",
    themeId: "midnight-teal",
    title: "GenAI",
    titleAccent: "Advocacy Deck",
    topics: [],
  },
  onboarding: {
    id: "onboarding",
    themeId: "gamma-dark",
    title: "Onboarding",
    titleAccent: "Guidebook",
    topics: [],
  },
  studio: {
    id: "studio",
    themeId: "studio-craft",
    title: "Studio",
    titleAccent: "Handbook",
    topics: [],
  },
  engineering: {
    id: "engineering",
    themeId: "linear",
    title: "Engineering",
    titleAccent: "Deep Dive",
    topics: [],
  },
  "verge-pop": {
    id: "verge-pop",
    themeId: "verge-orange",
    title: "Verge",
    titleAccent: "Pop",
    topics: [],
  },
  "atelier-sage": {
    id: "atelier-sage",
    themeId: "atelier-sage",
    title: "Atelier",
    titleAccent: "Sage",
    topics: [],
  },
};

function ControlPanelHarness({
  initialDeckKey = "current",
  initialThemeId = "midnight-teal",
  initialStyleModeId = "default",
  initialRenderFamily = "native",
  showLayoutFamilies = true,
  showEffects = true,
  showBackground = true,
}) {
  const [deckKey, setDeckKey] = useState(initialDeckKey);
  const [theme, setTheme] = useState(THEMES_BY_ID[initialThemeId] || THEMES[0]);
  const [themeManual, setThemeManual] = useState(false);
  const [styleModeId, setStyleModeId] = useState(initialStyleModeId);
  const [renderFamily, setRenderFamily] = useState(initialRenderFamily);
  const [animOptions, setAnimOptions] = useState({ intro: false, comet: false });
  const [heroImage, setHeroImage] = useState("https://example.com/hero.png");
  const [heroImageEnabled, setHeroImageEnabled] = useState(true);

  const deckThemeId = MOCK_DECKS[deckKey]?.themeId || "midnight-teal";

  return (
    <div
      style={{
        background: theme.bg,
        minHeight: "100vh",
        fontFamily: theme.fontBody,
        color: theme.text,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <link href={theme.fontsUrl} rel="stylesheet" />
      <div style={{ fontSize: 14, color: theme.textDim, textAlign: "center" }}>
        <p style={{ fontFamily: theme.fontDisplay, fontSize: 20, color: theme.text, marginBottom: 8 }}>
          Control Panel Demo
        </p>
        <p>Click the "Design" tab on the right edge to open the panel.</p>
        <p style={{ fontSize: 12, marginTop: 12 }}>
          Deck: <strong style={{ color: theme.accent }}>{deckKey}</strong>{" "}
          | Theme: <strong style={{ color: theme.accent }}>{theme.name}</strong>{" "}
          | Style: <strong style={{ color: theme.accent }}>{styleModeId}</strong>{" "}
          | Family: <strong style={{ color: theme.accent }}>{renderFamily}</strong>
        </p>
      </div>
      <ControlPanel
        decks={MOCK_DECKS}
        deckKey={deckKey}
        onDeckChange={(key) => {
          setDeckKey(key);
          if (!themeManual) {
            const nextTheme = THEMES_BY_ID[MOCK_DECKS[key]?.themeId];
            if (nextTheme) setTheme(nextTheme);
          }
        }}
        themes={THEMES}
        theme={theme}
        onThemeChange={(t) => { setThemeManual(true); setTheme(t); }}
        onThemeReset={() => {
          setThemeManual(false);
          const suggested = THEMES_BY_ID[deckThemeId];
          if (suggested) setTheme(suggested);
        }}
        themeManual={themeManual}
        deckThemeId={deckThemeId}
        styleModes={STYLE_MODES}
        styleModeId={styleModeId}
        onStyleModeChange={setStyleModeId}
        renderFamily={renderFamily}
        onRenderFamilyChange={setRenderFamily}
        showLayoutFamilies={showLayoutFamilies}
        animOptions={showEffects ? animOptions : undefined}
        onAnimOptionsChange={showEffects ? setAnimOptions : undefined}
        heroImage={showBackground ? heroImage : undefined}
        heroImageEnabled={showBackground ? heroImageEnabled : undefined}
        onHeroImageToggle={showBackground ? setHeroImageEnabled : undefined}
        onHeroImageChange={showBackground ? setHeroImage : undefined}
      />
    </div>
  );
}

export const Default = {
  render: () => <ControlPanelHarness />,
};

export const BrutalistStyle = {
  render: () => (
    <ControlPanelHarness
      initialStyleModeId="brutalist"
      initialThemeId="neon-noir"
    />
  ),
};

export const MinimalSections = {
  render: () => (
    <ControlPanelHarness
      showLayoutFamilies={false}
      showEffects={false}
      showBackground={false}
    />
  ),
};

export const LightTheme = {
  render: () => (
    <ControlPanelHarness
      initialThemeId="paper-ink"
      initialDeckKey="atelier-sage"
    />
  ),
};
