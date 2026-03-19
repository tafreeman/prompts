# decks-generated

A YAML-to-PPTX deck builder designed for AI copiloting. Authors write slide
content in structured YAML manifests, Zod schemas enforce presentation design
best practices (assertion-evidence model, 7+/-2 rule, 60-30-10 color), and the
pipeline renders to both a live browser preview and PowerPoint export.

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Validate the example deck
npm run validate decks/example-pitch.yaml

# 3. Export to PowerPoint
npm run export:pptx decks/example-pitch.yaml
```

## Architecture

```
  manifest.yaml          Zod Schemas             Output
 +----------------+    +----------------+    +------------------+
 |                |    |  SlideSchema   |    |                  |
 |  title: ...    |--->|  (12 layouts)  |--->|  React Preview   |
 |  theme: ...    |    |  DeckManifest  |    |  (Vite dev)      |
 |  slides:       |    |  ActionTitle   |    |                  |
 |    - layout:   |    |  BulletList    |    +------------------+
 |      title:    |    |  Source        |
 |      ...       |    +-------+--------+    +------------------+
 |                |            |             |                  |
 +----------------+     loadDeckOrThrow      |  PPTX Export     |
                               |             |  (pptxgenjs)     |
                               +------------>|                  |
                                             +------------------+
```

**Pipeline:** YAML file -> js-yaml parse -> Zod validation -> React components
(browser) or pptxgenjs builders (PowerPoint).

## CLI Commands

| Command | Description |
|---------|-------------|
| `npm run validate <file>` | Validate a deck manifest against Zod schemas |
| `npm run export:pptx <file>` | Export a validated deck to .pptx |
| `npm run new-deck -- --framework <id> --name <name>` | Scaffold from a framework template |
| `npm run dev` | Start Vite dev server for browser preview |
| `npm run build` | TypeScript check + Vite production build |
| `npm run typecheck` | TypeScript type checking only |
| `npm run test` | Run E2E lifecycle tests (Vitest) |
| `npm run audit` | Run design compliance audit (token usage, WCAG contrast) |

## Project Structure

```
decks-generated/
  decks/                  # Deck YAML files
    example-pitch.yaml    # Working 12-slide example
  src/
    schemas/              # Zod schemas (12 layouts, manifest, guards, framework)
    tokens/               # Design tokens (themes, style modes, type scale, spacing)
    frameworks/           # 5 framework templates with sample manifests
    layouts/              # 12 React layout components + registry
    components/           # Shared primitives (Heading, Body, Card, etc.)
    export/               # PPTX renderer + layout builders
    parse.ts              # YAML loading + validation pipeline
    cli/                  # CLI entry points (validate, build)
  tests/                  # Vitest E2E lifecycle tests
  scripts/                # Export, scaffolding, and audit scripts
```

## AI Usage

See [CLAUDE.md](./CLAUDE.md) for the complete AI copilot reference including:
- All 12 layout schemas with every field documented
- All 5 framework templates with slot definitions
- Common Zod validation errors and how to fix them
- AI copilot dry-run protocol
