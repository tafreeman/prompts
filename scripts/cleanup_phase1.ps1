<#
cleanup_phase1.ps1
Reversible P1 cleanup script (PowerShell)
Usage examples:
  # Dry run (default)
  .\scripts\cleanup_phase1.ps1 -DryRun

  # Apply moves
  .\scripts\cleanup_phase1.ps1 -Apply -DaysOldForResults 90 -DraftMonths 6 -Confirm

  # Undo last run
  .\scripts\cleanup_phase1.ps1 -Undo

What it does (P1 actions):
 - Creates archive folders: archive/legacy, archive/clutter, archive/drafts, archive/outputs
 - Moves `toolkit/prompts/` -> `archive/clutter/toolkit_prompts/` (if exists)
 - Moves `results/` files older than DaysOldForResults to `archive/outputs/`
 - Moves prompt markdown files under `prompts/` that have not been modified in DraftMonths months and contain `reviewStatus: draft` in frontmatter to `archive/drafts/` (dry-run by default)
 - Writes a reversible manifest: .cleanup_manifest.json

Caution: Review dry-run output before running with -Apply. This script moves files locally; commit changes after review.
#>
param(
    [switch]$DryRun = $true,
    [switch]$Apply,
    [switch]$Undo,
    [int]$DaysOldForResults = 90,
    [int]$DraftMonths = 6,
    [switch]$Confirm
)

## Compute repository root (parent of the scripts/ folder). This makes the script work
## whether invoked from the repo root or from the scripts directory.
$RepoRoot = Resolve-Path (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '..') | Select-Object -ExpandProperty Path
Set-Location $RepoRoot

$manifestPath = Join-Path $RepoRoot ".cleanup_manifest.json"
$ops = @()

function Ensure-Dir { param($p) if (-not (Test-Path $p)) { if ($DryRun) { Write-Host "[DRY] Would create: $p" } else { New-Item -ItemType Directory -Force -Path $p | Out-Null; Write-Host "Created: $p" } } }

function Move-File { param($src,$dst) if (-not (Test-Path $src)) { return } if ($DryRun) { Write-Host "[DRY] Move: $src -> $dst" } else { Ensure-Dir (Split-Path $dst); Move-Item -Path $src -Destination $dst -Force; Write-Host "Moved: $src -> $dst" } $ops += @{from=$src;to=$dst}
}

if ($Undo) {
    if (-not (Test-Path $manifestPath)) { Write-Host "No manifest found at $manifestPath"; exit 1 }
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
    Write-Host "Undoing $($manifest.ops.Count) operations..."
    foreach ($op in ($manifest.ops | Sort-Object -Property @{Expression={$_.time}} -Descending)) {
        $from = $op.to
        $to = $op.from
        if (Test-Path $from) {
            Write-Host "Undo Move: $from -> $to"
            if (-not $DryRun) { Ensure-Dir (Split-Path $to); Move-Item -Path $from -Destination $to -Force }
        } else { Write-Host "Skipping: $from (missing)" }
    }
    if (-not $DryRun) { Remove-Item $manifestPath -ErrorAction SilentlyContinue }
    Write-Host "Undo complete."; exit 0
}

# Preflight targets
$archiveLegacy = Join-Path $RepoRoot "archive\legacy"
$archiveClutter = Join-Path $RepoRoot "archive\clutter"
$archiveDrafts = Join-Path $RepoRoot "archive\drafts"
$archiveOutputs = Join-Path $RepoRoot "archive\outputs"

Ensure-Dir $archiveLegacy
Ensure-Dir $archiveClutter
Ensure-Dir $archiveDrafts
Ensure-Dir $archiveOutputs

# Target 1: toolkit/prompts -> archive/clutter/toolkit_prompts
$toolkitPrompts = Join-Path $RepoRoot "toolkit\prompts"
if (Test-Path $toolkitPrompts) {
    $dst = Join-Path $archiveClutter "toolkit_prompts"
    Move-File $toolkitPrompts $dst
} else { Write-Host "No toolkit/prompts found; skipping." }

# Target 2: results older than N days -> archive/outputs
$resultsDir = Join-Path $RepoRoot "results"
if (Test-Path $resultsDir) {
    $threshold = (Get-Date).AddDays(-$DaysOldForResults)
    $old = Get-ChildItem -Path $resultsDir -Recurse -File | Where-Object { $_.LastWriteTime -lt $threshold }
    if ($old.Count -eq 0) { Write-Host "No results older than $DaysOldForResults days." }
    foreach ($f in $old) {
        $rel = $f.FullName.Substring($RepoRoot.Length).TrimStart('\')
        $dst = Join-Path $archiveOutputs $rel
        Move-File $f.FullName $dst
    }
} else { Write-Host "No results/ directory found; skipping." }

# Target 3: stale draft prompts
$promptsDir = Join-Path $RepoRoot "prompts"
if (Test-Path $promptsDir) {
    $thresholdDraft = (Get-Date).AddMonths(-$DraftMonths)
    $mds = Get-ChildItem -Path $promptsDir -Recurse -Include *.md -File
    foreach ($md in $mds) {
        $content = Get-Content $md.FullName -Raw -ErrorAction SilentlyContinue
        if ($content -match "reviewStatus:\s*draft") {
            if ($md.LastWriteTime -lt $thresholdDraft) {
                $rel = $md.FullName.Substring($RepoRoot.Length).TrimStart('\')
                $dst = Join-Path $archiveDrafts $rel
                Move-File $md.FullName $dst
            }
        }
    }
} else { Write-Host "No prompts/ directory found; skipping." }

# Write manifest if applying
if ($Apply -and -not $DryRun) {
    $manifest = @{ time = (Get-Date).ToString('o'); ops = $ops }
    $manifest | ConvertTo-Json -Depth 5 | Out-File -FilePath $manifestPath -Encoding utf8
    Write-Host "Manifest written to $manifestPath"
}

Write-Host "Done. DryRun=$DryRun; Apply=$Apply"

if ($DryRun -and -not $Apply) { Write-Host "Run with -Apply -Confirm to execute moves." }

# Safety: require explicit -Confirm to run Apply
if ($Apply -and -not $Confirm) {
    Write-Host "Refusing to execute -Apply without -Confirm flag. Rerun with -Apply -Confirm."; exit 1
}
