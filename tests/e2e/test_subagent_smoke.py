"""E2E smoke test template that demonstrates running a single "subagent"
in a mocked environment. This test starts a tiny HTTP server to act as the
external API, writes a small ad-hoc subagent runner script that POSTS to the
server, runs it as a subprocess and asserts the output.

How to run locally:
  pytest tests/e2e/test_subagent_smoke.py -q

This keeps the test self-contained (no external network calls).
"""
import json
import os
import socket
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest


class EchoHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body)
        except Exception:
            payload = {"raw": body.decode(errors="ignore")}
        resp = {"received": payload, "status": "ok"}
        resp_bytes = json.dumps(resp).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.end_headers()
        self.wfile.write(resp_bytes)

    def log_message(self, format, *args):
        # silence to keep test output clean
        pass


def run_temp_server(server: HTTPServer):
    try:
        server.serve_forever()
    except Exception:
        pass


def find_free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    addr = s.getsockname()
    s.close()
    return addr[1]


def make_subagent_script(path: Path):
    """Create a tiny subagent runner script that POSTs JSON to TARGET_URL env var
    and prints the JSON response. Uses only standard library so it's runnable
    in minimal CI images.
    """
    content = r"""
import os, sys, json, urllib.request

target = os.environ.get('TARGET_URL')
if not target:
    print('ERROR: TARGET_URL not set', file=sys.stderr)
    sys.exit(2)

payload = {"task_input": {"example": 123}}
req = urllib.request.Request(target, data=json.dumps(payload).encode('utf-8'),
                             headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=10) as resp:
    body = resp.read().decode('utf-8')
    print(body)
"""
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def test_subagent_runner_against_mock_api(tmp_path):
    port = find_free_port()

    server = HTTPServer(("127.0.0.1", port), EchoHandler)
    t = threading.Thread(target=run_temp_server, args=(server,), daemon=True)
    t.start()

    # write a tiny runner script to a temp directory
    script_path = tmp_path / "subagent_runner.py"
    make_subagent_script(script_path)

    env = dict(**{
        **os.environ.copy(),
        "TARGET_URL": f"http://127.0.0.1:{port}/invoke",
    })

    # run the subagent as a separate process to emulate real e2e execution
    proc = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, env=env)

    server.shutdown()
    t.join(timeout=1)

    assert proc.returncode == 0, f"Subagent process failed: {proc.stderr}"
    out = proc.stdout.strip()
    assert out, "Expected output from subagent"
    data = json.loads(out)
    assert data.get("status") == "ok"
    assert "received" in data
    assert data["received"].get("task_input", {}).get("example") == 123
