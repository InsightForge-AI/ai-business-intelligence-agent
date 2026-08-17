"""
QA test suite for NLP Team B.
Covers unit-level logic (sentiment/keywords/summarizer) and the HTTP contract
of POST /nlp/analyze, including edge cases a human reviewer skimming the code
is unlikely to catch by hand.
"""

import sys
from pathlib import Path

import pytest

# nlp/teamB/api/main.py imports itself as `from teamB.src...` (a bare, unqualified
# package name). That only resolves if the `nlp/` directory -- not the repo root --
# is on sys.path, which is exactly what `run.py` does by setting cwd=nlp before
# launching uvicorn. We replicate that here. See test_module_namespace_collision.py
# for why this bare-name import style is itself a QA finding.
NLP_DIR = Path(__file__).resolve().parents[2]  # .../nlp
sys.path.insert(0, str(NLP_DIR))

from teamB.src.sentiment import get_sentiment  # noqa: E402
from teamB.src.keywords import get_keywords  # noqa: E402
from teamB.src.summarizer import summarize  # noqa: E402


# ---------------------------------------------------------------------------
# Unit tests: sentiment
# ---------------------------------------------------------------------------

class TestSentiment:

    def test_positive(self):
        assert get_sentiment("This product is great and amazing") == "positive"

    def test_negative(self):
        assert get_sentiment("This is terrible and broken") == "negative"

    def test_neutral_on_no_signal_words(self):
        assert get_sentiment("The package arrived on Tuesday") == "neutral"

    def test_empty_string_is_neutral(self):
        assert get_sentiment("") == "neutral"

    def test_none_is_neutral(self):
        assert get_sentiment(None) == "neutral"

    def test_whitespace_only_is_neutral(self):
        assert get_sentiment("   \n\t  ") == "neutral"

    def test_mixed_via_but_connector(self):
        assert get_sentiment("good but late delivery") == "mixed"

    def test_mixed_when_both_present_without_but(self):
        assert get_sentiment("good and bad experience") == "mixed"

    def test_negation_not_good_flips_to_negative(self):
        # "not" + a positive word with no negative words: code special-cases
        # this to "negative". Confirms the current (fragile) negation heuristic.
        assert get_sentiment("not good") == "negative"

    def test_negation_not_bad_flips_to_positive(self):
        assert get_sentiment("not bad") == "positive"

    def test_negation_is_silently_ignored_once_mixed_triggers(self):
        # "but" is present and there's a positive word ("good"), so the code
        # takes the `mixed` branch *before* ever consulting the "not" flip.
        # A human reader tracing the logic top-down could easily miss that
        # negation handling is unreachable whenever "but" is also present.
        assert get_sentiment("not good but not bad") == "mixed"

    def test_case_and_punctuation_are_normalized(self):
        assert get_sentiment("GOOD!!! Product... AMAZING!!") == "positive"

    def test_html_payload_does_not_crash_and_is_treated_as_text(self):
        result = get_sentiment("<script>alert(1)</script> good product")
        assert result in {"positive", "neutral", "mixed", "negative"}

    def test_very_long_input_does_not_crash(self):
        text = "good " * 20000  # 100k chars
        assert get_sentiment(text) == "positive"

    def test_non_string_input_is_coerced_not_crashed(self):
        # preprocess_text does str(text), so ints/lists must not raise.
        assert get_sentiment(12345) == "neutral"


# ---------------------------------------------------------------------------
# Unit tests: keywords
# ---------------------------------------------------------------------------

class TestKeywords:

    def test_extracts_non_stopwords_in_order_deduped(self):
        assert get_keywords("the product is good and the product is fast") == [
            "product", "good", "fast",
        ]

    def test_none_input_returns_placeholder(self):
        assert get_keywords(None) == ["No keywords found"]

    def test_empty_string_returns_placeholder(self):
        assert get_keywords("") == ["No keywords found"]

    def test_stopwords_only_returns_placeholder(self):
        assert get_keywords("the a an is and or") == ["No keywords found"]

    def test_symbols_only_returns_placeholder(self):
        assert get_keywords("!!! ??? ...") == ["No keywords found"]

    def test_html_tags_are_stripped_to_words_not_escaped(self):
        # Demonstrates the raw words survive; nothing here HTML-escapes them,
        # which matters because the frontend later injects results via
        # innerHTML (see backend/tests + frontend finding in the QA report).
        result = get_keywords("<img src=x onerror=alert(1)>")
        assert "img" in result
        assert "onerror" in result
        assert "alert" in result

    def test_numbers_are_kept_as_keywords(self):
        assert get_keywords("order 12345 shipped") == ["order", "12345", "shipped"]


# ---------------------------------------------------------------------------
# Unit tests: summarizer
# ---------------------------------------------------------------------------

class TestSummarizer:

    def test_empty_text(self):
        assert summarize("") == "No text provided"

    def test_none_text(self):
        assert summarize(None) == "No text provided"

    def test_single_sentence_returns_as_is_with_period(self):
        assert summarize("this is one sentence") == "this is one sentence."

    def test_multi_sentence_returns_period_joined_summary(self):
        text = (
            "Sales grew fast this quarter. Customers were happy overall. "
            "Support tickets dropped a lot. The team shipped three features. "
            "Revenue is at an all time high."
        )
        result = summarize(text)
        assert result.endswith(".")
        # summary_length for 5 sentences (<=6) is 3
        assert result.count(".") <= 3 or result.count(". ") <= 2

    def test_only_symbols_falls_back_to_no_text_provided(self):
        # preprocess() strips everything down to "" for pure symbol input,
        # even though the *original* text was non-empty -- an inconsistency
        # between what "empty" means for validation vs. summarization.
        assert summarize("!!! ??? ,,,") == "No text provided"

    def test_does_not_crash_on_very_long_text(self):
        text = ". ".join(f"Sentence number {i} is here" for i in range(500))
        result = summarize(text)
        assert isinstance(result, str) and result.endswith(".")


# ---------------------------------------------------------------------------
# HTTP contract tests: POST /nlp/analyze
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from teamB.api.main import app
    return TestClient(app)


class TestNlpApiContract:

    def test_normal_request(self, client):
        r = client.post("/nlp/analyze", json={"text": "This product is great"})
        assert r.status_code == 200
        body = r.json()
        assert set(body.keys()) == {"sentiment", "summary", "keywords"}
        assert body["sentiment"] == "positive"

    def test_missing_text_field_does_not_500(self, client):
        # `data.get("text", "")` in main.py defends against this -- confirm it.
        r = client.post("/nlp/analyze", json={})
        assert r.status_code == 200
        assert r.json()["sentiment"] == "neutral"

    def test_non_dict_body_returns_422(self, client):
        r = client.post("/nlp/analyze", json="just a string")
        assert r.status_code == 422

    def test_text_field_wrong_type_is_handled_or_fails_cleanly(self, client):
        # `text` as a list: `.get("text", "")` returns the list itself, which
        # is then passed into str.lower()-based preprocessing downstream.
        r = client.post("/nlp/analyze", json={"text": ["a", "b"]})
        assert r.status_code == 200
        # Must not silently corrupt the API contract even on bad input shape.
        assert "sentiment" in r.json()

    def test_response_never_exposes_internal_error_text(self, client):
        r = client.post("/nlp/analyze", json={"text": None})
        assert r.status_code == 200
        body = r.json()
        assert body["sentiment"] in {"neutral", "positive", "negative", "mixed"}

    def test_payload_under_the_size_cap_is_accepted(self, client):
        big_text = "great product " * 50000  # ~700KB, cap is 2MB
        r = client.post("/nlp/analyze", json={"text": big_text})
        assert r.status_code == 200

    def test_payload_over_the_size_cap_is_rejected(self, client):
        # MaxBodySizeMiddleware in nlp/teamB/api/main.py caps requests at
        # 2MB; this used to have no limit at all.
        huge_text = "x" * (3 * 1024 * 1024)
        r = client.post("/nlp/analyze", json={"text": huge_text})
        assert r.status_code == 413
