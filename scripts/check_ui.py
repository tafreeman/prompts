import requests
import os

# Default to 8010, can override with env var
PORT = os.environ.get("UI_PORT", "8010")
BASE_URL = f"http://127.0.0.1:{PORT}"

urls = [
    f"{BASE_URL}/",
    f"{BASE_URL}/api/workflows",
    f"{BASE_URL}/api/runs",
]

for u in urls:
    try:
        r = requests.get(u, timeout=5)
        print(f"{u} -> {r.status_code}")
        if "application/json" in r.headers.get("Content-Type", ""):
            print(r.json())
        else:
            print(r.text[:200])
    except Exception as e:
        print(f"{u} -> ERROR: {e}")
