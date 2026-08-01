"""
==========================================================
Phi-3 Client (Ollama)
==========================================================

Responsibilities
----------------
• Connect to Ollama
• Send prompt to Phi-3
• Return generated response
"""

import httpx

from utils.constants import (
    MODEL_NAME,
    OLLAMA_URL,
    DEFAULT_TIMEOUT
)


async def generate(
    prompt: str
) -> str:
    """
    Generate response using Phi-3.

    Parameters
    ----------
    prompt : str

    Returns
    -------
    str
    """

    payload = {

        "model": MODEL_NAME,

        "prompt": prompt,

        "stream": False,

        "format": "json",

        "options": {

            "temperature": 0,

            "top_p": 0.1,

            "num_predict": 128

        }

    }

    async with httpx.AsyncClient(

        timeout=DEFAULT_TIMEOUT

    ) as client:

        response = await client.post(

            OLLAMA_URL,

            json=payload

        )

    response.raise_for_status()

    result = response.json()

    return result.get(

        "response",

        ""

    )