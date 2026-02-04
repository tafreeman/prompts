# Windows AI NPU Integration

NPU-accelerated inference using **Phi Silica** via the Windows Copilot Runtime and Windows App SDK.

> **ℹ️ Unified Documentation**: For the full tools reference, see the [Unified Tools README](./README.md).

---

## 🚀 Status: **Functional (C# Bridge)**

The integration uses a high-performance C# Class Library (`PhiSilicaBridge.exe`) to interface directly with the Windows App SDK AI APIs, callable from Python via `subprocess`.

### **Hardware Requirements**

- **Copilot+ PC**: NPU is mandatory (Qualcomm Snapdragon X, AMD Ryzen AI 300 series, or Intel Core Ultra 200V).
- **Windows 11 24H2 (Build 26100+)**: Required for Copilot Runtime.

---

## 📦 Setup & Token

Windows AI (Phi Silica) is a **Limited Access Feature**.

1. **Apply for Access**: You MUST have an unlock token from Microsoft.
   - [Apply here: aka.ms/phi-silica-unlock](https://aka.ms/phi-silica-unlock)
2. **Setup**:
   - Run `scripts/setup_windows_ai.ps1` to install dependencies.
   - Once you have a token, add it to `tools/windows_ai_bridge/PhiSilicaBridge.csproj`.

---

## 🛠️ Usage

### **CLI (Preferred)**

```bash
# Run a prompt using the NPU
python prompt.py run prompts/example.md -p windows

# Evaluate a directory using NPU (Tier 7)
python prompt.py eval prompts/advanced/ -t 7
```

### **Python API**

```python
from tools.llm_client import LLMClient

# Dispatches to the C# bridge automatically
response = LLMClient.generate_text("windows-ai:phi-silica", "Hello from the NPU!")
```

---

## 📂 Components

| File | Purpose |
| ------ | --------- |
| `windows_ai.py` | Python wrapper and availability checks |
| `windows_ai_bridge/` | C# Source code for the CLI bridge |
| `PhiSilicaBridge.exe` | Compiled executable called by Python |

---

## 🔍 Troubleshooting

- **Access Denied**: You are likely missing the unlock token.
- **Model Unavailable**: Check the **AI Dev Gallery** to ensure Phi Silica is downloaded to your system.
- **NPU Not Found**: Ensure you are on a Copilot+ PC and NPU drivers are up to date.

For more details on all available tools, see the [main tools documentation](./README.md).
