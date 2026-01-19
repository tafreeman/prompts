# Windows AI Installation Guide

## Quick Install

### Option 1: PowerShell Script (Recommended)

```powershell
.\scripts\setup_windows_ai.ps1
```

### Option 2: Python Script

```bash
python scripts/setup_windows_ai.py
```

### Option 3: Manual Installation

1. **Install Python Package**

   ```bash
   pip install winrt-runtime
   ```

2. **Install Windows App SDK 1.7+**

   **Via WinGet:**

   ```powershell
   winget install Microsoft.WindowsAppSDK.1.7
   ```

   **Via Download:**
   - Visit: <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/downloads>
   - Download and run the installer

3. **Verify Installation**

   ```bash
   python tools/windows_ai.py --info
   ```

## System Requirements

✅ **Required:**

- Windows 11 (Build 22000+)
- Python 3.8+
- pip (Python package manager)

⚡ **Recommended for Full Functionality:**

- Copilot+ PC with NPU
- Windows App SDK 1.7+
- winrt-runtime Python package

## Usage Examples

### Check Status

```bash
python tools/windows_ai.py --info
```

### Test Generation

```bash
python tools/windows_ai.py -p "What is quantum computing?" -v
```

### Via Unified Toolkit

```bash
# Run a prompt with Windows AI
python prompt.py run myfile.md -p windows-ai --model phi-silica

# Evaluate with Windows AI (Tier 7)
python prompt.py eval prompts/ -t 7
```

### Via Python

```python
from tools.llm_client import LLMClient

response = LLMClient.generate_text(
    "windows-ai:phi-silica",
    "Explain machine learning",
    temperature=0.7,
    max_tokens=2000
)
print(response)
```

## Troubleshooting

### winrt-runtime Installation Fails

```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install winrt-runtime
pip install winrt-runtime
```

### Windows App SDK Not Detected

1. Check installed apps: `winget list | Select-String "WindowsAppSDK"`
2. Install manually from: <https://aka.ms/windowsappsdk/1.7/latest/windowsappruntimeinstall-x64.exe>

### NPU Not Detected

- Windows AI APIs work best on Copilot+ PCs with NPU
- Some features may fallback to CPU if no NPU available
- Check Device Manager → Neural Processing Units

## Testing

After installation, verify everything works:

```bash
# 1. Check installation
python scripts/setup_windows_ai.py

# 2. Test availability
python tools/windows_ai.py --info

# 3. Try a simple prompt
python tools/windows_ai.py -p "Hello, test!"
```

## Current Status

🟡 **Placeholder Implementation**

The integration infrastructure is complete, but the actual Windows AI API calls are pending Python/WinRT bindings for:

- `Windows.AI.Generative.PhiSilicaModel`
- `Windows.AI.Generative.PhiSilicaSession`

The toolkit will gracefully fallback to other providers until full implementation is available.

## Resources

- **Official Docs**: <https://learn.microsoft.com/en-us/windows/ai/apis/>
- **Phi Silica Guide**: <https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica>  
- **AI Dev Gallery**: ms-windows-store://pdp/?productid=9N9PN1MM3BD5
- **Windows App SDK**: <https://learn.microsoft.com/en-us/windows/apps/windows-app-sdk/>

## Next Steps

Once you have a Copilot+ PC with NPU and Windows App SDK installed:

1. Complete the Python/WinRT bindings in `tools/windows_ai.py`
2. Test with real hardware
3. Update placeholder implementation with actual API calls

For now, use other providers (local, azure-foundry, github, etc.) for full functionality.
