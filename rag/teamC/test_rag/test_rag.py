"""
QA test suite for RAG Team C.
Covers simple_search()/synonym expansion and the POST /rag/query contract.
Central finding: this "RAG" service has no retrieval backend at all -- it
matches against four hardcoded strings in search.py. These tests both
verify the documented behavior AND make that limitation impossible to miss.
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from rag.teamC.src.search import simple_search, expand_query_words, documents  # noqa: E402


class TestSimpleSearch:

    def test_direct_keyword_match(self):
        results = simple_search("delivery")
        ids = {r["id"] for r in results}
        assert 1 in ids and 2 in ids and 4 in ids

    def test_no_match_returns_empty_list(self):
        assert simple_search("quantum blockchain synergy") == []

    def test_empty_query_returns_empty_list(self):
        assert simple_search("") == []
        assert simple_search("   ") == []

    def test_results_sorted_by_score_descending(self):
        results = simple_search("sales delivery")
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_the_entire_corpus_is_four_hardcoded_sentences(self):
        """
        Documents the actual scale of the "knowledge base": exactly 4
        static strings baked into source code, not a real document store,
        index, or embedding search. Any claim of RAG/retrieval-over-real-
        documents should be treated as aspirational, not current behavior.
        """
        assert len(documents) == 4
        assert all(isinstance(d["text"], str) for d in documents)

    def test_synonym_expansion_causes_surprising_unrelated_matches(self):
        """
        "low" is wired as a synonym for "dropped" purely to satisfy a past
        test case (see the source comment "synonym rules to satisfy test
        cases"). That means any query containing the word "low" in an
        unrelated business sense (e.g. "low priority", "low stock") will
        spuriously match the sales-drop document. This test proves the
        collision exists rather than assuming it away.
        """
        results = simple_search("low priority ticket")
        matched_texts = {r["text"] for r in results}
        assert any("sales dropped" in t for t in matched_texts), (
            "Expected the 'low' -> 'dropped' synonym rule to spuriously "
            "match the unrelated 'low priority ticket' query."
        )

    def test_expand_query_words_is_case_sensitive(self):
        # SYNONYMS keys are lowercase; simple_search() lowercases first, but
        # expand_query_words() called directly does not -- a latent trap for
        # any future caller that doesn't pre-lowercase.
        assert expand_query_words(["Issue"]) == ["Issue"]
        assert set(expand_query_words(["issue"])) == {"issue", "complaining", "dissatisfaction"}

    def test_synonym_key_issue_has_a_single_definition(self):
        # SYNONYMS used to define "issue" twice; the dict literal silently
        # kept only the second value and the first was dead code. Cleaned
        # up to a single definition with the same effective (live) value --
        # this just guards against the duplicate resurfacing.
        from rag.teamC.src.search import SYNONYMS
        assert SYNONYMS["issue"] == ["complaining", "dissatisfaction"]

    def test_html_payload_does_not_crash(self):
        results = simple_search("<script>alert(1)</script> delivery")
        assert isinstance(results, list)


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from rag.teamC.api.main import app
    return TestClient(app)


class TestRagApiContract:

    def test_normal_query(self, client):
        r = client.post("/rag/query", json={"query": "delivery delay"})
        assert r.status_code == 200
        body = r.json()
        assert body["total_results"] > 0
        assert isinstance(body["content"], list)

    def test_empty_query_message(self, client):
        r = client.post("/rag/query", json={"query": ""})
        assert r.status_code == 200
        assert r.json()["message"] == "empty query"

    def test_no_match_message(self, client):
        r = client.post("/rag/query", json={"query": "spaceship warranty"})
        assert r.status_code == 200
        body = r.json()
        assert body["message"] == "not found"
        assert body["total_results"] == 0

    def test_missing_query_field_returns_422(self, client):
        r = client.post("/rag/query", json={})
        assert r.status_code == 422

    def test_query_under_the_size_cap_does_not_crash(self, client):
        r = client.post("/rag/query", json={"query": "delivery " * 20000})  # ~176KB, cap is 2MB
        assert r.status_code == 200

    def test_query_over_the_size_cap_is_rejected(self, client):
        # MaxBodySizeMiddleware in rag/teamC/api/main.py caps requests at
        # 2MB; this used to have no limit at all.
        r = client.post("/rag/query", json={"query": "x" * (3 * 1024 * 1024)})
        assert r.status_code == 413
