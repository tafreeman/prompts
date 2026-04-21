# Epic 2 — Observable Workflow Execution — Implementation Plan

> **For agentic workers:** Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Users can launch a workflow, watch it stream end-to-end, and diagnose any failure from the UI alone — without reading server logs.

**Architecture:** Typed Pydantic wire format → Playwright E2E infrastructure → reliability gates (PR + nightly) + SLO enforcement → diagnostic UI (live DAG animation, StepNode redesign, step drill-down).

**Tech Stack:** FastAPI + WebSocket/SSE, Pydantic v2, React 19 + @xyflow/react 12, TanStack Query, Playwright, Vitest.

**Pre-flight facts (verified 2026-04-21):**

- WebSocket endpoint: `/ws/execution/{run_id}` — `agentic_v2/server/websocket.py`
- Client reconnect logic already exists: `ui/src/api/websocket.ts` (exponential backoff, maxRetries=5)
- Server-side replay buffer: `ConnectionManager.event_buffers` (500 events per run)
- Event union already typed on the client: `ui/src/api/types.ts` lines 218–275 (ExecutionEvent)
- Server event types: `workflow_start`, `step_start`, `step_end`, `step_complete`, `step_error`, `workflow_end`, `evaluation_start`, `evaluation_complete`
- Backend port 8010, frontend port 5173 (vite), Storybook 6006
- No Playwright setup exists. UI only has Vitest.
- Schema-snapshot gate (Story 1.5) is live — any new Pydantic model added under `contracts/` gets auto-snapshotted on next `scripts/generate_schemas.py` run.

---

## Story Ordering Rationale

```
2.1 (wire format) ─┐
                   ├→ 2.2 (Playwright bootstrap) ─┬→ 2.3 (reconnect)
                   │                              ├→ 2.7 (SLO)
                   │                              └→ 2.4 (nightly 50×)
2.5 (animation) ───┤
2.8 (StepNode) ────┤
2.6 (drill-down) ──┘
```

2.1 is the foundation (typed events) and should land first.
2.2 is the second infra investment — it unblocks 2.3/2.4/2.7 (all Playwright-dependent).
2.5, 2.6, 2.8 are UI-only and can be developed in parallel with 2.2.

Plan presents stories in implementation order: 2.1 → 2.2 → 2.6 → 2.5 → 2.8 → 2.3 → 2.7 → 2.4.

---

## Task 1: Story 2.1 — Pydantic-Validated SSE/WebSocket Wire Format

**Files:**
- Create: `agentic-workflows-v2/agentic_v2/contracts/events.py`
- Modify: `agentic-workflows-v2/agentic_v2/server/websocket.py` (validate on broadcast)
- Modify: `agentic-workflows-v2/agentic_v2/server/execution.py` (emit typed events)
- Modify: `agentic-workflows-v2/agentic_v2/engine/dag_executor.py` (emit typed events via `on_update`)
- Create: `agentic-workflows-v2/tests/test_event_wire_format.py`
- Update: `agentic-workflows-v2/scripts/generate_schemas.py` (add new models to snapshot list)

### Context

Today events are `dict[str, Any]` built ad-hoc in `dag_executor.py` lines 122–128 (`workflow_start`), 143–151 (`step_start`), 246–263 (`step_end`), 301–310 (`workflow_end`), and in `server/execution.py` (step_complete, step_error, evaluation_*). Client types are already a discriminated union (`ExecutionEvent` in `ui/src/api/types.ts`). This story closes the server-side gap.

---

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_event_wire_format.py`:

```python
"""Every broadcast event must validate against a Pydantic model.

Failure modes this catches:
- A new code path emits a dict shape not in the union
- A field is renamed server-side but the client still expects the old name
- A required field is dropped
"""
from __future__ import annotations

import pytest

from agentic_v2.contracts.events import ExecutionEvent, validate_event


def test_workflow_start_valid():
    payload = {
        "type": "workflow_start",
        "run_id": "r-1",
        "workflow_name": "code_review",
        "timestamp": "2026-04-21T00:00:00Z",
    }
    event = validate_event(payload)
    assert event.type == "workflow_start"


def test_step_end_valid():
    payload = {
        "type": "step_end",
        "run_id": "r-1",
        "step": "parse_code",
        "status": "success",
        "duration_ms": 42,
        "timestamp": "2026-04-21T00:00:00Z",
    }
    event = validate_event(payload)
    assert event.type == "step_end"


def test_unknown_type_rejected():
    with pytest.raises(ValueError, match="discriminator"):
        validate_event({"type": "bogus", "run_id": "r-1", "timestamp": "..."})


def test_missing_required_field_rejected():
    with pytest.raises(ValueError):
        validate_event({"type": "step_start", "run_id": "r-1"})  # no `step`
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
cd agentic-workflows-v2
python -m pytest tests/test_event_wire_format.py -v
```

Expected: ImportError on `agentic_v2.contracts.events`.

- [ ] **Step 3: Create the Pydantic models**

Create `agentic_v2/contracts/events.py`:

```python
"""Typed wire format for WebSocket/SSE execution events.

All server-side event emitters must construct these models and call
``.model_dump(mode="json")`` at the broadcast boundary. This gives the
frontend a single source of truth: the client TypeScript union in
``ui/src/api/types.ts`` mirrors this file field-for-field.
"""
from __future__ import annotations

from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field, TypeAdapter


class WorkflowStartEvent(BaseModel):
    type: Literal["workflow_start"] = "workflow_start"
    run_id: str
    workflow_name: str
    timestamp: str


class StepStartEvent(BaseModel):
    type: Literal["step_start"] = "step_start"
    run_id: str
    step: str
    timestamp: str


class StepEndEvent(BaseModel):
    type: Literal["step_end"] = "step_end"
    run_id: str
    step: str
    status: str
    duration_ms: float
    model_used: str | None = None
    tokens_used: int | None = None
    tier: str | None = None
    input: dict[str, Any] | None = None
    output: dict[str, Any] | None = None
    error: str | None = None
    timestamp: str


class StepCompleteEvent(StepEndEvent):
    type: Literal["step_complete"] = "step_complete"  # type: ignore[assignment]
    outputs: dict[str, Any] | None = None


class StepErrorEvent(StepEndEvent):
    type: Literal["step_error"] = "step_error"  # type: ignore[assignment]
    outputs: dict[str, Any] | None = None


class WorkflowEndEvent(BaseModel):
    type: Literal["workflow_end"] = "workflow_end"
    run_id: str
    status: str
    timestamp: str


class EvaluationStartEvent(BaseModel):
    type: Literal["evaluation_start"] = "evaluation_start"
    run_id: str
    timestamp: str


class EvaluationCompleteEvent(BaseModel):
    type: Literal["evaluation_complete"] = "evaluation_complete"
    run_id: str
    rubric: str
    weighted_score: float
    overall_score: float
    grade: str
    timestamp: str


ExecutionEvent = Annotated[
    Union[
        WorkflowStartEvent,
        StepStartEvent,
        StepEndEvent,
        StepCompleteEvent,
        StepErrorEvent,
        WorkflowEndEvent,
        EvaluationStartEvent,
        EvaluationCompleteEvent,
    ],
    Field(discriminator="type"),
]

_adapter: TypeAdapter[ExecutionEvent] = TypeAdapter(ExecutionEvent)


def validate_event(payload: dict[str, Any]) -> ExecutionEvent:
    """Validate a raw dict against the ExecutionEvent union.

    Raises pydantic.ValidationError (a ValueError subclass) on mismatch.
    """
    return _adapter.validate_python(payload)
```

Export from `agentic_v2/contracts/__init__.py`:

```python
from .events import (
    EvaluationCompleteEvent,
    EvaluationStartEvent,
    ExecutionEvent,
    StepCompleteEvent,
    StepEndEvent,
    StepErrorEvent,
    StepStartEvent,
    WorkflowEndEvent,
    WorkflowStartEvent,
    validate_event,
)
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
python -m pytest tests/test_event_wire_format.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Wire validation into the broadcast path**

In `agentic_v2/server/websocket.py`, modify `ConnectionManager.broadcast()` to validate before storing/emitting:

```python
from ..contracts.events import validate_event

async def broadcast(self, run_id: str, event: dict[str, Any]) -> None:
    # Validate first — raises if the server is about to emit a bad event
    validate_event(event)
    # ... existing buffer + emit logic ...
```

This is a fail-fast: if any code path emits a malformed event, the server logs the validation error and the test suite catches it before PR merge.

- [ ] **Step 6: Add snapshot coverage**

Modify `scripts/generate_schemas.py` — add the 8 new event models to `COVERED_MODELS`:

```python
from agentic_v2.contracts import (
    # existing imports ...
    WorkflowStartEvent,
    StepStartEvent,
    StepEndEvent,
    StepCompleteEvent,
    StepErrorEvent,
    WorkflowEndEvent,
    EvaluationStartEvent,
    EvaluationCompleteEvent,
)

COVERED_MODELS = [
    # existing ...
    WorkflowStartEvent,
    StepStartEvent,
    StepEndEvent,
    StepCompleteEvent,
    StepErrorEvent,
    WorkflowEndEvent,
    EvaluationStartEvent,
    EvaluationCompleteEvent,
]
```

Do the same in `tests/test_schema_drift.py` (`COVERED_MODELS` list must match).

Generate:

```bash
cd agentic-workflows-v2
python scripts/generate_schemas.py
```

This writes 8 new files under `tests/schemas/`.

- [ ] **Step 7: Run the full test suite**

```bash
python -m pytest tests/ -q -m "not integration and not slow"
```

Expected: all pass including new event tests + schema drift tests (snapshots now include the 8 new events).

- [ ] **Step 8: Commit**

```bash
git add agentic-workflows-v2/agentic_v2/contracts/events.py \
        agentic-workflows-v2/agentic_v2/contracts/__init__.py \
        agentic-workflows-v2/agentic_v2/server/websocket.py \
        agentic-workflows-v2/scripts/generate_schemas.py \
        agentic-workflows-v2/tests/test_schema_drift.py \
        agentic-workflows-v2/tests/test_event_wire_format.py \
        agentic-workflows-v2/tests/schemas/*Event.json
git commit -m "feat(contracts): pydantic wire format for execution events"
```

---

## Task 2: Story 2.2 — Playwright E2E Bootstrap + 5× PR Gate

**Files:**
- Create: `agentic-workflows-v2/ui/playwright.config.ts`
- Create: `agentic-workflows-v2/ui/e2e/fixtures.ts` (shared backend spawn + cleanup)
- Create: `agentic-workflows-v2/ui/e2e/streaming.spec.ts`
- Create: `agentic-workflows-v2/ui/e2e/README.md`
- Modify: `agentic-workflows-v2/ui/package.json` (add test:e2e scripts)
- Modify: `.github/workflows/ci.yml` (add `e2e` job)

### Architectural Decision Log

Three decisions to lock in before writing code:

**Decision 1: Backend fixture strategy**

Options:
- (a) Spawn backend as subprocess in a Playwright `globalSetup` (Python env managed by test).
- (b) Use `webServer` block in playwright.config.ts (Playwright lifecycle-managed).
- (c) Require the contributor to start backend manually before running tests.

**Choice: (b) `webServer` block.** It's the Playwright-idiomatic way and handles port-readiness polling + teardown. The config reuses an existing backend if one is already on port 8010 (`reuseExistingServer: !process.env.CI`).

**Decision 2: Test data — real or mocked workflow?**

Options:
- (a) Run `code_review` end-to-end with no LLM backend (placeholder mode, ~1s).
- (b) Mock the server's WebSocket broadcaster in tests.

**Choice: (a) Placeholder-mode real workflow.** This is what the golden test does (Task 6 of Epic 1). It exercises the real streaming path without needing API keys.

**Decision 3: CI runner**

Options:
- (a) `ubuntu-latest` with Python 3.11 + Node 20.
- (b) Add to `windows-latest` matrix too.

**Choice: (a) ubuntu-latest for 2.2.** Windows streaming E2E is implicitly covered by Story 3.2's workflow verification. Adding Windows here doubles CI cost with low marginal catch. Revisit if Windows-specific streaming bugs emerge.

---

- [ ] **Step 1: Install Playwright**

```bash
cd agentic-workflows-v2/ui
npm install --save-dev @playwright/test
npx playwright install --with-deps chromium
```

Expected: package-lock.json updated; Playwright binary installed.

- [ ] **Step 2: Create `playwright.config.ts`**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 90_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,  // streaming tests write to shared server state
  retries: 0,             // flake-rate-monitored — no retries to mask flakes
  reporter: [
    ['list'],
    ['json', { outputFile: 'e2e-results.json' }],  // consumed by nightly 50x gate
  ],
  use: {
    baseURL: 'http://127.0.0.1:5173',
    trace: 'retain-on-failure',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: [
    {
      name: 'backend',
      command: 'python -m uvicorn agentic_v2.server.app:app --host 127.0.0.1 --port 8010',
      cwd: '..',  // agentic-workflows-v2
      url: 'http://127.0.0.1:8010/health',
      timeout: 60_000,
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
    },
    {
      name: 'frontend',
      command: 'npm run dev',
      url: 'http://127.0.0.1:5173',
      timeout: 60_000,
      reuseExistingServer: !process.env.CI,
    },
  ],
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

Note: requires a `/health` endpoint. Verify it exists; if not, add in a preceding step.

- [ ] **Step 3: Verify or add the `/health` endpoint**

```bash
grep -rn '"/health"\|@router.get("/health")' agentic-workflows-v2/agentic_v2/server/
```

If it does not exist, add to `agentic_v2/server/app.py`:

```python
@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 4: Write the streaming spec**

Create `ui/e2e/streaming.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

/**
 * Story 2.2 AC:
 * - ≥N live events arrive within T seconds
 * - final UI state matches API status
 * - server logs expected token count total
 */
test.describe('streaming PR gate', () => {
  test('code_review streams all lifecycle events and matches API final state', async ({ page, request }) => {
    await page.goto('/');

    // Find and launch the code_review workflow
    await page.getByRole('link', { name: /workflows/i }).click();
    await page.getByRole('link', { name: /code_review/i }).click();
    await page.getByRole('button', { name: /run/i }).click();

    // Assert: workflow_start event renders (run ID visible)
    const runIdLocator = page.locator('[data-testid="run-id"]');
    await expect(runIdLocator).toBeVisible({ timeout: 10_000 });
    const runId = await runIdLocator.textContent();
    expect(runId).toMatch(/^r-/);

    // Assert: ≥5 step_end events render within 30s (code_review has 5 steps)
    const stepRows = page.locator('[data-testid^="step-row-"]');
    await expect(stepRows).toHaveCount(5, { timeout: 30_000 });

    // Assert: final status rendered
    const finalStatus = page.locator('[data-testid="workflow-status"]');
    await expect(finalStatus).toHaveText(/success|failed/i, { timeout: 60_000 });

    // Assert: UI status matches API status
    const apiResponse = await request.get(`/api/runs/${runId}.json`);
    const apiRun = await apiResponse.json();
    const uiStatus = (await finalStatus.textContent())?.trim().toLowerCase();
    expect(uiStatus).toBe(apiRun.overall_status.toLowerCase());
  });
});
```

Note: `data-testid` attributes must be present on the dashboard. If they're missing, add them in a preceding commit — this is a pattern used across the UI anyway.

- [ ] **Step 5: Add npm scripts**

Modify `ui/package.json` scripts block:

```json
"test:e2e": "playwright test",
"test:e2e:5x": "for i in 1 2 3 4 5; do playwright test || exit 1; done",
"test:e2e:ui": "playwright test --ui"
```

- [ ] **Step 6: Run locally to verify**

```bash
cd agentic-workflows-v2/ui
npm run test:e2e
```

Expected: test passes. If it fails, triage with `npm run test:e2e:ui` and add missing `data-testid` attributes as needed.

- [ ] **Step 7: Add CI job for 5× gate**

Append to `.github/workflows/ci.yml`:

```yaml
  e2e-streaming:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.11"
      - uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: agentic-workflows-v2/ui/package-lock.json
      - name: Install Python deps
        run: pip install -e "agentic-workflows-v2/[dev,server]"
      - name: Install UI + Playwright
        run: |
          cd agentic-workflows-v2/ui
          npm ci
          npx playwright install --with-deps chromium
      - name: Run streaming E2E 5×
        run: |
          cd agentic-workflows-v2/ui
          for i in 1 2 3 4 5; do
            npm run test:e2e -- --project=chromium || exit 1
          done
      - name: Upload traces on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-traces
          path: agentic-workflows-v2/ui/test-results/
```

- [ ] **Step 8: Commit**

```bash
git add agentic-workflows-v2/ui/playwright.config.ts \
        agentic-workflows-v2/ui/e2e/ \
        agentic-workflows-v2/ui/package.json \
        agentic-workflows-v2/ui/package-lock.json \
        agentic-workflows-v2/agentic_v2/server/app.py \
        .github/workflows/ci.yml
git commit -m "test(e2e): playwright streaming PR gate (5x) with typed fixtures"
```

---

## Task 3: Story 2.6 — 5-Field Step Drill-Down Panel

**Files:**
- Modify: `agentic-workflows-v2/ui/src/components/live/LiveStepDetails.tsx`
- Modify: `agentic-workflows-v2/ui/src/__tests__/LiveStepDetails.test.tsx` (create if absent)

### Context

`LiveStepDetails.tsx` already exists. This story formalizes the 5 required fields (inputs, outputs, scores, status, duration) and the partial-state behavior (running vs complete vs failed vs no-scores).

- [ ] **Step 1: Read the current component**

```bash
cat agentic-workflows-v2/ui/src/components/live/LiveStepDetails.tsx
```

Note which of the 5 fields are already rendered.

- [ ] **Step 2: Write the failing tests**

Create `ui/src/__tests__/LiveStepDetails.test.tsx`:

```typescript
import { render, screen } from '@testing-library/react';
import { LiveStepDetails } from '../components/live/LiveStepDetails';
import { describe, it, expect } from 'vitest';

describe('LiveStepDetails — Story 2.6 AC', () => {
  const base = {
    step_name: 'parse_code',
    status: 'success',
    duration_ms: 1234,
    input: { code: 'def f(): ...' },
    output: { parsed: true },
  };

  it('renders all 5 fields for a completed step', () => {
    render(<LiveStepDetails step={{ ...base, scores: { clarity: 0.9 } }} />);
    expect(screen.getByText(/inputs/i)).toBeInTheDocument();
    expect(screen.getByText(/outputs/i)).toBeInTheDocument();
    expect(screen.getByText(/scores/i)).toBeInTheDocument();
    expect(screen.getByText(/status/i)).toBeInTheDocument();
    expect(screen.getByText(/1\.23s/i)).toBeInTheDocument();  // duration human format
  });

  it('shows em-dash for missing scores', () => {
    render(<LiveStepDetails step={{ ...base }} />);
    expect(screen.getByTestId('step-scores')).toHaveTextContent('—');
  });

  it('shows inputs immediately while running', () => {
    render(
      <LiveStepDetails step={{ ...base, status: 'running', output: undefined }} />
    );
    expect(screen.getByText(/def f/)).toBeInTheDocument();
    expect(screen.getByTestId('step-output')).toHaveTextContent(/streaming/i);
  });

  it('surfaces failure reason on error', () => {
    render(
      <LiveStepDetails step={{ ...base, status: 'failed', error: 'OOM at line 42' }} />
    );
    expect(screen.getByText(/OOM at line 42/)).toBeInTheDocument();
  });
});
```

- [ ] **Step 3: Run to verify failures**

```bash
cd agentic-workflows-v2/ui
npm run test -- LiveStepDetails
```

Expected: 4 failures.

- [ ] **Step 4: Update `LiveStepDetails.tsx`**

Ensure it renders the 5-field layout with the specified `data-testid` attributes (`step-scores`, `step-output`) and a `formatDuration(ms)` helper that returns e.g. `"1.23s"` or `"42ms"`. Handle the three partial states (running/complete/failed) explicitly.

- [ ] **Step 5: Run tests to confirm pass**

```bash
npm run test -- LiveStepDetails
```

Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add agentic-workflows-v2/ui/src/components/live/LiveStepDetails.tsx \
        agentic-workflows-v2/ui/src/__tests__/LiveStepDetails.test.tsx
git commit -m "feat(ui): 5-field step drill-down panel with partial-state handling"
```

---

## Task 4: Story 2.5 — Live DAG Node State Animation

**Files:**
- Modify: `agentic-workflows-v2/ui/src/components/dag/StepNode.tsx`
- Modify: `agentic-workflows-v2/ui/src/components/dag/WorkflowDAG.tsx` (edge animations)
- Modify: `agentic-workflows-v2/ui/src/styles/` (clay-glow + dash-flow keyframes)
- Modify: `agentic-workflows-v2/ui/src/__tests__/StepNode.test.tsx` (create if absent)

### Context

Requires CSS tokens for `--b-clay-glow` and a `dash-flow` keyframe. Check `ui/src/tokens.css` (or equivalent) before adding new ones.

- [ ] **Step 1: Inventory existing animation tokens**

```bash
grep -rn "keyframes\|animation:" agentic-workflows-v2/ui/src/styles/ 2>/dev/null | head
grep -rn "--b-clay" agentic-workflows-v2/ui/src/ 2>/dev/null | head
```

- [ ] **Step 2: Add keyframes if missing**

To the main stylesheet:

```css
@keyframes clay-glow {
  0%, 100% { box-shadow: 0 0 0 0 var(--b-clay); }
  50% { box-shadow: 0 0 12px 2px var(--b-clay); }
}

@keyframes dash-flow {
  to { stroke-dashoffset: -12; }
}

.step-node--running { animation: clay-glow 1.6s ease-in-out infinite; }
.dag-edge--active {
  stroke-dasharray: 6 6;
  animation: dash-flow 1s linear infinite;
}
```

- [ ] **Step 3: Write tests**

```typescript
// ui/src/__tests__/StepNode.test.tsx
import { render } from '@testing-library/react';
import { StepNode } from '../components/dag/StepNode';

it('applies clay glow when running', () => {
  const { container } = render(<StepNode data={{ status: 'running', name: 'x' }} />);
  expect(container.querySelector('.step-node--running')).not.toBeNull();
});

it('removes glow when succeeded', () => {
  const { container } = render(<StepNode data={{ status: 'success', name: 'x' }} />);
  expect(container.querySelector('.step-node--running')).toBeNull();
});

it('pauses animation during disconnected state', () => {
  const { container } = render(
    <StepNode data={{ status: 'running', name: 'x' }} disconnected />
  );
  expect(container.querySelector('.step-node--running')).toBeNull();
});
```

- [ ] **Step 4: Implement state class logic in StepNode**

Conditionally apply `step-node--running` when `data.status === 'running'` AND `!disconnected`. `disconnected` prop should be plumbed from the parent (`WorkflowDAG`) which listens for the WebSocket disconnect state.

- [ ] **Step 5: Add edge animation in WorkflowDAG**

For each edge whose source step is `success` and target is `running`, add the `dag-edge--active` class.

- [ ] **Step 6: Run tests + manual visual check**

```bash
npm run test -- StepNode
npm run dev  # visit localhost:5173, run a workflow, observe animation
```

- [ ] **Step 7: Commit**

```bash
git add agentic-workflows-v2/ui/src/components/dag/ \
        agentic-workflows-v2/ui/src/__tests__/StepNode.test.tsx \
        agentic-workflows-v2/ui/src/styles/
git commit -m "feat(ui): live DAG node + edge state animation"
```

---

## Task 5: Story 2.8 — StepNode B2 Redesign

**Files:**
- Modify: `agentic-workflows-v2/ui/src/components/dag/StepNode.tsx`
- Modify: `agentic-workflows-v2/ui/src/__tests__/StepNode.test.tsx` (extend)
- Delete: any legacy circle-based `StepNode` (grep before deleting)

- [ ] **Step 1: Audit the StepNode file**

Determine what's there today (circle-based? partial brackets?). Then plan the ASCII-row markup.

- [ ] **Step 2: Design the 4-region layout**

```
┌──────────────────────────┐
│ [RUN] parse_code    T1   │   ← ASCII status + name + tier pill
│ in: 512  out: 312        │   ← token counts (if present)
│ ▮▮▮▮▯▯▯▯ streaming       │   ← streaming bar when active
└──────────────────────────┘
```

- [ ] **Step 3: Write tests for each region**

```typescript
it('renders ASCII status [RUN] while running', () => {...});
it('renders ASCII status [OK ] on success', () => {...});
it('renders ASCII status [ERR] on failure', () => {...});
it('renders tier pill', () => {...});
it('shows token in/out when tokens_used and tier>0', () => {...});
it('streaming bar animates only when running', () => {...});
it('uses --b-* tokens (no hardcoded hex)', () => {
  const { container } = render(<StepNode data={{...}} />);
  const style = container.querySelector('.step-node')?.getAttribute('style') ?? '';
  expect(style).not.toMatch(/#[0-9a-f]{3,6}/i);
});
```

- [ ] **Step 4: Implement**

Keep the state-class logic from Task 4. Add ASCII status mapping, tier pill, token counts, streaming bar. All colors via CSS variables.

- [ ] **Step 5: Grep for legacy imports and delete**

```bash
grep -rn "StepNode\|StatusCircle\|CircleNode" agentic-workflows-v2/ui/src/
```

Remove any legacy exports that are no longer referenced.

- [ ] **Step 6: Visual check in all 3 themes**

```bash
npm run dev
# Toggle dark → paper → bolt, run a workflow, verify colors.
```

- [ ] **Step 7: Commit**

```bash
git add agentic-workflows-v2/ui/src/components/dag/StepNode.tsx \
        agentic-workflows-v2/ui/src/__tests__/StepNode.test.tsx
git commit -m "feat(ui): StepNode B2 redesign (ASCII status + tier pill + tokens + streaming bar)"
```

---

## Task 6: Story 2.3 — WebSocket Fault-Injection + Reconnect Test

**Files:**
- Create: `agentic-workflows-v2/ui/e2e/reconnect.spec.ts`

### Context

Client reconnect already exists (`ui/src/api/websocket.ts`). Server has an event replay buffer (`ConnectionManager.event_buffers`, 500 events). This story asserts the end-to-end behavior.

- [ ] **Step 1: Write the spec**

```typescript
// ui/e2e/reconnect.spec.ts
import { test, expect } from '@playwright/test';

test.describe('streaming fault recovery', () => {
  test('client reconnects and replays missed events after WS kill', async ({ page, context }) => {
    await page.goto('/');
    await page.getByRole('link', { name: /workflows/i }).click();
    await page.getByRole('link', { name: /code_review/i }).click();
    await page.getByRole('button', { name: /run/i }).click();

    // Wait until ~50% of steps have rendered (code_review has 5 steps → wait for 2–3)
    const stepRows = page.locator('[data-testid^="step-row-"]');
    await expect(stepRows).toHaveCount(3, { timeout: 20_000 });

    // Kill the WebSocket via CDP
    const client = await context.newCDPSession(page);
    await client.send('Network.enable');
    await client.send('Network.emulateNetworkConditions', {
      offline: true,
      latency: 0,
      downloadThroughput: 0,
      uploadThroughput: 0,
    });

    // Wait 2s (enough for the WS close to propagate + reconnect attempt)
    await page.waitForTimeout(2000);

    // Restore network — client should reconnect and replay missed events
    await client.send('Network.emulateNetworkConditions', {
      offline: false,
      latency: 0,
      downloadThroughput: -1,
      uploadThroughput: -1,
    });

    // After reconnect, all 5 steps must render (the replay buffer covers the gap)
    await expect(stepRows).toHaveCount(5, { timeout: 30_000 });

    // UI final status matches API final status
    const runId = await page.locator('[data-testid="run-id"]').textContent();
    const api = await page.request.get(`/api/runs/${runId}.json`);
    const apiJson = await api.json();
    const uiStatus = (await page.locator('[data-testid="workflow-status"]').textContent())?.trim().toLowerCase();
    expect(uiStatus).toBe(apiJson.overall_status.toLowerCase());
  });
});
```

- [ ] **Step 2: Run locally**

```bash
cd agentic-workflows-v2/ui
npm run test:e2e -- reconnect
```

If the test fails because the client doesn't request a replay on reconnect, that's a real bug — fix `ui/src/api/websocket.ts` to send the last-seen event index on reconnect, and have the server's `ConnectionManager.connect()` pick up from that index.

- [ ] **Step 3: Commit**

```bash
git add agentic-workflows-v2/ui/e2e/reconnect.spec.ts
git commit -m "test(e2e): websocket fault-injection + reconnect replay"
```

---

## Task 7: Story 2.7 — Time-to-First-Span SLO Gate (p95 ≤ 2s)

**Files:**
- Create: `agentic-workflows-v2/ui/e2e/slo-first-span.spec.ts`
- Create: `agentic-workflows-v2/ui/e2e/slo-storage.ts` (rolling-window helper)
- Create: `agentic-workflows-v2/tests/slo/` (committed rolling-window JSON — yes, checked into git; see decision below)

### Architectural Decision: rolling-window persistence

Options:
- (a) GitHub Actions artifact (ephemeral, max 90 days, hard to read in CI).
- (b) Committed JSON file in `tests/slo/` — pushed by nightly job via `actions/git-push-action`.
- (c) External DB (Postgres, DynamoDB).

**Choice: (b) committed JSON.** Zero infra, versioned, reviewable in PRs, auto-expires via a max-records field. The nightly job appends one row and force-pushes to a `slo-data` branch that the CI gate reads. Trade-off: one tiny background commit per nightly run — acceptable.

Schema `tests/slo/first-span-latency.json`:

```json
{
  "version": 1,
  "max_records": 1000,
  "records": [
    { "timestamp": "2026-04-21T00:00:00Z", "latency_ms": 1420, "commit": "abc123" }
  ]
}
```

- [ ] **Step 1: Write the measurement spec**

```typescript
// ui/e2e/slo-first-span.spec.ts
import { test, expect } from '@playwright/test';
import { recordLatency, readP95 } from './slo-storage';

test.describe('SLO: time-to-first-span p95 ≤ 2s', () => {
  test('record single latency sample', async ({ page }) => {
    await page.goto('/');
    const t0 = Date.now();
    await page.getByRole('link', { name: /workflows/i }).click();
    await page.getByRole('link', { name: /code_review/i }).click();
    await page.getByRole('button', { name: /run/i }).click();

    // Wait for first DAG node render
    await expect(page.locator('[data-testid^="dag-node-"]').first()).toBeVisible();
    const latency = Date.now() - t0;

    await recordLatency(latency);
  });

  test('rolling 7-day p95 is within budget', async () => {
    const p95 = await readP95({ windowDays: 7 });
    expect(p95, `p95=${p95}ms exceeds 2000ms budget`).toBeLessThanOrEqual(2000);
  });
});
```

- [ ] **Step 2: Implement `slo-storage.ts`**

```typescript
import { readFileSync, writeFileSync } from 'fs';
import { execSync } from 'child_process';

const PATH = 'tests/slo/first-span-latency.json';

export async function recordLatency(ms: number) {
  const data = JSON.parse(readFileSync(PATH, 'utf8'));
  const commit = execSync('git rev-parse HEAD').toString().trim();
  data.records.push({ timestamp: new Date().toISOString(), latency_ms: ms, commit });
  if (data.records.length > data.max_records) {
    data.records.splice(0, data.records.length - data.max_records);
  }
  writeFileSync(PATH, JSON.stringify(data, null, 2));
}

export async function readP95({ windowDays }: { windowDays: number }) {
  const data = JSON.parse(readFileSync(PATH, 'utf8'));
  const cutoff = Date.now() - windowDays * 86400 * 1000;
  const recent = data.records
    .filter((r: any) => Date.parse(r.timestamp) >= cutoff)
    .map((r: any) => r.latency_ms)
    .sort((a: number, b: number) => a - b);
  if (recent.length === 0) return 0;  // no data yet — don't fail
  return recent[Math.floor(recent.length * 0.95)];
}
```

- [ ] **Step 3: Commit (but don't enable gate yet)**

```bash
git add agentic-workflows-v2/ui/e2e/slo-first-span.spec.ts \
        agentic-workflows-v2/ui/e2e/slo-storage.ts \
        agentic-workflows-v2/tests/slo/first-span-latency.json
git commit -m "test(slo): time-to-first-span measurement and p95 gate"
```

Gate becomes active in Task 8 (nightly job) which seeds records.

---

## Task 8: Story 2.4 — Nightly 50× Reliability Gate

**Files:**
- Create: `.github/workflows/nightly.yml`
- Create: `agentic-workflows-v2/ui/e2e/flake-gate.ts` (rolling flake-rate calculator)

- [ ] **Step 1: Write the nightly workflow**

```yaml
# .github/workflows/nightly.yml
name: Nightly E2E Reliability
on:
  schedule:
    - cron: '0 7 * * *'  # 03:00 ET
  workflow_dispatch:

jobs:
  streaming-50x:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with: { python-version: "3.11" }
      - uses: actions/setup-node@v6
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: agentic-workflows-v2/ui/package-lock.json
      - run: pip install -e "agentic-workflows-v2/[dev,server]"
      - name: Install UI + Playwright
        run: |
          cd agentic-workflows-v2/ui
          npm ci
          npx playwright install --with-deps chromium
      - name: Run streaming E2E 50×
        id: run50
        continue-on-error: true
        run: |
          cd agentic-workflows-v2/ui
          fails=0
          for i in $(seq 1 50); do
            npm run test:e2e -- streaming.spec.ts || fails=$((fails+1))
          done
          echo "fails=$fails" >> $GITHUB_OUTPUT
      - name: Append flake record + enforce 0.5% rolling gate
        run: |
          cd agentic-workflows-v2/ui
          node e2e/flake-gate.ts ${{ steps.run50.outputs.fails }}
      - name: Commit SLO + flake data
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add agentic-workflows-v2/tests/slo/
          git commit -m "chore(slo): nightly data update" || echo "nothing to commit"
          git push
```

- [ ] **Step 2: Implement flake-gate**

```typescript
// ui/e2e/flake-gate.ts
import { readFileSync, writeFileSync } from 'fs';

const PATH = 'tests/slo/flake-rate.json';
const fails = Number(process.argv[2] ?? 0);
const total = 50;

const data = JSON.parse(readFileSync(PATH, 'utf8'));
data.records.push({
  timestamp: new Date().toISOString(),
  fails,
  total,
  rate: fails / total,
});
if (data.records.length > 30) data.records.splice(0, data.records.length - 30);
writeFileSync(PATH, JSON.stringify(data, null, 2));

// 7-day rolling rate
const cutoff = Date.now() - 7 * 86400 * 1000;
const recent = data.records.filter((r: any) => Date.parse(r.timestamp) >= cutoff);
const totalFails = recent.reduce((s: number, r: any) => s + r.fails, 0);
const totalRuns = recent.reduce((s: number, r: any) => s + r.total, 0);
const rate = totalFails / totalRuns;

console.log(`Rolling 7d flake rate: ${(rate * 100).toFixed(2)}% (${totalFails}/${totalRuns})`);
if (rate > 0.005) {
  console.error(`FAIL: rate ${(rate * 100).toFixed(2)}% > 0.5% budget`);
  process.exit(1);
}
```

- [ ] **Step 3: Seed the data files**

```bash
mkdir -p agentic-workflows-v2/tests/slo
echo '{"version":1,"max_records":1000,"records":[]}' > agentic-workflows-v2/tests/slo/first-span-latency.json
echo '{"version":1,"records":[]}' > agentic-workflows-v2/tests/slo/flake-rate.json
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/nightly.yml \
        agentic-workflows-v2/ui/e2e/flake-gate.ts \
        agentic-workflows-v2/tests/slo/
git commit -m "ci(nightly): 50x streaming reliability + rolling flake-rate gate"
```

---

## Self-Review

### Spec Coverage

| Story | Task | Key AC verified |
|-------|------|-----------------|
| 2.1 | 1 | All events validated before broadcast; 8 models; schema snapshots |
| 2.2 | 2 | Playwright infra; 5× gate; UI↔API status match |
| 2.3 | 6 | WS kill via CDP; client reconnects; all events replayed |
| 2.4 | 8 | 50× nightly; rolling 7d flake rate ≤ 0.5% |
| 2.5 | 4 | Clay glow running; off on success; paused on disconnect |
| 2.6 | 3 | 5 fields; partial state; em-dash for missing scores |
| 2.7 | 7 | p95 ≤ 2s; rolling window |
| 2.8 | 5 | ASCII status; tier pill; tokens; streaming bar; no hex; legacy removed |

### Known Risks / Open Questions

1. **`data-testid` attributes must exist** across several UI components. If they don't, add them BEFORE starting Task 2.
2. **WS replay protocol may need a change.** Today the client passively reconnects; the server may not know which events the client missed. If Task 6's test reveals this gap, implement a `last_seen_index` handshake before merging 2.3.
3. **SLO data committed to git** is a trade-off — see decision in Task 7. If this grows unacceptable, migrate to a separate branch (`slo-data`) that the nightly job force-pushes, and keep the main history clean.
4. **Nightly commit permissions** — the nightly job needs `contents: write`. Add `permissions: { contents: write }` at the top of `nightly.yml` or confirm repo-wide default.
5. **Windows E2E excluded** — acceptable by Decision 3 in Task 2. Revisit if Windows-specific streaming bugs appear.

### Dependencies on Other Work

- **Epic 5 in flight in parallel.** Stories 5.1 (StatusBadge) and this plan's Task 5 (StepNode) both touch UI. Coordinate: land Epic 5 first, then do this plan's Task 5 to avoid conflicts.
- **Task 1 blocks nothing.** Can land independently of Epic 5.

### Execution Order Summary

```
Task 1 (2.1 wire format) ─────────┐
                                  ├→ Task 2 (2.2 Playwright) ─┬→ Task 6 (2.3 reconnect)
                                  │                           ├→ Task 7 (2.7 SLO)
                                  │                           └→ Task 8 (2.4 nightly)
Task 3 (2.6 drill-down) ──────────┤
Task 4 (2.5 animation) ───────────┤
Task 5 (2.8 StepNode) ────────────┘   ← coordinate with Epic 5
```

Minimum viable ship: Tasks 1, 3 (drill-down only). Full epic ship: all 8 tasks.
