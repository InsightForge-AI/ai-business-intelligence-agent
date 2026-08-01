from fastapi.testclient import TestClient
from app import app
import io

client = TestClient(app)


def test_upload():

    pdf_content = b"%PDF-1.4 test pdf"

    response = client.post(

        "/upload",

        files={
            "file": (

                "sample.pdf",

                io.BytesIO(pdf_content),
                
                "application/pdf"
            )
        }
    )

    assert response.status_code == 200