# Retro — Epic 3: DevEx / Windows

> **Status:** COMPLETED 2026-04-22. This is a retrospective plan doc — Epic 3 shipped without a prospective plan. Written after the fact to preserve decision history.
> **Audience:** Anyone returning to this work or proposing similar DevEx initiatives.
> **Last verified:** 2026-04-22

---

## Goal

Make a fresh Windows clone a first-class developer experience. Eliminate the recurring friction points that were costing contributors 30+ minutes per bring-up attempt: unclear install sequencing, cryptic port-conflict errors, test-runner ambiguity across packages, unvalidated workflow YAML, and Unicode crashes in the CLI on the default codepage.

---

## Stories (shipped)

### 3.1 — Windows bring-up hardening
- **Commits:** `scripts/setup-dev.ps1` hardened iteratively through the epic window; CI validation added in `windows-workflows-ci.yml`.
- **Outcome:** A fresh Windows clone runs `.\scripts\setup-dev.ps1` and lands in a state where `agentic list workflows` succeeds. CI validates this on every PR against the Windows runner.

### 3.2 — `port-guard` devex tool
- **Commit chain:** `1fd7fe0 feat(devex): add workspace-test-runner and workflow-linter tools (stories 3-4, 3-5)` — port-guard shipped earlier in the chain.
- **Outcome:** Running the dev server surfaces "port 8010 held by process X" as an actionable message instead of a cryptic OS bind error. Checks 8010 (backend), 5173 (frontend), 6006 (Storybook).

### 3.3 — `workspace-test-runner`
- **Commit:** `1fd7fe0 feat(devex): add workspace-test-runner and workflow-linter tools (stories 3-4, 3-5)`
- **Outcome:** One command (`just test` at the root) runs the right suite for whichever package the contributor is in. No more "did I run pytest for the right package?"

### 3.4 — `workflow-linter`
- **Commit:** same as 3.3 (`1fd7fe0`).
- **Outcome:** YAML workflow definitions are validated against the required-fields contract (`name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`) before they reach the runtime. Catches malformed workflows at author time, not at run time.

### 3.5 — Windows Unicode CLI fix
- **Commit:** `8117b5c fix(cli): fix Windows Unicode crashes and add CLI verification to CI (story 3-6)`
- **Outcome:** The `agentic` CLI no longer crashes on the Windows default codepage when a workflow output contains non-ASCII. CI verification prevents regression.

---

## Lessons

### What worked

- **Ship as one bundled PR sequence.** Each story was a small, focused commit. Because they all sat under the same "DevEx" umbrella, the reviewer could keep context across them; no need for long PR descriptions re-establishing the problem.
- **Windows CI as the ratchet.** Adding `windows-workflows-ci.yml` as a required check meant a regression in Windows bring-up would surface within minutes. Prior to Epic 3, Windows friction was discovered by contributors at bring-up time — a vastly worse feedback loop.
- **Actionable errors over recovery.** `port-guard` does not close the conflicting process; it tells the contributor which process to close. That is the right level of automation — it leaves the human in charge of the destructive action.

### What would have been better with a plan

- **Scope creep on `setup-dev.ps1`.** The script grew opportunistic features (workflow smoke test, dependency audit) across the epic. Each addition was fine in isolation; collectively they made the script harder to reason about. A prospective plan would have bounded this.
- **`workspace-test-runner` contract was under-specified.** The tool shipped with implicit behavior about *which* tests it runs in each package — that behavior is now load-bearing but undocumented. A future contributor will have to read the source to understand the dispatch table.
- **Documentation lagged the code.** ONBOARDING.md and CONTRIBUTING.md did not gain pointers to the new tools until this docs sprint (2026-04-22). The tools were effectively invisible to anyone not reading CHANGELOG.

### Process notes for future DevEx epics

1. Write a one-page plan before the first commit — even for "small" epics. The epic gained four new tools; treating that as small in hindsight understates the onboarding surface created.
2. Pair every new tool with a line in `docs/ONBOARDING.md` in the same PR. A tool that is not documented on the onboarding path does not exist.
3. Windows-first acceptance criteria. The "CI validates on Windows runner" gate was the single most valuable output of this epic — prioritize it early in future efforts.

---

## Links

- CHANGELOG: [`../../../CHANGELOG.md`](../../../CHANGELOG.md) — Epic 3 entries under `[0.3.0]`.
- Setup script: [`../../../agentic-workflows-v2/scripts/setup-dev.ps1`](../../../agentic-workflows-v2/scripts/setup-dev.ps1)
- CI gate: [`../../../.github/workflows/windows-workflows-ci.yml`](../../../.github/workflows/windows-workflows-ci.yml)
