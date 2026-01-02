import subprocess

# Your prompt (the error message)
prompt = """
PS D:\\source\\prompts> & D:/source/prompts/.venv/Scripts/Activate.ps1
(.venv) PS D:\\source\\prompts> & D:/source/prompts/.venv/Scripts/python.exe c:/Users/tandf/.vscode/extensions/ms-python.vscode-pylance-2025.10.4/dist/typeshed-fallback/stdlib/builtins.pyi
Traceback (most recent call last):
  File "c:\\Users\\tandf\\.vscode\\extensions\\ms-python.vscode-pylance-2025.10.4\\dist\\typeshed-fallback\\stdlib\\builtins.pyi", line 7, in <module>
    from _typeshed import (
    ...<24 lines>...
    )
ImportError: cannot import name 'AnnotationForm' from '_typeshed' (unknown location)
(.venv) PS D:\\source\\prompts> & D:/source/prompts/.venv/Scripts/python.exe c:/Users/tandf/.vscode/extensions/ms-python.vscode-pylance-2025.10.4/dist/typeshed-fallback/stdlib/builtins.pyi
Traceback (most recent call last):
  File "c:\\Users\\tandf\\.vscode\\extensions\\ms-python.vscode-pylance-2025.10.4\\dist\\typeshed-fallback\\stdlib\\builtins.pyi", line 7, in <module>
    from _typeshed import (
    ...<24 lines>...
    )
ImportError: cannot import name 'AnnotationForm' from '_typeshed' (unknown location)
"""

# Replace <model> with your actual model name, e.g., gpt-4o-mini
model = "gpt-4o-mini"

# Run the gh models command
result = subprocess.run(
    ["gh", "models", "run", model, "--prompt", prompt],
    capture_output=True,
    text=True
)

print("Model response:\n", result.stdout)