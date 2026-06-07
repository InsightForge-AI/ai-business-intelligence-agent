"""
router.py
--------
The Agent "brain" that integrates every layer into one decision.

Pipeline (LLM-first with rule-based fallback, as required):

    question + file
        |
        v
   [M3] read metadata  --------------------------------+
        |                                               |
        v                                               |
   [M4] try LLM routing                                 |
        |                                               |
   valid? --yes--> [M5] normalize + validate --> return |
        |                                               |
        no / unavailable / error                        |
        |                                               |
        v                                               |
   [M2] rule-based fallback <---------------------------+
        |
        v
   [M5] final validate (hard default if ever invalid) --> return

Integration owners: Member 2 (rules) + Member 3 (metadata) + Member 4 (LLM)
"""

from fallback.fallback_router import fallback_route
from fallback.response_validator import normalize_response
from llm.llm_router import route_by_llm
from metadata.metadata_reader import read_metadata
from utils.helpers import get_logger
from validator import validate_response

logger = get_logger("agent.router")


def rule_based_routing(question: str, file_type: str = None) -> dict:
    """Member 2 contribution: pure rule-based routing entry point."""
    return fallback_route(question, file_type)


def analyze(question: str, filename: str = None, file_path: str = None) -> dict:
    """
    Run the full routing pipeline and return a canonical response:
        {"modules": [...], "confidence": float, "reason": str}
    """
    # ---- [M3] Metadata ------------------------------------------------- #
    metadata = read_metadata(filename=filename, file_path=file_path)
    file_type = metadata.get("extension") or None

    # ---- [M4] LLM routing (best effort) -------------------------------- #
    llm_result = route_by_llm(question, metadata)
    if llm_result is not None:
        normalized = normalize_response(llm_result)
        if normalized and validate_response(normalized):
            logger.info("Routed via LLM: %s", normalized["modules"])
            return normalized
        logger.info("LLM result invalid after normalization; falling back.")

    # ---- [M2] Rule-based fallback -------------------------------------- #
    result = fallback_route(question, file_type)

    # ---- [M5] Final safety gate ---------------------------------------- #
    if not validate_response(result):
        logger.error("Fallback produced invalid result; using hard default.")
        result = {
            "modules": ["nlp"],
            "confidence": 0.5,
            "reason": "Hard default (validation failed).",
        }

    logger.info("Routed via rules: %s", result["modules"])
    return result