import requests

urls = [
    "http://127.0.0.1:5050/",
    "http://127.0.0.1:5050/api/workflows",
    "http://127.0.0.1:5050/api/runs",
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
