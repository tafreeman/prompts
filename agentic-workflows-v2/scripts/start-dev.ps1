[CmdletBinding()]
param(
    [switch]$Reload,
    [string]$BackendHost = '127.0.0.1',
    [int]$BackendPort = 8012,
    [string]$FrontendHost = '127.0.0.1',
    [int]$FrontendPort = 5174,
    [string]$ApiProxyTarget = 'http://127.0.0.1:8012'
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$uiRoot = Join-Path $projectRoot 'ui'
$logsDir = Join-Path $projectRoot '.run-logs'
New-Item -ItemType Directory -Path $logsDir -Force | Out-Null

$backendOutLog = Join-Path $logsDir 'backend.out.log'
$backendErrLog = Join-Path $logsDir 'backend.err.log'
$frontendOutLog = Join-Path $logsDir 'frontend.out.log'
$frontendErrLog = Join-Path $logsDir 'frontend.err.log'
$backendPidFile = Join-Path $logsDir 'backend.pid'
$frontendPidFile = Join-Path $logsDir 'frontend.pid'

$python = Join-Path (Split-Path -Parent $projectRoot) '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
    $python = (Get-Command python -ErrorAction SilentlyContinue).Source
}
if (-not $python) {
    throw "Python was not found in .venv or on PATH"
}

$npmCmd = (Get-Command npm.cmd -ErrorAction SilentlyContinue).Source
if (-not $npmCmd) {
    throw "npm.cmd was not found on PATH"
}

Write-Host "Starting backend..." -ForegroundColor Cyan
$backendArgs = @('-m','uvicorn','agentic_v2.server.app:app','--host',$BackendHost,'--port',"$BackendPort",'--app-dir','.')
if ($Reload) { $backendArgs += '--reload' }

$backendProc = Start-Process -FilePath $python -ArgumentList $backendArgs -WorkingDirectory $projectRoot -PassThru -RedirectStandardOutput $backendOutLog -RedirectStandardError $backendErrLog
Set-Content -Path $backendPidFile -Value $backendProc.Id

Write-Host "Starting frontend..." -ForegroundColor Cyan
$frontendCommand = "`$env:VITE_API_PROXY_TARGET='$ApiProxyTarget'; & '$npmCmd' run dev -- --host $FrontendHost --port $FrontendPort"
$psHost = (Get-Command powershell.exe -ErrorAction SilentlyContinue).Source
if (-not $psHost) {
    $psHost = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
}
if (-not $psHost) {
    throw "Neither powershell.exe nor pwsh was found on PATH"
}

$frontendProc = Start-Process -FilePath $psHost -ArgumentList @('-NoProfile','-Command',$frontendCommand) -WorkingDirectory $uiRoot -PassThru -RedirectStandardOutput $frontendOutLog -RedirectStandardError $frontendErrLog
Set-Content -Path $frontendPidFile -Value $frontendProc.Id

Start-Sleep -Seconds 2

try {
    $health = Invoke-RestMethod -Uri "http://$BackendHost`:$BackendPort/api/health" -TimeoutSec 5
    Write-Host "Backend health: $($health.status)" -ForegroundColor Green
} catch {
    Write-Warning "Backend health check failed. See $backendErrLog"
}

try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://$FrontendHost`:$FrontendPort" -TimeoutSec 5
    Write-Host "Frontend HTTP: $($resp.StatusCode)" -ForegroundColor Green
} catch {
    Write-Warning "Frontend check failed. See $frontendErrLog"
}

Write-Host "Started." -ForegroundColor Green
Write-Host "Backend:  http://$BackendHost`:$BackendPort"
Write-Host "Frontend: http://$FrontendHost`:$FrontendPort"
Write-Host "Logs: $logsDir"
