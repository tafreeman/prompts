# Windows AI Setup Script
# Installs dependencies for Windows Copilot Runtime APIs (Phi Silica)

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Windows AI Setup for Prompt Toolkit" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Windows version
Write-Host "[1/5] Checking Windows version..." -ForegroundColor Yellow
$osVersion = [System.Environment]::OSVersion.Version
if ($osVersion.Major -lt 10 -or ($osVersion.Major -eq 10 -and $osVersion.Build -lt 22000)) {
    Write-Host "❌ Windows 11 required (Build 22000+). Current: $($osVersion.Build)" -ForegroundColor Red
    Write-Host "   Windows AI APIs require Windows 11 with NPU support." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Windows 11 detected (Build $($osVersion.Build))" -ForegroundColor Green

# Check for NPU (heuristic - checks for AI accelerator devices)
Write-Host ""
Write-Host "[2/5] Checking for NPU..." -ForegroundColor Yellow
$npuDevices = Get-PnpDevice | Where-Object { 
    $_.FriendlyName -like "*NPU*" -or 
    $_.FriendlyName -like "*Neural*" -or
    $_.FriendlyName -like "*AI Boost*" -or
    $_.FriendlyName -like "*Copilot*"
}

if ($npuDevices) {
    Write-Host "✓ NPU detected: $($npuDevices[0].FriendlyName)" -ForegroundColor Green
} else {
    Write-Host "⚠️  No NPU detected. Windows AI APIs require Copilot+ PC hardware." -ForegroundColor Yellow
    Write-Host "   Continuing anyway - some features may not work." -ForegroundColor Yellow
}

# Install Python winrt-runtime package
Write-Host ""
Write-Host "[3/5] Installing Python WinRT package..." -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip | Out-Null
    python -m pip install winrt-runtime --quiet
    Write-Host "✓ winrt-runtime installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install winrt-runtime: $_" -ForegroundColor Red
    Write-Host "   Try manually: pip install winrt-runtime" -ForegroundColor Red
}

# Check for Windows App SDK
Write-Host ""
Write-Host "[4/5] Checking for Windows App SDK..." -ForegroundColor Yellow

$sdkPaths = @(
    "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\makeappx.exe",
    "$env:ProgramFiles\WindowsApps\Microsoft.WindowsAppRuntime.*"
)

$sdkFound = $false
foreach ($path in $sdkPaths) {
    if (Test-Path $path) {
        $sdkFound = $true
        break
    }
}

if ($sdkFound) {
    Write-Host "✓ Windows App SDK detected" -ForegroundColor Green
} else {
    Write-Host "⚠️  Windows App SDK not detected" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   To install Windows App SDK 1.7+:" -ForegroundColor Cyan
    Write-Host "   1. Download from: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads" -ForegroundColor White
    Write-Host "   2. Or install via winget:" -ForegroundColor White
    Write-Host "      winget install Microsoft.WindowsAppSDK" -ForegroundColor Gray
    Write-Host ""
    
    # Offer to install via winget
    $install = Read-Host "   Install Windows App SDK now via winget? (y/N)"
    if ($install -eq 'y' -or $install -eq 'Y') {
        Write-Host "   Installing Windows App SDK..." -ForegroundColor Yellow
        winget install Microsoft.WindowsAppSDK.1.7 --accept-package-agreements --accept-source-agreements
    }
}

# Test availability
Write-Host ""
Write-Host "[5/5] Testing Windows AI availability..." -ForegroundColor Yellow
python tools/windows_ai.py --info | Out-String | Write-Host

# Summary
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Ensure you have a Copilot+ PC with NPU" -ForegroundColor Gray
Write-Host "  2. Install Windows App SDK 1.7+ if not detected" -ForegroundColor Gray
Write-Host "  3. Test with: python tools/windows_ai.py -p 'Hello!'" -ForegroundColor Gray
Write-Host "  4. Use in toolkit: python prompt.py run test.md -p windows-ai" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentation:" -ForegroundColor White
Write-Host "  • https://learn.microsoft.com/en-us/windows/ai/apis/" -ForegroundColor Gray
Write-Host "  • tools/WINDOWS_AI_README.md" -ForegroundColor Gray
Write-Host ""
