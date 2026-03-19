import { useState, useEffect, useCallback, type CSSProperties } from 'react';
import yaml from 'js-yaml';
import { ThemeContext } from './components/context/ThemeContext.js';
import { StyleContext } from './components/context/StyleContext.js';
import { DeckContext } from './components/context/DeckContext.js';
import { SlideContainer } from './components/deck/SlideContainer.js';
import { SlideNavigator } from './components/deck/SlideNavigator.js';
import { LayoutRenderer } from './layouts/LayoutRenderer.js';
import { LayoutCatalog } from './components/catalog/LayoutCatalog.js';
import { validateManifest } from './schemas/manifest.js';
import { THEMES_BY_ID, THEMES } from './tokens/themes.js';
import { STYLE_MODES_BY_ID, STYLE_MODES } from './tokens/style-modes.js';
import type { ThemeId } from './tokens/themes.js';
import type { StyleModeId } from './tokens/style-modes.js';
import type { DeckManifest } from './schemas/manifest.js';

// Vite raw import of the example deck YAML
import exampleYaml from '../decks/example-pitch.yaml?raw';

/**
 * Root application — loads a deck manifest and renders slides
 * with theme/style context + keyboard navigation.
 *
 * Query param: ?view=catalog renders the LayoutCatalog instead.
 */
export default function App() {
  // Check for catalog view mode
  const params = new URLSearchParams(window.location.search);
  if (params.get('view') === 'catalog') {
    return <LayoutCatalog />;
  }
  const [deck, setDeck] = useState<DeckManifest | null>(null);
  const [slideIndex, setSlideIndex] = useState(0);
  const [themeId, setThemeId] = useState<ThemeId>('midnight-teal');
  const [styleId, setStyleId] = useState<StyleModeId>('clean');
  const [error, setError] = useState<string | null>(null);
  const [controlsVisible, setControlsVisible] = useState(false);

  // Load and validate the example deck on mount
  useEffect(() => {
    try {
      const raw = yaml.load(exampleYaml);
      const result = validateManifest(raw);
      if (result.success && result.data) {
        setDeck(result.data);
        setThemeId(result.data.theme as ThemeId);
        setStyleId(result.data.style as StyleModeId);
      } else {
        setError(result.errors?.join('\n') ?? 'Unknown validation error');
      }
    } catch (e) {
      setError(`YAML parse error: ${(e as Error).message}`);
    }
  }, []);

  const handleNavigate = useCallback((index: number) => {
    setSlideIndex(index);
  }, []);

  // Resolve tokens
  const theme = THEMES_BY_ID[themeId] ?? THEMES[0];
  const style = STYLE_MODES_BY_ID[styleId] ?? STYLE_MODES[0];
  const currentSlide = deck?.slides[slideIndex];

  // Hover-reveal for control bar
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    function handleMove() {
      setControlsVisible(true);
      clearTimeout(timer);
      timer = setTimeout(() => setControlsVisible(false), 3000);
    }
    window.addEventListener('mousemove', handleMove);
    return () => {
      window.removeEventListener('mousemove', handleMove);
      clearTimeout(timer);
    };
  }, []);

  // Error state
  if (error) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        fontFamily: 'monospace',
        color: '#EF4444',
        background: '#0B0F1A',
        padding: 40,
        whiteSpace: 'pre-wrap',
      }}>
        <div>
          <h2 style={{ marginBottom: 16 }}>Deck Validation Error</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  // Loading state
  if (!deck || !currentSlide) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        color: '#CBD5E1',
        fontFamily: 'system-ui',
        background: '#0B0F1A',
      }}>
        Loading deck...
      </div>
    );
  }

  return (
    <ThemeContext.Provider value={theme}>
      <StyleContext.Provider value={style}>
        <DeckContext.Provider value={deck}>
          {/* Load theme fonts */}
          <link href={theme.fontsUrl} rel="stylesheet" />

          {/* Slide viewport */}
          <SlideContainer bgOverride={currentSlide.bgOverride}>
            <LayoutRenderer slide={currentSlide} />
          </SlideContainer>

          {/* Navigation */}
          <SlideNavigator
            totalSlides={deck.slides.length}
            currentIndex={slideIndex}
            onNavigate={handleNavigate}
          />

          {/* Theme/Style control bar — hover reveal, bottom-left */}
          <ControlBar
            themeId={themeId}
            styleId={styleId}
            onThemeChange={setThemeId}
            onStyleChange={setStyleId}
            visible={controlsVisible}
          />
        </DeckContext.Provider>
      </StyleContext.Provider>
    </ThemeContext.Provider>
  );
}

// -- ControlBar (inline, minimal) -----------------------------------------

interface ControlBarProps {
  themeId: ThemeId;
  styleId: StyleModeId;
  onThemeChange: (id: ThemeId) => void;
  onStyleChange: (id: StyleModeId) => void;
  visible: boolean;
}

function ControlBar({
  themeId,
  styleId,
  onThemeChange,
  onStyleChange,
  visible,
}: ControlBarProps) {
  const barStyle: CSSProperties = {
    position: 'fixed',
    bottom: 16,
    left: 16,
    display: 'flex',
    gap: 8,
    alignItems: 'center',
    background: 'rgba(15,22,41,0.92)',
    backdropFilter: 'blur(8px)',
    border: '1px solid rgba(100,255,218,0.15)',
    borderRadius: 999,
    padding: '6px 12px',
    zIndex: 1000,
    opacity: visible ? 0.95 : 0,
    transition: 'opacity 0.3s ease',
    pointerEvents: visible ? 'auto' : 'none',
  };

  const selectStyle: CSSProperties = {
    background: 'rgba(255,255,255,0.06)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: 6,
    color: '#CBD5E1',
    fontSize: 11,
    padding: '3px 6px',
    fontFamily: 'system-ui',
    cursor: 'pointer',
    outline: 'none',
  };

  const labelStyle: CSSProperties = {
    fontSize: 9,
    color: 'rgba(100,255,218,0.6)',
    textTransform: 'uppercase',
    letterSpacing: 1.5,
    fontWeight: 700,
    fontFamily: 'system-ui',
  };

  return (
    <div style={barStyle}>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        <span style={labelStyle}>Theme</span>
        <select
          style={selectStyle}
          value={themeId}
          onChange={(e) => onThemeChange(e.target.value as ThemeId)}
        >
          {THEMES.map((t) => (
            <option key={t.id} value={t.id}>{t.name}</option>
          ))}
        </select>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        <span style={labelStyle}>Style</span>
        <select
          style={selectStyle}
          value={styleId}
          onChange={(e) => onStyleChange(e.target.value as StyleModeId)}
        >
          {STYLE_MODES.map((m) => (
            <option key={m.id} value={m.id}>{m.name}</option>
          ))}
        </select>
      </div>
    </div>
  );
}
