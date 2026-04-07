from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

# ─── PATHS ────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH     = os.path.join(BASE_DIR, "data", "raw", "document.json")
CLEANED_DIR  = os.path.join(BASE_DIR, "data", "cleaned")
CLEANED_PATH = os.path.join(CLEANED_DIR, "pipeline_results.json")

# ─── Load documents ───────────────────────────────────────────
with open(RAW_PATH, "r") as f:
    documents = json.load(f)

# ─── Build FAISS index ────────────────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2", cache_folder="./model_cache")
contents = [doc["content"] for doc in documents]
embeddings = model.encode(contents)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# ─── Search Function ──────────────────────────────────────────
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
            "score": float(round(1 / (1 + distances[0][i]), 4))  # ← FIXED ✅
        })
    return results

# ─── Save Output to data/cleaned/ ─────────────────────────────
if __name__ == "__main__":
    os.makedirs(CLEANED_DIR, exist_ok=True)

    test_query = "delivery issues"
    results = search_pipeline(test_query)

    output = {
        "query": test_query,
        "total_results": len(results),
        "results": results
    }

    with open(CLEANED_PATH, "w") as f:
        json.dump(output, f, indent=4)

    print(f" Pipeline results saved to: {CLEANED_PATH}")