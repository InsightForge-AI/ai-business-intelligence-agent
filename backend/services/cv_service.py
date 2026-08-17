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

        # A dict (not a raised exception) so aggregation_service.py can
        # attribute this failure to "cv" specifically -- an exception
        # propagated through asyncio.gather(return_exceptions=True) loses
        # which module it came from and gets logged as "unknown".
        return {

            "module": "cv",

            "success": False,

            "message": f"CV API Error: {exc.response.status_code}"

        }

    except httpx.RequestError:

        logger.exception(

            "Unable to connect to CV Service."

        )

        return {

            "module": "cv",

            "success": False,

            "message": "CV Service is unavailable."

        }