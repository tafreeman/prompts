<#!
.SYNOPSIS
Run tools.prompteval for a single path/tier/model and write the JSON report.

.EXAMPLE
./scripts/prompteval/run-one.ps1 -Path prompts/analysis -Tier 2 -Model local:phi4-gpu

.NOTES
- Requires Python env configured for this repo.
- Output defaults under results/model-runs/.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path,

    [Parameter(Mandatory = $true)]
    [int]$Tier,

    [Parameter(Mandatory = $true)]
    [string]$Model,

    [string]$OutDir = "results/model-runs",

    [switch]$VerboseEval,

    [switch]$CI
)

Set-StrictMode -Version Latest

function ConvertTo-SafeName {
    param([Parameter(Mandatory = $true)][string]$Value)

    $safe = $Value
    $safe = $safe -replace "[\\/:*?\"<>|]", "-"
    $safe = $safe -replace "\s+", "-"
    $safe = $safe -replace "-+", "-"
    return $safe.Trim('-')
}

$null = New-Item -ItemType Directory -Force -Path $OutDir

$safeModel = ConvertTo-SafeName $Model
$safePath = ConvertTo-SafeName $Path

$outFile = Join-Path $OutDir ("{0}__tier{1}__{2}.json" -f $safePath, $Tier, $safeModel)

$argList = @(
    "-m", "tools.prompteval",
    $Path,
    "--tier", $Tier,
    "--model", $Model,
    "--output", $outFile
)

if ($VerboseEval) { $argList += "--verbose" }
if ($CI) { $argList += "--ci" }

Write-Host "Running: python $($argList -join ' ')" -ForegroundColor Cyan

& python @argList
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    throw "prompteval failed (exit $exitCode). Output: $outFile"
}

Write-Host "OK -> $outFile" -ForegroundColor Green
