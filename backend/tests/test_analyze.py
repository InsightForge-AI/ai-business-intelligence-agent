from fastapi.testclient import (
    TestClient
)

from app import app

client = TestClient(app)


def test_analyze():

    response = client.post(

        "/analyze",

        json={

            "file_id":"123",

            "file_name":"report.pdf",

            "file_path":"temp_uploads/report.pdf",

            "query":"Summarize report"
        }
    )

    assert (

        response.status_code == 200
    )
