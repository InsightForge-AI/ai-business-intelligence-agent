"""
QA test suite for the Backend integration layer (POST /analyze).

Downstream services (agent/nlp/ml/rag/cv) are mocked at the network
boundary so this suite runs standalone -- no other service needs to be
running. Every service file does `import requests; requests.post(...)`,
and `requests` is a single shared module object across the whole process,
so all five service modules' `.post` are literally the same function.
Patching them independently in one `with` block silently collides (the
last patch wins for everyone) -- this suite instead patches
`requests.post` exactly once with a single side_effect keyed by target
URL, which is the only way to give each service its own canned response.

This suite originally documented several live bugs found during a QA
pass: an illusory per-module timeout (ThreadPoolExecutor.__exit__ blocked
on the full real duration of a hung call), zero timeout= on any outbound
request, a CORS policy that granted credentialed access to any origin,
and a CV "upload" pipeline that never actually carried file bytes from
the frontend to the backend. All were fixed; this file now verifies the
fixed behavior and guards against regressions.
"""

import base64
import inspect
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))  # main.py/app.* import as `from app...`

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
import config  # noqa: E402

client = TestClient(app)


def _mock_response(json_body, status_code=200):
    resp = MagicMock()
    resp.json.return_value = json_body
    resp.status_code = status_code
    return resp


def _router(by_url, default=None, on_call=None):
    """Build a requests.post side_effect that dispatches on the target URL."""
    def _fn(url, *args, **kwargs):
        if on_call:
            on_call(url, *args, **kwargs)
        if url in by_url:
            behavior = by_url[url]
            if isinstance(behavior, Exception):
                raise behavior
            # NOTE: MagicMock instances (our canned responses) are themselves
            # callable, so a plain `callable(behavior)` check would invoke
            # them instead of returning them. Only real plain functions
            # (used for side-effect callbacks like `_slow_nlp` below) should
            # be called here.
            if inspect.isfunction(behavior):
                return behavior(*args, **kwargs)
            return behavior
        if default is not None:
            return default
        raise AssertionError(f"Unexpected requests.post call to {url}")
    return _fn


class TestAnalyzeOrchestration:

    def test_single_module_string_route(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("nlp"),
                config.NLP_API_URL: _mock_response(
                    {"sentiment": "positive", "summary": "s", "keywords": ["k"]}
                ),
            })
            r = client.post("/analyze", json={"query": "great product"})
            assert r.status_code == 200
            body = r.json()
            assert body["agent"] == ["nlp"]
            assert body["module_results"]["nlp"]["sentiment"] == "positive"
            assert body["status"] == "success"

    def test_multi_module_list_route(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response(["nlp", "cv"]),
                config.NLP_API_URL: _mock_response({"sentiment": "neutral"}),
                config.CV_API_URL: _mock_response({"objects": []}),
            })
            r = client.post("/analyze", json={"query": "product image review"})
            body = r.json()
            assert set(body["agent"]) == {"nlp", "cv"}
            assert "nlp" in body["module_results"]
            assert "cv" in body["module_results"]

    def test_agent_dict_with_action_key(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response({"action": "rag"}),
                config.RAG_API_URL: _mock_response(
                    {"content": ["doc"], "total_results": 1}
                ),
            })
            r = client.post("/analyze", json={"query": "search policy"})
            assert r.json()["agent"] == ["rag"]

    def test_agent_dict_without_action_falls_back_to_nlp(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response({"unexpected": "shape"}),
                config.NLP_API_URL: _mock_response({"sentiment": "neutral"}),
            })
            r = client.post("/analyze", json={"query": "hello"})
            assert r.json()["agent"] == ["nlp"]

    def test_unimplemented_module_reports_error_but_200(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("not_a_real_module"),
            })
            r = client.post("/analyze", json={"query": "x"})
            assert r.status_code == 200
            assert r.json()["module_results"]["not_a_real_module"] == {
                "error": "module not implemented"
            }

    def test_downstream_exception_is_contained_per_module(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("nlp"),
                config.NLP_API_URL: ConnectionError("service unreachable"),
            })
            r = client.post("/analyze", json={"query": "x"})
            assert r.status_code == 200
            assert "service unreachable" in r.json()["module_results"]["nlp"]["error"]
            assert r.json()["status"] == "success"  # per-module failure, not global

    def test_agent_service_itself_unreachable_returns_critical_fallback(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: ConnectionError("agent down"),
            })
            r = client.post("/analyze", json={"query": "x"})
            assert r.status_code == 200
            body = r.json()
            assert body["status"] == "error"
            assert body["agent"] == ["nlp"]

    def test_empty_query_still_calls_agent_with_empty_string(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("nlp"),
                config.NLP_API_URL: _mock_response({"sentiment": "neutral"}),
            })
            r = client.post("/analyze", json={"query": "   "})
            assert r.status_code == 200
            assert r.json()["query"] == ""

    def test_missing_query_field_returns_422(self):
        r = client.post("/analyze", json={})
        assert r.status_code == 422

    def test_payload_over_the_size_cap_is_rejected(self):
        # MaxBodySizeMiddleware in backend/main.py caps requests at 15MB
        # (sized for a base64-encoded image plus JSON overhead); this used
        # to have no limit at all.
        r = client.post("/analyze", json={"query": "x" * (16 * 1024 * 1024)})
        assert r.status_code == 413


class TestTimeoutProtectionIsNowReal:
    """
    Originally, execute_with_timeout() used
    `with ThreadPoolExecutor() as executor: ... future.result(timeout=5)`.
    That looked safe but wasn't: ThreadPoolExecutor.__exit__ calls
    shutdown(wait=True), which blocks until the still-running worker
    thread actually finishes -- so a hung call delayed the response by
    its full real duration, not 5 seconds. Fixed by not using the
    executor as a context manager and calling shutdown(wait=False) in a
    `finally` instead, so future.result(timeout=...) timing out actually
    lets the response return on schedule. Every backend service call also
    now passes timeout=REQUEST_TIMEOUT to requests.post().
    """

    def test_slow_downstream_call_is_now_bounded_near_the_timeout(self):
        SLEEP_SECONDS = 7  # > REQUEST_TIMEOUT (5)

        def _slow_nlp(*args, **kwargs):
            time.sleep(SLEEP_SECONDS)
            return _mock_response({"sentiment": "positive"})

        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("nlp"),
                config.NLP_API_URL: _slow_nlp,
            })
            start = time.time()
            r = client.post("/analyze", json={"query": "slow"})
            elapsed = time.time() - start

        assert r.status_code == 200
        assert r.json()["module_results"]["nlp"]["error"] == "nlp timeout"
        assert elapsed < config.REQUEST_TIMEOUT + 2, (
            f"Response took {elapsed:.1f}s -- expected it to return close to "
            f"REQUEST_TIMEOUT ({config.REQUEST_TIMEOUT}s), not wait out the "
            f"full {SLEEP_SECONDS}s of the slow call. The executor.shutdown"
            f"(wait=False) fix may have regressed."
        )

    @pytest.mark.parametrize("service_module,url_attr", [
        ("app.services.agent_service", "AGENT_API_URL"),
        ("app.services.nlp_service", "NLP_API_URL"),
        ("app.services.ml_service", "ML_API_URL"),
        ("app.services.rag_service", "RAG_API_URL"),
    ])
    def test_every_service_call_passes_an_explicit_timeout(self, service_module, url_attr):
        import importlib
        mod = importlib.import_module(service_module)
        run_fn = next(
            getattr(mod, name) for name in dir(mod)
            if name.startswith("run_") and callable(getattr(mod, name))
        )
        with patch("requests.post") as mock_post:
            mock_post.return_value = _mock_response({"ok": True})
            run_fn("some query")
            _, kwargs = mock_post.call_args
            assert kwargs.get("timeout") == config.REQUEST_TIMEOUT, (
                f"{service_module}.{run_fn.__name__} did not pass "
                f"timeout={config.REQUEST_TIMEOUT} to requests.post -- a "
                f"hung real downstream service would block indefinitely."
            )

    def test_cv_service_call_passes_an_explicit_timeout(self):
        from app.services.cv_service import run_cv
        with patch("requests.post") as mock_post:
            mock_post.return_value = _mock_response({"ok": True})
            run_cv("photo.png", base64.b64encode(b"x").decode())
            _, kwargs = mock_post.call_args
            assert kwargs.get("timeout") == config.REQUEST_TIMEOUT


class TestCvUploadPipelineIsFixed:
    """
    Originally the frontend sent `{ query, file: file?.name }` as JSON --
    never the actual bytes -- and AnalyzeRequest only declared `query`,
    so `file` was silently dropped by Pydantic. CV then received the raw
    chat text and tried to treat it as a filesystem path, so image
    analysis could never succeed through the chat UI under any real
    usage. Fixed: AnalyzeRequest now carries optional file_name/file_data
    (base64) fields, the frontend reads the attached File and sends its
    real bytes that way, and cv_service.run_cv() forwards the decoded
    bytes to the CV service as a real multipart upload instead of
    treating query text as a path.
    """

    def test_file_bytes_reach_the_cv_service_as_a_real_upload(self):
        captured = {}

        def _capture_cv_call(*args, **kwargs):
            captured["files"] = kwargs.get("files")
            return _mock_response({"status": "success", "result": {"format": "PNG"}})

        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("cv"),
                config.CV_API_URL: _capture_cv_call,
            })
            file_bytes = b"not a real png but bytes are what we're checking"
            r = client.post(
                "/analyze",
                json={
                    "query": "analyze this image",
                    "file_name": "product_photo.png",
                    "file_data": base64.b64encode(file_bytes).decode(),
                },
            )
            assert r.status_code == 200
            assert r.json()["module_results"]["cv"]["status"] == "success"

            assert "files" in captured and captured["files"] is not None
            sent_name, sent_bytes, _content_type = captured["files"]["file"]
            assert sent_name == "product_photo.png"
            assert sent_bytes == file_bytes, (
                "The actual uploaded bytes must reach the CV service -- "
                "this is the core of the original broken pipeline."
            )

    def test_cv_routed_with_no_file_gives_a_clear_error_not_a_path_guess(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("cv"),
            })
            r = client.post("/analyze", json={"query": "analyze this image"})
            assert r.status_code == 200
            assert r.json()["module_results"]["cv"]["error"] == "No image file was uploaded"

    def test_invalid_base64_file_data_is_handled_cleanly(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = _router({
                config.AGENT_API_URL: _mock_response("cv"),
            })
            r = client.post(
                "/analyze",
                json={
                    "query": "analyze this image",
                    "file_name": "x.png",
                    "file_data": "not valid base64 !!!",
                },
            )
            assert r.status_code == 200
            assert "base64" in r.json()["module_results"]["cv"]["error"].lower()


class TestCorsIsRestricted:
    """
    Originally allow_origins=["*"] + allow_credentials=True made Starlette
    reflect back *any* incoming Origin with credentials allowed --
    effectively no CORS protection. Fixed to an explicit origin allowlist
    (matching the frontend's actual static server) with credentials off.
    """

    def test_untrusted_origin_is_not_granted_access(self):
        r = client.options(
            "/analyze",
            headers={
                "Origin": "https://evil.example.com",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert r.headers.get("access-control-allow-origin") != "https://evil.example.com"

    def test_known_frontend_origin_is_allowed(self):
        r = client.options(
            "/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert r.headers.get("access-control-allow-origin") == "http://localhost:3000"
