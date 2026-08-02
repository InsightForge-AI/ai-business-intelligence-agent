"""
==========================================================
RAG Service
==========================================================

Responsibilities
----------------
• Execute complete RAG pipeline
• Retrieve relevant document chunks
• Re-rank retrieved chunks
• Generate grounded answer using Qwen
• Return standardized response
"""

from analysis.chunker import chunk_document
from analysis.embeddings import generate_embeddings
from analysis.vector_store import build_index
from analysis.retriever import retrieve_chunks
from analysis.reranker import rerank_chunks
from analysis.formatter import format_context

from llm.llm_service import generate_answer

from models.response import RAGResponse


async def run_analysis(
    query: str,
    content: str,
    metadata: dict
) -> RAGResponse:
    """
    Execute complete Retrieval-Augmented Generation pipeline.
    """

    # -----------------------------------------------------
    # Validate Content
    # -----------------------------------------------------

    if not content or not str(content).strip():

        return RAGResponse(

            module="rag",

            success=False,

            answer="Document content is empty.",

            sources=[],

            confidence=0.0,

            message="No content available."

        )

    # -----------------------------------------------------
    # Chunk Document
    # -----------------------------------------------------

    chunks = chunk_document(

        content

    )

    if not chunks:

        return RAGResponse(

            module="rag",

            success=False,

            answer="No content available for retrieval.",

            sources=[],

            confidence=0.0,

            message="Unable to create document chunks."

        )

    # -----------------------------------------------------
    # Generate Chunk Embeddings
    # -----------------------------------------------------

    chunk_embeddings = await generate_embeddings(

        chunks

    )

    # -----------------------------------------------------
    # Build Vector Index
    # -----------------------------------------------------

    build_index(

        chunks,

        chunk_embeddings

    )

    # -----------------------------------------------------
    # Generate Query Embedding
    # -----------------------------------------------------

    query_embedding = (

        await generate_embeddings(

            [query]

        )

    )[0]

    # -----------------------------------------------------
    # Retrieve Top Chunks
    # -----------------------------------------------------

    retrieved_chunks = retrieve_chunks(

        query_embedding=query_embedding,

        top_k=10

    )

    if not retrieved_chunks:

        return RAGResponse(

            module="rag",

            success=False,

            answer="I couldn't find any relevant information in the uploaded document.",

            sources=[],

            confidence=0.0,

            message="No relevant context found."

        )

    # -----------------------------------------------------
    # Re-rank Chunks
    # -----------------------------------------------------

    ranked_chunks = rerank_chunks(

        retrieved_chunks

    )

    if not ranked_chunks:

        return RAGResponse(

            module="rag",

            success=False,

            answer="No relevant information found after re-ranking.",

            sources=[],

            confidence=0.0,

            message="No relevant chunks available."

        )

    # -----------------------------------------------------
    # Limit Final Context
    # -----------------------------------------------------

    ranked_chunks = ranked_chunks[:5]

    # -----------------------------------------------------
    # Format Context
    # -----------------------------------------------------

    context = format_context(

        ranked_chunks

    )

    # -----------------------------------------------------
    # Build LLM Context
    # -----------------------------------------------------

    llm_context = {

        "query": query,

        "metadata": metadata,

        "context": context

    }

    # -----------------------------------------------------
    # Generate Answer
    # -----------------------------------------------------

    llm = await generate_answer(

        llm_context

    )

    # -----------------------------------------------------
    # Build Sources
    # -----------------------------------------------------

    sources = []

    for index, chunk in enumerate(ranked_chunks, start=1):

        if isinstance(chunk, dict):

            sources.append({

                "chunk": chunk.get(

                    "chunk_id",

                    index

                ),

                "page": chunk.get(

                    "page",

                    1

                )

            })

        else:

            sources.append({

                "chunk": index,

                "page": 1

            })

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    try:

        confidence = float(

            llm.get(

                "confidence",

                0.90

            )

        )

    except Exception:

        confidence = 0.90

    confidence = max(

        0.0,

        min(

            confidence,

            1.0

        )

    )

    # -----------------------------------------------------
    # Final Response
    # -----------------------------------------------------

    return RAGResponse(

        module="rag",

        success=True,

        answer=llm.get(

            "answer",

            "I could not find the requested information in the document."

        ),

        sources=sources,

        confidence=confidence,

        message="Question answered successfully."

    )