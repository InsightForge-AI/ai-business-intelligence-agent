from fastapi.testclient import TestClient
from app import app
import io

client = TestClient(app)


def test_upload():
    """
    Regression guard: this test used to POST to "/upload", which 404s
    because backend/api/routes.py registers everything under the "/api"
    prefix -- the real route is "/api/upload". Fixed to hit the actual
    endpoint.
    """

    pdf_content = b"%PDF-1.4 test pdf"

    response = client.post(

        "/api/upload",

        files={
            "file": (

                "sample.pdf",

                io.BytesIO(pdf_content),

                "application/pdf"
            )
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["type"] == ".pdf"
    assert body["data"]["file_path"]


def test_upload_rejects_unsupported_extension():

    response = client.post(

        "/api/upload",

        files={
            "file": (
                "payload.exe",
                io.BytesIO(b"MZ..."),
                "application/octet-stream",
            )
        }
    )

    assert response.status_code == 400


def test_upload_missing_file_returns_422():

    response = client.post("/api/upload")

    assert response.status_code == 422
