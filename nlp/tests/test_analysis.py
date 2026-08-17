"""
Tests for the NLP service's deterministic analysis modules (sentiment,
keyword extraction, entity extraction, preprocessing). These test files
were previously empty stubs (0 bytes) -- this is the first real
coverage for this module.

Mistral/LLM-backed pieces (llm/*) are not covered here since no Ollama
runtime is available in this environment.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # nlp/

from analysis.sentiment import analyze_sentiment
from analysis.keywords import extract_keywords
from analysis.ner import extract_entities
from analysis.preprocessing import preprocess_text


class TestSentiment:

    def test_positive_text(self):
        assert analyze_sentiment("Strong growth and improved profit this quarter") == "Positive"

    def test_negative_text(self):
        assert analyze_sentiment("Significant loss and declining revenue, a major risk") == "Negative"

    def test_neutral_when_no_signal_words(self):
        assert analyze_sentiment("The meeting is scheduled for Tuesday") == "Neutral"

    def test_neutral_when_balanced(self):
        assert analyze_sentiment("good decline") == "Neutral"

    def test_empty_text_is_neutral(self):
        assert analyze_sentiment("") == "Neutral"

    def test_none_is_neutral(self):
        assert analyze_sentiment(None) == "Neutral"

    def test_case_insensitive(self):
        assert analyze_sentiment("EXCELLENT GROWTH AND PROFIT") == "Positive"

    def test_word_boundaries_prevent_substring_false_positives(self):
        # "cost" is a negative word; "costume" must not trigger it.
        assert analyze_sentiment("The costume department bought new costumes") == "Neutral"


class TestKeywordExtraction:

    def test_extracts_frequent_words(self):
        text = "revenue revenue revenue customer growth strategy"
        keywords = extract_keywords(text, max_keywords=3)
        assert "Revenue" in keywords

    def test_stop_words_excluded(self):
        text = "the a an is this that report"
        keywords = extract_keywords(text)
        assert keywords == []

    def test_generic_business_words_excluded(self):
        text = "company business document report analysis"
        keywords = extract_keywords(text)
        assert keywords == []

    def test_empty_text_returns_empty_list(self):
        assert extract_keywords("") == []
        assert extract_keywords(None) == []

    def test_multi_word_phrases_prioritized(self):
        text = "Southeast Asia is a growing market. Southeast Asia leads."
        keywords = extract_keywords(text, max_keywords=5)
        assert "Southeast Asia" in keywords

    def test_respects_max_keywords_limit(self):
        text = " ".join(f"word{i} word{i}" for i in range(20))
        keywords = extract_keywords(text, max_keywords=4)
        assert len(keywords) <= 4


class TestEntityExtraction:

    def test_extracts_years(self):
        entities = extract_entities("Revenue grew from 2022 to 2023")
        assert "2022" in entities
        assert "2023" in entities

    def test_extracts_percentages(self):
        entities = extract_entities("Growth of 12.5% was recorded")
        assert "12.5%" in entities

    def test_extracts_monetary_values(self):
        entities = extract_entities("Revenue reached $5 million this year")
        assert any("$5" in e for e in entities)

    def test_extracts_proper_nouns(self):
        entities = extract_entities("Acme Corporation reported strong results")
        assert "Acme Corporation" in entities

    def test_common_determiners_are_filtered(self):
        entities = extract_entities("The report shows growth")
        assert "The" not in entities

    def test_duplicates_removed(self):
        entities = extract_entities("2023 2023 2023")
        assert entities.count("2023") == 1

    def test_empty_text_returns_empty_list(self):
        assert extract_entities("") == []

    def test_respects_max_entities_limit(self):
        text = " ".join(str(y) for y in range(2000, 2015))  # 15 distinct years
        entities = extract_entities(text, max_entities=5)
        assert len(entities) <= 5


class TestPreprocessing:

    def test_collapses_newlines_and_whitespace_to_single_spaces(self):
        # The final whitespace-normalization pass (`\s+` -> " ") also
        # matches newlines, so the earlier "collapse multiple newlines"
        # step never actually surfaces in the output -- everything ends
        # up on one space-joined line either way.
        assert preprocess_text("line1\n\n\nline2") == "line1 line2"

    def test_replaces_tabs_with_spaces(self):
        assert "\t" not in preprocess_text("a\tb")

    def test_normalizes_multiple_spaces(self):
        assert preprocess_text("a    b     c") == "a b c"

    def test_strips_leading_trailing_whitespace(self):
        assert preprocess_text("   hello   ") == "hello"

    def test_empty_text_returns_empty_string(self):
        assert preprocess_text("") == ""
        assert preprocess_text(None) == ""
