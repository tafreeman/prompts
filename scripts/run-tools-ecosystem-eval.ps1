<#
Runs the Tools Ecosystem Evaluator runner.

Usage (from Explorer):
  - Double-click: ..\Run-Tools-Ecosystem-Eval.cmd

Usage (from PowerShell):
  .\scripts\run-tools-ecosystem-eval.ps1
  .\scripts\run-tools-ecosystem-eval.ps1 -Model "gh:gpt-4o-mini" -TreeDepth 5 -MaxRounds 6
  .\scripts\run-tools-ecosystem-eval.ps1 -Parallel -Models @("gh:gpt-4o-mini","local:phi4mini")
  .\scripts\run-tools-ecosystem-eval.ps1 -Lite  # Use compact prompt for local models

Notes:
  - Reports are written under .\results\
  - JSONL logs are written under .\logs\
  - For cloud models, ensure auth is configured (e.g. GitHub Models via gh auth or GITHUB_TOKEN).
  - Use -Lite for local models with small context windows (phi4, mistral, etc.)
#>

[CmdletBinding()]
param(
    [string]$Model = "gh:gpt-4o-mini",
    [int]$TreeDepth = 4,
    [int]$MaxRounds = 6,
    [string]$Focus = $null,
    [string]$Compare = $null,
    [string]$Prior = $null,

    # Use the lite prompt (compact version for local models with small context windows)
    [switch]$Lite,

    # Run multiple models concurrently (separate report/log files per model)
    [switch]$Parallel,
    [string[]]$Models = @(),

    # After parallel runs, merge the per-model reports into one consolidated MVP report.
    [switch]$Merge,
    [string]$MergeModel = "gh:openai/gpt-4o-mini",

    # When running in parallel, also capture stdout/stderr to files under .\logs\
    [switch]$CaptureConsoleOutput
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    # This script lives in <repo>\scripts\
    return (Resolve-Path (Join-Path $PSScriptRoot ".."))
}

function Get-PythonExe([string]$RepoRoot) {
    $venvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path $venvPy) {
        return $venvPy
    }
    return "python"
}

function Slugify([string]$Text) {
    if ([string]::IsNullOrWhiteSpace($Text)) { return "model" }
    $s = $Text.ToLowerInvariant()
    $s = $s -replace "[^a-z0-9]+", "-"
    $s = $s.Trim("-")
    if ([string]::IsNullOrWhiteSpace($s)) { return "model" }
    return $s
}

$repoRoot = Get-RepoRoot
Set-Location $repoRoot

$python = Get-PythonExe -RepoRoot $repoRoot

$timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")

$resultsDir = Join-Path $repoRoot "results"
$logsDir = Join-Path $repoRoot "logs"
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null
New-Item -ItemType Directory -Force -Path $logsDir | Out-Null

# Decide which models to run
$runModels = @()
if ($Parallel) {
    if ($Models -and $Models.Count -gt 0) {
        $runModels = $Models
    } else {
        # Default: cloud-only models (local models need too much RAM)
        $runModels = @(
            "gh:openai/gpt-4o-mini",
            "gh:openai/gpt-4.1-mini",
            "gh:microsoft/phi-4-mini-instruct"
        )
    }
} else {
    $runModels = @($Model)
}

Write-Host "Repo root: $repoRoot"
Write-Host "Python:    $python"
Write-Host "Models:    $($runModels -join ', ')"
Write-Host "Parallel:  $Parallel"
Write-Host "Lite:      $Lite"
Write-Host ""

function Build-Args([string]$m, [string]$outPath, [string]$logJsonlPath) {
    $args = @(
        "prompt.py",
        "tools-eval",
        "--model", $m,
        "--tree-depth", $TreeDepth,
        "--max-rounds", $MaxRounds,
        "--out", $outPath,
        "--log-jsonl", $logJsonlPath
    )

    if ($Lite) { $args += "--lite" }
    if ($Focus) { $args += @("--focus", $Focus) }
    if ($Compare) { $args += @("--compare", $Compare) }
    if ($Prior) { $args += @("--prior", $Prior) }

    return $args
}

if (-not $Parallel) {
    $slug = Slugify $runModels[0]
    $outPath = Join-Path $resultsDir "tools-ecosystem-eval-$timestamp-$slug.md"
    $logJsonl = Join-Path $logsDir "tools-ecosystem-eval-$timestamp-$slug.jsonl"

    Write-Host "Running single evaluation..." -ForegroundColor Cyan
    Write-Host "  Report: $outPath"
    Write-Host "  Log:    $logJsonl"
    Write-Host ""

    $args = Build-Args -m $runModels[0] -outPath $outPath -logJsonlPath $logJsonl

    & $python @args
    $exit = $LASTEXITCODE

    Write-Host ""
    if ($exit -eq 0) {
        Write-Host "Done. Report written to: $outPath" -ForegroundColor Green
    } else {
        Write-Host "Failed with exit code $exit" -ForegroundColor Red
        Write-Host "See log: $logJsonl"
    }

    exit $exit
}

Write-Host "Launching parallel evaluations..." -ForegroundColor Cyan

$procs = @()
$reportPaths = @()
foreach ($m in $runModels) {
    $slug = Slugify $m
    $outPath = Join-Path $resultsDir "tools-ecosystem-eval-$timestamp-$slug.md"
    $logJsonl = Join-Path $logsDir "tools-ecosystem-eval-$timestamp-$slug.jsonl"

    $reportPaths += $outPath

    $args = Build-Args -m $m -outPath $outPath -logJsonlPath $logJsonl

    Write-Host "  Model:  $m"
    Write-Host "    Report: $outPath"
    Write-Host "    Log:    $logJsonl"

    $startInfo = @{
        FilePath         = $python
        ArgumentList     = $args
        WorkingDirectory = $repoRoot
        PassThru         = $true
    }

    if ($CaptureConsoleOutput) {
        $stdout = Join-Path $logsDir "tools-ecosystem-eval-$timestamp-$slug.stdout.txt"
        $stderr = Join-Path $logsDir "tools-ecosystem-eval-$timestamp-$slug.stderr.txt"
        $startInfo["RedirectStandardOutput"] = $stdout
        $startInfo["RedirectStandardError"] = $stderr
        # Can't use -WindowStyle with -NoNewWindow; in capture mode we run without a new window.
        $startInfo["NoNewWindow"] = $true
    } else {
        # Show child consoles so you can watch progress.
        $startInfo["WindowStyle"] = "Normal"
    }

    $procs += Start-Process @startInfo
}

Write-Host ""
Write-Host "Waiting for $($procs.Count) process(es) to finish..." -ForegroundColor Cyan

$exitCodes = @()
foreach ($p in $procs) {
    try {
        # Waiting by PID can race if the process exits quickly.
        if (-not $p.HasExited) {
            $p.WaitForExit()
        }
    } catch {
        # Ignore wait errors and fall through to exit code handling.
    }

    try {
        $exitCodes += $p.ExitCode
    } catch {
        # If we can't read ExitCode, treat as failure
        $exitCodes += 1
    }
}

Write-Host ""
Write-Host "Parallel run complete." -ForegroundColor Green
Write-Host "Exit codes: $($exitCodes -join ', ')"

if ($Merge) {
    Write-Host "" 
    Write-Host "Merging per-model reports into one MVP report..." -ForegroundColor Cyan

    $existingReports = @($reportPaths | Where-Object { Test-Path $_ })
    if (-not $existingReports -or $existingReports.Count -lt 2) {
        Write-Host "Not enough reports found to merge (need at least 2)." -ForegroundColor Yellow
    } else {
        $mergedOut = Join-Path $resultsDir "tools-ecosystem-eval-$timestamp-merged-mvp.md"
        $mergeLog = Join-Path $logsDir "tools-ecosystem-merge-$timestamp.jsonl"

        Write-Host "  Merge model: $MergeModel"
        Write-Host "  Output:      $mergedOut"
        Write-Host "  Log:         $mergeLog"

        $mergeArgs = @(
            "tools/tools_ecosystem_merge.py",
            "--model", $MergeModel,
            "--out", $mergedOut,
            "--log-jsonl", $mergeLog
        )
        if ($Focus) { $mergeArgs += @("--focus", $Focus) }
        $mergeArgs += $existingReports

        & $python @mergeArgs
        $mergeExit = $LASTEXITCODE

        if ($mergeExit -eq 0) {
            Write-Host "Merged report written to: $mergedOut" -ForegroundColor Green
        } else {
            Write-Host "Merge failed with exit code $mergeExit" -ForegroundColor Red
        }
    }
}

# Return non-zero if any worker failed
if ($exitCodes | Where-Object { $_ -ne 0 }) {
    exit 1
}
exit 0
