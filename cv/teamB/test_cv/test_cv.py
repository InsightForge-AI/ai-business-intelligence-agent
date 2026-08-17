"""
QA test suite for CV Team B.

Covers the (now-fixed) image_analysis logic and the POST /cv/analyze
contract, including a path-traversal regression guard for the upload
handler.

History: this suite originally documented three live bugs found during a
QA pass -- (1) image_analysis.py had three duplicate `analyze_image`
definitions where only a hardcoded fake stub survived, (2) the upload
folder was resolved relative to the process CWD instead of the module's
own location, and (3) the uploaded filename was used unsanitized,
allowing "../../evil.png" to write outside the upload folder entirely
(reproduced live: a real file landed in the repo root). All three were
fixed in cv/teamB/src/image_analysis.py and cv/teamB/api/main.py. Tests
below verify the fixed behavior and guard against regressions.
"""

import io
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

CV_TEAMB_DIR = REPO_ROOT / "cv" / "teamB"
UPLOAD_DIR = CV_TEAMB_DIR / "api" / "temp"  # matches Path(__file__).parent / "temp" in main.py


def _make_png_bytes(size=(4, 3), color=(255, 0, 0)) -> bytes:
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", size, color=color).save(buf, format="PNG")
    return buf.getvalue()


TINY_PNG = _make_png_bytes()


class TestImageAnalysisIsReal:

    def test_single_definition_no_dead_code(self):
        import inspect
        from cv.teamB.src import image_analysis
        # Exactly one `analyze_image` in the module's source -- guards
        # against the duplicate-definition pattern that silently shadowed
        # the real implementation before.
        source = inspect.getsource(image_analysis)
        assert source.count("def analyze_image") == 1

    def test_returns_real_dimensions_and_format(self, tmp_path):
        from cv.teamB.src.image_analysis import analyze_image
        img_path = tmp_path / "sample.png"
        img_path.write_bytes(_make_png_bytes(size=(10, 5)))

        result = analyze_image(img_path)
        assert result["width"] == 10
        assert result["height"] == 5
        assert result["format"] == "PNG"

    def test_different_images_produce_different_results(self, tmp_path):
        from cv.teamB.src.image_analysis import analyze_image
        a = tmp_path / "a.png"
        b = tmp_path / "b.png"
        a.write_bytes(_make_png_bytes(size=(10, 10)))
        b.write_bytes(_make_png_bytes(size=(50, 20)))

        result_a = analyze_image(a)
        result_b = analyze_image(b)
        assert result_a != result_b, (
            "Two different images produced identical analysis output -- "
            "this was the original stub bug; it must not resurface."
        )

    def test_object_detection_and_ocr_are_honestly_unimplemented(self, tmp_path):
        # No model exists for either in this repo. The result must say so
        # rather than fabricate plausible-looking fake data.
        from cv.teamB.src.image_analysis import analyze_image
        img_path = tmp_path / "sample.png"
        img_path.write_bytes(TINY_PNG)
        result = analyze_image(img_path)
        assert result["objects"] == []
        assert result["extracted_text"] is None


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from cv.teamB.api.main import app
    return TestClient(app)


@pytest.fixture(autouse=True)
def _cleanup_uploaded_temp_files():
    # main.py now deletes each upload after processing it, but sweep any
    # leftovers (e.g. from a test that fails before reaching that code)
    # so this suite never leaves scratch files behind.
    yield
    if UPLOAD_DIR.exists():
        for f in UPLOAD_DIR.iterdir():
            f.unlink(missing_ok=True)


class TestCvApiContract:

    def test_no_file_returns_not_found(self, client):
        r = client.post("/cv/analyze")
        assert r.status_code == 200
        assert r.json()["message"] == "not found"

    def test_valid_png_returns_real_metadata(self, client):
        r = client.post(
            "/cv/analyze",
            files={"file": ("photo.png", io.BytesIO(TINY_PNG), "image/png")},
        )
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "success"
        assert body["result"]["format"] == "PNG"
        assert body["result"]["width"] > 0 and body["result"]["height"] > 0

    def test_uploaded_file_is_cleaned_up_after_processing(self, client):
        r = client.post(
            "/cv/analyze",
            files={"file": ("cleanup_check.png", io.BytesIO(TINY_PNG), "image/png")},
        )
        assert r.status_code == 200
        assert not (UPLOAD_DIR / "cleanup_check.png").exists(), (
            "Uploaded file should be deleted after processing, not left "
            "to accumulate in the upload folder indefinitely."
        )

    def test_invalid_extension_rejected(self, client):
        r = client.post(
            "/cv/analyze",
            files={"file": ("payload.exe", io.BytesIO(b"MZ..."), "application/octet-stream")},
        )
        assert r.status_code == 200
        assert r.json()["message"] == "Invalid format"

    def test_empty_file_rejected(self, client):
        r = client.post(
            "/cv/analyze",
            files={"file": ("empty.png", io.BytesIO(b""), "image/png")},
        )
        assert r.status_code == 200
        assert r.json()["message"] == "Empty file"

    def test_corrupt_image_bytes_rejected(self, client):
        r = client.post(
            "/cv/analyze",
            files={"file": ("fake.jpg", io.BytesIO(b"not actually a jpeg"), "image/jpeg")},
        )
        assert r.status_code == 200
        assert r.json()["message"] == "Corrupt image"

    def test_upload_under_the_size_cap_is_accepted(self, client):
        under_cap = TINY_PNG + b"\x00" * (5 * 1024 * 1024)  # ~5MB, cap is 10MB
        r = client.post(
            "/cv/analyze",
            files={"file": ("big.png", io.BytesIO(under_cap), "image/png")},
        )
        assert r.status_code == 200

    def test_upload_over_the_size_cap_is_rejected(self, client):
        # MaxBodySizeMiddleware in cv/teamB/api/main.py caps requests at
        # 10MB; this used to have no limit at all.
        over_cap = TINY_PNG + b"\x00" * (11 * 1024 * 1024)
        r = client.post(
            "/cv/analyze",
            files={"file": ("huge.png", io.BytesIO(over_cap), "image/png")},
        )
        assert r.status_code == 413

    def test_path_traversal_filename_is_now_blocked(self, client):
        """
        Regression guard for the arbitrary-file-write bug fixed in
        cv/teamB/api/main.py: file_path = UPLOAD_DIR / Path(file.filename).name
        now strips any directory components from the untrusted filename,
        and UPLOAD_DIR is anchored to the module's own directory instead
        of the process CWD. Confirms uploading "../marker.png" no longer
        escapes anywhere -- not to the CWD-relative old location, not to
        the repo root, not anywhere outside UPLOAD_DIR.
        """
        marker_name = "cv_qa_traversal_marker.png"
        candidate_escape_targets = [
            REPO_ROOT / marker_name,
            REPO_ROOT.parent / marker_name,
            CV_TEAMB_DIR / marker_name,
            Path.cwd() / marker_name,
            Path.cwd().parent / marker_name,
        ]
        for target in candidate_escape_targets:
            target.unlink(missing_ok=True)

        try:
            r = client.post(
                "/cv/analyze",
                files={
                    "file": (
                        f"../{marker_name}",
                        io.BytesIO(TINY_PNG),
                        "image/png",
                    )
                },
            )
            assert r.status_code == 200
            # The traversal-y filename is sanitized to its basename and
            # processed normally -- not rejected, just contained.
            assert r.json()["status"] == "success"

            for target in candidate_escape_targets:
                assert not target.exists(), (
                    f"PATH TRAVERSAL REGRESSION: uploading filename "
                    f"'../{marker_name}' wrote a file to {target}, outside "
                    f"the upload directory."
                )
        finally:
            for target in candidate_escape_targets:
                target.unlink(missing_ok=True)
            (UPLOAD_DIR / marker_name).unlink(missing_ok=True)
