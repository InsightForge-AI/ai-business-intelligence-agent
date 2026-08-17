from fastapi.testclient import TestClient
from app import app
import io

import fitz  # PyMuPDF

client = TestClient(app)


def _make_valid_pdf_bytes() -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Quarterly report: revenue is up 12%.")
    return doc.tobytes()


def _upload_sample_pdf():
    response = client.post(
        "/api/upload",
        files={
            "file": (
                "report.pdf",
                io.BytesIO(_make_valid_pdf_bytes()),
                "application/pdf",
            )
        },
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def test_analyze():
    """
    Regression guard: this test used to POST to "/analyze" with a JSON
    body -- both wrong. The real endpoint is
    POST /api/analyze/{document_id}?query=..., where document_id is a
    path parameter (not a JSON field) for an already-uploaded document.

    No downstream services (agent/ml/nlp/rag/cv, or Ollama) are running
    in this test environment. agent_service.run_agent() already handles
    that gracefully (httpx.RequestError -> a routing dict with no
    selected_modules), so orchestration_service.run_analysis() degrades
    to "No AI modules selected" instead of hanging or crashing -- this
    test asserts exactly that graceful-degradation contract.
    """

    document_id = _upload_sample_pdf()

    response = client.post(

        f"/api/analyze/{document_id}",

        params={"query": "Summarize report"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert "summary" in body
    assert "insights" in body


def test_analyze_missing_document_returns_404():

    response = client.post(
        "/api/analyze/00000000-0000-0000-0000-000000000000",
        params={"query": "Summarize report"},
    )

    assert response.status_code == 404


def test_analyze_non_uuid_document_id_returns_404():
    """
    Regression guard for the document_id path traversal fix (see
    utils/validator.py validate_document_id). Every real document_id is a
    uuid4() (services/storage_service.py); anything else -- including a
    path-traversal payload -- must be rejected before it's used to build
    a filesystem path, not silently accepted.
    """

    response = client.post(
        "/api/analyze/not-a-real-uuid",
        params={"query": "Summarize report"},
    )

    assert response.status_code == 404
