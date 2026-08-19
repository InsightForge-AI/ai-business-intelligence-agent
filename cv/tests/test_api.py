"""
==========================================================
CV API Tests
==========================================================

Tests the API endpoints.
"""

from fastapi.testclient import TestClient

from app import app


client = TestClient(

    app

)


def test_health():
    """
    Test health endpoint.
    """

    response = client.get(

        "/cv/health"

    )

    assert response.status_code == 200

    assert response.json()["success"] is True


def test_analyze():
    """
    Test analyze endpoint.
    """

    payload = {

        "query": "Extract invoice details.",

        "content": "sample_data/invoice.png",

        "metadata": {}

    }

    response = client.post(

        "/cv/analyze",

        json=payload

    )

    assert response.status_code == 200

    data = response.json()

    assert data["module"] == "cv"

    assert data["success"] is True