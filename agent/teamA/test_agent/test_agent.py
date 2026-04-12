"""
Unit tests for Agent Team A - API Contract Compliance
Tests ensure the agent correctly routes queries to NLP, ML, or CV services
"""

import importlib
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


client = TestClient(app)


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
        assert response.status_code == 200
        assert response.json()["action"] == "nlp"

    def test_route_sentiment_query_to_nlp(self):
        """Query with 'sentiment' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "what is the sentiment?"})
        assert response.status_code == 200
        assert response.json()["action"] == "nlp"

    def test_route_text_query_to_nlp(self):
        """Query with 'text' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "analyze this text"})
        assert response.status_code == 200
        assert response.json()["action"] == "nlp"

    def test_route_feedback_query_to_nlp(self):
        """Query with 'feedback' should route to NLP"""
        response = client.post("/agent/analyze", json={"query": "show customer feedback"})
        assert response.status_code == 200
        assert response.json()["action"] == "nlp"


class TestAgentAnalyzeML:
    """Tests for ML routing"""

    def test_route_sales_query_to_ml(self):
        """Query with 'sales' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "show sales data"})
        assert response.status_code == 200
        assert response.json()["action"] == "ml"

    def test_route_revenue_query_to_ml(self):
        """Query with 'revenue' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "analyze revenue trends"})
        assert response.status_code == 200
        assert response.json()["action"] == "ml"

    def test_route_data_query_to_ml(self):
        """Query with 'data' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "process this data"})
        assert response.status_code == 200
        assert response.json()["action"] == "ml"

    def test_route_analytics_query_to_ml(self):
        """Query with 'analytics' should route to ML"""
        response = client.post("/agent/analyze", json={"query": "run analytics"})
        assert response.status_code == 200
        assert response.json()["action"] == "ml"


class TestAgentAnalyzeCV:
    """Tests for CV routing"""

    def test_route_image_query_to_cv(self):
        """Query with 'image' should route to CV"""
        response = client.post("/agent/analyze", json={"query": "analyze this image"})
        assert response.status_code == 200
        assert response.json()["action"] == "cv"

    def test_route_photo_query_to_cv(self):
        """Query with 'photo' should route to CV"""
        response = client.post("/agent/analyze", json={"query": "process this photo"})
        assert response.status_code == 200
        assert response.json()["action"] == "cv"

    def test_route_visual_query_to_cv(self):
        """Query with 'visual' should route to CV"""
        response = client.post("/agent/analyze", json={"query": "visual analysis"})
        assert response.status_code == 200
        assert response.json()["action"] == "cv"


class TestAgentAnalyzeUnknown:
    """Tests for unknown routing"""

    def test_route_unknown_query(self):
        """Query with no matching keywords should route to unknown"""
        response = client.post("/agent/analyze", json={"query": "hello world"})
        assert response.status_code == 200
        assert response.json()["action"] == "unknown"

    def test_route_random_query_to_unknown(self):
        """Random query should route to unknown"""
        response = client.post("/agent/analyze", json={"query": "what is the weather"})
        assert response.status_code == 200
        assert response.json()["action"] == "unknown"


class TestAgentAnalyzeErrors:
    """Tests for error handling"""

    def test_empty_query_returns_error(self):
        """Empty query should return 400 error"""
        response = client.post("/agent/analyze", json={"query": ""})
        assert response.status_code == 400

    def test_response_has_action_field(self):
        """Response should always have 'action' field"""
        response = client.post("/agent/analyze", json={"query": "test query"})
        data = response.json()
        assert "action" in data


class TestAPIContract:
    """Tests to ensure API Contract compliance"""

    def test_response_format_matches_contract(self):
        """Response must follow API Contract: { "action": "..." }"""
        response = client.post("/agent/analyze", json={"query": "analyze reviews"})
        data = response.json()
        assert set(data.keys()) == {"action"}
        assert data["action"] in ["nlp", "ml", "cv", "unknown"]

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
