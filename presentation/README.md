# Presentation Starter Kit

A config-driven React framework for building internal advocacy decks and presentation artifacts. Edit a single JSON file to customize content — the renderer handles layout, animation, and theming.

Works with any AI artifact renderer (Claude, ChatGPT, Gemini, etc.) or as a standard React app.

## Quick Start

1. Copy `advocacy-deck-artifact.jsx` into your AI tool's artifact/code panel
2. Edit the `config` object at the top to replace placeholder content with your data
3. Run/preview — the deck renders immediately

## Files

| File | Purpose |
|------|---------|
| `deck-config.json` | Standalone JSON config — edit this to customize your deck |
| `advocacy-deck.jsx` | Renderer app (imports JSON) — use in a standard React project |
| `advocacy-deck-artifact.jsx` | Single-file version (config inlined) — paste into any AI artifact |
| `presentation_starter.jsx` | Original reference implementation with inline config |
| `advocacy-deck-refactor.md` | The AI prompt that generates these files from scratch |

## Available Layouts

| Layout | Description |
|--------|-------------|
| `stat-cards` | Metric-driven cards with stat values and body text |
| `before-after` | Two-column challenge vs. solution split |
| `pillars` | 3-4 column pillar breakdown with optional results column |
| `timeline` | Horizontal phased roadmap with milestone cards |
| `sprint` | Animated figure-8 process diagram with human/AI nodes |
| `results` | KPI metric grid with supporting narrative cards |
| `personas` | Stakeholder role cards with pain/gain framing |
| `comparison` | Evaluation matrix comparing options across criteria |

## How to Edit the Config

### Deck-level settings
```json
{
  "deck": {
    "brand": "Your Brand · Division",
    "title": "Deck Title",
    "titleAccent": "Subtitle with Gradient",
    "tagline": "One-line description shown on landing page.",
    "accentGradient": ["#22D3EE", "#10B981"],
    "stats": [{ "val": "42%", "label": "Metric Name" }]
  }
}
```

### Adding a page
Add an entry to `pages[]`:
```json
{
  "id": "unique-id",
  "num": "01",
  "title": "Page Title",
  "subtitle": "Short subtitle.",
  "icon": "◉",
  "theme": { "color": "#0891B2", "light": "#22D3EE" },
  "layout": "stat-cards",
  "callout": "Bold closing statement.",
  "cards": [
    { "title": "Card", "body": "Description.", "stat": { "value": "X", "label": "Label" } }
  ]
}
```

The `layout` field determines which screen type renders. See the schema in `deck-config.json` for layout-specific fields (`before`/`after`, `phases`, `sprint`, `metrics`, `pillars`, `comparison`).

## Adding a New Layout Type

1. Create a new React component: `function MyLayoutScreen({ page, onBack }) { ... }`
2. Use `ScreenShell` for consistent chrome (particles, back button, header)
3. Add the case to `ScreenRouter`
4. Document any new config fields your layout expects

## Theme Customization

Edit `deck.theme` in the config to change colors, fonts, and background:
```json
"theme": {
  "bg": "#0B1426",
  "bgCard": "#111827",
  "text": "#F0F4F8",
  "fontDisplay": "'Space Grotesk', sans-serif",
  "fontBody": "'DM Sans', sans-serif",
  "googleFontsUrl": "https://fonts.googleapis.com/css2?family=..."
}
```

Per-page accent colors are set via `page.theme.color` and `page.theme.light`. Glow colors are derived automatically.
