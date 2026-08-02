"""
==========================================================
Qwen Client (Ollama)
==========================================================

Responsibilities
----------------
• Connect to Ollama
• Send prompt to Qwen
• Handle retries
• Handle errors
• Return generated response
"""

import asyncio

import httpx

from utils.constants import (
    MODEL_NAME,
    OLLAMA_URL,
    DEFAULT_TIMEOUT
)

from utils.logger import logger


MAX_RETRIES = 3


async def generate(
    prompt: str
) -> str:
    """
    Generate response using Qwen.

    Parameters
    ----------
    prompt : str

    Returns
    -------
    str
    """

    if not prompt or not prompt.strip():

        logger.warning(

            "Empty prompt received."

        )

        return ""

    payload = {

        "model": MODEL_NAME,

        "prompt": prompt,

        "stream": False

    }

    for attempt in range(

        1,

        MAX_RETRIES + 1

    ):

        try:

            logger.info(

                f"Calling Qwen (Attempt {attempt})..."

            )

            async with httpx.AsyncClient(

                timeout=DEFAULT_TIMEOUT

            ) as client:

                response = await client.post(

                    OLLAMA_URL,

                    json=payload

                )

            response.raise_for_status()

            result = response.json()

            answer = result.get(

                "response",

                ""

            )

            if not answer.strip():

                logger.warning(

                    "Qwen returned an empty response."

                )

                return ""

            logger.info(

                "Qwen response generated successfully."

            )

            return answer

        except httpx.TimeoutException:

            logger.warning(

                f"Qwen timeout (Attempt {attempt})"

            )

        except httpx.RequestError as exc:

            logger.warning(

                f"Unable to connect to Ollama (Attempt {attempt}): {exc}"

            )

        except Exception as exc:

            logger.exception(

                f"Unexpected Qwen error: {exc}"

            )

            break

        await asyncio.sleep(1)

    logger.error(

        "Failed to generate response after multiple attempts."

    )

    return ""