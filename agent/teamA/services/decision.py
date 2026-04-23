from __future__ import annotations

import re
from typing import Iterable

from ..config import ROUTING_KEYWORDS, ROUTING_PHRASES

NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9\s]+")
SPACE_PATTERN = re.compile(r"\s+")


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


MODULE_PRIORITY = {module: index for index, module in enumerate(ROUTING_KEYWORDS)}


def decide_modules(query: str) -> list[str]:
    normalized_query = normalize_query(query)
    if not normalized_query:
        return ["nlp"]

    tokens = set(normalized_query.split())
    scores: dict[str, int] = {}

    for module in ROUTING_KEYWORDS:
        phrase_score = _score_phrase_matches(normalized_query, ROUTING_PHRASES.get(module, []))
        keyword_score = _score_keyword_matches(tokens, ROUTING_KEYWORDS[module])
        scores[module] = phrase_score + keyword_score

    ranked_matches = sorted(
        ((module, score) for module, score in scores.items() if score > 0),
        key=lambda item: (-item[1], MODULE_PRIORITY[item[0]]),
    )

    if not ranked_matches:
        return ["nlp"]

    return [module for module, _score in ranked_matches]


def decide(query: str) -> str:
    return decide_modules(query)[0]
