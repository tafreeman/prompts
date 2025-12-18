#!/usr/bin/env python3
"""
Windows AI Quick Setup Script
Checks and installs dependencies for Windows AI APIs
"""

import sys
import subprocess
import platform
import os


def check_windows_version():
    """Check if running on Windows 11."""
    print("[1/4] Checking Windows version...")
    
    if sys.platform != 'win32':
        print("❌ Not running on Windows")
        return False
    
    version = platform.version()
    build = int(platform.win32_ver()[1].split('.')[2]) if platform.win32_ver()[1] else 0
    
    if build >= 22000:  # Windows 11
        print(f"✓ Windows 11 detected (Build {build})")
        return True
    else:
        print(f"⚠️  Windows {platform.win32_ver()[0]} (Build {build})")
        print("   Windows AI APIs require Windows 11 (Build 22000+)")
    return False


def install_winrt():
    """Install winrt-runtime package."""
    print("\n[2/4] Installing winrt-runtime...")
    
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "winrt-runtime", "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("✓ winrt-runtime installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install winrt-runtime: {e}")
        print("   Try manually: pip install winrt-runtime")
        return False


def check_windows_app_sdk():
    """Check for Windows App SDK."""
    print("\n[3/4] Checking for Windows App SDK...")
    
    # Check common SDK locations
    sdk_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin",
        os.path.expandvars(r"%ProgramFiles%\WindowsApps")
    ]
    
    sdk_found = any(os.path.exists(path) for path in sdk_paths)
    
    if sdk_found:
        print("✓ Windows App SDK detected")
    else:
        print("⚠️  Windows App SDK not detected")
        print("\n   To install Windows App SDK 1.7+:")
        print("   1. Download: https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads")
        print("   2. Or via winget: winget install Microsoft.WindowsAppSDK")
        print("")
    
    return sdk_found


def test_windows_ai():
    """Test Windows AI availability."""
    print("\n[4/4] Testing Windows AI availability...")
    
    try:
        result = subprocess.run(
            [sys.executable, "tools/windows_ai.py", "--info"],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main setup routine."""
    print("=" * 50)
    print("Windows AI Setup for Prompt Toolkit")
    print("=" * 50)
    print()
    
    # Run checks
    win11 = check_windows_version()
    winrt = install_winrt()
    sdk = check_windows_app_sdk()
    test = test_windows_ai()
    
    # Summary
    print("\n" + "=" * 50)
    print("Setup Summary")
    print("=" * 50)
    print(f"Windows 11:       {'✓' if win11 else '✗'}")
    print(f"winrt-runtime:    {'✓' if winrt else '✗'}")
    print(f"Windows App SDK:  {'✓' if sdk else '⚠️ '}")
    print(f"Integration Test: {'✓' if test else '⚠️ '}")
    print()
    
    if all([win11, winrt, sdk]):
        print("✅ All requirements met! Windows AI is ready.")
        print("\nUsage:")
        print("  python tools/windows_ai.py -p 'Test prompt'")
        print("  python prompt.py run test.md -p windows-ai")
    else:
        print("⚠️  Some requirements missing. See messages above.")
        print("\nRequired:")
        print("  • Windows 11 with NPU (Copilot+ PC)")
        print("  • Windows App SDK 1.7+")
        print("  • pip install winrt-runtime")
    
    print("\nDocumentation:")
    print("  https://learn.microsoft.com/en-us/windows/ai/apis/")
    print("  tools/WINDOWS_AI_README.md")
    print()


if __name__ == "__main__":
    main()
