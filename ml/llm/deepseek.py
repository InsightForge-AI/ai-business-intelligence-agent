"""
==========================================================
DeepSeek Client (Ollama)
==========================================================

Author:
    AI Business Intelligence Agent

Purpose
-------
Communicate with the Ollama server and generate
responses using DeepSeek-R1.

Responsibilities
----------------
• Build request payload
• Send request to Ollama
• Retry transient failures
• Validate response
• Return generated text
"""

from __future__ import annotations

import asyncio
import logging

import httpx

from utils.constants import (
    MODEL_NAME,
    OLLAMA_URL,
    DEFAULT_TIMEOUT,
)

logger = logging.getLogger(__name__)

# ==========================================================
# Configuration
# ==========================================================

MAX_RETRIES = 2

TEMPERATURE = 0.0

TOP_P = 0.9

REPEAT_PENALTY = 1.1

NUM_CTX = 8192


# ==========================================================
# Payload Builder
# ==========================================================

def build_payload(prompt: str) -> dict:
    """
    Build Ollama request payload.
    """

    return {

        "model": MODEL_NAME,

        "prompt": prompt,

        "format": "json",

        "stream": False,

        "options": {

            "temperature": TEMPERATURE,

            "top_p": TOP_P,

            "repeat_penalty": REPEAT_PENALTY,

            "num_ctx": NUM_CTX,

        },

    }


# ==========================================================
# Validate Response
# ==========================================================

def validate_response(result: dict) -> str:
    """
    Validate Ollama response.
    """

    if not isinstance(result, dict):

        raise RuntimeError(
            "Invalid response returned by Ollama."
        )

    if result.get("error"):

        raise RuntimeError(
            result["error"]
        )

    response = result.get("response")

    if not isinstance(response, str):

        raise RuntimeError(
            "Ollama returned an invalid response."
        )

    response = response.strip()

    if not response:

        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return response


# ==========================================================
# Generate
# ==========================================================

async def generate(
    prompt: str
) -> str:
    """
    Generate a response using DeepSeek-R1.
    """

    payload = build_payload(prompt)

    timeout = httpx.Timeout(DEFAULT_TIMEOUT)

    last_error = None

    for attempt in range(MAX_RETRIES + 1):

        try:

            async with httpx.AsyncClient(
                timeout=timeout
            ) as client:

                response = await client.post(
                    OLLAMA_URL,
                    json=payload
                )

            response.raise_for_status()

            result = response.json()

            return validate_response(result)

        except (
            httpx.RequestError,
            httpx.HTTPStatusError,
        ) as exc:

            last_error = exc

            logger.warning(

                "DeepSeek request failed "
                "(attempt %d/%d): %s",

                attempt + 1,

                MAX_RETRIES + 1,

                exc,

            )

            if attempt < MAX_RETRIES:

                await asyncio.sleep(1)

        except Exception:

            logger.exception(
                "Unexpected DeepSeek error."
            )

            raise

    raise RuntimeError(

        f"DeepSeek request failed after "
        f"{MAX_RETRIES + 1} attempts."

    ) from last_error


# ==========================================================
# Public API
# ==========================================================

__all__ = [

    "generate",

    "MODEL_NAME",

]