"""
==========================================================
RAG Service
==========================================================

Backend client for the Retrieval-Augmented Generation Service.
"""

import httpx

from config.endpoints import RAG_API
from utils.logger import logger


async def run_rag(
    query: str,
    content,
    metadata: dict
) -> dict:
    """
    Call RAG Service.
    """

    # -----------------------------------------------------
    # Convert extracted content into plain text
    # -----------------------------------------------------

    if isinstance(content, dict):

        if "text" in content:

            rag_content = content["text"]

        elif "content" in content:

            rag_content = content["content"]

        else:

            rag_content = str(content)

    else:

        rag_content = str(content)

    payload = {

        "query": query,

        "content": rag_content,

        "metadata": metadata

    }

    logger.info(

        "Calling RAG Service..."

    )

    try:

        async with httpx.AsyncClient(

            timeout=300

        ) as client:

            response = await client.post(

                f"{RAG_API}/rag/analyze",

                json=payload

            )

        response.raise_for_status()

        logger.info(

            "RAG Service completed successfully."

        )

        return response.json()

    except httpx.HTTPStatusError as exc:

        logger.exception(

            "RAG Service returned an error."

        )

        return {

            "module": "rag",

            "success": False,

            "message": f"RAG API Error: {exc.response.status_code}"

        }

    except httpx.RequestError:

        logger.exception(

            "Unable to connect to RAG Service."

        )

        return {

            "module": "rag",

            "success": False,

            "message": "RAG Service is unavailable."

        }