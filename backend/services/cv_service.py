"""
==========================================================
CV Service
==========================================================

Backend client for the Computer Vision Service.

Responsibilities
----------------
• Call CV API
• Return CV analysis
"""

import httpx

from config.endpoints import CV_API
from utils.logger import logger


async def run_cv(
    query: str,
    content,
    metadata: dict
) -> dict:
    """
    Call CV Service.

    Parameters
    ----------
    query : str

    content

    metadata : dict

    Returns
    -------
    dict
    """

    payload = {

        "query": query,

        "content": content,

        "metadata": metadata

    }

    logger.info(

        "Calling CV Service..."

    )

    try:

        async with httpx.AsyncClient(

            timeout=300

        ) as client:

            response = await client.post(

                f"{CV_API}/cv/analyze",

                json=payload

            )

        response.raise_for_status()

        logger.info(

            "CV Service completed successfully."

        )

        return response.json()

    except httpx.HTTPStatusError as exc:

        logger.exception(

            "CV Service returned an error."

        )

        raise RuntimeError(

            f"CV API Error: {exc.response.status_code}"

        ) from exc

    except httpx.RequestError as exc:

        logger.exception(

            "Unable to connect to CV Service."

        )

        raise RuntimeError(

            "CV Service is unavailable."

        ) from exc