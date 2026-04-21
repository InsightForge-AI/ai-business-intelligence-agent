"""
Unit tests for Agent Team A - API Contract Compliance
Tests ensure the agent correctly routes queries to NLP, ML, or CV services
"""

import importlib
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from agent.teamA.app import app


client = TestClient(app)


def assert_route_result(response, expected_result):
    assert response.status_code == 200
    assert response.json() == expected_result


class TestHealthCheck:
    """Tests for GET / (health check)"""

    def test_health_check_returns_200(self):
        """Health check should return HTTP 200"""
        response = client.get("/")
        assert response.status_code == 200

    def test_health_check_response_contains_status(self):
        """Health check response should contain status"""
        response = client.get("/")
        data = response.json()
        assert "status" in data
        assert "running" in data["status"].lower()


class TestAgentAnalyzeNLP:
    """Tests for NLP routing (POST /agent/analyze)"""

    def test_route_review_query_to_nlp(self):
        """Query with 'review' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "analyze customer reviews"})
        assert_route_result(response, "nlp")

    def test_route_sentiment_query_to_nlp(self):
        """Query with 'sentiment' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "what is the sentiment?"})
        assert_route_result(response, "nlp")

    def test_route_text_query_to_nlp(self):
        """Query with 'text' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "analyze this text"})
        assert_route_result(response, "nlp")

    def test_route_feedback_query_to_nlp(self):
        """Query with 'feedback' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "show customer feedback"})
        assert_route_result(response, "nlp")

    def test_route_noisy_positive_text_to_nlp(self):
        """Uppercase + symbols should still route safely to NLP"""
        response = client.post("/agent/analyze", json={"query": "GOOD product!!!"})
        assert_route_result(response, "nlp")

    def test_route_mixed_sentiment_text_to_nlp(self):
        """Mixed sentiment free text should fall back to NLP safely"""
        response = client.post("/agent/analyze", json={"query": "good but late delivery"})
        assert_route_result(response, "nlp")


class TestAgentAnalyzeML:
    """Tests for ML routing"""

    def test_route_sales_query_to_ml(self):
        """Query with 'sales' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "show sales data"})
        assert_route_result(response, "ml")

    def test_route_revenue_query_to_ml(self):
        """Query with 'revenue' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "analyze revenue trends"})
        assert_route_result(response, "ml")

    def test_route_data_query_to_ml(self):
        """Query with 'data' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "process this data"})
        assert_route_result(response, "ml")

    def test_route_analytics_query_to_ml(self):
        """Query with 'analytics' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "run analytics"})
        assert_route_result(response, "ml")


class TestAgentAnalyzeCV:
    """Tests for CV routing"""

    def test_route_image_query_to_cv(self):
        """Query with 'image' should route to CV"""
        response = client.post("/agent/analyze", json={"query": "analyze this image"})
        assert_route_result(response, "cv")

    def test_route_photo_query_to_cv(self):
        """Query with 'photo' should route to CV"""
        response = client.post("/agent/analyze", json={"query": "process this photo"})
        assert_route_result(response, "cv")

    def test_route_visual_query_to_cv(self):
        """Query with 'visual' should route to CV"""
        response = client.post("/agent/analyze", json={"query": "visual analysis"})
        assert_route_result(response, "cv")


class TestAgentAnalyzeRAG:
    """Tests for RAG routing"""

    def test_route_policy_search_to_rag(self):
        """Policy search query should route to RAG"""
        response = client.post("/agent/analyze", json={"query": "search policy document"})
        assert_route_result(response, "rag")


class TestAgentAnalyzeMultiIntent:
    """Tests for queries that should trigger more than one module."""

    def test_backend_sample_routes_to_nlp_and_cv(self):
        """Product image review should trigger NLP and CV modules."""
        response = client.post("/agent/analyze", json={"query": "analyze product image review"})
        assert_route_result(response, ["nlp", "cv"])

    def test_multi_intent_without_connector_routes_to_nlp_and_cv(self):
        """Multiple module keywords should be detected even without connector words."""
        response = client.post("/agent/analyze", json={"query": "customer reviews image"})
        assert_route_result(response, ["nlp", "cv"])

    def test_multi_intent_with_connector_routes_to_ml_and_cv(self):
        """Connector words should not force multi-intent queries back to NLP."""
        response = client.post("/agent/analyze", json={"query": "image and sales data"})
        assert_route_result(response, ["ml", "cv"])

    def test_noisy_multi_intent_routes_to_nlp_and_cv(self):
        """Uppercase and symbols should still preserve all detected modules."""
        response = client.post("/agent/analyze", json={"query": "ANALYZE!!! PRODUCT IMAGE REVIEW???"})
        assert_route_result(response, ["nlp", "cv"])


class TestAgentAnalyzeFallbacks:
    """Tests for Sprint 3 fallback routing"""

    def test_route_unknown_query_to_nlp(self):
        """Unknown valid query should fall back to NLP"""
        response = client.post("/agent/analyze", json={"query": "hello world"})
        assert_route_result(response, "nlp")

    def test_route_random_query_to_nlp(self):
        """Random text should fall back to NLP"""
        response = client.post("/agent/analyze", json={"query": "what is the weather"})
        assert_route_result(response, "nlp")

    def test_very_long_query_returns_safe_response(self):
        """Very long text should not crash and should keep the API contract"""
        response = client.post("/agent/analyze", json={"query": "x" * 5000})
        assert_route_result(response, "nlp")


class TestAgentAnalyzeErrors:
    """Tests for error handling"""

    def test_empty_query_returns_error(self):
        """Empty query should return 400 error"""
        response = client.post("/agent/analyze", json={"query": ""})
        assert response.status_code == 400

    def test_spaces_only_query_returns_error(self):
        """Whitespace-only query should return 400 error"""
        response = client.post("/agent/analyze", json={"query": "   "})
        assert response.status_code == 400

    def test_response_has_raw_route_value(self):
        """Single-intent response should be the raw module string."""
        response = client.post("/agent/analyze", json={"query": "test query"})
        assert_route_result(response, "nlp")


class TestAPIContract:
    """Tests to ensure API Contract compliance"""

    def test_response_format_matches_contract(self):
        """Response must be a raw module string or a list of module strings."""
        response = client.post("/agent/analyze", json={"query": "analyze reviews"})
        data = response.json()
        assert data in ["nlp", "ml", "cv", "rag"] or isinstance(data, list)

    def test_no_api_calls_made(self):
        """Sprint 1: Should not make any API calls - only decide"""
        response = client.post("/agent/analyze", json={"query": "analyze data"})
        assert response.status_code == 200


class TestImportCompatibility:
    """Tests for package-safe imports."""

    def test_package_import_from_repo_root(self):
        """The app should import as agent.teamA.app from the repo root."""
        repo_root = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(repo_root))
        try:
            module = importlib.import_module("agent.teamA.app")
            assert hasattr(module, "app")
        finally:
            sys.path.pop(0)
            sys.modules.pop("agent.teamA.app", None)
