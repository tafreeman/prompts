<#
.SYNOPSIS
Run tiered evaluations against the prompt library using free models only.

.DESCRIPTION
This script executes multiple evaluation runs using a mix of:
- Local ONNX models (local:*)
- Ollama models (ollama:*)  
- AI Toolkit models (aitk:*)
- GitHub Models (gh:*) - free tier

.EXAMPLE
./scripts/run-free-tier-evals.ps1

.EXAMPLE
./scripts/run-free-tier-evals.ps1 -Path prompts/analysis -Quick

.EXAMPLE
./scripts/run-free-tier-evals.ps1 -Discovery -MaxPerProvider 5

.EXAMPLE
./scripts/run-free-tier-evals.ps1 -LocalOnly -Tiers 1,2

.NOTES
Requires: Python 3.10+, GITHUB_TOKEN env var for gh:* models
#>

[CmdletBinding()]
param(
    [string]$Path = "prompts/",
    
    [int[]]$Tiers = @(1, 2),
    
    [string[]]$Models,
    
    [switch]$Discovery,
    
    [int]$MaxPerProvider = 3,
    
    [switch]$Quick,
    
    [switch]$LocalOnly,
    
    [switch]$NoGH,
    
    [int]$Parallel = 1,
    
    [switch]$Verbose,
    
    [string]$OutputDir,
    
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$scriptPath = Join-Path $repoRoot "scripts\run_free_tier_evals.py"

if (-not (Test-Path $scriptPath)) {
    Write-Error "Script not found: $scriptPath"
    exit 1
}

# Build arguments
$args = @()

if ($Path) {
    $args += "--path", $Path
}

if ($Tiers.Count -gt 0) {
    $args += "--tiers"
    $args += $Tiers
}

if ($Models.Count -gt 0) {
    $args += "--models"
    $args += $Models
}

if ($Discovery) {
    $args += "--discovery"
}

if ($MaxPerProvider -gt 0) {
    $args += "--max-per-provider", $MaxPerProvider
}

if ($Quick) {
    $args += "--quick"
}

if ($LocalOnly) {
    $args += "--local-only"
}

if ($NoGH) {
    $args += "--no-gh"
}

if ($Parallel -gt 1) {
    $args += "--parallel", $Parallel
}

if ($Verbose) {
    $args += "--verbose"
}

if ($OutputDir) {
    $args += "--output-dir", $OutputDir
}

if ($DryRun) {
    $args += "--dry-run"
}

Write-Host "🚀 Running free tier evaluations..." -ForegroundColor Cyan
Write-Host "   Command: python $scriptPath $($args -join ' ')" -ForegroundColor DarkGray

Push-Location $repoRoot
try {
    & python $scriptPath @args
    $exitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}

exit $exitCode
