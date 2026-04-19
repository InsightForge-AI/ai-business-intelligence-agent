from __future__ import annotations

import re
from typing import Iterable

from ..config import ROUTING_KEYWORDS, ROUTING_PHRASES

NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9\s]+")
SPACE_PATTERN = re.compile(r"\s+")
MULTI_INTENT_CONNECTORS = {"and", "plus", "with", "along", "also"}


def normalize_query(query: str | None) -> str:
    """Lowercase text and neutralize noisy punctuation safely."""
    text = "" if query is None else str(query)
    text = text.lower().strip()
    text = NON_ALNUM_PATTERN.sub(" ", text)
    return SPACE_PATTERN.sub(" ", text).strip()


def _score_phrase_matches(normalized_query: str, phrases: Iterable[str]) -> int:
    score = 0
    for phrase in phrases:
        if phrase in normalized_query:
            score += 3
    return score


def _score_keyword_matches(tokens: set[str], keywords: Iterable[str]) -> int:
    return sum(1 for keyword in keywords if keyword in tokens)


def decide(query: str) -> str:
    normalized_query = normalize_query(query)
    if not normalized_query:
        return "nlp"

    ordered_tokens = normalized_query.split()
    tokens = set(ordered_tokens)
    scores: dict[str, int] = {}

    for module in ROUTING_KEYWORDS:
        phrase_score = _score_phrase_matches(normalized_query, ROUTING_PHRASES.get(module, []))
        keyword_score = _score_keyword_matches(tokens, ROUTING_KEYWORDS[module])
        scores[module] = phrase_score + keyword_score

    ranked_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    top_module, top_score = ranked_scores[0]
    second_score = ranked_scores[1][1] if len(ranked_scores) > 1 else 0
    matched_modules = [module for module, score in scores.items() if score > 0]

    if top_score <= 0:
        return "nlp"

    if len(matched_modules) > 1 and any(token in MULTI_INTENT_CONNECTORS for token in ordered_tokens):
        return "nlp"

    if second_score == 0:
        return top_module

    # Safe Sprint 3 fallback: close scores mean the intent is ambiguous.
    if top_score - second_score <= 1:
        return "nlp"

    return top_module
