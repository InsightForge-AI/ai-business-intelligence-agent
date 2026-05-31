import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)

# ----------------------------------
# EMBEDDING MODEL
# ----------------------------------

embedding_model = (
    SentenceTransformer(
        "all-MiniLM-L6-v2"
    )
)

# ----------------------------------
# CHUNK CONFIG
# ----------------------------------

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


# ----------------------------------
# DOCUMENT CHUNKING
# ----------------------------------

def chunk_document(
    document_text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
):
    """
    Split document into overlapping chunks.
    """

    if not document_text:
        return []

    chunks = []

    start = 0

    while start < len(document_text):

        end = start + chunk_size

        chunk = (
            document_text[start:end]
        )

        chunks.append(
            chunk
        )

        start += (
            chunk_size - overlap
        )

    return chunks


# ----------------------------------
# EMBEDDINGS
# ----------------------------------

def generate_embeddings(
    chunks
):
    """
    Generate embeddings for chunks.
    """

    embeddings = (
        embedding_model.encode(
            chunks,
            convert_to_numpy=True
        )
    )

    return embeddings.astype(
        np.float32
    )


# ----------------------------------
# BUILD FAISS INDEX
# ----------------------------------

def create_faiss_index(
    embeddings
):
    """
    Create FAISS vector index.
    """

    dimension = (
        embeddings.shape[1]
    )

    index = (
        faiss.IndexFlatL2(
            dimension
        )
    )

    index.add(
        embeddings
    )

    return index


# ----------------------------------
# MAIN INGEST PIPELINE
# ----------------------------------

def build_document_index(
    document_text: str
):
    """
    Full ingestion pipeline.

    Returns:
        index
        chunks
    """

    chunks = chunk_document(
        document_text
    )

    if len(chunks) == 0:

        raise ValueError(
            "No chunks generated"
        )

    embeddings = (
        generate_embeddings(
            chunks
        )
    )

    index = (
        create_faiss_index(
            embeddings
        )
    )

    return index, chunks


# if __name__ == "__main__":

#     sample_document = """
#     Customers may request refunds
#     within 7 days of purchase.

#     Refunds require proof of purchase.
#     """

#     index, chunks = build_document_index(
#         sample_document
#     )

#     print("Chunks Created:")
#     print(len(chunks))

#     print("\nFirst Chunk:")
#     print(chunks[0])

#     print("\nFAISS Index Size:")
#     print(index.ntotal)