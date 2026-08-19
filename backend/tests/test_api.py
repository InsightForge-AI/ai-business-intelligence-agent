"""
Smoke tests for the top-level app: the root endpoint and the bundled
frontend mounted at /ui (backend/app.py).
"""

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root_reports_running_status():
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "running"
    assert body["ui"] == "/ui"


def test_ui_serves_index_html():
    response = client.get("/ui/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "DocuMind" in response.text


def test_ui_serves_static_assets():
    response = client.get("/ui/app.js")

    assert response.status_code == 200
    assert "/api/documents" in response.text
