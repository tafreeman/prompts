<#!
.SYNOPSIS
Run tools.prompteval across a matrix of models and tiers.

.DESCRIPTION
- Writes one JSON report per (path, tier, model) into results/model-matrix/.
- Continues across the matrix even if some runs fail (unless -StopOnFirstFailure).

.EXAMPLE
./scripts/prompteval/run-matrix.ps1 -Path prompts/analysis

.EXAMPLE
./scripts/prompteval/run-matrix.ps1 -Path prompts -Tiers 2,3 -Models local:phi4-gpu,ollama:phi4-reasoning:latest

.NOTES
If you include gh:* models, expect possible rate limiting; failures will be recorded and the script will still proceed.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path,

    [int[]]$Tiers = @(2, 3),

    [string[]]$Models = @(
        "local:phi4-cpu",
        "local:phi4-gpu",
        "ollama:gpt-oss:20b",
        "ollama:phi4-reasoning:latest",
        "aitk:phi-4-reasoning-14.7b-qnn",
        "aitk:phi-4-mini-reasoning",
        "ollama:gpt-oss:120b-cloud"
    ),

    # If set, ignore -Models and populate from discovery_results.json.
    # By default we only include free/local providers to avoid cloud costs and rate limits.
    [switch]$UseDiscovery,

    # Providers to include when -UseDiscovery is set.
    # Common free/local providers in this repo: local_onnx, ollama, ai_toolkit.
    [string[]]$DiscoveryProviders = @(
        "local_onnx",
        "ollama",
        "ai_toolkit"
    ),

    # Include GitHub Models (gh:*) from discovery. This is often free but may rate limit.
    [switch]$IncludeGithubModels,

    # Optional cap to keep runs manageable when using discovery.
    # 0 means no cap.
    [int]$MaxModelsPerProvider = 0,

    [string]$OutDir = "results/model-matrix",

    # When set, capture a PowerShell transcript (including python stdout/stderr)
    # to a timestamped log file under OutDir.
    [switch]$Transcript,

    [switch]$VerboseEval,

    [switch]$CI,

    # By default, skip running local:* models if a lock file indicates that model is already in use.
    # Use -AllowLockedLocalModels to force running anyway.
    [switch]$AllowLockedLocalModels,

    [switch]$StopOnFirstFailure
)

Set-StrictMode -Version Latest

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")

function ConvertTo-SafeName {
    param([Parameter(Mandatory = $true)][string]$Value)

    $safe = $Value
    $safe = $safe -replace '[\\/:*?''"<>|]', '-'
    $safe = $safe -replace "\s+", "-"
    $safe = $safe -replace "-+", "-"
    return $safe.Trim('-')
}

$outDirFull = Join-Path $repoRoot $OutDir
$null = New-Item -ItemType Directory -Force -Path $outDirFull

$safePath = ConvertTo-SafeName $Path

function Get-ModelLockDir {
    $home = [Environment]::GetFolderPath('UserProfile')
    return Join-Path $home ".cache\prompts-eval\locks"
}

function Get-ModelsInUse {
    # Read lock files created by tools.llm.model_locks.create_model_lock.
    # We validate PIDs using Get-Process (no psutil dependency).
    $lockDir = Get-ModelLockDir
    $inUse = @{}
    if (-not (Test-Path $lockDir)) { return $inUse }

    Get-ChildItem -Path $lockDir -Filter "*.lock" -ErrorAction SilentlyContinue | ForEach-Object {
        $lockFile = $_.FullName
        try {
            $raw = Get-Content -Raw -Path $lockFile -ErrorAction Stop
            $info = $raw | ConvertFrom-Json
            $pid = [int]$info.pid
            $modelName = [string]$info.model
            $script = [string]$info.script

            $p = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($null -ne $p) {
                if (-not [string]::IsNullOrWhiteSpace($modelName)) {
                    $inUse[$modelName] = ("PID {0}: {1}" -f $pid, $script)
                }
            }
            else {
                # Stale lock
                Remove-Item -Force -Path $lockFile -ErrorAction SilentlyContinue
            }
        }
        catch {
            # Corrupt lock
            Remove-Item -Force -Path $lockFile -ErrorAction SilentlyContinue
        }
    }

    return $inUse
}

function Write-SkippedResult {
    param(
        [Parameter(Mandatory = $true)][string]$OutFile,
        [Parameter(Mandatory = $true)][string]$EvalPath,
        [Parameter(Mandatory = $true)][int]$Tier,
        [Parameter(Mandatory = $true)][string]$Model,
        [Parameter(Mandatory = $true)][string]$Reason
    )

    $obj = [pscustomobject]@{
        skipped = $true
        file = $EvalPath
        tier = $Tier
        model = $Model
        reason = $Reason
    }
    $json = $obj | ConvertTo-Json -Depth 6
    $null = New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutFile)
    Set-Content -Path $OutFile -Value $json -Encoding UTF8
}

function Get-DiscoveredModels {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string[]]$Providers,
        [switch]$IncludeGithubModels,
        [int]$MaxPerProvider = 0
    )

    $discPath = Join-Path $RepoRoot "discovery_results.json"
    if (-not (Test-Path $discPath)) {
        throw "discovery_results.json not found at $discPath. Run: python -m tools.llm.model_probe --discover --force -o discovery_results.json"
    }

    $json = Get-Content -Raw -Path $discPath | ConvertFrom-Json
    $providersObj = $json.providers
    if (-not $providersObj) {
        throw "discovery_results.json missing 'providers'"
    }

    $resolvedProviders = New-Object System.Collections.Generic.List[string]
    foreach ($p in $Providers) { $resolvedProviders.Add($p) | Out-Null }
    if ($IncludeGithubModels) { $resolvedProviders.Add("github_models") | Out-Null }

    $models = New-Object System.Collections.Generic.List[string]
    foreach ($p in $resolvedProviders) {
        $payload = $providersObj.$p
        if (-not $payload) { continue }
        $available = $payload.available
        if (-not $available) { continue }

        $count = 0
        foreach ($m in $available) {
            if ([string]::IsNullOrWhiteSpace($m)) { continue }
            $models.Add([string]$m) | Out-Null
            $count++
            if ($MaxPerProvider -gt 0 -and $count -ge $MaxPerProvider) { break }
        }
    }

    # De-dupe while preserving order
    $seen = @{}
    $uniq = New-Object System.Collections.Generic.List[string]
    foreach ($m in $models) {
        $k = $m.ToLowerInvariant()
        if (-not $seen.ContainsKey($k)) {
            $seen[$k] = $true
            $uniq.Add($m) | Out-Null
        }
    }
    return $uniq
}

if ($UseDiscovery) {
    $Models = Get-DiscoveredModels -RepoRoot $repoRoot -Providers $DiscoveryProviders -IncludeGithubModels:$IncludeGithubModels -MaxPerProvider $MaxModelsPerProvider
    Write-Host ("Using discovery models: {0}" -f $Models.Count) -ForegroundColor DarkCyan
}

$transcriptPath = $null
if ($Transcript) {
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $transcriptPath = Join-Path $outDirFull ("{0}__matrix__{1}.log" -f $safePath, $timestamp)
    Start-Transcript -Path $transcriptPath -Force | Out-Null
    Write-Host ("Transcript: {0}" -f $transcriptPath) -ForegroundColor DarkGray
}

$failures = New-Object System.Collections.Generic.List[object]

try {
    foreach ($tier in $Tiers) {
        foreach ($model in $Models) {
        $safeModel = ConvertTo-SafeName $model
        $outFile = Join-Path $outDirFull ("{0}__tier{1}__{2}.json" -f $safePath, $tier, $safeModel)

        # Avoid conflicting local:* runs if another process is already using that model.
        if (-not $AllowLockedLocalModels -and $model.ToLowerInvariant().StartsWith("local:")) {
            $modelKey = $model.Split(":", 2)[1]
            $locks = Get-ModelsInUse

            # We treat a match as either an exact lock name (preferred) or a contains match.
            $busyInfo = $null
            if ($locks.ContainsKey($modelKey)) {
                $busyInfo = $locks[$modelKey]
            }
            else {
                foreach ($k in $locks.Keys) {
                    if ($k.ToLowerInvariant().Contains($modelKey.ToLowerInvariant())) {
                        $busyInfo = $locks[$k]
                        break
                    }
                }
            }

            if ($null -ne $busyInfo) {
                $reason = "Skipped: local model '{0}' appears to be in use ({1})" -f $modelKey, $busyInfo
                Write-Host $reason -ForegroundColor Yellow
                Write-SkippedResult -OutFile $outFile -EvalPath $Path -Tier $tier -Model $model -Reason $reason
                continue
            }
        }

        $argList = @(
            "-m", "tools.prompteval",
            $Path,
            "--tier", $tier,
            "--model", $model,
            "--output", $outFile
        )

        if ($VerboseEval) { $argList += "--verbose" }
        if ($CI) { $argList += "--ci" }

        Write-Host ("[{0}] tier={1} model={2}" -f (Get-Date -Format "HH:mm:ss"), $tier, $model) -ForegroundColor Cyan

        Push-Location $repoRoot
        try {
            & python @argList
        }
        finally {
            Pop-Location
        }
        $exitCode = $LASTEXITCODE

        # Treat evaluation errors as failures even when the CLI returns 0 (e.g., missing path when evaluating a single file).
        $jsonFailure = $false
        if (Test-Path $outFile) {
            try {
                $resultObj = Get-Content -Raw -Path $outFile | ConvertFrom-Json
                if ($null -ne $resultObj.error -and ("" + $resultObj.error).Length -gt 0) { $jsonFailure = $true }
                if ($resultObj.PSObject.Properties.Name -contains "errors" -and [int]$resultObj.errors -gt 0) { $jsonFailure = $true }
                if ($resultObj.PSObject.Properties.Name -contains "failed" -and [int]$resultObj.failed -gt 0) { $jsonFailure = $true }
            }
            catch {
                # If we can't parse the output JSON, treat it as a failure.
                $jsonFailure = $true
            }
        }

        if ($exitCode -eq 0 -and $jsonFailure) {
            $exitCode = 1
        }

        if ($exitCode -ne 0) {
            $msg = "FAILED (exit $exitCode) -> $outFile"
            Write-Warning $msg

            $failures.Add([pscustomobject]@{
                path = $Path
                tier = $tier
                model = $model
                exitCode = $exitCode
                output = $outFile
            }) | Out-Null

            if ($StopOnFirstFailure) {
                throw $msg
            }
        }
        else {
            Write-Host "OK" -ForegroundColor Green
        }
        }
    }

    if ($failures.Count -gt 0) {
        Write-Host "\nSummary: $($failures.Count) failures" -ForegroundColor Yellow
        $failures | Format-Table -AutoSize | Out-String | Write-Host
        exit 1
    }

    Write-Host "\nSummary: all runs succeeded" -ForegroundColor Green
    exit 0
}
finally {
    if ($Transcript -and $null -ne $transcriptPath) {
        try { Stop-Transcript | Out-Null } catch { }
    }
}
