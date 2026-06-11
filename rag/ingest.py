import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
"all-MiniLM-L6-v2"
)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def chunk_document(document_text: str,
                   chunk_size: int = CHUNK_SIZE,
                   overlap: int = CHUNK_OVERLAP):

    if not document_text or not document_text.strip():
        return []

    chunks = []
    start = 0

    while start < len(document_text):
        end = start + chunk_size
        chunks.append(document_text[start:end])
        start += (chunk_size - overlap)

    return chunks

def generate_embeddings(chunks):
    embeddings = embedding_model.encode(
    chunks,
    convert_to_numpy=True
)
    return embeddings.astype(
    np.float32
)

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def build_document_index(document_text: str):
    chunks = chunk_document(document_text)
    if not chunks:
        raise ValueError("Document is empty or no chunks were generated.")
    embeddings = generate_embeddings(chunks)
    index = create_faiss_index(embeddings)
    return index, chunks
if __name__ == "__main__":
    sample_document = """
Customers may request refunds within
7 days of purchase.

Refunds require proof of purchase.

Premium customers receive
priority support.
"""

index, chunks = build_document_index(
    sample_document
)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:")
print(chunks[0])

print("\nFAISS Vectors:")
print(index.ntotal)