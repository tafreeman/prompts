# Enterprise AI Prompt Library - One-Command IIS Deployment Script
# 
# Usage: .\deploy.ps1 [-AppPath "C:\inetpub\wwwroot\prompt_library"] [-SiteName "Enterprise AI Prompt Library"] [-Port 80]

[CmdletBinding()]
param(
    [string]$AppPath = "C:\inetpub\wwwroot\prompt_library",
    [string]$SiteName = "Enterprise AI Prompt Library",
    [int]$Port = 80,
    [string]$HostName = ""
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Enterprise AI Prompt Library - IIS Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "This script must be run as Administrator. Please restart PowerShell as Administrator and try again."
    exit 1
}

# Check if IIS is installed
Write-Host "[1/10] Checking IIS installation..." -ForegroundColor Yellow
$iisFeature = Get-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole -ErrorAction SilentlyContinue
if ($null -eq $iisFeature -or $iisFeature.State -ne "Enabled") {
    Write-Error "IIS is not installed. Please install IIS first using: Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole"
    exit 1
}
Write-Host "   ✓ IIS is installed" -ForegroundColor Green

# Check if CGI module is installed
Write-Host "[2/10] Checking CGI module..." -ForegroundColor Yellow
$cgiFeature = Get-WindowsOptionalFeature -Online -FeatureName IIS-CGI -ErrorAction SilentlyContinue
if ($null -eq $cgiFeature -or $cgiFeature.State -ne "Enabled") {
    Write-Host "   Installing CGI module..." -ForegroundColor Yellow
    Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI -NoRestart
}
Write-Host "   ✓ CGI module is ready" -ForegroundColor Green

# Detect Python installation
Write-Host "[3/10] Detecting Python installation..." -ForegroundColor Yellow
$pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonExe) {
    Write-Error "Python is not found in PATH. Please install Python 3.8+ and ensure it's in your PATH."
    exit 1
}
$pythonVersion = & python --version 2>&1
Write-Host "   ✓ Found: $pythonVersion at $pythonExe" -ForegroundColor Green

# Get Python site-packages directory
$sitePackages = python -c 'import site; print(site.getsitepackages()[0])'
Write-Host "   Site-packages: $sitePackages" -ForegroundColor Gray

# Create application directory
Write-Host "[4/10] Creating application directory..." -ForegroundColor Yellow
if (-not (Test-Path $AppPath)) {
    New-Item -ItemType Directory -Path $AppPath -Force | Out-Null
}
$srcPath = Join-Path $AppPath "src"
if (-not (Test-Path $srcPath)) {
    New-Item -ItemType Directory -Path $srcPath -Force | Out-Null
}
Write-Host "   ✓ Directory created: $AppPath" -ForegroundColor Green

# Create logs directory
$logsPath = Join-Path $AppPath "logs"
if (-not (Test-Path $logsPath)) {
    New-Item -ItemType Directory -Path $logsPath -Force | Out-Null
}
Write-Host "   ✓ Logs directory created: $logsPath" -ForegroundColor Green

# Copy application files
Write-Host "[5/10] Copying application files..." -ForegroundColor Yellow
$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$sourceSrc = Join-Path $repoRoot "src"
$sourcePrompts = Join-Path $repoRoot "prompts"

if (Test-Path $sourceSrc) {
    Copy-Item -Path "$sourceSrc\*" -Destination $srcPath -Recurse -Force
    Write-Host "   ✓ Application files copied from: $sourceSrc" -ForegroundColor Green
} else {
    Write-Error "Source directory not found: $sourceSrc"
    exit 1
}

# Copy prompts directory (required by load_prompts.py)
$promptsPath = Join-Path $AppPath "prompts"
if (Test-Path $sourcePrompts) {
    if (-not (Test-Path $promptsPath)) {
        New-Item -ItemType Directory -Path $promptsPath -Force | Out-Null
    }
    Copy-Item -Path "$sourcePrompts\*" -Destination $promptsPath -Recurse -Force
    Write-Host "   ✓ Prompts copied from: $sourcePrompts" -ForegroundColor Green
} else {
    Write-Warning "Prompts directory not found at $sourcePrompts - database will only contain embedded prompts"
}

# Install Python dependencies
Write-Host "[6/10] Installing Python dependencies..." -ForegroundColor Yellow
Push-Location $srcPath
try {
    & python -m pip install --upgrade pip 2>&1 | Out-Null
    & python -m pip install -r requirements.txt 2>&1 | Out-Null
    & python -m pip install wfastcgi 2>&1 | Out-Null
    Write-Host "   ✓ Dependencies installed" -ForegroundColor Green
} catch {
    Write-Error "Failed to install dependencies: $_"
    Pop-Location
    exit 1
}
Pop-Location

# Enable wfastcgi
Write-Host "[7/10] Configuring FastCGI..." -ForegroundColor Yellow
$wfastcgiPath = python -c 'import wfastcgi; print(wfastcgi.__file__)'
$scriptProcessor = "${pythonExe}|${wfastcgiPath}"
Write-Host "   Script Processor: $scriptProcessor" -ForegroundColor Gray

# Enable wfastcgi (this registers it in IIS)
wfastcgi-enable 2>&1 | Out-Null

# Create/Update web.config with correct paths
$webConfigContent = @"
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="FastCgiModule" 
           scriptProcessor="$scriptProcessor" 
           resourceType="Unspecified" requireAccess="Script" />
    </handlers>
    <defaultDocument>
      <files>
        <clear />
        <add value="app.py" />
      </files>
    </defaultDocument>
    <staticContent>
      <mimeMap fileExtension=".json" mimeType="application/json" />
    </staticContent>
    <rewrite>
      <rules>
        <rule name="Static Files" stopProcessing="true">
          <match url="^static/.*" />
          <action type="Rewrite" url="{R:0}" />
        </rule>
        <rule name="Flask Application">
          <match url="(.*)" />
          <conditions>
            <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
          </conditions>
          <action type="Rewrite" url="app.py/{R:1}" />
        </rule>
      </rules>
    </rewrite>
  </system.webServer>
  <appSettings>
    <add key="WSGI_HANDLER" value="app.app" />
    <add key="PYTHONPATH" value="$srcPath" />
    <add key="WSGI_LOG" value="$logsPath\wfastcgi.log" />
    <add key="FLASK_ENV" value="production" />
  </appSettings>
</configuration>
"@

Set-Content -Path (Join-Path $srcPath "web.config") -Value $webConfigContent -Force
Write-Host "   ✓ FastCGI configured" -ForegroundColor Green

# Initialize database
Write-Host "[8/10] Initializing database..." -ForegroundColor Yellow
Push-Location $srcPath
try {
    & python load_prompts.py 2>&1 | Out-Null
    Write-Host "   ✓ Database initialized" -ForegroundColor Green
} catch {
    Write-Warning "Database initialization had warnings (this may be normal)"
}
Pop-Location

# Set permissions
Write-Host "[9/10] Setting permissions..." -ForegroundColor Yellow
$acl = Get-Acl $AppPath
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule("IIS_IUSRS", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
$acl.SetAccessRule($rule)
Set-Acl $AppPath $acl

$dbPath = Join-Path $srcPath "prompt_library.db"
if (Test-Path $dbPath) {
    $acl = Get-Acl $dbPath
    $acl.SetAccessRule($rule)
    Set-Acl $dbPath $acl
}
Write-Host "   ✓ Permissions set" -ForegroundColor Green

# Create/Update IIS Site
Write-Host "[10/10] Configuring IIS site..." -ForegroundColor Yellow
Import-Module WebAdministration

# Check if site exists
$existingSite = Get-Website -Name $SiteName -ErrorAction SilentlyContinue
if ($existingSite) {
    Write-Host "   Updating existing site..." -ForegroundColor Yellow
    Stop-Website -Name $SiteName -ErrorAction SilentlyContinue
    Remove-Website -Name $SiteName
}

# Create site
$siteParams = @{
    Name = $SiteName
    PhysicalPath = $srcPath
    Port = $Port
}
if ($HostName) {
    $siteParams.HostHeader = $HostName
}

New-Website @siteParams | Out-Null

# Configure Application Pool
$appPoolName = $SiteName
Set-ItemProperty "IIS:\AppPools\$appPoolName" -Name managedRuntimeVersion -Value ""
Set-ItemProperty "IIS:\AppPools\$appPoolName" -Name managedPipelineMode -Value "Integrated"

# Start the site
Start-Website -Name $SiteName
Write-Host "   ✓ IIS site configured and started" -ForegroundColor Green

# Display summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nSite Details:" -ForegroundColor White
Write-Host "  Name: $SiteName" -ForegroundColor Gray
Write-Host "  Path: $srcPath" -ForegroundColor Gray
Write-Host "  Port: $Port" -ForegroundColor Gray
if ($HostName) {
    Write-Host "  URL: http://${HostName}:${Port}" -ForegroundColor Cyan
} else {
    Write-Host "  URL: http://localhost:${Port}" -ForegroundColor Cyan
}
Write-Host "`nNext Steps:" -ForegroundColor White
Write-Host "  1. Open your browser and navigate to the URL above" -ForegroundColor Gray
Write-Host "  2. Configure HTTPS if needed" -ForegroundColor Gray
Write-Host "  3. Set up Windows Authentication if required" -ForegroundColor Gray
$logFile = Join-Path $logsPath "wfastcgi.log"
Write-Host "`nLogs Location: $logFile" -ForegroundColor Yellow
Write-Host ""
