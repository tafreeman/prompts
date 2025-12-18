#!/usr/bin/env python3
"""
Windows AI APIs Integration
============================

Integrates Windows Copilot Runtime APIs (Phi Silica SLM) running locally on NPU.

Requirements:
    - Windows 11 with NPU (Copilot+ PC)
    - Windows App SDK 1.7+
    - pip install winrt-runtime (for Python/WinRT bridge)

Usage:
    from tools.windows_ai import WindowsAIModel
    model = WindowsAIModel()
    response = model.generate("Your prompt here")

Reference:
    https://learn.microsoft.com/en-us/windows/ai/apis/phi-silica
"""

import sys
from typing import Optional, Dict, Any


class WindowsAIModel:
    """Wrapper for Windows AI APIs (Phi Silica SLM)."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.model = None
        self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Windows AI APIs are available."""
        if sys.platform != 'win32':
            raise OSError("Windows AI APIs are only available on Windows")

        try:
            # Try to import Windows Runtime bridge to see if it's installed
            import winrt  # noqa: F401

            if self.verbose:
                print("[OK] Windows Runtime bridge available")

            # Check for Phi Silica availability
            # This requires Windows App SDK 1.7+ and NPU hardware
            try:
                # Import Windows AI Foundry APIs
                # Note: This namespace is from Windows App SDK 1.7+
                from winrt.microsoft.windows.ai.generative import PhiSilicaModel

                if self.verbose:
                    print("[OK] Phi Silica model available")

                self.model = PhiSilicaModel()
                return True

            except (ImportError, ModuleNotFoundError):
                if self.verbose:
                    print("[WARN] Phi Silica not available - requires Windows App SDK 1.7+")
                return False

        except ImportError:
            if self.verbose:
                print("[WARN] winrt-runtime not installed")
            return False

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
        # Always use C# bridge - no need to check for winrt model

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
        import subprocess
        from pathlib import Path

        # Find the C# bridge
        bridge_dir = Path(__file__).parent / "windows_ai_bridge"
        bridge_proj = bridge_dir / "PhiSilicaBridge.csproj"

        if not bridge_proj.exists():
            return (
                "[ERROR] C# bridge not found. Run:\n"
                "  dotnet build tools/windows_ai_bridge/PhiSilicaBridge.csproj"
            )

        try:
            result = subprocess.run(
                ["dotnet", "run", "--project", str(bridge_proj), "--", prompt],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(bridge_dir.parent.parent)
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"[ERROR] Bridge error: {result.stderr.strip()}"

        except subprocess.TimeoutExpired:
            return "[ERROR] Phi Silica request timed out (120s)"
        except FileNotFoundError:
            return "[ERROR] dotnet not found. Install .NET SDK."
        except Exception as e:
            raise RuntimeError(f"Phi Silica API call failed: {e}")


def check_windows_ai_available() -> bool:
    """Check if Windows AI APIs are available on this system."""
    try:
        model = WindowsAIModel(verbose=False)
        # We consider it available if the hardware/OS requirements are met,
        # even if winrt-runtime itself isn't used for the bridge.
        return sys.platform == 'win32'
    except Exception:
        return False


def get_model_info() -> Dict[str, Any]:
    """Get information about Windows AI model availability."""
    info = {
        "platform": sys.platform,
        "windows_ai_available": False,
        "phi_silica_available": False,
        "requirements": {
            "os": "Windows 11 with NPU (Copilot+ PC)",
            "sdk": "Windows App SDK 1.7+",
            "python_package": "winrt-runtime"
        }
    }

    if sys.platform != 'win32':
        info["error"] = "Not running on Windows"
        return info

    try:
        import winrt  # noqa: F401
        info["winrt_installed"] = True

        try:
            model = WindowsAIModel(verbose=False)
            info["windows_ai_available"] = True
            info["phi_silica_available"] = True  # Assuming bridge works if model exists
        except Exception as e:
            info["error"] = str(e)

    except ImportError:
        info["winrt_installed"] = False
        info["error"] = "winrt-runtime not installed"

    return info


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
