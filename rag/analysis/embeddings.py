"""
==========================================================
Embeddings
==========================================================

Responsibilities
----------------
• Generate embeddings using Ollama
• Support dictionary-based chunks
• Handle errors gracefully
"""

import httpx

OLLAMA_EMBED_URL = "http://127.0.0.1:11434/api/embed"

MODEL_NAME = "nomic-embed-text:latest"


async def generate_embeddings(
    chunks: list
) -> list[list[float]]:
    """
    Generate semantic embeddings using Ollama.

    Parameters
    ----------
    chunks : list
        List of strings or chunk dictionaries.

    Returns
    -------
    list[list[float]]
    """

    if not chunks:

        return []

    embeddings = []

    async with httpx.AsyncClient(

        timeout=300

    ) as client:

        for chunk in chunks:

            # ---------------------------------------------
            # Support dict-based chunks
            # ---------------------------------------------

            if isinstance(

                chunk,

                dict

            ):

                text = chunk.get(

                    "text",

                    ""

                )

            else:

                text = str(chunk)

            if not text.strip():

                continue

            try:

                response = await client.post(

                    OLLAMA_EMBED_URL,

                    json={

                        "model": MODEL_NAME,

                        "input": text

                    }

                )

                response.raise_for_status()

                result = response.json()

                embedding = result.get(

                    "embeddings",

                    [[]]

                )[0]

                embeddings.append(

                    embedding

                )

            except Exception:

                # Keep pipeline running
                embeddings.append([])

    return embeddings