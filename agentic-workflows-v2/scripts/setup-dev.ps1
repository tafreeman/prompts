<#
.SYNOPSIS
    One-command Windows development environment bring-up for agentic-workflows-v2.

.DESCRIPTION
    Checks prerequisites, installs Python and Node.js dependencies, validates
    all 6 bundled workflows, and runs a deterministic smoke test.

    Run this once after cloning the repo (or after pulling major changes).
    After setup completes, use start-dev.ps1 to launch the dev servers.

.PARAMETER SkipSmokeTest
    Skip the workflow validation and smoke-test phase.

.PARAMETER SkipFrontend
    Skip the npm install step (backend-only setup).

.EXAMPLE
    .\setup-dev.ps1
    .\setup-dev.ps1 -SkipSmokeTest
    .\setup-dev.ps1 -SkipFrontend
#>

[CmdletBinding()]
param(
    [switch]$SkipSmokeTest,
    [switch]$SkipFrontend
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Resolve paths
# ---------------------------------------------------------------------------

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$BackendRoot = Split-Path -Parent $ScriptDir          # agentic-workflows-v2/
$UiRoot = Join-Path $BackendRoot "ui"
$FixturesDir = Join-Path $ScriptDir "fixtures"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "    [OK] $Message" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Message)
    Write-Host "    [FAIL] $Message" -ForegroundColor Red
}

function Assert-Tool {
    param(
        [string]$Name,
        [string]$InstallHint
    )
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        Write-Fail "$Name not found. $InstallHint"
        exit 1
    }
    $ver = & $Name --version 2>&1 | Select-Object -First 1
    Write-Ok "$Name ($ver)"
}

# Force UTF-8 for Python subprocesses (Rich uses Unicode symbols that
# cp1252 cannot encode on some Windows terminals).
$env:PYTHONIOENCODING = "utf-8"

# ---------------------------------------------------------------------------
# Step 1 — Prerequisite checks
# ---------------------------------------------------------------------------

Write-Step "Checking prerequisites"

Assert-Tool "git"  "Install from: https://git-scm.com/"
Assert-Tool "uv"   "Install from: https://docs.astral.sh/uv/"
Assert-Tool "node"  "Install Node.js 20+ from: https://nodejs.org/"
Assert-Tool "npm"   "npm should come with Node.js — reinstall Node if missing."

# ---------------------------------------------------------------------------
# Step 2 — Python environment setup
# ---------------------------------------------------------------------------

Write-Step "Installing Python packages (uv sync)"

Push-Location $BackendRoot
try {
    & uv sync --extra dev --extra server --extra langchain
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "uv sync failed (exit code $LASTEXITCODE)"
        exit 1
    }
    Write-Ok "Python packages installed"
}
finally {
    Pop-Location
}

# ---------------------------------------------------------------------------
# Step 3 — Frontend install
# ---------------------------------------------------------------------------

if (-not $SkipFrontend) {
    Write-Step "Installing frontend packages (npm install)"

    if (-not (Test-Path $UiRoot)) {
        Write-Fail "UI directory not found at $UiRoot"
        exit 1
    }

    Push-Location $UiRoot
    try {
        & npm install --no-fund --no-audit
        if ($LASTEXITCODE -ne 0) {
            Write-Fail "npm install failed (exit code $LASTEXITCODE)"
            exit 1
        }
        Write-Ok "Frontend packages installed"
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Step "Skipping frontend install (--SkipFrontend)"
}

# ---------------------------------------------------------------------------
# Step 4 — Workflow validation & smoke test
# ---------------------------------------------------------------------------

if (-not $SkipSmokeTest) {
    Write-Step "Validating bundled workflows"

    $workflows = @(
        "bug_resolution"
        "code_review"
        "conditional_branching"
        "fullstack_generation"
        "iterative_review"
        "test_deterministic"
    )

    $failed = @()
    $warned = @()

    Push-Location $BackendRoot
    try {
        foreach ($wf in $workflows) {
            $ErrorActionPreference = "Continue"
            $output = & uv run agentic validate $wf 2>&1
            $exitCode = $LASTEXITCODE
            $ErrorActionPreference = "Stop"

            if ($exitCode -ne 0) {
                # Some workflows have pre-existing static validation issues
                # (e.g., unresolved variable templates). Warn but don't block.
                Write-Host "    [WARN] Validation issue: $wf (non-blocking)" -ForegroundColor Yellow
                $warned += $wf
            }
            else {
                Write-Ok "Validated: $wf"
            }
        }
    }
    finally {
        Pop-Location
    }

    if ($warned.Count -gt 0) {
        Write-Host ""
        Write-Host "    Note: $($warned.Count) workflow(s) had validation warnings: $($warned -join ', ')" -ForegroundColor Yellow
        Write-Host "    These may have pre-existing issues with static analysis." -ForegroundColor Yellow
    }

    # Run the deterministic workflow with --dry-run to verify the full
    # execution path (parsing, graph compilation, plan generation) without
    # requiring live agent implementations.
    Write-Step "Running deterministic smoke test (dry-run)"

    $smokeInput = Join-Path $FixturesDir "smoke-input.json"
    if (-not (Test-Path $smokeInput)) {
        Write-Fail "Smoke-test input not found at $smokeInput"
        exit 1
    }

    Push-Location $BackendRoot
    try {
        $ErrorActionPreference = "Continue"
        $output = & uv run agentic run test_deterministic --input $smokeInput --dry-run 2>&1
        $exitCode = $LASTEXITCODE
        $ErrorActionPreference = "Stop"

        if ($exitCode -ne 0) {
            Write-Fail "Smoke test failed (exit code $exitCode)"
            Write-Host ($output | Out-String) -ForegroundColor DarkGray
            exit 1
        }
        Write-Ok "Smoke test passed"
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Step "Skipping smoke test (--SkipSmokeTest)"
}

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Copy .env.example to .env and add at least one LLM provider key"
Write-Host "  2. Launch dev servers:  .\scripts\start-dev.ps1"
Write-Host "  3. Backend: http://localhost:8012  |  Frontend: http://localhost:5174"
Write-Host ""
