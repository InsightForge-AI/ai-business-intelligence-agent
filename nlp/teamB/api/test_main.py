from fastapi.testclient import TestClient
from teamB.api.main import app

client = TestClient(app)

def test_analyze_text():
    response = client.post(
        "/nlp/analyze",
        json={"text": "I love this product!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "summary" in data
    assert "keywords" in data
