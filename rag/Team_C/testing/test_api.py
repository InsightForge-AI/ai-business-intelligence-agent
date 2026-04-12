import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_rag_query():

    payload = {
        "query": "delivery delay",
        "top_k": 2
    }

    response = client.post("/rag/query", json=payload)

    # Check status
    assert response.status_code == 200

    data = response.json()

    # Check structure
    assert "context" in data
    assert isinstance(data["context"], dict)

    assert "query" in data["context"]
    assert "results" in data["context"]
    assert isinstance(data["context"]["results"], list)