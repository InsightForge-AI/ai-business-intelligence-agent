"""
==========================================================
Agent API Tests
==========================================================

Tests the Agent API endpoints.
"""

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


# ---------------------------------------------------------
# Health Endpoint
# ---------------------------------------------------------

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["module"] == "agent"

    assert data["status"] == "healthy"


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


# ---------------------------------------------------------
# Agent Analyze
# ---------------------------------------------------------

def test_agent_analyze():

    payload = {

        "query": "Analyze the quarterly sales report.",

        "metadata": {

            "file_type": "pdf",

            "document_type": "business_report"

        }

    }

    response = client.post(

        "/agent/analyze",

        json=payload

    )

    assert response.status_code == 200

    data = response.json()

    assert data["module"] == "agent"

    assert data["success"] is True

    assert "intent" in data

    assert "selected_modules" in data

    assert "execution_order" in data

    assert "message" in data


# ---------------------------------------------------------
# Invalid Request
# ---------------------------------------------------------

def test_invalid_request():

    payload = {

        "metadata": {}

    }

    response = client.post(

        "/agent/analyze",

        json=payload

    )

    assert response.status_code == 422