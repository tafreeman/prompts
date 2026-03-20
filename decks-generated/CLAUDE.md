# decks-generated

YAML-to-PPTX deck builder with AI copiloting. Write slide content in YAML,
validate with Zod schemas, preview in the browser, and export to PowerPoint.

## Quick Start

```bash
npm install
npm run validate decks/example-pitch.yaml
npm run export:pptx decks/example-pitch.yaml
```

## Commands

| Command | Description |
|---------|-------------|
| `npm run validate <file>` | Validate a deck YAML against Zod schemas |
| `npm run build:deck <file>` | Build a deck (validate + export) |
| `npm run export:pptx <file>` | Export a validated deck to PPTX |
| `npm run new-deck -- --framework <id> --name <name>` | Scaffold a new deck from a framework template |
| `npm run dev` | Start Vite dev server (browser preview) |
| `npm run build` | TypeScript check + Vite production build |
| `npm run typecheck` | TypeScript type checking (no emit) |
| `npm run test` | Run Vitest E2E lifecycle tests |
| `npm run audit` | Run design compliance audit (tokens, contrast) |

## How to Create a Deck

### From a Framework Template (recommended)

```bash
npm run new-deck -- --framework pitch-deck --name my-pitch
```

Then edit `decks/my-pitch/manifest.yaml`, replacing `[placeholder]` values.

### From Scratch

1. Copy from `decks/example-pitch.yaml`
2. Edit the YAML -- every slide needs: `id`, `layout`, `title`
3. Run `npm run validate <file>` to check for errors
4. Run `npm run export:pptx <file>` to generate PPTX

## Framework Templates

Pre-structured deck skeletons that AI populates with content. Each framework
defines required slides, layouts, and content hints.

| Framework ID | Name | Audience | Slides | Theme | Style |
|---|---|---|---|---|---|
| executive-brief | Executive Brief | C-suite, board | 4-8 | midnight-teal | clean |
| pitch-deck | Pitch Deck | Investors, VCs | 8-12 | midnight-teal | bold |
| strategy-scr | Strategy (SCR) | Internal stakeholders | 5-8 | signal-cobalt | clean |
| tech-architecture | Tech Architecture | Engineering teams | 6-10 | linear | editorial |
| status-report | Status Report | Program managers | 5-8 | paper-ink | clean |

### Framework Slot Definitions

Each framework defines ordered slots. Each slot specifies a position, layout,
title hint (pattern for AI to follow), content hint (guidance), and whether
it's required.

**executive-brief** (5 slots):
1. `cover` -- Opening slide with company/project name and 2-3 top-level KPIs
2. `text` -- Core problem or opportunity in 3-5 bullets, quantified cost of inaction
3. `cards` -- 3-4 cards summarizing solution pillars (title, stat, body)
4. `number` -- Single big number showing ROI, cost savings, or revenue impact
5. `closing` -- Decision needed, 3-4 concrete next steps, contact

**pitch-deck** (8 slots):
1. `cover` -- Company name, tagline, 2-3 headline KPIs (ARR, growth, customers)
2. `text` -- Problem statement with data, cost of status quo
3. `cards` -- 3-4 product pillars with key metrics per pillar
4. `scorecard` -- 4-6 KPIs: ARR, customers, retention, growth, churn
5. `number` -- TAM/SAM opportunity size with CAGR and SAM breakdown
6. `grid` (optional) -- 4-6 product capability cells with stats
7. `timeline` -- 4-6 milestones from current state to target ARR
8. `closing` -- Ask amount, valuation, use of funds, contact

**strategy-scr** (6 slots):
1. `cover` -- Strategy name and 2-3 KPIs showing current state or target
2. `text` -- Situation: shared understanding, 3-5 factual bullets
3. `compare` -- Complication: left=current pain, right=what happens if we act
4. `steps` -- Resolution: 3-5 concrete steps with descriptions
5. `scorecard` (optional) -- Evidence: 3-5 KPIs from pilots/benchmarks
6. `closing` -- Clear ask, 3-4 next steps with owners and timelines

**tech-architecture** (8 slots):
1. `cover` -- System name and 2-3 key technical metrics
2. `text` -- Business context, technical constraints, key requirements
3. `compare` -- Current architecture limitations vs. proposed benefits
4. `grid` -- 4-6 major system components with key specs
5. `steps` -- 3-5 implementation phases with deliverables
6. `table` -- Success metrics: current values, targets, measurement method
7. `timeline` (optional) -- 4-6 milestones from design review to production GA
8. `closing` -- Decision needed, review process, next steps with owners

**status-report** (6 slots):
1. `cover` -- Program name and 2-3 high-level status KPIs
2. `scorecard` -- 4-6 KPIs with trends: budget, schedule, scope, quality, risk
3. `steps` -- 3-5 workstream progress items
4. `table` -- Risk register: risk, likelihood, impact, mitigation, owner
5. `timeline` -- 4-6 milestones showing past completions and upcoming deadlines
6. `closing` -- Blockers requiring sponsor action, 3-4 next steps with owners

### AI Workflow

1. **Pick a framework** -- choose the template that matches your audience
2. **Scaffold** -- `npm run new-deck -- --framework <id> --name <name>`
3. **Edit YAML** -- replace all `[placeholder]` values with real content
4. **Validate** -- `npm run validate decks/<name>/manifest.yaml`
5. **Preview** -- `npm run dev` then open in browser
6. **Export** -- `npm run export:pptx decks/<name>/manifest.yaml`

### AI Copilot Dry-Run Protocol

When an AI creates a deck from scratch, follow this protocol:

1. Read this CLAUDE.md to understand available layouts, themes, and frameworks
2. Run `npm run new-deck -- --framework <id> --name <name>` to scaffold
3. Edit `decks/<name>/manifest.yaml`:
   - Fill in title, subtitle, author, date
   - Populate each slot with domain-specific content
   - Use stat values, KPIs, timeline events as appropriate
4. Run `npm run validate decks/<name>/manifest.yaml`
5. If errors: read the error messages, fix the YAML, re-validate
6. Run `npm run export:pptx decks/<name>/manifest.yaml`

**Success criteria:**
- AI never writes JSX -- only edits YAML manifest
- Validation errors are specific enough for AI to self-correct
- Resulting deck has 5+ slides across 3+ layout types

### Layout Catalog

View all 17 layouts with sample data at `?view=catalog` (append to dev server URL).

## Complete Layout Reference

All slides share these base fields:
- `id` (string, required) -- unique slide identifier
- `title` (string, required) -- action title stating a conclusion (1-100 chars)
- `subtitle` (string, optional) -- max 200 chars
- `eyebrow` (string, optional) -- uppercase label, max 50 chars
- `notes` (string, optional) -- speaker notes
- `bgOverride` (string, optional) -- per-slide background color override

### cover

Opening slide with company/project branding.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"cover"` | yes | |
| tagline | string | no | Short memorable phrase |
| kpis | KPI[] | no | Max 4; each: `{value, label, trend?, detail?}` |

### section

Section divider between major topics.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"section"` | yes | |
| sectionNumber | string or number | no | e.g., `1`, `"02"` |

### text

Body text slide with optional bullets, image, and two-column mode.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"text"` | yes | |
| body | string | no | Paragraph text |
| bullets | string[] | no | Max 7 items |
| image | string | no | URL or path |
| imageAlt | string | no | Alt text for image |
| columns | `"1"` or `"2"` | no | Default `"1"` |
| leftColumn | Column | no | Used when `columns: "2"` |
| rightColumn | Column | no | Used when `columns: "2"` |
| callout | string | no | Highlighted takeaway |
| source | string | no | Data source citation |

Column object: `{title?, body?, bullets?, items?}` (items: max 7 strings)

### cards

2-6 content or stat cards in a responsive grid.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"cards"` | yes | |
| cards | Card[] | yes | 1-6 items |
| callout | string | no | Highlighted takeaway |
| source | string | no | Data source citation |

Card object: `{title, body?, stat?, label?, icon?}`

### number

Single oversized metric with supporting context.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"number"` | yes | |
| stat | string or number | yes | The big metric value |
| statLabel | string | yes | What the number represents |
| context | string | no | Supporting paragraph |
| source | string | no | Data source citation |

### compare

Side-by-side comparison using two columns.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"compare"` | yes | |
| left | Column | yes | Left column content |
| right | Column | yes | Right column content |
| callout | string | no | Highlighted takeaway |
| source | string | no | Data source citation |

### steps

Process flow showing 2-7 ordered steps.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"steps"` | yes | |
| steps | Step[] | yes | 2-7 items |
| callout | string | no | Highlighted takeaway |

Step object: `{label, description?, icon?}`

### table

Tabular data in a styled HTML table.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"table"` | yes | |
| columns | string[] | yes | 1-8 column headers |
| rows | Record[] | yes | Min 1; keys match column names, values: string or number |
| highlight | string | no | Row ID or column to highlight |
| source | string | no | Data source citation |

### scorecard

KPI dashboard showing 1-8 key performance indicators.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"scorecard"` | yes | |
| kpis | KPI[] | yes | 1-8 items |
| callout | string | no | Highlighted takeaway |
| source | string | no | Data source citation |

KPI object: `{value, label, trend?, detail?}` (trend: `"up"`, `"down"`, or `"flat"`)

### timeline

Roadmap or history with 2-10 events.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"timeline"` | yes | |
| events | Event[] | yes | 2-10 items |
| callout | string | no | Highlighted takeaway |

Event object: `{date, title, description?, icon?}`

### grid

Card grid with 2-9 cells in configurable columns.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"grid"` | yes | |
| cells | Cell[] | yes | 2-9 items |
| columns | 2, 3, or 4 | no | Default 3 |
| callout | string | no | Highlighted takeaway |

Cell object: `{title, body?, stat?, icon?, size?}` (size: `"sm"`, `"md"`, or `"lg"`, default `"md"`)

### closing

Final call-to-action slide.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"closing"` | yes | |
| nextSteps | string[] | no | Max 7 action items |
| contact | string | no | Email or URL |

### chart

Grouped horizontal (or vertical) bar chart with optional comparison annotations panel.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"chart"` | yes | |
| chartType | `"bar-h"` or `"bar-v"` | no | Default `"bar-h"` |
| unit | string | no | e.g. `"%"` or `"$M"` |
| groups | Group[] | yes | 1-4 groups |
| annotations | Annotation[] | no | Right-side comparison panel |
| source | string | no | Data source citation |

Group: `{id, label?, bars[]}` — Bar: `{label, value, highlight?, accent?}` (highlight=pill band, accent=darker color)
Annotation: `{label, items?: [{label, value}]}`

### hub

Hub-and-spoke diagram — center concept with up to 8 labeled spoke endpoints and diagonal connector lines.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"hub"` | yes | |
| center | Center | yes | `{label, sublabel?}` |
| spokes | Spoke[] | yes | 2-8 items |
| body | string | no | Supporting text (bottom-right) |

Spoke: `{position: "top"|"bottom"|"left"|"right", label, eyebrow?}`

### workflow

Three-column process table — stage label | description | meta/time. No cell backgrounds, only horizontal dividers.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"workflow"` | yes | |
| columnLabels | [string, string, string] | no | Column header labels |
| stages | Stage[] | yes | 2-12 items |

Stage: `{label, description?, meta?, highlight?}` (highlight row shows full-opacity bold text)

### cycle

Circle/arc diagram — input node feeds into center arc, output items branch from the right.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"cycle"` | yes | |
| centerLabel | string | no | Text inside the circle |
| input | Node | no | Left input: `{label, body?}` |
| outputs | Node[] | yes | 1-6 right-side outputs: `{label, body?}` |
| source | string | no | Data source citation |

### quote

Large editorial pull-quote with decorative opening mark and attribution.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| layout | `"quote"` | yes | |
| quote | string | yes | Max 500 chars |
| attribution | string | no | Speaker name |
| role | string | no | Title and company |
| logo | string | no | Company logo URL |

## Themes

| ID | Name | Vibe | Fonts | Background |
|----|------|------|-------|------------|
| midnight-teal | Midnight Teal | Professional tech | Space Grotesk / DM Sans | Dark (#0B1426) |
| neon-noir | Neon Noir | Cyberpunk bold | Chakra Petch / Barlow | Dark (#050508) |
| linear | Linear | Clean product | Inter / Inter | Dark (#0F1117) |
| paper-ink | Paper & Ink | Classic editorial | DM Serif Display / Atkinson Hyperlegible | Light (#FAF8F5) |
| signal-cobalt | Signal Cobalt | Corporate systems | Sora / Libre Franklin | Light (#F7F6F1) |
| studio-craft | Studio Craft | Warm handbook | Syne / IBM Plex Sans | Light (#F8F6F0) |

## Style Modes

| ID | Name | Vibe | Radius | Border | Heading |
|----|------|------|--------|--------|---------|
| clean | Clean | Modern Tech | 16px | 1px | 700 normal |
| bold | Bold | Swiss Systems | 0px | 3px | 900 uppercase |
| editorial | Editorial | Magazine Pacing | 4px | 1px | 600 normal |

## Design Rules (enforced by schema)

- `title` required on every slide -- must be an action title (conclusion, not label)
- Max 7 bullets per list
- Max 6 cards per slide
- Max 7 process steps
- Max 8 KPIs per scorecard
- Max 10 timeline events
- Max 9 grid cells
- Max 4 cover KPIs
- Max 8 table columns
- Slide count: 1-50
- Source attribution recommended on data slides

## Troubleshooting: Common Zod Validation Errors

### "Action title required"
**Cause:** A slide has an empty `title` field.
**Fix:** Every slide must have a non-empty title stating a conclusion, not a descriptive label.
```yaml
# Bad
title: ""
title: "Quarterly Results"

# Good
title: "Q3 Revenue Exceeded Target by 15%"
```

### "String must contain at most 100 character(s)"
**Cause:** Title exceeds 100 characters.
**Fix:** Shorten the title. Move detail to `subtitle` or `body`.

### "Array must contain at most 7 element(s)" (bullets)
**Cause:** More than 7 bullets in a list.
**Fix:** Split into two slides or consolidate bullets.

### "Array must contain at most 6 element(s)" (cards)
**Cause:** More than 6 cards on a single slide.
**Fix:** Split into two card slides or use a grid layout instead.

### "Duplicate slide IDs: xxx"
**Cause:** Two or more slides share the same `id` value.
**Fix:** Every slide `id` must be unique within the deck.

### "Invalid discriminator value" (layout)
**Cause:** The `layout` field contains an unrecognized layout name.
**Fix:** Use one of the 12 valid layouts: cover, section, text, cards, number,
compare, steps, table, scorecard, timeline, grid, closing.

### "Required" on a field
**Cause:** A required field is missing from the YAML.
**Fix:** Check the layout reference above for required fields.

### "YAML parse error"
**Cause:** The YAML file has a syntax error (bad indentation, unclosed quotes, etc.).
**Fix:** Check indentation (2-space), ensure strings with special characters are quoted.

### "Deck must have at least 1 slide"
**Cause:** The `slides` array is empty.
**Fix:** Add at least one slide to the deck.

### "Max 50 slides per deck"
**Cause:** More than 50 slides in the deck.
**Fix:** Split into multiple decks or consolidate slides.
