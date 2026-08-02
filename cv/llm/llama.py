"""
==========================================================
Llama Client (Ollama)
==========================================================

Responsibilities
----------------
• Connect to Ollama
• Send prompt to Llama
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
    Generate response using Llama.

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

        "stream": False

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