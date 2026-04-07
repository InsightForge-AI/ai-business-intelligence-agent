from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# Load documents from JSON file
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned", "document_cleaned.json")
with open(file_path, "r", encoding="utf-8") as f:
    documents = json.load(f)

# Load model and encode documents
model = SentenceTransformer("all-MiniLM-L6-v2")
contents = [doc["content"] for doc in documents]
embeddings = model.encode(contents)
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
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

if __name__ == "__main__":
    results = search_pipeline("sales report")
    for r in results:
        print(r["title"], "->", r["category"], "| score:", r["score"])