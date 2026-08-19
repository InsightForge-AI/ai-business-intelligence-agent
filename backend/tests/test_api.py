"""
Smoke test for the top-level app's root endpoint.

backend/app.py also conditionally mounts a local-only frontend at /ui if
frontend/webpage/ exists on disk -- that directory is untracked (see
.gitignore) and not part of this repo, so it's deliberately not tested
here: on a fresh clone it won't exist, and asserting on it would fail
for everyone except whoever has that folder locally.
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root_reports_running_status():
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "running"
