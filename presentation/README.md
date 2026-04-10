# Presentation System

React 18 + Vite 5 presentation platform with 10 decks, 34 registered layouts, 15 themes, and 4 style modes. Includes Storybook for visual testing and an export pipeline for HTML, images, and PDF.

## Quick Start

```bash
cd presentation
npm install

npm run dev          # Dev server on :5173
npm run build        # Production build (TypeScript check + Vite)
npm run storybook    # Storybook on :6006 (60 stories, autodocs)
npm run export:all   # Export HTML + images + PDF
```

## Architecture

| Layer | Description |
|-------|-------------|
| **Entry** | `src/App.v14.jsx` — deck factory, transcription, state management |
| **Layout Registry** | `layoutRegistry.register(id, Component)` — 34 IDs across 8 families |
| **Transcription** | `transcribeTopic(topic, family)` reshapes content across layout families |
| **Tokens** | `src/tokens/*.ts` — `Theme`, `StyleMode`, `TypeScaleEntry` interfaces |
| **Decks** | `src/content/*/deck.js` — 6 content decks + 4 reference/legacy decks |
| **Control Panel** | Floating right-side drawer (DECK / THEME / STYLE / RENDER AS / EFFECTS / BACKGROUND) |

## Layout Families

| Family | Count | Purpose |
|--------|-------|---------|
| base | 6 | Foundation layouts |
| verge-pop | 6 | Visual-heavy layouts |
| sprint | 1 | Sprint/agile layout |
| onboarding | 7 | Team onboarding |
| handbook | 5 | Reference handbook |
| engineering | 4 | Technical deep-dives |
| advocacy | 5 | Advocacy/persuasion |
| advocacy-dense | 5 | Dense advocacy variant |
| **Total** | **34** | |

## Storybook

60 stories with autodocs enabled. Global `ThemeContext` + `ChromeContext` decorator with theme/chrome toolbar selectors in `.storybook/preview.jsx`.

## Copilot Reference

See [CLAUDE.md](CLAUDE.md) for AI assistant context including gotchas and build details.

## Related

- [Deck Generator](../decks-generated/README.md) — YAML-to-PPTX builder using the same design tokens
- [Root README](../README.md) — Monorepo overview
