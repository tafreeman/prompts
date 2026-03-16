# Presentation System

React 19 + Vite 5 presentation platform. 10 decks, 34 registered layouts, 15 themes, 4 style modes.

## Quick Start

```bash
npm install && npm run dev       # Dev on :5173
npm run storybook                # Storybook on :6006
npm run build                    # Production build
npm run export:all               # Export HTML + images + PDF
```

## Architecture

- **Entry:** `src/App.v14.jsx` (900 lines) — deck factory, transcription, state management
- **Registry:** `layoutRegistry.register(id, Component)` — 34 IDs across 8 families
- **Transcription:** `transcribeTopic(topic, family)` reshapes content across layout families
- **Tokens:** `src/tokens/*.ts` — Theme, StyleMode, TypeScaleEntry interfaces
- **Decks:** `src/content/*/deck.js` — 6 content decks + 4 reference/legacy decks
- **ControlPanel:** Floating right-side drawer (DECK / THEME / STYLE / RENDER AS / EFFECTS / BACKGROUND)

## App Versions (main.jsx)

v10 (monolith), v10.2 (dense monolith), v13 (extracted), v14 (registry-based, current)

## Layout Families

base (6), verge-pop (6), sprint (1), onboarding (7), handbook (5), engineering (4), advocacy (5), advocacy-dense (5) = 34 total

## Storybook

60 stories, autodocs enabled. ThemeContext + ChromeContext decorator with theme/chrome toolbar selectors in `.storybook/preview.jsx`.

## Gotchas

- Rollup does NOT auto-resolve `.js` → `.ts` — update import paths when renaming
- Tokens are `.ts` with exported interfaces — import with `.ts` extension
- All components are `.tsx`, stories remain `.jsx`
- No vitest — visual testing only via Storybook
- `@storybook/addon-actions` not installed — use `console.log` shim instead
