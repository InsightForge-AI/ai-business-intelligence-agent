from __future__ import annotations

import re
from typing import Iterable

from ..config import ROUTING_KEYWORDS, ROUTING_PHRASES
from .llm_router import refine_module_decision

NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9\s]+")
SPACE_PATTERN = re.compile(r"\s+")
CONNECTOR_PATTERN = re.compile(r"\balong with\b")
PHRASE_MATCH_SCORE = 3


def normalize_query(query: str | None) -> str:
    """Lowercase text and neutralize noisy punctuation safely."""
    text = "" if query is None else str(query)
    text = text.lower().strip()
    text = CONNECTOR_PATTERN.sub(" with ", text)
    text = NON_ALNUM_PATTERN.sub(" ", text)
    return SPACE_PATTERN.sub(" ", text).strip()


def _score_phrase_matches(normalized_query: str, phrases: Iterable[str]) -> int:
    score = 0
    for phrase in phrases:
        if phrase in normalized_query:
            score += PHRASE_MATCH_SCORE
    return score


def _score_keyword_matches(tokens: set[str], keywords: Iterable[str]) -> int:
    return sum(1 for keyword in keywords if keyword in tokens)


MODULE_PRIORITY = {module: index for index, module in enumerate(ROUTING_KEYWORDS)}


def _score_modules(normalized_query: str) -> dict[str, int]:
    tokens = set(normalized_query.split())
    scores: dict[str, int] = {}

    for module in ROUTING_KEYWORDS:
        phrase_score = _score_phrase_matches(normalized_query, ROUTING_PHRASES.get(module, []))
        keyword_score = _score_keyword_matches(tokens, ROUTING_KEYWORDS[module])
        scores[module] = phrase_score + keyword_score
    return scores


def _rank_modules_by_score(scores: dict[str, int]) -> list[str]:
    ranked_matches = sorted(
        ((module, score) for module, score in scores.items() if score > 0),
        key=lambda item: (-item[1], MODULE_PRIORITY[item[0]]),
    )
    return [module for module, _score in ranked_matches]


def decide_modules(query: str) -> list[str]:
    normalized_query = normalize_query(query)
    if not normalized_query:
        return ["nlp"]

    scores = _score_modules(normalized_query)
    ranked_modules = _rank_modules_by_score(scores)
    if not ranked_modules:
        return ["nlp"]

    rule_modules = [
    module
    for module in ROUTING_KEYWORDS
    if module in ranked_modules
    ]

    # Sprint 4 intelligent refinement using LLaMA3
    final_modules = refine_module_decision(
    query=query,
    detected_modules=rule_modules
    )

    return final_modules


def decide(query: str) -> str:
    normalized_query = normalize_query(query)
    if not normalized_query:
        return "nlp"

    ranked_modules = _rank_modules_by_score(_score_modules(normalized_query))
    if not ranked_modules:
        return "nlp"

    return ranked_modules[0]
