from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import importlib.util

spec = importlib.util.spec_from_file_location("document", "../data/document.py")
doc_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doc_module)
documents = doc_module.documents

model = SentenceTransformer("all-MiniLM-L6-v2")
contents = [doc["content"] for doc in documents]
embeddings = model.encode(contents)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

def search_pipeline(query: str, top_k: int = 3):
    query_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        doc = documents[idx]
        results.append({
            "title": doc["title"],
            "category": doc["category"],
            "content": doc["content"],
            "score": round(1 / (1 + distances[0][i]), 4)
        })
    return results