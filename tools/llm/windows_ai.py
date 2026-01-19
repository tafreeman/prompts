#!/usr/bin/env python3
"""tools.windows_ai

Windows AI (Phi Silica) Integration
===================================

This module integrates Phi Silica via the .NET bridge in
`tools/windows_ai_bridge/`.

Why a bridge?
- The Windows AI APIs are exposed via Windows App SDK WinRT APIs.
- The bridge provides a stable CLI interface for Python to call.

Limited Access Feature (LAF)
----------------------------
Depending on your Windows/App SDK channel, Phi Silica may be gated behind
Limited Access Features.

If you have a LAF token, configure these environment variables (recommended):
- PHI_SILICA_LAF_FEATURE_ID
- PHI_SILICA_LAF_TOKEN
- PHI_SILICA_LAF_ATTESTATION

Docs:
- Phi Silica: https://learn.microsoft.com/windows/ai/apis/phi-silica
- Troubleshooting: https://learn.microsoft.com/windows/ai/apis/troubleshooting
- Unlock (short link): https://aka.ms/phi-silica-unlock
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple


class WindowsAIModel:
    """Wrapper for Windows AI APIs (Phi Silica SLM)."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Phi Silica is available via the bridge."""
        if sys.platform != 'win32':
            raise OSError("Windows AI APIs are only available on Windows")

        info, _ = get_phi_silica_bridge_info(timeout_s=60)
        available = bool(info.get("available")) if isinstance(info, dict) else False
        if not available:
            err = None
            if isinstance(info, dict):
                err = info.get("error")
            raise RuntimeError(err or "Phi Silica not available")
        return True

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate text using Phi Silica SLM.

        Args:
            prompt: The input prompt
            system_instruction: Optional system prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        # Always use the C# bridge.

        try:
            # Build the full prompt
            full_prompt = prompt
            if system_instruction:
                full_prompt = f"{system_instruction}\n\n{prompt}"

            if self.verbose:
                print("🧠 Running Phi Silica (NPU)...")
                print(f"   Temperature: {temperature}")
                print(f"   Max tokens: {max_tokens}")

            # Call Phi Silica
            response = self._call_phi_silica(
                full_prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response

        except Exception as e:
            return f"[ERROR] Windows AI API error: {str(e)}"

    def _call_phi_silica(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Call Phi Silica model via C# bridge.

        Uses subprocess to call the PhiSilicaBridge C# application
        which has access to Windows App SDK AI APIs.
        """
        # Find the C# bridge
        bridge_dir = Path(__file__).parent / "windows_ai_bridge"
        bridge_proj = bridge_dir / "PhiSilicaBridge.csproj"

        if not bridge_proj.exists():
            return (
                "[ERROR] C# bridge not found. Run:\n"
                "  dotnet build tools/windows_ai_bridge/PhiSilicaBridge.csproj"
            )

        try:
            # The bridge reads LAF settings from environment variables.
            result = subprocess.run(
                ["dotnet", "run", "--project", str(bridge_proj), "--", prompt],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(bridge_dir)
            )

            if result.returncode == 0:
                return result.stdout.strip()

            stderr = (result.stderr or "").strip()
            stdout = (result.stdout or "").strip()
            msg = stderr or stdout or "Bridge failed"
            return f"[ERROR] Bridge error: {msg}"

        except subprocess.TimeoutExpired:
            return "[ERROR] Phi Silica request timed out (120s)"
        except FileNotFoundError:
            return "[ERROR] dotnet not found. Install .NET SDK."
        except Exception as e:
            raise RuntimeError(f"Phi Silica API call failed: {e}")


def check_windows_ai_available() -> bool:
    """Check if Windows AI APIs are available on this system."""
    try:
        info, _ = get_phi_silica_bridge_info(timeout_s=30)
        return bool(info.get("available")) if isinstance(info, dict) else False
    except Exception:
        return False


def get_model_info() -> Dict[str, Any]:
    """Get information about Windows AI model availability."""
    info, raw = get_phi_silica_bridge_info(timeout_s=60)
    out: Dict[str, Any] = {
        "platform": sys.platform,
        "bridge": {
            "project": str(_bridge_project_path()),
            "dotnet_on_path": bool(_which("dotnet")),
        },
        "info": info,
    }

    if raw and not info:
        out["info_raw"] = raw[:2000]
    return out


def _which(cmd: str) -> Optional[str]:
    import shutil
    return shutil.which(cmd)


def _bridge_project_path() -> Path:
    return Path(__file__).parent / "windows_ai_bridge" / "PhiSilicaBridge.csproj"


def get_phi_silica_bridge_info(timeout_s: int = 60) -> Tuple[Dict[str, Any], str]:
    """Call the bridge `--info` and parse its JSON output.

    Returns: (info_dict, raw_stdout)
    - `info_dict` may include `available`, `readyState`, and `error`.
    - bridge may return non-zero even when it prints JSON to stdout.
    """
    if sys.platform != "win32":
        return {"available": False, "error": "Not running on Windows"}, ""

    proj = _bridge_project_path()
    if not proj.exists():
        return {"available": False, "error": "Bridge project not found"}, ""

    if not _which("dotnet"):
        return {"available": False, "error": "dotnet not found. Install .NET SDK."}, ""

    try:
        r = subprocess.run(
            ["dotnet", "run", "--project", str(proj), "--", "--info"],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            cwd=str(proj.parent),
        )
        stdout = (r.stdout or "").strip()
        stderr = (r.stderr or "").strip()

        if stdout:
            try:
                return json.loads(stdout), stdout
            except Exception:
                # Fall through; return raw.
                pass

        return {
            "available": False,
            "error": stderr or stdout or f"Bridge exited {r.returncode}",
            "bridge_exit_code": r.returncode,
        }, stdout
    except subprocess.TimeoutExpired:
        return {"available": False, "error": f"Bridge --info timed out after {timeout_s}s"}, ""
    except Exception as e:
        return {"available": False, "error": str(e)}, ""


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Test Windows AI APIs (Phi Silica)",
        epilog="Example: python windows_ai.py -p 'Explain quantum computing in simple terms'"
    )
    parser.add_argument("-p", "--prompt", default="Hello, what is AI?",
                        help="Prompt to send to Phi Silica")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    parser.add_argument("--info", action="store_true",
                        help="Show model availability info")

    args = parser.parse_args()

    if args.info:
        import json
        info = get_model_info()
        print(json.dumps(info, indent=2))
        sys.exit(0)

    try:
        model = WindowsAIModel(verbose=args.verbose)
        response = model.generate(args.prompt)
        print("\n" + "="*60)
        print("RESPONSE FROM PHI SILICA (Windows AI)")
        print("="*60)
        print(response)
        print("="*60)

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)
